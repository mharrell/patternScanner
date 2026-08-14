"""QA pass over fetched daily bars (Phase 1 exit check).

Per DESIGN_BRIEF Phase 1: "Clean 2000-2025 daily bars, documented gaps."
This script does NOT fix or delete anything — it documents. Per the
pre-registration, data issues that matter (interior gaps, anomalous bars)
are reported here and in data/README.md; decisions about them are logged,
never silently "corrected".

Checks per ticker parquet:
  - index sanity (DatetimeIndex, sorted, unique, no NaNs, plausible prices)
  - OHLC consistency (High >= max(Open, Close), Low <= min(Open, Close))
  - interior gaps: consecutive-bar day diff > 7 calendar days
  - zero-volume days, |daily return| > 50% (possible split artifacts or
    real halts — flagged, not dropped)
  - span vs expected trading days (weekdays in range; holidays ignored,
    so a full-window ticker lands ~0.965, never ~1.0)

Inputs:  data/cache/bars/*.parquet, data/cache/fetch_log.json
Output:  data/cache/qa_report.md (+ printed summary)
"""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
BARS_DIR = CACHE / "bars"
LOG_PATH = CACHE / "fetch_log.json"
OUT_PATH = CACHE / "qa_report.md"
GAP_DAYS = 7          # interior gap threshold (calendar days)
MAX_RET = 0.50        # |daily return| threshold (flag, not drop)
SPAN_RATIO = 0.94     # rows / weekdays-in-span below this = short-data flag


def check_one(ticker: str) -> dict:
    p = BARS_DIR / f"{ticker}.parquet"
    rec = {"ticker": ticker, "rows": 0, "first": None, "last": None,
           "short_span": False, "gaps": 0, "max_gap_days": 0,
           "zero_vol": 0, "zero_vol_pre08": 0, "extreme_ret": 0,
           "price_nan": 0, "ohlc_bad": 0, "max_ohlc_dev": 0.0,
           "dup_dates": 0, "unsorted": False, "notes": []}
    if not p.exists():
        rec["notes"].append("no parquet")
        return rec
    df = pd.read_parquet(p)
    need = {"Open", "High", "Low", "Close", "Volume"}
    missing_cols = need - set(df.columns)
    if missing_cols:
        rec["notes"].append(f"missing cols: {sorted(missing_cols)}")
        return rec
    if not isinstance(df.index, pd.DatetimeIndex):
        rec["notes"].append("index not DatetimeIndex")
        return rec

    rec["rows"] = len(df)
    rec["first"] = str(df.index.min().date())
    rec["last"] = str(df.index.max().date())
    if not df.index.is_monotonic_increasing:
        rec["unsorted"] = True
        df = df.sort_index()
    dups = df.index.duplicated().sum()
    if dups:
        rec["dup_dates"] = int(dups)
    df = df[~df.index.duplicated()]

    prices = df[["Open", "High", "Low", "Close"]]
    rec["price_nan"] = int(prices.isna().sum().sum())
    neg = (prices <= 0).sum().sum()
    if neg:
        rec["notes"].append(f"{int(neg)} non-positive prices")

    hl_mask = ((df["High"] < df["Low"])
               | (df["High"] < df[["Open", "Close"]].max(axis=1))
               | (df["Low"] > df[["Open", "Close"]].min(axis=1)))
    rec["ohlc_bad"] = int(hl_mask.sum())
    if rec["ohlc_bad"]:
        # magnitude: max absolute violation (Yahoo special-dividend artifacts)
        h_hi = (df.loc[hl_mask, "High"] - df.loc[hl_mask, ["Open", "Close"]].max(axis=1)).abs()
        l_lo = (df.loc[hl_mask, "Low"] - df.loc[hl_mask, ["Open", "Close"]].min(axis=1)).abs()
        rec["max_ohlc_dev"] = float(pd.concat([h_hi, l_lo]).max())

    zvol = df["Volume"] <= 0
    rec["zero_vol"] = int(zvol.sum())
    rec["zero_vol_pre08"] = int(zvol[df.index < "2008-01-01"].sum())

    rets = df["Close"].pct_change()
    rec["extreme_ret"] = int((rets.abs() > MAX_RET).sum())

    diffs = df.index.to_series().diff().dt.days.iloc[1:]
    if len(diffs):
        big = diffs[diffs > GAP_DAYS]
        rec["gaps"] = int(len(big))
        rec["max_gap_days"] = int(big.max()) if len(big) else 0

    # Expected trading days: weekdays in span (holidays ignored). A clean
    # full-window ticker lands ~0.965; anything under SPAN_RATIO lost data.
    wk = len(pd.bdate_range(df.index.min(), df.index.max()))
    if wk and rec["rows"] / wk < SPAN_RATIO:
        rec["short_span"] = True
    return rec


def main() -> int:
    log = json.loads(LOG_PATH.read_text(encoding="utf-8")) if LOG_PATH.exists() else {"tickers": {}}
    tickers = sorted({p.stem for p in BARS_DIR.glob("*.parquet")}
                     | set(log["tickers"].keys()))

    rows = [check_one(t) for t in tickers]
    df = pd.DataFrame(rows)
    ok_log = {t: r for t, r in log["tickers"].items() if r["status"] == "ok"}
    bad_log = {t: r for t, r in log["tickers"].items() if r["status"] != "ok"}
    with_parquet = df[df["notes"].apply(lambda n: "no parquet" not in n)]

    n_full = 0
    n_end2025 = 0
    for r in rows:
        if r["first"] is not None and r["first"] <= "2000-01-07" and r["last"] >= "2025-12-24":
            n_full += 1
        if r["last"] is not None and r["last"] >= "2025-12-24":
            n_end2025 += 1

    max_dev = max((r["max_ohlc_dev"] for r in rows), default=0.0)
    zv_total = sum(r["zero_vol"] for r in rows)
    zv_pre08 = sum(r["zero_vol_pre08"] for r in rows)

    lines = [
        "# Phase 1 data QA report",
        "",
        f"- Generated: 2026-08-13 (see git history for reproducibility)",
        f"- Universe: `data/cache/universe_sp600_2026-08-13.csv` (603 tickers, frozen)",
        f"- Bars: `data/cache/bars/<ticker>.parquet`, yfinance adjusted OHLCV",
        f"- Fetch log: `data/cache/fetch_log.json`",
        f"- QA tool: `tools/qa_data.py` — flags only, nothing deleted or corrected",
        "",
        "## Fetch summary",
        "",
        f"- log entries: {len(log['tickers'])} (ok={len(ok_log)}, not-ok={len(bad_log)})",
        f"- parquet files on disk: {len(with_parquet)}",
        f"- full-window tickers (first bar ≤ 2000-01-07, last ≥ 2025-12-24): {n_full}",
        f"- tickers whose last bar is in Dec 2025: {n_end2025}",
        "",
        "## Coverage",
        "",
        f"- median rows/ticker: {int(df['rows'].median())}",
        f"- short-span flags (rows < 94% of weekdays in span): {int(df['short_span'].sum())}",
        f"- tickers with interior gaps > {GAP_DAYS} calendar days: {int((df['gaps'] > 0).sum())}",
        "",
        "## Known data artifacts (documented, not fixed)",
        "",
        f"- zero-volume days: {zv_total} across the universe, "
        f"{100 * zv_pre08 / zv_total:.0f}% before 2008 "
        f"(Yahoo's pre-2008 volume gap; affects relative-volume legs by "
        f"epoch, see data/README.md)",
        f"- largest adjusted-OHLC inconsistency: ${max_dev:.2f} "
        f"(Yahoo special-dividend artifact; distorts High/Low features on "
        f"isolated days, not Close-based returns)",
        "",
        "## Anomalies (flagged, not dropped)",
        "",
    ]
    flag_cols = {
        "gaps": "interior gaps > 7d",
        "max_gap_days": "worst gap (days)",
        "zero_vol": "zero-volume days",
        "extreme_ret": f"|ret| > {MAX_RET:.0%} days",
        "price_nan": "NaN prices",
        "ohlc_bad": "OHLC violations",
        "dup_dates": "duplicate dates",
        "unsorted": "unsorted index",
        "short_span": "short span",
    }
    mask = ((df["gaps"] > 0) | (df["zero_vol"] > 0) | (df["extreme_ret"] > 0)
            | (df["price_nan"] > 0) | (df["ohlc_bad"] > 0) | (df["dup_dates"] > 0)
            | df["unsorted"] | df["short_span"]
            | (df["notes"].apply(len) > 0))
    show = df[mask]
    if len(show):
        lines.append("| ticker | rows | first | last | " + " | ".join(flag_cols.values()) + " |")
        lines.append("|---|---|---|---|" + "---|" * len(flag_cols))
        for _, r in show.iterrows():
            cells = [f"{r['ticker']}", f"{r['rows']}", f"{r['first']}",
                     f"{r['last']}"] + [str(r[k]) if k != "short_span" else ("Y" if r[k] else "")
                                        for k in flag_cols]
            lines.append("| " + " | ".join(cells) + " |")
    else:
        lines.append("_No anomalies._")

    notes = df[df["notes"].apply(len) > 0]
    if len(notes):
        lines.append("")
        lines.append("## Notes / no-parquet")
        lines.append("")
        for _, r in notes.iterrows():
            lines.append(f"- `{r['ticker']}`: " + "; ".join(r["notes"]))

    lines += [
        "",
        "## Known expected patterns (not defects)",
        "",
        "- Later-IPO tickers legitimately have short spans (first bar after 2000).",
        "- Zero-volume days occur for suspended/tiny names; counted, not corrected.",
        "- Extreme single-day returns can be real (halts, gap-ups) or adjustment",
        "  artifacts; each is documented in the next section if it survived QA.",
        "",
        f"_(end of QA report — {len(df)} tickers checked)_",
        "",
    ]
    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"checked {len(df)} tickers -> {OUT_PATH.name}")
    print(f"  full-window: {n_full} | end-2025: {n_end2025} | parquet on disk: {len(with_parquet)}")
    print(f"  interior-gap tickers: {int((df['gaps'] > 0).sum())} | "
          f"zero-vol tickers: {int((df['zero_vol'] > 0).sum())} | "
          f"extreme-ret tickers: {int((df['extreme_ret'] > 0).sum())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
