"""E-03 leg attachment for pre-registration #6 (ledger E-03), frozen 2026-08-14.

Reads the frozen shape detections (data/cache/detections_v1.csv, pre-reg #2,
manifest e93ddf7a...) and attaches the E-03 legs at each signal day t (all
legs use data <= t only — no look-ahead):

  hist          = MACD(12,26,9) histogram at t (line - signal)
  bear_cross    = a BEARISH SIGNAL-LINE crossover within L bars before t:
                  exists k in [1, L] with hist_{t-k} < 0 and hist_{t-k-1} >= 0
                  ("when the MACD actually crosses... any attempt to break
                  out will reject" — E-03; cross strictly precedes the signal)
  bull_cross    = the opposite reading (hist crosses up) — sensitivity only
  zero_cross    = the pre-reg #3 zero-line reading (line crosses < 0) within
                  the window — sensitivity only, already measured in #3
  bear_regime   = SPY close < SPY 200-day simple moving average at t (the
                  pre-registered regime variable: "especially during the
                  bear market"); NaN where SPY history < 200 bars (pre-2000-11,
                  IS only) — excluded from the F2 regime family, counted

MACD on adjusted closes with ewm(adjust=False), standard (12,26,9) — identical
machinery to tools/veto.py. Warm-up guard (pre-reg #6 §1): detections at bar
index < 60 from series start are excluded from the campaign and flagged.

L = 20 primary; L = 5 is a pre-declared sensitivity re-subset of the same
leg columns (the stored hist series make re-windowing a pure re-read), so
only L = 20 and the cross-event flags are computed here.

Output: data/cache/e03_detections_v1.csv (frozen columns + leg columns) plus
a manifest (input detections sha, code sha, params). Deterministic: same data
+ same code = byte-identical output.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
BARS_DIR = CACHE / "bars"
DET_CSV = CACHE / "detections_v1.csv"
OUT_CSV = CACHE / "e03_detections_v1.csv"

PARAMS = {"macd": {"fast": 12, "slow": 26, "signal": 9},
          "cross_lookback": 20, "warmup_bars": 60,
          "regime_sma": 200, "regime_proxy": "SPY"}

_bars: dict = {}
_hist_c: dict = {}
_line_c: dict = {}


def bars(ticker: str) -> pd.DataFrame:
    if ticker not in _bars:
        df = pd.read_parquet(BARS_DIR / f"{ticker}.parquet")
        df.index = pd.to_datetime(df.index)
        _bars[ticker] = df.sort_index()
    return _bars[ticker]


def macd_line(c: pd.Series) -> pd.Series:
    """MACD line (fast-slow EMA difference), ewm(adjust=False)."""
    f, s = PARAMS["macd"]["fast"], PARAMS["macd"]["slow"]
    return c.ewm(span=f, adjust=False).mean() - c.ewm(span=s, adjust=False).mean()


def macd_hist(c: pd.Series) -> pd.Series:
    """MACD histogram = line - signal, standard (12,26,9)."""
    sg = PARAMS["macd"]["signal"]
    line = macd_line(c)
    return line - line.ewm(span=sg, adjust=False).mean()


def _hist_cache(t: str, c: pd.Series) -> pd.Series:
    if t not in _hist_c:
        _hist_c[t] = macd_hist(c)
    return _hist_c[t]


def _line_cache(t: str, c: pd.Series) -> pd.Series:
    if t not in _line_c:
        _line_c[t] = macd_line(c)
    return _line_c[t]


def regime_at(spy: pd.DataFrame, ts: pd.Timestamp):
    """bear (SPY < SMA200 at t) / False / None where SMA undefined."""
    loc = {x: j for j, x in enumerate(spy.index)}.get(ts)
    if loc is None:
        return None
    if loc < PARAMS["regime_sma"] - 1:
        return None
    close = spy["Close"].iloc[loc]
    sma = float(spy["Close"].iloc[loc - PARAMS["regime_sma"] + 1: loc + 1].mean())
    return bool(close < sma)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limit", type=int, default=0, help="first N detections only (test)")
    args = ap.parse_args()

    det = pd.read_csv(DET_CSV)
    if args.limit:
        det = det.head(args.limit)

    spy = bars(PARAMS["regime_proxy"])
    L = PARAMS["cross_lookback"]
    rows = []
    loc_cache: dict = {}
    n_warmup, n_no_regime = 0, 0
    for i, r in det.iterrows():
        t, ts = r["ticker"], pd.Timestamp(r["signal_date"])
        df = bars(t)
        if t not in loc_cache:
            loc_cache[t] = {x: j for j, x in enumerate(df.index)}
        loc = loc_cache[t].get(ts)
        if loc is None:
            continue  # cannot happen; guarded
        warmup = loc < PARAMS["warmup_bars"]
        n_warmup += int(warmup)
        if warmup:
            rows.append({**r.to_dict(), "warmup": True, "hist": None,
                         "bear_cross": False, "bull_cross": False,
                         "zero_cross": False, "bear_regime": None})
            continue

        hist = _hist_cache(t, df["Close"]).to_numpy()
        line = _line_cache(t, df["Close"]).to_numpy()
        # k in [1, L]: cross at t-k (state_{t-k-1} >= 0 -> state_{t-k} < 0)
        bear = any(hist[loc - k - 1] >= 0.0 and hist[loc - k] < 0.0
                   for k in range(1, L + 1))
        bull = any(hist[loc - k - 1] <= 0.0 and hist[loc - k] > 0.0
                   for k in range(1, L + 1))
        # zero-line reading (pre-reg #3 sensitivity): line crosses < 0
        zero = any(line[loc - k - 1] >= 0.0 and line[loc - k] < 0.0
                   for k in range(1, L + 1))

        reg = regime_at(spy, ts)
        n_no_regime += int(reg is None)

        rows.append({**r.to_dict(), "warmup": False, "hist": float(hist[loc]),
                     "bear_cross": bear, "bull_cross": bull,
                     "zero_cross": zero, "bear_regime": reg})

    out = pd.DataFrame(rows).sort_values(["shape", "ticker", "signal_date"]) \
                             .reset_index(drop=True)
    OUT_CSV.write_bytes(out.to_csv(index=False).encode("utf-8"))

    manifest = {
        "pre_reg": "#6",
        "e03_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_detections_sha256": hashlib.sha256(DET_CSV.read_bytes()).hexdigest(),
        "params": PARAMS,
        "run_date": str(pd.Timestamp.now().date()),
        "n_rows": int(len(out)), "n_warmup_excluded": int(n_warmup),
        "n_regime_undefined": int(n_no_regime),
    }
    OUT_CSV.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"wrote {OUT_CSV.name}: {len(out)} rows (warmup-excluded {n_warmup}, "
          f"regime-undefined {n_no_regime})")
    sub = out[out["warmup"] == False]
    for s in "ABC":
        d = sub[sub["shape"] == s]
        print(f"  {s}: {len(d)} detections | bear-cross {int(d['bear_cross'].sum())} "
              f"({int(d['bear_cross'].sum()) / max(len(d), 1):.1%}) | "
              f"bull-cross {int(d['bull_cross'].sum())} | "
              f"zero-cross {int(d['zero_cross'].sum())} | "
              f"bear-regime {int((d['bear_regime'] == True).sum())}")
    print(f"  manifest: {OUT_CSV.with_suffix('.manifest.json').name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
