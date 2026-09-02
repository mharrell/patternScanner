"""Pre-registration #28 measurement tool — daily selection follow-ups
(ledger rows 3rE-05/-06, 5X_-04/-06b, GMR-07/-08, ZS8-13/-14, HYo-14,
3rE-11).

Implements exactly PREREGISTRATION.md pre-reg #28 §2: ONE Holm family of 4
slots, OOS 2022-01-01..2025-12-31 (the #25/#16 F1 era), hist universe,
floors = 100 paired dates + 10 distinct names per leg, day-paired bootstrap
B=1000 seed 20260903 via measure_pricetier's day_paired_boot (imported
unchanged):
  H1 (UP):   rank-2/3 gainers (same-day ret >= +10%, ranked) vs rank >= 10
  H2 (UP):   same-day ret >= +10% vs 0-2% band
  H3 (DOWN): close within 1% BELOW the nearest half/whole-dollar level vs
             within 1% ABOVE it
  H4 (UP):   gap >= +2% (open_t/close_{t-1}-1) vs |gap| < 0.2%;
             outcome = open_t -> close_t (cost-applied)

N=10 close-to-close minus cost for H1-H3; H4 outcome is same-day open->close
minus cost. Bars/day_paired_boot imported from measure_pricetier.py (pre-reg
#16) unchanged; H4 and H3 read Open/Close directly (documented). Freeze
discipline: FROZEN_SHA blanked-self-hash computed from ON-DISK bytes.

Run:  python -X utf8 tools/measure_selection2.py
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
RESULTS_JSON = REPO / "data" / "cache" / "selection2_measure_results.json"
REPORT_MD = REPO / "data" / "cache" / "selection2_measure_report.md"

SEED = 20260903
B = 1000
ALPHA = 0.05
N_PRIMARY = 10
COST = 0.0015
OOS = (np.datetime64("2022-01-01"), np.datetime64("2025-12-31"))
FLOOR_DATES = 100
FLOOR_NAMES = 10
GAP_LE = 0.02
ROUND_BAND = 0.01
FROZEN_SHA = "d7c66148374a6189f56dde4f55d06698d94df133ded98c76aa72c085b71f4273"    # placeholder until freeze


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


def round_side(px: float) -> int:
    """+1 if px sits within ROUND_BAND ABOVE the nearest half/whole-dollar
    level (just cleared), -1 if within ROUND_BAND BELOW it, else 0."""
    below_lvl = np.floor(px * 2.0) / 2.0
    above_lvl = np.ceil(px * 2.0) / 2.0
    d_lo = (px - below_lvl) / below_lvl if below_lvl > 0 else 9.9
    d_hi = (above_lvl - px) / px if above_lvl > 0 else 9.9
    if d_lo <= ROUND_BAND and d_lo < d_hi:
        return 1
    if d_hi <= ROUND_BAND and d_hi <= d_lo:
        return -1
    return 0


def holm4(slots: dict, directions: dict) -> None:
    order = sorted(slots, key=lambda k: slots[k]["p"])
    prev = 1.0
    for rank, k in enumerate(order):
        gate = min(ALPHA / (len(order) - rank), prev)
        slots[k]["gate"] = gate
        slots[k]["rejected"] = slots[k]["p"] <= gate
        prev = gate
        d = directions[k]
        if not slots[k]["rejected"]:
            slots[k]["verdict"] = "NO EDGE"
        elif d == "up":
            slots[k]["verdict"] = ("EDGE" if slots[k]["ci_low"] > 0
                                   else "FADE" if slots[k]["ci_high"] < 0
                                   else "NO EDGE")
        else:
            slots[k]["verdict"] = ("EDGE" if slots[k]["ci_high"] < 0
                                   else "FADE" if slots[k]["ci_low"] > 0
                                   else "NO EDGE")


def fmt(v, spec="+.4f"):
    return "—" if v is None else format(v, spec)


def main() -> int:
    self_check()
    rng = np.random.default_rng(SEED)
    hist = pd.read_csv(HIST_UNIVERSE, dtype={"ticker": str})
    tickers = hist["ticker"].tolist()
    bars = Bars(tickers)
    lo, hi = OOS

    # Per-date pooled same-day returns and per-(ticker, date) N=10 forwards
    day_rets: dict[str, list[tuple[str, float]]] = {}
    fwd: dict[tuple[str, str], float] = {}
    fwd_dropped = 0
    for t in sorted(tickers):
        dts = bars.dates.get(t)
        if dts is None:
            continue
        cl = pd.read_parquet(BARS_DIR / f"{t}.parquet",
                             columns=["Close"])["Close"].to_numpy(dtype=float)
        n = len(dts)
        for i in range(1, n):
            d = str(dts[i])
            if not (lo <= np.datetime64(d) <= hi):
                continue
            day_rets.setdefault(d, []).append((t, cl[i] / cl[i - 1] - 1.0))
            if i + N_PRIMARY < n:
                fwd[(t, d)] = cl[i + N_PRIMARY] / cl[i] - 1.0 - COST
            else:
                fwd_dropped += 1

    class Leg:
        """date -> [ret], plus the distinct-name set per leg."""

        def __init__(self):
            self.dates: dict[str, list[float]] = {}
            self.names: set[str] = set()

        def add(self, d, name, ret):
            self.dates.setdefault(d, []).append(ret)
            self.names.add(name)

    h1_low, h1_high = Leg(), Leg()
    h2_low, h2_high = Leg(), Leg()
    h3_low, h3_high = Leg(), Leg()
    h4_low, h4_high = Leg(), Leg()

    # ---- H1 / H2 (from the pooled day returns) ----
    n_rank_days = 0
    for d, lst in day_rets.items():
        movers = sorted(((t, r) for t, r in lst if r >= 0.10 and (t, d) in fwd),
                        key=lambda x: -x[1])
        if len(movers) >= 12:
            n_rank_days += 1
            for t, r in movers[1:3]:
                h1_low.add(d, t, fwd[(t, d)])
            for t, r in movers[9:]:
                h1_high.add(d, t, fwd[(t, d)])
        for t, r in lst:
            if (t, d) not in fwd:
                continue
            if r >= 0.10:
                h2_low.add(d, t, fwd[(t, d)])
            elif 0.0 <= r < 0.02:
                h2_high.add(d, t, fwd[(t, d)])

    # ---- H3: just-below vs just-above round levels ----
    n_below = n_above = 0
    for t in sorted(tickers):
        dts = bars.dates.get(t)
        if dts is None:
            continue
        cl = pd.read_parquet(BARS_DIR / f"{t}.parquet",
                             columns=["Close"])["Close"].to_numpy(dtype=float)
        for i in range(1, len(dts)):
            d = str(dts[i])
            if not (lo <= np.datetime64(d) <= hi) or (t, d) not in fwd:
                continue
            s = round_side(cl[i])
            if s == 1:
                h3_high.add(d, t, fwd[(t, d)])
                n_above += 1
            elif s == -1:
                h3_low.add(d, t, fwd[(t, d)])
                n_below += 1

    # ---- H4: gap >= +2% vs flat open; outcome open->close ----
    for t in sorted(tickers):
        dts = bars.dates.get(t)
        if dts is None:
            continue
        df = pd.read_parquet(BARS_DIR / f"{t}.parquet",
                             columns=["Open", "Close"])
        op = df["Open"].to_numpy(dtype=float)
        cl = df["Close"].to_numpy(dtype=float)
        for i in range(1, len(dts)):
            d = str(dts[i])
            if not (lo <= np.datetime64(d) <= hi):
                continue
            g = op[i] / cl[i - 1] - 1.0
            o2c = cl[i] / op[i] - 1.0 - COST
            if g >= GAP_LE:
                h4_low.add(d, t, o2c)
            elif abs(g) < 0.002:
                h4_high.add(d, t, o2c)

    def slot_of(low: Leg, high: Leg):
        ds = sorted(set(low.dates) & set(high.dates))
        if not ds:
            return None, 0
        res = day_paired_boot(np.array([np.mean(low.dates[d]) for d in ds]),
                              np.array([np.mean(high.dates[d]) for d in ds]),
                              rng)
        res["n_dates"] = len(ds)
        return res, len(ds)

    specs = (("H1", h1_low, h1_high), ("H2", h2_low, h2_high),
             ("H3", h3_low, h3_high), ("H4", h4_low, h4_high))
    slots = {}
    print("cell counts (paired dates / distinct names per leg):")
    for k, low, high in specs:
        r, nd = slot_of(low, high)
        nlo, nhi = len(low.names), len(high.names)
        print(f"  {k}: dates={nd} names {nlo}/{nhi}")
        if r is None:
            slots[k] = {"verdict": "INCONCLUSIVE (no paired dates)",
                        "floor": "unmet"}
        else:
            ok = nd >= FLOOR_DATES and nlo >= FLOOR_NAMES and nhi >= FLOOR_NAMES
            r["floor"] = ("met" if ok else
                          f"unmet (dates {nd}, names {nlo}/{nhi})")
            if not ok:
                r["verdict"] = "INCONCLUSIVE (floor unmet)"
            slots[k] = r

    holm4({k: v for k, v in slots.items() if "p" in v},
          {"H1": "up", "H2": "up", "H3": "down", "H4": "up"})

    out = {
        "pre_reg": "#28",
        "claim": ("daily selection follow-ups: rank-2/3 gainers, "
                  "momentum-continuation at +10%, round-number proximity, "
                  "gap-and-go"),
        "params": {"n": N_PRIMARY, "cost": COST, "b": B, "seed": SEED,
                   "alpha": ALPHA, "era": [str(OOS[0]), str(OOS[1])],
                   "gap_le": GAP_LE, "round_band": ROUND_BAND,
                   "floor_dates": FLOOR_DATES, "floor_names": FLOOR_NAMES},
        "slots": slots,
        "assertions": {"rank2_3_days": n_rank_days,
                       "oos_days": len(day_rets),
                       "n_just_below": n_below, "n_just_above": n_above,
                       "fwd_dropped": fwd_dropped,
                       "name_counts": {k: [len(lo.names), len(hi.names)]
                                       for k, lo, hi in specs}},
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

    L = ["# Selection follow-ups measurement report (pre-registration #28)",
         "",
         f"- Pre-reg #28 (frozen per its freeze block); seed {SEED}, B={B}, "
         f"alpha {ALPHA}, N={N_PRIMARY}, cost {COST}; era OOS "
         f"{OOS[0]}..{OOS[1]} (hist universe)", ""]
    L.append("## Verdicts (Holm family of 4)")
    L.append("")
    labels = {"H1": "rank-2/3 vs rank>=10 gainers (UP)",
              "H2": ">=+10% vs 0-2% names (UP)",
              "H3": "just-below vs just-above round level (DOWN)",
              "H4": "gap>=+2% vs flat open, open->close (UP)"}
    for k in ("H1", "H2", "H3", "H4"):
        r = slots[k]
        if "p" not in r:
            L.append(f"- {k} ({labels[k]}): **{r['verdict']}**")
            continue
        L.append(f"- {k} ({labels[k]}): est {fmt(r['est'])} (CI "
                 f"{fmt(r['ci_low'])}..{fmt(r['ci_high'])}, p {r['p']:.3f}) "
                 f"| dates {r['n_dates']} | gate {r['gate']:.4f} -> "
                 f"**{r['verdict']}**")
    L.append("")
    L.append(f"- rank-2/3 constructible on {n_rank_days} of {len(day_rets)} "
             "OOS days (>= 12 movers that day)")
    L.append(f"- round-level population: just-below {n_below}, just-above "
             f"{n_above} ticker-days; forward-dropped {fwd_dropped}")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_selection2.py` regenerates this "
             "report (seed fixed). Engine measure_pricetier.py imported "
             f"unchanged ({out['fingerprints']['pricetier_engine_sha256'][:12]}…).")
    L.append("")
    REPORT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())