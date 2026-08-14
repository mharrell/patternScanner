"""E-02 win-rate measurement for pre-registration #7 (ledger E-02), frozen
2026-08-14.

Reads the frozen veto-pass subsets (data/cache/veto_detections_v1.csv,
written by tools/veto.py, pre-reg #3) — the operationalization of "the
setup when both filters pass" — and measures the claim "we've got an 80%
chance of this working" on the WIN-RATE outcome (win = forward return > 0
after cost, N=10). No new legs: the pass flag IS the setup.

  Family 1 — the claim test (the literal 80%): per shape, exact one-sided
    binomial test of H0: p >= 0.80 vs H1: p < 0.80 on the OOS pass-set win
    rate (p = P(X <= n_wins | Bin(n, 0.80)), logspace via lgamma, no RNG;
    Clopper-Pearson one-sided 95% upper bound by bisection). Holm across
    A/B/C at alpha=0.05. Verdict: rejected (claim falsified) if Holm-
    rejected AND CI upper < 0.80; supported if CI includes 0.80.
  Family 2 — the win-rate edge test: win-rate excess of the pass set vs
    era-matched random entries AND same-ticker windows (p_input =
    max(p_random, p_same)), bootstrap B=1000 seed 20260813, Holm across
    shapes. EDGE requires rejection AND excess CI-low > 0.

Sensitivities (pre-declared, NO verdicts): no-cost win rates; N=5/20;
0.70/0.60 reference thresholds (the claim's own "enough to be profitable"
language); pass-vs-kill and pass-vs-full win rates (E-01/E-04's
conditioning question in win-rate terms); raw-set win rates; per-year
pass win rates; IS record.

Engine pieces import from measure.py (frozen, sha c7421fbf...): measure_returns
computes the same forward returns as every prior campaign. same_ticker
baseline uses the pass set's own per-shape ticker distribution (the #6
protocol correction, per pre-reg #7 §3).
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import (COST, B, SEED, ALPHA, ERA_OOS,
                     load_bars, bootstrap_excess, measure_returns)
import measure
from measure_pillars import build_pools
from measure_veto import two_sample_excess

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
UNIVERSE_CSV = CACHE / "universe_sp600_2026-08-13.csv"
VETO_CSV = CACHE / "veto_detections_v1.csv"
RESULTS = CACHE / "e02_measure_results.json"
REPORT = CACHE / "e02_measure_report.md"

SHAPES = "ABC"
SENS_N = [5, 20]
P0 = 0.80                # the literal claim
REF_THRESH = [0.70, 0.60]  # his own "enough to be profitable" language
MISSING_PASS = 100       # count floor: >= 100 pass OOS per shape


def binomial_lower_tail(x: int, n: int, p0: float):
    """P(X <= x | X ~ Bin(n, p0)), exact, logspace (lgamma), no RNG.

    Returns (p, log10_p). p underflows to 0.0 for true values below
    ~1e-308; log10_p is exact in that range and reported instead.
    """
    if x < 0:
        return 0.0, -float("inf")
    if x >= n:
        return 1.0, 0.0
    if p0 <= 0.0:
        return 1.0, 0.0
    if p0 >= 1.0:
        return 0.0, -float("inf")
    logp, logq = math.log(p0), math.log1p(-p0)
    lnc = math.lgamma(n + 1)
    best, acc = None, 0.0
    for k in range(x + 1):
        v = (lnc - math.lgamma(k + 1) - math.lgamma(n - k + 1)
             + k * logp + (n - k) * logq)
        if best is None:
            best, acc = v, 1.0
        elif v > best:
            acc = 1.0 + acc * math.exp(best - v)
            best = v
        else:
            acc += math.exp(v - best)
    log10 = (best + math.log(acc)) / math.log(10.0)
    return acc * math.exp(best), log10


def binomial_ci_upper(x: int, n: int) -> float:
    """Clopper-Pearson one-sided 95% upper bound: solve P(X<=x | p) = 0.05.

    P(X<=x | p) decreases in p, so the root lies above mid when the tail
    probability at mid exceeds 0.05 (lo = mid), below when it falls below
    (hi = mid).
    """
    if x >= n:
        return 1.0
    lo, hi = float(x) / n, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if binomial_lower_tail(x, n, mid)[0] > 0.05:
            lo = mid
        else:
            hi = mid
    return hi


def fmt_p(p: float, log10: float) -> str:
    """Honest p formatting: exact when representable, log10 below 1e-308."""
    if p > 0.0:
        return f"{p:.4g}"
    return f"<1e-308 (log10 {log10:.1f})"


def win_rate(rets: np.ndarray) -> float:
    return float((rets > 0).mean()) if len(rets) else float("nan")


def run_holm(fam: dict, label: str, n_key: str, gate_order):
    """Apply Holm across shapes to a family dict of per-shape entries.

    fam[s] entries carry 'p' (the input p) and result fields; verdict per
    the pre-registered rules for this family via the family's own
    rule(p, fam[s], gate) applied in Holm order (ascending p).
    """
    order = sorted(SHAPES, key=lambda s: fam[s].get("p", 1.0))
    for rank, s in enumerate(order, start=1):
        gate = ALPHA / (len(SHAPES) - rank + 1)
        fam[s]["holm_gate"] = gate
        fam[s]["holm_rejected"] = fam[s].get("p", 1.0) < gate
    for s in SHAPES:
        fam[s]["verdict"] = gate_order(s, fam[s])


def verdict_f1(s: str, r: dict) -> str:
    if int(r["n"]) < MISSING_PASS:
        return f"INCONCLUSIVE (<{MISSING_PASS} pass OOS detections)"
    if r["holm_rejected"] and r["ci_upper"] < P0:
        return ("REJECTED — claim falsified (one-sided p %s; CI upper %.4f "
                "< 0.80, Holm-rejected)") % (fmt_p(r["p"], r["log10_p"]),
                                             r["ci_upper"])
    return ("SUPPORTED — cannot reject the claim (CI upper %.4f includes "
            "0.80)") % r["ci_upper"]


def verdict_f2(s: str, r: dict) -> str:
    if int(r["n"]) < MISSING_PASS:
        return f"INCONCLUSIVE (<{MISSING_PASS} pass OOS detections)"
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return ("EDGE (Holm-rejected; win-rate excess CI-low %.4f > 0)"
                % r["ci_low"])
    if r["ci_low"] > 0.0 and r["est"] > 0.0:
        return ("NO EDGE (CI includes 0 or Holm gate not cleared; est %.4f)"
                % r["est"])
    return "NO EDGE (CI includes 0 or estimate <= 0, or Holm gate not cleared)"


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def main() -> int:
    vd = pd.read_csv(VETO_CSV)
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()

    camp = vd[vd["warmup"] == False].copy()
    camp["veto_pass"] = camp["veto_pass"].astype(bool)
    sel = camp[camp["veto_pass"]].copy()
    kill = camp[~camp["veto_pass"]].copy()

    pools_pkg = build_pools(10, universe)
    _, random_pool, same_pool, spy_pool = pools_pkg
    rng = np.random.default_rng(SEED)

    fam1, fam2 = {}, {}
    kill_decomp = {}
    sens = {"no_cost": {}, "n5": {}, "n20": {}, "thresh": {}, "pass_vs_kill": {},
            "pass_vs_full": {}, "raw": {}, "per_year": {}, "is_record": {}}

    for s in SHAPES:
        p_rows, dropped = measure_returns(sel[sel["shape"] == s], 10)
        oos = p_rows[p_rows["is_oos"]]
        n_pass = int(len(oos))
        rets = oos["ret"].to_numpy()
        wins = (rets > 0).astype(float)
        wr = win_rate(rets)

        # ---- Family 1: the claim test ----
        n_wins = int(wins.sum())
        p1, log10p1 = binomial_lower_tail(n_wins, n_pass, P0)
        ci_up = binomial_ci_upper(n_wins, n_pass)
        fam1[s] = {"n": n_pass, "n_wins": n_wins, "win_rate": wr,
                   "p": p1, "log10_p": log10p1, "ci_upper": ci_up,
                   "claim": P0, "verdict": ""}

        # ---- Family 2: win-rate excess vs baselines ----
        x_det_tickers = oos["ticker"].to_numpy()

        def sample_same(M, det_tickers=x_det_tickers, same_pool=same_pool,
                        rng=rng):
            ts = det_tickers[rng.integers(0, len(det_tickers), size=M)]
            out = np.empty(M)
            for j, t in enumerate(ts):
                pool = same_pool.get(t)
                if pool is None or len(pool) == 0:
                    out[j] = np.nan
                else:
                    out[j] = pool[rng.integers(0, len(pool))]
            return (out > 0).astype(float)

        def sample_random(M, random_pool=random_pool, rng=rng):
            return (random_pool[rng.integers(0, len(random_pool),
                                             size=M)] > 0).astype(float)

        def sample_spy(M, spy_pool=spy_pool, rng=rng):
            return (spy_pool[rng.integers(0, len(spy_pool),
                                          size=M)] > 0).astype(float)

        e_rand = bootstrap_excess(wins, sample_random, rng)
        e_same = bootstrap_excess(wins, sample_same, rng)
        e_spy = bootstrap_excess(wins, sample_spy, rng)
        p_input = max(e_rand[4], e_same[4])
        fam2[s] = {"n": n_pass, "win_rate": wr, "p": p_input,
                   "excess": {"random_entries": list(e_rand),
                              "same_ticker": list(e_same),
                              "spy": list(e_spy)},
                   "est": float(max(e_rand[0], e_same[0])),
                   "ci_low": float(min(e_rand[2], e_same[2])),
                   "verdict": ""}

        # ---- Sensitivities (no verdicts) ----
        f_rows, _ = measure_returns(camp[camp["shape"] == s], 10)
        f_oos = f_rows[f_rows["is_oos"]]
        k_rows, _ = measure_returns(kill[kill["shape"] == s], 10)
        k_oos = k_rows[k_rows["is_oos"]]
        kill_decomp[s] = {"n_full": int(len(f_oos)), "n_pass": n_pass,
                          "wr_pass": wr,
                          "wr_kill": win_rate(k_oos["ret"].to_numpy()),
                          "wr_full": win_rate(f_oos["ret"].to_numpy())}

        # no-cost win rate: recompute returns without COST (own loop)
        rows_nc = []
        nc_loc: dict = {}
        for _, r in oos.iterrows():
            t = r["ticker"]
            if t not in nc_loc:
                nc_loc[t] = {x: j for j, x in enumerate(load_bars(t).index)}
            loc = nc_loc[t].get(pd.Timestamp(r["signal_date"]))
            if loc is None or loc + 10 >= len(load_bars(t)):
                continue
            df = load_bars(t)
            ret_nc = float(df["Close"].iloc[loc + 10] /
                           df["Open"].iloc[loc + 1] - 1.0)
            rows_nc.append(ret_nc)
        sens["no_cost"][s] = {"n": len(rows_nc),
                              "win_rate": win_rate(np.array(rows_nc))}

        for Nv in SENS_N:
            q_rows, _ = measure_returns(sel[sel["shape"] == s], Nv)
            q_oos = q_rows[q_rows["is_oos"]]
            sens[f"n{Nv}"][s] = {"n": int(len(q_oos)),
                                 "win_rate": win_rate(q_oos["ret"].to_numpy())}

        sens["thresh"][s] = {f"{t:.2f}": dict(
            zip(("p", "log10_p"),
                binomial_lower_tail(n_wins, n_pass, t)))
            for t in REF_THRESH}

        # pass-vs-kill win-rate excess (two-sample, bootstrap)
        k_wins = (k_oos["ret"].to_numpy() > 0).astype(float)
        pv = two_sample_excess(wins, k_wins, rng) if len(k_wins) else None
        sens["pass_vs_kill"][s] = {"pass_wr": wr,
                                   "kill_wr": win_rate(k_oos["ret"].to_numpy()),
                                   "excess": list(pv) if pv else None}

        f_wins = (f_oos["ret"].to_numpy() > 0).astype(float)
        pf = two_sample_excess(wins, f_wins, rng) if len(f_wins) else None
        sens["pass_vs_full"][s] = {"pass_wr": wr,
                                   "full_wr": win_rate(f_oos["ret"].to_numpy()),
                                   "excess": list(pf) if pf else None}

        sens["raw"][s] = {"n": int(len(f_oos)),
                          "win_rate": win_rate(f_oos["ret"].to_numpy())}

        years = oos.groupby(oos["signal_date"].str[:4])["ret"].apply(
            lambda v: float((v > 0).mean()))
        sens["per_year"][s] = {str(y): wr_y for y, wr_y in
                               sorted(years.items())}

        is_rows = p_rows[~p_rows["is_oos"]]
        sens["is_record"][s] = {"n": int(len(is_rows)),
                                "win_rate": win_rate(is_rows["ret"].to_numpy())}

    run_holm(fam1, "claim_test", "n", verdict_f1)
    run_holm(fam2, "win_rate_edge", "n", verdict_f2)

    out = {
        "pre_reg": "#7",
        "claim": "win rate >= 0.80 on the veto-pass setup",
        "params": {"p0": P0, "cost": COST, "n": 10, "b": B, "seed": SEED,
                   "alpha": ALPHA, "era_oos_start": ERA_OOS,
                   "count_floor": MISSING_PASS,
                   "reference_thresholds": REF_THRESH},
        "families": {"claim_test": fam1, "win_rate_edge": fam2},
        "kill_decomposition": kill_decomp,
        "sensitivities": sens,
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
    L.append("# E-02 measurement report (pre-registration #7)")
    L.append("")
    L.append("- Pre-registration #7 (frozen 2026-08-14): claim = win rate >= "
             "0.80 on the veto-pass setup (both filters pass), N=10 primary, "
             f"cost {COST}, alpha {ALPHA}, bootstrap {B} (seed {SEED})")
    L.append("- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)")
    L.append("- Inputs: veto_detections_v1.csv (pre-reg #3 output, %d rows, "
             "warm-up excluded %d)" % (len(vd), int(vd["warmup"].sum())))
    L.append("- Win = forward return > 0 after cost (entry open t+1, exit "
             "close t+N). Two verdict families, Holm across A/B/C at "
             "alpha=0.05, OOS only; F1 = exact one-sided binomial vs 0.80; "
             "F2 = win-rate excess vs era-matched baselines.")
    L.append("")
    for label, fam, ttl in (("claim_test", fam1, "Verdicts — Family 1: the "
                             "claim test (win rate >= 0.80)"),
                            ("win_rate_edge", fam2, "Verdicts — Family 2: "
                             "win-rate edge vs baselines")):
        L.append(f"## {ttl}")
        L.append("")
        for s in SHAPES:
            r = fam[s]
            if label == "claim_test":
                L.append(f"- F1-claim-test {s}: n_pass={r['n']} | n_wins="
                         f"{r['n_wins']} | win_rate {r['win_rate']:.4f} | "
                         f"one-sided p {fmt_p(r['p'], r['log10_p'])} vs claim "
                         f"{P0} (CI upper {r['ci_upper']:.4f}) -> "
                         f"**{r['verdict']}**")
            else:
                e_rand, e_same, e_spy = (r["excess"]["random_entries"],
                                         r["excess"]["same_ticker"],
                                         r["excess"]["spy"])
                L.append(f"- F2-win-rate-edge {s}: n_pass={r['n']} | win_rate "
                         f"{r['win_rate']:.4f} | excess vs random "
                         f"{e_rand[0]:+.4f} (CI {e_rand[2]:+.4f}.."
                         f"{e_rand[3]:+.4f}, p {e_rand[4]:.3f}) | vs same "
                         f"{e_same[0]:+.4f} (p {e_same[4]:.3f}) | vs spy "
                         f"{e_spy[0]:+.4f} (p {e_spy[4]:.3f}) | p_input "
                         f"{r['p']:.3f} -> **{r['verdict']}**")
        L.append("")
    L.append("## Sensitivities (exploratory — NO verdicts)")
    L.append("")
    L.append("| shape | no-cost wr | N=5 | N=20 | 0.70 p | 0.60 p | pass | "
             "kill | full | raw | IS |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for s in SHAPES:
        L.append(f"| {s} | {sens['no_cost'][s]['win_rate']:.4f} | "
                 f"{sens['n5'][s]['win_rate']:.4f} | "
                 f"{sens['n20'][s]['win_rate']:.4f} | "
                 f"{fmt_p(sens['thresh'][s]['0.70']['p'], sens['thresh'][s]['0.70']['log10_p'])} | "
                 f"{fmt_p(sens['thresh'][s]['0.60']['p'], sens['thresh'][s]['0.60']['log10_p'])} | "
                 f"{kill_decomp[s]['wr_pass']:.4f} | "
                 f"{kill_decomp[s]['wr_kill']:.4f} | "
                 f"{kill_decomp[s]['wr_full']:.4f} | "
                 f"{sens['raw'][s]['win_rate']:.4f} | "
                 f"{sens['is_record'][s]['win_rate']:.4f} |")
    L.append("")
    L.append("Pass-vs-kill and pass-vs-full win-rate excesses (two-sample "
             "bootstrap): " + "; ".join(
        f"{s}: kill {sens['pass_vs_kill'][s]['excess'][0]:+.4f} (p "
        f"{sens['pass_vs_kill'][s]['excess'][4]:.3f}), full "
        f"{sens['pass_vs_full'][s]['excess'][0]:+.4f} (p "
        f"{sens['pass_vs_full'][s]['excess'][4]:.3f})" for s in SHAPES))
    L.append("")
    L.append("Per-year pass-set win rates (OOS): " + "; ".join(
        f"{s}: " + ", ".join(f"{y} {v:.3f}" for y, v in
                             sens["per_year"][s].items()) for s in SHAPES))
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_e02.py` regenerates this report; "
             "the seed is fixed and F1 is RNG-free, so results are stable "
             "across runs.")
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
