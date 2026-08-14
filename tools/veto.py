"""Veto filter for pre-registration #3 (ledger E-01/E-04), frozen 2026-08-14.

Reads the frozen shape detections (data/cache/detections_v1.csv, pre-reg #2,
manifest e93ddf7a...) and attaches the two-filter-veto leg evaluations at
each signal day t (all legs use data <= t only — no look-ahead):

  MACD leg:    macd_neg   = MACD(12,26) line < 0 at t        (primary)
               macd_cross = line_t < 0 AND line_{t-1} >= 0   (sensitivity:
                            the stricter "crossed negative" reading of E-01)
  Volume leg:  red_high_vol = c_t < o_t AND v_t >= V * mean(v, prior 20),
               primary V = 2.0. "Selling" is operationalized as the red
               candle itself (OHLCV cannot separate selling from buying
               pressure beyond candle color). The 0/0 guard matches every
               other volume leg in the repo (mean > 0 required).
  veto_pass   = NOT macd_neg AND NOT red_high_vol
               ("if just one of them says no, I don't take the trade")

MACD is computed on adjusted closes with ewm(adjust=False), standard
(12,26,9) — "blue line" = the 12-26 EMA difference. Warm-up guard (pre-reg
#3 §1): detections at bar index < WARMUP from series start are excluded
from the campaign (EMA seed weight) and flagged as warmup.

V = 1.5/3.0 sensitivities are pure re-subsets of the stored vol_ratio, so
only V = 2.0 is computed here.

Output: data/cache/veto_detections_v1.csv (frozen columns + leg columns)
plus a manifest (input detections sha, code sha, params). Deterministic:
same data + same code = byte-identical output.
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
OUT_CSV = CACHE / "veto_detections_v1.csv"

PARAMS = {"macd": {"fast": 12, "slow": 26, "signal": 9},
          "vol_mult": 2.0, "vol_lookback": 20, "warmup_bars": 60}

_bars: dict = {}
_line_c: dict = {}


def _line_cache(t: str, c: pd.Series) -> pd.Series:
    if t not in _line_c:
        _line_c[t] = macd_line(c)
    return _line_c[t]


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


def vol_ratio_at(v: pd.Series, loc: int) -> float:
    """v[loc] / mean(v, prior 20) with the 0/0 guard; NaN if mean is 0."""
    mean = v.iloc[max(0, loc - PARAMS["vol_lookback"]):loc].mean()
    if mean > 0:
        return float(v.iloc[loc] / mean)
    return float("nan")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limit", type=int, default=0, help="first N detections only (test)")
    args = ap.parse_args()

    det = pd.read_csv(DET_CSV)
    if args.limit:
        det = det.head(args.limit)

    rows = []
    loc_cache: dict = {}
    n_warmup = 0
    for i, r in det.iterrows():
        t, ts = r["ticker"], pd.Timestamp(r["signal_date"])
        df = bars(t)
        if t not in loc_cache:
            loc_cache[t] = {x: j for j, x in enumerate(df.index)}
        loc = loc_cache[t].get(ts)
        if loc is None:
            continue  # cannot happen; guarded
        c, o, v = df["Close"], df["Open"], df["Volume"]
        warmup = loc < PARAMS["warmup_bars"]
        n_warmup += int(warmup)

        if warmup:
            # legs carry real booleans so the CSV round-trips as bool dtype;
            # the warmup flag is the authoritative exclusion marker
            rows.append({**r.to_dict(), "warmup": True, "macd_line": None,
                         "vol_ratio": None, "red": False, "macd_neg": False,
                         "macd_cross": False, "red_high_vol": False,
                         "veto_pass": False})
            continue

        line = _line_cache(t, c)
        line_t, line_prev = float(line.iloc[loc]), float(line.iloc[loc - 1])
        macd_neg = line_t < 0.0
        macd_cross = macd_neg and line_prev >= 0.0
        vr = vol_ratio_at(v, loc)
        red = float(c.iloc[loc]) < float(o.iloc[loc])
        vol_ok = not np.isnan(vr) and vr >= PARAMS["vol_mult"]
        red_high_vol = bool(red and vol_ok)

        rows.append({**r.to_dict(), "warmup": False, "macd_line": float(line_t),
                     "vol_ratio": vr, "red": red, "macd_neg": macd_neg,
                     "macd_cross": macd_cross, "red_high_vol": red_high_vol,
                     "veto_pass": bool(not macd_neg and not red_high_vol)})

    out = pd.DataFrame(rows).sort_values(["shape", "ticker", "signal_date"]) \
                             .reset_index(drop=True)
    OUT_CSV.write_bytes(out.to_csv(index=False).encode("utf-8"))

    manifest = {
        "pre_reg": "#3",
        "veto_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_detections_sha256": hashlib.sha256(DET_CSV.read_bytes()).hexdigest(),
        "params": PARAMS,
        "run_date": str(pd.Timestamp.now().date()),
        "n_rows": int(len(out)), "n_warmup_excluded": int(n_warmup),
    }
    OUT_CSV.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"wrote {OUT_CSV.name}: {len(out)} rows (warmup-excluded {n_warmup})")
    sub = out[out["warmup"] == False]
    for s in "ABC":
        d = sub[sub["shape"] == s]
        print(f"  {s}: {len(d)} detections | pass {int(d['veto_pass'].sum())} "
              f"| macd-alone {int((d['macd_neg'] & ~d['red_high_vol']).sum())} "
              f"| vol-alone {int((~d['macd_neg'] & d['red_high_vol']).sum())} "
              f"| both {int((d['macd_neg'] & d['red_high_vol']).sum())}")
    print(f"  manifest: {OUT_CSV.with_suffix('.manifest.json').name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
