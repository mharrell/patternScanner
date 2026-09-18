"""Nightly mover roster — the "his scanner" population capture (mover-
universe design, analysis/mover_universe_design.md §2).

Each evening after the close this fetches Yahoo's public day-gainers
screener with the FROZEN roster rule and writes two evidence files:

  data/mover_rosters/<session-date>.json   raw response + filter audit
  data/mover_rosters/<session-date>.csv    the roster (universe CSV for
                                           fetch_intraday_bars: `ticker`
                                           column + descriptors)

FROZEN RULE (design §2, fixed 2026-09-18 before first capture):
  1. last price $1.00-$20.00            (his stated bands, #25 §J.2)
  2. day volume >= 1,000,000 shares     (retail-scanner floor)
  3. listed exchanges NMS / NYQ / ASE   (no OTC/pinks — documented
                                        limitation)
  4. top 100 by % change after the filters

Discipline:
  * First capture of a session date wins; a later run the same night is
    a no-op (exit 0, "already captured") — rosters are append-only
    evidence and never rewritten.
  * Empty rosters are WRITTEN (empty CSV + JSON note) — a no-qualifier
    day is population data, never a silent skip.
  * The roster defines the population; bar-level measurement never uses
    screener numbers.
  * A screener schema/API change is an incident: the tool exits 3
    loudly and rosters halt — it does NOT adapt filters silently. Any
    rule change is a new population + new pre-registration.

Session-date semantics: the screener reflects the most recent completed
session. The recorded session date is today(ET) when fetched on a
weekday at/after 16:00 ET, else the most recent prior weekday. US
market holidays are NOT modeled (v1): on a holiday evening the roster
duplicates the prior session under the holiday's date — detectable via
the recorded quote dates; a known, documented artifact.

Usage:
  python -X utf8 tools/mover_roster.py            # capture (or no-op)
  python -X utf8 tools/mover_roster.py --dry-run  # fetch + report, write nothing

Exit: 0 ok (captured or already-captured), 1 network/API failure,
3 schema/integrity incident (roster rule could not be applied as
frozen).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

import pandas as pd
import yfinance as yf

REPO = Path(__file__).resolve().parents[1]
ROSTER_DIR = REPO / "data" / "mover_rosters"

# ---- frozen rule (design §2) ----
PRICE_MIN, PRICE_MAX = 1.00, 20.00
VOL_MIN = 1_000_000
EXCHANGES = ["NMS", "NYQ", "ASE"]
TOP_N = 100
SORT_FIELD = "percentchange"

ET = ZoneInfo("America/New_York")


def session_date(now: datetime | None = None) -> str:
    """The session the screener currently describes (see module doc)."""
    now = now or datetime.now(ET)
    d = now.date()
    if now.weekday() < 5 and now.hour >= 16:
        return d.isoformat()
    while d.weekday() >= 5:
        d = d.fromordinal(d.toordinal() - 1)
    if d == now.date():  # weekday but pre-16:00 → prior weekday
        d = d.fromordinal(d.toordinal() - 1)
        while d.weekday() >= 5:
            d = d.fromordinal(d.toordinal() - 1)
    return d.isoformat()


def build_query() -> "yf.EquityQuery":
    exch = yf.EquityQuery("IS-IN", ["exchange", *EXCHANGES])
    return yf.EquityQuery("AND", [
        yf.EquityQuery("EQ", ["region", "us"]),
        yf.EquityQuery("BTWN", ["eodprice", PRICE_MIN, PRICE_MAX]),
        yf.EquityQuery("GTE", ["dayvolume", VOL_MIN]),
        exch,
    ])


def fetch_screen() -> tuple[list[dict], str]:
    """Return (quotes, raw_sha256). Exits 3 on schema surprises."""
    q = build_query()
    res = yf.screen(q, size=250, offset=0, sortField=SORT_FIELD,
                    sortAsc=False)
    quotes = res.get("quotes") if isinstance(res, dict) else None
    if not isinstance(quotes, list):
        print(f"SCHEMA INCIDENT: unexpected screener shape "
              f"{type(res)!r} — halting (rule change = new pre-reg).",
              file=sys.stderr)
        sys.exit(3)
    raw = json.dumps(res, sort_keys=True, default=str).encode()
    return quotes, hashlib.sha256(raw).hexdigest()


def apply_rule(quotes: list[dict]) -> tuple[list[dict], dict]:
    """Apply the frozen rule to returned quotes; audit counts each step."""
    audit = {"returned": len(quotes), "dropped_not_equity": 0,
             "dropped_price": 0, "dropped_volume": 0,
             "dropped_exchange": 0, "kept": 0}
    rows = []
    for qt in quotes:
        if qt.get("quoteType") != "EQUITY" or not qt.get("symbol"):
            audit["dropped_not_equity"] += 1
            continue
        price = qt.get("regularMarketPrice")
        vol = qt.get("regularMarketVolume")
        exch = qt.get("exchange") or qt.get("fullExchangeName")
        pct = qt.get("regularMarketChangePercent")
        if price is None or not (PRICE_MIN <= price <= PRICE_MAX):
            audit["dropped_price"] += 1
            continue
        if vol is None or vol < VOL_MIN:
            audit["dropped_volume"] += 1
            continue
        if exch not in EXCHANGES:
            audit["dropped_exchange"] += 1
            continue
        rows.append({"ticker": qt["symbol"].replace("-", "."),
                     "company": (qt.get("shortName") or
                                 qt.get("longName") or "")[:80],
                     "price": price, "pct_change": pct,
                     "volume": vol, "exchange": exch})
    rows.sort(key=lambda r: (r["pct_change"] if r["pct_change"]
                             is not None else -1e9), reverse=True)
    rows = rows[:TOP_N]
    audit["kept"] = len(rows)
    return rows, audit


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="fetch + report; write nothing")
    args = ap.parse_args()

    ROSTER_DIR.mkdir(parents=True, exist_ok=True)
    sdate = session_date()
    csv_path = ROSTER_DIR / f"{sdate}.csv"
    json_path = ROSTER_DIR / f"{sdate}.json"

    quotes, raw_sha = fetch_screen()
    rows, audit = apply_rule(quotes)

    print(f"session date {sdate}: screener returned {audit['returned']}, "
          f"rule kept {audit['kept']} "
          f"(dropped: not-equity {audit['dropped_not_equity']}, "
          f"price {audit['dropped_price']}, volume {audit['dropped_volume']}, "
          f"exchange {audit['dropped_exchange']})")
    if rows:
        top = rows[0]
        print(f"  top: {top['ticker']} {top['pct_change']:+.1f}% "
              f"${top['price']:.2f} vol {top['volume']:,}")

    if args.dry_run:
        print("dry-run — nothing written")
        return 0
    if csv_path.exists():
        print(f"{csv_path.name} already captured — first capture wins "
              "(no-op)")
        return 0

    pd.DataFrame(rows).to_csv(csv_path, index=False)
    json_path.write_text(json.dumps({
        "session_date": sdate,
        "fetched_utc": datetime.now(ZoneInfo("UTC")).isoformat(),
        "rule": {"price": [PRICE_MIN, PRICE_MAX], "vol_min": VOL_MIN,
                 "exchanges": EXCHANGES, "top_n": TOP_N,
                 "sort": SORT_FIELD, "screen_size": 250},
        "audit": audit,
        "raw_response_sha256": raw_sha,
        "tickers": [r["ticker"] for r in rows],
    }, indent=2), encoding="utf-8")
    print(f"wrote {csv_path.name} + {json_path.name} ({len(rows)} tickers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
