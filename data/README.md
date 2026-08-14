# Phase 1 — data pipeline

Status: **done 2026-08-13** (DESIGN_BRIEF Phase 1 exit: "Clean 2000–2025 daily
bars, documented gaps").

## Layout

| Path | Contents | Size |
|---|---|---|
| `cache/universe_sp600_2026-08-13.csv` | Frozen S&P 600 membership snapshot + float (603 rows; **tracked in git**, never updated) | 53 KB |
| `cache/bars/<ticker>.parquet` | Adjusted daily OHLCV, 2000-01-01→2025-12-31, per ticker (gitignored, regenerable) | 599 files, 117 MB |
| `cache/fetch_log.json` | Per-ticker fetch status, spans, meta (gitignored) | 400 KB |
| `cache/qa_report.md` | QA pass output (tracked) | — |
| `README.md` (this file) | Provenance + documented gaps | — |

## Provenance

- **Membership:** Wikipedia "List of S&P 600 companies", snapshot date
  2026-08-13 (frozen; per PREREGISTRATION §5). Wikipedia lists 603 rows vs
  600 index members — recent additions mid-transition; snapshot as published.
- **Float:** Yahoo `floatShares`, fallback `sharesOutstanding`, fetched once
  at snapshot via yfinance `get_info`. Coverage 603/603:
  - 601 × `floatShares`
  - 1 × `sharesOutstanding` (fallback per pre-reg §5)
  - 1 × `floatShares(base:CWEN)` — CWEN-A doesn't exist on Yahoo's quote
    API; base symbol `CWEN` is the same Clearway Energy class-A security
- **Bars:** yfinance 1.6.0, `auto_adjust=True` (splits/dividends), window
  `2000-01-01` → `2026-01-01` (exclusive), curl_cffi TLS impersonation.

Reproduce (in order):

```
python -X utf8 tools/build_universe.py --snapshot-date 2026-08-13
python -X utf8 tools/fetch_daily_bars.py --threads 6
python -X utf8 tools/qa_data.py
```

## Coverage

- 599/603 tickers have bars; all 599 reach 2025-12-31 (no delisted members
  — expected, the universe is current constituents, see survivorship).
- 282 tickers have the full 2000–2025 window; 317 IPO'd later (expected).
- **Interior gaps > 7 calendar days: 0.**
- 4 tickers have **no Yahoo chart data at all**: ADIG (ADI Global
  Distribution), MBGL (Mobility Global), MFP (Midera Food Processing),
  VGNT (Versigent PLC) — recent index additions. They contribute no
  detections; documented, not substituted.

## Documented artifacts (flagged in `qa_report.md`, NOT fixed)

1. **Zero-volume days — 19,186 across the universe, 63% before 2008.**
   Yahoo's historical volume series has a known pre-2008 gap for some
   names (AGX: 1,226 zero-volume days, all pre-2014). Impact: the
   relative-volume legs (≥5× / ≥10× mean) see fewer *eligible* days in
   early epochs; the series is internally consistent, so this biases
   detection counts per decade, not returns. Handled at measurement time
   (per-decade breakdown is already pre-registered).
2. **Adjusted-OHLC inconsistencies — 306 tickers, up to $53.74 (LEU,
   25% of its median price; CPF 59.6%).** Yahoo's split/dividend
   adjustment multiplies each day's OHLC by a per-day factor, so bars
   around large special dividends / reverse splits can have
   `High < max(Open, Close)` or `Low > min(Open, Close)`. Close-based
   features and returns are unaffected; High/Low-based shape features
   (new-high signals, stop levels) can be distorted on isolated days.
   Phase 2 decision (pre-register): use Close-only features, or clamp.
3. **|Daily return| > 50% — 91 tickers**, e.g. AAP +14% in a day
   (2025-05-22, real — 27.5M shares). Mostly real gaps/halts; a few
   adjustment artifacts. Flagged, kept.
4. **Survivorship (structural):** current constituents only — the null is
   strengthened, positives need historical lists (pre-reg §5(b)).

## Measurement-stage notes (Phase 3)

- N=1 horizon uses `(c_{t+1} − o_{t+1}) / o_{t+1}` — Open/Close only,
  unaffected by artifact 2.
- Zero-volume days must be handled in the volume-ratio legs (0/0 → NaN);
  decision logged in Phase 2 pre-registration.
- The 4 no-data names and the pre-2008 volume gap reduce detection counts
  in affected eras — the verdict rules (<100 detections → inconclusive)
  already price that in.
