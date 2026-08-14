"""Per-decade drift decomposition for pre-registration #5, frozen 2026-08-14.

Follow-up of pre-reg #4: is the N=20 drift uniform across the OOS era or
concentrated in 2020-2025? Reuses the frozen Phase-3 engine (measure.py,
sha c7421fbf..., NEVER modified) for constants and shared pieces, and
measure_momentum for the entry-set machinery (family_rows, run_holm).

Sub-eras (fixed in pre-reg #5 section 1): early = 2016-01-01..2020-01-01,
late = 2020-01-01..2026-01-01. Era by signal date, as everywhere; baseline
windows are drawn only from bars whose START date falls in the same
sub-era (window_pool_era, same formula as window_pool).

Two pre-registered verdict families, each Holm-corrected across A/C/H3 at
alpha=0.05, OOS only:

  F1 sub-era excess difference: mean N=20 excess vs within-sub-era
     baselines in 2020-2025 MINUS 2016-2019 > 0. Two-sample bootstrap:
     per draw, resample entries and baseline windows within each sub-era,
     diff the excess means. p_input = max(p_random, p_same).
  F2 late-era absolute: within 2020-2025 alone, N=20 excess vs
     within-sub-era baselines > 0 (identical verdict structure to #1-4).

Edge rules (pre-reg #5 section 4, applied per baseline as in #1-4):
  F1: Holm-rejected AND diff CI-lo > 0 vs random AND vs same-ticker.
  F2: Holm-rejected AND excess CI-lo > 0 vs random AND vs same-ticker.

Sensitivities (no verdicts): sub-era continuation diffs and their
difference, early-era absolute, N=40 within sub-eras, per-year N=20 means,
dedupe-20 per sub-era.

Deterministic: fixed seed -> byte-identical outputs across runs.
Outputs: data/cache/decade_measure_results.json + decade_measure_report.md.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import measure_momentum as mm
from measure import (ALPHA, B, COST, ERA_OOS, SEED, load_bars,
                     window_pool, bootstrap_excess, dedupe_20)
from measure_pillars import (UNIVERSE_CSV, build_pools, metric_cis_hyp,
                             measure_returns_hyp, dedupe_20_hyp)

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
DET_SHAPES = CACHE / "detections_v1.csv"
DET_PILLARS = CACHE / "pillar_detections_v1.csv"
RESULTS = CACHE / "decade_measure_results.json"
REPORT = CACHE / "decade_measure_report.md"

N = 20                          # pre-reg #5 primary horizon (= #4 primary)
N_PAIRED = 5
ERAS = {"early": ("2016-01-01", "2020-01-01"),
        "late": ("2020-01-01", "2026-01-01")}
FAMILIES = mm.FAMILIES          # ["A", "C", "H3"]
YEARS = list(range(2016, 2026))

_pools_cache: dict = {}


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def window_pool_era(df: pd.DataFrame, N: int, a: str, b: str) -> np.ndarray:
    """window_pool restricted to start bars in [a, b) — same formula."""
    o = df["Open"].to_numpy()
    c = df["Close"].to_numpy()
    n = len(df)
    i = np.arange(0, n - N)
    rets = c[i + N] / o[i + 1] - 1.0
    dates = df.index
    in_era = (dates >= pd.Timestamp(a)) & (dates < pd.Timestamp(b))
    return rets[in_era[i]]


def pools_for_era(N: int, era: str, universe_tickers):
    """Within-sub-era OOS window pools (same structure as build_pools)."""
    if (N, era) not in _pools_cache:
        a, b = ERAS[era]
        pools = {}
        for t in universe_tickers:
            if not (CACHE / "bars" / f"{t}.parquet").exists():
                continue
            pools[t] = window_pool_era(load_bars(t), N, a, b)
        random_pool = np.concatenate(list(pools.values())) - COST
        same_pool = {t: p - COST for t, p in pools.items()}
        spy_pool = window_pool_era(load_bars("SPY"), N, a, b)
        _pools_cache[(N, era)] = (pools, random_pool, same_pool, spy_pool)
    return _pools_cache[(N, era)]


def era_rows(family: str, N: int, a: str, b: str):
    """Entry returns within one sub-era (signal date in [a, b))."""
    rows, _ = mm.family_rows(family, N)
    return rows[(rows["signal_date"] >= a) & (rows["signal_date"] < b)]


def abs_era_block(family: str, N: int, era: str, universe_tickers, rng):
    """Absolute block within one sub-era: stats + within-era baselines."""
    a, b = ERAS[era]
    oos = era_rows(family, N, a, b)
    n_oos = len(oos)
    rets = oos["ret"].to_numpy()
    mean = float(rets.mean()) if n_oos else float("nan")
    med = float(np.median(rets)) if n_oos else float("nan")
    ci = [float(x) for x in np.percentile(rets, [2.5, 97.5])] if n_oos \
        else [float("nan")] * 2

    pools, random_pool, same_pool, spy_pool = pools_for_era(N, era,
                                                            universe_tickers)
    base_res = {}
    if n_oos:
        det_tickers = oos["ticker"].to_numpy()

        def sample_same(M, det_tickers=det_tickers, same_pool=same_pool, rng=rng):
            out = np.empty(M)
            for m in range(M):
                pool = same_pool[det_tickers[rng.integers(0, len(det_tickers))]]
                out[m] = pool[rng.integers(0, len(pool))]
            return out

        def sample_random(M, random_pool=random_pool, rng=rng):
            return random_pool[rng.integers(0, len(random_pool), size=M)]

        def sample_spy(M, spy_pool=spy_pool, rng=rng):
            return spy_pool[rng.integers(0, len(spy_pool), size=M)]

        base_res["random_entries"] = bootstrap_excess(rets, sample_random, rng)
        base_res["same_ticker"] = bootstrap_excess(rets, sample_same, rng)
        base_res["spy"] = bootstrap_excess(rets, sample_spy, rng)

    metrics = metric_cis_hyp(oos.sort_values("signal_date"), rng, N) if n_oos else None
    return {"n_oos": int(n_oos), "mean": mean, "median": med, "ci": ci,
            "metrics": metrics,
            "excess": {k: (v[0], v[1], v[2], v[3], v[4]) if v else None
                       for k, v in base_res.items()},
            "p_vs_random": base_res["random_entries"][4] if base_res else 1.0,
            "p_vs_same_ticker": base_res["same_ticker"][4] if base_res else 1.0,
            "p_holm_input": max(base_res["random_entries"][4],
                                base_res["same_ticker"][4]) if base_res else 1.0}


def era_diff_block(family: str, universe_tickers, rng):
    """F1: two-sample bootstrap of excess_late - excess_early (N=20)."""
    late = era_rows(family, N, *ERAS["late"])
    early = era_rows(family, N, *ERAS["early"])
    retsL, retsE = late["ret"].to_numpy(), early["ret"].to_numpy()
    tickL, tickE = late["ticker"].to_numpy(), early["ticker"].to_numpy()
    poolsL = pools_for_era(N, "late", universe_tickers)
    poolsE = pools_for_era(N, "early", universe_tickers)
    rndL, rndE = poolsL[1], poolsE[1]
    sameL, sameE = poolsL[2], poolsE[2]
    ML, ME = len(retsL), len(retsE)

    def s_random(pool, M):
        return pool[rng.integers(0, len(pool), size=M)]

    def s_same(tickers, same_pool, M):
        out = np.empty(M)
        for m in range(M):
            p = same_pool[tickers[rng.integers(0, len(tickers))]]
            out[m] = p[rng.integers(0, len(p))]
        return out

    d_random = np.empty(B)
    d_same = np.empty(B)
    for b in range(B):
        excL_r = retsL[rng.integers(0, ML, ML)].mean() - s_random(rndL, ML).mean()
        excE_r = retsE[rng.integers(0, ME, ME)].mean() - s_random(rndE, ME).mean()
        d_random[b] = excL_r - excE_r
        excL_s = retsL[rng.integers(0, ML, ML)].mean() - s_same(tickL, sameL, ML).mean()
        excE_s = retsE[rng.integers(0, ME, ME)].mean() - s_same(tickE, sameE, ME).mean()
        d_same[b] = excL_s - excE_s

    def pack(d, point):
        lo, hi = np.percentile(d, [2.5, 97.5])
        p = 2.0 * min((d <= 0).mean(), (d >= 0).mean())
        # draw mean, per the bootstrap_excess reporting convention
        return {"diff": float(d.mean()), "point": float(point),
                "ci": [float(lo), float(hi)], "p": float(p)}

    point_r = (retsL.mean() - rndL.mean()) - (retsE.mean() - rndE.mean())
    p_r = 2.0 * min((d_random <= 0).mean(), (d_random >= 0).mean())
    p_s = 2.0 * min((d_same <= 0).mean(), (d_same >= 0).mean())
    return {"n_early": int(ME), "n_late": int(ML),
            "n_oos": int(min(ME, ML)),          # count floor: smaller sub-era
            "excess_early": float(retsE.mean() - rndE.mean()),
            "excess_late": float(retsL.mean() - rndL.mean()),
            "random": pack(d_random, point_r),
            "same": pack(d_same, point_r),
            "p_holm_input": max(p_r, p_s)}


def cont_diff_block(family: str, rng):
    """Sensitivity: paired N=20 vs N=5 diffs per sub-era and their diff."""
    out = {}
    d_late = d_early = None
    for era in ("early", "late"):
        a, b = ERAS[era]
        m5 = era_rows(family, N_PAIRED, a, b)[["ticker", "signal_date", "ret"]] \
            .rename(columns={"ret": "r5"})
        m20 = era_rows(family, N, a, b)[["ticker", "signal_date", "ret"]] \
            .rename(columns={"ret": "r20"})
        m = m5.merge(m20, on=["ticker", "signal_date"], how="inner")
        d = (m["r20"] - m["r5"]).to_numpy()
        out[era] = {"n_pairs": int(len(d)), "mean_diff": float(d.mean()),
                    "mean_r5": float(m["r5"].mean()),
                    "mean_r20": float(m["r20"].mean())}
        if era == "late":
            d_late = d
        else:
            d_early = d
    diffs = np.empty(B)
    ML, ME = len(d_late), len(d_early)
    for b in range(B):
        diffs[b] = d_late[rng.integers(0, ML, ML)].mean() \
            - d_early[rng.integers(0, ME, ME)].mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    out["diff_late_minus_early"] = {"diff": float(d_late.mean() - d_early.mean()),
                                    "ci": [float(lo), float(hi)], "p": float(p)}
    return out


def main() -> int:
    mm.det_shapes = pd.read_csv(DET_SHAPES)
    mm.h3_det = pd.read_csv(DET_PILLARS)
    mm.h3_det = mm.h3_det[mm.h3_det["hypothesis"] == "H3"].reset_index(drop=True)
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()
    rng = np.random.default_rng(SEED)

    # F1 — sub-era excess difference (late minus early), N=20
    f1 = {f: era_diff_block(f, universe, rng) for f in FAMILIES}

    # F2 — late-era absolute at N=20 vs within-era baselines
    f2 = {f: abs_era_block(f, N, "late", universe, rng) for f in FAMILIES}

    f1_edge = lambda r, rej: (rej and r["random"]["ci"][0] > 0
                              and r["same"]["ci"][0] > 0)
    f2_edge = lambda r, rej: (rej and r["excess"]["random_entries"][2] > 0
                              and r["excess"]["same_ticker"][2] > 0)
    f1_lines = mm.run_holm(f1, "p_holm_input", f1_edge)
    f2_lines = mm.run_holm(f2, "p_holm_input", f2_edge)

    # Sensitivities (exploratory, NO verdicts)
    sens = {"continuation_by_era": {f: cont_diff_block(f, rng) for f in FAMILIES},
            "early_absolute": {f: abs_era_block(f, N, "early", universe, rng)
                               for f in FAMILIES},
            "n40_by_era": {}, "per_year": {}, "dedupe20_by_era": {}}
    for f in FAMILIES:
        sens["n40_by_era"][f] = {
            era: {"n": int(len(era_rows(f, 40, *ERAS[era]))),
                  "mean": float(era_rows(f, 40, *ERAS[era])["ret"].mean())}
            for era in ("early", "late")}
        sens["per_year"][f] = {
            str(y): {"n": int(len(era_rows(f, N, f"{y}-01-01", f"{y + 1}-01-01"))),
                     "mean": float(era_rows(f, N, f"{y}-01-01", f"{y + 1}-01-01")["ret"].mean())}
            for y in YEARS}
    for era in ("early", "late"):
        a, b = ERAS[era]
        for f in FAMILIES:
            if f == "H3":
                dd = dedupe_20_hyp(mm.h3_det)
                rows, _ = measure_returns_hyp(dd, N)
                rows = rows[rows["hypothesis"] == "H3"]
            else:
                dd = dedupe_20(mm.det_shapes[mm.det_shapes["shape"] == f])
                rows, _ = mm.measure_returns(dd, N)
                rows = rows[rows["shape"] == f]
            era_dd = rows[(rows["signal_date"] >= a) & (rows["signal_date"] < b)]
            sens["dedupe20_by_era"][f"{f}_{era}"] = {
                "n": int(len(era_dd)), "mean": float(era_dd["ret"].mean())}

    results = {"meta": {
        "pre_reg": "#5", "primary_n": N, "paired_n": N_PAIRED,
        "cost": COST, "bootstrap": B, "seed": SEED, "alpha": ALPHA,
        "era_oos_start": ERA_OOS, "eras": ERAS, "universe": UNIVERSE_CSV.name,
        "detections": [DET_SHAPES.name, DET_PILLARS.name],
        "detections_sha256": {f.name: sha(f)[:16] for f in (DET_SHAPES, DET_PILLARS)},
        "measure_code_sha256": sha(Path(__file__))[:16],
        "measure_engine_sha256": "c7421fbf (frozen Phase-3 engine, imported)",
        "note": "verdict machinery runs on OOS only; within-sub-era baseline "
                "windows by start-bar date. F1 two-sample bootstrap of "
                "excess_late - excess_early; F2 late-era absolute. p_input = "
                "max(p_random, p_same). Random/same baselines pay COST; SPY raw.",
    }, "family1": f1, "family2": f2, "sensitivities": sens}

    RESULTS.write_bytes(json.dumps(results, indent=2).encode("utf-8"))

    report = ["# Per-decade drift report (pre-registration #5)", "",
              f"- Pre-registration #5 (frozen 2026-08-14): primary N={N}, "
              f"paired N={N_PAIRED}, cost {COST:.4f}, alpha {ALPHA}, "
              f"bootstrap {B} (seed {SEED})",
              f"- Era split: IS 2000-2015 / OOS 2016-2025, sub-eras "
              f"{ERAS['early'][0]}..{ERAS['early'][1]} (early) and "
              f"{ERAS['late'][0]}..{ERAS['late'][1]} (late), by signal date",
              f"- Inputs: {DET_SHAPES.name} ({len(mm.det_shapes)} rows) and "
              f"{DET_PILLARS.name} (H3 subset {len(mm.h3_det)} rows) — frozen",
              "- Two pre-registered verdict families, each Holm-corrected "
              "across A/C/H3 at alpha=0.05: F1 sub-era excess difference "
              "(late minus early, two-sample bootstrap); F2 late-era "
              "absolute vs within-sub-era baselines",
              "- Baselines are drawn only from bars whose start date falls "
              "in the same sub-era (era-matched at sub-era granularity); "
              "strategy and baselines pay 0.15% round-trip; SPY is raw.",
              "", "## Verdicts — Family 1: sub-era excess difference "
              "(2020-25 minus 2016-19, N=20)", ""]
    report += f1_lines
    report += ["", "## Verdicts — Family 2: late-era absolute at N=20 "
              "(within-sub-era baselines)", ""]
    report += f2_lines

    report += ["", "## Family 1 detail (two-sample bootstrap)", ""]
    for f in FAMILIES:
        r = f1[f]
        report += [f"### {f}",
                   f"n_early {r['n_early']} | n_late {r['n_late']} | "
                   f"excess_early {r['excess_early']:+.4f} | excess_late "
                   f"{r['excess_late']:+.4f}",
                   f"| baseline | diff (late - early) | 95% CI | p |",
                   f"|---|---|---|---|"]
        for k in ("random", "same"):
            v = r[k]
            report.append(f"| {k} | {v['diff']:+.4f} | "
                          f"{v['ci'][0]:+.4f}..{v['ci'][1]:+.4f} | "
                          f"{v['p']:.4f} |")

    report += ["", "## Family 2 detail (late-era absolute)", ""]
    for f in FAMILIES:
        r = f2[f]
        report += [f"### {f}", f"n={r['n_oos']} | mean {r['mean']:+.4f} "
                   f"(CI {r['ci'][0]:+.4f}..{r['ci'][1]:+.4f})",
                   "| baseline | mean excess | median excess | 95% CI | "
                   "p (two-sided) |", "|---|---|---|---|---|"]
        for k in ("random_entries", "same_ticker", "spy"):
            e = r["excess"][k]
            report.append(f"| {k} | {e[0]:+.4f} | {e[1]:+.4f} | "
                          f"{e[2]:+.4f}..{e[3]:+.4f} | {e[4]:.4f} |")
        if r["metrics"]:
            m = r["metrics"]
            report += ["", "| metric | estimate | 95% CI |", "|---|---|---|",
                       f"| hit rate | {m['hit'][0]:.3f} | "
                       f"{m['hit'][1]:.3f}..{m['hit'][2]:.3f} |",
                       f"| Sharpe (annualized, per-N) | {m['sharpe'][0]:.2f} | "
                       f"{m['sharpe'][1]:.2f}..{m['sharpe'][2]:.2f} |", ""]

    report += ["", "## Sensitivities (exploratory — NO verdicts)", ""]
    for f in FAMILIES:
        c = sens["continuation_by_era"][f]
        report.append(f"- Continuation {f}: early diff {c['early']['mean_diff']:+.4f} "
                      f"(n={c['early']['n_pairs']}) | late diff "
                      f"{c['late']['mean_diff']:+.4f} (n={c['late']['n_pairs']}) | "
                      f"late-early {c['diff_late_minus_early']['diff']:+.4f} "
                      f"(CI {c['diff_late_minus_early']['ci'][0]:+.4f}.."
                      f"{c['diff_late_minus_early']['ci'][1]:+.4f}, "
                      f"p {c['diff_late_minus_early']['p']:.4f})")
    for f in FAMILIES:
        e = sens["early_absolute"][f]
        report.append(f"- Early-era absolute {f}: n={e['n_oos']} mean "
                      f"{e['mean']:+.4f} (vs random {e['excess']['random_entries'][0]:+.4f}, "
                      f"p {e['p_holm_input']:.4f})")
    for f in FAMILIES:
        n40 = sens["n40_by_era"][f]
        report.append(f"- N=40 {f}: early {n40['early']['mean']:+.4f} (n="
                      f"{n40['early']['n']}) | late {n40['late']['mean']:+.4f} "
                      f"(n={n40['late']['n']})")
    report.append("- Per-year N=20 means: " + " | ".join(
        f"{y}: " + ", ".join(f"{f} {sens['per_year'][f][str(y)]['mean']:+.3f}"
                             for f in FAMILIES) for y in YEARS))
    report.append("- Dedupe-20 by sub-era: " + " | ".join(
        f"{k}: n={v['n']} mean {v['mean']:+.4f}"
        for k, v in sens["dedupe20_by_era"].items()))

    report += ["", "## Reproducibility", "",
               "`python -X utf8 tools/measure_decade.py` regenerates this "
               "report; the seed is fixed, so bootstrap results are stable "
               "across runs.",
               "Input fingerprints: " + ", ".join(
                   f"{f.name} {sha(f)[:16]}…" for f in (DET_SHAPES, DET_PILLARS)) +
               f", decade code {sha(Path(__file__))[:16]}…, measure code "
               "c7421fbf… (Phase-3 engine imported unchanged).",
               "Any change to the detector, data, or measurement code changes "
               "the frozen inputs and requires a new pre-registration before "
               "it can drive a verdict."]

    REPORT.write_bytes(("\n".join(report) + "\n").encode("utf-8"))
    print(f"wrote {RESULTS.name} and {REPORT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
