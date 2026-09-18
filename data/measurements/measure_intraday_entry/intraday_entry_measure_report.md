# Pre-registration #19 intraday entry-timing measure report — reversal new-high / pullback-count / second-confirmation (1-min)

- Mode: measure
- FROZEN_SHA: cac0e7ed205c8fbea62dad2c1f3f181cbe6b2b247d00c34c9c93b0c426c4b48c
- Window: bar-dates >= 2026-08-19

## F1 — reversal new-high (long/short), N=60, COST 0.15%

Family verdict: **FADE**
- long: n=43722, mean -0.0020, excess vs universe (primary) -0.0015 (CI -0.0016..-0.0014, p=0.000), same-ticker (secondary) -0.0007 (CI -0.0008..-0.0006, p=0.000), Holm 0.025, rejected) — FADE
- short: n=41985, mean -0.0011, excess vs universe (primary) -0.0016 (CI -0.0017..-0.0014, p=0.000), same-ticker (secondary) -0.0007 (CI -0.0008..-0.0005, p=0.000), Holm 0.050, rejected) — FADE

## F2 — pullback-count (early k<=2 vs late k>=3)

Family verdict: **NO EDGE**
- early − late: n_early=5812, n_late=2512, mean_early -0.0019, mean_late -0.0017, contrast -0.0002 (CI -0.0006..+0.0004, p=0.522) — NO EDGE

## F3 — second-confirmation (E2 − E1, paired)

Family verdict: **FADE**
- E2−E1: n=18008, mean_e1 -0.0013, mean_e2 -0.0020, contrast -0.0007 (CI -0.0007..-0.0007, p=0.000) — FADE

## Measurement rows (no verdicts)

- R:R long: mean 3.58, median 1.15, frac ≥2:1 0.359 (n=37543, degenerate 21731)
- R:R short: mean 3.65, median 1.12, frac ≥2:1 0.352 (n=36670, degenerate 19825)
- F1 events: 85707 measured of 115769 detected (dropped 30062); F2 8324 of 11392; F3 18008 pairs of 24244

### Pullback count by k (F2)

| k | n | mean | win rate |
|---|---|---|---|
| 1 | 3907 | -0.0022 | 0.383 |
| 2 | 1905 | -0.0013 | 0.426 |
| 3 | 1028 | -0.0018 | 0.399 |
| 4 | 610 | -0.0013 | 0.410 |
| 5+ | 874 | -0.0020 | 0.394 |

### Hour-of-day profile of F1 events (pre-reg #22 cross-check)

| hour (ET) | n | mean ret |
|---|---|---|
| 09:30-10:00 | 9954 | -0.0013 |
| 10:00-11:00 | 21204 | -0.0015 |
| 11:00-12:00 | 16174 | -0.0016 |
| 12:00-13:00 | 13097 | -0.0014 |
| 13:00-14:00 | 12215 | -0.0016 |
| 14:00-15:00 | 13063 | -0.0017 |
| 15:00-16:00 | 0 | - |

## Sensitivities (exploratory, NO verdicts)

- S-D2: {'n_f1_events': 345993, 'f1': 'FADE', 'f1_long': -0.0019191674539251083, 'f1_long_n': 130776, 'f2': 'NO EDGE', 'f3': 'FADE'}
- S-D5: {'n_f1_events': 14724, 'f1': 'FADE', 'f1_long': -0.0017829621853430973, 'f1_long_n': 5529, 'f2': 'NO EDGE', 'f3': 'FADE'}
- S-5M: {'n_f1_events': 21918, 'f1': 'NO EDGE', 'f1_long': -0.0032944433400071598, 'f1_long_n': 1262, 'f2': 'INCONCLUSIVE', 'f3': 'FADE'}
- S-C05: {'n_f1_events': 115769, 'f1': 'FADE', 'f1_long_mean': -0.000990939899572442, 'f2': 'NO EDGE', 'f3': 'FADE'}
- S-C30: {'n_f1_events': 115769, 'f1': 'FADE', 'f1_long_mean': -0.0034909398995724423, 'f2': 'NO EDGE', 'f3': 'FADE'}

## §6 audit

- Audit: **PASSED**

