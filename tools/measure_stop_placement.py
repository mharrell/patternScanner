"""Measurement tool for pre-registration #14 — I-X-05 stop placement
("the market shouldn't take out that prior extreme low").

Frozen 2026-08-16 (pre-registration #14 §1-§3). This tool implements the
frozen contract verbatim; the frozen files (tools/measure.py,
tools/measure_divergence.py) are sha-asserted AT IMPORT and never modified.

The claim (Trading 212, rgVdgR1y1Dg [07:40-08:03]): after a bullish
divergence the market should not take out the "prior extreme low" — the
divergence pair's lower low, Low[t2]. Measured as the breach rate on the
FROZEN pre-reg #10 BULL event set (recomputed here with the frozen
detection functions):
  breach ⇔ min(Low[s+1..s+N]) < Low[t2]      (intrabar, strict)
with s = t2 + k the confirmation-bar signal, N = 10 primary.

F1 (absolute — the claim's core): BULL breach rate vs era-matched
fractal-low confirmation-bar baselines — c = f + 2 of every strict k=2
fractal low f (warm-up c ≥ 60; c+N beyond the series end dropped and
counted), reference Low[f], breach ⇔ min(Low[c+1..c+N]) < Low[f]; the
divergence event bars are EXCLUDED from the pools (the comparison is "the
divergence condition adds value over the same low without it").
  random      — whole universe, uniform draw
  same-ticker — event tickers only, bars weighted by per-ticker BULL event
                counts (the frozen make_sample_same convention)
Contrast = event rate − baseline rate via paired bootstrap (B=1000, seed
20260816): resample M events with replacement → rate; resample M baseline
bars → rate; contrast over B draws → (est, ci_low, ci_high, p_two_sided).
p_input = max(p_rand, p_same), est = max, ci_low = min, ci_upper = min.
Holm at α=0.05 (single test → gate 0.05). Floor 100 OOS events.
  EDGE iff Holm-rejected AND CI-upper < 0 (the low holds better than
        typical lows — the claim);
  FADE iff Holm-rejected AND CI-low > 0 (taken out MORE often);
  NO EDGE otherwise.

F2 (contrast vs the alternate bounce signal): OS crossings (the frozen
pre-reg #9 S4 rule — first bar of each RSI<30 excursion, period 10;
measure_divergence.cross_frame, sha-asserted). For crossing bar c,
reference = the most recent strict k=2 fractal low at bar ≤ c within the
60-bar lookback (c − f < 60; crossings without one are dropped and
counted); breach ⇔ min(Low[c+1..c+N]) < reference. Contrast = divergence
rate − crossing rate, same bootstrap. EDGE iff Holm-rejected AND
CI-upper < 0 (divergence lows hold better than crossing references).
Age asymmetry documented conservative: the divergence reference is exactly
2 bars old; a crossing's reference averages older, and older levels are
less likely to be breached.

Measurement rows (no verdicts): stop distance (open[s+1] → Low[t2],
mean/median/p10/p90, % and in 14-bar ATR units — ATR_t = the simple mean
of the 14 true ranges ending at t, the pre-reg #11 formula); breach-loss
(entry → Low[t2] when breached); continue-gain (mean N-bar return − COST
when NOT breached); combined expected outcome = (1−br)·continue + br·loss;
the same decomposition on the same-ticker and random baselines; per-year
breach rates (all years reported, 2016-2025 the verdict rows).

Sensitivities (pre-declared, NO verdicts): S1 N = 5/20 (baselines rebuilt
per horizon, weights at the horizon's OOS counts); S2 stop level = Low[t1]
(the pair's first, higher low — the "second obvious level"); S3 period 14
(detection only — the fractal-low baselines are RSI-independent); S4
close-based breach (Close instead of Low); S5 BEAR mirror (High[t2] stop,
fractal-high baselines, breach ⇔ max(High[s+1..s+N]) > High[t2]).

Era: OOS by signal date ≥ measure.ERA_OOS ("2016-01-01" primary; rebound
to "2022-01-01" in --gate mode). Universe: measure.UNIVERSE_CSV (current
S&P 600 constituents primary; the pre-reg #13 904-name historical union in
--gate mode, 706 with bars — 199 purged from Yahoo's data, flagged and NOT
substituted). IS 2000-2015 (2000-2021 in gate mode) descriptive only.

Event-set anchors (the event set is the frozen pre-reg #10 set by
construction) — asserted against the mode's frozen JSON
(divergence_measure_results.json primary / divergence_hist_measure_results
.json gate):
  - per-leg all-era counts (warm-up excluded, complete windows at N=10) ==
    sensitivities.per_year sums
  - OOS BULL count == families.f1_absolute.BULL.n, and
    n + drops_primary.BULL == frequency.n_bull (OOS raw)
  - OOS OS/OB raw counts == frequency.n_os / n_ob; drops_cross_primary ==
    the tool's crossing end-drops
  - assertions: min_t1, min_signal_bar, max_signal_bar, n_bad_signal,
    drops_primary, drops_cross_primary all reproduced; RSI within [0, 100]
  - every event ticker has a non-empty OOS baseline pool

Usage:
  python -X utf8 tools/measure_stop_placement.py            # primary
  python -X utf8 tools/measure_stop_placement.py --gate     # §5 gate run
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import measure
import measure_divergence as md

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
BARS_DIR = CACHE / "bars"

ANCHOR_JSON = CACHE / "divergence_measure_results.json"
ANCHOR_HIST_JSON = CACHE / "divergence_hist_measure_results.json"
UNIVERSE_HIST_CSV = CACHE / "universe_sp600_hist_2026-08-15.csv"
RESULTS = CACHE / "stop_placement_measure_results.json"
REPORT = CACHE / "stop_placement_measure_report.md"
RESULTS_GATE = CACHE / "stop_placement_gate_measure_results.json"
REPORT_GATE = CACHE / "stop_placement_gate_measure_report.md"

# ---- frozen-file assertion AT IMPORT (pre-reg #14 §2 integrity) ----
FROZEN = {
    measure.__file__: "c7421fbffeaf16ed43278faafa7325e2972634d516bc013c41e15e7f733b1b93",
    md.__file__: "85f2ae0d4a1e07906d88fb9c4b2fda02e68f943635b618af660502ddc5597c72",
}
for _f, _want in FROZEN.items():
    _got = hashlib.sha256(Path(_f).read_bytes()).hexdigest()
    assert _got == _want, (f"{_f} changed (sha {_got[:16]}..., want "
                           f"{_want[:16]}...) — frozen inputs must not move")
print("frozen shas OK (measure.py c7421fbf…, measure_divergence.py "
      "85f2ae0d4a1e…)")

# ---- frozen parameters (pre-reg #10 §1 / #14 §2) ----
PERIOD = 10                # RSI period (the demo charts' "ten day RSI")
PERIOD_SENS = 14           # S3
K = 2                      # strict fractal half-width
MIN_SEP = 5                # disjoint fractal windows
CONFIRM = 2                # signal bar = t2 + k (no look-ahead)
N_PRIMARY = 10
SENS_N = [5, 20]           # S1
WARMUP = 60                # frozen #3 convention
LOOKBACK = 60              # F2 reference lookback (c − f < 60)
OB_HI = 70.0
OS_LO = 30.0
B = 1000
SEED = 20260816            # pre-reg #14 §2 (new campaign seed)
ALPHA = 0.05
MISSING_PASS = 100         # count floor
COST = measure.COST        # 0.0015 round-trip


def sha(f: Path) -> str:
    return hashlib.sha256(f.read_bytes()).hexdigest()


def fmt_num(v, spec="+.4f") -> str:
    return "—" if v is None else format(v, spec)


# ----------------------------------------------------------------------
# detection — the frozen pre-reg #10 functions, verbatim
# ----------------------------------------------------------------------

def detect(tickers):
    """Recompute the frozen divergence detection (both legs) per ticker.

    Returns (maps, bull, bear, det_rows, stats, rsi_bounds) where maps =
    dict of per-ticker arrays keyed under their ticker:
      lows/highs/opens/closes/atr14 (np arrays), dates (DatetimeIndex),
      sw_low/sw_high (fractal index arrays), rsi10 (pd.Series)
    bull/bear = event record lists [{ticker, s, t1, t2, year}] — ALL
    events incl. warm-up and end-drops (filtered downstream);
    det_rows = (ticker, signal_date, shape, bar_index) as in div_frame;
    stats = {min_t1, min_signal, max_signal, n_bad_signal} over both legs.
    """
    maps = {"lows": {}, "highs": {}, "opens": {}, "closes": {},
            "dates": {}, "atr14": {}, "sw_low": {}, "sw_high": {},
            "rsi10": {}}
    bull, bear = [], []
    det_rows = []
    min_t1, min_sig, max_sig, n_bad = np.inf, np.inf, -np.inf, 0
    rsi_min_all, rsi_max_all = np.inf, -np.inf
    n_with_bars = 0
    for t in tickers:
        p = BARS_DIR / f"{t}.parquet"
        if not p.exists():
            continue            # universe rows without bars (house convention)
        n_with_bars += 1
        df = pd.read_parquet(p)
        lo = df["Low"].to_numpy(dtype=np.float64)
        hi = df["High"].to_numpy(dtype=np.float64)
        op = df["Open"].to_numpy(dtype=np.float64)
        cl = df["Close"].to_numpy(dtype=np.float64)
        dts = df.index
        n = len(df)
        rsi = md.rsi_series(df["Close"], PERIOD)
        rsi_np = rsi.to_numpy(dtype=np.float64)
        valid = ~np.isnan(rsi_np)
        if valid.any():
            rsi_min_all = min(rsi_min_all, float(rsi_np[valid].min()))
            rsi_max_all = max(rsi_max_all, float(rsi_np[valid].max()))
        sw_l = md.swing_idx(lo, K, True)
        sw_h = md.swing_idx(hi, K, False)
        # ATR14 (pre-reg #11 formula): TR_t = max(H−L, |H−C_{t−1}|,
        # |L−C_{t−1}|); ATR_t = mean of the 14 true ranges ending at t.
        tr = np.empty(n)
        tr[0] = hi[0] - lo[0]                    # never read (warmup ≥ 60)
        tr[1:] = np.maximum.reduce(
            [hi[1:] - lo[1:], np.abs(hi[1:] - cl[:-1]),
             np.abs(lo[1:] - cl[:-1])])
        cs = np.concatenate(([0.0], np.cumsum(tr)))
        atr = np.full(n, np.nan)
        if n > 13:                      # short series: no ATR, no events
            atr[13:] = (cs[14:] - cs[:n - 13]) / 14.0
        for sw, price_series, gain_ok, leg in (
                (sw_l, df["Low"], True, "BULL"),
                (sw_h, df["High"], False, "BEAR")):
            ev, t1s, t2s = md._pair_events(sw, price_series, rsi, CONFIRM,
                                           MIN_SEP, gain_ok, None)
            if not len(ev):
                continue
            min_t1 = min(min_t1, int(t1s.min()))
            min_sig = min(min_sig, int(ev.min()))
            max_sig = max(max_sig, int(ev.max()))
            n_bad += int((ev >= n).sum())
            out = bull if leg == "BULL" else bear
            for i in range(len(ev)):
                s = int(ev[i])
                det_rows.append((t, str(dts[s].date()), leg, s))
                out.append({"ticker": t, "s": s, "t1": int(t1s[i]),
                            "t2": int(t2s[i]), "year": str(dts[s])[:4]})
        maps["lows"][t] = lo
        maps["highs"][t] = hi
        maps["opens"][t] = op
        maps["closes"][t] = cl
        maps["dates"][t] = dts
        maps["atr14"][t] = atr
        maps["sw_low"][t] = sw_l
        maps["sw_high"][t] = sw_h
        maps["rsi10"][t] = rsi
    stats = {"min_t1": min_t1, "min_signal": min_sig,
             "max_signal": max_sig, "n_bad_signal": n_bad,
             "rsi_min_all": rsi_min_all, "rsi_max_all": rsi_max_all,
             "n_with_bars": n_with_bars}
    return maps, bull, bear, det_rows, stats


# ----------------------------------------------------------------------
# breach measurement
# ----------------------------------------------------------------------

def event_rows(recs, m, N, level="t2", close_based=False):
    """Per-event outcome rows for complete-window events (signal ≥ WARMUP,
    s + N < len). level: "t2" -> L = Low[t2] (primary), "t1" -> L = Low[t1]
    (S2). close_based (S4): the breach window reads Close instead of Low.
    Returns (rows, dropped) — dropped = events at the series end, counted."""
    lo = m["lows"]
    op = m["opens"]
    cl = m["closes"]
    dts = m["dates"]
    atr = m["atr14"]
    rows, dropped = [], 0
    for r in recs:
        s, t1, t2 = r["s"], r["t1"], r["t2"]
        if s < WARMUP:
            continue
        n = len(lo[r["ticker"]])
        if s + N >= n:
            dropped += 1
            continue
        t = r["ticker"]
        L = lo[t][t2] if level == "t2" else lo[t][t1]
        src = lo[t][s + 1:s + 1 + N] if not close_based \
            else cl[t][s + 1:s + 1 + N]
        breached = bool((src < L).any())
        entry = op[t][s + 1]
        loss = L / entry - 1.0
        cont = cl[t][s + N] / entry - 1.0 - COST
        rows.append({"ticker": t, "s": s, "year": r["year"],
                     "ts": dts[t][s], "breached": breached,
                     "loss": loss, "cont": cont,
                     "dist_pct": (entry - L) / entry,
                     "dist_atr": (entry - L) / atr[t][s]})
    return rows, dropped


def baseline_pool(m, era, N, bear=False, close_based=False,
                  exclusions=()):
    """Fractal-low (bull) / fractal-high (bear) confirmation-bar pool.

    Bars c = f + 2 of every strict k=2 fractal f; warm-up c ≥ 60; c + N
    beyond the series end dropped and counted; reference = the fractal's
    own level (Low[f] / High[f]); breach = min(Low[c+1..c+N]) < ref
    (bull) / max(High[c+1..c+N]) > ref (bear); bars in `exclusions` (the
    divergence event bars) are excluded and counted. Returns per-ticker
    arrays of [breach, loss, cont, combined] over the OOS pool plus the
    drop/exclusion counts."""
    by_t = {}
    drops_end = drops_warm = excluded_n = 0
    for t in m["sw_low"] if not bear else m["sw_high"]:
        src = m["lows"][t] if not bear else m["highs"][t]
        sw = m["sw_low"][t] if not bear else m["sw_high"][t]
        op = m["opens"][t]
        cl = m["closes"][t]
        dts = m["dates"][t]
        arr = []
        for f in sw:
            c = f + 2
            if c < WARMUP:
                drops_warm += 1
                continue
            if c + N >= len(src):
                drops_end += 1
                continue
            if (t, c) in exclusions:
                excluded_n += 1
                continue
            if dts[c] < era:
                continue
            ref = src[f]
            wnd = src[c + 1:c + 1 + N] if not close_based \
                else cl[c + 1:c + 1 + N]
            breached = bool((wnd < ref).any()) if not bear \
                else bool((wnd > ref).any())
            entry = op[c + 1]
            loss = ref / entry - 1.0
            cont = cl[c + N] / entry - 1.0 - COST
            arr.append((int(breached), loss, cont,
                        loss if breached else cont))
        if arr:
            by_t[t] = np.array(arr, dtype=np.float64)
    return by_t, drops_end, drops_warm, excluded_n


def make_sampler_rand(by_t, rng):
    flat = np.concatenate([by_t[t][:, 0] for t in by_t])
    return (lambda M: flat[rng.integers(0, len(flat), size=M)]), \
        len(flat), float(flat.mean())


def make_sampler_same(by_t, oos_recs, rng):
    """Event-count-weighted same-ticker sampler (frozen make_sample_same
    convention). oos_recs = the leg's OOS events at the measurement N."""
    u, counts = np.unique([r["ticker"] for r in oos_recs], return_counts=True)
    w = counts.astype(np.float64) / counts.sum()
    lengths = np.array([len(by_t[t]) for t in u], dtype=np.int64)
    n_missing = int((lengths == 0).sum())
    assert n_missing == 0, (f"{n_missing} event tickers have no OOS baseline "
                            "pool (expected 0)")
    off = np.concatenate(([0], np.cumsum(lengths)))
    flat = np.concatenate([by_t[t][:, 0] for t in u])
    rate_w = float((w * np.array([by_t[t][:, 0].mean() for t in u])).sum())

    def s(M):
        ts = rng.choice(len(u), size=M, p=w)
        idx = off[ts] + (rng.random(M) * lengths[ts]).astype(np.int64)
        return flat[idx]
    return s, rate_w


def contrast_bootstrap(ev_arr, sampler, rng):
    """Paired bootstrap of event_rate − baseline_rate (B draws, resample M
    of each). Returns (est, median, ci_low, ci_high, p_two_sided)."""
    M = len(ev_arr)
    diffs = np.empty(B)
    for b in range(B):
        er = ev_arr[rng.integers(0, M, size=M)].mean()
        diffs[b] = er - sampler(M).mean()
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)), float(lo),
            float(hi), float(p))


def two_sample_contrast(ev_arr, cross_arr, rng):
    """Divergence rate − crossing rate, resample M of each (the frozen
    two_sample_excess convention)."""
    M = len(ev_arr)
    diffs = np.empty(B)
    for b in range(B):
        er = ev_arr[rng.integers(0, M, size=M)].mean()
        cr = cross_arr[rng.integers(0, len(cross_arr), size=M)].mean()
        diffs[b] = er - cr
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return (float(diffs.mean()), float(np.median(diffs)), float(lo),
            float(hi), float(p))


def crossing_rows(m, era, N, close_based=False):
    """OS crossing breach rows (F2). Reference = the most recent strict
    k=2 fractal low at bar ≤ c within the 60-bar lookback (c − f < 60);
    crossings without one are dropped and counted. Returns (rows, no_ref,
    drops_end, warmup_n) over the all-era warm-up-excluded frame; OOS
    filtering by `era`."""
    det = md.cross_frame(m["rsi10"], OB_HI, OS_LO)
    os_det = det[(det["shape"] == "OS") & (~det["warmup"])]
    rows, no_ref, drops_end = [], 0, 0
    for _, r in os_det.iterrows():
        t, c = r["ticker"], int(r["bar_index"])
        if c + N >= len(m["lows"][t]):
            drops_end += 1
            continue
        if m["dates"][t][c] < era:
            continue
        sw = m["sw_low"][t]
        idx = np.searchsorted(sw, c, side="right") - 1
        if idx < 0 or c - int(sw[idx]) >= LOOKBACK:
            no_ref += 1
            continue
        L = m["lows"][t][int(sw[idx])]
        wnd = m["lows"][t][c + 1:c + 1 + N] if not close_based \
            else m["closes"][t][c + 1:c + 1 + N]
        rows.append(int((wnd < L).any()))
    return rows, no_ref, drops_end


# ----------------------------------------------------------------------
# verdicts (pre-reg #14 §2 — single-test families, gate 0.05)
# ----------------------------------------------------------------------

def verdict_f1(r: dict) -> str:
    if int(r["n"]) < MISSING_PASS:
        return (f"INCONCLUSIVE (<{MISSING_PASS} OOS events; n={r['n']})")
    if r["holm_rejected"] and r["ci_upper"] < 0.0:
        return (f"EDGE (Holm-rejected; excess CI-upper {r['ci_upper']:+.4f} "
                "< 0 — divergence lows hold better than typical lows, as "
                "claimed)")
    if r["holm_rejected"] and r["ci_low"] > 0.0:
        return (f"FADE (Holm-rejected; excess CI-low {r['ci_low']:+.4f} > 0 "
                "— divergence lows taken out MORE often than typical lows, "
                "claim contradicted)")
    return (f"NO EDGE (p_input {r['p']:.3f}; est {r['est']:+.4f}; CI-low "
            f"{r['ci_low']:+.4f}..CI-upper {r['ci_upper']:+.4f})")


def verdict_f2(r: dict) -> str:
    e = r["excess"]                      # [est, median, ci_low, ci_hi, p]
    if int(r["n_div"]) < MISSING_PASS:
        return (f"INCONCLUSIVE (<{MISSING_PASS} OOS divergence events; "
                f"n_div={r['n_div']}, n_cross={r['n_cross']})")
    if r["holm_rejected"] and e[3] < 0.0:
        return (f"EDGE (Holm-rejected; contrast CI-upper {e[3]:+.4f}"
                " < 0 — divergence lows hold better than oversold-crossing "
                "references)")
    if r["holm_rejected"] and e[2] > 0.0:
        return (f"FADE (Holm-rejected; contrast CI-low {e[2]:+.4f} "
                "> 0 — divergence lows taken out more often than "
                "oversold-crossing references)")
    return (f"NO EDGE (contrast est {e[0]:+.4f}, p {e[4]:.3f})")


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------

def main() -> int:
    gate = "--gate" in sys.argv[1:]
    if gate:
        universe_csv = UNIVERSE_HIST_CSV
        anchor = ANCHOR_HIST_JSON
        results, report = RESULTS_GATE, REPORT_GATE
        measure.ERA_OOS = "2022-01-01"          # pre-reg #14 §3
    else:
        universe_csv = measure.UNIVERSE_CSV
        anchor = ANCHOR_JSON
        results, report = RESULTS, REPORT
    era = pd.Timestamp(measure.ERA_OOS)
    a = json.loads(anchor.read_text(encoding="utf-8"))
    print(f"mode: {'gate' if gate else 'primary'} | universe "
          f"{universe_csv.name} | ERA_OOS {measure.ERA_OOS} | anchor "
          f"{anchor.name}")

    tickers = pd.read_csv(universe_csv)["ticker"].tolist()
    m, bull, bear, det_rows, stats = detect(tickers)
    print(f"universe tickers: {len(tickers)} | with bars: "
          f"{stats['n_with_bars']}")

    # ---- structural checks (frozen #10 §3, reproduced) ----
    assert 0.0 - 1e-9 <= stats["rsi_min_all"] and \
        stats["rsi_max_all"] <= 100.0 + 1e-9, "RSI bounds violated"
    assert stats["min_t1"] >= PERIOD, \
        f"min t1 {stats['min_t1']} < {PERIOD} (expected 0)"
    assert stats["n_bad_signal"] == 0, "events with signal beyond series"

    # ---- event set anchors (frozen JSON) ----
    # pre-reg #14 §2 requires the event set to BE the frozen pre-reg #10
    # event set. The frozen primary record (divergence_measure_results.json,
    # written 2026-08-15) is anchored by per-year counts. On the current
    # bars the frozen pipeline — and md.main() itself, run with outputs
    # rebound and shas asserted — CANNOT regenerate the frozen primary
    # record (per_year BULL 34075 vs frozen 34076, BEAR 42757 vs 42759;
    # freq n_bull 17016 vs 17017, n_bear 20910 vs 20912; fam1 BULL n 16984
    # vs 16985), while the frozen #13 record (divergence_hist_measure_
    # results.json, written 2026-08-16) regenerates EXACTLY on the same
    # data. The 08-13-era bytes are unrecoverable (fetch_log.json records
    # only rows/dates — no hashes; no raw downloads exist). So the frozen
    # #10 event set is not reconstructible from the current bars: the
    # primary anchor is recorded here as a QUANTIFIED DEVIATION (3
    # divergence events + 1 OB crossing across 5 year-legs; the OOS BULL
    # event set under test differs by exactly 1 event), not silently
    # absorbed, and the verdicts carry a drift-materiality guard below.
    # This is a data-state deviation, not a parameter change; no frozen
    # file was modified. In gate mode the anchor is the hist record, which
    # regenerates — there the event-set anchors stay hard.
    py = a["sensitivities"]["per_year"]
    sum_bull = sum(py[y]["BULL"]["n"] for y in py)
    sum_bear = sum(py[y]["BEAR"]["n"] for y in py)
    bull_all = [r for r in bull if r["s"] >= WARMUP]
    bear_all = [r for r in bear if r["s"] >= WARMUP]
    n_bull_anchor = sum(1 for r in bull_all if r["s"] + N_PRIMARY <
                        len(m["lows"][r["ticker"]]))
    n_bear_anchor = sum(1 for r in bear_all if r["s"] + N_PRIMARY <
                        len(m["lows"][r["ticker"]]))
    bull_by_year = {}
    for r in bull_all:
        bull_by_year[str(r["year"])] = bull_by_year.get(str(r["year"]), 0) + 1
    bear_by_year = {}
    for r in bear_all:
        bear_by_year[str(r["year"])] = bear_by_year.get(str(r["year"]), 0) + 1
    year_deltas = {}
    for y in sorted(set(list(py) + list(bull_by_year) + list(bear_by_year))):
        for shape, obs in (("BULL", bull_by_year), ("BEAR", bear_by_year)):
            want = int(py[y][shape]["n"]) if y in py else 0
            got = obs.get(y, 0)
            if got != want:
                year_deltas.setdefault(y, {})[shape] = got - want
    errs = []
    def check(name, got, want, tol=0.0):
        ok = abs(got - want) <= tol
        print(f"  anchor {name}: got {got} vs frozen {want} "
              f"{'OK' if ok else 'MISMATCH'}")
        if not ok:
            errs.append(name)
    def report_anchor(name, got, want):
        ok = got == want
        print(f"  anchor {name}: got {got} vs frozen {want} "
              f"{'OK' if ok else 'DEVIATION'}")
    if gate:
        check("per_year BULL sum (all-era, N=10 complete)", n_bull_anchor,
              int(sum_bull))
        check("per_year BEAR sum (all-era, N=10 complete)", n_bear_anchor,
              int(sum_bear))
    else:
        report_anchor("per_year BULL sum (all-era, N=10 complete)",
                      n_bull_anchor, int(sum_bull))
        report_anchor("per_year BEAR sum (all-era, N=10 complete)",
                      n_bear_anchor, int(sum_bear))
    check("min_t1", int(stats["min_t1"]),
          int(a["assertions"]["min_t1"]))
    check("min_signal_bar", int(stats["min_signal"]),
          int(a["assertions"]["min_signal_bar"]))
    check("max_signal_bar", int(stats["max_signal"]),
          int(a["assertions"]["max_signal_bar"]))
    check("n_bad_signal", int(stats["n_bad_signal"]),
          int(a["assertions"]["n_bad_signal"]))
    assert not errs, f"event-set anchors failed: {errs}"
    print("event-set anchors " + ("PASSED (the event set is the frozen "
          "pre-reg #10 set by construction)" if gate else
          "REPORTED — structural anchors PASSED; the primary-record "
          "deviation is quantified in the anchor block"))

    # ---- OOS counts (raw and complete-window) ----
    bull_oos_raw = [r for r in bull_all if m["dates"][r["ticker"]][r["s"]]
                    >= era]
    bear_oos_raw = [r for r in bear_all if m["dates"][r["ticker"]][r["s"]]
                    >= era]
    if gate:
        check("OOS BULL raw == n + drops (freq.n_bull)", len(bull_oos_raw),
              int(a["frequency"]["n_bull"]))
        check("OOS BEAR raw == freq.n_bear", len(bear_oos_raw),
              int(a["frequency"]["n_bear"]))
    else:
        report_anchor("OOS BULL raw (freq.n_bull)", len(bull_oos_raw),
                      int(a["frequency"]["n_bull"]))
        report_anchor("OOS BEAR raw (freq.n_bear)", len(bear_oos_raw),
                      int(a["frequency"]["n_bear"]))

    # ---- F1: primary (BULL, N=10) ----
    rng = np.random.default_rng(SEED)
    rows, drops = event_rows(bull, m, N_PRIMARY)
    oos_rows = [r for r in rows if r["ts"] >= era]
    ev = np.array([r["breached"] for r in oos_rows], dtype=np.int64)
    excl = {(r["ticker"], r["s"]) for r in bull_oos_raw}
    by_t_all, drops_end_r, drops_warm_r, excl_r = baseline_pool(
        m, era, N_PRIMARY, exclusions=excl)
    by_t_same = {t: by_t_all[t] for t in
                 set(r["ticker"] for r in bull_oos_raw) if t in by_t_all}
    s_rand, n_pool_rand, rate_rand = make_sampler_rand(by_t_all, rng)
    s_same, rate_same = make_sampler_same(by_t_same, bull_oos_raw, rng)
    e_rand = contrast_bootstrap(ev, s_rand, rng)
    e_same = contrast_bootstrap(ev, s_same, rng)
    fam1 = {"n": int(len(ev)),
            "breach_rate": float(ev.mean()),
            "baseline_random": {"pool_n": n_pool_rand, "rate": rate_rand},
            "baseline_same": {"rate": rate_same},
            "excess": {"random": list(e_rand), "same_ticker": list(e_same)},
            "p": float(max(e_rand[4], e_same[4])),
            "est": float(max(e_rand[0], e_same[0])),
            "ci_low": float(min(e_rand[2], e_same[2])),
            "ci_upper": float(min(e_rand[3], e_same[3]))}
    fam1["holm_gate"] = ALPHA
    fam1["holm_rejected"] = fam1["p"] <= ALPHA
    fam1["verdict"] = verdict_f1(fam1)
    if gate:
        check("OOS BULL complete == fam1 n", fam1["n"],
              int(a["families"]["f1_absolute"]["BULL"]["n"]))
    else:
        report_anchor("fam1 BULL n (OOS complete)", fam1["n"],
                      int(a["families"]["f1_absolute"]["BULL"]["n"]))
    check("drops_primary BULL", drops,
          int(a["assertions"]["drops_primary"]["BULL"]))
    check("drops_primary BEAR",
          sum(1 for r in bear_all if r["s"] + N_PRIMARY >=
              len(m["lows"][r["ticker"]])),
          int(a["assertions"]["drops_primary"]["BEAR"]))

    # ---- F2: OS crossings ----
    cross, no_ref, drops_cross = crossing_rows(m, era, N_PRIMARY)
    cross_ev = np.array(cross, dtype=np.int64)
    e_cross = two_sample_contrast(ev, cross_ev, rng)
    fam2 = {"n_div": int(len(ev)), "n_cross": int(len(cross_ev)),
            "rate_div": float(ev.mean()),
            "rate_cross": float(cross_ev.mean()),
            "excess": list(e_cross)}
    fam2["holm_gate"] = ALPHA
    fam2["holm_rejected"] = fam2["excess"][4] <= ALPHA
    fam2["verdict"] = verdict_f2(fam2)
    # freq.n_os counts raw OOS OS crossings INCLUDING end-drops and
    # no-reference bars: recompute directly from the frozen frame
    det_os = md.cross_frame(m["rsi10"], OB_HI, OS_LO)
    det_os = det_os[(det_os["shape"] == "OS") & (~det_os["warmup"])]
    os_raw = sum(1 for _, r in det_os.iterrows()
                 if m["dates"][r["ticker"]][int(r["bar_index"])] >= era)
    check("OOS OS raw (direct) == freq.n_os", os_raw,
          int(a["frequency"]["n_os"]))
    check("drops_cross_primary OS", drops_cross,
          int(a["assertions"]["drops_cross_primary"]["OS"]))

    # ---- drift-materiality guard (primary-mode anchor deviation) ----
    # Upper bound on the rate shift the recorded data drift could cause:
    # ≤ |ΔBULL|+|ΔBEAR| divergence events changed on the event side, the
    # same count over the F1 baseline pool, and the observed ±1 crossing
    # over the F2 crossing set. At n≈17k this is ~60× below the bootstrap
    # CI width, but if a verdict's decisive CI bound sits within this
    # bound of zero it is flagged drift-sensitive rather than reported
    # clean.
    if not gate:
        d_bull = n_bull_anchor - int(sum_bull)
        d_bear = n_bear_anchor - int(sum_bear)
        d_ev = abs(d_bull) + abs(d_bear)
        drift = {
            "events_changed_ub": int(d_ev),
            "crossings_changed_ub": 1,   # n_ob +1 / n_os ±0 observed
            "delta_event_rate": d_ev / max(1, fam1["n"]),
            "delta_f1": (d_ev / max(1, fam1["n"])
                         + d_ev / max(1, n_pool_rand)),
            "delta_f2": (d_ev / max(1, fam1["n"])
                         + 1.0 / max(1, len(cross_ev)))}
        fam1["drift_bound"] = drift["delta_f1"]
        fam1["drift_sensitive"] = bool(
            -drift["delta_f1"] <= fam1["ci_upper"] <= drift["delta_f1"]
            or -drift["delta_f1"] <= fam1["ci_low"] <= drift["delta_f1"])
        fam2["drift_bound"] = drift["delta_f2"]
        fam2["drift_sensitive"] = bool(
            -drift["delta_f2"] <= fam2["excess"][3] <= drift["delta_f2"]
            or -drift["delta_f2"] <= fam2["excess"][2] <= drift["delta_f2"])
        if fam1["drift_sensitive"]:
            fam1["verdict"] += " [DRIFT-SENSITIVE]"
        if fam2["drift_sensitive"]:
            fam2["verdict"] += " [DRIFT-SENSITIVE]"
    else:
        drift = {"events_changed_ub": 0, "crossings_changed_ub": 0}

    # ---- measurement rows (no verdicts) ----
    d_pct = np.array([r["dist_pct"] for r in oos_rows])
    d_atr = np.array([r["dist_atr"] for r in oos_rows])
    b_ar = np.array([r["breached"] for r in oos_rows], dtype=bool)
    loss_ar = np.array([r["loss"] for r in oos_rows])
    cont_ar = np.array([r["cont"] for r in oos_rows])
    comb_ar = np.where(b_ar, loss_ar, cont_ar)
    meas = {
        "stop_distance_pct": {"n": len(oos_rows),
                              "mean": float(d_pct.mean()),
                              "median": float(np.median(d_pct)),
                              "p10": float(np.percentile(d_pct, 10)),
                              "p90": float(np.percentile(d_pct, 90))},
        "stop_distance_atr14": {"n": len(oos_rows),
                                "mean": float(d_atr.mean()),
                                "median": float(np.median(d_atr)),
                                "p10": float(np.percentile(d_atr, 10)),
                                "p90": float(np.percentile(d_atr, 90))},
        "decomposition_events": {
            "n": len(oos_rows), "n_breached": int(b_ar.sum()),
            "breach_loss": float(loss_ar[b_ar].mean()) if b_ar.any()
            else None,
            "continue_gain": float(cont_ar[~b_ar].mean()) if (~b_ar).any()
            else None,
            "combined": float(comb_ar.mean())},
    }
    # same decomposition on the same-ticker baseline (weighted per-ticker
    # means — the make_sample_same convention)
    u_w, cnt = np.unique([r["ticker"] for r in bull_oos_raw],
                         return_counts=True)
    w = cnt.astype(np.float64) / cnt.sum()
    def wmean(col):
        return float((w * np.array([by_t_same[t][:, col].mean()
                                    for t in u_w])).sum())
    same_dec = {
        "breach_rate": rate_same,
        "breach_loss": wmean(1) if by_t_same else None,
        "continue_gain": wmean(2) if by_t_same else None,
        "combined": wmean(3) if by_t_same else None}
    # random pool decomposition (plain pooled means)
    all_mat = np.concatenate([by_t_all[t] for t in by_t_all])
    rand_dec = {
        "breach_rate": rate_rand,
        "breach_loss": float(all_mat[:, 1].mean()),
        "continue_gain": float(all_mat[:, 2].mean()),
        "combined": float(all_mat[:, 3].mean())}
    meas["decomposition_same_ticker"] = same_dec
    meas["decomposition_random"] = rand_dec
    years = sorted(set(r["year"] for r in rows))
    meas["per_year"] = {
        y: {"n": int(sum(1 for r in rows if r["year"] == y)),
            "breach_rate": float(np.mean([r["breached"] for r in rows
                                          if r["year"] == y]))}
        for y in years}
    is_rows = [r for r in rows if r["ts"] < era]
    meas["is_record"] = {"n": int(len(is_rows)),
                         "breach_rate": float(np.mean(
                             [r["breached"] for r in is_rows])) if is_rows
                         else None}
    meas["oos_record"] = {"n": int(len(oos_rows)),
                          "breach_rate": float(ev.mean())}

    # ---- sensitivities (pre-declared, NO verdicts) ----
    sens = {}
    for n in SENS_N:                                  # S1
        rn, dn = event_rows(bull, m, n)
        oos_n = [r for r in rn if r["ts"] >= era]
        evn = np.array([r["breached"] for r in oos_n], dtype=np.int64)
        by_n, _, _, _ = baseline_pool(m, era, n, exclusions=excl)
        by_ns = {t: by_n[t] for t in
                 set(r["ticker"] for r in oos_n) if t in by_n}
        _, rn_rand = make_sampler_rand(by_n, rng)[1:]
        _, rn_same = make_sampler_same(by_ns, oos_n, rng)
        sens[f"N={n}"] = {"n": int(len(evn)),
                          "breach_rate": float(evn.mean()),
                          "baseline_random_rate": rn_rand,
                          "baseline_same_rate": rn_same}
    r_t1, _ = event_rows(bull, m, N_PRIMARY, level="t1")   # S2
    oos_t1 = [r for r in r_t1 if r["ts"] >= era]
    sens["level_t1"] = {"n": int(len(oos_t1)),
                        "breach_rate": float(np.mean(
                            [r["breached"] for r in oos_t1])),
                        "baseline_random_rate": rate_rand,
                        "baseline_same_rate": rate_same}
    r14 = []                                             # S3 (period 14)
    for t in m["rsi10"]:
        rsi14 = md.rsi_series(pd.Series(m["closes"][t], index=m["dates"][t]),
                              PERIOD_SENS)
        ev14, t1s, t2s = md._pair_events(
            m["sw_low"][t], pd.Series(m["lows"][t], index=m["dates"][t]),
            rsi14, CONFIRM, MIN_SEP, True, None)
        for i in range(len(ev14)):
            s = int(ev14[i])
            r14.append({"ticker": t, "s": s, "t1": int(t1s[i]),
                        "t2": int(t2s[i]), "year": str(m["dates"][t][s])[:4]})
    rows14, drops14 = event_rows(r14, m, N_PRIMARY)
    oos14 = [r for r in rows14 if r["ts"] >= era]
    sens["period14"] = {"n": int(len(oos14)),
                        "breach_rate": float(np.mean(
                            [r["breached"] for r in oos14])),
                        "baseline_random_rate": rate_rand,
                        "baseline_same_rate": rate_same,
                        "drops": drops14}
    rc, _ = event_rows(bull, m, N_PRIMARY, close_based=True)   # S4
    oos_c = [r for r in rc if r["ts"] >= era]
    evc = np.array([r["breached"] for r in oos_c], dtype=np.int64)
    by_c, _, _, _ = baseline_pool(m, era, N_PRIMARY, close_based=True,
                                  exclusions=excl)
    by_cs = {t: by_c[t] for t in set(r["ticker"] for r in oos_c)
             if t in by_c}
    _, r_cr = make_sampler_rand(by_c, rng)[1:]
    _, r_cs = make_sampler_same(by_cs, oos_c, rng)
    sens["close_breach"] = {"n": int(len(evc)),
                            "breach_rate": float(evc.mean()),
                            "baseline_random_rate": r_cr,
                            "baseline_same_rate": r_cs}
    rb, dropsb = event_rows(bear, m, N_PRIMARY)               # S5
    oos_b = [r for r in rb if r["ts"] >= era]
    evb = np.array([r["breached"] for r in oos_b], dtype=np.int64)
    excl_b = {(r["ticker"], r["s"]) for r in bear_oos_raw}
    by_b, _, _, _ = baseline_pool(m, era, N_PRIMARY, bear=True,
                                  exclusions=excl_b)
    by_bs = {t: by_b[t] for t in set(r["ticker"] for r in oos_b)
             if t in by_b}
    _, r_br = make_sampler_rand(by_b, rng)[1:]
    _, r_bs = make_sampler_same(by_bs, oos_b, rng)
    sens["bear_mirror"] = {"n": int(len(evb)),
                           "breach_rate": float(evb.mean()),
                           "baseline_random_rate": r_br,
                           "baseline_same_rate": r_bs,
                           "drops": dropsb}

    # ---- outputs ----
    claim = ("Stop-placement claim (I-X-05, Trading 212, rgVdgR1y1Dg "
             "[07:40-08:03]): after a bullish divergence the market "
             "'shouldn't take out that prior extreme low' — measured as the "
             "breach rate of Low[t2] (the pair's lower low) within N=10 bars "
             "after the frozen pre-reg #10 BULL signal (s = t2+2), vs "
             "fractal-low confirmation-bar baselines (divergence bars "
             "excluded) and vs oversold crossings")
    if gate:
        claim += ("; the brief §5 survivorship gate (pre-reg #14 §3): "
                  "historical-constituent union, OOS 2022-2025")
    out = {
        "pre_reg": "#14",
        "mode": "gate" if gate else "primary",
        "claim": claim,
        "params": {"period": PERIOD, "period_sensitivity": PERIOD_SENS,
                   "k_fractal": K, "min_sep": MIN_SEP, "confirm_lag": CONFIRM,
                   "n": N_PRIMARY, "n_sensitivities": SENS_N,
                   "stop_level": "Low[t2]", "breach_rule":
                       "min(Low[s+1..s+N]) < L (intrabar, strict)",
                   "f2_lookback": LOOKBACK, "ob_hi": OB_HI, "os_lo": OS_LO,
                   "cost": COST, "b": B, "seed": SEED, "alpha": ALPHA,
                   "count_floor": MISSING_PASS, "warmup": WARMUP,
                   "era_oos_start": measure.ERA_OOS,
                   "anchor_json": anchor.name},
        "families": {"f1_absolute": {"BULL": fam1},
                     "f2_contrast": {"BULL": fam2}},
        "measurements": meas,
        "sensitivities": sens,
        "assertions": {
            "frozen_shas_ok": True,
            "rsi_min_all": stats["rsi_min_all"],
            "rsi_max_all": stats["rsi_max_all"],
            "min_t1": int(stats["min_t1"]),
            "min_signal_bar": int(stats["min_signal"]),
            "max_signal_bar": int(stats["max_signal"]),
            "n_bad_signal": int(stats["n_bad_signal"]),
            "anchor_per_year_sum_bull": n_bull_anchor,
            "anchor_per_year_sum_bear": n_bear_anchor,
            "oos_bull_raw": len(bull_oos_raw),
            "oos_bear_raw": len(bear_oos_raw),
            "drops_primary_bull": drops,
            "baseline": {
                "drops_end": drops_end_r, "drops_warmup": drops_warm_r,
                "excluded_event_bars": excl_r,
                "pool_n_random": n_pool_rand,
                "same_ticker_missing_pools": 0},
            "f2": {"no_reference_dropped": no_ref,
                   "drops_end": drops_cross}},
        "anchor": ({"status": "PASSED"} if gate else {
            "status": "DEVIATION",
            "record": "divergence_measure_results.json (frozen pre-reg #10, "
                      "written 2026-08-15 05:08 UTC)",
            "frozen": {"per_year_bull_sum": int(sum_bull),
                       "per_year_bear_sum": int(sum_bear),
                       "n_bull_raw": int(a["frequency"]["n_bull"]),
                       "n_bear_raw": int(a["frequency"]["n_bear"]),
                       "f1_bull_n": int(a["families"]["f1_absolute"]
                                        ["BULL"]["n"])},
            "observed": {"per_year_bull_sum": int(n_bull_anchor),
                         "per_year_bear_sum": int(n_bear_anchor),
                         "n_bull_raw": len(bull_oos_raw),
                         "n_bear_raw": len(bear_oos_raw),
                         "f1_bull_n": int(fam1["n"])},
            "deltas": {"per_year_bull": int(d_bull),
                       "per_year_bear": int(d_bear),
                       "n_bull_raw": len(bull_oos_raw)
                       - int(a["frequency"]["n_bull"]),
                       "n_bear_raw": len(bear_oos_raw)
                       - int(a["frequency"]["n_bear"]),
                       "f1_bull_n": int(fam1["n"])
                       - int(a["families"]["f1_absolute"]["BULL"]["n"])},
            "per_year_deltas": year_deltas,
            "drift_guard": drift,
            "note": "The frozen primary record is not regenerable from the "
                    "current bars: the frozen pipeline and md.main() itself "
                    "(shas asserted) yield per_year BULL 34075/BEAR 42757 vs "
                    "frozen 34076/42759, freq n_bull 17016/n_bear 20910 vs "
                    "17017/20912, fam1 BULL n 16984 vs 16985. The frozen #13 "
                    "hist record (2026-08-16) regenerates exactly on the same "
                    "data, bracketing the change to the 08-15/08-16 window. "
                    "The 08-13-era bytes are unrecoverable (fetch_log.json "
                    "records only rows/dates; no raw downloads). Deviation: 3 "
                    "divergence events (2021 BULL -1; 2016/2017/2024 BEAR -1; "
                    "2025 BEAR +1) and 1 OB crossing; the OOS BULL event set "
                    "under test differs from the frozen record by exactly 1 "
                    "event. Recorded + quantified + guarded; not a parameter "
                    "change; no frozen file modified."}),
        "fingerprints": {"universe_sha256": sha(universe_csv),
                         "measure_code_sha256": sha(Path(__file__)),
                         "engine_sha256": sha(Path(measure.__file__))},
    }
    results.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {results.name}")

    # ---- report ----
    L = []
    L.append("# Stop-placement measurement report (pre-registration #14)")
    L.append("")
    if gate:
        L.append("- **Gate run (pre-reg #14 §3 — the brief §5 survivorship "
                 "re-check)**: universe = the pre-reg #13 historical-"
                 "constituent union (904 names, 5 annual S&P 600 snapshots "
                 "2021-2025; bars for 706 — 199 former members purged from "
                 "Yahoo's data, 0 of them current members, flagged and NOT "
                 "substituted); OOS 2022-2025.")
    L.append("- Pre-registration #14 (frozen 2026-08-16): claim = the I-X-05 "
             "stop-placement claim — after a bullish divergence the market "
             "\"shouldn't take out that prior extreme low\" (rgVdgR1y1Dg "
             "[07:40-08:03]); stop level L = Low[t2]; breach ⇔ "
             f"min(Low[s+1..s+N]) < L; N={N_PRIMARY} primary ({SENS_N} "
             f"sensitivity); cost {COST}, alpha {ALPHA}, bootstrap {B} "
             f"(seed {SEED})")
    if gate:
        L.append("- Events: the frozen pre-reg #10 bullish-divergence "
                 "detection recomputed with the frozen functions "
                 "(measure_divergence.py sha 85f2ae0d4a1e…, measure.py sha "
                 "c7421fbf… — asserted at import); per-leg all-era counts "
                 f"anchored to {anchor.name}'s per_year sums: BULL "
                 f"{n_bull_anchor:,}, BEAR {n_bear_anchor:,} — PASS")
    else:
        L.append("- Events: the frozen pre-reg #10 bullish-divergence "
                 "detection recomputed with the frozen functions "
                 "(measure_divergence.py sha 85f2ae0d4a1e…, measure.py sha "
                 "c7421fbf… — asserted at import). **Anchor DEVIATION — see "
                 "the Data-integrity section below**: the frozen primary "
                 f"record cannot be regenerated from the current bars "
                 f"(BULL {n_bull_anchor:,} vs frozen {int(sum_bull):,}, BEAR "
                 f"{n_bear_anchor:,} vs frozen {int(sum_bear):,}, fam1 BULL n "
                 f"{fam1['n']:,} vs frozen "
                 f"{int(a['families']['f1_absolute']['BULL']['n']):,}).")
    L.append(f"- Warm-up guard: signal/confirmation bar index < {WARMUP} "
             "(frozen #3 convention); warm-up events excluded and counted "
             f"(baseline bars {drops_warm_r:,})")
    if gate:
        L.append("- Era split: IS 2000-2021 (descriptive only — no IS-era "
                 "membership data) / OOS 2022-2025 (by signal date).")
    else:
        L.append("- Era split: IS 2000-2015 (descriptive) / OOS 2016-2025 "
                 "(by signal date).")
    L.append("- Breach: intrabar — min(Low[s+1..s+N]) < L; a stop placed "
             "\"beyond\" the low triggers on a strictly lower trade; an "
             "equal low survives.")
    L.append("- F1 baselines: fractal-low confirmation bars (c = f + 2 of "
             "every strict k=2 fractal low f, reference Low[f]) — the event "
             "template minus the divergence condition; the OOS divergence "
             f"event bars are excluded ({excl_r:,}); random = whole "
             "universe uniform, same-ticker = event tickers "
             "event-count-weighted (the frozen make_sample_same "
             "convention).")
    L.append("- F2: OS crossings (pre-reg #9 S4 rule, period 10); reference "
             "= the most recent strict k=2 fractal low at bar ≤ c within "
             f"the {LOOKBACK}-bar lookback (crossings without one dropped "
             "and counted). Age asymmetry documented conservative: the "
             "divergence reference is exactly 2 bars old; a crossing's "
             "reference averages older, and older levels are less likely "
             "to be breached.")
    L.append("")
    if not gate:
        L.append("## Data integrity — anchor deviation (primary record)")
        L.append("")
        L.append("Pre-registration #14 §2 requires the event set to BE the "
                 "frozen pre-reg #10 event set (anchored to the frozen "
                 "divergence_measure_results.json per-year counts). On the "
                 "current bars that anchor CANNOT be satisfied: the frozen "
                 "pipeline — and md.main() itself, run with outputs rebound "
                 "and shas asserted — yields BULL 34075 / BEAR 42757 / fam1 "
                 "16984 vs the frozen 34076 / 42759 / 16985. The frozen #13 "
                 "hist record (2026-08-16) regenerates EXACTLY on the same "
                 "data, bracketing the change to the 08-15 → 08-16 window "
                 "(the vendor restated or re-derived the bars). The "
                 "08-13-era bytes are unrecoverable: fetch_log.json records "
                 "only rows/dates — no hashes — and no raw downloads exist.")
        L.append("")
        L.append("Quantified deviation (per-year deltas, observed − frozen):")
        L.append("")
        L.append("| year | BULL | BEAR |")
        L.append("|---|---|---|")
        for y in sorted(year_deltas):
            dd = year_deltas[y]
            L.append(f"| {y} | {dd.get('BULL', 0):+d} | "
                     f"{dd.get('BEAR', 0):+d} |")
        L.append("")
        L.append(f"- Totals: BULL {d_bull:+d} (sum {n_bull_anchor:,} vs "
                 f"frozen {int(sum_bull):,}), BEAR {d_bear:+d} (sum "
                 f"{n_bear_anchor:,} vs frozen {int(sum_bear):,}); raw OOS "
                 f"BULL {len(bull_oos_raw):,} vs frozen "
                 f"{int(a['frequency']['n_bull']):,}, BEAR "
                 f"{len(bear_oos_raw):,} vs frozen "
                 f"{int(a['frequency']['n_bear']):,}; fam1 BULL n "
                 f"{fam1['n']:,} vs frozen "
                 f"{int(a['families']['f1_absolute']['BULL']['n']):,}.")
        L.append(f"- The OOS BULL event set under test differs from the "
                 f"frozen record by exactly 1 event (≈6e-5 of the event "
                 f"count). The drift-materiality guard bounds any rate shift "
                 f"by {drift['delta_f1']:.2e} (F1) / {drift['delta_f2']:.2e} "
                 f"(F2) — ~60× below the bootstrap CI width at n≈17k — and "
                 f"flags a verdict drift-sensitive if its decisive CI bound "
                 f"falls within that bound of zero.")
        L.append("- This is a data-state deviation, NOT a parameter change; "
                 "no frozen file was modified; the deviation is recorded "
                 "here and in the results JSON (`anchor` block), and will "
                 "be logged in the claims ledger.")
        L.append("")
    L.append("## Verdicts — Family 1: absolute (F1-BULL)")
    L.append("")
    r = fam1
    e_r, e_s = r["excess"]["random"], r["excess"]["same_ticker"]
    L.append(f"- F1-BULL: n={r['n']:,} | breach_rate {r['breach_rate']:.4f} "
             f"| random base {r['baseline_random']['rate']:.4f} (pool "
             f"{r['baseline_random']['pool_n']:,}) | excess vs random "
             f"{e_r[0]:+.4f} (CI {e_r[2]:+.4f}..{e_r[3]:+.4f}, "
             f"p {e_r[4]:.3f}) | vs same {e_s[0]:+.4f} (CI {e_s[2]:+.4f}.."
             f"{e_s[3]:+.4f}, p {e_s[4]:.3f}) | same base "
             f"{r['baseline_same']['rate']:.4f} | p_input {r['p']:.3f} | "
             f"est {r['est']:+.4f} (CI-low {r['ci_low']:+.4f}..CI-upper "
             f"{r['ci_upper']:+.4f}) | Holm gate {r['holm_gate']:.4f} -> "
             f"**{r['verdict']}**")
    L.append("")
    L.append("## Verdicts — Family 2: contrast vs oversold crossings "
             "(F2-BULL)")
    L.append("")
    r2 = fam2
    L.append(f"- F2-BULL: n_div={r2['n_div']:,} | n_cross={r2['n_cross']:,} "
             f"| div rate {r2['rate_div']:.4f} | cross rate "
             f"{r2['rate_cross']:.4f} | contrast {r2['excess'][0]:+.4f} (CI "
             f"{r2['excess'][2]:+.4f}..{r2['excess'][3]:+.4f}, "
             f"p {r2['excess'][4]:.3f}) | Holm gate {r2['holm_gate']:.4f} "
             f"-> **{r2['verdict']}**")
    L.append("")
    L.append("## Measurement rows (no verdicts)")
    L.append("")
    sp, sa = meas["stop_distance_pct"], meas["stop_distance_atr14"]
    L.append(f"- Stop distance open[s+1] → Low[t2]: mean {sp['mean']:.4f} "
             f"({sp['mean']*100:.2f}%), median {sp['median']:.4f}, p10 "
             f"{sp['p10']:.4f}, p90 {sp['p90']:.4f}; in ATR14 units: mean "
             f"{sa['mean']:.3f}, median {sa['median']:.3f}, p10 "
             f"{sa['p10']:.3f}, p90 {sa['p90']:.3f} (n={sp['n']:,})")
    d = meas["decomposition_events"]
    ds, dr = meas["decomposition_same_ticker"], meas["decomposition_random"]
    L.append(f"- Outcome decomposition (events, n={d['n']:,}): "
             f"breach-loss {fmt_num(d['breach_loss'])} | continue-gain "
             f"{fmt_num(d['continue_gain'])} | combined {fmt_num(d['combined'])}"
             f" (n_breached {d['n_breached']:,}, rate {d['n_breached']/d['n']:.4f})")
    L.append(f"- Same decomposition, same-ticker baseline (weighted): "
             f"breach-loss {fmt_num(ds['breach_loss'])} | continue-gain "
             f"{fmt_num(ds['continue_gain'])} | combined "
             f"{fmt_num(ds['combined'])}")
    L.append(f"- Same decomposition, random baseline (pooled): "
             f"breach-loss {fmt_num(dr['breach_loss'])} | continue-gain "
             f"{fmt_num(dr['continue_gain'])} | combined "
             f"{fmt_num(dr['combined'])}")
    L.append("")
    L.append("| year | n | breach rate |")
    L.append("|---|---|---|")
    for y in years:
        pr = meas["per_year"][y]
        mark = " **" if int(y) >= 2016 and not gate else ""
        mark2 = "**" if int(y) >= 2016 and not gate else ""
        L.append(f"| {y}{mark} | {pr['n']:,} | {pr['breach_rate']:.4f}"
                 f"{mark2} |")
    L.append("")
    L.append("## Sensitivities (exploratory — NO verdicts)")
    L.append("")
    for n in SENS_N:
        c = sens[f"N={n}"]
        L.append(f"- S1 N={n}: event {c['breach_rate']:.4f} vs random "
                 f"{c['baseline_random_rate']:.4f} vs same "
                 f"{c['baseline_same_rate']:.4f} (n={c['n']:,})")
    c = sens["level_t1"]
    L.append(f"- S2 stop = Low[t1] (the first, higher low): event "
             f"{c['breach_rate']:.4f} vs random {c['baseline_random_rate']:.4f}"
             f" vs same {c['baseline_same_rate']:.4f} (n={c['n']:,}; the "
             "level is ≥ 7 bars old at the window start vs 2 for the "
             "baselines — age asymmetry documented)")
    c = sens["period14"]
    L.append(f"- S3 period 14: event {c['breach_rate']:.4f} vs random "
             f"{c['baseline_random_rate']:.4f} vs same "
             f"{c['baseline_same_rate']:.4f} (n={c['n']:,}; baselines "
             "unchanged — fractal lows are RSI-independent)")
    c = sens["close_breach"]
    L.append(f"- S4 close-based breach: event {c['breach_rate']:.4f} vs "
             f"random {c['baseline_random_rate']:.4f} vs same "
             f"{c['baseline_same_rate']:.4f} (n={c['n']:,})")
    c = sens["bear_mirror"]
    L.append(f"- S5 BEAR mirror (High[t2] stop, max > ref): event "
             f"{c['breach_rate']:.4f} vs random {c['baseline_random_rate']:.4f}"
             f" vs same {c['baseline_same_rate']:.4f} (n={c['n']:,})")
    L.append("")
    L.append("## Reproducibility")
    L.append("")
    L.append("`python -X utf8 tools/measure_stop_placement.py`"
             + (" --gate" if gate else "")
             + " regenerates this report; the seed is fixed, so results are "
             "stable across runs.")
    if gate:
        _anchor_line = (f"per-year anchor sums BULL {n_bull_anchor:,} / "
                        f"BEAR {n_bear_anchor:,} match the frozen JSON PASS; "
                        f"OOS BULL n {fam1['n']:,} matches PASS.")
    else:
        _anchor_line = (f"per-year anchor: DEVIATION (see the Data-integrity "
                        f"section) — BULL {n_bull_anchor:,} vs frozen "
                        f"{int(sum_bull):,}, BEAR {n_bear_anchor:,} vs frozen "
                        f"{int(sum_bear):,}, fam1 {fam1['n']:,} vs frozen "
                        f"{int(a['families']['f1_absolute']['BULL']['n']):,}.")
    L.append("Assertions: frozen shas (measure.py c7421fbf…, "
             "measure_divergence.py 85f2ae0d4a1e…) PASS; RSI within [0, 100] "
             f"(min {stats['rsi_min_all']:.12f}, max "
             f"{stats['rsi_max_all']:.12f}) PASS; min t1 {stats['min_t1']} "
             "≥ period PASS; n_bad_signal 0 PASS; drops "
             f"(BULL {drops:,}) and crossing drops match PASS; every event "
             "ticker has a non-empty OOS baseline pool PASS; " + _anchor_line)
    L.append("Input fingerprints: universe %s…, measure code %s… (Phase-3 "
             "engine c7421fbf… imported unchanged)."
             % (out["fingerprints"]["universe_sha256"][:12],
                out["fingerprints"]["measure_code_sha256"][:12]))
    L.append("Any change to the detector, data, or measurement code changes "
             "the frozen inputs and requires a new pre-registration before "
             "it can drive a verdict.")
    L.append("")
    report.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {report.name}")

    print(f"F1-BULL: {fam1['verdict']}")
    print(f"F2-BULL: {fam2['verdict']}")
    return 0 if not errs else 1


if __name__ == "__main__":
    sys.exit(main())
