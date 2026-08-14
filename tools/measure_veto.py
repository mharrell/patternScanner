"""Veto measurement for pre-registration #3 (ledger E-01/E-04), frozen
2026-08-14.

Reads the veto-filtered detections (data/cache/veto_detections_v1.csv,
written by tools/veto.py from the frozen shape detections) and measures two
pre-registered verdict families per shape S in {A, B, C}:

  Family 1 — conditioning (the claim as stated): mean(veto-passing OOS) -
    mean(full OOS) > 0, two-sample bootstrap (B=1000, seed 20260813).
  Family 2 — absolute bar (DESIGN_BRIEF §1): the veto-passing subset vs the
    three era-matched baselines (random entries -COST, same-ticker -COST,
    SPY raw), the same machinery as campaigns #1/#2.

Shared protocol identical to pre-reg #1/#2: N=10 primary, COST 0.15%,
Holm across A/B/C at alpha=0.05 per family, OOS 2016-2025 only, >=100
veto-passing OOS detections for a verdict. Warm-up detections (bar index
< 60, flagged by veto.py) are excluded from the campaign and counted.

The kill-rate table + killed-set means answer E-04's "filters killing
setups vs setups working": mean(full) = pass_frac*mean(pass) +
kill_frac*mean(killed).

Sensitivities (pre-declared, exploratory, NO verdicts): N=5/20; MACD
zero-crossing reading; volume leg V=1.5/3.0; the veto applied to the H3
rank-1 cohort (pillar detections, N=1).

Engine pieces import from measure.py (frozen, sha c7421fbf...): measure_returns
and metric_cis are used as-is — they are shape-keyed, and metric_cis' Sharpe
factor uses HORIZONS["primary"]=10, which IS this campaign's primary horizon.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import (COST, B, SEED, ALPHA, ERA_OOS, TRADING_DAYS,
                     load_bars, window_pool, bootstrap_excess,
                     measure_returns, metric_cis)
from measure_pillars import build_pools, measure_returns_hyp
import veto as veto_mod

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
UNIVERSE_CSV = CACHE / "universe_sp600_2026-08-13.csv"
DET_CSV = CACHE / "detections_v1.csv"
VETO_CSV = CACHE / "veto_detections_v1.csv"
PILLAR_DET = CACHE / "pillar_detections_v1.csv"
RESULTS = CACHE / "veto_measure_results.json"
REPORT = CACHE / "veto_measure_report.md"

SHAPES = "ABC"
SENS_N = [5, 20]


def two_sample_excess(selected: np.ndarray, full: np.ndarray, rng):
    """Bootstrap mean(selected) - mean(full); returns (mean, med, lo, hi, p)."""
    M, F = len(selected), len(full)
    diffs = np.empty(B)
    for b in range(B):
        s = selected[rng.integers(0, M, size=M)].mean()
        f = full[rng.integers(0, F, size=F)].mean()
        diffs[b] = s - f
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return float(diffs.mean()), float(np.median(diffs)), float(lo), float(hi), float(p)


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def main() -> int:
    det = pd.read_csv(DET_CSV)
    vd = pd.read_csv(VETO_CSV)
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()

    # campaign set: warm-up rows excluded (counted); selected = veto pass
    camp = vd[vd["warmup"] == False].copy()
    for col in ("macd_neg", "macd_cross", "red_high_vol", "veto_pass"):
        camp[col] = camp[col].astype(bool)
    sel = camp[camp["veto_pass"]].copy()

    # subset integrity: camp keys must equal detections keys (minus warmup)
    k_det = set(map(tuple, det[["shape", "ticker", "signal_date"]].astype(str).values))
    k_camp = set(map(tuple, camp[["shape", "ticker", "signal_date"]].astype(str).values))
    n_warmup = int((vd["warmup"] == True).sum())
    assert len(k_camp) == len(det) - n_warmup and k_camp <= k_det, \
        "veto campaign set is not the frozen detections minus warm-up"

    rng = np.random.default_rng(SEED)
    N = 10  # pre-reg #3 primary (frozen with pre-reg #2)
    pools_pkg = build_pools(N, universe)
    _, random_pool, same_pool, spy_pool = pools_pkg

    full_rows, _ = measure_returns(camp, N)
    pass_rows, _ = measure_returns(sel, N)
    det_tickers_all = pass_rows[pass_rows["is_oos"]]["ticker"].to_numpy()

    results = {"meta": {
        "pre_reg": "#3", "primary_n": N, "cost": COST, "bootstrap": B,
        "seed": SEED, "alpha": ALPHA, "era_oos_start": ERA_OOS,
        "universe": UNIVERSE_CSV.name,
        "detections": DET_CSV.name, "detections_sha256": sha(DET_CSV)[:16],
        "veto_file": VETO_CSV.name, "veto_file_sha256": sha(VETO_CSV)[:16],
        "veto_code_sha256": sha(Path(veto_mod.__file__))[:16],
        "measure_code_sha256": sha(Path(__file__))[:16],
        "measure_engine_sha256": "c7421fbf (frozen Phase-3 engine, imported)",
        "warmup_excluded": int(n_warmup),
        "note": "verdict machinery runs on OOS only; IS is record only. "
                "Two pre-registered verdict families (conditioning effect and "
                "absolute bar), each Holm-corrected across A/B/C.",
    }, "families": {}, "kill_rates": {}, "sensitivities": {}}

    # ---- per-shape analysis: both families + kill decomposition ----
    fam1, fam2 = {}, {}
    kill = {}
    for s in SHAPES:
        full = full_rows[(full_rows["shape"] == s) & (full_rows["is_oos"])]
        psub = pass_rows[(pass_rows["shape"] == s) & (pass_rows["is_oos"])]
        n_full, n_pass = len(full), len(psub)
        f_rets = full["ret"].to_numpy()
        p_rets = psub["ret"].to_numpy()

        def sample_same(M, det_tickers=det_tickers_all, same_pool=same_pool, rng=rng):
            out = np.empty(M)
            for m in range(M):
                pool = same_pool[det_tickers[rng.integers(0, len(det_tickers))]]
                out[m] = pool[rng.integers(0, len(pool))]
            return out

        def sample_random(M, random_pool=random_pool, rng=rng):
            return random_pool[rng.integers(0, len(random_pool), size=M)]

        def sample_spy(M, spy_pool=spy_pool, rng=rng):
            return spy_pool[rng.integers(0, len(spy_pool), size=M)]

        cond = two_sample_excess(p_rets, f_rets, rng) if n_pass and n_full \
            else (float("nan"),) * 5
        abs_r = bootstrap_excess(p_rets, sample_random, rng) if n_pass else None
        abs_s = bootstrap_excess(p_rets, sample_same, rng) if n_pass else None
        abs_spy = bootstrap_excess(p_rets, sample_spy, rng) if n_pass else None
        metrics = metric_cis(psub.sort_values("signal_date"), rng) if n_pass else None

        fam1[s] = {"n_full": int(n_full), "n_pass": int(n_pass),
                   "mean_full": float(f_rets.mean()) if n_full else float("nan"),
                   "mean_pass": float(p_rets.mean()) if n_pass else float("nan"),
                   "mean": float(p_rets.mean()) if n_pass else float("nan"),
                   "excess": cond, "p_holm_input": cond[4],
                   "verdict": None, "holm_gate": None, "holm_rejected": None}
        fam2[s] = {"n_pass": int(n_pass), "mean": fam1[s]["mean_pass"],
                   "ci": [float(x) for x in np.percentile(p_rets, [2.5, 97.5])]
                         if n_pass else [float("nan")] * 2,
                   "excess": {"random_entries": abs_r, "same_ticker": abs_s,
                              "spy": abs_spy} if abs_r else {},
                   "p_holm_input": max(abs_r[4], abs_s[4]) if abs_r else 1.0,
                   "metrics": metrics, "verdict": None,
                   "holm_gate": None, "holm_rejected": None}

        # kill decomposition (OOS) — answers E-04. Killed = camp minus the
        # pass set (sel); measured with the frozen machinery so exit-beyond-
        # series-end drops are handled the same way as everywhere else.
        c = camp[(camp["shape"] == s)].copy()
        c["_key"] = c["ticker"] + "|" + c["signal_date"]
        sel_s = sel[sel["shape"] == s].copy()
        sel_s["_key"] = sel_s["ticker"] + "|" + sel_s["signal_date"]
        killed_df = c[~c["_key"].isin(set(sel_s["_key"]))].drop(columns="_key")
        kr, dropped_k = measure_returns(killed_df, N)
        killed_oos = kr[kr["is_oos"]]
        c_oos = c[c["signal_date"] >= ERA_OOS]
        kill[s] = {"n_total": int((camp["shape"] == s).sum()),
                   "n_oos": int(len(c_oos)),
                   "n_pass_oos": int(fam1[s]["n_pass"]),
                   "n_killed_oos": int(len(killed_oos)),
                   "killed_dropped": dropped_k[s],
                   "macd_alone_oos": int((c_oos["macd_neg"] & ~c_oos["red_high_vol"]).sum()),
                   "vol_alone_oos": int((~c_oos["macd_neg"] & c_oos["red_high_vol"]).sum()),
                   "both_oos": int((c_oos["macd_neg"] & c_oos["red_high_vol"]).sum()),
                   "mean_killed": float(killed_oos["ret"].mean())
                       if len(killed_oos) else float("nan"),
                   "n_killed_total": int((camp["shape"] == s).sum()
                                         - int((sel["shape"] == s).sum()))}

    results["families"]["conditioning"] = fam1
    results["families"]["absolute"] = fam2
    results["kill_rates"] = kill

    # ---- Holm per family across A/B/C ----
    def run_holm(fam, label):
        lines = []
        order = sorted(SHAPES, key=lambda s: fam[s]["p_holm_input"])
        for i, s in enumerate(order):
            k = len(order)
            r = fam[s]
            gate = ALPHA / (k - i)
            rejected = r["p_holm_input"] <= gate
            n = r["n_pass"]
            exc = r["excess"]
            if isinstance(exc, dict):  # family 2: dict of baseline tuples
                e_rand, e_same = exc.get("random_entries"), exc.get("same_ticker")
                ci_lo = min(e_rand[2] if e_rand else 1.0,
                            e_same[2] if e_same else 1.0)
                e_mean = e_rand[0] if e_rand else float("nan")
                reason = "excess vs random AND same-ticker excludes 0"
            else:                      # family 1: (mean, med, lo, hi, p) tuple
                ci_lo = exc[2]
                e_mean = exc[0]
                reason = "conditioning excess (subset - full) excludes 0"
            if n < 100:
                verdict = "INCONCLUSIVE (<100 veto-passing OOS detections)"
            elif rejected and ci_lo > 0:
                verdict = f"EDGE (Holm-rejected; {reason})"
            else:
                verdict = "NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)"
            r["holm_gate"], r["holm_rejected"], r["verdict"] = \
                gate, bool(rejected), verdict
            lines.append(
                f"- {label} {s}: n_pass={n} | mean {r['mean']:+.4f} "
                f"(full {r.get('mean_full', float('nan')):+.4f}) | "
                f"excess {e_mean:+.4f} (CI-lo {ci_lo:+.4f}) | "
                f"p {r['p_holm_input']:.4f} (Holm gate {gate:.4f}) -> **{verdict}**")
        return lines

    v1 = run_holm(fam1, "F1-conditioning")
    v2 = run_holm(fam2, "F2-absolute")

    # ---- sensitivities (exploratory) ----
    sens = []
    for n_h in SENS_N:
        fr, _ = measure_returns(camp, n_h)
        pr, _ = measure_returns(sel, n_h)
        line = f"- N={n_h}: "
        parts = []
        for s in SHAPES:
            f = fr[(fr["shape"] == s) & (fr["is_oos"])]["ret"]
            p = pr[(pr["shape"] == s) & (pr["is_oos"])]["ret"]
            parts.append(f"{s}: pass n={len(p)} mean {p.mean():+.4f} "
                         f"(full {f.mean():+.4f})")
        sens.append(line + " | ".join(parts))
    # zero-crossing + V variants + H3 (pure re-subsets of the stored legs;
    # the V variants recompose the volume leg as red AND vr >= V)
    for label, mask in (
        ("MACD zero-crossing reading", ~camp["macd_cross"] & ~camp["red_high_vol"]),
        ("volume leg V=1.5", ~camp["macd_neg"]
         & ~(camp["red"] & (camp["vol_ratio"] >= 1.5))),
        ("volume leg V=3.0", ~camp["macd_neg"]
         & ~(camp["red"] & (camp["vol_ratio"] >= 3.0))),
    ):
        s2 = camp[mask].copy()
        pr, _ = measure_returns(s2, N)
        parts = []
        for s in SHAPES:
            p = pr[(pr["shape"] == s) & (pr["is_oos"])]["ret"]
            parts.append(f"{s}: n={len(p)} mean {p.mean():+.4f}")
        sens.append(f"- {label}: " + " | ".join(parts))
    # H3 rank-1 cohort with the veto (pillar detections, N=1)
    h3 = pd.read_csv(PILLAR_DET)
    h3 = h3[h3["hypothesis"] == "H3"].copy()
    legs = []
    for _, r in h3.iterrows():
        df = veto_mod.bars(r["ticker"])
        loc = list(df.index).index(pd.Timestamp(r["signal_date"]))
        if loc < veto_mod.PARAMS["warmup_bars"]:
            legs.append(None)
            continue
        c = df["Close"]
        line = veto_mod.macd_line(c)
        vr = veto_mod.vol_ratio_at(df["Volume"], loc)
        red = float(c.iloc[loc]) < float(df["Open"].iloc[loc])
        legs.append((float(line.iloc[loc]) < 0.0,
                     red and not np.isnan(vr) and vr >= veto_mod.PARAMS["vol_mult"]))
    h3["macd_neg"] = [x[0] if x else False for x in legs]
    h3["red_high_vol"] = [x[1] if x else False for x in legs]
    h3["veto_pass"] = ~h3["macd_neg"] & ~h3["red_high_vol"]
    h3f, _ = measure_returns_hyp(h3, 1)
    h3p, _ = measure_returns_hyp(h3[h3["veto_pass"]], 1)
    for dframe, label in ((h3f, "full H3"), (h3p, "veto-passing H3")):
        o = dframe[dframe["is_oos"]]["ret"]
        sens.append(f"- Veto on H3 rank-1 cohort (N=1, {label}): "
                    f"n={len(o)} mean {o.mean():+.4f}")
    results["sensitivities"] = {"n_horizons": SENS_N,
                                "h3_veto_n_oos": int((h3p[h3p["is_oos"]]).shape[0])}

    report = ["# Veto measurement report (pre-registration #3)", "",
              f"- Pre-registration #3 (frozen 2026-08-14): N={N} primary, "
              f"cost {COST:.4f}, alpha {ALPHA}, bootstrap {B} (seed {SEED})",
              f"- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)",
              f"- Inputs: {DET_CSV.name} ({len(det)} rows) -> {VETO_CSV.name} "
              f"({len(vd)} rows; warm-up-excluded {n_warmup})",
              f"- Veto (frozen in tools/veto.py): kill = MACD(12,26) line < 0 "
              f"OR (red candle AND vol >= {veto_mod.PARAMS['vol_mult']}x prior-20 "
              f"mean); pass = both legs clear.",
              f"- Two pre-registered verdict families, each Holm-corrected "
              f"across A/B/C at alpha=0.05, OOS only: F1 (conditioning — the "
              f"claim as stated), F2 (absolute bar vs era-matched baselines).",
              f"- The strategy pays {COST:.2%} round-trip; random-entries and "
              f"same-ticker baselines pay it too; SPY is raw.",
              "", "## Verdicts — Family 1: conditioning (subset vs full set)",
              ""] + v1 + ["", "## Verdicts — Family 2: absolute bar (vs "
                                "baselines)", ""] + v2

    report += ["", "## Kill-rate decomposition (OOS; E-04: filters killing "
                   "setups vs setups working)", "",
               "| shape | total det | OOS | pass | killed | macd-alone | "
               "vol-alone | both | mean(pass) | mean(killed) |",
               "|---|---|---|---|---|---|---|---|---|---|"]
    for s in SHAPES:
        k = kill[s]
        report.append(f"| {s} | {k['n_total']} | {k['n_oos']} | "
                      f"{k['n_pass_oos']} | {k['n_killed_oos']} | "
                      f"{k['macd_alone_oos']} | {k['vol_alone_oos']} | "
                      f"{k['both_oos']} | {fam1[s]['mean_pass']:+.4f} | "
                      f"{k['mean_killed']:+.4f} |")

    report += ["", "## Per-shape detail (OOS, primary N=10)", ""]
    for s in SHAPES:
        r1, r2 = fam1[s], fam2[s]
        m = r2["metrics"] or {}
        line = (f"### Shape {s}\n\n"
                f"F1 conditioning: pass n={r1['n_pass']} of {r1['n_full']} | "
                f"mean pass {r1['mean_pass']:+.4f} vs full {r1['mean_full']:+.4f} | "
                f"excess {r1['excess'][0]:+.4f} (95% CI {r1['excess'][2]:+.4f}.."
                f"{r1['excess'][3]:+.4f}) | p={r1['p_holm_input']:.4f} "
                f"-> **{r1['verdict']}**\n\n"
                f"F2 absolute: n={r2['n_pass']} | mean {r2['mean']:+.4f} "
                f"(95% CI {r2['ci'][0]:+.4f}..{r2['ci'][1]:+.4f}) | "
                f"p={r2['p_holm_input']:.4f} -> **{r2['verdict']}**\n\n")
        if m:
            line += (f"| metric | estimate | 95% CI |\n|---|---|---|\n"
                     f"| hit rate | {m['hit'][0]:.3f} | {m['hit'][1]:.3f}..{m['hit'][2]:.3f} |\n"
                     f"| Sharpe (annualized) | {m['sharpe'][0]:.2f} | "
                     f"{m['sharpe'][1]:.2f}..{m['sharpe'][2]:.2f} |\n"
                     f"| max drawdown (trade curve) | {m['max_dd'][0]:.3f} | "
                     f"{m['max_dd'][1]:.3f}..{m['max_dd'][2]:.3f} |\n\n")
        line += "| baseline | mean excess | median excess | 95% CI | p (two-sided) |\n|---|---|---|---|---|\n"
        for name, v in r2["excess"].items():
            if v:
                line += (f"| {name} | {v[0]:+.4f} | {v[1]:+.4f} | "
                         f"{v[2]:+.4f}..{v[3]:+.4f} | {v[4]:.4f} |\n")
        report.append(line)

    report += ["", "## IS record (2000-2015) — observation only, no verdicts", "",
               "| shape | n pass | mean pass | n full | mean full |",
               "|---|---|---|---|---|"]
    for s in SHAPES:
        f = full_rows[(full_rows["shape"] == s) & (~full_rows["is_oos"])]["ret"]
        p = pass_rows[(pass_rows["shape"] == s) & (~pass_rows["is_oos"])]["ret"]
        report.append(f"| {s} | {len(p)} | {p.mean():+.4f} | {len(f)} | "
                      f"{f.mean():+.4f} |")

    report += ["", "## Sensitivities (exploratory — NO verdicts)", ""] + sens

    report += ["", "## Reproducibility", "",
               "`python -X utf8 tools/measure_veto.py` regenerates this report; "
               "the seed is fixed, so bootstrap results are stable across runs.",
               "Input fingerprints: detections "
               f"{results['meta']['detections_sha256']}…, veto file "
               f"{results['meta']['veto_file_sha256']}…, veto code "
               f"{results['meta']['veto_code_sha256']}…, measure code "
               f"{results['meta']['measure_code_sha256']}… (Phase-3 engine "
               f"c7421fbf… imported unchanged).",
               "Any change to the detector, data, or measurement code changes "
               "the frozen inputs and requires a new pre-registration before it "
               "can drive a verdict.", ""]

    REPORT.write_text("\n".join(report), encoding="utf-8")
    RESULTS.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("report -> data/cache/veto_measure_report.md")
    print("results -> data/cache/veto_measure_results.json")
    for line in v1 + [""] + v2:
        print(line.replace("**", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
