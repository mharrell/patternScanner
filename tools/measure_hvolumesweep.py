"""Pre-registration #31 measurement tool — detection follow-ups: the
accuracy/horizon tradeoff (UvX-30) and the absolute-volume leg (Wd_-14).

Implements exactly PREREGISTRATION.md pre-reg #31 §2: ONE Holm family of 2
slots, OOS 2016-2025, count floor 100 paired OOS detections per cell:
  H1 (DOWN): hit_rate(N=20) - hit_rate(N=1) < 0, PAIRED per detection
             (both horizons computable; detections missing either horizon
             are excluded and counted). The hit-rate-by-N table
             (N=1/5/10/20) prints before the rule applies.
  H2 (UP):   detection forward returns (N=10, cost) on >25M-share-volume
             days vs <=25M days, two-sample bootstrap.

Machinery imported from the frozen #8-family tools: measure_returns
(measure.py), two_sample_excess (measure_veto.py). Volume read from the
bars parquet directly (as #24's RV did). Freeze discipline: FROZEN_SHA
blanked-self-hash computed from ON-DISK bytes.

Run:  python -X utf8 tools/measure_hvolumesweep.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import measure_returns
from measure_veto import two_sample_excess

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "data" / "cache"
BARS_DIR = CACHE / "bars"
VETO_CSV = CACHE / "veto_detections_v1.csv"
RESULTS_JSON = CACHE / "hvolumesweep_measure_results.json"
REPORT_MD = CACHE / "hvolumesweep_measure_report.md"

SEED = 20260906
B = 1000
ALPHA = 0.05
HORIZONS = (1, 5, 10, 20)
VOL_SPLIT = 25_000_000.0
FLOOR = 100
FROZEN_SHA = "8862de26276749027405f4d182a3b8f4d19148186173d26580da0010729b18fe"    # placeholder until freeze


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


def main() -> int:
    self_check()
    rng = np.random.default_rng(SEED)

    vd = pd.read_csv(VETO_CSV)
    camp = vd[vd["warmup"] == False].copy().reset_index(drop=True)  # noqa: E712
    camp["veto_pass"] = camp["veto_pass"].astype(bool)
    sel = camp[camp["veto_pass"]].copy()

    # ---- paired per-horizon returns on the SAME detections ----
    def rets_at(n: int) -> dict[tuple[str, str], float]:
        rows, _ = measure_returns(sel, n)
        return {(r["ticker"], r["signal_date"]): r["ret"]
                for _, r in rows.iterrows()}

    rets = {n: rets_at(n) for n in HORIZONS}
    common = set(rets[HORIZONS[0]])
    for n in HORIZONS[1:]:
        common &= set(rets[n])
    keys = sorted(common)
    n_excluded = len(rets[HORIZONS[0]]) - len(keys)
    print(f"paired detections (all horizons): {len(keys)} "
          f"(excluded {n_excluded})")

    # ---- (a) hit-rate-by-N table BEFORE the H1 rule ----
    hit_rates = {}
    for n in HORIZONS:
        v = np.array([rets[n][k] for k in keys])
        hit_rates[str(n)] = {"hit_rate": float((v > 0).mean()),
                             "mean_ret": float(v.mean())}
        print(f"  N={n:>2}: hit_rate {hit_rates[str(n)]['hit_rate']:.4f} "
              f"| mean_ret {hit_rates[str(n)]['mean_ret']:+.4f}")

    v1 = np.array([rets[HORIZONS[0]][k] for k in keys])
    v20 = np.array([rets[HORIZONS[-1]][k] for k in keys])
    M = len(keys)

    if M >= FLOOR:
        est = float((v20 > 0).mean() - (v1 > 0).mean())
        diffs = np.empty(B)
        for b in range(B):
            idx = rng.integers(0, M, M)
            diffs[b] = ((v20[idx] > 0).mean() - (v1[idx] > 0).mean())
        ci_low, ci_high = np.percentile(diffs, [2.5, 97.5])
        p = 2.0 * min(float((diffs <= 0).mean()),
                      float((diffs >= 0).mean()))
        est = float((v20 > 0).mean() - (v1 > 0).mean())
        h1 = {"n": M, "hit_rate_n1": hit_rates[str(HORIZONS[0])]["hit_rate"],
              "hit_rate_n20": hit_rates[str(HORIZONS[-1])]["hit_rate"],
              "est": est, "ci_low": float(ci_low), "ci_upper": float(ci_high),
              "p": min(p, 1.0)}
    else:
        h1 = {"n": M, "est": None, "ci_low": None, "ci_upper": None, "p": 1.0}

    # ---- H2: >25M vs <=25M volume-day detections (N=10) ----
    vol_map: dict[tuple[str, str], float] = {}
    from measure_pricetier import Bars
    bars = Bars(sorted(sel["ticker"].unique()))
    for t in sorted(sel["ticker"].unique()):
        dts = bars.dates.get(t)
        if dts is None:
            continue
        vol = pd.read_parquet(BARS_DIR / f"{t}.parquet",
                              columns=["Volume"])["Volume"].to_numpy(dtype=float)
        pos = {str(x)[:10]: j for j, x in enumerate(dts)}
        for k in keys:
            if k[0] != t:
                continue
            loc = pos.get(k[1])
            if loc is not None and loc < len(vol):
                vol_map[k] = float(vol[loc])
    r10 = rets[10]
    hi_rets = [r10[k] for k in keys if vol_map.get(k, 0.0) > VOL_SPLIT]
    lo_rets = [r10[k] for k in keys if 0.0 < vol_map.get(k, 0.0) <= VOL_SPLIT]
    print(f"H2 volume buckets: >25M n={len(hi_rets)}, <=25M n={len(lo_rets)}")
    if len(hi_rets) >= FLOOR and len(lo_rets) >= FLOOR:
        tx = two_sample_excess(np.array(hi_rets), np.array(lo_rets), rng)
        h2 = {"n_high": len(hi_rets), "n_low": len(lo_rets),
              "mean_high": float(np.mean(hi_rets)),
              "mean_low": float(np.mean(lo_rets)),
              "est": float(tx[0]), "ci_low": float(tx[2]),
              "ci_upper": float(tx[3]), "p": float(tx[4])}
    else:
        h2 = {"n_high": len(hi_rets), "n_low": len(lo_rets), "p": 1.0,
              "est": None, "ci_low": None, "ci_upper": None}

    slots = {"H1_tradeoff": dict(h1), "H2_volume": dict(h2)}
    order = sorted(slots, key=lambda k: slots[k]["p"])
    prev = 1.0
    for rank, k in enumerate(order):
        gate = min(ALPHA / (len(order) - rank), prev)
        slots[k]["gate"] = gate
        slots[k]["rejected"] = slots[k]["p"] <= gate
        prev = gate
        if not slots[k]["rejected"]:
            slots[k]["verdict"] = "NO EDGE"
        elif k == "H1_tradeoff":
            slots[k]["verdict"] = ("EDGE" if slots[k]["ci_upper"] < 0
                                   else "FADE" if slots[k]["ci_low"] > 0
                                   else "NO EDGE")
        else:
            slots[k]["verdict"] = ("EDGE" if slots[k]["ci_low"] > 0
                                   else "FADE" if slots[k]["ci_high"] < 0
                                   else "NO EDGE")
        if k == "H1_tradeoff" and slots[k].get("n", 0) < FLOOR:
            slots[k]["verdict"] = "INCONCLUSIVE (floor unmet)"
        if k == "H2_volume" and (slots[k].get("n_high", 0) < FLOOR
                                 or slots[k].get("n_low", 0) < FLOOR):
            slots[k]["verdict"] = "INCONCLUSIVE (floor unmet)"

    out = {
        "pre_reg": "#31",
        "claim": ("detection follow-ups: the accuracy/horizon tradeoff "
                  "(hit rate falls with holding horizon) and the "
                  "absolute-volume leg (>25M-share days best)"),
        "params": {"horizons": list(HORIZONS), "vol_split": VOL_SPLIT,
                   "b": B, "seed": SEED, "alpha": ALPHA, "count_floor": FLOOR},
        "slots": slots,
        "hit_rate_table": hit_rates,
        "assertions": {"n_paired": M,
                       "n_excluded_unequal_horizon": n_excluded,
                       "n_no_volume": int(M - len(hi_rets) - len(lo_rets))},
        "fingerprints": {
            "veto_file_sha256": hashlib.sha256(VETO_CSV.read_bytes()).hexdigest(),
            "measure_code_sha256": hashlib.sha256(
                Path(__file__).read_bytes()).hexdigest(),
        },
    }
    RESULTS_JSON.write_text(json.dumps(out, indent=2, default=str),
                            encoding="utf-8")
    print(f"wrote {RESULTS_JSON.name}")

    L = ["# H-sweep / volume measurement report (pre-registration #31)", "",
         f"- Pre-reg #31 (frozen per its freeze block); seed {SEED}, B={B}, "
         f"alpha {ALPHA}; paired detections {M} (excluded {n_excluded})", ""]
    L.append("## Hit-rate table (N = 1/5/10/20, paired detections)")
    L.append("")
    L.append("| N | hit_rate | mean_ret |")
    L.append("|---|---|---|")
    for n in HORIZONS:
        r = hit_rates[str(n)]
        L.append(f"| {n} | {r['hit_rate']:.4f} | {r['mean_ret']:+.4f} |")
    L.append("")
    L.append("## Verdicts (Holm family of 2)")
    L.append("")
    labels = {"H1_tradeoff": "hit_rate(N=20) − hit_rate(N=1) < 0 (DOWN)",
              "H2_volume": ">25M-volume days vs ≤25M (UP)"}
    for k in ("H1_tradeoff", "H2_volume"):
        r = slots[k]
        if r["est"] is None:
            L.append(f"- {k} ({labels[k]}): **{r['verdict']}**")
            continue
        L.append(f"- {k} ({labels[k]}): est {fmt(r['est'])} (CI "
                 f"{fmt(r['ci_low'])}..{fmt(r['ci_upper'])}, p {r['p']:.3f}) "
                 f"| gate {r['gate']:.4f} -> **{r['verdict']}**")
    L.append("")
    L.append("`python -X utf8 tools/measure_hvolumesweep.py` regenerates "
             "this report (seed fixed).")
    L.append("")
    REPORT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())