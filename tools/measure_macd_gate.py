"""Pre-registration #27 measurement tool — the MACD crossover gate on
1-minute bars (ledger rows J-B-01, J-B-04, J-C-01, 2n2-05/-07/-08/-21/-22).

Implements exactly PREREGISTRATION.md pre-reg #27 §3:
  F1, 4 Holm slots (count floor 100 evaluable per slot), two-sample
  bootstrap via measure_intraday_entry's contrast_two, B=1000 seed 20260902,
  N=60 primary, cost 0.15%, hour-matched same-ticker + random-universe
  baselines (#15 §4 convention):
    1. open − closed   : MACD-open (line ≥ 9-signal) entries − MACD-closed
    2. open − raw      : MACD-open entries − all evaluable candidates
    3. window          : gate-open entries ≤ 30 min after the session's
                         FIRST bullish cross − > 30 min after it
    4. new-highs       : gate-open entries with signal-bar High within 0.5%
                         of the RUNNING session high (no look-ahead) − below
  Each slot reports its two time-since-open strata (≤30 min / >30 min from
  session open) as pre-declared descriptive rows (J-B-04 news-spike
  exemption).
  F2 descriptives (no verdicts): gate shares, overlap with #21's line<0
  form, 5-min-MACD state at entry.

Entry set: pre-reg #19 F1 reversal new-high entries — built by reusing
measure_intraday_veto's Archive (frozen #21 machinery, imported unchanged).
MACD = EMA12 − EMA26 of the file's close series (warm-up ≥ 26 bars); signal
= EMA9 of the MACD line (standard 12/26/9, J-E-01).

Floors (§4, one-shot): ≥20 full-universe bar-dates ≥2026-08-19, ≥2,000
F1-evaluable candidates, ≥100 tickers, ≥15 dates with events. `--floors`
reports floor status WITHOUT computing verdicts and does not consume the
one-shot. §5 archive-integrity gate: the manifest sha is recorded; EDGE
verdicts additionally require the #15 §6 audit to pass (verify_intraday.py)
on the same archive state — recorded in §8.

Freeze discipline: FROZEN_SHA blanked-self-hash; refuses to run on
placeholder/mismatch.

Run:  python -X utf8 tools/measure_macd_gate.py [--floors]
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
                                   MIN_SLOT, WINDOW_START, INTRA,
                                   MANIFEST_PATH)

REPO = Path(__file__).resolve().parents[1]
RESULTS_JSON = REPO / "data" / "cache" / "macdgate_measure_results.json"
REPORT_MD = REPO / "data" / "cache" / "macdgate_measure_report.md"

SEED = 20260902
WINDOW_MIN = 30          # 2n2-07's 30-minute profit window
NH_PCT = 0.005           # 2n2-08 new-highs conjunct: within 0.5% of RTH high
FLOORS = {"min_bar_dates": 20, "min_events": 2000,
          "min_tickers": 100, "min_dates_with_events": 15}
FROZEN_SHA = "c8b75434390965601b94adc37737e31d67a38d43d9294a6c20024c564ff23431"    # placeholder until freeze


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
        print(f"FATAL: measure_macd_gate.py sha mismatch — frozen "
              f"{FROZEN_SHA[:12]}…, on disk {actual[:12]}….", file=sys.stderr)
        sys.exit(1)


def gate_fields(df, wpos, e_pos, e_abs) -> dict:
    """MACD line/signal at the entry bar, minutes since the first bullish
    cross, minutes since session open, and the running-session-high test.
    Known at the close of the entry bar (no look-ahead): the cross scan and
    the running high use bars ≤ e_abs only."""
    closes = df["Close"].to_numpy()
    highs = df["High"].to_numpy()
    times = df.index[wpos]
    n = e_abs + 1
    c = closes[:n]
    line = MIV._ema_series(c, 12) - MIV._ema_series(c, 26)
    sig = MIV._ema_series(line, 9)
    open_gate = bool(line[-1] >= sig[-1])
    # first bullish cross of the session (line crosses above signal)
    cross_i = None
    above_prev = line[0] >= sig[0]
    for i in range(1, n):
        above = line[i] >= sig[i]
        if above and not above_prev:
            cross_i = i
            break
        above_prev = above
    t_e = df.index[e_abs]
    t_open = df.index[wpos[0]]
    mins_open = (t_e - t_open).total_seconds() / 60.0
    if cross_i is None:
        mins_cross = None
    else:
        mins_cross = (t_e - df.index[cross_i]).total_seconds() / 60.0
    run_high = float(highs[wpos[:e_pos + 1]].max())
    nh = bool(highs[e_abs] >= (1 - NH_PCT) * run_high)
    return {"gate_open": open_gate_safe(open_gate), "mins_open": mins_open,
            "mins_cross": mins_cross, "new_high": nh,
            "line": float(line[-1]), "signal": float(sig[-1])}


def open_gate_safe(v):
    return bool(v)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--floors", action="store_true",
                    help="report §4 floor status only; no verdicts, no "
                         "one-shot consumption")
    args = ap.parse_args()

    MIV.self_check()   # the #21 veto tool must be unmodified (imported engine)
    manifest_sha = hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()

    a = Archive(detector="reversal")

    # crossover-gate fields per event
    for ev in a.events:
        df = a.files[ev["rel"]]
        w = a.wpos(ev["rel"])
        gf = gate_fields(df, w, ev["e_pos"], ev["e_abs"])
        ev.update(gf)
        ev["evaluable"] = ev["evaluable"] and gf["mins_open"] is not None

    floors = MIV.check_floors(a)
    print("floors:", floors)
    if args.floors:
        out = {"pre_reg": "#27", "mode": "floors-only",
               "floors": floors, "manifest_sha256": manifest_sha}
        RESULTS_JSON.write_text(json.dumps(out, indent=2, default=str),
                                encoding="utf-8")
        print(f"wrote {RESULTS_JSON.name} (floors mode — one-shot intact)")
        return 0
    if not floors["met"]:
        print("FLOORS UNMET — refusing measurement (one-shot rule, "
              "pre-reg #27 §4).", file=sys.stderr)
        return 2

    rng = np.random.default_rng(SEED)
    valid = [ev for ev in a.events if ev["valid"] and ev["evaluable"]]

    open_evs = [ev for ev in valid if ev["gate_open"]]
    closed_evs = [ev for ev in valid if not ev["gate_open"]]
    early = [ev for ev in open_evs
             if ev["mins_cross"] is not None and ev["mins_cross"] <= WINDOW_MIN]
    late = [ev for ev in open_evs
            if ev["mins_cross"] is None or ev["mins_cross"] > WINDOW_MIN]
    nh_in = [ev for ev in open_evs if ev["new_high"]]
    nh_out = [ev for ev in open_evs if not ev["new_high"]]
    early_session = [ev for ev in valid if ev["mins_open"] <= WINDOW_MIN]
    late_session = [ev for ev in valid if ev["mins_open"] > WINDOW_MIN]

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

    slot("open_minus_closed", "open − closed (primary claim)",
         open_evs, closed_evs)
    slot("open_minus_raw", "open − raw (net filter value)",
         open_evs, valid)
    slot("window", f"≤{WINDOW_MIN}min-after-cross − >{WINDOW_MIN}min",
         early, late)
    slot("new_highs", "at-running-high − below (gate-open only)",
         nh_in, nh_out)
    fam = MIE.holm(fam, "F1")
    for k, r in fam.items():
        if r.get("verdict") == "INCONCLUSIVE":
            continue
        r["verdict"] = ("EDGE" if r["holm_rejected"] and r["ci_low"] > 0
                        else "FADE" if r["holm_rejected"] and r["ci_upper"] < 0
                        else "NO EDGE")

    # F2 descriptives (no verdicts)
    n_line_neg = sum(1 for ev in valid if ev.get("macd_neg"))
    overlap = sum(1 for ev in valid if not ev["gate_open"] and ev.get("macd_neg"))
    f2 = {
        "n_valid": len(valid),
        "gate_open": len(open_evs), "gate_closed": len(closed_evs),
        "line_neg_share": n_line_neg / len(valid) if valid else None,
        "closed_and_line_neg_share": overlap / len(closed_evs)
        if closed_evs else None,
        "strata_minutes_since_open": {
            "early_<=30min": {"n": len(early_session),
                              "open_share": (sum(1 for ev in early_session
                                                 if ev["gate_open"])
                                             / len(early_session))
                             if early_session else None},
            "late_>30min": {"n": len(late_session),
                            "open_share": (sum(1 for ev in late_session
                                               if ev["gate_open"])
                                           / len(late_session))
                            if late_session else None}},
    }

    out = {
        "pre_reg": "#27",
        "claim": ("MACD crossover gate on 1-min bars: line ≥ 9-signal at "
                  "entry, the 30-minute window after the first bullish "
                  "cross, and the new-highs conjunct; news-spike "
                  "stratification per J-B-04"),
        "params": {"n": N_PRIMARY, "cost": COST_PRIMARY, "b": B,
                   "seed": SEED, "alpha": ALPHA,
                   "window_min": WINDOW_MIN, "nh_pct": NH_PCT,
                   "holm_slots": list(fam), "min_slot": MIN_SLOT},
        "f1": fam,
        "f2_descriptives": f2,
        "floors": floors,
        "fingerprints": {
            "manifest_sha256": manifest_sha,
            "measure_code_sha256": hashlib.sha256(
                Path(__file__).read_bytes()).hexdigest(),
            "veto_engine_sha256": VETO_SHA,
            "entry_engine_sha256": hashlib.sha256(
                Path(MIE.__file__).read_bytes()).hexdigest(),
        },
    }
    RESULTS_JSON.write_text(json.dumps(out, indent=2, default=str),
                            encoding="utf-8")
    print(f"wrote {RESULTS_JSON.name}")

    L = ["# MACD gate measurement report (pre-registration #27)", "",
         f"- Pre-reg #27 (frozen per its freeze block); seed {SEED}, B={B}, "
         f"alpha {ALPHA}, N={N_PRIMARY}, cost {COST_PRIMARY}; entry set = "
         "#19 F1 reversal new-high entries (reusing the frozen #21 Archive)",
         f"- Floors: {floors}", ""]
    L.append("## F1 verdicts (Holm family of 4)")
    L.append("")
    for k, r in fam.items():
        L.append(f"- {r['slot']}: n_a={r['n_a']} n_b={r['n_b']} | est "
                 f"{MIV._fmt(r['est'])} (CI {MIV._fmt(r['ci_low'])}.."
                 f"{MIV._fmt(r['ci_upper'])}, p {r['p']:.3f}) | gate "
                 f"{r.get('holm_gate', '—')} -> **{r['verdict']}**")
    L.append("")
    L.append("## Strata (news-spike exemption, J-B-04 — descriptive)")
    L.append("")
    for k, s in f2["strata_minutes_since_open"].items():
        L.append(f"- {k}: n={s['n']}, gate-open share "
                 f"{MIV._fmt(s['open_share'])}")
    L.append("")
    L.append("## F2 descriptives")
    L.append("")
    L.append(f"- gate-open {f2['gate_open']} / closed {f2['gate_closed']} of "
             f"{f2['n_valid']} evaluable entries; line<0 share "
             f"{MIV._fmt(f2['line_neg_share'])}; closed∩line<0 share "
             f"{MIV._fmt(f2['closed_and_line_neg_share'])}")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_macd_gate.py` regenerates this "
             "report (seed fixed). `--floors` reports floor status only.")
    L.append(f"Manifest sha {manifest_sha[:12]}…; veto engine {VETO_SHA[:12]}… "
             "imported unchanged.")
    L.append("")
    REPORT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {REPORT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())