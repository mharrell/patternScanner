"""Pre-registration #21 measurement tool — the two-filter pre-entry veto on
1-minute bars: MACD negative and high-volume red candle (ledger rows E-01,
E-04).

Entry set = the pre-reg #19 F1 reversal-new-high LONG leg (decline = D=3
consecutive DOWN bars, signal bar e = first bar with High[e] > High[e-1],
entry = open of e+1), frozen in tools/measure_intraday_entry.py. Its
LF-normalized sha256 is asserted AT IMPORT (the shared frozen input).

Veto legs (both fully known at the close of the entry bar e, before entry
open e+1):
  (i)   MACD: MACD = EMA12 - EMA26 of the file's 1-min close series from
        the day's first bar; warm-up >= 26 closes; MACD < 0 at the entry
        bar -> veto. If the warm-up is unmet (entry bar at file-absolute
        index < 25) the leg is UNEVALUABLE and the candidate is excluded
        from the pass/fail classification (counted separately).
  (ii)  Volume: the entry bar's volume >= V x the file's median RTH bar
        volume AND the bar is red (Close < Open) -> veto (V = 3 primary).
  veto-pass = neither leg fires; veto-fail = either leg fires; a candidate
  is classifiable only when the MACD warm-up is met.

Implements PREREGISTRATION.md §Pre-registration #21 exactly:
  * §1 the veto legs (V = 3 primary; S-V2: 2, S-V5: 5),
  * §3 the measurement: F1 (conditioning) - 4 Holm slots (pass-fail,
    pass-raw, MACD leg, volume leg); F2 (kill-rate decomposition) rows,
    NO verdicts; the declared sensitivities (S-V2/S-V5, S-C05/S-C30,
    S-N15/S-N120/S-N240, S-B01 veto applied to the B-01 entry set);
  * §4 the sample-size floors and the one-shot rule (measurement REFUSED
    until the floors are met; audit-only mode computes no returns),
  * §5 the archive-integrity audit (shared with pre-reg #15).

Frozen 2026-08-21, before any measurement. The module sha is asserted at
run (FROZEN_SHA below, the fixed-point convention; measure_code_sha256
records the raw file sha): any byte change invalidates the campaign. The
frozen-input detector tools are asserted at import at their LF-normalized
sha256 (committed blobs, checkout-independent):
  tools/measure_intraday_entry.py  = the reversal-new-high entry set
  tools/measure_intraday.py        = the B-01 detector (S-B01 only)

Modes:
  python -X utf8 tools/measure_intraday_veto.py --audit-only
      §5 audit + entry detection counts only. Computes NO forward return
      of any kind. Exit 0 = audit clean; 1 = audit FAILED.
  python -X utf8 tools/measure_intraday_veto.py
      Full measurement. Requires the §5 floors; otherwise REFUSES (exit
      2). Writes data/cache/intraday_veto_measure_report.md +
      intraday_veto_measure_results.json, prints their sha256 for the
      determinism check (two runs must byte-compare).

Exit codes: 0 ok, 1 audit/integrity failure, 2 floors unmet (refused),
3 input error.

Spec mapping (pre-reg #21 §1/§3; the primary column):
  F1 - 4 Holm slots, each a two-sample bootstrap contrast (B=1000, seed
  20260821, Holm alpha 0.05) of mean N=60-bar forward returns
  (C[e+N] - O[e+1])/O[e+1] - COST 0.0015, count floor 100:
    1. pass - fail   (veto-pass minus veto-fail; claim: pass better)
    2. pass - raw    (veto-pass minus all cleanly-classified candidates)
    3. macd leg      (MACD >= 0 minus MACD < 0, the leg alone)
    4. volume leg    (no red volume-spike minus with, the leg alone)
  F2 rows (no verdicts): kill-rate decomposition - what fraction each leg
  alone kills, and the killed sets' mean forwards vs the kept set; the kept
  set's hour-matched same-ticker / random-universe baseline excess (pre-reg
  #15 §4 convention).
  Sensitivities (no verdicts): S-V2/S-V5 (volume threshold), S-C05/S-C30
  (cost), S-N15/S-N120/S-N240 (horizon), S-B01 (the veto on the B-01
  entry set as a cross-check on the entry-set choice).
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np

import measure_intraday_entry as MIE
import measure_intraday as MI

ROOT = Path(__file__).resolve().parent.parent
INTRA = ROOT / "data" / "intraday"
RAW_DIR = INTRA / "raw"
MANIFEST_PATH = INTRA / "manifest.json"
REPAIRS_PATH = INTRA / "repairs.json"
OUT_DIR = ROOT / "data" / "cache"
REPORT_PATH = OUT_DIR / "intraday_veto_measure_report.md"
RESULTS_PATH = OUT_DIR / "intraday_veto_measure_results.json"

WINDOW_START = "2026-08-19"

# ---- frozen-input assertions (pre-reg #21 §1/§2) ----
# The entry set is the frozen pre-reg #19 reversal-new-high detector in
# tools/measure_intraday_entry.py; its LF-normalized sha256 (the committed
# blob, checkout-independent) is asserted here. tools/measure_intraday.py is
# the frozen pre-reg #15 B-01 detector, used only by the S-B01 sensitivity.
_FROZEN_INPUT_ENTRY_SHA256 = \
    "d58a889c6c0a634952bacd90bf412140709102053facebf1ee82b5df67592656"
_FROZEN_INPUT_B01_SHA256 = \
    "c58282caf75c344f228b70b329e9182b54a663d013891fe6a17103dc89f5e14c"


def _lf_sha(module) -> str:
    """LF-normalized sha256 of a tools module (committed-blob equivalent)."""
    return hashlib.sha256(Path(module.__file__).read_bytes()
                          .replace(b"\r\n", b"\n")).hexdigest()


_got_entry = _lf_sha(MIE)
assert _got_entry == _FROZEN_INPUT_ENTRY_SHA256, (
    f"{MIE.__file__} changed (sha {_got_entry[:16]}..., want "
    f"{_FROZEN_INPUT_ENTRY_SHA256[:16]}...) — frozen input must not move")
_got_b01 = _lf_sha(MI)
assert _got_b01 == _FROZEN_INPUT_B01_SHA256, (
    f"{MI.__file__} changed (sha {_got_b01[:16]}..., want "
    f"{_FROZEN_INPUT_B01_SHA256[:16]}...) — frozen input must not move")

# ---- frozen parameters (pre-reg #21 §1/§3) ----
N_PRIMARY = 60               # forward horizon (bars; S-N15/S-N120/S-N240)
COST_PRIMARY = 0.0015
V_PRIMARY = 3.0              # volume-spike multiple (S-V2: 2, S-V5: 5)
D_PRIMARY = 3                # decline run length (frozen #19 detector)
WARMUP_MACD = 26             # EMA26 warm-up: closes from day open to entry
B = 1000
SEED = 20260821              # freeze date
ALPHA = 0.05
FLOORS = {"min_bar_dates": 20, "min_events": 2000,
          "min_tickers": 100, "min_dates_with_events": 15}
MIN_SLOT = 100  # per-slot count floor (house)

# Freeze sha (house convention, measure_intraday.py/measure_cexit.py): the
# sha of this file with its own FROZEN_SHA hex blanked to 64 zeros — a
# well-defined fixed point (a file cannot hash to a value embedded in
# itself). Any byte change outside the blanked hex breaks the assertion.
FROZEN_SHA = "60569201e50982a2a2a837464aaaae81ac2111e0f2dba78c4c0835e36f304997"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


_FROZEN_RE = re.compile(rb'(FROZEN_SHA = "[0-9a-f]{64}")')


def hash_self() -> str:
    """sha256 of this file with the FROZEN_SHA hex blanked (fixed point)."""
    b = Path(__file__).read_bytes()
    b2, n = _FROZEN_RE.subn(b'FROZEN_SHA = "' + b"0" * 64 + b'"', b)
    if n != 1:
        raise RuntimeError("expected exactly one FROZEN_SHA hex line")
    return sha_bytes(b2)


def self_check() -> None:
    if FROZEN_SHA == "0" * 64:
        print("FATAL: FROZEN_SHA is blank — tool not frozen. Refusing to run.",
              file=sys.stderr)
        sys.exit(3)
    actual = hash_self()
    if actual != FROZEN_SHA:
        print(f"FATAL: measure_intraday_veto.py sha mismatch — frozen "
              f"{FROZEN_SHA[:12]}…, on disk {actual[:12]}…. A frozen "
              f"measurement tool must not change.", file=sys.stderr)
        sys.exit(1)


# --------------------------------------------------------------------------
# §3 veto legs (pre-reg #21 §1) — both known at the close of the entry bar
# --------------------------------------------------------------------------

def _ema_series(closes: np.ndarray, span: int) -> np.ndarray:
    """Exponential moving average of closes, seeded at the first close
    (alpha = 2/(span+1)), length preserved."""
    alpha = 2.0 / (span + 1)
    out = np.empty(len(closes))
    out[0] = closes[0]
    e = closes[0]
    for i in range(1, len(closes)):
        e = alpha * closes[i] + (1 - alpha) * e
        out[i] = e
    return out


def macd_at(closes: np.ndarray, i: int) -> float | None:
    """MACD (EMA12 - EMA26) of closes[0..i] — the (bar-date, ticker) close
    series from the day's first bar through the entry bar. None when the
    EMA-26 warm-up (>= WARMUP_MACD closes) is unmet at the entry bar."""
    if i + 1 < WARMUP_MACD:
        return None
    c = closes[:i + 1]
    return float(_ema_series(c, 12)[-1] - _ema_series(c, 26)[-1])


def volume_spike(df, wpos: np.ndarray, e_abs: int, v: float) -> bool:
    """The volume leg: the entry bar's volume >= v x the file's median RTH
    bar volume AND the bar is red (Close < Open). A file with no positive
    RTH volume baseline (median <= 0) is vacuously no-spike."""
    med = float(np.median(df["Volume"].to_numpy()[wpos]))
    if med <= 0:
        return False
    op = float(df["Open"].to_numpy()[e_abs])
    cl = float(df["Close"].to_numpy()[e_abs])
    return (cl < op) and float(df["Volume"].to_numpy()[e_abs]) >= v * med


# --------------------------------------------------------------------------
# §3 measurement: Archive + families
# --------------------------------------------------------------------------

class Archive:
    """Window bar-dates loaded once; serves the entry events with their
    veto legs, the rets_for forward returns, and the per-file/per-hour
    baseline pools. Deterministic iteration (sorted rels)."""

    def __init__(self, cost: float = COST_PRIMARY, n: int = N_PRIMARY,
                 v: float = V_PRIMARY, detector: str = "reversal"):
        self.cost, self.n, self.v = cost, n, v
        self.detector = detector
        self.files = {}
        self.events = []          # entry-candidate dicts (+ veto legs)
        self.dropped_by_date = {}
        self.dropped = 0
        self._wpos_cache = {}
        self.same_pools = {}
        self.uni_pools = {}
        self._load()

    def _load(self):
        m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for rel in sorted(f for f in m.get("files", {})
                          if f.split("/")[0] >= WINDOW_START):
            df = MIE.load_day(rel)
            self.files[rel] = df
            w = self.wpos(rel)
            npos = len(w)
            date = rel.split("/")[0]
            if self.detector == "reversal":
                rv = MIE.detect_reversal(df, d=MIE.D_PRIMARY,
                                         win=None, five_min=False)
                cands = rv["long"]
                det_dropped = rv["dropped"]
            else:  # detector == "b01" (S-B01 sensitivity cross-check)
                rv = MI.detect_b01(df, n_need=self.n)
                cands = rv["events"]
                det_dropped = rv["dropped"]
            self.dropped_by_date.setdefault(date, 0)
            self.dropped_by_date[date] += det_dropped
            self.dropped += det_dropped
            ticker = rel.split("/")[1][:-len(".parquet")]
            closes = df["Close"].to_numpy()
            for ev in cands:
                ev["rel"], ev["date"], ev["ticker"] = rel, date, ticker
                ev["npos"] = npos
                ev["e_abs"] = int(w[ev["e_pos"]])
                ev["valid"] = ev["e_pos"] + 1 + self.n < npos
                ev["macd"] = macd_at(closes, ev["e_abs"])
                ev["vol_spike"] = volume_spike(df, w, ev["e_abs"], self.v)
                ev["evaluable"] = ev["macd"] is not None
                ev["macd_neg"] = ev["macd"] is not None and ev["macd"] < 0
                ev["veto_fail"] = (ev["evaluable"]
                                   and (ev["macd_neg"] or ev["vol_spike"]))
                ev["veto_pass"] = ev["evaluable"] and not ev["veto_fail"]
                self.events.append(ev)
        self._build_pools()

    def wpos(self, rel: str) -> np.ndarray:
        if rel not in self._wpos_cache:
            self._wpos_cache[rel] = MIE.wpos(self.files[rel], None)
        return self._wpos_cache[rel]

    def _build_pools(self):
        """Per-file, per-hour baseline pools (gross): a baseline bar c must
        have c+1 and c+N within the window end, in the same hour bucket as
        the candidate's entry bar, and must not itself be an entry bar
        (pre-reg #15 §4 convention)."""
        hours = list(range(MIE.RTH_OPEN.hour, MIE.RTH_END.hour))
        self.same_pools = {}
        self.uni_pools = {h: [] for h in hours}
        entry_pos = {rel: {ev["e_pos"] for ev in self.events
                           if ev["rel"] == rel} for rel in self.files}
        for rel, df in self.files.items():
            w = self.wpos(rel)
            n = len(w)
            if n <= self.n + 1:
                self.same_pools[rel] = {}
                continue
            op = df["Open"].to_numpy()[w]
            cl = df["Close"].to_numpy()[w]
            times = df.index[w]
            c = np.arange(n)[: n - self.n - 1]
            if len(c) == 0:
                self.same_pools[rel] = {}
                continue
            rets = (cl[c + self.n] - op[c + 1]) / op[c + 1]
            ep = entry_pos.get(rel, set())
            ep_arr = np.fromiter(ep, dtype=int, count=len(ep)) if ep \
                else np.array([], dtype=int)
            per_hour = {}
            for h in range(MIE.RTH_OPEN.hour, MIE.RTH_END.hour):
                hm = times[c].hour == h
                keep = hm & ~np.isin(c, ep_arr)
                if keep.any():
                    per_hour[h] = rets[keep]
            self.same_pools[rel] = per_hour
            for h, v in per_hour.items():
                self.uni_pools[h].append(v)
        self.uni_pools = {h: np.concatenate(v) if v else np.array([])
                          for h, v in self.uni_pools.items()}

    def rets_for(self, evs: list) -> np.ndarray:
        """(C[wpos[e_pos + n]] - entry_open)/entry_open - cost per event.
        Callers pass only valid events (forward window present)."""
        out = []
        for ev in evs:
            cl = self.files[ev["rel"]]["Close"].to_numpy()
            w = self.wpos(ev["rel"])
            gross = (cl[w[ev["e_pos"] + self.n]] - ev["entry_open"]) \
                / ev["entry_open"]
            out.append(gross - self.cost)
        return np.array(out)

    def sample_baseline(self, evs: list, rng, kind: str) -> np.ndarray:
        """Bootstrap baseline draw for the measurement rows: for each of M
        events, a random baseline bar in the same hour bucket (same-ticker
        pool per the event's file, or the random-universe pool)."""
        M = len(evs)
        out = np.empty(M)
        for i in range(M):
            ev = evs[rng.integers(0, M)]
            h = ev["hour"]
            pool = (self.same_pools[ev["rel"]].get(h)
                    if kind == "same" else self.uni_pools.get(h))
            if pool is None or len(pool) == 0:
                out[i] = 0.0
            else:
                out[i] = pool[rng.integers(0, len(pool))]
        return out


def run_f1(a: Archive, rng) -> dict:
    """F1 (conditioning) - 4 Holm slots; two-sample bootstrap of mean
    forward returns (pre-reg #21 §3). Count floor 100 per slot."""
    valid = [ev for ev in a.events if ev["valid"]]
    passes = [ev for ev in valid if ev["veto_pass"]]
    fails = [ev for ev in valid if ev["veto_fail"]]
    raw = [ev for ev in valid if ev["evaluable"]]
    macd_ge0 = [ev for ev in valid
                if ev["macd"] is not None and ev["macd"] >= 0]
    macd_lt0 = [ev for ev in valid
                if ev["macd"] is not None and ev["macd"] < 0]
    nosp = [ev for ev in valid if not ev["vol_spike"]]
    sp = [ev for ev in valid if ev["vol_spike"]]
    fam = {}

    def slot(key, label, evs_a, evs_b):
        if len(evs_a) < MIN_SLOT or len(evs_b) < MIN_SLOT:
            fam[key] = {"slot": label, "n": min(len(evs_a), len(evs_b)),
                        "n_a": len(evs_a), "n_b": len(evs_b),
                        "p": 1.0, "est": None, "ci_low": None,
                        "ci_upper": None, "verdict": "INCONCLUSIVE"}
            return
        ra = a.rets_for(evs_a)
        rb = a.rets_for(evs_b)
        d = MIE.contrast_two(ra, rb, rng)
        fam[key] = {"slot": label, "n": min(len(evs_a), len(evs_b)),
                    "n_a": len(evs_a), "n_b": len(evs_b),
                    "mean_a": float(ra.mean()), "mean_b": float(rb.mean()),
                    "est": d[0], "ci_low": d[2], "ci_upper": d[3],
                    "p": d[4]}

    slot("pass_minus_fail", "pass − fail", passes, fails)
    slot("pass_minus_raw", "pass − raw", passes, raw)
    slot("macd_leg", "macd leg (MACD ≥ 0 − MACD < 0)", macd_ge0, macd_lt0)
    slot("volume_leg", "volume leg (no spike − spike)", nosp, sp)
    return MIE.holm(fam, "F1")


def kill_rate_rows(a: Archive, rng) -> dict:
    """F2 kill-rate decomposition (pre-reg #21 §3, measurement rows only,
    NO verdicts): what fraction of candidates each leg alone kills, and the
    killed sets' mean forward returns vs the kept set."""
    valid = [ev for ev in a.events if ev["valid"]]
    eval_evs = [ev for ev in valid if ev["evaluable"]]
    n = len(eval_evs)
    passes = [ev for ev in eval_evs if ev["veto_pass"]]
    fails = [ev for ev in eval_evs if ev["veto_fail"]]
    macd_lt0 = [ev for ev in eval_evs if ev["macd"] < 0]
    macd_ge0 = [ev for ev in eval_evs if ev["macd"] >= 0]
    sp = [ev for ev in eval_evs if ev["vol_spike"]]
    nosp = [ev for ev in eval_evs if not ev["vol_spike"]]
    both = [ev for ev in eval_evs if ev["macd"] < 0 and ev["vol_spike"]]
    out = {
        "n": n,
        "n_unavailable_macd": sum(1 for ev in valid if not ev["evaluable"]),
        "n_veto_pass": len(passes), "pass_rate": (len(passes) / n if n else 0.0),
        "n_veto_fail": len(fails), "fail_rate": (len(fails) / n if n else 0.0),
        "n_macd_killed": len(macd_lt0),
        "macd_kill_rate": (len(macd_lt0) / n if n else 0.0),
        "n_vol_killed": len(sp),
        "vol_kill_rate": (len(sp) / n if n else 0.0),
        "n_both_killed": len(both),
        "both_kill_rate": (len(both) / n if n else 0.0)}
    if n:
        pr = a.rets_for(passes) if passes else np.array([])
        fr = a.rets_for(fails) if fails else np.array([])
        m_ge = a.rets_for(macd_ge0) if macd_ge0 else np.array([])
        m_lt = a.rets_for(macd_lt0) if macd_lt0 else np.array([])
        s_ = a.rets_for(sp) if sp else np.array([])
        ns = a.rets_for(nosp) if nosp else np.array([])
        out["means"] = {
            "pass": float(pr.mean()) if len(pr) else None,
            "fail": float(fr.mean()) if len(fr) else None,
            "diff_pass_minus_fail": (float(pr.mean() - fr.mean())
                                     if len(pr) and len(fr) else None),
            "macd_ge0": float(m_ge.mean()) if len(m_ge) else None,
            "macd_lt0": float(m_lt.mean()) if len(m_lt) else None,
            "vol_spike": float(s_.mean()) if len(s_) else None,
            "no_spike": float(ns.mean()) if len(ns) else None}
    # Hour-matched baseline excess of the kept (pass) set (rows only).
    if passes:
        e_same = MIE.bootstrap_excess(
            pr, lambda M: a.sample_baseline(passes, rng, "same"), rng)
        e_uni = MIE.bootstrap_excess(
            pr, lambda M: a.sample_baseline(passes, rng, "uni"), rng)
        out["pass_excess"] = {
            "same_ticker": {"est": e_same[0], "ci_low": e_same[2],
                            "ci_upper": e_same[3], "p": e_same[4]},
            "universe": {"est": e_uni[0], "ci_low": e_uni[2],
                         "ci_upper": e_uni[3], "p": e_uni[4]}}
    by_date = {}
    by_ticker = {}
    by_hour = {}
    for ev in eval_evs:
        by_date.setdefault(ev["date"], []).append(ev)
        by_ticker.setdefault(ev["ticker"], []).append(ev)
        by_hour.setdefault(ev["hour"], []).append(ev)
    out["by_bar_date"] = {d: {"n": len(ix), "pass_rate": float(
        np.mean([e["veto_pass"] for e in ix]))}
        for d, ix in sorted(by_date.items())}
    out["by_ticker"] = {t: {"n": len(ix), "pass_rate": float(
        np.mean([e["veto_pass"] for e in ix]))}
        for t, ix in sorted(by_ticker.items())}
    out["by_hour"] = {h: {"n": len(ix), "pass_rate": float(
        np.mean([e["veto_pass"] for e in ix]))}
        for h, ix in sorted(by_hour.items())}
    return out


def run_sensitivities() -> dict:
    """Pre-declared sensitivities (NO verdicts): volume threshold, cost,
    horizon, and the B-01 entry-set cross-check."""
    out = {}
    for i, (key, cost, n, v, detector) in enumerate((
            ("S-V2", COST_PRIMARY, N_PRIMARY, 2.0, "reversal"),
            ("S-V5", COST_PRIMARY, N_PRIMARY, 5.0, "reversal"),
            ("S-C05", COST_PRIMARY / 3, N_PRIMARY, V_PRIMARY, "reversal"),
            ("S-C30", COST_PRIMARY * 2, N_PRIMARY, V_PRIMARY, "reversal"),
            ("S-N15", COST_PRIMARY, 15, V_PRIMARY, "reversal"),
            ("S-N120", COST_PRIMARY, 120, V_PRIMARY, "reversal"),
            ("S-N240", COST_PRIMARY, 240, V_PRIMARY, "reversal"),
            ("S-B01", COST_PRIMARY, N_PRIMARY, V_PRIMARY, "b01"))):
        arc = Archive(cost=cost, n=n, v=v, detector=detector)
        rng = np.random.default_rng(SEED + 1 + i)
        f1 = run_f1(arc, rng)
        out[key] = {"f1_family": f1.get("_family"),
                    "slots": {k: {"slot": r.get("slot"), "n": r.get("n"),
                                  "est": r.get("est"), "p": r.get("p"),
                                  "verdict": r.get("verdict")}
                              for k, r in f1.items() if k != "_family"}}
    return out


def check_floors(a: Archive) -> dict:
    """§4 sample-size floors. F1-evaluable = entry candidates with the
    fixed-N forward window."""
    dates = sorted({rel.split("/")[0] for rel in a.files})
    valid = [ev for ev in a.events if ev["valid"]]
    floors = {
        "window_bar_dates": len(dates),
        "events_f1_valid": len(valid),
        "tickers": len({ev["ticker"] for ev in valid}),
        "dates_with_events": len({ev["date"] for ev in valid})}
    floors["met"] = (floors["window_bar_dates"] >= FLOORS["min_bar_dates"]
                     and floors["events_f1_valid"] >= FLOORS["min_events"]
                     and floors["tickers"] >= FLOORS["min_tickers"]
                     and floors["dates_with_events"]
                     >= FLOORS["min_dates_with_events"])
    return floors


def _fmt(x, nd=4):
    if x is None or (isinstance(x, float) and x != x):
        return "—"
    return f"{x:.{nd}f}"


def write_report(audit: dict, arc: Archive, floors: dict | None,
                 measure: dict | None, audit_only: bool) -> str:
    L = []
    L.append("# Pre-registration #21 measurement — the two-filter veto")
    L.append("")
    L.append(f"- tool sha (raw): `{sha_bytes(Path(__file__).read_bytes())}`")
    L.append(f"- tool FROZEN_SHA (fixed point): `{FROZEN_SHA}`")
    L.append(f"- frozen input `tools/measure_intraday_entry.py` sha256 "
             f"(LF-normalized): `{_lf_sha(MIE)}`")
    L.append(f"- frozen input `tools/measure_intraday.py` sha256 "
             f"(LF-normalized): `{_lf_sha(MI)}`")
    L.append(f"- window: bar-dates >= {WINDOW_START}")
    L.append("")
    L.append("## Archive-integrity audit (§5/§6)")
    L.append("")
    L.append(f"- **PASSED**" if audit["passed"] else f"- **FAILED**")
    if audit["errors"]:
        L.append("- errors:")
        for e in audit["errors"]:
            L.append(f"  - {e}")
    L.append(f"- pulls checked: {audit['n_pulls']}; ledger files: "
             f"{audit['n_files_ledger']}")
    if audit["repairs"]:
        L.append(f"- repairs on record: {len(audit['repairs'])}")
        for r in audit["repairs"]:
            L.append(f"  - {r['path']}: {r['reason']}")
    if audit["window_pulls"]:
        L.append("- window pulls:")
        L.append("  | pull_id | universe | requested | ok | failed |")
        L.append("  |---|---|---|---|---|")
        for p in audit["window_pulls"]:
            L.append(f"  | {p['pull_id']} | {p['universe_file']} | "
                     f"{p['tickers_requested']} | {p['tickers_ok']} | "
                     f"{p['tickers_failed']} |")
    if audit_only:
        L.append("")
        L.append("## Entry-set detection (audit-only; no returns computed)")
        L.append("")
        L.append(f"detector: {arc.detector} — veto legs computed (MACD, "
                 f"volume) as detection metadata; NO forward returns")
        L.append("")
        L.append("| bar-date | entries | dropped | F1-evaluable |")
        L.append("|---|---|---|---|")
        per_date = {}
        ev_by = {}
        for ev in arc.events:
            per_date.setdefault(ev["date"], 0)
            per_date[ev["date"]] += 1
            if ev["valid"]:
                ev_by.setdefault(ev["date"], 0)
                ev_by[ev["date"]] += 1
        for d in sorted(per_date):
            L.append(f"| {d} | {per_date.get(d, 0)} | "
                     f"{arc.dropped_by_date.get(d, 0)} | "
                     f"{ev_by.get(d, 0)} |")
        return "\n".join(L) + "\n"
    L.append("")
    L.append(f"## Sample-size floors (§4)")
    L.append("")
    L.append("| floor | required | actual | met |")
    L.append("|---|---|---|---|")
    for k, req in FLOORS.items():
        L.append(f"| {k} | {req} | {floors[k]} | "
                 f"{'✓' if floors[k] >= req else '✗'} |")
    L.append("")
    L.append("## F1 — conditioning (4 Holm slots)")
    L.append("")
    L.append("Family verdict: **" + measure["f1"]["_family"] + "**")
    L.append("")
    L.append("| slot | n (a/b) | mean a | mean b | diff (a − b) | CI 95% | "
             "p | Holm gate | rej | verdict |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for k, r in measure["f1"].items():
        if k == "_family":
            continue
        L.append(f"| {r['slot']} | {r['n']} ({r['n_a']}/{r['n_b']}) | "
                 f"{_fmt(r.get('mean_a'))} | {_fmt(r.get('mean_b'))} | "
                 f"{_fmt(r.get('est'))} | "
                 f"{_fmt(r.get('ci_low'))} … {_fmt(r.get('ci_upper'))} | "
                 f"{_fmt(r.get('p'), 3)} | {_fmt(r.get('holm_gate'), 3)} | "
                 f"{'✓' if r.get('holm_rejected') else '—'} | "
                 f"{r.get('verdict')} |")
    L.append("")
    L.append("## F2 — kill-rate decomposition (rows, NO verdicts)")
    L.append("")
    r2 = measure["rows"]
    L.append(f"- classifiable entries: {r2['n']} (MACD warm-up unmet: "
             f"{r2['n_unavailable_macd']})")
    L.append(f"- veto-pass: {r2['n_veto_pass']} "
             f"({r2['pass_rate']:.4f})  ·  veto-fail: {r2['n_veto_fail']} "
             f"({r2['fail_rate']:.4f})")
    L.append(f"- MACD leg kills: {r2['n_macd_killed']} "
             f"({r2['macd_kill_rate']:.4f})  ·  volume leg kills: "
             f"{r2['n_vol_killed']} ({r2['vol_kill_rate']:.4f})  ·  both: "
             f"{r2['n_both_killed']} ({r2['both_kill_rate']:.4f})")
    if "means" in r2:
        m = r2["means"]
        L.append(f"- mean forward — pass: {_fmt(m.get('pass'))}, "
                 f"fail: {_fmt(m.get('fail'))}, diff (pass−fail): "
                 f"{_fmt(m.get('diff_pass_minus_fail'))}")
        L.append(f"- mean forward — MACD ≥ 0: {_fmt(m.get('macd_ge0'))}, "
                 f"MACD < 0: {_fmt(m.get('macd_lt0'))}, vol spike: "
                 f"{_fmt(m.get('vol_spike'))}, no spike: "
                 f"{_fmt(m.get('no_spike'))}")
    if "pass_excess" in r2:
        pe = r2["pass_excess"]
        L.append(f"- pass set excess vs hour-matched baseline — same-ticker: "
                 f"{_fmt(pe['same_ticker']['est'])} (CI "
                 f"{_fmt(pe['same_ticker']['ci_low'])} … "
                 f"{_fmt(pe['same_ticker']['ci_upper'])}), universe: "
                 f"{_fmt(pe['universe']['est'])} (CI "
                 f"{_fmt(pe['universe']['ci_low'])} … "
                 f"{_fmt(pe['universe']['ci_upper'])}))")
    L.append("")
    L.append("### By bar-date")
    L.append("")
    L.append("| date | n | pass rate |")
    L.append("|---|---|---|")
    for d, r in r2["by_bar_date"].items():
        L.append(f"| {d} | {r['n']} | {r['pass_rate']:.4f} |")
    L.append("")
    L.append("## Sensitivities (pre-declared, NO verdicts)")
    L.append("")
    for key, s in measure["sensitivities"].items():
        parts = []
        for k, v in s["slots"].items():
            parts.append(f"{v['slot']} n={v['n']} "
                         f"est={_fmt(v.get('est'))} p={_fmt(v.get('p'), 3)} "
                         f"{v.get('verdict', '')}".strip())
        L.append(f"- {key}: F1 family {s['f1_family']} — " +
                 "; ".join(parts))
    L.append("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-only", action="store_true",
                    help="§5 audit + entry counts only, no returns")
    args = ap.parse_args()
    self_check()
    audit = MIE.audit_archive()
    if args.audit_only:
        arc = Archive()
        report = write_report(audit, arc, None, None, True)
        print(report)
        print("AUDIT_EXIT=" + ("0" if audit["passed"] else "1"))
        sys.exit(0 if audit["passed"] else 1)
    arc = Archive()
    floors = check_floors(arc)
    if not floors["met"]:
        print("FATAL: §5 sample-size floors not met. Refusing measurement.",
              file=sys.stderr)
        _req_of = {"window_bar_dates": "min_bar_dates",
                   "events_f1_valid": "min_events",
                   "tickers": "min_tickers",
                   "dates_with_events": "min_dates_with_events"}
        for k, v in floors.items():
            if k == "met":
                continue
            print(f"  {k}: {v} (need {FLOORS[_req_of[k]]})", file=sys.stderr)
        sys.exit(2)
    rng = np.random.default_rng(SEED)
    f1 = run_f1(arc, rng)
    rows = kill_rate_rows(arc, rng)
    sens = run_sensitivities()
    measure = {"f1": f1, "rows": rows, "sensitivities": sens}
    report = write_report(audit, arc, floors, measure, False)
    REPORT_PATH.write_text(report, encoding="utf-8")
    results = {
        "frozen_sha": FROZEN_SHA,
        "measure_code_sha256": sha_bytes(Path(__file__).read_bytes()),
        "input_entry_sha256": _FROZEN_INPUT_ENTRY_SHA256,
        "input_b01_sha256": _FROZEN_INPUT_B01_SHA256,
        "seed": SEED, "bootstrap": B, "alpha": ALPHA,
        "floors": floors,
        "f1": {k: v for k, v in f1.items() if k != "_family"},
        "f1_family": f1["_family"],
        "rows": rows,
        "sensitivities": sens,
        "audit_passed": audit["passed"]}
    RESULTS_PATH.write_text(
        json.dumps(results, indent=1, sort_keys=True), encoding="utf-8")
    print(f"wrote {REPORT_PATH}")
    print(f"report sha256: {sha_file(REPORT_PATH)}")
    print(f"wrote {RESULTS_PATH}")
    print(f"results sha256: {sha_file(RESULTS_PATH)}")
    print("F1:", f1["_family"])
    sys.exit(0)


if __name__ == "__main__":
    main()
