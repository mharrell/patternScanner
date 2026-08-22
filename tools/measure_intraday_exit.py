"""Pre-registration #20 measurement tool — intraday exit rules on 1-minute
bars: the breakeven-trail + sell-half (I-C-02), the 9MA->20MA->VWAP target
ladder (I-C-03), and the flat-out rule (I-C-04) on the shared B-01 entry
set (pre-reg #15 detector).

Implements PREREGISTRATION.md §Pre-registration #20 exactly:
  * §3 the measurement (F1: each rule vs the fixed-N=60 primary and
    fixed-2R secondary benchmarks; F2: the flat premise), measurement rows,
  * §4 the sample-size floors and the one-shot rule (measurement REFUSED
    until the floors are met; audit-only mode computes no returns),
  * §5 the archive-integrity audit (shared with pre-reg #15).

The B-01 entry detector is the frozen pre-reg #15 detector in
`tools/measure_intraday.py`; its raw measure_code_sha256 is asserted AT
IMPORT (pre-reg #20 §2: the shared, frozen entry set).

Frozen 2026-08-21, before any measurement. The module sha is asserted at
run (FROZEN_SHA below, the fixed-point convention; measure_code_sha256
records the raw file sha): any byte change invalidates the campaign.

Modes:
  python -X utf8 tools/measure_intraday_exit.py --audit-only
      §6 audit + B-01 detection counts only. Computes NO return of any
      kind. Exit 0 = audit clean; 1 = audit FAILED.
  python -X utf8 tools/measure_intraday_exit.py
      Full measurement. Requires the §5 floors; otherwise REFUSES (exit
      2). Writes data/cache/intraday_exit_measure_report.md +
      intraday_exit_measure_results.json, prints their sha256 for the
      determinism check.

Exit codes: 0 ok, 1 audit/integrity failure, 2 floors unmet (refused),
3 input error.

Spec mapping (pre-reg #20 §1/§3; the primary column):
  Entry set = B-01 events of pre-reg #15 (R=3, P=2, double-bottom), all
  RTH, entry = open of the bar after the signal. COST 0.0015 round-trip
  per entry (S-C05/S-C30 sensitivities). Benchmarks on the same entry set:
  fixed-N (hold to the N=60-bar close), fixed-2R (exit at entry+2d or
  entry-d stop, whichever first, terminal at session close; d = entry -
  initial stop). B=1000, seed 20260821, Holm alpha 0.05.
  F1 — 3 Holm slots (breakeven_trail, ladder, flat_out): mean realized
  return of the rule minus mean of the fixed-N benchmark (primary) and
  minus mean of fixed-2R (secondary), same entry set, paired bootstrap.
  F2 (the flat premise) — 1 Holm slot: contrast mean N-forward return of
  flat-after-entry events minus matched non-flat (same hour bucket, same
  direction).  Floors: >= 20 window bar-dates, >= 2,000 F1-evaluable B-01
  entries, >= 100 tickers, >= 15 dates.  Per-slot floor 100.
  Sensitivities: S-C05 (COST 0.0005), S-C30 (COST 0.0030), S-E2 (flat
  eps x2), S-M20 (flat M=20). Exploratory, NO verdicts.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import measure_intraday as MI

ROOT = Path(__file__).resolve().parent.parent
INTRA = ROOT / "data" / "intraday"
RAW_DIR = INTRA / "raw"
MANIFEST_PATH = INTRA / "manifest.json"
REPAIRS_PATH = INTRA / "repairs.json"
OUT_DIR = ROOT / "data" / "cache"
REPORT_PATH = OUT_DIR / "intraday_exit_measure_report.md"
RESULTS_PATH = OUT_DIR / "intraday_exit_measure_results.json"

WINDOW_START = "2026-08-19"

# ---- frozen-input assertion (pre-reg #20 §2): the B-01 detector ----
# measure_intraday.py is the frozen pre-reg #15 tool; its raw
# measure_code_sha256 (LF-normalized, checkout-independent) was recorded
# in PREREGISTRATION #15 §9.
_FROZEN_INPUT_SHA256 = "c58282caf75c344f228b70b329e9182b54a663d013891fe6a17103dc89f5e14c"


def _detector_sha() -> str:
    """LF-normalized sha256 of tools/measure_intraday.py — equals #15 §9's
    measure_code_sha256 regardless of working-tree line endings."""
    return hashlib.sha256(Path(MI.__file__).read_bytes()
                          .replace(b"\r\n", b"\n")).hexdigest()


_got = _detector_sha()
assert _got == _FROZEN_INPUT_SHA256, (
    f"{MI.__file__} changed (sha {_got[:16]}..., want "
    f"{_FROZEN_INPUT_SHA256[:16]}...) — frozen input must not move")

# ---- frozen parameters (pre-reg #20 §1/§3) ----
N_PRIMARY = 60        # fixed-horizon benchmark
COST_PRIMARY = 0.0015
M_FLAT = 10           # flat rule: M consecutive bars (S-M20: 20)
EPS_FLAT = 0.001      # flat epsilon as a fraction of entry (S-E2: 0.002)
R_TARGET = 2.0        # fixed-2R target multiple
HALF_MULT = 1.5       # breakeven-trail half-sell trigger multiple
B = 1000
SEED = 20260821
ALPHA = 0.05
FLOORS = {"min_bar_dates": 20, "min_events": 2000,
          "min_tickers": 100, "min_dates_with_events": 15}
MIN_SLOT = 100

# Freeze sha (house fixed-point convention; see measure_intraday.py).
FROZEN_SHA = "544a1c0b911721664136e9a7e3cb5a3b7d776a530a51c789caa2c1d4e180ee5c"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


_FROZEN_RE = re.compile(rb'(FROZEN_SHA = "[0-9a-f]{64}")')


def hash_self() -> str:
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
        print(f"FATAL: measure_intraday_exit.py sha mismatch — frozen "
              f"{FROZEN_SHA[:12]}…, on disk {actual[:12]}…. A frozen "
              f"measurement tool must not change.", file=sys.stderr)
        sys.exit(1)


# --------------------------------------------------------------------------
# §5 archive-integrity audit
# --------------------------------------------------------------------------

def audit_archive() -> dict:
    """§5 audit: pull-chain validity, file/hash ledger match, per-pull
    universe attribution, blind-capture check, repairs list. Identical to
    pre-reg #15 §6 (re-registered by reference)."""
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
            ufp = ROOT / "data" / "cache" / uf
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
# §3 exit-rule simulations
# --------------------------------------------------------------------------

def breakeven_trail_s(op, hi, lo, cl, wmins, e, entry, stop, npos,
                      half: float = HALF_MULT):
    """breakeven-trail + sell-half (I-C-02) on a B-01 entry at open[e+1].

    Initial stop = entry - d (d = entry - stop). Once any close >= entry,
    the stop moves to breakeven. When a 5-min close (minute % 5 == 0) is
    >= entry + half*d, half sells at the next bar open and the remainder
    trails at the low of the last 5-minute candle (ratcheting up). Any
    open portion settles at its stop when a bar's low <= stop, or at the
    session close otherwise.

    Returns (realized_fractional_return, half_fired: bool) or None when
    degenerate (stop >= entry)."""
    if stop >= entry:
        return None
    d = entry - stop
    S = stop
    frac = 1.0
    tot = 0.0
    half_fired = False
    for k in range(e + 1, npos):
        if lo[k] <= S:
            tot += frac * (S - entry) / entry
            return tot, half_fired
        if not half_fired:
            if S < entry and cl[k] >= entry:
                S = entry
            if wmins[k] % 5 == 0 and cl[k] >= entry + half * d:
                ex = op[k + 1] if k + 1 < npos else cl[k]
                tot += 0.5 * (ex - entry) / entry
                half_fired = True
                frac = 0.5
                lo5 = lo[max(e + 1, k - 4): k + 1].min()
                S = max(entry, lo5)
                if lo[k] <= S:
                    tot += frac * (S - entry) / entry
                    return tot, half_fired
        else:
            lo5 = lo[max(e + 1, k - 4): k + 1].min()
            if lo5 > S:
                S = lo5
    tot += frac * (cl[npos - 1] - entry) / entry
    return tot, half_fired


def ladder_s(op, hi, lo, cl, vwap, e, entry, npos):
    """9MA->20MA->VWAP target ladder (I-C-03): exit thirds at C >= MA9,
    then C >= MA20, then C >= cumulative VWAP (MAs over the post-entry
    closes; VWAP cumulative from the session open), each at the next bar
    open; the remainder liquidates at the session close.

    Returns (realized_fractional_return, legs_fired: int) or None when
    degenerate."""
    tot = 0.0
    fired = 0
    for k in range(e + 1, npos):
        if fired == 0 and k - e >= 8:
            ma9 = cl[e + 1: k + 1].mean()
            if cl[k] >= ma9:
                ex = op[k + 1] if k + 1 < npos else cl[k]
                tot += (1.0 / 3.0) * (ex - entry) / entry
                fired = 1
                if k + 1 >= npos:
                    break
                continue
        if fired == 1 and k - e >= 19:
            ma20 = cl[e + 1: k + 1].mean()
            if cl[k] >= ma20:
                ex = op[k + 1] if k + 1 < npos else cl[k]
                tot += (1.0 / 3.0) * (ex - entry) / entry
                fired = 2
                if k + 1 >= npos:
                    break
                continue
        if fired >= 2 and cl[k] >= vwap[k]:
            ex = op[k + 1] if k + 1 < npos else cl[k]
            tot += (1.0 / 3.0) * (ex - entry) / entry
            fired = 3
            break
    if fired < 3:
        tot += (3 - fired) / 3.0 * (cl[npos - 1] - entry) / entry
    return tot, fired


def flat_out_s(cl, e, entry, npos, m: int = M_FLAT,
               eps: float = EPS_FLAT, n_hold: int = N_PRIMARY):
    """flat-out rule (I-C-04): if |C[k]-entry| <= eps*entry for all bars
    e+1..e+M, exit at the close of the M-th bar; otherwise hold to the
    fixed-N close. Returns (realized, flat: bool) or None when the
    forward window is missing."""
    if e + m >= npos:
        return None
    flat = True
    for k in range(e + 1, e + m + 1):
        if abs(cl[k] - entry) > eps * entry:
            flat = False
            break
    if flat:
        return (cl[e + m] - entry) / entry, True
    if e + n_hold >= npos:
        return None
    return (cl[e + n_hold] - entry) / entry, False


def fixed_n_s(cl, e, entry, npos, n: int = N_PRIMARY):
    """fixed-N benchmark: hold every entry to the N-bar close."""
    if e + n >= npos:
        return None
    return (cl[e + n] - entry) / entry


def fixed_2r_s(op, hi, lo, cl, e, entry, stop, npos):
    """fixed-2R benchmark: exit at entry + 2d when High reaches it, or at
    entry - d when Low hits it (whichever first), else session close.
    None when degenerate (stop >= entry)."""
    if stop >= entry:
        return None
    d = entry - stop
    target = entry + R_TARGET * d
    for k in range(e + 1, npos):
        if lo[k] <= entry - d:
            return (entry - d - entry) / entry
        if hi[k] >= target:
            return (target - entry) / entry
    return (cl[npos - 1] - entry) / entry


def vwap_series(df: pd.DataFrame, w: np.ndarray) -> np.ndarray:
    """Cumulative VWAP over the window bars (typical-price x volume)."""
    hi = df["High"].to_numpy()[w]
    lo = df["Low"].to_numpy()[w]
    cl = df["Close"].to_numpy()[w]
    vol = df["Volume"].to_numpy()[w]
    tp = (hi + lo + cl) / 3.0
    num = np.cumsum(tp * vol)
    den = np.cumsum(vol)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(den > 0, num / np.maximum(den, 1e-9), 0.0)


# --------------------------------------------------------------------------
# §3/§4 statistics
# --------------------------------------------------------------------------

def bootstrap_excess(a: np.ndarray, sample_b, rng) -> tuple:
    """Paired bootstrap of mean(a) - mean(sample_b(M)): B draws,
    percentile 2.5/97.5 CI, p = 2*min(P(diff<=0), P(diff>=0))."""
    M = len(a)
    if M == 0:
        raise ValueError("bootstrap_excess: empty array")
    diffs = np.empty(B)
    for b in range(B):
        s_mean = a[rng.integers(0, M, size=M)].mean()
        diffs[b] = s_mean - sample_b(M).mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)),
            float(lo), float(hi), float(p))


def paired_contrast(a: np.ndarray, b: np.ndarray, rng) -> tuple:
    """Paired bootstrap of mean(a) - mean(b), resampling event indices
    jointly."""
    M = len(a)
    if M == 0:
        raise ValueError("paired_contrast: empty array")
    diffs = np.empty(B)
    for i in range(B):
        idx = rng.integers(0, M, size=M)
        diffs[i] = a[idx].mean() - b[idx].mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)),
            float(lo), float(hi), float(p))


def holm(fam: dict, family: str) -> dict:
    """Holm at ALPHA across the family's slots (pre-reg #20 §3). Family
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


# --------------------------------------------------------------------------
# §3 measurement: Archive + families
# --------------------------------------------------------------------------

class Archive:
    """Window bar-dates loaded once; serves the B-01 entry set and the
    exit-rule simulations. Deterministic iteration (sorted rels)."""

    def __init__(self, cost: float = COST_PRIMARY, m: int = M_FLAT,
                 eps: float = EPS_FLAT, n_hold: int = N_PRIMARY):
        self.cost, self.m, self.eps, self.n_hold = cost, m, eps, n_hold
        self.files = {}
        self.events = []
        self.dropped = 0
        self._load()

    def _load(self):
        m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for rel in sorted(f for f in m.get("files", {})
                          if f.split("/")[0] >= WINDOW_START):
            df = MI.load_day(rel)
            self.files[rel] = df
            npos = len(np.flatnonzero(
                MI.window_mask(df.index, None)))
            det = MI.detect_b01(df, n_need=self.n_hold)
            date, ticker = rel.split("/")
            ticker = ticker[:-len(".parquet")]
            for ev in det["events"]:
                ev["rel"], ev["date"], ev["ticker"] = rel, date, ticker
                ev["npos"] = npos
                ev["evaluable"] = (ev["e_pos"] + self.n_hold < npos
                                   and ev["stop"] < ev["entry_open"])
                self.events.append(ev)
            self.dropped += det["dropped"]
        self.events.sort(key=lambda ev: (ev["rel"], ev["e_pos"]))

    def pos(self, rel):
        return np.flatnonzero(MI.window_mask(self.files[rel].index, None))

    def vwap(self, rel):
        return vwap_series(self.files[rel], self.pos(rel))

    def align(self):
        """F1 entry set (e+60 within session, non-degenerate) and the
        per-event realized returns of every rule/benchmark on that set,
        with the rule-mechanism flags. Returns a dict of aligned arrays
        plus the event list."""
        res = {"bre": [], "ladder": [], "flat": [], "fixed_n": [],
               "fixed_2r": [], "half_fired": [], "legs": [],
               "flat_flag": [], "evs": []}
        for ev in self.events:
            w = self.pos(ev["rel"])
            df = self.files[ev["rel"]]
            op = df["Open"].to_numpy()[w]
            hi = df["High"].to_numpy()[w]
            lo = df["Low"].to_numpy()[w]
            cl = df["Close"].to_numpy()[w]
            e, entry, stop = ev["e_pos"], ev["entry_open"], ev["stop"]
            npos = len(w)
            if e + self.n_hold >= npos:
                continue
            wmins = (df.index[w].hour.to_numpy() * 60 +
                     df.index[w].minute.to_numpy())
            br = breakeven_trail_s(op, hi, lo, cl, wmins, e, entry, stop, npos)
            if br is None:
                continue
            vw = self.vwap(ev["rel"])
            ld = ladder_s(op, hi, lo, cl, vw, e, entry, npos)
            fl = flat_out_s(cl, e, entry, npos, self.m, self.eps)
            fn = fixed_n_s(cl, e, entry, npos)
            f2 = fixed_2r_s(op, hi, lo, cl, e, entry, stop, npos)
            res["bre"].append(br[0] - self.cost)
            res["ladder"].append(ld[0] - self.cost)
            res["flat"].append(fl[0] - self.cost)
            res["fixed_n"].append(fn - self.cost)
            res["fixed_2r"].append(f2 - self.cost)
            res["half_fired"].append(1 if br[1] else 0)
            res["legs"].append(ld[1])
            res["flat_flag"].append(1 if fl[1] else 0)
            res["evs"].append(ev)
        out = {}
        for k in ("bre", "ladder", "flat", "fixed_n", "fixed_2r"):
            out[k] = np.array(res[k], dtype=float)
        out["half_fired"] = np.array(res["half_fired"], dtype=np.int8)
        out["legs"] = np.array(res["legs"], dtype=np.int8)
        out["flat_flag"] = np.array(res["flat_flag"], dtype=np.int8)
        out["evs"] = res["evs"]
        return out


def _fmt(x, nd=4):
    if x is None or (isinstance(x, float) and x != x):
        return "—"
    return f"{x:.{nd}f}"


def run_f1(a, rng) -> dict:
    """F1 — 3 Holm slots; slot-level Holm test uses the fixed-N contrast
    (primary); the fixed-2R contrast is reported as the slot's secondary
    statistic. Same entry set, paired bootstrap."""
    fam = {}
    for k, label in (("bre", "breakeven-trail"), ("ladder", "ladder"),
                     ("flat", "flat-out")):
        rule = a[k]
        bench_n = a["fixed_n"]
        bench_2r = a["fixed_2r"]
        if len(rule) < MIN_SLOT:
            fam[k] = {"slot": label, "n": len(rule), "verdict": "INCONCLUSIVE",
                      "p": 1.0, "ci_low": float("nan"),
                      "ci_upper": float("nan"), "holm_rejected": False,
                      "mean_rule": float("nan"),
                      "mean_fixed_n": float("nan"),
                      "mean_fixed_2r": float("nan"),
                      "diff_2r": float("nan"), "diff_2r_lo": float("nan"),
                      "diff_2r_hi": float("nan")}
            continue
        d1 = paired_contrast(rule, bench_n, rng)
        d2 = paired_contrast(rule, bench_2r, rng)
        fam[k] = {"slot": label, "n": len(rule),
                  "mean_rule": float(rule.mean()),
                  "mean_fixed_n": float(bench_n.mean()),
                  "excess_primary": d1[0], "ci_low": d1[3],
                  "ci_upper": d1[4], "p": d1[4],
                  "mean_fixed_2r": float(bench_2r.mean()),
                  "diff_2r": d2[0], "diff_2r_lo": d2[3],
                  "diff_2r_hi": d2[4], "p_2r": d2[4]}
    return holm(fam, "F1")


def run_f2(arch, a, rng) -> dict:
    """F2 — the flat premise (1 Holm slot): contrast mean N-forward return
    of flat-after-entry events minus hour-matched non-flat events on the
    same entry set. EDGE iff Holm-rejected and CI-upper < 0 (flat is
    worse); FADE iff Holm-rejected and CI-low > 0; NO EDGE otherwise."""
    idx_flat = np.flatnonzero(a["flat_flag"] == 1)
    idx_non = np.flatnonzero(a["flat_flag"] == 0)
    fr = a["fixed_n"][idx_flat]
    pool = {}
    for i in idx_non:
        h = a["evs"][i]["hour"]
        pool.setdefault(h, []).append(a["fixed_n"][i])

    def sample_b(M):
        arr = np.empty(M)
        for j in range(M):
            fi = idx_flat[rng.integers(0, len(idx_flat))]
            h = a["evs"][fi]["hour"]
            p = pool.get(h)
            if not p:
                p = [v for k in pool for v in pool[k]]
            arr[j] = p[rng.integers(0, len(p))]
        return arr

    fam = {}
    if len(fr) < MIN_SLOT:
        fam["flat_premise"] = {"slot": "flat premise", "n": len(fr),
                               "verdict": "INCONCLUSIVE", "p": 1.0,
                               "ci_low": float("nan"),
                               "ci_upper": float("nan")}
        fam["_family"] = "INCONCLUSIVE"
        return fam
    d = bootstrap_excess(fr, sample_b, rng)
    fam["flat_premise"] = {"slot": "flat premise", "n": len(fr),
                           "mean_flat": float(fr.mean()),
                           "diff": d[0], "ci_low": d[3], "ci_upper": d[4],
                           "p": d[4]}
    r = fam["flat_premise"]
    r["holm_gate"] = ALPHA
    r["holm_rejected"] = r["p"] <= ALPHA
    if r["holm_rejected"] and r["ci_upper"] < 0:
        r["verdict"] = "EDGE"      # premise confirmed
    elif r["holm_rejected"] and r["ci_low"] > 0:
        r["verdict"] = "FADE"      # flat is better than non-flat
    else:
        r["verdict"] = "NO EDGE"
    fam["_family"] = r["verdict"]
    return fam


def measurement_rows(a) -> dict:
    evs = a["evs"]
    legs = a["legs"]
    hf = a["half_fired"]
    ff = a["flat_flag"]
    out = {
        "n": len(evs),
        "ladder": {
            "n_9ma": int((legs >= 1).sum()),
            "n_20ma": int((legs >= 2).sum()),
            "n_vwap": int((legs >= 3).sum()),
            "rate_9ma": float((legs >= 1).mean()),
            "rate_20ma": float((legs >= 2).mean()),
            "rate_vwap": float((legs >= 3).mean())},
        "breakeven": {
            "half_fired_n": int(hf.sum()),
            "half_fired_rate": float(hf.mean())},
        "flat": {
            "n_flat": int(ff.sum()),
            "n_flat_out": int(ff.sum())}}
    by_date = {}
    by_ticker = {}
    by_hour = {}
    for i, ev in enumerate(evs):
        by_date.setdefault(ev["date"], []).append(i)
        by_ticker.setdefault(ev["ticker"], []).append(i)
        by_hour.setdefault(ev["hour"], []).append(i)
    out["by_bar_date"] = {d: {"n": len(ix), "mean_fixed_n":
                              float(a["fixed_n"][ix].mean()),
                              "mean_bre": float(a["bre"][ix].mean()),
                              "mean_ladder": float(a["ladder"][ix].mean()),
                              "mean_flat": float(a["flat"][ix].mean())}
                          for d, ix in sorted(by_date.items())}
    out["by_ticker"] = {t: {"n": len(ix),
                            "mean_fixed": float(a["fixed_n"][ix].mean())}
                        for t, ix in sorted(by_ticker.items())}
    out["by_hour"] = {h: {"n": len(ix), "mean_fixed":
                          float(a["fixed_n"][ix].mean()),
                          "flat_rate": float(a["flat_flag"][ix].mean())}
                      for h, ix in sorted(by_hour.items())}
    return out


def run_sensitivities() -> dict:
    """Pre-declared sensitivities, exploratory (NO verdicts): cost, flat
    epsilon, and flat M."""
    out = {}
    for key, cost, m, eps in (
            ("S-C05", COST_PRIMARY / 3, M_FLAT, EPS_FLAT),
            ("S-C30", COST_PRIMARY * 2, M_FLAT, EPS_FLAT),
            ("S-E2", COST_PRIMARY, M_FLAT, EPS_FLAT * 2),
            ("S-M20", COST_PRIMARY, 20, EPS_FLAT)):
        arc = Archive(cost=cost, m=m, eps=eps)
        a = arc.align()
        rng = np.random.default_rng(SEED + 1)
        f1 = run_f1(a, rng)
        out[key] = {"f1": {k: {"slot": v["slot"], "n": v["n"],
                               "mean_rule": v.get("mean_rule"),
                               "diff_primary": v.get("excess_primary"),
                               "p": v.get("p")}
                           for k, v in f1.items()
                           if k != "_family"},
                    "f1_family": f1.get("_family")}
    return out


def check_floors(archive) -> dict:
    """§4 sample-size floors. F1-evaluable = B-01 events with the fixed-N
    forward AND a non-degenerate stop (the rules produce a return)."""
    dates = sorted({rel.split("/")[0] for rel in archive.files})
    eval_evs = [ev for ev in archive.events if ev["evaluable"]]
    floors = {
        "window_bar_dates": len(dates),
        "events_f1_valid": len(eval_evs),
        "tickers": len({ev["ticker"] for ev in eval_evs}),
        "dates_with_events": len({ev["date"] for ev in eval_evs})}
    floors["met"] = (floors["window_bar_dates"] >= FLOORS["min_bar_dates"]
                     and floors["events_f1_valid"] >= FLOORS["min_events"]
                     and floors["tickers"] >= FLOORS["min_tickers"]
                     and floors["dates_with_events"]
                     >= FLOORS["min_dates_with_events"])
    return floors


def write_report(audit: dict, arc, floors: dict | None,
                 measure: dict | None, audit_only: bool) -> str:
    L = []
    L.append("# Pre-registration #20 measurement — intraday exit rules")
    L.append("")
    L.append(f"- tool sha (raw): `{sha_bytes(Path(__file__).read_bytes())}`")
    L.append(f"- tool FROZEN_SHA (fixed point): `{FROZEN_SHA}`")
    L.append(f"- frozen input `tools/measure_intraday.py` sha256 "
             f"(LF-normalized): `{_detector_sha()}`")
    L.append(f"- window: bar-dates >= {WINDOW_START}")
    L.append("")
    L.append("## Archive-integrity audit (§5/§6)")
    L.append("")
    L.append(f"- **PASSED**" if audit["passed"] else f"- **FAILED**")
    if audit["errors"]:
        L.append("- errors:")
        for e in audit["errors"]:
            L.append(f"  - {e}")
    L.append(f"- pulls checked: {audit['n_pulls']}; ledger files: "
             f"{audit['n_files_ledger']}")
    if audit["repairs"]:
        L.append(f"- repairs on record: {len(audit['repairs'])}")
        for r in audit["repairs"]:
            L.append(f"  - {r['path']}: {r['reason']}")
    if audit["window_pulls"]:
        L.append("- window pulls:")
        L.append("  | pull_id | universe | requested | ok | failed |")
        L.append("  |---|---|---|---|---|")
        for p in audit["window_pulls"]:
            L.append(f"  | {p['pull_id']} | {p['universe_file']} | "
                     f"{p['tickers_requested']} | {p['tickers_ok']} | "
                     f"{p['tickers_failed']} |")
    if audit_only:
        L.append("")
        L.append("## B-01 detection (audit-only; no returns computed)")
        L.append("")
        L.append("| bar-date | B-01 events | dropped | F1-evaluable |")
        L.append("|---|---|---|---|")
        per_date = {}
        eval_by = {}
        dropped = {}
        for ev in arc.events:
            per_date.setdefault(ev["date"], 0)
            per_date[ev["date"]] += 1
            if ev["evaluable"]:
                eval_by.setdefault(ev["date"], 0)
                eval_by[ev["date"]] += 1
        for rel in sorted(arc.files):
            d = rel.split("/")[0]
            if d < WINDOW_START:
                continue
            det = MI.detect_b01(arc.files[rel], n_need=N_PRIMARY)
            dropped.setdefault(d, 0)
            dropped[d] += det["dropped"]
        for d in sorted(per_date):
            L.append(f"| {d} | {per_date.get(d, 0)} | "
                     f"{dropped.get(d, 0)} | {eval_by.get(d, 0)} |")
        return "\n".join(L) + "\n"
    L.append("")
    L.append(f"## Sample-size floors (§4)")
    L.append("")
    L.append("| floor | required | actual | met |")
    L.append("|---|---|---|---|")
    for k, req in FLOORS.items():
        L.append(f"| {k} | {req} | {floors[k]} | "
                 f"{'✓' if floors[k] >= req else '✗'} |")
    L.append("")
    L.append("## F1 — rule vs fixed-N (primary) / fixed-2R (secondary)")
    L.append("")
    L.append("Family verdict: **" + measure["f1"]["_family"] + "**")
    L.append("")
    L.append("| slot | n | mean rule | mean fixed-N | excess | CI 95% | "
             "p | Holm gate | rej | verdict |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for k, r in measure["f1"].items():
        if k == "_family":
            continue
        L.append(f"| {r['slot']} | {r['n']} | "
                 f"{_fmt(r.get('mean_rule'))} | "
                 f"{_fmt(r.get('mean_fixed_n'))} | "
                 f"{_fmt(r.get('excess_primary'))} | "
                 f"{_fmt(r.get('ci_low'))} … {_fmt(r.get('ci_upper'))} | "
                 f"{_fmt(r.get('p'), 3)} | {_fmt(r.get('holm_gate'), 3)} | "
                 f"{'✓' if r.get('holm_rejected') else '—'} | "
                 f"{r.get('verdict')} |")
    L.append("")
    L.append("Secondary (fixed-2R):")
    L.append("")
    L.append("| slot | mean fixed-2R | diff | CI 95% | p |")
    L.append("|---|---|---|---|---|")
    for k, r in measure["f1"].items():
        if k == "_family":
            continue
        L.append(f"| {r['slot']} | {_fmt(r.get('mean_fixed_2r'))} | "
                 f"{_fmt(r.get('diff_2r'))} | "
                 f"{_fmt(r.get('diff_2r_lo'))} … {_fmt(r.get('diff_2r_hi'))} | "
                 f"{_fmt(r.get('p_2r'), 3)} |")
    L.append("")
    L.append("## F2 — the flat premise")
    L.append("")
    r = measure["f2"]["flat_premise"]
    L.append(f"Contrast (mean N-forward flat − matched non-flat): "
             f"{_fmt(r.get('diff'))}   CI 95% "
             f"{_fmt(r.get('ci_low'))} … {_fmt(r.get('ci_upper'))}   "
             f"p {_fmt(r.get('p'), 3)}   n {r['n']}   "
             f"verdict **{r['verdict']}**")
    L.append("")
    L.append("## Measurement rows")
    L.append("")
    rows = measure["rows"]
    L.append(f"- entries (F1 set): {rows['n']}")
    L.append(f"- ladder reach 9MA: {rows['ladder']['rate_9ma']:.4f} "
             f"({rows['ladder']['n_9ma']})")
    L.append(f"- ladder reach 20MA: {rows['ladder']['rate_20ma']:.4f} "
             f"({rows['ladder']['n_20ma']})")
    L.append(f"- ladder reach VWAP: {rows['ladder']['rate_vwap']:.4f} "
             f"({rows['ladder']['n_vwap']})")
    L.append(f"- breakeven-trail half fired: {rows['breakeven']['half_fired_rate']:.4f} "
             f"({rows['breakeven']['half_fired_n']})")
    L.append(f"- flat-out trades (flat events): {rows['flat']['n_flat']}")
    L.append("")
    L.append("### By bar-date")
    L.append("")
    L.append("| date | n | mean fixed-N | mean breakeven | mean ladder | "
             "mean flat |")
    L.append("|---|---|---|---|---|---|")
    for d, r in rows["by_bar_date"].items():
        L.append(f"| {d} | {r['n']} | {_fmt(r['mean_fixed_n'])} | "
                 f"{_fmt(r['mean_bre'])} | {_fmt(r['mean_ladder'])} | "
                 f"{_fmt(r['mean_flat'])} |")
    L.append("")
    L.append("## Sensitivities (pre-declared, NO verdicts)")
    L.append("")
    for key, s in measure["sensitivities"].items():
        L.append(f"- {key}: F1 family {s['f1_family']} — " +
                 ", ".join(f"{v['slot']} n={v['n']} "
                           f"diff={_fmt(v.get('diff_primary'))} "
                           f"p={_fmt(v.get('p'), 3)}"
                           for v in s["f1"].values()))
    L.append("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-only", action="store_true",
                    help="§6 audit + detection counts only, no returns")
    args = ap.parse_args()
    self_check()
    audit = audit_archive()
    if args.audit_only:
        arc = Archive()
        report = write_report(audit, arc, None, None, True)
        print(report)
        print("AUDIT_EXIT=" + ("0" if audit["passed"] else "1"))
        sys.exit(0 if audit["passed"] else 1)
    arc = Archive()
    floors = check_floors(arc)
    if not floors["met"]:
        print("FATAL: §5 sample-size floors not met. Refusing measurement.",
              file=sys.stderr)
        _req_of = {"window_bar_dates": "min_bar_dates",
                   "events_f1_valid": "min_events",
                   "tickers": "min_tickers",
                   "dates_with_events": "min_dates_with_events"}
        for k, v in floors.items():
            if k == "met":
                continue
            print(f"  {k}: {v} (need {FLOORS[_req_of[k]]})", file=sys.stderr)
        sys.exit(2)
    rng = np.random.default_rng(SEED)
    a = arc.align()
    f1 = run_f1(a, rng)
    f2 = run_f2(arc, a, rng)
    rows = measurement_rows(a)
    sens = run_sensitivities()
    measure = {"f1": f1, "f2": f2, "rows": rows,
               "sensitivities": sens}
    report = write_report(audit, arc, floors, measure, False)
    REPORT_PATH.write_text(report, encoding="utf-8")
    results = {
        "frozen_sha": FROZEN_SHA,
        "measure_code_sha256": sha_bytes(Path(__file__).read_bytes()),
        "input_measure_intraday_sha256": _FROZEN_INPUT_SHA256,
        "seed": SEED, "bootstrap": B, "alpha": ALPHA,
        "floors": floors,
        "f1": {k: v for k, v in f1.items() if k != "_family"},
        "f1_family": f1["_family"],
        "f2": {k: v for k, v in f2.items() if k != "_family"},
        "f2_family": f2["_family"],
        "rows": rows,
        "sensitivities": sens,
        "audit_passed": audit["passed"]}
    RESULTS_PATH.write_text(
        json.dumps(results, indent=1, sort_keys=True), encoding="utf-8")
    print(f"wrote {REPORT_PATH}")
    print(f"report sha256: {sha_file(REPORT_PATH)}")
    print(f"wrote {RESULTS_PATH}")
    print(f"results sha256: {sha_file(RESULTS_PATH)}")
    print("F1:", f1["_family"], "F2:", f2["_family"])
    sys.exit(0)


if __name__ == "__main__":
    main()
