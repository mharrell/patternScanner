"""Build the historical-constituent universe for pre-registration #13
(brief §5 survivorship gate — the re-check of pre-reg #10's F1-BULL EDGE
against historical constituents).

Source (pre-reg #13 §1, amended 2026-08-15): the Wikipedia article "List
of S&P 600 companies", served from the page's OWN revision history via the
MediaWiki API — the canonical archive (every revision immutable and
exact-dated, gap-free from page creation 2018-08-27).

AMENDED SNAPSHOT SCHEDULE (evidence recorded in pre-reg #13 §1): the page
was created 2018-08-27 as an "S&P 1000" page (S&P 400 + S&P 600 combined)
and carried that sloppy 1000-row table until March 2021 — the table kept
ghost members (delisted/moved names such as AKRX, AKS, AVP still listed in
Jan 2021), so a set-difference reconstruction "600 = 1000-table minus
S&P 400 table" was probed and REJECTED (validated 2021-01-26: reconstructed
755 vs 600 real; 155 ghosts). The true S&P 600 list appears on the page
from 2021-03-12. Snapshots therefore (frozen amendment, 5):

  2021-06 .. 2025-06: the most recent revision before Y-07-01T00:00:00Z
           (membership as of June 30 of each year; the 2021-03-12 earliest
           list is subsumed — it adds only names removed before 2021-06,
           which have no measurement-window events)

Parsing: same ticker normalization as tools/build_universe.py (yahoo_ticker:
strip footnotes, "." -> "-", drop placeholder cells); the table is
identified by a symbol column ("symbol" or "ticker symbol" — the page's
column was renamed between 2021 and 2026) plus a security/company column,
with a row-count sanity gate (550-750).

Output:
  data/cache/universe_sp600_hist_<SNAPSHOT_DATE>.csv   (union universe,
    columns: ticker, company, sector, industry, date_added, first_seen,
    n_snapshots; measurement reads only "ticker")
  data/cache/hist_universe_provenance.json  (per-snapshot revid,
    timestamp, ticker count, parse QA/fallbacks; union summary)

Resumable/deterministic: recorded revision ids are reused on re-runs, so
a rebuild after the first successful run produces a byte-identical CSV.
"""
import io
import json
import re
import sys
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "cache"
TITLE = "List of S&P 600 companies"
API = "https://en.wikipedia.org/w/api.php"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "patternScanner/phase1 research (historical re-check)"}
# (year-label, limit) — for 2021-03 the limit triggers the earliest-600 scan.
SNAPSHOTS = [("2021-06", "2021-07-01T00:00:00Z"),
             ("2022-06", "2022-07-01T00:00:00Z"),
             ("2023-06", "2023-07-01T00:00:00Z"),
             ("2024-06", "2024-07-01T00:00:00Z"),
             ("2025-06", "2025-07-01T00:00:00Z")]
ROW_MIN, ROW_MAX = 550, 750           # the S&P 600 table is ~600 rows


def yahoo_ticker(raw: str) -> str:
    """Same normalization as tools/build_universe.py (pre-reg #13 §1)."""
    t = raw.strip()
    t = re.sub(r"\[[^\]]*\]", "", t)  # footnote refs
    if not t or t in {"—", "-", "--"}:
        return ""
    return t.replace(".", "-")


def api_get(params: dict, tries: int = 8) -> dict:
    """GET with 429/network retry + backoff (the API throttles bursts)."""
    import time
    params = {**params, "format": "json", "formatversion": "2"}
    for i in range(tries):
        try:
            resp = requests.get(API, params=params, headers=UA, timeout=60)
            if resp.status_code == 200 and resp.text.startswith("{"):
                data = resp.json()
                if "error" not in data:
                    return data
        except Exception:
            pass
        time.sleep(3 * (i + 1))
    raise RuntimeError(f"API failed after {tries} tries: "
                       f"{str(params)[:60]}")


def latest_before(limit: str) -> dict:
    """Most recent revision strictly before limit: {revid, timestamp}."""
    data = api_get({
        "action": "query", "prop": "revisions", "titles": TITLE,
        "rvstart": limit, "rvdir": "older", "rvlimit": "1",
        "rvprop": "ids|timestamp",
    })
    revs = data["query"]["pages"][0].get("revisions", [])
    if not revs:
        raise RuntimeError(f"no revision before {limit}")
    return {"revid": revs[0]["revid"], "timestamp": revs[0]["timestamp"]}


def rendered_table(revid: int):
    """Rendered HTML of the revision -> (df, rows) or (None, 0) if no
    usable symbol table."""
    data = api_get({"action": "parse", "oldid": revid, "prop": "text"})
    html = data["parse"]["text"]
    tables = pd.read_html(io.StringIO(html), flavor="lxml")
    for t in tables:
        cols = {str(c).strip().lower() for c in t.columns}
        if (cols & {"symbol", "ticker symbol"}
                and cols & {"security", "company"}):
            if not (ROW_MIN <= len(t) <= ROW_MAX):
                continue  # not the S&P 600 table (S&P 1000 era: ~1000 rows)
            df = t.copy()
            df.columns = [str(c).strip().lower() for c in df.columns]
            sym_col = next(c for c in df.columns
                           if c in ("symbol", "ticker symbol"))
            df = df.rename(columns={sym_col: "ticker"})
            keep = {
                "ticker": "ticker", "company": "company",
                "security": "company", "gics sector": "sector",
                "gics sub-industry": "industry", "date added": "date_added",
            }
            df = df.rename(columns={k: v for k, v in keep.items()
                                    if k in df.columns})
            return df, len(df)
    return None, 0


def snapshot(year_label: str, limit: str, provenance: dict):
    """One snapshot: (re)use the recorded revid or resolve it; parse with a
    same-year next-older fallback on failure; record deviations."""
    if year_label not in provenance:
        provenance[year_label] = latest_before(limit)
    rec = provenance[year_label]
    last_err, attempt = None, rec
    while True:
        try:
            df, rows = rendered_table(attempt["revid"])
            if df is None:
                raise ValueError(f"no 600-row table in {attempt['revid']}")
            return {**attempt, "status": "ok", "rows": rows}, df
        except Exception as e:
            last_err = e
            if attempt.get("fallback_used"):
                break  # never fall back twice
            from datetime import datetime, timedelta
            ts = datetime.fromisoformat(
                attempt["timestamp"].replace("Z", "+00:00"))
            nxt = latest_before(
                (ts + timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%SZ"))
            if not nxt["timestamp"].startswith(year_label[:4]):
                break  # next-older revision is outside the snapshot year
            attempt = {**nxt, "fallback_used": True}
            print(f"    {year_label}: parse failed, falling back to revid "
                  f"{nxt['revid']} ({nxt['timestamp']})")
    raise RuntimeError(f"year {year_label}: no parseable revision "
                       f"(last err: {last_err.__class__.__name__}: "
                       f"{str(last_err)[:120]})")


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--snapshot-date", default="2026-08-15")
    args = ap.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    prov_path = CACHE / "hist_universe_provenance.json"
    provenance = {}
    if prov_path.exists():
        provenance = json.loads(prov_path.read_text(encoding="utf-8"))
        provenance.pop("union", None)  # rebuilt each run

    frames, snap_records = [], []
    for year_label, limit in SNAPSHOTS:
        rec, df = snapshot(year_label, limit, provenance)
        df = df.copy()
        df["ticker"] = df["ticker"].map(yahoo_ticker)
        df = df[df["ticker"] != ""]
        df = df.drop_duplicates(subset="ticker")
        if "date_added" in df.columns:
            df["date_added"] = df["date_added"].astype(str).str.strip()
        keep = [c for c in
                ["ticker", "company", "sector", "industry", "date_added"]
                if c in df.columns]
        df = df[keep]
        frames.append(df.assign(_snapshot_year=year_label))
        snap_records.append({**rec, "year": year_label, "status": "ok",
                             "n_tickers": int(len(df))})
        print(f"  {year_label}: revid {rec['revid']} ({rec['timestamp']}) "
              f"-> {len(df)} tickers")

    all_df = pd.concat(frames, ignore_index=True)
    first_seen = (all_df.groupby("ticker")["_snapshot_year"]
                         .min().rename("first_seen"))
    n_snapshots = (all_df.groupby("ticker")["_snapshot_year"]
                         .size().rename("n_snapshots"))
    cols = [c for c in ["company", "sector", "industry", "date_added"]
            if c in all_df.columns]
    union = (all_df.groupby("ticker", as_index=False)
                   .agg({**{c: "first" for c in cols},
                         "_snapshot_year": "first"})
                   .merge(first_seen, on="ticker")
                   .merge(n_snapshots, on="ticker")
                   .drop(columns="_snapshot_year"))
    union = union.sort_values("ticker").reset_index(drop=True)

    out = CACHE / f"universe_sp600_hist_{args.snapshot_date}.csv"
    union.to_csv(out, index=False)

    ticker_sets = {r["year"]: set(frames[i]["ticker"])
                   for i, r in enumerate(snap_records)}
    prov = {
        "artifact": "historical-constituent union (pre-reg #13 §1, amended)",
        "source": ("https://en.wikipedia.org/wiki/List_of_S%26P_600_companies"
                   " revision history (MediaWiki API)"),
        "snapshot_date": args.snapshot_date,
        "schedule": ("earliest 600-row table (2021-03) + most recent "
                     "revision before Y-07-01T00:00:00Z for 2021-2025; "
                     "S&P 1000-era revisions (2018-2021-01) excluded — "
                     "ghost-member table; reconstruction rejected (pre-reg "
                     "#13 §1)"),
        "snapshots": snap_records,
        "union": {
            "n_tickers": int(len(union)),
            "per_snapshot_ticker_sets": {y: len(s) for y, s in
                                         sorted(ticker_sets.items())},
            "pairwise_overlaps": {
                f"{a}|{b}": len(sa & sb)
                for a, sa in sorted(ticker_sets.items())
                for b, sb in sorted(ticker_sets.items()) if b > a},
        },
    }
    prov_path.write_text(json.dumps(prov, indent=2), encoding="utf-8")

    print(f"\nwrote {out.name}: {len(union)} union tickers "
          f"({len(frames)} snapshots)")
    print(f"wrote {prov_path.name}")
    print(union.head(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
