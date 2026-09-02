"""Pre-registration #30 measurement tool — sector sympathy momentum
(ledger rows afN-06, afN-02).

Implements exactly PREREGISTRATION.md pre-reg #30 §2: ONE Holm family of 2
slots, OOS 2016-01-01..2025-12-31, floors = 100 paired dates + 10 distinct
names per leg, day-paired bootstrap B=1000 seed 20260905 via
measure_pricetier's day_paired_boot (imported unchanged):
  H1 (UP): next-day N=10 forward returns (cost) of same-sector names from
           a leader's parabolic-day close vs all other names that day
  H2 (UP): same-sector names' SAME-day returns on parabolic-leader days vs
           other names'
Leader day: a hist-universe name with same-day return >= +50% (#26's
parabolic threshold); leaders excluded from both legs. Sector labels from
the frozen hist-universe CSV (snapshot applied backward — documented).
Freeze discipline: FROZEN_SHA blanked-self-hash from ON-DISK bytes.

Run:  python -X utf8 tools/measure_sympathy.py
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
BARS_DIR = REPO / "data" / "cache" / "bars"
HIST_UNIVERSE = REPO / "data" / "cache" / "universe_sp600_hist_2026-08-15.csv"
RESULTS_JSON = REPO / "data" / "cache" / "sympathy_measure_results.json"
REPORT_MD = REPO / "data" / "cache" / "sympathy_measure_report.md"

SEED = 20260905
B = 1000
ALPHA = 0.05
N_PRIMARY = 10
COST = 0.0015
OOS = (np.datetime64("2016-01-01"), np.datetime64("2025-12-31"))
LEADER_RET = 0.50
FLOOR_DATES = 100
FLOOR_NAMES = 10
FROZEN_SHA = "720c7c72c4c1bd99cfeb4d776d711fb0ef8c09dd671a30bf4eca1c121cdc47e8"    # placeholder until freeze


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


def holm2(slots: dict) -> None:
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
    rng = np.random.default_rng(SEED)
    hist = pd.read_csv(HIST_UNIVERSE, dtype={"ticker": str})
    tickers = hist["ticker"].tolist()
    sector = dict(zip(hist["ticker"], hist["sector"].astype(str)))
    bars = Bars(tickers)
    lo, hi = OOS

    # ---- pooled per-date returns + N=10 forwards ----
    day_rets: dict[str, list[tuple[str, float]]] = {}
    fwd: dict[tuple[str, str], float] = {}
    fwd_dropped = 0
    for t in tickers:
        dts = bars.dates.get(t)
        if dts is None:
            continue
        cl = pd.read_parquet(BARS_DIR / f"{t}.parquet",
                             columns=["Close"])["Close"].to_numpy(dtype=float)
        n = len(dts)
        for i in range(1, n):
            d = str(dts[i])[:10]
            if not (lo <= np.datetime64(d) <= hi):
                continue
            day_rets.setdefault(d, []).append((t, cl[i] / cl[i - 1] - 1.0))
            if i + N_PRIMARY < n:
                fwd[(t, d)] = cl[i + N_PRIMARY] / cl[i] - 1.0 - COST
            else:
                fwd_dropped += 1

    # ---- leader days: any name with ret >= +50% ----
    h1_low, h1_high = {}, {}   # low leg = same-sector (next-day), high = other
    h2_low, h2_high = {}, {}   # low = same-sector same-day, high = other
    h1_names, h2_names = set(), set()
    h2_names_o = set()
    leader_days = 0
    leader_events_by_year: dict[str, int] = {}
    for d, lst in sorted(day_rets.items()):
        leaders = [t for t, r in lst if r >= LEADER_RET]
        if not leaders:
            continue
        leader_days += 1
        for t in leaders:
            leader_events_by_year[d[:4]] = leader_events_by_year.get(d[:4], 0) + 1
        leader_sectors = {sector.get(t, "?") for t in leaders}
        sec, oth, sec2, oth2 = [], [], [], []
        for t, r in lst:
            if t in leaders:
                continue  # leaders excluded from both legs
            if sector.get(t, "?") in leader_sectors:
                sec2.append(r)
                if (t, d) in fwd:
                    sec = fwd[(t, d)]
                    if sec is not None:
                        h1_low.setdefault(d, []).append(sec)
                        h1_names.add(t)
            else:
                oth2.append(r)
                if (t, d) in fwd:
                    o = fwd[(t, d)]
                    if o is not None:
                        h1_high.setdefault(d, []).append(o)
            # (oth names tracked for H2 names below)
        # H2: same-day means per leg
        if sec2 and oth2:
            h2_low.setdefault(d, []).append(float(np.mean(sec2)))
            h2_high.setdefault(d, []).append(float(np.mean(oth2)))
            h2_names.update(t for t, _ in lst
                            if sector.get(t, "?") in leader_sectors
                            and t not in leaders)

    # ---- H1 day-paired over dates where both legs present ----
    def paired(lows: dict, highs: dict):
        ds = sorted(set(lows) & set(highs))
        if not ds:
            return None, 0
        res = day_paired_boot(np.array([np.mean(lows[d]) for d in ds]),
                              np.array([np.mean(highs[d]) for d in ds]), rng)
        res["n_dates"] = len(ds)
        return res, len(ds)

    r1, d1 = paired(h1_low, h1_high)
    r2, d2 = paired(h2_low, h2_high)
    slots = {}
    print("cell counts (paired dates / notes):")
    for k, r, nd, nlo in (("H1_nextday", r1, d1, len(h1_names)),
                          ("H2_sameday", r2, d2, len(h2_names))):
        print(f"  {k}: dates={nd} distinct_names={nlo}")
        if r is None:
            slots[k] = {"verdict": "INCONCLUSIVE (no paired dates)",
                        "floor": "unmet"}
        else:
            ok = nd >= FLOOR_DATES and nlo >= FLOOR_NAMES
            r["floor"] = "met" if ok else f"unmet (dates {nd}, names {nlo})"
            if not ok:
                r["verdict"] = "INCONCLUSIVE (floor unmet)"
            slots[k] = r

    holm2({k: v for k, v in slots.items() if "p" in v})

    out = {
        "pre_reg": "#30",
        "claim": ("sector sympathy momentum: same-sector names move with a "
                  "parabolic leader (same day) and continue (next-day N=10)"),
        "params": {"n": N_PRIMARY, "cost": COST, "b": B, "seed": SEED,
                   "alpha": ALPHA, "era": [str(OOS[0]), str(OOS[1])],
                   "leader_ret": LEADER_RET,
                   "floor_dates": FLOOR_DATES, "floor_names": FLOOR_NAMES},
        "slots": slots,
        "assertions": {"leader_days": leader_days,
                       "leader_events_by_year": leader_events_by_year,
                       "fwd_dropped": fwd_dropped,
                       "names": {"H1": len(h1_names), "H2": len(h2_names)}},
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

    L = ["# Sector sympathy measurement report (pre-registration #30)", "",
         f"- Pre-reg #30 (frozen per its freeze block); seed {SEED}, B={B}, "
         f"alpha {ALPHA}, N={N_PRIMARY}, cost {COST}; era OOS "
         f"{OOS[0]}..{OOS[1]} (hist universe, frozen sector labels)",
         f"- Leader days (>= +50% name): {leader_days} dates, "
         f"{sum(leader_events_by_year.values())} events", ""]
    L.append("## Verdicts (Holm family of 2)")
    L.append("")
    labels = {"H1_nextday": "same-sector next-day N=10 vs other names (UP)",
              "H2_sameday": "same-sector same-day vs other names (UP)"}
    for k in ("H1_nextday", "H2_sameday"):
        r = slots[k]
        if "p" not in r:
            L.append(f"- {k} ({labels[k]}): **{r['verdict']}**")
            continue
        L.append(f"- {k} ({labels[k]}): est {fmt(r['est'])} (CI "
                 f"{fmt(r['ci_low'])}..{fmt(r['ci_high'])}, p {r['p']:.3f}) "
                 f"| dates {r['n_dates']} | gate {r['gate']:.4f} -> "
                 f"**{r['verdict']}**")
    L.append("")
    L.append("## Leader events by year (cross-check vs #26 C3)")
    L.append("")
    L.append("| year | leader events (>=+50%) |")
    L.append("|---|---|")
    for y in sorted(leader_events_by_year):
        L.append(f"| {y} | {leader_events_by_year[y]} |")
    L.append("")
    L.append("`python -X utf8 tools/measure_sympathy.py` regenerates this "
             "report (seed fixed).")
    L.append("")
    REPORT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())