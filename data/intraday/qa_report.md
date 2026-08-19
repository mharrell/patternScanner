# Intraday archive QA report

- Generated: 2026-08-19T00:13:07.887471-04:00
- Files checked: 30 (6 tickers, 5 bar-dates)
- QA tool: `tools/qa_intraday.py` — flags only, nothing deleted or corrected
- Daily envelope source: `C:\Users\Silver Pangolin\PycharmProjects\patternScanner\.claude\worktrees\intraday-accumulation\data\cache\bars`

## Summary

- regular-session coverage < 98%: 15 files
- interior gap minutes across archive: 9771
- envelope violations (high/low): 0 / 0
- volume-sum mismatches (> 2%): 0
- naive-tz / not-minute-floored / unsorted / dup-ts files: 0 / 0 / 0 / 0

## Anomalies (flagged, not fixed)

| file | rows | RTH coverage | gap minutes | OHLC violations | env>High | env<Low | vol ratio | zero-vol mins | NaN prices | non-pos prices | dup timestamps | naive tz | not floored | unsorted | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-08-12/AAMI.parquet | 264 | 60.5% | 666 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | RTH coverage 60.5% < 98% |
| 2026-08-12/AAP.parquet | 416 | 91.8% | 530 | 0 | 0 | 0 |  | 57 | 0 | 0 | 0 |  |  |  | RTH coverage 91.8% < 98% |
| 2026-08-12/AAPL.parquet | 958 | 105.4% | 2 | 0 | 0 | 0 |  | 568 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-12/AAT.parquet | 161 | 31.8% | 769 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | RTH coverage 31.8% < 98% |
| 2026-08-12/MSFT.parquet | 958 | 105.4% | 2 | 0 | 0 | 0 |  | 567 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-12/SPY.parquet | 942 | 101.5% | 18 | 0 | 0 | 0 |  | 551 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-13/AAMI.parquet | 289 | 63.8% | 645 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | RTH coverage 63.8% < 98% |
| 2026-08-13/AAP.parquet | 422 | 96.4% | 519 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | RTH coverage 96.4% < 98% |
| 2026-08-13/AAPL.parquet | 960 | 105.4% | 0 | 0 | 0 | 0 |  | 570 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-13/AAT.parquet | 236 | 54.1% | 697 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | RTH coverage 54.1% < 98% |
| 2026-08-13/MSFT.parquet | 955 | 105.4% | 5 | 0 | 0 | 0 |  | 564 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-13/SPY.parquet | 944 | 101.5% | 16 | 0 | 0 | 0 |  | 553 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-14/AAMI.parquet | 227 | 51.8% | 703 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | RTH coverage 51.8% < 98% |
| 2026-08-14/AAP.parquet | 411 | 94.9% | 542 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  | RTH coverage 94.9% < 98% |
| 2026-08-14/AAPL.parquet | 959 | 105.4% | 1 | 0 | 0 | 0 |  | 568 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-14/AAT.parquet | 214 | 45.9% | 721 | 0 | 0 | 0 |  | 34 | 0 | 0 | 0 |  |  |  | RTH coverage 45.9% < 98% |
| 2026-08-14/MSFT.parquet | 944 | 105.4% | 16 | 0 | 0 | 0 |  | 553 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-14/SPY.parquet | 943 | 101.5% | 17 | 0 | 0 | 0 |  | 552 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-17/AAMI.parquet | 275 | 58.7% | 654 | 0 | 0 | 0 |  | 47 | 0 | 0 | 0 |  |  |  | RTH coverage 58.7% < 98% |
| 2026-08-17/AAP.parquet | 411 | 92.6% | 544 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | RTH coverage 92.6% < 98% |
| 2026-08-17/AAPL.parquet | 958 | 105.4% | 2 | 0 | 0 | 0 |  | 567 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-17/AAT.parquet | 217 | 47.4% | 723 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | RTH coverage 47.4% < 98% |
| 2026-08-17/MSFT.parquet | 959 | 105.4% | 1 | 0 | 0 | 0 |  | 568 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-17/SPY.parquet | 944 | 101.5% | 16 | 0 | 0 | 0 |  | 553 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-18/AAMI.parquet | 292 | 69.2% | 635 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | RTH coverage 69.2% < 98% |
| 2026-08-18/AAP.parquet | 436 | 96.9% | 523 | 0 | 0 | 0 |  | 57 | 0 | 0 | 0 |  |  |  | RTH coverage 96.9% < 98% |
| 2026-08-18/AAPL.parquet | 959 | 105.4% | 1 | 0 | 0 | 0 |  | 568 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-18/AAT.parquet | 148 | 30.8% | 786 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | RTH coverage 30.8% < 98% |
| 2026-08-18/MSFT.parquet | 959 | 105.4% | 1 | 0 | 0 | 0 |  | 568 | 0 | 0 | 0 |  |  |  |  |
| 2026-08-18/SPY.parquet | 944 | 101.5% | 16 | 0 | 0 | 0 |  | 553 | 0 | 0 | 0 |  |  |  |  |

## Known expected patterns (not defects)

- **Thin-name minute sparsity (verified 2026-08-18):** Yahoo 1m emits
  a bar only when the name prints a trade/quote, so thinly-traded
  S&P 600 names show real RTH minute gaps (e.g. AAT ~30-55% RTH
  coverage) while liquid names are complete (AAPL/MSFT/SPY 390/390
  RTH). This is data reality, not a pipeline fault — measurement on
  thin names must resample (e.g. 5-min) or count RTH coverage.
- Pre-market span often starts later than 04:00 for thin names
  (Yahoo coverage); regular session 09:30-16:00 is the strict check.
- Envelope/volume tolerances absorb dividend adjustments on the
  adjusted daily bars; a *sustained* break across many files is the
  signature of an unrecorded split — record it in
  `data/intraday/splits.json` (procedure in the README).
- The archive starts fresh: earlier bar-dates are legitimately
  absent before enough nightly pulls have run.

_(end of QA report — 30 files checked)_
