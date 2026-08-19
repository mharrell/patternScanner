"""Pre-registration #16 measurement tool — the price-tier family.

Implements exactly PREREGISTRATION.md pre-reg #16 §2 (and §3's gate):
  F1 (I-D-01 "my sweet spot is $2-5", A-04 ">$10 unprofitable") —
    short-horizon price-tier screen: N=10 forward returns by close-price
    band, four Holm-corrected contrast slots, day-paired bootstrap.
  F2 (I-X-06 "penny stocks and small caps fall drastically over the long
    term") — the 2021 snapshot cohort: index-exit rates (F2a, exact from
    the frozen artifact's first_seen/n_snapshots) and multi-year cumulative
    returns (F2b, 3y primary).
  §5 gate (--gate): F1 re-run on the current-constituent universe
    (OOS 2016-2025); F2 re-anchored on the 2022 cohort (horizon
    2025-12-31). Gate slots with unmet floors are INCONCLUSIVE (pre-reg
    §3: "INCONCLUSIVE on either → gate UNMET with a documented data
    limitation") — the gate is reported, never refused.

Freeze discipline (pre-reg §6): FROZEN_SHA is the sha256 of this file with
its own FROZEN_SHA hex blanked to 64 zeros (a file cannot hash to a value
embedded in it; blanking makes it well-defined). It is asserted at every
run; no forward-return computation happens before the freeze lands.
measure_code_sha256 (raw file sha) is recorded in every output.

Band semantics (recorded decisions, zero parameter freedom):
  tier_of(c):  lt2 [0,2) | 2-5 [2,5) | 5-10 [5,10) | 10-20 [10,20) | gt20 [20,∞)
  F1 slots use the claim's TRADING bands: lt2 bar-dates sit below the
  $2 floor of both stated bands and are excluded from the F1a/F1b/F1c
  verdict slots (reported as a descriptive row). F1b's low leg is [2,10)
  — A-04's "$2-10 trading band" (translation row) — vs high leg [10,∞).
  F1d follows the pre-reg's literal "(<$10)": the same-name control's low
  leg includes lt2 (in this universe the lt2 population is ~empty, so the
  distinction is a rounding decision — recorded here).
  F2's pooled low leg is <$10 INCLUDING lt2 — the penny-stock claim
  (I-X-06) is about the cheapest names, so no $2 floor applies there.

Run:  python -X utf8 tools/measure_pricetier.py [--audit-only] [--gate]
Exit codes: 0 ok; 1 input audit FAILED; 2 measurement floors unmet
(primary run refused — one-shot rule); 3 not-frozen / input error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Frozen constants (pre-reg #16 — no parameter may change after freeze)
# --------------------------------------------------------------------------
REPO = Path(__file__).resolve().parents[1]
BARS_DIR = REPO / "data" / "cache" / "bars"
HIST_UNIVERSE = REPO / "data" / "cache" / "universe_sp600_hist_2026-08-15.csv"
CURRENT_UNIVERSE = REPO / "data" / "cache" / "universe_sp600_2026-08-13.csv"
PROVENANCE = REPO / "data" / "cache" / "hist_universe_provenance.json"
RESULTS_JSON = REPO / "data" / "cache" / "pricetier_measure_results.json"
REPORT_MD = REPO / "data" / "cache" / "pricetier_measure_report.md"

N_PRIMARY = 10          # pre-reg #16 §2: N = 10 primary (house)
N_ALTS = (5, 20)        # sensitivity N=5/20
COST = 0.0015           # house §6 round-trip cost
B = 1000                # bootstrap resamples
SEED = 20260819         # pre-reg #16 §2
ALPHA = 0.05            # Holm per family
OOS_START = np.datetime64("2022-01-01")     # primary era (snapshot-bracketed)
OOS_END = np.datetime64("2025-12-31")       # bars end here
IS_START = np.datetime64("2021-06-30")      # IS, descriptive only
GATE_OOS_START = np.datetime64("2016-01-01")  # gate era (current universe)
FLOORS = {"f1_bar_dates": 100, "f1_names": 10, "f2_names": 30}
COHORT_2021 = "2021-06"     # F2 primary cohort (exact: 601 names)
COHORT_2022 = "2022-06"     # F2 §5 gate cohort
F2_ANCHOR = {"2021-06": "2021-06-30", "2022-06": "2022-06-30"}
F2_HORIZONS = {"1y": "2022-06-30", "2y": "2023-06-30", "3y": "2024-06-30",
               "4y": "2025-06-30"}       # F2b primary: 3y (2024-06-30)
F2_GATE_HORIZONS = {"1y": "2023-06-30", "2y": "2024-06-30",
                    "3y": "2025-06-30", "3.5y": "2025-12-31"}
F2_GATE_PRIMARY = "3.5y"    # gate primary: horizon to 2025-12-31 (pre-reg §3)
FROZEN_SHA = "675106eb8b31431566e8188828692b7a5624d1ae13a5df138c7c2197663e6e89"


# --------------------------------------------------------------------------
# Freeze machinery
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
def tier_of(c: float) -> str:
    if c < 2:
        return "lt2"
    if c < 5:
        return "2-5"
    if c < 10:
        return "5-10"
    if c < 20:
        return "10-20"
    return "gt20"


BAND_ORDER = ("lt2", "2-5", "5-10", "10-20", "gt20")


def load_universe() -> tuple[pd.DataFrame, pd.DataFrame]:
    hist = pd.read_csv(HIST_UNIVERSE, dtype={"ticker": str}).set_index("ticker")
    cur = pd.read_csv(CURRENT_UNIVERSE, dtype={"ticker": str}).set_index("ticker")
    return hist, cur


class Bars:
    """Per-name daily bars (cached in memory per run)."""

    def __init__(self, tickers: list[str]):
        self.tickers = tickers
        self.dates: dict[str, np.ndarray] = {}
        self.close: dict[str, np.ndarray] = {}
        self.missing: list[str] = []
        for t in tickers:
            f = BARS_DIR / f"{t}.parquet"
            if not f.exists():
                self.missing.append(t)
                continue
            df = pd.read_parquet(f)
            self.dates[t] = df.index.to_numpy()
            self.close[t] = df["Close"].to_numpy(dtype=float)

    def fwd_ret(self, t: str, i: int, n: int) -> float:
        """Close[t+i+n]/Close[t+i] - 1 (COST applied at aggregation)."""
        return self.close[t][i + n] / self.close[t][i] - 1.0


# --------------------------------------------------------------------------
# Bootstrap (house bootstrap_excess conventions)
# --------------------------------------------------------------------------
def two_sample_boot(a: np.ndarray, b: np.ndarray, rng) -> dict:
    """Contrast a.mean() - b.mean(); B draws resampling each leg with
    replacement; percentile 2.5/97.5 CI; p = 2*min(P(diff<=0), P(diff>=0))."""
    M, K = len(a), len(b)
    if M == 0 or K == 0:
        raise ValueError(f"empty leg: M={M} K={K}")
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    est = float(a.mean() - b.mean())
    diffs = np.empty(B)
    for r in range(B):
        sa = a[rng.integers(0, M, M)]
        sb = b[rng.integers(0, K, K)]
        diffs[r] = sa.mean() - sb.mean()
    ci_low, ci_high = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min(float((diffs <= 0).mean()), float((diffs >= 0).mean()))
    return {"est": est, "ci_low": float(ci_low), "ci_high": float(ci_high),
            "p": min(p, 1.0)}


def day_paired_boot(low_dates: np.ndarray, high_dates: np.ndarray,
                    rng) -> dict:
    """Day-paired contrast: aligned per-bar-date cross-sectional means.
    Resample M dates with replacement; contrast over draws (pre-reg §2:
    M = min leg n over dates where both tiers are present)."""
    M = len(low_dates)
    if M == 0:
        raise ValueError("empty paired dates")
    low_dates = np.asarray(low_dates, dtype=float)
    high_dates = np.asarray(high_dates, dtype=float)
    est = float(low_dates.mean() - high_dates.mean())
    diffs = np.empty(B)
    for r in range(B):
        idx = rng.integers(0, M, M)
        diffs[r] = low_dates[idx].mean() - high_dates[idx].mean()
    ci_low, ci_high = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min(float((diffs <= 0).mean()), float((diffs >= 0).mean()))
    return {"est": est, "ci_low": float(ci_low), "ci_high": float(ci_high),
            "p": min(p, 1.0)}


def holm(slots: list[dict], label: str) -> list[dict]:
    """Holm at ALPHA across the slots; adds gate/rejected/verdict.
    Verdict by slot direction (pre-reg §2):
      upward slots (F1a/b/c, F2a): EDGE iff rejected AND CI-low > 0,
        FADE iff rejected AND CI-upper < 0.
      downward slots (F2b): EDGE iff rejected AND CI-upper < 0,
        FADE iff rejected AND CI-low > 0.
    Slot dicts carry "direction": "up" or "down"."""
    n = len(slots)
    order = sorted(range(n), key=lambda i: slots[i]["p"])
    prev_gate = 1.0
    for rank, i in enumerate(order):
        gate = ALPHA / (n - rank)
        slots[i]["gate"] = min(gate, prev_gate)
        slots[i]["holm_rejected"] = slots[i]["p"] <= slots[i]["gate"]
        prev_gate = slots[i]["gate"]
        if not slots[i]["holm_rejected"]:
            slots[i]["verdict"] = "NO EDGE"
        elif slots[i]["direction"] == "down":
            if slots[i]["ci_high"] < 0:
                slots[i]["verdict"] = "EDGE"
            elif slots[i]["ci_low"] > 0:
                slots[i]["verdict"] = "FADE"
            else:
                slots[i]["verdict"] = "NO EDGE"
        else:
            if slots[i]["ci_low"] > 0:
                slots[i]["verdict"] = "EDGE"
            elif slots[i]["ci_high"] < 0:
                slots[i]["verdict"] = "FADE"
            else:
                slots[i]["verdict"] = "NO EDGE"
    return slots


# --------------------------------------------------------------------------
# F1 — price-tier screen (I-D-01 / A-04)
# --------------------------------------------------------------------------
def f1_bands(tickers: list[str], n_need: int, cost: float, bars: Bars,
             era: tuple, tier_offsets: tuple = (0,)) -> dict:
    """Per bar-date (in era), per band: list of pair returns.

    Returns band -> {date -> [ret]}, per-band pair registries, and drops
    (t+N beyond the bar series)."""
    band_dates: dict[str, dict] = {b: {} for b in BAND_ORDER}
    band_pairs: dict[str, list] = {b: [] for b in BAND_ORDER}
    drops = {b: 0 for b in BAND_ORDER}
    era_start, era_end = era
    for t in sorted(tickers):
        dts = bars.dates.get(t)
        if dts is None:
            continue
        closes = bars.close[t]
        n = len(dts)
        for i in range(n):
            d = dts[i]
            if d < era_start:
                continue
            if d > era_end:
                break
            ti = i
            for off in tier_offsets:
                if off:
                    if i - off < 0:
                        ti = -1
                        break
                    ti = i - off
            if ti < 0:
                continue  # lag points before the series start — not a pair
            if i + n_need >= n:
                drops[tier_of(closes[ti])] += 1
                continue
            band = tier_of(closes[ti])
            r = bars.fwd_ret(t, i, n_need) - cost
            band_dates[band].setdefault(str(d), []).append(r)
            band_pairs[band].append((t, str(d), float(r)))
    return {"band_dates": band_dates, "band_pairs": band_pairs,
            "drops": drops}


def f1_slot(band_dates: dict, low_bands: tuple, high_bands: tuple,
            rng) -> dict | None:
    """Day-paired contrast low - high over dates where both legs present."""
    dates = sorted(set().union(*[band_dates[b].keys() for b in low_bands],
                               *[band_dates[b].keys() for b in high_bands]))
    lows, highs, used = [], [], []
    for d in dates:
        ll = [r for b in low_bands for r in band_dates[b].get(d, [])]
        hh = [r for b in high_bands for r in band_dates[b].get(d, [])]
        if ll and hh:
            lows.append(float(np.mean(ll)))
            highs.append(float(np.mean(hh)))
            used.append(d)
    if not lows:
        return None
    res = day_paired_boot(np.array(lows), np.array(highs), rng)
    res["n_dates"] = len(lows)
    res["dates"] = used
    return res


def f1d_same_name(band_pairs: dict, rng) -> dict | None:
    """Same-name control (pre-reg §2 F1d): each low-tier (<$10, incl. lt2)
    bar-date matched to the SAME name's >$20 bar-dates (the pair's own
    bar-date excluded from the pool — pools are distinct per pair)."""
    lows = [p for p in band_pairs["lt2"] + band_pairs["2-5"]
            + band_pairs["5-10"]]
    high_pools: dict[str, list[float]] = {}
    for t, d, r in band_pairs["gt20"]:
        high_pools.setdefault(t, []).append(r)
    paired = []
    dropped = 0
    for t, d, r in lows:
        pool = high_pools.get(t, [])
        if not pool:
            dropped += 1
            continue
        paired.append((t, r, pool))
    if not paired:
        return None
    M = len(paired)
    est_high = float(np.mean([p[2][rng.integers(0, len(p[2]))] for p in paired]))
    diffs = np.empty(B)
    for k in range(B):
        idx = rng.integers(0, M, M)
        hl = np.array([paired[i][2][rng.integers(0, len(paired[i][2]))]
                       for i in idx])
        diffs[k] = np.mean([paired[i][1] for i in idx]) - hl.mean()
    ci_low, ci_high = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min(float((diffs <= 0).mean()), float((diffs >= 0).mean()))
    est_low = float(np.mean([p[1] for p in paired]))
    return {"est": est_low - est_high, "ci_low": float(ci_low),
            "ci_high": float(ci_high), "p": min(p, 1.0), "n_pairs": M,
            "n_dropped": dropped, "n_low_names": len({p[0] for p in paired}),
            "direction": "up"}


SLOT_DEFS = {
    "F1a_2_5_vs_gt20": (("2-5",), ("gt20",)),
    "F1b_2_10_vs_gt10": (("2-5", "5-10"), ("10-20", "gt20")),
    "F1c_10_20_vs_gt20": (("10-20",), ("gt20",)),
}


def measure_f1(tickers: list[str], bars: Bars, rng, n_need: int = N_PRIMARY,
               cost: float = COST, era: tuple = (OOS_START, OOS_END),
               tier_offsets: tuple = (0,),
               rows_era: tuple | None = None) -> dict:
    """Full F1 family: slots, floors, rows. rows_era covers IS+OOS for the
    primary (per-year rows incl. 2021); defaults to era (gate)."""
    if rows_era is None:
        rows_era = era
    res = f1_bands(tickers, n_need, cost, bars, era, tier_offsets)
    bd = res["band_dates"]
    bp = res["band_pairs"]
    slots: dict[str, dict] = {}
    for key, (lo, hi) in SLOT_DEFS.items():
        s = f1_slot(bd, lo, hi, rng)
        if s is None:
            s = {"est": None, "ci_low": None, "ci_high": None, "p": 1.0,
                 "n_dates": 0, "dates": []}
        lo_names = {p[0] for b in lo for p in bp[b]}
        hi_names = {p[0] for b in hi for p in bp[b]}
        s["n_low_names"] = len(lo_names)
        s["n_high_names"] = len(hi_names)
        s["direction"] = "up"
        slots[key] = s
    f1d = f1d_same_name(bp, rng)
    if f1d is None:
        f1d = {"est": None, "ci_low": None, "ci_high": None, "p": 1.0,
               "n_pairs": 0, "n_dropped": 0, "n_low_names": 0,
               "direction": "up"}
    slots["F1d_same_name"] = f1d
    # floors (pre-reg §2: >=100 bar-dates/slot AND >=10 names/band-slot)
    floors = {}
    for key, (lo, hi) in SLOT_DEFS.items():
        n_dates = slots[key]["n_dates"]
        n_names = min(slots[key]["n_low_names"], slots[key]["n_high_names"])
        floors[key] = {"bar_dates": n_dates, "names": n_names,
                       "ok": n_dates >= FLOORS["f1_bar_dates"]
                       and n_names >= FLOORS["f1_names"]}
    floors["F1d_same_name"] = {
        "pairs": f1d["n_pairs"], "names": f1d["n_low_names"],
        "ok": f1d["n_pairs"] >= FLOORS["f1_bar_dates"]
        and f1d["n_low_names"] >= FLOORS["f1_names"]}
    # rows from the (wider) rows era: per-band stats, per-year means,
    # name-day collapse, IS block (primary only)
    rr = f1_bands(tickers, n_need, cost, bars, rows_era, tier_offsets)
    rbp = rr["band_pairs"]
    rows = {"per_band": {}, "per_year": {}, "drops": res["drops"], "is": {}}
    for b in BAND_ORDER:
        pairs = rbp[b]
        if pairs:
            rets = np.array([p[2] for p in pairs])
            rows["per_band"][b] = {
                "n_pairs": int(len(rets)),
                "n_names": int(len({p[0] for p in pairs})),
                "mean": float(rets.mean()),
                "median": float(np.median(rets)),
                "p10": float(np.percentile(rets, 10)),
                "p90": float(np.percentile(rets, 90)),
            }
            years: dict[str, list] = {}
            for p in pairs:
                years.setdefault(p[1][:4], []).append(p[2])
            rows["per_year"][b] = {
                y: {"n": len(v), "mean": float(np.mean(v))}
                for y, v in sorted(years.items())}
            # IS block: signal bar-dates in [IS_START, 2021-12-31]
            is_vals = [p[2] for p in pairs
                       if p[1] >= str(IS_START)[:10]
                       and p[1][:4] == "2021"]
            if is_vals:
                rows["is"][b] = {"n": len(is_vals),
                                 "mean": float(np.mean(is_vals))}
        else:
            rows["per_band"][b] = {"n_pairs": 0, "n_names": 0,
                                   "mean": None, "median": None,
                                   "p10": None, "p90": None}
            rows["per_year"][b] = {}
    per_name = {}
    for v in rbp.values():
        for p in v:
            per_name[p[0]] = per_name.get(p[0], 0) + 1
    rows["name_day"] = {
        "n_pairs_total": int(sum(len(v) for v in rbp.values())),
        "n_names_total": int(len(per_name)),
        "max_pairs_per_name": max(per_name.values(), default=0)}
    rows["drops_oos"] = res["drops"]
    return {"slots": slots, "floors": floors, "rows": rows}


# --------------------------------------------------------------------------
# F2 — long-term fall (I-X-06)
# --------------------------------------------------------------------------
def f2_cohort(bars: Bars, hist: pd.DataFrame, cohort: str, horizons: dict,
              primary: str, rng) -> dict:
    """Cohort measurement: tier at anchor close; F2a removal (n_snapshots
    < max for first_seen — exact); F2b cumulative returns to horizons."""
    anchor = F2_ANCHOR[cohort]
    year = int(cohort[:4])
    max_n = 5 - (year - 2021)   # 2021 cohort: 5 snapshots; 2022: 4; ...
    members = []
    for t, row in hist[hist["first_seen"] == cohort].iterrows():
        dts = bars.dates.get(t)
        if dts is None:
            members.append({"ticker": t, "tier": "no_bars",
                            "removed": bool(row["n_snapshots"] < max_n),
                            "rets": {}})
            continue
        i0 = int(np.searchsorted(dts, np.datetime64(anchor)))
        if i0 >= len(dts):
            members.append({"ticker": t, "tier": "no_anchor",
                            "removed": bool(row["n_snapshots"] < max_n),
                            "rets": {}})
            continue
        c0 = float(bars.close[t][i0])
        tier = tier_of(c0)
        rets = {}
        for tag, hdate in horizons.items():
            i1 = int(np.searchsorted(dts, np.datetime64(hdate),
                                     side="right")) - 1
            if i1 <= i0:
                rets[tag] = None
            else:
                rets[tag] = float(bars.close[t][i1] / c0 - 1.0)
        members.append({"ticker": t, "tier": tier,
                        "removed": bool(row["n_snapshots"] < max_n),
                        "rets": rets})
    # verdict legs: pooled low = <$10 (incl. lt2), high = >$20
    low = [m for m in members if m["tier"] in ("lt2", "2-5", "5-10")]
    high = [m for m in members if m["tier"] == "gt20"]
    # F2a — removal (needs only the tier; no_bars excluded from verdict
    # legs — pre-reg: "no price data → no tier")
    a_low = np.array([m["removed"] for m in low])
    a_high = np.array([m["removed"] for m in high])
    if len(a_low) >= FLOORS["f2_names"] and len(a_high) >= FLOORS["f2_names"]:
        f2a = two_sample_boot(a_low, a_high, rng)
        f2a.update({"n_low": len(a_low), "n_high": len(a_high),
                    "rate_low": float(a_low.mean()),
                    "rate_high": float(a_high.mean())})
    else:
        f2a = {"n_low": len(a_low), "n_high": len(a_high),
               "rate_low": float(a_low.mean()) if len(a_low) else None,
               "rate_high": float(a_high.mean()) if len(a_high) else None,
               "est": None, "ci_low": None, "ci_high": None, "p": 1.0}
    f2a["direction"] = "up"
    f2a["verdict_rule"] = "EDGE iff Holm-rejected AND CI-low > 0"
    # F2b — returns, names with bars only (no-bar names excluded and counted)
    lo_ret = [m["rets"][primary] for m in low
              if m["rets"].get(primary) is not None]
    hi_ret = [m["rets"][primary] for m in high
              if m["rets"].get(primary) is not None]
    if len(lo_ret) >= FLOORS["f2_names"] and len(hi_ret) >= FLOORS["f2_names"]:
        f2b = two_sample_boot(np.array(lo_ret), np.array(hi_ret), rng)
        f2b.update({"n_low": len(lo_ret), "n_high": len(hi_ret),
                    "mean_low": float(np.mean(lo_ret)),
                    "mean_high": float(np.mean(hi_ret))})
    else:
        f2b = {"n_low": len(lo_ret), "n_high": len(hi_ret),
               "mean_low": float(np.mean(lo_ret)) if lo_ret else None,
               "mean_high": float(np.mean(hi_ret)) if hi_ret else None,
               "est": None, "ci_low": None, "ci_high": None, "p": 1.0}
    f2b["direction"] = "down"
    f2b["verdict_rule"] = "EDGE iff Holm-rejected AND CI-upper < 0"
    # rows: per-band removal + returns; purge share per band; no_bars row
    rows = {"per_band": {}, "purge_share": {}}
    for b in BAND_ORDER + ("no_bars", "no_anchor"):
        sub = [m for m in members if m["tier"] == b]
        if not sub:
            rows["per_band"][b] = None
            continue
        rr = {}
        for tag in horizons:
            vals = [m["rets"][tag] for m in sub
                    if m["rets"].get(tag) is not None]
            rr[tag] = float(np.mean(vals)) if vals else None
        rows["per_band"][b] = {
            "n": len(sub),
            "n_removed": int(sum(m["removed"] for m in sub)),
            "removal_rate": float(np.mean([m["removed"] for m in sub])),
            "rets": rr}
    for b in BAND_ORDER:
        sub = [m for m in members if m["tier"] == b]
        if sub:
            rows["purge_share"][b] = {"n": len(sub)}
    rows["n_members"] = len(members)
    rows["n_no_bars"] = sum(1 for m in members if m["tier"] == "no_bars")
    return {"f2a": f2a, "f2b": f2b, "rows": rows, "members": members,
            "primary_horizon": primary, "horizons": list(horizons),
            "cohort": cohort, "max_n": max_n}


def measure_f2(bars: Bars, hist: pd.DataFrame, rng,
               cohort: str = COHORT_2021, horizons: dict = F2_HORIZONS,
               primary: str = "3y") -> dict:
    return f2_cohort(bars, hist, cohort, horizons, primary, rng)


# --------------------------------------------------------------------------
# Sensitivities (exploratory, NO verdicts) — primary era only
# --------------------------------------------------------------------------
def measure_sensitivities(tickers: list[str], bars: Bars, hist: pd.DataFrame,
                          rng) -> dict:
    out = {}
    # N=5/20
    for n in N_ALTS:
        f1 = measure_f1(tickers, bars, rng, n_need=n)
        out[f"S-N{n}"] = {
            "slots": {k: {kk: v for kk, v in s.items() if kk != "dates"}
                      for k, s in f1["slots"].items()}}
    # S-BAND10: bands 2-10 vs >$20 (the 2019 filter)
    r = f1_bands(tickers, N_PRIMARY, COST, bars, (OOS_START, OOS_END))
    s = f1_slot(r["band_dates"], ("2-5", "5-10"), ("gt20",), rng)
    out["S-BAND10"] = {kk: v for kk, v in s.items() if kk != "dates"} if s \
        else {"est": None, "n_dates": 0}
    # S-LAG5: tier at Close[t-5]
    r5 = f1_bands(tickers, N_PRIMARY, COST, bars, (OOS_START, OOS_END),
                  tier_offsets=(5,))
    s = f1_slot(r5["band_dates"], ("2-5", "5-10"), ("gt20",), rng)
    out["S-LAG5"] = {kk: v for kk, v in s.items() if kk != "dates"} if s \
        else {"est": None, "n_dates": 0}
    # S-REL: bottom vs top price quartile at t (>=16 names per date so each
    # quartile has >=4)
    dates: dict[str, list] = {}
    for t in sorted(tickers):
        dts = bars.dates.get(t)
        if dts is None:
            continue
        closes = bars.close[t]
        n = len(dts)
        for i in range(n):
            d = dts[i]
            if d < OOS_START:
                continue
            if d > OOS_END:
                break
            if i + N_PRIMARY >= n:
                continue
            dates.setdefault(str(d), []).append(
                (closes[i], bars.fwd_ret(t, i, N_PRIMARY) - COST))
    lows, highs, n_dates = [], [], 0
    for d in sorted(dates):
        pairs = sorted(dates[d], key=lambda x: x[0])
        q = len(pairs) // 4
        if q < 4:
            continue
        lows.append(float(np.mean([p[1] for p in pairs[:q]])))
        highs.append(float(np.mean([p[1] for p in pairs[-q:]])))
        n_dates += 1
    s = day_paired_boot(np.array(lows), np.array(highs), rng) if lows else None
    out["S-REL"] = dict(s) if s else {"n_dates": 0}
    out["S-REL"]["n_dates"] = n_dates
    # S-ERA: F1b contrast per single year
    per_year = {}
    r = f1_bands(tickers, N_PRIMARY, COST, bars, (OOS_START, OOS_END))
    for y in range(2022, 2026):
        bd = {b: {d: v for d, v in dts.items() if d[:4] == str(y)}
              for b, dts in r["band_dates"].items()}
        s = f1_slot(bd, ("2-5", "5-10"), ("gt20",), rng)
        per_year[str(y)] = {kk: v for kk, v in s.items()
                            if kk != "dates"} if s else {"n_dates": 0}
    out["S-ERA"] = per_year
    # F2 horizon sensitivities: per-horizon contrast on the 2021 cohort
    f2 = f2_cohort(bars, hist, COHORT_2021, F2_HORIZONS, "3y", rng)
    legs = {b: [] for b in BAND_ORDER}
    for m in f2["members"]:
        if m["tier"] in legs:
            legs[m["tier"]].append(m)
    out["F2-horizons"] = {}
    for tag in F2_HORIZONS:
        lo = [m["rets"][tag] for m in legs["lt2"] + legs["2-5"]
              + legs["5-10"] if m["rets"].get(tag) is not None]
        hi = [m["rets"][tag] for m in legs["gt20"]
              if m["rets"].get(tag) is not None]
        if lo and hi:
            s = two_sample_boot(np.array(lo), np.array(hi), rng)
            out["F2-horizons"][tag] = {kk: v for kk, v in s.items()}
            out["F2-horizons"][tag]["n_low"] = len(lo)
            out["F2-horizons"][tag]["n_high"] = len(hi)
        else:
            out["F2-horizons"][tag] = {"n_low": len(lo), "n_high": len(hi),
                                       "est": None}
    return out


# --------------------------------------------------------------------------
# Audit (no returns)
# --------------------------------------------------------------------------
def audit(hist: pd.DataFrame, cur: pd.DataFrame, bars: Bars) -> dict:
    """Input-integrity audit: frozen-artifact facts verified (union size,
    first_seen/n_snapshots distributions, 2021-cohort removal count, bar
    presence). Computes NO returns."""
    prov = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    issues = []
    exp_fc = {"2021-06": 601, "2022-06": 65, "2023-06": 83,
              "2024-06": 81, "2025-06": 74}
    exp_ns = {1: 163, 2: 164, 3: 134, 4: 101, 5: 342}
    fc = hist["first_seen"].value_counts().to_dict()
    ns = hist["n_snapshots"].value_counts().to_dict()
    n_union = len(hist)
    if n_union != prov["union"]["n_tickers"]:
        issues.append(f"union {n_union} != provenance "
                      f"{prov['union']['n_tickers']}")
    if fc != exp_fc:
        issues.append(f"first_seen {fc} != frozen {exp_fc}")
    if ns != exp_ns:
        issues.append(f"n_snapshots {ns} != frozen {exp_ns}")
    if prov["union"]["per_snapshot_ticker_sets"] != \
            {"2021-06": 601, "2022-06": 601, "2023-06": 601,
             "2024-06": 602, "2025-06": 602}:
        issues.append("provenance per-snapshot counts drifted")
    if len(cur) != 603:
        issues.append(f"current universe {len(cur)} != 603")
    # 2021-cohort removal (exact): n_snapshots < 5 among first_seen 2021-06
    c2021 = hist[hist["first_seen"] == COHORT_2021]
    rem = int((c2021["n_snapshots"] < 5).sum())
    if len(c2021) != 601 or rem != 259:
        issues.append(f"2021 cohort {len(c2021)} names / {rem} removed "
                      f"!= frozen 601/259")
    # bar presence on the union. NOTE: pre-reg #16's text says "199 purged"
    # — copied from pre-reg #13's narrative, which was itself off by one:
    # #13's own §8 says "the 706-name universe" (904 - 706 = 198). The
    # operative census, re-verified at tool freeze 2026-08-19: 198 purged /
    # 706 with bars (record-correction amendment accompanies this tool).
    missing = sorted(set(bars.missing) & set(hist.index))
    if len(missing) != 198:
        issues.append(f"purged (no bars) {len(missing)} != 198 (frozen "
                      f"census 2026-08-19)")
    cur_missing = sorted(set(bars.missing) & set(cur.index))
    ok = not issues
    return {"ok": ok, "issues": issues, "n_union": n_union,
            "n_with_bars": n_union - len(missing), "n_purged": len(missing),
            "n_current_purged": len(cur_missing), "cohort2021": len(c2021),
            "cohort2021_removed": rem}


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------
def _f(x, nd=4) -> str:
    return "-" if x is None else f"{x:.{nd}f}"


def write_report(results: dict, audit_res: dict, mode: str) -> None:
    L = []
    L.append("# Pre-registration #16 measure report — price-tier family "
             "(I-D-01 / I-X-06 / A-04)")
    L.append("")
    L.append(f"- Mode: {mode}")
    L.append(f"- FROZEN_SHA: {results['frozen_sha']}")
    L.append(f"- measure_code_sha256: {results['measure_code_sha256']}")
    L.append("")
    if mode == "audit-only":
        L.append("## Audit-only (no returns computed)")
        L.append("")
        L.append(f"- Audit: **{'PASSED' if audit_res['ok'] else 'FAILED'}**")
        for i in audit_res["issues"]:
            L.append(f"  - {i}")
        L.append("")
        L.append(f"- Union {audit_res['n_union']} names; bars present for "
                 f"{audit_res['n_with_bars']}; purged (no bars) "
                 f"{audit_res['n_purged']} (frozen census 2026-08-19; pre-reg "
                 f"#13/#16 narrative said 199 — off by one, the operative "
                 f"census was always 706 with bars).")
        L.append(f"- Current universe purged: {audit_res['n_current_purged']}.")
        L.append(f"- 2021 cohort: {audit_res['cohort2021']} names, "
                 f"{audit_res['cohort2021_removed']} removed (frozen "
                 f"record: 601/259).")
        L.append("")
    else:
        f1 = results["f1"]
        f2 = results["f2"]
        f2a, f2b = f2["f2a"], f2["f2b"]
        hz = f2["horizons"]
        L.append(f"## F1 — price-tier screen (I-D-01/A-04)")
        L.append("")
        L.append(f"- Universe: {results['universe_label']}; N = "
                 f"{results['n_need']}; era {results['era_label']}; "
                 f"COST {results['cost']}.")
        L.append("")
        L.append("### F1 floors (pre-reg §2: >=100 bar-dates/slot AND >=10 "
                 "distinct names/band-slot)")
        L.append("")
        L.append("| slot | bar-dates | names (low/high) | met |")
        L.append("|---|---|---|---|")
        for k, f_ in f1["floors"].items():
            if k == "F1d_same_name":
                L.append(f"| {k} | {f_['pairs']} pairs | "
                         f"{f_['names']} (low) | {'yes' if f_['ok'] else 'NO'} |")
            else:
                s = f1["slots"][k]
                L.append(f"| {k} | {f_['bar_dates']} | "
                         f"{s['n_low_names']}/{s['n_high_names']} | "
                         f"{'yes' if f_['ok'] else 'NO'} |")
        L.append("")
        L.append("### F1 verdicts (Holm at 0.05 across the 4 slots; EDGE iff "
                 "Holm-rejected AND CI-low > 0)")
        L.append("")
        L.append("| slot | n | est | CI-low | CI-high | p | gate | verdict |")
        L.append("|---|---|---|---|---|---|---|---|")
        for k, s in f1["slots"].items():
            n = s.get("n_dates", s.get("n_pairs", "-"))
            L.append(f"| {k} | {n} | {_f(s['est'])} | {_f(s['ci_low'])} | "
                     f"{_f(s['ci_high'])} | {_f(s['p'], 3)} | "
                     f"{_f(s.get('gate'), 3)} | {s.get('verdict', '-')} |")
        L.append("")
        L.append("### F1 rows (per band — reported regardless of verdict; "
                 "name-day collapse; lt2 descriptive)")
        L.append("")
        L.append("| band | n_pairs | names | mean | median | p10 | p90 |")
        L.append("|---|---|---|---|---|---|---|")
        for b in BAND_ORDER:
            r = f1["rows"]["per_band"][b]
            L.append(f"| {b} | {r['n_pairs']} | {r['n_names']} | "
                     f"{_f(r['mean'])} | {_f(r['median'])} | {_f(r['p10'])} "
                     f"| {_f(r['p90'])} |")
        L.append("")
        L.append("Per-year per-band means (measurement row):")
        for b in BAND_ORDER:
            ys = f1["rows"]["per_year"][b]
            if ys:
                L.append(f"- {b}: " + ", ".join(
                    f"{y} {_f(v['mean'])} (n={v['n']})"
                    for y, v in ys.items()))
        if f1["rows"]["is"]:
            L.append("")
            L.append("IS window 2021-06-30–2021-12-31 (descriptive only):")
            for b, v in f1["rows"]["is"].items():
                L.append(f"- {b}: mean {_f(v['mean'])} (n={v['n']})")
        L.append("")
        L.append(f"- Name-day collapse: "
                 f"{f1['rows']['name_day']['n_pairs_total']} (name, bar-date) "
                 f"pairs across {f1['rows']['name_day']['n_names_total']} "
                 f"distinct names.")
        L.append(f"- Drops (t+N beyond bars): {f1['rows']['drops_oos']}")
        L.append("")
        L.append(f"## F2 — long-term fall (I-X-06), cohort "
                 f"{f2['cohort']} ({results['f2_universe_label']}), primary "
                 f"horizon {f2['primary_horizon']}")
        L.append("")
        L.append("### F2a — index-exit rate (removed at least once; exact "
                 "from the frozen artifact: n_snapshots < max_n)")
        L.append("")
        L.append(f"- low (<$10): n={f2a.get('n_low', '-')}, rate "
                 f"{_f(f2a.get('rate_low'))} | high (>$20): n="
                 f"{f2a.get('n_high', '-')}, rate {_f(f2a.get('rate_high'))}")
        L.append(f"- contrast (low - high): {_f(f2a['est'])} (CI "
                 f"{_f(f2a['ci_low'])}..{_f(f2a['ci_high'])}, "
                 f"p={_f(f2a['p'], 3)}) — {f2a.get('verdict', '-')}; floor "
                 f">=30 names/leg: "
                 f"{'met' if (f2a.get('n_low') or 0) >= FLOORS['f2_names'] and (f2a.get('n_high') or 0) >= FLOORS['f2_names'] else 'UNMET'}")
        L.append("")
        L.append("### F2b — cumulative returns (names with bars only; no-bar "
                 "names excluded and counted)")
        L.append("")
        L.append(f"- low (<$10): n={f2b.get('n_low', '-')}, mean "
                 f"{_f(f2b.get('mean_low'))} | high (>$20): n="
                 f"{f2b.get('n_high', '-')}, mean {_f(f2b.get('mean_high'))}")
        L.append(f"- contrast (low - high): {_f(f2b['est'])} (CI "
                 f"{_f(f2b['ci_low'])}..{_f(f2b['ci_high'])}, "
                 f"p={_f(f2b['p'], 3)}) — {f2b.get('verdict', '-')}; floor: "
                 f"{'met' if (f2b.get('n_low') or 0) >= FLOORS['f2_names'] and (f2b.get('n_high') or 0) >= FLOORS['f2_names'] else 'UNMET'}")
        L.append("")
        L.append("### F2 rows (per band: removal + returns; purge share; "
                 "no-bar row)")
        L.append("")
        L.append("| band | n | n_removed | removal_rate | " +
                 " | ".join(f"{t} ret" for t in hz) + " |")
        L.append("|---|---|---|---" + "---" * len(hz) + "|")
        for b in BAND_ORDER + ("no_bars", "no_anchor"):
            r = f2["rows"]["per_band"].get(b)
            if not r:
                continue
            rets = " | ".join(_f(r["rets"].get(t)) for t in hz)
            L.append(f"| {b} | {r['n']} | {r['n_removed']} | "
                     f"{_f(r['removal_rate'])} | {rets} |")
        L.append("")
        if results.get("sensitivities"):
            L.append("## Sensitivities (exploratory, NO verdicts)")
            L.append("")
            for k, v in results["sensitivities"].items():
                if k.startswith("S-N"):
                    slots = v["slots"]
                    L.append(f"- {k}: " + "; ".join(
                        f"{sk} {_f(s['est'])} (n={s.get('n_dates', '-')})"
                        for sk, s in slots.items()))
                elif k == "F2-horizons":
                    L.append(f"- {k}: " + "; ".join(
                        f"{t} {_f(v2['est'])} (n={v2.get('n_low', '-')}/"
                        f"{v2.get('n_high', '-')})" for t, v2 in v.items()))
                elif k == "S-ERA":
                    L.append(f"- {k}: " + "; ".join(
                        f"{y} {_f(v2['est'])} (n={v2.get('n_dates', '-')})"
                        for y, v2 in v.items()))
                else:
                    L.append(f"- {k}: est {_f(v.get('est'))} "
                             f"(n={v.get('n_dates', v.get('n_pairs', '-'))})")
            L.append("")
        if mode == "gate":
            L.append("## §5 gate outcome")
            L.append("")
            L.append("- F1 gate: a slot is INCONCLUSIVE when its floors are "
                     "unmet (pre-reg §3 — gate UNMET with a documented data "
                     "limitation); PASSED iff an EDGE survives with floors "
                     "met.")
            L.append(f"- F1 gate: {results['gate_f1']}")
            L.append(f"- F2 gate: {results['gate_f2']}")
            L.append("")
    L.append("## Determinism")
    L.append("")
    L.append(f"- report sha256: {results['report_sha']}")
    REPORT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-only", action="store_true",
                    help="input audit + bar census only; computes NO returns")
    ap.add_argument("--gate", action="store_true",
                    help="pre-registered §5 gate: F1 on the current "
                         "constituents (OOS 2016-2025); F2 re-anchored on "
                         "the 2022 cohort")
    args = ap.parse_args()

    self_check()
    hist, cur = load_universe()
    tickers = sorted(set(hist.index) | set(cur.index))
    bars = Bars(tickers)
    audit_res = audit(hist, cur, bars)
    measure_code = raw_sha256(Path(__file__))

    if not audit_res["ok"]:
        print("REFUSED: input audit FAILED:")
        for i in audit_res["issues"]:
            print("  -", i)
        return 1

    if args.audit_only:
        results = {"mode": "audit-only", "frozen_sha": FROZEN_SHA,
                   "measure_code_sha256": measure_code, "report_sha": ""}
        write_report(results, audit_res, "audit-only")
        sha = hashlib.sha256(REPORT_MD.read_text("utf-8").encode()).hexdigest()
        results["report_sha"] = sha
        write_report(results, audit_res, "audit-only")
        print(f"wrote {REPORT_MD}")
        print(f"measure_code_sha256: {measure_code}")
        print(f"report sha256: {sha}")
        return 0

    rng = np.random.default_rng(SEED)
    if args.gate:
        era_label = "OOS 2016-2025"
        g_tickers = sorted(cur.index)
        f1 = measure_f1(g_tickers, bars, rng, era=(GATE_OOS_START, OOS_END))
        f2 = measure_f2(bars, hist, rng, cohort=COHORT_2022,
                        horizons=F2_GATE_HORIZONS, primary=F2_GATE_PRIMARY)
        results = {"mode": "gate", "frozen_sha": FROZEN_SHA,
                   "measure_code_sha256": measure_code,
                   "era_label": era_label, "n_need": N_PRIMARY,
                   "cost": COST, "universe_label": "current 603 (frozen "
                   "2026-08-13)", "f2_universe_label": "2022-06 cohort",
                   "f1": f1, "f2": f2, "sensitivities": {}}
    else:
        era_label = "OOS 2022-2025 (IS 2021-06-30-2021-12-31 descriptive)"
        h_tickers = sorted(hist.index)
        f1 = measure_f1(h_tickers, bars, rng, era=(OOS_START, OOS_END),
                        rows_era=(IS_START, OOS_END))
        f2 = measure_f2(bars, hist, rng)
        results = {"mode": "measure", "frozen_sha": FROZEN_SHA,
                   "measure_code_sha256": measure_code,
                   "era_label": era_label, "n_need": N_PRIMARY,
                   "cost": COST, "universe_label": "hist union 904 "
                   "(names with bars)", "f2_universe_label": "2021-06 cohort",
                   "f1": f1, "f2": f2}
        results["sensitivities"] = measure_sensitivities(h_tickers, bars,
                                                         hist, rng)

    # Verdicts (Holm per family, pre-reg §2)
    slot_keys = list(f1["slots"])
    holmed = holm(list(f1["slots"].values()), "F1")
    for k, s in zip(slot_keys, holmed):
        f1["slots"][k] = s
    for tag in ("f2a", "f2b"):
        s = f2[tag]
        holmed = holm([s], "F2")[0]
        s.update(holmed)
        s.pop("direction", None)

    # Gate: floor-unmet slots are INCONCLUSIVE (pre-reg §3) — and the
    # gate PASSED/UNMET determination.
    if args.gate:
        surv = False
        for k, s in f1["slots"].items():
            if not f1["floors"][k]["ok"]:
                s["verdict"] = ("INCONCLUSIVE (floors unmet: "
                                + json.dumps({kk: vv for kk, vv in
                                              f1["floors"][k].items()
                                              if kk != "ok"}))
            elif s["verdict"] == "EDGE":
                surv = True
        results["gate_f1"] = ("PASSED" if surv else
                              "UNMET (no EDGE with floors met)")
        for tag in ("f2a", "f2b"):
            s = f2[tag]
            n_low = s.get("n_low") or 0
            n_high = s.get("n_high") or 0
            if n_low < FLOORS["f2_names"] or n_high < FLOORS["f2_names"]:
                s["verdict"] = ("INCONCLUSIVE (floors unmet: "
                                f"{n_low}/{n_high} names)")
        results["gate_f2"] = (
            "PASSED" if f2["f2b"]["verdict"] == "EDGE"
            and (f2["f2b"].get("n_low") or 0) >= FLOORS["f2_names"]
            and (f2["f2b"].get("n_high") or 0) >= FLOORS["f2_names"]
            else "UNMET")

    # Primary run: measurement floors gate the measurement itself (one-shot
    # rule — a below-floor slot cannot produce a verdict).
    if not args.gate:
        ok_floors = all(f_["ok"] for f_ in f1["floors"].values())
        for tag in ("f2a", "f2b"):
            s = f2[tag]
            if (s.get("n_low") or 0) < FLOORS["f2_names"] or \
               (s.get("n_high") or 0) < FLOORS["f2_names"]:
                ok_floors = False
        if not ok_floors:
            print("REFUSED: measurement floors unmet (pre-reg #16 §2 — "
                  "one-shot rule):")
            print(json.dumps(
                {"f1_floors": {k: {kk: vv for kk, vv in f_.items()
                                   if kk != "ok"}
                               for k, f_ in f1["floors"].items()},
                 "f2_names": [f2["f2a"].get("n_low"),
                              f2["f2a"].get("n_high"),
                              f2["f2b"].get("n_low"),
                              f2["f2b"].get("n_high")]}, indent=1))
            return 2

    # Determinism: report/JSON carry the sha of the report's own bytes
    results["report_sha"] = ""
    results_json = json.dumps(results, sort_keys=True, indent=1)
    RESULTS_JSON.write_text(results_json, encoding="utf-8")
    write_report(results, audit_res, results["mode"])
    sha = hashlib.sha256(REPORT_MD.read_text("utf-8").encode()).hexdigest()
    results["report_sha"] = sha
    results_json = json.dumps(results, sort_keys=True, indent=1)
    RESULTS_JSON.write_text(results_json, encoding="utf-8")
    write_report(results, audit_res, results["mode"])
    print(f"wrote {RESULTS_JSON}")
    print(f"wrote {REPORT_MD}")
    print(f"measure_code_sha256: {measure_code}")
    print(f"results sha256: {hashlib.sha256(results_json.encode()).hexdigest()}")
    print(f"report sha256: {sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
