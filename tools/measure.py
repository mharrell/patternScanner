"""Phase 3: measurement engine (pre-reg #1 §3 protocol, pre-reg #2 §5 rules).

For every detection at signal bar t: entry at open of t+1, exit at close of
t+N, return (c_{t+N} - o_{t+1}) / o_{t+1} - COST. No look-ahead (t+1 is the
first tradable bar). Primary N = 10 (frozen); N = 5/20 are exploratory.
Detections whose exit bar lies beyond the end of the ticker's series are
dropped and counted (n_dropped).

Baselines (bootstrap B = 1,000, fixed seed; all verdict machinery runs on
OOS, so baseline windows are drawn from OOS bars only — era-matched):
  1. random entries   — a random N-bar window of a random universe ticker
  2. SPY buy-and-hold — a random N-bar window of SPY, NO cost (market
     benchmark: raw return; the strategy pays COST, the benchmark does not)
  3. same-ticker B&H  — a random N-bar window of the detection's own ticker
Baselines 1 and 3 are cost-adjusted (they are trades); SPY is raw.

Per shape, per bootstrap resample: shape_mean_b - baseline_mean_b over the
M OOS detections -> distribution of the excess. Report mean and median
excess, 95% percentile CI, two-sided bootstrap p.

Metrics (with bootstrap percentile CIs): mean, median, hit rate, Sharpe
(annualized x sqrt(252/N)), maxDD on the trade-equity curve ordered by
signal date (approximate by design — no capital constraints).

Verdicts (pre-reg #2 §5, OOS only, primary N = 10):
  Edge         — Holm-corrected excess vs BOTH random-entries AND
                 same-ticker excludes 0 (positive), with >= 100 detections
  No edge      — mean excess <= 0 or CI includes 0, >= 100 detections
  Inconclusive — < 100 detections
Holm across A/B/C at alpha = 0.05 (k = 3), input p = max(p_random, p_same).

Outputs:
  data/cache/measure_results.json   (canonical, machine-readable)
  data/cache/measure_report.md      (per-shape tables + verdicts)
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
BARS_DIR = CACHE / "bars"
UNIVERSE_CSV = CACHE / "universe_sp600_2026-08-13.csv"
DET_CSV = CACHE / "detections_v1.csv"
RESULTS = CACHE / "measure_results.json"
REPORT = CACHE / "measure_report.md"

COST = 0.0015          # round-trip, deducted from every strategy trade
B = 1000               # bootstrap resamples
SEED = 20260813        # fixed: report is reproducible
ALPHA = 0.05
HORIZONS = {"primary": 10, "exploratory": [5, 20]}
ERA_OOS = "2016-01-01"
TRADING_DAYS = 252

_bars_cache: dict = {}
_loc_cache: dict = {}


def load_bars(ticker: str) -> pd.DataFrame:
    if ticker not in _bars_cache:
        df = pd.read_parquet(BARS_DIR / f"{ticker}.parquet",
                             columns=["Open", "Close"])
        df.index = pd.to_datetime(df.index)
        _bars_cache[ticker] = df
    return _bars_cache[ticker]


def loc_map(ticker: str) -> dict:
    """Timestamp -> bar index, built once per ticker."""
    if ticker not in _loc_cache:
        _loc_cache[ticker] = {ts: i for i, ts in enumerate(load_bars(ticker).index)}
    return _loc_cache[ticker]


def window_pool(df: pd.DataFrame, N: int) -> np.ndarray:
    """OOS-only N-bar window returns c[i+N]/o[i+1] - 1 for start bars i."""
    o = df["Open"].to_numpy()
    c = df["Close"].to_numpy()
    n = len(df)
    i = np.arange(0, n - N)                     # start bars 0..n-N-1
    rets = c[i + N] / o[i + 1] - 1.0
    dates = df.index
    oos = dates >= pd.Timestamp(ERA_OOS)
    return rets[oos[i]]


def bootstrap_excess(shape_rets: np.ndarray, sample_base, rng):
    """Paired bootstrap of shape_mean - baseline_mean.

    sample_base(M) returns M baseline returns (one per detection).
    Returns (mean_diff, median_diff, ci_low, ci_high, p_two_sided).
    """
    M = len(shape_rets)
    diffs = np.empty(B)
    for b in range(B):
        s_mean = shape_rets[rng.integers(0, M, size=M)].mean()
        diffs[b] = s_mean - sample_base(M).mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return float(diffs.mean()), float(np.median(diffs)), float(lo), float(hi), float(p)


def metric_cis(oos: pd.DataFrame, rng) -> dict:
    """Bootstrap CIs for hit rate, Sharpe, maxDD.

    rets is date-sorted (by signal_date). Each resample draws trades with
    replacement and re-sorts them by signal date, so the maxDD curve keeps
    its chronological definition across resamples.
    """
    rets = oos["ret"].to_numpy()
    M = len(rets)
    hits, sharpes, dds = np.empty(B), np.empty(B), np.empty(B)
    for b in range(B):
        idx = rng.integers(0, M, size=M)
        r = rets[idx]
        hits[b] = (r > 0).mean()
        std = r.std(ddof=1)
        sharpes[b] = r.mean() / std * np.sqrt(TRADING_DAYS / HORIZONS["primary"]) if std > 0 else np.nan
        eq = np.cumprod(1 + rets[np.sort(idx)])  # chronological trade curve
        dds[b] = (eq / np.maximum.accumulate(eq) - 1).min()
    lo, hi = np.percentile(hits, [2.5, 97.5])
    s_lo, s_hi = np.percentile(sharpes[~np.isnan(sharpes)], [2.5, 97.5])
    d_lo, d_hi = np.percentile(dds, [2.5, 97.5])
    # point estimate on the actual OOS trade curve, ordered by signal date
    eq = np.cumprod(1 + rets)
    dd_point = float((eq / np.maximum.accumulate(eq) - 1).min())
    return {"hit": [float(hits.mean()), float(lo), float(hi)],
            "sharpe": [float(np.nanmean(sharpes)), float(s_lo), float(s_hi)],
            "max_dd": [dd_point, float(d_lo), float(d_hi)]}


def measure_returns(det: pd.DataFrame, N: int):
    """Per-detection forward returns (entry open t+1, exit close t+N, -COST).

    Returns (rows, dropped) where dropped counts detections whose exit bar
    lies beyond the end of the ticker's series.
    """
    rows = []
    dropped = {"A": 0, "B": 0, "C": 0}
    for _, r in det.iterrows():
        loc = loc_map(r["ticker"]).get(pd.Timestamp(r["signal_date"]))
        if loc is None:
            continue  # signal date absent from bars — cannot happen, guarded
        df = load_bars(r["ticker"])
        if loc + N >= len(df):
            dropped[r["shape"]] += 1
            continue
        o = df["Open"].iloc[loc + 1]
        c_exit = df["Close"].iloc[loc + N]
        rows.append({"shape": r["shape"], "ticker": r["ticker"],
                     "signal_date": r["signal_date"],
                     "is_oos": r["signal_date"] >= ERA_OOS,
                     "ret": float(c_exit / o - 1.0 - COST)})
    return pd.DataFrame(rows), dropped


def dedupe_20(det: pd.DataFrame) -> pd.DataFrame:
    """Exploratory sensitivity: one detection per ticker per 20-bar window.

    Pre-reg #1 §3 sensitivity list (inherited by #2 §5 "identical protocol"):
    chronological greedy per (shape, ticker) — keep a detection only if at
    least 20 bars have passed since the last kept one.
    """
    keep = []
    last_loc = {}
    for _, r in det.sort_values("signal_date").iterrows():
        key = (r["shape"], r["ticker"])
        loc = loc_map(r["ticker"])[pd.Timestamp(r["signal_date"])]
        prev = last_loc.get(key)
        if prev is None or loc - prev >= 20:
            keep.append(r)
            last_loc[key] = loc
    return pd.DataFrame(keep)


def main() -> int:
    det = pd.read_csv(DET_CSV)
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()
    rng = np.random.default_rng(SEED)
    N = HORIZONS["primary"]

    # OOS window-return pools, once (per ticker), for the baselines.
    pools = {}
    for t in universe:
        if not (BARS_DIR / f"{t}.parquet").exists():
            print(f"note: {t} has no bars (4 known no-data tickers) — skipped in random pool")
            continue
        pools[t] = window_pool(load_bars(t), N)
    random_pool = np.concatenate(list(pools.values())) - COST      # a trade: pays cost
    same_pool = {t: p - COST for t, p in pools.items()}
    spy_pool = window_pool(load_bars("SPY"), N)                    # market benchmark: raw

    shape_rows, dropped_all = measure_returns(det, N)

    results = {"meta": {
        "pre_reg": "#2", "primary_n": N, "cost": COST, "bootstrap": B,
        "seed": SEED, "alpha": ALPHA, "era_oos_start": ERA_OOS,
        "universe": UNIVERSE_CSV.name,
        "detections": DET_CSV.name,
        "detections_sha256": hashlib.sha256(DET_CSV.read_bytes()).hexdigest(),
        "measure_code_sha256": hashlib.sha256(
            Path(__file__).read_bytes()).hexdigest(),
        "note": "verdict machinery runs on OOS only; IS is record only. "
                "Random-entries and same-ticker baselines pay COST; SPY is raw.",
    }, "shapes": {}, "sensitivities": {}}

    shapes = "ABC"
    verdict_lines = []
    report = ["# Phase 3 measurement report", "",
              f"- Pre-registration #2 (frozen 2026-08-13): N={N}, cost {COST:.4f}, "
              f"alpha {ALPHA}, bootstrap {B} (seed {SEED})",
              f"- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date; an exit "
              f"crossing the boundary is attributed to the signal date)",
              f"- Detections: {DET_CSV.name} ({len(det)} rows) — "
              f"dropped (exit beyond series end): {json.dumps(dropped_all)}",
              f"- Verdicts use OOS only; baseline windows are drawn from OOS bars "
              f"only (era-matched).",
              f"- The strategy pays {COST:.2%} round-trip; random-entries and "
              f"same-ticker baselines pay it too; SPY buy-and-hold is raw "
              f"(market benchmark).",
              f"- Max drawdown: trade-equity curve ordered by signal date, "
              f"cumprod(1+ret), no capital constraints — approximate by design.",
              "", "## Verdicts (OOS 2016-2025, primary N)", ""]

    for s in shapes:
        sub = shape_rows[shape_rows["shape"] == s]
        oos = sub[sub["is_oos"]]
        n_oos = len(oos)
        rets = oos["ret"].to_numpy()
        mean = float(rets.mean()) if n_oos else float("nan")
        med = float(np.median(rets)) if n_oos else float("nan")
        ci = [float(x) for x in np.percentile(rets, [2.5, 97.5])] if n_oos else [float("nan")] * 2

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

        metrics = metric_cis(oos.sort_values("signal_date"), rng) if n_oos else None

        p_rand = base_res["random_entries"][4] if base_res else 1.0
        p_same = base_res["same_ticker"][4] if base_res else 1.0
        p_shape = max(p_rand, p_same)
        results["shapes"][s] = {
            "n_total": int(len(sub)), "n_oos": int(n_oos),
            "mean": mean, "median": med, "ci": ci, "metrics": metrics,
            "excess": {k: (v[0], v[1], v[2], v[3], v[4]) if v else None
                       for k, v in base_res.items()},
            "p_vs_random": p_rand, "p_vs_same_ticker": p_same,
            "p_holm_input": p_shape,
        }

    # Holm across A/B/C
    order = sorted(shapes, key=lambda s: results["shapes"][s]["p_holm_input"])
    for i, s in enumerate(order):
        k = len(order)
        r = results["shapes"][s]
        gate = ALPHA / (k - i)
        rejected = r["p_holm_input"] <= gate
        if r["n_oos"] < 100:
            verdict = "INCONCLUSIVE (<100 detections)"
        elif rejected and r["excess"]["random_entries"][2] > 0 \
                and r["excess"]["same_ticker"][2] > 0:
            verdict = "EDGE (Holm-rejected; excess vs random AND same-ticker excludes 0)"
        else:
            verdict = "NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)"
        r["holm_gate"] = gate
        r["holm_rejected"] = bool(rejected)
        r["verdict"] = verdict
        verdict_lines.append(
            f"- **{s}**: n={r['n_oos']} | mean {r['mean']:+.4f} "
            f"(CI {r['ci'][0]:+.4f}..{r['ci'][1]:+.4f}) | p {r['p_holm_input']:.4f} "
            f"(Holm gate {gate:.4f}) -> **{verdict}**")

    report += verdict_lines + ["", "## Per-shape detail (OOS, primary N)", ""]
    for s in shapes:
        r = results["shapes"][s]
        m = r["metrics"] or {}
        line = (f"### Shape {s}\n\n"
                f"n={r['n_oos']} (of {r['n_total']} total) | mean {r['mean']:+.4f} "
                f"(95% CI {r['ci'][0]:+.4f}..{r['ci'][1]:+.4f}) | median {r['median']:+.4f}\n\n"
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

    # IS record + per-decade breakdown (record only, no verdicts)
    report += ["", "## IS record (2000-2015) — observation only, no verdicts", "",
               "| shape | n | mean | median | hit rate |", "|---|---|---|---|---|"]
    for s in shapes:
        d = shape_rows[(shape_rows["shape"] == s) & (~shape_rows["is_oos"])]["ret"]
        if len(d):
            report.append(f"| {s} | {len(d)} | {d.mean():+.4f} | "
                          f"{d.median():+.4f} | {(d > 0).mean():.3f} |")
    report += ["", "## Per-decade breakdown (all detections, record only)", "",
               "| shape | decade | n | mean | hit rate |", "|---|---|---|---|---|"]
    shape_rows["decade"] = shape_rows["signal_date"].str[:3] + "0s"
    for s in shapes:
        for dec in ["2000s", "2010s", "2020s"]:
            d = shape_rows[(shape_rows["shape"] == s) & (shape_rows["decade"] == dec)]
            if len(d):
                report.append(f"| {s} | {dec} | {len(d)} | {d['ret'].mean():+.4f} "
                              f"| {(d['ret'] > 0).mean():.3f} |")

    # Sensitivities (exploratory — NO verdicts, no Holm slots)
    report += ["", "## Sensitivities (exploratory — NO verdicts)", ""]
    for n_h in HORIZONS["exploratory"]:
        rr, dropped_n = measure_returns(det, n_h)
        oos = rr[rr["is_oos"]]
        report.append(f"- N={n_h} (dropped {json.dumps(dropped_n)}): OOS n="
                      f"{len(oos)}")
        for s in shapes:
            d = oos[oos["shape"] == s]["ret"]
            if len(d):
                report.append(f"  - {s}: n={len(d)}, mean {d.mean():+.4f}, "
                              f"hit {(d > 0).mean():.3f}")
    kept = dedupe_20(det)
    kr, dropped_k = measure_returns(kept, N)
    ko = kr[kr["is_oos"]]
    results["sensitivities"]["cap20"] = {
        "n_kept": int(len(kept)), "dropped": dropped_k,
        "n_oos": int(len(ko))}
    report.append(f"- One detection per ticker per 20-bar window (pre-reg #1 §3 "
                  f"sensitivity; kept {len(kept)} of {len(det)} detections, "
                  f"dropped {json.dumps(dropped_k)} unmeasurable):")
    for s in shapes:
        d = ko[ko["shape"] == s]["ret"]
        if len(d):
            report.append(f"  - {s}: n={len(d)}, mean {d.mean():+.4f}, "
                          f"hit {(d > 0).mean():.3f}")

    report += ["", "## Reproducibility", "",
               "`python -X utf8 tools/measure.py` regenerates this report; the "
               "seed is fixed, so bootstrap results are stable across runs.",
               "Input fingerprints: detections "
               f"{results['meta']['detections_sha256'][:12]}…, measure code "
               f"{results['meta']['measure_code_sha256'][:12]}….",
               "Any change to the detector, data, or measurement code changes "
               "the frozen inputs and requires a new pre-registration before it "
               "can drive a verdict.", ""]

    REPORT.write_text("\n".join(report), encoding="utf-8")
    RESULTS.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("report -> data/cache/measure_report.md")
    print("results -> data/cache/measure_results.json")
    for line in verdict_lines:
        print(line.replace("**", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
