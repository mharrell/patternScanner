"""Phase 2: shape detectors A/B/C (DESIGN_BRIEF §4, operationalized).

Detections only — no returns, no baselines, no verdicts (that is Phase 3).

Reads raw adjusted OHLCV parquets under data/cache/bars/ and writes
data/cache/detections_v1.csv. Deterministic: same data + same code =
byte-identical output (verified in data/cache/detections_report.md).

Operationalization notes (judgment calls, to be locked in pre-reg #2):
  A  consolidation band is close-based: lo/hi = min/max of the K setup
     closes ending at t-1. (An intraday-band variant would be exploratory.)
  B  pullback requires a net decline across the P bars (c_{t-1} < c_{t-P});
     "K-day high" = max of the previous K highs, bar t excluded.
  C  swing low = center-window minimum (2S+1 bars, min_periods=1 at the
     series edges); a pattern signals only after L2 is confirmed (bar b2+S),
     so the entry is honest at t+1; peak P = max high between the lows and
     must exceed both lows; one signal per pattern.

Parameters (DRAFT — final values pre-registered before any measurement):
  A: K=10, W=0.05, V=2.0      B: M=20, T=5, P=3, K=20      C: S=5, D=5, X=0.03
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
BARS_DIR = CACHE / "bars"
DETECTOR_VERSION = "v1"

# Draft parameter sets (DESIGN_BRIEF §4 placeholders).
PARAMS = {
    "A": {"K": 10, "W": 0.05, "V": 2.0},
    "B": {"M": 20, "T": 5, "P": 3, "K": 20},
    "C": {"S": 5, "D": 5, "X": 0.03},
}
VOL_LOOKBACK = 20  # volume leg: mean of the *prior* 20 bars


def _vol_ratio_ok(v: pd.Series, mult: float) -> pd.Series:
    """v_t >= mult * mean(v, prior 20). Guard: mean must be > 0 (a 0/0
    must fail, per the pre-2008 zero-volume artifact documentation)."""
    mean = v.rolling(VOL_LOOKBACK).mean().shift(1)
    return (v >= mult * mean) & (mean > 0)


def detect_a(c: pd.Series, v: pd.Series, K: int, W: float, V: float):
    """Consolidation breakout.

    setup : the K closes ending at t-1 span [lo, hi] with (hi-lo)/lo <= W
    signal: c_t > hi AND v_t >= V * mean(v, prior 20)
    """
    lo = c.rolling(K).min().shift(1)
    hi = c.rolling(K).max().shift(1)
    range_ok = ((hi - lo) / lo <= W) & (lo > 0)
    sig = (c > hi) & range_ok & _vol_ratio_ok(v, V)
    return sig.fillna(False), hi, lo


def detect_b(c: pd.Series, h: pd.Series, M: int, T: int, P: int, K: int):
    """Pullback to trend.

    setup    : the T closes ending at t-P-1 are all above the M-day SMA
    pullback : closes t-P..t-1 all above the M-day SMA, with a net decline
               (c_{t-1} < c_{t-P} — price fell toward the MA)
    signal   : c_t > max(h, previous K bars)  [first close above the K-day high]
    """
    sma = c.rolling(M).mean()
    above = c > sma
    uptrend = above.rolling(T).min() == 1  # >= T consecutive above, ends t-P-1
    uptrend_ok = uptrend.shift(P + 1).fillna(False)
    pullback_ok = (above.rolling(P).min() == 1).shift(1).fillna(False)
    declined = c.shift(1) < c.shift(P)  # close at end of pullback < start
    new_high = c > h.rolling(K).max().shift(1)  # above previous K highs
    sig = uptrend_ok & pullback_ok & declined & new_high
    return sig.fillna(False), sma, h.rolling(K).max().shift(1)


def detect_c(c: pd.Series, h: pd.Series, l: pd.Series, S: int, D: int, X: float):
    """Double bottom.

    swing low : l_i equals the rolling min over a 2S+1 center window
    setup     : swing lows L1 (b1) and L2 (b2), b2-b1 >= D, |L1-L2|/L1 <= X,
                peak P = max(h, b1..b2) with P > max(L1, L2)
    signal    : first close > P at t >= b2+S (L2 confirmed — no look-ahead),
                before the next swing low forms. One signal per pattern.
    """
    n = len(c)
    roll_min = l.rolling(2 * S + 1, center=True, min_periods=1).min()
    swing_idx = [i for i in range(n) if l.iloc[i] <= roll_min.iloc[i]]
    dets = []
    i1 = 0
    while i1 < len(swing_idx):
        b1 = swing_idx[i1]
        l1 = l.iloc[b1]
        i2 = i1 + 1
        while i2 < len(swing_idx):
            b2 = swing_idx[i2]
            l2 = l.iloc[b2]
            if b2 - b1 < D:  # too close: keep L1, try the next L2
                i2 += 1
                continue
            if abs(l1 - l2) / l1 > X:  # depth diverged: keep L1, try next L2
                i2 += 1
                continue
            peak = h.iloc[b1 : b2 + 1].max()
            if peak <= max(l1, l2):  # no rise between lows — not a W
                i2 += 1
                continue
            # Pattern formed at b2; signal from b2+S (L2 confirmed), until
            # the next swing low replaces this pattern.
            end = swing_idx[i2 + 1] if i2 + 1 < len(swing_idx) else n
            for t in range(max(b2 + S, b2 + 1), end):
                if c.iloc[t] > peak:
                    dets.append({"b1": b1, "b2": b2, "l1": l1, "l2": l2,
                                 "peak": peak, "bar": t})
                    break
            i1 = i2  # chain: L2 becomes the next L1
            break
        if i2 >= len(swing_idx):
            break
    return dets


def detect_ticker(ticker: str, p: Path) -> list[dict]:
    df = pd.read_parquet(p).sort_index()
    c, h, l, v = df["Close"], df["High"], df["Low"], df["Volume"]
    last = df.index[-1]
    out = []

    sig_a, hi, lo = detect_a(c, v, **PARAMS["A"])
    if sig_a.any():
        vmean = v.rolling(VOL_LOOKBACK).mean().shift(1)
        for t in sig_a[sig_a].index:
            if t >= last:
                continue  # entry bar (open of t+1) must exist
            ti = df.index.get_loc(t)
            out.append({"shape": "A", "ticker": ticker,
                        "signal_date": str(t.date()),
                        "signal_close": float(c.loc[t]),
                        "entry_open": float(df["Open"].iloc[ti + 1]),
                        "detail": json.dumps({
                            "hi": float(hi.loc[t]), "lo": float(lo.loc[t]),
                            "vol_ratio": float(v.loc[t] / vmean.loc[t]),
                        })})

    sig_b, sma, kh = detect_b(c, h, **PARAMS["B"])
    if sig_b.any():
        for t in sig_b[sig_b].index:
            if t >= last:
                continue
            ti = df.index.get_loc(t)
            out.append({"shape": "B", "ticker": ticker,
                        "signal_date": str(t.date()),
                        "signal_close": float(c.loc[t]),
                        "entry_open": float(df["Open"].iloc[ti + 1]),
                        "detail": json.dumps({
                            "kday_high": float(kh.loc[t]),
                            "sma": float(sma.loc[t]),
                        })})

    for d in detect_c(c, h, l, **PARAMS["C"]):
        t = df.index[d["bar"]]
        if t >= last:
            continue
        ti = df.index.get_loc(t)
        out.append({"shape": "C", "ticker": ticker,
                    "signal_date": str(t.date()),
                    "signal_close": float(c.loc[t]),
                    "entry_open": float(df["Open"].iloc[ti + 1]),
                    "detail": json.dumps({
                        "b1": str(df.index[d["b1"]].date()), "l1": float(d["l1"]),
                        "b2": str(df.index[d["b2"]].date()), "l2": float(d["l2"]),
                        "peak": float(d["peak"]),
                    })})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--universe", type=Path,
                    default=CACHE / "universe_sp600_2026-08-13.csv")
    ap.add_argument("--out", type=Path, default=CACHE / "detections_v1.csv")
    ap.add_argument("--limit", type=int, default=0, help="first N tickers only (test)")
    ap.add_argument("--shapes", default="ABC", help="subset of shapes to run")
    args = ap.parse_args()

    uni = pd.read_csv(args.universe)
    tickers = uni["ticker"].tolist()
    if args.limit:
        tickers = tickers[: args.limit]
    shapes = set(args.shapes)

    rows = []
    n_skip = 0
    for t in tickers:
        p = BARS_DIR / f"{t}.parquet"
        if not p.exists():
            n_skip += 1
            continue
        for r in detect_ticker(t, p):
            if r["shape"] in shapes:
                r["params"] = json.dumps(PARAMS[r["shape"]], sort_keys=True)
                rows.append(r)

    out = pd.DataFrame(rows)
    if len(out):
        out = out.sort_values(["shape", "ticker", "signal_date"]).reset_index(drop=True)
    out.to_csv(args.out, index=False)

    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest = {
        "detector_version": DETECTOR_VERSION,
        "detector_file_sha256": sha,
        "params": PARAMS,
        "run_date": str(pd.Timestamp.now().date()),
        "bars_dir": str(BARS_DIR.relative_to(ROOT)),
        "universe": args.universe.name,
        "shapes_run": sorted(shapes),
    }
    (args.out.with_suffix(".manifest.json")).write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")

    counts = out.groupby("shape").size() if len(out) else pd.Series(dtype=int)
    print(f"wrote {args.out.name}: {len(out)} detections"
          f" ({', '.join(f'{k}:{v}' for k, v in counts.items()) or 'none'})")
    print(f"  tickers skipped (no parquet): {n_skip}")
    print(f"  manifest: {args.out.with_suffix('.manifest.json').name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
