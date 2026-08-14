"""E-03 measurement for pre-registration #6 (ledger E-03), frozen 2026-08-14.

Reads the leg-attached detections (data/cache/e03_detections_v1.csv, written
by tools/e03.py from the frozen shape detections) and measures three
pre-registered verdict families per shape S in {A, B, C}:

  Family 1 — cross conditioning, all OOS: mean(S bear-crossed OOS) -
    mean(S not-crossed OOS) < 0 (the claim without regime), two-sample
    bootstrap (B=1000, seed 20260813).
  Family 2 — cross conditioning, bear-market OOS days only (SPY < SMA200
    at the signal date): same comparison, within-regime control.
  Family 3 — avoidance bar: the crossed subset's N=10 excess vs era-matched
    random entries AND same-ticker buy-and-hold is significantly BELOW 0
    (p_input = max(p_random, p_same)) — the cross identifies breakouts
    worth avoiding.

The claim is negative ("more times than not, any attempt to break out will
reject and the price will end up selling off"), so the Edge vocabulary is
applied in the claim's direction: FADE EDGE requires Holm-rejected AND the
excess CI UPPER bound < 0; the sign convention is flipped vs campaigns #1-5
(pre-reg #6 §4). Inconclusive: < 100 crossed OOS detections (F2: < 100
crossed on bear days). Warm-up rows (bar index < 60, flagged by e03.py) are
excluded from the campaign and counted; regime-undefined rows (SPY history
< 200 bars, IS only) are excluded from F2 and counted.

Shared protocol identical to pre-reg #1-5: N=10 primary, COST 0.15%, Holm
across A/B/C at alpha=0.05 per family, OOS 2016-2025 only.

Sensitivities (pre-declared, exploratory, NO verdicts): L=5 window, k in
[0,20] (cross on or before the signal bar), zero-line cross reading
(pre-reg #3 sensitivity, no signal there), bullish signal-line cross,
non-bear regime conditioning, crossed subset vs baselines within bear days
only, N=5/20, per-year OOS means of the crossed subset.

Engine pieces import from measure.py (frozen, sha c7421fbf...) as-is.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import (COST, B, SEED, ALPHA, ERA_OOS, load_bars, window_pool,
                     bootstrap_excess, measure_returns, metric_cis)
from measure_pillars import build_pools
from measure_veto import two_sample_excess
import e03 as e03_mod

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
UNIVERSE_CSV = CACHE / "universe_sp600_2026-08-13.csv"
DET_CSV = CACHE / "detections_v1.csv"
E03_CSV = CACHE / "e03_detections_v1.csv"
RESULTS = CACHE / "e03_measure_results.json"
REPORT = CACHE / "e03_measure_report.md"

SHAPES = "ABC"
SENS_N = [5, 20]


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def main() -> int:
    det = pd.read_csv(DET_CSV)
    ed = pd.read_csv(E03_CSV)
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()

    # campaign set: warm-up rows excluded (counted); regime-undefined counted
    camp = ed[ed["warmup"] == False].copy()
    for col in ("bear_cross", "bull_cross", "zero_cross"):
        camp[col] = camp[col].astype(bool)
    camp["bear_regime"] = camp["bear_regime"].astype(object)
    camp.loc[camp["bear_regime"].isna(), "bear_regime"] = None

    # subset integrity: camp keys must equal detections keys (minus warmup)
    k_det = set(map(tuple, det[["shape", "ticker", "signal_date"]].astype(str).values))
    k_camp = set(map(tuple, camp[["shape", "ticker", "signal_date"]].astype(str).values))
    n_warmup = int((ed["warmup"] == True).sum())
    assert len(k_camp) == len(det) - n_warmup and k_camp <= k_det, \
        "E-03 campaign set is not the frozen detections minus warm-up"

    crossed = camp[camp["bear_cross"]].copy()
    not_crossed = camp[~camp["bear_cross"]].copy()
    bear = camp[camp["bear_regime"] == True].copy()
    bear_crossed = bear[bear["bear_cross"]].copy()
    bear_not = bear[~bear["bear_cross"]].copy()
    n_no_regime = int(camp["bear_regime"].isna().sum())

    rng = np.random.default_rng(SEED)
    N = 10  # pre-reg #6 primary (frozen with pre-reg #2)
    pools_pkg = build_pools(N, universe)
    _, random_pool, same_pool, spy_pool = pools_pkg

    full_rows, _ = measure_returns(camp, N)
    x_rows, _ = measure_returns(crossed, N)
    nx_rows, _ = measure_returns(not_crossed, N)
    bx_rows, _ = measure_returns(bear_crossed, N)
    bnx_rows, _ = measure_returns(bear_not, N)

    results = {"meta": {
        "pre_reg": "#6", "primary_n": N, "cost": COST, "bootstrap": B,
        "seed": SEED, "alpha": ALPHA, "era_oos_start": ERA_OOS,
        "universe": UNIVERSE_CSV.name,
        "detections": DET_CSV.name, "detections_sha256": sha(DET_CSV)[:16],
        "e03_file": E03_CSV.name, "e03_file_sha256": sha(E03_CSV)[:16],
        "e03_code_sha256": sha(Path(e03_mod.__file__))[:16],
        "measure_code_sha256": sha(Path(__file__))[:16],
        "measure_engine_sha256": "c7421fbf (frozen Phase-3 engine, imported)",
        "warmup_excluded": int(n_warmup), "regime_undefined": int(n_no_regime),
        "cross_definition": "bearish signal-line crossover within L=20 bars "
                            "before the signal bar; regime = SPY close < SPY "
                            "200-day SMA at t",
        "note": "verdict machinery runs on OOS only; IS is record only. "
                "Three pre-registered verdict families (cross conditioning "
                "all-OOS, cross conditioning bear-days-only, avoidance bar), "
                "each Holm-corrected across A/B/C. Negative claim: FADE EDGE "
                "requires CI upper bound < 0 (sign convention flipped vs #1-5).",
    }, "families": {}, "sensitivities": {}}

    # ---- per-shape analysis: three families ----
    fam1, fam2, fam3 = {}, {}, {}
    for s in SHAPES:
        f = full_rows[(full_rows["shape"] == s) & (full_rows["is_oos"])]
        x = x_rows[(x_rows["shape"] == s) & (x_rows["is_oos"])]
        nx = nx_rows[(nx_rows["shape"] == s) & (nx_rows["is_oos"])]
        bx = bx_rows[(bx_rows["shape"] == s) & (bx_rows["is_oos"])]
        bnx = bnx_rows[(bnx_rows["shape"] == s) & (bnx_rows["is_oos"])]
        n_f, n_x, n_nx, n_bx, n_bnx = map(len, (f, x, nx, bx, bnx))
        x_rets = x["ret"].to_numpy()
        nx_rets = nx["ret"].to_numpy()
        bx_rets = bx["ret"].to_numpy()
        bnx_rets = bnx["ret"].to_numpy()

        # F1: crossed vs not-crossed, all OOS (true two-sample partition)
        cond = two_sample_excess(x_rets, nx_rets, rng) if n_x and n_nx \
            else (float("nan"),) * 5
        # F2: same comparison on bear-market OOS days only
        cond_bear = two_sample_excess(bx_rets, bnx_rets, rng) if n_bx and n_bnx \
            else (float("nan"),) * 5

        # F3 same-ticker baseline: the shape's OWN crossed-subset ticker
        # distribution (per the #1-5 protocol — the detection's own ticker).
        x_det_tickers = x["ticker"].to_numpy()

        def sample_same(M, det_tickers=x_det_tickers, same_pool=same_pool, rng=rng):
            out = np.empty(M)
            for m in range(M):
                pool = same_pool[det_tickers[rng.integers(0, len(det_tickers))]]
                out[m] = pool[rng.integers(0, len(pool))]
            return out

        def sample_random(M, random_pool=random_pool, rng=rng):
            return random_pool[rng.integers(0, len(random_pool), size=M)]

        def sample_spy(M, spy_pool=spy_pool, rng=rng):
            return spy_pool[rng.integers(0, len(spy_pool), size=M)]

        abs_r = bootstrap_excess(x_rets, sample_random, rng) if n_x else None
        abs_s = bootstrap_excess(x_rets, sample_same, rng) if n_x else None
        abs_spy = bootstrap_excess(x_rets, sample_spy, rng) if n_x else None
        metrics = metric_cis(x.sort_values("signal_date"), rng) if n_x else None

        fam1[s] = {"n_crossed": int(n_x), "n_not_crossed": int(n_nx),
                   "mean_crossed": float(x_rets.mean()) if n_x else float("nan"),
                   "mean_not_crossed": float(nx_rets.mean()) if n_nx else float("nan"),
                   "mean": float(x_rets.mean()) if n_x else float("nan"),
                   "excess": cond, "p_holm_input": cond[4],
                   "verdict": None, "holm_gate": None, "holm_rejected": None}
        fam2[s] = {"n_crossed_bear": int(n_bx), "n_not_crossed_bear": int(n_bnx),
                   "mean_crossed_bear": float(bx_rets.mean()) if n_bx else float("nan"),
                   "mean_not_crossed_bear": float(bnx_rets.mean()) if n_bnx else float("nan"),
                   "excess": cond_bear, "p_holm_input": cond_bear[4],
                   "verdict": None, "holm_gate": None, "holm_rejected": None}
        fam3[s] = {"n_crossed": int(n_x), "mean": fam1[s]["mean"],
                   "ci": [float(v) for v in np.percentile(x_rets, [2.5, 97.5])]
                         if n_x else [float("nan")] * 2,
                   "excess": {"random_entries": abs_r, "same_ticker": abs_s,
                              "spy": abs_spy} if abs_r else {},
                   "p_holm_input": max(abs_r[4], abs_s[4]) if abs_r else 1.0,
                   "metrics": metrics, "verdict": None,
                   "holm_gate": None, "holm_rejected": None}

    results["families"]["cross_all_oos"] = fam1
    results["families"]["cross_bear_days"] = fam2
    results["families"]["avoidance_bar"] = fam3

    # ---- Holm per family across A/B/C (negative claim: CI-hi < 0) ----
    def run_holm(fam, label, n_key):
        lines = []
        order = sorted(SHAPES, key=lambda s: fam[s]["p_holm_input"])
        for i, s in enumerate(order):
            k = len(order)
            r = fam[s]
            gate = ALPHA / (k - i)
            rejected = r["p_holm_input"] <= gate
            n = r[n_key]
            exc = r["excess"]
            if isinstance(exc, dict):  # family 3: dict of baseline tuples
                e_rand, e_same = exc.get("random_entries"), exc.get("same_ticker")
                ci_hi = max(e_rand[3] if e_rand else -1.0,
                            e_same[3] if e_same else -1.0)
                e_mean = e_rand[0] if e_rand else float("nan")
                reason = "excess vs random AND same-ticker upper bound < 0"
            else:                      # families 1/2: (mean, med, lo, hi, p)
                ci_hi = exc[3]
                e_mean = exc[0]
                reason = "conditioning excess (crossed - not-crossed) upper bound < 0"
            if n < 100:
                verdict = f"INCONCLUSIVE (<100 crossed OOS detections)"
            elif rejected and ci_hi < 0:
                verdict = f"FADE EDGE (Holm-rejected; {reason})"
            else:
                verdict = "NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)"
            r["holm_gate"], r["holm_rejected"], r["verdict"] = \
                gate, bool(rejected), verdict
            m_crossed = r.get("mean", r.get("mean_crossed_bear", float("nan")))
            m_not = r.get("mean_not_crossed",
                          r.get("mean_not_crossed_bear", float("nan")))
            lines.append(
                f"- {label} {s}: n_crossed={n} | mean_crossed {m_crossed:+.4f} "
                f"(not-crossed {m_not:+.4f}) | "
                f"excess {e_mean:+.4f} (CI-hi {ci_hi:+.4f}) | "
                f"p {r['p_holm_input']:.4f} (Holm gate {gate:.4f}) -> **{verdict}**")
        return lines

    v1 = run_holm(fam1, "F1-cross-all-OOS", "n_crossed")
    v2 = run_holm(fam2, "F2-cross-bear-days", "n_crossed_bear")
    v3 = run_holm(fam3, "F3-avoidance-bar", "n_crossed")

    # ---- sensitivities (exploratory, NO verdicts) ----
    sens = []

    def variant_crossed(camp_rows, L, k0, flag):
        """Rows whose cross flag fired within [k0, L] bars before t.

        Re-derives flags from the raw bars with the same frozen e03 machinery
        (no new data); 'bull' uses the stored L=20 window flag.
        """
        loc_c = {}
        sel_rows = []
        for _, r in camp_rows.iterrows():
            t, ts = r["ticker"], pd.Timestamp(r["signal_date"])
            df = e03_mod.bars(t)
            if t not in loc_c:
                loc_c[t] = {x: j for j, x in enumerate(df.index)}
            loc = loc_c[t][ts]
            hist = e03_mod._hist_cache(t, df["Close"]).to_numpy()
            line = e03_mod._line_cache(t, df["Close"]).to_numpy()
            if flag == "bear":
                hit = any(hist[loc - k - 1] >= 0.0 and hist[loc - k] < 0.0
                          for k in range(k0, L + 1))
            elif flag == "zero":
                hit = any(line[loc - k - 1] >= 0.0 and line[loc - k] < 0.0
                          for k in range(k0, L + 1))
            elif flag == "zero_at_t":   # pre-reg #3's exact reading (cross on t)
                hit = bool(line[loc] < 0.0 and line[loc - 1] >= 0.0)
            else:                       # "bull": stored L=20 window flag
                hit = bool(r["bull_cross"])
            if hit:
                sel_rows.append(r)
        return pd.DataFrame(sel_rows)

    def subset_means(dframe, label):
        """OOS means of a variant crossed subset, per shape."""
        parts = []
        if len(dframe) == 0:
            parts = [f"{s}: n=0 (no detections match)" for s in SHAPES]
            sens.append(f"- {label}: " + " | ".join(parts))
            return
        sr, _ = measure_returns(dframe, N)
        for s in SHAPES:
            o = sr[(sr["shape"] == s) & (sr["is_oos"])]["ret"]
            parts.append(f"{s}: n={len(o)} "
                         f"mean {o.mean() if len(o) else float('nan'):+.4f}")
        sens.append(f"- {label}: " + " | ".join(parts))

    subset_means(variant_crossed(camp, 5, 1, "bear"), "L=5 (cross within "
                 "5 bars) — crossed subset means")
    subset_means(variant_crossed(camp, 20, 0, "bear"), "k in [0,20] (cross "
                 "on or before the signal bar) — crossed subset means")
    subset_means(variant_crossed(camp, 20, 1, "zero_at_t"), "zero-line "
                 "cross AT the signal bar (pre-reg #3 reading, no signal "
                 "there) — crossed subset means")
    subset_means(variant_crossed(camp, 20, 1, "zero"), "zero-line cross "
                 "within L=20 — crossed subset means")
    subset_means(variant_crossed(camp, 20, 1, "bull"), "bullish signal-line "
                 "cross within L=20 (opposite direction) — crossed subset "
                 "means")

    # non-bear regime conditioning (F1 within non-bear OOS days)
    nb = camp[camp["bear_regime"] == False]
    nbx, _ = measure_returns(nb[nb["bear_cross"]], N)
    nbnx, _ = measure_returns(nb[~nb["bear_cross"]], N)
    parts = []
    for s in SHAPES:
        x = nbx[(nbx["shape"] == s) & (nbx["is_oos"])]["ret"].to_numpy()
        nx = nbnx[(nbnx["shape"] == s) & (nbnx["is_oos"])]["ret"].to_numpy()
        d = two_sample_excess(x, nx, rng) if len(x) and len(nx) else (float("nan"),) * 5
        parts.append(f"{s}: crossed n={len(x)} mean {x.mean() if len(x) else float('nan'):+.4f} "
                     f"excess {d[0]:+.4f} (p {d[4]:.4f})")
    sens.append("- Non-bear regime conditioning (F1 within non-bear OOS days): "
                + " | ".join(parts))

    # bear-only absolute (F3's regime form)
    bear_oos = bear_crossed[bear_crossed["signal_date"] >= ERA_OOS]
    br, _ = measure_returns(bear_oos, N)
    parts = []
    for s in SHAPES:
        x = br[(br["shape"] == s) & (br["is_oos"])]["ret"].to_numpy()
        if len(x):
            det_tickers = br[(br["shape"] == s) & (br["is_oos"])]["ticker"].to_numpy()

            def bs(M, det_tickers=det_tickers, same_pool=same_pool, rng=rng):
                out = np.empty(M)
                for m in range(M):
                    pool = same_pool[det_tickers[rng.integers(0, len(det_tickers))]]
                    out[m] = pool[rng.integers(0, len(pool))]
                return out

            e_r = bootstrap_excess(x, sample_random, rng)
            e_s = bootstrap_excess(x, bs, rng)
            parts.append(f"{s}: n={len(x)} mean {x.mean():+.4f} vs random "
                         f"{e_r[0]:+.4f} (p {e_r[4]:.4f}) vs same {e_s[0]:+.4f} (p {e_s[4]:.4f})")
        else:
            parts.append(f"{s}: n=0")
    sens.append("- Bear-days crossed subset vs baselines (F3 regime form): "
                + " | ".join(parts))

    # N=5/20 crossed vs not-crossed
    for n_h in SENS_N:
        xr, _ = measure_returns(crossed, n_h)
        nxr, _ = measure_returns(not_crossed, n_h)
        parts = []
        for s in SHAPES:
            x = xr[(xr["shape"] == s) & (xr["is_oos"])]["ret"]
            nx = nxr[(nxr["shape"] == s) & (nxr["is_oos"])]["ret"]
            parts.append(f"{s}: crossed n={len(x)} mean {x.mean() if len(x) else float('nan'):+.4f} "
                         f"(not-crossed {nx.mean() if len(nx) else float('nan'):+.4f})")
        sens.append(f"- N={n_h}: " + " | ".join(parts))

    # per-year OOS means of the crossed subset
    xo = x_rows[x_rows["is_oos"]]
    py = {}
    for y in range(2016, 2026):
        yr = xo[(xo["signal_date"] >= f"{y}-01-01") & (xo["signal_date"] < f"{y + 1}-01-01")]
        py[str(y)] = {"n": int(len(yr)), "mean": float(yr["ret"].mean()) if len(yr) else float("nan")}
    results["sensitivities"]["per_year_crossed"] = py
    parts = [f"{y}: n={py[str(y)]['n']} mean {py[str(y)]['mean']:+.4f}" for y in range(2016, 2026)]
    sens.append("- Per-year crossed-subset means (OOS): " + " | ".join(parts))

    results["sensitivities"]["n_horizons"] = SENS_N

    report = ["# E-03 measurement report (pre-registration #6)", "",
              f"- Pre-registration #6 (frozen 2026-08-14): N={N} primary, "
              f"cost {COST:.4f}, alpha {ALPHA}, bootstrap {B} (seed {SEED})",
              f"- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)",
              f"- Inputs: {DET_CSV.name} ({len(det)} rows) -> {E03_CSV.name} "
              f"({len(ed)} rows; warm-up-excluded {n_warmup}, regime-undefined "
              f"{n_no_regime})",
              f"- Legs (frozen in tools/e03.py): bearish signal-line MACD "
              f"(12,26,9) crossover within L=20 bars before the signal bar; "
              f"regime = SPY close < SPY 200-day SMA at t.",
              f"- Three pre-registered verdict families, each Holm-corrected "
              f"across A/B/C at alpha=0.05, OOS only: F1 (cross conditioning, "
              f"all OOS), F2 (cross conditioning, bear days only), F3 "
              f"(avoidance bar vs era-matched baselines). Negative claim — "
              f"FADE EDGE requires CI upper bound < 0.",
              f"- The strategy pays {COST:.2%} round-trip; random-entries and "
              f"same-ticker baselines pay it too; SPY is raw.",
              "", "## Verdicts — Family 1: cross conditioning, all OOS", ""
              ] + v1 + ["", "## Verdicts — Family 2: cross conditioning, "
                            "bear-market days only", ""] + v2 + [
              "", "## Verdicts — Family 3: avoidance bar (crossed subset vs "
                  "baselines)", ""] + v3

    report += ["", "## Per-shape detail (OOS, primary N=10)", ""]
    for s in SHAPES:
        r1, r2, r3 = fam1[s], fam2[s], fam3[s]
        m = r3["metrics"] or {}
        line = (f"### Shape {s}\n\n"
                f"F1: crossed n={r1['n_crossed']} of {r1['n_crossed'] + r1['n_not_crossed']} "
                f"| mean crossed {r1['mean_crossed']:+.4f} vs not-crossed "
                f"{r1['mean_not_crossed']:+.4f} | excess {r1['excess'][0]:+.4f} "
                f"(95% CI {r1['excess'][2]:+.4f}..{r1['excess'][3]:+.4f}) | "
                f"p={r1['p_holm_input']:.4f} -> **{r1['verdict']}**\n\n"
                f"F2 (bear days): crossed n={r2['n_crossed_bear']} vs "
                f"not-crossed n={r2['n_not_crossed_bear']} | mean "
                f"{r2['mean_crossed_bear']:+.4f} vs {r2['mean_not_crossed_bear']:+.4f} "
                f"| excess {r2['excess'][0]:+.4f} (95% CI {r2['excess'][2]:+.4f}.."
                f"{r2['excess'][3]:+.4f}) | p={r2['p_holm_input']:.4f} -> "
                f"**{r2['verdict']}**\n\n"
                f"F3: mean {r3['mean']:+.4f} (95% CI {r3['ci'][0]:+.4f}.."
                f"{r3['ci'][1]:+.4f}) | p={r3['p_holm_input']:.4f} -> "
                f"**{r3['verdict']}**\n\n")
        if m:
            line += (f"| metric | estimate | 95% CI |\n|---|---|---|\n"
                     f"| hit rate | {m['hit'][0]:.3f} | {m['hit'][1]:.3f}..{m['hit'][2]:.3f} |\n"
                     f"| Sharpe (annualized) | {m['sharpe'][0]:.2f} | "
                     f"{m['sharpe'][1]:.2f}..{m['sharpe'][2]:.2f} |\n"
                     f"| max drawdown (trade curve) | {m['max_dd'][0]:.3f} | "
                     f"{m['max_dd'][1]:.3f}..{m['max_dd'][2]:.3f} |\n\n")
        line += "| baseline | mean excess | median excess | 95% CI | p (two-sided) |\n|---|---|---|---|---|\n"
        for name, v in r3["excess"].items():
            if v:
                line += (f"| {name} | {v[0]:+.4f} | {v[1]:+.4f} | "
                         f"{v[2]:+.4f}..{v[3]:+.4f} | {v[4]:.4f} |\n")
        report.append(line)

    report += ["", "## IS record (2000-2015) — observation only, no verdicts", "",
               "| shape | n crossed | mean crossed | n not-crossed | mean not-crossed |",
               "|---|---|---|---|---|"]
    for s in SHAPES:
        x = x_rows[(x_rows["shape"] == s) & (~x_rows["is_oos"])]["ret"]
        nx = nx_rows[(nx_rows["shape"] == s) & (~nx_rows["is_oos"])]["ret"]
        report.append(f"| {s} | {len(x)} | {x.mean() if len(x) else float('nan'):+.4f} "
                      f"| {len(nx)} | {nx.mean() if len(nx) else float('nan'):+.4f} |")

    report += ["", "## Sensitivities (exploratory — NO verdicts)", ""] + sens

    report += ["", "## Reproducibility", "",
               "`python -X utf8 tools/measure_e03.py` regenerates this report; "
               "the seed is fixed, so bootstrap results are stable across runs.",
               "Input fingerprints: detections "
               f"{results['meta']['detections_sha256']}…, e03 file "
               f"{results['meta']['e03_file_sha256']}…, e03 code "
               f"{results['meta']['e03_code_sha256']}…, measure code "
               f"{results['meta']['measure_code_sha256']}… (Phase-3 engine "
               f"c7421fbf… imported unchanged).",
               "Any change to the detector, data, or measurement code changes "
               "the frozen inputs and requires a new pre-registration before it "
               "can drive a verdict.", ""]

    REPORT.write_text("\n".join(report), encoding="utf-8")
    RESULTS.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("report -> data/cache/e03_measure_report.md")
    print("results -> data/cache/e03_measure_results.json")
    for line in v1 + [""] + v2 + [""] + v3:
        print(line.replace("**", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
