"""Pre-registration #22 measurement tool — the intraday regime: the
morning-is-best window (ledger rows F-01, I-B-05) and pre-market cleanliness
(F-02) on 1-minute bars.

Implements PREREGISTRATION.md §Pre-registration #22 exactly:
  * §1 the buckets: B1 = 07:00-10:00 ET (F-01 peak volatility/liquidity),
    B2 = 09:30-12:00 ET (I-B-05 money window), and the pre-market 04:00-09:30
    vs RTH 09:30-16:00 split (F-02);
  * §3 the measurement:
      F1 — 2 Holm slots (B1, B2). For each bucket, the contrast = the
        bucket's mean metric minus the MAXIMUM of the other buckets' means
        (the canonical buckets that do not overlap the tested bucket),
        bootstrapped against the runner-up bucket (the single highest other
        bucket's point mean, held fixed at its point value). Two statistics
        per slot: volatility (mean |r| per bar) and liquidity (volume
        share). Verdict applies to the jointly-measured pair: EDGE iff the
        bucket leads on BOTH with CI-low > 0; FADE iff it trails on BOTH
        with CI-upper < 0; NO EDGE otherwise. Floor: 100 bar-dates with >= 10
        names in the bucket.
      F2 (1 Holm slot): mean forward return of the pre-reg #19 F1
        reversal-long entry when the entry bar is in B2 minus the mean when
        outside B2 (same entry set; hour-matched same-ticker and
        random-universe baseline excesses reported as secondary rows). EDGE
        iff CI-low > 0; FADE iff CI-upper < 0. Floor 100 per leg.
      F3 (1 Holm slot — pre-market cleanliness): pre-market (04:00-09:30)
        per-bar mean |r| minus RTH (09:30-16:00) per-bar mean |r| (primary),
        plus the tail-frequency contrast (|r| > 3x the file's window median
        |r|; secondary). EDGE iff BOTH contrasts negative with CI-upper < 0
        (pre-market cleaner on both); FADE iff CI-low > 0 on both.
      Measurement rows (NO verdicts): the pre-reg #15 F-01/F-02 descriptive
        rows kept for continuity (time_of_day, pre_vs_rth), the 09:30-10:30
        single-hour variant, the 09:30-09:35 first-5-minutes row, per-hour
        profiles, and the per-bar-date / per-ticker leader rows.
  * §4 the sample-size floors and the one-shot rule (measurement REFUSED
    until the floors are met; audit-only mode computes no returns).
  * §5 the archive-integrity audit (shared with pre-reg #15).

Frozen 2026-08-21, before any measurement. The module sha is asserted at
run (FROZEN_SHA below, the fixed-point convention; measure_code_sha256
records the raw file sha): any byte change invalidates the campaign. The
frozen-input tools are asserted at import at their LF-normalized sha256
(committed blobs, checkout-independent):
  tools/measure_intraday_entry.py = the pre-reg #19 F1 entry set (F2) and
                                    the shared audit/detection functions
  tools/measure_intraday.py       = the pre-reg #15 continuity-rows reference

Modes:
  python -X utf8 tools/measure_intraday_regime.py --audit-only
      §5 audit + entry detection counts + bucket coverage only. Computes NO
      return of any kind. Exit 0 = audit clean; 1 = audit FAILED.
  python -X utf8 tools/measure_intraday_regime.py
      Full measurement. Requires the §5 floors; otherwise REFUSES (exit
      2). Writes data/cache/intraday_regime_measure_report.md +
      intraday_regime_measure_results.json, prints their sha256 for the
      determinism check (two runs must byte-compare).

Exit codes: 0 ok, 1 audit/integrity failure, 2 floors unmet (refused),
3 input error.

Spec mapping (pre-reg #22 §1/§3):
  The canonical day partition is the pre-reg #15 10-bucket time-of-day set
  (04:00-07:00, 07:00-09:30, 09:30-10:00, 10:00-11:00, 11:00-12:00,
  12:00-13:00, 13:00-14:00, 14:00-15:00, 15:00-16:00, 16:00-20:00 ET), kept
  for continuity. B1 covers buckets 1-2 (07:00-10:00); B2 covers 2-4
  (09:30-12:00). The pre-market/RTH split (04:00-09:30 vs 09:30-16:00) is
  the #15 pre_vs_rth pair. All comparisons are over 1-minute bars of the
  window bar-dates; the volume-share denominator is the window's total bar
  volume. Bootstrap B = 1000, seed 20260821, Holm alpha 0.05.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import time as dtime
from pathlib import Path

import numpy as np

import measure_intraday_entry as MIE
import measure_intraday as MI

ROOT = Path(__file__).resolve().parent.parent
INTRA = ROOT / "data" / "intraday"
MANIFEST_PATH = INTRA / "manifest.json"
OUT_DIR = ROOT / "data" / "cache"
REPORT_PATH = OUT_DIR / "intraday_regime_measure_report.md"
RESULTS_PATH = OUT_DIR / "intraday_regime_measure_results.json"

WINDOW_START = "2026-08-19"

# ---- frozen-input assertions (pre-reg #22 §1/§2) ----
# The entry set for F2 is the frozen pre-reg #19 reversal-new-high detector
# in tools/measure_intraday_entry.py; its LF-normalized sha256 (the committed
# blob, checkout-independent) is asserted here. tools/measure_intraday.py is
# the frozen pre-reg #15 tool whose time_of_day / pre_vs_rth rows the
# measurement keeps for continuity; asserted here as the frozen reference.
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

# ---- frozen parameters (pre-reg #22 §1/§3) ----
N_PRIMARY = 60               # F2 forward horizon (bars)
COST_PRIMARY = 0.0015        # F2 round-trip cost
B = 1000
SEED = 20260821              # freeze date
ALPHA = 0.05
FLOORS = {"min_bar_dates": 20, "min_events": 2000,
          "min_tickers": 100, "min_dates_with_events": 15}
MIN_SLOT = 100           # per-slot/leg count floor (house)
MIN_BUCKET_DATES = 100   # F1: bucket bar-dates with >= 10 names
MIN_NAMES_PER_DATE = 10  # F1 coverage floor per bar-date
TAIL_MULT = 3.0          # F3 tail: |r| > 3x the file's window median |r|

# The canonical day partition (pre-reg #15 time_of_day, kept for continuity).
CANON = [
    (dtime(4, 0), dtime(7, 0)),
    (dtime(7, 0), dtime(9, 30)),
    (dtime(9, 30), dtime(10, 0)),
    (dtime(10, 0), dtime(11, 0)),
    (dtime(11, 0), dtime(12, 0)),
    (dtime(12, 0), dtime(13, 0)),
    (dtime(13, 0), dtime(14, 0)),
    (dtime(14, 0), dtime(15, 0)),
    (dtime(15, 0), dtime(16, 0)),
    (dtime(16, 0), dtime(20, 0)),
]
BUCKET_LABELS = ["04:00-07:00", "07:00-09:30", "09:30-10:00",
                 "10:00-11:00", "11:00-12:00", "12:00-13:00",
                 "13:00-14:00", "14:00-15:00", "15:00-16:00",
                 "16:00-20:00"]
# F1 tested buckets: label, interval, the canonical buckets they cover.
F1_SLOTS = [
    {"key": "B1", "label": "B1 (07:00-10:00)", "t0": dtime(7, 0),
     "t1": dtime(10, 0), "cover_idx": [1, 2]},
    {"key": "B2", "label": "B2 (09:30-12:00)", "t0": dtime(9, 30),
     "t1": dtime(12, 0), "cover_idx": [2, 3, 4]},
]
PRE = (dtime(4, 0), dtime(9, 30))
RTH = (dtime(9, 30), dtime(16, 0))

# Freeze sha (house convention, measure_intraday.py/measure_cexit.py): the
# sha of this file with its own FROZEN_SHA hex blanked to 64 zeros — a
# well-defined fixed point. Any byte change outside the blanked hex breaks
# the assertion.
FROZEN_SHA = "b1fe067d8bac111c4532cfc838bb6d210f13a906defc0db8a083bd228a1095c0"


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
        print(f"FATAL: measure_intraday_regime.py sha mismatch — frozen "
              f"{FROZEN_SHA[:12]}…, on disk {actual[:12]}…. A frozen "
              f"measurement tool must not change.", file=sys.stderr)
        sys.exit(1)


# --------------------------------------------------------------------------
# §3 bootstrap contrast
# --------------------------------------------------------------------------

def boot_two(x: np.ndarray, y: np.ndarray, rng, stat) -> tuple:
    """Two-sample bootstrap of stat(pool_x) - stat(pool_y): B draws, each
    resampled at its own size, percentile 2.5/97.5 CI, two-sided p. The
    statistic is the sample mean (per-bar |r|, tail fraction) or the volume
    share (stat = lambda s: s.sum() / denom). Returns (est, lo, hi, p)."""
    Mx, My = len(x), len(y)
    if Mx == 0 or My == 0:
        raise ValueError("boot_two: empty pool — callers must guard with "
                         "the count floor")
    diffs = np.empty(B)
    for b in range(B):
        diffs[b] = (stat(x[rng.integers(0, Mx, size=Mx)])
                    - stat(y[rng.integers(0, My, size=My)]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(lo), float(hi), float(p))


# --------------------------------------------------------------------------
# §3 measurement: Archive + families
# --------------------------------------------------------------------------

class Archive:
    """Window bar-dates loaded once; serves the F2 entry events (pre-reg #19
    F1 reversal-long), the canonical per-bucket pools, the F3 window pools,
    and the per-hour baseline pools. Deterministic iteration (sorted rels)."""

    def __init__(self, n: int = N_PRIMARY, cost: float = COST_PRIMARY):
        self.n, self.cost = n, cost
        self.files = {}
        self.entries = []          # reversal-long entry dicts (+ rel/ticker)
        self.dropped_by_date = {}
        self.dropped = 0
        self._wpos_cache = {}
        self.same_pools = {}
        self.uni_pools = {}
        self._load()
        self._canon = None
        self._canon_total_vol = None
        self._f3 = None

    def _load(self):
        m = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for rel in sorted(f for f in m.get("files", {})
                          if f.split("/")[0] >= WINDOW_START):
            df = MIE.load_day(rel)
            self.files[rel] = df
            w = self.wpos(rel)
            npos = len(w)
            rv = MIE.detect_reversal(df, d=MIE.D_PRIMARY,
                                     win=None, five_min=False)
            cands = rv["long"]
            date = rel.split("/")[0]
            self.dropped_by_date[date] = (self.dropped_by_date.get(date, 0)
                                          + rv["dropped"])
            self.dropped += rv["dropped"]
            ticker = rel.split("/")[1][:-len(".parquet")]
            for ev in cands:
                ev["rel"], ev["date"], ev["ticker"] = rel, date, ticker
                ev["npos"] = npos
                ev["e_abs"] = int(w[ev["e_pos"]])
                ev["valid"] = ev["e_pos"] + 1 + self.n < npos
                t = df.index[ev["e_abs"]].time()
                ev["min"] = t.hour * 60 + t.minute
                ev["hour"] = t.hour
                self.entries.append(ev)
        self._build_pools()

    def wpos(self, rel: str) -> np.ndarray:
        if rel not in self._wpos_cache:
            self._wpos_cache[rel] = MIE.wpos(self.files[rel], None)
        return self._wpos_cache[rel]

    def _build_pools(self):
        """Per-file, per-hour baseline pools (gross, long convention): a
        baseline bar c must have c+1 and c+N within the window end, in the
        same hour bucket as the candidate's entry bar, and must not itself
        be an entry bar (pre-reg #15 §4 convention)."""
        hours = list(range(MIE.RTH_OPEN.hour, MIE.RTH_END.hour))
        self.same_pools = {}
        self.uni_pools = {h: [] for h in hours}
        entry_pos = {rel: {ev["e_pos"] for ev in self.entries
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

    # -- bucket pools --------------------------------------------------------

    def _bucket_pool(self, t0, t1) -> dict:
        """Per-file-window aggregation for [t0,t1): per-bar |r| (diff within
        each file's window, the pre-#15 convention), per-bar volume, and the
        bar-date name coverage (dates with >= MIN_NAMES_PER_DATE names)."""
        abs_parts, vol_parts = [], []
        names = {}
        for rel, df in self.files.items():
            t = df.index.time
            m = np.array([(x >= t0) and (x < t1) for x in t])
            x = df[m]
            if len(x) == 0:
                continue
            date = rel.split("/")[0]
            names.setdefault(date, set()).add(
                rel.split("/")[1][:-len(".parquet")])
            c = x["Close"].to_numpy()
            r = np.abs(np.diff(c) / c[:-1])
            if len(r):
                abs_parts.append(r)
            vol_parts.append(x["Volume"].to_numpy())
        abs_r = np.concatenate(abs_parts) if abs_parts else np.array([])
        vol = np.concatenate(vol_parts) if vol_parts else np.array([])
        return {
            "abs_r": abs_r, "vol": vol, "n_vol": int(len(vol)),
            "vol_sum": float(vol.sum()) if len(vol) else 0.0,
            "n_dates_ge10": int(sum(1 for s in names.values()
                                    if len(s) >= MIN_NAMES_PER_DATE))}

    def canon(self) -> list:
        """Per-canonical-bucket pools + the window's total bar volume."""
        if self._canon is None:
            self._canon = [self._bucket_pool(t0, t1) for (t0, t1) in CANON]
            self._canon_total_vol = float(sum(
                df["Volume"].sum() for df in self.files.values()))
        return self._canon

    def total_volume(self) -> float:
        self.canon()
        return self._canon_total_vol

    def window_stats(self, t0, t1) -> dict:
        """Pre-#15 continuity stats for a window (per-file window medians for
        the tail flags): the pools (abs_r, tails) + bar count."""
        abs_parts, tail_parts, n_bars = [], [], 0
        for df in self.files.values():
            t = df.index.time
            m = np.array([(x >= t0) and (x < t1) for x in t])
            x = df[m]
            c = x["Close"].to_numpy()
            r = np.abs(np.diff(c) / c[:-1])
            if len(r) == 0:
                continue
            med = float(np.median(r))
            abs_parts.append(r)
            tail_parts.append((r > TAIL_MULT * med).astype(float))
            n_bars += int(len(r))
        if not abs_parts:
            return {"abs_r": np.array([]), "tails": np.array([]),
                    "n_bars": 0}
        return {"abs_r": np.concatenate(abs_parts),
                "tails": np.concatenate(tail_parts),
                "n_bars": n_bars}

    def _leader_maps(self):
        """(bar-date, ticker) -> {bucket_idx: {mean_abs_r, vol_sum}} for the
        per-bar-date and per-ticker leader rows."""
        by_date = {}
        by_ticker = {}
        for rel, df in self.files.items():
            date, ticker = rel.split("/")
            ticker = ticker[:-len(".parquet")]
            t = df.index.time
            for i, (t0, t1) in enumerate(CANON):
                m = np.array([(x >= t0) and (x < t1) for x in t])
                x = df[m]
                if len(x) == 0:
                    continue
                c = x["Close"].to_numpy()
                r = np.abs(np.diff(c) / c[:-1])
                cell_d = by_date.setdefault(date, {}).setdefault(
                    i, {"abs_parts": [], "vol": 0.0})
                cell_t = by_ticker.setdefault(ticker, {}).setdefault(
                    i, {"abs_parts": [], "vol": 0.0})
                if len(r):
                    cell_d["abs_parts"].append(r)
                    cell_t["abs_parts"].append(r)
                cell_d["vol"] += float(x["Volume"].sum())
                cell_t["vol"] += float(x["Volume"].sum())

        def agg(maps):
            out = {}
            for key, b in maps.items():
                out[key] = {i: {
                    "mean_abs_r": (float(np.concatenate(cell["abs_parts"]).mean())
                                   if cell["abs_parts"] else None),
                    "vol_sum": cell["vol"]}
                    for i, cell in b.items()}
            return out
        return agg(by_date), agg(by_ticker)

    def leader_rows(self) -> dict:
        by_date, by_ticker = self._leader_maps()
        out = {}
        for key, maps in (("by_bar_date", by_date), ("by_ticker", by_ticker)):
            n = 0
            b1_v = b1_l = b2_v = b2_l = 0
            for b in maps.values():
                n += 1
                iv = max((i for i in b if b[i]["mean_abs_r"] is not None),
                         key=lambda i: b[i]["mean_abs_r"], default=None)
                il = max((i for i in b), key=lambda i: b[i]["vol_sum"],
                         default=None)
                if iv is not None:
                    if iv in F1_SLOTS[0]["cover_idx"]:
                        b1_v += 1
                    if iv in F1_SLOTS[1]["cover_idx"]:
                        b2_v += 1
                if il is not None:
                    if il in F1_SLOTS[0]["cover_idx"]:
                        b1_l += 1
                    if il in F1_SLOTS[1]["cover_idx"]:
                        b2_l += 1
            out[key] = {"n": n,
                        "B1_lead_vol": b1_v / n if n else None,
                        "B1_lead_liq": b1_l / n if n else None,
                        "B2_lead_vol": b2_v / n if n else None,
                        "B2_lead_liq": b2_l / n if n else None}
        return out


def run_f1(a: Archive, rng) -> dict:
    """F1 (morning volatility/liquidity peak) — 2 Holm slots (B1, B2).
    Each slot = two contrasts (volatility mean |r|, liquidity volume share),
    each vs the maximum of the other buckets' point means (the runner-up
    canonical bucket, held fixed). Verdict applies to the jointly-measured
    pair."""
    canon = a.canon()
    tot = a.total_volume()
    fam = {}
    for slot in F1_SLOTS:
        cover = set(slot["cover_idx"])
        others = [i for i in range(len(CANON)) if i not in cover]
        pool_r = np.concatenate([canon[i]["abs_r"] for i in slot["cover_idx"]])
        pool_v = np.concatenate([canon[i]["vol"] for i in slot["cover_idx"]])
        # The maximum of the other buckets' point means, held fixed.
        i_v_max = max(others, key=lambda i: (canon[i]["abs_r"].mean()
                                             if len(canon[i]["abs_r"])
                                             else -1.0))
        i_l_max = max(others, key=lambda i: (canon[i]["vol_sum"] / tot
                                             if canon[i]["vol_sum"] else -1.0))
        vol = boot_two(pool_r, canon[i_v_max]["abs_r"], rng, np.mean)
        liq = boot_two(pool_v, canon[i_l_max]["vol"], rng,
                       lambda s: s.sum() / tot)
        coverage = max(canon[i]["n_dates_ge10"] for i in slot["cover_idx"])
        floor_ok = (coverage >= MIN_BUCKET_DATES
                    and len(pool_r) >= MIN_SLOT and len(pool_v) >= MIN_SLOT
                    and len(canon[i_v_max]["abs_r"]) >= MIN_SLOT
                    and len(canon[i_l_max]["vol"]) >= MIN_SLOT)
        fam[slot["key"]] = {
            "slot": slot["label"],
            "runner_vol_bucket": BUCKET_LABELS[i_v_max],
            "runner_liq_bucket": BUCKET_LABELS[i_l_max],
            "n_abs_r": int(len(pool_r)), "n_vol": int(len(pool_v)),
            "n_runner_vol": int(len(canon[i_v_max]["abs_r"])),
            "n_runner_liq": int(len(canon[i_l_max]["vol"])),
            "coverage_dates_ge10": int(coverage),
            "vol": {"est": vol[0], "ci_low": vol[1], "ci_upper": vol[2],
                    "p": vol[3],
                    "mean": float(pool_r.mean()), "mean_r": float(
                        canon[i_v_max]["abs_r"].mean())},
            "liq": {"est": liq[0], "ci_low": liq[1], "ci_upper": liq[2],
                    "p": liq[3],
                    "mean": float(pool_v.sum() / tot),
                    "mean_r": float(canon[i_l_max]["vol_sum"] / tot)},
            "p": max(vol[3], liq[3]),
            "floor_met": floor_ok}
    return _holm(fam, "F1", _f1_verdict)


def _f1_verdict(slot: dict) -> str:
    if not slot["floor_met"]:
        return "INCONCLUSIVE"
    if not slot["holm_rejected"]:
        return "NO EDGE"
    if slot["vol"]["ci_low"] > 0 and slot["liq"]["ci_low"] > 0:
        return "EDGE"
    if slot["vol"]["ci_upper"] < 0 and slot["liq"]["ci_upper"] < 0:
        return "FADE"
    return "NO EDGE"


def run_f2(a: Archive, rng) -> dict:
    """F2 (the money claim) — 1 Holm slot: mean forward return of the
    pre-reg #19 F1 reversal-long entry in B2 (09:30-12:00) minus the mean
    outside B2."""
    long = [ev for ev in a.entries if ev["valid"]]
    b2 = [ev for ev in long if 570 <= ev["min"] < 720]
    out = [ev for ev in long if not (570 <= ev["min"] < 720)]
    ra = a.rets_for(b2) if b2 else np.array([])
    rb = a.rets_for(out) if out else np.array([])
    floor_met = len(b2) >= MIN_SLOT and len(out) >= MIN_SLOT
    if not floor_met:
        slot = {"slot": "B2 09:30-12:00 vs outside",
                "n_a": len(b2), "n_b": len(out),
                "p": 1.0, "est": None, "ci_low": None, "ci_upper": None,
                "floor_met": False}
    else:
        d = boot_two(ra, rb, rng, np.mean)
        slot = {"slot": "B2 09:30-12:00 vs outside",
                "n_a": len(b2), "n_b": len(out),
                "mean_a": float(ra.mean()), "mean_b": float(rb.mean()),
                "est": d[0], "ci_low": d[1], "ci_upper": d[2], "p": d[3],
                "floor_met": True}
        # Secondary rows: hour-matched baseline excess of the B2 set.
        e_same = MIE.bootstrap_excess(
            ra, lambda M: a.sample_baseline(b2, rng, "same"), rng)
        e_uni = MIE.bootstrap_excess(
            ra, lambda M: a.sample_baseline(b2, rng, "uni"), rng)
        slot["excess_same"] = {"est": e_same[0], "ci_low": e_same[2],
                               "ci_upper": e_same[3], "p": e_same[4]}
        slot["excess_uni"] = {"est": e_uni[0], "ci_low": e_uni[2],
                              "ci_upper": e_uni[3], "p": e_uni[4]}
    return _holm({"F2": slot}, "F2", _pos_verdict)


def _pos_verdict(slot: dict) -> str:
    if not slot["floor_met"]:
        return "INCONCLUSIVE"
    if not slot["holm_rejected"]:
        return "NO EDGE"
    if slot["ci_low"] > 0:
        return "EDGE"
    if slot["ci_upper"] < 0:
        return "FADE"
    return "NO EDGE"


def run_f3(a: Archive, rng) -> dict:
    """F3 (pre-market cleanliness) — 1 Holm slot: pre-market (04:00-09:30)
    per-bar |r| minus RTH (09:30-16:00), plus the tail-frequency contrast.
    EDGE iff BOTH contrasts negative with CI-upper < 0."""
    pre = a.window_stats(*PRE)
    rth = a.window_stats(*RTH)
    floor_met = pre["n_bars"] >= MIN_SLOT and rth["n_bars"] >= MIN_SLOT
    if not floor_met:
        slot = {"slot": "pre-market 04:00-09:30 vs RTH 09:30-16:00",
                "n_pre": pre["n_bars"], "n_rth": rth["n_bars"],
                "p": 1.0, "est": None, "ci_low": None, "ci_upper": None,
                "vol": None, "tail": None, "floor_met": False}
    else:
        v = boot_two(pre["abs_r"], rth["abs_r"], rng, np.mean)
        t = boot_two(pre["tails"], rth["tails"], rng, np.mean)
        slot = {"slot": "pre-market 04:00-09:30 vs RTH 09:30-16:00",
                "n_pre": pre["n_bars"], "n_rth": rth["n_bars"],
                "vol": {"est": v[0], "ci_low": v[1], "ci_upper": v[2],
                        "p": v[3],
                        "mean_pre": float(pre["abs_r"].mean()),
                        "mean_rth": float(rth["abs_r"].mean())},
                "tail": {"est": t[0], "ci_low": t[1], "ci_upper": t[2],
                         "p": t[3],
                         "frac_pre": float(pre["tails"].mean()),
                         "frac_rth": float(rth["tails"].mean())},
                "p": max(v[3], t[3]),
                "floor_met": True}
    return _holm({"F3": slot}, "F3", _f3_verdict)


def _f3_verdict(slot: dict) -> str:
    if not slot["floor_met"]:
        return "INCONCLUSIVE"
    if not slot["holm_rejected"]:
        return "NO EDGE"
    if slot["vol"]["ci_upper"] < 0 and slot["tail"]["ci_upper"] < 0:
        return "EDGE"
    if slot["vol"]["ci_low"] > 0 and slot["tail"]["ci_low"] > 0:
        return "FADE"
    return "NO EDGE"


def _holm(fam: dict, family: str, verdict_fn) -> dict:
    """Holm-Bonferroni across the family's slots. Each slot's ``p`` is its
    Holm key; the verdict comes from verdict_fn (the slot's joint rule).
    Family verdict: EDGE if every slot is EDGE, FADE if every slot is FADE,
    INCONCLUSIVE if any is INCONCLUSIVE, else NO EDGE."""
    order = sorted(fam, key=lambda k: fam[k].get("p", 1.0))
    for rank, k in enumerate(order, start=1):
        gate = ALPHA / (len(order) - rank + 1)
        fam[k]["holm_gate"] = gate
        fam[k]["holm_rejected"] = fam[k].get("p", 1.0) <= gate
    for k, r in fam.items():
        r["verdict"] = verdict_fn(r)
    vs = [fam[k]["verdict"] for k in fam]
    if all(v == "EDGE" for v in vs):
        fam["_family"] = "EDGE"
    elif all(v == "FADE" for v in vs):
        fam["_family"] = "FADE"
    elif any(v == "INCONCLUSIVE" for v in vs):
        fam["_family"] = "INCONCLUSIVE"
    else:
        fam["_family"] = "NO EDGE"
    return fam


def measurement_rows(a: Archive) -> dict:
    """Rows, NO verdicts (pre-reg #22 §3): the continuity profiles, the
    single-hour and first-5-minute variants, the leader rows, and the F2
    per-hour counts."""
    rows = {}
    canon = a.canon()
    tot = a.total_volume()
    tod = {}
    for i, (b0, b1) in enumerate(CANON):
        cp = canon[i]
        hl = []
        for df in a.files.values():
            t = df.index.time
            m = np.array([(x >= b0) and (x < b1) for x in t])
            x = df[m]
            if len(x) == 0:
                continue
            hl.append((x["High"].to_numpy() - x["Low"].to_numpy())
                      / x["Open"].to_numpy())
        tod[BUCKET_LABELS[i]] = {
            "mean_abs_ret": (float(cp["abs_r"].mean())
                             if len(cp["abs_r"]) else None),
            "mean_hl_over_o": (float(np.concatenate(hl).mean())
                               if hl else None),
            "vol_share": cp["vol_sum"] / tot if tot else None}
    rows["time_of_day"] = tod

    def win_stats_row(t0, t1):
        w = a.window_stats(t0, t1)
        if w["n_bars"] == 0:
            return None
        return {"mean_abs_ret": float(w["abs_r"].mean()),
                "median_abs_ret": float(np.median(w["abs_r"])),
                "tail_frac_gt_3x_median": float(w["tails"].mean()),
                "n_bars": w["n_bars"]}

    rows["pre_vs_rth"] = {
        "premarket_04_0930": win_stats_row(*PRE),
        "rth_0930_1600": win_stats_row(*RTH)}
    rows["single_hour_0930_1030"] = win_stats_row(dtime(9, 30), dtime(10, 30))
    rows["first_5_min_0930_0935"] = win_stats_row(dtime(9, 30), dtime(9, 35))
    rows["leaders"] = a.leader_rows()
    entries = [ev for ev in a.entries if ev["valid"]]
    if entries:
        rets = a.rets_for(entries)
        by_h = {}
        for i, ev in enumerate(entries):
            by_h.setdefault(ev["hour"], []).append(rets[i])
        rows["f2_per_hour"] = {
            f"{h:02d}": {"n": len(v), "mean_ret": float(np.mean(v))}
            for h, v in sorted(by_h.items())}
        rows["f2_n_by_date"] = {
            d: sum(1 for ev in entries
                   if ev["date"] == d and 570 <= ev["min"] < 720)
            for d in sorted({ev["date"] for ev in entries})}
    return rows


def check_floors(a: Archive) -> dict:
    """§4 sample-size floors (F2's pool = the F1-evaluable long entries)."""
    valid = [ev for ev in a.entries if ev["valid"]]
    floors = {
        "window_bar_dates": len({rel.split("/")[0] for rel in a.files}),
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
    L.append("# Pre-registration #22 measurement — the intraday regime")
    L.append("")
    L.append(f"- tool sha (raw): `{sha_bytes(Path(__file__).read_bytes())}`")
    L.append(f"- tool FROZEN_SHA (fixed point): `{FROZEN_SHA}`")
    L.append(f"- frozen input `tools/measure_intraday_entry.py` sha256 "
             f"(LF-normalized): `{_lf_sha(MIE)}`")
    L.append(f"- frozen input `tools/measure_intraday.py` sha256 "
             f"(LF-normalized): `{_lf_sha(MI)}`")
    L.append(f"- window: bar-dates >= {WINDOW_START}")
    L.append("")
    L.append("## Archive-integrity audit (§5)")
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
        L.append(f"detector: reversal-new-high (long) — {len(arc.entries)} "
                 f"entries, dropped {arc.dropped}; NO forward returns")
        L.append("")
        L.append("| bar-date | entries | dropped |")
        L.append("|---|---|---|")
        for d in sorted(arc.dropped_by_date):
            L.append(f"| {d} | "
                     f"{sum(1 for ev in arc.entries if ev['date'] == d)} | "
                     f"{arc.dropped_by_date.get(d, 0)} |")
        L.append("")
        L.append(f"### Bucket coverage (bar-dates with >= "
                 f"{MIN_NAMES_PER_DATE} names)")
        L.append("")
        L.append("| bucket | dates >= 10 names |")
        L.append("|---|---|")
        for i, cp in enumerate(arc.canon()):
            L.append(f"| {BUCKET_LABELS[i]} | {cp['n_dates_ge10']} |")
        return "\n".join(L) + "\n"
    L.append("")
    L.append("## Sample-size floors (§4)")
    L.append("")
    L.append("| floor | required | actual | met |")
    L.append("|---|---|---|---|")
    for k, req in FLOORS.items():
        L.append(f"| {k} | {req} | {floors[k]} | "
                 f"{'✓' if floors[k] >= req else '✗'} |")
    L.append("")
    L.append("## F1 — morning volatility/liquidity peak (2 Holm slots)")
    L.append("")
    L.append("Family verdict: **" + measure["f1"]["_family"] + "**")
    L.append("")
    for k, r in measure["f1"].items():
        if k == "_family":
            continue
        L.append(f"- **{k}** {r['slot']} — coverage dates >= 10 names: "
                 f"{r['coverage_dates_ge10']} (runner "
                 f"{r['runner_vol_bucket']} vol / {r['runner_liq_bucket']} "
                 f"liq)")
        L.append(f"  - volatility: bucket mean |r| {_fmt(r['vol']['mean'])} "
                 f"− runner {_fmt(r['vol']['mean_r'])}, diff "
                 f"{_fmt(r['vol']['est'])} (CI {_fmt(r['vol']['ci_low'])} … "
                 f"{_fmt(r['vol']['ci_upper'])}), p {_fmt(r['vol']['p'], 3)}")
        L.append(f"  - liquidity: bucket share {_fmt(r['liq']['mean'])} − "
                 f"runner {_fmt(r['liq']['mean_r'])}, diff "
                 f"{_fmt(r['liq']['est'])} (CI {_fmt(r['liq']['ci_low'])} … "
                 f"{_fmt(r['liq']['ci_upper'])}), p {_fmt(r['liq']['p'], 3)}")
        L.append(f"  - Holm gate {_fmt(r['holm_gate'], 3)} — "
                 f"{'rejected' if r['holm_rejected'] else 'not rejected'} · "
                 f"verdict **{r['verdict']}**")
    L.append("")
    L.append("## F2 — the money claim (1 Holm slot)")
    L.append("")
    L.append("Family verdict: **" + measure["f2"]["_family"] + "**")
    for k, r in measure["f2"].items():
        if k == "_family":
            continue
        L.append(f"- {r['slot']} — n_a {r['n_a']} (in B2), n_b {r['n_b']} "
                 f"(outside); mean a {_fmt(r.get('mean_a'))}, mean b "
                 f"{_fmt(r.get('mean_b'))}")
        L.append(f"  - diff (B2 − outside) {_fmt(r.get('est'))} (CI "
                 f"{_fmt(r.get('ci_low'))} … {_fmt(r.get('ci_upper'))}), "
                 f"p {_fmt(r.get('p'), 3)} · Holm gate "
                 f"{_fmt(r.get('holm_gate'), 3)} — "
                 f"{'rejected' if r.get('holm_rejected') else 'not rejected'} "
                 f"· verdict **{r.get('verdict')}**")
        if "excess_same" in r:
            L.append(f"  - hour-matched baseline excess (same-ticker): "
                     f"{_fmt(r['excess_same']['est'])} (CI "
                     f"{_fmt(r['excess_same']['ci_low'])} … "
                     f"{_fmt(r['excess_same']['ci_upper'])}))")
            L.append(f"  - hour-matched baseline excess (universe): "
                     f"{_fmt(r['excess_uni']['est'])} (CI "
                     f"{_fmt(r['excess_uni']['ci_low'])} … "
                     f"{_fmt(r['excess_uni']['ci_upper'])}))")
    L.append("")
    L.append("## F3 — pre-market cleanliness (1 Holm slot)")
    L.append("")
    L.append("Family verdict: **" + measure["f3"]["_family"] + "**")
    for k, r in measure["f3"].items():
        if k == "_family":
            continue
        L.append(f"- {r['slot']} — n pre {r['n_pre']}, n rth {r['n_rth']}")
        if r.get("vol"):
            L.append(f"  - mean |r|: pre {_fmt(r['vol']['mean_pre'])} − rth "
                     f"{_fmt(r['vol']['mean_rth'])}, diff "
                     f"{_fmt(r['vol']['est'])} (CI "
                     f"{_fmt(r['vol']['ci_low'])} … "
                     f"{_fmt(r['vol']['ci_upper'])}), p "
                     f"{_fmt(r['vol']['p'], 3)}")
            L.append(f"  - tail frac: pre {_fmt(r['tail']['frac_pre'])} − "
                     f"rth {_fmt(r['tail']['frac_rth'])}, diff "
                     f"{_fmt(r['tail']['est'])} (CI "
                     f"{_fmt(r['tail']['ci_low'])} … "
                     f"{_fmt(r['tail']['ci_upper'])}), p "
                     f"{_fmt(r['tail']['p'], 3)}")
        L.append(f"  - Holm gate {_fmt(r.get('holm_gate'), 3)} — "
                 f"{'rejected' if r.get('holm_rejected') else 'not rejected'} "
                 f"· verdict **{r.get('verdict')}**")
    L.append("")
    L.append("## Measurement rows (NO verdicts)")
    L.append("")
    r2 = measure["rows"]
    L.append("### Continuity: time-of-day profile")
    L.append("| bucket | mean |r| | mean (H−L)/O | volume share |")
    L.append("|---|---|---|---|")
    for lbl, v in r2["time_of_day"].items():
        L.append(f"| {lbl} | {_fmt(v.get('mean_abs_ret'))} | "
                 f"{_fmt(v.get('mean_hl_over_o'))} | "
                 f"{_fmt(v.get('vol_share'))} |")
    pv = r2["pre_vs_rth"]
    L.append("### Continuity: pre-market vs RTH")
    for lbl, v in pv.items():
        if v is None:
            L.append(f"- {lbl}: no bars")
        else:
            L.append(f"- {lbl}: mean |r| {_fmt(v['mean_abs_ret'])}, median "
                     f"{_fmt(v['median_abs_ret'])}, tail frac "
                     f"{_fmt(v['tail_frac_gt_3x_median'])}, n {v['n_bars']}")
    for lbl, v in (("09:30-10:30 single hour",
                    r2.get("single_hour_0930_1030")),
                   ("09:30-09:35 first 5 min",
                    r2.get("first_5_min_0930_0935"))):
        if v is None:
            L.append(f"- {lbl}: no bars")
        else:
            L.append(f"- {lbl}: mean |r| {_fmt(v['mean_abs_ret'])}, tail "
                     f"frac {_fmt(v['tail_frac_gt_3x_median'])}, n "
                     f"{v['n_bars']}")
    ld = r2.get("leaders", {})
    for lbl in ("by_bar_date", "by_ticker"):
        r = ld.get(lbl)
        if not r:
            continue
        L.append(f"- leader freq {lbl} (n {r['n']}): B1 vol "
                 f"{_fmt(r.get('B1_lead_vol'))}, B1 liq "
                 f"{_fmt(r.get('B1_lead_liq'))}, B2 vol "
                 f"{_fmt(r.get('B2_lead_vol'))}, B2 liq "
                 f"{_fmt(r.get('B2_lead_liq'))}")
    if "f2_per_hour" in r2:
        L.append("### F2 returns per entry hour")
        L.append("| hour | n | mean ret |")
        L.append("|---|---|---|")
        for h, v in r2["f2_per_hour"].items():
            L.append(f"| {h} | {v['n']} | {_fmt(v['mean_ret'])} |")
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
    f2 = run_f2(arc, rng)
    f3 = run_f3(arc, rng)
    rows = measurement_rows(arc)
    measure = {"f1": f1, "f2": f2, "f3": f3, "rows": rows}
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
        "f2": {k: v for k, v in f2.items() if k != "_family"},
        "f2_family": f2["_family"],
        "f3": {k: v for k, v in f3.items() if k != "_family"},
        "f3_family": f3["_family"],
        "rows": rows,
        "audit_passed": audit["passed"]}
    RESULTS_PATH.write_text(
        json.dumps(results, indent=1, sort_keys=True), encoding="utf-8")
    print(f"wrote {REPORT_PATH}")
    print(f"report sha256: {sha_file(REPORT_PATH)}")
    print(f"wrote {RESULTS_PATH}")
    print(f"results sha256: {sha_file(RESULTS_PATH)}")
    print("F1:", f1["_family"], "F2:", f2["_family"], "F3:", f3["_family"])
    sys.exit(0)


if __name__ == "__main__":
    main()
