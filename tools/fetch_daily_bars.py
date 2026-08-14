"""Fetch 2000-2025 daily OHLCV bars for a universe (Phase 1).

Per PREREGISTRATION #1 §3/§5 and DESIGN_BRIEF §5: yfinance (Yahoo-sourced),
adjusted closes (splits/dividends), explicit start/end, no look-ahead
concerns at fetch time (that is a measurement-stage property).

Outputs:
  data/cache/bars/<ticker>.parquet   — Open/High/Low/Close/Volume, Date index
  data/cache/fetch_log.json          — per-ticker status + coverage + meta

Resumable: tickers with an existing parquet are skipped unless --refresh.
Retries with backoff on network errors; Yahoo rate limits are handled by
curl_cffi TLS impersonation (see requirements.txt).
"""
import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
BARS_DIR = CACHE / "bars"
LOG_PATH = CACHE / "fetch_log.json"
DEFAULT_START = "2000-01-01"
DEFAULT_END = "2026-01-01"  # exclusive: covers 2000-01-01..2025-12-31
COLS = ["Open", "High", "Low", "Close", "Volume"]


def fetch_one(ticker: str, start: str, end: str, attempts: int = 3):
    """Return dict(ticker, status, rows, first, last, error)."""
    import re

    import yfinance as yf

    last_err = None
    # Yahoo's chart API, like quoteSummary, often 404s class-suffixed tickers
    # (CWEN-A) while the base symbol resolves. Tried only on no_data.
    base = re.sub(r"[-.][A-Za-z]+$", "", ticker) if "-" in ticker or "." in ticker else None
    symbols = [ticker] + ([base] if base and base != ticker else [])
    for sym in symbols:
        for i in range(attempts):
            try:
                df = yf.download(sym, start=start, end=end, auto_adjust=True,
                                 progress=False, threads=False)
                if df is None or df.empty:
                    raise ValueError("no data")  # -> next attempt, then next symbol
                break
            except Exception as e:  # network error, throttle, parse issue
                last_err = e
                if i < attempts - 1 or sym != symbols[-1]:
                    time.sleep(1.5 * (i + 1))
                df = None
        else:
            continue  # inner loop exhausted -> try base symbol
        if df is not None and not df.empty:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel("Ticker")  # single ticker
            df = df[COLS].copy()
            df = df[~df.index.duplicated()].sort_index()
            df.index = df.index.normalize()
            df.index.name = "Date"
            out = BARS_DIR / f"{ticker}.parquet"
            df.to_parquet(out)
            return {"ticker": ticker, "status": "ok" if sym == ticker else f"ok(base:{sym})",
                    "rows": len(df),
                    "first": str(df.index[0].date()), "last": str(df.index[-1].date()),
                    "error": None}
    return {"ticker": ticker, "status": "no_data", "rows": 0,
            "first": None, "last": None,
            "error": f"last error: {last_err}" if last_err else None}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--universe", type=Path,
                    default=CACHE / "universe_sp600_2026-08-13.csv")
    ap.add_argument("--start", default=DEFAULT_START)
    ap.add_argument("--end", default=DEFAULT_END)
    ap.add_argument("--threads", type=int, default=6)
    ap.add_argument("--refresh", action="store_true",
                    help="re-fetch tickers that already have a parquet")
    ap.add_argument("--limit", type=int, default=0, help="first N tickers only (test)")
    args = ap.parse_args()

    BARS_DIR.mkdir(parents=True, exist_ok=True)
    uni = pd.read_csv(args.universe)
    tickers = uni["ticker"].tolist()
    if args.limit:
        tickers = tickers[: args.limit]

    # Resumable: merge prior log, skip tickers already ok.
    log = {"meta": {"fetched": str(date.today()), "start": args.start,
                    "end": args.end, "auto_adjust": True,
                    "universe": args.universe.name},
           "tickers": {}}
    if LOG_PATH.exists():
        log = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    done = {t for t, rec in log["tickers"].items()
            if rec["status"] == "ok" and not args.refresh}

    todo = [t for t in tickers if t not in done]
    print(f"{len(todo)} to fetch ({len(done)} already ok, {len(tickers)} universe)")
    results = []
    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        futs = {pool.submit(fetch_one, t, args.start, args.end): t for t in todo}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            log["tickers"][r["ticker"]] = r
            with LOG_PATH.open("w", encoding="utf-8") as f:
                json.dump(log, f, indent=2)
    if not todo:
        results = [r for t, r in log["tickers"].items()]

    ok = [r for r in results if r["status"] == "ok"]
    bad = [r for r in results if r["status"] != "ok"]
    print(f"\nfetched {len(ok)} ok, {len(bad)} not-ok")
    for r in bad[:10]:
        print(f"  {r['ticker']}: {r['status']} {r['error'] or ''}")
    print(f"\nlog: {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
