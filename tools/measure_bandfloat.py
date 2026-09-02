"""Pre-registration #25 measurement tool — price-band + float-cap drift
adjudication (ledger rows UvX-18, 4Pc-11, HYo-03, 5X_-05, 3rE-07/-09,
GXl-12, 2n2-14, dkO-12, afN-11).

Implements exactly PREREGISTRATION.md pre-reg #25 §2: ONE Holm family of 4
slots, OOS only, floors = 100 paired dates + 10 distinct names per leg:
  H1  band $2-20  vs >$20    (hist universe, OOS 2022-01-01..2025-12-31)
  H2  band $1-20  vs >$20    (same era; $1-2 ~empty in this universe)
  H3  float <= 20M vs > 20M  (current universe, OOS 2016-01-01..2025-12-31)
  H4  float <= 10M vs > 20M  (same protocol)
All slots "up": EDGE iff Holm-rejected AND CI-low > 0; FADE iff rejected AND
CI-upper < 0.

Protocol imported from measure_pricetier.py (pre-reg #16, FROZEN_SHA
675106eb...) unchanged: Bars, f1_bands (price bands), f1_slot,
day_paired_boot, tier_of, two_sample conventions. Float buckets use the
frozen 2026-08-13 float_shares snapshot applied backward (documented
limitation: no historical float series; current-universe membership
survivorship).

Sensitivities (NO verdicts): #16 slot reproductions (cross-check vs
data/cache/pricetier_measure_results.json when present), float <=30M vs
>30M, the "2020 rule" conjunction ($2-20 AND float <= 20M, descriptive),
five-tier sub-band means, N=5/20 for H1/H3, per-year, IS record.

Freeze discipline (pre-reg #16 convention): FROZEN_SHA is the sha256 of
this file with its own FROZEN_SHA hex blanked to 64 zeros; asserted at
every run; no forward-return computation happens before the freeze lands.

Run:  python -X utf8 tools/measure_bandfloat.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure_pricetier import (Bars, BAND_ORDER, N_PRIMARY, COST, B, ALPHA,
                               OOS_START, OOS_END, IS_START,
                               day_paired_boot, f1_bands, f1_slot, tier_of,
                               SLOT_DEFS, raw_sha256)

REPO = Path(__file__).resolve().parents[1]
HIST_UNIVERSE = REPO / "data" / "cache" / "universe_sp600_hist_2026-08-15.csv"
CURRENT_UNIVERSE = REPO / "data" / "cache" / "universe_sp600_2026-08-13.csv"
PRICE16_RESULTS = REPO / "data" / "cache" / "pricetier_measure_results.json"
RESULTS_JSON = REPO / "data" / "cache" / "bandfloat_measure_results.json"
REPORT_MD = REPO / "data" / "cache" / "bandfloat_measure_report.md"

SEED = 20260901
N_ALTS = (5, 20)
OOS16 = (np.datetime64("2016-01-01"), np.datetime64("2025-12-31"))
IS_ERA = (np.datetime64("2021-06-30"), np.datetime64("2021-12-31"))
FLOOR_DATES = 100
FLOOR_NAMES = 10
FLOAT_LE10 = 10_000_000.0
FLOAT_LE20 = 20_000_000.0
FLOAT_LE30 = 30_000_000.0
FLOAT_ORDER = ("le10", "10-20", "20-30", "gt30")
FROZEN_SHA = "eded78974ae2e894197a2f8618d846d32f3eee45549d0170b545282eab36f242"   # placeholder until freeze


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


def float_bucket(f: float) -> str:
    if f <= FLOAT_LE10:
        return "le10"
    if f <= FLOAT_LE20:
        return "10-20"
    if f <= FLOAT_LE30:
        return "20-30"
    return "gt30"


def float_bands(tickers, float_map, era, n_need, bars: Bars) -> dict:
    """Per bar-date per float bucket: N-forward returns (mirrors f1_bands)."""
    bucket_dates = {b: {} for b in FLOAT_ORDER}
    bucket_pairs = {b: [] for b in FLOAT_ORDER}
    drops = {b: 0 for b in FLOAT_ORDER}
    era_start, era_end = era
    for t in sorted(tickers):
        f = float_map.get(t)
        if f is None:
            continue
        dts = bars.dates.get(t)
        if dts is None:
            continue
        n = len(dts)
        for i in range(n):
            d = dts[i]
            if d < era_start:
                continue
            if d > era_end:
                break
            if i + n_need >= n:
                drops[float_bucket(f)] += 1
                continue
            r = bars.fwd_ret(t, i, n_need) - COST
            b = float_bucket(f)
            bucket_dates[b].setdefault(str(d), []).append(r)
            bucket_pairs[b].append((t, str(d), float(r)))
    return {"bucket_dates": bucket_dates, "bucket_pairs": bucket_pairs,
            "drops": drops}


def groups_slot(group_dates: dict, low_groups, high_groups, rng):
    """Day-paired contrast low - high (f1_slot generalized to buckets)."""
    dates = sorted(set().union(*[group_dates[g].keys() for g in low_groups],
                               *[group_dates[g].keys() for g in high_groups]))
    lows, highs = [], []
    for d in dates:
        ll = [r for g in low_groups for r in group_dates[g].get(d, [])]
        hh = [r for g in high_groups for r in group_dates[g].get(d, [])]
        if ll and hh:
            lows.append(float(np.mean(ll)))
            highs.append(float(np.mean(hh)))
    if not lows:
        return None
    res = day_paired_boot(np.array(lows), np.array(highs), rng)
    res["n_dates"] = len(lows)
    return res


def names_in(pairs: dict, groups) -> int:
    return len({t for g in groups for t, _, _ in pairs[g]})


def floor_check(res, n_lo, n_hi):
    if res is None:
        return False, "no paired dates"
    if res["n_dates"] < FLOOR_DATES:
        return False, f"paired dates {res['n_dates']} < {FLOOR_DATES}"
    if n_lo < FLOOR_NAMES or n_hi < FLOOR_NAMES:
        return False, f"names {n_lo}/{n_hi} < {FLOOR_NAMES}"
    return True, ""


def fmt(v, spec="+.4f"):
    return "—" if v is None else format(v, spec)


def holm4(slots: dict) -> None:
    order = sorted(slots, key=lambda k: slots[k]["p"])
    prev = 1.0
    for rank, k in enumerate(order):
        gate = min(ALPHA / (len(order) - rank), prev)
        slots[k]["gate"] = gate
        slots[k]["rejected"] = slots[k]["p"] <= gate
        prev = gate
        if not slots[k]["rejected"]:
            slots[k]["verdict"] = "NO EDGE"
        elif slots[k]["ci_low"] > 0:
            slots[k]["verdict"] = "EDGE"
        elif slots[k]["ci_high"] < 0:
            slots[k]["verdict"] = "FADE"
        else:
            slots[k]["verdict"] = "NO EDGE"


def main() -> int:
    self_check()
    hist = pd.read_csv(HIST_UNIVERSE, dtype={"ticker": str})
    cur = pd.read_csv(CURRENT_UNIVERSE, dtype={"ticker": str})
    float_map = dict(zip(cur["ticker"], cur["float_shares"].astype(float)))
    rng = np.random.default_rng(SEED)
    hist_t, cur_t = hist["ticker"].tolist(), cur["ticker"].tolist()

    bars_hist = Bars(hist_t)
    bars_cur = Bars(cur_t)

    # ---- primary slots ----
    f1 = f1_bands(hist_t, N_PRIMARY, COST, bars_hist, (OOS_START, OOS_END))
    h1 = f1_slot(f1["band_dates"], ("2-5", "5-10", "10-20"), ("gt20",), rng)
    h2 = f1_slot(f1["band_dates"], ("lt2", "2-5", "5-10", "10-20"),
                 ("gt20",), rng)
    f2 = float_bands(cur_t, float_map, OOS16, N_PRIMARY, bars_cur)
    h3 = groups_slot(f2["bucket_dates"], ("le10", "10-20"),
                     ("20-30", "gt30"), rng)
    h4 = groups_slot(f2["bucket_dates"], ("le10",), ("20-30", "gt30"), rng)

    n_names = {
        "H1_low": names_in(f1["band_pairs"], ("2-5", "5-10", "10-20")),
        "H1_high": names_in(f1["band_pairs"], ("gt20",)),
        "H2_low": names_in(f1["band_pairs"],
                           ("lt2", "2-5", "5-10", "10-20")),
        "H3_low": names_in(f2["bucket_pairs"], ("le10", "10-20")),
        "H3_high": names_in(f2["bucket_pairs"], ("20-30", "gt30")),
        "H4_low": names_in(f2["bucket_pairs"], ("le10",)),
    }

    # (b) cell counts before p-values; (c) $1-2 population
    print("cell counts (paired dates / distinct names per leg):")
    for k, r in (("H1", h1), ("H2", h2), ("H3", h3), ("H4", h4)):
        if r is None:
            print(f"  {k}: NO PAIRED DATES")
        else:
            lo = {"H1": n_names["H1_low"], "H2": n_names["H2_low"],
                  "H3": n_names["H3_low"], "H4": n_names["H4_low"]}[k]
            hi = {"H1": n_names["H1_high"], "H2": n_names["H1_high"],
                  "H3": n_names["H3_high"], "H4": n_names["H3_high"]}[k]
            print(f"  {k}: dates={r['n_dates']} names {lo}/{hi}")
    lt2_pairs = len(f1["band_pairs"]["lt2"])
    print(f"lt2 ($1-2) pair count (expected ~0 in S&P 600): {lt2_pairs}")

    slots = {}
    for k, r, lo_g, hi_g, pairs in (
            ("H1", h1, ("2-5", "5-10", "10-20"), ("gt20",), f1["band_pairs"]),
            ("H2", h2, ("lt2", "2-5", "5-10", "10-20"), ("gt20",),
             f1["band_pairs"]),
            ("H3", h3, ("le10", "10-20"), ("20-30", "gt30"),
             f2["bucket_pairs"]),
            ("H4", h4, ("le10",), ("20-30", "gt30"), f2["bucket_pairs"])):
        if r is None:
            slots[k] = {"verdict": "INCONCLUSIVE (no paired dates)",
                        "floor": "unmet"}
            continue
        ok, why = floor_check(r, names_in(pairs, lo_g), names_in(pairs, hi_g))
        r["floor"] = "met" if ok else f"unmet ({why})"
        if not ok:
            r["verdict"] = f"INCONCLUSIVE ({why})"
        slots[k] = r

    holm4({k: v for k, v in slots.items() if "p" in v})

    # ---- sensitivities (NO verdicts) ----
    sens = {}
    # #16 slot reproductions (same era/protocol; #16 seed differs — est is
    # deterministic, CI/p are not compared)
    repro = {}
    for name, (lo, hi) in SLOT_DEFS.items():
        r = f1_slot(f1["band_dates"], lo, hi, rng)
        repro[name] = None if r is None else {
            "est": r["est"], "ci_low": r["ci_low"], "ci_high": r["ci_high"],
            "p": r["p"], "n_dates": r["n_dates"]}
    sens["repro_16_slots"] = repro
    cross = {}
    if PRICE16_RESULTS.exists():
        p16 = json.loads(PRICE16_RESULTS.read_text(encoding="utf-8"))
        for name, mine in repro.items():
            theirs = p16.get("f1", {}).get("slots", {}).get(name)
            if theirs and mine and "est" in theirs:
                d = abs(mine["est"] - theirs["est"])
                cross[name] = {"est_mine": mine["est"],
                               "est_16": theirs["est"], "absdiff": d,
                               "within_1e-6": d < 1e-6}
    sens["crosscheck_16"] = cross

    # float <=30M vs >30M
    sens["float_le30_vs_gt30"] = groups_slot(
        f2["bucket_dates"], ("le10", "10-20", "20-30"), ("gt30",), rng)

    # "2020 rule" conjunction (descriptive): price in [2,20) AND float <= 20M
    # vs complement, day-paired on the OOS16 era
    in_rule_dates, out_dates = {}, {}
    for b, pairs in f1["band_pairs"].items():
        for t, d, r in pairs:
            fb = float_bucket(float_map.get(t, np.nan))
            in_rule = (b in ("2-5", "5-10", "10-20")) and (fb in ("le10", "10-20"))
            tgt = in_rule_dates if in_rule else out_dates
            tgt.setdefault(d, []).append(r)
    dates = sorted(set(in_rule_dates) & set(out_dates))
    if dates:
        a = np.array([np.mean(in_rule_dates[d]) for d in dates])
        bb = np.array([np.mean(out_dates[d]) for d in dates])
        sens["rule_2020_conjunction"] = dict(
            day_paired_boot(a, bb, rng), n_dates=len(dates))
    else:
        sens["rule_2020_conjunction"] = None

    # sub-band means (the drift table itself)
    sens["subband_means"] = {
        b: {"n_pairs": len(f1["band_pairs"][b]),
            "mean_ret": float(np.mean([r for _, _, r in f1["band_pairs"][b]]))
            if f1["band_pairs"][b] else None}
        for b in BAND_ORDER}

    # N=5/20 for H1/H3
    n_alts = {}
    for n in N_ALTS:
        f1n = f1_bands(hist_t, n, COST, bars_hist, (OOS_START, OOS_END))
        h1n = f1_slot(f1n["band_dates"], ("2-5", "5-10", "10-20"),
                      ("gt20",), rng)
        f2n = float_bands(cur_t, float_map, OOS16, n, bars_cur)
        h3n = groups_slot(f2n["bucket_dates"], ("le10", "10-20"),
                          ("20-30", "gt30"), rng)
        n_alts[str(n)] = {"H1": None if h1n is None else
                          {k: h1n[k] for k in ("est", "ci_low", "ci_high",
                                               "p", "n_dates")},
                          "H3": None if h3n is None else
                          {k: h3n[k] for k in ("est", "ci_low", "ci_high",
                                               "p", "n_dates")}}
    sens["n_alternatives"] = n_alts

    # per-year (H1/H3, low-leg minus high-leg paired date means)
    def per_year(pairs, lo_g, hi_g):
        lo_d, hi_d = {}, {}
        for g in lo_g:
            for t, d, r in pairs[g]:
                lo_d.setdefault(d, []).append(r)
        for g in hi_g:
            for t, d, r in pairs[g]:
                hi_d.setdefault(d, []).append(r)
        out = {}
        for d in sorted(set(lo_d) & set(hi_d)):
            y = d[:4]
            out.setdefault(y, []).append(
                np.mean(lo_d[d]) - np.mean(hi_d[d]))
        return {y: {"mean": float(np.mean(v)), "n_dates": len(v)}
                for y, v in sorted(out.items())}

    sens["per_year"] = {
        "H1": per_year(f1["band_pairs"], ("2-5", "5-10", "10-20"), ("gt20",)),
        "H3": per_year(f2["bucket_pairs"], ("le10", "10-20"),
                       ("20-30", "gt30"))}

    # IS record (descriptive)
    f1i = f1_bands(hist_t, N_PRIMARY, COST, bars_hist, IS_ERA)
    f2i = float_bands(cur_t, float_map, IS_ERA, N_PRIMARY, bars_cur)
    sens["is_record"] = {
        "H1": f1_slot(f1i["band_dates"], ("2-5", "5-10", "10-20"),
                      ("gt20",), rng),
        "H3": groups_slot(f2i["bucket_dates"], ("le10", "10-20"),
                          ("20-30", "gt30"), rng)}

    out = {
        "pre_reg": "#25",
        "claim": ("price-band and float-cap drift adjudication: the newer "
                  "stated bands ($2-20, $1-20) and float caps (<=20M, <=10M) "
                  "vs their excluded complements"),
        "params": {"n_primary": N_PRIMARY, "cost": COST, "b": B, "seed": SEED,
                   "alpha": ALPHA, "f1_era": [str(OOS_START), str(OOS_END)],
                   "f2_era": [str(OOS16[0]), str(OOS16[1])],
                   "floor_dates": FLOOR_DATES, "floor_names": FLOOR_NAMES,
                   "float_buckets": FLOAT_ORDER},
        "slots": slots,
        "sensitivities": sens,
        "assertions": {"lt2_pairs": lt2_pairs, "name_counts": n_names},
        "fingerprints": {
            "hist_universe_sha256": raw_sha256(HIST_UNIVERSE),
            "current_universe_sha256": raw_sha256(CURRENT_UNIVERSE),
            "measure_code_sha256": raw_sha256(Path(__file__)),
            "pricetier_engine_sha256": raw_sha256(
                REPO / "tools" / "measure_pricetier.py"),
        },
    }
    RESULTS = REPO / "data" / "cache" / "bandfloat_measure_results.json"
    RESULTS.write_text(json.dumps(out, indent=2, default=str),
                       encoding="utf-8")
    print(f"wrote {RESULTS.name}")

    # ---- report ----
    L = ["# Band/float measurement report (pre-registration #25)", "",
         f"- Pre-reg #25 (frozen per its freeze block): one Holm family of 4 "
         f"slots; N={N_PRIMARY}, cost {COST}, alpha {ALPHA}, bootstrap {B} "
         f"(seed {SEED})",
         f"- H1/H2 era OOS {OOS_START}..{OOS_END} (hist universe, #16's "
         f"primary era); H3/H4 era OOS {OOS16[0]}..{OOS16[1]} (current "
         "universe, frozen 2026-08-13 float snapshot applied backward)",
         f"- Floors: {FLOOR_DATES} paired dates, {FLOOR_NAMES} names/leg; "
         f"lt2 pairs {lt2_pairs} (expected ~0)", ""]
    L.append("## Verdicts (Holm family of 4)")
    L.append("")
    for k in ("H1", "H2", "H3", "H4"):
        r = slots[k]
        if "p" not in r:
            L.append(f"- {k}: **{r['verdict']}**")
            continue
        L.append(f"- {k}: est {r['est']:+.4f} (CI {r['ci_low']:+.4f}.."
                 f"{r['ci_high']:+.4f}, p {r['p']:.3f}) | dates "
                 f"{r['n_dates']} | floor {r['floor']} | gate "
                 f"{r['gate']:.4f} -> **{r['verdict']}**")
    L.append("")
    L.append("## Sensitivities (exploratory — NO verdicts)")
    L.append("")
    L.append("### #16 slot reproductions (cross-check)")
    L.append("")
    L.append("| slot | est | CI | p | dates |")
    L.append("|---|---|---|---|---|")
    for name, r in repro.items():
        if r is None:
            L.append(f"| {name} | — no paired dates — | | | |")
        else:
            L.append(f"| {name} | {r['est']:+.4f} | {r['ci_low']:+.4f}.."
                     f"{r['ci_high']:+.4f} | {r['p']:.3f} | {r['n_dates']} |")
    if cross:
        L.append("")
        L.append("Cross-check vs #16 stored results: " + "; ".join(
            f"{k}: absdiff {v['absdiff']:.2e} ({'PASS' if v['within_1e-6'] else 'FAIL'})"
            for k, v in cross.items()) or "no stored #16 results found")
    L.append("")
    L.append("### Sub-band means (the drift table)")
    L.append("")
    L.append("| band | n_pairs | mean_ret |")
    L.append("|---|---|---|")
    for b, r in sens["subband_means"].items():
        L.append(f"| {b} | {r['n_pairs']} | {fmt(r['mean_ret'])} |")
    L.append("")
    L.append("### Float buckets (means)")
    L.append("")
    L.append("| bucket | n_pairs | mean_ret |")
    L.append("|---|---|---|")
    for b in FLOAT_ORDER:
        pr = f2["bucket_pairs"][b]
        m = float(np.mean([r for _, _, r in pr])) if pr else None
        L.append(f"| {b} | {len(pr)} | {fmt(m)} |")
    L.append("")
    L.append(f"### '2020 rule' conjunction ($2-20 AND float<=20M) vs complement")
    rc = sens["rule_2020_conjunction"]
    if rc:
        L.append(f"est {rc['est']:+.4f} (CI {rc['ci_low']:+.4f}.."
                 f"{rc['ci_high']:+.4f}, p {rc['p']:.3f}), "
                 f"n_dates {rc['n_dates']} — descriptive only")
    else:
        L.append("no paired dates")
    L.append("")
    L.append("### N alternatives (H1/H3)")
    L.append("")
    for n, d in n_alts.items():
        h1n, h3n = d["H1"], d["H3"]
        L.append(f"- N={n}: H1 "
                 f"{fmt(h1n['est']) if h1n else '—'} (p "
                 f"{h1n['p']:.3f}, dates {h1n['n_dates']}) " if h1n else
                 f"- N={n}: H1 —")
        L.append(f"  H3 {fmt(h3n['est']) if h3n else '—'} (p "
                 f"{h3n['p']:.3f}, dates {h3n['n_dates']})" if h3n else
                 "  H3 —")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_bandfloat.py` regenerates this "
             "report; the seed is fixed, so results are stable across runs.")
    L.append("Engine: measure_pricetier.py imported unchanged (frozen #16 "
             "conventions); inputs: hist universe %s…, current universe %s…, "
             "tool %s…." % (out["fingerprints"]["hist_universe_sha256"][:12],
                            out["fingerprints"]["current_universe_sha256"][:12],
                            out["fingerprints"]["measure_code_sha256"][:12]))
    L.append("Any change to the detector, data, or measurement code changes "
             "the frozen inputs and requires a new pre-registration before "
             "it can drive a verdict.")
    L.append("")
    REPORT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())