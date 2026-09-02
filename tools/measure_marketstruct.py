"""Pre-registration #26 measurement tool — market-structure calibration
(ledger rows 3rE-03, 3rE-04, afN-22, GMR-10/ul3-15, Wd_-01/-02).

Implements exactly PREREGISTRATION.md pre-reg #26 §2:
  H1 (inference, ONE Holm slot, direction DOWN): 200DMA veto — right-under
      [close < MA200 and close >= 0.98*MA200] vs right-above [close > MA200
      and close <= 1.02*MA200], day-paired N=10 contrast, hist universe,
      OOS 2022-01-01..2025-12-31. Claim confirmed (EDGE) iff Holm-rejected
      (single slot -> alpha) AND CI-upper < 0; FADE iff rejected AND
      CI-low > 0.
  C1 (decision rule): share of (ticker, day) |ret| > 4%, OOS 2016-2025 —
      CONFIRMED <= 5%, CONTRADICTED >= 10%, else PARTIAL.
  C2 (decision rule): daily count of names >= +10% (dates with >= 100
      reporting names) — CONFIRMED if OOS median in [5,10]; CONTRADICTED if
      median >= 20 or >= 50% zero-days; else PARTIAL.
  C3 (decision rule): annual counts of >= +50% days (parabolic, per 0sl-21),
      2000-2025 — CONFIRMED if the max annual count falls in 2020/2021;
      CONTRADICTED if a pre-2020 year is strictly higher; else PARTIAL.
  Wd (calibration only, NO verdict): leader proxy L_t = daily max return
      across the universe (dates with >= 100 names); distribution per year,
      lag-1 autocorrelation, next-day universe mean return by leader
      tercile. Downstream campaigns consume this definition, not a re-tune.

Bars/day_paired_boot imported from measure_pricetier.py (pre-reg #16)
unchanged. Freeze discipline: FROZEN_SHA blanked-self-hash, refuses to run
on placeholder/mismatch.

Run:  python -X utf8 tools/measure_marketstruct.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure_pricetier import Bars, day_paired_boot, raw_sha256

REPO = Path(__file__).resolve().parents[1]
HIST_UNIVERSE = REPO / "data" / "cache" / "universe_sp600_hist_2026-08-15.csv"
RESULTS_JSON = REPO / "data" / "cache" / "marketstruct_measure_results.json"
REPORT_MD = REPO / "data" / "cache" / "marketstruct_measure_report.md"

SEED = 20260902
B = 1000
ALPHA = 0.05
N_PRIMARY = 10
COST = 0.0015
OOS_CAL = (np.datetime64("2016-01-01"), np.datetime64("2025-12-31"))
OOS_H1 = (np.datetime64("2022-01-01"), np.datetime64("2025-12-31"))
IS_CAL = (np.datetime64("2000-01-01"), np.datetime64("2015-12-31"))
MIN_NAMES_PER_DAY = 100
BAND_PCT = 0.02
MA_WINDOW = 200
FLOOR_DATES = 100
PARABOLIC_RET = 0.50
FROZEN_SHA = "fc457780f6a8c1963bd17e7c773a2ff2e285dbaceb1072b5d9e3d45074373d6a"    # placeholder until freeze


def hash_self() -> str:
    b = Path(__file__).read_bytes()
    pat = re.compile(rb'(FROZEN_SHA = "[0-9a-f]{64}")')
    b2, n = pat.subn(b'FROZEN_SHA = "' + b"0" * 64 + b'"', b)
    if n != 1:
        raise RuntimeError(f"expected exactly one FROZEN_SHA hex, got {n}")
    return hashlib.sha256(b2).hexdigest()


def self_check() -> None:
    if FROZEN_SHA == "0" * 64:
        sys.exit("REFUSED: FROZEN_SHA is unset (placeholder) — the freeze "
                 "has not landed; no measurement may run.")
    if hash_self() != FROZEN_SHA:
        sys.exit("REFUSED: FROZEN_SHA mismatch — the tool has been modified "
                 f"after freeze.\n  frozen {FROZEN_SHA}\n  actual {hash_self()}")


def fmt(v, spec="+.4f"):
    return "—" if v is None else format(v, spec)


def era_dates(ret_by_date: dict, era) -> list[str]:
    lo, hi = era
    return [d for d in sorted(ret_by_date)
            if lo <= np.datetime64(d) <= hi]


def main() -> int:
    self_check()
    rng = np.random.default_rng(SEED)
    hist = pd.read_csv(HIST_UNIVERSE, dtype={"ticker": str})
    tickers = hist["ticker"].tolist()
    bars = Bars(tickers)

    # ---- per-name daily returns, pooled by date ----
    ret_by_date: dict[str, list[float]] = {}
    for t in sorted(tickers):
        dts = bars.dates.get(t)
        if dts is None:
            continue
        closes = bars.close[t]
        for i in range(1, len(dts)):
            ret_by_date.setdefault(str(dts[i]), []).append(
                float(closes[i] / closes[i - 1] - 1.0))
    all_rets = np.array([r for v in ret_by_date.values() for r in v])

    # ---- C1: |ret| > 4% share ----
    def ret_share(era):
        rs = np.array([r for d in era_dates(ret_by_date, era)
                       for r in ret_by_date[d]])
        return {"n": int(len(rs)),
                "share_abs_gt4": float((np.abs(rs) > 0.04).mean()),
                "share_gt4": float((rs > 0.04).mean()),
                "share_lt_minus4": float((rs < -0.04).mean())}
    c1_oos = ret_share(OOS_CAL)
    c1_is = ret_share(IS_CAL)
    c1_full = {"n": int(len(all_rets)),
               "share_abs_gt4": float((np.abs(all_rets) > 0.04).mean())}
    c1_by_year = {}
    for y in sorted({d[:4] for d in ret_by_date}):
        rs = np.array([r for d in ret_by_date if d.startswith(y)
                       for r in ret_by_date[d]])
        c1_by_year[y] = {"share_abs_gt4": float((np.abs(rs) > 0.04).mean()),
                         "n": int(len(rs))}
    sh = c1_oos["share_abs_gt4"]
    c1_verdict = ("CONFIRMED" if sh <= 0.05 else
                  "CONTRADICTED" if sh >= 0.10 else "PARTIAL")
    print(f"C1: |ret|>4% share OOS {sh:.4f} (IS {c1_is['share_abs_gt4']:.4f}) "
          f"-> {c1_verdict}")

    # ---- C2: daily count of names >= +10% ----
    def daily_counts(era):
        return np.array([sum(1 for r in ret_by_date[d] if r >= 0.10)
                         for d in era_dates(ret_by_date, era)
                         if len(ret_by_date[d]) >= MIN_NAMES_PER_DAY])
    c2_oos = daily_counts(OOS_CAL)
    c2_median = float(np.median(c2_oos)) if len(c2_oos) else None
    c2_zero = float((c2_oos == 0).mean()) if len(c2_oos) else None
    if c2_median is None:
        c2_verdict = "INCONCLUSIVE (no OOS dates)"
    elif 5 <= c2_median <= 10:
        c2_verdict = "CONFIRMED"
    elif c2_median >= 20 or (c2_zero or 0) >= 0.5:
        c2_verdict = "CONTRADICTED"
    else:
        c2_verdict = "PARTIAL"
    print(f"C2: OOS median daily >=+10% count {c2_median} (zero-days "
          f"{c2_zero}), n_dates {len(c2_oos)} -> {c2_verdict}")

    # ---- C3: parabolic (>= +50%) annual counts ----
    def parabolic_by_year(thr):
        out = {}
        for d, rs in ret_by_date.items():
            y = d[:4]
            out[y] = out.get(y, 0) + sum(1 for r in rs if r >= thr)
        return dict(sorted(out.items()))
    par_year = parabolic_by_year(PARABOLIC_RET)
    peak_year = max(par_year, key=par_year.get)
    pre2020 = {y: v for y, v in par_year.items() if int(y) < 2020}
    pre2020_max = (max(pre2020.values()), max(pre2020, key=pre2020.get)) \
        if pre2020 else (0, None)
    if peak_year in ("2020", "2021"):
        c3_verdict = "CONFIRMED"
    elif pre2020 and pre2020_max[0] > max(par_year.get("2020", 0),
                                          par_year.get("2021", 0)):
        c3_verdict = "CONTRADICTED"
    else:
        c3_verdict = "PARTIAL"
    print(f"C3: parabolic peak year {peak_year} (pre-2020 max "
          f"{pre2020_max[0]} in {pre2020_max[1]}) -> {c3_verdict}")

    par100 = parabolic_by_year(1.0)

    # ---- Wd leader proxy (calibration only) ----
    leader = {d: max(rs) for d, rs in ret_by_date.items()
              if len(rs) >= MIN_NAMES_PER_DAY}
    lds = sorted(leader)
    lv = np.array([leader[d] for d in lds])
    lag1 = float(np.corrcoef(lv[:-1], lv[1:])[0, 1])
    ldf = pd.DataFrame({
        "d": lds[:-1],
        "L": lv[:-1],
        "next_ret": [float(np.mean(ret_by_date[d])) for d in lds[1:]],
    })
    ldf["year"] = ldf["d"].str[:4]
    ldf["tercile"] = pd.qcut(ldf["L"], 3, labels=["low", "mid", "high"])
    terc = {str(k): float(v) for k, v in
            ldf.groupby("tercile", observed=True)["next_ret"].mean().items()}
    leader_per_year = {k: float(v) for k, v in
                       ldf.groupby("year")["L"].median().items()}

    # ---- H1: 200DMA right-under vs right-above (OOS 2022-2025) ----
    def ma_contrast(pct):
        u_dates, a_dates = {}, {}
        unames, anames = set(), set()
        warm_dropped = 0
        lo, hi = OOS_H1
        for t in sorted(tickers):
            dts = bars.dates.get(t)
            if dts is None:
                continue
            closes = bars.close[t]
            n = len(dts)
            if n < MA_WINDOW + 2:
                continue
            ma = pd.Series(closes).rolling(MA_WINDOW).mean().to_numpy()
            for i in range(MA_WINDOW, n):
                if np.isnan(ma[i]):
                    warm_dropped += 1
                    continue
                d = str(dts[i])
                dt = np.datetime64(d)
                if dt < lo or dt > hi or i + N_PRIMARY >= n:
                    continue
                f = closes[i + N_PRIMARY] / closes[i] - 1.0 - COST
                if closes[i] < ma[i] and closes[i] >= (1 - pct) * ma[i]:
                    u_dates.setdefault(d, []).append(f)
                    unames.add(t)
                elif closes[i] > ma[i] and closes[i] <= (1 + pct) * ma[i]:
                    a_dates.setdefault(d, []).append(f)
                    anames.add(t)
        ds = sorted(set(u_dates) & set(a_dates))
        if not ds:
            return None, len(unames), len(anames), warm_dropped
        res = day_paired_boot(
            np.array([np.mean(u_dates[d]) for d in ds]),
            np.array([np.mean(a_dates[d]) for d in ds]), rng)
        res["n_dates"] = len(ds)
        return res, len(unames), len(anames), warm_dropped

    h1, n_under, n_above, warm = ma_contrast(BAND_PCT)
    print(f"H1: paired dates {0 if h1 is None else h1['n_dates']}, "
          f"names under/above {n_under}/{n_above}, warmup-dropped {warm}")
    if h1 is not None and h1["n_dates"] >= FLOOR_DATES \
            and n_under >= 10 and n_above >= 10:
        h1["gate"] = ALPHA
        h1["rejected"] = h1["p"] <= ALPHA
        if not h1["rejected"]:
            h1["verdict"] = "NO EDGE"
        elif h1["ci_high"] < 0:
            h1["verdict"] = "EDGE (right-under underperforms — claim confirmed)"
        elif h1["ci_low"] > 0:
            h1["verdict"] = "FADE (right-under outperforms — claim contradicted)"
        else:
            h1["verdict"] = "NO EDGE"
    else:
        h1 = h1 or {}
        h1["verdict"] = "INCONCLUSIVE (floor unmet)"
    band_var = {}
    for pct in (0.01, 0.05):
        r, nu, na, _ = ma_contrast(pct)
        band_var[str(pct)] = r
        band_var[str(pct)]["n_names"] = [nu, na] if r else None

    out = {
        "pre_reg": "#26",
        "claim": ("market-structure calibration: 4% day rarity, 5-10 "
                  "gainers/day, parabolic-frequency peak, 200DMA veto, "
                  "leader proxy"),
        "params": {"n": N_PRIMARY, "cost": COST, "b": B, "seed": SEED,
                   "alpha": ALPHA, "ma_window": MA_WINDOW,
                   "band_pct": BAND_PCT,
                   "min_names_per_day": MIN_NAMES_PER_DAY,
                   "parabolic_ret": PARABOLIC_RET,
                   "cal_era": [str(OOS_CAL[0]), str(OOS_CAL[1])],
                   "h1_era": [str(OOS_H1[0]), str(OOS_H1[1])]},
        "h1_200dma": h1,
        "calibration": {
            "c1": {"oos": c1_oos, "is_2000_2015": c1_is, "full": c1_full,
                   "by_year": c1_by_year, "verdict": c1_verdict},
            "c2": {"median": c2_median, "zero_share": c2_zero,
                   "n_dates": int(len(c2_oos)), "verdict": c2_verdict},
            "c3": {"peak_year": peak_year,
                   "pre2020_max": {"count": pre2020_max[0],
                                   "year": pre2020_max[1]},
                   "counts_ge50": par_year, "counts_ge100": par100,
                   "verdict": c3_verdict}},
        "wd_leader_proxy": {"lag1_autocorr": lag1,
                            "per_year_median": leader_per_year,
                            "terciles_next_day_mean_ret": terc,
                            "n_days": int(len(ldf))},
        "sensitivities": {"ma_band_variants": band_var},
        "assertions": {"ma_warmup_dropped": warm,
                       "h1_names": {"under": n_under, "above": n_above}},
        "fingerprints": {
            "hist_universe_sha256": raw_sha256(HIST_UNIVERSE),
            "measure_code_sha256": raw_sha256(Path(__file__)),
            "pricetier_engine_sha256": raw_sha256(
                REPO / "tools" / "measure_pricetier.py"),
        },
    }
    RESULTS_JSON.write_text(json.dumps(out, indent=2, default=str),
                            encoding="utf-8")
    print(f"wrote {RESULTS_JSON.name}")

    # ---- report ----
    L = ["# Market-structure calibration report (pre-registration #26)", "",
         f"- Pre-reg #26 (frozen per its freeze block); seed {SEED}, B={B}, "
         f"alpha {ALPHA}; hist universe; OOS cal {OOS_CAL[0]}..{OOS_CAL[1]}, "
         f"H1 era {OOS_H1[0]}..{OOS_H1[1]}", ""]
    L.append(f"- H1 200DMA veto: est {fmt(h1.get('est'))} (CI "
             f"{fmt(h1.get('ci_low'))}..{fmt(h1.get('ci_high'))}, p "
             f"{h1.get('p', 1.0):.3f}), dates {h1.get('n_dates')} -> "
             f"**{h1.get('verdict')}**")
    L.append(f"- C1 |ret|>4%: OOS {sh:.4f} -> **{c1_verdict}**")
    L.append(f"- C2 gainer count: OOS median {c2_median} -> **{c2_verdict}**")
    L.append(f"- C3 parabolic peak: {peak_year} (pre-2020 max "
             f"{pre2020_max[0]} in {pre2020_max[1]}) -> **{c3_verdict}**")
    L.append(f"- Wd leader proxy: lag-1 autocorr {lag1:+.3f}; next-day "
             f"universe mean by leader tercile: {terc} (calibration only)")
    L.append("")
    L.append("## Parabolic counts per year (>= +50%)")
    L.append("")
    L.append("| year | >=+50% | >=+100% |")
    L.append("|---|---|---|")
    for y in sorted(par_year):
        L.append(f"| {y} | {par_year[y]} | {par100.get(y, 0)} |")
    L.append("")
    L.append("## C1 |ret|>4% share by year")
    L.append("")
    L.append("| year | share | n |")
    L.append("|---|---|---|")
    for y, r in c1_by_year.items():
        L.append(f"| {y} | {r['share_abs_gt4']:.4f} | {r['n']} |")
    L.append("")
    L.append("## MA-band variants (descriptive)")
    L.append("")
    for pct, r in band_var.items():
        if r:
            L.append(f"- ±{float(pct):.0%}: est {r['est']:+.4f} (CI "
                     f"{r['ci_low']:+.4f}..{r['ci_high']:+.4f}, p {r['p']:.3f}), "
                     f"dates {r['n_dates']}")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_marketstruct.py` regenerates "
             "this report; the seed is fixed, so results are stable across "
             "runs.")
    L.append("Inputs: hist universe %s…, tool %s… (engine %s… imported "
             "unchanged)." % (
                 out["fingerprints"]["hist_universe_sha256"][:12],
                 out["fingerprints"]["measure_code_sha256"][:12],
                 out["fingerprints"]["pricetier_engine_sha256"][:12]))
    L.append("")
    REPORT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())