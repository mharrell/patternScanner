"""I-F-03 market-trend measurement for pre-registration #18, frozen
2026-08-21.

Claim (txWaMpSzHhM [31:55-32:38]): "Stocks will trend with the overall
market unless they have a reason not to." Catalyst names buck the market —
"running when the markets tanking".

This is a STRUCTURAL campaign: no forward returns, no entry/exit, no COST.
The Phase-3 engine's measure_returns is NOT invoked; the claim is about
co-movement, not profitability. Phase 5 cannot fire from it by construction.

Operationalization (pre-reg #18 sec 1-2):

  F1 (market-trending baseline, 1 Holm slot): per-stock Pearson corr of
    daily returns with SPY on OOS days (>= MIN_OOS_DAYS). Statistic = mean
    over stocks; one-sample bootstrap over stocks. EDGE if Holm-rejected
    AND CI-low > 0 (stocks trend with the market, as claimed).

  F2 (catalyst decoupling, 2 slots gap/vol): per stock, diff =
    corr(catalyst days) - corr(non-catalyst days), requiring >= 30 catalyst
    AND >= 30 non-catalyst OOS days. Statistic = mean of diffs; bootstrap
    over stocks. EDGE if Holm-rejected AND CI-upper < 0 (decoupling as
    claimed).

  F3 (buck-the-trend, 2 slots gap/vol): on each SPY-down OOS day, the
    cross-sectional mean return of catalyst stocks minus non-catalyst
    stocks (>= MIN_SIDES each side to qualify). Statistic = mean over
    qualifying down-days; bootstrap over days. EDGE if Holm-rejected AND
    CI-low > 0 (running when the market tanks, as claimed).

Catalyst proxies (per stock, per day): gap = |open_t/close_{t-1} - 1| >= 2%
(GAP_PRIMARY); volume spike RV = vol_t / mean(vol, prior 20) >= 2.0
(RV_PRIMARY). Bar index >= 1 for returns; RV defined from bar index 20.

Floors: F1 >= 100 stocks with >= 100 OOS days; F2 >= 100 stocks with
>= 30/30; F3 >= 100 qualifying down-days. Below a floor -> INCONCLUSIVE.

Bootstrap B = 1000, seed = measure.SEED (20260813), alpha = 0.05, Holm
within each family, era split IS 2000-2015 / OOS 2016-2025 by bar date.
Percentile 2.5/97.5 CI, two-sided p.

The historical-constituent gate (--gate, pre-reg #18 sec 6) re-runs
F1/F2/F3 on the frozen 904-name union (706 with bars); all three families
are re-run and recorded regardless of primary verdicts; an EDGE survives
only if the gate delivers EDGE with the same floors.

Sensitivities (pre-declared, NO verdicts): S1 gap 1/3/5%; S2 vol 1.5/3.0;
S3 combined gap-OR-vol catalyst; S4 idiosyncratic move size (per-stock
|market residual| on catalyst vs non-catalyst days); S5 IS record
(2000-2015, descriptive); S6 per-year OOS; S7 equal-weight S&P 600 mean as
the market factor; S8 up-market-day F3 contrast (the catalyst up-bias
control); S9 Fisher-z correlations.

Frozen-input convention (fixed-point sha, pre-reg #14/#16/#17): FROZEN_SHA
is the sha256 of this file with its own FROZEN_SHA hex blanked to 64 zeros;
self_check() refuses to run if unset or modified. --audit-only computes NO
measurement (exit 1 on FAILED). measure_code_sha256 = the raw file sha,
recorded in every output.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import B, SEED, ALPHA, ERA_OOS, UNIVERSE_CSV, BARS_DIR
import measure
from measure_divergence import run_holm, fmt_num
from measure_veto import two_sample_excess

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
HIST_UNIVERSE = CACHE / "universe_sp600_hist_2026-08-15.csv"
RESULTS = CACHE / "if03_measure_results.json"
REPORT = CACHE / "if03_measure_report.md"
GATE_RESULTS = CACHE / "if03_gate_measure_results.json"
GATE_REPORT = CACHE / "if03_gate_measure_report.md"

# ---- pre-reg #18 frozen parameters ----
GAP_PRIMARY = 0.02          # |gap| threshold (catalyst leg "gap")
RV_PRIMARY = 2.0            # volume-ratio threshold (catalyst leg "vol")
RV_WINDOW = 20              # prior-bar window for the volume ratio
MIN_OOS_DAYS = 100          # F1: per-stock OOS-day floor
MIN_CATALYST_DAYS = 30      # F2: per-stock catalyst-day floor
MIN_NONCATALYST_DAYS = 30   # F2: per-stock non-catalyst-day floor
MIN_STOCKS = 100            # F1/F2: qualifying-stock floor
MIN_DOWN_DAYS = 100         # F3: qualifying down-day floor
MIN_SIDES = 5               # F3: per-down-day side floor
F1_LEG = "base"
F2_LEGS = ("gap", "vol")
F3_LEGS = ("gap", "vol")
GAP_SENS = [0.01, 0.03, 0.05]
RV_SENS = [1.5, 3.0]
EW_MIN_CONTRIB = 100        # EW market: drop days with fewer contributors
MISSING_CUR = ["ADIG", "MBGL", "MFP", "VGNT"]
OOS_YEARS = list(range(2016, 2026))

FROZEN_SHA = "779861550ad3fc2769c5e50a34b56507490294dda5e56b48dfa00d7f8e287e62"


# --------------------------------------------------------------------------
# Freeze machinery (pre-4 #14/#16/#17 convention)
# --------------------------------------------------------------------------
def hash_self() -> str:
    """sha256 of this file with its own FROZEN_SHA hex blanked."""
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
                 f"after freeze.\n  frozen {FROZEN_SHA}\n  actual "
                 f"{hash_self()}")


def raw_sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------
_bars: dict = {}


def load_bars(ticker: str) -> pd.DataFrame:
    """Frozen daily OHLCV parquet (cached in memory per run)."""
    if ticker not in _bars:
        df = pd.read_parquet(BARS_DIR / f"{ticker}.parquet",
                             columns=["Open", "Close", "Volume"])
        df.index = pd.to_datetime(df.index)
        _bars[ticker] = df
    return _bars[ticker]


def market_series_spy() -> pd.Series:
    """SPY daily close-to-close returns indexed by bar date (bar 0 NaN)."""
    df = load_bars("SPY")
    c = df["Close"].to_numpy(dtype=np.float64)
    r = np.full(len(c), np.nan)
    r[1:] = c[1:] / c[:-1] - 1.0
    return pd.Series(r, index=df.index)


def stock_record(t: str, mkt_spy: pd.Series, ctr: dict) -> dict:
    """Per-stock arrays aligned to the bar index, plus structural counters."""
    df = load_bars(t)
    c = df["Close"].to_numpy(dtype=np.float64)
    o = df["Open"].to_numpy(dtype=np.float64)
    v = df["Volume"].to_numpy(dtype=np.float64)
    n = len(df)
    idx = df.index

    ctr["n_stocks"] += 1
    ctr["n_index0"] += 1                              # one first bar per stock
    if np.isnan(v).all():
        ctr["n_vol_nan_stocks"] += 1

    r = np.full(n, np.nan)
    gap = np.full(n, np.nan)
    if n >= 2:
        prev = c[:-1]
        valid = np.isfinite(prev) & (prev != 0.0) & np.isfinite(c[1:]) \
            & np.isfinite(o[1:])
        ctr["n_bad_prior_close"] += int((~valid).sum())
        r[1:] = np.where(valid, c[1:] / prev - 1.0, np.nan)
        gap[1:] = np.where(valid, np.abs(o[1:] / prev - 1.0), np.nan)

    rv = np.full(n, np.nan)
    vs = pd.Series(v)
    mean20 = vs.rolling(RV_WINDOW).mean().shift(1).to_numpy(dtype=np.float64)
    ok = np.isfinite(v) & np.isfinite(mean20) & (mean20 > 0.0)
    rv = np.where(ok, v / np.where(mean20 > 0, mean20, np.nan), np.nan)

    mkt = mkt_spy.reindex(idx).to_numpy(dtype=np.float64)
    oos = (idx >= pd.Timestamp(ERA_OOS)) & np.isfinite(r) \
        & np.isfinite(mkt)
    ctr["n_missing_mkt_oos"] += int(
        ((idx >= pd.Timestamp(ERA_OOS)) & np.isfinite(r) & np.isnan(mkt))
        .sum())

    return {"t": t, "idx": idx, "r": r, "gap": np.abs(gap), "rv": rv,
            "mkt": mkt, "oos": oos}


# --------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------
def pearson(x: np.ndarray, y: np.ndarray):
    """Pearson r on the finite-common pairs; None if < 2 pairs or zero var."""
    m = np.isfinite(x) & np.isfinite(y)
    if int(m.sum()) < 2:
        return None
    xx, yy = x[m], y[m]
    if xx.std() == 0.0 or yy.std() == 0.0:
        return None
    return float(np.corrcoef(xx, yy)[0, 1])


def boot_mean(x: np.ndarray, rng):
    """One-sample bootstrap of the mean; (mean, med, lo, hi, p)."""
    m = len(x)
    b = np.empty(B)
    for i in range(B):
        b[i] = x[rng.integers(0, m, size=m)].mean()
    lo, hi = np.percentile(b, [2.5, 97.5])
    p = 2.0 * min((b <= 0).mean(), (b >= 0).mean())
    return (float(b.mean()), float(np.median(b)), float(lo), float(hi),
            float(p))


def cell(vals: np.ndarray, rng, name: str, floor: int, floor_label: str,
         extra: dict = None) -> dict:
    """Bootstrap a unit-vector into a family cell (None stats if empty)."""
    out = {"name": name, "n": int(len(vals)), "floor": floor,
           "floor_label": floor_label,
           "mean": float(vals.mean()) if len(vals) else None}
    if len(vals) == 0:
        out.update({"est": None, "med": None, "ci_low": None,
                    "ci_upper": None, "p": 1.0, "holm_gate": ALPHA,
                    "holm_rejected": False})
    else:
        est, med, lo, hi, p = boot_mean(vals, rng)
        out.update({"est": est, "med": med, "ci_low": lo, "ci_upper": hi,
                    "p": p, "holm_gate": ALPHA, "holm_rejected": False})
    if extra:
        out.update(extra)
    return out


# --------------------------------------------------------------------------
# Catalyst helpers and unit vectors
# --------------------------------------------------------------------------
def cat_gap_of(rec, g=GAP_PRIMARY):
    return np.abs(rec["gap"]) >= g


def cat_vol_of(rec, v=RV_PRIMARY):
    return rec["rv"] >= v


def cat_comb_of(rec):
    return cat_gap_of(rec) | cat_vol_of(rec)


def f1_vals(recs, oos_mask=None) -> np.ndarray:
    """F1 units: per-stock corr(r_i, market) on the selected days (default
    rec['oos']). oos_mask, when given, REPLACES the default (the caller
    must include validity); used for the IS record."""
    vals = []
    for rec in recs:
        oos = rec["oos"] if oos_mask is None else oos_mask(rec)
        if int(oos.sum()) < MIN_OOS_DAYS:
            continue
        cc = pearson(rec["r"][oos], rec["mkt"][oos])
        if cc is not None:
            vals.append(cc)
    return np.array(vals, dtype=np.float64)


def f2_vals(recs, catf, oos_mask=None) -> np.ndarray:
    """F2 units: per-stock corr(cat) - corr(non-cat), floors 30/30."""
    vals = []
    for rec in recs:
        oos = rec["oos"] if oos_mask is None else oos_mask(rec)
        cat = catf(rec) & oos
        non = (~catf(rec)) & oos
        if int(cat.sum()) < MIN_CATALYST_DAYS or \
                int(non.sum()) < MIN_NONCATALYST_DAYS:
            continue
        cc = pearson(rec["r"][cat], rec["mkt"][cat])
        cn = pearson(rec["r"][non], rec["mkt"][non])
        if cc is not None and cn is not None:
            vals.append(cc - cn)
    return np.array(vals, dtype=np.float64)


def f3_day_contrasts(recs, catf, down, oos_mask=None):
    """F3 units: per-day mean(cat) - mean(non), >= MIN_SIDES each side.
    down=True -> SPY-down; down=False -> SPY-up; None -> all days."""
    days = {}
    for rec in recs:
        oos = rec["oos"] if oos_mask is None else oos_mask(rec)
        if down is None:
            sel = oos
        elif down:
            sel = oos & (rec["mkt"] < 0)
        else:
            sel = oos & (rec["mkt"] > 0)
        cat = catf(rec)
        for i in np.flatnonzero(sel):
            d = rec["idx"][i]
            if cat[i]:
                days.setdefault(d, ([], []))[0].append(rec["r"][i])
            else:
                days.setdefault(d, ([], []))[1].append(rec["r"][i])
    contrasts, qual, excluded = [], [], 0
    for d, (cv, nv) in days.items():
        if len(cv) >= MIN_SIDES and len(nv) >= MIN_SIDES:
            contrasts.append(float(np.mean(cv)) - float(np.mean(nv)))
            qual.append(d)
        else:
            excluded += 1
    return np.array(contrasts, dtype=np.float64), qual, excluded


# ---------------------------------------------------------------------------
# Verdicts (pre-4 #18 sec 4)
# ---------------------------------------------------------------------------
def verdict_f1(r: dict) -> str:
    if int(r["n"]) < MIN_STOCKS:
        return f"INCONCLUSIVE (<{MIN_STOCKS} stocks; n={r['n']})"
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return (f"EDGE (Holm-rejected; CI-low {r['ci_low']:+.4f} > 0 — "
                "stocks trend with the market, as claimed)")
    if r["holm_rejected"] and r["ci_upper"] < 0.0:
        return (f"FADE (Holm-rejected; CI-upper {r['ci_upper']:+.4f} < 0 — "
                "stocks on average anti-correlate with the market, claim "
                "contradicted)")
    return (f"NO EDGE (p {r['p']:.4f}; est {fmt_num(r['est'], '+.4f')}; "
            f"CI {fmt_num(r['ci_low'], '+.4f')}.."
            f"{fmt_num(r['ci_upper'], '+.4f')})")


def verdict_f2(r: dict) -> str:
    if int(r["n"]) < MIN_STOCKS:
        return f"INCONCLUSIVE (<{MIN_STOCKS} stocks; n={r['n']})"
    if r["holm_rejected"] and r["ci_upper"] < 0.0:
        return (f"EDGE (Holm-rejected; CI-upper {r['ci_upper']:+.4f} < 0 — "
                "correlation lower on catalyst days, decoupling as claimed)")
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return (f"FADE (Holm-rejected; CI-low {r['ci_low']:+.4f} > 0 — "
                "correlation HIGHER on catalyst days, claim contradicted)")
    return (f"NO EDGE (p {r['p']:.4f}; est {fmt_num(r['est'], '+.4f')}; "
            f"CI {fmt_num(r['ci_low'], '+.4f')}.."
            f"{fmt_num(r['ci_upper'], '+.4f')})")


def verdict_f3(r: dict) -> str:
    if int(r["n"]) < MIN_DOWN_DAYS:
        return f"INCONCLUSIVE (<{MIN_DOWN_DAYS} down-days; n={r['n']})"
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return (f"EDGE (Holm-rejected; CI-low {r['ci_low']:+.4f} > 0 — "
                "catalyst stocks run when the market runs, as claimed)")
    if r["holm_rejected"] and r["ci_upper"] < 0.0:
        return (f"FADE (Holm-rejected; CI-upper {r['ci_upper']:+.4f} < 0 — "
                "catalyst stocks fall harder on down days, claim "
                "contradicted)")
    return (f"NO EDGE (p {r['p']:.4f}; est {fmt_num(r['est'], '+.4f')}; "
            f"CI {fmt_num(r['ci_low'], '+.4f')}.."
            f"{fmt_num(r['ci_upper'], '+.4f')})")


# ---------------------------------------------------------------------------
# Families
# ---------------------------------------------------------------------------
def run_families(recs, rng) -> tuple[dict, list]:
    """F1/F2/F3 with Holm; returns (families, report lines)."""
    f1 = cell(f1_vals(recs), rng, "F1", MIN_STOCKS,
              f">= {MIN_STOCKS} stocks", {"leg": F1_LEG,
                                          "min_oos": MIN_OOS_DAYS})
    run_holm({"base": f1}, ("base",))
    f1["verdict"] = verdict_f1(f1)

    f2 = {}
    for leg in F2_LEGS:
        catf = cat_gap_of if leg == "gap" else cat_vol_of
        f2[leg] = cell(f2_vals(recs, catf), rng, f"F2-{leg}", MIN_STOCKS,
                       f">= {MIN_STOCKS} stocks")
    run_holm(f2, F2_LEGS)
    for leg in F2_LEGS:
        f2[leg]["verdict"] = verdict_f2(f2[leg])

    f3 = {}
    for leg in F3_LEGS:
        catf = cat_gap_of if leg == "gap" else cat_vol_of
        dc, qual, excl = f3_day_contrasts(recs, catf, down=True)
        f3[leg] = cell(dc, rng, f"F3-{leg}", MIN_DOWN_DAYS,
                       f">= {MIN_DOWN_DAYS} down-days",
                       {"n_qual_days": int(len(qual)),
                        "n_excluded_days": int(excl)})
    run_holm(f3, F3_LEGS)
    for leg in F3_LEGS:
        f3[leg]["verdict"] = verdict_f3(f3[leg])

    lines = [
        f"- **F1** (trend): n_stocks={f1['n']} | mean corr "
        f"{fmt_num(f1['mean'], '+.4f')} | CI {fmt_num(f1['ci_low'], '+.4f')}"
        f"..{fmt_num(f1['ci_upper'], '+.4f')} | p {f1['p']:.4f} "
        f"(gate {f1['holm_gate']:.4f}) -> **{f1['verdict']}**"]
    for leg in F2_LEGS:
        r = f2[leg]
        lines.append(f"- **F2-{leg}** (decoupling): n_stocks={r['n']} | "
                     f"mean diff {fmt_num(r['mean'], '+.4f')} | "
                     f"CI {fmt_num(r['ci_low'], '+.4f')}.."
                     f"{fmt_num(r['ci_upper'], '+.4f')} | p {r['p']:.4f} "
                     f"(gate {r['holm_gate']:.4f}) -> **{r['verdict']}**")
    for leg in F3_LEGS:
        r = f3[leg]
        lines.append(f"- **F3-{leg}** (buck-the-run): n_down={r['n']} "
                     f"(excl {r['n_excluded_days']}) | "
                     f"mean contrast {fmt_num(r['mean'], '+.4f')} | "
                     f"CI {fmt_num(r['ci_low'], '+.4f')}.."
                     f"{fmt_num(r['ci_upper'], '+.4f')} | p {r['p']:.4f} "
                     f"(gate {r['holm_gate']:.4f}) -> **{r['verdict']}**")
    return {"f1": f1, "f2": f2, "f3": f3}, lines


# --------------------------------------------------------------------------
# Sensitivities (pre-declared, NO verdicts)
# --------------------------------------------------------------------------
def sens_gap_vol(recs, rng) -> dict:
    """S1 gap 1/3/5%; S2 vol 1.5/3.0 — F2/F3 estimates only."""
    out = {}
    for g in GAP_SENS:
        f2 = f2_vals(recs, lambda x, g=g: cat_gap_of(x, g))
        dc, _, _ = f3_day_contrasts(recs, lambda x, g=g: cat_gap_of(x, g),
                                    down=True)
        out[f"gap={g:.2f}"] = {
            "f2": cell(f2, rng, "S1", 0, "sensitivity"),
            "f3": cell(dc, rng, "S1", 0, "sensitivity")}
    for v in RV_SENS:
        f2 = f2_vals(recs, lambda x, v=v: cat_vol_of(x, v))
        dc, _, _ = f3_day_contrasts(recs, lambda x, v=v: cat_vol_of(x, v),
                                    down=True)
        out[f"vol={v:.1f}"] = {
            "f2": cell(f2, rng, "S2", 0, "sensitivity"),
            "f3": cell(dc, rng, "S2", 0, "sensitivity")}
    return out


def sens_combined(recs, rng) -> dict:
    """S3 combined gap-OR-volume catalyst."""
    f2 = f2_vals(recs, cat_comb_of)
    dc, _, _ = f3_day_contrasts(recs, cat_comb_of, down=True)
    return {"f2": cell(f2, rng, "S3", 0, "sensitivity"),
            "f3": cell(dc, rng, "S3", 0, "sensitivity")}


def sens_idio(recs, rng) -> dict:
    """S4 per-stock |market residual| on catalyst vs non-catalyst days."""
    diffs = []
    for rec in recs:
        oos = rec["oos"]
        m = rec["mkt"][oos]
        x = rec["r"][oos]
        if np.var(m) == 0.0:
            continue
        beta = float(np.cov(m, x)[0, 1] / np.var(m))
        resid = x - beta * m
        cat = cat_comb_of(rec)[oos]
        if int(cat.sum()) < MIN_CATALYST_DAYS or \
                int((~cat).sum()) < MIN_NONCATALYST_DAYS:
            continue
        diffs.append(float(np.abs(resid)[cat].mean())
                     - float(np.abs(resid)[~cat].mean()))
    return cell(np.array(diffs, dtype=np.float64), rng, "S4", 0,
                "sensitivity")


def sens_is(recs, rng) -> dict:
    """S5 IS record (2000-2015) descriptive."""
    om = lambda rec: ((rec["idx"] < pd.Timestamp(ERA_OOS))
                      & np.isfinite(rec["r"]) & np.isfinite(rec["mkt"]))
    return {"f1": cell(f1_vals(recs, om), rng, "S5", 0, "sensitivity"),
            "f2_gap": cell(f2_vals(recs, cat_gap_of, om), rng, "S5", 0,
                           "sensitivity"),
            "f2_vol": cell(f2_vals(recs, cat_vol_of, om), rng, "S5", 0,
                           "sensitivity"),
            "f3_gap": cell(f3_day_contrasts(recs, cat_gap_of, True, om)[0],
                           rng, "S5", 0, "sensitivity"),
            "f3_vol": cell(f3_day_contrasts(recs, cat_vol_of, True, om)[0],
                           rng, "S5", 0, "sensitivity")}


def sens_year(recs, rng) -> dict:
    """S6 per-year pooled ret contrast (gap) + F3-gap down-day contrast."""
    out = {}
    for y in OOS_YEARS:
        lo = pd.Timestamp(f"{y}-01-01")
        hi = pd.Timestamp(f"{y + 1}-01-01")
        o = lambda rec, lo=lo, hi=hi: (rec["oos"] & (rec["idx"] >= lo)
                                       & (rec["idx"] < hi))
        cat_rets, non_rets = [], []
        for rec in recs:
            sel = rec["oos"] & o(rec)
            cat = cat_gap_of(rec) & sel
            non = (~cat_gap_of(rec)) & sel
            cat_rets.extend(rec["r"][cat].tolist())
            non_rets.extend(rec["r"][non].tolist())
        pooled = (float(np.mean(cat_rets)) - float(np.mean(non_rets))
                  if cat_rets and non_rets else None)
        dc, _, _ = f3_day_contrasts(recs, cat_gap_of, True, o)
        out[str(y)] = {"n_cat_days": len(cat_rets),
                       "n_non_days": len(non_rets),
                       "pooled_ret_contrast": pooled,
                       "f3_down_mean": float(dc.mean()) if len(dc) else None,
                       "f3_down_n": int(len(dc))}
    return out


def sens_ew(recs, rng) -> dict:
    """S7 equal-weight S&P 600 mean as the market factor."""
    agg = {}
    for rec in recs:
        for i in np.flatnonzero(np.isfinite(rec["r"])):
            d = rec["idx"][i]
            if d not in agg:
                agg[d] = [0.0, 0]
            agg[d][0] += rec["r"][i]
            agg[d][1] += 1
    ew = pd.Series({d: (s / c if c >= EW_MIN_CONTRIB else np.nan)
                    for d, (s, c) in sorted(agg.items())})
    er = []
    for rec in recs:
        m = ew.reindex(rec["idx"]).to_numpy(dtype=np.float64)
        er.append({**rec, "mkt": m,
                   "oos": (rec["idx"] >= pd.Timestamp(ERA_OOS))
                   & np.isfinite(rec["r"]) & np.isfinite(m)})
    return {"f1": cell(f1_vals(er), rng, "S7", 0, "sensitivity"),
            "f2_gap": cell(f2_vals(er, cat_gap_of), rng, "S7", 0,
                           "sensitivity"),
            "f2_vol": cell(f2_vals(er, cat_vol_of), rng, "S7", 0,
                           "sensitivity"),
            "f3_gap": cell(f3_day_contrasts(er, cat_gap_of, True)[0], rng,
                           "S7", 0, "sensitivity"),
            "f3_vol": cell(f3_day_contrasts(er, cat_vol_of, True)[0], rng,
                           "S7", 0, "sensitivity"),
            "ew_days": int(len(ew))}


def sens_updown(recs, rng) -> dict:
    """S8 up-market-day F3 contrast + down-minus-up two-sample contrast
    (the catalyst up-bias control)."""
    out = {}
    for leg in F3_LEGS:
        catf = cat_gap_of if leg == "gap" else cat_vol_of
        dd, _, _ = f3_day_contrasts(recs, catf, True)
        ud, _, _ = f3_day_contrasts(recs, catf, False)
        est = med = lo = hi = p = None
        if len(dd) and len(ud):
            est, med, lo, hi, p = two_sample_excess(dd, ud, rng)
        out[leg] = {"down": cell(dd, rng, "S8", 0, "sensitivity"),
                    "up": cell(ud, rng, "S8", 0, "sensitivity"),
                    "down_minus_up": [est, med, lo, hi, p]}
    return out


def sens_fisherz(recs, rng) -> dict:
    """S9 Fisher-z transformed correlations (F1, F2-gap, F2-vol)."""
    z1 = []
    for rec in recs:
        oos = rec["oos"]
        if int(oos.sum()) < MIN_OOS_DAYS:
            continue
        m = np.isfinite(rec["r"][oos]) & np.isfinite(rec["mkt"][oos])
        if int(m.sum()) < 2:
            continue
        x, y = rec["r"][oos][m], rec["mkt"][oos][m]
        if x.std() == 0 or y.std() == 0:
            continue
        r = float(np.corrcoef(x, y)[0, 1])
        if abs(r) < 1.0:
            z1.append(float(np.arctanh(r)))
    dz = {}
    for leg in F2_LEGS:
        catf = cat_gap_of if leg == "gap" else cat_vol_of
        legdz = []
        for rec in recs:
            oos = rec["oos"]
            cat = catf(rec) & oos
            non = (~catf(rec)) & oos
            if int(cat.sum()) < MIN_CATALYST_DAYS or \
                    int(non.sum()) < MIN_NONCATALYST_DAYS:
                continue
            zc = pearson_z(rec["r"][cat], rec["mkt"][cat])
            zn = pearson_z(rec["r"][non], rec["mkt"][non])
            if zc is not None and zn is not None:
                legdz.append(zc - zn)
        dz[leg] = np.array(legdz, dtype=np.float64)
    out = {"f1": {"n": len(z1),
                  "mean_z": float(np.mean(z1)) if z1 else None,
                  "corr_from_z": float(np.tanh(np.mean(z1)))
                  if z1 else None,
                  "p": None}}
    for leg in F2_LEGS:
        v = dz[leg]
        out[f"f2_{leg}"] = {
            "n": int(len(v)),
            "mean_z": float(np.mean(v)) if len(v) else None,
            "corr_diff_from_z": float(np.tanh(np.mean(v)))
            if len(v) else None}
    return out


def pearson_z(x: np.ndarray, y: np.ndarray):
    cc = pearson(x, y)
    if cc is None or abs(cc) >= 1.0:
        return None
    return float(np.arctanh(cc))


# --------------------------------------------------------------------------
# Census + audit
# --------------------------------------------------------------------------
def census_of(recs) -> dict:
    f1c = f2gc = f2vc = 0
    oos_days = cat_gap_days = cat_vol_days = 0
    down = set()
    for rec in recs:
        oos = rec["oos"]
        n_oos = int(oos.sum())
        oos_days += n_oos
        if n_oos >= MIN_OOS_DAYS:
            f1c += 1
        cg = cat_gap_of(rec) & oos
        cv = cat_vol_of(rec) & oos
        if int(cg.sum()) >= MIN_CATALYST_DAYS and \
                int((~cat_gap_of(rec) & oos).sum()) >= MIN_NONCATALYST_DAYS:
            f2gc += 1
        if int(cv.sum()) >= MIN_CATALYST_DAYS and \
                int((~cat_vol_of(rec) & oos).sum()) >= MIN_NONCATALYST_DAYS:
            f2vc += 1
        cat_gap_days += int(cg.sum())
        cat_vol_days += int(cv.sum())
        down.update(rec["idx"][oos & (rec["mkt"] < 0)])
    return {"n_stocks": len(recs),
            "oos_stock_days": int(oos_days),
            "cat_gap_stock_days": int(cat_gap_days),
            "cat_vol_stock_days": int(cat_vol_days),
            "f1_candidates": int(f1c),
            "f2_gap_candidates": int(f2gc),
            "f2_vol_candidates": int(f2vc),
            "n_down_days_total": int(len(down))}


def audit(cur: list, hist: list, mkt_spy: pd.Series, recs: list,
          ctr: dict) -> dict:
    """Input-integrity audit; computes NO measurement (counts only)."""
    issues = []
    n_cur_missing = len([t for t in cur
                         if not (BARS_DIR / f"{t}.parquet").exists()])
    n_hist_missing = len([t for t in hist
                          if not (BARS_DIR / f"{t}.parquet").exists()])
    if len(cur) != 603:
        issues.append(f"current universe {len(cur)} != 603")
    if n_cur_missing != len(MISSING_CUR):
        issues.append(f"current missing-bars {n_cur_missing} != {len(MISSING_CUR)}")
    if len(hist) != 904:
        issues.append(f"hist union {len(hist)} != 904")
    if n_hist_missing != 198:
        issues.append(f"hist missing-bars {n_hist_missing} != 198")
    spy = load_bars("SPY")
    if spy.index.min().year != 2000 or spy.index.max().year != 2025:
        issues.append("SPY does not span 2000-2025")
    if bool(spy["Close"].isna().any()):
        issues.append("SPY Close contains NaN")
    cen = census_of(recs)
    if cen["f1_candidates"] < MIN_STOCKS:
        issues.append(f"F1 floor unmet: {cen['f1_candidates']} stocks with "
                      f">= {MIN_OOS_DAYS} OOS days < {MIN_STOCKS}")
    if cen["f2_gap_candidates"] < MIN_STOCKS:
        issues.append(f"F2-gap floor unmet: {cen['f2_gap_candidates']} "
                      f"< {MIN_STOCKS}")
    if cen["f2_vol_candidates"] < MIN_STOCKS:
        issues.append(f"F2-vol floor unmet: {cen['f2_vol_candidates']} "
                      f"< {MIN_STOCKS}")
    if cen["n_down_days_total"] < MIN_DOWN_DAYS:
        issues.append(f"down-days {cen['n_down_days_total']} < "
                      f"{MIN_DOWN_DAYS}")
    return {"ok": not issues, "issues": issues, "current_n": len(cur),
            "current_missing": n_cur_missing,
            "hist_n": len(hist), "hist_missing": n_hist_missing,
            "census": cen, "counters": {k: ctr[k] for k in
                                        ("n_index0", "n_bad_prior_close",
                                         "n_missing_mkt_oos",
                                         "n_vol_nan_stocks")}}


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------
def cl(r: dict) -> str:
    """Concise rendering of a cell's estimates."""
    return (f"n={r['n']} | mean {fmt_num(r['mean'], '+.4f')} | "
            f"CI {fmt_num(r['ci_low'], '+.4f')}.."
            f"{fmt_num(r['ci_upper'], '+.4f')} | p {r['p']:.4f}")


def build_report(mode: str, results: dict) -> list:
    """Report lines for measure / gate / audit-only modes."""
    fams = results.get("families", {})
    lines = results.get("verdict_lines", [])
    audit_res = results["audit"]
    L = []
    title = ("# I-F-03 market-trend measurement report "
             "(pre-registration #18)") if mode != "gate" else (
                 "# I-F-03 §5 gate report (pre-registration #18) — "
                 "historical-constituent re-check")
    L.append(title)
    L.append("")
    if mode == "audit-only":
        L.append("- Mode: input audit only — NO measurement computed.")
        L.append("- Frozen-input facts verified (see the audit block below); "
                 "the audit is the whole output of this mode.")
        L += audit_lines(audit_res)
        L.append("")
        L.append("## Reproducibility")
        L.append("")
        L.append(f"- Tool sha (raw file): {results['measure_code_sha256']}")
        L.append(f"- Engine sha (measure.py, NOT invoked): "
                 f"{results['engine_code_sha256']}")
        return "\n".join(L) + "\n"

    L.append(f"- Pre-registration #18 (frozen 2026-08-21): claim = 'Stocks "
             f"will trend with the overall market unless they have a reason "
             f"not to' (txWaMpSzHhM [31:55-32:38]). Ledger row I-F-03; "
             f"priority-list item 17 (the final testable-daily item).")
    L.append("- Structural campaign: no forward returns, no entry/exit, no "
             "cost. The Phase-3 engine's measure_returns is NOT invoked — "
             "the claim is about co-movement, not profitability. Phase 5 "
             "cannot fire from this campaign by construction.")
    L.append(f"- Universe: {results['universe_label']}. Market factor: SPY "
             "daily close-to-close (equal-weight S&P 600 mean = sensitivity "
             "S7). Era split: IS 2000-2015 / OOS 2016-2025 (by bar date).")
    L.append(f"- Bootstrap B={B}, seed {SEED}, alpha {ALPHA}, Holm within "
             f"each family; catalyst = gap |open/prior close - 1| >= "
             f"{GAP_PRIMARY} OR RV = vol/mean(vol, prior 20) >= {RV_PRIMARY}.")
    L.append("")
    L.append("## Verdicts — Family 1 (market-trending baseline)")
    L.append("")
    if fam1 := fams.get("f1"):
        L.append(lines[0])
    L.append("")
    L.append("## Verdicts — Family 2 (catalyst decoupling)")
    L.append("")
    L.extend(lines[1:3])
    L.append("")
    L.append("## Verdicts — Family 3 (buck-the-trend)")
    L.append("")
    L.extend(lines[3:5])
    L.append("")
    L.append("## Census")
    L.append("")
    cen = results["census"]
    L.append("| measure | value |")
    L.append("|---|---|")
    for k, v in cen.items():
        L.append(f"| {k} | {v} |")
    L.append("")
    if mode == "measure":
        L.append("## Sensitivities (pre-declared, exploratory — NO verdicts)")
        L.append("")
        sens = results["sensitivities"]
        L.extend(sens_lines(sens))
        L.append("")
        L.append("## IS record (2000-2015, descriptive — no verdicts)")
        L.append("")
        if "is" in sens:
            for k in ("f1", "f2_gap", "f2_vol", "f3_gap", "f3_vol"):
                L.append(f"- IS-{k}: {cl(sens['is'][k])}")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_if03.py [--gate]` regenerates "
             "this report; the seed is fixed, so bootstrap results are "
             "stable across runs.")
    L.append(f"- Tool sha256: {results['measure_code_sha256']} (frozen "
             f"fixed-point sha {results['frozen_sha'][:16]}…)")
    L.append(f"- Engine sha (measure.py, NOT invoked): "
             f"{results['engine_code_sha256']}")
    L.append(f"- Report sha256: {results.get('report_sha') or '__REPORT_SHA__'}")
    L.append("")
    return "\n".join(L) + "\n"


def audit_lines(audit_res: dict) -> list:
    L = ["", "## Input audit", ""]
    L.append(f"- ok: {audit_res['ok']}")
    if audit_res["issues"]:
        L.append("- issues:")
        for i in audit_res["issues"]:
            L.append(f"  - {i}")
    cen = audit_res["census"]
    L.append("- census: " + "; ".join(f"{k}={v}" for k, v in cen.items()))
    ctr = audit_res["counters"]
    L.append("- counters: " + "; ".join(f"{k}={v}" for k, v in ctr.items()))
    return L


def sens_lines(sens: dict) -> list:
    L = []
    for label in ("gap=0.01", "gap=0.03", "gap=0.05"):
        if label in sens:
            s = sens[label]
            L.append(f"- S1 {label}: F2 {cl(s['f2'])} | F3 {cl(s['f3'])}")
    for label in ("vol=1.5", "vol=3.0"):
        if label in sens:
            s = sens[label]
            L.append(f"- S2 {label}: F2 {cl(s['f2'])} | F3 {cl(s['f3'])}")
    if "combined" in sens:
        s = sens["combined"]
        L.append(f"- S3 combined gap-OR-vol: F2 {cl(s['f2'])} | "
                 f"F3 {cl(s['f3'])}")
    if "idio" in sens:
        L.append(f"- S4 |market residual| cat - non: {cl(sens['idio'])}")
    if "year" in sens:
        yrs = sens["year"]
        L.append("- S6 per-year: " + "; ".join(
            f"{y}: pooled {v['pooled_ret_contrast'] if v['pooled_ret_contrast'] is not None else '—'} "
            f"(cat {v['n_cat_days']} / non {v['n_non_days']} days), "
            f"F3-gap {v['f3_down_mean'] if v['f3_down_mean'] is not None else '—'} "
            f"({v['f3_down_n']} days)"
            for y, v in sens["year"].items()))
    if "ew" in sens:
        s = sens["ew"]
        L.append(f"- S7 EW market ({s['ew_days']} days): "
                 f"F1 {cl(s['f1'])} | F2-gap {cl(s['f2_gap'])} | "
                 f"F2-vol {cl(s['f2_vol'])} | F3-gap {cl(s['f3_gap'])} | "
                 f"F3-vol {cl(s['f3_vol'])}")
    if "updown" in sens:
        for leg in F3_LEGS:
            s = sens["updown"][leg]
            dmu = s["down_minus_up"]
            dmu_s = ("—" if dmu[0] is None
                     else f"{dmu[0]:+.4f} (CI {dmu[2]:+.4f}..{dmu[3]:+.4f}, "
                          f"p {dmu[4]:.4f})")
            L.append(f"- S8 F3-{leg} up-day contrast: down {cl(s['down'])} "
                     f"| up {cl(s['up'])} | down-minus-up {dmu_s}")
    if "fisherz" in sens:
        fz = sens["fisherz"]
        f1 = fz["f1"]
        L.append(f"- S9 F1 (z): n={f1['n']} mean z "
                 f"{f1['mean_z'] if f1['mean_z'] is not None else '—'}, "
                 f"corr {f1['corr_from_z'] if f1['corr_from_z'] is not None else '—'}")
        for leg in F2_LEGS:
            f2 = fz[f"f2_{leg}"]
            L.append(f"- S9 F2-{leg} (z): n={f2['n']} mean dz "
                     f"{f2['mean_z'] if f2['mean_z'] is not None else '—'}, "
                     f"corr-diff "
                     f"{f2['corr_diff_from_z'] if f2['corr_diff_from_z'] is not None else '—'}")
    return L


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-only", action="store_true",
                    help="input audit + census only; computes NO measurement")
    ap.add_argument("--gate", action="store_true",
                    help="pre-registered §5 gate: F1/F2/F3 re-run on the "
                         "historical-constituent union")
    args = ap.parse_args()

    self_check()
    measure_code = raw_sha256(Path(__file__))
    engine_code = raw_sha256(Path(measure.__file__))[:16]
    universe_sha = raw_sha256(UNIVERSE_CSV)[:16]
    hist_sha = raw_sha256(HIST_UNIVERSE)[:16]

    cur = pd.read_csv(UNIVERSE_CSV, dtype={"ticker": str})["ticker"].tolist()
    hist = pd.read_csv(HIST_UNIVERSE, dtype={"ticker": str})["ticker"].tolist()
    mkt_spy = market_series_spy()

    ctr = {"n_stocks": 0, "n_index0": 0, "n_vol_nan_stocks": 0,
           "n_bad_prior_close": 0, "n_missing_mkt_oos": 0}
    cur_recs = [stock_record(t, mkt_spy, ctr) for t in cur
                if (BARS_DIR / f"{t}.parquet").exists()]
    audit_res = audit(cur, hist, mkt_spy, cur_recs, ctr)
    if not audit_res["ok"]:
        print("REFUSED: input audit FAILED:")
        for i in audit_res["issues"]:
            print("  -", i)
        return 1

    if args.audit_only:
        results = {"mode": "audit-only", "frozen_sha": FROZEN_SHA,
                   "measure_code_sha256": measure_code,
                   "engine_code_sha256": engine_code, "audit": audit_res,
                   "report_sha": ""}
        write_report(results, "audit-only", REPORT)
        sha = hashlib.sha256(REPORT.read_bytes()).hexdigest()
        results["report_sha"] = sha
        write_report(results, "audit-only", REPORT)
        print(f"wrote {REPORT.name} (audit-only)")
        print(f"measure_code_sha256: {measure_code}")
        print(f"report sha256: {sha}")
        return 0

    rng = np.random.default_rng(SEED)
    if args.gate:
        gctr = {"n_stocks": 0, "n_index0": 0, "n_vol_nan_stocks": 0,
                "n_bad_prior_close": 0, "n_missing_mkt_oos": 0}
        gate_records = [stock_record(t, mkt_spy, gctr) for t in hist
                        if (BARS_DIR / f"{t}.parquet").exists()]
        fams, lines = run_families(gate_records, rng)
        census = census_of(gate_records)
        results = {
            "mode": "gate", "pre_reg": "#18",
            "claim": "Stocks will trend with the overall market unless they "
                     "have a reason not to",
            "frozen_date": "2026-08-21",
            "params": {"gap": GAP_PRIMARY, "rv": RV_PRIMARY,
                       "rv_window": RV_WINDOW, "min_oos": MIN_OOS_DAYS,
                       "min_cat": MIN_CATALYST_DAYS,
                       "min_noncat": MIN_NONCATALYST_DAYS,
                       "min_stocks": MIN_STOCKS,
                       "min_down": MIN_DOWN_DAYS, "min_sides": MIN_SIDES},
            "era_label": "IS 2000-2015 / OOS 2016-2025 (by bar date)",
            "universe_label": "hist union 904 (706 with bars) — §5 gate",
            "frozen_sha": FROZEN_SHA, "measure_code_sha256": measure_code,
            "engine_code_sha256": engine_code, "universe_sha": universe_sha,
            "hist_sha": hist_sha, "audit": audit_res,
            "families": fams, "verdict_lines": lines, "census": census,
            "sensitivities": {}, "report_sha": ""}
        write_report(results, "gate", GATE_REPORT)
        GATE_RESULTS.write_text(json.dumps(results, indent=2),
                                encoding="utf-8")
        sha = hashlib.sha256(GATE_REPORT.read_bytes()).hexdigest()
        results["report_sha"] = sha
        write_report(results, "gate", GATE_REPORT)
        GATE_RESULTS.write_text(json.dumps(results, indent=2),
                                encoding="utf-8")
        print(f"wrote {GATE_REPORT.name} + {GATE_RESULTS.name}")
        print(f"measure_code_sha256: {measure_code}")
        print(f"report sha256: {sha}")
        for line in lines:
            print(line.replace("**", ""))
        return 0

    fams, lines = run_families(cur_recs, rng)
    census = census_of(cur_recs)
    sens = {
        **sens_gap_vol(cur_recs, rng),
        "combined": sens_combined(cur_recs, rng),
        "idio": sens_idio(cur_recs, rng),
        "is": sens_is(cur_recs, rng),
        "year": sens_year(cur_recs, rng),
        "ew": sens_ew(cur_recs, rng),
        "updown": sens_updown(cur_recs, rng),
        "fisherz": sens_fisherz(cur_recs, rng),
    }
    results = {
        "mode": "measure", "pre_reg": "#18",
        "claim": "Stocks will trend with the overall market unless they "
                 "have a reason not to",
        "frozen_date": "2026-08-21",
        "params": {"gap": GAP_PRIMARY, "rv": RV_PRIMARY,
                   "rv_window": RV_WINDOW, "min_oos": MIN_OOS_DAYS,
                   "min_cat": MIN_CATALYST_DAYS,
                   "min_noncat": MIN_NONCATALYST_DAYS,
                   "min_stocks": MIN_STOCKS, "min_down": MIN_DOWN_DAYS,
                   "min_sides": MIN_SIDES},
        "era_label": "IS 2000-2015 / OOS 2016-2025 (by bar date)",
        "universe_label": "current 603 (599 with bars; 4 missing logged)",
        "frozen_sha": FROZEN_SHA, "measure_code_sha256": measure_code,
        "engine_code_sha256": engine_code, "universe_sha": universe_sha,
        "hist_sha": hist_sha, "audit": audit_res,
        "families": fams, "verdict_lines": lines, "census": census,
        "sensitivities": sens, "report_sha": ""}
    write_report(results, "measure", REPORT)
    RESULTS.write_text(json.dumps(results, indent=2), encoding="utf-8")
    sha = hashlib.sha256(REPORT.read_bytes()).hexdigest()
    results["report_sha"] = sha
    write_report(results, "measure", REPORT)
    RESULTS.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"wrote {REPORT.name} + {RESULTS.name}")
    print(f"measure_code_sha256: {measure_code}")
    print(f"report sha256: {sha}")
    for line in lines:
        print(line.replace("**", ""))
    return 0


def write_report(results: dict, mode: str, target: Path) -> None:
    target.write_text(build_report(mode, results), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
