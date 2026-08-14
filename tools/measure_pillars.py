"""Pillar measurement for pre-registration #1 (H1-H3), frozen 2026-08-13.

Imports the engine pieces from measure.py (Phase 3, sha c7421fbf... frozen —
NOT modified): COST, B, SEED, ALPHA, ERA_OOS, TRADING_DAYS, load_bars,
loc_map, window_pool, bootstrap_excess. Local copies, keyed on "hypothesis"
and with the N=1 annualization factor, are provided for:

  measure_returns_hyp / dedupe_20_hyp / metric_cis_hyp

because measure.py's versions are keyed on "shape" and metric_cis
hardcodes HORIZONS["primary"]=10 for Sharpe annualization. The copies are
byte-identical in logic except for the key and the factor.

Protocol (pre-reg #1 §3-4):
  - primary N = 1: entry open of t+1, exit close of t+1 (same bar),
    (c_{t+1} - o_{t+1}) / o_{t+1} - COST. Sensitivities N=3/5/10, the
    high-based trigger and the $2-10 price range at N=1, and the 20-bar
    per-ticker dedupe at N=1 — all exploratory, no verdicts.
  - baselines (bootstrap B=1000, seed 20260813; OOS-only windows so they
    are era-matched): random entries (-COST), same-ticker B&H (-COST),
    SPY B&H (raw).
  - verdicts on OOS only, Holm across H1/H2/H3 at alpha=0.05, input p =
    max(p_random, p_same); Edge needs Holm rejection AND CI-low > 0 vs
    BOTH baselines AND >= 100 detections. Hypotheses with zero OOS
    detections enter the Holm family at p=1.0 (non-rejections).
  - H3 direct claim test (reported, NOT Holm-gated): day-paired
    rank-1 vs rank-2..10 cohort, paired bootstrap over OOS days.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import (COST, B, SEED, ALPHA, ERA_OOS, TRADING_DAYS,
                     load_bars, loc_map, window_pool, bootstrap_excess)

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
BARS_DIR = CACHE / "bars"
UNIVERSE_CSV = CACHE / "universe_sp600_2026-08-13.csv"
DET = CACHE / "pillar_detections_v1.csv"
DET_HIGH = CACHE / "pillar_detections_v1_high.csv"
DET_R210 = CACHE / "pillar_detections_v1_r210.csv"
COHORTS = CACHE / "pillar_h3cohorts_v1.csv"
RESULTS = CACHE / "pillar_measure_results.json"
REPORT = CACHE / "pillar_measure_report.md"

HYPOTHESES = ["H1", "H2", "H3"]
SENS_N = [3, 5, 10]


def measure_returns_hyp(det: pd.DataFrame, N: int):
    """measure.py's measure_returns keyed on "hypothesis" (same logic)."""
    rows = []
    dropped = {h: 0 for h in HYPOTHESES}
    for _, r in det.iterrows():
        loc = loc_map(r["ticker"]).get(pd.Timestamp(r["signal_date"]))
        if loc is None:
            continue
        df = load_bars(r["ticker"])
        if loc + N >= len(df):
            dropped[r["hypothesis"]] += 1
            continue
        o = df["Open"].iloc[loc + 1]
        c_exit = df["Close"].iloc[loc + N]
        rows.append({"hypothesis": r["hypothesis"], "ticker": r["ticker"],
                     "signal_date": r["signal_date"],
                     "is_oos": r["signal_date"] >= ERA_OOS,
                     "ret": float(c_exit / o - 1.0 - COST)})
    return pd.DataFrame(rows), dropped


def dedupe_20_hyp(det: pd.DataFrame) -> pd.DataFrame:
    """measure.py's dedupe_20 keyed on (hypothesis, ticker)."""
    keep = []
    last_loc = {}
    for _, r in det.sort_values("signal_date").iterrows():
        key = (r["hypothesis"], r["ticker"])
        loc = loc_map(r["ticker"])[pd.Timestamp(r["signal_date"])]
        prev = last_loc.get(key)
        if prev is None or loc - prev >= 20:
            keep.append(r)
            last_loc[key] = loc
    return pd.DataFrame(keep)


def metric_cis_hyp(oos: pd.DataFrame, rng, N: int) -> dict:
    """measure.py's metric_cis with per-N Sharpe annualization (x sqrt(252/N))."""
    rets = oos["ret"].to_numpy()
    M = len(rets)
    hits, sharpes, dds = np.empty(B), np.empty(B), np.empty(B)
    for b in range(B):
        idx = rng.integers(0, M, size=M)
        r = rets[idx]
        hits[b] = (r > 0).mean()
        std = r.std(ddof=1)
        sharpes[b] = r.mean() / std * np.sqrt(TRADING_DAYS / N) if std > 0 else np.nan
        eq = np.cumprod(1 + rets[np.sort(idx)])
        dds[b] = (eq / np.maximum.accumulate(eq) - 1).min()
    lo, hi = np.percentile(hits, [2.5, 97.5])
    s_lo, s_hi = np.percentile(sharpes[~np.isnan(sharpes)], [2.5, 97.5])
    d_lo, d_hi = np.percentile(dds, [2.5, 97.5])
    eq = np.cumprod(1 + rets)
    dd_point = float((eq / np.maximum.accumulate(eq) - 1).min())
    return {"hit": [float(hits.mean()), float(lo), float(hi)],
            "sharpe": [float(np.nanmean(sharpes)), float(s_lo), float(s_hi)],
            "max_dd": [dd_point, float(d_lo), float(d_hi)]}


def build_pools(N: int, universe_tickers):
    """OOS-only N-bar window pools, same construction as measure.py main()."""
    pools = {}
    for t in universe_tickers:
        if not (BARS_DIR / f"{t}.parquet").exists():
            continue
        pools[t] = window_pool(load_bars(t), N)
    random_pool = np.concatenate(list(pools.values())) - COST
    same_pool = {t: p - COST for t, p in pools.items()}
    spy_pool = window_pool(load_bars("SPY"), N)
    return pools, random_pool, same_pool, spy_pool


def cohort_paired(cohorts: pd.DataFrame, rng: np.random.Generator, N: int) -> dict:
    """H3 direct claim test: day-paired rank-1 vs rank-2..10 on OOS days.

    Per OOS day: r1 = rank-1 return, r210 = mean of ranks 2-10 returns,
    diff = r1 - r210. Paired bootstrap over days (resample days, mean of
    diffs). Reported, not Holm-gated (secondary analysis within H3).
    """
    rows = []
    dropped = 0
    for _, r in cohorts.iterrows():
        loc = loc_map(r["ticker"]).get(pd.Timestamp(r["signal_date"]))
        if loc is None:
            continue
        df = load_bars(r["ticker"])
        if loc + N >= len(df):
            dropped += 1
            continue
        o = df["Open"].iloc[loc + 1]
        c_exit = df["Close"].iloc[loc + N]
        rows.append({"rank": int(r["rank"]), "signal_date": r["signal_date"],
                     "ret": float(c_exit / o - 1.0 - COST)})
    rr = pd.DataFrame(rows)
    oos = rr[rr["signal_date"] >= ERA_OOS]
    oos["ret"] = oos["ret"].astype(float)

    r1 = oos[oos["rank"] == 1].groupby("signal_date")["ret"].mean()
    r210 = oos[oos["rank"] >= 2].groupby("signal_date")["ret"].mean()
    days = r1.index.intersection(r210.index)
    r1, r210 = r1.loc[days], r210.loc[days]
    diff = (r1 - r210).to_numpy()
    n_days = len(diff)
    diffs = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n_days, size=n_days)
        diffs[b] = diff[idx].mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return {"n_days": int(n_days), "dropped": int(dropped),
            "rank1_day_mean": float(r1.mean()), "r210_day_mean": float(r210.mean()),
            "paired_diff_mean": float(diff.mean()), "ci": [float(lo), float(hi)],
            "p_two_sided": float(p),
            "hit_rate_r1": float((r1 > 0).mean()), "hit_rate_r210": float((r210 > 0).mean())}


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def verdict_block(sub, pools_pkg, rng, N):
    """Per-hypothesis OOS analysis + baselines; returns results dict + lines."""
    oos = sub[sub["is_oos"]]
    n_oos = len(oos)
    rets = oos["ret"].to_numpy()
    mean = float(rets.mean()) if n_oos else float("nan")
    med = float(np.median(rets)) if n_oos else float("nan")
    ci = [float(x) for x in np.percentile(rets, [2.5, 97.5])] if n_oos else [float("nan")] * 2

    pools, random_pool, same_pool, spy_pool = pools_pkg
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
    p_rand = base_res["random_entries"][4] if base_res else 1.0
    p_same = base_res["same_ticker"][4] if base_res else 1.0
    return {"n_total": int(len(sub)), "n_oos": int(n_oos),
            "mean": mean, "median": med, "ci": ci, "metrics": metrics,
            "excess": {k: (v[0], v[1], v[2], v[3], v[4]) if v else None
                       for k, v in base_res.items()},
            "p_vs_random": p_rand, "p_vs_same_ticker": p_same,
            "p_holm_input": max(p_rand, p_same)}


def main() -> int:
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()
    rng = np.random.default_rng(SEED)
    N = 1  # pre-reg #1 primary

    det = pd.read_csv(DET)
    det_high = pd.read_csv(DET_HIGH)
    det_r210 = pd.read_csv(DET_R210)
    cohorts = pd.read_csv(COHORTS)

    pools_pkg = build_pools(N, universe)
    shape_rows, dropped_all = measure_returns_hyp(det, N)

    results = {"meta": {
        "pre_reg": "#1", "primary_n": N, "cost": COST, "bootstrap": B,
        "seed": SEED, "alpha": ALPHA, "era_oos_start": ERA_OOS,
        "universe": UNIVERSE_CSV.name,
        "detections": [f.name for f in (DET, DET_HIGH, DET_R210)],
        "detections_sha256": {f.name: sha(f)[:16] for f in (DET, DET_HIGH, DET_R210)},
        "cohorts": COHORTS.name, "cohorts_sha256": sha(COHORTS)[:16],
        "measure_code_sha256": sha(Path(__file__))[:16],
        "measure_engine_sha256": "c7421fbf (frozen Phase-3 engine, imported)",
        "note": "verdict machinery runs on OOS only; IS is record only. "
                "H1/H2 had zero OOS detections and enter the Holm family at "
                "p=1.0 (non-rejections). Random-entries and same-ticker "
                "baselines pay COST; SPY is raw.",
    }, "hypotheses": {}, "h3_cohort_test": {}, "sensitivities": {}}

    hyps = {}
    for h in HYPOTHESES:
        sub = shape_rows[shape_rows["hypothesis"] == h]
        hyps[h] = verdict_block(sub, pools_pkg, rng, N)
    results["hypotheses"] = hyps

    results["h3_cohort_test"] = cohort_paired(cohorts, rng, N)

    # Holm across H1/H2/H3 (untestable -> p=1.0)
    order = sorted(HYPOTHESES, key=lambda h: hyps[h]["p_holm_input"])
    verdict_lines = []
    for i, h in enumerate(order):
        k = len(order)
        r = hyps[h]
        gate = ALPHA / (k - i)
        rejected = r["p_holm_input"] <= gate
        if r["n_oos"] < 100:
            verdict = "INCONCLUSIVE (<100 OOS detections)"
        elif rejected and r["excess"]["random_entries"][2] > 0 \
                and r["excess"]["same_ticker"][2] > 0:
            verdict = "EDGE (Holm-rejected; excess vs random AND same-ticker excludes 0)"
        else:
            verdict = "NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)"
        r["holm_gate"] = gate
        r["holm_rejected"] = bool(rejected)
        r["verdict"] = verdict
        verdict_lines.append(
            f"- **{h}**: n={r['n_oos']} | mean {r['mean']:+.4f} "
            f"(CI {r['ci'][0]:+.4f}..{r['ci'][1]:+.4f}) | p {r['p_holm_input']:.4f} "
            f"(Holm gate {gate:.4f}) -> **{verdict}**")

    c = results["h3_cohort_test"]
    cohort_lines = [
        f"- OOS days paired: {c['n_days']} (ranks 2-10 present on all; "
        f"{c['dropped']} cohort rows dropped at series end)",
        f"- rank-1 day-mean {c['rank1_day_mean']:+.4f} vs ranks 2-10 "
        f"{c['r210_day_mean']:+.4f} | paired diff {c['paired_diff_mean']:+.4f} "
        f"(95% CI {c['ci'][0]:+.4f}..{c['ci'][1]:+.4f}), p={c['p_two_sided']:.4f}",
        f"- hit rate rank-1 {c['hit_rate_r1']:.3f} vs ranks 2-10 {c['hit_rate_r210']:.3f}"]

    report = ["# Pillar measurement report (pre-registration #1)", "",
              f"- Pre-registration #1 (frozen 2026-08-13): primary N={N}, "
              f"cost {COST:.4f}, alpha {ALPHA}, bootstrap {B} (seed {SEED})",
              f"- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)",
              f"- Detections: {DET.name} ({len(det)} rows) — dropped (exit "
              f"beyond series end): {json.dumps(dropped_all)}",
              f"- Cohorts (H3 direct claim test): {COHORTS.name} ({len(cohorts)} rows)",
              f"- Verdicts use OOS only; baseline windows are drawn from OOS "
              f"bars only (era-matched).",
              f"- The strategy pays {COST:.2%} round-trip; random-entries and "
              f"same-ticker baselines pay it too; SPY buy-and-hold is raw "
              f"(market benchmark).",
              f"- Operationalization (frozen in pillars.py): close-to-close "
              f"gain leg ('still up at close' — the stronger subset per the "
              f"translation table); rank over the full frozen universe "
              f"(stricter than his pre-filtered scanner universe — documented, "
              f"not adjusted); float = frozen snapshot "
              f"(DESIGN_BRIEF §9 row 7 (a)); signals on a ticker's last bar "
              f"skipped.",
              f"- H1/H2 fired 7/6 times in 26 years across 599 tickers, all in "
              f"IS (2000-2010) — too rare to test; they enter the Holm family "
              f"at p=1.0 and are Inconclusive by the >=100-detection floor.",
              "", "## Verdicts (OOS 2016-2025, primary N=1)", ""] + verdict_lines

    report += ["", "## H3 direct claim test — day-paired rank-1 vs rank-2..10 "
                   "(OOS)", ""] + cohort_lines + [
               "", "*Reported, not Holm-gated: secondary analysis within H3.*"]

    report += ["", "## Per-hypothesis detail (OOS, primary N=1)", ""]
    for h in HYPOTHESES:
        r = hyps[h]
        if r["n_oos"] == 0:
            is_part = shape_rows[(shape_rows["hypothesis"] == h) &
                                 (~shape_rows["is_oos"])]["ret"]
            line = (f"### {h}\n\n"
                    f"n=0 OOS (of {r['n_total']} total) — no verdict possible; "
                    f"all detections fell in IS. IS record (record only): "
                    f"n={len(is_part)}, mean {is_part.mean():+.4f}, "
                    f"median {is_part.median():+.4f}, hit {(is_part > 0).mean():.3f}.\n")
            report.append(line)
            continue
        m = r["metrics"] or {}
        line = (f"### {h}\n\n"
                f"n={r['n_oos']} (of {r['n_total']} total) | mean {r['mean']:+.4f} "
                f"(95% CI {r['ci'][0]:+.4f}..{r['ci'][1]:+.4f}) | "
                f"median {r['median']:+.4f}\n\n"
                f"| metric | estimate | 95% CI |\n|---|---|---|\n")
        if m:
            line += (f"| hit rate | {m['hit'][0]:.3f} | {m['hit'][1]:.3f}..{m['hit'][2]:.3f} |\n"
                     f"| Sharpe (annualized) | {m['sharpe'][0]:.2f} | "
                     f"{m['sharpe'][1]:.2f}..{m['sharpe'][2]:.2f} |\n"
                     f"| max drawdown (trade curve) | {m['max_dd'][0]:.3f} | "
                     f"{m['max_dd'][1]:.3f}..{m['max_dd'][2]:.3f} |\n")
        line += ("\n| baseline | mean excess | median excess | 95% CI | p (two-sided) |\n"
                 "|---|---|---|---|---|\n")
        for name, v in r["excess"].items():
            if v:
                line += (f"| {name} | {v[0]:+.4f} | {v[1]:+.4f} | "
                         f"{v[2]:+.4f}..{v[3]:+.4f} | {v[4]:.4f} |\n")
        report.append(line)

    report += ["", "## IS record (2000-2015) — observation only, no verdicts", "",
               "| hypothesis | n | mean | median | hit rate |", "|---|---|---|---|---|"]
    for h in HYPOTHESES:
        d = shape_rows[(shape_rows["hypothesis"] == h) & (~shape_rows["is_oos"])]["ret"]
        if len(d):
            report.append(f"| {h} | {len(d)} | {d.mean():+.4f} | "
                          f"{d.median():+.4f} | {(d > 0).mean():.3f} |")

    # Sensitivities (exploratory — NO verdicts, no Holm slots)
    report += ["", "## Sensitivities (exploratory — NO verdicts)", ""]
    for n_h in SENS_N:
        rr, dropped_n = measure_returns_hyp(det, n_h)
        oos = rr[rr["is_oos"]]
        report.append(f"- N={n_h} (dropped {json.dumps(dropped_n)}): OOS n={len(oos)}")
        for h in HYPOTHESES:
            d = oos[oos["hypothesis"] == h]["ret"]
            if len(d):
                report.append(f"  - {h}: n={len(d)}, mean {d.mean():+.4f}, "
                              f"hit {(d > 0).mean():.3f}")
    for label, f in (("high trigger", DET_HIGH), ("$2-10 range", DET_R210)):
        rr, dropped_n = measure_returns_hyp(pd.read_csv(f), N)
        oos = rr[rr["is_oos"]]
        report.append(f"- {label} at N=1 (dropped {json.dumps(dropped_n)}): "
                      f"OOS n={len(oos)}")
        for h in HYPOTHESES:
            d = oos[oos["hypothesis"] == h]["ret"]
            if len(d):
                report.append(f"  - {h}: n={len(d)}, mean {d.mean():+.4f}, "
                              f"hit {(d > 0).mean():.3f}")
    kept = dedupe_20_hyp(det)
    kr, dropped_k = measure_returns_hyp(kept, N)
    ko = kr[kr["is_oos"]]
    results["sensitivities"]["cap20"] = {
        "n_kept": int(len(kept)), "dropped": dropped_k, "n_oos": int(len(ko))}
    report.append(f"- One detection per ticker per 20-bar window (pre-reg #1 "
                  f"sensitivity; kept {len(kept)} of {len(det)} detections, "
                  f"dropped {json.dumps(dropped_k)} unmeasurable):")
    for h in HYPOTHESES:
        d = ko[ko["hypothesis"] == h]["ret"]
        if len(d):
            report.append(f"  - {h}: n={len(d)}, mean {d.mean():+.4f}, "
                          f"hit {(d > 0).mean():.3f}")

    report += ["", "## Reproducibility", "",
               "`python -X utf8 tools/measure_pillars.py` regenerates this "
               "report; the seed is fixed, so bootstrap results are stable "
               "across runs.",
               "Input fingerprints: detections "
               + ", ".join(f"{k} {v}…" for k, v in
                           results["meta"]["detections_sha256"].items())
               + f", cohorts {results['meta']['cohorts_sha256']}…, "
               f"measure code {results['meta']['measure_code_sha256']}… "
               f"(Phase-3 engine c7421fbf… imported unchanged).",
               "Any change to the detector, data, or measurement code changes "
               "the frozen inputs and requires a new pre-registration before it "
               "can drive a verdict.", ""]

    REPORT.write_text("\n".join(report), encoding="utf-8")
    RESULTS.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("report -> data/cache/pillar_measure_report.md")
    print("results -> data/cache/pillar_measure_results.json")
    for line in verdict_lines:
        print(line.replace("**", ""))
    print("cohort test: paired diff %+.4f (p=%.4f)" % (c["paired_diff_mean"], c["p_two_sided"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
