"""RV re-measurement for pre-registration #24 (ledger rows yFo-01/-05/-09/-14,
3rE-02, GXl-12), frozen per the #24 pre-registration freeze block.

The claim (his stated parameters, per the §J scan): relative volume with a
30-50-day baseline, threshold 5x — "almost 98% of it comes from stocks that
have relative volume of 5 or higher" (yFo-01), "a relative volume of three
in my opinion is not high enough" (yFo-05), "without that relative volume
the patterns aren't predictable" (yFo-09). Pre-reg #8 measured the frozen
detector's RV (20-bar lookback, 2.0) — looser threshold, shorter lookback.

This tool re-measures the SAME conditioning question at HIS stated
parameters. It is a variant of measure_rv.py (pre-reg #8); that tool and the
detection set are NOT modified.

  RV50_t = v_t / mean(v, prior 50 bars)   primary (his platform display, yFo-14)
  RV30_t = v_t / mean(v, prior 30 bars)   sensitivity (his stated GXl-12
                                          definition; NO verdicts)
  Primary threshold: 5.0 (yFo-01); low cell < 2.0 (mirrors #8's low cell).
  Sensitivities (NO verdicts): RV50 at 2.0/3.0 (the yFo-05 gray zone);
    RV30 at 5.0/2.0; per-year; IS record; distributions; #8 cross-check.

  Hypotheses (pre-reg #24 sec 2, ONE Holm family of 5 slots, alpha=0.05, OOS
  only, count floor 100 OOS detections per cell):
    H1 F1-A absolute: Shape A detections with RV50 >= 5 beat era-matched
       random AND same-ticker baselines (p_input = max of the two p's).
    H2 F1-B absolute: same on Shape B.
    H3 F2-B contrast: Shape B, mean(high RV50 >= 5) - mean(low RV50 < 2) > 0.
    H4 F2-C contrast: same on Shape C.
    H5 F2-A contrast: same on Shape A. NOT inconclusive by construction
       under RV50: the #8 construction note was specific to the 20-bar
       denominator. Asserted empirically: min RV50 over A detections < 2.0.

  EDGE = Holm-rejected AND excess/contrast CI-low > 0. FADE (contrast only)
  = Holm-rejected AND CI-upper < 0. Bootstrap B=1000, seed 20260813, engine
  imports from measure.py (frozen c7421fbf...) unchanged. Era split by
  signal date: IS 2000-2015 (record only) / OOS 2016-2025 (verdicts only).

Implementation assertions (red-flag on violation, pre-reg #24 sec 3):
  (a) RV50 recomputable for every detection (n_undef == 0);
  (b) min RV50 over Shape A detections < 2.0 (H5 is live);
  (c) cell counts printed before any p-value is applied.
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
RESULTS = CACHE / "rv2_measure_results.json"
REPORT = CACHE / "rv2_measure_report.md"

SHAPES = "ABC"
LOOKBACK_PRIMARY = 50         # his platform display (yFo-14)
LOOKBACK_SENS = 30            # his stated GXl-12 definition
RV_PRIMARY = 5.0              # yFo-01: "relative volume of 5 or higher"
RV_LOW = 2.0                  # low cell for contrasts (mirrors #8)
RV_SENS = [(50, 3.0), (50, 2.0), (30, 5.0), (30, 2.0)]  # pre-reg sec 6
MISSING_PASS = 100            # count floor: >= 100 OOS detections per cell
N_PRIMARY = 10
SLOTS = ["H1-F1A", "H2-F1B", "H3-F2B", "H4-F2C", "H5-F2A"]


def run_holm5(slots: dict):
    """Holm step-down across the single pre-registered family of 5 slots."""
    order = sorted(slots, key=lambda k: slots[k].get("p", 1.0))
    for rank, k in enumerate(order, start=1):
        gate = ALPHA / (len(order) - rank + 1)
        slots[k]["holm_gate"] = gate
        slots[k]["holm_rejected"] = slots[k].get("p", 1.0) < gate


def verdict_f1(r: dict) -> str:
    if int(r["n_high"]) < MISSING_PASS:
        return (f"INCONCLUSIVE (<{MISSING_PASS} high-RV OOS detections; "
                f"n={r['n_high']})")
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return (f"EDGE (Holm-rejected; excess CI-low {r['ci_low']:+.4f} > 0 "
                f"vs both random and same-ticker)")
    return (f"NO EDGE (p_input {r['p']:.3f}; est {r['est']:+.4f}; CI-low "
            f"{r['ci_low']:+.4f})")


def verdict_f2(r: dict) -> str:
    if (int(r["n_high"]) < MISSING_PASS or int(r["n_low"]) < MISSING_PASS):
        return (f"INCONCLUSIVE (<{MISSING_PASS} OOS detections in a cell; "
                f"high {r['n_high']}, low {r['n_low']})")
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return (f"EDGE (Holm-rejected; contrast CI-low {r['ci_low']:+.4f} > 0)")
    if r["holm_rejected"] and r["ci_upper"] < 0.0:
        return (f"FADE (Holm-rejected; contrast CI-upper {r['ci_upper']:+.4f} < 0)")
    return (f"NO EDGE (contrast est {r['est']:+.4f}; p {r['p']:.3f})")


def fmt_num(v, spec="+.4f") -> str:
    return "—" if v is None else format(v, spec)


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def compute_rv(veto_rows: pd.DataFrame, lookback: int) -> pd.Series:
    """RV per detection row: v_t / mean(v, prior `lookback` bars)."""
    out = np.full(len(veto_rows), np.nan)
    n_undef = 0
    for t, grp in veto_rows.groupby("ticker"):
        bars = pd.read_parquet(BARS_DIR / f"{t}.parquet")
        pos = {x: j for j, x in enumerate(bars.index)}
        vol = bars["Volume"].to_numpy()
        for orig_idx, row in grp.iterrows():
            loc = pos.get(pd.Timestamp(row["signal_date"]))
            if loc is None or loc < lookback:
                n_undef += 1
                continue
            mean_lb = float(np.mean(vol[loc - lookback:loc]))
            if mean_lb <= 0.0:
                n_undef += 1
                continue
            out[orig_idx] = float(vol[loc]) / mean_lb
    return pd.Series(out, index=veto_rows.index), n_undef


def main() -> int:
    vd = pd.read_csv(VETO_CSV)
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()

    camp = vd[vd["warmup"] == False].copy().reset_index(drop=True)  # noqa: E712
    camp["veto_pass"] = camp["veto_pass"].astype(bool)

    # (c) cell counts before any p-value: printed below as computed.
    rv50, n_undef50 = compute_rv(camp, LOOKBACK_PRIMARY)
    camp["rv50"] = rv50
    rv30, n_undef30 = compute_rv(camp, LOOKBACK_SENS)   # sensitivity definition
    camp["rv30"] = rv30
    rv20, n_undef20 = compute_rv(camp, 20)      # #8 cross-check definition
    camp["rv20"] = rv20
    assert n_undef50 == 0, f"RV50 undefined for {n_undef50} detections"
    assert n_undef30 == 0, f"RV30 undefined for {n_undef30} detections"
    assert n_undef20 == 0, f"RV20 undefined for {n_undef20} detections"

    sel = camp[camp["veto_pass"]].copy()
    full = camp.copy()

    # ---- assertion (b): H5 is live under RV50 ----
    a_rv50 = sel.loc[sel["shape"] == "A", "rv50"]
    min_rv50_a = float(a_rv50.min())
    assert min_rv50_a < RV_LOW, (
        f"H5 not live: min RV50 over A detections {min_rv50_a:.6f} >= 2.0 — "
        "the F2-A low cell is empty by construction after all; pre-reg #24 "
        "sec 2 asserted otherwise. STOP: this contradicts the pre-registration.")

    pools_pkg = build_pools(N_PRIMARY, universe)
    _, random_pool, same_pool, spy_pool = pools_pkg
    rng = np.random.default_rng(SEED)

    def subset_rets(sub, s, n=N_PRIMARY):
        rows, _ = measure_returns(sub[sub["shape"] == s], n)
        return rows

    fam1 = {}   # absolute: A, B only (H1/H2)
    fam2 = {}   # contrast: A, B, C (H3/H4/H5)
    rv_col = "rv50"
    rv_thr_hi, rv_thr_lo = RV_PRIMARY, RV_LOW

    # ---- cell counts first (assertion (c)) ----
    # OOS rule identical to measure_returns' is_oos (signal_date >= ERA_OOS);
    # counts computed on the detection frame itself (measure_returns does not
    # propagate the rv columns).
    oos_mask = camp["signal_date"] >= ERA_OOS
    print("cell counts (OOS, veto-pass), RV50 >= %.1f / < %.1f:" % (rv_thr_hi, rv_thr_lo))
    counts = {}
    for s in SHAPES:
        sub = sel[(sel["shape"] == s) & oos_mask]
        hi_n = int((sub["rv50"] >= rv_thr_hi).sum())
        lo_n = int((sub["rv50"] < rv_thr_lo).sum())
        counts[s] = (hi_n, lo_n)
        print(f"  shape {s}: n_total_oos={len(sub)} high={hi_n} low={lo_n}")

    for s in ("A", "B"):
        hi = sel[(sel["shape"] == s) & (sel[rv_col] >= rv_thr_hi)]
        hi_rows = subset_rets(hi, s)
        oos_hi = hi_rows[hi_rows["is_oos"]]
        rets_hi = oos_hi["ret"].to_numpy()
        n_hi = int(len(oos_hi))

        def sample_same(M, det_tickers=oos_hi["ticker"].to_numpy(),
                        same_pool=same_pool, rng=rng):
            ts = det_tickers[rng.integers(0, len(det_tickers), size=M)]
            out = np.empty(M)
            for j, t in enumerate(ts):
                pool = same_pool.get(t)
                out[j] = (pool[rng.integers(0, len(pool))]
                          if pool is not None and len(pool) else np.nan)
            return out

        def sample_random(M, random_pool=random_pool, rng=rng):
            return random_pool[rng.integers(0, len(random_pool), size=M)]

        e_rand = bootstrap_excess(rets_hi, sample_random, rng)
        e_same = bootstrap_excess(rets_hi, sample_same, rng)
        e_spy = bootstrap_excess(rets_hi,
                                 lambda M: spy_pool[rng.integers(0, len(spy_pool), size=M)], rng)
        p_input = max(e_rand[4], e_same[4])
        fam1[s] = {"n_high": n_hi,
                   "mean_ret": float(rets_hi.mean()) if n_hi else None,
                   "p": float(p_input),
                   "excess": {"random_entries": list(e_rand),
                              "same_ticker": list(e_same),
                              "spy": list(e_spy)},
                   "est": float(max(e_rand[0], e_same[0])),
                   "ci_low": float(min(e_rand[2], e_same[2])),
                   "verdict": ""}

    for s in SHAPES:
        hi = sel[(sel["shape"] == s) & (sel[rv_col] >= rv_thr_hi)]
        lo = sel[(sel["shape"] == s) & (sel[rv_col] < rv_thr_lo)]
        hi_rows, lo_rows = subset_rets(hi, s), subset_rets(lo, s)
        oos_hi, oos_lo = hi_rows[hi_rows["is_oos"]], lo_rows[lo_rows["is_oos"]]
        rets_hi, rets_lo = oos_hi["ret"].to_numpy(), oos_lo["ret"].to_numpy()
        n_hi, n_lo = int(len(oos_hi)), int(len(oos_lo))
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

    slots = {"H1-F1A": dict(fam1["A"]), "H2-F1B": dict(fam1["B"]),
             "H3-F2B": dict(fam2["B"]), "H4-F2C": dict(fam2["C"]),
             "H5-F2A": dict(fam2["A"])}
    run_holm5(slots)
    for k, (fam, s) in {"H1-F1A": (fam1, "A"), "H2-F1B": (fam1, "B"),
                        "H3-F2B": (fam2, "B"), "H4-F2C": (fam2, "C"),
                        "H5-F2A": (fam2, "A")}.items():
        fam[s]["holm_gate"] = slots[k]["holm_gate"]
        fam[s]["holm_rejected"] = slots[k]["holm_rejected"]
        fam[s]["verdict"] = (verdict_f1(fam[s]) if fam is fam1
                             else verdict_f2(fam[s]))

    # ---- sensitivities (NO verdicts) ----
    sens = {"rv50_thresholds": {}, "rv30": {}, "per_year": {}, "is_record": {},
            "distributions": {}, "crosscheck_8": {}}

    def f1f2_at(col, thr_hi, thr_lo=None):
        f1t, f2t = {}, {}
        for s in SHAPES:
            hiT = sel[(sel["shape"] == s) & (sel[col] >= thr_hi)]
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
                      "excess_random": list(e_rand), "excess_same": list(e_same),
                      "p_input": float(max(e_rand[4], e_same[4]))}
            if thr_lo is None:
                f2t[s] = {"n_high": n_hi, "excess": None}
                continue
            loT = sel[(sel["shape"] == s) & (sel[col] < thr_lo)]
            rows_lo = subset_rets(loT, s)
            oos_lo = rows_lo[rows_lo["is_oos"]]
            rets_lo = oos_lo["ret"].to_numpy()
            if len(rets_hi) >= 2 and len(rets_lo) >= 2:
                tx = two_sample_excess(rets_hi, rets_lo, rng)
            else:
                tx = None
            f2t[s] = {"n_high": int(len(oos_hi)), "n_low": int(len(oos_lo)),
                      "excess": list(tx) if tx else None,
                      "p": float(tx[4]) if tx else None}
        return f1t, f2t

    sens["rv50_thresholds"] = {}
    for thr in (3.0, 2.0):
        f1t, f2t = f1f2_at("rv50", thr, RV_LOW)
        sens["rv50_thresholds"][f"{thr:.1f}"] = {"f1": f1t, "f2": f2t}
    for thr in (5.0, 2.0):
        f1t, _ = f1f2_at("rv30", thr, None)
        f1t2, f2t2 = f1f2_at("rv30", thr, RV_LOW)
        sens["rv30"][f"{thr:.1f}"] = {"f1": f1t, "f2": f2t2}

    # per-year + IS record at the primary definition
    for s in SHAPES:
        hi = sel[(sel["shape"] == s) & (sel["rv50"] >= RV_PRIMARY)]
        hi_rows = subset_rets(hi, s)
        oos_hi = hi_rows[hi_rows["is_oos"]]
        if len(oos_hi):
            py = oos_hi.groupby(oos_hi["signal_date"].str[:4])["ret"].agg(["mean", "count"])
            sens["per_year"][s] = {str(y): {"mean_ret": float(r["mean"]), "n": int(r["count"])}
                                   for y, r in py.iterrows()}
        else:
            sens["per_year"][s] = {}
        is_hi = hi_rows[~hi_rows["is_oos"]]
        sens["is_record"][s] = {"n": int(len(is_hi)),
                                "mean_ret": float(is_hi["ret"].mean()) if len(is_hi) else None,
                                "win_rate": float((is_hi["ret"] > 0).mean()) if len(is_hi) else None}

    for s in SHAPES:
        rv_s = sel.loc[sel["shape"] == s, "rv50"]
        sens["distributions"][s] = {
            "n": int(len(rv_s)), "median_rv50": float(rv_s.median()),
            "share_ge_2.0": float((rv_s >= 2.0).mean()),
            "share_ge_3.0": float((rv_s >= 3.0).mean()),
            "share_ge_5.0": float((rv_s >= 5.0).mean()),
            "min_rv50": float(rv_s.min())}

    # ---- #8 cross-check: RV20 >= 2.0 must reproduce the §I.5 cells ----
    for s in SHAPES:
        hi8 = sel[(sel["shape"] == s) & (sel["rv20"] >= 2.0)]
        rows8 = subset_rets(hi8, s)
        oos8 = rows8[rows8["is_oos"]]
        sens["crosscheck_8"][s] = {
            "n_high_rv20_ge_2": int(len(oos8)),
            "mean_ret": float(oos8["ret"].mean()) if len(oos8) else None}

    out = {
        "pre_reg": "#24",
        "claim": ("RV conditioning at his stated parameters: threshold 5x on "
                  "a 50-day baseline (primary); low cell < 2.0; contrast and "
                  "absolute families on the frozen veto-pass detections"),
        "params": {"lookback_primary": LOOKBACK_PRIMARY,
                   "lookback_sensitivity": LOOKBACK_SENS,
                   "rv_primary": RV_PRIMARY, "rv_low": RV_LOW,
                   "rv_sensitivities": [list(x) for x in RV_SENS],
                   "cost": COST, "n": N_PRIMARY, "b": B, "seed": SEED,
                   "alpha": ALPHA, "era_oos_start": ERA_OOS,
                   "count_floor": MISSING_PASS,
                   "holm_slots": SLOTS,
                   "rv50_undefined": n_undef50, "rv30_undefined": n_undef30,
                   "rv20_undefined": n_undef20},
        "families": {"f1_absolute": fam1, "f2_contrast": fam2},
        "sensitivities": sens,
        "assertions": {"min_rv50_over_A_detections": min_rv50_a,
                       "rv50_undefined_count": n_undef50,
                       "rv30_undefined_count": n_undef30,
                       "rv20_undefined_count": n_undef20,
                       "cell_counts_oos": {s: {"high": c[0], "low": c[1]}
                                           for s, c in counts.items()}},
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
    L.append("# RV2 measurement report (pre-registration #24)")
    L.append("")
    L.append(f"- Pre-reg #24 (frozen per its freeze block): claim = RV "
             f"conditioning at HIS stated parameters — RV50 = v_t / mean(v, "
             f"prior {LOOKBACK_PRIMARY} bars), threshold {RV_PRIMARY:.1f} "
             f"(yFo-01), low cell < {RV_LOW:.1f}; N={N_PRIMARY}, cost {COST}, "
             f"alpha {ALPHA}, bootstrap {B} (seed {SEED})")
    L.append(f"- One Holm family of {len(SLOTS)} slots ({', '.join(SLOTS)}), "
             "OOS only, count floor 100 OOS detections per cell")
    L.append(f"- Inputs: veto_detections_v1.csv (%d rows, warm-up excluded "
             "%d; RV50 undefined %d — expected 0)"
             % (len(vd), int(vd["warmup"].sum()), n_undef50))
    L.append("- Structural difference vs #8: F2-A is LIVE under the 50-bar "
             "denominator; asserted min RV50 over A detections %.6f < 2.0"
             % min_rv50_a)
    L.append("")
    L.append("## Verdicts — Family 1: absolute edge of the RV50 >= 5 subset")
    L.append("")
    for s in ("A", "B"):
        r = fam1[s]
        e_rand, e_same, e_spy = (r["excess"]["random_entries"],
                                 r["excess"]["same_ticker"], r["excess"]["spy"])
        L.append(f"- F1-absolute {s}: n_high={r['n_high']} | mean_ret "
                 f"{fmt_num(r['mean_ret'])} "
                 f"| excess vs random {e_rand[0]:+.4f} (CI {e_rand[2]:+.4f}.."
                 f"{e_rand[3]:+.4f}, p {e_rand[4]:.3f}) | vs same "
                 f"{e_same[0]:+.4f} (CI {e_same[2]:+.4f}..{e_same[3]:+.4f}, "
                 f"p {e_same[4]:.3f}) | vs spy {e_spy[0]:+.4f} (p "
                 f"{e_spy[4]:.3f}) | p_input {r['p']:.3f} | Holm gate "
                 f"{r['holm_gate']:.4f} -> **{r['verdict']}**")
    L.append("")
    L.append("## Verdicts — Family 2: high (RV50 >= 5) minus low (RV50 < 2) contrast")
    L.append("")
    for s in SHAPES:
        r = fam2[s]
        L.append(f"- F2-contrast {s}: n_high={r['n_high']} | n_low={r['n_low']} "
                 f"| high {fmt_num(r['mean_high'])} | low "
                 f"{fmt_num(r['mean_low'])} | excess {fmt_num(r['est'])} "
                 f"(CI {fmt_num(r['ci_low'])}..{fmt_num(r['ci_upper'])}, p "
                 f"{r['p']:.3f}) | Holm gate "
                 f"{r['holm_gate'] if r['holm_gate'] is not None else '—'} "
                 f"-> **{r['verdict']}**")
    L.append("")
    L.append("## Sensitivities (exploratory — NO verdicts)")
    L.append("")
    for tag, d in (("RV50 thresholds (3.0, 2.0)", sens["rv50_thresholds"]),
                   ("RV30 (30-bar lookback) at 5.0 and 2.0", sens["rv30"])):
        L.append(f"### {tag}")
        L.append("")
        for thr, res in d.items():
            f1t = res["f1"]
            L.append(f"**threshold {thr}** — F1:")
            L.append("")
            L.append("| shape | n_high | mean_ret | vs random (CI, p) | vs same (CI, p) | p_input |")
            L.append("|---|---|---|---|---|---|")
            for s in SHAPES:
                r = f1t[s]
                e_r, e_s = r["excess_random"], r["excess_same"]
                L.append(f"| {s} | {r['n_high']} | {fmt_num(r['mean_ret'])} | "
                         f"{e_r[0]:+.4f} ({e_r[2]:+.4f}..{e_r[3]:+.4f}, {e_r[4]:.3f}) | "
                         f"{e_s[0]:+.4f} ({e_s[2]:+.4f}..{e_s[3]:+.4f}, {e_s[4]:.3f}) | "
                         f"{r['p_input']:.3f} |")
            if "f2" in res:
                f2t = res["f2"]
                L.append("")
                L.append("F2 (contrast): " + "; ".join(
                    f"{s}: n_high {f2t[s]['n_high']}, n_low {f2t[s]['n_low']}, "
                    f"excess {fmt_num(f2t[s]['excess'][0] if f2t[s]['excess'] else None)}"
                    for s in SHAPES))
            L.append("")
    L.append("### Per-year high-RV50 mean returns (OOS)")
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
    L.append("### IS record at RV50 >= 5.0 (descriptive — selection era)")
    L.append("")
    L.append("| shape | n | mean_ret | win_rate |")
    L.append("|---|---|---|---|")
    for s in SHAPES:
        r = sens["is_record"][s]
        L.append(f"| {s} | {r['n']} | {fmt_num(r['mean_ret'])} | "
                 f"{fmt_num(r['win_rate'], '.4f')} |")
    L.append("")
    L.append("### Shape-level RV50 distributions (veto-pass detections)")
    L.append("")
    L.append("| shape | n | median RV50 | min RV50 | share >= 2.0 | >= 3.0 | >= 5.0 |")
    L.append("|---|---|---|---|---|---|---|")
    for s in SHAPES:
        r = sens["distributions"][s]
        L.append(f"| {s} | {r['n']} | {r['median_rv50']:.3f} | "
                 f"{r['min_rv50']:.3f} | {r['share_ge_2.0']:.4f} | "
                 f"{r['share_ge_3.0']:.4f} | {r['share_ge_5.0']:.4f} |")
    L.append("")
    L.append("### #8 cross-check: RV20 >= 2.0 reproduces the §I.5 cells")
    L.append("")
    L.append("| shape | n_high (RV20 >= 2, OOS) | mean_ret |")
    L.append("|---|---|---|")
    for s in SHAPES:
        r = sens["crosscheck_8"][s]
        L.append(f"| {s} | {r['n_high_rv20_ge_2']} | {fmt_num(r['mean_ret'])} |")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_rv2.py` regenerates this report; "
             "the seed is fixed, so results are stable across runs.")
    L.append("Assertions: (a) RV50/RV30 undefined for %d/%d detections (expected 0/0); "
             "(b) min RV50 over Shape A detections %.6f < 2.0 (H5 live, "
             "PASS); (c) cell counts printed before p-values."
             % (n_undef50, n_undef30, min_rv50_a))
    L.append("Input fingerprints: veto file %s…, measure code %s… "
             "(Phase-3 engine %s… imported unchanged)."
             % (out["fingerprints"]["veto_file_sha256"][:12],
                out["fingerprints"]["measure_code_sha256"][:12],
                out["fingerprints"]["engine_sha256"][:12]))
    L.append("Any change to the detector, data, or measurement code changes "
             "the frozen inputs and requires a new pre-registration before "
             "it can drive a verdict.")
    L.append("")
    REPORT.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())