"""Pillar detector for pre-registration #1, hypotheses H1-H3 (frozen 2026-08-13).

Detections only — no returns, no baselines, no verdicts (that is the
measurement stage). Reads raw adjusted OHLCV parquets under data/cache/bars/
plus the frozen universe snapshot (float_shares) and writes
data/cache/pillar_detections_v1[.high/.r210].csv. Deterministic: same data +
same code = byte-identical output.

Hypotheses (pre-reg #1 §2, exact legs):
  H1  $2 <= c_t <= $20  AND  c_t/c_{t-1} - 1 >= 0.30  AND
      v_t >= 5 * mean(v, prior 20)  AND  floatShares <= 10M
  H2  $1 <= c_t <= $10  AND  c_t/c_{t-1} - 1 >= 0.25  AND
      v_t >= 10 * mean(v, prior 20)  AND  floatShares <= 10M  AND
      daily %-gain rank <= 3 in U
  H3  membership in the daily rank-1 %-gainer cohort of U (unconditional of
      the other filters, per §2); the rank-2..10 cohort is written to a
      companion file for the direct claim test.

Operationalization notes (fixed here, part of the frozen spec):
  - gain leg is close-to-close by default ("still up at close" — the
    stronger subset per the translation table); the high-based trigger
    (h_t >= 1.30/1.25 * c_{t-1}) is the pre-declared --trigger high
    sensitivity.
  - volume leg is identical to detectors.py: mean of the *prior* 20 bars
    (shifted), and a 0/0 must fail (pre-2008 zero-volume artifact).
  - rank is over the full frozen universe (all tickers with bars on day t);
    per the translation table, this is a stricter reading than his
    pre-filtered scanner universe — documented, not adjusted.
  - float is the frozen snapshot value (universe_sp600_2026-08-13.csv),
    allowed as a static screening filter per DESIGN_BRIEF §9 row 7 (a).
  - signals on a ticker's last bar are skipped (entry open of t+1 must
    exist).
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

PARAMS = {
    "H1": {"price_lo": 2.0, "price_hi": 20.0, "gain": 0.30, "vol_mult": 5.0},
    "H2": {"price_lo": 1.0, "price_hi": 10.0, "gain": 0.25, "vol_mult": 10.0,
           "rank_max": 3},
    "H3": {"rank": 1, "cohort_hi": 10},
    "FLOAT_MAX": 10_000_000,
    "VOL_LOOKBACK": 20,
}
VOL_LOOKBACK = PARAMS["VOL_LOOKBACK"]


def _vol_ratio_ok(v: pd.Series, mult: float) -> pd.Series:
    """v_t >= mult * mean(v, prior 20); 0/0 must fail (same guard as
    detectors.py — pre-2008 zero-volume artifact)."""
    mean = v.rolling(VOL_LOOKBACK).mean().shift(1)
    return (v >= mult * mean) & (mean > 0)


def build_rank(uni_tickers: list[str], trigger: str) -> dict:
    """Daily %-gain rank (1 = top gainer) per ticker, over the full universe.

    Returns {ticker: Series(rank, index=ticker's bars)}.
    """
    closes, highs = {}, {}
    for t in uni_tickers:
        p = BARS_DIR / f"{t}.parquet"
        if not p.exists():
            continue  # 4 known no-data tickers — no bars, no rank
        df = pd.read_parquet(p,
                             columns=["Close"] + (["High"] if trigger == "high" else []))
        closes[t] = df["Close"]
        if trigger == "high":
            highs[t] = df["High"]
    c_frame = pd.DataFrame(closes)
    if trigger == "close":
        pct = c_frame.pct_change()
    else:
        pct = pd.DataFrame(highs) / c_frame.shift(1) - 1.0
    rank = pct.rank(axis=1, method="first", ascending=False)
    return {t: rank.loc[c_frame[t].dropna().index, t]
            for t in uni_tickers if t in c_frame}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--universe", type=Path,
                    default=CACHE / "universe_sp600_2026-08-13.csv")
    ap.add_argument("--trigger", choices=["close", "high"], default="close",
                    help="close-to-close gain leg (primary) or high-based (sensitivity)")
    ap.add_argument("--price-range", choices=["std", "2-10"], default="std",
                    help="H1 price leg $2-20 (primary) or $2-10 sub-range (sensitivity)")
    ap.add_argument("--hypotheses", nargs="+", choices=["H1", "H2", "H3"],
                    default=["H1", "H2", "H3"], help="hypotheses to run")
    ap.add_argument("--limit", type=int, default=0, help="first N tickers only (test)")
    args = ap.parse_args()

    uni = pd.read_csv(args.universe)
    uni_tickers = uni["ticker"].tolist()
    float_map = dict(zip(uni["ticker"], uni["float_shares"]))
    if args.limit:
        uni_tickers = uni_tickers[: args.limit]

    rank = build_rank(uni_tickers, args.trigger)
    hyps = set(args.hypotheses)
    price_h1 = (2.0, 10.0) if args.price_range == "2-10" else \
        (PARAMS["H1"]["price_lo"], PARAMS["H1"]["price_hi"])

    rows, cohort_rows = [], []
    n_skip = 0
    for t in uni_tickers:
        p = BARS_DIR / f"{t}.parquet"
        if not p.exists():
            n_skip += 1
            continue
        df = pd.read_parquet(p).sort_index()
        c, o, h, v = df["Close"], df["Open"], df["High"], df["Volume"]
        f = float_map.get(t)
        float_ok = pd.Series(
            f is not None and pd.notna(f) and f <= PARAMS["FLOAT_MAX"],
            index=df.index)
        last = df.index[-1]

        if args.trigger == "close":
            gain = c / c.shift(1) - 1.0
        else:
            gain = h / c.shift(1) - 1.0
        rank_t = rank[t].reindex(df.index)

        if "H1" in hyps:
            p1 = PARAMS["H1"]
            sig = (c >= price_h1[0]) & (c <= price_h1[1]) & \
                  (gain >= p1["gain"]) & _vol_ratio_ok(v, p1["vol_mult"]) & float_ok
            for t_sig in sig[sig].index:
                if t_sig >= last:
                    continue
                ti = df.index.get_loc(t_sig)
                rows.append({"hypothesis": "H1", "ticker": t,
                             "signal_date": str(t_sig.date()),
                             "signal_close": float(c.loc[t_sig]),
                             "entry_open": float(o.iloc[ti + 1]),
                             "detail": json.dumps({
                                 "gain": float(gain.loc[t_sig]),
                                 "price": float(c.loc[t_sig]),
                                 "vol_ratio": float(
                                     v.loc[t_sig] / v.rolling(VOL_LOOKBACK).mean()
                                     .shift(1).loc[t_sig]),
                                 "float_shares": float(f),
                             }),
                             "params": json.dumps(PARAMS["H1"], sort_keys=True)})

        if "H2" in hyps:
            p2 = PARAMS["H2"]
            sig = (c >= p2["price_lo"]) & (c <= p2["price_hi"]) & \
                  (gain >= p2["gain"]) & _vol_ratio_ok(v, p2["vol_mult"]) & \
                  float_ok & (rank_t <= p2["rank_max"])
            for t_sig in sig[sig].index:
                if t_sig >= last:
                    continue
                ti = df.index.get_loc(t_sig)
                rows.append({"hypothesis": "H2", "ticker": t,
                             "signal_date": str(t_sig.date()),
                             "signal_close": float(c.loc[t_sig]),
                             "entry_open": float(o.iloc[ti + 1]),
                             "detail": json.dumps({
                                 "gain": float(gain.loc[t_sig]),
                                 "price": float(c.loc[t_sig]),
                                 "vol_ratio": float(
                                     v.loc[t_sig] / v.rolling(VOL_LOOKBACK).mean()
                                     .shift(1).loc[t_sig]),
                                 "float_shares": float(f),
                                 "rank": int(rank_t.loc[t_sig]),
                             }),
                             "params": json.dumps(PARAMS["H2"], sort_keys=True)})

        if "H3" in hyps:
            entry = o.shift(-1)  # open of t+1, NaN on the last bar
            rk = rank_t
            day_rank1 = rk == PARAMS["H3"]["rank"]
            for t_sig in day_rank1[day_rank1].index:
                e = entry.loc[t_sig]
                if pd.isna(e):
                    continue  # entry open of t+1 must exist
                rows.append({"hypothesis": "H3", "ticker": t,
                             "signal_date": str(t_sig.date()),
                             "signal_close": float(c.loc[t_sig]),
                             "entry_open": float(e),
                             "detail": json.dumps({
                                 "rank": 1, "gain": float(gain.loc[t_sig]),
                             }),
                             "params": json.dumps(PARAMS["H3"], sort_keys=True)})
            # companion file: all ranks 1..10 on every day (direct claim test)
            in_cohort = rk.between(1, PARAMS["H3"]["cohort_hi"])
            for t_sig in in_cohort[in_cohort].index:
                e = entry.loc[t_sig]
                if pd.isna(e):
                    continue
                cohort_rows.append({"rank": int(rk.loc[t_sig]), "ticker": t,
                                    "signal_date": str(t_sig.date()),
                                    "signal_close": float(c.loc[t_sig]),
                                    "entry_open": float(e)})

    out = pd.DataFrame(rows)
    if len(out):
        out = out.sort_values(["hypothesis", "ticker", "signal_date"]) \
                 .reset_index(drop=True)
    cohorts = pd.DataFrame(cohort_rows)
    if len(cohorts):
        cohorts = cohorts.sort_values(["signal_date", "rank"]) \
                         .reset_index(drop=True)

    suffix = ("_high" if args.trigger == "high" else "") + \
             ("_r210" if args.price_range == "2-10" else "")
    det_path = CACHE / f"pillar_detections_v1{suffix}.csv"
    cohorts_path = CACHE / f"pillar_h3cohorts_v1{suffix}.csv"
    det_path.write_bytes(out.to_csv(index=False).encode("utf-8"))
    cohorts_path.write_bytes(cohorts.to_csv(index=False).encode("utf-8"))

    sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest = {
        "detector_version": DETECTOR_VERSION,
        "detector_file_sha256": sha,
        "params": PARAMS,
        "trigger": args.trigger,
        "price_range": args.price_range,
        "hypotheses_run": sorted(hyps),
        "run_date": str(pd.Timestamp.now().date()),
        "bars_dir": str(BARS_DIR.relative_to(ROOT)),
        "universe": args.universe.name,
    }
    (det_path.with_suffix(".manifest.json")).write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")

    counts = out.groupby("hypothesis").size() if len(out) else pd.Series(dtype=int)
    print(f"wrote {det_path.name}: {len(out)} detections"
          f" ({', '.join(f'{k}:{v}' for k, v in counts.items()) or 'none'})")
    print(f"  cohorts file {cohorts_path.name}: {len(cohorts)} rows")
    print(f"  tickers skipped (no parquet): {n_skip}")
    print(f"  manifest: {det_path.with_suffix('.manifest.json').name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
