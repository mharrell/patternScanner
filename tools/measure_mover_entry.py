"""Pre-registration #33 measurement tool — his timing rules on HIS
population: the #15 (B-01) and #19 (reversal/pullback-count/second-
confirmation) families re-run on the MOVER archive
(data/intraday_movers; design: analysis/mover_universe_design.md).

STATUS: SKELETON, built 2026-09-18 — pre-reg #33 is DRAFT, NOT frozen.
This tool REFUSES full-mode measurement until the freeze record below
is completed (FROZEN = True + seeds set) — an accidental early run is
a loud exit 3, never a silent one-shot. `--floors` is safe anytime.

Mechanics: the frozen engines are IMPORTED UNCHANGED and their archive
paths/window are redirected at runtime to the mover archive (module
globals are read at call time — no frozen byte is touched; each
engine's self_check still asserts its frozen sha). The baselines are
computed WITHIN the mover archive (the right null: other moments of
the same movers), which falls out of the engines' own baseline pools.

Campaigns (one seed each, fixed at freeze):
  A — #15 families on movers: B-01 micro pullback (measure_intraday
      engine) -> mover_b01_measure_{results.json,report.md}
  B — #19 families on movers: reversal long/short, pullback-count,
      second-confirmation (measure_intraday_entry engine) ->
      mover_entry_measure_{results.json,report.md}

Floors (draft #33 §4): >= 20 mover bar-dates, >= 2,000 events per
campaign, >= 100 tickers, >= 15 bar-dates with events; per-slot count
floor 100; house protocol (COST 0.15%, B=1000, Holm a=0.05, one-shot,
audit PASSED gates any EDGE).

Run:
  python -X utf8 tools/measure_mover_entry.py --floors   # safe
  python -X utf8 tools/measure_mover_entry.py            # full; refuses
                                                         # until frozen
Exit: 0 ok, 1 integrity failure, 2 floors unmet (refused, one-shot
intact), 3 not-frozen / config error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

import measure_intraday as MI
import measure_intraday_entry as MIE

REPO = Path(__file__).resolve().parents[1]
MOVER_INTRA = REPO / "data" / "intraday_movers"
MOVER_OUT = REPO / "data" / "cache"
MOVER_WINDOW_START = "2026-09-11"   # first mover-archive bar-date

# ---- FREEZE RECORD (pre-reg #33 §5) — completed at freeze, before any
# full-mode run. Seeds are the freeze date, per house convention. ----
FROZEN = False
FROZEN_DATE: str | None = None      # e.g. "2026-09-25"
SEED_B01: int | None = None         # e.g. 20260925
SEED_ENTRY: int | None = None
FLOORS = {"min_bar_dates": 20, "min_events": 2000,
          "min_tickers": 100, "min_dates_with_events": 15}


def _redirect(mod, report_name: str, results_name: str) -> None:
    """Point a frozen engine's archive/report globals at the mover
    archive. The engines read these module globals at call time; their
    code bytes — and therefore their self-checks — are untouched."""
    mod.INTRA = MOVER_INTRA
    mod.RAW_DIR = MOVER_INTRA / "raw"
    mod.MANIFEST_PATH = MOVER_INTRA / "manifest.json"
    mod.WINDOW_START = MOVER_WINDOW_START
    mod.REPORT_PATH = MOVER_OUT / report_name
    mod.RESULTS_PATH = MOVER_OUT / results_name


def freeze_check() -> None:
    if not (FROZEN and FROZEN_DATE and SEED_B01 and SEED_ENTRY):
        print("FATAL: pre-reg #33 is not frozen (DRAFT) — full-mode "
              "measurement is refused. Complete the freeze record in "
              "tools/measure_mover_entry.py after the shakedown "
              "(design §6), then re-run.", file=sys.stderr)
        sys.exit(3)


def campaign_b01() -> int:
    _redirect(MI, "mover_b01_measure_report.md",
              "mover_b01_measure_results.json")
    MI.self_check()
    audit = MI.audit_archive()
    if not audit.get("passed", False):
        print("FATAL: mover archive integrity audit FAILED — campaign "
              "void (pre-reg #33 §5 gate).", file=sys.stderr)
        return 1
    a = MI.Archive()
    floors = MI.check_floors(a)
    print("[B-01 movers] floors:", floors)
    if not floors["met"]:
        print("FLOORS UNMET (B-01) — refusing measurement; one-shot "
              "intact.", file=sys.stderr)
        return 2
    rng = np.random.default_rng(SEED_B01)
    results = MI.run_measurement(a, rng)
    MI.write_report(results, audit)
    print(f"[B-01 movers] family: {results.get('f1', {}).get('_family')}")
    return 0


def campaign_entry() -> int:
    _redirect(MIE, "mover_entry_measure_report.md",
              "mover_entry_measure_results.json")
    MIE.self_check()
    audit = MIE.audit_archive()
    if not audit.get("passed", False):
        print("FATAL: mover archive integrity audit FAILED — campaign "
              "void (pre-reg #33 §5 gate).", file=sys.stderr)
        return 1
    a = MIE.Archive()
    floors = MIE.check_floors(a)
    print("[entry movers] floors:", floors)
    if not floors["met"]:
        print("FLOORS UNMET (entry) — refusing measurement; one-shot "
              "intact.", file=sys.stderr)
        return 2
    rng = np.random.default_rng(SEED_ENTRY)
    results = MIE.run_measurement(a, rng)
    MIE.write_report(results, audit)
    for fam in ("f1", "f2", "f3"):
        f = results.get(fam, {})
        if f:
            print(f"[entry movers] {fam} family: "
                  f"{f.get('_family')}")
    return 0


def floors_only() -> int:
    """Safe: build both archives, report floors, write nothing."""
    out = {"pre_reg": "#33", "mode": "floors-only",
           "window_start": MOVER_WINDOW_START,
           "frozen": FROZEN}
    for tag, mod in (("b01", MI), ("entry", MIE)):
        _redirect(mod, f"mover_{tag}_measure_report.md",
                  f"mover_{tag}_measure_results.json")
        mod.self_check()
        a = mod.Archive()
        floors = mod.check_floors(a)
        floors["floors"] = FLOORS
        out[tag] = floors
        print(f"[{tag}] floors: {floors}")
    MOVER_OUT.joinpath("mover_floors.json").write_text(
        json.dumps(out, indent=2, default=str), encoding="utf-8")
    print("wrote mover_floors.json (floors mode — no one-shot touched)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--floors", action="store_true",
                    help="report floor status only; no verdicts, no "
                         "one-shot consumption")
    args = ap.parse_args()
    if args.floors:
        return floors_only()
    freeze_check()
    rc = campaign_b01()
    if rc:
        return rc
    return campaign_entry()


if __name__ == "__main__":
    sys.exit(main())
