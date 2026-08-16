"""Driver for pre-registration #13 — historical-constituent re-check of the
RSI-divergence bullish EDGE (brief §5 survivorship gate; pre-reg #10 §8).

Runs the FROZEN pre-reg #10 measurement (tools/measure_divergence.py, sha
85f2ae0d4a1e...; Phase-3 engine measure.py, sha c7421fbffe...) byte-
identically against the historical-constituent union universe, via
process-local rebinding only — no frozen file is modified, nothing is
imported from a copy. Then patches ONLY the pre-registered presentation
labels (pre-reg #13 §2, amended 2026-08-15), each listed verbatim:

JSON (divergence_hist_measure_results.json):
  "pre_reg": "#10" -> "#13"
  "claim" -> the re-check descriptor (below)
  (everything else — era_oos_start, fingerprints, all numbers — is
  produced by the frozen code from the rebound inputs)

Report (divergence_hist_measure_report.md):
  header: "# RSI divergence measurement report (pre-registration #10)"
      -> "# RSI divergence measurement report (pre-registration #13 — the
          historical-constituent re-check)"
  pre-reg block: "- Pre-registration #10 (frozen 2026-08-14): claims = "
      -> "- Pre-registration #13 (frozen 2026-08-15; the brief §5
          historical-constituent re-check of pre-reg #10, pre-reg #10 §8;
          universe = union of 5 annual S&P 600 snapshots 2021-2025, 904
          names incl. ~330 delisted/removed; OOS 2022-2025): claims = "
  era-split line: "IS 2000-2015 / OOS 2016-2025" -> "IS 2000-2021
      (descriptive only — no IS-era membership data) / OOS 2022-2025"
  S6 header: "### S6: IS record (descriptive — selection era)"
      -> "### S6: IS record (descriptive only — no IS-era membership data)"
  reproducibility line: "python -X utf8 tools/measure_divergence.py" ->
      "python -X utf8 tools/measure_divergence_hist.py"

No numeric content is changed anywhere; every replacement is an exact
string substitution on a line that would otherwise misidentify the run.

Rebind surface (verified against the frozen call chain, 2026-08-15):
  measure_divergence.UNIVERSE_CSV / ERA_OOS / RESULTS / REPORT (module
      level; ERA_OOS gates the frequency function)
  measure.ERA_OOS (call-time global of window_pool, measure_returns and
      the is_oos tag — this gates the baseline pools AND the F1/F2 rows)
  measure_pillars.ERA_OOS / measure_veto.ERA_OOS are import-time copies
      but are never read in this call chain (build_pools delegates to
      window_pool; two_sample_excess has no era gate) — left untouched.

Usage: python -X utf8 tools/measure_divergence_hist.py
"""
import hashlib
import json
import sys
from pathlib import Path

import measure
import measure_divergence as md

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"

UNIVERSE_HIST = CACHE / "universe_sp600_hist_2026-08-15.csv"   # pre-reg #13 §1
RESULTS = CACHE / "divergence_hist_measure_results.json"       # pre-reg #13 §2
REPORT = CACHE / "divergence_hist_measure_report.md"
ERA_OOS = "2022-01-01"                      # pre-reg #13 §3 (amended)

FROZEN = {
    measure.__file__: "c7421fbffeaf16ed43278faafa7325e2972634d516bc013c41e15e7f733b1b93",
    md.__file__: "85f2ae0d4a1e07906d88fb9c4b2fda02e68f943635b618af660502ddc5597c72",
}

CLAIM_RECHECK = (
    "Re-check of the pre-reg #10 claim (bullish divergence: price lower "
    "low + RSI higher low => bounce; bearish divergence: price higher "
    "high + RSI lower high => pullback; 'a lot less common so arguably a "
    "bit more reliable' vs 70/30 signals) against historical constituents "
    "— brief §5 survivorship gate, pre-reg #10 §8; universe = union of 5 "
    "annual S&P 600 snapshots 2021-2025 (904 names, incl. ~330 delisted/"
    "removed); measurement = frozen pre-reg #10 code byte-identical, era "
    "boundary the only change (OOS 2022-2025)"
)


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def patch_labels() -> None:
    """Pre-registered label patch (pre-reg #13 §2) — labels only."""
    j = json.loads(RESULTS.read_text(encoding="utf-8"))
    assert j["pre_reg"] == "#10", f"unexpected pre_reg: {j['pre_reg']}"
    j["pre_reg"] = "#13"
    assert j["claim"].startswith("Bullish divergence (price lower low"), \
        "unexpected claim layout"
    j["claim"] = CLAIM_RECHECK
    RESULTS.write_text(json.dumps(j, indent=2), encoding="utf-8")

    text = REPORT.read_text(encoding="utf-8")
    old = "# RSI divergence measurement report (pre-registration #10)"
    new = ("# RSI divergence measurement report (pre-registration #13 — "
           "the historical-constituent re-check)")
    assert text.count(old) == 1
    text = text.replace(old, new)

    old = "- Pre-registration #10 (frozen 2026-08-14): claims = "
    new = ("- Pre-registration #13 (frozen 2026-08-15; the brief §5 "
           "historical-constituent re-check of pre-reg #10, pre-reg #10 "
           "§8; universe = union of 5 annual S&P 600 snapshots 2021-2025, "
           "904 names incl. ~330 delisted/removed; OOS 2022-2025): "
           "claims = ")
    assert text.count(old) == 1
    text = text.replace(old, new)

    old = "IS 2000-2015 / OOS 2016-2025"
    new = ("IS 2000-2021 (descriptive only — no IS-era membership data) "
           "/ OOS 2022-2025")
    assert text.count(old) == 1
    text = text.replace(old, new)

    old = "### S6: IS record (descriptive — selection era)"
    new = "### S6: IS record (descriptive only — no IS-era membership data)"
    assert text.count(old) == 1
    text = text.replace(old, new)

    old = "`python -X utf8 tools/measure_divergence.py`"
    new = "`python -X utf8 tools/measure_divergence_hist.py`"
    assert text.count(old) == 1
    text = text.replace(old, new)

    REPORT.write_text(text, encoding="utf-8")


def main() -> int:
    for f, want in FROZEN.items():
        got = sha(Path(f))
        assert got == want, f"{f} changed (sha {got[:16]}..., want {want[:16]}...)"
    print("frozen shas OK (measure.py c7421fbf…, measure_divergence.py "
          "85f2ae0d4a1e…)")

    md.UNIVERSE_CSV = UNIVERSE_HIST
    md.ERA_OOS = ERA_OOS
    measure.ERA_OOS = ERA_OOS
    md.RESULTS = RESULTS
    md.REPORT = REPORT
    print(f"rebound: universe {UNIVERSE_HIST.name}, ERA_OOS {ERA_OOS}, "
          f"results {RESULTS.name}, report {REPORT.name}")

    rc = md.main()
    patch_labels()
    print("labels patched (pre-reg #13 §2)")
    return rc


if __name__ == "__main__":
    sys.exit(main())
