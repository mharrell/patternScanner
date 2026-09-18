# Pre-registration #21 measurement — the two-filter veto

- tool sha (raw): `94ac41bf97f184992d170b49ce712d114e291fbce3b8ba7b7c91c2e861007042`
- tool FROZEN_SHA (fixed point): `6989330642d0e23951cb6b00d8343df37025428ac1349fef73b9e4da0d3e833a`
- frozen input `tools/measure_intraday_entry.py` sha256 (LF-normalized): `d58a889c6c0a634952bacd90bf412140709102053facebf1ee82b5df67592656`
- frozen input `tools/measure_intraday.py` sha256 (LF-normalized): `c58282caf75c344f228b70b329e9182b54a663d013891fe6a17103dc89f5e14c`
- window: bar-dates >= 2026-08-19

## Archive-integrity audit (§5/§6)

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

## F1 — conditioning (4 Holm slots)

Family verdict: **NO EDGE**

| slot | n (a/b) | mean a | mean b | diff (a − b) | CI 95% | p | Holm gate | rej | verdict |
|---|---|---|---|---|---|---|---|---|---|
| pass − fail | 13225 (13225/28270) | -0.0020 | -0.0020 | -0.0000 | -0.0002 … 0.0002 | 0.834 | 0.025 | — | NO EDGE |
| pass − raw | 13225 (13225/41495) | -0.0020 | -0.0020 | -0.0000 | -0.0002 … 0.0002 | 0.886 | 0.050 | — | NO EDGE |
| macd leg (MACD ≥ 0 − MACD < 0) | 13651 (13651/27844) | -0.0020 | -0.0019 | -0.0001 | -0.0003 … 0.0001 | 0.326 | 0.017 | — | NO EDGE |
| volume leg (no spike − spike) | 1663 (42059/1663) | -0.0020 | -0.0023 | 0.0003 | -0.0002 … 0.0008 | 0.278 | 0.013 | — | NO EDGE |

## F2 — kill-rate decomposition (rows, NO verdicts)

- classifiable entries: 41495 (MACD warm-up unmet: 2227)
- veto-pass: 13225 (0.3187)  ·  veto-fail: 28270 (0.6813)
- MACD leg kills: 27844 (0.6710)  ·  volume leg kills: 1564 (0.0377)  ·  both: 1138 (0.0274)
- mean forward — pass: -0.0020, fail: -0.0020, diff (pass−fail): -0.0000
- mean forward — MACD ≥ 0: -0.0020, MACD < 0: -0.0019, vol spike: -0.0023, no spike: -0.0020
- pass set excess vs hour-matched baseline — same-ticker: -0.0024 (CI -0.0027 … -0.0022), universe: -0.0015 (CI -0.0017 … -0.0013))

### By bar-date

| date | n | pass rate |
|---|---|---|
| 2026-08-19 | 2291 | 0.3767 |
| 2026-08-20 | 2188 | 0.2811 |
| 2026-08-21 | 1907 | 0.3697 |
| 2026-08-24 | 1810 | 0.3094 |
| 2026-08-25 | 1619 | 0.3119 |
| 2026-08-26 | 1598 | 0.3185 |
| 2026-08-27 | 1729 | 0.3308 |
| 2026-08-28 | 1953 | 0.2734 |
| 2026-08-31 | 1857 | 0.2752 |
| 2026-09-01 | 2318 | 0.2627 |
| 2026-09-02 | 2035 | 0.4329 |
| 2026-09-03 | 1960 | 0.3469 |
| 2026-09-04 | 1633 | 0.3870 |
| 2026-09-08 | 1953 | 0.2939 |
| 2026-09-09 | 2106 | 0.2574 |
| 2026-09-10 | 1995 | 0.2967 |
| 2026-09-11 | 1738 | 0.3297 |
| 2026-09-14 | 2212 | 0.3440 |
| 2026-09-15 | 2196 | 0.3169 |
| 2026-09-16 | 2325 | 0.2834 |
| 2026-09-17 | 2072 | 0.3147 |

## Sensitivities (pre-declared, NO verdicts)

- S-V2: F1 family NO EDGE — pass − fail n=12907 est=-0.0000 p=0.944 NO EDGE; pass − raw n=12907 est=-0.0000 p=0.928 NO EDGE; macd leg (MACD ≥ 0 − MACD < 0) n=13651 est=-0.0001 p=0.332 NO EDGE; volume leg (no spike − spike) n=2826 est=0.0002 p=0.416 NO EDGE
- S-V5: F1 family NO EDGE — pass − fail n=13445 est=-0.0000 p=0.642 NO EDGE; pass − raw n=13445 est=-0.0000 p=0.806 NO EDGE; macd leg (MACD ≥ 0 − MACD < 0) n=13651 est=-0.0001 p=0.340 NO EDGE; volume leg (no spike − spike) n=800 est=-0.0001 p=0.742 NO EDGE
- S-C05: F1 family NO EDGE — pass − fail n=13225 est=-0.0000 p=0.834 NO EDGE; pass − raw n=13225 est=-0.0000 p=0.924 NO EDGE; macd leg (MACD ≥ 0 − MACD < 0) n=13651 est=-0.0001 p=0.358 NO EDGE; volume leg (no spike − spike) n=1663 est=0.0003 p=0.292 NO EDGE
- S-C30: F1 family NO EDGE — pass − fail n=13225 est=-0.0000 p=0.894 NO EDGE; pass − raw n=13225 est=-0.0000 p=0.896 NO EDGE; macd leg (MACD ≥ 0 − MACD < 0) n=13651 est=-0.0001 p=0.346 NO EDGE; volume leg (no spike − spike) n=1663 est=0.0003 p=0.222 NO EDGE
- S-N15: F1 family NO EDGE — pass − fail n=15993 est=-0.0000 p=0.312 NO EDGE; pass − raw n=15993 est=-0.0000 p=0.426 NO EDGE; macd leg (MACD ≥ 0 − MACD < 0) n=16575 est=-0.0001 p=0.126 NO EDGE; volume leg (no spike − spike) n=2271 est=0.0002 p=0.126 NO EDGE
- S-N120: F1 family NO EDGE — pass − fail n=10414 est=-0.0003 p=0.060 NO EDGE; pass − raw n=10414 est=-0.0002 p=0.170 NO EDGE; macd leg (MACD ≥ 0 − MACD < 0) n=10747 est=-0.0004 p=0.006 FADE; volume leg (no spike − spike) n=1290 est=0.0002 p=0.582 NO EDGE
- S-N240: F1 family NO EDGE — pass − fail n=5059 est=-0.0002 p=0.612 NO EDGE; pass − raw n=5059 est=-0.0001 p=0.710 NO EDGE; macd leg (MACD ≥ 0 − MACD < 0) n=5237 est=-0.0003 p=0.260 NO EDGE; volume leg (no spike − spike) n=663 est=0.0001 p=0.896 NO EDGE
- S-B01: F1 family INCONCLUSIVE — pass − fail n=799 est=0.0000 p=0.948 NO EDGE; pass − raw n=1071 est=-0.0000 p=0.970 NO EDGE; macd leg (MACD ≥ 0 − MACD < 0) n=762 est=-0.0001 p=0.778 NO EDGE; volume leg (no spike − spike) n=70 est=— p=1.000 INCONCLUSIVE

