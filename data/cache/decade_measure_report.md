# Per-decade drift report (pre-registration #5)

- Pre-registration #5 (frozen 2026-08-14): primary N=20, paired N=5, cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260813)
- Era split: IS 2000-2015 / OOS 2016-2025, sub-eras 2016-01-01..2020-01-01 (early) and 2020-01-01..2026-01-01 (late), by signal date
- Inputs: detections_v1.csv (31570 rows) and pillar_detections_v1.csv (H3 subset 6537 rows) — frozen
- Two pre-registered verdict families, each Holm-corrected across A/C/H3 at alpha=0.05: F1 sub-era excess difference (late minus early, two-sample bootstrap); F2 late-era absolute vs within-sub-era baselines
- Baselines are drawn only from bars whose start date falls in the same sub-era (era-matched at sub-era granularity); strategy and baselines pay 0.15% round-trip; SPY is raw.

## Verdicts — Family 1: sub-era excess difference (2020-25 minus 2016-19, N=20)

- **H3**: n=1006 | p 0.1380 (Holm gate 0.0167) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- **C**: n=182 | p 0.2960 (Holm gate 0.0250) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- **A**: n=2403 | p 0.5100 (Holm gate 0.0500) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

## Verdicts — Family 2: late-era absolute at N=20 (within-sub-era baselines)

- **H3**: n=1488 | p 0.2380 (Holm gate 0.0167) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- **C**: n=182 | p 0.4440 (Holm gate 0.0250) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- **A**: n=2403 | p 0.9720 (Holm gate 0.0500) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

## Family 1 detail (two-sample bootstrap)

### A
n_early 3243 | n_late 2403 | excess_early -0.0052 | excess_late -0.0004
| baseline | diff (late - early) | 95% CI | p |
|---|---|---|---|
| random | +0.0047 | -0.0071..+0.0179 | 0.5100 |
| same | +0.0061 | -0.0051..+0.0208 | 0.3040 |
### C
n_early 182 | n_late 182 | excess_early -0.0073 | excess_late +0.0102
| baseline | diff (late - early) | 95% CI | p |
|---|---|---|---|
| random | +0.0179 | -0.0170..+0.0505 | 0.2960 |
| same | +0.0206 | -0.0134..+0.0521 | 0.2120 |
### H3
n_early 1006 | n_late 1488 | excess_early -0.0009 | excess_late +0.0337
| baseline | diff (late - early) | 95% CI | p |
|---|---|---|---|
| random | +0.0348 | +0.0080..+0.0622 | 0.0080 |
| same | +0.0240 | -0.0069..+0.0551 | 0.1380 |

## Family 2 detail (late-era absolute)

### A
n=2403 | mean +0.0106 (CI -0.1969..+0.2352)
| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | -0.0007 | -0.0012 | -0.0117..+0.0121 | 0.8360 |
| same_ticker | +0.0004 | -0.0001 | -0.0101..+0.0135 | 0.9720 |
| spy | -0.0017 | -0.0022 | -0.0103..+0.0120 | 0.6660 |

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.507 | 0.488..0.527 |
| Sharpe (annualized, per-N) | 0.16 | 0.07..0.30 |

### C
n=182 | mean +0.0211 (CI -0.2001..+0.2616)
| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | +0.0093 | +0.0098 | -0.0172..+0.0364 | 0.4440 |
| same_ticker | +0.0122 | +0.0121 | -0.0157..+0.0377 | 0.3460 |
| spy | +0.0091 | +0.0091 | -0.0096..+0.0277 | 0.3660 |

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.565 | 0.495..0.632 |
| Sharpe (annualized, per-N) | 0.64 | 0.14..1.14 |

### H3
n=1488 | mean +0.0447 (CI -0.3673..+0.8095)
| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | +0.0338 | +0.0327 | +0.0134..+0.0585 | 0.0020 |
| same_ticker | +0.0147 | +0.0144 | -0.0088..+0.0404 | 0.2380 |
| spy | +0.0324 | +0.0321 | +0.0130..+0.0537 | 0.0000 |

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.491 | 0.465..0.515 |
| Sharpe (annualized, per-N) | 0.40 | 0.27..0.57 |


## Sensitivities (exploratory — NO verdicts)

- Continuation A: early diff +0.0094 (n=3243) | late diff +0.0115 (n=2403) | late-early +0.0022 (CI -0.0066..+0.0141, p 0.8060)
- Continuation C: early diff +0.0066 (n=182) | late diff +0.0164 (n=182) | late-early +0.0098 (CI -0.0106..+0.0301, p 0.3540)
- Continuation H3: early diff +0.0123 (n=1006) | late diff +0.0404 (n=1488) | late-early +0.0281 (CI +0.0045..+0.0534, p 0.0200)
- Early-era absolute A: n=3243 mean +0.0087 (vs random -0.0052, p 0.0440)
- Early-era absolute C: n=182 mean +0.0066 (vs random -0.0079, p 0.4900)
- Early-era absolute H3: n=1006 mean +0.0130 (vs random -0.0008, p 0.9420)
- N=40 A: early +0.0195 (n=3243) | late +0.0087 (n=2368)
- N=40 C: early +0.0441 (n=182) | late +0.0129 (n=179)
- N=40 H3: early +0.0381 (n=1006) | late +0.0982 (n=1468)
- Per-year N=20 means: 2016: A +0.039, C +0.014, H3 +0.057 | 2017: A +0.005, C +0.007, H3 +0.007 | 2018: A -0.005, C -0.016, H3 -0.011 | 2019: A +0.001, C +0.027, H3 -0.002 | 2020: A -0.017, C +0.075, H3 +0.091 | 2021: A +0.034, C -0.004, H3 +0.062 | 2022: A -0.011, C +0.049, H3 +0.001 | 2023: A -0.014, C +0.018, H3 +0.061 | 2024: A +0.033, C +0.007, H3 +0.046 | 2025: A +0.002, C -0.037, H3 +0.004
- Dedupe-20 by sub-era: A_early: n=2782 mean +0.0080 | C_early: n=168 mean +0.0085 | H3_early: n=791 mean +0.0227 | A_late: n=2177 mean +0.0099 | C_late: n=171 mean +0.0206 | H3_late: n=1236 mean +0.0332

## Reproducibility

`python -X utf8 tools/measure_decade.py` regenerates this report; the seed is fixed, so bootstrap results are stable across runs.
Input fingerprints: detections_v1.csv 9b44f66160130c3a…, pillar_detections_v1.csv d5f80746f14f53fd…, decade code c9451c59135e6439…, measure code c7421fbf… (Phase-3 engine imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
