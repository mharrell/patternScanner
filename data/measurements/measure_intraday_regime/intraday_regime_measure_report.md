# Pre-registration #22 measurement — the intraday regime

- tool sha (raw): `0a0528281f5d4795d4ed8a71da541a7cf8460d2ae19d7e5d5a83f2ecf733291d`
- tool FROZEN_SHA (fixed point): `e4502ba5cea73841338d4a1c239808d8557ff5a10850961c9f46abee71d164fc`
- frozen input `tools/measure_intraday_entry.py` sha256 (LF-normalized): `d58a889c6c0a634952bacd90bf412140709102053facebf1ee82b5df67592656`
- frozen input `tools/measure_intraday.py` sha256 (LF-normalized): `c58282caf75c344f228b70b329e9182b54a663d013891fe6a17103dc89f5e14c`
- window: bar-dates >= 2026-08-19

## Archive-integrity audit (§5)

- **PASSED**
- pulls checked: 39; ledger files: 15667
- repairs on record: 2
  - 2026-08-12/AAMI.parquet: corruption test - tampered file, deliberate removal
  - 2026-08-12/AAAA.parquet: review-test orphan repair
- window pulls:
  | pull_id | universe | requested | ok | failed |
  |---|---|---|---|---|
  | 20260820-040534 | universe_sp600_2026-08-13.csv | 603 | 603 | 0 |

## Sample-size floors (§4)

| floor | required | actual | met |
|---|---|---|---|
| min_bar_dates | 20 | 21 | ✓ |
| min_events | 2000 | 43722 | ✓ |
| min_tickers | 100 | 600 | ✓ |
| min_dates_with_events | 15 | 21 | ✓ |

## F1 — morning volatility/liquidity peak (2 Holm slots)

Family verdict: **INCONCLUSIVE**

- **B1** B1 (07:00-10:00) — coverage dates >= 10 names: 21 (runner 16:00-20:00 vol / 15:00-16:00 liq)
  - volatility: bucket mean |r| 0.0030 − runner 0.0030, diff 0.0000 (CI -0.0000 … 0.0000), p 0.546
  - liquidity: bucket share 0.0842 − runner 0.2741, diff -0.1899 (CI -0.1931 … -0.1868), p 0.000
  - Holm gate 0.050 — not rejected · verdict **INCONCLUSIVE**
- **B2** B2 (09:30-12:00) — coverage dates >= 10 names: 21 (runner 07:00-09:30 vol / 15:00-16:00 liq)
  - volatility: bucket mean |r| 0.0013 − runner 0.0045, diff -0.0032 (CI -0.0032 … -0.0031), p 0.000
  - liquidity: bucket share 0.3008 − runner 0.2741, diff 0.0266 (CI 0.0227 … 0.0305), p 0.000
  - Holm gate 0.025 — rejected · verdict **INCONCLUSIVE**

## F2 — the money claim (1 Holm slot)

Family verdict: **EDGE**
- B2 09:30-12:00 vs outside — n_a 23986 (in B2), n_b 19736 (outside); mean a -0.0018, mean b -0.0022
  - diff (B2 − outside) 0.0004 (CI 0.0002 … 0.0005), p 0.000 · Holm gate 0.050 — rejected · verdict **EDGE**
  - hour-matched baseline excess (same-ticker): -0.0005 (CI -0.0007 … -0.0004))
  - hour-matched baseline excess (universe): -0.0015 (CI -0.0016 … -0.0013))

## F3 — pre-market cleanliness (1 Holm slot)

Family verdict: **FADE**
- pre-market 04:00-09:30 vs RTH 09:30-16:00 — n pre 164963, n rth 3144038
  - mean |r|: pre 0.0039 − rth 0.0009, diff 0.0030 (CI 0.0030 … 0.0030), p 0.000
  - tail frac: pre 0.1981 − rth 0.1320, diff 0.0661 (CI 0.0642 … 0.0683), p 0.000
  - Holm gate 0.050 — rejected · verdict **FADE**

## Measurement rows (NO verdicts)

### Continuity: time-of-day profile
| bucket | mean |r| | mean (H−L)/O | volume share |
|---|---|---|---|
| 04:00-07:00 | 0.0027 | 0.0014 | 0.0000 |
| 07:00-09:30 | 0.0045 | 0.0026 | 0.0000 |
| 09:30-10:00 | 0.0024 | 0.0022 | 0.0842 |
| 10:00-11:00 | 0.0013 | 0.0010 | 0.1170 |
| 11:00-12:00 | 0.0008 | 0.0007 | 0.0997 |
| 12:00-13:00 | 0.0007 | 0.0006 | 0.0861 |
| 13:00-14:00 | 0.0006 | 0.0005 | 0.0872 |
| 14:00-15:00 | 0.0006 | 0.0006 | 0.1026 |
| 15:00-16:00 | 0.0008 | 0.0009 | 0.2741 |
| 16:00-20:00 | 0.0030 | 0.0006 | 0.1492 |
### Continuity: pre-market vs RTH
- premarket_04_0930: mean |r| 0.0039, median 0.0005, tail frac 0.1981, n 164963
- rth_0930_1600: mean |r| 0.0009, median 0.0005, tail frac 0.1320, n 3144038
- 09:30-10:30 single hour: mean |r| 0.0019, tail frac 0.1239, n 480682
- 09:30-09:35 first 5 min: mean |r| 0.0039, tail frac 0.0685, n 30192
- leader freq by_bar_date (n 21): B1 vol 1.0000, B1 liq 0.0000, B2 vol 0.0000, B2 liq 0.0000
- leader freq by_ticker (n 603): B1 vol 0.6119, B1 liq 0.0116, B2 vol 0.1642, B2 liq 0.0182
### F2 returns per entry hour
| hour | n | mean ret |
|---|---|---|
| 09 | 5082 | -0.0022 |
| 10 | 10734 | -0.0015 |
| 11 | 8170 | -0.0020 |
| 12 | 6706 | -0.0017 |
| 13 | 6238 | -0.0018 |
| 14 | 6792 | -0.0030 |

