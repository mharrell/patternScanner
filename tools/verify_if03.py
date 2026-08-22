"""Independent verification of the I-F-03 measurement (pre-registration #18).

Recomputes the I-F-03 families + sensitivities from the frozen bar files with
STANDALONE code — imports nothing from tools/* (measure.py, measure_if03.py,
measure_divergence.py, measure_veto.py are all intentionally avoided), uses
fresh bootstrap seeds, and compares against the recorded
data/cache/if03_measure_results.json.

Check classes:
  EXACT     (tol 1e-9): census counts, family unit-vector lengths + means,
            deterministic sensitivity values (S6 per-year, S7 EW, S9
            Fisher-z), Holm gates, verdict categories.
  MC-SPREAD (fresh seeds): every bootstrapped estimate (est / med / CI / p)
            recomputed with fresh RNGs and required to land within a
            tolerance derived from the bootstrap SE of the statistic; verdict
            categories re-derived from the fresh stats and required to match.

Exit 0 only when every check passes; exit 1 on any FAIL.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
BARS = ROOT / "data" / "cache" / "bars"
CACHE = ROOT / "data" / "cache"
UNI = CACHE / "universe_sp600_2026-08-13.csv"
HIST = CACHE / "universe_sp600_hist_2026-08-15.csv"
RES_JSON = CACHE / "if03_measure_results.json"

# ---- frozen parameters (pre-reg #18 sec 3) ----
GAP, RV, WIN = 0.02, 2.0, 20
MIN_OOS, MIN_CAT, MIN_NON = 100, 30, 30
MIN_STK, MIN_DOWN, MIN_SIDES = 100, 100, 5
ERA = pd.Timestamp("2016-01-01")
B, ALPHA, SEED = 1000, 0.05, 20260813
EW_MIN_CONTRIB = 100
FRESH_SEEDS = [1013, 2707, 4217]  # independent fresh bootstrap seeds

PASS = FAIL = 0


def check(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {detail}")


def close(a, b, tol):
    return abs(a - b) <= tol


# ---------------------------------------------------------------------------
# Standalone data path (frozen input contract, no imports from the stack)
# ---------------------------------------------------------------------------
_bars = {}


def load(t):
    if t not in _bars:
        df = pd.read_parquet(BARS / f"{t}.parquet",
                             columns=["Open", "Close", "Volume"])
        df.index = pd.to_datetime(df.index)
        _bars[t] = df
    return _bars[t]


def mkt_spy():
    df = load("SPY")
    c = df["Close"].to_numpy(np.float64)
    r = np.full(len(c), np.nan)
    r[1:] = c[1:] / c[:-1] - 1.0
    return pd.Series(r, index=df.index)


def record(t, mkt):
    df = load(t)
    c = df["Close"].to_numpy(np.float64)
    o = df["Open"].to_numpy(np.float64)
    v = df["Volume"].to_numpy(np.float64)
    n = len(df)
    idx = df.index

    r = np.full(n, np.nan)
    gap = np.full(n, np.nan)
    if n >= 2:
        prev = c[:-1]
        valid = np.isfinite(prev) & (prev != 0.0) & np.isfinite(c[1:]) \
            & np.isfinite(o[1:])
        r[1:] = np.where(valid, c[1:] / prev - 1.0, np.nan)
        gap[1:] = np.where(valid, np.abs(o[1:] / prev - 1.0), np.nan)

    rv = np.full(n, np.nan)
    mean20 = pd.Series(v).rolling(WIN).mean().shift(1).to_numpy(np.float64)
    ok = np.isfinite(v) & np.isfinite(mean20) & (mean20 > 0.0)
    rv[ok] = v[ok] / mean20[ok]

    mm = mkt.reindex(idx).to_numpy(np.float64)
    oos = (idx >= ERA) & np.isfinite(r) & np.isfinite(mm)
    return {"idx": idx, "r": r, "gap": np.abs(gap), "rv": rv, "mkt": mm,
            "oos": oos}


def pearson(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    if int(m.sum()) < 2:
        return None
    xx, yy = x[m], y[m]
    if xx.std() == 0.0 or yy.std() == 0.0:
        return None
    return float(np.corrcoef(xx, yy)[0, 1])


def pearson_z(x, y):
    cc = pearson(x, y)
    if cc is None or abs(cc) >= 1.0:
        return None
    return float(np.arctanh(cc))


# ---------------------------------------------------------------------------
# Unit vectors (independent implementations)
# ---------------------------------------------------------------------------
def f1_units(recs, maskf=None):
    out = []
    for rec in recs:
        oos = rec["oos"] if maskf is None else maskf(rec)
        if int(oos.sum()) < MIN_OOS:
            continue
        cc = pearson(rec["r"][oos], rec["mkt"][oos])
        if cc is not None:
            out.append(cc)
    return np.array(out, np.float64)


def f2_units(recs, catf, maskf=None):
    out = []
    for rec in recs:
        oos = rec["oos"] if maskf is None else maskf(rec)
        cat = catf(rec) & oos
        non = (~catf(rec)) & oos
        if int(cat.sum()) < MIN_CAT or int(non.sum()) < MIN_NON:
            continue
        cc = pearson(rec["r"][cat], rec["mkt"][cat])
        cn = pearson(rec["r"][non], rec["mkt"][non])
        if cc is not None and cn is not None:
            out.append(cc - cn)
    return np.array(out, np.float64)


def f3_units(recs, catf, down, maskf=None):
    days = {}
    for rec in recs:
        oos = rec["oos"] if maskf is None else maskf(rec)
        if down is None:
            sel = oos
        elif down:
            sel = oos & (rec["mkt"] < 0)
        else:
            sel = oos & (rec["mkt"] > 0)
        cat = catf(rec)
        for i in np.flatnonzero(sel):
            d = rec["idx"][i]
            days.setdefault(d, ([], []))
            (days[d][0] if cat[i] else days[d][1]).append(rec["r"][i])
    contr, qual, excl = [], [], 0
    for d, (cv, nv) in days.items():
        if len(cv) >= MIN_SIDES and len(nv) >= MIN_SIDES:
            contr.append(float(np.mean(cv)) - float(np.mean(nv)))
            qual.append(d)
        else:
            excl += 1
    return np.array(contr, np.float64), qual, excl


def cat_gap(rec, g=GAP):
    return rec["gap"] >= g


def cat_vol(rec, v=RV):
    return rec["rv"] >= v


def cat_comb(rec):
    return cat_gap(rec) | cat_vol(rec)


# ---------------------------------------------------------------------------
# Bootstrap + Holm + verdict (standalone)
# ---------------------------------------------------------------------------
def boot_mean(x, rng):
    m = len(x)
    b = np.empty(B)
    for i in range(B):
        b[i] = x[rng.integers(0, m, size=m)].mean()
    lo, hi = np.percentile(b, [2.5, 97.5])
    p = 2.0 * min((b <= 0).mean(), (b >= 0).mean())
    return (float(b.mean()), float(np.median(b)), float(lo), float(hi),
            float(p), float(b.std()))


def verdict_cat(n, est, ci_lo, ci_hi, p, gate, rej, floor, positive):
    """Verdict category; `positive` = the claim is "statistic > 0" (F1/F3)
    as opposed to F2's "statistic < 0" (decoupling: correlation lower)."""
    if n < floor:
        return "INCONCLUSIVE"
    if positive:
        if rej and ci_lo > 0.0:
            return "EDGE"
        if rej and ci_hi < 0.0:
            return "FADE"
    else:
        if rej and ci_hi < 0.0:
            return "EDGE"
        if rej and ci_lo > 0.0:
            return "FADE"
    return "NO EDGE"


def rec_cat_of(verdict: str) -> str:
    for tok in ("INCONCLUSIVE", "EDGE", "FADE", "NO EDGE"):
        if verdict.startswith(tok):
            return tok
    raise ValueError(f"unparsed verdict {verdict!r}")


def cell_checks(name, rec_cell, vec, floor, positive=True):
    """EXACT n/mean; MC-spread est/CI/p; verdict category from fresh stats
    (only when the recorded cell carries a verdict)."""
    n = int(len(vec))
    check(f"{name}-n", n == rec_cell["n"], f"got {n} vs {rec_cell['n']}")
    check(f"{name}-mean", close(float(vec.mean()), rec_cell["mean"], 1e-9),
          f"got {vec.mean():.12f} vs {rec_cell['mean']}")
    if n == 0:
        return
    rng0 = np.random.default_rng(FRESH_SEEDS[0])
    rng1 = np.random.default_rng(FRESH_SEEDS[1])
    est_tol, ci_tol, p_tol, _ = mc_tols(vec, rng0)
    est, med, lo, hi, p, _ = boot_mean(vec, rng1)
    check(f"{name}-est", close(est, rec_cell["est"], est_tol),
          f"got {est:.6f} vs {rec_cell['est']}")
    check(f"{name}-ci-lo", close(lo, rec_cell["ci_low"], ci_tol),
          f"got {lo:.6f} vs {rec_cell['ci_low']} (tol {ci_tol:.2e})")
    check(f"{name}-ci-hi", close(hi, rec_cell["ci_upper"], ci_tol),
          f"got {hi:.6f} vs {rec_cell['ci_upper']} (tol {ci_tol:.2e})")
    check(f"{name}-p", abs(p - rec_cell["p"]) <= p_tol,
          f"got {p:.4f} vs {rec_cell['p']}")
    if "verdict" in rec_cell:
        gate = rec_cell["holm_gate"]
        cat = verdict_cat(n, est, lo, hi, p, gate, p <= gate, floor, positive)
        rec_cat = rec_cat_of(rec_cell["verdict"])
        check(f"{name}-verdict", cat == rec_cat,
              f"got {cat} vs {rec_cell['verdict']}")


def mc_tols(x, rng):
    """bootstrap SE of the mean -> MC tolerances for est / CI / p."""
    m = len(x)
    b = np.empty(B)
    for i in range(B):
        b[i] = x[rng.integers(0, m, size=m)].mean()
    s = float(b.std())
    return 3.0 * s / np.sqrt(B), 0.6 * s, 0.05, s


def holm_two(pvals):
    """Holm gates + rejections for the two-slot F2/F3 families (stable
    tie-break by insertion order, matching the frozen stack)."""
    gates, rej = {}, {}
    for rank, s in enumerate(sorted(("gap", "vol"), key=lambda s: pvals[s]),
                             start=1):
        gates[s] = ALPHA / (2 - rank + 1)
        rej[s] = pvals[s] <= gates[s]
    return gates, rej


def main() -> int:
    global PASS, FAIL
    rec = json.loads(RES_JSON.read_text(encoding="utf-8"))
    cur = pd.read_csv(UNI, dtype={"ticker": str})["ticker"].tolist()
    hist = pd.read_csv(HIST, dtype={"ticker": str})["ticker"].tolist()

    mkt = mkt_spy()
    print("== frozen-input integrity ==")
    check("current-universe-603", len(cur) == 603, f"got {len(cur)}")
    check("hist-union-904", len(hist) == 904, f"got {len(hist)}")
    cur_bars = [t for t in cur if (BARS / f"{t}.parquet").exists()]
    hist_bars = [t for t in hist if (BARS / f"{t}.parquet").exists()]
    check("current-with-bars-599", len(cur_bars) == 599, f"got {len(cur_bars)}")
    check("hist-with-bars-706", len(hist_bars) == 706, f"got {len(hist_bars)}")
    spy = load("SPY")
    check("SPY-2000-2025",
          spy.index.min().year == 2000 and spy.index.max().year == 2025)

    recs = [record(t, mkt) for t in cur_bars]
    fam = rec["families"]

    # ---- census ----
    print("\n== census (EXACT) ==")
    f1c = f2gc = f2vc = 0
    oos_days = cat_gap_days = cat_vol_days = 0
    down = set()
    for rr in recs:
        oos = rr["oos"]
        n_o = int(oos.sum())
        oos_days += n_o
        if n_o >= MIN_OOS:
            f1c += 1
        cg = cat_gap(rr) & oos
        cv = cat_vol(rr) & oos
        if int(cg.sum()) >= MIN_CAT and \
                int((~cat_gap(rr) & oos).sum()) >= MIN_NON:
            f2gc += 1
        if int(cv.sum()) >= MIN_CAT and \
                int((~cat_vol(rr) & oos).sum()) >= MIN_NON:
            f2vc += 1
        cat_gap_days += int(cg.sum())
        cat_vol_days += int(cv.sum())
        down.update(rr["idx"][oos & (rr["mkt"] < 0)])
    cen = dict(n_stocks=len(recs), oos_stock_days=oos_days,
               cat_gap_stock_days=cat_gap_days, cat_vol_stock_days=cat_vol_days,
               f1_candidates=f1c, f2_gap_candidates=f2gc,
               f2_vol_candidates=f2vc, n_down_days_total=len(down))
    for k, v in cen.items():
        check(f"census-{k}", cen[k] == rec["census"][k],
              f"got {cen[k]} vs {rec['census'][k]}")

    # ---- families ----
    print("\n== families (EXACT means + MC-spread CIs) ==")
    cell_checks("F1", fam["f1"], f1_units(recs), MIN_STK, positive=True)
    cell_checks("F2-gap", fam["f2"]["gap"], f2_units(recs, cat_gap), MIN_STK,
                positive=False)
    cell_checks("F2-vol", fam["f2"]["vol"], f2_units(recs, cat_vol), MIN_STK,
                positive=False)
    f3g, _, exclg = f3_units(recs, cat_gap, True)
    f3v, _, exclv = f3_units(recs, cat_vol, True)
    check("F3-gap-excl", exclg == fam["f3"]["gap"]["n_excluded_days"],
          f"got {exclg} vs {fam['f3']['gap']['n_excluded_days']}")
    check("F3-vol-excl", exclv == fam["f3"]["vol"]["n_excluded_days"],
          f"got {exclv} vs {fam['f3']['vol']['n_excluded_days']}")
    cell_checks("F3-gap", fam["f3"]["gap"], f3g, MIN_DOWN)
    cell_checks("F3-vol", fam["f3"]["vol"], f3v, MIN_DOWN)

    # ---- Holm gates (recomputed from recorded p; must reproduce) ----
    print("\n== Holm gates ==")
    g2, _ = holm_two({"gap": fam["f2"]["gap"]["p"],
                      "vol": fam["f2"]["vol"]["p"]})
    g3, _ = holm_two({"gap": fam["f3"]["gap"]["p"],
                      "vol": fam["f3"]["vol"]["p"]})
    for leg in ("gap", "vol"):
        check(f"F2-{leg}-gate", g2[leg] == fam["f2"][leg]["holm_gate"],
              f"got {g2[leg]} vs {fam['f2'][leg]['holm_gate']}")
        check(f"F3-{leg}-gate", g3[leg] == fam["f3"][leg]["holm_gate"],
              f"got {g3[leg]} vs {fam['f3'][leg]['holm_gate']}")

    # ---- sensitivities ----
    print("\n== sensitivities ==")
    s = rec["sensitivities"]
    for label in ("gap=0.01", "gap=0.03", "gap=0.05"):
        g = float(label.split("=")[1])
        cell_checks(f"S1-{label}-F2", s[label]["f2"],
                    f2_units(recs, lambda r, g=g: cat_gap(r, g)), 0)
        dc, _, _ = f3_units(recs, lambda r, g=g: cat_gap(r, g), True)
        cell_checks(f"S1-{label}-F3", s[label]["f3"], dc, 0)
    for label in ("vol=1.5", "vol=3.0"):
        v = float(label.split("=")[1])
        cell_checks(f"S2-{label}-F2", s[label]["f2"],
                    f2_units(recs, lambda r, v=v: cat_vol(r, v)), 0)
        dc, _, _ = f3_units(recs, lambda r, v=v: cat_vol(r, v), True)
        cell_checks(f"S2-{label}-F3", s[label]["f3"], dc, 0)
    cell_checks("S3-F2", s["combined"]["f2"], f2_units(recs, cat_comb), 0)
    dc, _, _ = f3_units(recs, cat_comb, True)
    cell_checks("S3-F3", s["combined"]["f3"], dc, 0)

    # S4 idiosyncratic move size
    d4 = []
    for rr in recs:
        oos = rr["oos"]
        mm, xx = rr["mkt"][oos], rr["r"][oos]
        if np.var(mm) == 0.0:
            continue
        beta = float(np.cov(mm, xx)[0, 1] / np.var(mm))
        resid = xx - beta * mm
        cat = cat_comb(rr)[oos]
        if int(cat.sum()) < MIN_CAT or int((~cat).sum()) < MIN_NON:
            continue
        d4.append(float(np.abs(resid)[cat].mean()) -
                  float(np.abs(resid)[~cat].mean()))
    cell_checks("S4-idio", s["idio"], np.array(d4, np.float64), 0)

    # S5 IS record
    om = lambda rr: ((rr["idx"] < ERA) & np.isfinite(rr["r"])
                     & np.isfinite(rr["mkt"]))
    cell_checks("IS-f1", s["is"]["f1"], f1_units(recs, om), 0)
    cell_checks("IS-f2_gap", s["is"]["f2_gap"], f2_units(recs, cat_gap, om), 0)
    cell_checks("IS-f2_vol", s["is"]["f2_vol"], f2_units(recs, cat_vol, om), 0)
    dc, _, _ = f3_units(recs, cat_gap, True, om)
    cell_checks("IS-f3_gap", s["is"]["f3_gap"], dc, 0)
    dc, _, _ = f3_units(recs, cat_vol, True, om)
    cell_checks("IS-f3_vol", s["is"]["f3_vol"], dc, 0)

    # S6 per-year (deterministic)
    for y in range(2016, 2026):
        lo = pd.Timestamp(f"{y}-01-01")
        hi = pd.Timestamp(f"{y + 1}-01-01")
        yy = s["year"][str(y)]
        cat_r, non_r = [], []
        for rr in recs:
            sel = rr["oos"] & (rr["idx"] >= lo) & (rr["idx"] < hi)
            cat = cat_gap(rr) & sel
            non = (~cat_gap(rr)) & sel
            cat_r.extend(rr["r"][cat].tolist())
            non_r.extend(rr["r"][non].tolist())
        pooled = float(np.mean(cat_r)) - float(np.mean(non_r))
        check(f"S6-{y}-pooled",
              close(pooled, yy["pooled_ret_contrast"], 1e-9),
              f"got {pooled:.12f} vs {yy['pooled_ret_contrast']}")
        check(f"S6-{y}-ncat", len(cat_r) == yy["n_cat_days"],
              f"got {len(cat_r)} vs {yy['n_cat_days']}")
        check(f"S6-{y}-nnon", len(non_r) == yy["n_non_days"],
              f"got {len(non_r)} vs {yy['n_non_days']}")
        od = lambda rr, lo=lo, hi=hi: (rr["oos"] & (rr["idx"] >= lo)
                                       & (rr["idx"] < hi))
        dc, _, _ = f3_units(recs, cat_gap, True, od)
        fm = float(dc.mean()) if len(dc) else None
        check(f"S6-{y}-f3mean",
              (fm == yy["f3_down_mean"]) if fm is None
              else close(fm, yy["f3_down_mean"], 1e-9),
              f"got {fm} vs {yy['f3_down_mean']}")
        check(f"S6-{y}-f3n", len(dc) == yy["f3_down_n"],
              f"got {len(dc)} vs {yy['f3_down_n']}")

    # S7 equal-weight market
    agg = {}
    for rr in recs:
        for i in np.flatnonzero(np.isfinite(rr["r"])):
            d = rr["idx"][i]
            agg.setdefault(d, [0.0, 0])
            agg[d][0] += rr["r"][i]
            agg[d][1] += 1
    ew = pd.Series({d: (tot / c if c >= EW_MIN_CONTRIB else np.nan)
                    for d, (tot, c) in sorted(agg.items())})
    check("S7-ew_days", int(len(ew)) == s["ew"]["ew_days"],
          f"got {len(ew)} vs {s['ew']['ew_days']}")
    erecs = []
    for rr in recs:
        m = ew.reindex(rr["idx"]).to_numpy(np.float64)
        erecs.append({"idx": rr["idx"], "r": rr["r"], "gap": rr["gap"],
                      "rv": rr["rv"], "mkt": m,
                      "oos": (rr["idx"] >= ERA) & np.isfinite(rr["r"])
                      & np.isfinite(m)})
    for k, vec in (("f1", f1_units(erecs)),
                   ("f2_gap", f2_units(erecs, cat_gap)),
                   ("f2_vol", f2_units(erecs, cat_vol))):
        cell_checks(f"S7-{k}", s["ew"][k], vec, 0)
    for leg, vec in (("gap", f3_units(erecs, cat_gap, True)[0]),
                     ("vol", f3_units(erecs, cat_vol, True)[0])):
        cell_checks(f"S7-f3_{leg}", s["ew"][f"f3_{leg}"], vec, 0)

    # S8 up-down two-sample contrast (MC-spread)
    for leg in ("gap", "vol"):
        cf = cat_gap if leg == "gap" else cat_vol
        dd, _, _ = f3_units(recs, cf, True)
        ud, _, _ = f3_units(recs, cf, False)
        rng = np.random.default_rng(FRESH_SEEDS[2])
        diffs = np.empty(B)
        for bi in range(B):
            s1 = dd[rng.integers(0, len(dd), size=len(dd))].mean()
            s2 = ud[rng.integers(0, len(ud), size=len(ud))].mean()
            diffs[bi] = s1 - s2
        lo, hi = np.percentile(diffs, [2.5, 97.5])
        p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
        dmu = s["updown"][leg]["down_minus_up"]
        tol = 0.6 * float(diffs.std())
        check(f"S8-{leg}-dmu-est",
              close(float(diffs.mean()), dmu[0], tol),
              f"got {diffs.mean():.6f} vs {dmu[0]}")
        check(f"S8-{leg}-dmu-ci",
              close(lo, dmu[2], tol) and close(hi, dmu[3], tol),
              f"got {lo:.6f}..{hi:.6f} vs {dmu[2]}..{dmu[3]}")
        check(f"S8-{leg}-dmu-p", abs(p - dmu[4]) <= 0.05,
              f"got {p:.4f} vs {dmu[4]}")

    # S9 Fisher-z (EXACT)
    z1 = []
    for rr in recs:
        oos = rr["oos"]
        if int(oos.sum()) < MIN_OOS:
            continue
        m = np.isfinite(rr["r"][oos]) & np.isfinite(rr["mkt"][oos])
        if int(m.sum()) < 2:
            continue
        x, y = rr["r"][oos][m], rr["mkt"][oos][m]
        if x.std() == 0 or y.std() == 0:
            continue
        cc = float(np.corrcoef(x, y)[0, 1])
        if abs(cc) < 1.0:
            z1.append(float(np.arctanh(cc)))
    fz1 = s["fisherz"]["f1"]
    check("S9-f1-n", len(z1) == fz1["n"], f"got {len(z1)} vs {fz1['n']}")
    check("S9-f1-mean_z", close(float(np.mean(z1)), fz1["mean_z"], 1e-9),
          f"got {np.mean(z1):.12f} vs {fz1['mean_z']}")
    check("S9-f1-corr",
          close(float(np.tanh(np.mean(z1))), fz1["corr_from_z"], 1e-9),
          f"got {np.tanh(np.mean(z1)):.12f} vs {fz1['corr_from_z']}")
    for leg in ("gap", "vol"):
        cf = cat_gap if leg == "gap" else cat_vol
        dz = []
        for rr in recs:
            oos = rr["oos"]
            cat = cf(rr) & oos
            non = (~cf(rr)) & oos
            if int(cat.sum()) < MIN_CAT or int(non.sum()) < MIN_NON:
                continue
            zc = pearson_z(rr["r"][cat], rr["mkt"][cat])
            zn = pearson_z(rr["r"][non], rr["mkt"][non])
            if zc is not None and zn is not None:
                dz.append(zc - zn)
        fz2 = s["fisherz"][f"f2_{leg}"]
        check(f"S9-f2_{leg}-n", len(dz) == fz2["n"],
              f"got {len(dz)} vs {fz2['n']}")
        check(f"S9-f2_{leg}-mean_z",
              close(float(np.mean(dz)), fz2["mean_z"], 1e-9),
              f"got {np.mean(dz):.12f} vs {fz2['mean_z']}")
        check(f"S9-f2_{leg}-cdiff",
              close(float(np.tanh(np.mean(dz))), fz2["corr_diff_from_z"], 1e-9),
              f"got {np.tanh(np.mean(dz)):.12f} vs {fz2['corr_diff_from_z']}")

    print()
    print(f"VERIFICATION: {PASS} passed, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
