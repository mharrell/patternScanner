# Momentum measurement report (pre-registration #4)

- Pre-registration #4 (frozen 2026-08-14): primary N=20, paired N=5, cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260813)
- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)
- Inputs: detections_v1.csv (31570 rows) and pillar_detections_v1.csv (H3 subset 6537 rows) — frozen pre-reg #2/#1 detections, no re-detection
- Two pre-registered verdict families, each Holm-corrected across A/C/H3 at alpha=0.05, OOS only: F1 absolute at N=20 vs era-matched baselines; F2 continuation (paired N=20 vs N=5 on identical entries)
- The strategy pays 0.15% round-trip; random-entries and same-ticker baselines pay it too; SPY is raw.

## Verdicts — Family 1: absolute at N=20 (vs baselines)

- **H3**: n=2494 | p 0.4720 (Holm gate 0.0167) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- **A**: n=5646 | p 0.6140 (Holm gate 0.0250) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- **C**: n=364 | p 0.8840 (Holm gate 0.0500) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

## Verdicts — Family 2: continuation (paired N=20 vs N=5)

- **A**: n=5646 | p 0.0000 (Holm gate 0.0167) -> **EDGE**
- **H3**: n=2494 | p 0.0000 (Holm gate 0.0250) -> **EDGE**
- **C**: n=364 | p 0.0380 (Holm gate 0.0500) -> **EDGE**

## Per-entry detail (OOS, primary N=20)

### Shape A
n=5646 | mean +0.0095 (CI -0.1757..+0.2244)
| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | -0.0025 | -0.0026 | -0.0082..+0.0041 | 0.3940 |
| same_ticker | -0.0014 | -0.0015 | -0.0074..+0.0052 | 0.6140 |
| spy | -0.0025 | -0.0028 | -0.0070..+0.0037 | 0.3360 |

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.523 | 0.510..0.536 |
| Sharpe (annualized, per-N) | 0.21 | 0.14..0.34 |
| max drawdown (trade curve) | -1.000 | -1.000..-1.000 |

### Shape C
n=364 | mean +0.0139 (CI -0.2002..+0.2695)
| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | +0.0011 | +0.0012 | -0.0176..+0.0191 | 0.8840 |
| same_ticker | +0.0023 | +0.0020 | -0.0133..+0.0199 | 0.8220 |
| spy | +0.0016 | +0.0017 | -0.0111..+0.0135 | 0.7640 |

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.524 | 0.472..0.574 |
| Sharpe (annualized, per-N) | 0.43 | 0.06..0.81 |
| max drawdown (trade curve) | -0.746 | -0.986..-0.740 |

### H3 rank-1
n=2494 | mean +0.0319 (CI -0.3769..+0.6812)
| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | +0.0200 | +0.0195 | +0.0059..+0.0363 | 0.0040 |
| same_ticker | +0.0066 | +0.0065 | -0.0086..+0.0244 | 0.4720 |
| spy | +0.0200 | +0.0199 | +0.0069..+0.0343 | 0.0040 |

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.497 | 0.477..0.518 |
| Sharpe (annualized, per-N) | 0.33 | 0.23..0.46 |
| max drawdown (trade curve) | -1.000 | -1.000..-1.000 |

## Continuation detail (OOS, paired)

- **A**: n_pairs=5646 | mean r5 -0.0008 | mean r20 +0.0095 | diff +0.0103 (95% CI +0.0066..+0.0161), p=0.0000
- **C**: n_pairs=364 | mean r5 +0.0024 | mean r20 +0.0139 | diff +0.0115 (95% CI +0.0010..+0.0217), p=0.0380
- **H3**: n_pairs=2494 | mean r5 +0.0028 | mean r20 +0.0319 | diff +0.0291 (95% CI +0.0178..+0.0431), p=0.0000

## IS record (2000-2015) — observation only, no verdicts

| family | n | mean |
|---|---|---|
| A | 8914 | +0.0129 |
| C | 688 | +0.0031 |
| H3 | 4024 | +0.0536 |

## Sensitivities (exploratory — NO verdicts)

- N=40 absolute: A: n=5611 mean +0.0149 | C: n=361 mean +0.0286 | H3: n=2474 mean +0.0738
- N=40 continuation (paired N=40 vs N=5): A: diff +0.0159 (p 0.000) | C: diff +0.0265 (p 0.000) | H3: diff +0.0711 (p 0.000)
- Dedupe-20 at N=20: A: n=4959 mean +0.0088 | C: n=339 mean +0.0146 | H3: n=2027 mean +0.0291
- Per-decade OOS at N=20 (A): 2016-2019: n=3243 mean +0.0087 | 2020-2025: n=2403 mean +0.0106
- Per-decade OOS at N=20 (C): 2016-2019: n=182 mean +0.0066 | 2020-2025: n=182 mean +0.0211
- Per-decade OOS at N=20 (H3): 2016-2019: n=1006 mean +0.0130 | 2020-2025: n=1488 mean +0.0447
- Shape B at N=20 (exploratory, no verdict): n=7148 mean -0.0001

## Reproducibility

`python -X utf8 tools/measure_momentum.py` regenerates this report; the seed is fixed, so bootstrap results are stable across runs.
Input fingerprints: detections_v1.csv 9b44f66160130c3a…, pillar_detections_v1.csv d5f80746f14f53fd…, momentum code 5b67a39a957e2e0e…, measure code c7421fbf… (Phase-3 engine imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
