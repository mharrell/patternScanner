"""Independent verification of the five frozen intraday measurements
(pre-regs #15, #19, #20, #21, #22).

Recomputes each campaign's census, sample-size floors, family statistics
(n / deterministic means / bootstrapped est-CI-p), Holm gates, and verdict
categories from the frozen 1-minute archive with STANDALONE code —
imports nothing from tools/* (the five measure_intraday*.py tools are
intentionally avoided) — and compares against the recorded
data/cache/intraday_*_measure_results.json.

Check classes:
  EXACT     (tol 1e-9): census counts, floor counts, family unit-vector
            lengths and deterministic means, runner-bucket labels,
            coverage counts, Holm gates recomputed from the recorded p's,
            and verdict categories re-derived from the recorded gate.
  MC-SPREAD (fresh seeds): every bootstrapped estimate (est / CI / p)
            recomputed with independent seeds and required to land within a
            tolerance derived from the bootstrap SE (3*s/sqrt(B) for est,
            0.6*s for the CI endpoints; a data-driven p tolerance,
            6*sqrt(a(1-a)/B) with a = P(diff<=0) and a 0.05 floor, so
            near-zero-effect slots are not false-flagged). Verdict categories
            are re-derived from the fresh (correct) statistics and the
            recorded gates, so a frozen tool whose CI semantics are wrong is
            flagged.

Each results JSON carries the tool's FROZEN_SHA; the verifier asserts it
equals the documented freeze value (a re-frozen tool is caught before its
recorded numbers are trusted). The verifier implements the CORRECT CI
semantics everywhere; during cross-validation this exposed a ci-swap bug in
the pre-fix #20 exit tool, which was re-frozen pre-measurement (§8
amendment) — both the tool and this verifier now agree.

Usage:
  python -X utf8 tools/verify_intraday.py --campaign <b01|entry|exit|veto|regime|all> [--results <path>]

Exit 0 only when every check passes; exit 1 on any FAIL.
"""
import argparse
import json
import math
import sys
from datetime import time as dtime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INTRA = ROOT / "data" / "intraday"
RAW = INTRA / "raw"
MANIFEST = INTRA / "manifest.json"
CACHE = ROOT / "data" / "cache"
WINDOW_START = "2026-08-19"

# ---- frozen parameters (PREREGISTRATION #15 / #19-#22 §3/§4) ----
B = 1000
ALPHA = 0.05
MIN_SLOT = 100
N_PRIMARY = 60
COST_PRIMARY = 0.0015
R_PRIMARY, P_PRIMARY = 3, 2          # #15 B-01 (double-bottom required)
D_PRIMARY = 3                        # #19/#21/#22 decline/rise length
M_FLAT, EPS_FLAT = 10, 0.001         # #20 flat-out rule
R_TARGET, HALF_MULT = 2.0, 1.5       # #20 fixed-2R / breakeven half-mult
V_PRIMARY, WARMUP_MACD = 3.0, 26     # #21 veto legs
MIN_BUCKET_DATES, MIN_NAMES_PER_DATE = 100, 10   # #22 F1 coverage
TAIL_MULT = 3.0                      # #22 F3 tail multiple

# Documented freeze values (the recorded JSON's frozen_sha must match).
FROZEN = {
    "b01":   "765ff1df23c80c006104d2f28b754593e3401e256132115207a161ebf5fdc6f5",
    "entry": "cac0e7ed205c8fbea62dad2c1f3f181cbe6b2b247d00c34c9c93b0c426c4b48c",
    "exit":  "0c798159ea3e93d966d8435c6dceb9eb80fb7c62cd3c91b983cf0ee17c6e863c",
    "veto":  "60569201e50982a2a2a837464aaaae81ac2111e0f2dba78c4c0835e36f304997",
    "regime": "b1fe067d8bac111c4532cfc838bb6d210f13a906defc0db8a083bd228a1095c0",
}
# Frozen-input tools' LF-normalized shas recorded in the results JSONs.
INPUT_ENTRY_SHA = \
    "d58a889c6c0a634952bacd90bf412140709102053facebf1ee82b5df67592656"
INPUT_B01_SHA = \
    "c58282caf75c344f228b70b329e9182b54a663d013891fe6a17103dc89f5e14c"

RES_FILES = {
    "b01": "intraday_measure_results.json",
    "entry": "intraday_entry_measure_results.json",
    "exit": "intraday_exit_measure_results.json",
    "veto": "intraday_veto_measure_results.json",
    "regime": "intraday_regime_measure_results.json",
}
FRESH = [1013, 2707, 4217]           # independent fresh bootstrap seeds

PASS = FAIL = 0


def check(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


def close(a, b, tol=1e-9):
    if a is None or b is None:
        return False
    if math.isnan(a) or math.isnan(b):
        return math.isnan(a) and math.isnan(b)
    return abs(a - b) <= tol


# ---------------------------------------------------------------------------
# Standalone data path (frozen archive, no imports from the stack)
# ---------------------------------------------------------------------------
_FILES = {}
_WCACHE = {}


def load_files():
    """Window bar-date files (manifest-driven, sorted rels), cached."""
    if not _FILES:
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        rels = sorted(f for f in m.get("files", {})
                      if f.split("/")[0] >= WINDOW_START)
        for rel in rels:
            _FILES[rel] = pd.read_parquet(RAW / rel)
    return _FILES


def wpos_of(rel):
    """Absolute row indices of the RTH bars (09:30-16:00 ET)."""
    if rel not in _WCACHE:
        df = _FILES[rel]
        t = df.index.time
        _WCACHE[rel] = np.flatnonzero(
            np.array([(x >= dtime(9, 30)) and (x < dtime(16, 0)) for x in t]))
    return _WCACHE[rel]


# ---------------------------------------------------------------------------
# Detectors (independent implementations of the frozen §3 rules)
# ---------------------------------------------------------------------------
def detect_b01(df, pos, r=R_PRIMARY, p=P_PRIMARY, db=True, gap_min=None,
               n_need=N_PRIMARY):
    """Pre-reg #15 §3 B-01 detector on the RTH bars ``pos``. Returns
    events, chase events, and the dropped count."""
    n = len(pos)
    if n < r + p + 2:
        return {"events": [], "chase": [], "dropped": 0}
    hi = df["High"].to_numpy()[pos]
    lo = df["Low"].to_numpy()[pos]
    op = df["Open"].to_numpy()[pos]
    cl = df["Close"].to_numpy()[pos]
    times = df.index[pos]
    up = cl > op
    down = cl < op
    if gap_min is not None:
        diffs_min = np.diff(times).astype("timedelta64[m]").astype(int)
        contiguous = np.concatenate(([True], diffs_min <= gap_min))
    events, chase, dropped = [], [], 0
    j = r - 1
    while j < n:
        if not up[j - r + 1: j + 1].all():
            j += 1
            continue
        for c in range(j - r + 1, j + 1):
            if c >= 1 and hi[c] > hi[c - 1] and c + 1 < n:
                chase.append({"e_pos": c, "entry_open": float(op[c + 1])})
        if j + p >= n or not down[j + 1: j + p + 1].all():
            j += 1
            continue
        l1 = lo[j + 1]
        l2 = lo[j + 2] if p >= 2 else l1
        if db and l2 < l1:
            j += 1
            continue
        stop = float(lo[j + 1: j + p + 1].min())
        k = j + p + 1
        while k < n and hi[k] <= hi[k - 1]:
            k += 1
        if k + 1 >= n:
            j += 1
            continue
        if gap_min is not None and not contiguous[j - r + 1: k + 1].all():
            j += 1
            continue
        target = float(hi[j - r + 1: k + 1].max())
        if k + n_need >= n:
            dropped += 1
        events.append({"e_pos": k, "entry_open": float(op[k + 1]),
                       "stop": stop, "target": target,
                       "hour": int(times[k].hour)})
        j = k + 1
    return {"events": events, "chase": chase, "dropped": dropped}


def detect_reversal(df, pos, d=D_PRIMARY):
    """Pre-reg #19 §3 F1 detector (reversal new-high, long + short)."""
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
        target = float(hi[j - d + 1: k + 1].max())
        if k + 1 + N_PRIMARY >= n:
            dropped += 1
        long_ev.append({"dir": "long", "e_pos": k,
                        "entry_open": float(op[k + 1]), "stop": stop,
                        "target": target, "hour": int(times[k].hour)})
        j = k + 1

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
        stop = float(hi[j - d + 1: j + 1].max())
        target = float(lo[j - d + 1: k + 1].min())
        if k + 1 + N_PRIMARY >= n:
            dropped += 1
        short_ev.append({"dir": "short", "e_pos": k,
                         "entry_open": float(op[k + 1]), "stop": stop,
                         "target": target, "hour": int(times[k].hour)})
        j = k + 1
    return {"long": long_ev, "short": short_ev, "dropped": dropped}


def detect_pullback_count(df, pos):
    """Pre-reg #19 §3 F2 detector (B-03 / I-B-01 pullback-count)."""
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
        j = r
    return {"events": events, "dropped": dropped}


def detect_second_conf(df, pos):
    """Pre-reg #19 §3 F3 detector (B-05 second-confirmation pairs)."""
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
        if k + 1 >= n:
            j += 1
            continue
        if cl[k + 1] <= cl[k]:
            dropped += 1
            j += 1
            continue
        if k + 2 >= n:
            dropped += 1
            j += 1
            continue
        if k + 1 + N_PRIMARY >= n or k + 2 + N_PRIMARY >= n:
            dropped += 1
        pairs.append({"c1_pos": k, "e1_open": float(op[k + 1]),
                      "e2_open": float(op[k + 2]),
                      "hour": int(df.index[pos[k]].hour)})
        j = k + 1
    return {"pairs": pairs, "dropped": dropped}


# ---------------------------------------------------------------------------
# #20 exit-rule simulations (independent implementations)
# ---------------------------------------------------------------------------
def breakeven_trail_s(op, hi, lo, cl, wmins, e, entry, stop, npos,
                      half=HALF_MULT):
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


def flat_out_s(cl, e, entry, npos, m=M_FLAT, eps=EPS_FLAT, n_hold=N_PRIMARY):
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


def fixed_n_s(cl, e, entry, npos, n=N_PRIMARY):
    if e + n >= npos:
        return None
    return (cl[e + n] - entry) / entry


def fixed_2r_s(op, hi, lo, cl, e, entry, stop, npos):
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


def vwap_series(df, w):
    hi = df["High"].to_numpy()[w]
    lo = df["Low"].to_numpy()[w]
    cl = df["Close"].to_numpy()[w]
    vol = df["Volume"].to_numpy()[w]
    tp = (hi + lo + cl) / 3.0
    num = np.cumsum(tp * vol)
    den = np.cumsum(vol)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(den > 0, num / np.maximum(den, 1e-9), 0.0)


# ---------------------------------------------------------------------------
# #21 veto legs (independent implementations)
# ---------------------------------------------------------------------------
def _ema_series(closes, span):
    alpha = 2.0 / (span + 1)
    out = np.empty(len(closes))
    out[0] = closes[0]
    e = closes[0]
    for i in range(1, len(closes)):
        e = alpha * closes[i] + (1 - alpha) * e
        out[i] = e
    return out


def macd_at(closes, i):
    if i + 1 < WARMUP_MACD:
        return None
    c = closes[:i + 1]
    return float(_ema_series(c, 12)[-1] - _ema_series(c, 26)[-1])


def volume_spike(df, wpos, e_abs, v=V_PRIMARY):
    med = float(np.median(df["Volume"].to_numpy()[wpos]))
    if med <= 0:
        return False
    op = float(df["Open"].to_numpy()[e_abs])
    cl = float(df["Close"].to_numpy()[e_abs])
    return (cl < op) and float(df["Volume"].to_numpy()[e_abs]) >= v * med


# ---------------------------------------------------------------------------
# Bootstrap + Holm + verdict (standalone)
# ---------------------------------------------------------------------------
def boot_excess(a, sample_b, rng):
    """Paired bootstrap of mean(a) - mean(sample_b(M)); 6-tuple with the raw
    diff distribution appended for MC tolerance."""
    M = len(a)
    if M == 0:
        raise ValueError("boot_excess: empty array")
    diffs = np.empty(B)
    for b in range(B):
        s_mean = a[rng.integers(0, M, size=M)].mean()
        diffs[b] = s_mean - sample_b(M, rng).mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)),
            float(lo), float(hi), float(p), diffs)


def contrast_two(x, y, rng):
    Mx, My = len(x), len(y)
    if Mx == 0 or My == 0:
        raise ValueError("contrast_two: empty array")
    diffs = np.empty(B)
    for b in range(B):
        sx = x[rng.integers(0, Mx, size=Mx)].mean()
        sy = y[rng.integers(0, My, size=My)].mean()
        diffs[b] = sx - sy
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)),
            float(lo), float(hi), float(p), diffs)


def paired_contrast(a, b, rng):
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
            float(lo), float(hi), float(p), diffs)


def contrast_paired(d, rng):
    M = len(d)
    if M == 0:
        raise ValueError("contrast_paired: empty array")
    diffs = np.empty(B)
    for b in range(B):
        diffs[b] = d[rng.integers(0, M, size=M)].mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)),
            float(lo), float(hi), float(p), diffs)


def boot_two(x, y, rng, stat):
    Mx, My = len(x), len(y)
    if Mx == 0 or My == 0:
        raise ValueError("boot_two: empty pool")
    diffs = np.empty(B)
    for b in range(B):
        diffs[b] = (stat(x[rng.integers(0, Mx, size=Mx)])
                    - stat(y[rng.integers(0, My, size=My)]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)),
            float(lo), float(hi), float(p), diffs)


def holm(fam):
    """Standard Holm (used by #15/#19/#20-F1/#21). Per-slot verdict:
    INCONCLUSIVE if n < MIN_SLOT; EDGE if rejected and ci_low > 0; FADE if
    rejected and ci_upper < 0; else NO EDGE. Family = all-EDGE / all-FADE /
    any-INCONCLUSIVE / NO EDGE."""
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


def rec_cat_of(verdict):
    for tok in ("INCONCLUSIVE", "EDGE", "FADE", "NO EDGE"):
        if str(verdict).startswith(tok):
            return tok
    raise ValueError(f"unparsed verdict {verdict!r}")


def verdict_cat(n, ci_lo, ci_hi, p, gate, rej):
    """Standard-Holm per-slot verdict from fresh stats + recorded gate."""
    if n < MIN_SLOT:
        return "INCONCLUSIVE"
    if rej and ci_lo > 0.0:
        return "EDGE"
    if rej and ci_hi < 0.0:
        return "FADE"
    return "NO EDGE"


def mc_tols(diffs):
    """MC tolerances from the bootstrap SE of the statistic (house §4):
    3*s/sqrt(B) for est, 0.6*s for the CI endpoints. The p tolerance is
    data-driven: p = 2*min(a, 1-a) with a = P(diff<=0), so SE(p) =
    2*sqrt(a(1-a)/B); 3-sigma with a 0.05 floor (near-zero-effect slots
    legitimately scatter more than a fixed 0.05 across bootstrap streams)."""
    s = float(diffs.std())
    a = min((diffs <= 0).mean(), (diffs >= 0).mean())
    p_tol = max(0.05, 6.0 * math.sqrt(a * (1.0 - a) / B))
    return 3.0 * s / np.sqrt(B), 0.6 * s, p_tol


def gates_of(rec_fam):
    """Recompute Holm gates EXACTLY from the recorded p's (tool slot order).
    The recorded dict may embed a "_family" string key (#15/#19 write the
    holm()-returned dict verbatim); slot keys only."""
    order = sorted((k for k in rec_fam if k != "_family"),
                   key=lambda k: rec_fam[k].get("p", 1.0))
    gates = {}
    for rank, k in enumerate(order, start=1):
        gates[k] = ALPHA / (len(order) - rank + 1)
    return gates


def check_holm(name, rec_fam, fam_order):
    """EXACT gate/rejection from recorded p's; family verdict category."""
    gates = gates_of(rec_fam)
    for k in fam_order:
        rec = rec_fam[k]
        gate = gates[k]
        p = rec.get("p", 1.0)
        rej = p <= gate
        check(f"{name}.{k}.holm_gate", close(rec.get("holm_gate"), gate),
              f"got {rec.get('holm_gate')} vs {gate}")
        check(f"{name}.{k}.holm_rejected",
              bool(rec.get("holm_rejected")) == rej,
              f"got {rec.get('holm_rejected')} vs {rej}")
    fam = rec_fam.get("_family")
    if fam is None:
        return
    cats = [rec_cat_of(rec_fam[k]["verdict"]) for k in fam_order]
    want = ("EDGE" if all(c == "EDGE" for c in cats)
            else "FADE" if all(c == "FADE" for c in cats)
            else "INCONCLUSIVE" if any(c == "INCONCLUSIVE" for c in cats)
            else "NO EDGE")
    check(f"{name}.family", rec_cat_of(fam) == want,
          f"got {fam} vs {want}")


def check_mc(name, rec, boot_fn, n, ci_low_key="ci_low",
             ci_upper_key="ci_upper", p_key="p", est_key="est",
             verdict=False, gate=None, rej=None):
    """MC-SPREAD est/CI/p from fresh seeds against the recorded cell.
    ``boot_fn(rng)`` returns (est, med, lo, hi, p, diffs) — the tolerance is
    derived from the raw diff distribution's bootstrap SE. Verdict, when
    asked, is re-derived from the fresh (correct) stats and recorded gate."""
    if rec.get(est_key) is None or rec.get(p_key) is None:
        return
    d0 = boot_fn(np.random.default_rng(FRESH[0]))
    d1 = boot_fn(np.random.default_rng(FRESH[1]))
    est_tol, ci_tol, p_tol = mc_tols(d0[5])
    e, _, lo, hi, p = d1[:5]
    check(f"{name}.est", close(e, rec.get(est_key), est_tol),
          f"got {e:.6f} vs {rec.get(est_key)} (tol {est_tol:.2e})")
    check(f"{name}.ci_lo", close(lo, rec.get(ci_low_key), ci_tol),
          f"got {lo:.6f} vs {rec.get(ci_low_key)} (tol {ci_tol:.2e})")
    check(f"{name}.ci_hi", close(hi, rec.get(ci_upper_key), ci_tol),
          f"got {hi:.6f} vs {rec.get(ci_upper_key)} (tol {ci_tol:.2e})")
    check(f"{name}.p", abs(p - rec.get(p_key)) <= p_tol,
          f"got {p:.4f} vs {rec.get(p_key)}")
    if verdict and gate is not None:
        cat = verdict_cat(n, lo, hi, p, gate, rej)
        rec_cat = rec_cat_of(rec.get("verdict", ""))
        check(f"{name}.verdict", cat == rec_cat,
              f"fresh {cat} vs recorded {rec.get('verdict')}")


# ---------------------------------------------------------------------------
# Event/return helpers
# ---------------------------------------------------------------------------
def rets_for(evs, n=N_PRIMARY, cost=COST_PRIMARY, flip=False):
    out = []
    for ev in evs:
        cl = _FILES[ev["rel"]]["Close"].to_numpy()
        w = wpos_of(ev["rel"])
        gross = (cl[w[ev["e_pos"] + n]] - ev["entry_open"]) / ev["entry_open"]
        out.append((-gross if flip else gross) - cost)
    return np.array(out)


def build_pools(entry_positions, with_reach=False):
    """Per-file, per-hour baseline pools (gross): a baseline bar c must have
    c+1 and c+N within the window end, in the same hour bucket, and must not
    be an event entry bar. Optionally the F2 reach flags."""
    hours = list(range(9, 16))
    same = {}
    uni = {h: [] for h in hours}
    same_reach = {}
    uni_reach = {h: [] for h in hours}
    for rel in sorted(_FILES):
        df = _FILES[rel]
        w = wpos_of(rel)
        n = len(w)
        if n <= N_PRIMARY + 1:
            same[rel] = {}
            same_reach[rel] = {}
            continue
        hi = df["High"].to_numpy()[w]
        op = df["Open"].to_numpy()[w]
        cl = df["Close"].to_numpy()[w]
        times = df.index[w]
        c = np.arange(n)[: n - N_PRIMARY - 1]
        if len(c) == 0:
            same[rel] = {}
            same_reach[rel] = {}
            continue
        rets = (cl[c + N_PRIMARY] - op[c + 1]) / op[c + 1]
        if with_reach:
            prefix = np.maximum.accumulate(hi)
            suffix = np.empty(n)
            suffix[-1] = hi[-1]
            for i in range(n - 2, -1, -1):
                suffix[i] = max(suffix[i + 1], hi[i])
            reach = suffix[c + 1] >= prefix[c]
        per_hour = {}
        per_hour_reach = {}
        ep = entry_positions.get(rel, set())
        ep_arr = np.fromiter(ep, dtype=int, count=len(ep)) if ep \
            else np.array([], dtype=int)
        for h in hours:
            hm = times[c].hour == h
            keep = hm & ~np.isin(c, ep_arr)
            if keep.any():
                per_hour[h] = rets[keep]
                if with_reach:
                    per_hour_reach[h] = reach[keep]
        same[rel] = per_hour
        same_reach[rel] = per_hour_reach
        for h, v in per_hour.items():
            uni[h].append(v)
            if with_reach:
                uni_reach[h].append(per_hour_reach[h])
    uni = {h: np.concatenate(v) if v else np.array([])
           for h, v in uni.items()}
    uni_reach = {h: np.concatenate(v) if v else np.array([])
                 for h, v in uni_reach.items()}
    if with_reach:
        return same, uni, same_reach, uni_reach
    return same, uni


def sample_baseline(evs, same, uni, kind, flip=False):
    def sample_b(M, rng):
        out = np.empty(M)
        for i in range(M):
            ev = evs[rng.integers(0, len(evs))]
            h = ev["hour"]
            pool = (same[ev["rel"]].get(h) if kind == "same" else uni.get(h))
            if pool is None or len(pool) == 0:
                out[i] = 0.0
            else:
                v = pool[rng.integers(0, len(pool))]
                out[i] = -v if flip else v
        return out
    return sample_b


def f2_adjusted(evs, same, uni, kind):
    out = []
    for ev in evs:
        h = ev["hour"]
        pool = (same[ev["rel"]].get(h) if kind == "same" else uni.get(h))
        base = pool.mean() if (pool is not None and len(pool)) else 0.0
        cl = _FILES[ev["rel"]]["Close"].to_numpy()
        w = wpos_of(ev["rel"])
        r = (cl[w[ev["e_pos"] + N_PRIMARY]] - ev["entry_open"]) \
            / ev["entry_open"] - COST_PRIMARY
        out.append(r - base)
    return np.array(out)


def pair_rets(pairs, entry_key):
    out = []
    for pr in pairs:
        w = wpos_of(pr["rel"])
        cl = _FILES[pr["rel"]]["Close"].to_numpy()
        k = pr["c1_pos"]
        if entry_key == "e1_open":
            gross = (cl[w[k + 1 + N_PRIMARY]] - pr["e1_open"]) / pr["e1_open"]
        else:
            gross = (cl[w[k + 2 + N_PRIMARY]] - pr["e2_open"]) / pr["e2_open"]
        out.append(gross - COST_PRIMARY)
    return np.array(out)


def reach_events(events):
    flags = []
    for ev in events:
        hi = _FILES[ev["rel"]]["High"].to_numpy()
        w = wpos_of(ev["rel"])
        tail = hi[w[ev["e_pos"] + 1: ev["npos"]]]
        flags.append(bool(tail.max() >= ev["target"]))
    return np.array(flags, dtype=float)


# ===========================================================================
# Campaign #15 — B-01 (measure_intraday.py)
# ===========================================================================
def verify_15(res):
    events, chase, dropped = [], [], 0
    for rel in sorted(_FILES):
        det = detect_b01(_FILES[rel], wpos_of(rel), n_need=N_PRIMARY)
        date, ticker = rel.split("/")
        ticker = ticker[:-len(".parquet")]
        npos = len(wpos_of(rel))
        for ev in det["events"]:
            ev["rel"] = rel
            ev["date"] = date
            ev["ticker"] = ticker
            ev["npos"] = npos
            ev["valid_n"] = ev["e_pos"] + N_PRIMARY < npos
            events.append(ev)
        for ch in det["chase"]:
            ch["rel"] = rel
            ch["npos"] = npos
            chase.append(ch)
        dropped += det["dropped"]
    valid = [ev for ev in events if ev["valid_n"]]
    rets = rets_for(valid)

    # Census EXACT
    census = {"n_events": len(events), "n_measured_f1": len(valid),
              "n_chase": len(chase),
              "n_dropped_f1": sum(1 for ev in events if not ev["valid_n"])}
    for k, v in census.items():
        check(f"15.census.{k}", close(v, res.get(k)),
              f"got {v} vs {res.get(k)}")

    # Floors EXACT
    fl = res.get("floors", {})
    if fl:
        bar_dates = sorted({rel.split("/")[0] for rel in _FILES})
        event_dates = sorted({ev["date"] for ev in events})
        tickers = {ev["ticker"] for ev in events}
        want = {"window_bar_dates": len(bar_dates), "events": len(events),
                "tickers": len(tickers), "dates_with_events": len(event_dates),
                "met": (len(bar_dates) >= fl.get("floors", {}).get(
                    "min_bar_dates", 20)
                        and len(events) >= fl.get("floors", {}).get(
                            "min_events", 2000)
                        and len(tickers) >= fl.get("floors", {}).get(
                            "min_tickers", 100)
                        and len(event_dates) >= fl.get("floors", {}).get(
                            "min_dates_with_events", 15))}
        for k in ("window_bar_dates", "events", "tickers",
                  "dates_with_events", "met"):
            if k in fl:
                check(f"15.floors.{k}", close(want[k], fl.get(k)),
                      f"got {want[k]} vs {fl.get(k)}")

    positions = {rel: {ev["e_pos"] for ev in events if ev["rel"] == rel}
                 for rel in _FILES}
    same, uni, same_reach, uni_reach = build_pools(positions, with_reach=True)

    # F1 — 2 Holm slots
    fam = res.get("f1", {})
    fam_order = ["same_ticker", "universe"]
    gates = gates_of(fam)
    for slot in fam_order:
        rec = fam.get(slot, {})
        kind = "same" if slot == "same_ticker" else "uni"
        name = f"15.f1.{slot}"
        check(f"{name}.n", close(len(valid), rec.get("n")),
              f"got {len(valid)} vs {rec.get('n')}")
        check(f"{name}.mean_ret", close(rets.mean(), rec.get("mean_ret")),
              f"got {rets.mean():.6f} vs {rec.get('mean_ret')}")
        sb = sample_baseline(valid, same, uni, kind)
        check_mc(name, rec, lambda rng: boot_excess(rets, sb, rng),
                 len(valid), verdict=True, gate=gates.get(slot),
                 rej=(rec.get("p", 1.0) <= gates.get(slot, 0)))
    check_holm("15.f1", fam, fam_order)

    # F2 — reach-rate, 2 Holm slots
    reach = reach_events(events)
    fam = res.get("f2", {})
    gates = gates_of(fam)

    def sample_reach(M, rng, kind):
        out = np.empty(M)
        for i in range(M):
            ev = events[rng.integers(0, len(events))]
            h = ev["hour"]
            pool = (same_reach[ev["rel"]].get(h)
                    if kind == "same" else uni_reach.get(h))
            if pool is None or len(pool) == 0:
                out[i] = 0.0
            else:
                out[i] = pool[rng.integers(0, len(pool))]
        return out
    for slot in fam_order:
        rec = fam.get(slot, {})
        kind = "same" if slot == "same_ticker" else "uni"
        name = f"15.f2.{slot}"
        check(f"{name}.n", close(len(reach), rec.get("n")),
              f"got {len(reach)} vs {rec.get('n')}")
        check(f"{name}.reach_rate", close(reach.mean(), rec.get("reach_rate")),
              f"got {reach.mean():.6f} vs {rec.get('reach_rate')}")
        sb = (lambda M, rng, kind=kind: sample_reach(M, rng, kind))
        check_mc(name, rec, lambda rng: boot_excess(reach, sb, rng),
                 len(reach), verdict=True, gate=gates.get(slot),
                 rej=(rec.get("p", 1.0) <= gates.get(slot, 0)))
    check_holm("15.f2", fam, fam_order)

    # F3 — pullback vs chase, 2 Holm slots
    ch = [c for c in chase if c["e_pos"] + N_PRIMARY < c["npos"]]
    ch_ret = rets_for(ch)
    both = {ev["rel"] for ev in valid} & {c["rel"] for c in ch}
    pb_both = np.array([r for i, ev in enumerate(valid)
                        if ev["rel"] in both for r in [rets[i]]])
    ch_both = np.array([r for i, c in enumerate(ch)
                        if c["rel"] in both for r in [ch_ret[i]]])
    fam = res.get("f3", {})
    gates = gates_of(fam)
    for slot, (x, y) in (("same_ticker_pairs", (pb_both, ch_both)),
                         ("universe", (rets, ch_ret))):
        rec = fam.get(slot, {})
        name = f"15.f3.{slot}"
        check(f"{name}.n", close(len(x), rec.get("n")),
              f"got {len(x)} vs {rec.get('n')}")
        check(f"{name}.n_chase", close(len(y), rec.get("n_chase")),
              f"got {len(y)} vs {rec.get('n_chase')}")
        if len(x) and rec.get("mean_pullback") is not None:
            check(f"{name}.mean_pullback",
                  close(x.mean(), rec.get("mean_pullback")),
                  f"got {x.mean():.6f} vs {rec.get('mean_pullback')}")
            check(f"{name}.mean_chase", close(y.mean(), rec.get("mean_chase")),
                  f"got {y.mean():.6f} vs {rec.get('mean_chase')}")
            sb = (lambda M, rng, y=y: y[rng.integers(0, len(y), size=M)])
            check_mc(name, rec, lambda rng: boot_excess(x, sb, rng),
                     len(x), verdict=True, gate=gates.get(slot),
                     rej=(rec.get("p", 1.0) <= gates.get(slot, 0)))
    check_holm("15.f3", fam,
               ["same_ticker_pairs", "universe"])


# ===========================================================================
# Campaign #19 — entry timing (measure_intraday_entry.py)
# ===========================================================================
def verify_19(res):
    f1_events, f2_events, f3_pairs = [], [], []
    dropped_f1 = dropped_f2 = dropped_f3 = 0
    for rel in sorted(_FILES):
        rv = detect_reversal(_FILES[rel], wpos_of(rel))
        pc = detect_pullback_count(_FILES[rel], wpos_of(rel))
        sc = detect_second_conf(_FILES[rel], wpos_of(rel))
        date, ticker = rel.split("/")
        ticker = ticker[:-len(".parquet")]
        npos = len(wpos_of(rel))
        for ev in rv["long"] + rv["short"]:
            ev["rel"], ev["date"], ev["ticker"] = rel, date, ticker
            ev["npos"] = npos
            ev["valid_n"] = ev["e_pos"] + 1 + N_PRIMARY < npos
            f1_events.append(ev)
        for ev in pc["events"]:
            ev["rel"], ev["date"], ev["ticker"] = rel, date, ticker
            ev["npos"] = npos
            ev["valid_n"] = ev["e_pos"] + 1 + N_PRIMARY < npos
            f2_events.append(ev)
        for pr in sc["pairs"]:
            pr["rel"], pr["date"], pr["ticker"] = rel, date, ticker
            pr["npos"] = npos
            pr["both_valid"] = (pr["c1_pos"] + 1 + N_PRIMARY < npos
                                and pr["c1_pos"] + 2 + N_PRIMARY < npos)
            f3_pairs.append(pr)
        dropped_f1 += rv["dropped"]
        dropped_f2 += pc["dropped"]
        dropped_f3 += sc["dropped"]

    f1_valid = sum(1 for ev in f1_events if ev["valid_n"])
    f2_valid = sum(1 for ev in f2_events if ev["valid_n"])
    f3_both = sum(1 for pr in f3_pairs if pr["both_valid"])
    census = {"n_f1_events": len(f1_events), "n_f1_valid": f1_valid,
              "n_f1_dropped": dropped_f1,
              "n_f2_events": len(f2_events), "n_f2_valid": f2_valid,
              "n_f2_dropped": dropped_f2,
              "n_f3_pairs": len(f3_pairs), "n_f3_both_valid": f3_both,
              "n_f3_dropped": dropped_f3, "n_f1": f1_valid}
    for k, v in census.items():
        if k in res:
            check(f"19.census.{k}", close(v, res.get(k)),
                  f"got {v} vs {res.get(k)}")

    fl = res.get("floors", {})
    if fl:
        valid = [ev for ev in f1_events if ev["valid_n"]]
        bar_dates = sorted({rel.split("/")[0] for rel in _FILES})
        event_dates = sorted({ev["date"] for ev in valid})
        tickers = {ev["ticker"] for ev in valid}
        want = {"window_bar_dates": len(bar_dates),
                "events_f1_valid": len(valid), "tickers": len(tickers),
                "dates_with_events": len(event_dates),
                "met": (len(bar_dates) >= fl.get("floors", {}).get(
                    "min_bar_dates", 20)
                        and len(valid) >= fl.get("floors", {}).get(
                            "min_events", 2000)
                        and len(tickers) >= fl.get("floors", {}).get(
                            "min_tickers", 100)
                        and len(event_dates) >= fl.get("floors", {}).get(
                            "min_dates_with_events", 15))}
        for k in ("window_bar_dates", "events_f1_valid", "tickers",
                  "dates_with_events", "met"):
            if k in fl:
                check(f"19.floors.{k}", close(want[k], fl.get(k)),
                      f"got {want[k]} vs {fl.get(k)}")

    positions = {rel: {ev["e_pos"] for ev in f1_events if ev["rel"] == rel}
                 for rel in _FILES}
    same, uni = build_pools(positions)

    # F1 — 2 Holm slots (long, short), universe primary + same-ticker secondary
    fam = res.get("f1", {})
    gates = gates_of(fam)
    for slot, dir_name in (("long", "long"), ("short", "short")):
        evs = [ev for ev in f1_events
               if ev["dir"] == dir_name and ev["valid_n"]]
        rec = fam.get(slot, {})
        name = f"19.f1.{slot}"
        check(f"{name}.n", close(len(evs), rec.get("n")),
              f"got {len(evs)} vs {rec.get('n')}")
        if not evs:
            continue
        flip = (dir_name == "short")
        rets = rets_for(evs, flip=flip)
        check(f"{name}.mean_ret", close(rets.mean(), rec.get("mean_ret")),
              f"got {rets.mean():.6f} vs {rec.get('mean_ret')}")
        sb_uni = sample_baseline(evs, same, uni, "uni", flip=flip)
        sb_same = sample_baseline(evs, same, uni, "same", flip=flip)
        check_mc(name, rec, lambda rng: boot_excess(rets, sb_uni, rng),
                 len(evs), verdict=True, gate=gates.get(slot),
                 rej=(rec.get("p", 1.0) <= gates.get(slot, 0)))
        eu = rec.get("excess_universe", {})
        if "est" in eu:
            check_mc(f"{name}.excess_universe", eu,
                     lambda rng: boot_excess(rets, sb_uni, rng), len(evs))
        es = rec.get("excess_same_ticker", {})
        if "est" in es:
            check_mc(f"{name}.excess_same_ticker", es,
                     lambda rng: boot_excess(rets, sb_same, rng), len(evs))
    check_holm("19.f1", fam, ["long", "short"])

    # F2 — pullback-count, 1 Holm slot (early - late)
    early = [ev for ev in f2_events if ev["k"] <= 2 and ev["valid_n"]]
    late = [ev for ev in f2_events if ev["k"] >= 3 and ev["valid_n"]]
    fam = res.get("f2", {})
    rec = fam.get("early_minus_late", {})
    n_rec = rec.get("n")
    want_n = min(len(early), len(late))
    check("19.f2.early_minus_late.n", close(want_n, n_rec),
          f"got {want_n} vs {n_rec}")
    check("19.f2.early_minus_late.n_early", close(len(early), rec.get("n_early")),
          f"got {len(early)} vs {rec.get('n_early')}")
    check("19.f2.early_minus_late.n_late", close(len(late), rec.get("n_late")),
          f"got {len(late)} vs {rec.get('n_late')}")
    if len(early) >= MIN_SLOT and len(late) >= MIN_SLOT:
        er = rets_for(early)
        lr = rets_for(late)
        check("19.f2.early_minus_late.mean_early",
              close(er.mean(), rec.get("mean_early")),
              f"got {er.mean():.6f} vs {rec.get('mean_early')}")
        check("19.f2.early_minus_late.mean_late",
              close(lr.mean(), rec.get("mean_late")),
              f"got {lr.mean():.6f} vs {rec.get('mean_late')}")
        check_mc("19.f2.early_minus_late", rec,
                 lambda rng: contrast_two(er, lr, rng), want_n,
                 verdict=True, gate=ALPHA,
                 rej=(rec.get("p", 1.0) <= ALPHA))
        adj_same = rec.get("adj_same_ticker", {})
        if "est" in adj_same:
            check_mc("19.f2.early_minus_late.adj_same_ticker", adj_same,
                     lambda rng: contrast_two(f2_adjusted(early, same, uni,
                                                          "same"),
                                              f2_adjusted(late, same, uni,
                                                          "same"), rng),
                     want_n)
        adj_uni = rec.get("adj_universe", {})
        if "est" in adj_uni:
            check_mc("19.f2.early_minus_late.adj_universe", adj_uni,
                     lambda rng: contrast_two(f2_adjusted(early, same, uni,
                                                          "uni"),
                                              f2_adjusted(late, same, uni,
                                                          "uni"), rng),
                     want_n)
    check_holm("19.f2", fam, ["early_minus_late"])

    # F3 — second-confirmation, 1 Holm slot (paired E2-E1)
    pairs = [pr for pr in f3_pairs if pr["both_valid"]]
    fam = res.get("f3", {})
    rec = fam.get("e2_minus_e1", {})
    check("19.f3.e2_minus_e1.n", close(0 if len(pairs) < MIN_SLOT
                                       else len(pairs), rec.get("n")),
          f"got {0 if len(pairs) < MIN_SLOT else len(pairs)} vs {rec.get('n')}")
    check("19.f3.e2_minus_e1.n_pairs", close(len(pairs), rec.get("n_pairs")),
          f"got {len(pairs)} vs {rec.get('n_pairs')}")
    if len(pairs) >= MIN_SLOT:
        e1 = pair_rets(pairs, "e1_open")
        e2 = pair_rets(pairs, "e2_open")
        check("19.f3.e2_minus_e1.mean_e1", close(e1.mean(), rec.get("mean_e1")),
              f"got {e1.mean():.6f} vs {rec.get('mean_e1')}")
        check("19.f3.e2_minus_e1.mean_e2", close(e2.mean(), rec.get("mean_e2")),
              f"got {e2.mean():.6f} vs {rec.get('mean_e2')}")
        check_mc("19.f3.e2_minus_e1", rec,
                 lambda rng: contrast_paired(e2 - e1, rng), len(pairs),
                 verdict=True, gate=ALPHA,
                 rej=(rec.get("p", 1.0) <= ALPHA))
    check_holm("19.f3", fam, ["e2_minus_e1"])


# ===========================================================================
# Campaign #20 — exit rules (measure_intraday_exit.py) — CORRECT ci semantics
# ===========================================================================
def align_exit(events):
    """F1 entry set (e+60 within session, non-degenerate) + per-event
    realized returns of every rule/benchmark + mechanism flags."""
    res = {"bre": [], "ladder": [], "flat": [], "fixed_n": [],
           "fixed_2r": [], "half_fired": [], "legs": [],
           "flat_flag": [], "evs": []}
    for ev in sorted(events, key=lambda ev: (ev["rel"], ev["e_pos"])):
        w = wpos_of(ev["rel"])
        df = _FILES[ev["rel"]]
        op = df["Open"].to_numpy()[w]
        hi = df["High"].to_numpy()[w]
        lo = df["Low"].to_numpy()[w]
        cl = df["Close"].to_numpy()[w]
        e, entry, stop = ev["e_pos"], ev["entry_open"], ev["stop"]
        npos = len(w)
        if e + N_PRIMARY >= npos:
            continue
        wmins = (df.index[w].hour.to_numpy() * 60 +
                 df.index[w].minute.to_numpy())
        br = breakeven_trail_s(op, hi, lo, cl, wmins, e, entry, stop, npos)
        if br is None:
            continue
        vw = vwap_series(df, w)
        ld = ladder_s(op, hi, lo, cl, vw, e, entry, npos)
        fl = flat_out_s(cl, e, entry, npos)
        fn = fixed_n_s(cl, e, entry, npos)
        f2 = fixed_2r_s(op, hi, lo, cl, e, entry, stop, npos)
        res["bre"].append(br[0] - COST_PRIMARY)
        res["ladder"].append(ld[0] - COST_PRIMARY)
        res["flat"].append(fl[0] - COST_PRIMARY)
        res["fixed_n"].append(fn - COST_PRIMARY)
        res["fixed_2r"].append(f2 - COST_PRIMARY)
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


def verify_20(res):
    events = []
    for rel in sorted(_FILES):
        det = detect_b01(_FILES[rel], wpos_of(rel), n_need=N_PRIMARY)
        date, ticker = rel.split("/")
        ticker = ticker[:-len(".parquet")]
        npos = len(wpos_of(rel))
        for ev in det["events"]:
            ev["rel"] = ev.get("rel", rel)
            ev["date"] = ev.get("date", date)
            ev["ticker"] = ev.get("ticker", ticker)
            ev["npos"] = npos
            ev["evaluable"] = (ev["e_pos"] + N_PRIMARY < npos
                               and ev["stop"] < ev["entry_open"])
            events.append(ev)

    a = align_exit(events)

    fl = res.get("floors", {})
    if fl:
        eval_evs = [ev for ev in events if ev["evaluable"]]
        bar_dates = sorted({rel.split("/")[0] for rel in _FILES})
        want = {"window_bar_dates": len(bar_dates),
                "events_f1_valid": len(eval_evs),
                "tickers": len({ev["ticker"] for ev in eval_evs}),
                "dates_with_events": len({ev["date"] for ev in eval_evs}),
                "met": (len(bar_dates) >= fl.get("min_bar_dates", 20)
                        and len(eval_evs) >= fl.get("min_events", 2000)
                        and len({ev["ticker"] for ev in eval_evs}) >= fl.get(
                            "min_tickers", 100)
                        and len({ev["date"] for ev in eval_evs}) >= fl.get(
                            "min_dates_with_events", 15))}
        for k in ("window_bar_dates", "events_f1_valid", "tickers",
                  "dates_with_events", "met"):
            if k in fl:
                check(f"20.floors.{k}", close(want[k], fl.get(k)),
                      f"got {want[k]} vs {fl.get(k)}")

    # F1 — 3 Holm slots (bre, ladder, flat), CORRECT ci semantics
    fam = res.get("f1", {})
    gates = gates_of(fam)
    for k in ("bre", "ladder", "flat"):
        rec = fam.get(k, {})
        rule = a[k]
        bench_n = a["fixed_n"]
        bench_2r = a["fixed_2r"]
        name = f"20.f1.{k}"
        check(f"{name}.n", close(len(rule), rec.get("n")),
              f"got {len(rule)} vs {rec.get('n')}")
        if len(rule) < MIN_SLOT:
            continue
        check(f"{name}.mean_rule", close(rule.mean(), rec.get("mean_rule")),
              f"got {rule.mean():.6f} vs {rec.get('mean_rule')}")
        check(f"{name}.mean_fixed_n",
              close(bench_n.mean(), rec.get("mean_fixed_n")),
              f"got {bench_n.mean():.6f} vs {rec.get('mean_fixed_n')}")
        check(f"{name}.mean_fixed_2r",
              close(bench_2r.mean(), rec.get("mean_fixed_2r")),
              f"got {bench_2r.mean():.6f} vs {rec.get('mean_fixed_2r')}")
        check_mc(name, rec, lambda rng: paired_contrast(rule, bench_n, rng),
                 len(rule), est_key="excess_primary",
                 verdict=True, gate=gates.get(k),
                 rej=(rec.get("p", 1.0) <= gates.get(k, 0)))
        # fixed-2R secondary contrast (correct lo/hi semantics).
        d0 = paired_contrast(rule, bench_2r, np.random.default_rng(FRESH[0]))
        d1 = paired_contrast(rule, bench_2r, np.random.default_rng(FRESH[1]))
        et, ct, pt = mc_tols(d0[5])
        e1, _, l1, h1, p1 = d1[:5]
        check(f"{name}.diff_2r", close(e1, rec.get("diff_2r"), et),
              f"got {e1:.6f} vs {rec.get('diff_2r')} (tol {et:.2e})")
        check(f"{name}.diff_2r_lo", close(l1, rec.get("diff_2r_lo"), ct),
              f"got {l1:.6f} vs {rec.get('diff_2r_lo')} (tol {ct:.2e})")
        check(f"{name}.diff_2r_hi", close(h1, rec.get("diff_2r_hi"), ct),
              f"got {h1:.6f} vs {rec.get('diff_2r_hi')} (tol {ct:.2e})")
        check(f"{name}.p_2r", abs(p1 - rec.get("p_2r")) <= pt,
              f"got {p1:.4f} vs {rec.get('p_2r')}")
    check_holm("20.f1", fam, ["bre", "ladder", "flat"])
    cats = [rec_cat_of(fam[k]["verdict"]) for k in ("bre", "ladder", "flat")]
    want_fam = ("EDGE" if all(c == "EDGE" for c in cats)
                else "FADE" if all(c == "FADE" for c in cats)
                else "INCONCLUSIVE" if any(c == "INCONCLUSIVE" for c in cats)
                else "NO EDGE")
    check("20.f1.family", rec_cat_of(res.get("f1_family")) == want_fam,
          f"got {res.get('f1_family')} vs {want_fam}")

    # F2 — the flat premise, 1 Holm slot (CORRECT ci semantics)
    fam = res.get("f2", {})
    rec = fam.get("flat_premise", {})
    idx_flat = np.flatnonzero(a["flat_flag"] == 1)
    idx_non = np.flatnonzero(a["flat_flag"] == 0)
    fr = a["fixed_n"][idx_flat]
    check("20.f2.flat_premise.n", close(len(fr), rec.get("n")),
          f"got {len(fr)} vs {rec.get('n')}")
    if len(fr) >= MIN_SLOT:
        pool = {}
        for i in idx_non:
            h = a["evs"][i]["hour"]
            pool.setdefault(h, []).append(a["fixed_n"][i])

        def sample_b(M, rng):
            arr = np.empty(M)
            for j in range(M):
                fi = idx_flat[rng.integers(0, len(idx_flat))]
                h = a["evs"][fi]["hour"]
                p = pool.get(h)
                if not p:
                    p = [v for k in pool for v in pool[k]]
                arr[j] = p[rng.integers(0, len(p))]
            return arr
        check("20.f2.flat_premise.mean_flat",
              close(fr.mean(), rec.get("mean_flat")),
              f"got {fr.mean():.6f} vs {rec.get('mean_flat')}")
        check_mc("20.f2.flat_premise", rec,
                 lambda rng: boot_excess(fr, sample_b, rng), len(fr),
                 est_key="diff",
                 verdict=True, gate=ALPHA,
                 rej=(rec.get("p", 1.0) <= ALPHA))
    # Family (single slot) = slot verdict (#20 strips _family into f2_family).
    rec_cat = rec_cat_of(res.get("f2_family", "NO EDGE"))
    slot_cat = rec_cat_of(rec.get("verdict", "NO EDGE"))
    check("20.f2.family", rec_cat == slot_cat,
          f"family {res.get('f2_family')} vs slot {rec.get('verdict')}")


# ===========================================================================
# Campaign #21 — the two-filter veto (measure_intraday_veto.py)
# ===========================================================================
def verify_21(res):
    events = []
    dropped = 0
    for rel in sorted(_FILES):
        df = _FILES[rel]
        rv = detect_reversal(df, wpos_of(rel))
        date, ticker = rel.split("/")
        ticker = ticker[:-len(".parquet")]
        npos = len(wpos_of(rel))
        w = wpos_of(rel)
        closes = df["Close"].to_numpy()
        for ev in rv["long"]:
            ev["rel"], ev["date"], ev["ticker"] = rel, date, ticker
            ev["npos"] = npos
            ev["e_abs"] = int(w[ev["e_pos"]])
            ev["valid"] = ev["e_pos"] + 1 + N_PRIMARY < npos
            ev["macd"] = macd_at(closes, ev["e_abs"])
            ev["vol_spike"] = volume_spike(df, w, ev["e_abs"])
            ev["evaluable"] = ev["macd"] is not None
            ev["macd_neg"] = ev["macd"] is not None and ev["macd"] < 0
            ev["veto_fail"] = (ev["evaluable"]
                               and (ev["macd_neg"] or ev["vol_spike"]))
            ev["veto_pass"] = ev["evaluable"] and not ev["veto_fail"]
            events.append(ev)
        dropped += rv["dropped"]

    fl = res.get("floors", {})
    if fl:
        valid = [ev for ev in events if ev["valid"]]
        bar_dates = sorted({rel.split("/")[0] for rel in _FILES})
        want = {"window_bar_dates": len(bar_dates),
                "events_f1_valid": len(valid),
                "tickers": len({ev["ticker"] for ev in valid}),
                "dates_with_events": len({ev["date"] for ev in valid}),
                "met": (len(bar_dates) >= fl.get("min_bar_dates", 20)
                        and len(valid) >= fl.get("min_events", 2000)
                        and len({ev["ticker"] for ev in valid}) >= fl.get(
                            "min_tickers", 100)
                        and len({ev["date"] for ev in valid}) >= fl.get(
                            "min_dates_with_events", 15))}
        for k in ("window_bar_dates", "events_f1_valid", "tickers",
                  "dates_with_events", "met"):
            if k in fl:
                check(f"21.floors.{k}", close(want[k], fl.get(k)),
                      f"got {want[k]} vs {fl.get(k)}")

    # F1 — 4 Holm slots
    valid = [ev for ev in events if ev["valid"]]
    passes = [ev for ev in valid if ev["veto_pass"]]
    fails = [ev for ev in valid if ev["veto_fail"]]
    raw = [ev for ev in valid if ev["evaluable"]]
    macd_ge0 = [ev for ev in valid if ev["macd"] is not None and ev["macd"] >= 0]
    macd_lt0 = [ev for ev in valid if ev["macd"] is not None and ev["macd"] < 0]
    nosp = [ev for ev in valid if not ev["vol_spike"]]
    sp = [ev for ev in valid if ev["vol_spike"]]
    fam = res.get("f1", {})
    gates = gates_of(fam)

    def slot_checks(key, label, evs_a, evs_b):
        rec = fam.get(key, {})
        name = f"21.f1.{key}"
        n = min(len(evs_a), len(evs_b))
        check(f"{name}.n", close(n, rec.get("n")), f"got {n} vs {rec.get('n')}")
        check(f"{name}.n_a", close(len(evs_a), rec.get("n_a")),
              f"got {len(evs_a)} vs {rec.get('n_a')}")
        check(f"{name}.n_b", close(len(evs_b), rec.get("n_b")),
              f"got {len(evs_b)} vs {rec.get('n_b')}")
        if len(evs_a) < MIN_SLOT or len(evs_b) < MIN_SLOT:
            return
        ra = rets_for(evs_a)
        rb = rets_for(evs_b)
        check(f"{name}.mean_a", close(ra.mean(), rec.get("mean_a")),
              f"got {ra.mean():.6f} vs {rec.get('mean_a')}")
        check(f"{name}.mean_b", close(rb.mean(), rec.get("mean_b")),
              f"got {rb.mean():.6f} vs {rec.get('mean_b')}")
        check_mc(name, rec, lambda rng: contrast_two(ra, rb, rng), n,
                 verdict=True, gate=gates.get(key),
                 rej=(rec.get("p", 1.0) <= gates.get(key, 0)))

    slot_checks("pass_minus_fail", "pass - fail", passes, fails)
    slot_checks("pass_minus_raw", "pass - raw", passes, raw)
    slot_checks("macd_leg", "macd leg", macd_ge0, macd_lt0)
    slot_checks("volume_leg", "volume leg", nosp, sp)
    check_holm("21.f1", fam,
               ["pass_minus_fail", "pass_minus_raw", "macd_leg", "volume_leg"])
    cats = [rec_cat_of(fam[k]["verdict"]) for k in
            ("pass_minus_fail", "pass_minus_raw", "macd_leg", "volume_leg")]
    want_fam = ("EDGE" if all(c == "EDGE" for c in cats)
                else "FADE" if all(c == "FADE" for c in cats)
                else "INCONCLUSIVE" if any(c == "INCONCLUSIVE" for c in cats)
                else "NO EDGE")
    check("21.f1.family", rec_cat_of(res.get("f1_family")) == want_fam,
          f"got {res.get('f1_family')} vs {want_fam}")

    # Kill-rate rows (the veto census) — deterministic EXACT.
    rows = res.get("rows", {})
    eval_evs = [ev for ev in valid if ev["evaluable"]]
    n = len(eval_evs)
    e_passes = [ev for ev in eval_evs if ev["veto_pass"]]
    e_fails = [ev for ev in eval_evs if ev["veto_fail"]]
    e_lt = [ev for ev in eval_evs if ev["macd"] < 0]
    e_sp = [ev for ev in eval_evs if ev["vol_spike"]]
    e_both = [ev for ev in eval_evs if ev["macd"] < 0 and ev["vol_spike"]]
    want_rows = {
        "n": n,
        "n_unavailable_macd": sum(1 for ev in valid if not ev["evaluable"]),
        "n_veto_pass": len(e_passes),
        "n_veto_fail": len(e_fails),
        "n_macd_killed": len(e_lt),
        "n_vol_killed": len(e_sp),
        "n_both_killed": len(e_both),
    }
    for k, v in want_rows.items():
        if k in rows:
            check(f"21.rows.{k}", close(v, rows.get(k)),
                  f"got {v} vs {rows.get(k)}")
    if n:
        check("21.rows.pass_rate",
              close(len(e_passes) / n, rows.get("pass_rate")),
              f"got {len(e_passes)/n:.6f} vs {rows.get('pass_rate')}")
        check("21.rows.fail_rate",
              close(len(e_fails) / n, rows.get("fail_rate")),
              f"got {len(e_fails)/n:.6f} vs {rows.get('fail_rate')}")
        check("21.rows.macd_kill_rate",
              close(len(e_lt) / n, rows.get("macd_kill_rate")),
              f"got {len(e_lt)/n:.6f} vs {rows.get('macd_kill_rate')}")
        check("21.rows.vol_kill_rate",
              close(len(e_sp) / n, rows.get("vol_kill_rate")),
              f"got {len(e_sp)/n:.6f} vs {rows.get('vol_kill_rate')}")
        check("21.rows.both_kill_rate",
              close(len(e_both) / n, rows.get("both_kill_rate")),
              f"got {len(e_both)/n:.6f} vs {rows.get('both_kill_rate')}")
    # Means of the kill-rate decomposition (deterministic).
    means = rows.get("means", {})
    if means and n:
        pr = rets_for(e_passes) if e_passes else np.array([])
        fr = rets_for(e_fails) if e_fails else np.array([])
        m_ge = rets_for(macd_ge0) if macd_ge0 else np.array([])
        m_lt = rets_for(macd_lt0) if macd_lt0 else np.array([])
        s_ = rets_for(e_sp) if e_sp else np.array([])
        e_nosp = [ev for ev in eval_evs if not ev["vol_spike"]]
        ns = rets_for(e_nosp) if e_nosp else np.array([])
        for key, arr in (("pass", pr), ("fail", fr), ("macd_ge0", m_ge),
                         ("macd_lt0", m_lt), ("vol_spike", s_),
                         ("no_spike", ns)):
            if key in means:
                got = float(arr.mean()) if len(arr) else None
                check(f"21.rows.means.{key}", close(got, means.get(key)),
                      f"got {got} vs {means.get(key)}")


# ===========================================================================
# Campaign #22 — the intraday regime (measure_intraday_regime.py)
# ===========================================================================
CANON = [
    (dtime(4, 0), dtime(7, 0)), (dtime(7, 0), dtime(9, 30)),
    (dtime(9, 30), dtime(10, 0)), (dtime(10, 0), dtime(11, 0)),
    (dtime(11, 0), dtime(12, 0)), (dtime(12, 0), dtime(13, 0)),
    (dtime(13, 0), dtime(14, 0)), (dtime(14, 0), dtime(15, 0)),
    (dtime(15, 0), dtime(16, 0)), (dtime(16, 0), dtime(20, 0)),
]
BUCKET_LABELS = ["04:00-07:00", "07:00-09:30", "09:30-10:00", "10:00-11:00",
                 "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
                 "15:00-16:00", "16:00-20:00"]
F1_SLOTS = [
    {"key": "B1", "label": "B1 (07:00-10:00)", "t0": dtime(7, 0),
     "t1": dtime(10, 0), "cover_idx": [1, 2]},
    {"key": "B2", "label": "B2 (09:30-12:00)", "t0": dtime(9, 30),
     "t1": dtime(12, 0), "cover_idx": [2, 3, 4]},
]
PRE = (dtime(4, 0), dtime(9, 30))
RTH = (dtime(9, 30), dtime(16, 0))


def bucket_pool(t0, t1):
    abs_parts, vol_parts, names = [], [], {}
    for rel, df in _FILES.items():
        t = df.index.time
        m = np.array([(x >= t0) and (x < t1) for x in t])
        x = df[m]
        if len(x) == 0:
            continue
        date = rel.split("/")[0]
        names.setdefault(date, set()).add(rel.split("/")[1][:-len(".parquet")])
        c = x["Close"].to_numpy()
        r = np.abs(np.diff(c) / c[:-1])
        if len(r):
            abs_parts.append(r)
        vol_parts.append(x["Volume"].to_numpy())
    abs_r = np.concatenate(abs_parts) if abs_parts else np.array([])
    vol = np.concatenate(vol_parts) if vol_parts else np.array([])
    return {"abs_r": abs_r, "vol": vol, "n_vol": int(len(vol)),
            "vol_sum": float(vol.sum()) if len(vol) else 0.0,
            "n_dates_ge10": int(sum(1 for s in names.values()
                                    if len(s) >= MIN_NAMES_PER_DATE))}


def window_stats(t0, t1):
    abs_parts, tail_parts, n_bars = [], [], 0
    for df in _FILES.values():
        t = df.index.time
        m = np.array([(x >= t0) and (x < t1) for x in t])
        x = df[m]
        c = x["Close"].to_numpy()
        r = np.abs(np.diff(c) / c[:-1])
        if len(r) == 0:
            continue
        med = float(np.median(r))
        abs_parts.append(r)
        tail_parts.append((r > TAIL_MULT * med).astype(float))
        n_bars += int(len(r))
    if not abs_parts:
        return {"abs_r": np.array([]), "tails": np.array([]), "n_bars": 0}
    return {"abs_r": np.concatenate(abs_parts),
            "tails": np.concatenate(tail_parts), "n_bars": n_bars}


def verify_22(res):
    entries = []
    for rel in sorted(_FILES):
        df = _FILES[rel]
        rv = detect_reversal(df, wpos_of(rel))
        date, ticker = rel.split("/")
        ticker = ticker[:-len(".parquet")]
        npos = len(wpos_of(rel))
        w = wpos_of(rel)
        for ev in rv["long"]:
            ev["rel"], ev["date"], ev["ticker"] = rel, date, ticker
            ev["npos"] = npos
            ev["e_abs"] = int(w[ev["e_pos"]])
            ev["valid"] = ev["e_pos"] + 1 + N_PRIMARY < npos
            t = df.index[ev["e_abs"]].time()
            ev["min"] = t.hour * 60 + t.minute
            ev["hour"] = t.hour
            entries.append(ev)

    fl = res.get("floors", {})
    if fl:
        valid = [ev for ev in entries if ev["valid"]]
        bar_dates = sorted({rel.split("/")[0] for rel in _FILES})
        want = {"window_bar_dates": len(bar_dates),
                "events_f1_valid": len(valid),
                "tickers": len({ev["ticker"] for ev in valid}),
                "dates_with_events": len({ev["date"] for ev in valid}),
                "met": (len(bar_dates) >= fl.get("min_bar_dates", 20)
                        and len(valid) >= fl.get("min_events", 2000)
                        and len({ev["ticker"] for ev in valid}) >= fl.get(
                            "min_tickers", 100)
                        and len({ev["date"] for ev in valid}) >= fl.get(
                            "min_dates_with_events", 15))}
        for k in ("window_bar_dates", "events_f1_valid", "tickers",
                  "dates_with_events", "met"):
            if k in fl:
                check(f"22.floors.{k}", close(want[k], fl.get(k)),
                      f"got {want[k]} vs {fl.get(k)}")

    canon = [bucket_pool(t0, t1) for (t0, t1) in CANON]
    tot = float(sum(df["Volume"].sum() for df in _FILES.values()))

    # F1 — 2 Holm slots (B1, B2)
    fam = res.get("f1", {})
    gates = gates_of(fam)
    for slot in F1_SLOTS:
        key = slot["key"]
        rec = fam.get(key, {})
        name = f"22.f1.{key}"
        cover = set(slot["cover_idx"])
        others = [i for i in range(len(CANON)) if i not in cover]
        pool_r = np.concatenate([canon[i]["abs_r"] for i in slot["cover_idx"]])
        pool_v = np.concatenate([canon[i]["vol"] for i in slot["cover_idx"]])
        i_v_max = max(others, key=lambda i: (canon[i]["abs_r"].mean()
                                             if len(canon[i]["abs_r"])
                                             else -1.0))
        i_l_max = max(others, key=lambda i: (canon[i]["vol_sum"] / tot
                                             if canon[i]["vol_sum"] else -1.0))
        n_r = len(pool_r)
        n_v = len(pool_v)
        n_rr = len(canon[i_v_max]["abs_r"])
        n_rl = len(canon[i_l_max]["vol"])
        coverage = max(canon[i]["n_dates_ge10"] for i in slot["cover_idx"])
        floor_ok = (coverage >= MIN_BUCKET_DATES
                    and n_r >= MIN_SLOT and n_v >= MIN_SLOT
                    and n_rr >= MIN_SLOT and n_rl >= MIN_SLOT)
        for kk, got, key_ in (
                ("n_abs_r", n_r, "n_abs_r"), ("n_vol", n_v, "n_vol"),
                ("n_runner_vol", n_rr, "n_runner_vol"),
                ("n_runner_liq", n_rl, "n_runner_liq"),
                ("coverage_dates_ge10", coverage, "coverage_dates_ge10"),
                ("floor_met", floor_ok, "floor_met")):
            check(f"{name}.{kk}", close(got, rec.get(key_)),
                  f"got {got} vs {rec.get(key_)}")
        check(f"{name}.runner_vol_bucket",
              rec.get("runner_vol_bucket") == BUCKET_LABELS[i_v_max],
              f"got {BUCKET_LABELS[i_v_max]} vs {rec.get('runner_vol_bucket')}")
        check(f"{name}.runner_liq_bucket",
              rec.get("runner_liq_bucket") == BUCKET_LABELS[i_l_max],
              f"got {BUCKET_LABELS[i_l_max]} vs {rec.get('runner_liq_bucket')}")
        v_rec = rec.get("vol", {})
        l_rec = rec.get("liq", {})
        if not floor_ok:
            continue
        check(f"{name}.vol.mean",
              close(pool_r.mean(), v_rec.get("mean")),
              f"got {pool_r.mean():.6f} vs {v_rec.get('mean')}")
        check(f"{name}.vol.mean_r",
              close(canon[i_v_max]["abs_r"].mean(), v_rec.get("mean_r")),
              f"got {canon[i_v_max]['abs_r'].mean():.6f} vs {v_rec.get('mean_r')}")
        check(f"{name}.liq.mean",
              close(pool_v.sum() / tot, l_rec.get("mean")),
              f"got {pool_v.sum()/tot:.6f} vs {l_rec.get('mean')}")
        check(f"{name}.liq.mean_r",
              close(canon[i_l_max]["vol_sum"] / tot, l_rec.get("mean_r")),
              f"got {canon[i_l_max]['vol_sum']/tot:.6f} vs {l_rec.get('mean_r')}")
        check_mc(f"{name}.vol", v_rec,
                 lambda rng: boot_two(pool_r, canon[i_v_max]["abs_r"], rng,
                                      np.mean),
                 n_r)
        check_mc(f"{name}.liq", l_rec,
                 lambda rng: boot_two(pool_v, canon[i_l_max]["vol"], rng,
                                      lambda s: s.sum() / tot),
                 n_v)
        # p = max(vol.p, liq.p), floor_met, verdict.
        p_rec = rec.get("p")
        p_want = max(v_rec.get("p", 0.0), l_rec.get("p", 0.0))
        check(f"{name}.p", close(p_want, p_rec),
              f"got {p_want} vs {p_rec}")
        gate = gates.get(key)
        rej = (rec.get("p", 1.0) <= gate)
        check(f"{name}.holm_gate", close(rec.get("holm_gate"), gate),
              f"got {rec.get('holm_gate')} vs {gate}")
        check(f"{name}.holm_rejected",
              bool(rec.get("holm_rejected")) == rej,
              f"got {rec.get('holm_rejected')} vs {rej}")
        # verdict from fresh vol/liq ci.
        r1 = np.random.default_rng(FRESH[1])
        v1 = boot_two(pool_r, canon[i_v_max]["abs_r"], r1, np.mean)
        l1 = boot_two(pool_v, canon[i_l_max]["vol"], r1, lambda s: s.sum() / tot)
        if not rej:
            cat = "NO EDGE"
        elif v1[2] > 0 and l1[2] > 0:
            cat = "EDGE"
        elif v1[3] < 0 and l1[3] < 0:
            cat = "FADE"
        else:
            cat = "NO EDGE"
        rec_cat = rec_cat_of(rec.get("verdict", ""))
        check(f"{name}.verdict", cat == rec_cat,
              f"fresh {cat} vs recorded {rec.get('verdict')}")
    # family
    fam_order = [s["key"] for s in F1_SLOTS]
    cats = [rec_cat_of(fam[k]["verdict"]) for k in fam_order]
    want_fam = ("EDGE" if all(c == "EDGE" for c in cats)
                else "FADE" if all(c == "FADE" for c in cats)
                else "INCONCLUSIVE" if any(c == "INCONCLUSIVE" for c in cats)
                else "NO EDGE")
    check("22.f1.family", rec_cat_of(res.get("f1_family")) == want_fam,
          f"got {res.get('f1_family')} vs {want_fam}")

    # F2 — 1 Holm slot (B2 vs outside)
    long = [ev for ev in entries if ev["valid"]]
    b2 = [ev for ev in long if 570 <= ev["min"] < 720]
    out = [ev for ev in long if not (570 <= ev["min"] < 720)]
    rec = res.get("f2", {}).get("F2", {})
    name = "22.f2.F2"
    check(f"{name}.n_a", close(len(b2), rec.get("n_a")),
          f"got {len(b2)} vs {rec.get('n_a')}")
    check(f"{name}.n_b", close(len(out), rec.get("n_b")),
          f"got {len(out)} vs {rec.get('n_b')}")
    floor_ok = len(b2) >= MIN_SLOT and len(out) >= MIN_SLOT
    check(f"{name}.floor_met", floor_ok == rec.get("floor_met"),
          f"got {floor_ok} vs {rec.get('floor_met')}")
    if floor_ok:
        ra = rets_for(b2)
        rb = rets_for(out)
        check(f"{name}.mean_a", close(ra.mean(), rec.get("mean_a")),
              f"got {ra.mean():.6f} vs {rec.get('mean_a')}")
        check(f"{name}.mean_b", close(rb.mean(), rec.get("mean_b")),
              f"got {rb.mean():.6f} vs {rec.get('mean_b')}")
        check_mc(name, rec, lambda rng: boot_two(ra, rb, rng, np.mean),
                 min(len(b2), len(out)), verdict=False,
                 ci_low_key="ci_low", ci_upper_key="ci_upper")
        gate = ALPHA
        rej = rec.get("p", 1.0) <= gate
        check(f"{name}.holm_gate", close(rec.get("holm_gate"), gate),
              f"got {rec.get('holm_gate')} vs {gate}")
        check(f"{name}.holm_rejected", bool(rec.get("holm_rejected")) == rej,
              f"got {rec.get('holm_rejected')} vs {rej}")
        if not rej:
            cat = "NO EDGE"
        else:
            r1 = np.random.default_rng(FRESH[1])
            d1 = boot_two(ra, rb, r1, np.mean)
            cat = "EDGE" if d1[2] > 0 else "FADE" if d1[3] < 0 else "NO EDGE"
        check(f"{name}.verdict", cat == rec_cat_of(rec.get("verdict", "")),
              f"fresh {cat} vs recorded {rec.get('verdict')}")
        # secondary baseline excesses
        positions = {r2_: {ev["e_pos"] for ev in entries
                           if ev["rel"] == r2_} for r2_ in _FILES}
        same, uni = build_pools(positions)
        sb_same = sample_baseline(b2, same, uni, "same")
        sb_uni = sample_baseline(b2, same, uni, "uni")
        e_same = rec.get("excess_same", {})
        if "est" in e_same:
            check_mc(f"{name}.excess_same", e_same,
                     lambda rng: boot_excess(ra, sb_same, rng), len(b2))
        e_uni = rec.get("excess_uni", {})
        if "est" in e_uni:
            check_mc(f"{name}.excess_uni", e_uni,
                     lambda rng: boot_excess(ra, sb_uni, rng), len(b2))
    else:
        check("22.f2.F2.p", close(rec.get("p", 1.0), 1.0),
              f"got {rec.get('p')} vs 1.0")
        check("22.f2.F2.verdict",
              rec_cat_of(rec.get("verdict", "")) == "INCONCLUSIVE",
              f"got {rec.get('verdict')}")
    check("22.f2.family",
          rec_cat_of(res.get("f2_family")) == rec_cat_of(
              res.get("f2", {}).get("F2", {}).get("verdict", "NO EDGE")),
          f"got {res.get('f2_family')}")

    # F3 — 1 Holm slot (pre-market cleanliness)
    pre = window_stats(*PRE)
    rth = window_stats(*RTH)
    rec = res.get("f3", {}).get("F3", {})
    name = "22.f3.F3"
    check(f"{name}.n_pre", close(pre["n_bars"], rec.get("n_pre")),
          f"got {pre['n_bars']} vs {rec.get('n_pre')}")
    check(f"{name}.n_rth", close(rth["n_bars"], rec.get("n_rth")),
          f"got {rth['n_bars']} vs {rec.get('n_rth')}")
    floor_ok = pre["n_bars"] >= MIN_SLOT and rth["n_bars"] >= MIN_SLOT
    check(f"{name}.floor_met", floor_ok == rec.get("floor_met"),
          f"got {floor_ok} vs {rec.get('floor_met')}")
    if floor_ok:
        v_rec = rec.get("vol", {})
        t_rec = rec.get("tail", {})
        check(f"{name}.vol.mean_pre",
              close(pre["abs_r"].mean(), v_rec.get("mean_pre")),
              f"got {pre['abs_r'].mean():.6f} vs {v_rec.get('mean_pre')}")
        check(f"{name}.vol.mean_rth",
              close(rth["abs_r"].mean(), v_rec.get("mean_rth")),
              f"got {rth['abs_r'].mean():.6f} vs {v_rec.get('mean_rth')}")
        check(f"{name}.tail.frac_pre",
              close(pre["tails"].mean(), t_rec.get("frac_pre")),
              f"got {pre['tails'].mean():.6f} vs {t_rec.get('frac_pre')}")
        check(f"{name}.tail.frac_rth",
              close(rth["tails"].mean(), t_rec.get("frac_rth")),
              f"got {rth['tails'].mean():.6f} vs {t_rec.get('frac_rth')}")
        check_mc(f"{name}.vol", v_rec,
                 lambda rng: boot_two(pre["abs_r"], rth["abs_r"], rng,
                                      np.mean),
                 min(pre["n_bars"], rth["n_bars"]))
        check_mc(f"{name}.tail", t_rec,
                 lambda rng: boot_two(pre["tails"], rth["tails"], rng,
                                      np.mean),
                 min(pre["n_bars"], rth["n_bars"]))
        p_want = max(v_rec.get("p", 0.0), t_rec.get("p", 0.0))
        check(f"{name}.p", close(p_want, rec.get("p")),
              f"got {p_want} vs {rec.get('p')}")
        gate = ALPHA
        rej = rec.get("p", 1.0) <= gate
        check(f"{name}.holm_gate", close(rec.get("holm_gate"), gate),
              f"got {rec.get('holm_gate')} vs {gate}")
        check(f"{name}.holm_rejected", bool(rec.get("holm_rejected")) == rej,
              f"got {rec.get('holm_rejected')} vs {rej}")
        if not rej:
            cat = "NO EDGE"
        else:
            r1 = np.random.default_rng(FRESH[1])
            v1 = boot_two(pre["abs_r"], rth["abs_r"], r1, np.mean)
            t1 = boot_two(pre["tails"], rth["tails"], r1, np.mean)
            cat = "EDGE" if (v1[3] < 0 and t1[3] < 0) \
                else "FADE" if (v1[2] > 0 and t1[2] > 0) else "NO EDGE"
        check(f"{name}.verdict", cat == rec_cat_of(rec.get("verdict", "")),
              f"fresh {cat} vs recorded {rec.get('verdict')}")
    else:
        check("22.f3.F3.p", close(rec.get("p", 1.0), 1.0),
              f"got {rec.get('p')} vs 1.0")
        check("22.f3.F3.verdict",
              rec_cat_of(rec.get("verdict", "")) == "INCONCLUSIVE",
              f"got {rec.get('verdict')}")
    check("22.f3.family",
          rec_cat_of(res.get("f3_family")) == rec_cat_of(
              res.get("f3", {}).get("F3", {}).get("verdict", "NO EDGE")),
          f"got {res.get('f3_family')}")


# ===========================================================================
# Entry point
# ===========================================================================
CAMPAIGNS = {
    "b01": verify_15, "entry": verify_19, "exit": verify_20,
    "veto": verify_21, "regime": verify_22,
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--campaign", default="all",
                    choices=["b01", "entry", "exit", "veto", "regime", "all"])
    ap.add_argument("--results", default=None,
                    help="results JSON path (default data/cache/<campaign file>)")
    args = ap.parse_args()

    if not MANIFEST.exists() or not RAW.exists():
        print("FATAL: archive missing", file=sys.stderr)
        return 3
    load_files()  # populate _FILES (window bar-dates) for the verifiers

    campaigns = (["b01", "entry", "exit", "veto", "regime"]
                 if args.campaign == "all" else [args.campaign])

    for camp in campaigns:
        print(f"\n== {camp.upper()} ==")
        path = (Path(args.results) if args.results
                else CACHE / RES_FILES[camp])
        if not path.exists():
            print(f"  SKIP  results not found: {path}")
            continue
        res = json.loads(path.read_text(encoding="utf-8"))

        # Frozen-sha integrity: the recorded tool sha must equal the
        # documented freeze value.
        rec_sha = res.get("frozen_sha")
        check(f"{camp}.frozen_sha",
              rec_sha == FROZEN[camp],
              f"got {rec_sha} vs {FROZEN[camp]}")
        # Frozen-input assertions (recorded vs documented).
        if camp in ("exit",):
            check(f"{camp}.input_measure_intraday_sha256",
                  res.get("input_measure_intraday_sha256") == INPUT_B01_SHA,
                  f"got {res.get('input_measure_intraday_sha256')} "
                  f"vs {INPUT_B01_SHA}")
        if camp in ("veto", "regime"):
            check(f"{camp}.input_entry_sha256",
                  res.get("input_entry_sha256") == INPUT_ENTRY_SHA,
                  f"got {res.get('input_entry_sha256')} vs {INPUT_ENTRY_SHA}")
            check(f"{camp}.input_b01_sha256",
                  res.get("input_b01_sha256") == INPUT_B01_SHA,
                  f"got {res.get('input_b01_sha256')} vs {INPUT_B01_SHA}")

        CAMPAIGNS[camp](res)

    print(f"\nVERIFICATION: {PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
