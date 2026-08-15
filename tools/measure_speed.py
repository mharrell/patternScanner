"""Speed-asymmetry measurement for pre-registration #12 (ledger row
I-F-02), frozen 2026-08-15.

The claim (Warrior Trading, jfe1Zl-5EQI [28:28-28:47], corroborated at
[17:34-17:37]):
  "The move up that may have taken hours can be all given back in a
  matter of minutes on the good top reversal... the Bulls take the stairs
  and the Bears take the window so the sell offs can be very quick".

Daily translation (pre-reg #12 sec 1): on daily bars each bar is one time
unit, so speed = price distance per bar. Two assertions, both measured:
  A1 (unconditional directional asymmetry): down-bars' mean per-bar move
     size exceeds up-bars' ("stairs" small/slow vs "window" large/fast).
  A2 (reversal speed): the retracement of a big up-move (the frozen
     pre-reg #11 UP events, L=10, tau=3) covers its distance faster than
     the move did ("hours up, minutes down").

Per-bar quantity (F1/F2): r_t = close_t/close_{t-1} - 1 (percent), size =
|r_t|, bar index >= 1 (index-0 bars excluded and counted). Leg by sign of
r_t: UP (r_t > 0), DOWN (r_t < 0); zero-move bars (r_t = 0 exactly)
excluded from the legs and counted. OOS population = bars with date >=
2016-01-01 (no warm-up guard: the measurement uses only the bar itself
and its prior close — no lookback window).

F1 (absolute, per leg vs the typical-bar baseline): each leg's mean |r|
minus the era-matched unconditional mean |r| over all OOS bars (the
calibrated null — "typical bar size"). Joint one-sample bootstrap on the
OOS bar population (resample bars; recompute all/up/down means jointly;
form both excesses). Holm across the two legs.
  UP: EDGE iff Holm-rejected AND CI-upper < 0 (up-bars smaller than
      typical — "stairs", as claimed); FADE iff Holm-rejected AND
      CI-low > 0.
  DOWN: EDGE iff Holm-rejected AND CI-low > 0 (down-bars larger than
      typical — "window", as claimed); FADE iff Holm-rejected AND
      CI-upper < 0.
  Structural note (pre-reg #12 sec 2): the all-bars mean is the weighted
  average of the legs (plus zeros), so the two excesses are mechanically
  opposite-signed; Holm is conservative; the interpretable single number
  is F2.

F2 (the asymmetry contrast): DOWN - UP mean |r|, two-sample bootstrap
(independent resamples). EDGE iff CI-low > 0; FADE iff CI-upper < 0.

F4 (retracement speed on big up-moves — A2): per frozen pre-reg #11 UP
event (warm-up excluded, OOS signal date), j = the first bar in
[t+1, t+N] whose close <= the move's midpoint (close_t + close_{t-L})/2.
Events with i + N >= n (tail-invalid) dropped and counted; events with no
crossing within N excluded and counted (their non-retracement is pre-reg
#11 F2's result). move-rate = (close_t - close_{t-L}) / close_{t-L} / L;
retrace-rate = (close_t - mid) / close_{t-L} / j (fraction of the move's
base per bar). Paired contrast retrace-rate - move-rate, one-sample
bootstrap. EDGE iff CI-low > 0 (retracement outpaces the move — "given
back in a matter of minutes", as claimed); FADE iff CI-upper < 0. Count
floor 100 -> INCONCLUSIVE.
  Equivalence (pre-reg #12 sec 2): retrace-rate > move-rate  <=>  j < L/2
  = 5 bars.

Phase 5: no family measures forward returns — the claim is about bar
geometry (speed/size), not profitability. The Phase-5 trigger (a positive
absolute return edge, brief sec 1) cannot fire from this campaign by
construction.

Protocol (pre-reg #12 sec 3): B = 1000, seed 20260813, alpha 0.05, era
split by bar date (IS 2000-2015 / OOS 2016-2025), Holm-Bonferroni within
each family, count floor 100 events per family population (F4 only; F1/F2
populations are ~1.5M bars). No engine call: the Phase-3 engine's
measure_returns is NOT invoked — no forward returns are measured (pre-reg
#12 sec 3; the engine's COST/N conventions therefore do not apply).

Sensitivities (pre-declared, NO verdicts): S1 median |r| (F1 joint +
F2); S2 candle-sign version (red = close < open, body |close-open|/open,
same F1/F2 structure); S3 per-ticker contrasts + ticker-cluster CI on F2;
S4 IS-era (2000-2015) F1/F2 (descriptive); S5 per-year F1/F2 (OOS); S6
swing-scale A1 (k=2/3/5 fractal swings on Close, strict — ties never form
a swing; same-type pivot runs coalesced to the more extreme; paired
contrast down-swing rate - preceding up-swing rate); S7 F4 variants
(N = 5/20, event population tau = 2/5); S8 tail concentration (the share
of down-bars in the largest-|r| decile vs the overall down-bar share).

Structural checks (pre-reg #12 sec 3): (a) every F1/F2 bar has a finite
nonzero prior close (bad-prior and index-0 bars counted); (b) zero-move
bars counted, never dropped silently; (c) F4 events' signal bars >= 60
(inherited from the frozen detector) and tail-invalid events counted;
(d) crossing j in [1, N].

Generic helpers import from measure_veto (two_sample_excess), the pre-reg
#10 divergence tool (run_holm, fmt_num, sha, swing_idx) and the pre-reg
#11 big-move tool (tr_series, atr_simple, bigmove_det — the frozen
detection reused for F4's population).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import (B, SEED, ALPHA, ERA_OOS, UNIVERSE_CSV, BARS_DIR)
from measure_divergence import run_holm, fmt_num, sha, swing_idx
from measure_veto import two_sample_excess
from measure_bigmove import tr_series, atr_simple, bigmove_det

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
RESULTS = CACHE / "speed_measure_results.json"
REPORT = CACHE / "speed_measure_report.md"

L_PRIMARY = 10                   # pre-reg #11 frozen detection (F4 population)
TAU_PRIMARY = 3.0
ATR_PERIOD_PRIMARY = 14
N_PRIMARY = 10                   # pre-reg #12: F4 crossing window
WARMUP = 60                      # frozen #3 convention (F4 events inherit it)
MISSING_PASS = 100               # count floor
LEGS = ("UP", "DOWN")
SENS_N = (5, 20)                 # pre-reg #12 sec 6 S7 (F4 window)
SENS_TAU = (2.0, 5.0)            # pre-reg #12 sec 6 S7 (event population)
K_SWINGS = (2, 3, 5)             # pre-reg #12 sec 6 S6


def per_ticker_sizes(close_map: dict, open_map: dict, candle: bool):
    """Per-ticker per-bar sizes and leg codes.

    candle=False (primary): r_t = close_t/close_{t-1} - 1; size = |r_t|;
    legs by sign of r_t (0 = UP, 1 = DOWN, 2 = ZERO).
    candle=True (S2): body size = |close_t - open_t| / open_t; legs by
    close vs open (red bar = close < open — the trader's vocabulary).
    Bars with no defined prior (index 0, NaN/zero prior close/open) are
    excluded and counted. Returns ({t: (dates, size, leg)}, counts).
    """
    pop, counts = {}, {"n_index0": 0, "n_bad_prior": 0}
    for t in close_map:
        c = close_map[t].to_numpy(dtype=np.float64)
        n = len(c)
        dates = close_map[t].index.to_numpy(dtype="datetime64[ns]")
        if candle:
            prev = open_map[t].to_numpy(dtype=np.float64)
        else:
            prev = np.empty_like(c)
            prev[0] = np.nan
            prev[1:] = c[:-1]
        ok = np.isfinite(prev) & (prev != 0.0)
        if candle:
            move = (c - prev) / prev
        else:
            move = c / prev - 1.0
        move = np.where(ok, move, np.nan)
        size = np.abs(move)
        leg = np.full(n, 2, dtype=np.int8)
        leg[ok & (move > 0.0)] = 0
        leg[ok & (move < 0.0)] = 1
        valid = ok & np.isfinite(size)
        valid[0] = False          # ticker-first bar: no prior bar in either mode
        counts["n_index0"] += 1
        counts["n_bad_prior"] += int(n - valid.sum() - 1)
        pop[t] = (dates[valid], size[valid], leg[valid])
    return pop, counts


def era_arrays(pop: dict, era_oos: str, era_is: bool = False):
    """Concatenated (size, leg) arrays over one era's bars. era_is=True:
    bars with date < era_oos (the selection era — descriptive only)."""
    sizes, legs = [], []
    t0 = np.datetime64(era_oos)
    for t, (dates, size, leg) in pop.items():
        m = dates < t0 if era_is else dates >= t0
        sizes.append(size[m])
        legs.append(leg[m])
    return (np.concatenate(sizes) if sizes else np.empty(0),
            np.concatenate(legs) if legs else np.empty(0, dtype=np.int8))


def stat_by_leg(size: np.ndarray, leg: np.ndarray, code: int, stat=np.mean):
    return float(stat(size[leg == code])) if (leg == code).any() else np.nan


def f1_joint(size: np.ndarray, leg: np.ndarray, rng, stat=np.mean):
    """Joint one-sample bootstrap of (leg mean - all mean) for both legs.

    Resamples the OOS bar population and recomputes the all-bars mean and
    the two leg means jointly, so the dependence between the two excesses
    is captured. Returns ({leg: (mean, med, lo, hi, p)}, all/up/down
    sample means).
    """
    m = len(size)
    n_up = int((leg == 0).sum())
    n_dn = int((leg == 1).sum())
    mean_all = float(stat(size))
    mean_up = stat_by_leg(size, leg, 0, stat)
    mean_dn = stat_by_leg(size, leg, 1, stat)
    up_exc = np.empty(B)
    dn_exc = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, m, size=m)
        s = size[idx]
        l = leg[idx]
        m_all = stat(s)
        up_exc[b] = stat(s[l == 0]) - m_all
        dn_exc[b] = stat(s[l == 1]) - m_all
    out = {}
    for code, exc in ((0, up_exc), (1, dn_exc)):
        lo, hi = np.percentile(exc, [2.5, 97.5])
        p = 2.0 * min((exc <= 0).mean(), (exc >= 0).mean())
        out["UP" if code == 0 else "DOWN"] = (
            float(exc.mean()), float(np.median(exc)), float(lo), float(hi),
            float(p))
    return out, mean_all, mean_up, mean_dn, n_up, n_dn


def one_sample_mean(x: np.ndarray, rng):
    """One-sample bootstrap of the mean; (mean, med, lo, hi, p)."""
    m = len(x)
    diffs = np.empty(B)
    for b in range(B):
        diffs[b] = x[rng.integers(0, m, size=m)].mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)), float(lo),
            float(hi), float(p))


def f1_cell(size: np.ndarray, leg: np.ndarray, rng, stat=np.mean) -> dict:
    """F1 family on one era's bar population (joint bootstrap + Holm)."""
    jb, mean_all, mean_up, mean_dn, n_up, n_dn = f1_joint(size, leg, rng, stat)
    fam = {}
    for legname, (est, med, lo, hi, p) in jb.items():
        fam[legname] = {"n_up": n_up, "n_down": n_dn,
                        "n_zero": int((leg == 2).sum()),
                        "n_all": int(len(size)),
                        "mean_all": mean_all, "mean_up": mean_up,
                        "mean_down": mean_dn,
                        "excess": [est, med, lo, hi, p],
                        "p": p, "est": est, "ci_low": lo, "ci_upper": hi}
    run_holm(fam, LEGS)
    for legname in LEGS:
        fam[legname]["verdict"] = verdict_f1(legname, fam[legname])
    return fam


def f2_cell(down: np.ndarray, up: np.ndarray, rng) -> dict:
    """F2: DOWN - UP contrast, two-sample bootstrap. Single test at
    alpha (holm gate = ALPHA)."""
    n_d, n_u = len(down), len(up)
    if n_d < 2 or n_u < 2:
        return {"n_down": n_d, "n_up": n_u, "mean_down": None,
                "mean_up": None, "est": None, "ci_low": None,
                "ci_upper": None, "p": 1.0, "holm_gate": ALPHA,
                "holm_rejected": False, "verdict": "NO EDGE (insufficient)"}
    est, med, lo, hi, p = two_sample_excess(down, up, rng)
    r = {"n_down": n_d, "n_up": n_u, "mean_down": float(down.mean()),
         "mean_up": float(up.mean()), "est": est, "ci_low": lo,
         "ci_upper": hi, "p": p, "holm_gate": ALPHA,
         "holm_rejected": p <= ALPHA}
    r["verdict"] = verdict_f2(r)
    return r


def retrace_speed(events_up: list, close_map: dict, L: int, N: int):
    """F4 per-event retracement-vs-move rate contrast on the frozen
    pre-reg #11 UP events. events_up = [(ticker, bar_index)] (warm-up
    excluded, OOS). Returns (diffs, j_list, n_retraced, n_non, n_tail)."""
    diffs, js = [], []
    n_retraced = n_non = n_tail = 0
    for t, i in events_up:
        c = close_map[t].to_numpy(dtype=np.float64)
        n = len(c)
        if i + N >= n:
            n_tail += 1
            continue
        base = c[i - L]
        if base == 0.0:
            n_tail += 1
            continue
        mid = (c[i] + base) / 2.0
        j = 0
        for k in range(1, N + 1):
            if c[i + k] <= mid:
                j = k
                break
        if j == 0:
            n_non += 1
            continue
        n_retraced += 1
        js.append(j)
        move_rate = (c[i] - base) / base / L
        retr_rate = (c[i] - mid) / base / j
        diffs.append(retr_rate - move_rate)
    return np.asarray(diffs, dtype=np.float64), np.asarray(js), \
        n_retraced, n_non, n_tail


def f4_cell(events_up: list, close_map: dict, L: int, N: int, rng) -> dict:
    """F4 family cell: paired one-sample bootstrap of
    (retrace-rate - move-rate)."""
    diffs, js, n_retraced, n_non, n_tail = retrace_speed(events_up,
                                                         close_map, L, N)
    r = {"n_events_total": len(events_up), "n_retraced": n_retraced,
         "n_non_retraced": n_non, "n_tail_dropped": n_tail,
         "mean_j": float(js.mean()) if len(js) else None,
         "share_crossed_within_N": (float(n_retraced) / (n_retraced
                                                          + n_non)
                                    if n_retraced + n_non else None),
         "mean_diff": float(diffs.mean()) if len(diffs) else None}
    if len(diffs) < MISSING_PASS:
        r.update({"est": None, "ci_low": None, "ci_upper": None, "p": 1.0,
                  "holm_gate": ALPHA, "holm_rejected": False})
        r["verdict"] = (f"INCONCLUSIVE (<{MISSING_PASS} retracing OOS "
                        f"events; n={n_retraced})")
        return r
    est, med, lo, hi, p = one_sample_mean(diffs, rng)
    r.update({"est": est, "ci_low": lo, "ci_upper": hi, "p": p,
              "holm_gate": ALPHA, "holm_rejected": p <= ALPHA})
    r["verdict"] = verdict_f4(r)
    return r


def verdict_f1(legname: str, r: dict) -> str:
    """F1 verdicts (pre-reg #12 sec 4)."""
    if int(r["n_all"]) < MISSING_PASS:
        return f"INCONCLUSIVE (<{MISSING_PASS} OOS bars; n={r['n_all']})"
    if legname == "UP":
        if r["holm_rejected"] and r["ci_upper"] < 0.0:
            return (f"EDGE (Holm-rejected; excess CI-upper {r['ci_upper']:+.4f}"
                    " < 0 — up-bars smaller than typical, stairs as claimed)")
        if r["holm_rejected"] and r["ci_low"] > 0.0:
            return (f"FADE (Holm-rejected; excess CI-low {r['ci_low']:+.4f} "
                    "> 0 — up-bars larger than typical, claim contradicted)")
    else:  # DOWN
        if r["holm_rejected"] and r["ci_low"] > 0.0:
            return (f"EDGE (Holm-rejected; excess CI-low {r['ci_low']:+.4f} "
                    "> 0 — down-bars larger than typical, window as claimed)")
        if r["holm_rejected"] and r["ci_upper"] < 0.0:
            return (f"FADE (Holm-rejected; excess CI-upper {r['ci_upper']:+.4f}"
                    " < 0 — down-bars smaller than typical, claim "
                    "contradicted)")
    return (f"NO EDGE (p {r['p']:.3f}; est {r['est']:+.4f}; CI-low "
            f"{r['ci_low']:+.4f}..CI-upper {r['ci_upper']:+.4f})")


def verdict_f2(r: dict) -> str:
    """F2 verdicts (pre-reg #12 sec 4)."""
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return (f"EDGE (contrast CI-low {r['ci_low']:+.4f} > 0 — down-bars "
                "larger than up-bars, the asymmetry as claimed)")
    if r["holm_rejected"] and r["ci_upper"] < 0.0:
        return (f"FADE (contrast CI-upper {r['ci_upper']:+.4f} < 0 — up-bars "
                "larger than down-bars, claim contradicted)")
    return (f"NO EDGE (contrast est {r['est']:+.4f}, p {r['p']:.3f})")


def verdict_f4(r: dict) -> str:
    """F4 verdicts (pre-reg #12 sec 4)."""
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return (f"EDGE (contrast CI-low {r['ci_low']:+.4f} > 0 — big "
                "up-moves' retracements outpace the moves, given-back-fast "
                "as claimed)")
    if r["holm_rejected"] and r["ci_upper"] < 0.0:
        return (f"FADE (contrast CI-upper {r['ci_upper']:+.4f} < 0 — "
                "retracements slower than the moves, claim contradicted)")
    return (f"NO EDGE (contrast est {r['est']:+.4f}, p {r['p']:.3f})")


def swing_rates(close_map: dict, k: int, era_oos: str):
    """S6: paired down-swing rate - up-swing rate on strict k-fractal
    swings of Close (same-type pivot runs coalesced to the more extreme;
    completed swings only, swing-end date >= era_oos)."""
    t0 = np.datetime64(era_oos)
    pairs = []
    n_up_sw = n_dn_sw = 0
    for t, c_s in close_map.items():
        c = c_s.to_numpy(dtype=np.float64)
        dates = c_s.index.to_numpy(dtype="datetime64[ns]")
        hi = swing_idx(c, k, False)
        lo = swing_idx(c, k, True)
        if not len(hi) or not len(lo):
            continue
        seq = sorted([(int(i), 1) for i in hi] + [(int(i), 0) for i in lo])
        piv = []
        for i, ty in seq:
            if piv and piv[-1][1] == ty:
                if ty == 1 and c[i] > c[piv[-1][0]]:
                    piv[-1] = (i, ty)
                elif ty == 0 and c[i] < c[piv[-1][0]]:
                    piv[-1] = (i, ty)
            else:
                piv.append((i, ty))
        # consecutive pivots alternate -> swings alternate up/down
        prev_rate = None
        prev_down = None
        for a, b in zip(piv, piv[1:]):
            i1, t1 = a
            i2, t2 = b
            if t1 == t2 or i2 - i1 == 0:
                continue
            size = abs(c[i2] - c[i1])
            rate = size / (i2 - i1)
            is_down = t1 == 1 and t2 == 0      # high -> low
            if dates[i2] < t0:
                prev_rate, prev_down = None, None
                continue
            if is_down:
                n_dn_sw += 1
                if prev_rate is not None and prev_down is False:
                    pairs.append(rate - prev_rate)
            else:
                n_up_sw += 1
            prev_rate, prev_down = rate, is_down
    return np.asarray(pairs, dtype=np.float64), n_up_sw, n_dn_sw


def main() -> int:
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()

    close_map, open_map, high_map, low_map = {}, {}, {}, {}
    for t in universe:
        if not (BARS_DIR / f"{t}.parquet").exists():
            continue
        df = pd.read_parquet(BARS_DIR / f"{t}.parquet")
        close_map[t] = df["Close"]
        open_map[t] = df["Open"]
        high_map[t] = df["High"]
        low_map[t] = df["Low"]

    # ---- primary per-bar population (close-to-close) ----
    pop, counts = per_ticker_sizes(close_map, open_map, candle=False)
    size_oos, leg_oos = era_arrays(pop, ERA_OOS)
    size_is, leg_is = era_arrays(pop, ERA_OOS, era_is=True)

    # ---- structural checks (pre-reg #12 sec 3) ----
    assert counts["n_bad_prior"] == 0, (
        f"{counts['n_bad_prior']} bars with a NaN/zero prior close "
        "(expected 0 in the frozen QA'd data)")
    assert int((leg_oos == 2).sum()) + int((leg_oos == 0).sum()) \
        + int((leg_oos == 1).sum()) == int(len(size_oos)), (
        "leg partition != full OOS population")

    rng = np.random.default_rng(SEED)

    # ---- F1 + F2 (primary) ----
    fam1 = f1_cell(size_oos, leg_oos, rng)
    down = size_oos[leg_oos == 1]
    up = size_oos[leg_oos == 0]
    fam2 = f2_cell(down, up, rng)

    # ---- F4 (retracement speed on the frozen pre-reg #11 UP events) ----
    # ATR-14 simple on the true ranges (the frozen pre-reg #11 convention).
    tr_map = {t: tr_series(pd.DataFrame({"High": high_map[t],
                                         "Low": low_map[t],
                                         "Close": close_map[t]}))
              for t in close_map}
    atr14 = {t: atr_simple(tr_map[t], ATR_PERIOD_PRIMARY)
             for t in close_map}
    det, stats = bigmove_det(close_map, atr14, L_PRIMARY, TAU_PRIMARY)
    ev_up = [(r.ticker, int(r.bar_index))
             for r in det.itertuples()
             if r.shape == "UP" and not bool(r.warmup)
             and str(r.signal_date) >= ERA_OOS]
    f4_min_sig = min((i for _, i in ev_up), default=None)
    assert f4_min_sig is None or f4_min_sig >= WARMUP, \
        "warm-up event leaked into F4"
    assert stats["n_bad_signal"] == 0
    fam4 = f4_cell(ev_up, close_map, L_PRIMARY, N_PRIMARY, rng)

    freq = {"n_all": int(len(size_oos)),
            "n_up": int((leg_oos == 0).sum()),
            "n_down": int((leg_oos == 1).sum()),
            "n_zero": int((leg_oos == 2).sum()),
            "down_share": float((leg_oos == 1).mean()),
            "n_index0": counts["n_index0"],
            "n_bad_prior": counts["n_bad_prior"]}

    # ---- sensitivities (pre-declared, NO verdicts) ----
    sens = {}

    # S1: median |r| (skew-robust), F1 joint + F2
    sens["median"] = {
        "f1": f1_cell(size_oos, leg_oos, rng, stat=np.median),
        "f2": median_contrast(down, up, rng)}

    # S2: candle-sign version (red = close < open)
    pop_c, counts_c = per_ticker_sizes(close_map, open_map, candle=True)
    size_c, leg_c = era_arrays(pop_c, ERA_OOS)
    sens["candle_sign"] = {
        "counts": {"n_bad_prior": counts_c["n_bad_prior"],
                   "n_zero_doji": int((leg_c == 2).sum())},
        "f1": f1_cell(size_c, leg_c, rng),
        "f2": f2_cell(size_c[leg_c == 1], size_c[leg_c == 0], rng)}

    # S3: per-ticker contrasts + ticker-cluster CI (OOS bars only, as S5)
    tick_contrasts = {}
    for t, (dates, size, leg) in pop.items():
        m = dates >= np.datetime64(ERA_OOS)
        if not m.any():
            continue
        s, l = size[m], leg[m]
        if not (l == 0).any() or not (l == 1).any():
            continue
        tick_contrasts[t] = float(s[l == 1].mean()
                                  - s[l == 0].mean())
    tc = np.fromiter(tick_contrasts.values(), dtype=np.float64)
    tc_bs = one_sample_mean(tc, rng)
    sens["per_ticker"] = {
        "n_tickers": int(len(tc)),
        "n_positive": int((tc > 0).sum()),
        "share_positive": float((tc > 0).mean()),
        "mean_contrast": float(tc.mean()),
        "cluster_ci_low": tc_bs[2], "cluster_ci_upper": tc_bs[3],
        "cluster_p": tc_bs[4]}

    # S4: IS-era (descriptive — selection era)
    sens["is_era"] = {
        "f1": f1_cell(size_is, leg_is, rng),
        "f2": f2_cell(size_is[leg_is == 1], size_is[leg_is == 0], rng)}

    # S5: per-year F1/F2 (OOS)
    py = {}
    for t, (dates, size, leg) in pop.items():
        m = dates >= np.datetime64(ERA_OOS)
        if not m.any():
            continue
        yrs = dates[m].astype("datetime64[Y]").astype(int) + 1970
        for y in np.unique(yrs):
            yy = int(y)
            ym = yrs == y
            s, l = size[m][ym], leg[m][ym]
            cell = py.setdefault(yy, {"n_up": 0, "n_down": 0, "sum_up": 0.0,
                                      "sum_down": 0.0, "n_zero": 0})
            cell["n_up"] += int((l == 0).sum())
            cell["n_down"] += int((l == 1).sum())
            cell["n_zero"] += int((l == 2).sum())
            cell["sum_up"] += float(s[l == 0].sum())
            cell["sum_down"] += float(s[l == 1].sum())
    sens["per_year"] = {
        str(y): {"n_up": c["n_up"], "n_down": c["n_down"],
                 "n_zero": c["n_zero"],
                 "mean_up": (c["sum_up"] / c["n_up"]
                             if c["n_up"] else None),
                 "mean_down": (c["sum_down"] / c["n_down"]
                               if c["n_down"] else None),
                 "contrast": ((c["sum_down"] / c["n_down"]
                               - c["sum_up"] / c["n_up"])
                              if c["n_up"] and c["n_down"] else None)}
        for y, c in sorted(py.items())}

    # S6: swing-scale A1 (paired down-rate - up-rate)
    sens["swings"] = {}
    for k in K_SWINGS:
        pairs, n_u, n_d = swing_rates(close_map, k, ERA_OOS)
        cell = {"k": k, "n_up_swings": n_u, "n_down_swings": n_d,
                "n_pairs": int(len(pairs))}
        if len(pairs):
            bs = one_sample_mean(pairs, rng)
            cell.update({"mean_contrast": bs[0], "ci_low": bs[2],
                         "ci_upper": bs[3], "p": bs[4]})
        else:
            cell.update({"mean_contrast": None, "ci_low": None,
                         "ci_upper": None, "p": 1.0})
        sens["swings"][f"k={k}"] = cell

    # S7: F4 variants — N = 5/20 windows and tau = 2/5 populations
    sens["f4_variants"] = {}
    for n in SENS_N:
        cell = f4_cell(ev_up, close_map, L_PRIMARY, n, rng)
        cell.pop("verdict", None)
        sens["f4_variants"][f"N={n}"] = cell
    for tau in SENS_TAU:
        det_t, _ = bigmove_det(close_map, atr14, L_PRIMARY, tau)
        ev_t = [(r.ticker, int(r.bar_index))
                for r in det_t.itertuples()
                if r.shape == "UP" and not bool(r.warmup)
                and str(r.signal_date) >= ERA_OOS]
        cell = f4_cell(ev_t, close_map, L_PRIMARY, N_PRIMARY, rng)
        cell.pop("verdict", None)
        sens["f4_variants"][f"tau={tau:g}"] = cell

    # S8: tail concentration — down-bar share in the largest-|r| decile
    th = np.percentile(size_oos, 90.0)
    top = size_oos >= th
    n_top = int(top.sum())
    n_top_dn = int((top & (leg_oos == 1)).sum())
    sens["tail_decile"] = {
        "threshold": float(th), "n_top": n_top,
        "n_top_down": n_top_dn,
        "share_down_top": float(n_top_dn / n_top),
        "share_down_all": float(freq["down_share"]),
        "diff_pp": float(n_top_dn / n_top - freq["down_share"]) * 100.0}

    out = {
        "pre_reg": "#12",
        "claim": ("'The move up that may have taken hours can be all given "
                  "back in a matter of minutes on the good top reversal... "
                  "the Bulls take the stairs and the Bears take the window "
                  "so the sell offs can be very quick' (Warrior Trading, "
                  "jfe1Zl-5EQI [28:28-28:47], corroborated [17:34-17:37]). "
                  "Measured: per-bar speed asymmetry on US equity daily "
                  "bars — A1: down-bars' mean |close-to-close % move| vs "
                  "up-bars' (F1 legs vs the typical-bar baseline, F2 "
                  "contrast); A2: retracements of the frozen pre-reg #11 "
                  "big up-moves (L=10, tau=3) vs the moves themselves "
                  "(F4). Intraday->daily translation pre-declared: daily "
                  "speed is per-bar magnitude."),
        "params": {"n": N_PRIMARY, "b": B, "seed": SEED, "alpha": ALPHA,
                   "era_oos_start": ERA_OOS, "count_floor": MISSING_PASS,
                   "f4_move_L": L_PRIMARY, "f4_tau": TAU_PRIMARY,
                   "f4_atr_period": ATR_PERIOD_PRIMARY,
                   "f4_warmup": WARMUP,
                   "f4_n_sensitivities": list(SENS_N),
                   "f4_tau_sensitivities": list(SENS_TAU),
                   "swing_k_sensitivities": list(K_SWINGS),
                   "engine_sha256": "c7421fbf (frozen Phase-3 engine — "
                                    "NOT invoked: no forward returns)"},
        "families": {"f1_typical_size": fam1, "f2_asymmetry": fam2,
                     "f4_retrace_speed": fam4},
        "frequency": freq,
        "sensitivities": sens,
        "assertions": {"n_bad_prior": counts["n_bad_prior"],
                       "n_index0": counts["n_index0"],
                       "n_zero_bars": int((leg_oos == 2).sum()),
                       "f4_min_signal": f4_min_sig,
                       "f4_n_events": len(ev_up),
                       "f4_stats": stats,
                       "partitions_ok": True},
        "fingerprints": {
            "universe_sha256": sha(UNIVERSE_CSV),
            "measure_code_sha256": sha(Path(__file__)),
            "engine_sha256": sha(Path(__file__).parent / "measure.py"),
            "divergence_code_sha256": sha(
                Path(__file__).parent / "measure_divergence.py"),
            "bigmove_code_sha256": sha(
                Path(__file__).parent / "measure_bigmove.py"),
            "veto_code_sha256": sha(
                Path(__file__).parent / "measure_veto.py"),
        },
    }
    RESULTS.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {RESULTS.name}")

    # ---- report ----
    L = []
    L.append("# Speed-asymmetry measurement report (pre-registration #12)")
    L.append("")
    L.append("- Pre-registration #12 (frozen 2026-08-15): claim = 'the move "
             "up that may have taken hours can be all given back in a matter "
             "of minutes on the good top reversal... the Bulls take the "
             "stairs and the Bears take the window so the sell offs can be "
             "very quick' (I-F-02, jfe1Zl-5EQI [28:28-28:47], corroborated "
             "[17:34-17:37]). Daily translation: speed = price distance per "
             "bar. Per-bar size = |close_t/close_{t-1} - 1|; UP bars "
             "(r > 0), DOWN bars (r < 0), zero bars (r = 0) excluded from "
             "the legs and counted. A1 (F1/F2): down-bars larger than "
             "up-bars; A2 (F4): retracements of the frozen pre-reg #11 big "
             "up-moves (L=10, tau=3, excursion-first) outpace the moves "
             f"themselves. N = {N_PRIMARY} crossing window; bootstrap {B} "
             f"(seed {SEED}); alpha {ALPHA}; Holm within each family; count "
             "floor 100 events.")
    L.append("- No forward returns are measured: the Phase-3 engine's "
             "measure_returns is NOT invoked (pre-reg #12 sec 3) — the "
             "claim is about bar geometry, not profitability. Phase 5 is "
             "not implicated by construction.")
    L.append("- Era split: IS 2000-2015 / OOS 2016-2025 (by bar date). "
             "Intraday->daily translation pre-declared: daily 'speed' is "
             "per-bar magnitude; overnight gaps register as fast. Measured "
             "on US equity daily bars (the frozen S&P 600 universe).")
    L.append(f"- OOS bar population: {freq['n_all']} bars "
             f"(UP {freq['n_up']}, DOWN {freq['n_down']}, ZERO "
             f"{freq['n_zero']}); {counts['n_index0']} ticker-first bars "
             f"excluded; down-bar share {freq['down_share']:.4f}.")
    L.append("")
    L.append("## Verdicts — Family 1: absolute, per leg vs the "
             "typical-bar baseline")
    L.append("")
    for legname in LEGS:
        r = fam1[legname]
        L.append(f"- F1-{legname}: n={r['n_all']} (UP {r['n_up']}, DOWN "
                 f"{r['n_down']}, ZERO {r['n_zero']}) | mean all "
                 f"{fmt_num(r['mean_all'])} | mean {legname.lower()} "
                 f"{fmt_num(r['mean_up'] if legname == 'UP' else r['mean_down'])}"
                 f" | excess {r['est']:+.4f} (CI {r['ci_low']:+.4f}.."
                 f"{r['ci_upper']:+.4f}, p {r['p']:.3f}) | Holm gate "
                 f"{r['holm_gate']:.4f} -> **{r['verdict']}**")
    L.append("")
    L.append("## Verdicts — Family 2: the asymmetry contrast (DOWN - UP)")
    L.append("")
    r = fam2
    L.append(f"- F2: n_down={r['n_down']} n_up={r['n_up']} | mean down "
             f"{fmt_num(r['mean_down'])} vs mean up {fmt_num(r['mean_up'])}"
             f" | contrast {r['est']:+.4f} (CI {r['ci_low']:+.4f}.."
             f"{r['ci_upper']:+.4f}, p {r['p']:.3f}) | Holm gate "
             f"{r['holm_gate']:.4f} -> **{r['verdict']}**")
    L.append("")
    L.append("## Verdicts — Family 4: retracement speed on big up-moves "
             "(A2)")
    L.append("")
    r = fam4
    L.append(f"- F4: n_events={r['n_events_total']} (retraced "
             f"{r['n_retraced']}, non-retraced {r['n_non_retraced']}, "
             f"tail-dropped {r['n_tail_dropped']}); share crossing within "
             f"{N_PRIMARY} bars "
             f"{fmt_num(r['share_crossed_within_N'], '.4f')}; mean j "
             f"{fmt_num(r['mean_j'], '.2f')} bars; mean contrast "
             f"{fmt_num(r['mean_diff'])} per bar (CI {fmt_num(r['ci_low'])}.."
             f"{fmt_num(r['ci_upper'])}, p {r['p']:.3f}) -> **{r['verdict']}**")
    L.append("")
    L.append("## Frequency (measurement, not a verdict family)")
    L.append("")
    L.append(f"- OOS bars: UP {freq['n_up']} / DOWN {freq['n_down']} / ZERO "
             f"{freq['n_zero']} / all {freq['n_all']}; down-bar share "
             f"{freq['down_share']:.4f}; index-0 excluded {freq['n_index0']}; "
             f"bad prior {freq['n_bad_prior']}.")
    L.append("")
    L.append("## Sensitivities (exploratory — NO verdicts)")
    L.append("")
    L.append("### S1: median |r| (skew-robust)")
    L.append("")
    for legname in LEGS:
        r = sens["median"]["f1"][legname]
        L.append(f"- F1-{legname}: median up {fmt_num(r['mean_up'])} / "
                 f"median down {fmt_num(r['mean_down'])} | excess "
                 f"{r['est']:+.4f} (CI {r['ci_low']:+.4f}..{r['ci_upper']:+.4f}"
                 f", p {r['p']:.3f})")
    r = sens["median"]["f2"]
    L.append(f"- F2 (median contrast): {fmt_num(r['est'])} (CI "
             f"{fmt_num(r['ci_low'])}..{fmt_num(r['ci_upper'])}, "
             f"p {r['p']:.3f})")
    L.append("")
    L.append("### S2: candle-sign version (red = close < open)")
    L.append("")
    L.append(f"*Bad priors {sens['candle_sign']['counts']['n_bad_prior']}, "
             f"dojis (close == open) "
             f"{sens['candle_sign']['counts']['n_zero_doji']}.*")
    for legname in LEGS:
        r = sens["candle_sign"]["f1"][legname]
        body = r["mean_up"] if legname == "UP" else r["mean_down"]
        L.append(f"- F1-{legname}: mean body {fmt_num(body)} | excess "
                 f"{r['est']:+.4f} (CI {r['ci_low']:+.4f}..{r['ci_upper']:+.4f}"
                 f", p {r['p']:.3f})")
    r = sens["candle_sign"]["f2"]
    L.append(f"- F2 (red - green): {fmt_num(r['est'])} (CI "
             f"{fmt_num(r['ci_low'])}..{fmt_num(r['ci_upper'])}, "
             f"p {r['p']:.3f})")
    L.append("")
    L.append("### S3: per-ticker contrasts (ticker-cluster CI)")
    L.append("")
    r = sens["per_ticker"]
    L.append(f"- n_tickers={r['n_tickers']}; share positive {fmt_num(r['share_positive'], '.4f')}; "
             f"mean per-ticker contrast {fmt_num(r['mean_contrast'])} "
             f"(cluster CI {fmt_num(r['cluster_ci_low'])}.."
             f"{fmt_num(r['cluster_ci_upper'])}, p {r['cluster_p']:.3f})")
    L.append("")
    L.append("### S4: IS-era (descriptive — selection era)")
    L.append("")
    for legname in LEGS:
        r = sens["is_era"]["f1"][legname]
        L.append(f"- F1-{legname}: n={r['n_all']} | excess {r['est']:+.4f} "
                 f"(CI {r['ci_low']:+.4f}..{r['ci_upper']:+.4f}, "
                 f"p {r['p']:.3f})")
    r = sens["is_era"]["f2"]
    L.append(f"- F2 (IS): {fmt_num(r['est'])} (CI {fmt_num(r['ci_low'])}.."
             f"{fmt_num(r['ci_upper'])}, p {r['p']:.3f})")
    L.append("")
    L.append("### S5: per-year (OOS)")
    L.append("")
    L.append("| year | mean UP | mean DOWN | contrast (pp) |")
    L.append("|---|---|---|---|")
    for y in sorted(sens["per_year"]):
        c = sens["per_year"][y]
        L.append(f"| {y} | {fmt_num(c['mean_up'])} (n={c['n_up']}) | "
                 f"{fmt_num(c['mean_down'])} (n={c['n_down']}) | "
                 f"{fmt_num(c['contrast'] * 100.0, '+.2f') if c['contrast'] is not None else '—'} |")
    L.append("")
    L.append("### S6: swing-scale A1 (strict k-fractal swings on Close)")
    L.append("")
    L.append("*Paired contrast: down-swing rate (size/duration) - preceding "
             "up-swing rate; same-type pivot runs coalesced to the more "
             "extreme; completed swings, swing-end date in OOS.*")
    for k in K_SWINGS:
        c = sens["swings"][f"k={k}"]
        L.append(f"- k={k}: n_pairs={c['n_pairs']} (up {c['n_up_swings']}, "
                 f"down {c['n_down_swings']}) | mean contrast "
                 f"{fmt_num(c['mean_contrast'])} (CI "
                 f"{fmt_num(c['ci_low'])}..{fmt_num(c['ci_upper'])}, "
                 f"p {c['p']:.3f})")
    L.append("")
    L.append("### S7: F4 variants")
    L.append("")
    for key, c in sens["f4_variants"].items():
        L.append(f"- {key}: retraced {c['n_retraced']} / total "
                 f"{c['n_events_total']}; mean j {fmt_num(c['mean_j'], '.2f')}"
                 f" | mean contrast {fmt_num(c['mean_diff'])} (CI "
                 f"{fmt_num(c['ci_low'])}..{fmt_num(c['ci_upper'])}, "
                 f"p {c['p']:.3f})")
    L.append("")
    L.append("### S8: tail concentration (largest-|r| decile)")
    L.append("")
    c = sens["tail_decile"]
    L.append(f"- threshold {fmt_num(c['threshold'], '.4f')}; n_top="
             f"{c['n_top']}, down share in top decile "
             f"{fmt_num(c['share_down_top'], '.4f')} vs overall "
             f"{fmt_num(c['share_down_all'], '.4f')} (diff "
             f"{fmt_num(c['diff_pp'], '+.2f')}pp)")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_speed.py` regenerates this "
             "report; the seed is fixed, so results are stable across runs.")
    L.append(f"Assertions: no bad prior closes ({counts['n_bad_prior']}); "
             f"zero bars counted ({freq['n_zero']}); leg partition covers "
             "the full OOS population (PASS); F4 signal bars >= 60 (min "
             f"{out['assertions']['f4_min_signal']}, PASS); no event whose "
             "signal bar lies beyond the ticker's series (PASS); F4 "
             "crossing j in [1, N] (by construction).")
    L.append("Input fingerprints: universe %s…, measure code %s… (engine "
             "%s… NOT invoked — no forward returns; generic helpers from "
             "measure_divergence %s…, measure_veto %s…, measure_bigmove "
             "%s…)."
             % (out["fingerprints"]["universe_sha256"][:12],
                out["fingerprints"]["measure_code_sha256"][:12],
                out["fingerprints"]["engine_sha256"][:12],
                out["fingerprints"]["divergence_code_sha256"][:12],
                out["fingerprints"]["veto_code_sha256"][:12],
                out["fingerprints"]["bigmove_code_sha256"][:12]))
    L.append("Any change to the detector, data, or measurement code changes "
             "the frozen inputs and requires a new pre-registration before "
             "it can drive a verdict.")
    L.append("")
    REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT.name}")
    return 0


def median_contrast(down: np.ndarray, up: np.ndarray, rng):
    """Two-sample bootstrap of the median difference (S1)."""
    M, F = len(down), len(up)
    diffs = np.empty(B)
    for b in range(B):
        diffs[b] = np.median(down[rng.integers(0, M, size=M)]) \
            - np.median(up[rng.integers(0, F, size=F)])
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return {"est": float(diffs.mean()), "ci_low": float(lo),
            "ci_upper": float(hi), "p": float(p)}


if __name__ == "__main__":
    sys.exit(main())
