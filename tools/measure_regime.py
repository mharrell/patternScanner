"""Pre-registration #29 measurement tool — regime conditioning with the
frozen leader proxy (ledger rows KzV-10, Wd_-03, UvX-24, J-E-02).

Implements exactly PREREGISTRATION.md pre-reg #29 §2: ONE Holm family of 2
slots, OOS 2016-2025, count floor 100 OOS detections per cell:
  H1 (UP contrast): veto-pass shape detections on high-regime days
     (trailing 10-day mean of the #26 leader proxy, top tercile) minus
     low-regime days (bottom tercile), two-sample bootstrap.
  H2 (UP absolute): high-regime detections beat era-matched random AND
     same-ticker baselines (p_input = max).

Leader proxy: L_t = daily max close-to-close return across the hist
universe (dates with >= 100 reporting names) — pre-reg #26 §1, unchanged.
Regime: trailing 10-session mean of L strictly BEFORE t; tercile cutpoints
= 1/3 and 2/3 quantiles of that trailing-mean series over the FULL
2000-2025 daily series (fixed here, not tuned on OOS).

Machinery imported from the frozen #8-family tools: measure_returns,
bootstrap_excess (measure.py), build_pools (measure_pillars.py),
two_sample_excess (measure_veto.py). Freeze discipline: FROZEN_SHA
blanked-self-hash computed from ON-DISK bytes.

Run:  python -X utf8 tools/measure_regime.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from measure import bootstrap_excess, measure_returns
from measure_pillars import build_pools
from measure_veto import two_sample_excess

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "data" / "cache"
UNIVERSE_CSV = CACHE / "universe_sp600_2026-08-13.csv"
VETO_CSV = CACHE / "veto_detections_v1.csv"
MKTSTRUCT_RESULTS = CACHE / "marketstruct_measure_results.json"
RESULTS_JSON = CACHE / "regime_measure_results.json"
REPORT_MD = CACHE / "regime_measure_report.md"

SEED = 20260904
B = 1000
ALPHA = 0.05
N_PRIMARY = 10
COST = 0.0015
OOS = (np.datetime64("2016-01-01"), np.datetime64("2025-12-31"))
IS_ERA = (np.datetime64("2000-01-01"), np.datetime64("2015-12-31"))
WINDOW_DAYS = 10
MIN_NAMES_PER_DAY = 100
MISSING_PASS = 100
FROZEN_SHA = "b1ecccc1823d2b1a54f79c221509de1d71c0ae5607031fef23ef9ba6b788572d"    # placeholder until freeze


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
    universe = pd.read_csv(UNIVERSE_CSV)["ticker"].tolist()
    hist_u = CACHE / "universe_sp600_hist_2026-08-15.csv"
    hist_t = pd.read_csv(hist_u, dtype={"ticker": str})["ticker"].tolist()

    # ---- leader proxy L_t (pre-reg #26 §1, unchanged) ----
    bars_l = {}
    from measure_pricetier import Bars
    bars = Bars(hist_t)
    for t in hist_t:
        dts = bars.dates.get(t)
        if dts is None:
            continue
        cl = bars.close[t]
        for i in range(1, len(dts)):
            # truncate to 'YYYY-MM-DD': str(np.datetime64) carries
            # 'T00:00:00.000', which would never match the detections'
            # bare signal_date keys
            bars_l.setdefault(str(dts[i])[:10], []).append(
                cl[i] / cl[i - 1] - 1.0)
    leader = {d: max(rs) for d, rs in bars_l.items()
              if len(rs) >= MIN_NAMES_PER_DAY}
    lds = sorted(leader)
    lv = pd.Series([leader[d] for d in lds], index=lds)
    # regime = trailing WINDOW_DAYS-session mean strictly before t
    roll = lv.rolling(WINDOW_DAYS).mean()
    trail = roll.shift(1)          # value at lds[i] uses lds[i-WINDOW..i-1]
    trail = trail.dropna()
    q1, q2 = float(trail.quantile(1 / 3)), float(trail.quantile(2 / 3))

    def regime_of(d: str) -> str | None:
        v = trail.get(d)
        if v is None or v != v:
            return None
        if v >= q2:
            return "high"
        if v < q1:
            return "low"
        return "mid"

    # assertion (a): per-year medians of L match #26 on shared years
    py = {}
    # mirror #26 exactly: its per-year medians were computed over lds[:-1]
    # (the leader frame drops the final day when pairing with next-day
    # returns), so the cross-check must use the same population
    for d in lds[:-1]:
        py.setdefault(d[:4], []).append(leader[d])
    py_med = {y: float(np.median(v)) for y, v in py.items()}
    xcheck = {}
    MKT26 = CACHE / "marketstruct_measure_results.json"
    if MKT26.exists():
        m26 = json.loads(MKT26.read_text(encoding="utf-8"))
        for y, v in m26["wd_leader_proxy"]["per_year_median"].items():
            if y in py_med:
                xcheck[y] = abs(py_med[y] - v)
    max_diff = max(xcheck.values()) if xcheck else None
    assert max_diff is not None and max_diff < 1e-9, (
        f"leader series mismatch vs #26 (max per-year median diff {max_diff})")
    print(f"leader cross-check vs #26: max per-year median diff {max_diff:.2e} PASS")

    # ---- detections + regime ----
    vd = pd.read_csv(CACHE / "veto_detections_v1.csv")
    camp = vd[vd["warmup"] == False].copy().reset_index(drop=True)  # noqa: E712
    camp["veto_pass"] = camp["veto_pass"].astype(bool)
    sel = camp[camp["veto_pass"]].copy()
    sel["regime"] = sel["signal_date"].map(regime_of)
    n_unassigned = int(sel["regime"].isna().sum())

    rows_all, dropped = measure_returns(sel, N_PRIMARY)
    rows_all = rows_all.reset_index(drop=True)
    keys = list(zip(rows_all["ticker"], rows_all["signal_date"]))
    # plain dict lookup: (ticker, date) keys are DUPLICATED (multiple shapes
    # per day), so Series.get would return a Series per key
    reg_map = dict(zip(zip(sel["ticker"], sel["signal_date"]), sel["regime"]))
    rows_all["regime"] = [reg_map[k] for k in keys]
    rows_all["is_oos"] = rows_all["signal_date"] >= str(OOS[0])

    oos = rows_all[rows_all["is_oos"] & rows_all["regime"].notna()]
    hi = oos[oos["regime"] == "high"]
    lo = oos[oos["regime"] == "low"]
    print(f"regime distribution across OOS detections: high {len(hi)}, "
          f"mid {int((oos['regime'] == 'mid').sum())}, low {len(lo)}; "
          f"unassigned (warm-up) {n_unassigned}")

    # ---- H1: high − low contrast ----
    if len(hi) >= MISSING_PASS and len(lo) >= MISSING_PASS:
        tx = two_sample_excess(hi["ret"].to_numpy(), lo["ret"].to_numpy(), rng)
        h1 = {"n_high": int(len(hi)), "n_low": int(len(lo)),
              "mean_high": float(hi["ret"].mean()),
              "mean_low": float(lo["ret"].mean()),
              "est": float(tx[0]), "ci_low": float(tx[2]),
              "ci_upper": float(tx[3]), "p": float(tx[4])}
    else:
        h1 = {"n_high": int(len(hi)), "n_low": int(len(lo)), "p": 1.0,
              "est": None, "ci_low": None, "ci_upper": None}

    # ---- H2: high-regime detections vs baselines ----
    pools = build_pools(N_PRIMARY, universe)
    _, random_pool, same_pool, _ = pools
    hi_rows = hi
    rets_hi = hi["ret"].to_numpy()

    def sample_same(M):
        ts = hi["ticker"].to_numpy()[rng.integers(0, len(hi), size=M)]
        out = np.empty(M)
        for j, t in enumerate(ts):
            pool = same_pool.get(t)
            out[j] = (pool[rng.integers(0, len(pool))]
                      if pool is not None and len(pool) else np.nan)
        return out

    def sample_random(M):
        return random_pool[rng.integers(0, len(random_pool), size=M)]

    if len(hi) >= MISSING_PASS:
        e_rand = bootstrap_excess(rets_hi, sample_random, rng)
        e_same = bootstrap_excess(rets_hi, sample_same, rng)
        h2 = {"n": int(len(hi)),
              "mean_ret": float(rets_hi.mean()),
              "excess_random": list(e_rand), "excess_same": list(e_same),
              "p": float(max(e_rand[4], e_same[4])),
              "est": float(max(e_rand[0], e_same[0])),
              "ci_low": float(min(e_rand[2], e_same[2]))}
    else:
        h2 = {"n": int(len(hi)), "p": 1.0, "est": None, "ci_low": None}

    # ---- Holm over the 2 slots ----
    slots = {"H1_contrast": dict(h1), "H2_absolute": dict(h2)}
    order = sorted(slots, key=lambda k: slots[k]["p"])
    prev = 1.0
    for rank, k in enumerate(order):
        gate = min(ALPHA / (len(order) - rank), prev)
        slots[k]["gate"] = gate
        slots[k]["rejected"] = slots[k]["p"] <= gate
        prev = gate
        if not slots[k]["rejected"]:
            slots[k]["verdict"] = "NO EDGE"
        elif slots[k]["ci_low"] is not None and slots[k]["ci_low"] > 0:
            slots[k]["verdict"] = "EDGE"
        elif slots[k].get("ci_upper") is not None and slots[k]["ci_upper"] < 0:
            slots[k]["verdict"] = "FADE"
        else:
            slots[k]["verdict"] = "NO EDGE"
        if k == "H1_contrast" and (slots[k].get("n_high", 0) < MISSING_PASS
                                   or slots[k].get("n_low", 0) < MISSING_PASS):
            slots[k]["verdict"] = "INCONCLUSIVE (floor unmet)"
        if k == "H2_absolute" and slots[k].get("n", 0) < MISSING_PASS:
            slots[k]["verdict"] = "INCONCLUSIVE (floor unmet)"

    # IS record + per-year descriptives
    is_hi = rows_all[(~rows_all["is_oos"]) & (rows_all["regime"] == "high")]
    sens = {"is_record_high": {"n": int(len(is_hi)),
                               "mean_ret": float(is_hi["ret"].mean())
                               if len(is_hi) else None}}
    py_h = oos.groupby([oos["signal_date"].str[:4], "regime"])["ret"] \
              .agg(["mean", "count"])
    sens["per_year_regime"] = {f"{y}|{r}": {"mean": float(v["mean"]),
                                            "n": int(v["count"])}
                               for (y, r), v in py_h.iterrows()}

    out = {
        "pre_reg": "#29",
        "claim": ("regime conditioning with the frozen leader proxy: "
                  "detections on high-regime days vs low-regime days "
                  "(contrast) and vs baselines (absolute)"),
        "params": {"n": N_PRIMARY, "cost": COST, "b": B, "seed": SEED,
                   "alpha": ALPHA, "window_days": WINDOW_DAYS,
                   "tercile_cutpoints": [q1, q2],
                   "era": [str(OOS[0]), str(OOS[1])],
                   "count_floor": MISSING_PASS},
        "slots": slots,
        "sensitivities": sens,
        "assertions": {"leader_crosscheck_max_diff": max_diff,
                       "regime_unassigned_detections": n_unassigned},
        "fingerprints": {
            "veto_file_sha256": hashlib.sha256(
                (CACHE / "veto_detections_v1.csv").read_bytes()).hexdigest(),
            "measure_code_sha256": hashlib.sha256(
                Path(__file__).read_bytes()).hexdigest(),
        },
    }
    RESULTS_JSON.write_text(json.dumps(out, indent=2, default=str),
                            encoding="utf-8")
    print(f"wrote {RESULTS_JSON.name}")

    L = ["# Regime conditioning measurement report (pre-registration #29)",
         "",
         f"- Pre-reg #29 (frozen per its freeze block); seed {SEED}, B={B}, "
         f"alpha {ALPHA}, N={N_PRIMARY}, cost {COST}",
         f"- Regime: trailing {WINDOW_DAYS}-session mean of the #26 leader "
         f"proxy; cutpoints q1 {q1:+.4f} / q2 {q2:+.4f} (full 2000-2025 "
         "series, fixed pre-OOS)",
         f"- Leader cross-check vs #26: max per-year median diff {max_diff} "
         "(PASS < 1e-9)", ""]
    L.append("## Verdicts (Holm family of 2)")
    L.append("")
    labels = {"H1_contrast": "high-regime − low-regime detections (UP)",
              "H2_absolute": "high-regime detections vs baselines (UP)"}
    for k in ("H1_contrast", "H2_absolute"):
        r = slots[k]
        if "est" not in r or r["est"] is None:
            L.append(f"- {k} ({labels[k]}): **{r['verdict']}**")
            continue
        L.append(f"- {k} ({labels[k]}): est {fmt(r['est'])} (CI "
                 f"{fmt(r['ci_low'])}..{fmt(r.get('ci_upper'))}, p "
                 f"{r['p']:.3f}) | gate {r['gate']:.4f} -> "
                 f"**{r['verdict']}**")
    L.append("")
    L.append("## Regime distribution (OOS detections)")
    L.append("")
    L.append(f"- high {len(hi)} / mid {int((oos['regime'] == 'mid').sum())} / "
             f"low {len(lo)}; unassigned {n_unassigned}")
    L.append("")
    L.append("`python -X utf8 tools/measure_regime.py` regenerates this "
             "report (seed fixed).")
    L.append("")
    REPORT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())