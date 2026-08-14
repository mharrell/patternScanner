# Veto measurement report (pre-registration #3)

- Pre-registration #3 (frozen 2026-08-14): N=10 primary, cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260813)
- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)
- Inputs: detections_v1.csv (31570 rows) -> veto_detections_v1.csv (31570 rows; warm-up-excluded 344)
- Veto (frozen in tools/veto.py): kill = MACD(12,26) line < 0 OR (red candle AND vol >= 2.0x prior-20 mean); pass = both legs clear.
- Two pre-registered verdict families, each Holm-corrected across A/B/C at alpha=0.05, OOS only: F1 (conditioning — the claim as stated), F2 (absolute bar vs era-matched baselines).
- The strategy pays 0.15% round-trip; random-entries and same-ticker baselines pay it too; SPY is raw.

## Verdicts — Family 1: conditioning (subset vs full set)

- F1-conditioning A: n_pass=3941 | mean +0.0021 (full +0.0040) | excess -0.0019 (CI-lo -0.0057) | p 0.3540 (Holm gate 0.0167) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- F1-conditioning C: n_pass=280 | mean +0.0046 (full +0.0062) | excess -0.0017 (CI-lo -0.0152) | p 0.7980 (Holm gate 0.0250) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- F1-conditioning B: n_pass=6940 | mean -0.0001 (full -0.0001) | excess +0.0000 (CI-lo -0.0026) | p 0.9880 (Holm gate 0.0500) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

## Verdicts — Family 2: absolute bar (vs baselines)

- F2-absolute B: n_pass=6940 | mean -0.0001 (full +nan) | excess -0.0050 (CI-lo -0.0080) | p 0.0020 (Holm gate 0.0167) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- F2-absolute A: n_pass=3941 | mean +0.0021 (full +nan) | excess -0.0027 (CI-lo -0.0064) | p 0.1480 (Holm gate 0.0250) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**
- F2-absolute C: n_pass=280 | mean +0.0046 (full +nan) | excess -0.0007 (CI-lo -0.0155) | p 0.9780 (Holm gate 0.0500) -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

## Kill-rate decomposition (OOS; E-04: filters killing setups vs setups working)

| shape | total det | OOS | pass | killed | macd-alone | vol-alone | both | mean(pass) | mean(killed) |
|---|---|---|---|---|---|---|---|---|---|
| A | 14464 | 5651 | 3941 | 1700 | 1106 | 456 | 141 | +0.0021 | +0.0083 |
| B | 15857 | 7212 | 6940 | 258 | 136 | 122 | 0 | -0.0001 | -0.0007 |
| C | 905 | 331 | 280 | 51 | 44 | 6 | 1 | +0.0046 | +0.0154 |

## Per-shape detail (OOS, primary N=10)

### Shape A

F1 conditioning: pass n=3941 of 5641 | mean pass +0.0021 vs full +0.0040 | excess -0.0019 (95% CI -0.0057..+0.0016) | p=0.3540 -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

F2 absolute: n=3941 | mean +0.0021 (95% CI -0.1289..+0.1496) | p=0.1480 -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.486 | 0.472..0.502 |
| Sharpe (annualized) | 0.16 | 0.00..0.31 |
| max drawdown (trade curve) | -1.000 | -1.000..-1.000 |

| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | -0.0027 | -0.0027 | -0.0064..+0.0010 | 0.1480 |
| same_ticker | -0.0028 | -0.0028 | -0.0063..+0.0006 | 0.1080 |
| spy | -0.0037 | -0.0036 | -0.0060..-0.0016 | 0.0000 |

### Shape B

F1 conditioning: pass n=6940 of 7198 | mean pass -0.0001 vs full -0.0001 | excess +0.0000 (95% CI -0.0026..+0.0024) | p=0.9880 -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

F2 absolute: n=6940 | mean -0.0001 (95% CI -0.1579..+0.1619) | p=0.0020 -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.490 | 0.479..0.501 |
| Sharpe (annualized) | -0.01 | -0.13..0.11 |
| max drawdown (trade curve) | -1.000 | -1.000..-1.000 |

| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | -0.0050 | -0.0049 | -0.0080..-0.0023 | 0.0000 |
| same_ticker | -0.0050 | -0.0050 | -0.0077..-0.0023 | 0.0020 |
| spy | -0.0060 | -0.0060 | -0.0079..-0.0041 | 0.0000 |

### Shape C

F1 conditioning: pass n=280 of 331 | mean pass +0.0046 vs full +0.0062 | excess -0.0017 (95% CI -0.0152..+0.0106) | p=0.7980 -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

F2 absolute: n=280 | mean +0.0046 (95% CI -0.1624..+0.1709) | p=0.9780 -> **NO EDGE (mean <= 0 or CI includes 0, or Holm gate not cleared)**

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.528 | 0.475..0.586 |
| Sharpe (annualized) | 0.29 | -0.32..0.89 |
| max drawdown (trade curve) | -0.651 | -0.960..-0.553 |

| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | -0.0007 | -0.0010 | -0.0144..+0.0132 | 0.8880 |
| same_ticker | -0.0002 | -0.0001 | -0.0155..+0.0136 | 0.9780 |
| spy | -0.0012 | -0.0011 | -0.0115..+0.0088 | 0.8180 |


## IS record (2000-2015) — observation only, no verdicts

| shape | n pass | mean pass | n full | mean full |
|---|---|---|---|---|
| A | 6365 | +0.0070 | 8813 | +0.0064 |
| B | 8446 | +0.0019 | 8645 | +0.0022 |
| C | 487 | +0.0006 | 574 | +0.0014 |

## Sensitivities (exploratory — NO verdicts)

- N=5: A: pass n=3948 mean -0.0005 (full -0.0009) | B: pass n=6952 mean -0.0018 (full -0.0016) | C: pass n=280 mean +0.0030 (full +0.0037)
- N=20: A: pass n=3926 mean +0.0053 (full +0.0094) | B: pass n=6873 mean -0.0006 (full -0.0002) | C: pass n=276 mean +0.0111 (full +0.0159)
- MACD zero-crossing reading: A: n=5046 mean +0.0027 | B: n=7076 mean +0.0000 | C: n=324 mean +0.0058
- volume leg V=1.5: A: n=3941 mean +0.0021 | B: n=6910 mean -0.0001 | C: n=275 mean +0.0064
- volume leg V=3.0: A: n=4182 mean +0.0018 | B: n=6988 mean -0.0002 | C: n=281 mean +0.0049
- Veto on H3 rank-1 cohort (N=1, full H3): n=2513 mean -0.0019
- Veto on H3 rank-1 cohort (N=1, veto-passing H3): n=1543 mean -0.0018

## Reproducibility

`python -X utf8 tools/measure_veto.py` regenerates this report; the seed is fixed, so bootstrap results are stable across runs.
Input fingerprints: detections 9b44f66160130c3a…, veto file eebdc6b11a19e243…, veto code 162bab437e0dc95f…, measure code 214c907131d07a54… (Phase-3 engine c7421fbf… imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
