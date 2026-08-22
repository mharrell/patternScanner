# I-F-03 market-trend measurement report (pre-registration #18)

- Pre-registration #18 (frozen 2026-08-21): claim = 'Stocks will trend with the overall market unless they have a reason not to' (txWaMpSzHhM [31:55-32:38]). Ledger row I-F-03; priority-list item 17 (the final testable-daily item).
- Structural campaign: no forward returns, no entry/exit, no cost. The Phase-3 engine's measure_returns is NOT invoked — the claim is about co-movement, not profitability. Phase 5 cannot fire from this campaign by construction.
- Universe: current 603 (599 with bars; 4 missing logged). Market factor: SPY daily close-to-close (equal-weight S&P 600 mean = sensitivity S7). Era split: IS 2000-2015 / OOS 2016-2025 (by bar date).
- Bootstrap B=1000, seed 20260813, alpha 0.05, Holm within each family; catalyst = gap |open/prior close - 1| >= 0.02 OR RV = vol/mean(vol, prior 20) >= 2.0.

## Verdicts — Family 1 (market-trending baseline)

- **F1** (trend): n_stocks=598 | mean corr +0.4601 | CI +0.4521..+0.4681 | p 0.0000 (gate 0.0500) -> **EDGE (Holm-rejected; CI-low +0.4521 > 0 — stocks trend with the market, as claimed)**

## Verdicts — Family 2 (catalyst decoupling)

- **F2-gap** (decoupling): n_stocks=590 | mean diff +0.0968 | CI +0.0864..+0.1080 | p 0.0000 (gate 0.0250) -> **FADE (Holm-rejected; CI-low +0.0864 > 0 — correlation HIGHER on catalyst days, claim contradicted)**
- **F2-vol** (decoupling): n_stocks=589 | mean diff -0.2253 | CI -0.2357..-0.2134 | p 0.0000 (gate 0.0500) -> **EDGE (Holm-rejected; CI-upper -0.2134 < 0 — correlation lower on catalyst days, decoupling as claimed)**

## Verdicts — Family 3 (buck-the-trend)

- **F3-gap** (buck-the-run): n_down=1086 (excl 27) | mean contrast +0.0005 | CI -0.0009..+0.0019 | p 0.4880 (gate 0.0500) -> **NO EDGE (p 0.4880; est +0.0005; CI -0.0009..+0.0019)**
- **F3-vol** (buck-the-run): n_down=1080 (excl 33) | mean contrast +0.0021 | CI +0.0009..+0.0033 | p 0.0020 (gate 0.0250) -> **EDGE (Holm-rejected; CI-low +0.0009 > 0 — catalyst stocks run when the market runs, as claimed)**

## Census

| measure | value |
|---|---|
| n_stocks | 599 |
| oos_stock_days | 1371291 |
| cat_gap_stock_days | 105516 |
| cat_vol_stock_days | 74522 |
| f1_candidates | 598 |
| f2_gap_candidates | 590 |
| f2_vol_candidates | 589 |
| n_down_days_total | 1113 |

## Sensitivities (pre-declared, exploratory — NO verdicts)

- S1 gap=0.01: F2 n=598 | mean +0.1149 | CI +0.1065..+0.1225 | p 0.0000 | F3 n=1111 | mean -0.0024 | CI -0.0031..-0.0016 | p 0.0000
- S1 gap=0.03: F2 n=550 | mean +0.0856 | CI +0.0727..+0.0982 | p 0.0000 | F3 n=891 | mean +0.0012 | CI -0.0013..+0.0037 | p 0.3560
- S1 gap=0.05: F2 n=264 | mean +0.0305 | CI +0.0101..+0.0490 | p 0.0020 | F3 n=395 | mean +0.0016 | CI -0.0030..+0.0061 | p 0.5040
- S2 vol=1.5: F2 n=596 | mean -0.1483 | CI -0.1575..-0.1387 | p 0.0000 | F3 n=1108 | mean +0.0017 | CI +0.0011..+0.0023 | p 0.0000
- S2 vol=3.0: F2 n=483 | mean -0.3043 | CI -0.3212..-0.2891 | p 0.0000 | F3 n=701 | mean +0.0012 | CI -0.0021..+0.0046 | p 0.4520
- S3 combined gap-OR-vol: F2 n=595 | mean +0.0421 | CI +0.0325..+0.0518 | p 0.0000 | F3 n=1108 | mean -0.0001 | CI -0.0010..+0.0007 | p 0.7780
- S4 |market residual| cat - non: n=595 | mean +0.0185 | CI +0.0179..+0.0191 | p 0.0000
- S6 per-year: 2016: pooled -0.0015272229402730428 (cat 6168 / non 113023 days), F3-gap -0.0013031741603715251 (112 days); 2017: pooled 0.004448400438409778 (cat 3683 / non 119699 days), F3-gap 0.00637218184532452 (104 days); 2018: pooled 0.006423686835584506 (cat 4793 / non 124060 days), F3-gap 0.0034739074825049774 (114 days); 2019: pooled 0.001101638451583839 (cat 4947 / non 127964 days), F3-gap 0.0013933831851821704 (97 days); 2020: pooled 0.0037094814911924666 (cat 29631 / non 106675 days), F3-gap 0.001073010502370668 (107 days); 2021: pooled 0.0036915866083738597 (cat 9943 / non 131898 days), F3-gap 0.0051578875634205965 (104 days); 2022: pooled 0.001429161024944885 (cat 15092 / non 129568 days), F3-gap -0.005910907416668139 (138 days); 2023: pooled 0.007455611006513055 (cat 8453 / non 137353 days), F3-gap -0.003968106580835214 (109 days); 2024: pooled 0.004592002961885992 (cat 10054 / non 138947 days), F3-gap 0.00027285602914841744 (101 days); 2025: pooled -0.0036812250131891874 (cat 12752 / non 136588 days), F3-gap 0.0006096698002629814 (100 days)
- S7 EW market (6538 days): F1 n=598 | mean +0.5448 | CI +0.5344..+0.5549 | p 0.0000 | F2-gap n=590 | mean +0.0437 | CI +0.0340..+0.0536 | p 0.0000 | F2-vol n=589 | mean -0.2392 | CI -0.2521..-0.2265 | p 0.0000 | F3-gap n=1164 | mean -0.0009 | CI -0.0021..+0.0005 | p 0.2180 | F3-vol n=1161 | mean +0.0005 | CI -0.0007..+0.0016 | p 0.4160
- S8 F3-gap up-day contrast: down n=1086 | mean +0.0005 | CI -0.0009..+0.0020 | p 0.4640 | up n=1361 | mean +0.0100 | CI +0.0084..+0.0116 | p 0.0000 | down-minus-up -0.0095 (CI -0.0117..-0.0075, p 0.0000)
- S8 F3-vol up-day contrast: down n=1080 | mean +0.0021 | CI +0.0009..+0.0034 | p 0.0000 | up n=1356 | mean +0.0063 | CI +0.0050..+0.0079 | p 0.0000 | down-minus-up -0.0042 (CI -0.0062..-0.0023, p 0.0000)
- S9 F1 (z): n=598 mean z 0.5049107705731557, corr 0.4659704462031393
- S9 F2-gap (z): n=590 mean dz 0.14545458674677367, corr-diff 0.1444373981438885
- S9 F2-vol (z): n=589 mean dz -0.27047388830213237, corr-diff -0.2640657343456434

## IS record (2000-2015, descriptive — no verdicts)

- IS-f1: n=463 | mean +0.4220 | CI +0.4093..+0.4345 | p 0.0000
- IS-f2_gap: n=399 | mean +0.0097 | CI -0.0030..+0.0212 | p 0.1420
- IS-f2_vol: n=426 | mean -0.2082 | CI -0.2201..-0.1952 | p 0.0000
- IS-f3_gap: n=1809 | mean +0.0025 | CI +0.0011..+0.0041 | p 0.0000
- IS-f3_vol: n=1809 | mean +0.0055 | CI +0.0045..+0.0065 | p 0.0000

## Reproducibility

`python -X utf8 tools/measure_if03.py [--gate]` regenerates this report; the seed is fixed, so bootstrap results are stable across runs.
- Tool sha256: 86e382c4b6e7ebeb61babde9721b667830cfa19591b8fa1b40cda4676372e9f3 (frozen fixed-point sha 779861550ad3fc27…)
- Engine sha (measure.py, NOT invoked): 2d2c6b2ec85787c0
- Report sha256: c391458cdc96073e04ad7e6b8576b415894e14eabb8608862dbc003120b107a8

