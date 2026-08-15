"""RSI 70/30 reversal measurement for pre-registration #9 (ledger I-X-01),
frozen 2026-08-14.

The claim: "anything above seventy percent... the market is said to be
overbought... anything below thirty percent... the market is said to be
oversold... maybe the market has gone down too far and is due a bounce
back" (Trading 212, rgVdgR1y1Dg [03:16-03:27]).

Measured on the frozen Phase-1 bars, RSI computed from parquet closes with
the SIMPLE-AVERAGE (Cutler) formula the video itself teaches:

    RS_t  = mean(gains over the 14 daily changes ending at t) /
            mean(|losses| over the 14 daily changes ending at t)
    RSI_t = 100 - 100 / (1 + RS_t)

Conventions (frozen, pre-reg #9 sec 1): avg_loss = 0 -> RSI = 100 (covers
the all-gain and flat cases, TA-Lib rule); avg_gain = 0 and avg_loss > 0
-> RSI = 0.

Legs (state-based primary — every qualifying bar is a detection):
    OB: RSI_t > 70  (pullback due; directional claim: below baselines)
    OS: RSI_t < 30  (bounce due; directional claim: above baselines)
Warm-up guard: bar index < 60 excluded (frozen #3 convention; also bounds
the 14-bar lookback with margin).

Protocol (pre-reg #9 sec 3-4): N = 10 primary, COST = 0.0015 round-trip,
bootstrap B = 1000 seed 20260813, era split by signal date (IS 2000-2015 /
OOS 2016-2025), Holm-Bonferroni at alpha = 0.05 within each family, count
floor 100 OOS detections per leg.

F1 (absolute, directional per leg): OOS mean forward return of the leg vs
the era-matched baselines (random entries -COST, same-ticker -COST, SPY
raw). Convention as #6/#7/#8: p_input = max(p_rand, p_same), est = max,
ci_low = min; ci_upper = min too (the directional side that matters for OB).
  OB: EDGE iff Holm-rejected AND excess CI-upper < 0; FADE iff Holm-
      rejected AND CI-low > 0.
  OS: EDGE iff Holm-rejected AND excess CI-low > 0; FADE iff Holm-
      rejected AND CI-upper < 0.
F2 (contrast, the reversal symmetry): two-sample bootstrap excess
mean(OS) - mean(OB) (two_sample_excess from the veto campaign), single
test at alpha = 0.05. EDGE iff CI-low > 0; FADE iff CI-upper < 0.

Sensitivities (pre-declared, NO verdicts): S1 N = 1/5/20 (F1 + F2);
S2 thresholds 80/20, 90/10, 60/40 at period 14 (F1 + F2); S3 period 10 at
70/30 (F1 + F2); S4 crossing-based events (first bar of each excursion
above 70 / below 30, until re-entry) at 70/30 (F1 + F2); S5 per-year F1
leg mean returns (OOS); S6 IS record at 70/30 (F1 table, descriptive);
S7 RSI distribution over OOS bars (leg shares, min/max RSI).

Structural checks (pre-reg #9 sec 3): (a) RSI values within [0, 100]
everywhere — asserted over all computed values; (b) no detections with
< 14 prior closes (the lookback) — asserted, expected 0 (warm-up covers).

Engine pieces import from measure.py (frozen, sha c7421fbf...): forward
returns run through the engine's measure_returns unchanged. Its dropped
dict is keyed on shape labels A/B/C (frozen engine), so the OB/OS legs
are passed with placeholder shapes (OB -> "A", OS -> "B") and relabeled
after measurement; the mislabeled dropped counts are read back from the
placeholder keys, per leg. The same-ticker baseline uses each subset's
own per-leg ticker distribution (the #6 protocol correction, per pre-reg
#9 sec 2).

sample_same is vectorized (the RV #8 convention): per draw the ticker is
drawn with the leg's empirical ticker distribution, then a uniform draw
within that ticker's OOS window pool — distributionally identical to the
per-draw loops of earlier campaigns, deterministic via the frozen seed.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import (COST, B, SEED, ALPHA, ERA_OOS, UNIVERSE_CSV, BARS_DIR,
                     load_bars, bootstrap_excess, measure_returns)
import measure
from measure_pillars import build_pools
from measure_veto import two_sample_excess

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
RESULTS = CACHE / "rsi_measure_results.json"
REPORT = CACHE / "rsi_measure_report.md"

PERIOD_PRIMARY = 14
PERIOD_SENS = 10
OB_HI = 70.0
OS_LO = 30.0
THRESH_SENS = [(80, 20), (90, 10), (60, 40)]   # pre-reg #9 sec 6 S2
N_PRIMARY = 10
SENS_N = [1, 5, 20]                            # pre-reg #9 sec 6 S1
WARMUP = 60                                    # frozen #3 convention
MISSING_PASS = 100                             # count floor per leg
LEGS = ("OB", "OS")
LEG_PLACEHOLDER = {"OB": "A", "OS": "B"}       # measure_returns' dropped
                                               # dict is keyed A/B/C (frozen
                                               # engine); legs relabeled after


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def rsi_series(close: pd.Series, period: int) -> pd.Series:
    """Simple-average (Cutler) RSI, the formula the video teaches.

    RSI at bar t uses the `period` daily changes ending at t (closes
    t-period..t). avg_loss = 0 -> 100 (all-gain and flat); avg_gain = 0
    and avg_loss > 0 -> 0. NaN before period prior closes exist.
    """
    d = close.diff()
    gains = d.clip(lower=0.0)
    losses = (-d).clip(lower=0.0)
    # window = the `period` changes ENDING at t (deltas t-period+1..t,
    # INCLUDING the change at t — unlike the volume convention, which
    # excludes the signal bar); first valid at bar index `period`
    g = gains.rolling(period).mean()
    l = losses.rolling(period).mean()
    with np.errstate(divide="ignore", invalid="ignore"):
        rsi = np.where(l == 0, 100.0, np.where(g == 0, 0.0,
                                               100.0 - 100.0 / (1.0 + g / l)))
    return pd.Series(rsi, index=close.index)


def det_frame(rsi_map: dict, ob_hi: float, os_lo: float) -> pd.DataFrame:
    """State-based leg detections from precomputed per-ticker RSI series.

    Every bar with RSI in the leg's range is a detection (bar index, date,
    warm-up flag). Returns rows in ticker order, bar order.
    """
    rows = []
    for t, rsi in rsi_map.items():
        rsi_np = rsi.to_numpy()
        leg = np.where(rsi_np > ob_hi, "OB", np.where(rsi_np < os_lo, "OS", ""))
        pos = np.where(leg != "")[0]
        dates = rsi.index
        rows += [(t, str(dates[i].date()), str(leg[i]), int(i)) for i in pos]
    det = pd.DataFrame(rows, columns=["ticker", "signal_date", "shape",
                                      "bar_index"])
    det["warmup"] = det["bar_index"] < WARMUP
    return det


def cross_frame(rsi_map: dict, ob_hi: float, os_lo: float) -> pd.DataFrame:
    """Crossing-based events (pre-reg #9 sec 6 S4): the first bar of each
    excursion above ob_hi / below os_lo, until re-entry."""
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
    """Engine forward returns per leg (placeholder shapes, relabeled).

    measure_returns' dropped dict is keyed A/B/C (frozen engine); the legs
    pass as placeholders and the per-leg drops are read from those keys.
    """
    out = {}
    drops = {}
    for leg in LEGS:
        sub = det[det["shape"] == leg].assign(shape=LEG_PLACEHOLDER[leg])
        rows, dropped = measure_returns(sub, N)
        rows["shape"] = leg
        out[leg] = rows
        drops[leg] = int(dropped[LEG_PLACEHOLDER[leg]])
    return out, drops


def make_sample_same(det_tickers: np.ndarray, same_pool: dict, rng):
    """Vectorized same-ticker sampler (RV #8 convention).

    Ticker drawn with the leg's empirical ticker distribution, then a
    uniform draw within that ticker's OOS window pool — distributionally
    identical to the per-draw loops of earlier campaigns, deterministic
    via the frozen seed.
    """
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
    """F1 absolute, per leg: OOS mean forward return vs the baselines.

    Convention as #6/#7/#8: p_input = max(p_rand, p_same), est = max,
    ci_low = min; ci_upper = min too (the directional side that matters
    for the OB leg).
    """
    oos = rows[rows["is_oos"]]
    n = int(len(oos))
    if n == 0:
        return {"n": 0, "mean_ret": None, "median_ret": None,
                "excess": {"random_entries": None, "same_ticker": None,
                           "spy": None},
                "p": 1.0, "est": None, "ci_low": None, "ci_upper": None}
    rets = oos["ret"].to_numpy()
    sample_same = make_sample_same(oos["ticker"].to_numpy(), pools["same"], rng)
    e_rand = bootstrap_excess(rets, sample_from(pools["random"], rng), rng)
    e_same = bootstrap_excess(rets, sample_same, rng)
    e_spy = bootstrap_excess(rets, sample_from(pools["spy"], rng), rng)
    return {"n": n, "mean_ret": float(rets.mean()),
            "median_ret": float(np.median(rets)),
            "excess": {"random_entries": list(e_rand),
                       "same_ticker": list(e_same), "spy": list(e_spy)},
            "p": float(max(e_rand[4], e_same[4])),
            "est": float(max(e_rand[0], e_same[0])),
            "ci_low": float(min(e_rand[2], e_same[2])),
            "ci_upper": float(min(e_rand[3], e_same[3]))}


def f2_contrast(rows_ob: pd.DataFrame, rows_os: pd.DataFrame, rng) -> dict:
    """F2 contrast (the reversal symmetry): mean(OS) - mean(OB), OOS.

    Two-sample bootstrap excess (two_sample_excess, the veto campaign's
    frozen function). Single test at alpha = 0.05.
    """
    o_ob = rows_ob[rows_ob["is_oos"]]["ret"].to_numpy()
    o_os = rows_os[rows_os["is_oos"]]["ret"].to_numpy()
    n_ob, n_os = len(o_ob), len(o_os)
    if n_ob < 2 or n_os < 2:
        return {"n_ob": n_ob, "n_os": n_os, "mean_ob": None, "mean_os": None,
                "est": None, "ci_low": None, "ci_upper": None, "p": 1.0}
    tx = two_sample_excess(o_os, o_ob, rng)
    return {"n_ob": n_ob, "n_os": n_os,
            "mean_ob": float(o_ob.mean()), "mean_os": float(o_os.mean()),
            "est": float(tx[0]), "ci_low": float(tx[2]),
            "ci_upper": float(tx[3]), "p": float(tx[4])}


def run_holm(fam: dict, shapes):
    """Holm-Bonferroni at ALPHA across `shapes` (engine convention: <=)."""
    order = sorted(shapes, key=lambda s: fam[s].get("p", 1.0))
    for rank, s in enumerate(order, start=1):
        gate = ALPHA / (len(shapes) - rank + 1)
        fam[s]["holm_gate"] = gate
        fam[s]["holm_rejected"] = fam[s].get("p", 1.0) <= gate


def verdict_f1(leg: str, r: dict) -> str:
    """Directional F1 verdicts (pre-reg #9 sec 4)."""
    if int(r["n"]) < MISSING_PASS:
        return (f"INCONCLUSIVE (<{MISSING_PASS} OOS detections; n={r['n']})")
    if leg == "OB":
        if r["holm_rejected"] and r["ci_upper"] < 0.0:
            return (f"EDGE (Holm-rejected; excess CI-upper {r['ci_upper']:+.4f}"
                    " < 0 — overbought, pullback as claimed)")
        if r["holm_rejected"] and r["ci_low"] > 0.0:
            return (f"FADE (Holm-rejected; excess CI-low {r['ci_low']:+.4f} "
                    "> 0 — overbought keeps rising, claim contradicted)")
    else:  # OS
        if r["holm_rejected"] and r["ci_low"] > 0.0:
            return (f"EDGE (Holm-rejected; excess CI-low {r['ci_low']:+.4f} "
                    "> 0 — oversold, bounce as claimed)")
        if r["holm_rejected"] and r["ci_upper"] < 0.0:
            return (f"FADE (Holm-rejected; excess CI-upper {r['ci_upper']:+.4f}"
                    " < 0 — oversold keeps falling, claim contradicted)")
    return (f"NO EDGE (p_input {r['p']:.3f}; est {r['est']:+.4f}; CI-low "
            f"{r['ci_low']:+.4f}..CI-upper {r['ci_upper']:+.4f})")


def verdict_f2(r: dict) -> str:
    """F2 verdict (pre-reg #9 sec 4): single test at alpha = 0.05."""
    if (int(r["n_ob"]) < MISSING_PASS or int(r["n_os"]) < MISSING_PASS):
        return (f"INCONCLUSIVE (<{MISSING_PASS} OOS detections in a leg; "
                f"OB {r['n_ob']}, OS {r['n_os']})")
    if r["ci_low"] > 0.0:
        return (f"EDGE (contrast CI-low {r['ci_low']:+.4f} > 0 — OS beats OB, "
                "reversal symmetry holds)")
    if r["ci_upper"] < 0.0:
        return (f"FADE (contrast CI-upper {r['ci_upper']:+.4f} < 0 — OB beats "
                "OS, reversal contradicted)")
    return (f"NO EDGE (contrast est {r['est']:+.4f}, p {r['p']:.3f})")


def fmt_num(v, spec="+.4f") -> str:
    """Format a possibly-None number; '—' for None (no format applied)."""
    return "—" if v is None else format(v, spec)


def main() -> int:
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()

    # ---- per-ticker RSI(14), primary detection frame, S7 + bounds ----
    rsi14 = {}
    s7 = {"n_oos_bars": 0, "n_ob_bars": 0, "n_os_bars": 0, "n_mid_bars": 0,
          "min_rsi": np.inf, "max_rsi": -np.inf}
    rsi_min_all, rsi_max_all = np.inf, -np.inf
    for t in universe:
        if not (BARS_DIR / f"{t}.parquet").exists():
            continue  # universe rows without bars (build_pools convention)
        df = load_bars(t)
        rsi = rsi_series(df["Close"], PERIOD_PRIMARY)
        rsi14[t] = rsi
        v = rsi.to_numpy(dtype=np.float64)
        valid = ~np.isnan(v)
        if valid.any():
            rsi_min_all = min(rsi_min_all, float(v[valid].min()))
            rsi_max_all = max(rsi_max_all, float(v[valid].max()))
        oos = df.index >= pd.Timestamp(ERA_OOS)
        ov = valid & oos
        if ov.any():
            s7["n_oos_bars"] += int(ov.sum())
            s7["n_ob_bars"] += int((ov & (v > OB_HI)).sum())
            s7["n_os_bars"] += int((ov & (v < OS_LO)).sum())
            s7["n_mid_bars"] += int((ov & ~(v > OB_HI) & ~(v < OS_LO)).sum())
            s7["min_rsi"] = min(s7["min_rsi"], float(v[ov].min()))
            s7["max_rsi"] = max(s7["max_rsi"], float(v[ov].max()))

    det_primary = det_frame(rsi14, OB_HI, OS_LO)
    det_cross = cross_frame(rsi14, OB_HI, OS_LO)
    n_warmup = int(det_primary["warmup"].sum())

    # ---- structural checks (pre-reg #9 sec 3) ----
    assert rsi_min_all >= 0.0 - 1e-9 and rsi_max_all <= 100.0 + 1e-9, (
        f"RSI bounds violated: min {rsi_min_all:.12f}, max {rsi_max_all:.12f}")
    assert int(det_primary["bar_index"].min()) >= PERIOD_PRIMARY, (
        "detection with < 14 prior closes (expected 0)")

    # ---- primary measurement ----
    rng = np.random.default_rng(SEED)
    pools_pkg = build_pools(N_PRIMARY, universe)
    _, random_pool, same_pool, spy_pool = pools_pkg
    pools = {"random": random_pool, "same": same_pool, "spy": spy_pool}

    camp = det_primary[~det_primary["warmup"]].copy()
    rows_p, drops_p = measure_legs(camp, N_PRIMARY)

    fam1 = {leg: f1_leg(rows_p[leg], pools, rng) for leg in LEGS}
    run_holm(fam1, LEGS)
    for leg in LEGS:
        fam1[leg]["verdict"] = verdict_f1(leg, fam1[leg])
    f2 = f2_contrast(rows_p["OB"], rows_p["OS"], rng)
    f2["verdict"] = verdict_f2(f2)

    # ---- sensitivities (pre-declared, NO verdicts) ----
    sens = {}

    # S1: horizons N = 1 / 5 / 20 (F1 + F2). Baselines rebuilt per horizon:
    # the pre-reg S1 tables read "entry next open, exit close t+N" — the
    # era-matched window pools must be horizon-matched too (N-bar windows),
    # not the primary N=10 pools.
    sens["horizons"] = {}
    for n in SENS_N:
        rows_n, drops_n = measure_legs(camp, n)
        pools_n = build_pools(n, universe)
        pools_n = {"random": pools_n[1], "same": pools_n[2], "spy": pools_n[3]}
        sens["horizons"][f"N={n}"] = {
            "drops": drops_n,
            "f1": {leg: f1_leg(rows_n[leg], pools_n, rng) for leg in LEGS},
            "f2": f2_contrast(rows_n["OB"], rows_n["OS"], rng)}

    # S2: thresholds 80/20, 90/10, 60/40 at period 14 (F1 + F2)
    sens["thresholds"] = {}
    for (hi, lo) in THRESH_SENS:
        det_t = det_frame(rsi14, float(hi), float(lo))
        rows_t, drops_t = measure_legs(det_t[~det_t["warmup"]].copy(), N_PRIMARY)
        sens["thresholds"][f"{hi}/{lo}"] = {
            "drops": drops_t,
            "f1": {leg: f1_leg(rows_t[leg], pools, rng) for leg in LEGS},
            "f2": f2_contrast(rows_t["OB"], rows_t["OS"], rng)}

    # S3: period 10 at 70/30 (F1 + F2)
    rsi10 = {}
    for t in universe:
        if not (BARS_DIR / f"{t}.parquet").exists():
            continue
        rsi10[t] = rsi_series(load_bars(t)["Close"], PERIOD_SENS)
    det_p10 = det_frame(rsi10, OB_HI, OS_LO)
    rows_10, drops_10 = measure_legs(det_p10[~det_p10["warmup"]].copy(),
                                     N_PRIMARY)
    sens["period10"] = {
        "drops": drops_10,
        "f1": {leg: f1_leg(rows_10[leg], pools, rng) for leg in LEGS},
        "f2": f2_contrast(rows_10["OB"], rows_10["OS"], rng)}

    # S4: crossing-based events (F1 + F2)
    rows_c, drops_c = measure_legs(det_cross[~det_cross["warmup"]].copy(),
                                   N_PRIMARY)
    sens["crossing"] = {
        "drops": drops_c,
        "n_events": {leg: int(len(rows_c[leg])) for leg in LEGS},
        "f1": {leg: f1_leg(rows_c[leg], pools, rng) for leg in LEGS},
        "f2": f2_contrast(rows_c["OB"], rows_c["OS"], rng)}

    # S5: per-year F1 leg mean returns (OOS)
    oos_p = pd.concat([rows_p[leg] for leg in LEGS], ignore_index=True)
    py = oos_p.groupby([oos_p["signal_date"].str[:4], "shape"])["ret"].agg(
        ["mean", "count"])
    sens["per_year"] = {
        str(y): {leg: {"mean_ret": float(py.loc[(y, leg), "mean"]),
                       "n": int(py.loc[(y, leg), "count"])}
                 for leg in LEGS if (y, leg) in py.index}
        for y in sorted(set(i[0] for i in py.index))}

    # S6: IS record at 70/30 (descriptive — selection era)
    sens["is_record"] = {}
    for leg in LEGS:
        is_rows = rows_p[leg][~rows_p[leg]["is_oos"]]
        sens["is_record"][leg] = {
            "n": int(len(is_rows)),
            "mean_ret": float(is_rows["ret"].mean()) if len(is_rows) else None,
            "win_rate": float((is_rows["ret"] > 0).mean())
            if len(is_rows) else None}

    # S7: RSI distribution over OOS bars
    s7_out = {k: (float("nan") if k in ("min_rsi", "max_rsi") and
                  s7[k] in (np.inf, -np.inf) else float(s7[k]))
              for k in ("n_oos_bars", "n_ob_bars", "n_os_bars", "n_mid_bars",
                        "min_rsi", "max_rsi")}
    s7_out["share_ob"] = s7_out["n_ob_bars"] / s7_out["n_oos_bars"]
    s7_out["share_os"] = s7_out["n_os_bars"] / s7_out["n_oos_bars"]
    s7_out["share_mid"] = s7_out["n_mid_bars"] / s7_out["n_oos_bars"]
    sens["rsi_distribution"] = s7_out

    out = {
        "pre_reg": "#9",
        "claim": ("RSI > 70 overbought => pullback due; RSI < 30 oversold => "
                  "bounce due (Trading 212, rgVdgR1y1Dg [03:16-03:27]); "
                  "simple-average (Cutler) RSI formula as taught in the "
                  "video, measured on US equity daily bars (cross-market "
                  "translation, pre-declared)"),
        "params": {"period_primary": PERIOD_PRIMARY,
                   "period_sensitivity": PERIOD_SENS,
                   "ob_hi": OB_HI, "os_lo": OS_LO,
                   "threshold_sensitivities": THRESH_SENS,
                   "cost": COST, "n": N_PRIMARY, "n_sensitivities": SENS_N,
                   "b": B, "seed": SEED, "alpha": ALPHA,
                   "era_oos_start": ERA_OOS, "count_floor": MISSING_PASS,
                   "warmup_excluded": n_warmup,
                   "engine_sha256": "c7421fbf (frozen Phase-3 engine, "
                                    "imported)"},
        "families": {"f1_absolute": fam1, "f2_contrast": f2},
        "sensitivities": sens,
        "assertions": {"rsi_min_all": rsi_min_all, "rsi_max_all": rsi_max_all,
                       "n_detections_lt_14_prior_closes": 0,
                       "drops_primary": drops_p},
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
    L.append("# RSI 70/30 measurement report (pre-registration #9)")
    L.append("")
    L.append("- Pre-registration #9 (frozen 2026-08-14): claim = RSI > 70 "
             "overbought (pullback due) / RSI < 30 oversold (bounce due); "
             f"simple-average RSI, period {PERIOD_PRIMARY} primary "
             f"({PERIOD_SENS} sensitivity), thresholds {OB_HI:.0f}/"
             f"{OS_LO:.0f}; N={N_PRIMARY} primary, cost {COST}, alpha "
             f"{ALPHA}, bootstrap {B} (seed {SEED})")
    L.append("- RSI_t = 100 - 100/(1 + RS) with RS = mean(gains over the 14 "
             "daily changes ending at t) / mean(|losses|, same window) — "
             "the simple-average formula the video teaches; conventions: "
             "avg_loss = 0 -> 100, avg_gain = 0 and avg_loss > 0 -> 0")
    L.append("- Legs are state-based (every qualifying bar is a detection); "
             "warm-up guard bar index < 60 (frozen #3 convention, also "
             f"bounds the lookback); {n_warmup} warm-up detections excluded "
             "and counted")
    L.append("- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date). "
             "Cross-market caveat pre-declared: the video demos GBP/USD; "
             "measured on US equities.")
    L.append(f"- Detections (period {PERIOD_PRIMARY}, {OB_HI:.0f}/{OS_LO:.0f}, "
             "warm-up excluded): OB n=%d, OS n=%d (drops at series end: "
             "%s)" % (len(rows_p["OB"]), len(rows_p["OS"]),
                      json.dumps(drops_p)))
    L.append("- F1 (absolute, directional per leg): OOS mean forward return "
             "vs era-matched random entries AND same-ticker (SPY reported), "
             "p_input = max, Holm across OB/OS. OB: EDGE iff CI-upper < 0 "
             "(pullback); FADE iff CI-low > 0. OS: EDGE iff CI-low > 0 "
             "(bounce); FADE iff CI-upper < 0. F2 (contrast): two-sample "
             "excess mean(OS) - mean(OB), single test at alpha = 0.05.")
    L.append("")
    L.append("## Verdicts — Family 1: absolute (directional per leg)")
    L.append("")
    for leg in LEGS:
        r = fam1[leg]
        e_rand, e_same, e_spy = (r["excess"]["random_entries"],
                                 r["excess"]["same_ticker"], r["excess"]["spy"])
        L.append(f"- F1-{leg}: n={r['n']} | mean_ret {fmt_num(r['mean_ret'])} "
                 f"| excess vs random {e_rand[0]:+.4f} (CI {e_rand[2]:+.4f}.."
                 f"{e_rand[3]:+.4f}, p {e_rand[4]:.3f}) | vs same {e_same[0]:+.4f} "
                 f"(CI {e_same[2]:+.4f}..{e_same[3]:+.4f}, p {e_same[4]:.3f}) "
                 f"| vs spy {e_spy[0]:+.4f} (p {e_spy[4]:.3f}) | p_input "
                 f"{r['p']:.3f} | est {r['est']:+.4f} (CI-low {r['ci_low']:+.4f}"
                 f"..CI-upper {r['ci_upper']:+.4f}) | Holm gate "
                 f"{r['holm_gate']:.4f} -> **{r['verdict']}**")
    L.append("")
    L.append("## Verdict — Family 2: contrast (reversal symmetry, OS minus OB)")
    L.append("")
    L.append(f"- F2: n_ob={f2['n_ob']} | n_os={f2['n_os']} | OB mean "
             f"{fmt_num(f2['mean_ob'])} | OS mean {fmt_num(f2['mean_os'])} | "
             f"excess {fmt_num(f2['est'])} (CI {fmt_num(f2['ci_low'])}.."
             f"{fmt_num(f2['ci_upper'])}, p {f2['p']:.3f}) -> "
             f"**{f2['verdict']}**")
    L.append("")
    L.append("## Sensitivities (exploratory — NO verdicts)")
    L.append("")

    L.append("### S1: horizons N = 1 / 5 / 20")
    L.append("")
    L.append("*Baselines rebuilt per horizon (era- AND horizon-matched "
             "N-bar window pools).*")
    L.append("")
    for n in SENS_N:
        cell = sens["horizons"][f"N={n}"]
        L.append(f"**N={n}** (drops {json.dumps(cell['drops'])}):")
        for leg in LEGS:
            r = cell["f1"][leg]
            e_r, e_s = r["excess"]["random_entries"], r["excess"]["same_ticker"]
            L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} "
                     f"| vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                     f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
        f2c = cell["f2"]
        L.append(f"- F2: OS {fmt_num(f2c['mean_os'])} minus OB "
                 f"{fmt_num(f2c['mean_ob'])} = {fmt_num(f2c['est'])} (p "
                 f"{f2c['p']:.3f})")
        L.append("")
    L.append("### S2: thresholds 80/20, 90/10, 60/40 (period 14)")
    L.append("")
    for (hi, lo) in THRESH_SENS:
        cell = sens["thresholds"][f"{hi}/{lo}"]
        L.append(f"**{hi}/{lo}** (drops {json.dumps(cell['drops'])}):")
        for leg in LEGS:
            r = cell["f1"][leg]
            e_r, e_s = r["excess"]["random_entries"], r["excess"]["same_ticker"]
            L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} "
                     f"| vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                     f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
        f2c = cell["f2"]
        L.append(f"- F2: OS {fmt_num(f2c['mean_os'])} minus OB "
                 f"{fmt_num(f2c['mean_ob'])} = {fmt_num(f2c['est'])} (p "
                 f"{f2c['p']:.3f})")
        L.append("")
    L.append("### S3: period 10 at 70/30")
    L.append("")
    cell = sens["period10"]
    L.append(f"Drops {json.dumps(cell['drops'])}:")
    for leg in LEGS:
        r = cell["f1"][leg]
        e_r, e_s = r["excess"]["random_entries"], r["excess"]["same_ticker"]
        L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} | "
                 f"vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                 f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
    f2c = cell["f2"]
    L.append(f"- F2: OS {fmt_num(f2c['mean_os'])} minus OB "
             f"{fmt_num(f2c['mean_ob'])} = {fmt_num(f2c['est'])} (p "
             f"{f2c['p']:.3f})")
    L.append("")
    L.append("### S4: crossing-based events (first bar of each excursion)")
    L.append("")
    cell = sens["crossing"]
    L.append(f"Events: OB {cell['n_events']['OB']}, OS {cell['n_events']['OS']} "
             f"(drops {json.dumps(cell['drops'])}):")
    for leg in LEGS:
        r = cell["f1"][leg]
        e_r, e_s = r["excess"]["random_entries"], r["excess"]["same_ticker"]
        L.append(f"- F1-{leg}: n={r['n']} | mean {fmt_num(r['mean_ret'])} | "
                 f"vs random {e_r[0]:+.4f} (p {e_r[4]:.3f}) | vs same "
                 f"{e_s[0]:+.4f} (p {e_s[4]:.3f})")
    f2c = cell["f2"]
    L.append(f"- F2: OS {fmt_num(f2c['mean_os'])} minus OB "
             f"{fmt_num(f2c['mean_ob'])} = {fmt_num(f2c['est'])} (p "
             f"{f2c['p']:.3f})")
    L.append("")
    L.append("### S5: per-year F1 leg mean returns (OOS)")
    L.append("")
    L.append("| year | OB | OS |")
    L.append("|---|---|---|")
    for y in sorted(sens["per_year"]):
        cells = []
        for leg in LEGS:
            r = sens["per_year"][y].get(leg)
            cells.append(f"{r['mean_ret']:+.4f} (n={r['n']})" if r else "—")
        L.append(f"| {y} | " + " | ".join(cells) + " |")
    L.append("")
    L.append("### S6: IS record at 70/30 (descriptive — selection era)")
    L.append("")
    L.append("| leg | n | mean_ret | win_rate |")
    L.append("|---|---|---|---|")
    for leg in LEGS:
        r = sens["is_record"][leg]
        L.append(f"| {leg} | {r['n']} | {fmt_num(r['mean_ret'])} | "
                 f"{fmt_num(r['win_rate'], '.4f')} |")
    L.append("")
    L.append("### S7: RSI distribution over OOS bars")
    L.append("")
    d7 = sens["rsi_distribution"]
    L.append(f"- OOS bars with RSI defined: {int(d7['n_oos_bars']):,} | "
             f"share > 70 (OB): {d7['share_ob']:.4f} | share < 30 (OS): "
             f"{d7['share_os']:.4f} | share in [30, 70]: {d7['share_mid']:.4f}")
    L.append(f"- RSI min {fmt_num(d7['min_rsi'], '.4f')} / max "
             f"{fmt_num(d7['max_rsi'], '.4f')} over OOS bars")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_rsi.py` regenerates this report; "
             "the seed is fixed, so results are stable across runs.")
    L.append(f"Assertions: RSI within [0, 100] everywhere (min {rsi_min_all:.12f}, "
             f"max {rsi_max_all:.12f}; PASS); no detections with < "
             f"{PERIOD_PRIMARY} prior closes (PASS); no leg ticker missing an "
             "OOS window pool (PASS).")
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
