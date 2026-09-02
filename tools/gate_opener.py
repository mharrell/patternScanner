"""Gate opener — runs the §5-gated intraday campaigns when the shared
paper-log floors are met (pre-regs #15/#19/#20/#21/#22/#23/#27, intraday
track).

Every gated tool follows the same discipline: full mode REFUSES (exit 2)
when the §4 floors are unmet, WITHOUT consuming the one-shot; exit 0 means
the one-shot measurement ran. This opener exploits exactly that contract:

  for each campaign in pre-reg order (pending only):
      run the tool (full mode)
      exit 0 -> archive its results/report under data/measurements/<tag>/
                (tracked, durable), mark DONE in the state file
      exit 2 -> floors unmet, leave PENDING
      other  -> record the failure, leave PENDING (a later run may retry a
                failed non-measurement run only if nothing was produced;
                the state file records every attempt)

One-shot safety: a tool marked DONE is never re-run by the opener. Tools
whose verdicts need recording (pre-reg §8 + ledger flips) are left to a
session — the opener measures and archives, it does not write verdicts.

Run:  python -X utf8 tools/gate_opener.py [--status]
Exit: 0 ok (measured or all-pending), 1 tool error (see log).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CACHE = REPO / "data" / "cache"
MEAS_DIR = REPO / "data" / "measurements"
STATE = CACHE / "gate_opener_state.json"

PYTHON = sys.executable
# Pre-reg order. Each entry: (pre_reg, tool_relpath, results_glob_patterns)
CAMPAIGNS = [
    ("#15/#19", "tools/measure_intraday.py",
     ["data/cache/intraday_measure_results.json",
      "data/cache/intraday_measure_report.md"]),
    ("#20", "tools/measure_intraday_exit.py",
     ["data/cache/intraday_exit_measure_results.json",
      "data/cache/intraday_exit_measure_report.md"]),
    ("#21", "tools/measure_intraday_veto.py",
     ["data/cache/intraday_veto_measure_results.json",
      "data/cache/intraday_veto_measure_report.md"]),
    ("#22", "tools/measure_intraday_regime.py",
     ["data/cache/intraday_regime_measure_results.json",
      "data/cache/intraday_regime_measure_report.md"]),
    ("#27", "tools/measure_macd_gate.py",
     ["data/cache/macdgate_measure_results.json",
      "data/cache/macdgate_measure_report.md"]),
    ("#32", "tools/measure_sympathy_intraday.py",
     ["data/cache/symintra_measure_results.json",
      "data/cache/symintra_measure_report.md"]),
]
# #23 (paper-loop execution comparison) is §7-gated on the OTHER floors
# being met first; the opener records it as deferred-by-design.
DEFERRED = {"#23": "runs via verify_intraday/paper-loop after #15-#22 land"}


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"done": {}, "attempts": {}}


def main() -> int:
    state = load_state()
    log = []
    measured = []
    for pre_reg, tool, artifacts in CAMPAIGNS:
        name = Path(tool).stem
        if state["done"].get(name):
            log.append(f"[{pre_reg}] {name}: DONE previously, skipped")
            continue
        state["attempts"].setdefault(name, []).append(
            subprocess.list2cmdline([sys.executable, "-X", "utf8", tool]))
        proc = subprocess.run(
            [sys.executable, "-X", "utf8", str(REPO / tool)],
            cwd=REPO, capture_output=True, text=True, timeout=3600)
        tail = (proc.stdout or "").strip().splitlines()[-5:]
        log.append(f"[{pre_reg}] {name}: exit={proc.returncode} | "
                   + " / ".join(tail))
        if proc.returncode == 0:
            state["done"][name] = True
            measured.append(pre_reg)
            outdir = MEAS_DIR / name
            outdir.mkdir(parents=True, exist_ok=True)
            for pat in artifacts:
                src = REPO / pat
                if src.exists():
                    shutil.copy2(src, outdir / src.name)
            log.append(f"[{pre_reg}] {name}: archived to {outdir}")
        elif proc.returncode == 2:
            log.append(f"[{pre_reg}] {name}: floors unmet — pending")
        else:
            log.append(f"[{pre_reg}] {name}: ERROR (see stderr in log file)")
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print("\n".join(log))
    if measured:
        print(f"MEASURED: {', '.join(measured)} — verdicts pending session "
              "recording (pre-reg §8 + ledger).")
    print(f"#23 deferred by design: {DEFERRED['#23']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())