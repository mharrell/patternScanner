"""Build the S&P 600 universe snapshot + float data (Phase 1).

Per PREREGISTRATION #1 §5: universe = current S&P 600 constituents,
snapshotted on a FIXED date (never updated after). Membership source:
Wikipedia "List of S&P 600 companies" (the pre-registration's preferred
option). Float: Yahoo `floatShares` (fallback `sharesOutstanding`), fetched
once at snapshot time via yfinance `get_info`.

Output:
  data/cache/universe_sp600_<SNAPSHOT_DATE>.csv
    columns: ticker, company, sector, industry, date_added, float_shares,
             float_source (floatShares | sharesOutstanding | missing)

Resumable: re-running skips tickers that already have a float value.
"""
import argparse
import io
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies"


def yahoo_ticker(raw: str) -> str:
    """Yahoo uses '-' for share classes (e.g. BRK.B -> BRK-B).

    Also strips Wikipedia footnote markers like 'ABCB[1]' and non-ticker
    placeholder cells."""
    import re

    t = raw.strip()
    t = re.sub(r"\[[^\]]*\]", "", t)  # footnote refs
    if not t or t in {"—", "-", "--"}:
        return ""
    return t.replace(".", "-")


def scrape_wikipedia() -> pd.DataFrame:
    resp = requests.get(
        WIKI_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                               "patternScanner/phase1 research"},
        timeout=30,
    )
    resp.raise_for_status()
    tables = pd.read_html(io.StringIO(resp.text))
    for t in tables:
        cols = {str(c).strip().lower() for c in t.columns}
        if "symbol" in cols and "security" in cols:
            df = t.copy()
            df.columns = [str(c).strip().lower() for c in df.columns]
            # Wikipedia's column names differ from the canonical ones.
            keep = {
                "symbol": "ticker",
                "security": "company",
                "gics sector": "sector",
                "gics sub-industry": "industry",
                "date added": "date_added",
            }
            df = df.rename(columns={k: v for k, v in keep.items() if k in df.columns})
            return df
    raise RuntimeError(f"No usable constituent table found on {WIKI_URL}")


def fetch_float(ticker: str):
    """Return (float_shares, source). Retries with backoff.

    Yahoo's delimiter conventions are inconsistent (CWEN-A vs CWEN.A), so on
    a 404-style failure the alternate delimiter is tried before giving up."""
    import yfinance as yf

    last_err = None
    import re

    candidates = [ticker]
    if "-" in ticker:
        candidates.append(ticker.replace("-", "."))
    elif "." in ticker:
        candidates.append(ticker.replace(".", "-"))
    # Yahoo's quoteSummary often fails on class suffixes (CWEN-A, CWEN.A);
    # the base symbol resolves (use with the documented caveat).
    base = re.sub(r"[-.][A-Za-z]+$", "", ticker)
    if base and base != ticker:
        candidates.append(base)
    for sym in candidates:
        for attempt in range(3):
            try:
                info = yf.Ticker(sym).get_info()
                if not isinstance(info, dict) or "error" in info or len(info) < 5:
                    # Yahoo swallows 404s as a 1-key {"error": ...} dict;
                    # treat as a failed lookup so the next candidate is tried.
                    raise ValueError(f"lookup failed for {sym}: {str(info)[:80]}")
                if info.get("floatShares"):
                    source = "floatShares" if sym == ticker else f"floatShares(base:{sym})"
                    return int(info["floatShares"]), source
                if info.get("sharesOutstanding"):
                    source = "sharesOutstanding" if sym == ticker else f"sharesOutstanding(base:{sym})"
                    return int(info["sharesOutstanding"]), source
                return None, "missing"
            except Exception as e:  # network / parse / 404 errors — retry
                last_err = e
                time.sleep(1.0 * (attempt + 1))
    return None, f"error:{last_err.__class__.__name__}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--snapshot-date", default="2026-08-13",
                    help="fixed snapshot date; list is never updated after this")
    ap.add_argument("--threads", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0, help="fetch float for first N tickers only (test)")
    ap.add_argument("--skip-float", action="store_true", help="membership only, no float fetch")
    args = ap.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / f"universe_sp600_{args.snapshot_date}.csv"

    df = scrape_wikipedia()
    df["ticker"] = df["ticker"].map(yahoo_ticker)
    df = df[df["ticker"] != ""]
    df = df.drop_duplicates(subset="ticker")
    if "date_added" in df.columns:
        df["date_added"] = df["date_added"].astype(str).str.strip()
    # Canonical column set only (drop Wikipedia's SEC-filings/CIK noise).
    keep_cols = [c for c in
                 ["ticker", "company", "sector", "industry", "date_added"]
                 if c in df.columns]
    df = df[keep_cols]
    df["float_shares"] = None
    df["float_source"] = None

    # Resumable: load previous snapshot if present and merge back floats.
    if out.exists() and not args.skip_float:
        prev = pd.read_csv(out)
        have = prev.set_index("ticker")[["float_shares", "float_source"]]
        df = df.set_index("ticker").join(have, rsuffix="_prev").reset_index()
        df["float_shares"] = df["float_shares"].fillna(df.get("float_shares_prev"))
        df["float_source"] = df["float_source"].fillna(df.get("float_source_prev"))
        if "float_shares_prev" in df.columns:
            df = df.drop(columns=["float_shares_prev", "float_source_prev"])

    if not args.skip_float:
        todo = df[df["float_shares"].isna()]["ticker"].tolist()
        if args.limit:
            todo = todo[: args.limit]
        print(f"fetching float for {len(todo)} tickers ({args.threads} threads)...")
        n_done = 0
        with ThreadPoolExecutor(max_workers=args.threads) as pool:
            futs = {pool.submit(fetch_float, t): t for t in todo}
            for fut in as_completed(futs):
                t = futs[fut]
                shares, source = fut.result()
                df.loc[df["ticker"] == t, ["float_shares", "float_source"]] = shares, source
                n_done += 1
                if n_done % 25 == 0:
                    df.to_csv(out, index=False)
                    print(f"  {n_done}/{len(todo)} floats fetched")
        df.to_csv(out, index=False)

    df.to_csv(out, index=False)
    n = len(df)
    nf = df["float_shares"].notna().sum()
    print(f"\nwrote {out.name}: {n} tickers, float coverage {nf}/{n}")
    missing = df[df["float_shares"].isna()]["ticker"].tolist()
    if missing:
        print(f"missing float: {', '.join(missing[:20])}{'...' if len(missing) > 20 else ''}")
    print(df.head(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
