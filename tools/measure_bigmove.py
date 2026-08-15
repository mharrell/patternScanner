"""Big-move mean-reversion measurement for pre-registration #11 (ledger
row I-F-01), frozen 2026-08-14.

The claim (Warrior Trading, jfe1Zl-5EQI [16:01-16:09], [15:05-15:09]):
  "We know that almost all of the big moves will eventually be corrected";
  "what goes up must come down and what goes down must come back up".

Definitions (frozen, pre-reg #11 sec 1):
  Big-move event at bar t: |close_t - close_{t-L}| >= TAU * ATR_t, with
  L = 10 primary (a two-week move) and TAU = 3 primary ("a move of three
  average true ranges"). UP leg iff close_t > close_{t-L}; DOWN leg iff
  close_t < close_{t-L}. Claims: an UP move => below-baseline forward
  returns (corrected); a DOWN move => above-baseline forward returns
  (recovered).
  ATR_t = simple mean of the 14 true ranges ending at t (Cutler-style,
  consistent with the project's simple-average RSI — no ATR teaching was
  found in the corpus, so the definition is pre-registered):
  TR_t = max(high_t - low_t, |high_t - close_{t-1}|, |low_t - close_{t-1}|);
  ATR_t = mean(TR_{t-13..t}). Wilder's smoothing (RMA) is sensitivity S4.
  EVENT-LEVEL: the event is the FIRST bar of each maximal run of
  consecutive qualifying bars (the pre-reg #9 S4 crossing rule; the
  RSI-70/30 lesson). The state-level view (every qualifying bar) is
  sensitivity S5, NOT the primary.
  TIMING: signal at close t (uses only bars <= t); entry open t+1;
  exit close t+N. No look-ahead.

F1 (absolute, directional per leg): mean OOS N-bar forward return of the
leg vs era-matched baselines (random entries -COST, same-ticker -COST,
SPY raw). Convention as pre-regs #9/#10: p_input = max(p_rand, p_same),
est = max, ci_low = min, ci_upper = min. Holm across the two legs.
  UP: EDGE iff Holm-rejected AND excess CI-upper < 0 (significantly below
      both baselines — "corrected", as claimed); FADE iff Holm-rejected
      AND CI-low > 0.
  DOWN: EDGE iff Holm-rejected AND excess CI-low > 0 (significantly above
      both baselines — "recovered", as claimed); FADE iff Holm-rejected
      AND CI-upper < 0.

F2 (retracement claim test, per leg): the leg's share of events with
close_{t+N} past the move's midpoint (close_t + close_{t-L})/2 within
N = 10 sessions ("corrected half"; UP: close_{t+N} <= midpoint, DOWN:
close_{t+N} >= midpoint), minus the same share on era-matched random bars
— each random bar's own trailing L-bar move, direction-matched to the leg
(an UP-leg null bar has close_r > close_{r-L}, a DOWN-leg null bar has
close_r < close_{r-L}), same N, same universe, warm-up guard and tail
validity applied identically. The calibrated null ("what share of typical
bars retrace half their trailing move"), not an assumed 0.5. Holm across
the two legs: EDGE iff Holm-rejected AND CI-low > 0; FADE iff
Holm-rejected AND CI-upper < 0.

Phase-5 trigger (pre-reg #11 sec 4): ONLY an F1-DOWN EDGE can trigger the
trigger-check conversation (F1-UP EDGE is a negative-return finding; F2
is a differential finding).

Protocol (pre-reg #11 sec 3): N = 10 primary, COST = 0.0015, B = 1000
seed 20260813, era split by signal date (IS 2000-2015 / OOS 2016-2025),
warm-up guard signal-bar index < 60 excluded and counted (bounds the
10-bar move window and the 14-bar ATR lookback with margin),
Holm-Bonferroni at alpha = 0.05 within each family, count floor 100 OOS
events per leg (F1 and F2 both -> INCONCLUSIVE).

Sensitivities (pre-declared, NO verdicts): S1 horizons N = 1/5/20 (F1,
baselines rebuilt per horizon; retracement reported at N = 5 — the
claim's "5-10 sessions" range); S2 TAU = 2/5 (F1 + F2, L=10); S3 L = 5
(F1 + F2, TAU = 3); S4 ATR period 7 and Wilder's smoothing (F1); S5
state-level view (F1, overlap-inflated by construction); S6 per-year F1
leg mean returns (OOS); S7 IS record (F1, descriptive); S8 retracement vs
the move window's extreme (UP: midpoint of close_{t-L} and the window's
max high; DOWN: midpoint of close_{t-L} and the window's min low) — F2.

Structural checks (pre-reg #11 sec 3): (a) ATR >= 0 everywhere (TR >= 0
by construction; a zero-range day can give ATR = 0 — the threshold is
compared in price units, never a divisor); (b) no measured event with
signal bar < 60 (warm-up guard, excluded and counted); (c) no event with
t - L < 0 (impossible under (b); asserted over ALL events as min_signal
>= L); (d) no event with signal bar > n_bars - 1 (n_bad_signal = 0;
series-end drops are the engine's standard drops, counted, and the F2
event-side drops must equal the engine's drops per leg).

Engine pieces import from measure.py (frozen, sha c7421fbf...): forward
returns run through the engine's measure_returns unchanged. Its dropped
dict is keyed A/B/C (frozen engine), so the UP/DOWN legs pass with
placeholder shapes (UP -> "A", DOWN -> "B") and rows are relabeled after
measurement (the pre-reg #9/#10 convention). Generic measurement helpers
(f1_leg, two_sample_hit, run_holm) import from measure_divergence so the
p_input = max / est = max / CI = min convention is byte-identical with
the pre-reg #10 campaign. ATR, moves, excursions, and retracement
indicators are computed here from the frozen parquet bars read directly
(signal inputs <= signal bar only, same frozen Close column as load_bars;
High/Low/Open are read only for the detector and the engine's own
forward-return formula).
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import measure
from measure import (COST, B, SEED, ALPHA, ERA_OOS, UNIVERSE_CSV, BARS_DIR,
                     measure_returns)
from measure_pillars import build_pools
from measure_divergence import (f1_leg, two_sample_hit, run_holm, fmt_num,
                                sha, pools_of)

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
RESULTS = CACHE / "bigmove_measure_results.json"
REPORT = CACHE / "bigmove_measure_report.md"

L_PRIMARY = 10                   # pre-reg #11 sec 1: move window (two weeks)
TAU_PRIMARY = 3.0                #   |move| >= 3 * ATR_t ("three average true
                                 #   ranges")
ATR_PERIOD_PRIMARY = 14          #   simple mean of the 14 true ranges ending
                                 #   at t (pre-registered; no corpus teaching)
N_PRIMARY = 10
SENS_N = [1, 5, 20]              # pre-reg #11 sec 6 S1 (retracement at N=5)
SENS_TAU = (2.0, 5.0)            # pre-reg #11 sec 6 S2
L_SENS = 5                       # pre-reg #11 sec 6 S3
ATR_PERIOD_SENS = 7              # pre-reg #11 sec 6 S4 (simple period 7)
WARMUP = 60                      # frozen #3 convention
MISSING_PASS = 100               # count floor per leg
LEGS = ("UP", "DOWN")
LEG_PLACEHOLDER = {"UP": "A", "DOWN": "B"}   # measure_returns' dropped dict
                                             # is keyed A/B/C (frozen engine);
                                             # legs relabeled after
U_DIR = "up"                     # report wording
D_DIR = "down"


def tr_series(df: pd.DataFrame) -> pd.Series:
    """True range at bar t: max(high_t - low_t, |high_t - close_{t-1}|,
    |low_t - close_{t-1}|); undefined (NaN) at t = 0 (no prior close)."""
    high = df["High"].to_numpy(dtype=np.float64)
    low = df["Low"].to_numpy(dtype=np.float64)
    close = df["Close"].to_numpy(dtype=np.float64)
    prev_close = np.empty_like(close)
    prev_close[0] = np.nan
    prev_close[1:] = close[:-1]
    tr = np.maximum(high - low,
                    np.maximum(np.abs(high - prev_close),
                               np.abs(low - prev_close)))
    return pd.Series(tr, index=df.index)


def atr_simple(tr: pd.Series, period: int) -> pd.Series:
    """ATR_t = simple mean of the `period` true ranges ending at t
    (TR_{t-period+1..t}). tr[0] is NaN (no prior close), so the first valid
    bar is index `period`."""
    return tr.rolling(period).mean()


def atr_wilder(tr: pd.Series, period: int) -> pd.Series:
    """Wilder's RMA variant (S4): seeded with the simple mean of the first
    `period` valid ranges (tr[1..period], since tr[0] is NaN) at index
    `period` — aligned with the simple ATR's first valid bar — then
    ATR_t = (ATR_{t-1} * (period - 1) + TR_t) / period."""
    v = tr.to_numpy(dtype=np.float64)
    n = len(v)
    out = np.full(n, np.nan)
    if n > period:
        out[period] = float(np.nanmean(v[1:period + 1]))
        for i in range(period + 1, n):
            out[i] = (out[i - 1] * (period - 1) + v[i]) / period
    return pd.Series(out, index=tr.index)


def bigmove_det(close_map: dict, atr_map: dict, L: int, tau: float,
                state_level: bool = False):
    """Big-move event detections across the universe.

    Qualifying bar t: |close_t - close_{t-L}| >= tau * ATR_t (both legs
    strict in direction: UP iff close_t > close_{t-L}, DOWN iff close_t <
    close_{t-L}). Event-level: the FIRST bar of each maximal run of
    consecutive qualifying bars (state_level=True: every qualifying bar —
    the overlap-inflated S5 view). Returns (det, stats) with stats =
    {min_signal, max_signal, n_bad_signal} over the events.
    """
    rows = []
    min_sig, max_sig, n_bad = np.inf, -np.inf, 0
    for t, close in close_map.items():
        c = close.to_numpy(dtype=np.float64)
        atr = atr_map[t].to_numpy(dtype=np.float64)
        dates = close.index
        n_bars = len(c)
        move = np.full(n_bars, np.nan)
        move[L:] = c[L:] - c[:n_bars - L]       # close_t - close_{t-L}, t >= L
        up = (move >= tau * atr) & (move > 0.0)
        dn = (move <= -tau * atr) & (move < 0.0)
        for leg, flag in (("UP", up), ("DOWN", dn)):
            if state_level:
                pos = np.where(flag)[0]
            else:
                start = flag.copy()
                start[1:] &= ~flag[:-1]         # first bar of each run
                pos = np.where(start)[0]
            if not len(pos):
                continue
            min_sig = min(min_sig, int(pos.min()))
            max_sig = max(max_sig, int(pos.max()))
            n_bad += int((pos >= n_bars).sum())
            rows += [(t, str(dates[i].date()), leg, int(i)) for i in pos]
    det = pd.DataFrame(rows, columns=["ticker", "signal_date", "shape",
                                      "bar_index"])
    det["warmup"] = det["bar_index"] < WARMUP
    stats = {"min_signal": min_sig, "max_signal": max_sig,
             "n_bad_signal": n_bad}
    return det, stats


def measure_legs(det: pd.DataFrame, N: int):
    """Engine forward returns per leg (placeholder shapes, relabeled)."""
    out = {}
    drops = {}
    for leg in LEGS:
        sub = det[det["shape"] == leg].assign(shape=LEG_PLACEHOLDER[leg])
        rows, dropped = measure_returns(sub, N)
        rows["shape"] = leg
        out[leg] = rows
        drops[leg] = int(dropped[LEG_PLACEHOLDER[leg]])
    return out, drops


def event_retrace(det_leg: pd.DataFrame, close_map: dict, high_map: dict,
                  low_map: dict, L: int, N: int, extreme: bool = False):
    """0/1 corrected-half indicators per event (warm-up-excluded rows):
    close_{t+N} on the far side of the move's midpoint. Events whose exit
    bar lies beyond the ticker's series are dropped and counted — the
    drop count must equal the engine's drops for the leg (same rule).

    extreme (S8): midpoint of close_{t-L} and the move window's extreme
    (UP: max high over bars t-L..t; DOWN: min low over bars t-L..t)
    instead of the close-to-close midpoint.
    """
    inds = []
    drops = 0
    for _, r in det_leg.iterrows():
        c = close_map[r["ticker"]].to_numpy(dtype=np.float64)
        n = len(c)
        i = int(r["bar_index"])
        if i + N >= n:
            drops += 1
            continue
        if extreme:
            if r["shape"] == "UP":
                hi = high_map[r["ticker"]].iloc[i - L:i + 1].max()
                mid = (c[i - L] + float(hi)) / 2.0
            else:
                lo = low_map[r["ticker"]].iloc[i - L:i + 1].min()
                mid = (c[i - L] + float(lo)) / 2.0
        else:
            mid = (c[i] + c[i - L]) / 2.0
        fwd = c[i + N]
        if r["shape"] == "UP":
            inds.append(1.0 if fwd <= mid else 0.0)
        else:
            inds.append(1.0 if fwd >= mid else 0.0)
    return np.asarray(inds, dtype=np.float64), drops


def null_arrays(close_map: dict, high_map: dict, low_map: dict, L: int,
                N: int, extreme: bool = False):
    """Era-matched random-bar corrected-half indicators, per leg.

    Every OOS bar (warm-up guard and tail validity applied identically to
    the events) contributes its OWN trailing L-bar move: UP-leg null bars
    have close_r > close_{r-L}, DOWN-leg null bars have close_r <
    close_{r-L}. Vectorized per ticker.
    """
    up_all, dn_all = [], []
    for t, c_s in close_map.items():
        c = c_s.to_numpy(dtype=np.float64)
        oos = pd.to_datetime(c_s.index) >= pd.Timestamp(ERA_OOS)
        n = len(c)
        move = np.full(n, np.nan)
        move[L:] = c[L:] - c[:n - L]
        prev = np.full(n, np.nan)
        prev[L:] = c[:n - L]                     # c[i - L]
        fwd = np.full(n, np.nan)
        fwd[:n - N] = c[N:]                      # c[i + N]
        valid = (oos & (np.arange(n) >= WARMUP) & ~np.isnan(move)
                 & ~np.isnan(fwd))
        if extreme:
            hi = high_map[t].rolling(L + 1).max().to_numpy()
            lo = low_map[t].rolling(L + 1).min().to_numpy()
            mid_up = (prev + hi) / 2.0
            mid_dn = (prev + lo) / 2.0
            u = valid & (move > 0.0) & ~np.isnan(mid_up)
            d = valid & (move < 0.0) & ~np.isnan(mid_dn)
            up_all.append((fwd[u] <= mid_up[u]).astype(np.float64))
            dn_all.append((fwd[d] >= mid_dn[d]).astype(np.float64))
        else:
            mid = (c + prev) / 2.0
            u = valid & (move > 0.0)
            d = valid & (move < 0.0)
            up_all.append((fwd[u] <= mid[u]).astype(np.float64))
            dn_all.append((fwd[d] >= mid[d]).astype(np.float64))
    up = np.concatenate(up_all) if up_all else np.empty(0, dtype=np.float64)
    dn = np.concatenate(dn_all) if dn_all else np.empty(0, dtype=np.float64)
    return up, dn


def f2_leg(sel: np.ndarray, full: np.ndarray, rng) -> dict:
    """F2 cell: events' corrected-half rate minus the random-bar rate
    (two-sample bootstrap, the two_sample_hit convention from pre-reg #10)."""
    n_s, n_f = len(sel), len(full)
    if n_s == 0 or n_f == 0:
        return {"n_events": n_s, "n_random": n_f, "rate_events": None,
                "rate_random": None, "est": None, "ci_low": None,
                "ci_upper": None, "p": 1.0}
    tx = two_sample_hit(sel, full, rng)
    return {"n_events": n_s, "n_random": n_f,
            "rate_events": float(sel.mean()),
            "rate_random": float(full.mean()),
            "est": float(tx[0]), "ci_low": float(tx[2]),
            "ci_upper": float(tx[3]), "p": float(tx[4])}


def f2_family(camp: pd.DataFrame, close_map: dict, high_map: dict,
              low_map: dict, L: int, N: int, null_up: np.ndarray,
              null_dn: np.ndarray, rng, extreme: bool = False,
              drops_ref: dict = None) -> dict:
    """F2 family: per-leg corrected-half contrast (events vs the
    era-matched random-bar rate), Holm across the two legs. When drops_ref
    is given, verifies the event-side drop count against the engine's
    drops for the leg (same tail rule — expected equal)."""
    fam = {}
    for leg in LEGS:
        sel, dr = event_retrace(camp[camp["shape"] == leg], close_map,
                                high_map, low_map, L, N, extreme)
        if drops_ref is not None:
            assert dr == drops_ref[leg], (f"F2 {leg}: event-side drops {dr} "
                                          f"!= engine drops {drops_ref[leg]}")
        full = null_up if leg == "UP" else null_dn
        fam[leg] = f2_leg(sel, full, rng)
    run_holm(fam, LEGS)
    for leg in LEGS:
        fam[leg]["verdict"] = verdict_f2(leg, fam[leg])
    return fam


def verdict_f1(leg: str, r: dict) -> str:
    """Directional F1 verdicts (pre-reg #11 sec 4)."""
    if int(r["n"]) < MISSING_PASS:
        return (f"INCONCLUSIVE (<{MISSING_PASS} OOS events; n={r['n']})")
    if leg == "UP":
        if r["holm_rejected"] and r["ci_upper"] < 0.0:
            return (f"EDGE (Holm-rejected; excess CI-upper {r['ci_upper']:+.4f}"
                    " < 0 — big up-moves below both baselines, correction as "
                    "claimed)")
        if r["holm_rejected"] and r["ci_low"] > 0.0:
            return (f"FADE (Holm-rejected; excess CI-low {r['ci_low']:+.4f} "
                    "> 0 — big up-moves beat the baselines, claim "
                    "contradicted)")
    else:  # DOWN
        if r["holm_rejected"] and r["ci_low"] > 0.0:
            return (f"EDGE (Holm-rejected; excess CI-low {r['ci_low']:+.4f} "
                    "> 0 — big down-moves above both baselines, recovery as "
                    "claimed)")
        if r["holm_rejected"] and r["ci_upper"] < 0.0:
            return (f"FADE (Holm-rejected; excess CI-upper {r['ci_upper']:+.4f}"
                    " < 0 — big down-moves lose to the baselines, claim "
                    "contradicted)")
    return (f"NO EDGE (p_input {r['p']:.3f}; est {r['est']:+.4f}; CI-low "
            f"{r['ci_low']:+.4f}..CI-upper {r['ci_upper']:+.4f})")


def verdict_f2(leg: str, r: dict) -> str:
    """Retracement-claim verdicts (pre-reg #11 sec 4)."""
    if int(r["n_events"]) < MISSING_PASS:
        return (f"INCONCLUSIVE (<{MISSING_PASS} OOS events; "
                f"n={r['n_events']})")
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return (f"EDGE (Holm-rejected; contrast CI-low {r['ci_low']:+.4f} "
                f"> 0 — big {leg.lower()} moves retrace half within N more "
                "often than typical bars, corrected as claimed)")
    if r["holm_rejected"] and r["ci_upper"] < 0.0:
        return (f"FADE (Holm-rejected; contrast CI-upper {r['ci_upper']:+.4f}"
                f" < 0 — big {leg.lower()} moves retrace half within N less "
                "often than typical bars, claim contradicted)")
    return (f"NO EDGE (contrast est {r['est']:+.4f}, p {r['p']:.3f})")


def freq_measure(det: pd.DataFrame, det_state: pd.DataFrame) -> dict:
    """Frequency (measurement, not a verdict family): OOS event counts per
    leg (excursion-firsts, warm-up excluded) and the OOS qualifying-bar
    counts per leg (state-level, pre-collapse) — the runs-collapse view."""
    e = det[~det["warmup"]]
    s = det_state[~det_state["warmup"]]
    oos_e = e[e["signal_date"] >= ERA_OOS]
    oos_s = s[s["signal_date"] >= ERA_OOS]
    return {"n_oos_events": {leg: int((oos_e["shape"] == leg).sum())
                             for leg in LEGS},
            "n_oos_qualifying_bars": {leg: int((oos_s["shape"] == leg).sum())
                                      for leg in LEGS},
            "n_warmup_events": {leg: int(
                ((det["shape"] == leg) & det["warmup"]).sum())
                for leg in LEGS}}


def main() -> int:
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()

    # ---- per-ticker bars (full OHLCV read directly from the frozen
    # parquets — ATR needs High/Low and close_{t-1}; same frozen Close
    # column as the engine's load_bars)
    close_map, high_map, low_map, tr_map = {}, {}, {}, {}
    atr14 = {}
    atr_min_all = np.inf
    for t in universe:
        if not (BARS_DIR / f"{t}.parquet").exists():
            continue  # universe rows without bars (build_pools convention)
        df = pd.read_parquet(BARS_DIR / f"{t}.parquet")
        high_map[t] = df["High"]
        low_map[t] = df["Low"]
        close_map[t] = df["Close"]
        tr_map[t] = tr_series(df)
        atr14[t] = atr_simple(tr_map[t], ATR_PERIOD_PRIMARY)
        v = atr14[t].to_numpy(dtype=np.float64)
        valid = ~np.isnan(v)
        if valid.any():
            atr_min_all = min(atr_min_all, float(v[valid].min()))

    det, stats = bigmove_det(close_map, atr14, L_PRIMARY, TAU_PRIMARY)
    det_state, _ = bigmove_det(close_map, atr14, L_PRIMARY, TAU_PRIMARY,
                               state_level=True)
    n_warmup_ev = int(det["warmup"].sum())
    n_warmup_st = int(det_state["warmup"].sum())

    # ---- structural checks (pre-reg #11 sec 3) ----
    assert atr_min_all >= -1e-9, (f"ATR < 0: min {atr_min_all:.12f} (TR >= 0 "
                                  "by construction — expected 0)")
    assert stats["min_signal"] >= L_PRIMARY, (
        f"event with t - L < 0: min signal bar {stats['min_signal']} < "
        f"{L_PRIMARY} (expected 0)")
    assert stats["n_bad_signal"] == 0, (
        f"{stats['n_bad_signal']} events whose signal bar lies beyond the "
        "ticker's series (expected 0)")

    # ---- primary measurement ----
    rng = np.random.default_rng(SEED)
    pools = pools_of(build_pools(N_PRIMARY, universe))

    camp = det[~det["warmup"]].copy()
    rows_p, drops_p = measure_legs(camp, N_PRIMARY)

    fam1 = {leg: f1_leg(rows_p[leg], pools, rng) for leg in LEGS}
    run_holm(fam1, LEGS)
    for leg in LEGS:
        fam1[leg]["verdict"] = verdict_f1(leg, fam1[leg])

    null_up, null_dn = null_arrays(close_map, high_map, low_map,
                                   L_PRIMARY, N_PRIMARY)
    fam2 = f2_family(camp, close_map, high_map, low_map, L_PRIMARY,
                     N_PRIMARY, null_up, null_dn, rng, drops_ref=drops_p)

    freq = freq_measure(det, det_state)

    # ---- sensitivities (pre-declared, NO verdicts) ----
    sens = {}

    # S1: horizons N = 1 / 5 / 20 (F1, baselines rebuilt per horizon —
    # era- AND horizon-matched N-bar window pools, the pre-reg #9 S1 fix);
    # the retracement metric reported at N = 5 (the claim's 5-10 range).
    sens["horizons"] = {}
    for n in SENS_N:
        rows_n, drops_n = measure_legs(camp, n)
        pools_n = pools_of(build_pools(n, universe))
        cell = {"drops": drops_n,
                "f1": {leg: f1_leg(rows_n[leg], pools_n, rng)
                       for leg in LEGS}}
        if n == 5:
            nu, nd = null_arrays(close_map, high_map, low_map, L_PRIMARY, n)
            cell["f2"] = {leg: f2_leg(
                event_retrace(camp[camp["shape"] == leg], close_map,
                              high_map, low_map, L_PRIMARY, n)[0],
                nu if leg == "UP" else nd, rng) for leg in LEGS}
        sens["horizons"][f"N={n}"] = cell

    # S2: threshold tau = 2 / 5 (F1 + F2, L = 10; the null is direction-only,
    # unchanged)
    sens["tau"] = {}
    for tau in SENS_TAU:
        det_t, _ = bigmove_det(close_map, atr14, L_PRIMARY, tau)
        camp_t = det_t[~det_t["warmup"]].copy()
        rows_t, drops_t = measure_legs(camp_t, N_PRIMARY)
        sens["tau"][f"tau={tau:g}"] = {
            "drops": drops_t,
            "f1": {leg: f1_leg(rows_t[leg], pools, rng) for leg in LEGS},
            "f2": f2_family(camp_t, close_map, high_map, low_map, L_PRIMARY,
                            N_PRIMARY, null_up, null_dn, rng,
                            drops_ref=drops_t)}

    # S3: move window L = 5 (F1 + F2, tau = 3; null recomputed at L = 5)
    det_l5, _ = bigmove_det(close_map, atr14, L_SENS, TAU_PRIMARY)
    camp_l5 = det_l5[~det_l5["warmup"]].copy()
    rows_l5, drops_l5 = measure_legs(camp_l5, N_PRIMARY)
    nu5, nd5 = null_arrays(close_map, high_map, low_map, L_SENS, N_PRIMARY)
    sens["L5"] = {
        "drops": drops_l5,
        "f1": {leg: f1_leg(rows_l5[leg], pools, rng) for leg in LEGS},
        "f2": f2_family(camp_l5, close_map, high_map, low_map, L_SENS,
                        N_PRIMARY, nu5, nd5, rng, drops_ref=drops_l5)}

    # S4: ATR period 7 (simple) and Wilder's smoothing (F1 only)
    atr7 = {t: atr_simple(tr_map[t], ATR_PERIOD_SENS) for t in close_map}
    det_a7, _ = bigmove_det(close_map, atr7, L_PRIMARY, TAU_PRIMARY)
    rows_a7, drops_a7 = measure_legs(det_a7[~det_a7["warmup"]].copy(),
                                     N_PRIMARY)
    sens["atr_period7"] = {
        "drops": drops_a7,
        "f1": {leg: f1_leg(rows_a7[leg], pools, rng) for leg in LEGS}}

    atr_w = {t: atr_wilder(tr_map[t], ATR_PERIOD_PRIMARY) for t in close_map}
    det_aw, _ = bigmove_det(close_map, atr_w, L_PRIMARY, TAU_PRIMARY)
    rows_aw, drops_aw = measure_legs(det_aw[~det_aw["warmup"]].copy(),
                                     N_PRIMARY)
    sens["atr_wilder"] = {
        "drops": drops_aw,
        "f1": {leg: f1_leg(rows_aw[leg], pools, rng) for leg in LEGS}}

    # S5: state-level view — every qualifying bar is an event
    # (overlap-inflated by construction; the pre-reg #9 S4 lesson —
    # reported for contrast, not as evidence)
    rows_st, drops_st = measure_legs(det_state[~det_state["warmup"]].copy(),
                                     N_PRIMARY)
    sens["state_level"] = {
        "drops": drops_st,
        "f1": {leg: f1_leg(rows_st[leg], pools, rng) for leg in LEGS}}

    # S6: per-year F1 leg mean returns (OOS)
    oos_p = pd.concat([rows_p[leg] for leg in LEGS], ignore_index=True)
    py = oos_p.groupby([oos_p["signal_date"].str[:4], "shape"])["ret"].agg(
        ["mean", "count"])
    sens["per_year"] = {
        str(y): {leg: {"mean_ret": float(py.loc[(y, leg), "mean"]),
                       "n": int(py.loc[(y, leg), "count"])}
                 for leg in LEGS if (y, leg) in py.index}
        for y in sorted(set(i[0] for i in py.index))}

    # S7: IS record (descriptive — selection era)
    sens["is_record"] = {}
    for leg in LEGS:
        is_rows = rows_p[leg][~rows_p[leg]["is_oos"]]
        sens["is_record"][leg] = {
            "n": int(len(is_rows)),
            "mean_ret": float(is_rows["ret"].mean()) if len(is_rows) else None,
            "win_rate": float((is_rows["ret"] > 0).mean())
            if len(is_rows) else None}

    # S8: retracement vs the move window's extreme (UP: midpoint of
    # close_{t-L} and the window's max high; DOWN: midpoint of close_{t-L}
    # and the window's min low) — F2, events and random bars alike
    nu_x, nd_x = null_arrays(close_map, high_map, low_map, L_PRIMARY,
                             N_PRIMARY, extreme=True)
    fam_x = f2_family(camp, close_map, high_map, low_map, L_PRIMARY,
                      N_PRIMARY, nu_x, nd_x, rng, extreme=True,
                      drops_ref=drops_p)
    sens["extreme_midpoint"] = {"f2": fam_x}

    out = {
        "pre_reg": "#11",
        "claim": ("'We know that almost all of the big moves will eventually "
                  "be corrected'; 'what goes up must come down and what goes "
                  "down must come back up' (Warrior Trading, jfe1Zl-5EQI "
                  "[16:01-16:09], [15:05-15:09]). Measured: big-move event "
                  "at bar t iff |close_t - close_{t-L}| >= 3 * ATR_t "
                  "(ATR = simple mean of the 14 true ranges ending at t, "
                  "pre-registered — no ATR teaching in the corpus), L = 10 "
                  "primary, excursion-first event resolution, UP leg iff "
                  "close_t > close_{t-L} (claims correction), DOWN leg iff "
                  "close_t < close_{t-L} (claims recovery), on US equity "
                  "daily bars (intraday->daily translation, pre-declared)"),
        "params": {"move_window_L": L_PRIMARY, "atr_tau": TAU_PRIMARY,
                   "atr_period": ATR_PERIOD_PRIMARY,
                   "atr_period_sensitivity": ATR_PERIOD_SENS,
                   "n": N_PRIMARY, "n_sensitivities": SENS_N,
                   "tau_sensitivities": list(SENS_TAU),
                   "l_sensitivity": L_SENS, "cost": COST, "b": B,
                   "seed": SEED, "alpha": ALPHA,
                   "era_oos_start": ERA_OOS, "count_floor": MISSING_PASS,
                   "warmup_guard": WARMUP,
                   "warmup_excluded_events": n_warmup_ev,
                   "warmup_excluded_state_bars": n_warmup_st,
                   "engine_sha256": "c7421fbf (frozen Phase-3 engine, "
                                    "imported)"},
        "families": {"f1_absolute": fam1, "f2_retracement": fam2},
        "frequency": freq,
        "sensitivities": sens,
        "assertions": {"atr_min_all": atr_min_all,
                       "min_signal": stats["min_signal"],
                       "max_signal": stats["max_signal"],
                       "n_bad_signal": stats["n_bad_signal"],
                       "drops_primary": drops_p,
                       "n_oos_events_primary": {leg: int(
                           (camp["shape"] == leg).sum()) for leg in LEGS}},
        "fingerprints": {
            "universe_sha256": sha(UNIVERSE_CSV),
            "measure_code_sha256": sha(Path(__file__)),
            "engine_sha256": sha(Path(measure.__file__)),
            "divergence_code_sha256": sha(
                Path(__file__).parent / "measure_divergence.py"),
        },
    }
    RESULTS.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {RESULTS.name}")

    # ---- report ----
    L = []
    L.append("# Big-move mean-reversion measurement report (pre-registration "
             "#11)")
    L.append("")
    L.append("- Pre-registration #11 (frozen 2026-08-14): claim = 'almost all "
             "of the big moves will eventually be corrected'; 'what goes up "
             "must come down and what goes down must come back up' "
             "(I-F-01, jfe1Zl-5EQI [16:01-16:09], [15:05-15:09]). Big-move "
             f"event at bar t iff |close_t - close_{{t-L}}| >= {TAU_PRIMARY:g} "
             f"x ATR_t, L = {L_PRIMARY} primary, ATR = simple mean of the "
             f"{ATR_PERIOD_PRIMARY} true ranges ending at t (pre-registered — "
             "no ATR teaching in the corpus); UP leg iff close_t > "
             "close_{t-L}, DOWN leg iff close_t < close_{t-L}; event = the "
             "first bar of each leg excursion (the pre-reg #9 S4 rule). "
             f"Signal at close t, entry open t+1, exit close t+{N_PRIMARY} "
             f"(-cost {COST}); bootstrap {B} (seed {SEED}); alpha {ALPHA}; "
             "Holm within each family; count floor 100 OOS events per leg.")
    L.append("- Warm-up guard signal-bar index < 60 (frozen #3 convention — "
             f"bounds the {L_PRIMARY}-bar move window and the "
             f"{ATR_PERIOD_PRIMARY}-bar ATR lookback with margin): "
             f"{n_warmup_ev} warm-up events and {n_warmup_st} warm-up "
             "qualifying bars excluded and counted.")
    L.append("- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date). "
             "Intraday->daily translation pre-declared: the regularity is "
             "stated in a 2015 intraday-trading classroom; measured on US "
             "equity daily bars (the frozen S&P 600 universe). Only the "
             "regularity is measured — the reversal strategy is process "
             "content, not a claim.")
    L.append(f"- Events (L={L_PRIMARY}, tau={TAU_PRIMARY:g}, warm-up "
             "excluded): UP n=%d, DOWN n=%d (drops at series end: %s); "
             "state-level qualifying bars (S5 contrast): UP n=%d, DOWN n=%d"
             % (len(rows_p["UP"]), len(rows_p["DOWN"]), json.dumps(drops_p),
                len(rows_st["UP"]), len(rows_st["DOWN"])))
    L.append("- F1 (absolute, directional per leg): OOS mean forward return "
             "vs era-matched random entries AND same-ticker (SPY reported), "
             "p_input = max, Holm across UP/DOWN. UP: EDGE iff Holm-rejected "
             "AND CI-upper < 0 (correction, as claimed); FADE iff CI-low > 0. "
             "DOWN: EDGE iff Holm-rejected AND CI-low > 0 (recovery, as "
             "claimed); FADE iff CI-upper < 0. F2 (retracement claim test): "
             "the leg's share of events with close_{t+N} past the move's "
             "midpoint within N=10 ('corrected half') minus the same share "
             "on era-matched random bars (each random bar's own trailing "
             f"{L_PRIMARY}-bar move, direction-matched to the leg), Holm "
             "across UP/DOWN — the calibrated null, not an assumed 0.5.")
    L.append("- Phase-5 trigger (pre-reg #11 sec 4): ONLY an F1-DOWN EDGE "
             "can trigger the trigger-check conversation (F1-UP EDGE is a "
             "negative-return finding; F2 is a differential finding).")
    L.append("")
    L.append("## Verdicts — Family 1: absolute (directional per leg)")
    L.append("")
    for leg in LEGS:
        r = fam1[leg]
        e_rand, e_same, e_spy = (r["excess"]["random_entries"],
                                 r["excess"]["same_ticker"],
                                 r["excess"]["spy"])
        L.append(f"- F1-{leg}: n={r['n']} | mean_ret {fmt_num(r['mean_ret'])} "
                 f"| win_rate {fmt_num(r['win_rate'], '.4f')} | excess vs "
                 f"random {e_rand[0]:+.4f} (CI {e_rand[2]:+.4f}.."
                 f"{e_rand[3]:+.4f}, p {e_rand[4]:.3f}) | vs same "
                 f"{e_same[0]:+.4f} (CI {e_same[2]:+.4f}..{e_same[3]:+.4f}, "
                 f"p {e_same[4]:.3f}) | vs spy {e_spy[0]:+.4f} "
                 f"(p {e_spy[4]:.3f}) | p_input {r['p']:.3f} | est "
                 f"{r['est']:+.4f} (CI-low {r['ci_low']:+.4f}..CI-upper "
                 f"{r['ci_upper']:+.4f}) | Holm gate {r['holm_gate']:.4f} -> "
                 f"**{r['verdict']}**")
    L.append("")
    L.append("## Verdicts — Family 2: retracement claim test (corrected-half "
             "within N=10 vs era-matched random bars)")
    L.append("")
    for leg in LEGS:
        r = fam2[leg]
        L.append(f"- F2-{leg}: n_events={r['n_events']:,} | n_random="
                 f"{r['n_random']:,} | events retrace-half "
                 f"{fmt_num(r['rate_events'], '.4f')} | random retrace-half "
                 f"{fmt_num(r['rate_random'], '.4f')} | contrast "
                 f"{fmt_num(r['est'])} (CI {fmt_num(r['ci_low'])}.."
                 f"{fmt_num(r['ci_upper'])}, p {r['p']:.3f}) | Holm gate "
                 f"{r['holm_gate']:.4f} -> **{r['verdict']}**")
    L.append("")
    L.append("## Frequency (measurement, not a verdict family)")
    L.append("")
    L.append(f"- OOS events (excursion-firsts): UP {freq['n_oos_events']['UP']:,}"
             f" / DOWN {freq['n_oos_events']['DOWN']:,}; OOS qualifying bars "
             f"(pre-collapse): UP {freq['n_oos_qualifying_bars']['UP']:,} / "
             f"DOWN {freq['n_oos_qualifying_bars']['DOWN']:,} — the runs "
             "collapse view (typical runs span several qualifying bars).")
    L.append("")
    L.append("## Sensitivities (exploratory — NO verdicts)")
    L.append("")
    L.append("### S1: horizons N = 1 / 5 / 20")
    L.append("")
    L.append("*Baselines rebuilt per horizon (era- AND horizon-matched "
             "N-bar window pools); the retracement metric reported at N = 5 "
             "(the claim's '5-10 sessions' range).*")
    L.append("")
    for n in SENS_N:
        cell = sens["horizons"][f"N={n}"]
        L.append(f"**N={n}** (drops {json.dumps(cell['drops'])}):")
        for leg in LEGS:
            r = cell["f1"][leg]
            e_r, e_s = (r["excess"]["random_entries"],
                        r["excess"]["same_ticker"])
            L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} "
                     f"| win {fmt_num(r['win_rate'], '.4f')} | vs random "
                     f"{e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same {e_s[0]:+.4f} "
                     f"(p {e_s[4]:.3f})")
        if n == 5:
            for leg in LEGS:
                r = cell["f2"][leg]
                L.append(f"- F2-{leg} (N=5): events "
                         f"{fmt_num(r['rate_events'], '.4f')} vs random "
                         f"{fmt_num(r['rate_random'], '.4f')} — contrast "
                         f"{fmt_num(r['est'])} (p {r['p']:.3f})")
        L.append("")
    L.append("### S2: threshold tau = 2 / 5 (L = 10)")
    L.append("")
    for tau in SENS_TAU:
        cell = sens["tau"][f"tau={tau:g}"]
        L.append(f"**tau={tau:g}** (drops {json.dumps(cell['drops'])}):")
        for leg in LEGS:
            r = cell["f1"][leg]
            e_r, e_s = (r["excess"]["random_entries"],
                        r["excess"]["same_ticker"])
            L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} "
                     f"| vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                     f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
        for leg in LEGS:
            r = cell["f2"][leg]
            L.append(f"- F2-{leg}: events {fmt_num(r['rate_events'], '.4f')} "
                     f"vs random {fmt_num(r['rate_random'], '.4f')} — "
                     f"contrast {fmt_num(r['est'])} (CI {fmt_num(r['ci_low'])}"
                     f"..{fmt_num(r['ci_upper'])}, p {r['p']:.3f})")
        L.append("")
    L.append("### S3: move window L = 5 (tau = 3)")
    L.append("")
    cell = sens["L5"]
    L.append(f"Drops {json.dumps(cell['drops'])}:")
    for leg in LEGS:
        r = cell["f1"][leg]
        e_r, e_s = (r["excess"]["random_entries"],
                    r["excess"]["same_ticker"])
        L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} | "
                 f"vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                 f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
    for leg in LEGS:
        r = cell["f2"][leg]
        L.append(f"- F2-{leg}: events {fmt_num(r['rate_events'], '.4f')} vs "
                 f"random {fmt_num(r['rate_random'], '.4f')} — contrast "
                 f"{fmt_num(r['est'])} (p {r['p']:.3f})")
    L.append("")
    L.append("### S4: ATR period 7 (simple) and Wilder's smoothing "
             "(L = 10, tau = 3)")
    L.append("")
    for key, cell in (("atr_period7", sens["atr_period7"]),
                      ("atr_wilder", sens["atr_wilder"])):
        L.append(f"**{key}** (drops {json.dumps(cell['drops'])}):")
        for leg in LEGS:
            r = cell["f1"][leg]
            e_r, e_s = (r["excess"]["random_entries"],
                        r["excess"]["same_ticker"])
            L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} "
                     f"| vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                     f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
        L.append("")
    L.append("### S5: state-level view (every qualifying bar is an event)")
    L.append("")
    L.append("*Overlap-inflated by construction — the pre-reg #9 S4 lesson; "
             "reported for contrast, not as evidence.*")
    L.append("")
    cell = sens["state_level"]
    L.append(f"Drops {json.dumps(cell['drops'])}:")
    for leg in LEGS:
        r = cell["f1"][leg]
        e_r, e_s = (r["excess"]["random_entries"],
                    r["excess"]["same_ticker"])
        L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} | "
                 f"vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                 f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
    L.append("")
    L.append("### S6: per-year F1 leg mean returns (OOS)")
    L.append("")
    L.append("| year | UP | DOWN |")
    L.append("|---|---|---|")
    for y in sorted(sens["per_year"]):
        cells = []
        for leg in LEGS:
            r = sens["per_year"][y].get(leg)
            cells.append(f"{r['mean_ret']:+.4f} (n={r['n']})" if r else "—")
        L.append(f"| {y} | " + " | ".join(cells) + " |")
    L.append("")
    L.append("### S7: IS record (descriptive — selection era)")
    L.append("")
    L.append("| leg | n | mean_ret | win_rate |")
    L.append("|---|---|---|---|")
    for leg in LEGS:
        r = sens["is_record"][leg]
        L.append(f"| {leg} | {r['n']} | {fmt_num(r['mean_ret'])} | "
                 f"{fmt_num(r['win_rate'], '.4f')} |")
    L.append("")
    L.append("### S8: retracement vs the move window's extreme (S8 midpoint)")
    L.append("")
    L.append("*UP: midpoint of close_{t-L} and the window's max high; DOWN: "
             "midpoint of close_{t-L} and the window's min low — instead of "
             "the close-to-close midpoint, events and random bars alike.*")
    L.append("")
    for leg in LEGS:
        r = sens["extreme_midpoint"]["f2"][leg]
        L.append(f"- F2-{leg}: events {fmt_num(r['rate_events'], '.4f')} vs "
                 f"random {fmt_num(r['rate_random'], '.4f')} — contrast "
                 f"{fmt_num(r['est'])} (CI {fmt_num(r['ci_low'])}.."
                 f"{fmt_num(r['ci_upper'])}, p {r['p']:.3f})")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_bigmove.py` regenerates this "
             "report; the seed is fixed, so results are stable across runs.")
    L.append(f"Assertions: ATR >= 0 everywhere (min {atr_min_all:.12f}; "
             "PASS); no event with t - L < 0 (min signal bar "
             f"{stats['min_signal']} >= {L_PRIMARY}; PASS); no event whose "
             "signal bar lies beyond the ticker's series (PASS); F2 event-"
             "side drops equal the engine's drops per leg (PASS); no leg "
             "ticker missing an OOS window pool (PASS).")
    L.append("Input fingerprints: universe %s…, measure code %s… (Phase-3 "
             "engine c7421fbf… imported unchanged; generic helpers from "
             "measure_divergence %s…)."
             % (out["fingerprints"]["universe_sha256"][:12],
                out["fingerprints"]["measure_code_sha256"][:12],
                out["fingerprints"]["divergence_code_sha256"][:12]))
    L.append("Any change to the detector, data, or measurement code changes "
             "the frozen inputs and requires a new pre-registration before "
             "it can drive a verdict.")
    L.append("")
    REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
