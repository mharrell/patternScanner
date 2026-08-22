"""Pre-registration #19 measurement tool — intraday entry timing: the
reversal new-high (I-B-02), the pullback-count rule (B-03 / I-B-01), and
the second-confirmation entry (B-05) on 1-minute bars.

Implements PREREGISTRATION.md §Pre-registration #19 exactly:
  * §3 the detectors (reversal new-high long+short; pullback-count
    sequences; second-confirmation pairs — frozen parameters and
    sensitivities),
  * §4 the measurement (F1/F2/F3 families, baselines, measurement rows),
  * §5 the sample-size floors and the one-shot rule (measurement is
    REFUSED until the floors are met; audit-only mode computes no
    returns at all),
  * §6 the archive-integrity audit (shared with pre-reg #15).

Frozen 2026-08-21, before any measurement. The module sha is asserted at
run (FROZEN_SHA below, hashing the file with its own FROZEN_SHA hex
blanked — the fixed-point convention; measure_code_sha256 additionally
records the raw file sha, house-style): any byte change invalidates the
campaign.

Modes:
  python -X utf8 tools/measure_intraday_entry.py --audit-only
      §6 audit + detection event counts + entry metadata only. Computes NO
      return of any kind (per pre-reg #19 §5: no forward-return number
      before the floors are met). Exit 0 = audit clean; 1 = audit FAILED.
  python -X utf8 tools/measure_intraday_entry.py
      Full measurement. Requires the §5 floors; otherwise REFUSES (exit
      2). Writes data/cache/intraday_entry_measure_report.md +
      intraday_entry_measure_results.json, prints their sha256 for the
      determinism check (two runs must byte-compare).

Exit codes: 0 ok, 1 audit/integrity failure, 2 floors unmet (refused),
3 input error.

Spec mapping (pre-reg #19 §3/§4; the primary column):
  F1 I-B-02 reversal — long: decline = D=3 consecutive DOWN bars
  (close<open), signal e = first bar after the decline with High[e] >
  High[e-1], entry = open of e+1, forward (C[e+N]-O[e+1])/O[e+1] - COST,
  N=60 primary; short: D consecutive UP bars, signal s = first bar with
  Low[s] < Low[s-1], forward sign-flipped (long convention). 2 Holm slots
  (long, short); the slot-level Holm test uses the hour-matched
  RANDOM-UNIVERSE baseline (primary, #15 convention); the hour-matched
  same-ticker excess is reported as the slot's secondary statistic.
  Sensitivities S-D2/S-D5 (decline/rise length), S-5M (every-5th-bar
  sample), S-C05/S-C30 (cost). All sensitivities exploratory, NO verdicts.
  F2 (pullback-count) — run = >=3 consecutive UP bars, pullback = >=2
  consecutive DOWN bars, resume r = first bar with High[r] > High[r-1];
  each resume is labelled k = its ordinal in the day's chain (1st, 2nd,
  3rd...); early = k<=2, late = k>=3; entry open of r+1. Contrast =
  mean(early) - mean(late), paired bootstrap; single Holm slot; the
  same-ticker and random-universe baseline-adjusted contrasts are reported
  as rows (both baseline pairs).
  F3 (second-confirmation) — after a D=3 decline, c1 = first bar closing
  above its prior close, c2 = the next consecutive bar closing above its
  prior close; occurrences with only c1 are dropped and counted. Two
  entries per occurrence: E1 = open of bar after c1, E2 = open of bar
  after c2. Contrast = mean forward N=60 of E2 - mean of E1, paired on
  the occurrence. 1 Holm slot.
  COST 0.0015 round-trip, B=1000, seed 20260821, alpha 0.05, window start
  bar-date 2026-08-19, floors shared with pre-reg #15.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import time as dtime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INTRA = ROOT / "data" / "intraday"
RAW_DIR = INTRA / "raw"
MANIFEST_PATH = INTRA / "manifest.json"
REPAIRS_PATH = INTRA / "repairs.json"
OUT_DIR = ROOT / "data" / "cache"
REPORT_PATH = OUT_DIR / "intraday_entry_measure_report.md"
RESULTS_PATH = OUT_DIR / "intraday_entry_measure_results.json"

TZ = ZoneInfo("America/New_York")
RTH_OPEN = dtime(9, 30)
RTH_END = dtime(16, 0)
WINDOW_START = "2026-08-19"  # first bar-date of the measurement window

# Primary parameters (pre-reg #19 §3/§4) — frozen.
D_PRIMARY = 3               # decline/rise run length (S-D2=2, S-D5=5)
N_PRIMARY = 60              # forward horizon (bars)
COST_PRIMARY = 0.0015
B = 1000
SEED = 20260821             # freeze date
ALPHA = 0.05
FLOORS = {"min_bar_dates": 20, "min_events": 2000,
          "min_tickers": 100, "min_dates_with_events": 15}
MIN_SLOT = 100  # per-slot count floor (house)

# Freeze sha (house convention, measure_intraday.py/measure_cexit.py): the
# sha of this file with its own FROZEN_SHA hex blanked to 64 zeros — a
# well-defined fixed point (a file cannot hash to a value embedded in
# itself). Any byte change outside the blanked hex breaks the assertion.
FROZEN_SHA = "cac0e7ed205c8fbea62dad2c1f3f181cbe6b2b247d00c34c9c93b0c426c4b48c"


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
        print(f"FATAL: measure_intraday_entry.py sha mismatch — frozen "
              f"{FROZEN_SHA[:12]}…, on disk {actual[:12]}…. A frozen "
              f"measurement tool must not change.", file=sys.stderr)
        sys.exit(1)


def window_mask(idx: pd.DatetimeIndex, win: tuple | None) -> np.ndarray:
    """Bars in the detection window: RTH 09:30-16:00 (primary)."""
    t = idx.time
    if win is not None:
        a, b = win
        return np.array([(x >= a) and (x < b) for x in t])
    return np.array([(x >= RTH_OPEN) and (x < RTH_END) for x in t])


# --------------------------------------------------------------------------
# §6 archive-integrity audit
# --------------------------------------------------------------------------

def audit_archive() -> dict:
    """§6 audit: pull-chain validity, file/hash ledger match, per-pull
    universe attribution, blind-capture check, repairs list. Returns the
    evidence dict; 'passed' is the summary. Any failure voids the campaign
    (pre-reg §6) — measurement is refused."""
    m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    pulls = m.get("pulls", [])
    files = m.get("files", {})
    ev = {"passed": True, "errors": [], "notes": [],
          "n_pulls": len(pulls), "n_files_ledger": len(files),
          "chain": [], "window_pulls": [], "repairs": []}

    for i, p in enumerate(pulls):
        expect = ("root" if i == 0 else sha_bytes(
            json.dumps(pulls[i - 1], sort_keys=True).encode("utf-8")))
        ok = p.get("prev_pull_sha256") == expect
        ev["chain"].append({"pull_id": p["pull_id"], "ok": ok})
        if not ok:
            ev["passed"] = False
            ev["errors"].append(
                f"pull {p['pull_id']} prev_pull_sha256 mismatch")

    on_disk = {p.relative_to(RAW_DIR).as_posix()
               for p in RAW_DIR.glob("*/*.parquet")}
    for rel, rec in files.items():
        p = RAW_DIR / rel
        if not p.exists():
            ev["passed"] = False
            ev["errors"].append(f"ledger entry missing on disk: {rel}")
            continue
        if sha_file(p) != rec.get("sha256"):
            ev["passed"] = False
            ev["errors"].append(f"hash mismatch: {rel}")
    orphans = sorted(on_disk - set(files))
    if orphans:
        ev["passed"] = False
        ev["errors"].append(f"orphan file(s) not in ledger: {orphans}")

    if REPAIRS_PATH.exists():
        rep = json.loads(REPAIRS_PATH.read_text(encoding="utf-8"))
        ev["repairs"] = [{"path": r.get("path"), "reason": r.get("reason")}
                         for r in rep.get("repairs", [])]

    pull_by_id = {p["pull_id"]: p for p in pulls}
    rows_of = {}
    seen = set()
    for rel in sorted(files):
        if rel.split("/")[0] < WINDOW_START:
            continue
        p = pull_by_id.get(files[rel].get("pull_id"))
        if p is None:
            ev["passed"] = False
            ev["errors"].append(f"{rel}: pull_id not found")
            continue
        uf = p.get("universe_file", "")
        if not uf.startswith("universe_sp600_"):
            ev["passed"] = False
            ev["errors"].append(f"{rel}: pull {p['pull_id']} universe "
                                f"{uf!r} is not a membership file "
                                f"(non-blind capture)")
            continue
        if uf not in rows_of:
            ufp = INTRA / ".." / "cache" / uf
            if not ufp.exists():
                ev["passed"] = False
                ev["errors"].append(
                    f"universe file missing locally: {uf}")
                rows_of[uf] = None
            else:
                rows_of[uf] = len(pd.read_csv(ufp))
        want = rows_of[uf]
        if want is not None and p.get("tickers_requested") != want:
            ev["passed"] = False
            ev["errors"].append(
                f"{rel}: pull {p['pull_id']} requested "
                f"{p.get('tickers_requested')} != universe rows {want} "
                f"(--limit / non-blind run in window)")
        if uf not in seen:
            seen.add(uf)
            ev["window_pulls"].append({
                "pull_id": p["pull_id"], "universe_file": uf,
                "universe_sha256": p.get("universe_sha256"),
                "tickers_requested": p.get("tickers_requested"),
                "tickers_ok": p.get("tickers_ok"),
                "tickers_failed": p.get("tickers_failed")})
    return ev


# --------------------------------------------------------------------------
# §3 detectors
# --------------------------------------------------------------------------

def load_day(rel: str) -> pd.DataFrame:
    """One (bar-date, ticker) file, tz-aware ET index. Schema anomalies
    abort loudly (the archive contract treats them as fatal)."""
    df = pd.read_parquet(RAW_DIR / rel)
    if not isinstance(df.index, pd.DatetimeIndex) or df.index.tz is None:
        raise ValueError(f"{rel}: naive index — archive schema violation")
    if (df.index.second.to_numpy() != 0).any() or \
            (df.index.microsecond.to_numpy() != 0).any() or \
            (df.index.nanosecond.to_numpy() != 0).any():
        raise ValueError(f"{rel}: index not minute-floored")
    return df


def wpos(df: pd.DataFrame, win: tuple | None,
         five_min: bool = False) -> np.ndarray:
    """Absolute row indices of the detection bars: RTH, or RTH subsampled
    every 5th bar (S-5M)."""
    pos = np.flatnonzero(window_mask(df.index, win))
    if five_min:
        pos = pos[::5]
    return pos


def detect_reversal(df: pd.DataFrame, d: int = D_PRIMARY,
                    win: tuple | None = None,
                    five_min: bool = False) -> dict:
    """§3 F1 detector (I-B-02 reversal new-high) on one day file. Returns
    long_events, short_events (dicts, positions relative to the detection
    bar order), and the count of events whose entry+forward exceeds the
    session end (dropped and counted per §5)."""
    pos = wpos(df, win, five_min)
    n = len(pos)
    if n < d + 2:
        return {"long": [], "short": [], "dropped": 0}
    hi = df["High"].to_numpy()[pos]
    lo = df["Low"].to_numpy()[pos]
    op = df["Open"].to_numpy()[pos]
    cl = df["Close"].to_numpy()[pos]
    up = cl > op
    down = cl < op
    times = df.index[pos]
    long_ev, short_ev, dropped = [], [], 0

    # Long: decline of d consecutive DOWN bars ending at j, then the first
    # bar e > j with High[e] > High[e-1]. Entry = open of e+1.
    j = d - 1
    while j < n:
        if not down[j - d + 1: j + 1].all():
            j += 1
            continue
        k = j + 1
        while k < n and hi[k] <= hi[k - 1]:
            k += 1
        if k + 1 >= n:
            j += 1
            continue
        stop = float(lo[j - d + 1: j + 1].min())
        target = float(hi[j - d + 1: k + 1].max())  # day-high-so-far
        if k + 1 + N_PRIMARY >= n:
            dropped += 1
        long_ev.append({"dir": "long", "e_pos": k,
                        "entry_open": float(op[k + 1]), "stop": stop,
                        "target": target,
                        "hour": int(times[k].hour)})
        j = k + 1

    # ---- short: rise of consecutive UP ending at j, then the first bar
    # s > j with Low[s] < Low[s-1]; forward sign-flipped (long convention).
    j = d - 1
    while j < n:
        if not up[j - d + 1: j + 1].all():
            j += 1
            continue
        k = j + 1
        while k < n and lo[k] >= lo[k - 1]:
            k += 1
        if k + 1 >= n:
            j += 1
            continue
        stop = float(hi[j - d + 1: j + 1].max())   # short stop above
        target = float(lo[j - d + 1: k + 1].min())  # day-low-so-far
        if k + 1 + N_PRIMARY >= n:
            dropped += 1
        short_ev.append({"dir": "short", "e_pos": k,
                         "entry_open": float(op[k + 1]), "stop": stop,
                         "target": target,
                         "hour": int(times[k].hour)})
        j = k + 1
    return {"long": long_ev, "short": short_ev, "dropped": dropped}


def detect_pullback_count(df: pd.DataFrame, win: tuple | None = None,
                          five_min: bool = False) -> dict:
    """§3. F2 detector (B-03 / I-B-01 pullback-count rule). Run >= 3
    consecutive UP, pullback >= 2 consecutive DOWN, resume r = first bar
    with High[r] > High[r-1]. Each completed sequence is labelled k = its
    ordinal in the day's chain. Entry = open of r+1."""
    pos = wpos(df, win, five_min)
    n = len(pos)
    if n < 3 + 2 + 2:
        return {"events": [], "dropped": 0}
    hi = df["High"].to_numpy()[pos]
    op = df["Open"].to_numpy()[pos]
    cl = df["Close"].to_numpy()[pos]
    up = cl > op
    down = cl < op
    times = df.index[pos]
    events, dropped, kth = [], 0, 0
    j = 2
    while j < n:
        if not up[j - 2: j + 1].all():
            j += 1
            continue
        if j + 2 >= n or not (down[j + 1] and down[j + 2]):
            j += 1
            continue
        r = j + 2
        while r < n and hi[r] <= hi[r - 1]:
            r += 1
        if r + 1 >= n:
            j += 1
            continue
        kth += 1
        if r + 1 + N_PRIMARY >= n:
            dropped += 1
        events.append({"e_pos": r, "entry_open": float(op[r + 1]),
                       "k": kth, "hour": int(times[r].hour)})
        j = r  # resume bar may start the next run; pullback bars prevent
               # re-detection (they are DOWN).
    return {"events": events, "dropped": dropped}


def detect_second_conf(df: pd.DataFrame, win: tuple | None = None,
                       five_min: bool = False) -> dict:
    """§3. F3 detector (B-05 second-confirmation). After a decline (>= 3
    consecutive DOWN), c1 = first bar closing above its prior close, c2 =
    the next consecutive bar closing above its prior close. Only
    occurrences with both c1 and c2 are measured; others are dropped and
    counted. E1 = open of bar after c1, E2 = open of bar after c2."""
    pos = wpos(df, win, five_min)
    n = len(pos)
    if n < 3 + 2:
        return {"pairs": [], "dropped": 0}
    cl = df["Close"].to_numpy()[pos]
    op = df["Open"].to_numpy()[pos]
    down = cl < op
    pairs, dropped = [], 0
    j = 3
    while j < n:
        if not down[j - 2: j + 1].all():
            j += 1
            continue
        k = j + 1
        while k < n and cl[k] <= cl[k - 1]:
            k += 1
        if k + 1 >= n:               # no c1
            j += 1
            continue
        if cl[k + 1] <= cl[k]:       # c1 exists, no c2
            dropped += 1
            j += 1
            continue
        if k + 2 >= n:               # c2 exists, no forward bars
            dropped += 1
            j += 1
            continue
        if k + 1 + N_PRIMARY >= n or k + 2 + N_PRIMARY >= n:
            dropped += 1
        pairs.append({"c1_pos": k,
                      "e1_open": float(op[k + 1]),
                      "e2_open": float(op[k + 2]),
                      "hour": int(df.index[pos[k]].hour)})
        j = k + 1
    return {"pairs": pairs, "dropped": dropped}


# --------------------------------------------------------------------------
# §4 measurement
# --------------------------------------------------------------------------

def bootstrap_excess(a: np.ndarray, sample_b, rng) -> tuple:
    """Paired bootstrap of mean(a) - mean(sample_b(M)): B draws,
    percentile 2.5/97.5 CI, p = 2*min(P(diff<=0), P(diff>=0)). House
    convention (measure_intraday.py bootstrap_excess), seeded rng."""
    M = len(a)
    if M == 0:
        raise ValueError("bootstrap_excess: empty array — callers must "
                         "guard with the count floor")
    diffs = np.empty(B)
    for b in range(B):
        s_mean = a[rng.integers(0, M, size=M)].mean()
        diffs[b] = s_mean - sample_b(M).mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)),
            float(lo), float(hi), float(p))


def contrast_two(x: np.ndarray, y: np.ndarray, rng) -> tuple:
    """Bootstrap of mean(x) - mean(y), each resampled at its own size."""
    Mx, My = len(x), len(y)
    diffs = np.empty(B)
    for b in range(B):
        sx = x[rng.integers(0, Mx, size=Mx)].mean()
        sy = y[rng.integers(0, My, size=My)].mean()
        diffs[b] = sx - sy
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)),
            float(lo), float(hi), float(p))


def contrast_paired(d: np.ndarray, rng) -> tuple:
    """Bootstrap of mean(d) for a pre-paired difference array."""
    M = len(d)
    diffs = np.empty(B)
    for b in range(B):
        diffs[b] = d[rng.integers(0, M, size=M)].mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)),
            float(lo), float(hi), float(p))


def holm(fam: dict, family: str) -> dict:
    """Holm at ALPHA across the family's slots (pre-reg #19 §4). Family
    verdict: EDGE iff all slots Holm-rejected with CI-low > 0; FADE iff
    all with CI-upper < 0; mixed -> NO EDGE; any inconclusive slot ->
    INCONCLUSIVE."""
    order = sorted(fam, key=lambda k: fam[k].get("p", 1.0))
    for rank, k in enumerate(order, start=1):
        gate = ALPHA / (len(order) - rank + 1)
        fam[k]["holm_gate"] = gate
        fam[k]["holm_rejected"] = fam[k].get("p", 1.0) <= gate
    for k, r in fam.items():
        if r.get("n", 0) < MIN_SLOT:
            r["verdict"] = "INCONCLUSIVE"
        elif r["holm_rejected"] and r["ci_low"] > 0:
            r["verdict"] = "EDGE"
        elif r["holm_rejected"] and r["ci_upper"] < 0:
            r["verdict"] = "FADE"
        else:
            r["verdict"] = "NO EDGE"
    vs = [fam[k]["verdict"] for k in fam]
    if all(v == "EDGE" for v in vs):
        fam["_family"] = "EDGE"
    elif all(v == "FADE" for v in vs):
        fam["_family"] = "FADE"
    elif any(v == "INCONCLUSIVE" for v in vs):
        fam["_family"] = "INCONCLUSIVE"
    else:
        fam["_family"] = "NO EDGE"
    return fam


class Archive:
    """Window bar-dates loaded once; serves F1/F2/F3 events, the per-file
    and per-hour baseline pools, and the window position maps. Deterministic
    iteration everywhere (sorted rels)."""

    def __init__(self, d: int = D_PRIMARY, win: tuple | None = None,
                 five_min: bool = False, n: int = N_PRIMARY,
                 cost: float = COST_PRIMARY):
        self.d, self.win, self.five_min = d, win, five_min
        self.n, self.cost = n, cost
        self.files = {}        # rel -> df (window bar-dates only)
        self.f1_events = []    # long+short dicts (with rel, date, ticker)
        self.f2_events = []    # pullback-count dicts (k ordinal)
        self.f3_pairs = []     # second-confirmation pairs
        self.dropped_f1 = 0
        self.dropped_f2 = 0
        self.dropped_f3 = 0
        self._wpos_cache = {}
        self._load()

    def _load(self):
        m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for rel in sorted(f for f in m.get("files", {})
                          if f.split("/")[0] >= WINDOW_START):
            df = load_day(rel)
            self.files[rel] = df
            npos = len(self.wpos(rel))
            rv = detect_reversal(df, d=self.d, win=self.win,
                                 five_min=self.five_min)
            pc = detect_pullback_count(df, win=self.win,
                                       five_min=self.five_min)
            sc = detect_second_conf(df, win=self.win,
                                    five_min=self.five_min)
            date, ticker = rel.split("/")
            ticker = ticker[:-len(".parquet")]
            for ev in rv["long"] + rv["short"]:
                ev["rel"], ev["date"], ev["ticker"] = rel, date, ticker
                ev["npos"] = npos
                ev["valid_n"] = ev["e_pos"] + 1 + self.n < npos
                self.f1_events.append(ev)
            for ev in pc["events"]:
                ev["rel"], ev["date"], ev["ticker"] = rel, date, ticker
                ev["npos"] = npos
                ev["valid_n"] = ev["e_pos"] + 1 + self.n < npos
                self.f2_events.append(ev)
            for pr in sc["pairs"]:
                pr["rel"], pr["date"], pr["ticker"] = rel, date, ticker
                pr["npos"] = npos
                pr["both_valid"] = (pr["c1_pos"] + 1 + self.n < npos
                                    and pr["c1_pos"] + 2 + self.n < npos)
                self.f3_pairs.append(pr)
            self.dropped_f1 += rv["dropped"]
            self.dropped_f2 += pc["dropped"]
            self.dropped_f3 += sc["dropped"]
        self._build_pools()

    def wpos(self, rel: str) -> np.ndarray:
        if rel not in self._wpos_cache:
            self._wpos_cache[rel] = wpos(self.files[rel],
                                         win=None,
                                         five_min=self.five_min)
        return self._wpos_cache[rel]

    def _build_pools(self):
        """Per-file, per-hour baseline pools (long convention, gross): a
        baseline bar c must have c+1 and c+N within the window end, in the
        same hour bucket as the event's entry bar, and must not be an
        event entry bar. For the short slot the pools are sign-flipped at
        draw time."""
        hours = list(range(RTH_OPEN.hour, RTH_END.hour))
        self.same_pools = {}   # rel -> {hour: returns array}
        self.uni_pools = {h: [] for h in hours}
        entry_pos = {rel: {ev["e_pos"] for ev in self.f1_events
                           if ev["rel"] == rel} for rel in self.files}
        for rel, df in self.files.items():
            pos = self.wpos(rel)
            n = len(pos)
            if n <= self.n + 1:
                self.same_pools[rel] = {}
                continue
            op = df["Open"].to_numpy()[pos]
            cl = df["Close"].to_numpy()[pos]
            times = df.index[pos]
            c = np.arange(n)[: n - self.n - 1]
            if len(c) == 0:
                self.same_pools[rel] = {}
                continue
            rets = (cl[c + self.n] - op[c + 1]) / op[c + 1]
            per_hour = {}
            ep = entry_pos.get(rel, set())
            ep_arr = np.fromiter(ep, dtype=int, count=len(ep)) if ep \
                else np.array([], dtype=int)
            for h in range(RTH_OPEN.hour, RTH_END.hour):
                hm = times[c].hour == h
                keep = hm & ~np.isin(c, ep_arr)
                if keep.any():
                    per_hour[h] = rets[keep]
            self.same_pools[rel] = per_hour
            for h, v in per_hour.items():
                self.uni_pools[h].append(v)
        self.uni_pools = {h: np.concatenate(v) if v else np.array([])
                          for h, v in self.uni_pools.items()}

    # -- event arrays -----------------------------------------------------
    def rets_for(self, evs: list, n: int | None = None,
                 cost: float | None = None, flip: bool = False) -> np.ndarray:
        """(C[wpos[e_pos+n]] - entry_open)/entry_open - cost per event,
        sign-flipped for the short slot. Events without the forward window
        are skipped by the caller."""
        if n is None:
            n = self.n
        if cost is None:
            cost = self.cost
        out = []
        for ev in evs:
            w = self.wpos(ev["rel"])
            cl = self.files[ev["rel"]]["Close"].to_numpy()
            gross = (cl[w[ev["e_pos"] + n]] - ev["entry_open"]) \
                / ev["entry_open"]
            out.append((-gross if flip else gross) - cost)
        return np.array(out)

    def hour_of(self, ev: dict) -> int:
        w = self.wpos(ev["rel"])
        return int(self.files[ev["rel"]].index[w[ev["e_pos"]]].hour)

    # -- F1 baseline sampling ---------------------------------------------
    def sample_f1(self, evs: list, rng, kind: str, flip: bool) -> np.ndarray:
        """Bootstrap baseline draw for F1: for each of M events, sample a
        random baseline bar in the same hour bucket (same-ticker pool per
        event's file, or the random-universe pool). Sign-flip for the short
        slot."""
        M = len(evs)
        out = np.empty(M)
        for i in range(M):
            ev = evs[rng.integers(0, M)]
            h = ev["hour"]
            pool = (self.same_pools[ev["rel"]].get(h)
                    if kind == "same" else self.uni_pools.get(h))
            if pool is None or len(pool) == 0:
                out[i] = 0.0
            else:
                v = pool[rng.integers(0, len(pool))]
                out[i] = -v if flip else v
        return out

    # -- F2 baseline-adjusted contrast ------------------------------------
    def f2_adjusted(self, evs: list, kind: str) -> np.ndarray:
        """Each event's return minus the mean of its hour-matched baseline
        pool (same-ticker or universe) — the baseline-adjusted leg returns
        for the F2 'both baseline pairs' rows."""
        out = []
        for ev in evs:
            h = ev["hour"]
            pool = (self.same_pools[ev["rel"]].get(h)
                    if kind == "same" else self.uni_pools.get(h))
            base = pool.mean() if (pool is not None and len(pool)) else 0.0
            w = self.wpos(ev["rel"])
            cl = self.files[ev["rel"]]["Close"].to_numpy()
            r = (cl[w[ev["e_pos"] + self.n]] - ev["entry_open"]) \
                / ev["entry_open"] - self.cost
            out.append(r - base)
        return np.array(out)

    def pair_rets(self, pairs: list, entry_key: str) -> np.ndarray:
        """F3 leg returns. entry_key 'e1_open' -> entry open of bar after
        c1 (C[wpos[c1+1+n]] - e1_open)/e1_open - cost; 'e2_open' -> entry
        open of bar after c2 (C[wpos[c1+2+n]] - e2_open)/e2_open - cost."""
        out = []
        for pr in pairs:
            w = self.wpos(pr["rel"])
            cl = self.files[pr["rel"]]["Close"].to_numpy()
            k = pr["c1_pos"]
            if entry_key == "e1_open":
                gross = (cl[w[k + 1 + self.n]] - pr["e1_open"]) \
                    / pr["e1_open"]
            else:
                gross = (cl[w[k + 2 + self.n]] - pr["e2_open"]) \
                    / pr["e2_open"]
            out.append(gross - self.cost)
        return np.array(out)


def run_measurement(a: Archive, rng) -> dict:
    """§4 families on the primary parameters. Returns the results dict."""
    res = {"n_f1_events": len(a.f1_events),
           "n_f1_valid": sum(1 for ev in a.f1_events if ev["valid_n"]),
           "n_f1_dropped": a.dropped_f1,
           "n_f2_events": len(a.f2_events),
           "n_f2_valid": sum(1 for ev in a.f2_events if ev["valid_n"]),
           "n_f2_dropped": a.dropped_f2,
           "n_f3_pairs": len(a.f3_pairs),
           "n_f3_both_valid": sum(1 for pr in a.f3_pairs
                                  if pr["both_valid"]),
           "n_f3_dropped": a.dropped_f3,
           "dropped_note": "events without the forward window (or with only "
                           "one confirmation candle for F3) are dropped and "
                           "counted (pre-reg #19 §4)"}

    # ---- F1: reversal new-high, 2 Holm slots (long, short) --------------
    fam1 = {}
    for slot, dir_name in (("long", "long"), ("short", "short")):
        evs = [ev for ev in a.f1_events
               if ev["dir"] == dir_name and ev["valid_n"]]
        if len(evs) == 0:
            fam1[slot] = {"n": 0, "mean_ret": None, "est": None,
                          "ci_low": None, "ci_upper": None, "p": 1.0}
            continue
        rets = a.rets_for(evs, flip=(dir_name == "short"))
        flip = dir_name == "short"
        # Primary (Holm-feed): random-universe hour-matched baseline.
        e_uni = bootstrap_excess(
            rets, lambda M: a.sample_f1(evs, rng, "uni", flip), rng)
        # Secondary: same-ticker hour-matched baseline (reported).
        e_same = bootstrap_excess(
            rets, lambda M: a.sample_f1(evs, rng, "same", flip), rng)
        fam1[slot] = {"n": int(len(evs)), "mean_ret": float(rets.mean()),
                      "excess_universe": {"est": e_uni[0],
                                          "ci_low": e_uni[2],
                                          "ci_upper": e_uni[3],
                                          "p": e_uni[4]},
                      "excess_same_ticker": {"est": e_same[0],
                                             "ci_low": e_same[2],
                                             "ci_upper": e_same[3],
                                             "p": e_same[4]},
                      "est": e_uni[0], "ci_low": e_uni[2],
                      "ci_upper": e_uni[3], "p": e_uni[4]}
    res["f1"] = holm(fam1, "F1")

    # ---- F2: pullback-count, 1 Holm slot (early - late) ----------------
    early = [ev for ev in a.f2_events if ev["k"] <= 2 and ev["valid_n"]]
    late = [ev for ev in a.f2_events if ev["k"] >= 3 and ev["valid_n"]]
    fam2 = {}
    if len(early) < MIN_SLOT or len(late) < MIN_SLOT:
        fam2["early_minus_late"] = {
            "n": min(len(early), len(late)), "n_early": len(early),
            "n_late": len(late), "mean_early": None, "mean_late": None,
            "est": None, "ci_low": None, "ci_upper": None, "p": 1.0}
    else:
        er = a.rets_for(early)
        lr = a.rets_for(late)
        e = contrast_two(er, lr, rng)
        adj_same = contrast_two(a.f2_adjusted(early, "same"),
                                a.f2_adjusted(late, "same"), rng)
        adj_uni = contrast_two(a.f2_adjusted(early, "uni"),
                               a.f2_adjusted(late, "uni"), rng)
        fam2["early_minus_late"] = {
            "n": int(min(len(early), len(late))),
            "n_early": int(len(early)), "n_late": int(len(late)),
            "mean_early": float(er.mean()), "mean_late": float(lr.mean()),
            "adj_same_ticker": {"est": adj_same[0], "ci_low": adj_same[2],
                                "ci_upper": adj_same[3], "p": adj_same[4]},
            "adj_universe": {"est": adj_uni[0], "ci_low": adj_uni[2],
                             "ci_upper": adj_uni[3], "p": adj_uni[4]},
            "est": e[0], "ci_low": e[2], "ci_upper": e[3], "p": e[4]}
    res["f2"] = holm(fam2, "F2")

    # ---- F3: second-confirmation, 1 Holm slot (paired E2-E1) -----------
    pairs = [pr for pr in a.f3_pairs if pr["both_valid"]]
    fam3 = {}
    if len(pairs) < MIN_SLOT:
        fam3["e2_minus_e1"] = {"n": 0, "n_pairs": len(pairs),
                               "est": None, "ci_low": None,
                               "ci_upper": None, "p": 1.0}
    else:
        e1 = a.pair_rets(pairs, entry_key="e1_open")
        e2 = a.pair_rets(pairs, entry_key="e2_open")
        e = contrast_paired(e2 - e1, rng)
        fam3["e2_minus_e1"] = {"n": int(len(pairs)),
                               "n_pairs": int(len(pairs)),
                               "mean_e1": float(e1.mean()),
                               "mean_e2": float(e2.mean()),
                               "est": e[0], "ci_low": e[2],
                               "ci_upper": e[3], "p": e[4]}
    res["f3"] = holm(fam3, "F3")

    # ---- Measurement rows (no verdicts) ---------------------------------
    res["rows"] = measurement_rows(a)
    return res


def measurement_rows(a: Archive) -> dict:
    rows = {}

    # (a) R:R geometry per direction (target = day-high/low-so-far, stop =
    # the decline low / rise high). Long: (T-O[e+1])/(O[e+1]-S); short:
    # (O[e+1]-T)/(S-O[e+1]).
    rr_long, rr_short, deg_long, deg_short = [], [], 0, 0
    for ev in a.f1_events:
        if ev["dir"] == "long":
            if ev["entry_open"] > ev["stop"]:
                rr_long.append((ev["target"] - ev["entry_open"]) /
                               (ev["entry_open"] - ev["stop"]))
            else:
                deg_long += 1
        else:
            if ev["stop"] > ev["entry_open"]:
                rr_short.append((ev["entry_open"] - ev["target"]) /
                                (ev["stop"] - ev["entry_open"]))
            else:
                deg_short += 1
    rows["rr_long"] = {"n": int(len(rr_long)),
                       "frac_ge_2": float((np.array(rr_long) >= 2.0).mean())
                       if rr_long else None,
                       "n_degenerate_entry_le_stop": deg_long,
                       **_statistics(rr_long)}
    rows["rr_short"] = {"n": int(len(rr_short)),
                        "frac_ge_2": float((np.array(rr_short) >= 2.0).mean())
                        if rr_short else None,
                        "n_degenerate_entry_le_stop": deg_short,
                        **_statistics(rr_short)}

    # (b) per-k pullback means and win rates (F2)
    krows = {}
    for ev in a.f2_events:
        if not ev["valid_n"]:
            continue
        k = ev["k"] if ev["k"] <= 4 else "5+"
        krows.setdefault(k, []).append(ev)
    rows["pullback_by_k"] = {}
    for k in sorted(krows, key=lambda x: (x if isinstance(x, int) else 99)):
        evs = krows[k]
        r = a.rets_for(evs)
        rows["pullback_by_k"][str(k)] = {
            "n": int(len(evs)), "mean": float(r.mean()),
            "win_rate": float((r > 0).mean()),
            **_statistics(r)}

    # (c) name-day / ticker / bar-date F1 breakdowns (signed long+short)
    valid = [ev for ev in a.f1_events if ev["valid_n"]]
    rets = a.rets_for(valid, flip=False)
    # signed: short legs use the flipped array
    rets_signed = []
    for i, ev in enumerate(valid):
        w = a.wpos(ev["rel"])
        cl = a.files[ev["rel"]]["Close"].to_numpy()
        gross = (cl[w[ev["e_pos"] + a.n]] - ev["entry_open"]) \
            / ev["entry_open"]
        signed = gross if ev["dir"] == "long" else -gross
        rets_signed.append(signed - a.cost)
    rets_signed = np.array(rets_signed)
    by_date, by_ticker = {}, {}
    for ev, r in zip(valid, rets_signed):
        by_date.setdefault(ev["date"], []).append(r)
        by_ticker.setdefault(ev["ticker"], []).append(r)
    rows["by_bar_date"] = {k: float(np.mean(v)) for k, v in
                           sorted(by_date.items())}
    rows["by_ticker"] = {k: float(np.mean(v)) for k, v in
                         sorted(by_ticker.items())}

    # (d) entry-bar gap distribution (F1 events; real index minutes)
    gaps = []
    for ev in valid:
        w = a.wpos(ev["rel"])
        if ev["e_pos"] < 1:
            continue
        idx = a.files[ev["rel"]].index
        t = idx[w[ev["e_pos"]]]
        tp = idx[w[ev["e_pos"] - 1]]
        gaps.append(int((t - tp) / np.timedelta64(1, "m")))
    rows["entry_gaps_min"] = {"n": len(gaps),
                              "frac_gt_2min": float((np.array(gaps) > 2).mean())
                              if gaps else None,
                              **_statistics(gaps)}

    # (e) hour-of-day profile of F1 events (pre-reg #22 cross-check).
    # Bucket labels are the actual ET minute ranges covered by the hour.
    prof = {}
    for h in range(RTH_OPEN.hour, RTH_END.hour):
        lo = "09:30" if h == RTH_OPEN.hour else f"{h:02d}:00"
        hi = f"{h + 1:02d}:00"
        h_ret = [r for ev, r in zip(valid, rets_signed) if ev["hour"] == h]
        h_n = sum(1 for ev in valid if ev["hour"] == h)
        prof[f"{lo}-{hi}"] = {"n": h_n,
                              "mean_ret": float(np.mean(h_ret))
                              if h_ret else None}
    rows["hour_of_day"] = prof
    return rows


def _statistics(vals) -> dict:
    vals = np.asarray(vals, dtype=float)
    return _stat(vals, ("mean", "median", "p10", "p90"))


def _stat(vals: np.ndarray, keys: tuple) -> dict:
    if len(vals) == 0:
        return {k: None for k in keys}
    out = {}
    for k in keys:
        out[k] = float({"mean": np.mean, "median": np.median,
                        "p10": lambda v: np.percentile(v, 10),
                        "p90": lambda v: np.percentile(v, 90)}[k](vals))
    return out


# --------------------------------------------------------------------------
# sensitivities (exploratory; computed, reported, NO verdicts)
# --------------------------------------------------------------------------

def run_sensitivities(a: Archive, rng) -> dict:
    out = {}
    for label, kwargs in (("S-D2", {"d": 2}), ("S-D5", {"d": 5}),
                          ("S-5M", {"five_min": True})):
        aa = Archive(**kwargs)
        r = run_measurement(aa, np.random.default_rng(SEED))
        out[label] = {"n_f1_events": len(aa.f1_events),
                      "f1": r["f1"]["_family"],
                      "f1_long": r["f1"]["long"].get("mean_ret"),
                      "f1_long_n": r["f1"]["long"].get("n"),
                      "f2": r["f2"]["_family"],
                      "f3": r["f3"]["_family"]}
    for label, cost in (("S-C05", 0.0005), ("S-C30", 0.0030)):
        aa = Archive(cost=cost)
        r = run_measurement(aa, np.random.default_rng(SEED))
        out[label] = {"n_f1_events": len(aa.f1_events),
                      "f1": r["f1"]["_family"],
                      "f1_long_mean": r["f1"]["long"].get("mean_ret"),
                      "f2": r["f2"]["_family"],
                      "f3": r["f3"]["_family"]}
    return out


# --------------------------------------------------------------------------
# floors (§5) and report
# --------------------------------------------------------------------------

def check_floors(a: Archive) -> dict:
    valid = [ev for ev in a.f1_events if ev["valid_n"]]
    bar_dates = sorted({rel.split("/")[0] for rel in a.files})
    event_dates = sorted({ev["date"] for ev in valid})
    tickers = {ev["ticker"] for ev in valid}
    return {"window_bar_dates": len(bar_dates),
            "events_f1_valid": len(valid),
            "tickers": len(tickers),
            "dates_with_events": len(event_dates),
            "floors": FLOORS,
            "met": (len(bar_dates) >= FLOORS["min_bar_dates"]
                    and len(valid) >= FLOORS["min_events"]
                    and len(tickers) >= FLOORS["min_tickers"]
                    and len(event_dates) >= FLOORS["min_dates_with_events"])}


def write_report(results: dict, audit: dict) -> None:
    L = []
    L.append("# Pre-registration #19 intraday entry-timing measure report — "
             "reversal new-high / pullback-count / second-confirmation (1-min)")
    L.append("")
    L.append(f"- Mode: {results['mode']}")
    L.append(f"- FROZEN_SHA: {results['frozen_sha']}")
    L.append(f"- Window: bar-dates >= {WINDOW_START}")
    if results["mode"] == "audit-only":
        L.append("")
        L.append("## Audit-only (no returns computed)")
        L.append("")
        L.append(f"- Audit: **{'PASSED' if audit['passed'] else 'FAILED'}**")
        for e in audit.get("errors", []):
            L.append(f"- ERROR: {e}")
        L.append("")
        L.append("### Detection event counts (pre-reg #19 §5 audit allowance)")
        L.append("")
        L.append("| bar-date | F1 long | F1 short | F1 dropped | F2 seqs | "
                 "F2 dropped | F3 pairs | F3 dropped |")
        L.append("|---|---|---|---|---|---|---|---|")
        for d in sorted(results.get("events_by_date", {})):
            c = results["events_by_date"][d]
            L.append(f"| {d} | {c['long']} | {c['short']} | {c['f1_dropped']} "
                     f"| {c['f2']} | {c['f2_dropped']} | {c['f3']} | "
                     f"{c['f3_dropped']} |")
        L.append("")
    else:
        L.append("")
        def _f(x, fmt="{:+.4f}"):
            return fmt.format(x) if x is not None else "-"

        L.append("## F1 — reversal new-high (long/short), N=60, COST 0.15%")
        L.append("")
        L.append(f"Family verdict: **{results['f1']['_family']}**")
        for k in ("long", "short"):
            r = results["f1"][k]
            u = r.get("excess_universe", {})
            s = r.get("excess_same_ticker", {})
            L.append(f"- {k}: n={r['n']}, mean {_f(r.get('mean_ret'))}, "
                     f"excess vs universe (primary) {_f(u.get('est'))} "
                     f"(CI {_f(u.get('ci_low'))}..{_f(u.get('ci_upper'))}, "
                     f"p={u.get('p', 1.0):.3f}), same-ticker (secondary) "
                     f"{_f(s.get('est'))} (CI {_f(s.get('ci_low'))}.."
                     f"{_f(s.get('ci_upper'))}, p={s.get('p', 1.0):.3f}), "
                     f"Holm {_f(r.get('holm_gate'), '{:.3f}')}, "
                     f"{'rejected' if r.get('holm_rejected') else 'not'}) — "
                     f"{r['verdict']}")
        L.append("")
        L.append("## F2 — pullback-count (early k<=2 vs late k>=3)")
        L.append("")
        L.append(f"Family verdict: **{results['f2']['_family']}**")
        r = results["f2"]["early_minus_late"]
        L.append(f"- early − late: n_early={r.get('n_early')}, "
                 f"n_late={r.get('n_late')}, mean_early {_f(r.get('mean_early'))}, "
                 f"mean_late {_f(r.get('mean_late'))}, contrast {_f(r.get('est'))} "
                 f"(CI {_f(r.get('ci_low'))}..{_f(r.get('ci_upper'))}, "
                 f"p={r.get('p', 1.0):.3f}) — {r['verdict']}")
        L.append("")
        L.append("## F3 — second-confirmation (E2 − E1, paired)")
        L.append("")
        L.append(f"Family verdict: **{results['f3']['_family']}**")
        r = results["f3"]["e2_minus_e1"]
        L.append(f"- E2−E1: n={r.get('n_pairs')}, mean_e1 "
                 f"{_f(r.get('mean_e1'))}, mean_e2 {_f(r.get('mean_e2'))}, "
                 f"contrast {_f(r.get('est'))} (CI {_f(r.get('ci_low'))}.."
                 f"{_f(r.get('ci_upper'))}, p={r.get('p', 1.0):.3f}) — "
                 f"{r['verdict']}")
        L.append("")
        L.append("## Measurement rows (no verdicts)")
        L.append("")
        rows = results["rows"]
        rr = rows["rr_long"]
        L.append(f"- R:R long: mean {_f(rr['mean'], '{:.2f}')}, "
                 f"median {_f(rr['median'], '{:.2f}')}, frac ≥2:1 "
                 f"{_f(rr['frac_ge_2'], '{:.3f}')} (n={rr['n']}, degenerate "
                 f"{rr['n_degenerate_entry_le_stop']})")
        rrs = rows["rr_short"]
        L.append(f"- R:R short: mean {_f(rrs['mean'], '{:.2f}')}, "
                 f"median {_f(rrs['median'], '{:.2f}')}, frac ≥2:1 "
                 f"{_f(rrs['frac_ge_2'], '{:.3f}')} (n={rrs['n']}, degenerate "
                 f"{rrs['n_degenerate_entry_le_stop']})")
        L.append(f"- F1 events: {results['n_f1_valid']} measured of "
                 f"{results['n_f1_events']} detected (dropped "
                 f"{results['n_f1_dropped']}); F2 {results['n_f2_valid']} of "
                 f"{results['n_f2_events']}; F3 {results['n_f3_both_valid']} "
                 f"pairs of {results['n_f3_pairs']}")
        L.append("")
        L.append("### Pullback count by k (F2)")
        L.append("")
        L.append("| k | n | mean | win rate |")
        L.append("|---|---|---|---|")
        for k, v in rows["pullback_by_k"].items():
            L.append(f"| {k} | {v['n']} | {v['mean']:.4f} | "
                     f"{v['win_rate']:.3f} |")
        L.append("")
        L.append("### Hour-of-day profile of F1 events (pre-reg #22 cross-check)")
        L.append("")
        L.append("| hour (ET) | n | mean ret |")
        L.append("|---|---|---|")
        for h, v in rows["hour_of_day"].items():
            L.append(f"| {h} | {v['n']} | {_f(v['mean_ret'])} |")
        L.append("")
        L.append("## Sensitivities (exploratory, NO verdicts)")
        L.append("")
        for k, v in results["sensitivities"].items():
            L.append(f"- {k}: {v}")
        L.append("")
    L.append("## §6 audit")
    L.append("")
    L.append(f"- Audit: **{'PASSED' if audit['passed'] else 'FAILED'}**")
    for e in audit.get("errors", []):
        L.append(f"- ERROR: {e}")
    L.append("")
    REPORT_PATH.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {REPORT_PATH}")


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--audit-only", action="store_true",
                    help="§6 audit + detection counts only (no returns)")
    args = ap.parse_args()

    self_check()
    if not RAW_DIR.exists() or not MANIFEST_PATH.exists():
        print("FATAL: archive missing", file=sys.stderr)
        return 3

    audit = audit_archive()
    if not audit["passed"]:
        print("REFUSED: §6 audit FAILED — campaign void until the archive "
              "is restored or the failure is explained (pre-reg #19 §6).",
              file=sys.stderr)
        for e in audit["errors"]:
            print(f"  - {e}", file=sys.stderr)
        return 1

    if args.audit_only:
        # Detection counts per bar-date (pre-reg #19 §5: allowed
        # pre-measurement; computes no returns).
        ev_by_date = {}
        m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for rel in sorted(m.get("files", {})):
            d = rel.split("/")[0]
            df = load_day(rel)
            rv = detect_reversal(df)
            pc = detect_pullback_count(df)
            sc = detect_second_conf(df)
            c = ev_by_date.setdefault(d, {"long": 0, "short": 0,
                                          "f1_dropped": 0, "f2": 0,
                                          "f2_dropped": 0, "f3": 0,
                                          "f3_dropped": 0})
            c["long"] += len(rv["long"])
            c["short"] += len(rv["short"])
            c["f1_dropped"] += rv["dropped"]
            c["f2"] += len(pc["events"])
            c["f2_dropped"] += pc["dropped"]
            c["f3"] += len(sc["pairs"])
            c["f3_dropped"] += sc["dropped"]
        results = {"mode": "audit-only", "frozen_sha": FROZEN_SHA,
                   "measure_code_sha256": sha_bytes(Path(__file__).read_bytes()),
                   "events_by_date": ev_by_date}
        write_report(results, audit)
        print(f"measure_code_sha256: {sha_bytes(Path(__file__).read_bytes())}")
        print(f"report sha256: {sha_file(REPORT_PATH)}")
        return 0

    a = Archive()
    floors = check_floors(a)
    if not floors["met"]:
        print(f"REFUSED: measurement floors unmet (pre-reg #19 §5): "
              f"{floors}", file=sys.stderr)
        return 2

    rng = np.random.default_rng(SEED)
    res = run_measurement(a, rng)
    res["n_f1"] = sum(1 for ev in a.f1_events if ev["valid_n"])
    res["floors"] = floors
    res["sensitivities"] = run_sensitivities(a, rng)
    res["audit"] = audit
    res["frozen_sha"] = FROZEN_SHA
    res["measure_code_sha256"] = sha_bytes(Path(__file__).read_bytes())
    res["seed"] = SEED
    res["alpha"] = ALPHA
    res["mode"] = "measure"
    RESULTS_PATH.write_text(json.dumps(res, indent=2), encoding="utf-8")
    write_report(res, audit)
    print(f"wrote {RESULTS_PATH}")
    print(f"measure_code_sha256: {res['measure_code_sha256']}")
    print(f"results sha256: {sha_file(RESULTS_PATH)}")
    print(f"report  sha256: {sha_file(REPORT_PATH)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

