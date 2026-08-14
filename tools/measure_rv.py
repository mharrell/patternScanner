"""RV measurement for pre-registration #8 (ledger I-D-07 / I-E-01), frozen
2026-08-14.

The claim: "pattern trading you have to remember does not work on all
stocks... it only works on the stocks that have high relative volume...
volume is relative... we just look for what's above average for that stock"
(Class 1, txWaMpSzHhM [25:49-26:36]), with the HFT veto ([16:33-17:02]).
Measured as a CONDITIONING LAYER on the frozen veto-pass detections
(data/cache/veto_detections_v1.csv, pre-reg #3) -- no new detection legs.

  RV_t = v_t / mean(v, prior 20 bars)  -- the frozen detector's exact
    _vol_ratio_ok formula: mean of the prior 20 bars only
    (rolling(20).mean().shift(1)), mean > 0 guard.
  Primary threshold: RV >= 2.0 (the V = 2.0 multiplier reused from the
    shape campaign, pre-reg #3 convention: frozen, not tuned).
  Sensitivities (NO verdicts): thresholds 1.0 / 3.0 / 5.0; full-set at 2.0;
    per-year; IS record; shape-level RV distributions.

  Family 1 (absolute): per shape, OOS mean forward return (N=10, cost) of
    the high-RV subset vs era-matched random entries AND same-ticker
    (p_input = max(p_rand, p_same)), bootstrap B=1000 seed 20260813, Holm
    across A/B/C. EDGE requires Holm rejection AND excess CI-low > 0.
  Family 2 (contrast): per shape, two-sample bootstrap excess high-RV
    minus low-RV (same shape's detections, OOS). Holm across B/C only.
    EDGE requires Holm rejection AND contrast CI-low > 0; FADE requires
    Holm rejection AND CI-upper < 0.

  Structural pre-declaration (pre-reg #8 sec 2): Shape A's frozen detector
    requires v_t >= 2.0 * mean(v, prior 20) at the signal bar
    (PARAMS["A"]["V"] = 2.0), so every A detection has RV >= 2.0 and
    F2-A is INCONCLUSIVE BY CONSTRUCTION -- asserted empirically below
    (min RV over A detections >= 2.0 - 1e-9; violated assertion = red flag).

Engine pieces import from measure.py (frozen, sha c7421fbf...): measure_returns
computes the same forward returns as every prior campaign. Volume is read
from the bars parquet directly (load_bars exposes only Open/Close). The
same-ticker baseline uses the subset's own per-shape ticker distribution
(the #6 protocol correction, per pre-reg #8 sec 3).
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import (COST, B, SEED, ALPHA, ERA_OOS, BARS_DIR,
                     load_bars, bootstrap_excess, measure_returns)
import measure
from measure_pillars import build_pools
from measure_veto import two_sample_excess

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
UNIVERSE_CSV = CACHE / "universe_sp600_2026-08-13.csv"
VETO_CSV = CACHE / "veto_detections_v1.csv"
RESULTS = CACHE / "rv_measure_results.json"
REPORT = CACHE / "rv_measure_report.md"

SHAPES = "ABC"
F2_SHAPES = ("B", "C")       # shapes with a testable contrast (A excluded
                             # by construction, pre-reg #8 sec 2)
VOL_LOOKBACK = 20            # detector convention (VOL_LOOKBACK in detectors.py)
RV_PRIMARY = 2.0             # the frozen V = 2.0 multiplier
RV_SENS = [1.0, 3.0, 5.0]    # pre-reg #8 sec 6 S1
MISSING_PASS = 100           # count floor: >= 100 OOS detections per cell
N_PRIMARY = 10


def run_holm(fam: dict, shapes, n_key: str):
    """Apply Holm across `shapes` to a family dict of per-shape entries."""
    order = sorted(shapes, key=lambda s: fam[s].get("p", 1.0))
    for rank, s in enumerate(order, start=1):
        gate = ALPHA / (len(shapes) - rank + 1)
        fam[s]["holm_gate"] = gate
        fam[s]["holm_rejected"] = fam[s].get("p", 1.0) < gate
    for s in fam:
        if s not in order:
            fam[s]["holm_gate"] = None
            fam[s]["holm_rejected"] = False


def verdict_f1(s: str, r: dict) -> str:
    if int(r["n_high"]) < MISSING_PASS:
        return (f"INCONCLUSIVE (<{MISSING_PASS} high-RV OOS detections; "
                f"n={r['n_high']})")
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return (f"EDGE (Holm-rejected; excess CI-low {r['ci_low']:+.4f} > 0 "
                f"vs both random and same-ticker)")
    return (f"NO EDGE (p_input {r['p']:.3f}; est {r['est']:+.4f}; CI-low "
            f"{r['ci_low']:+.4f})")


def verdict_f2(s: str, r: dict) -> str:
    if r.get("construction"):
        return ("INCONCLUSIVE by construction (Shape A detector requires "
                "RV >= 2.0; min RV asserted)")
    if (int(r["n_high"]) < MISSING_PASS or int(r["n_low"]) < MISSING_PASS):
        return (f"INCONCLUSIVE (<{MISSING_PASS} OOS detections in a cell; "
                f"high {r['n_high']}, low {r['n_low']})")
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return (f"EDGE (Holm-rejected; contrast CI-low {r['ci_low']:+.4f} "
                f"> 0)")
    if r["holm_rejected"] and r["ci_upper"] < 0.0:
        return (f"FADE (Holm-rejected; contrast CI-upper {r['ci_upper']:+.4f}"
                f" < 0)")
    return (f"NO EDGE (contrast est {r['est']:+.4f}; p {r['p']:.3f})")


def fmt_num(v, spec="+.4f") -> str:
    """Format a possibly-None number; '—' for None (no format applied)."""
    return "—" if v is None else format(v, spec)


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def main() -> int:
    vd = pd.read_csv(VETO_CSV)
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()

    camp = vd[vd["warmup"] == False].copy().reset_index(drop=True)
    camp["veto_pass"] = camp["veto_pass"].astype(bool)

    # ---- RV per detection (the detector's exact formula) ----
    # loc of the signal bar in the ticker's bars; RV = v[loc] / mean(v,
    # prior 20 bars). Undefined (NaN) if the bar is missing or < 20 prior
    # bars exist -- expected 0, warm-up (bar index < 60) covers it.
    vol_idx = {}
    n_undef = 0
    rv_arr = np.full(len(camp), np.nan)
    for t, grp in camp.groupby("ticker"):
        bars = pd.read_parquet(BARS_DIR / f"{t}.parquet")
        pos = {x: j for j, x in enumerate(bars.index)}
        vol = bars["Volume"].to_numpy()
        for orig_idx, row in grp.iterrows():
            loc = pos.get(pd.Timestamp(row["signal_date"]))
            if loc is None or loc < VOL_LOOKBACK:
                n_undef += 1
                continue
            mean20 = float(np.mean(vol[loc - VOL_LOOKBACK:loc]))
            if mean20 <= 0.0:
                n_undef += 1
                continue
            rv_arr[orig_idx] = float(vol[loc]) / mean20
    camp["rv"] = rv_arr
    sel = camp[camp["veto_pass"]].copy()
    full = camp.copy()

    # ---- structural assertion: every A detection has RV >= 2.0 ----
    a_rv = sel.loc[sel["shape"] == "A", "rv"]
    min_rv_a = float(a_rv.min())
    assert min_rv_a >= RV_PRIMARY - 1e-9, (
        f"Shape A construction violated: min RV {min_rv_a:.9f} < 2.0")
    assert n_undef == 0, f"RV undefined for {n_undef} detections (expected 0)"

    pools_pkg = build_pools(N_PRIMARY, universe)
    _, random_pool, same_pool, spy_pool = pools_pkg
    rng = np.random.default_rng(SEED)

    fam1, fam2 = {}, {}
    sens = {"thresholds": {}, "full_set": {}, "per_year": {},
            "is_record": {}, "distributions": {}}
    rv_stats = {}

    def subset_rets(sub, s, n=N_PRIMARY):
        rows, _ = measure_returns(sub[sub["shape"] == s], n)
        return rows

    for s in SHAPES:
        rv_s = sel.loc[sel["shape"] == s, "rv"]
        rv_stats[s] = {
            "n": int(len(rv_s)),
            "median_rv": float(rv_s.median()),
            "share_ge_2.0": float((rv_s >= 2.0).mean()),
            "share_ge_3.0": float((rv_s >= 3.0).mean()),
            "share_ge_5.0": float((rv_s >= 5.0).mean()),
            "min_rv": float(rv_s.min()),
        }

        # ---- primary threshold subsets ----
        hi = sel[(sel["shape"] == s) & (sel["rv"] >= RV_PRIMARY)]
        lo = sel[(sel["shape"] == s) & (sel["rv"] < RV_PRIMARY)]

        # ---- Family 1: absolute edge of the high-RV subset ----
        hi_rows = subset_rets(hi, s)
        oos_hi = hi_rows[hi_rows["is_oos"]]
        n_hi = int(len(oos_hi))
        rets_hi = oos_hi["ret"].to_numpy()

        def sample_same(M, det_tickers=oos_hi["ticker"].to_numpy(),
                        same_pool=same_pool, rng=rng):
            ts = det_tickers[rng.integers(0, len(det_tickers), size=M)]
            out = np.empty(M)
            for j, t in enumerate(ts):
                pool = same_pool.get(t)
                if pool is None or len(pool) == 0:
                    out[j] = np.nan
                else:
                    out[j] = pool[rng.integers(0, len(pool))]
            return out

        def sample_random(M, random_pool=random_pool, rng=rng):
            return random_pool[rng.integers(0, len(random_pool), size=M)]

        def sample_spy(M, spy_pool=spy_pool, rng=rng):
            return spy_pool[rng.integers(0, len(spy_pool), size=M)]

        e_rand = bootstrap_excess(rets_hi, sample_random, rng)
        e_same = bootstrap_excess(rets_hi, sample_same, rng)
        e_spy = bootstrap_excess(rets_hi, sample_spy, rng)
        p_input = max(e_rand[4], e_same[4])
        fam1[s] = {"n_high": n_hi,
                   "mean_ret": float(rets_hi.mean()) if n_hi else None,
                   "p": p_input,
                   "excess": {"random_entries": list(e_rand),
                              "same_ticker": list(e_same),
                              "spy": list(e_spy)},
                   "est": float(max(e_rand[0], e_same[0])),
                   "ci_low": float(min(e_rand[2], e_same[2])),
                   "verdict": ""}

        # ---- Family 2: high-minus-low contrast ----
        if s == "A":
            # INCONCLUSIVE by construction: every A detection has RV >= 2.0,
            # the low-RV cell is empty (asserted above). No contrast to run.
            fam2[s] = {"construction": True, "n_high": n_hi, "n_low": 0,
                       "est": None, "ci_low": None, "ci_upper": None,
                       "p": 1.0, "verdict": ""}
        else:
            lo_rows = subset_rets(lo, s)
            oos_lo = lo_rows[lo_rows["is_oos"]]
            n_lo = int(len(oos_lo))
            rets_lo = oos_lo["ret"].to_numpy()
            if n_hi >= 2 and n_lo >= 2:
                tx = two_sample_excess(rets_hi, rets_lo, rng)
            else:
                tx = None
            fam2[s] = {"n_high": n_hi, "n_low": n_lo,
                       "mean_high": float(rets_hi.mean()) if n_hi else None,
                       "mean_low": float(rets_lo.mean()) if n_lo else None,
                       "excess": list(tx) if tx else None,
                       "est": float(tx[0]) if tx else None,
                       "ci_low": float(tx[2]) if tx else None,
                       "ci_upper": float(tx[3]) if tx else None,
                       "p": float(tx[4]) if tx else 1.0,
                       "verdict": ""}

        # ---- Sensitivities (pre-declared, NO verdicts) ----
        # S4: IS record at the primary threshold
        is_hi = hi_rows[~hi_rows["is_oos"]]
        sens["is_record"][s] = {
            "n": int(len(is_hi)),
            "mean_ret": float(is_hi["ret"].mean()) if len(is_hi) else None,
            "win_rate": float((is_hi["ret"] > 0).mean())
            if len(is_hi) else None}

        # S3: per-year high-RV mean returns (OOS)
        if n_hi:
            py = oos_hi.groupby(oos_hi["signal_date"].str[:4])["ret"].agg(
                ["mean", "count"])
            sens["per_year"][s] = {
                str(y): {"mean_ret": float(r["mean"]), "n": int(r["count"])}
                for y, r in py.iterrows()}
        else:
            sens["per_year"][s] = {}

    run_holm(fam1, SHAPES, "n_high")
    run_holm(fam2, F2_SHAPES, "n_high")
    for s in SHAPES:
        fam1[s]["verdict"] = verdict_f1(s, fam1[s])
        fam2[s]["verdict"] = verdict_f2(s, fam2[s])

    # ---- S1: thresholds 1.0 / 3.0 / 5.0 (F1 + F2, NO verdicts) ----
    for T in RV_SENS:
        f1t, f2t = {}, {}
        for s in SHAPES:
            hiT = sel[(sel["shape"] == s) & (sel["rv"] >= T)]
            loT = sel[(sel["shape"] == s) & (sel["rv"] < T)]
            rows_hi = subset_rets(hiT, s)
            oos_hi = rows_hi[rows_hi["is_oos"]]
            rets_hi = oos_hi["ret"].to_numpy()
            n_hi = int(len(oos_hi))

            def sample_same_T(M, det_tickers=oos_hi["ticker"].to_numpy(),
                              same_pool=same_pool, rng=rng):
                ts = det_tickers[rng.integers(0, len(det_tickers), size=M)]
                out = np.empty(M)
                for j, t in enumerate(ts):
                    pool = same_pool.get(t)
                    out[j] = (pool[rng.integers(0, len(pool))]
                              if pool is not None and len(pool) else np.nan)
                return out

            e_rand = bootstrap_excess(rets_hi, sample_random, rng)
            e_same = bootstrap_excess(rets_hi, sample_same_T, rng)
            f1t[s] = {"n_high": n_hi,
                      "mean_ret": float(rets_hi.mean()) if n_hi else None,
                      "excess_random": list(e_rand),
                      "excess_same": list(e_same),
                      "p_input": float(max(e_rand[4], e_same[4]))}

            if s == "A":
                f2t[s] = {"n_high": n_hi, "n_low": int(
                    len(subset_rets(loT, s))), "excess": None}
                continue
            rows_lo = subset_rets(loT, s)
            oos_lo = rows_lo[rows_lo["is_oos"]]
            rets_lo = oos_lo["ret"].to_numpy()
            if len(rets_hi) >= 2 and len(rets_lo) >= 2:
                tx = two_sample_excess(rets_hi, rets_lo, rng)
            else:
                tx = None
            f2t[s] = {"n_high": int(len(oos_hi)), "n_low": int(len(oos_lo)),
                      "mean_high": float(rets_hi.mean())
                      if len(oos_hi) else None,
                      "mean_low": float(rets_lo.mean())
                      if len(oos_lo) else None,
                      "excess": list(tx) if tx else None}
        sens["thresholds"][f"{T:.1f}"] = {"f1": f1t, "f2": f2t}

    # ---- S2: full (non-vetoed) set at RV >= 2.0, F1 only ----
    for s in SHAPES:
        hiF = full[(full["shape"] == s) & (full["rv"] >= RV_PRIMARY)]
        rows_hi = subset_rets(hiF, s)
        oos_hi = rows_hi[rows_hi["is_oos"]]
        rets_hi = oos_hi["ret"].to_numpy()
        n_hi = int(len(oos_hi))

        def sample_same_F(M, det_tickers=oos_hi["ticker"].to_numpy(),
                          same_pool=same_pool, rng=rng):
            ts = det_tickers[rng.integers(0, len(det_tickers), size=M)]
            out = np.empty(M)
            for j, t in enumerate(ts):
                pool = same_pool.get(t)
                out[j] = (pool[rng.integers(0, len(pool))]
                          if pool is not None and len(pool) else np.nan)
            return out

        e_rand = bootstrap_excess(rets_hi, sample_random, rng)
        e_same = bootstrap_excess(rets_hi, sample_same_F, rng)
        sens["full_set"][s] = {"n_high": n_hi,
                               "mean_ret": float(rets_hi.mean())
                               if n_hi else None,
                               "excess_random": list(e_rand),
                               "excess_same": list(e_same)}

    sens["distributions"] = rv_stats

    out = {
        "pre_reg": "#8",
        "claim": ("pattern trading only works on stocks with high relative "
                  "volume (RV >= 2.0); low-RV names are the losing side"),
        "params": {"rv_primary": RV_PRIMARY, "rv_sensitivities": RV_SENS,
                   "vol_lookback": VOL_LOOKBACK, "cost": COST, "n": N_PRIMARY,
                   "b": B, "seed": SEED, "alpha": ALPHA,
                   "era_oos_start": ERA_OOS, "count_floor": MISSING_PASS,
                   "rv_undefined": n_undef},
        "families": {"f1_absolute": fam1, "f2_contrast": fam2},
        "sensitivities": sens,
        "assertions": {"min_rv_over_A_detections": min_rv_a,
                       "rv_undefined_count": n_undef},
        "fingerprints": {
            "veto_file_sha256": sha(VETO_CSV),
            "measure_code_sha256": sha(Path(__file__)),
            "engine_sha256": sha(Path(measure.__file__)),
        },
    }
    RESULTS.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {RESULTS.name}")

    # ---- report ----
    L = []
    L.append("# RV measurement report (pre-registration #8)")
    L.append("")
    L.append("- Pre-registration #8 (frozen 2026-08-14): claim = pattern "
             "trading only works on high-relative-volume stocks (RV >= 2.0, "
             f"the frozen V = 2.0 multiplier); N={N_PRIMARY} primary, cost "
             f"{COST}, alpha {ALPHA}, bootstrap {B} (seed {SEED})")
    L.append("- RV_t = v_t / mean(v, prior 20 bars) — the frozen detector's "
             "exact formula (rolling(20).mean().shift(1), mean > 0 guard). "
             f"Primary threshold {RV_PRIMARY:.1f}; sensitivities "
             + ", ".join(f"{t:.1f}" for t in RV_SENS) + " (no verdicts)")
    L.append("- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)")
    L.append("- Inputs: veto_detections_v1.csv (pre-reg #3 output, %d rows, "
             "warm-up excluded %d; RV undefined %d — expected 0)"
             % (len(vd), int(vd["warmup"].sum()), n_undef))
    L.append("- F1 (absolute): high-RV subset vs era-matched random entries "
             "AND same-ticker, p_input = max, Holm across A/B/C. F2 "
             "(contrast): high-RV minus low-RV two-sample excess, Holm "
             "across B/C — F2-A INCONCLUSIVE BY CONSTRUCTION (every A "
             "detection has RV >= 2.0; min %.3f asserted)." % min_rv_a)
    L.append("")
    L.append("## Verdicts — Family 1: absolute edge of the high-RV subset")
    L.append("")
    for s in SHAPES:
        r = fam1[s]
        e_rand, e_same, e_spy = (r["excess"]["random_entries"],
                                 r["excess"]["same_ticker"],
                                 r["excess"]["spy"])
        L.append(f"- F1-absolute {s}: n_high={r['n_high']} | mean_ret "
                 f"{fmt_num(r['mean_ret'])} "
                 f"| excess vs random {e_rand[0]:+.4f} (CI "
                 f"{e_rand[2]:+.4f}..{e_rand[3]:+.4f}, p {e_rand[4]:.3f}) | "
                 f"vs same {e_same[0]:+.4f} (CI {e_same[2]:+.4f}.."
                 f"{e_same[3]:+.4f}, p {e_same[4]:.3f}) | vs spy "
                 f"{e_spy[0]:+.4f} (p {e_spy[4]:.3f}) | p_input {r['p']:.3f} "
                 f"| Holm gate {r['holm_gate']:.4f} -> **{r['verdict']}**")
    L.append("")
    L.append("## Verdicts — Family 2: high-RV minus low-RV contrast")
    L.append("")
    for s in SHAPES:
        r = fam2[s]
        if r.get("construction"):
            L.append(f"- F2-contrast {s}: **{r['verdict']}** — min RV over "
                     f"A detections {min_rv_a:.6f} >= 2.0 (asserted); the "
                     f"RV < 2.0 cell is empty")
            continue
        L.append(f"- F2-contrast {s}: n_high={r['n_high']} | n_low="
                 f"{r['n_low']} | high {r['mean_high']:+.4f} | low "
                 f"{r['mean_low']:+.4f} | excess {r['est']:+.4f} (CI "
                 f"{r['ci_low']:+.4f}..{r['ci_upper']:+.4f}, p {r['p']:.3f}) "
                 f"| Holm gate {r['holm_gate'] if r['holm_gate'] is not None else '—'} "
                 f"-> **{r['verdict']}**")
    L.append("")
    L.append("## Sensitivities (exploratory — NO verdicts)")
    L.append("")
    for T in RV_SENS:
        f1t = sens["thresholds"][f"{T:.1f}"]["f1"]
        f2t = sens["thresholds"][f"{T:.1f}"]["f2"]
        L.append(f"### Threshold RV >= {T:.1f}")
        L.append("")
        L.append("| shape | n_high | mean_ret | vs random (CI, p) | vs same "
                 "(CI, p) | p_input |")
        L.append("|---|---|---|---|---|---|")
        for s in SHAPES:
            r = f1t[s]
            e_r, e_s = r["excess_random"], r["excess_same"]
            L.append(f"| {s} | {r['n_high']} | {fmt_num(r['mean_ret'])} | "
                     f"{e_r[0]:+.4f} ({e_r[2]:+.4f}..{e_r[3]:+.4f}, "
                     f"{e_r[4]:.3f}) | {e_s[0]:+.4f} ({e_s[2]:+.4f}.."
                     f"{e_s[3]:+.4f}, {e_s[4]:.3f}) | {r['p_input']:.3f} |")
        L.append("")
        L.append("F2 (contrast): " + "; ".join(
            f"{s}: n_high {r['n_high']}, n_low {r['n_low']}, excess "
            f"{fmt_num(r['excess'][0] if r['excess'] else None)} (p "
            f"{r['excess'][4] if r['excess'] else '—'})"
            for s in SHAPES for r in [f2t[s]]))
        L.append("")
    L.append("### Full (non-vetoed) set at RV >= 2.0 — F1 only")
    L.append("")
    L.append("| shape | n_high | mean_ret | vs random (p) | vs same (p) |")
    L.append("|---|---|---|---|---|")
    for s in SHAPES:
        r = sens["full_set"][s]
        L.append(f"| {s} | {r['n_high']} | {fmt_num(r['mean_ret'])} | "
                 f"{r['excess_random'][0]:+.4f} ({r['excess_random'][4]:.3f}) "
                 f"| {r['excess_same'][0]:+.4f} ({r['excess_same'][4]:.3f}) |")
    L.append("")
    L.append("### Per-year high-RV mean returns (OOS)")
    L.append("")
    L.append("| year | " + " | ".join(SHAPES) + " |")
    L.append("|---" * (len(SHAPES) + 1) + "|")
    years = sorted({y for s in SHAPES for y in sens["per_year"][s]})
    for y in years:
        cells = []
        for s in SHAPES:
            r = sens["per_year"][s].get(y)
            cells.append(f"{r['mean_ret']:+.4f} (n={r['n']})" if r else "—")
        L.append(f"| {y} | " + " | ".join(cells) + " |")
    L.append("")
    L.append("### IS record at RV >= 2.0 (descriptive — selection era)")
    L.append("")
    L.append("| shape | n | mean_ret | win_rate |")
    L.append("|---|---|---|---|")
    for s in SHAPES:
        r = sens["is_record"][s]
        L.append(f"| {s} | {r['n']} | {fmt_num(r['mean_ret'])} | "
                 f"{fmt_num(r['win_rate'], '.4f')} |")
    L.append("")
    L.append("### Shape-level RV distributions (veto-pass detections)")
    L.append("")
    L.append("| shape | n | median RV | min RV | share >= 2.0 | >= 3.0 | "
             ">= 5.0 |")
    L.append("|---|---|---|---|---|---|---|")
    for s in SHAPES:
        r = sens["distributions"][s]
        L.append(f"| {s} | {r['n']} | {r['median_rv']:.3f} | "
                 f"{r['min_rv']:.3f} | {r['share_ge_2.0']:.4f} | "
                 f"{r['share_ge_3.0']:.4f} | {r['share_ge_5.0']:.4f} |")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_rv.py` regenerates this report; "
             "the seed is fixed, so results are stable across runs.")
    L.append("Assertions: min RV over Shape A detections %.6f >= 2.0 - 1e-9 "
             "(detector construction check, PASS); RV undefined for %d "
             "detections (expected 0)."
             % (min_rv_a, n_undef))
    L.append("Input fingerprints: veto file %s…, measure code %s… "
             "(Phase-3 engine c7421fbf… imported unchanged)."
             % (out["fingerprints"]["veto_file_sha256"][:12],
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
