"""Pre-registration #32 measurement tool — intraday sector sympathy
(ledger rows afN-06; §J.7 follow-up).

Implements exactly PREREGISTRATION.md pre-reg #32 §2: ONE Holm family of 2
slots (UP), count floor 100 evaluable per slot, N=60 forward, cost 0.15%,
B=1000 seed 20260907, two-sample bootstrap via measure_intraday_entry's
contrast_two; §5-gated floors per the #27 convention (≥20 full-universe
bar-dates ≥2026-08-19, ≥2,000 evaluable entries, ≥100 tickers, ≥15 dates;
`--floors` does not consume the one-shot):
  H1 (UP): sector-hot reversal entries (a same-sector mate's intraday
           running move from session open reached >= +40% at/before the
           entry bar) vs sector-cold entries.
  H2 (UP): sector-hot entries vs the raw candidate pool.

Entry set: pre-reg #19 F1 reversal new-high entries via
measure_intraday_veto.Archive (frozen #21 machinery, imported unchanged).
Leader-spike index per (bar-date, ticker): first bar where
max(High[:i])/Open[0] - 1 >= 0.40. Sector labels: frozen hist-universe CSV;
archive tickers absent from it are excluded from the sector test (counted).
Freeze discipline: FROZEN_SHA blanked-self-hash from ON-DISK bytes.

Run:  python -X utf8 tools/measure_sympathy_intraday.py [--floors]
Exit: 0 ok, 2 floors unmet (refused), 1 integrity failure.
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

import measure_intraday_entry as MIE
import measure_intraday_veto as MIV
from measure_intraday_veto import (Archive, FROZEN_SHA as VETO_SHA,
                                   N_PRIMARY, COST_PRIMARY, B, ALPHA,
                                   MIN_SLOT, MANIFEST_PATH)

REPO = Path(__file__).resolve().parents[1]
HIST_UNIVERSE = REPO / "data" / "cache" / "universe_sp600_hist_2026-08-15.csv"
RESULTS_JSON = REPO / "data" / "cache" / "symintra_measure_results.json"
REPORT_MD = REPO / "data" / "cache" / "symintra_measure_report.md"

SEED = 20260907
LEADER_INTRA = 0.40          # pre-reg #32 §1: +40% from session open
FLOORS = {"min_bar_dates": 20, "min_events": 2000,
          "min_tickers": 100, "min_dates_with_events": 15}
FROZEN_SHA = "bcddce00f1f2e03c81e618b2205e4078e4ab3a840be487e56f96268599bb0453"    # placeholder until freeze


def hash_self() -> str:
    b = Path(__file__).read_bytes()
    pat = re.compile(rb'(FROZEN_SHA = "[0-9a-f]{64}")')
    b2, n = pat.subn(b'FROZEN_SHA = "' + b"0" * 64 + b'"', b)
    if n != 1:
        raise RuntimeError(f"expected exactly one FROZEN_SHA hex, got {n}")
    return hashlib.sha256(b2).hexdigest()


def self_check() -> None:
    if FROZEN_SHA == "0" * 64:
        print("FATAL: FROZEN_SHA is blank — tool not frozen. Refusing to run.",
              file=sys.stderr)
        sys.exit(3)
    actual = hash_self()
    if actual != FROZEN_SHA:
        print(f"FATAL: measure_sympathy_intraday.py sha mismatch — frozen "
              f"{FROZEN_SHA[:12]}…, on disk {actual[:12]}….", file=sys.stderr)
        sys.exit(1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--floors", action="store_true",
                    help="report floor status only; no verdicts, no "
                         "one-shot consumption")
    args = ap.parse_args()

    MIV.self_check()   # imported #21 engine must be unmodified
    manifest_sha = hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()
    hist = pd.read_csv(HIST_UNIVERSE, dtype={"ticker": str})
    sector = dict(zip(hist["ticker"], hist["sector"].astype(str)))

    a = Archive(detector="reversal")

    # ---- per-(rel) leader-spike index: first bar where running move from
    # session open crosses +40% ----
    spike_idx: dict[str, int | None] = {}
    for rel, df in a.files.items():
        highs = df["High"].to_numpy()
        opens = df["Open"].to_numpy()
        if len(highs) == 0 or opens[0] <= 0:
            spike_idx[rel] = None
            continue
        run = np.maximum.accumulate(highs) / opens[0] - 1.0
        idx = np.argmax(run >= LEADER_INTRA) if (run >= LEADER_INTRA).any() \
            else None
        spike_idx[rel] = int(idx) if idx is not None else None

    ticker_of = {rel: rel.split("/")[1][:-len(".parquet")] for rel in a.files}
    date_of = {rel: rel.split("/")[0] for rel in a.files}
    # sector mates per (date, sector): rels with a spike on that date
    spiked_mates: dict[tuple[str, str], set[str]] = {}
    unmapped = 0
    for rel, si in spike_idx.items():
        t = ticker_of[rel]
        s = sector.get(t)
        if s is None:
            unmapped += 1
            continue
        if si is not None:
            spiked_mates.setdefault((date_of[rel], s), set()).add(t)

    n_leaders = sum(1 for si in spike_idx.values() if si is not None)
    print(f"leader spikes (>= +40% from open): {n_leaders} (bar-date, "
          f"ticker) files; unmapped tickers: {unmapped}")

    for ev in a.events:
        t, d = ev["ticker"], ev["date"]
        s = sector.get(t)
        hot = False
        if s is not None:
            mates = spiked_mates.get((d, s), set())
            hot = any(m != t and spike_idx[r] is not None
                      and spike_idx[r] <= ev["e_abs"]
                      for m in mates
                      for r in [f"{d}/{m}.parquet"] if r in spike_idx)
        ev["sector_hot"] = hot
        ev["evaluable"] = ev["valid"] and s is not None

    floors = MIV.check_floors(a)
    print("floors:", floors)
    if args.floors:
        RESULTS_JSON.write_text(json.dumps(
            {"pre_reg": "#32", "mode": "floors-only", "floors": floors,
             "manifest_sha256": manifest_sha}, indent=2, default=str),
            encoding="utf-8")
        print(f"wrote {RESULTS_JSON.name} (floors mode — one-shot intact)")
        return 0
    if not floors["met"]:
        print("FLOORS UNMET — refusing measurement (one-shot rule, "
              "pre-reg #32 §1).", file=sys.stderr)
        return 2

    rng = np.random.default_rng(SEED)
    valid = [ev for ev in a.events if ev["valid"] and ev["evaluable"]]
    hot = [ev for ev in valid if ev["sector_hot"]]
    cold = [ev for ev in valid if not ev["sector_hot"]]

    fam = {}

    def slot(key, label, evs_a, evs_b):
        if len(evs_a) < MIN_SLOT or len(evs_b) < MIN_SLOT:
            fam[key] = {"slot": label, "n_a": len(evs_a), "n_b": len(evs_b),
                        "p": 1.0, "est": None, "ci_low": None,
                        "ci_upper": None, "verdict": "INCONCLUSIVE"}
            return
        ra, rb = a.rets_for(evs_a), a.rets_for(evs_b)
        d = MIE.contrast_two(ra, rb, rng)
        fam[key] = {"slot": label, "n_a": len(evs_a), "n_b": len(evs_b),
                    "mean_a": float(ra.mean()), "mean_b": float(rb.mean()),
                    "est": d[0], "ci_low": d[2], "ci_upper": d[3], "p": d[4]}

    slot("hot_minus_cold", "sector-hot − sector-cold", hot, cold)
    slot("hot_minus_raw", "sector-hot − raw (net value)", hot, valid)
    fam = MIE.holm(fam, "F1")
    for k, r in fam.items():
        if r.get("verdict") == "INCONCLUSIVE":
            continue
        r["verdict"] = ("EDGE" if r["holm_rejected"] and r["ci_low"] > 0
                        else "FADE" if r["holm_rejected"] and r["ci_upper"] < 0
                        else "NO EDGE")

    # J-B-04 strata (descriptive)
    early = [ev for ev in valid if ev.get("hour", 99) is not None]
    strata = {"n_valid": len(valid), "n_hot": len(hot), "n_cold": len(cold)}

    out = {
        "pre_reg": "#32",
        "claim": ("intraday sector sympathy: reversal entries with a "
                  "same-sector mate spiking >= +40% from the open beat "
                  "sector-cold entries"),
        "params": {"n": N_PRIMARY, "cost": 0.0015, "seed": SEED,
                   "leader_intra": LEADER_INTRA,
                   "holm_slots": list(fam)},
        "f1": fam,
        "descriptives": strata,
        "floors": floors,
        "fingerprints": {
            "manifest_sha256": manifest_sha,
            "measure_code_sha256": hashlib.sha256(
                Path(__file__).read_bytes()).hexdigest(),
            "veto_engine_sha256": VETO_SHA,
        },
    }
    RESULTS_JSON.write_text(json.dumps(out, indent=2, default=str),
                            encoding="utf-8")
    print(f"wrote {RESULTS_JSON.name}")

    L = ["# Intraday sympathy measurement report (pre-registration #32)", "",
         f"- Pre-reg #32 (frozen per its freeze block); seed {SEED}; entry "
         "set = #19 F1 reversal new-high entries (frozen #21 Archive)",
         f"- Leader spikes (>= +40% from session open): {n_leaders}; "
         f"unmapped tickers {unmapped}", f"- Floors: {floors}", ""]
    L.append("## F1 verdicts (Holm family of 2)")
    L.append("")
    for k, r in fam.items():
        L.append(f"- {r['slot']}: n_a={r['n_a']} n_b={r['n_b']} | est "
                 f"{MIV._fmt(r['est'])} (CI {MIV._fmt(r['ci_low'])}.."
                 f"{MIV._fmt(r['ci_upper'])}, p {r['p']:.3f}) | gate "
                 f"{r.get('holm_gate', '—')} -> **{r['verdict']}**")
    L.append("")
    L.append("`python -X utf8 tools/measure_sympathy_intraday.py` "
             "regenerates this report (seed fixed). `--floors` is safe.")
    L.append("")
    REPORT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())