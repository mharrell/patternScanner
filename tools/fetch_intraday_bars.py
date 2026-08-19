"""Fetch and accumulate 1-minute OHLCV bars (intraday track, v1).

Design contract (frozen 2026-08-18; see data/intraday/README.md):

  * Append-only, immutable archive: one parquet per (bar-date, ticker) at
    data/intraday/raw/<YYYY-MM-DD>/<TICKER>.parquet, written ONCE by the
    first pull that sees the bar-date complete; never modified afterwards.
  * Atomic writes: temp file -> fsync -> os.replace, so a crash mid-write
    can never leave a partial file as the visible state.
  * Manifest of evidence: data/intraday/manifest.json records SHA-256, row
    count and span for every file ever written. Every run re-verifies ALL
    recorded files (plus an orphan walk over raw/) BEFORE writing anything;
    a missing or corrupt file aborts the pull with a loud error and is
    NEVER silently regenerated. The only way to remove a file is the
    explicit --repair mode, which records the deletion first.
  * A bar-date is written only after its session has fully closed: date D
    is complete iff D < today(ET), or D == today(ET) and now(ET) >= 20:01
    (regular + extended hours 04:00-20:00 ET included). No partial days.
  * Timestamps: tz-aware America/New_York, floored to the minute. A naive
    timestamp is an ERROR (schema rule, enforced at load by
    tools/qa_intraday.py).
  * Universe: the full membership list is pulled blindly every run (no
    cherry-picking); the universe file and its SHA-256 are recorded in the
    pull record — the anti-survivorship-bias discipline (pre-reg #15 §5
    design note in data/intraday/README.md).
  * Unadjusted OHLCV; split events are recorded in data/intraday/splits.json
    and never folded into stored data. Renormalization is a measurement-time
    concern and NEVER rewrites stored files.
  * Yahoo driver: rolling 7-day 1m window (Yahoo's hard cap), extended hours
    included, curl_cffi TLS impersonation via yfinance, polite retries with
    backoff. A failed ticker is recorded in the pull record and retried next
    run; it never aborts the batch.

Outputs:
  data/intraday/raw/<date>/<ticker>.parquet   — immutable day bars (LFS-tracked)
  data/intraday/manifest.json                 — cumulative SHA-256 ledger (tracked)
  data/intraday/repairs.json                  — deliberate deletions (tracked)
  data/intraday/splits.json                   — recorded split events (tracked)

Usage (nightly; Task Scheduler entry in data/intraday/README.md):
  python -X utf8 tools/fetch_intraday_bars.py              # full pull
  python -X utf8 tools/fetch_intraday_bars.py --limit 5    # first N (test)
  python -X utf8 tools/fetch_intraday_bars.py --qa         # pull, then QA
  python -X utf8 tools/fetch_intraday_bars.py --repair "2026-08-18/AAP.parquet" \
      --reason "documented restatement fix"
  python -X utf8 tools/fetch_intraday_bars.py --adopt "2026-08-18/AAP.parquet" \
      --reason "crashed-pull file, hash-verified"

The only sanctioned deletion is --repair (recorded first). Crashed-pull
orphans — valid files the manifest never recorded — are recovered with
--adopt (hash + schema-check + register, kept) or --repair (delete with a
record; the next pull re-fetches while the window lasts).
"""
import argparse
import hashlib
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INTRA = ROOT / "data" / "intraday"
RAW_DIR = INTRA / "raw"
MANIFEST_PATH = INTRA / "manifest.json"
REPAIRS_PATH = INTRA / "repairs.json"
SPLITS_PATH = INTRA / "splits.json"
LOCK_PATH = INTRA / ".lock"

TZ = ZoneInfo("America/New_York")   # exchange-local; Yahoo 1m data is ET
POST_MARKET_CLOSE = dtime(20, 1)    # 04:00-20:00 ET session, 1-min grace
WINDOW = "7d"                       # Yahoo's hard cap for 1m data
COLS = ["Open", "High", "Low", "Close", "Volume"]
SCHEMA_VERSION = 1
STALE_LOCK_HOURS = 12
EXIT_OK, EXIT_TICKER_FAILURES, EXIT_ABORT = 0, 1, 2


class DataError(Exception):
    """Fatal data-integrity violation — the pull must abort."""


# ---------------------------------------------------------------------------
# Locking (concurrent runs must never interleave)
# ---------------------------------------------------------------------------

def acquire_lock() -> None:
    """Exclusive-create lock; a crash leaves it behind and the next run
    aborts with instructions rather than guessing (loud, not silent)."""
    INTRA.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOCK_PATH, "x", encoding="utf-8") as f:
            f.write(json.dumps({"pid": os.getpid(),
                                "started_utc": datetime.now(ZoneInfo("UTC")).isoformat()}))
    except FileExistsError:
        age = time.time() - LOCK_PATH.stat().st_mtime
        if age > STALE_LOCK_HOURS * 3600:
            raise DataError(f"lock is {age/3600:.1f}h old — a pull cannot "
                            f"legitimately run this long. Verify no pull is "
                            f"running, delete {LOCK_PATH}, re-run.")
        raise DataError(
            f"lock {LOCK_PATH} exists ({age/3600:.1f}h old). If no pull is "
            f"running, delete it manually and re-run — never while one is "
            f"running, or two pulls may interleave.")


def release_lock() -> None:
    try:
        LOCK_PATH.unlink()
    except FileNotFoundError:
        pass


# ---------------------------------------------------------------------------
# Atomic file I/O
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write_bytes(path: Path, data: bytes) -> None:
    """Temp file in the SAME directory (same volume) -> fsync -> replace.
    os.replace is atomic on Windows within a volume; the visible state is
    either the old file or the complete new one, never a partial write."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp-{os.getpid()}")
    try:
        with open(tmp, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass
        raise


def atomic_write_json(path: Path, obj) -> None:
    atomic_write_bytes(path, json.dumps(obj, indent=2).encode("utf-8"))


# ---------------------------------------------------------------------------
# Manifest of evidence
# ---------------------------------------------------------------------------

def empty_manifest() -> dict:
    return {"schema_version": SCHEMA_VERSION, "pulls": [], "files": {}}


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        # A fresh archive must also be empty — files without a manifest are
        # orphans and are never trusted.
        orphans = list(RAW_DIR.glob("*/*.parquet"))
        if orphans:
            raise DataError(f"no manifest but {len(orphans)} parquet files "
                            f"exist under {RAW_DIR} — refusing to build a new "
                            f"ledger over unknown files.")
        return empty_manifest()
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        raise DataError(f"manifest {MANIFEST_PATH} unreadable ({e}). Restore it "
                        f"from git before continuing — never rebuild from scratch.")
    # Pull-chain validation: each record's prev_pull_sha256 must hash the
    # preceding record (or "root" for the first). Catches hand-edited or
    # badly-merged manifests — the one silent metadata corruption path.
    pulls = manifest.get("pulls", [])
    for i, p in enumerate(pulls):
        expect = "root" if i == 0 else hashlib.sha256(
            json.dumps(pulls[i - 1], sort_keys=True).encode("utf-8")).hexdigest()
        if p.get("prev_pull_sha256") != expect:
            raise DataError(f"pull chain broken at record {i} "
                            f"({p.get('pull_id')}): prev_pull_sha256 "
                            f"{str(p.get('prev_pull_sha256'))[:12]}… != "
                            f"{expect[:12]}… — manifest was edited by hand or "
                            f"merged badly; restore it from git.")
    return manifest


def verify_manifest(manifest: dict, repairs: dict) -> tuple[int, int]:
    """Re-hash every recorded file + walk raw/ for orphans. Returns
    (checked, ok). Raises DataError on any inconsistency — nothing is
    written until this passes."""
    repaired = {r["path"] for r in repairs.get("repairs", [])}
    files = manifest.get("files", {})
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise DataError(f"manifest schema_version {manifest.get('schema_version')} "
                        f"!= {SCHEMA_VERSION} — stop and investigate.")
    checked = ok = 0
    for rel, rec in list(files.items()):
        p = RAW_DIR / rel
        if rel in repaired:
            if not p.exists():
                # Zombie state: the repair record was written and the file
                # removed, but a crash landed between the unlink and the
                # manifest rewrite. The recorded intent is documented, so we
                # complete it loudly — an entry whose file is gone must not
                # pass as "verified" in every future pull record.
                del manifest["files"][rel]
                print(f"NOTE: completing recorded repair — {rel}: manifest "
                      f"entry dropped (file already removed by a prior "
                      f"repair)", file=sys.stderr)
                continue
            # Repair recorded but the file survived (crash before the
            # unlink): hash it like any other recorded file.
        if not p.exists():
            raise DataError(f"manifest records {rel} but the file is MISSING and "
                            f"has no repair record — restore it or --repair it "
                            f"with a reason. Nothing written.")
        if p.stat().st_size == 0:
            raise DataError(f"{rel} is 0 bytes — corrupt. Restore or --repair.")
        checked += 1
        try:
            actual = sha256_file(p)
        except OSError as e:
            raise DataError(f"{rel} unreadable ({e}) — restore it or --repair "
                            f"it with a reason. Nothing written.")
        if actual == rec["sha256"]:
            ok += 1
        else:
            raise DataError(f"{rel} FAILED its SHA-256 check (recorded "
                            f"{rec['sha256'][:12]}…). Corrupt or restated — "
                            f"restore it or --repair it with a reason. "
                            f"Nothing written.")
    # Orphan walk: parquet files on disk that no manifest entry records.
    on_disk = {p.relative_to(RAW_DIR).as_posix()
               for p in RAW_DIR.glob("*/*.parquet")}
    unrecorded = on_disk - set(files) - repaired
    if unrecorded:
        shown = ", ".join(sorted(unrecorded)[:5])
        raise DataError(f"{len(unrecorded)} unrecorded parquet files under "
                        f"{RAW_DIR} (e.g. {shown}) — from a crashed run or an "
                        f"unsupervised add. They are not in the ledger, so "
                        f"they are not trusted. Crashed-pull files are valid "
                        f"data: --adopt each (hash + schema-verified, kept) "
                        f"or --repair each (delete with a reason) and the "
                        f"next pull re-writes them from the window.")
    return checked, ok


def load_repairs() -> dict:
    if not REPAIRS_PATH.exists():
        return {"repairs": []}
    try:
        return json.loads(REPAIRS_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        raise DataError(f"repairs ledger {REPAIRS_PATH} unreadable ({e}) — "
                        f"repair history is evidence; restore it from git.")


def last_pull_sha(manifest: dict) -> str:
    if not manifest["pulls"]:
        return "root"
    prev = manifest["pulls"][-1]
    return hashlib.sha256(json.dumps(prev, sort_keys=True).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Yahoo driver (vendor-agnostic seam: DRIVERS["name"] -> fetch_one)
# ---------------------------------------------------------------------------

def fetch_one_yahoo(ticker: str) -> pd.DataFrame:
    """Return normalized tz-aware ET minute bars for the rolling 7-day
    window (extended hours included), or raise ValueError('no data')."""
    import re

    import yfinance as yf

    last_err = None
    base = re.sub(r"[-.][A-Za-z]+$", "", ticker) if "-" in ticker or "." in ticker else None
    symbols = [ticker] + ([base] if base and base != ticker else [])
    for sym in symbols:
        for i in range(3):
            try:
                df = yf.download(sym, period=WINDOW, interval="1m",
                                 auto_adjust=False, prepost=True,
                                 progress=False, threads=False)
                if df is None or df.empty:
                    raise ValueError("no data")
                break
            except Exception as e:          # network error, throttle, parse
                last_err = e
                if i < 2:
                    time.sleep(1.5 * (i + 1))
                df = None
        else:
            continue                        # exhausted -> try base symbol
        if df is not None and not df.empty:
            return normalize(df, sym)
    raise ValueError(f"no data (last error: {last_err})")


def normalize(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Schema rule: tz-aware ET, minute-aligned, unique, sorted. A naive
    index is a hard error — naive timestamps must never enter the archive."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel("Ticker")
    df = df[COLS].copy()
    idx = df.index
    if idx.tz is None:
        raise DataError(f"{ticker}: driver returned NAIVE timestamps — refusing "
                        f"(tz discipline, data/intraday/README.md)")
    idx = idx.tz_convert(TZ)
    idx = idx.floor("min")
    df.index = idx
    df.index.name = "Timestamp"
    df = df[~df.index.duplicated(keep="first")].sort_index()
    return df


DRIVERS = {"yahoo": fetch_one_yahoo}


# ---------------------------------------------------------------------------
# Completeness rule
# ---------------------------------------------------------------------------

def complete_dates(now_et: datetime) -> set:
    """Bar-dates whose full 04:00-20:00 ET session has closed by now_et.
    A date is never written before it is complete (no partial days)."""
    today = now_et.date()
    cutoff = datetime.combine(today, POST_MARKET_CLOSE, tzinfo=TZ)
    span = [today - timedelta(days=i) for i in range(8)]
    return {d for d in span if d < today or now_et >= cutoff}


def split_by_date(df: pd.DataFrame, now_et: datetime) -> dict:
    """Group a fetched window by complete bar-date, sorted, deterministic."""
    # .date yields a numpy array; wrap in pd.Index for .isin
    keep = df[pd.Index(df.index.date).isin(complete_dates(now_et))]
    out = {}
    for d in sorted(set(keep.index.date)):
        out[d] = keep[keep.index.date == d]
    return out


# ---------------------------------------------------------------------------
# Pull
# ---------------------------------------------------------------------------

def write_day_file(day_df: pd.DataFrame, rel: str, pull_id: str,
                   manifest: dict) -> dict:
    """Atomic write of one immutable day file + manifest entry. The file
    must not exist (orphan walk guarantees it); a pre-existing file is a
    contract violation and aborts."""
    target = RAW_DIR / rel
    if target.exists():
        raise DataError(f"{rel} already exists — immutable archive contract "
                        f"(first write wins). Investigate before touching it.")
    data = day_df.to_parquet()                # already bytes (pandas 3.0)
    atomic_write_bytes(target, data)
    rec = {"sha256": hashlib.sha256(data).hexdigest(),
           "rows": int(len(day_df)),
           "first": str(day_df.index[0]),
           "last": str(day_df.index[-1]),
           "pull_id": pull_id}
    manifest["files"][rel] = rec
    return rec


def drift_check(day_df: pd.DataFrame, rel: str, rec: dict) -> str | None:
    """Byte-level compare of a freshly fetched window against the recorded
    file for the same (date, ticker). Hashing the fresh parquet against the
    stored SHA-256 catches ANY Yahoo restatement, even one that leaves rows
    and span looking identical. We never rewrite — we report loudly so a
    human decides (--repair is the sanctioned recovery)."""
    fresh = hashlib.sha256(day_df.to_parquet()).hexdigest()
    if fresh == rec["sha256"]:
        return None
    return (f"{rel}: fresh fetch differs from stored file (stored "
            f"{rec['sha256'][:12]}… vs fresh {fresh[:12]}…; "
            f"rows {rec['rows']}->{len(day_df)}) — possible Yahoo "
            f"restatement; stored file is final, --repair + re-pull to refresh")


def run_pull(args) -> int:
    """The pull itself — runs under the lock (see main)."""
    manifest = load_manifest()
    repairs = load_repairs()
    n_checked, n_ok = verify_manifest(manifest, repairs)

    uni = pd.read_csv(args.universe)
    tickers = list(uni["ticker"])
    if args.limit:
        tickers = tickers[: args.limit]

    pull_id = datetime.now(ZoneInfo("UTC")).strftime("%Y%m%d-%H%M%S")
    now_et = datetime.now(TZ)
    pull = {"pull_id": pull_id,
            "started_utc": datetime.now(ZoneInfo("UTC")).isoformat(),
            "driver": "yahoo", "window": WINDOW,
            "universe_file": args.universe.name,
            "universe_sha256": sha256_file(args.universe),
            "tickers_requested": len(tickers),
            "tickers_ok": 0, "tickers_no_data": 0, "tickers_failed": 0,
            "files_written": 0, "files_skipped_existing": 0,
            "files_verified": n_checked, "files_verified_ok": n_ok,
            "drift": [], "failed": []}

    results = {}
    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        futs = {pool.submit(DRIVERS["yahoo"], t): t for t in tickers}
        for fut in as_completed(futs):
            t = futs[fut]
            try:
                results[t] = fut.result()
            except ValueError as e:
                results[t] = None
                pull["tickers_no_data"] += 1
                pull["failed"].append(f"{t}: {e}")
            except Exception as e:
                results[t] = None
                pull["tickers_failed"] += 1
                pull["failed"].append(f"{t}: {e}")
            print(f"  {t}: {'ok' if results[t] is not None else 'no_data/failed'}",
                  flush=True)

    # Writes are single-threaded and ticker-sorted for determinism.
    for t in sorted(results):
        df = results[t]
        if df is None:
            continue
        pull["tickers_ok"] += 1
        for d, day_df in split_by_date(df, now_et).items():
            rel = f"{d.isoformat()}/{t}.parquet"
            if rel in manifest["files"]:
                note = drift_check(day_df, rel, manifest["files"][rel])
                if note:
                    pull["drift"].append(note)
                    print(f"  DRIFT: {note}", file=sys.stderr)
                pull["files_skipped_existing"] += 1
            else:
                write_day_file(day_df, rel, pull_id, manifest)
                pull["files_written"] += 1

    pull["prev_pull_sha256"] = last_pull_sha(manifest)
    pull["finished_utc"] = datetime.now(ZoneInfo("UTC")).isoformat()
    manifest["pulls"].append(pull)
    atomic_write_json(MANIFEST_PATH, manifest)     # atomic: ledger lands whole

    print(f"\npull {pull_id}: {pull['files_written']} written, "
          f"{pull['files_skipped_existing']} skipped (existing), "
          f"{pull['files_verified']} files hash-verified "
          f"({pull['files_verified_ok']} ok)")
    print(f"  ok={pull['tickers_ok']} no_data={pull['tickers_no_data']} "
          f"failed={pull['tickers_failed']}")
    for f in pull["failed"][:10]:
        print(f"  FAILED {f}")
    if pull["drift"]:
        print(f"  {len(pull['drift'])} drift note(s) — see manifest pull record",
              file=sys.stderr)
    if args.qa:
        from qa_intraday import main as qa_main
        qa_rc = qa_main([])
        if qa_rc:
            return qa_rc
    if pull["tickers_failed"] or pull["tickers_no_data"]:
        return EXIT_TICKER_FAILURES
    return EXIT_OK


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--universe", type=Path,
                    default=ROOT / "data" / "cache" / "universe_sp600_2026-08-13.csv")
    ap.add_argument("--threads", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0, help="first N tickers only (test)")
    ap.add_argument("--qa", action="store_true", help="run tools/qa_intraday.py after")
    ap.add_argument("--repair", metavar="REL_PATH",
                    help="delete one archived file with a repair record "
                         "(e.g. '2026-08-18/AAP.parquet'); works on orphans "
                         "(no manifest entry) too; requires --reason")
    ap.add_argument("--adopt", metavar="REL_PATH",
                    help="register one crashed-pull orphan in the manifest "
                         "(hash + schema-verified, kept) instead of "
                         "re-fetching; requires --reason")
    ap.add_argument("--reason", default="", help="required with --repair/--adopt")
    args = ap.parse_args(argv)

    if args.repair:
        return do_repair(args.repair, args.reason)
    if args.adopt:
        return do_adopt(args.adopt, args.reason)
    acquired = False
    try:
        acquire_lock()
        acquired = True
        return run_pull(args)
    except DataError as e:
        print(f"ABORT: {e}", file=sys.stderr)
        return EXIT_ABORT
    finally:
        if acquired:
            release_lock()


# ---------------------------------------------------------------------------
# Repair (the ONLY sanctioned way to remove archive data)
# ---------------------------------------------------------------------------

def do_repair(rel: str, reason: str) -> int:
    """Delete one archived file WITH a repair record. The manifest entry is
    also removed (after the repair is recorded) so the next pull may write
    the (date, ticker) fresh — the sanctioned path for a restated/wrong
    file. repairs.json retains the audit trail either way."""
    if not reason.strip():
        print("ABORT: --repair requires --reason (what happened, who decided)", file=sys.stderr)
        return EXIT_ABORT
    rel = rel.replace("\\", "/")
    p = (RAW_DIR / rel).resolve()
    if not p.is_relative_to(RAW_DIR.resolve()) or ".." in Path(rel).parts \
            or not rel.endswith(".parquet"):
        print(f"ABORT: {rel!r} is not an archive file path under {RAW_DIR}", file=sys.stderr)
        return EXIT_ABORT
    acquired = False
    try:
        acquire_lock()
        acquired = True
        manifest = load_manifest()
        rec = manifest["files"].get(rel)
        if rec is None:
            if not p.exists():
                print(f"ABORT: {rel} has no manifest entry and no file on "
                      f"disk — nothing to repair", file=sys.stderr)
                return EXIT_ABORT
            print(f"note: {rel} has no manifest entry (crashed-pull orphan) "
                  f"— recording the deletion without an entry; the next "
                  f"pull re-writes it from the window", file=sys.stderr)
        elif not p.exists():
            print(f"ABORT: {rel} does not exist (manifest entry present but "
                  f"file missing — restore it first, or let the next pull "
                  f"complete the recorded repair)", file=sys.stderr)
            return EXIT_ABORT
        repairs = load_repairs()
        repairs["repairs"].append({"path": rel,
                                   "at_utc": datetime.now(ZoneInfo("UTC")).isoformat(),
                                   "sha256_before": rec["sha256"] if rec
                                   else sha256_file(p),
                                   "manifest_rec": rec,
                                   "reason": reason})
        atomic_write_json(REPAIRS_PATH, repairs)   # record FIRST, then delete
        p.unlink()
        if rec is not None:
            del manifest["files"][rel]
            atomic_write_json(MANIFEST_PATH, manifest)  # then drop the entry
        print(f"repaired: {rel} deleted with repair record (sha "
              f"{repairs['repairs'][-1]['sha256_before'][:12]}…, "
              f"reason: {reason})")
        print(f"note: manifest entry removed — the next pull will re-write "
              f"{rel} fresh if the window still covers it")
        return EXIT_OK
    except DataError as e:
        print(f"ABORT: {e}", file=sys.stderr)
        return EXIT_ABORT
    finally:
        if acquired:
            release_lock()


# ---------------------------------------------------------------------------
# Adoption (the sanctioned way to keep crashed-pull orphans)
# ---------------------------------------------------------------------------

def validate_day_file(p: Path) -> dict:
    """Trust-but-verify for --adopt: a file is registered in the manifest
    only if it is a plausible archived day file (schema rules of the
    archive). Returns rows/first/last for the entry."""
    rel = p.relative_to(RAW_DIR).as_posix()
    try:
        df = pd.read_parquet(p)
    except Exception as e:
        raise DataError(f"adopt {rel}: unreadable parquet ({e}) — not adopted.")
    if not set(COLS) <= set(df.columns):
        raise DataError(f"adopt {rel}: missing OHLCV columns "
                        f"({sorted(set(COLS) - set(df.columns))}) — not adopted.")
    idx = df.index
    if not isinstance(idx, pd.DatetimeIndex):
        raise DataError(f"adopt {rel}: index is not a DatetimeIndex — not adopted.")
    if idx.tz is None:
        raise DataError(f"adopt {rel}: naive timestamps — tz discipline "
                        f"(README), not adopted.")
    idx = idx.tz_convert(TZ)
    if not (idx.floor("min") == idx).all():
        raise DataError(f"adopt {rel}: not minute-floored — not adopted.")
    if not idx.is_monotonic_increasing:
        raise DataError(f"adopt {rel}: timestamps not sorted — not adopted.")
    if idx.duplicated().any():
        raise DataError(f"adopt {rel}: duplicate timestamps — not adopted.")
    bar_date = Path(rel).parts[0]
    if len(idx) == 0 or {d.isoformat() for d in idx.date} != {bar_date}:
        raise DataError(f"adopt {rel}: all rows must be bar-date {bar_date} "
                        f"(got {len(idx)} rows spanning "
                        f"{sorted({d.isoformat() for d in idx.date})[:3]}) — "
                        f"not adopted.")
    return {"rows": int(len(idx)), "first": str(idx[0]), "last": str(idx[-1])}


def do_adopt(rel: str, reason: str) -> int:
    """Register one crashed-pull orphan in the manifest after hashing and
    schema-checking it, so it becomes a normal, permanently verified member
    of the archive. The alternative to --repair when the file is valid and
    the 7-day window no longer covers a re-fetch."""
    if not reason.strip():
        print("ABORT: --adopt requires --reason (what happened, who decided)",
              file=sys.stderr)
        return EXIT_ABORT
    rel = rel.replace("\\", "/")
    p = (RAW_DIR / rel).resolve()
    if not p.is_relative_to(RAW_DIR.resolve()) or ".." in Path(rel).parts \
            or not rel.endswith(".parquet"):
        print(f"ABORT: {rel!r} is not an archive file path under {RAW_DIR}",
              file=sys.stderr)
        return EXIT_ABORT
    acquired = False
    try:
        acquire_lock()
        acquired = True
        manifest = load_manifest()
        if rel in manifest["files"]:
            print(f"ABORT: {rel} already has a manifest entry — nothing to "
                  f"adopt", file=sys.stderr)
            return EXIT_ABORT
        if not p.exists():
            print(f"ABORT: {rel} does not exist — nothing to adopt",
                  file=sys.stderr)
            return EXIT_ABORT
        info = validate_day_file(p)
        manifest["files"][rel] = {
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "rows": info["rows"], "first": info["first"], "last": info["last"],
            "pull_id": f"adopt-{datetime.now(ZoneInfo('UTC')).strftime('%Y%m%d-%H%M%S')}",
            "adopted": True, "reason": reason}
        atomic_write_json(MANIFEST_PATH, manifest)
        print(f"adopted: {rel} registered in the manifest (sha "
              f"{manifest['files'][rel]['sha256'][:12]}…, rows {info['rows']}, "
              f"reason: {reason})")
        print(f"note: the next pull will verify and drift-check {rel} like "
              f"any archived file")
        return EXIT_OK
    except DataError as e:
        print(f"ABORT: {e}", file=sys.stderr)
        return EXIT_ABORT
    finally:
        if acquired:
            release_lock()


if __name__ == "__main__":
    sys.exit(main())
