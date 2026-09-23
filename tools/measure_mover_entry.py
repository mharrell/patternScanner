"""Pre-registration #33 measurement tool — his timing rules on HIS
population: the #15 (B-01) and #19 (reversal/pullback-count/second-
confirmation) families re-run on the MOVER archive
(data/intraday_movers; design: analysis/mover_universe_design.md).

STATUS: SKELETON (2026-09-18) + shakedown gate/population work (2026-09-22)
— pre-reg #33 is DRAFT, NOT frozen. This tool REFUSES full-mode measurement
until the freeze record below is completed (FROZEN = True + seeds set) — an
accidental early run is a loud exit 3, never a silent one-shot. `--audit`
and `--floors` are safe anytime.

Shakedown findings addressed here (pre-reg #33 §5, 2026-09-22):

  1. **The §5 gate.** The frozen #15 audit's universe-attribution clause is
     S&P-600-specific: it demands an `universe_sp600_*` membership file per
     in-window pull, and mover pulls name a roster CSV, so it returned
     `passed: False` with 1,581 errors (one per file) and `window_pulls`
     empty — both campaigns would have been declared VOID at the gate.
     `mover_audit()` re-reads the evidence dict the frozen audit produced
     (keeping every archive-agnostic check: pull chain, per-file SHA-256
     ledger match, orphans, repairs) and re-adjudicates ONLY that clause
     against the mover archive's own notion of a blind full-universe pull:
     an in-window file is attributable iff its pull named a roster CSV
     recorded in `data/mover_rosters/` whose row count equals the pull's
     `tickers_requested`. The frozen engines stay byte-identical (their
     frozen shas are asserted at import by `self_check`).

  2. **The population of record.** The roster CSV, never the directory
     listing: a bar-date directory accumulates the union of every roster in
     Yahoo's 7-day window, so a listing-derived population would be partly
     determined by LATER captures. `restrict_to_rosters()` keeps only events
     whose (bar-date, ticker) is on the roster captured FOR that bar-date; a
     bar-date with no roster contributes no events. Bars from the whole
     archive remain available as baseline material — the design's stated null
     is "other moments of the same movers" and the frozen engine's own pools
     are window-wide, so the baseline treatment is unchanged.

  Both are recorded in PREREGISTRATION #33 §5. **Open for the freeze
  session:** §4's "≥ 20 mover bar-dates" should be read as bar-dates with a
  ROSTER (the population of record), not archive bar-dates — `--floors`
  prints both counts so the choice is made with the numbers in view.

  3. **The bootstrap smoke test.** Running the new gate surfaced that the
     archive's first pull (`20260918-200323`) was a `--limit 3` smoke test,
     so 15 files (3 names × the 5 then-available bar-dates) were NOT blind
     full-roster captures. They sit entirely on PRE-ROSTER dates
     (2026-09-11…09-17) and so contribute no events under §3; the gate
     records a bounded exemption (by pull id, only outside the roster
     window, always printed). Deleting them via `--repair` is the
     alternative — a freeze-session decision, since those dates are long
     outside Yahoo's 7-day window and a repair would delete the bars
     permanently.

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
  python -X utf8 tools/measure_mover_entry.py --audit    # safe: §5 gate only
  python -X utf8 tools/measure_mover_entry.py --floors   # safe
  python -X utf8 tools/measure_mover_entry.py            # full; refuses
                                                         # until frozen
Exit: 0 ok, 1 integrity failure, 2 floors unmet (refused, one-shot
intact), 3 not-frozen / config error.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np

import measure_intraday as MI
import measure_intraday_entry as MIE

REPO = Path(__file__).resolve().parents[1]
MOVER_INTRA = REPO / "data" / "intraday_movers"
MOVER_ROSTERS = REPO / "data" / "mover_rosters"
MOVER_OUT = REPO / "data" / "cache"
MOVER_WINDOW_START = "2026-09-11"   # first mover-archive bar-date
ROSTER_NAME_RE = re.compile(r"\d{4}-\d{2}-\d{2}\.csv")
ATTRIB_MARKER = "is not a membership file (non-blind capture)"

# ---- recorded bootstrap exception (pre-reg #33 §5, finding 3) --------------
# The archive's FIRST pull (pull 20260918-200323, 2026-09-18 14:21 local) was
# a `--limit 3` smoke test of the mover runner: 3 names (CANG/GEMI/SECZ) × the
# 5 window bar-dates then available — 15 files, all on PRE-ROSTER dates
# (2026-09-11…09-17), which contribute no events under §3's population rule.
# The gate exempts that pull BY ID and only on bar-dates before the first
# roster; a non-blind capture can never be exempted inside the roster window,
# and the exemption is printed in the gate evidence, never silent. The
# alternative (a recorded `--repair` of the 15 files) is a freeze-session
# decision: the dates are long outside Yahoo's 7-day window, so a repair now
# would delete the bars permanently.
BOOTSTRAP_SMOKE_PULLS = {"20260918-200323"}

# ---- FREEZE RECORD (pre-reg #33 §5) — completed at freeze, before any
# full-mode run. Seeds are the freeze date, per house convention. ----
FROZEN = False
FROZEN_DATE: str | None = None      # e.g. "2026-10-16"
SEED_B01: int | None = None         # e.g. 20261016
SEED_ENTRY: int | None = None
FLOORS = {"min_bar_dates": 20, "min_events": 2000,
          "min_tickers": 100, "min_dates_with_events": 15}


# --------------------------------------------------------------------------
# the roster — the population of record (pre-reg #33 §1/§3)
# --------------------------------------------------------------------------

def roster_dates() -> list[str]:
    """Bar-dates with a captured roster ("first capture wins", design §2)."""
    if not MOVER_ROSTERS.exists():
        return []
    return sorted(p.stem for p in MOVER_ROSTERS.glob("*.csv")
                  if ROSTER_NAME_RE.fullmatch(p.name))


def roster_tickers(uf: str) -> list[str]:
    """Ticker column of a roster CSV (uf is a bare '<date>.csv' name).

    Empty rosters are recorded as empty by the capture tool and yield an
    empty list here — "no qualifiers today" is itself population data.
    """
    p = MOVER_ROSTERS / uf
    with p.open(newline="", encoding="utf-8") as fh:
        return [r["ticker"].strip().upper()
                for r in csv.DictReader(fh) if (r.get("ticker") or "").strip()]


def roster_sets() -> dict[str, set[str]]:
    return {d: set(roster_tickers(f"{d}.csv")) for d in roster_dates()}


def _rel_key(rel: str) -> tuple[str, str]:
    date, name = rel.split("/")
    return date, name[: -len(".parquet")]


# The two frozen engines name their event lists differently; the population
# filter applies to whichever exist on the archive object.
EVENT_LISTS = ("events", "chase", "f1_events", "f2_events", "f3_pairs")


# --------------------------------------------------------------------------
# §5 gate — the frozen audit with the attribution clause re-adjudicated
# --------------------------------------------------------------------------

def mover_audit(mod) -> dict:
    """Pre-reg #33 §5 gate (see the module docstring, finding 1).

    Every archive-agnostic check comes from the frozen engine's own
    `audit_archive()` — this function does not re-implement them. Only the
    S&P-600 universe-attribution class is re-decided, against the roster
    rule, and the rebuilt `window_pulls` records the evidence.
    """
    ev = mod.audit_archive()
    superseded = [e for e in ev["errors"] if ATTRIB_MARKER in e]
    errors = [e for e in ev["errors"] if ATTRIB_MARKER not in e]

    m = json.loads(Path(mod.MANIFEST_PATH).read_text(encoding="utf-8"))
    pulls = {p["pull_id"]: p for p in m.get("pulls", [])}
    files = m.get("files", {})

    checked = clean = exempt = 0
    rows_of: dict[str, list | None] = {}
    seen: set[str] = set()
    window_pulls: list[dict] = []
    first_roster = (roster_dates() or [None])[0]

    for rel in sorted(files):
        if rel.split("/")[0] < mod.WINDOW_START:
            continue                     # pre-window bar-dates are outside
        p = pulls.get(files[rel].get("pull_id"))
        if p is None:
            errors.append(f"{rel}: pull_id not found")
            continue
        checked += 1
        if p["pull_id"] in BOOTSTRAP_SMOKE_PULLS:
            # bounded exemption: by pull id AND outside the roster window
            if first_roster is not None and rel.split("/")[0] >= first_roster:
                errors.append(
                    f"{rel}: pull {p['pull_id']} is on the bootstrap "
                    f"smoke-test exemption list but its bar-date is inside "
                    f"the roster window (>= {first_roster}) — exemption "
                    f"scope violated")
            else:
                exempt += 1
            continue
        uf = p.get("universe_file") or ""
        if not ROSTER_NAME_RE.fullmatch(uf):
            errors.append(f"{rel}: pull {p['pull_id']} universe {uf!r} is not "
                          f"a roster CSV (non-blind capture)")
            continue
        if uf not in rows_of:
            if not (MOVER_ROSTERS / uf).exists():
                errors.append(f"{rel}: roster missing locally: {uf}")
                rows_of[uf] = None
            else:
                rows_of[uf] = roster_tickers(uf)
        want = rows_of[uf]
        if want is None:
            continue
        if p.get("tickers_requested") != len(want):
            errors.append(f"{rel}: pull {p['pull_id']} requested "
                          f"{p.get('tickers_requested')} != roster rows "
                          f"{len(want)} (--limit / non-blind run in window)")
            continue
        if uf not in seen:
            seen.add(uf)
            window_pulls.append({
                "pull_id": p["pull_id"], "universe_file": uf,
                "universe_sha256": p.get("universe_sha256"),
                "tickers_requested": p.get("tickers_requested"),
                "tickers_ok": p.get("tickers_ok"),
                "tickers_failed": p.get("tickers_failed")})
        clean += 1

    out = dict(ev)
    out["errors"] = errors
    out["passed"] = not errors
    out["window_pulls"] = window_pulls
    out["mover_attribution"] = {
        "rule": "in-window file -> its pull named a roster CSV recorded in "
                "data/mover_rosters/, with tickers_requested == that "
                "roster's row count; the bar-date's own roster must exist "
                "to contribute events",
        "checked": checked, "clean": clean, "errors": len(errors),
        "superseded_sp600_errors": len(superseded),
        "exempt_bootstrap_smoke_test": exempt,
        "exempt_pull_ids": sorted(BOOTSTRAP_SMOKE_PULLS),
        "exempt_scope": f"bar-dates < first roster ({first_roster})",
    }
    return out


# --------------------------------------------------------------------------
# the population of record (pre-reg #33 §3)
# --------------------------------------------------------------------------

def restrict_to_rosters(archive, rosters: dict[str, set[str]]) -> dict:
    """Keep only events whose (bar-date, ticker) is on that date's roster.

    Mutates the archive in place (event lists filtered, pools rebuilt) and
    returns the population read-out. Call before check_floors/run_measurement.
    The two frozen engines name their event lists differently, so whichever
    of EVENT_LISTS exist are filtered.
    """
    stats: dict[str, dict] = {}
    kept_total = dropped_total = 0
    for name in EVENT_LISTS:
        seq = getattr(archive, name, None)
        if not isinstance(seq, list):
            continue
        kept, dropped = [], 0
        for item in seq:
            date, ticker = _rel_key(item["rel"])
            ro = rosters.get(date)
            if ro is None or ticker not in ro:
                dropped += 1
            else:
                kept.append(item)
        setattr(archive, name, kept)
        stats[name] = {"kept": len(kept), "dropped": dropped}
        kept_total += len(kept)
        dropped_total += dropped
    archive._build_pools()               # pools follow the frozen engine

    primary = next((n for n in ("events", "f1_events")
                    if isinstance(getattr(archive, n, None), list)), None)
    event_dates = sorted({ev["date"] for ev in getattr(archive, primary, [])}
                         ) if primary else []
    file_dates = sorted({rel.split("/")[0] for rel in archive.files})
    return {
        "roster_bar_dates": len(rosters),
        "archive_bar_dates": len(file_dates),
        "kept": kept_total, "dropped": dropped_total,
        "per_list": stats,
        "dates_with_events": len(event_dates),
        "event_dates": event_dates,
        "roster_tickers": sum(len(v) for v in rosters.values()),
    }


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


def _gate(tag: str, mod) -> dict | None:
    """Run the §5 gate; print the evidence; None means campaign void."""
    audit = mover_audit(mod)
    a = audit["mover_attribution"]
    chain_ok = all(c["ok"] for c in audit["chain"])
    print(f"[{tag}] §5 gate: {'PASS' if audit['passed'] else 'FAIL'} — "
          f"attribution {a['clean']}/{a['checked']} clean "
          f"({a['superseded_sp600_errors']} S&P-600-clause errors "
          f"re-adjudicated, {a['exempt_bootstrap_smoke_test']} bootstrap "
          f"smoke-test files exempt), {len(audit['window_pulls'])} roster "
          f"pulls attributed, {audit['n_files_ledger']} ledger files, "
          f"chain {'ok' if chain_ok else 'FAIL'}")
    if not audit["passed"]:
        print("FATAL: mover archive integrity audit FAILED — campaign void "
              "(pre-reg #33 §5).", file=sys.stderr)
        for e in audit["errors"][:10]:
            print(f"  - {e}", file=sys.stderr)
        return None
    return audit


def campaign_b01() -> int:
    _redirect(MI, "mover_b01_measure_report.md",
              "mover_b01_measure_results.json")
    MI.self_check()
    audit = _gate("B-01 movers", MI)
    if audit is None:
        return 1
    a = MI.Archive()
    pop = restrict_to_rosters(a, roster_sets())
    print(f"[B-01 movers] population: {pop}")
    floors = MI.check_floors(a)
    print(f"[B-01 movers] floors: {floors}")
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
    audit = _gate("entry movers", MIE)
    if audit is None:
        return 1
    a = MIE.Archive()
    pop = restrict_to_rosters(a, roster_sets())
    print(f"[entry movers] population: {pop}")
    floors = MIE.check_floors(a)
    print(f"[entry movers] floors: {floors}")
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


def audit_only() -> int:
    """Safe: the §5 gate alone — writes nothing, consumes no one-shot."""
    for tag, mod in (("b01", MI), ("entry", MIE)):
        _redirect(mod, f"mover_{tag}_measure_report.md",
                  f"mover_{tag}_measure_results.json")
        mod.self_check()
        audit = _gate(tag, mod)
        if audit is None:
            return 1
    print("§5 gate PASSES on the mover archive under the roster rule "
          "(pre-reg #33 §5 finding 1, resolved).")
    return 0


def floors_only() -> int:
    """Safe: build both archives, report floors, write nothing."""
    rd = roster_dates()
    out = {"pre_reg": "#33", "mode": "floors-only",
           "window_start": MOVER_WINDOW_START,
           "frozen": FROZEN,
           "roster_dates": rd, "n_roster_dates": len(rd),
           "note": "§4's 'mover bar-dates' should be read as ROSTER "
                   "bar-dates (the population of record); archive "
                   "bar-dates are reported alongside — freeze-session "
                   "decision, pre-reg #33 §5 finding 2."}
    print(f"roster bar-dates: {len(rd)} {rd if len(rd) <= 8 else rd[:3] + ['...'] + rd[-2:]}")
    for tag, mod in (("b01", MI), ("entry", MIE)):
        _redirect(mod, f"mover_{tag}_measure_report.md",
                  f"mover_{tag}_measure_results.json")
        mod.self_check()
        a = mod.Archive()
        pop = restrict_to_rosters(a, roster_sets())
        floors = mod.check_floors(a)
        floors["floors"] = FLOORS
        floors["population"] = pop
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
    ap.add_argument("--audit", action="store_true",
                    help="run the §5 gate only (roster attribution rule); "
                         "writes nothing, consumes no one-shot")
    args = ap.parse_args()
    if args.audit:
        return audit_only()
    if args.floors:
        return floors_only()
    freeze_check()
    rc = campaign_b01()
    if rc:
        return rc
    return campaign_entry()


if __name__ == "__main__":
    sys.exit(main())
