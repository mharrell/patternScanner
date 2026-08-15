"""RSI divergence measurement for pre-registration #10 (ledger I-X-02/03/04),
frozen 2026-08-14.

The claims (Trading 212, rgVdgR1y1Dg):
  I-X-03 [05:51-06:15]  Bullish divergence: price lower low + RSI higher low
                        => "weakness running out of steam" => bounce.
  I-X-04 [06:39-07:03]  Bearish divergence: price higher high + RSI lower
                        high => "strength running out of steam" => pullback.
  I-X-02 [05:33-05:39]  "...a lot less common so arguably a bit more reliable"
                        (vs the 70/30 overbought/oversold signals themselves,
                        per [04:44-04:58]).

Definitions (frozen, pre-reg #10 sec 1):
  RSI: the same simple-average (Cutler) formula as pre-reg #9 (the video's
  own formula), period 10 PRIMARY (the demo charts' "daily chart again ten
  day RSI" [06:25]); period 14 kept as a sensitivity.
  Swings: strict k=2 fractals on Low (bull) / High (bear): the bar's low is
  strictly below the k bars on each side (ties never form a swing). Events
  use CONSECUTIVE swing pairs with disjoint fractal windows (t2 - t1 >= 5).
  Bullish divergence event: low_t2 < low_t1 AND RSI_t2 > RSI_t1.
  Bearish divergence event: high_t2 > high_t1 AND RSI_t2 < RSI_t1.
  TIMING (strict no-look-ahead): a k-fractal at t2 is only knowable at close
  t2+k, so the SIGNAL BAR is the confirmation bar t2+k; entry open t2+k+1,
  exit close t2+k+N. The chartist's-eye variant (signal at the pivot bar t2,
  entry open t2+1) is sensitivity S8 with its pre-declared selection-tilt
  caveat — not the primary.
  Crossings (the I-X-02 comparison baseline): first bar of each excursion
  above 70 / below 30 (the pre-reg #9 S4 rule), same period.

Protocol (pre-reg #10 sec 3-4): N = 10 primary, COST = 0.0015 round-trip,
bootstrap B = 1000 seed 20260813, era split by signal date (IS 2000-2015 /
OOS 2016-2025), warm-up guard signal-bar index < 60, Holm-Bonferroni at
alpha = 0.05 within each family, count floor 100 OOS events per leg.

F1 (absolute, directional per leg): OOS mean forward return of the leg vs
the era-matched baselines (random entries -COST, same-ticker -COST, SPY raw).
Convention as #6/#7/#8/#9: p_input = max(p_rand, p_same), est = max,
ci_low = min, ci_upper = min. Holm across the two legs (BULL, BEAR).
  BULL: EDGE iff Holm-rejected AND excess CI-low > 0 (bounce, as claimed);
        FADE iff Holm-rejected AND CI-upper < 0.
  BEAR: EDGE iff Holm-rejected AND excess CI-upper < 0 (pullback, as
        claimed); FADE iff Holm-rejected AND CI-low > 0.

F2 (reliability contrast, I-X-02): per leg, per metric, the two-sample
bootstrap contrast divergence - 70/30 crossings at the same period
(oversold crossings vs BULL; overbought crossings vs BEAR), on (a) mean
forward return and (b) directional hit rate (share of events with ret > 0
after cost). Holm across the four tests (2 legs x 2 metrics).
  BULL-mean / BULL-hit: EDGE iff CI-low > 0; FADE iff CI-upper < 0.
  BEAR-mean / BEAR-hit: EDGE iff CI-upper < 0; FADE iff CI-low > 0.

Frequency (I-X-02 first half): OOS event counts (divergence vs crossings at
the same period) + ratio + ticker-cluster bootstrap CI on the ratio
(CI-upper < 1 => "less common" confirmed). A measurement, not a verdict
family. Reported at period 10 (primary) and 14 (S3).

Sensitivities (pre-declared, NO verdicts): S1 N = 1/5/20 (F1 + F2, baselines
rebuilt per horizon); S2 swing scale k = 3/5 (F1 + F2); S3 period 14 (F1 +
F2, crossings recomputed at 14; frequency at 14); S4 min separation >= 10
(F1 + F2); S5 per-year F1 mean returns (OOS); S6 IS record (F1 table,
descriptive); S7 extreme-gated divergence (first swing's RSI beyond 70/30);
S8 chartist's-eye timing (signal at the pivot bar, entry open t2+1 — with
its selection-tilt caveat).

Structural checks (pre-reg #10 sec 3): (a) RSI values within [0, 100]
everywhere; (b) no event with t1 < period (first swing's RSI undefined) —
expected 0; (c) no event whose fractal lacks its confirmation bars — expected
0; (d) no signal bar < 60 after the warm-up guard — expected 0.

Engine pieces import from measure.py (frozen, sha c7421fbf...): forward
returns run through the engine's measure_returns unchanged. Its dropped
dict is keyed on shape labels A/B/C (frozen engine), so the BULL/BEAR legs
pass with placeholder shapes (BULL -> "A", BEAR -> "B") and the crossing
frame passes as "C"; rows are relabeled after measurement and the
mislabeled dropped counts are read back from the placeholder keys, per leg
(the pre-reg #9 convention). The same-ticker baseline uses the leg's own
empirical ticker distribution (vectorized, the RV #8 convention — draws are
distributionally identical to the per-draw loops, deterministic via seed).
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import (COST, B, SEED, ALPHA, ERA_OOS, UNIVERSE_CSV, BARS_DIR,
                     bootstrap_excess, measure_returns)
import measure
from measure_pillars import build_pools
from measure_veto import two_sample_excess

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
RESULTS = CACHE / "divergence_measure_results.json"
REPORT = CACHE / "divergence_measure_report.md"

PERIOD_PRIMARY = 10                      # pre-reg #10 sec 1: the demo charts'
PERIOD_SENS = 14                         #   "ten day RSI" is the primary
OB_HI = 70.0
OS_LO = 30.0
K_PRIMARY = 2                            # strict fractal half-width
K_SENS = [3, 5]                          # pre-reg #10 sec 6 S2
MIN_SEP_PRIMARY = 5                      # disjoint fractal windows
MIN_SEP_SENS = 10                        # pre-reg #10 sec 6 S4
CONFIRM = K_PRIMARY                      # signal bar = t2 + k (no look-ahead)
N_PRIMARY = 10
SENS_N = [1, 5, 20]                      # pre-reg #10 sec 6 S1
WARMUP = 60                              # frozen #3 convention
MISSING_PASS = 100                       # count floor per leg
LEGS = ("BULL", "BEAR")
LEG_PLACEHOLDER = {"BULL": "A", "BEAR": "B"}   # measure_returns' dropped
                                               # dict is keyed A/B/C (frozen
                                               # engine); legs relabeled after
CROSS_LEGS = ("OB", "OS")
F2_TESTS = (("BULL", "mean"), ("BULL", "hit"), ("BEAR", "mean"), ("BEAR", "hit"))


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def rsi_series(close: pd.Series, period: int) -> pd.Series:
    """Simple-average (Cutler) RSI — the frozen pre-reg #9 formula, unchanged.

    RSI at bar t uses the `period` daily changes ending at t (closes
    t-period..t). avg_loss = 0 -> 100 (all-gain and flat); avg_gain = 0 and
    avg_loss > 0 -> 0. NaN before `period` prior closes exist.
    """
    d = close.diff()
    gains = d.clip(lower=0.0)
    losses = (-d).clip(lower=0.0)
    # window = the `period` changes ENDING at t (deltas t-period+1..t,
    # INCLUDING the change at t); first valid at bar index `period`
    g = gains.rolling(period).mean()
    l = losses.rolling(period).mean()
    with np.errstate(divide="ignore", invalid="ignore"):
        rsi = np.where(l == 0, 100.0, np.where(g == 0, 0.0,
                                               100.0 - 100.0 / (1.0 + g / l)))
    return pd.Series(rsi, index=close.index)


def swing_idx(v: np.ndarray, k: int, low: bool) -> np.ndarray:
    """Strict k-fractal indices: bar i is a swing iff v[i] is strictly
    below (low) / above (high) the k bars on each side. Ties never form a
    swing. Returns the qualifying bar indices (positions k..n-k-1)."""
    n = len(v)
    if n < 2 * k + 1:
        return np.empty(0, dtype=np.int64)
    i = np.arange(k, n - k)
    m = v[i]
    nbrs = [v[i - j] for j in range(1, k + 1)] + [v[i + j] for j in range(1, k + 1)]
    if low:
        return i[(m < np.minimum.reduce(nbrs))]
    return i[(m > np.maximum.reduce(nbrs))]


def _pair_events(sw: np.ndarray, price: pd.Series, rsi: pd.Series,
                 t_off: int, min_sep: int, gain_ok: bool, extreme: float):
    """Events from consecutive swing pairs: price + RSI conditions.

    sw: swing bar indices (ascending); price: Low (bull) or High (bear);
    gain_ok=True (bull): price_t2 < price_t1 AND RSI_t2 > RSI_t1;
    gain_ok=False (bear): price_t2 > price_t1 AND RSI_t2 < RSI_t1.
    Returns (event_bar, t1, t2) arrays for qualifying pairs.
    """
    if len(sw) < 2:
        return np.empty(0, dtype=np.int64), np.empty(0, dtype=np.int64), \
            np.empty(0, dtype=np.int64)
    t1 = sw[:-1]
    t2 = sw[1:]
    sep_ok = (t2 - t1) >= min_sep
    p1 = price.iloc[t1].to_numpy(dtype=np.float64)
    p2 = price.iloc[t2].to_numpy(dtype=np.float64)
    r1 = rsi.iloc[t1].to_numpy(dtype=np.float64)
    r2 = rsi.iloc[t2].to_numpy(dtype=np.float64)
    if gain_ok:
        cond = sep_ok & (p2 < p1) & (r2 > r1) & np.isfinite(r1) & np.isfinite(r2)
        if extreme is not None:
            cond &= r1 < extreme          # S7: first swing RSI < 30
    else:
        cond = sep_ok & (p2 > p1) & (r2 < r1) & np.isfinite(r1) & np.isfinite(r2)
        if extreme is not None:
            cond &= r1 > extreme          # S7: first swing RSI > 70
    t1_e, t2_e = t1[cond], t2[cond]
    return t2_e + t_off, t1_e, t2_e       # t_off = signal bar lag (k, or 0 for S8)


def div_frame(low_map: dict, high_map: dict, rsi_map: dict, k: int,
              min_sep: int, confirm: int, extreme: float = None):
    """Divergence event detections across the universe.

    Signal bar = t2 + confirm (the fractal confirmation bar; confirm = k
    primary, 0 in the S8 chartist's-eye variant). Returns (det, stats)
    with stats = {min_t1, min_signal, max_signal, n_bad_signal} over the
    events (n_bad_signal = events whose signal bar lies beyond the ticker's
    own series — the structural check (c), expected 0).
    """
    rows = []
    min_t1, min_sig, max_sig, n_bad = np.inf, np.inf, -np.inf, 0
    for t in rsi_map:
        low = low_map[t].to_numpy(dtype=np.float64)
        high = high_map[t].to_numpy(dtype=np.float64)
        rsi = rsi_map[t]
        dates = rsi.index
        n_bars = len(dates)
        sw_l = swing_idx(low, k, True)
        sw_h = swing_idx(high, k, False)
        for sw, gain_ok, leg, pr in ((sw_l, True, "BULL", low_map[t]),
                                     (sw_h, False, "BEAR", high_map[t])):
            ev_bars, t1s, t2s = _pair_events(sw, pr, rsi, confirm, min_sep,
                                             gain_ok, extreme)
            if not len(ev_bars):
                continue
            min_t1 = min(min_t1, int(t1s.min()))
            min_sig = min(min_sig, int(ev_bars.min()))
            max_sig = max(max_sig, int(ev_bars.max()))
            n_bad += int((ev_bars >= n_bars).sum())
            rows += [(t, str(dates[i].date()), leg, int(i))
                     for i in ev_bars]
    det = pd.DataFrame(rows, columns=["ticker", "signal_date", "shape",
                                      "bar_index"])
    det["warmup"] = det["bar_index"] < WARMUP
    stats = {"min_t1": min_t1, "min_signal": min_sig, "max_signal": max_sig,
             "n_bad_signal": n_bad}
    return det, stats


def cross_frame(rsi_map: dict, ob_hi: float, os_lo: float) -> pd.DataFrame:
    """70/30 crossing events (pre-reg #9 S4 rule): the first bar of each
    excursion above ob_hi / below os_lo, until re-entry. The I-X-02
    comparison baseline (pre-reg #10 sec 1)."""
    rows = []
    for t, rsi in rsi_map.items():
        flag_ob = rsi > ob_hi
        start = flag_ob & (~flag_ob.shift(1, fill_value=False))
        flag_os = rsi < os_lo
        start = start | (flag_os & (~flag_os.shift(1, fill_value=False)))
        pos = np.where(start.to_numpy())[0]
        rsi_np = rsi.to_numpy()
        dates = rsi.index
        rows += [(t, str(dates[i].date()),
                  "OB" if rsi_np[i] > ob_hi else "OS", int(i)) for i in pos]
    det = pd.DataFrame(rows, columns=["ticker", "signal_date", "shape",
                                      "bar_index"])
    det["warmup"] = det["bar_index"] < WARMUP
    return det


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


def measure_cross_legs(det: pd.DataFrame, N: int):
    """Engine forward returns for the crossing baseline, per crossing leg.
    All rows pass as placeholder "C" (frozen engine's third slot)."""
    out = {}
    drops = {}
    for leg in CROSS_LEGS:
        sub = det[det["shape"] == leg].assign(shape="C")
        rows, dropped = measure_returns(sub, N)
        rows["shape"] = leg
        out[leg] = rows
        drops[leg] = int(dropped["C"])
    return out, drops


def make_sample_same(det_tickers: np.ndarray, same_pool: dict, rng):
    """Vectorized same-ticker sampler (RV #8 convention)."""
    u, counts = np.unique(det_tickers, return_counts=True)
    weights = counts.astype(np.float64) / counts.sum()
    lengths = np.array([len(same_pool[t]) for t in u], dtype=np.int64)
    n_missing = int((lengths == 0).sum())
    assert n_missing == 0, (f"{n_missing} leg tickers have no OOS window "
                            "pool (expected 0)")
    off = np.concatenate(([0], np.cumsum(lengths)))
    flat = np.concatenate([same_pool[t] for t in u])

    def sample_same(M: int) -> np.ndarray:
        ts = rng.choice(len(u), size=M, p=weights)
        idx = off[ts] + (rng.random(M) * lengths[ts]).astype(np.int64)
        return flat[idx]
    return sample_same


def sample_from(pool: np.ndarray, rng):
    def s(M: int) -> np.ndarray:
        return pool[rng.integers(0, len(pool), size=M)]
    return s


def f1_leg(rows: pd.DataFrame, pools, rng) -> dict:
    """F1 absolute, per leg (convention as pre-reg #9: p_input = max,
    est = max, ci_low = min, ci_upper = min)."""
    oos = rows[rows["is_oos"]]
    n = int(len(oos))
    if n == 0:
        return {"n": 0, "mean_ret": None, "median_ret": None,
                "excess": {"random_entries": None, "same_ticker": None,
                           "spy": None},
                "p": 1.0, "est": None, "ci_low": None, "ci_upper": None,
                "win_rate": None}
    rets = oos["ret"].to_numpy()
    sample_same = make_sample_same(oos["ticker"].to_numpy(), pools["same"], rng)
    e_rand = bootstrap_excess(rets, sample_from(pools["random"], rng), rng)
    e_same = bootstrap_excess(rets, sample_same, rng)
    e_spy = bootstrap_excess(rets, sample_from(pools["spy"], rng), rng)
    return {"n": n, "mean_ret": float(rets.mean()),
            "median_ret": float(np.median(rets)),
            "win_rate": float((rets > 0).mean()),
            "excess": {"random_entries": list(e_rand),
                       "same_ticker": list(e_same), "spy": list(e_spy)},
            "p": float(max(e_rand[4], e_same[4])),
            "est": float(max(e_rand[0], e_same[0])),
            "ci_low": float(min(e_rand[2], e_same[2])),
            "ci_upper": float(min(e_rand[3], e_same[3]))}


def two_sample_hit(selected: np.ndarray, full: np.ndarray, rng):
    """Bootstrap P(ret > 0 | selected) - P(ret > 0 | full); same shape and
    p-convention as two_sample_excess (mean, med, lo, hi, p)."""
    M, F = len(selected), len(full)
    diffs = np.empty(B)
    for b in range(B):
        s = (selected[rng.integers(0, M, size=M)] > 0).mean()
        f = (full[rng.integers(0, F, size=F)] > 0).mean()
        diffs[b] = s - f
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return float(diffs.mean()), float(np.median(diffs)), float(lo), float(hi), float(p)


def f2_cell(rows_div: pd.DataFrame, rows_cross: pd.DataFrame, metric: str,
            rng) -> dict:
    """F2 reliability contrast cell: divergence - crossings, OOS, on the
    mean forward return or the directional hit rate."""
    d = rows_div[rows_div["is_oos"]]["ret"].to_numpy()
    c = rows_cross[rows_cross["is_oos"]]["ret"].to_numpy()
    n_d, n_c = len(d), len(c)
    if n_d < 2 or n_c < 2:
        return {"n_div": n_d, "n_cross": n_c, "mean_div": None,
                "mean_cross": None, "hit_div": None, "hit_cross": None,
                "est": None, "ci_low": None, "ci_upper": None, "p": 1.0}
    tx = two_sample_excess(d, c, rng) if metric == "mean" \
        else two_sample_hit(d, c, rng)
    return {"n_div": n_d, "n_cross": n_c, "mean_div": float(d.mean()),
            "mean_cross": float(c.mean()), "hit_div": float((d > 0).mean()),
            "hit_cross": float((c > 0).mean()),
            "est": float(tx[0]), "ci_low": float(tx[2]),
            "ci_upper": float(tx[3]), "p": float(tx[4])}


def f2_family(rows: dict, rows_cross: dict, rng) -> dict:
    """F2 family: 4 tests (2 legs x 2 metrics), Holm across all four."""
    fam = {}
    for leg, metric in F2_TESTS:
        cross_leg = "OS" if leg == "BULL" else "OB"
        fam[f"{leg}-{metric}"] = f2_cell(rows[leg], rows_cross[cross_leg],
                                         metric, rng)
    order = sorted(fam, key=lambda k: fam[k].get("p", 1.0))
    for rank, k in enumerate(order, start=1):
        gate = ALPHA / (len(order) - rank + 1)
        fam[k]["holm_gate"] = gate
        fam[k]["holm_rejected"] = fam[k].get("p", 1.0) <= gate
    for k, r in fam.items():
        fam[k]["verdict"] = verdict_f2(k, r)
    return fam


def run_holm(fam: dict, shapes):
    """Holm-Bonferroni at ALPHA across `shapes` (engine convention: <=)."""
    order = sorted(shapes, key=lambda s: fam[s].get("p", 1.0))
    for rank, s in enumerate(order, start=1):
        gate = ALPHA / (len(shapes) - rank + 1)
        fam[s]["holm_gate"] = gate
        fam[s]["holm_rejected"] = fam[s].get("p", 1.0) <= gate


def verdict_f1(leg: str, r: dict) -> str:
    """Directional F1 verdicts (pre-reg #10 sec 4)."""
    if int(r["n"]) < MISSING_PASS:
        return (f"INCONCLUSIVE (<{MISSING_PASS} OOS events; n={r['n']})")
    if leg == "BULL":
        if r["holm_rejected"] and r["ci_low"] > 0.0:
            return (f"EDGE (Holm-rejected; excess CI-low {r['ci_low']:+.4f} "
                    "> 0 — bullish divergence, bounce as claimed)")
        if r["holm_rejected"] and r["ci_upper"] < 0.0:
            return (f"FADE (Holm-rejected; excess CI-upper {r['ci_upper']:+.4f}"
                    " < 0 — bullish divergence loses to the baselines, claim "
                    "contradicted)")
    else:  # BEAR
        if r["holm_rejected"] and r["ci_upper"] < 0.0:
            return (f"EDGE (Holm-rejected; excess CI-upper {r['ci_upper']:+.4f}"
                    " < 0 — bearish divergence, pullback as claimed)")
        if r["holm_rejected"] and r["ci_low"] > 0.0:
            return (f"FADE (Holm-rejected; excess CI-low {r['ci_low']:+.4f} "
                    "> 0 — bearish divergence beats the baselines, claim "
                    "contradicted)")
    return (f"NO EDGE (p_input {r['p']:.3f}; est {r['est']:+.4f}; CI-low "
            f"{r['ci_low']:+.4f}..CI-upper {r['ci_upper']:+.4f})")


def verdict_f2(test: str, r: dict) -> str:
    """F2 reliability verdicts (pre-reg #10 sec 4)."""
    if int(r["n_div"]) < MISSING_PASS:
        return (f"INCONCLUSIVE (<{MISSING_PASS} OOS divergence events; "
                f"n_div={r['n_div']}, n_cross={r['n_cross']})")
    if test.startswith("BULL"):
        if r["ci_low"] > 0.0:
            return (f"EDGE (contrast CI-low {r['ci_low']:+.4f} > 0 — bullish "
                    "divergence more reliable than oversold crossings)")
        if r["ci_upper"] < 0.0:
            return (f"FADE (contrast CI-upper {r['ci_upper']:+.4f} < 0 — "
                    "bullish divergence less reliable than oversold crossings)")
    else:
        if r["ci_upper"] < 0.0:
            return (f"EDGE (contrast CI-upper {r['ci_upper']:+.4f} < 0 — "
                    "bearish divergence more reliable than overbought "
                    "crossings)")
        if r["ci_low"] > 0.0:
            return (f"FADE (contrast CI-low {r['ci_low']:+.4f} > 0 — bearish "
                    "divergence less reliable than overbought crossings)")
    return (f"NO EDGE (contrast est {r['est']:+.4f}, p {r['p']:.3f})")


def freq_measure(det_div: pd.DataFrame, det_cross: pd.DataFrame,
                 rng) -> dict:
    """I-X-02 frequency: OOS event counts (warm-up excluded), ratio, and a
    ticker-cluster bootstrap CI on the ratio. A measurement, not a verdict."""
    d = det_div[~det_div["warmup"]]
    c = det_cross[~det_cross["warmup"]]
    oos_d = d[d["signal_date"] >= ERA_OOS]
    oos_c = c[c["signal_date"] >= ERA_OOS]
    div_counts = oos_d.groupby("ticker").size().to_numpy(dtype=np.float64)
    cross_counts = oos_c.groupby("ticker").size().to_numpy(dtype=np.float64)
    n_div = int(oos_d.shape[0])
    n_cross = int(oos_c.shape[0])
    if n_div == 0 or n_cross == 0 or len(div_counts) == 0:
        return {"n_div": n_div, "n_cross": n_cross, "ratio": None,
                "ci_low": None, "ci_upper": None,
                "n_bull": int((oos_d["shape"] == "BULL").sum()),
                "n_bear": int((oos_d["shape"] == "BEAR").sum()),
                "n_ob": int((oos_c["shape"] == "OB").sum()),
                "n_os": int((oos_c["shape"] == "OS").sum())}
    ratios = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, len(div_counts), size=len(div_counts))
        d_b = div_counts[idx].sum()
        c_b = cross_counts[idx].sum()
        ratios[b] = d_b / max(c_b, 1)
    lo, hi = np.percentile(ratios, [2.5, 97.5])
    return {"n_div": n_div, "n_cross": n_cross, "ratio": n_div / n_cross,
            "ci_low": float(lo), "ci_upper": float(hi),
            "n_bull": int((oos_d["shape"] == "BULL").sum()),
            "n_bear": int((oos_d["shape"] == "BEAR").sum()),
            "n_ob": int((oos_c["shape"] == "OB").sum()),
            "n_os": int((oos_c["shape"] == "OS").sum())}


def fmt_num(v, spec="+.4f") -> str:
    """Format a possibly-None number; '—' for None (no format applied)."""
    return "—" if v is None else format(v, spec)


def pools_of(pkg) -> dict:
    return {"random": pkg[1], "same": pkg[2], "spy": pkg[3]}


def main() -> int:
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()

    # ---- per-ticker bars (full OHLCV — the fractal needs Low/High; the
    # frozen engine loads only Open/Close, so the tool reads the frozen
    # parquets directly for High/Low and uses the same Close as load_bars)
    low_map, high_map, close_map = {}, {}, {}
    rsi10 = {}
    rsi_min_all, rsi_max_all = np.inf, -np.inf
    for t in universe:
        if not (BARS_DIR / f"{t}.parquet").exists():
            continue  # universe rows without bars (build_pools convention)
        df = pd.read_parquet(BARS_DIR / f"{t}.parquet")
        low_map[t] = df["Low"]
        high_map[t] = df["High"]
        close_map[t] = df["Close"]
        rsi = rsi_series(df["Close"], PERIOD_PRIMARY)
        rsi10[t] = rsi
        v = rsi.to_numpy(dtype=np.float64)
        valid = ~np.isnan(v)
        if valid.any():
            rsi_min_all = min(rsi_min_all, float(v[valid].min()))
            rsi_max_all = max(rsi_max_all, float(v[valid].max()))

    det_div, div_stats = div_frame(low_map, high_map, rsi10, K_PRIMARY,
                                   MIN_SEP_PRIMARY, CONFIRM)
    det_cross = cross_frame(rsi10, OB_HI, OS_LO)
    n_warmup_div = int(det_div["warmup"].sum())
    n_warmup_cross = int(det_cross["warmup"].sum())

    # ---- structural checks (pre-reg #10 sec 3) ----
    assert rsi_min_all >= 0.0 - 1e-9 and rsi_max_all <= 100.0 + 1e-9, (
        f"RSI bounds violated: min {rsi_min_all:.12f}, max {rsi_max_all:.12f}")
    assert div_stats["min_t1"] >= PERIOD_PRIMARY, (
        f"event with first-swing RSI undefined: min t1 "
        f"{div_stats['min_t1']} < {PERIOD_PRIMARY} (expected 0)")
    assert div_stats["n_bad_signal"] == 0, (
        f"{div_stats['n_bad_signal']} events whose signal bar lies beyond "
        "the ticker's series (expected 0)")

    # ---- primary measurement ----
    rng = np.random.default_rng(SEED)
    pools = pools_of(build_pools(N_PRIMARY, universe))

    camp_div = det_div[~det_div["warmup"]].copy()
    camp_cross = det_cross[~det_cross["warmup"]].copy()
    rows_p, drops_p = measure_legs(camp_div, N_PRIMARY)
    rows_cross, drops_cross = measure_cross_legs(camp_cross, N_PRIMARY)

    fam1 = {leg: f1_leg(rows_p[leg], pools, rng) for leg in LEGS}
    run_holm(fam1, LEGS)
    for leg in LEGS:
        fam1[leg]["verdict"] = verdict_f1(leg, fam1[leg])
    fam2 = f2_family(rows_p, rows_cross, rng)

    freq = freq_measure(det_div, det_cross, rng)

    # ---- sensitivities (pre-declared, NO verdicts) ----
    sens = {}

    # S1: horizons N = 1 / 5 / 20 (F1 + F2). Baselines rebuilt per horizon
    # (era- AND horizon-matched N-bar window pools — the pre-reg #9 S1 bug
    # fix); crossings re-measured at the horizon for the F2 contrast.
    sens["horizons"] = {}
    for n in SENS_N:
        rows_n, drops_n = measure_legs(camp_div, n)
        rows_cn, drops_cn = measure_cross_legs(camp_cross, n)
        pools_n = pools_of(build_pools(n, universe))
        sens["horizons"][f"N={n}"] = {
            "drops": drops_n, "drops_cross": drops_cn,
            "f1": {leg: f1_leg(rows_n[leg], pools_n, rng) for leg in LEGS},
            "f2": f2_family(rows_n, rows_cn, rng)}

    # S2: swing scale k = 3 / 5 (F1 + F2; signal bar = t2 + k)
    sens["swing_scale"] = {}
    for k in K_SENS:
        det_k, stats_k = div_frame(low_map, high_map, rsi10, k,
                                   MIN_SEP_PRIMARY, k)
        rows_k, drops_k = measure_legs(det_k[~det_k["warmup"]].copy(),
                                       N_PRIMARY)
        sens["swing_scale"][f"k={k}"] = {
            "drops": drops_k, "min_t1": stats_k["min_t1"],
            "f1": {leg: f1_leg(rows_k[leg], pools, rng) for leg in LEGS},
            "f2": f2_family(rows_k, rows_cross, rng)}

    # S3: period 14 (F1 + F2, crossings recomputed at 14; frequency at 14)
    rsi14 = {t: rsi_series(close_map[t], PERIOD_SENS) for t in low_map}
    det_14, stats_14 = div_frame(low_map, high_map, rsi14, K_PRIMARY,
                                 MIN_SEP_PRIMARY, CONFIRM)
    det_c14 = cross_frame(rsi14, OB_HI, OS_LO)
    rows_14, drops_14 = measure_legs(det_14[~det_14["warmup"]].copy(),
                                     N_PRIMARY)
    rows_c14, drops_c14 = measure_cross_legs(det_c14[~det_c14["warmup"]].copy(),
                                             N_PRIMARY)
    sens["period14"] = {
        "drops": drops_14, "drops_cross": drops_c14,
        "f1": {leg: f1_leg(rows_14[leg], pools, rng) for leg in LEGS},
        "f2": f2_family(rows_14, rows_c14, rng),
        "frequency": freq_measure(det_14, det_c14, rng)}

    # S4: min separation >= 10 bars (F1 + F2)
    det_10, stats_10 = div_frame(low_map, high_map, rsi10, K_PRIMARY,
                                 MIN_SEP_SENS, CONFIRM)
    rows_s4, drops_s4 = measure_legs(det_10[~det_10["warmup"]].copy(),
                                     N_PRIMARY)
    sens["min_sep10"] = {
        "drops": drops_s4,
        "f1": {leg: f1_leg(rows_s4[leg], pools, rng) for leg in LEGS},
        "f2": f2_family(rows_s4, rows_cross, rng)}

    # S5: per-year F1 leg mean returns (OOS)
    oos_p = pd.concat([rows_p[leg] for leg in LEGS], ignore_index=True)
    py = oos_p.groupby([oos_p["signal_date"].str[:4], "shape"])["ret"].agg(
        ["mean", "count"])
    sens["per_year"] = {
        str(y): {leg: {"mean_ret": float(py.loc[(y, leg), "mean"]),
                       "n": int(py.loc[(y, leg), "count"])}
                 for leg in LEGS if (y, leg) in py.index}
        for y in sorted(set(i[0] for i in py.index))}

    # S6: IS record (descriptive — selection era)
    sens["is_record"] = {}
    for leg in LEGS:
        is_rows = rows_p[leg][~rows_p[leg]["is_oos"]]
        sens["is_record"][leg] = {
            "n": int(len(is_rows)),
            "mean_ret": float(is_rows["ret"].mean()) if len(is_rows) else None,
            "win_rate": float((is_rows["ret"] > 0).mean())
            if len(is_rows) else None}

    # S7: extreme-gated divergence — per-leg gate on the FIRST swing's RSI:
    # BULL requires RSI_t1 < 30, BEAR requires RSI_t1 > 70 (the video's
    # bearish example notes the RSI "blips briefly into overbought" at the
    # first high). Each leg's frame is built with its own gate.
    fam_x, drops_x_l = {}, {}
    for leg, extreme in (("BULL", OS_LO), ("BEAR", OB_HI)):
        det_l, _ = div_frame(low_map, high_map, rsi10, K_PRIMARY,
                             MIN_SEP_PRIMARY, CONFIRM, extreme=extreme)
        rows_l, drops_l = measure_legs(det_l[~det_l["warmup"]].copy(),
                                       N_PRIMARY)
        fam_x[leg] = f1_leg(rows_l[leg], pools, rng)
        drops_x_l[leg] = drops_l[leg]
    run_holm(fam_x, LEGS)
    for leg in LEGS:
        fam_x[leg]["verdict"] = verdict_f1(leg, fam_x[leg])
    sens["extreme_gated"] = {"drops": drops_x_l, "f1": fam_x}

    # S8: chartist's-eye timing (signal at the pivot bar, entry open t2+1)
    det_s8, stats_s8 = div_frame(low_map, high_map, rsi10, K_PRIMARY,
                                 MIN_SEP_PRIMARY, 0)
    rows_s8, drops_s8 = measure_legs(det_s8[~det_s8["warmup"]].copy(),
                                     N_PRIMARY)
    fam_s8 = {leg: f1_leg(rows_s8[leg], pools, rng) for leg in LEGS}
    run_holm(fam_s8, LEGS)
    for leg in LEGS:
        fam_s8[leg]["verdict"] = verdict_f1(leg, fam_s8[leg])
    sens["chartist_eye"] = {"drops": drops_s8, "f1": fam_s8}

    out = {
        "pre_reg": "#10",
        "claim": ("Bullish divergence (price lower low + RSI higher low) => "
                  "bounce; bearish divergence (price higher high + RSI lower "
                  "high) => pullback; divergence signals 'a lot less common "
                  "so arguably a bit more reliable' than the 70/30 "
                  "overbought/oversold signals (Trading 212, rgVdgR1y1Dg "
                  "[05:33-07:03]); simple-average (Cutler) RSI, period 10 "
                  "primary (the demo charts' 'ten day RSI'), measured on US "
                  "equity daily bars (cross-market translation, pre-declared)"),
        "params": {"period_primary": PERIOD_PRIMARY,
                   "period_sensitivity": PERIOD_SENS,
                   "k_fractal": K_PRIMARY, "k_sensitivities": K_SENS,
                   "min_sep": MIN_SEP_PRIMARY, "min_sep_sensitivity":
                       MIN_SEP_SENS, "confirm_lag": CONFIRM,
                   "ob_hi": OB_HI, "os_lo": OS_LO, "cost": COST,
                   "n": N_PRIMARY, "n_sensitivities": SENS_N, "b": B,
                   "seed": SEED, "alpha": ALPHA,
                   "era_oos_start": ERA_OOS, "count_floor": MISSING_PASS,
                   "warmup_excluded_div": n_warmup_div,
                   "warmup_excluded_cross": n_warmup_cross,
                   "engine_sha256": "c7421fbf (frozen Phase-3 engine, "
                                    "imported)"},
        "families": {"f1_absolute": fam1, "f2_reliability": fam2},
        "frequency": freq,
        "sensitivities": sens,
        "assertions": {"rsi_min_all": rsi_min_all, "rsi_max_all": rsi_max_all,
                       "min_t1": div_stats["min_t1"],
                       "min_signal_bar": div_stats["min_signal"],
                       "max_signal_bar": div_stats["max_signal"],
                       "n_bad_signal": div_stats["n_bad_signal"],
                       "drops_primary": drops_p,
                       "drops_cross_primary": drops_cross},
        "fingerprints": {
            "universe_sha256": sha(UNIVERSE_CSV),
            "measure_code_sha256": sha(Path(__file__)),
            "engine_sha256": sha(Path(measure.__file__)),
        },
    }
    RESULTS.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {RESULTS.name}")

    # ---- report ----
    L = []
    L.append("# RSI divergence measurement report (pre-registration #10)")
    L.append("")
    L.append("- Pre-registration #10 (frozen 2026-08-14): claims = bullish "
             "divergence (price lower low + RSI higher low) => bounce; "
             "bearish divergence (price higher high + RSI lower high) => "
             "pullback; 'a lot less common so arguably a bit more reliable' "
             "vs the 70/30 signals (I-X-02/03/04); simple-average RSI, "
             f"period {PERIOD_PRIMARY} primary ({PERIOD_SENS} sensitivity), "
             f"k={K_PRIMARY} fractal, min separation {MIN_SEP_PRIMARY}, "
             f"signal at the confirmation bar t2+{CONFIRM}; N={N_PRIMARY} "
             f"primary, cost {COST}, alpha {ALPHA}, bootstrap {B} "
             f"(seed {SEED})")
    L.append("- Swings: strict k-fractals on Low (bull) / High (bear) — ties "
             "never form a swing; consecutive swing pairs only, disjoint "
             "fractal windows (t2 - t1 >= 5). Signal bar = t2 + k (the "
             "fractal is only knowable at close t2+k — strict no-look-ahead); "
             "entry open t2+k+1, exit close t2+k+N.")
    L.append("- Crossings (the I-X-02 baseline): first bar of each excursion "
             f"above {OB_HI:.0f} / below {OS_LO:.0f} (pre-reg #9 S4 rule), "
             "same period.")
    L.append("- Warm-up guard signal-bar index < 60 (frozen #3 convention, "
             f"also bounds the lookback): {n_warmup_div} divergence and "
             f"{n_warmup_cross} crossing warm-up events excluded and counted")
    L.append("- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date). "
             "Cross-market caveat pre-declared: the video demos GBP/USD and "
             "USD/JPY; measured on US equities.")
    L.append(f"- Events (period {PERIOD_PRIMARY}, k={K_PRIMARY}, min-sep "
             f"{MIN_SEP_PRIMARY}, warm-up excluded): BULL n=%d, BEAR n=%d "
             "(drops at series end: %s); crossings: OB n=%d, OS n=%d (drops: "
             "%s)" % (len(rows_p["BULL"]), len(rows_p["BEAR"]),
                      json.dumps(drops_p), len(rows_cross["OB"]),
                      len(rows_cross["OS"]), json.dumps(drops_cross)))
    L.append("- F1 (absolute, directional per leg): OOS mean forward return "
             "vs era-matched random entries AND same-ticker (SPY reported), "
             "p_input = max, Holm across BULL/BEAR. BULL: EDGE iff CI-low > 0 "
             "(bounce); FADE iff CI-upper < 0. BEAR: EDGE iff CI-upper < 0 "
             "(pullback); FADE iff CI-low > 0. F2 (reliability contrast, "
             "I-X-02): divergence minus 70/30 crossings at the same period, "
             "per leg on mean return AND hit rate (ret > 0 after cost), "
             "Holm across the 4 tests.")
    L.append("")
    L.append("## Verdicts — Family 1: absolute (directional per leg)")
    L.append("")
    for leg in LEGS:
        r = fam1[leg]
        e_rand, e_same, e_spy = (r["excess"]["random_entries"],
                                 r["excess"]["same_ticker"], r["excess"]["spy"])
        L.append(f"- F1-{leg}: n={r['n']} | mean_ret {fmt_num(r['mean_ret'])} "
                 f"| win_rate {fmt_num(r['win_rate'], '.4f')} | excess vs "
                 f"random {e_rand[0]:+.4f} (CI {e_rand[2]:+.4f}.."
                 f"{e_rand[3]:+.4f}, p {e_rand[4]:.3f}) | vs same {e_same[0]:+.4f} "
                 f"(CI {e_same[2]:+.4f}..{e_same[3]:+.4f}, p {e_same[4]:.3f}) "
                 f"| vs spy {e_spy[0]:+.4f} (p {e_spy[4]:.3f}) | p_input "
                 f"{r['p']:.3f} | est {r['est']:+.4f} (CI-low {r['ci_low']:+.4f}"
                 f"..CI-upper {r['ci_upper']:+.4f}) | Holm gate "
                 f"{r['holm_gate']:.4f} -> **{r['verdict']}**")
    L.append("")
    L.append("## Verdicts — Family 2: reliability contrast (I-X-02, "
             "divergence minus 70/30 crossings)")
    L.append("")
    for k in F2_TESTS:
        r = fam2["%s-%s" % k]
        L.append(f"- F2-{k[0]}-{k[1]}: n_div={r['n_div']} | n_cross="
                 f"{r['n_cross']} | div mean {fmt_num(r['mean_div'])} | cross "
                 f"mean {fmt_num(r['mean_cross'])} | div hit "
                 f"{fmt_num(r['hit_div'], '.4f')} | cross hit "
                 f"{fmt_num(r['hit_cross'], '.4f')} | contrast "
                 f"{fmt_num(r['est'])} (CI {fmt_num(r['ci_low'])}.."
                 f"{fmt_num(r['ci_upper'])}, p {r['p']:.3f}) | Holm gate "
                 f"{r['holm_gate']:.4f} -> **{r['verdict']}**")
    L.append("")
    L.append("## Frequency (I-X-02 first half — measurement, not a verdict)")
    L.append("")
    L.append(f"- OOS divergence events: {freq['n_div']:,} "
             f"(BULL {freq['n_bull']:,}, BEAR {freq['n_bear']:,}) vs 70/30 "
             f"crossing events: {freq['n_cross']:,} (OB {freq['n_ob']:,}, "
             f"OS {freq['n_os']:,}) — ratio {fmt_num(freq['ratio'], '.4f')} "
             f"(ticker-cluster bootstrap CI {fmt_num(freq['ci_low'], '.4f')}"
             f"..{fmt_num(freq['ci_upper'], '.4f')}); CI-upper < 1 confirms "
             f"\"a lot less common\"")
    L.append("")
    L.append("## Sensitivities (exploratory — NO verdicts)")
    L.append("")

    L.append("### S1: horizons N = 1 / 5 / 20")
    L.append("")
    L.append("*Baselines rebuilt per horizon (era- AND horizon-matched "
             "N-bar window pools); crossings re-measured at the horizon for "
             "the F2 contrast.*")
    L.append("")
    for n in SENS_N:
        cell = sens["horizons"][f"N={n}"]
        L.append(f"**N={n}** (drops {json.dumps(cell['drops'])}):")
        for leg in LEGS:
            r = cell["f1"][leg]
            e_r, e_s = r["excess"]["random_entries"], r["excess"]["same_ticker"]
            L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} "
                     f"| win {fmt_num(r['win_rate'], '.4f')} | vs random "
                     f"{e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same {e_s[0]:+.4f} "
                     f"(p {e_s[4]:.3f})")
        for k in F2_TESTS:
            r = cell["f2"]["%s-%s" % k]
            L.append(f"- F2-{k[0]}-{k[1]}: contrast {fmt_num(r['est'])} "
                     f"(p {r['p']:.3f}); div hit {fmt_num(r['hit_div'], '.4f')}"
                     f" vs cross hit {fmt_num(r['hit_cross'], '.4f')}")
        L.append("")
    L.append("### S2: swing scale k = 3 / 5 (period 10)")
    L.append("")
    for k in K_SENS:
        cell = sens["swing_scale"][f"k={k}"]
        L.append(f"**k={k}** (drops {json.dumps(cell['drops'])}):")
        for leg in LEGS:
            r = cell["f1"][leg]
            e_r, e_s = r["excess"]["random_entries"], r["excess"]["same_ticker"]
            L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} "
                     f"| vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                     f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
        for kk in F2_TESTS:
            r = cell["f2"]["%s-%s" % kk]
            L.append(f"- F2-{kk[0]}-{kk[1]}: contrast {fmt_num(r['est'])} "
                     f"(p {r['p']:.3f})")
        L.append("")
    L.append("### S3: period 14 (textbook default; crossings at 14)")
    L.append("")
    cell = sens["period14"]
    L.append(f"Drops {json.dumps(cell['drops'])}:")
    for leg in LEGS:
        r = cell["f1"][leg]
        e_r, e_s = r["excess"]["random_entries"], r["excess"]["same_ticker"]
        L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} | "
                 f"vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                 f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
    for k in F2_TESTS:
        r = cell["f2"]["%s-%s" % k]
        L.append(f"- F2-{k[0]}-{k[1]}: contrast {fmt_num(r['est'])} "
                 f"(p {r['p']:.3f}); div hit {fmt_num(r['hit_div'], '.4f')}"
                 f" vs cross hit {fmt_num(r['hit_cross'], '.4f')}")
    fr = cell["frequency"]
    L.append(f"- Frequency at period 14: divergence {fr['n_div']:,} vs "
             f"crossings {fr['n_cross']:,} — ratio {fmt_num(fr['ratio'], '.4f')}"
             f" (CI {fmt_num(fr['ci_low'], '.4f')}.."
             f"{fmt_num(fr['ci_upper'], '.4f')})")
    L.append("")
    L.append("### S4: min separation >= 10 bars")
    L.append("")
    cell = sens["min_sep10"]
    L.append(f"Drops {json.dumps(cell['drops'])}:")
    for leg in LEGS:
        r = cell["f1"][leg]
        e_r, e_s = r["excess"]["random_entries"], r["excess"]["same_ticker"]
        L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} | "
                 f"vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                 f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
    for k in F2_TESTS:
        r = cell["f2"]["%s-%s" % k]
        L.append(f"- F2-{k[0]}-{k[1]}: contrast {fmt_num(r['est'])} "
                 f"(p {r['p']:.3f})")
    L.append("")
    L.append("### S5: per-year F1 leg mean returns (OOS)")
    L.append("")
    L.append("| year | BULL | BEAR |")
    L.append("|---|---|---|")
    for y in sorted(sens["per_year"]):
        cells = []
        for leg in LEGS:
            r = sens["per_year"][y].get(leg)
            cells.append(f"{r['mean_ret']:+.4f} (n={r['n']})" if r else "—")
        L.append(f"| {y} | " + " | ".join(cells) + " |")
    L.append("")
    L.append("### S6: IS record (descriptive — selection era)")
    L.append("")
    L.append("| leg | n | mean_ret | win_rate |")
    L.append("|---|---|---|---|")
    for leg in LEGS:
        r = sens["is_record"][leg]
        L.append(f"| {leg} | {r['n']} | {fmt_num(r['mean_ret'])} | "
                 f"{fmt_num(r['win_rate'], '.4f')} |")
    L.append("")
    L.append("### S7: extreme-gated divergence (first swing's RSI beyond "
             "70/30)")
    L.append("")
    cell = sens["extreme_gated"]
    L.append(f"Drops {json.dumps(cell['drops'])}:")
    for leg in LEGS:
        r = cell["f1"][leg]
        e_r, e_s = r["excess"]["random_entries"], r["excess"]["same_ticker"]
        L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} | "
                 f"vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                 f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
    L.append("")
    L.append("### S8: chartist's-eye timing (signal at the pivot bar, entry "
             "open t2+1)")
    L.append("")
    L.append("*Pre-declared caveat: the swing's future-side fractal "
             "condition is then a selection input — it excludes pivots "
             "followed by continuation, tilting toward the claim.*")
    L.append("")
    cell = sens["chartist_eye"]
    L.append(f"Drops {json.dumps(cell['drops'])}:")
    for leg in LEGS:
        r = cell["f1"][leg]
        e_r, e_s = r["excess"]["random_entries"], r["excess"]["same_ticker"]
        L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} | "
                 f"vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                 f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_divergence.py` regenerates this "
             "report; the seed is fixed, so results are stable across runs.")
    L.append(f"Assertions: RSI within [0, 100] everywhere (min "
             f"{rsi_min_all:.12f}, max {rsi_max_all:.12f}; PASS); no event "
             f"with first-swing RSI undefined (min t1 {div_stats['min_t1']}; "
             "PASS); no event whose fractal lacks confirmation bars (PASS); "
             "no leg ticker missing an OOS window pool (PASS).")
    L.append("Input fingerprints: universe %s…, measure code %s… (Phase-3 "
             "engine c7421fbf… imported unchanged)."
             % (out["fingerprints"]["universe_sha256"][:12],
                out["fingerprints"]["measure_code_sha256"][:12]))
    L.append("Any change to the detector, data, or measurement code changes "
             "the frozen inputs and requires a new pre-registration before "
             "it can drive a verdict.")
    L.append("")
    REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
