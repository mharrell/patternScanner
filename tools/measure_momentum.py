"""Momentum horizon measurement for pre-registration #4, frozen 2026-08-14.

Reuses the frozen Phase-3 engine (tools/measure.py, sha c7421fbf..., NEVER
modified) for every shared piece: COST, B, SEED, ALPHA, ERA_OOS,
TRADING_DAYS, load_bars, loc_map, window_pool, bootstrap_excess,
measure_returns (shape-keyed), dedupe_20; and measure_pillars' build_pools,
measure_returns_hyp (hypothesis-keyed, used for H3), metric_cis_hyp
(per-N Sharpe annualization).

Two pre-registered verdict families, each Holm-corrected across its three
slots at alpha=0.05, OOS-only (2016-2025 by signal date):

  F1 absolute (N=20 primary): mean forward return of the entry set at N=20
     vs era-matched baselines — random entries and same-ticker buy-and-hold
     (both pay COST; SPY raw, reported not gating). p_input = max(p_random,
     p_same), identical to pre-regs #1-#3.
  F2 continuation: paired N=20 vs N=5 on IDENTICAL entries (per-entry
     d = r20 - r5), paired bootstrap over entries, two-sided p.

Entry sets: Shape A, Shape C, H3 rank-1 (pre-reg #4 section 2; Shape B is
exploratory-only by pre-registration, not by result). Sensitivities (no
verdicts): N=40, dedupe-20, per-decade OOS, Shape B at N=20.

Deterministic: fixed seed -> byte-identical outputs across runs.

Outputs: data/cache/momentum_measure_results.json + momentum_measure_report.md.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import (ALPHA, B, COST, ERA_OOS, SEED, TRADING_DAYS, load_bars,
                     loc_map, window_pool, bootstrap_excess, measure_returns,
                     dedupe_20)
from measure_pillars import (UNIVERSE_CSV, build_pools, measure_returns_hyp,
                             metric_cis_hyp, dedupe_20_hyp)

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
DET_SHAPES = CACHE / "detections_v1.csv"
DET_PILLARS = CACHE / "pillar_detections_v1.csv"
RESULTS = CACHE / "momentum_measure_results.json"
REPORT = CACHE / "momentum_measure_report.md"

N_PRIMARY = 20          # pre-reg #4 primary horizon
N_PAIRED = 5            # F2 comparator (paired on identical entries)
SENS_N = [40]
FAMILIES = ["A", "C", "H3"]          # primary slots (pre-reg #4 section 2)
DECADES = [("2016-2019", "2016-01-01", "2020-01-01"),
           ("2020-2025", "2020-01-01", "2026-01-01")]

det_shapes = None
h3_det = None
_pools_cache: dict = {}


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def pools_for(N: int, universe_tickers):
    """Era-matched OOS window pools at horizon N, built once per N."""
    if N not in _pools_cache:
        _pools_cache[N] = build_pools(N, universe_tickers)
    return _pools_cache[N]


def family_rows(family: str, N: int):
    """Per-detection forward returns for one entry family (entry o_{t+1} ->
    exit c_{t+N}, -COST). Returns (rows, dropped_count)."""
    if family == "H3":
        rows, dropped = measure_returns_hyp(h3_det, N)
        rows = rows[rows["hypothesis"] == "H3"].copy()
        rows["family"] = "H3"
    else:
        rows, dropped = measure_returns(det_shapes, N)
        rows = rows[rows["shape"] == family].copy()
        rows["family"] = family
    return rows, int(dropped[family])


def abs_block(family: str, N: int, universe_tickers, rng):
    """F1 machinery at horizon N: OOS stats + era-matched baselines."""
    rows, dropped = family_rows(family, N)
    oos = rows[rows["is_oos"]]
    n_oos = len(oos)
    rets = oos["ret"].to_numpy()
    mean = float(rets.mean()) if n_oos else float("nan")
    med = float(np.median(rets)) if n_oos else float("nan")
    ci = [float(x) for x in np.percentile(rets, [2.5, 97.5])] if n_oos \
        else [float("nan")] * 2

    pools, random_pool, same_pool, spy_pool = pools_for(N, universe_tickers)
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
    return {"n_total": int(len(rows)), "dropped": dropped, "n_oos": int(n_oos),
            "mean": mean, "median": med, "ci": ci, "metrics": metrics,
            "excess": {k: (v[0], v[1], v[2], v[3], v[4]) if v else None
                       for k, v in base_res.items()},
            "p_vs_random": base_res["random_entries"][4] if base_res else 1.0,
            "p_vs_same_ticker": base_res["same_ticker"][4] if base_res else 1.0,
            "p_holm_input": max(base_res["random_entries"][4],
                                base_res["same_ticker"][4]) if base_res else 1.0}


def cont_block(family: str, rng, N_long=N_PRIMARY, N_short=N_PAIRED):
    """F2 machinery: paired N_long vs N_short on identical entries, OOS only."""
    r_short, _ = family_rows(family, N_short)
    r_long, _ = family_rows(family, N_long)
    m = r_short[["ticker", "signal_date", "ret"]].rename(columns={"ret": "r_short"}) \
        .merge(r_long[["ticker", "signal_date", "ret"]].rename(columns={"ret": "r_long"}),
               on=["ticker", "signal_date"], how="inner")
    oos = m[m["signal_date"] >= ERA_OOS]
    d = (oos["r_long"] - oos["r_short"]).to_numpy()
    n = len(d)
    diffs = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, size=n)
        diffs[b] = d[idx].mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return {"n_pairs": int(n), "mean_r_short": float(oos["r_short"].mean()),
            "mean_r_long": float(oos["r_long"].mean()), "mean_diff": float(d.mean()),
            "ci": [float(lo), float(hi)], "p_two_sided": float(p)}


def run_holm(items, p_key, edge_fn):
    """Holm across the family dict {family: block} at alpha; verdict lines."""
    order = sorted(items, key=lambda f: items[f][p_key])
    lines = []
    for i, f in enumerate(order):
        gate = ALPHA / (len(order) - i)
        r = items[f]
        n = r["n_oos"] if "n_oos" in r else r["n_pairs"]
        rejected = r[p_key] <= gate
        if n < 100:
            verdict = "INCONCLUSIVE (<100 OOS detections)"
        elif edge_fn(r, rejected):
            verdict = "EDGE"
        else:
            verdict = "NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)"
        r["holm_gate"] = gate
        r["holm_rejected"] = bool(rejected)
        r["verdict"] = verdict
        lines.append(f"- **{f}**: n={n} | p {r[p_key]:.4f} "
                     f"(Holm gate {gate:.4f}) -> **{verdict}**")
    return lines


def main() -> int:
    global det_shapes, h3_det
    det_shapes = pd.read_csv(DET_SHAPES)
    h3_det = pd.read_csv(DET_PILLARS)
    h3_det = h3_det[h3_det["hypothesis"] == "H3"].reset_index(drop=True)
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()
    rng = np.random.default_rng(SEED)

    # F1 — absolute at N=20
    f1 = {f: abs_block(f, N_PRIMARY, universe, rng) for f in FAMILIES}

    # F2 — continuation (paired N=20 vs N=5)
    f2 = {f: cont_block(f, rng) for f in FAMILIES}

    f1_edge = lambda r, rej: (rej and r["excess"]["random_entries"][2] > 0
                              and r["excess"]["same_ticker"][2] > 0)
    f2_edge = lambda r, rej: (rej and r["ci"][0] > 0)

    f1_lines = run_holm(f1, "p_holm_input", f1_edge)
    f2_lines = run_holm(f2, "p_two_sided", f2_edge)

    # Sensitivities (exploratory, NO verdicts)
    sens = {}
    sens["n40_absolute"] = {f: abs_block(f, 40, universe, rng)
                            for f in FAMILIES}
    sens["n40_continuation"] = {f: cont_block(f, rng, N_long=40, N_short=N_PAIRED)
                                for f in FAMILIES}
    sens["dedupe20_absolute"] = {}
    for f in FAMILIES:
        if f == "H3":
            dd = dedupe_20_hyp(h3_det)
            rows, _ = measure_returns_hyp(dd, N_PRIMARY)
            rows = rows[rows["hypothesis"] == "H3"]
        else:
            dd = dedupe_20(det_shapes[det_shapes["shape"] == f])
            rows, _ = measure_returns(dd, N_PRIMARY)
            rows = rows[rows["shape"] == f]
        oos = rows[rows["is_oos"]]
        sens["dedupe20_absolute"][f] = {"n_oos": int(len(oos)),
                                        "mean": float(oos["ret"].mean())}
    sens["decade_absolute"] = {}
    for f in FAMILIES:
        rows, _ = family_rows(f, N_PRIMARY)
        oos = rows[rows["is_oos"]]
        sens["decade_absolute"][f] = {
            label: {"n": int(len(d)), "mean": float(d["ret"].mean())}
            for label, a, b in DECADES
            for d in [oos[(oos["signal_date"] >= a) & (oos["signal_date"] < b)]]}
    b_rows, _ = family_rows("B", N_PRIMARY)
    sens["shapeB_n20"] = {"n_oos": int(len(b_rows[b_rows["is_oos"]])),
                          "mean": float(
                              b_rows[b_rows["is_oos"]]["ret"].mean())}

    # IS record (observation only)
    is_record = {}
    for f in FAMILIES:
        rows, _ = family_rows(f, N_PRIMARY)
        isd = rows[~rows["is_oos"]]
        is_record[f] = {"n": int(len(isd)), "mean": float(isd["ret"].mean())}

    results = {"meta": {
        "pre_reg": "#4", "primary_n": N_PRIMARY, "paired_n": N_PAIRED,
        "cost": COST, "bootstrap": B, "seed": SEED, "alpha": ALPHA,
        "era_oos_start": ERA_OOS, "universe": UNIVERSE_CSV.name,
        "detections": [DET_SHAPES.name, DET_PILLARS.name],
        "detections_sha256": {f.name: sha(f)[:16] for f in (DET_SHAPES, DET_PILLARS)},
        "measure_code_sha256": sha(Path(__file__))[:16],
        "measure_engine_sha256": "c7421fbf (frozen Phase-3 engine, imported)",
        "note": "verdict machinery runs on OOS only; IS is record only. "
                "F1 p_input = max(p_random, p_same); F2 paired on identical "
                "entries. Random/same baselines pay COST; SPY is raw.",
    }, "family1": f1, "family2": f2, "sensitivities": sens,
       "is_record": is_record}

    RESULTS.write_bytes(json.dumps(results, indent=2).encode("utf-8"))

    def fmt_exc(e):
        if not e:
            return "n/a"
        return f"{e[0]:+.4f} (CI {e[2]:+.4f}..{e[3]:+.4f}, p {e[4]:.4f})"

    report = ["# Momentum measurement report (pre-registration #4)", "",
              f"- Pre-registration #4 (frozen 2026-08-14): primary N={N_PRIMARY}, "
              f"paired N={N_PAIRED}, cost {COST:.4f}, alpha {ALPHA}, "
              f"bootstrap {B} (seed {SEED})",
              f"- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)",
              f"- Inputs: {DET_SHAPES.name} ({len(det_shapes)} rows) and "
              f"{DET_PILLARS.name} (H3 subset {len(h3_det)} rows) — frozen "
              f"pre-reg #2/#1 detections, no re-detection",
              "- Two pre-registered verdict families, each Holm-corrected "
              "across A/C/H3 at alpha=0.05, OOS only: F1 absolute at N=20 vs "
              "era-matched baselines; F2 continuation (paired N=20 vs N=5 on "
              "identical entries)",
              "- The strategy pays 0.15% round-trip; random-entries and "
              "same-ticker baselines pay it too; SPY is raw.",
              "", "## Verdicts — Family 1: absolute at N=20 (vs baselines)", ""]
    report += f1_lines
    report += ["", "## Verdicts — Family 2: continuation (paired N=20 vs N=5)", ""]
    report += f2_lines

    report += ["", "## Per-entry detail (OOS, primary N=20)", ""]
    for f in FAMILIES:
        r = f1[f]
        report += [f"### {'Shape ' + f if f != 'H3' else 'H3 rank-1'}",
                   f"n={r['n_oos']} | mean {r['mean']:+.4f} "
                   f"(CI {r['ci'][0]:+.4f}..{r['ci'][1]:+.4f})",
                   f"| baseline | mean excess | median excess | 95% CI | p (two-sided) |",
                   f"|---|---|---|---|---|"]
        for k, lab in (("random_entries", "random_entries"),
                       ("same_ticker", "same_ticker"), ("spy", "spy")):
            e = r["excess"][k]
            report.append(f"| {lab} | {e[0]:+.4f} | {e[1]:+.4f} | "
                          f"{e[2]:+.4f}..{e[3]:+.4f} | {e[4]:.4f} |")
        if r["metrics"]:
            m = r["metrics"]
            report += ["", "| metric | estimate | 95% CI |", "|---|---|---|",
                       f"| hit rate | {m['hit'][0]:.3f} | "
                       f"{m['hit'][1]:.3f}..{m['hit'][2]:.3f} |",
                       f"| Sharpe (annualized, per-N) | {m['sharpe'][0]:.2f} | "
                       f"{m['sharpe'][1]:.2f}..{m['sharpe'][2]:.2f} |",
                       f"| max drawdown (trade curve) | {m['max_dd'][0]:.3f} | "
                       f"{m['max_dd'][1]:.3f}..{m['max_dd'][2]:.3f} |", ""]

    report += ["## Continuation detail (OOS, paired)", ""]
    for f in FAMILIES:
        c = f2[f]
        report.append(f"- **{f}**: n_pairs={c['n_pairs']} | mean r5 "
                      f"{c['mean_r_short']:+.4f} | mean r20 {c['mean_r_long']:+.4f} "
                      f"| diff {c['mean_diff']:+.4f} "
                      f"(95% CI {c['ci'][0]:+.4f}..{c['ci'][1]:+.4f}), "
                      f"p={c['p_two_sided']:.4f}")

    report += ["", "## IS record (2000-2015) — observation only, no verdicts", "",
               "| family | n | mean |", "|---|---|---|"]
    for f in FAMILIES:
        ir = is_record[f]
        report.append(f"| {f} | {ir['n']} | {ir['mean']:+.4f} |")

    report += ["", "## Sensitivities (exploratory — NO verdicts)", ""]
    report.append("- N=40 absolute: " + " | ".join(
        f"{f}: n={sens['n40_absolute'][f]['n_oos']} mean "
        f"{sens['n40_absolute'][f]['mean']:+.4f}" for f in FAMILIES))
    report.append("- N=40 continuation (paired N=40 vs N=5): " + " | ".join(
        f"{f}: diff {sens['n40_continuation'][f]['mean_diff']:+.4f} "
        f"(p {sens['n40_continuation'][f]['p_two_sided']:.3f})" for f in FAMILIES))
    report.append("- Dedupe-20 at N=20: " + " | ".join(
        f"{f}: n={sens['dedupe20_absolute'][f]['n_oos']} mean "
        f"{sens['dedupe20_absolute'][f]['mean']:+.4f}" for f in FAMILIES))
    for f in FAMILIES:
        dec = sens["decade_absolute"][f]
        report.append(f"- Per-decade OOS at N=20 ({f}): " + " | ".join(
            f"{lab}: n={dec[lab]['n']} mean {dec[lab]['mean']:+.4f}"
            for lab, _, _ in DECADES))
    b = sens["shapeB_n20"]
    report.append(f"- Shape B at N=20 (exploratory, no verdict): "
                  f"n={b['n_oos']} mean {b['mean']:+.4f}")

    report += ["", "## Reproducibility", "",
               "`python -X utf8 tools/measure_momentum.py` regenerates this "
               "report; the seed is fixed, so bootstrap results are stable "
               "across runs.",
               "Input fingerprints: " + ", ".join(
                   f"{f.name} {sha(f)[:16]}…" for f in (DET_SHAPES, DET_PILLARS)) +
               f", momentum code {sha(Path(__file__))[:16]}…, measure code "
               "c7421fbf… (Phase-3 engine imported unchanged).",
               "Any change to the detector, data, or measurement code changes "
               "the frozen inputs and requires a new pre-registration before "
               "it can drive a verdict."]

    REPORT.write_bytes(("\n".join(report) + "\n").encode("utf-8"))
    print(f"wrote {RESULTS.name} and {REPORT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
