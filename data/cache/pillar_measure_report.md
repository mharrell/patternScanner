# Pillar measurement report (pre-registration #1)

- Pre-registration #1 (frozen 2026-08-13): primary N=1, cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260813)
- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)
- Detections: pillar_detections_v1.csv (6550 rows) — dropped (exit beyond series end): {"H1": 0, "H2": 0, "H3": 0}
- Cohorts (H3 direct claim test): pillar_h3cohorts_v1.csv (65370 rows)
- Verdicts use OOS only; baseline windows are drawn from OOS bars only (era-matched).
- The strategy pays 0.15% round-trip; random-entries and same-ticker baselines pay it too; SPY buy-and-hold is raw (market benchmark).
- Operationalization (frozen in pillars.py): close-to-close gain leg ('still up at close' — the stronger subset per the translation table); rank over the full frozen universe (stricter than his pre-filtered scanner universe — documented, not adjusted); float = frozen snapshot (DESIGN_BRIEF §9 row 7 (a)); signals on a ticker's last bar skipped.
- H1/H2 fired 7/6 times in 26 years across 599 tickers, all in IS (2000-2010) — too rare to test; they enter the Holm family at p=1.0 and are Inconclusive by the >=100-detection floor.

## Verdicts (OOS 2016-2025, primary N=1)

- **H3**: n=2513 | mean -0.0019 (CI -0.1261..+0.1293) | p 0.7160 (Holm gate 0.0167) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- **H1**: n=0 | mean +nan (CI +nan..+nan) | p 1.0000 (Holm gate 0.0250) -> **INCONCLUSIVE (<100 OOS detections)**
- **H2**: n=0 | mean +nan (CI +nan..+nan) | p 1.0000 (Holm gate 0.0500) -> **INCONCLUSIVE (<100 OOS detections)**

## H3 direct claim test — day-paired rank-1 vs rank-2..10 (OOS)

- OOS days paired: 2513 (ranks 2-10 present on all; 0 cohort rows dropped at series end)
- rank-1 day-mean -0.0019 vs ranks 2-10 -0.0019 | paired diff +0.0000 (95% CI -0.0025..+0.0025), p=0.9860
- hit rate rank-1 0.440 vs ranks 2-10 0.455

*Reported, not Holm-gated: secondary analysis within H3.*

## Per-hypothesis detail (OOS, primary N=1)

### H1

n=0 OOS (of 7 total) — no verdict possible; all detections fell in IS. IS record (record only): n=7, mean -0.0509, median -0.0207, hit 0.286.

### H2

n=0 OOS (of 6 total) — no verdict possible; all detections fell in IS. IS record (record only): n=6, mean -0.0554, median -0.0398, hit 0.500.

### H3

n=2513 (of 6537 total) | mean -0.0019 (95% CI -0.1261..+0.1293) | median -0.0024

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.439 | 0.420..0.458 |
| Sharpe (annualized) | -0.47 | -1.13..0.13 |
| max drawdown (trade curve) | -1.000 | -1.000..-0.998 |

| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | -0.0006 | -0.0006 | -0.0034..+0.0023 | 0.7160 |
| same_ticker | -0.0007 | -0.0007 | -0.0037..+0.0023 | 0.6360 |
| spy | -0.0021 | -0.0021 | -0.0047..+0.0006 | 0.1100 |


## IS record (2000-2015) — observation only, no verdicts

| hypothesis | n | mean | median | hit rate |
|---|---|---|---|---|
| H1 | 7 | -0.0509 | -0.0207 | 0.286 |
| H2 | 6 | -0.0554 | -0.0398 | 0.500 |
| H3 | 4024 | +0.0002 | -0.0015 | 0.375 |

## Sensitivities (exploratory — NO verdicts)

- N=3 (dropped {"H1": 0, "H2": 0, "H3": 2}): OOS n=2511
  - H3: n=2511, mean -0.0003, hit 0.460
- N=5 (dropped {"H1": 0, "H2": 0, "H3": 4}): OOS n=2509
  - H3: n=2509, mean +0.0028, hit 0.459
- N=10 (dropped {"H1": 0, "H2": 0, "H3": 9}): OOS n=2504
  - H3: n=2504, mean +0.0163, hit 0.481
- high trigger at N=1 (dropped {"H1": 0, "H2": 0, "H3": 0}): OOS n=2513
  - H3: n=2513, mean -0.0043, hit 0.431
- $2-10 range at N=1 (dropped {"H1": 0, "H2": 0, "H3": 0}): OOS n=2513
  - H3: n=2513, mean -0.0019, hit 0.440
- One detection per ticker per 20-bar window (pre-reg #1 sensitivity; kept 4927 of 6550 detections, dropped {"H1": 0, "H2": 0, "H3": 0} unmeasurable):
  - H3: n=2045, mean -0.0018, hit 0.447

## Reproducibility

`python -X utf8 tools/measure_pillars.py` regenerates this report; the seed is fixed, so bootstrap results are stable across runs.
Input fingerprints: detections pillar_detections_v1.csv d5f80746f14f53fd…, pillar_detections_v1_high.csv e7d0388056df08ea…, pillar_detections_v1_r210.csv 25615cd68f2b14f9…, cohorts 67ac8bcffe7c82be…, measure code 26b71cdc6e0e17dd… (Phase-3 engine c7421fbf… imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
