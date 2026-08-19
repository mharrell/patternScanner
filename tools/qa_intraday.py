"""QA pass over the intraday accumulation archive (intraday track, v1).

Mirrors tools/qa_data.py philosophy: this script does NOT fix or delete
anything — it documents. Issues are reported here and in data/intraday/
README.md; decisions about them are logged, never silently "corrected".

Checks per (bar-date, ticker) parquet:
  - index sanity: DatetimeIndex, tz-aware America/New_York, minute-floored,
    sorted, unique, monotonic (a naive timestamp is a schema violation)
  - OHLC sanity: High >= max(Open, Close), Low <= min(Open, Close),
    High >= Low, positive prices
  - coverage: actual rows vs expected regular-session minutes (390 for
    09:30-16:00 ET); observed span vs nominal 04:00-20:00 ET
  - zero-volume / NaN-volume minutes, NaN prices
  - interior gaps: missing minute slots inside the observed span
  - envelope vs daily bars (data/cache/bars/<ticker>.parquet): intraday
    High/Low must sit inside the daily High/Low (1% tolerance), intraday
    volume sum must match daily Volume (2% tolerance). Daily missing or the
    file predating the daily snapshot -> noted, not failed. A sustained
    envelope break is the signature of an unrecorded split.

Inputs:  data/intraday/raw/**/*.parquet, data/intraday/manifest.json,
         --daily-bars data/cache/bars (optional, default)
Output:  data/intraday/qa_report.md (+ printed summary)
"""
import argparse
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INTRA = ROOT / "data" / "intraday"
RAW_DIR = INTRA / "raw"
MANIFEST_PATH = INTRA / "manifest.json"
DAILY_BARS = ROOT / "data" / "cache" / "bars"
OUT_PATH = INTRA / "qa_report.md"

TZ = ZoneInfo("America/New_York")
RTH_OPEN, RTH_CLOSE = 9, 30     # 09:30 ET
RTH_END_H, RTH_END_M = 16, 0    # 16:00 ET (exclusive -> 390 minutes)
PRICE_TOL = 0.01                # envelope tolerance (splits/adjustment slack)
VOL_TOL = 0.02                  # volume-sum tolerance
RTH_COV_FLOOR = 0.98            # regular-session coverage flag threshold
GAP_FLAG = 5                    # interior gaps above this are flagged


def rth_mask(idx: pd.DatetimeIndex) -> pd.Series:
    t = idx.tz_convert(TZ)
    return (t.hour * 60 + t.minute >= RTH_OPEN * 60 + RTH_CLOSE) & \
           (t.hour * 60 + t.minute < RTH_END_H * 60 + RTH_END_M)


def check_one(rel: str, manifest_files: dict, daily_cache: dict) -> dict:
    p = RAW_DIR / rel
    rec = {"file": rel, "ticker": rel.split("/")[-1].removesuffix(".parquet"),
           "bar_date": rel.split("/")[0], "rows": 0,
           "rth_rows": 0, "rth_cov": 0.0, "span_first": None, "span_last": None,
           "naive_tz": False, "not_floored": False, "unsorted": False,
           "dup_ts": 0, "ohlc_bad": 0, "price_nonpos": 0, "zero_vol": 0,
           "nan_price": 0, "interior_gaps": 0,
           "env_high_viol": 0, "env_low_viol": 0, "max_env_dev_pct": 0.0,
           "vol_sum_ratio": None, "daily_missing": False, "notes": []}
    if p.exists() and rel not in manifest_files:
        rec["notes"].append("on disk but NOT in manifest — ledger inconsistency")
    if not p.exists():
        rec["notes"].append("missing on disk")
        return rec
    try:
        df = pd.read_parquet(p)
    except Exception as e:
        rec["notes"].append(f"unreadable parquet: {e}")
        return rec

    idx = df.index
    if not isinstance(idx, pd.DatetimeIndex):
        rec["notes"].append("index not DatetimeIndex")
        return rec
    rec["rows"] = len(df)
    rec["span_first"] = str(idx.min())
    rec["span_last"] = str(idx.max())

    if idx.tz is None:
        rec["naive_tz"] = True
    else:
        idx = idx.tz_convert(TZ)
    minutes = idx.floor("min")
    if not (minutes == idx).all():
        rec["not_floored"] = True
    if not idx.is_monotonic_increasing:
        rec["unsorted"] = True
        df = df.sort_index()
    dups = idx.duplicated().sum()
    if dups:
        rec["dup_ts"] = int(dups)
    df = df[~df.index.duplicated()]

    rth = rth_mask(df.index)
    rec["rth_rows"] = int(rth.sum())
    rec["rth_cov"] = round(rec["rth_rows"] / 390.0, 4)
    if rec["rth_cov"] < RTH_COV_FLOOR:
        rec["notes"].append(f"RTH coverage {rec['rth_cov']:.1%} < {RTH_COV_FLOOR:.0%}")

    prices = df[["Open", "High", "Low", "Close"]]
    rec["nan_price"] = int(prices.isna().sum().sum())
    rec["price_nonpos"] = int((prices <= 0).sum().sum())
    hl = ((df["High"] < df["Low"])
          | (df["High"] < df[["Open", "Close"]].max(axis=1))
          | (df["Low"] > df[["Open", "Close"]].min(axis=1)))
    rec["ohlc_bad"] = int(hl.sum())
    rec["zero_vol"] = int((df["Volume"] <= 0).sum())

    if len(df) > 1:
        full = pd.date_range(df.index[0], df.index[-1], freq="min")
        rec["interior_gaps"] = int(len(full) - len(df.index))

    # Envelope vs daily bars (adjusted). Raw intraday vs adjusted daily are
    # equal absent splits/dividend adjustments; tolerances absorb the rest.
    key = rec["ticker"]
    daily = daily_cache.get(key)
    if daily is None:
        rec["daily_missing"] = True
        rec["notes"].append("daily bar missing — envelope check skipped")
    else:
        d = pd.Timestamp(rec["bar_date"], tz=TZ)
        day = daily[daily.index == d]
        if len(day):
            day = day.iloc[0]
            dev_h = (df["High"].max() - day["High"]) / day["High"]
            dev_l = (day["Low"] - df["Low"].min()) / day["Low"]
            rec["max_env_dev_pct"] = round(100 * max(0, dev_h, dev_l), 3)
            rec["env_high_viol"] = int((df["High"] > day["High"] * (1 + PRICE_TOL)).sum())
            rec["env_low_viol"] = int((df["Low"] < day["Low"] * (1 - PRICE_TOL)).sum())
            if day["Volume"] and day["Volume"] > 0:
                rec["vol_sum_ratio"] = round(df["Volume"].sum() / day["Volume"], 4)
                if abs(rec["vol_sum_ratio"] - 1) > VOL_TOL:
                    rec["notes"].append(f"volume sum ratio {rec['vol_sum_ratio']}")
        else:
            rec["notes"].append(f"no daily bar for {rec['bar_date']}")
    return rec


def load_daily_cache(daily_dir: Path) -> dict:
    cache = {}
    if not daily_dir.exists():
        print(f"NOTE: daily-bars cache {daily_dir} not found — envelope "
              f"check skipped for all files (see 'daily bar missing' in "
              f"qa_report.md)", file=sys.stderr)
        return cache
    for p in daily_dir.glob("*.parquet"):
        try:
            df = pd.read_parquet(p, columns=["Open", "High", "Low", "Volume"])
            df.index = df.index.tz_localize(TZ)
            cache[p.stem] = df
        except Exception as e:
            print(f"NOTE: daily-bars cache failed to load {p.name} ({e}) — "
                  f"envelope check skipped for {p.stem}", file=sys.stderr)
    return cache


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--daily-bars", type=Path, default=DAILY_BARS,
                    help="daily parquet dir for the envelope check "
                         "(default: data/cache/bars)")
    args = ap.parse_args(argv)

    manifest_files = {}
    if MANIFEST_PATH.exists():
        manifest_files = json.loads(
            MANIFEST_PATH.read_text(encoding="utf-8")).get("files", {})
    on_disk = sorted(p.relative_to(RAW_DIR).as_posix()
                     for p in RAW_DIR.glob("*/*.parquet"))
    if not on_disk and not manifest_files:
        print("archive is empty — nothing to QA")
        return 0
    rels = sorted(set(on_disk) | set(manifest_files))

    daily = load_daily_cache(args.daily_bars)
    rows = [check_one(r, manifest_files, daily) for r in rels]
    df = pd.DataFrame(rows)
    try:
        daily_src = str(args.daily_bars.relative_to(ROOT))
    except ValueError:
        daily_src = str(args.daily_bars)

    n_files = len(df)
    n_tickers = df["ticker"].nunique()
    n_dates = df["bar_date"].nunique()
    rth_floor = int((df["rth_cov"] < RTH_COV_FLOOR).sum())
    env_h = int(df["env_high_viol"].sum())
    env_l = int(df["env_low_viol"].sum())
    vol_flags = df[df["vol_sum_ratio"].notna()
                   & ((df["vol_sum_ratio"] - 1).abs() > VOL_TOL)]
    gaps = int(df["interior_gaps"].sum())

    lines = [
        "# Intraday archive QA report",
        "",
        f"- Generated: {pd.Timestamp.now(TZ).isoformat()}",
        f"- Files checked: {n_files} ({n_tickers} tickers, {n_dates} bar-dates)",
        f"- QA tool: `tools/qa_intraday.py` — flags only, nothing deleted or corrected",
        f"- Daily envelope source: `{daily_src}`",
        "",
        "## Summary",
        "",
        f"- regular-session coverage < {RTH_COV_FLOOR:.0%}: {rth_floor} files",
        f"- interior gap minutes across archive: {gaps}",
        f"- envelope violations (high/low): {env_h} / {env_l}",
        f"- volume-sum mismatches (> {VOL_TOL:.0%}): {len(vol_flags)}",
        f"- daily-bar envelope unavailable (missing/not-loaded): "
        f"{int(df['daily_missing'].sum())} files",
        f"- naive-tz / not-minute-floored / unsorted / dup-ts files: "
        f"{int(df['naive_tz'].sum())} / {int(df['not_floored'].sum())} / "
        f"{int(df['unsorted'].sum())} / {int(df['dup_ts'].sum())}",
        "",
        "## Anomalies (flagged, not fixed)",
        "",
    ]
    flag_cols = {
        "rth_cov": "RTH coverage",
        "interior_gaps": "gap minutes",
        "ohlc_bad": "OHLC violations",
        "env_high_viol": "env>High",
        "env_low_viol": "env<Low",
        "vol_sum_ratio": "vol ratio",
        "zero_vol": "zero-vol mins",
        "nan_price": "NaN prices",
        "price_nonpos": "non-pos prices",
        "dup_ts": "dup timestamps",
        "naive_tz": "naive tz",
        "not_floored": "not floored",
        "unsorted": "unsorted",
        "daily_missing": "daily missing",
    }
    mask = ((df["rth_cov"] < RTH_COV_FLOOR) | (df["interior_gaps"] > 0)
            | (df["ohlc_bad"] > 0) | (df["env_high_viol"] > 0)
            | (df["env_low_viol"] > 0)
            | (df["vol_sum_ratio"].notna() & ((df["vol_sum_ratio"] - 1).abs() > VOL_TOL))
            | (df["zero_vol"] > 0) | (df["nan_price"] > 0)
            | (df["price_nonpos"] > 0) | (df["dup_ts"] > 0)
            | df["naive_tz"] | df["not_floored"] | df["unsorted"]
            | df["daily_missing"] | (df["notes"].apply(len) > 0))
    show = df[mask]
    if len(show):
        lines.append("| file | rows | " + " | ".join(flag_cols.values()) + " | notes |")
        lines.append("|---|---|" + "---|" * len(flag_cols) + "---|")
        for _, r in show.iterrows():
            cells = [f"{r['file']}", f"{r['rows']}"]
            for k in flag_cols:
                v = r[k]
                if k == "rth_cov":
                    cells.append(f"{v:.1%}")
                elif k == "vol_sum_ratio":
                    cells.append(f"{v:.3f}" if pd.notna(v) else "")
                elif isinstance(v, bool):
                    cells.append("Y" if v else "")
                else:
                    cells.append(str(v))
            cells.append("; ".join(r["notes"])[:120])
            lines.append("| " + " | ".join(cells) + " |")
    else:
        lines.append("_No anomalies._")

    lines += [
        "",
        "## Known expected patterns (not defects)",
        "",
        "- **Thin-name minute sparsity (verified 2026-08-18):** Yahoo 1m emits",
        "  a bar only when the name prints a trade/quote, so thinly-traded",
        "  S&P 600 names show real RTH minute gaps (e.g. AAT ~30-55% RTH",
        "  coverage) while liquid names are complete (AAPL/MSFT/SPY 390/390",
        "  RTH). This is data reality, not a pipeline fault — measurement on",
        "  thin names must resample (e.g. 5-min) or count RTH coverage.",
        "- Pre-market span often starts later than 04:00 for thin names",
        "  (Yahoo coverage); regular session 09:30-16:00 is the strict check.",
        "- Envelope/volume tolerances absorb dividend adjustments on the",
        "  adjusted daily bars; a *sustained* break across many files is the",
        "  signature of an unrecorded split — record it in",
        "  `data/intraday/splits.json` (procedure in the README).",
        "- The archive starts fresh: earlier bar-dates are legitimately",
        "  absent before enough nightly pulls have run.",
        "",
        f"_(end of QA report — {n_files} files checked)_",
        "",
    ]
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"checked {n_files} files ({n_tickers} tickers, {n_dates} dates) -> {OUT_PATH.name}")
    print(f"  RTH<{RTH_COV_FLOOR:.0%}: {rth_floor} | gaps: {gaps} | "
          f"env: {env_h}/{env_l} | vol-ratio flags: {len(vol_flags)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
