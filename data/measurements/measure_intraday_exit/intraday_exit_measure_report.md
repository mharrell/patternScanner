# Pre-registration #20 measurement — intraday exit rules

- tool sha (raw): `04fc14b7222a6c062915d4747b8d6441e7c7275e1efe4c70f896899523d47b16`
- tool FROZEN_SHA (fixed point): `71aca8c2b79da1b112d057d0c6f2745c95405bb6a1041d8e93ab3e12854a8a3a`
- frozen input `tools/measure_intraday.py` sha256 (LF-normalized): `c58282caf75c344f228b70b329e9182b54a663d013891fe6a17103dc89f5e14c`
- window: bar-dates >= 2026-08-19

## Archive-integrity audit (§5/§6)

- **PASSED**
- pulls checked: 52; ledger files: 21677
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
| min_bar_dates | 20 | 31 | ✓ |
| min_events | 2000 | 2029 | ✓ |
| min_tickers | 100 | 401 | ✓ |
| min_dates_with_events | 15 | 31 | ✓ |

## F1 — rule vs fixed-N (primary) / fixed-2R (secondary)

Family verdict: **NO EDGE**

| slot | n | mean rule | mean fixed-N | excess | CI 95% | p | Holm gate | rej | verdict |
|---|---|---|---|---|---|---|---|---|---|
| breakeven-trail | 2029 | -0.0015 | -0.0020 | 0.0006 | 0.0001 … 0.0010 | 0.018 | 0.017 | — | NO EDGE |
| ladder | 2029 | -0.0021 | -0.0020 | -0.0000 | -0.0004 … 0.0003 | 0.862 | 0.025 | — | NO EDGE |
| flat-out | 2029 | -0.0020 | -0.0020 | -0.0000 | -0.0000 … 0.0000 | 0.870 | 0.050 | — | NO EDGE |

Secondary (fixed-2R):

| slot | mean fixed-2R | diff | CI 95% | p |
|---|---|---|---|---|
| breakeven-trail | -0.0017 | 0.0002 | 0.0001 … 0.0004 | 0.004 |
| ladder | -0.0017 | -0.0004 | -0.0007 … -0.0001 | 0.012 |
| flat-out | -0.0017 | -0.0003 | -0.0008 … 0.0001 | 0.130 |

## F2 — the flat premise

Contrast (mean N-forward flat − matched non-flat): —   CI 95% — … —   p 1.000   n 94   verdict **INCONCLUSIVE**

## Measurement rows

- entries (F1 set): 2029
- ladder reach 9MA: 0.9911 (2011)
- ladder reach 20MA: 0.9704 (1969)
- ladder reach VWAP: 0.8674 (1760)
- breakeven-trail half fired: 0.1316 (267)
- flat-out trades (flat events): 94

### By bar-date

| date | n | mean fixed-N | mean breakeven | mean ladder | mean flat |
|---|---|---|---|---|---|
| 2026-08-19 | 96 | -0.0028 | -0.0012 | -0.0027 | -0.0029 |
| 2026-08-20 | 49 | -0.0073 | -0.0021 | -0.0054 | -0.0072 |
| 2026-08-21 | 77 | -0.0011 | -0.0012 | -0.0029 | -0.0010 |
| 2026-08-24 | 49 | -0.0011 | -0.0013 | -0.0017 | -0.0012 |
| 2026-08-25 | 63 | -0.0036 | -0.0019 | -0.0033 | -0.0036 |
| 2026-08-26 | 47 | -0.0029 | -0.0009 | -0.0005 | -0.0030 |
| 2026-08-27 | 56 | 0.0018 | -0.0017 | -0.0006 | 0.0016 |
| 2026-08-28 | 57 | -0.0051 | -0.0018 | -0.0035 | -0.0051 |
| 2026-08-31 | 49 | -0.0038 | -0.0016 | -0.0028 | -0.0037 |
| 2026-09-01 | 59 | -0.0034 | -0.0016 | -0.0020 | -0.0034 |
| 2026-09-02 | 79 | -0.0016 | -0.0015 | -0.0031 | -0.0017 |
| 2026-09-03 | 64 | -0.0033 | -0.0017 | -0.0024 | -0.0033 |
| 2026-09-04 | 67 | -0.0005 | -0.0015 | -0.0016 | -0.0006 |
| 2026-09-08 | 64 | -0.0003 | -0.0016 | -0.0013 | -0.0003 |
| 2026-09-09 | 54 | -0.0034 | -0.0019 | -0.0026 | -0.0034 |
| 2026-09-10 | 61 | -0.0019 | -0.0013 | -0.0023 | -0.0019 |
| 2026-09-11 | 55 | -0.0014 | -0.0017 | -0.0014 | -0.0014 |
| 2026-09-14 | 72 | -0.0033 | -0.0022 | -0.0027 | -0.0032 |
| 2026-09-15 | 76 | -0.0017 | -0.0016 | -0.0013 | -0.0018 |
| 2026-09-16 | 73 | -0.0043 | -0.0016 | -0.0048 | -0.0041 |
| 2026-09-17 | 58 | 0.0008 | -0.0013 | -0.0012 | 0.0009 |
| 2026-09-18 | 53 | -0.0003 | -0.0013 | -0.0014 | -0.0003 |
| 2026-09-21 | 61 | -0.0013 | -0.0016 | -0.0018 | -0.0014 |
| 2026-09-22 | 80 | -0.0038 | -0.0013 | -0.0024 | -0.0038 |
| 2026-09-23 | 82 | 0.0002 | -0.0009 | -0.0008 | 0.0003 |
| 2026-09-24 | 72 | 0.0001 | -0.0011 | -0.0001 | -0.0000 |
| 2026-09-25 | 80 | -0.0002 | -0.0007 | -0.0006 | -0.0003 |
| 2026-09-28 | 62 | -0.0027 | -0.0018 | -0.0019 | -0.0026 |
| 2026-09-29 | 53 | -0.0038 | -0.0012 | -0.0023 | -0.0040 |
| 2026-09-30 | 63 | -0.0037 | -0.0015 | -0.0028 | -0.0036 |
| 2026-10-01 | 98 | 0.0001 | -0.0013 | -0.0006 | 0.0001 |

## Sensitivities (pre-declared, NO verdicts)

- S-C05: F1 family NO EDGE — breakeven-trail n=2029 diff=0.0006 p=0.008, ladder n=2029 diff=-0.0000 p=0.820, flat-out n=2029 diff=-0.0000 p=0.858
- S-C30: F1 family NO EDGE — breakeven-trail n=2029 diff=0.0006 p=0.008, ladder n=2029 diff=-0.0000 p=0.820, flat-out n=2029 diff=-0.0000 p=0.858
- S-E2: F1 family NO EDGE — breakeven-trail n=2029 diff=0.0006 p=0.008, ladder n=2029 diff=-0.0000 p=0.820, flat-out n=2029 diff=0.0001 p=0.110
- S-M20: F1 family NO EDGE — breakeven-trail n=2029 diff=0.0006 p=0.008, ladder n=2029 diff=-0.0000 p=0.820, flat-out n=2029 diff=0.0000 p=0.662

