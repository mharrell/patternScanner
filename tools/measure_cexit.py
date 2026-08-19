"""Measurement tool for pre-registration #17 — C-exit comparison: indicator
exits vs fixed-2R on the same entries (ledger rows C-01/C-03/C-04;
priority-list item 9).

Frozen 2026-08-19 (pre-registration #17 §1–§7). This tool implements the
frozen contract verbatim; the frozen inputs (tools/detectors.py,
data/cache/detections_v1.csv) are sha-asserted AT IMPORT and never
modified. FROZEN_SHA below is the fixed point of this file's own hash with
its FROZEN_SHA hex blanked; self_check() aborts on any mismatch.

The claims (ultimate-guide): C-01 exit indicators — (1) high-volume red
candle, (4) break of VWAP going down, (5) break of the 9 EMA going down
((2) MACD needs 1-minute data — out of scope; (3) topping tail has no
stated definition — excluded from primary, added as S-DOJI); C-03
two-steps-down ("two candles that go lower and lower"); C-04 "cap my
losers, not my winners" — losers at the −1R max-loss point, winners run to
an exit indicator. Measured as a same-entry system contrast: the
INDICATOR arm (stop −1R, no target, exit on the first of S1–S4) vs the
FIXED-2R arm (target +2R, stop −1R, the corpus's own 2:1 standard) on the
frozen pre-reg #2 A/B/C detections (OOS 2016–2025 by signal date), in
R-units with the house 0.15% round trip as COST_R = 0.0015·E/R.

Families (pre-reg #17 §4):
  F1 system contrast — slots A/B/C/pooled; est = mean(ind R) − mean(fix R)
  F2 per-signal exit timing — slots s1..s4 (the signal is the BINDING
     exit); post-exit 10-bar % return from the exit close vs a same-ticker
     baseline (10 random bars per event, rng2 = SEED+1, binding-exit bars
     excluded); est = mean(baseline) − mean(post-exit)
  F3 C-04 upper tail — slots q90/q95/q99; quantile(ind R) − quantile(fix R)
Date-paired bootstrap B = 1000, seed 20260819, Holm at α = 0.05 within
each family. Count floor 100 events / 20 distinct dates per slot.

Usage:
  python -X utf8 tools/measure_cexit.py            # primary
  python -X utf8 tools/measure_cexit.py --gate     # §5 gate (904-union)
"""
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

import detectors

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
BARS_DIR = CACHE / "bars"

DETECTIONS_CSV = CACHE / "detections_v1.csv"
DETECTIONS_SHA = "9b44f66160130c3a51c9f6de7252536239be63dbdf1a9c1698ec6a1e47b6efa8"
DETECTOR_SHA = "e93ddf7a6c68666a420998d2c96d3eb010b4b4552f6798b9528c3a3523077722"
UNIVERSE_HIST_CSV = CACHE / "universe_sp600_hist_2026-08-15.csv"
RESULTS = CACHE / "cexit_measure_results.json"
REPORT = CACHE / "cexit_measure_report.md"
RESULTS_GATE = CACHE / "cexit_gate_measure_results.json"
REPORT_GATE = CACHE / "cexit_gate_measure_report.md"

# ---- frozen-file assertions AT IMPORT (pre-reg #17 §2 integrity) ----
_got = hashlib.sha256(Path(detectors.__file__).read_bytes()).hexdigest()
assert _got == DETECTOR_SHA, (f"{detectors.__file__} changed (sha "
                              f"{_got[:16]}..., want {DETECTOR_SHA[:16]}...) "
                              "— frozen inputs must not move")
_got = hashlib.sha256(DETECTIONS_CSV.read_bytes()).hexdigest()
assert _got == DETECTIONS_SHA, (f"{DETECTIONS_CSV} changed (sha "
                                f"{_got[:16]}..., want {DETECTIONS_SHA[:16]}...) "
                                "— frozen inputs must not move")
print("frozen shas OK (detectors.py e93ddf7a…, detections_v1.csv "
      "9b44f661…)")

# ---- freeze (house convention: fixed point of this file's own hash) ----
FROZEN_SHA = "afcc0222fcd4b753839e6f3338ee16f1a4e79362f6b280664904b9ab30d8e406"
_FROZEN_RE = re.compile(rb'(FROZEN_SHA = "[0-9a-f]{64}")')


def hash_self() -> str:
    """sha256 of this file with the FROZEN_SHA hex blanked (fixed point)."""
    b = Path(__file__).read_bytes()
    b2, n = _FROZEN_RE.subn(b'FROZEN_SHA = "' + b"0" * 64 + b'"', b)
    if n != 1:
        raise RuntimeError(f"expected exactly one FROZEN_SHA hex line "
                           f"(got {n})")
    return hashlib.sha256(b2).hexdigest()


def self_check() -> None:
    if FROZEN_SHA == "0" * 64:
        print("FATAL: FROZEN_SHA is blank — tool not frozen. Refusing to "
              "run.", file=sys.stderr)
        sys.exit(3)
    actual = hash_self()
    if actual != FROZEN_SHA:
        print(f"FATAL: freeze mismatch — recorded {FROZEN_SHA[:12]}…, "
              f"on disk {actual[:12]}…. A frozen tool must not change.",
              file=sys.stderr)
        sys.exit(1)


self_check()

# ---- frozen parameters (pre-reg #17 §3–§7) ----
K_SETUP = 10              # Shape A setup closes (detector A: K)
P_PULL = 3                # Shape B pullback bars (detector B: P)
VOL_LOOKBACK = 20         # S1 volume mean lookback
VOL_MULT = 1.5            # S1 threshold (S-VOL2: 2.0)
EMA_SPAN = 9              # S3 9-day EMA
TARGET_R = 2.0            # fixed arm target (the corpus 2:1 standard)
STOP_R = 1.0              # both arms: the −1R max-loss point
MAXHOLD = 20              # max-hold bars, primary (S-N10/S-N60)
COST = 0.0015             # house round trip
F2_N = 10                 # F2 post-exit horizon
B = 1000
SEED = 20260819           # pre-reg #17 §4 (freeze date)
ALPHA = 0.05
FLOOR_N = 100             # per-slot count floor
FLOOR_DATES = 20          # per-slot distinct-date floor
Q_TAILS = [0.90, 0.95, 0.99]
ERA_START = "2016-01-01"  # OOS window (pre-reg #2 convention)
ERA_END = "2025-12-31"
SENS_N = [10, 60]         # S-N10 / S-N60
SENS_TARGETS = [1.5, 3.0]  # S-1R5 / S-3R
SENS_COSTS = [0.0005, 0.0030]  # S-C05 / S-C30
SENS_VOL = [2.0]          # S-VOL2
DOJI = {"body": 0.1, "upper": 0.6, "prox": 0.25}  # S-DOJI
SIGNALS = ["s1", "s2", "s3", "s4"]
SLOTS_F1 = ["A", "B", "C", "pooled"]

VERDICT_UP = "EDGE (Holm-rejected; CI-low > 0 — claim holds)"
VERDICT_DOWN = "FADE (Holm-rejected; CI-upper < 0 — claim contradicts)"

CFG_BASE = dict(target_r=TARGET_R, maxhold=MAXHOLD, cost=COST,
                vol_mult=VOL_MULT, vwap_mode="anchor", doji=False,
                opx=False, close_fills=False)


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def fmt_num(v, spec="+.4f") -> str:
    return "—" if v is None else format(v, spec)


# ----------------------------------------------------------------------
# data loading
# ----------------------------------------------------------------------

def load_detections() -> list[dict]:
    """The frozen pre-reg #2 detection set (OOS window applied downstream)."""
    df = pd.read_csv(DETECTIONS_CSV)
    out = []
    for _, r in df.iterrows():
        out.append({
            "ticker": r["ticker"], "shape": r["shape"],
            "signal_date": str(r["signal_date"]),
            "ts": pd.Timestamp(r["signal_date"]),
            "entry": float(r["entry_open"]),
            "detail": json.loads(r["detail"]),
            "year": str(r["signal_date"])[:4],
        })
    return out


def gate_detections() -> list[dict]:
    """§5 gate: the frozen detector re-run on the historical-constituent
    union names (pre-reg #17 §6), same frozen detector."""
    uni = pd.read_csv(UNIVERSE_HIST_CSV)
    tickers = sorted(uni["ticker"].tolist())
    out = []
    for t in tickers:
        p = BARS_DIR / f"{t}.parquet"
        if not p.exists():
            continue
        for r in detectors.detect_ticker(t, p):
            out.append({
                "ticker": r["ticker"], "shape": r["shape"],
                "signal_date": str(r["signal_date"]),
                "ts": pd.Timestamp(r["signal_date"]),
                "entry": float(r["entry_open"]),
                "detail": json.loads(r["detail"]),
                "year": str(r["signal_date"])[:4],
            })
    out.sort(key=lambda r: (r["ticker"], r["signal_date"], r["shape"]))
    return out


def load_bars(tickers: list[str]) -> dict:
    """Per-ticker arrays + precomputed S3 EMA-9 and S-VWAP5 series."""
    bars = {}
    for t in sorted(set(tickers)):
        p = BARS_DIR / f"{t}.parquet"
        if not p.exists():
            continue
        df = pd.read_parquet(p)
        n = len(df)
        if n < MAXHOLD + F2_N + 2:
            continue
        d = {
            "dates": df.index,
            "o": df["Open"].to_numpy(dtype=np.float64),
            "h": df["High"].to_numpy(dtype=np.float64),
            "l": df["Low"].to_numpy(dtype=np.float64),
            "c": df["Close"].to_numpy(dtype=np.float64),
            "v": df["Volume"].to_numpy(dtype=np.float64),
        }
        d["ema9"] = pd.Series(d["c"], index=d["dates"]).ewm(
            span=EMA_SPAN, adjust=False).mean().to_numpy(dtype=np.float64)
        tp = (d["h"] + d["l"] + d["c"]) / 3.0
        vp = pd.Series(tp * d["v"], index=d["dates"])
        vv = pd.Series(d["v"], index=d["dates"])
        d["vw5"] = (vp.rolling(5).sum() / vv.rolling(5).sum()
                    ).to_numpy(dtype=np.float64)
        bars[t] = d
    return bars


def stop_for(shape: str, detail: dict, lo: np.ndarray, i: int) -> float:
    """The pattern's structural low (pre-reg #17 §3), computed from bars."""
    if shape == "A":
        j = i - K_SETUP
        if j < 0:
            return float("nan")
        return float(lo[j:i].min())
    if shape == "B":
        j = i - P_PULL
        if j < 0:
            return float("nan")
        return float(lo[j:i].min())
    return float(min(detail["l1"], detail["l2"]))


# ----------------------------------------------------------------------
# trade simulation (pre-reg #17 §3) — both arms, identical entries
# ----------------------------------------------------------------------

def simulate_event(bs: dict, i: int, E: float, S: float, R: float,
                   cfg: dict) -> dict:
    """Simulate one event for both arms. Per arm returns
    {trigger (bar index), reason, fill}. Same-bar stop+target / stop+signal
    -> the stop (conservative, pre-registered)."""
    n = len(bs["c"])
    o, h, l, c, v = bs["o"], bs["h"], bs["l"], bs["c"], bs["v"]
    ema9, vw5 = bs["ema9"], bs["vw5"]
    maxhold = cfg["maxhold"]
    tgt = E + cfg["target_r"] * R
    res = {}
    for arm in ("fix", "ind"):
        trigger, reason = None, None
        vw, vwv = 0.0, 0.0
        run_max = E
        for t in range(i + 1, i + maxhold + 1):
            if t >= n:
                break                    # unreachable under the validity rule
            if l[t] <= S:
                trigger, reason = t, "stop"
                break
            if arm == "fix":
                if h[t] >= tgt:
                    trigger, reason = t, "target"
                    break
            else:
                run_max = max(run_max, h[t])
                lo20 = t - VOL_LOOKBACK
                vm = float(v[max(0, lo20):t].mean()) if t > 0 else 0.0
                s1 = (c[t] < o[t] and vm > 0.0
                      and v[t] >= cfg["vol_mult"] * vm)
                if cfg["vwap_mode"] == "anchor":
                    vw += (h[t] + l[t] + c[t]) / 3.0 * v[t]
                    vwv += v[t]
                    s2 = (c[t] < vw / vwv) if vwv > 0.0 else False
                else:
                    s2 = c[t] < vw5[t]
                s3 = c[t] < ema9[t]
                s4 = (t >= i + 2 and c[t] < o[t] and c[t - 1] < o[t - 1]
                      and l[t] < l[t - 1] and l[t - 1] < l[t - 2])
                sd = False
                if cfg["doji"] and t >= i + 2:
                    rng_t = h[t] - l[t]
                    u = h[t] - max(o[t], c[t])
                    sd = (rng_t > 0.0
                          and abs(o[t] - c[t]) <= DOJI["body"] * rng_t
                          and u >= DOJI["upper"] * rng_t
                          and h[t] >= run_max - DOJI["prox"] * R)
                for name, hit in (("s1", s1), ("s2", s2), ("s3", s3),
                                  ("s4", s4), ("doji", sd)):
                    if hit:
                        trigger, reason = t, name
                        break
                if trigger is not None:
                    break
        if trigger is None:
            trigger = i + maxhold
            reason = "maxhold"
        if cfg["opx"]:
            fill = o[trigger + 1]
        elif reason in ("stop", "target"):
            fill = c[trigger] if cfg["close_fills"] else (
                S if reason == "stop" else tgt)
        else:
            fill = c[trigger]
        res[arm] = {"trigger": int(trigger), "reason": reason,
                    "fill": float(fill), "i": i}
    return res


def r_return(fill: float, E: float, R: float, cost: float) -> float:
    """Outcome in R units, house 0.15% round trip as COST_R."""
    return (fill - E) / R - cost * E / R


def r_return_pct(fill: float, E: float, cost: float) -> float:
    """Outcome in flat % units (S-PCT)."""
    return (fill - E) / E - cost


# ----------------------------------------------------------------------
# event build (validity, stops, both arms) — pre-reg #17 §3
# ----------------------------------------------------------------------

def build_events(evs: list[dict], bars: dict, cfg: dict) -> dict:
    """Simulate all events; return records + drop counts.
    records: {ticker, shape, ts, year, E, S, R,
              ind: {trigger, reason, fill, r, i}, fix: {…}}"""
    recs = []
    drops = {"no_bars": 0, "r_le_0": 0, "end": 0}
    for r in sorted(evs, key=lambda r: (r["ticker"], r["signal_date"])):
        bs = bars.get(r["ticker"])
        if bs is None:
            drops["no_bars"] += 1
            continue
        i = bs["dates"].get_loc(r["ts"]) if r["ts"] in bs["dates"] else -1
        if i < 0:
            drops["no_bars"] += 1
            continue
        n = len(bs["c"])
        if i + cfg["maxhold"] + (1 if cfg["opx"] else 0) >= n:
            drops["end"] += 1
            continue
        S = stop_for(r["shape"], r["detail"], bs["l"], i)
        if not np.isfinite(S):
            drops["r_le_0"] += 1
            continue
        E = r["entry"]
        R = E - S
        if R <= 0.0:
            drops["r_le_0"] += 1
            continue
        sim = simulate_event(bs, i, E, S, R, cfg)
        recs.append({
            "ticker": r["ticker"], "shape": r["shape"], "ts": r["ts"],
            "year": r["year"], "E": E, "S": S, "R": R,
            "ind": {**sim["ind"],
                    "r": r_return(sim["ind"]["fill"], E, R, cfg["cost"])},
            "fix": {**sim["fix"],
                    "r": r_return(sim["fix"]["fill"], E, R, cfg["cost"])},
        })
    return {"records": recs, "drops": drops}


# ----------------------------------------------------------------------
# bootstrap machinery (date-paired, house convention)
# ----------------------------------------------------------------------

def paired_contrast(vals_a: np.ndarray, vals_b: np.ndarray,
                    dates: np.ndarray, rng) -> list:
    """Date-paired bootstrap: est = mean(A) − mean(B) (the deterministic
    full-sample pooled difference, pre-reg #17 §4); CI and p from the B
    draws that resample the distinct dates jointly. Returns
    [est, median, ci_low, ci_high, p_two_sided]."""
    un = np.unique(dates)
    n_dates = len(un)
    di = {d: k for k, d in enumerate(un)}
    didx = np.array([di[d] for d in dates], dtype=np.int64)
    cnt = np.zeros(n_dates, dtype=np.int64)
    sa = np.zeros(n_dates)
    sb = np.zeros(n_dates)
    np.add.at(cnt, didx, 1)
    np.add.at(sa, didx, vals_a)
    np.add.at(sb, didx, vals_b)
    draws = rng.integers(0, n_dates, size=(B, n_dates))
    ca = cnt[draws].sum(axis=1)
    ma = sa[draws].sum(axis=1) / ca
    mb = sb[draws].sum(axis=1) / ca
    diffs = ma - mb
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min(float((diffs <= 0.0).mean()), float((diffs >= 0.0).mean()))
    est = float(np.mean(vals_a) - np.mean(vals_b))
    return [est, float(np.median(diffs)), float(lo), float(hi), float(p)]


def quantile_contrast(arr_a: np.ndarray, arr_b: np.ndarray,
                      dates: np.ndarray, q: float, rng) -> list:
    """Date-paired bootstrap of quantile_q(A) − quantile_q(B); est = the
    deterministic plain quantile difference (pre-reg #17 §4)."""
    order = np.argsort(dates, kind="stable")
    aa, ab, ds = arr_a[order], arr_b[order], dates[order]
    un = np.unique(ds)
    n_dates = len(un)
    di = {d: k for k, d in enumerate(un)}
    didx = np.array([di[d] for d in ds], dtype=np.int64)
    cnt = np.zeros(n_dates, dtype=np.int64)
    np.add.at(cnt, didx, 1)
    off = np.cumsum(cnt) - cnt
    diffs = np.empty(B)
    for b in range(B):
        dsel = rng.integers(0, n_dates, size=n_dates)
        idx = np.concatenate(
            [np.arange(off[d], off[d] + cnt[d]) for d in dsel])
        diffs[b] = np.quantile(aa[idx], q) - np.quantile(ab[idx], q)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min(float((diffs <= 0.0).mean()), float((diffs >= 0.0).mean()))
    est = float(np.quantile(arr_a, q) - np.quantile(arr_b, q))
    return [est, float(np.median(diffs)), float(lo), float(hi), float(p)]


def holm_rejected(p_list: list[float], alpha: float) -> list[bool]:
    """Holm-Bonferroni within a family: p_list in slot order."""
    k = len(p_list)
    order = np.argsort(p_list)
    gates = {}
    for rank, slot in enumerate(order):
        gates[int(slot)] = alpha / (k - rank)
    return [bool(p_list[i] <= gates[i]) for i in range(k)]


# ----------------------------------------------------------------------
# verdicts (pre-reg #17 §4–§5)
# ----------------------------------------------------------------------

def floor_ok(n: int, n_dates: int) -> bool:
    return n >= FLOOR_N and n_dates >= FLOOR_DATES


def verdict_slot(s: dict, up: str, down: str) -> str:
    if not floor_ok(s["n"], s["n_dates"]):
        return (f"INCONCLUSIVE (count floor {FLOOR_N}/{FLOOR_DATES} unmet: "
                f"n={s['n']}, dates={s['n_dates']})")
    if s.get("holm_rejected") and s["ci_low"] is not None \
            and s["ci_low"] > 0.0:
        return up
    if s.get("holm_rejected") and s["ci_high"] is not None \
            and s["ci_high"] < 0.0:
        return down
    return (f"NO EDGE (p {s['p']:.3f}; est {fmt_num(s['est'])}; CI "
            f"{fmt_num(s['ci_low'])}..{fmt_num(s['ci_high'])})")


# ----------------------------------------------------------------------
# family computations (pre-reg #17 §4)
# ----------------------------------------------------------------------

def family_f1(build: dict, rng) -> dict:
    """F1 system contrast: est = mean(ind R) − mean(fix R), per slot."""
    recs = build["records"]
    out = {}
    p_list = []
    for name in SLOTS_F1:
        ev = recs if name == "pooled" else \
            [r for r in recs if r["shape"] == name]
        ia = np.array([r["ind"]["r"] for r in ev], dtype=np.float64)
        fa = np.array([r["fix"]["r"] for r in ev], dtype=np.float64)
        ds = np.array([r["ts"] for r in ev])
        s = {"n": int(len(ev)),
             "n_dates": int(len(np.unique(ds))) if len(ev) else 0,
             "mean_ind": float(ia.mean()) if len(ev) else None,
             "mean_fix": float(fa.mean()) if len(ev) else None,
             "est": None, "ci_low": None, "ci_high": None, "p": 1.0}
        if len(ev) >= 2 and len(np.unique(ds)) >= 2:
            c = paired_contrast(ia, fa, ds, rng)
            s.update(est=c[0], ci_low=c[2], ci_high=c[3], p=c[4])
        out[name] = s
        p_list.append(s["p"])
    rej = holm_rejected(p_list, ALPHA)
    for k, name in enumerate(SLOTS_F1):
        out[name]["holm_rejected"] = rej[k]
        out[name]["verdict"] = verdict_slot(out[name], VERDICT_UP,
                                            VERDICT_DOWN)
    return out


def family_f2(build: dict, bars: dict, rng2) -> dict:
    """F2 per-signal exit timing: est = mean(baseline) − mean(post-exit)
    over 10-bar forward returns. Baseline: 10 seeded random bars per
    binding event, same ticker, OOS-era, binding-exit bars excluded."""
    recs = build["records"]
    era_lo, era_hi = pd.Timestamp(ERA_START), pd.Timestamp(ERA_END)
    out = {}
    p_list = []
    for sig in SIGNALS:
        ev = [r for r in recs if r["ind"]["reason"] == sig]
        # post-exit forward returns (validity: trigger + F2_N < n)
        posts, post_dates = [], []
        drops_end = 0
        for r in ev:
            t = r["ind"]["trigger"]
            bs = bars[r["ticker"]]
            if t + F2_N >= len(bs["c"]):
                drops_end += 1
                continue
            posts.append((bs["c"][t + F2_N] - bs["c"][t]) / bs["c"][t])
            post_dates.append(r["ts"])
        # baseline pool per ticker (same-ticker bars, OOS era, exit bars out)
        pool = {}
        for t in sorted({r["ticker"] for r in ev}):
            bs = bars.get(t)
            if bs is None:
                continue
            n = len(bs["c"])
            mask = ((bs["dates"] >= era_lo) & (bs["dates"] <= era_hi)
                    & (np.arange(n) + F2_N < n))
            idx = np.flatnonzero(mask)
            excl = {int(r["ind"]["trigger"]) for r in ev if r["ticker"] == t}
            idx = np.array([j for j in idx if j not in excl],
                           dtype=np.int64)
            if idx.size:
                fwd = (bs["c"][idx + F2_N] - bs["c"][idx]) / bs["c"][idx]
                pool[t] = (idx, fwd, bs["dates"][idx])
        # 10 seeded draws per event from its ticker's pool
        b_vals, b_dates = [], []
        for r in ev:
            if r["ticker"] not in pool:
                continue
            idx, fwd, dts = pool[r["ticker"]]
            sel = rng2.integers(0, len(idx), size=10)
            b_vals.extend(fwd[sel].tolist())
            b_dates.extend(pd.Timestamp(x) for x in dts[sel].tolist())
        na = np.array(posts, dtype=np.float64)
        ba = np.array(b_vals, dtype=np.float64)
        rec = {"signal": sig, "n": int(len(ev)),
               "n_dates": int(len(np.unique(post_dates))) if posts else 0,
               "drops_end": int(drops_end),
               "n_baseline": int(len(b_vals)),
               "mean_post_exit": float(na.mean()) if len(na) else None,
               "mean_baseline": float(ba.mean()) if len(ba) else None,
               "est": None, "ci_low": None, "ci_high": None, "p": 1.0}
        if len(na) >= 2 and len(ba) >= 1 \
                and len(np.unique(post_dates)) >= 2:
            ad = np.array(post_dates)
            bd = np.array(b_dates)
            all_dates = np.concatenate([ad, bd])
            un = np.unique(all_dates)
            n_dates = len(un)
            di = {d: k for k, d in enumerate(un)}
            didx_p = np.array([di[d] for d in ad], dtype=np.int64)
            didx_b = np.array([di[d] for d in bd], dtype=np.int64)
            cp = np.zeros(n_dates, dtype=np.int64)
            cb = np.zeros(n_dates, dtype=np.int64)
            sp = np.zeros(n_dates)
            sb = np.zeros(n_dates)
            np.add.at(cp, didx_p, 1)
            np.add.at(sp, didx_p, na)
            np.add.at(cb, didx_b, 1)
            np.add.at(sb, didx_b, ba)
            draws = rng2.integers(0, n_dates, size=(B, n_dates))
            mp = sp[draws].sum(axis=1) / cp[draws].sum(axis=1)
            mb = sb[draws].sum(axis=1) / cb[draws].sum(axis=1)
            diffs = mb - mp
            lo, hi = np.percentile(diffs, [2.5, 97.5])
            p = 2.0 * min(float((diffs <= 0.0).mean()),
                          float((diffs >= 0.0).mean()))
            # est = mean(baseline) − mean(post-exit) on the drawn pools
            # (deterministic given the draw; pre-reg #17 §4)
            rec.update(est=float(ba.mean() - na.mean()), ci_low=float(lo),
                       ci_high=float(hi), p=float(p))
        out[sig] = rec
        p_list.append(rec["p"])
    rej = holm_rejected(p_list, ALPHA)
    for k, sig in enumerate(SIGNALS):
        out[sig]["holm_rejected"] = rej[k]
        out[sig]["verdict"] = verdict_slot(out[sig], VERDICT_UP,
                                           VERDICT_DOWN)
    return out


def family_f3(build: dict, rng) -> dict:
    """F3 C-04 upper tail: quantile(ind R) − quantile(fix R), pooled."""
    recs = build["records"]
    ia = np.array([r["ind"]["r"] for r in recs], dtype=np.float64)
    fa = np.array([r["fix"]["r"] for r in recs], dtype=np.float64)
    ds = np.array([r["ts"] for r in recs])
    out = {}
    p_list = []
    for q in Q_TAILS:
        key = f"q{int(q * 100)}"
        s = {"n": int(len(recs)),
             "n_dates": int(len(np.unique(ds))) if len(recs) else 0,
             "q": float(q),
             "est": None, "ci_low": None, "ci_high": None, "p": 1.0}
        if len(recs) >= 2 and len(np.unique(ds)) >= 2:
            c = quantile_contrast(ia, fa, ds, q, rng)
            s.update(est=c[0], ci_low=c[2], ci_high=c[3], p=c[4])
        out[key] = s
        p_list.append(s["p"])
    rej = holm_rejected(p_list, ALPHA)
    for k, key in enumerate([f"q{int(q * 100)}" for q in Q_TAILS]):
        out[key]["holm_rejected"] = rej[k]
        out[key]["verdict"] = verdict_slot(out[key], VERDICT_UP,
                                           VERDICT_DOWN)
    return out


# ----------------------------------------------------------------------
# measurement rows
# ----------------------------------------------------------------------

def measurement_rows(build: dict) -> dict:
    recs = build["records"]
    m = {}
    for arm in ("ind", "fix"):
        rv = np.array([r[arm]["r"] for r in recs], dtype=np.float64)
        m[f"{arm}_n"] = int(len(rv))
        m[f"{arm}_mean_r"] = float(rv.mean()) if len(rv) else None
        m[f"{arm}_median_r"] = float(np.median(rv)) if len(rv) else None
        m[f"{arm}_frac_pos"] = float((rv > 0.0).mean()) if len(rv) else None
        m[f"{arm}_frac_ge1r"] = (float((rv >= 1.0).mean())
                                 if len(rv) else None)
        m[f"{arm}_frac_ge2r"] = (float((rv >= 2.0).mean())
                                 if len(rv) else None)
        for reason in ("stop", "target", "maxhold") + tuple(SIGNALS):
            sub = [r[arm] for r in recs if r[arm]["reason"] == reason]
            m[f"{arm}_frac_{reason}"] = (float(len(sub) / len(recs))
                                         if recs else None)
            if sub:
                m[f"{arm}_hold_{reason}"] = float(np.mean(
                    [x["trigger"] - x["i"] for x in sub]))
    binds = Counter(r["ind"]["reason"] for r in recs)
    for s in SIGNALS:
        m[f"bind_{s}_frac"] = (float(binds.get(s, 0) / len(recs))
                               if recs else None)
    for shape in SLOTS_F1:
        sub = recs if shape == "pooled" else \
            [r for r in recs if r["shape"] == shape]
        for arm in ("ind", "fix"):
            by = {}
            for r in sub:
                k = (r["ticker"], r["ts"])
                by.setdefault(k, []).append(r[arm]["r"])
            means = [np.mean(v) for v in by.values()]
            m[f"nd_{shape}_{arm}_n"] = len(by)
            m[f"nd_{shape}_{arm}_mean"] = (float(np.mean(means))
                                           if means else None)
    for shape in SLOTS_F1:
        sub = recs if shape == "pooled" else \
            [r for r in recs if r["shape"] == shape]
        Rs = np.array([r["R"] for r in sub], dtype=np.float64)
        Es = np.array([r["E"] for r in sub], dtype=np.float64)
        m[f"geo_{shape}_n"] = int(len(sub))
        m[f"geo_{shape}_mean_R"] = float(Rs.mean()) if len(Rs) else None
        m[f"geo_{shape}_median_R"] = float(np.median(Rs)) if len(Rs) \
            else None
        m[f"geo_{shape}_mean_E"] = float(Es.mean()) if len(Es) else None
    for y in sorted({r["year"] for r in recs}):
        sub = [r for r in recs if r["year"] == y]
        if not sub:
            continue
        m[f"year_{y}_n"] = len(sub)
        m[f"year_{y}_ind"] = float(np.mean([r["ind"]["r"] for r in sub]))
        m[f"year_{y}_fix"] = float(np.mean([r["fix"]["r"] for r in sub]))
    return m


# ----------------------------------------------------------------------
# sensitivities (pre-reg #17 §7) — plain per-slot estimates
# ----------------------------------------------------------------------

def slot_ests(build: dict, kind: str = "r") -> dict:
    out = {}
    for name in SLOTS_F1:
        ev = build["records"] if name == "pooled" else \
            [r for r in build["records"] if r["shape"] == name]
        ds = np.array([r["ts"] for r in ev])
        if kind == "r":
            est = (float(np.mean([r["ind"]["r"] for r in ev]))
                   - float(np.mean([r["fix"]["r"] for r in ev])))
        else:
            est = (float(np.mean([r_return_pct(r["ind"]["fill"], r["E"],
                                               CFG_BASE["cost"])
                                  for r in ev]))
                   - float(np.mean([r_return_pct(r["fix"]["fill"], r["E"],
                                                 CFG_BASE["cost"])
                                    for r in ev])))
        out[name] = {"n": int(len(ev)),
                     "n_dates": int(len(np.unique(ds))) if ev else 0,
                     "est": float(est) if ev else None}
    return out


def sens_suni(build: dict, bars: dict, rng2) -> dict:
    """S-UNI (pre-reg #17 §7): F2's 'random-universe baseline leg' — the
    baseline drawn from the whole event universe (any ticker's OOS-era
    bars, c+10 valid, the signal's binding-exit bars excluded) instead of
    the same ticker. Plain estimates; no verdicts."""
    recs = build["records"]
    era_lo, era_hi = pd.Timestamp(ERA_START), pd.Timestamp(ERA_END)
    pool = {}
    for t in sorted(bars):
        bs = bars[t]
        n = len(bs["c"])
        mask = ((bs["dates"] >= era_lo) & (bs["dates"] <= era_hi)
                & (np.arange(n) + F2_N < n))
        idx = np.flatnonzero(mask)
        if idx.size:
            fwd = (bs["c"][idx + F2_N] - bs["c"][idx]) / bs["c"][idx]
            pool[t] = (idx, fwd, bs["dates"][idx])
    out = {}
    for sig in SIGNALS:
        ev = [r for r in recs if r["ind"]["reason"] == sig]
        posts, post_dates = [], []
        for r in ev:
            t = r["ind"]["trigger"]
            bs = bars[r["ticker"]]
            if t + F2_N >= len(bs["c"]):
                continue
            posts.append((bs["c"][t + F2_N] - bs["c"][t]) / bs["c"][t])
            post_dates.append(r["ts"])
        excl_by_t = {}
        for t in sorted({r["ticker"] for r in ev}):
            excl_by_t[t] = {int(x["ind"]["trigger"]) for x in ev
                            if x["ticker"] == t}
        b_vals, b_dates = [], []
        for r in ev:
            t = r["ticker"]
            if t not in pool:
                continue
            idx, fwd, dts = pool[t]
            excl = excl_by_t.get(t, set())
            sel0 = np.array([p for p, j in enumerate(idx)
                             if j not in excl], dtype=np.int64)
            if not sel0.size:
                continue
            sel = rng2.integers(0, len(sel0), size=10)
            b_vals.extend(fwd[sel0[sel]].tolist())
            b_dates.extend(pd.Timestamp(x) for x in dts[sel0[sel]].tolist())
        na = np.array(posts, dtype=np.float64)
        ba = np.array(b_vals, dtype=np.float64)
        out[sig] = {
            "n": int(len(ev)),
            "n_dates": int(len(np.unique(post_dates))) if posts else 0,
            "n_baseline": int(len(b_vals)),
            "mean_post_exit": float(na.mean()) if len(na) else None,
            "mean_baseline": float(ba.mean()) if len(ba) else None,
            "est": (float(ba.mean() - na.mean())
                    if len(na) and len(ba) else None),
        }
    return {"slots": out}


def run_sensitivities(evs: list[dict], evs_all: list[dict], bars: dict,
                      primary_build: dict, rng2) -> dict:
    out = {}

    def add(name, cfg=None, build=None, binds=False, pct=False):
        if build is None:
            build = build_events(evs, bars, cfg)
        d = {"slots": slot_ests(build, "pct" if pct else "r"),
             "drops": dict(build["drops"])}
        if binds:
            d["binds"] = dict(Counter(r["ind"]["reason"]
                                      for r in build["records"]))
        out[name] = d

    for tname, tr in (("S-1R5", 1.5), ("S-3R", 3.0)):
        add(tname, {**CFG_BASE, "target_r": tr}, binds=True)
    for nname, mh in (("S-N10", 10), ("S-N60", 60)):
        add(nname, {**CFG_BASE, "maxhold": mh}, binds=True)
    for cname, cc in (("S-C05", 0.0005), ("S-C30", 0.0030)):
        add(cname, {**CFG_BASE, "cost": cc})
    add("S-OPX", {**CFG_BASE, "opx": True}, binds=True)
    add("S-CLOSE", {**CFG_BASE, "close_fills": True}, binds=True)
    add("S-VOL2", {**CFG_BASE, "vol_mult": 2.0}, binds=True)
    add("S-VWAP5", {**CFG_BASE, "vwap_mode": "roll5"}, binds=True)
    add("S-DOJI", {**CFG_BASE, "doji": True}, binds=True)
    out["S-UNI"] = sens_suni(primary_build, bars, rng2)
    is_evs = [e for e in evs_all if e["ts"] < pd.Timestamp(ERA_START)]
    add("S-IS", build=build_events(is_evs, bars, CFG_BASE), binds=True)
    add("S-PCT", build=primary_build, pct=True)
    return out


# ----------------------------------------------------------------------
# reporting
# ----------------------------------------------------------------------

def fmt_num_report(v) -> str:
    return "—" if v is None else format(v, "+.4f")


def write_outputs(mode: str, results: dict) -> tuple:
    code_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    results["fingerprints"]["measure_code_sha256"] = code_sha
    results_path, report_path = (RESULTS_GATE, REPORT_GATE) if mode == "gate" \
        else (RESULTS, REPORT)
    text = json.dumps(results, indent=2, sort_keys=True) + "\n"
    results_path.write_text(text, encoding="utf-8")
    results_sha = sha(results_path)
    md = build_report(mode, results, results_sha)
    report_path.write_text(md, encoding="utf-8")
    return code_sha, results_sha, sha(report_path)


def build_report(mode: str, results: dict, results_sha: str) -> str:
    L = []
    L.append("# Pre-registration #17 — C-exit comparison: indicator exits "
             "vs fixed-2R on the same entries (C-01/C-03/C-04)")
    L.append("")
    L.append(f"mode: **{results['mode']}** — frozen pre-reg #2 A/B/C "
             "detections, OOS 2016-01-01..2025-12-31 by signal date")
    L.append(f"tool: tools/measure_cexit.py (frozen 2026-08-19, "
             f"FROZEN_SHA {results['fingerprints']['frozen_sha'][:12]}…)")
    L.append("")
    L.append("## Input fingerprints")
    L.append("- detectors.py — e93ddf7a… (frozen; asserted at import)")
    L.append("- detections_v1.csv — 9b44f661… (frozen; asserted at import)")
    L.append(f"- universe_sp600_hist_2026-08-15.csv — "
             f"{results['assertions']['universe_hist_sha256'][:12]}… "
             f"(gate universe)")
    L.append(f"- bars parquets — {results['assertions']['bars_count']}")
    L.append("")
    L.append("## Contract (pre-reg #17 §3–§4)")
    L.append("- entries: frozen A/B/C detections; entry = open of "
             "signal+1")
    L.append("- stops: A min(low i-10..i-1) · B min(low i-3..i-1) · "
             "C min(l1, l2)")
    L.append("- R = E − S; outcome = (fill − E)/R − 0.0015·E/R")
    L.append("- fixed arm: +2R target / −1R stop, trigger fills")
    L.append("- indicator arm: −1R stop, no target; exit = first of "
             "S1 high-volume red / S2 anchored-VWAP break / S3 9-EMA "
             "break / S4 two-steps-down; fills at signal close; "
             "same-bar stop+signal → stop; max-hold e+20")
    L.append("- validity: i+20 < n; R ≤ 0 or out-of-range events dropped "
             "(counted)")
    L.append("- F1 est = mean(ind) − mean(fix); F2 est = "
             "mean(baseline) − mean(post-exit); F3 est = quantile(ind) − "
             "quantile(fix)")
    L.append("- date-paired bootstrap B=1000, seed 20260819; Holm α=0.05 "
             "per family; floors 100 events / 20 dates per slot")
    L.append("")
    L.append("## Drops (events excluded and why)")
    L.append("| reason | n |")
    L.append("| --- | --- |")
    for k, v in sorted(results["drops"].items()):
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("## F1 — system contrast, est = mean(ind R) − mean(fix R) "
             "(Holm 0.05/4)")
    L.append("| slot | n | dates | mean ind | mean fix | est | CI low | "
             "CI high | p | verdict |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | "
             "--- |")
    for k, s in sorted(results["families"]["f1"].items()):
        L.append(f"| {k} | {s['n']} | {s['n_dates']} | "
                 f"{fmt_num_report(s['mean_ind'])} | "
                 f"{fmt_num_report(s['mean_fix'])} | "
                 f"{fmt_num_report(s['est'])} | "
                 f"{fmt_num_report(s['ci_low'])} | "
                 f"{fmt_num_report(s['ci_high'])} | {s['p']:.4f} | "
                 f"{s['verdict']} |")
    L.append("")
    L.append("## F2 — per-signal exit timing, est = mean(baseline) − "
             "mean(post-exit) (Holm 0.05/4)")
    L.append("| signal | n | dates | drops_end | n_baseline | mean post | "
             "mean base | est | CI low | CI high | p | verdict |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | "
             "--- | --- | --- |")
    for k, s in sorted(results["families"]["f2"].items()):
        L.append(f"| {k} | {s['n']} | {s['n_dates']} | {s['drops_end']} | "
                 f"{s['n_baseline']} | "
                 f"{fmt_num_report(s['mean_post_exit'])} | "
                 f"{fmt_num_report(s['mean_baseline'])} | "
                 f"{fmt_num_report(s['est'])} | "
                 f"{fmt_num_report(s['ci_low'])} | "
                 f"{fmt_num_report(s['ci_high'])} | {s['p']:.4f} | "
                 f"{s['verdict']} |")
    L.append("")
    L.append("## F3 — C-04 upper tail, est = quantile(ind R) − "
             "quantile(fix R), pooled (Holm 0.05/3)")
    L.append("| slot | q | n | dates | est | CI low | CI high | p | "
             "verdict |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for k, s in sorted(results["families"]["f3"].items()):
        L.append(f"| {k} | {s['q']:.2f} | {s['n']} | {s['n_dates']} | "
                 f"{fmt_num_report(s['est'])} | "
                 f"{fmt_num_report(s['ci_low'])} | "
                 f"{fmt_num_report(s['ci_high'])} | {s['p']:.4f} | "
                 f"{s['verdict']} |")
    L.append("")
    L.append("## Measurements")
    for k, v in sorted(results["measurements"].items()):
        L.append(f"- {k}: {fmt_num_report(v) if isinstance(v, float) else v}")
    L.append("")
    L.append("## Sensitivities (plain per-slot estimates, pre-reg #17 §7)")
    L.append("| sensitivity | slot | n | dates | est (ind − fix) |")
    L.append("| --- | --- | --- | --- | --- |")
    for name, d in sorted(results["sensitivities"].items()):
        for k, s in sorted(d["slots"].items()):
            L.append(f"| {name} | {k} | {s['n']} | {s['n_dates']} | "
                     f"{fmt_num_report(s['est'])} |")
    L.append("")
    L.append("## Notes")
    L.append("- F2 baseline: 10 seeded random bars per binding event, "
             "same ticker, OOS era, binding-exit bars excluded; post-exit "
             "return measured from the exit close over 10 bars.")
    L.append("- S-DOJI topping tail: h[t] within 0.25R of the run's max "
             "high since entry (entry price as baseline), body ≤ 0.1·range, "
             "upper shadow ≥ 0.6·range; S-DOJI is a sensitivity only.")
    L.append("- S-UNI: F2's random-universe baseline leg — the baseline "
             "drawn from any ticker's bars in the event universe instead "
             "of the same ticker; S-IS uses the in-sample window (before "
             "2016-01-01).")
    L.append("- One-shot rule (pre-reg #17 §5): this file is the first "
             "measurement; verdicts are fixed here and returned to the "
             "ledger before any parameter change becomes a new "
             "hypothesis.")
    L.append("")
    L.append(f"results sha256: {results_sha}")
    return "\n".join(L) + "\n"


def print_summary(results: dict) -> None:
    print("== F1 system contrast (indicator − fixed-2R) ==")
    for k, s in sorted(results["families"]["f1"].items()):
        print(f"  {k}: est {fmt_num_report(s['est'])} CI "
              f"{fmt_num_report(s['ci_low'])}.."
              f"{fmt_num_report(s['ci_high'])} "
              f"p {s['p']:.4f} — {s['verdict']}")
    print("== F2 per-signal exit timing (baseline − post-exit) ==")
    for k, s in sorted(results["families"]["f2"].items()):
        print(f"  {k}: n {s['n']} est {fmt_num_report(s['est'])} CI "
              f"{fmt_num_report(s['ci_low'])}.."
              f"{fmt_num_report(s['ci_high'])} "
              f"p {s['p']:.4f} — {s['verdict']}")
    print("== F3 upper tail (ind − fix) ==")
    for k, s in sorted(results["families"]["f3"].items()):
        print(f"  {k}: est {fmt_num_report(s['est'])} CI "
              f"{fmt_num_report(s['ci_low'])}.."
              f"{fmt_num_report(s['ci_high'])} "
              f"p {s['p']:.4f} — {s['verdict']}")


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------

def main() -> None:
    gate = "--gate" in sys.argv[1:]
    mode = "gate" if gate else "measure"
    era_lo, era_hi = pd.Timestamp(ERA_START), pd.Timestamp(ERA_END)
    if gate:
        evs_all = gate_detections()
    else:
        evs_all = load_detections()
    universe_n = len({e["ticker"] for e in evs_all})
    bars = load_bars([e["ticker"] for e in evs_all])
    evs = [e for e in evs_all if era_lo <= e["ts"] <= era_hi]
    evs_is = [e for e in evs_all if e["ts"] < era_lo]
    rng = np.random.default_rng(SEED)
    rng2 = np.random.default_rng(SEED + 1)
    build = build_events(evs, bars, CFG_BASE)
    f1 = family_f1(build, rng)
    f2 = family_f2(build, bars, rng2)
    f3 = family_f3(build, rng)
    meas = measurement_rows(build)
    sens = run_sensitivities(evs, evs_all, bars, build, rng2)
    results = {
        "pre_reg": "17",
        "mode": mode,
        "title": ("C-exit comparison: indicator exits vs fixed-2R on the "
                  "same entries (C-01/C-03/C-04; priority-list item 9)"),
        "claim": ("C-01 exit indicators + C-03 two-steps-down + C-04 "
                  "cap-losers/run-winners beat the corpus's own fixed-2R "
                  "exits on the same entries"),
        "params": {
            "k_setup": K_SETUP, "p_pull": P_PULL,
            "vol_lookback": VOL_LOOKBACK, "vol_mult": VOL_MULT,
            "ema_span": EMA_SPAN, "target_r": TARGET_R, "stop_r": STOP_R,
            "maxhold": MAXHOLD, "cost": COST, "f2_n": F2_N, "b": B,
            "seed": SEED, "alpha": ALPHA, "floor_n": FLOOR_N,
            "floor_dates": FLOOR_DATES,
            "era": [ERA_START, ERA_END], "q_tails": Q_TAILS,
            "doji": DOJI, "signals": SIGNALS,
        },
        "families": {"f1": f1, "f2": f2, "f3": f3},
        "measurements": meas,
        "sensitivities": sens,
        "drops": build["drops"],
        "assertions": {
            "detector_sha256": DETECTOR_SHA,
            "detections_sha256": DETECTIONS_SHA,
            "universe_hist_sha256": sha(UNIVERSE_HIST_CSV),
            "bars_count": len(bars),
            "universe_names": universe_n,
            "events_oos": len(evs),
            "events_is": len(evs_is),
        },
        "fingerprints": {"frozen_sha": FROZEN_SHA},
    }
    code_sha, results_sha, report_sha = write_outputs(mode, results)
    print_summary(results)
    print(f"events OOS {len(evs)} / IS {len(evs_is)} / universe "
          f"{universe_n} names")
    print(f"code sha256: {code_sha}")
    print(f"results sha256: {results_sha}")
    print(f"report sha256: {report_sha}")


if __name__ == "__main__":
    main()
