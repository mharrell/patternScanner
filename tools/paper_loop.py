"""Pre-registration #23 paper-loop tool — live-execution study of the frozen
intraday signals.

Implements PREREGISTRATION.md §Pre-registration #23 exactly:
  * §3 the paper-loop tool (frozen): imports the five frozen tools, asserting
    their LF-normalized shas at import; runs per bar-date as it lands; logs
    the decision path; byte-deterministic; FROZEN_SHA fixed-point.
  * §4 the slippage/fill model (frozen): three price columns per entry/exit —
    recorded-bar reference, modeled fill (s per side), observed fill
    (operator, ground truth). The modeled-fill comparison is a sensitivity;
    the observed-fill comparison is the L-007 measurement.
  * §5 the gate-decision log (frozen): per entry candidate — signal bar, entry
    bar, entry price, stop, target, hour, veto verdict, regime bucket, and per
    exit rule the exit the rules would take with the exit price.
  * §6 the daily journal (frozen format): automated facts + operator notes.
  * §7 the §5-gated comparison (pre-registered): the L-007 gap measurement row.

Frozen 2026-08-23, before any paper-log results exist. The module sha is
asserted at run (FROZEN_SHA below, the fixed-point convention): any byte
change invalidates the campaign.

Modes:
  python -X utf8 tools/paper_loop.py --date YYYY-MM-DD
      Process one bar-date.
  python -X utf8 tools/paper_loop.py --latest
      Process the most recent complete bar-date in the manifest (nightly task).
  python -X utf8 tools/paper_loop.py --all
      Process every window bar-date >= 2026-08-19 (backfill, idempotent).
  python -X utf8 tools/paper_loop.py --check
      Determinism check: re-run --all and byte-compare the JSON logs against
      the committed ones.
  python -X utf8 tools/paper_loop.py --compare
      The §5-gated comparison (refuses with exit 2 until the floors are met;
      runs the audit gate).

Exit codes: 0 ok, 1 audit/integrity failure, 2 floors unmet (refused),
3 input error.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import time as dtime
from pathlib import Path

import numpy as np
import pandas as pd

import measure_intraday as MI
import measure_intraday_entry as MIE
import measure_intraday_exit as MIX
import measure_intraday_veto as MIV
import measure_intraday_regime as MIR

ROOT = Path(__file__).resolve().parent.parent
INTRA = ROOT / "data" / "intraday"
RAW_DIR = INTRA / "raw"
MANIFEST_PATH = INTRA / "manifest.json"
PAPER_DIR = ROOT / "data" / "paper"
JOURNAL_DIR = PAPER_DIR / "journal"
OBSERVED_DIR = PAPER_DIR / "observed"

WINDOW_START = "2026-08-19"

# ---- frozen-input assertions (pre-reg #23 §3): the five frozen tools ----
# Each tool's LF-normalized sha256 (checkout-independent) is asserted AT
# IMPORT; a change to any frozen input aborts loudly. The first two are
# recorded in pre-regs #15/#19 §8; the last three are recorded in #23 §10.
_FROZEN_INPUTS = {
    "measure_intraday.py":
        "c58282caf75c344f228b70b329e9182b54a663d013891fe6a17103dc89f5e14c",
    "measure_intraday_entry.py":
        "d58a889c6c0a634952bacd90bf412140709102053facebf1ee82b5df67592656",
    "measure_intraday_exit.py":
        "50af1ea6adf7e85acab666e38cdb9ec951cac4afb518f6f2fa3fe6a662394a7f",
    "measure_intraday_veto.py":
        "e35f0a52d76a7414fd4345a4076964e8640a1f31691ef4f9b2400b247723880a",
    "measure_intraday_regime.py":
        "2fed9790feffe6c5eabf195876ecc655007aeff8b7d5bbda2ea0bf7467792cec",
}
_FROZEN_MODULES = {
    "measure_intraday.py": MI,
    "measure_intraday_entry.py": MIE,
    "measure_intraday_exit.py": MIX,
    "measure_intraday_veto.py": MIV,
    "measure_intraday_regime.py": MIR,
}


def _lf_sha(module) -> str:
    """LF-normalized sha256 of a module file — checkout-independent."""
    return hashlib.sha256(Path(module.__file__).read_bytes()
                          .replace(b"\r\n", b"\n")).hexdigest()


for _name, _mod in _FROZEN_MODULES.items():
    _got = _lf_sha(_mod)
    _want = _FROZEN_INPUTS[_name]
    assert _got == _want, (
        f"{_name} changed (sha {_got[:16]}..., want {_want[:16]}...) — "
        f"frozen input must not move")

# ---- frozen parameters (pre-reg #23 §4/§7) ----
S_PRIMARY = 0.0005          # per-side slippage, primary (S-C05 intraday tier)
S_SENS = [0.0015, 0.0030]   # sensitivities (house daily tier, 0.30%)
MATCH_TOL_MIN = 2           # observed-fill match tolerance (±2 minutes)
COMPLETENESS_FLOOR = 0.90   # paper-log completeness floor (§7)

# Freeze sha (house fixed-point convention; see measure_intraday.py): the
# sha of this file with its own FROZEN_SHA hex blanked to 64 zeros — a
# well-defined fixed point. Any byte change outside the blanked hex breaks
# the assertion.
FROZEN_SHA = "c08b3ca53cb8d24af404f9f0b2f5fb2779a151fa02e130706ea7f3adc13b579a"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


_FROZEN_RE = re.compile(rb'(FROZEN_SHA = "[0-9a-f]{64}")')


def hash_self() -> str:
    """sha256 of this file with the FROZEN_SHA hex blanked (fixed point)."""
    b = Path(__file__).read_bytes()
    b2, n = _FROZEN_RE.subn(b'FROZEN_SHA = "' + b"0" * 64 + b'"', b)
    if n != 1:
        raise RuntimeError("expected exactly one FROZEN_SHA hex line")
    return sha_bytes(b2)


def self_check() -> None:
    if FROZEN_SHA == "0" * 64:
        print("FATAL: FROZEN_SHA is blank — tool not frozen. Refusing to run.",
              file=sys.stderr)
        sys.exit(3)
    actual = hash_self()
    if actual != FROZEN_SHA:
        print(f"FATAL: paper_loop.py sha mismatch — frozen "
              f"{FROZEN_SHA[:12]}…, on disk {actual[:12]}…. A frozen "
              f"measurement tool must not change.", file=sys.stderr)
        sys.exit(1)


# --------------------------------------------------------------------------
# §4 the slippage/fill model (frozen)
# --------------------------------------------------------------------------

def modeled_fills(entry_open: float, exit_price: float, s: float) -> tuple:
    """Pre-reg #23 §4: entry_fill = entry_open*(1+s), exit_fill =
    exit_price*(1-s), modeled_ret = (exit_fill - entry_fill)/entry_fill.
    At s=0 the modeled return equals the frozen gross return exactly
    (parity)."""
    entry_fill = entry_open * (1 + s)
    exit_fill = exit_price * (1 - s)
    modeled_ret = (exit_fill - entry_fill) / entry_fill
    return entry_fill, exit_fill, modeled_ret


def rule_row(entry: float, gross_ret: float, **flags) -> dict:
    """One exit rule's row: the recorded-bar reference (entry price, exit
    price derived from the frozen gross return), the modeled fills at the
    primary s, and the mechanism flags (pre-reg #23 §4/§5)."""
    exit_price = entry * (1 + gross_ret)
    entry_fill, exit_fill, modeled_ret = modeled_fills(entry, exit_price,
                                                       S_PRIMARY)
    row = {
        "exit_price": round(exit_price, 6),
        "recorded_ret": round(gross_ret, 8),
        "entry_fill": round(entry_fill, 6),
        "exit_fill": round(exit_fill, 6),
        "modeled_ret": round(modeled_ret, 8),
    }
    row.update(flags)
    return row


# --------------------------------------------------------------------------
# §5 the gate-decision log (frozen)
# --------------------------------------------------------------------------

def regime_bucket(ts) -> str:
    """Pre-reg #22 §1: B1 = 07:00-10:00, B2 = 09:30-12:00, else 'outside'.
    B1 takes precedence in the 09:30-10:00 overlap (the earlier window)."""
    t = ts.time()
    if dtime(7, 0) <= t < dtime(10, 0):
        return "B1"
    if dtime(9, 30) <= t < dtime(12, 0):
        return "B2"
    return "outside"


def veto_verdict(macd, vol: bool) -> dict:
    """Pre-reg #21 §1: veto-pass = neither leg fires; veto-fail = >=1 leg
    fires. macd None (EMA-26 warm-up unmet) => not evaluable."""
    if macd is None:
        return {"evaluable": False, "pass": None, "macd_neg": None,
                "vol_spike": vol, "legs": []}
    macd_neg = macd < 0
    legs = []
    if macd_neg:
        legs.append("macd")
    if vol:
        legs.append("volume")
    return {"evaluable": True, "pass": not legs, "macd_neg": macd_neg,
            "vol_spike": vol, "legs": legs}


def wpos(df: pd.DataFrame) -> np.ndarray:
    """RTH window positions (pre-reg #15 §3)."""
    return np.flatnonzero(MI.window_mask(df.index, None))


def process_file(rel: str, df: pd.DataFrame) -> dict:
    """Run all five frozen definitions on one (bar-date, ticker) file and
    return the decision-path dict (pre-reg #23 §3/§5)."""
    w = wpos(df)
    npos = len(w)
    op = df["Open"].to_numpy()[w]
    hi = df["High"].to_numpy()[w]
    lo = df["Low"].to_numpy()[w]
    cl = df["Close"].to_numpy()[w]
    closes = df["Close"].to_numpy()
    times = df.index[w]
    wmins = (times.hour.to_numpy() * 60 + times.minute.to_numpy())
    vw = MIX.vwap_series(df, w)

    out = {"b01": [], "reversal": [], "pullback": [], "second_conf": [],
           "regime": {}}

    # B-01 events (pre-reg #15 §3) -> the five exit rules (pre-reg #20 §3).
    det = MI.detect_b01(df, n_need=MI.N_PRIMARY)
    for ev in det["events"]:
        e, entry, stop = ev["e_pos"], ev["entry_open"], ev["stop"]
        entry_et = times[e + 1]
        exits = {}
        br = MIX.breakeven_trail_s(op, hi, lo, cl, wmins, e, entry, stop,
                                   npos)
        if br is not None:
            exits["breakeven_trail"] = rule_row(entry, br[0],
                                                half_fired=bool(br[1]))
        ld = MIX.ladder_s(op, hi, lo, cl, vw, e, entry, npos)
        if ld is not None:
            exits["ladder"] = rule_row(entry, ld[0], legs=int(ld[1]))
        fl = MIX.flat_out_s(cl, e, entry, npos, MIX.M_FLAT, MIX.EPS_FLAT)
        if fl is not None:
            exits["flat_out"] = rule_row(entry, fl[0], flat=bool(fl[1]))
        fn = MIX.fixed_n_s(cl, e, entry, npos)
        if fn is not None:
            exits["fixed_n"] = rule_row(entry, fn)
        f2 = MIX.fixed_2r_s(op, hi, lo, cl, e, entry, stop, npos)
        if f2 is not None:
            exits["fixed_2r"] = rule_row(entry, f2)
        out["b01"].append({
            "signal_et": times[e].isoformat(),
            "entry_et": entry_et.isoformat(),
            "dir": "long",
            "entry_open": round(entry, 6),
            "stop": round(stop, 6),
            "target": round(ev["target"], 6),
            "hour": ev["hour"],
            "regime": regime_bucket(entry_et),
            "exits": exits,
        })

    # Reversal new-high (pre-reg #19 F1) -> the veto legs (pre-reg #21 §1).
    rv = MIE.detect_reversal(df, d=MIE.D_PRIMARY, win=None, five_min=False)
    for d_ in ("long", "short"):
        for ev in rv[d_]:
            e = ev["e_pos"]
            e_abs = int(w[e])
            entry_et = times[e + 1]
            macd = MIV.macd_at(closes, e_abs)
            vol = MIV.volume_spike(df, w, e_abs, MIV.V_PRIMARY)
            out["reversal"].append({
                "signal_et": times[e].isoformat(),
                "entry_et": entry_et.isoformat(),
                "dir": d_,
                "entry_open": round(ev["entry_open"], 6),
                "stop": round(ev["stop"], 6),
                "target": round(ev["target"], 6),
                "hour": ev["hour"],
                "regime": regime_bucket(entry_et),
                "veto": veto_verdict(macd, vol),
            })

    # Pullback-count (pre-reg #19 F2).
    pb = MIE.detect_pullback_count(df, win=None, five_min=False)
    for ev in pb["events"]:
        e = ev["e_pos"]
        entry_et = times[e + 1]
        out["pullback"].append({
            "signal_et": times[e].isoformat(),
            "entry_et": entry_et.isoformat(),
            "k": ev["k"],
            "entry_open": round(ev["entry_open"], 6),
            "hour": ev["hour"],
            "regime": regime_bucket(entry_et),
        })

    # Second-confirmation (pre-reg #19 F3).
    sc = MIE.detect_second_conf(df, win=None, five_min=False)
    for p in sc["pairs"]:
        out["second_conf"].append({
            "c1_et": times[p["c1_pos"]].isoformat(),
            "e1_open": round(p["e1_open"], 6),
            "e2_open": round(p["e2_open"], 6),
            "hour": p["hour"],
            "regime": regime_bucket(times[p["c1_pos"]]),
        })

    # Regime: per-file bucket membership (pre-reg #22 §1).
    out["regime"] = {"B1": 0, "B2": 0, "outside": 0}
    for t in times:
        out["regime"][regime_bucket(t)] += 1

    return out


# --------------------------------------------------------------------------
# run / write
# --------------------------------------------------------------------------

def window_dates() -> list:
    """Sorted window bar-dates (>= WINDOW_START) present in the manifest."""
    m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return sorted({f.split("/")[0] for f in m.get("files", {})
                   if f.split("/")[0] >= WINDOW_START})


def latest_date() -> str:
    """The most recent complete bar-date in the manifest."""
    dates = window_dates()
    if not dates:
        raise SystemExit("no window bar-dates in the manifest")
    return dates[-1]


def run_day(date: str) -> dict:
    """Process one bar-date: iterate sorted manifest files for the date,
    process_file each, aggregate (pre-reg #23 §3)."""
    m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    rels = sorted(f for f in m.get("files", {}) if f.split("/")[0] == date)
    files = {}
    for rel in rels:
        df = MI.load_day(rel)
        files[rel] = process_file(rel, df)
    return {
        "bar_date": date,
        "frozen_inputs": {name: sha for name, sha in _FROZEN_INPUTS.items()},
        "fill_model": {"s_primary": S_PRIMARY, "s_sens": S_SENS},
        "files": files,
    }


def write_json(date: str, data: dict) -> Path:
    """Write data/paper/<date>.json (sorted keys, fixed float precision)."""
    PAPER_DIR.mkdir(parents=True, exist_ok=True)
    p = PAPER_DIR / f"{date}.json"
    p.write_text(json.dumps(data, sort_keys=True, indent=1) + "\n",
                 encoding="utf-8")
    return p


def write_journal(date: str, data: dict) -> Path:
    """Write the journal skeleton data/paper/journal/<date>.md (pre-reg #23
    §6): header, automated facts, empty operator notes. Written once — the
    operator's notes are never overwritten."""
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    p = JOURNAL_DIR / f"{date}.md"
    if p.exists():
        return p
    n_files = len(data["files"])
    n_b01 = sum(len(f["b01"]) for f in data["files"].values())
    n_rev = sum(len(f["reversal"]) for f in data["files"].values())
    n_pb = sum(len(f["pullback"]) for f in data["files"].values())
    n_sc = sum(len(f["second_conf"]) for f in data["files"].values())
    veto_pass = sum(1 for f in data["files"].values() for ev in f["reversal"]
                    if ev["veto"]["evaluable"] and ev["veto"]["pass"])
    veto_fail = sum(1 for f in data["files"].values() for ev in f["reversal"]
                    if ev["veto"]["evaluable"] and not ev["veto"]["pass"])
    veto_na = sum(1 for f in data["files"].values() for ev in f["reversal"]
                  if not ev["veto"]["evaluable"])
    n_b1 = sum(f["regime"]["B1"] for f in data["files"].values())
    n_b2 = sum(f["regime"]["B2"] for f in data["files"].values())
    n_out = sum(f["regime"]["outside"] for f in data["files"].values())
    L = [
        f"# Paper loop journal — {date}",
        "",
        "## Automated facts (from the frozen detectors)",
        "",
        f"- Bar-date: {date}",
        f"- Files processed: {n_files}",
        f"- B-01 entries: {n_b01}",
        f"- Reversal new-high entries: {n_rev} (long+short)",
        f"- Pullback-count entries: {n_pb}",
        f"- Second-confirmation pairs: {n_sc}",
        f"- Veto verdicts: pass {veto_pass} / fail {veto_fail} / "
        f"not-evaluable {veto_na}",
        f"- Regime buckets (bars): B1 {n_b1} / B2 {n_b2} / outside {n_out}",
        "",
        "## Operator notes (the muscle)",
        "",
        "- What did the tape look like today?",
        "- Were the modeled fills realistic? Any observed fills?",
        "- What did I learn?",
        "",
    ]
    p.write_text("\n".join(L), encoding="utf-8")
    return p


# --------------------------------------------------------------------------
# --check (determinism) and --compare (§7)
# --------------------------------------------------------------------------

def run_check() -> int:
    """Determinism check: re-run --all and byte-compare the JSON logs
    against the committed ones (pre-reg #23 §7 integrity gate)."""
    ok = True
    for date in window_dates():
        data = run_day(date)
        p = PAPER_DIR / f"{date}.json"
        if not p.exists():
            print(f"MISSING: {p}")
            ok = False
            continue
        expected = json.dumps(data, sort_keys=True, indent=1) + "\n"
        actual = p.read_text(encoding="utf-8")
        if actual != expected:
            print(f"MISMATCH: {p}")
            ok = False
    print("paper-log determinism check: " + ("OK" if ok else "FAILED"))
    return 0 if ok else 1


def _load_observed(date: str) -> list:
    """The operator's observed fills for a bar-date (pre-reg #23 §6)."""
    p = OBSERVED_DIR / f"{date}.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("fills", [])


def _pct(vals, q: float) -> float:
    """The q-th percentile of a list (0..1)."""
    if not vals:
        return float("nan")
    a = np.sort(np.asarray(vals, dtype=float))
    return float(np.percentile(a, q * 100))


def _min_of_day(t) -> float:
    """Minutes-of-day of a datetime.time (or a time-parseable value)."""
    tt = t.time() if hasattr(t, "time") else t
    return tt.hour * 60 + tt.minute + tt.second / 60.0


def _match_observed(obs: list, data: dict) -> tuple:
    """Match observed fills to deterministic B-01 entries by (ticker,
    signal_et, dir) with a ±MATCH_TOL_MIN-minute tolerance (pre-reg #23
    §6). Returns (matched, unmatched) lists."""
    matched, unmatched = [], []
    for o in obs:
        ticker = o.get("ticker")
        sig = o.get("signal_et")
        d_ = o.get("dir")
        if not ticker or not sig or not d_:
            unmatched.append(o)
            continue
        sig_min = _min_of_day(pd.Timestamp(sig))
        hit = None
        for rel, f in data["files"].items():
            if rel.split("/")[1][:-len(".parquet")] != ticker:
                continue
            for ev in f["b01"]:
                if ev["dir"] != d_:
                    continue
                et_min = _min_of_day(pd.Timestamp(ev["signal_et"]))
                if abs(et_min - sig_min) <= MATCH_TOL_MIN:
                    hit = (rel, ev)
                    break
            if hit:
                break
        if hit:
            matched.append((o, hit))
        else:
            unmatched.append(o)
    return matched, unmatched


def run_compare() -> int:
    """The §5-gated comparison (pre-reg #23 §7): the L-007 gap measurement
    row. Refuses (exit 2) until the floors are met; runs the audit gate."""
    audit = MI.audit_archive()
    if not audit["passed"]:
        print("FATAL: archive-integrity audit FAILED — comparison void.")
        for e in audit["errors"][:10]:
            print(f"  - {e}")
        return 1
    window = window_dates()
    if len(window) < MI.FLOORS["min_bar_dates"]:
        print(f"REFUSED: §5 floor unmet — {len(window)} window bar-dates < "
              f"{MI.FLOORS['min_bar_dates']}.")
        return 2
    logged = [d for d in window if (PAPER_DIR / f"{d}.json").exists()]
    coverage = len(logged) / len(window)
    if coverage < COMPLETENESS_FLOOR:
        print(f"REFUSED: paper-log completeness {coverage:.0%} < "
              f"{COMPLETENESS_FLOOR:.0%} — INCONCLUSIVE.")
        return 2

    # Paper-log integrity: recompute the recorded-bar returns from the
    # archive and verify they match the logs' recorded-bar references.
    n_checked = 0
    for date in logged:
        data = json.loads((PAPER_DIR / f"{date}.json")
                          .read_text(encoding="utf-8"))
        m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        rels = sorted(f for f in m.get("files", {})
                      if f.split("/")[0] == date)
        for rel in rels:
            df = MI.load_day(rel)
            w = wpos(df)
            npos = len(w)
            op = df["Open"].to_numpy()[w]
            hi = df["High"].to_numpy()[w]
            lo = df["Low"].to_numpy()[w]
            cl = df["Close"].to_numpy()[w]
            vw = MIX.vwap_series(df, w)
            wmins = (df.index[w].hour.to_numpy() * 60 +
                     df.index[w].minute.to_numpy())
            logged_evs = data["files"].get(rel, {}).get("b01", [])
            det = MI.detect_b01(df, n_need=MI.N_PRIMARY)
            for ev, lev in zip(det["events"], logged_evs):
                e, entry, stop = ev["e_pos"], ev["entry_open"], ev["stop"]
                fn = MIX.fixed_n_s(cl, e, entry, npos)
                if fn is None:
                    continue
                want = round(fn, 8)
                got = lev["exits"].get("fixed_n", {}).get("recorded_ret")
                if got is None or abs(got - want) > 1e-9:
                    print(f"INTEGRITY FAIL: {rel} fixed_n recorded_ret "
                          f"{got} != recomputed {want}")
                    return 1
                n_checked += 1
    print(f"paper-log integrity: OK ({n_checked} fixed-N returns verified)")

    # The L-007 gap measurement row (pre-reg #23 §7): per exit rule on the
    # B-01 set, mean(paper-log realized return) - mean(recorded-bar return).
    # Modeled fills (primary s) on the full set = the sensitivity; observed
    # fills where present = the L-007 measurement. Reported per rule with
    # the distribution (p10/p50/p90) and the per-bar-date breakdown.
    rows = []
    for date in logged:
        data = json.loads((PAPER_DIR / f"{date}.json")
                          .read_text(encoding="utf-8"))
        for rel, f in data["files"].items():
            for ev in f["b01"]:
                for rule, r in ev["exits"].items():
                    rows.append({"date": date, "rel": rel, "rule": rule,
                                 "recorded": r["recorded_ret"],
                                 "modeled": r["modeled_ret"]})
    if not rows:
        print("no B-01 exit rows in the paper log — comparison empty.")
        return 0
    print("L-007 gap measurement row (B-01 entry set; modeled = primary s "
          "sensitivity, observed = L-007 measurement):")
    for rule in sorted({r["rule"] for r in rows}):
        rr = [r["recorded"] for r in rows if r["rule"] == rule]
        mr = [r["modeled"] for r in rows if r["rule"] == rule]
        gaps = [m - c for c, m in zip(rr, mr)]
        print(f"  {rule:16s} n={len(rr):5d}  recorded "
              f"{sum(rr)/len(rr):+.6f}  modeled {sum(mr)/len(mr):+.6f}  "
              f"gap {sum(gaps)/len(gaps):+.6f}  "
              f"p10 {_pct(gaps, 0.1):+.6f}  p50 {_pct(gaps, 0.5):+.6f}  "
              f"p90 {_pct(gaps, 0.9):+.6f}")
    print("  per-bar-date (fixed_n gap):")
    for date in sorted({r["date"] for r in rows}):
        rr = [r["recorded"] for r in rows
              if r["date"] == date and r["rule"] == "fixed_n"]
        mr = [r["modeled"] for r in rows
              if r["date"] == date and r["rule"] == "fixed_n"]
        if rr:
            print(f"    {date}: n={len(rr):5d}  gap "
                  f"{sum(mr)/len(mr) - sum(rr)/len(rr):+.6f}")

    # Observed fills (the L-007 measurement): match to deterministic B-01
    # entries, compute the observed return, the gap vs. the recorded-bar
    # fixed-N return.
    obs_rows = []
    for date in logged:
        data = json.loads((PAPER_DIR / f"{date}.json")
                          .read_text(encoding="utf-8"))
        obs = _load_observed(date)
        matched, unmatched = _match_observed(obs, data)
        for o, (rel, ev) in matched:
            entry_fill = o.get("entry_fill")
            exit_fill = o.get("exit_fill")
            if not entry_fill or not exit_fill:
                continue
            obs_ret = (exit_fill - entry_fill) / entry_fill
            rec = ev["exits"].get("fixed_n", {}).get("recorded_ret")
            if rec is None:
                continue
            obs_rows.append({"date": date, "rel": rel,
                             "observed": obs_ret, "recorded": rec})
        if unmatched:
            print(f"  observed fills unmatched on {date}: "
                  f"{len(unmatched)} (counted, never dropped)")
    if obs_rows:
        og = [o["observed"] - o["recorded"] for o in obs_rows]
        print(f"  observed-fill L-007 gap: n={len(obs_rows)}  "
              f"mean {sum(og)/len(og):+.6f}  "
              f"p10 {_pct(og, 0.1):+.6f}  p50 {_pct(og, 0.5):+.6f}  "
              f"p90 {_pct(og, 0.9):+.6f}")
    else:
        print("  observed-fill L-007 gap: no observed fills recorded yet "
              "(the operator's ground-truth layer is empty by design until "
              "the live tape is watched)")
    return 0


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> int:
    self_check()
    ap = argparse.ArgumentParser(
        description="Pre-reg #23 paper loop — live-execution study of the "
                    "frozen intraday signals.")
    ap.add_argument("--date", metavar="YYYY-MM-DD",
                    help="process one bar-date")
    ap.add_argument("--latest", action="store_true",
                    help="process the most recent complete bar-date")
    ap.add_argument("--all", action="store_true",
                    help="process every window bar-date (backfill)")
    ap.add_argument("--check", action="store_true",
                    help="determinism check (byte-compare the JSON logs)")
    ap.add_argument("--compare", action="store_true",
                    help="the §5-gated comparison (L-007 gap)")
    args = ap.parse_args()

    # Skip if the pull is still running (data/intraday/.lock present) — the
    # nightly paper task runs 25 min after the pull starts; a still-running
    # pull means the bar-date may be incomplete.
    if (INTRA / ".lock").exists():
        print("SKIP: pull still running (data/intraday/.lock present).")
        return 0

    # Audit gate: refuse to log if the archive is dirty (pre-reg #15 §6).
    audit = MI.audit_archive()
    if not audit["passed"]:
        print("FATAL: archive-integrity audit FAILED — refusing to log.")
        for e in audit["errors"][:10]:
            print(f"  - {e}")
        return 1

    if args.compare:
        return run_compare()
    if args.check:
        return run_check()
    if args.all:
        dates = window_dates()
    elif args.latest:
        dates = [latest_date()]
    elif args.date:
        dates = [args.date]
    else:
        ap.print_help()
        return 3

    for date in dates:
        if date < WINDOW_START:
            print(f"SKIP: {date} < window start {WINDOW_START}")
            continue
        data = run_day(date)
        p = write_json(date, data)
        j = write_journal(date, data)
        print(f"{date}: {len(data['files'])} files -> {p.name}, "
              f"journal {j.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
