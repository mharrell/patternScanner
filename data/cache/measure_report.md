# Phase 3 measurement report

- Pre-registration #2 (frozen 2026-08-13): N=10, cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260813)
- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date; an exit crossing the boundary is attributed to the signal date)
- Detections: detections_v1.csv (31570 rows) — dropped (exit beyond series end): {"A": 10, "B": 14, "C": 0}
- Verdicts use OOS only; baseline windows are drawn from OOS bars only (era-matched).
- The strategy pays 0.15% round-trip; random-entries and same-ticker baselines pay it too; SPY buy-and-hold is raw (market benchmark).
- Max drawdown: trade-equity curve ordered by signal date, cumprod(1+ret), no capital constraints — approximate by design.

## Verdicts (OOS 2016-2025, primary N)

- **B**: n=7218 | mean -0.0002 (CI -0.1577..+0.1615) | p 0.0020 (Holm gate 0.0167) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- **C**: n=368 | mean +0.0033 (CI -0.1751..+0.1769) | p 0.8300 (Holm gate 0.0250) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- **A**: n=5669 | mean +0.0042 (CI -0.1286..+0.1472) | p 0.9120 (Holm gate 0.0500) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

## Per-shape detail (OOS, primary N)

### Shape A

n=5669 (of 14583 total) | mean +0.0042 (95% CI -0.1286..+0.1472) | median -0.0006

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.495 | 0.483..0.509 |
| Sharpe (annualized) | 0.17 | 0.09..0.29 |
| max drawdown (trade curve) | -1.000 | -1.000..-1.000 |

| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | -0.0008 | -0.0010 | -0.0045..+0.0041 | 0.6440 |
| same_ticker | -0.0002 | -0.0003 | -0.0042..+0.0046 | 0.9120 |
| spy | -0.0016 | -0.0018 | -0.0046..+0.0025 | 0.3520 |

### Shape B

n=7218 (of 15907 total) | mean -0.0002 (95% CI -0.1577..+0.1615) | median -0.0013

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.491 | 0.479..0.502 |
| Sharpe (annualized) | -0.01 | -0.13..0.11 |
| max drawdown (trade curve) | -1.000 | -1.000..-1.000 |

| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | -0.0050 | -0.0050 | -0.0081..-0.0022 | 0.0020 |
| same_ticker | -0.0053 | -0.0052 | -0.0079..-0.0028 | 0.0000 |
| spy | -0.0060 | -0.0060 | -0.0079..-0.0041 | 0.0000 |

### Shape C

n=368 (of 1056 total) | mean +0.0033 (95% CI -0.1751..+0.1769) | median +0.0029

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.528 | 0.476..0.579 |
| Sharpe (annualized) | 0.19 | -0.33..0.69 |
| max drawdown (trade curve) | -0.819 | -0.988..-0.743 |

| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | -0.0016 | -0.0016 | -0.0151..+0.0117 | 0.7980 |
| same_ticker | -0.0014 | -0.0015 | -0.0133..+0.0109 | 0.8300 |
| spy | -0.0023 | -0.0023 | -0.0120..+0.0065 | 0.6060 |


## IS record (2000-2015) — observation only, no verdicts

| shape | n | mean | median | hit rate |
|---|---|---|---|---|
| A | 8914 | +0.0065 | +0.0019 | 0.519 |
| B | 8689 | +0.0023 | +0.0004 | 0.504 |
| C | 688 | +0.0011 | +0.0004 | 0.504 |

## Per-decade breakdown (all detections, record only)

| shape | decade | n | mean | hit rate |
|---|---|---|---|---|
| A | 2000s | 4990 | +0.0073 | 0.519 |
| A | 2010s | 7167 | +0.0042 | 0.506 |
| A | 2020s | 2426 | +0.0063 | 0.502 |
| B | 2000s | 4783 | +0.0053 | 0.510 |
| B | 2010s | 6598 | -0.0012 | 0.500 |
| B | 2020s | 4526 | +0.0004 | 0.483 |
| C | 2000s | 470 | -0.0003 | 0.489 |
| C | 2010s | 400 | +0.0017 | 0.542 |
| C | 2020s | 186 | +0.0077 | 0.511 |

## Sensitivities (exploratory — NO verdicts)

- N=5 (dropped {"A": 0, "B": 2, "C": 0}): OOS n=13277
  - A: n=5679, mean -0.0008, hit 0.467
  - B: n=7230, mean -0.0016, hit 0.481
  - C: n=368, mean +0.0021, hit 0.524
- N=20 (dropped {"A": 33, "B": 84, "C": 4}): OOS n=13158
  - A: n=5646, mean +0.0095, hit 0.522
  - B: n=7148, mean -0.0001, hit 0.479
  - C: n=364, mean +0.0139, hit 0.525
- One detection per ticker per 20-bar window (pre-reg #1 §3 sensitivity; kept 26082 of 31570 detections, dropped {"A": 9, "B": 13, "C": 0} unmeasurable):
  - A: n=4982, mean +0.0037, hit 0.492
  - B: n=5979, mean +0.0007, hit 0.497
  - C: n=343, mean +0.0036, hit 0.531

## Reproducibility

`python -X utf8 tools/measure.py` regenerates this report; the seed is fixed, so bootstrap results are stable across runs.
Input fingerprints: detections 9b44f6616013…, measure code c7421fbffeaf….
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
