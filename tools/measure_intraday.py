"""Pre-registration #15 measurement tool — B-01 micro pullback on 1-min bars.

Implements PREREGISTRATION.md §Pre-registration #15 exactly:
  * §3 the detector (frozen parameters and sensitivities),
  * §4 the measurement (F1/F2/F3 families, baselines, measurement rows),
  * §5 the sample-size floors and the one-shot rule (measurement is REFUSED
    until the floors are met; audit-only mode computes no returns at all),
  * §6 the archive-integrity audit (continuous-capture gate).

Frozen 2026-08-19, before any measurement. The module sha is asserted at
run (FROZEN_SHA below, hashing the file with its own FROZEN_SHA hex
blanked — the fixed-point convention; measure_code_sha256 additionally
records the raw file sha, house-style): any byte change invalidates the
campaign.

Modes:
  python -X utf8 tools/measure_intraday.py --audit-only
      §6 audit + detection event counts + entry metadata only. Computes NO
      return of any kind (per pre-reg §5: no forward-return number before
      the floors are met). Exit 0 = audit clean; 1 = audit FAILED.
  python -X utf8 tools/measure_intraday.py
      Full measurement. Requires the §5 floors; otherwise REFUSES (exit 2).
      Writes data/cache/intraday_measure_report.md +
      intraday_measure_results.json, prints their sha256 for the
      determinism check (two runs must byte-compare).

Exit codes: 0 ok, 1 audit/integrity failure, 2 floors unmet (refused),
3 input error.

Spec mapping (pre-reg §3/§4; the primary column):
  R=3, P=2, double-bottom required, RTH 09:30-16:00 ET, N=60, COST 0.0015,
  B=1000, seed 20260819, alpha 0.05, window start bar-date 2026-08-19.
  Sensitivities: S-R4 (R=4), S-R2 (R=2), S-P3 (P=3), S-DB (no double
  bottom), S-WIN (07:00-10:00 ET), S-GAP (detection bars <= 2 min apart),
  S-N15/S-N120/S-N240 (N), S-C05/S-C30 (COST). All sensitivities are
  exploratory: computed, reported, NO verdicts (pre-reg §4). For S-WIN the
  day-high-so-far T starts at 07:00 (window open); for S-P3 the stop is the
  low of the p pullback bars and the double-bottom check is on the first
  two bars (the pre-reg's L1/L2 definition), per §3.
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
UNIVERSE_DIR = ROOT / "data" / "cache"
OUT_DIR = ROOT / "data" / "cache"
REPORT_PATH = OUT_DIR / "intraday_measure_report.md"
RESULTS_PATH = OUT_DIR / "intraday_measure_results.json"

TZ = ZoneInfo("America/New_York")
RTH_OPEN = dtime(9, 30)
RTH_END = dtime(16, 0)
WIN_OPEN = dtime(7, 0)      # S-WIN window start
WIN_END = dtime(10, 0)      # S-WIN window end
WINDOW_START = "2026-08-19"  # first bar-date of the measurement window

# Primary parameters (pre-reg §3/§4) — frozen.
R_PRIMARY = 3
P_PRIMARY = 2
N_PRIMARY = 60
COST_PRIMARY = 0.0015
B = 1000
SEED = 20260819
ALPHA = 0.05
FLOORS = {"min_bar_dates": 20, "min_events": 2000,
          "min_tickers": 100, "min_dates_with_events": 15}
MIN_SLOT = 100  # per-slot count floor (house)

# Freeze sha (house convention, measure.py/measure_divergence.py): the
# sha of this file with its own FROZEN_SHA hex blanked to 64 zeros — a
# well-defined fixed point (a file cannot hash to a value embedded in
# itself). Any byte change outside the blanked hex breaks the assertion.
FROZEN_SHA = "765ff1df23c80c006104d2f28b754593e3401e256132115207a161ebf5fdc6f5"


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
    if not FROZEN_SHA:
        print("FATAL: FROZEN_SHA is empty — tool not frozen. Refusing to run.",
              file=sys.stderr)
        sys.exit(3)
    actual = hash_self()
    if actual != FROZEN_SHA:
        print(f"FATAL: measure_intraday.py sha mismatch — frozen "
              f"{FROZEN_SHA[:12]}…, on disk {actual[:12]}…. A frozen "
              f"measurement tool must not change.", file=sys.stderr)
        sys.exit(1)


def window_mask(idx: pd.DatetimeIndex, win: tuple | None) -> np.ndarray:
    """Bars in the detection window: RTH 09:30-16:00, or the S-WIN window."""
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

    # Pull chain: prev_pull_sha256 must hash the prior record (root first).
    for i, p in enumerate(pulls):
        expect = ("root" if i == 0 else sha_bytes(
            json.dumps(pulls[i - 1], sort_keys=True).encode("utf-8")))
        ok = p.get("prev_pull_sha256") == expect
        ev["chain"].append({"pull_id": p["pull_id"], "ok": ok})
        if not ok:
            ev["passed"] = False
            ev["errors"].append(
                f"pull {p['pull_id']} prev_pull_sha256 mismatch")

    # Ledger/files: every ledger entry present + hash-matched; no orphans.
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

    # Repairs: list reasons (judgment per §6 at measurement time).
    if REPAIRS_PATH.exists():
        rep = json.loads(REPAIRS_PATH.read_text(encoding="utf-8"))
        ev["repairs"] = [{"path": r.get("path"), "reason": r.get("reason")}
                         for r in rep.get("repairs", [])]

    # Window pulls: universe attribution + blind-capture check. Every file
    # with bar-date >= WINDOW_START must trace to a blind full-universe pull
    # (its tickers_requested == the row count of its own universe file).
    pull_by_id = {p["pull_id"]: p for p in pulls}
    rows_of = {}
    seen = set()
    for rel in sorted(files):
        if rel.split("/")[0] < WINDOW_START:
            continue  # pre-window bar-dates are outside the campaign
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
            ufp = UNIVERSE_DIR / uf
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
# §3 detector
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


def detect_b01(df: pd.DataFrame, r: int = R_PRIMARY,
               p: int = P_PRIMARY, db: bool = True,
               win: tuple | None = None, gap_min: int | None = None,
               n_need: int = N_PRIMARY) -> dict:
    """§3 detector on one day file. Returns
      events:   list of dicts (one per entry signal), positions relative
                to the detection-window bar order
      chase:    list of chase-event dicts (§4 F3: run-up new-high bars)
      dropped:  count of detected events whose e+N exceeds the window end
    All info complete at the close of the entry bar e; entry = open e+1.
    n_need: the forward window that must exist for F1 (events without it
    are 'dropped and counted' per §4)."""
    idx = df.index
    mask = window_mask(idx, win)
    pos = np.flatnonzero(mask)
    n = len(pos)
    if n < r + p + 2:
        return {"events": [], "chase": [], "dropped": 0}

    hi = df["High"].to_numpy()[pos]
    lo = df["Low"].to_numpy()[pos]
    op = df["Open"].to_numpy()[pos]
    cl = df["Close"].to_numpy()[pos]
    times = idx[pos]
    up = cl > op
    down = cl < op

    if gap_min is not None:
        diffs_min = np.diff(times).astype("timedelta64[m]").astype(int)
        contiguous = np.concatenate(([True], diffs_min <= gap_min))

    events, chase = [], []
    dropped = 0
    j = r - 1
    while j < n:
        # Run-up of r consecutive UP bars ending at j.
        if not up[j - r + 1: j + 1].all():
            j += 1
            continue
        # Chase events from this run-up (§4 F3): every run-up bar c with
        # High[c] > High[c-1] (entry = open c+1).
        for c in range(j - r + 1, j + 1):
            if c >= 1 and hi[c] > hi[c - 1] and c + 1 < n:
                chase.append({"e_pos": c, "entry_open": float(op[c + 1])})
        # Pullback of p consecutive DOWN bars after the run-up.
        if j + p >= n or not down[j + 1: j + p + 1].all():
            j += 1
            continue
        l1 = lo[j + 1]
        l2 = lo[j + 2] if p >= 2 else l1
        if db and l2 < l1:
            j += 1
            continue
        stop = float(lo[j + 1: j + p + 1].min())
        # Entry: first bar after the pullback with High > prev High.
        k = j + p + 1
        while k < n and hi[k] <= hi[k - 1]:
            k += 1
        if k + 1 >= n:
            j += 1
            continue
        if gap_min is not None and not contiguous[j - r + 1: k + 1].all():
            j += 1
            continue
        target = float(hi[j - r + 1: k + 1].max())  # T = day-high-so-far
        if k + n_need >= n:
            dropped += 1
        ev = {"e_pos": k, "entry_open": float(op[k + 1]), "stop": stop,
              "target": target, "hour": int(times[k].hour)}
        events.append(ev)
        j = k + 1  # no overlapping detections
    return {"events": events, "chase": chase, "dropped": dropped}


# --------------------------------------------------------------------------
# §4 measurement
# --------------------------------------------------------------------------

def bootstrap_excess(a: np.ndarray, sample_b, rng) -> tuple:
    """Paired bootstrap of mean(a) - mean(sample_b(M)): B=1000 draws,
    percentile 2.5/97.5 CI, p = 2*min(P(diff<=0), P(diff>=0)). House
    convention (measure.py bootstrap_excess), seeded rng."""
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


def holm(fam: dict, family: str) -> dict:
    """Holm at ALPHA across the family's slots (pre-reg §4). Family
    verdict: EDGE iff both slots Holm-rejected with CI-low > 0; FADE iff
    both with CI-upper < 0; mixed -> NO EDGE; any inconclusive slot ->
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
    """Window bar-dates loaded once; serves events, chase events, per-file
    pools and the window position maps to the families. Deterministic
    iteration everywhere (sorted rels)."""

    def __init__(self, r: int = R_PRIMARY, p: int = P_PRIMARY,
                 db: bool = True, win: tuple | None = None,
                 gap_min: int | None = None):
        self.r, self.p, self.db, self.win, self.gap_min = r, p, db, win, gap_min
        self.files = {}     # rel -> df (window bar-dates only)
        self.events = []    # event dicts (with rel, date, ticker, npos)
        self.chase = []     # chase dicts (rel, e_pos, npos)
        self.dropped = 0
        self._wpos_cache = {}
        self._load()

    def _load(self):
        m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for rel in sorted(f for f in m.get("files", {})
                          if f.split("/")[0] >= WINDOW_START):
            df = load_day(rel)
            self.files[rel] = df
            npos = len(self.wpos(rel))
            det = detect_b01(df, r=self.r, p=self.p, db=self.db,
                             win=self.win, gap_min=self.gap_min,
                             n_need=N_PRIMARY)
            date, ticker = rel.split("/")
            ticker = ticker[:-len(".parquet")]
            for ev in det["events"]:
                ev["rel"] = rel
                ev["date"] = date
                ev["ticker"] = ticker
                ev["npos"] = npos
                ev["valid_n"] = ev["e_pos"] + N_PRIMARY < npos
                self.events.append(ev)
            for ch in det["chase"]:
                ch["rel"] = rel
                ch["npos"] = npos
                self.chase.append(ch)
            self.dropped += det["dropped"]
        self._build_pools()

    def wpos(self, rel: str) -> np.ndarray:
        """Absolute row indices of the detection-window bars for a file."""
        if rel not in self._wpos_cache:
            self._wpos_cache[rel] = np.flatnonzero(
                window_mask(self.files[rel].index, self.win))
        return self._wpos_cache[rel]

    def _build_pools(self):
        """Per-file, per-hour baseline pools for the same-ticker and
        random-universe baselines (§4). A baseline bar c must have c+1 and
        c+N within the window end, in the same hour bucket as the event's
        entry bar, and must not be an event entry bar."""
        if self.win is not None:
            hours = list(range(self.win[0].hour, self.win[1].hour))
        else:
            hours = list(range(RTH_OPEN.hour, RTH_END.hour))
        self.same_pools = {}   # rel -> {hour: returns array}
        self.same_reach = {}   # rel -> {hour: reach flags array}
        self.uni_pools = {h: [] for h in hours}    # hour -> list of arrays
        self.uni_reach = {h: [] for h in hours}
        entry_pos = {rel: {ev["e_pos"] for ev in self.events
                           if ev["rel"] == rel} for rel in self.files}
        for rel, df in self.files.items():
            pos = self.wpos(rel)
            n = len(pos)
            if n <= N_PRIMARY + 1:
                self.same_pools[rel] = {}
                self.same_reach[rel] = {}
                continue
            hi = df["High"].to_numpy()[pos]
            lo = df["Low"].to_numpy()[pos]
            op = df["Open"].to_numpy()[pos]
            cl = df["Close"].to_numpy()[pos]
            times = df.index[pos]
            # Baseline bar c (window-relative): c+1 and c+N must exist.
            c = np.arange(n)[: n - N_PRIMARY - 1]
            if len(c) == 0:
                self.same_pools[rel] = {}
                self.same_reach[rel] = {}
                continue
            rets = (cl[c + N_PRIMARY] - op[c + 1]) / op[c + 1]
            # F2 baseline reach flags: suffix max >= prefix max (over the
            # same window the detector sees).
            prefix = np.maximum.accumulate(hi)
            suffix = np.empty(n)
            suffix[-1] = hi[-1]
            for i in range(n - 2, -1, -1):
                suffix[i] = max(suffix[i + 1], hi[i])
            reach = suffix[c + 1] >= prefix[c]
            per_hour, per_hour_reach = {}, {}
            ep = entry_pos.get(rel, set())
            ep_arr = np.fromiter(ep, dtype=int, count=len(ep)) if ep \
                else np.array([], dtype=int)
            for h in hours:
                hm = times[c].hour == h
                keep = hm & ~np.isin(c, ep_arr)
                if keep.any():
                    per_hour[h] = rets[keep]
                    per_hour_reach[h] = reach[keep]
            self.same_pools[rel] = per_hour
            self.same_reach[rel] = per_hour_reach
            for h in hours:
                if h in per_hour:
                    self.uni_pools[h].append(per_hour[h])
                    self.uni_reach[h].append(per_hour_reach[h])
        self.uni_pools = {h: np.concatenate(v) if v else np.array([])
                          for h, v in self.uni_pools.items()}
        self.uni_reach = {h: np.concatenate(v) if v else np.array([])
                          for h, v in self.uni_reach.items()}

    # -- event arrays -----------------------------------------------------
    def rets_for(self, evs: list, n: int = N_PRIMARY,
                 cost: float = COST_PRIMARY) -> np.ndarray:
        """(C[wpos[e+n]] - entry_open)/entry_open - cost for each event.
        Events without the forward window are skipped by the caller."""
        out = []
        for ev in evs:
            w = self.wpos(ev["rel"])
            cl = self.files[ev["rel"]]["Close"].to_numpy()
            out.append((cl[w[ev["e_pos"] + n]] - ev["entry_open"])
                       / ev["entry_open"] - cost)
        return np.array(out)

    def reach_events(self) -> np.ndarray:
        """F2 event reach flags: max(High[e+1..session close]) >= T."""
        flags = []
        for ev in self.events:
            w = self.wpos(ev["rel"])
            hi = self.files[ev["rel"]]["High"].to_numpy()
            tail = hi[w[ev["e_pos"] + 1: ev["npos"]]]
            flags.append(bool(tail.max() >= ev["target"]))
        return np.array(flags, dtype=float)

    def hour_of(self, ev: dict) -> int:
        w = self.wpos(ev["rel"])
        return int(self.files[ev["rel"]].index[w[ev["e_pos"]]].hour)


def run_measurement(a: Archive, rng) -> dict:
    """§4 families on the primary parameters. Returns the results dict."""
    evs = [ev for ev in a.events if ev["valid_n"]]
    rets = a.rets_for(evs)
    res = {"n_events": len(a.events), "n_measured_f1": len(evs),
           "n_chase": len(a.chase),
           "n_dropped_f1": sum(1 for ev in a.events if not ev["valid_n"]),
           "dropped_note": "events with e+N beyond the session end are "
                           "dropped and counted (pre-reg §4)"}

    # ---- F1: absolute forward returns, N=60, COST 0.0015 ---------------
    fam1 = {}
    for slot, kind in (("same_ticker", "same"), ("universe", "uni")):
        if len(rets) == 0:
            fam1[slot] = {"n": 0, "mean_ret": None, "est": None,
                          "ci_low": None, "ci_upper": None, "p": 1.0}
            continue

        def sample_b(M, kind=kind):
            out = np.empty(M)
            for i in range(M):
                ev = evs[rng.integers(0, len(evs))]
                h = ev["hour"]
                pool = (a.same_pools[ev["rel"]].get(h)
                        if kind == "same" else a.uni_pools.get(h))
                if pool is None or len(pool) == 0:
                    out[i] = 0.0
                else:
                    out[i] = pool[rng.integers(0, len(pool))]
            return out
        e = bootstrap_excess(rets, sample_b, rng)
        fam1[slot] = {"n": int(len(rets)), "mean_ret": float(rets.mean()),
                      "est": e[0], "ci_low": e[2], "ci_upper": e[3],
                      "p": e[4]}
    res["f1"] = holm(fam1, "F1")

    # ---- F2: HOD-retest reach rate (all detected events) ---------------
    reach = a.reach_events()
    fam2 = {}
    for slot, kind in (("same_ticker", "same"), ("universe", "uni")):
        if len(reach) == 0:
            fam2[slot] = {"n": 0, "reach_rate": None, "est": None,
                          "ci_low": None, "ci_upper": None, "p": 1.0}
            continue

        def sample_b(M, kind=kind):
            out = np.empty(M)
            for i in range(M):
                ev = a.events[rng.integers(0, len(a.events))]
                h = a.hour_of(ev)
                pool = (a.same_reach[ev["rel"]].get(h)
                        if kind == "same" else a.uni_reach.get(h))
                if pool is None or len(pool) == 0:
                    out[i] = 0.0
                else:
                    out[i] = pool[rng.integers(0, len(pool))]
            return out
        e = bootstrap_excess(reach, sample_b, rng)
        fam2[slot] = {"n": int(len(reach)),
                      "reach_rate": float(reach.mean()),
                      "est": e[0], "ci_low": e[2], "ci_upper": e[3],
                      "p": e[4]}
    res["f2"] = holm(fam2, "F2")

    # ---- F3: pullback vs chase (B-02/I-E-02) ----------------------------
    ch = [c for c in a.chase if c["e_pos"] + N_PRIMARY < c["npos"]]
    ch_ret = a.rets_for(ch)
    both = {ev["rel"] for ev in evs} & {c["rel"] for c in ch}
    pb_both = np.array([r for i, ev in enumerate(evs)
                        if ev["rel"] in both for r in [rets[i]]])
    ch_both = np.array([r for i, c in enumerate(ch)
                        if c["rel"] in both for r in [ch_ret[i]]])
    fam3 = {}
    for slot, (x, y) in (("same_ticker_pairs", (pb_both, ch_both)),
                         ("universe", (rets, ch_ret))):
        if len(x) < MIN_SLOT or len(y) < MIN_SLOT:
            fam3[slot] = {"n": int(len(x)), "n_chase": int(len(y)),
                          "mean_pullback": float(x.mean()) if len(x) else None,
                          "mean_chase": float(y.mean()) if len(y) else None,
                          "est": None, "ci_low": None, "ci_upper": None,
                          "p": 1.0}
            continue

        def sample_b(M, y=y):
            return y[rng.integers(0, len(y), size=M)]
        e = bootstrap_excess(x, sample_b, rng)
        fam3[slot] = {"n": int(len(x)), "n_chase": int(len(y)),
                      "mean_pullback": float(x.mean()),
                      "mean_chase": float(y.mean()),
                      "est": e[0], "ci_low": e[2], "ci_upper": e[3],
                      "p": e[4]}
    res["f3"] = holm(fam3, "F3")

    # ---- Measurement rows (no verdicts) ---------------------------------
    res["rows"] = measurement_rows(a, rets, evs, reach)
    return res


def measurement_rows(a: Archive, rets: np.ndarray, evs: list,
                     reach: np.ndarray) -> dict:
    rows = {}

    _FNS = {"mean": np.mean, "median": np.median,
            "p10": lambda v: np.percentile(v, 10),
            "p90": lambda v: np.percentile(v, 90)}

    def _row_stats(vals: np.ndarray, keys: tuple) -> dict:
        """Summary dict; None-filled when the array is empty."""
        if len(vals) == 0:
            return {k: None for k in keys}
        out = {}
        for k in keys:
            out[k] = float(_FNS[k](vals))
        return out

    # (a) R:R geometry: (T - O[e+1]) / (O[e+1] - S)
    rr = np.array([(ev["target"] - ev["entry_open"]) /
                   (ev["entry_open"] - ev["stop"])
                   for ev in a.events if ev["entry_open"] > ev["stop"]])
    degenerate = sum(1 for ev in a.events if ev["entry_open"] <= ev["stop"])
    rows["rr"] = {"n": int(len(rr)),
                  "frac_ge_2": float((rr >= 2.0).mean()) if len(rr) else None,
                  "n_degenerate_entry_le_stop": degenerate,
                  **_row_stats(rr, ("mean", "median", "p10", "p90"))}
    # (b) name-day collapse: mean F1 return per (ticker, bar-date)
    nd = {}
    for i, ev in enumerate(evs):
        nd.setdefault((ev["ticker"], ev["date"]), []).append(rets[i])
    nd_means = np.array([np.mean(v) for v in nd.values()])
    rows["name_day"] = {"n_name_days": int(len(nd_means)),
                        "frac_positive": float((nd_means > 0).mean())
                        if len(nd_means) else None,
                        "mean_of_means": float(np.mean(nd_means))
                        if len(nd_means) else None,
                        "median_of_means": float(np.median(nd_means))
                        if len(nd_means) else None}
    # (c) entry-bar gap distribution (sparse names)
    gaps = []
    for ev in a.events:
        w = a.wpos(ev["rel"])
        idx = a.files[ev["rel"]].index
        t = idx[w[ev["e_pos"]]]
        tprev = idx[w[ev["e_pos"] - 1]]
        gaps.append(int((t - tprev) / np.timedelta64(1, "m")))
    gaps = np.array(gaps)
    rows["entry_gaps_min"] = {
        "frac_gt_2min": float((gaps > 2).mean()) if len(gaps) else None,
        **_row_stats(gaps, ("mean", "median", "p90"))}
    # (d) F-01 time-of-day profile; (e) F-02 pre-market vs RTH
    buckets = [(dtime(4, 0), dtime(7, 0)), (dtime(7, 0), dtime(9, 30)),
               (dtime(9, 30), dtime(10, 0)), (dtime(10, 0), dtime(11, 0)),
               (dtime(11, 0), dtime(12, 0)), (dtime(12, 0), dtime(13, 0)),
               (dtime(13, 0), dtime(14, 0)), (dtime(14, 0), dtime(15, 0)),
               (dtime(15, 0), dtime(16, 0)), (dtime(16, 0), dtime(20, 0))]
    tot_vol = sum(float(df["Volume"].sum()) for df in a.files.values())
    prof = {}
    for b0, b1 in buckets:
        r_abs, hl, vol = [], [], 0.0
        for rel, df in a.files.items():
            t = df.index.time
            m = np.array([(x >= b0) and (x < b1) for x in t])
            x = df[m]
            if len(x) < 2:
                continue
            c = x["Close"].to_numpy()
            r_abs.append(np.abs(np.diff(c) / c[:-1]))
            hl.append((x["High"].to_numpy() - x["Low"].to_numpy())
                      / x["Open"].to_numpy())
            vol += float(x["Volume"].sum())
        if r_abs:
            ra = np.concatenate(r_abs)
            hla = np.concatenate(hl)
            prof[f"{b0.strftime('%H:%M')}-{b1.strftime('%H:%M')}"] = {
                "mean_abs_ret": float(ra.mean()),
                "mean_hl_over_o": float(hla.mean()),
                "vol_share": float(vol / tot_vol) if tot_vol else None}
    rows["time_of_day"] = prof

    def stats(t0, t1):
        r_abs, vols = [], []
        tail_all, n_all = 0, 0
        for rel, df in a.files.items():
            t = df.index.time
            m = np.array([(x >= t0) and (x < t1) for x in t])
            x = df[m]
            if len(x) < 3:
                continue
            c = x["Close"].to_numpy()
            r = np.abs(np.diff(c) / c[:-1])
            if len(r) == 0:
                continue
            r_abs.append(r)
            vols.append(float(x["Volume"].sum()))
            med = np.median(r)
            tail_all += int((r > 3 * med).sum())
            n_all += int(len(r))
        if not r_abs:
            return None
        ra = np.concatenate(r_abs)
        return {"mean_abs_ret": float(ra.mean()),
                "median_abs_ret": float(np.median(ra)),
                "tail_frac_gt_3x_median": float(tail_all / n_all),
                "vol_share": float(sum(vols) / tot_vol) if tot_vol else None}
    rows["pre_vs_rth"] = {
        "premarket_04_0930": stats(dtime(4, 0), dtime(9, 30)),
        "rth_0930_1600": stats(dtime(9, 30), dtime(16, 0))}
    # (f) per-bar-date and per-ticker F1 means
    by_date, by_ticker = {}, {}
    for i, ev in enumerate(evs):
        by_date.setdefault(ev["date"], []).append(rets[i])
        by_ticker.setdefault(ev["ticker"], []).append(rets[i])
    rows["by_bar_date"] = {k: float(np.mean(v)) for k, v in
                           sorted(by_date.items())}
    rows["by_ticker"] = {k: float(np.mean(v)) for k, v in
                         sorted(by_ticker.items())}
    rows["reach_rate_events"] = float(reach.mean()) if len(reach) else None
    return rows


# --------------------------------------------------------------------------
# sensitivities (exploratory; computed, reported, NO verdicts)
# --------------------------------------------------------------------------

def run_sensitivities(a: Archive, rng) -> dict:
    out = {}
    for label, kwargs in (("S-R4", {"r": 4}), ("S-R2", {"r": 2}),
                          ("S-P3", {"p": 3}), ("S-DB", {"db": False}),
                          ("S-WIN", {"win": (WIN_OPEN, WIN_END)}),
                          ("S-GAP", {"gap_min": 2})):
        aa = Archive(**kwargs)
        r = run_measurement(aa, np.random.default_rng(SEED))
        out[label] = {"n_events": len(aa.events),
                      "f1": r["f1"]["_family"], "f2": r["f2"]["_family"],
                      "f3": r["f3"]["_family"],
                      "mean_f1_ret": r["f1"]["same_ticker"]["mean_ret"]}
    for label, n in (("S-N15", 15), ("S-N120", 120), ("S-N240", 240)):
        aa = Archive()
        valid = [ev for ev in aa.events
                 if ev["e_pos"] + n < ev["npos"]]
        out[label] = {"n_events": int(len(valid)),
                      "mean_ret": float(aa.rets_for(valid, n=n).mean())
                      if valid else None}
    for label, cost in (("S-C05", 0.0005), ("S-C30", 0.0030)):
        aa = Archive()
        valid = [ev for ev in aa.events if ev["valid_n"]]
        out[label] = {"n_events": int(len(valid)),
                      "mean_ret": float(aa.rets_for(valid, cost=cost).mean())
                      if valid else None}
    return out


# --------------------------------------------------------------------------
# floors (§5) and report
# --------------------------------------------------------------------------

def check_floors(a: Archive) -> dict:
    bar_dates = sorted({rel.split("/")[0] for rel in a.files})
    event_dates = sorted({ev["date"] for ev in a.events})
    tickers = {ev["ticker"] for ev in a.events}
    return {"window_bar_dates": len(bar_dates),
            "events": len(a.events), "tickers": len(tickers),
            "dates_with_events": len(event_dates),
            "floors": FLOORS,
            "met": (len(bar_dates) >= FLOORS["min_bar_dates"]
                    and len(a.events) >= FLOORS["min_events"]
                    and len(tickers) >= FLOORS["min_tickers"]
                    and len(event_dates) >= FLOORS["min_dates_with_events"])}


def write_report(results: dict, audit: dict) -> None:
    L = []
    L.append("# Pre-registration #15 intraday measure report — B-01 micro pullback (1-min)")
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
        L.append("### Detection event counts (pre-reg §5 audit allowance)")
        L.append("")
        L.append("| bar-date | events | dropped (e+N beyond session) |")
        L.append("|---|---|---|")
        for d, cnt in sorted(results.get("events_by_date", {}).items()):
            L.append(f"| {d} | {cnt['events']} | {cnt['dropped']} |")
        L.append("")
    else:
        L.append("")
        def _f(x, fmt="{:+.4f}"):
            return fmt.format(x) if x is not None else "-"

        L.append("## F1 — absolute forward returns (N=60, COST 0.15%)")
        L.append("")
        L.append(f"Family verdict: **{results['f1']['_family']}**")
        for k in ("same_ticker", "universe"):
            r = results["f1"][k]
            L.append(f"- {k}: n={r['n']}, mean {_f(r['mean_ret'])}, "
                     f"excess {_f(r['est'])} (CI {_f(r['ci_low'])}.."
                     f"{_f(r['ci_upper'])}, p={r['p']:.3f}, Holm "
                     f"{r['holm_gate']:.3f}, {'rejected' if r['holm_rejected'] else 'not'}) "
                     f"— {r['verdict']}")
        L.append("")
        L.append("## F2 — HOD-retest reach rate")
        L.append("")
        L.append(f"Family verdict: **{results['f2']['_family']}**")
        for k in ("same_ticker", "universe"):
            r = results["f2"][k]
            L.append(f"- {k}: n={r['n']}, reach {_f(r['reach_rate'], '{:.4f}')}, "
                     f"excess {_f(r['est'])} (CI {_f(r['ci_low'])}.."
                     f"{_f(r['ci_upper'])}, p={r['p']:.3f}) — {r['verdict']}")
        L.append("")
        L.append("## F3 — pullback vs chase (B-02/I-E-02)")
        L.append("")
        L.append(f"Family verdict: **{results['f3']['_family']}**")
        for k in ("same_ticker_pairs", "universe"):
            r = results["f3"][k]
            L.append(f"- {k}: n={r['n']} / chase {r['n_chase']}, "
                     f"pullback {r.get('mean_pullback')}, "
                     f"excess {r.get('est')}, p={r.get('p')} — "
                     f"{r['verdict']}")
        L.append("")
        L.append("## Measurement rows (no verdicts)")
        L.append("")
        rr = results["rows"]["rr"]
        L.append(f"- R:R geometry: mean {_f(rr['mean'], '{:.2f}')}, "
                 f"median {_f(rr['median'], '{:.2f}')}, "
                 f"frac ≥2:1 {_f(rr['frac_ge_2'], '{:.3f}')} "
                 f"(n={rr['n']}, degenerate entry≤stop "
                 f"{rr['n_degenerate_entry_le_stop']})")
        nd = results["rows"]["name_day"]
        L.append(f"- Name-day collapse: {nd['n_name_days']} name-days, "
                 f"mean-of-means {_f(nd['mean_of_means'])}")
        g = results["rows"]["entry_gaps_min"]
        L.append(f"- Entry gaps (min): median {_f(g['median'], '{:.0f}')}, "
                 f"frac >2min {_f(g['frac_gt_2min'], '{:.3f}')}")
        L.append(f"- Reach rate (events): "
                 f"{_f(results['rows']['reach_rate_events'], '{:.4f}')}")
        L.append("")
        L.append("### Time-of-day profile (F-01 row)")
        L.append("")
        L.append("| bucket (ET) | mean |r| | mean (H-L)/O | vol share |")
        L.append("|---|---|---|---|")
        for k, v in results["rows"]["time_of_day"].items():
            L.append(f"| {k} | {v['mean_abs_ret']:.6f} | "
                     f"{v['mean_hl_over_o']:.6f} | {v['vol_share']:.3f} |")
        L.append("")
        L.append("### Pre-market vs RTH (F-02 row)")
        L.append("")
        for k in ("premarket_04_0930", "rth_0930_1600"):
            v = results["rows"]["pre_vs_rth"][k]
            L.append(f"- {k}: mean |r| {v['mean_abs_ret']:.6f}, "
                     f"median {v['median_abs_ret']:.6f}, "
                     f"tail {v['tail_frac_gt_3x_median']:.4f}, "
                     f"vol share {v['vol_share']:.3f}")
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
              "is restored or the failure is explained (pre-reg #15 §6).",
              file=sys.stderr)
        for e in audit["errors"]:
            print(f"  - {e}", file=sys.stderr)
        return 1

    if args.audit_only:
        # Detection counts per bar-date (pre-reg §5: allowed pre-measurement;
        # computes no returns).
        ev_by_date = {}
        m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for rel in sorted(m.get("files", {})):
            d = rel.split("/")[0]
            det = detect_b01(load_day(rel), n_need=N_PRIMARY)
            c = ev_by_date.setdefault(d, {"events": 0, "dropped": 0})
            c["events"] += len(det["events"])
            c["dropped"] += det["dropped"]
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
        print(f"REFUSED: measurement floors unmet (pre-reg #15 §5): "
              f"{floors}", file=sys.stderr)
        return 2

    rng = np.random.default_rng(SEED)
    res = run_measurement(a, rng)
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
