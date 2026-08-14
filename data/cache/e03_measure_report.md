# E-03 measurement report (pre-registration #6)

- Pre-registration #6 (frozen 2026-08-14): N=10 primary, cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260813)
- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)
- Inputs: detections_v1.csv (31570 rows) -> e03_detections_v1.csv (31570 rows; warm-up-excluded 344, regime-undefined 491)
- Legs (frozen in tools/e03.py): bearish signal-line MACD (12,26,9) crossover within L=20 bars before the signal bar; regime = SPY close < SPY 200-day SMA at t.
- Three pre-registered verdict families, each Holm-corrected across A/B/C at alpha=0.05, OOS only: F1 (cross conditioning, all OOS), F2 (cross conditioning, bear days only), F3 (avoidance bar vs era-matched baselines). Negative claim — FADE EDGE requires CI upper bound < 0.
- The strategy pays 0.15% round-trip; random-entries and same-ticker baselines pay it too; SPY is raw.

## Verdicts — Family 1: cross conditioning, all OOS

- F1-cross-all-OOS C: n_crossed=204 | mean_crossed +0.0104 (not-crossed -0.0004) | excess +0.0107 (CI-hi +0.0301) | p 0.2300 (Holm gate 0.0167) -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**
- F1-cross-all-OOS A: n_crossed=3477 | mean_crossed +0.0021 (not-crossed +0.0070) | excess -0.0048 (CI-hi +0.0018) | p 0.2540 (Holm gate 0.0250) -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**
- F1-cross-all-OOS B: n_crossed=2930 | mean_crossed -0.0004 (not-crossed +0.0000) | excess -0.0005 (CI-hi +0.0032) | p 0.8100 (Holm gate 0.0500) -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**

## Verdicts — Family 2: cross conditioning, bear-market days only

- F2-cross-bear-days B: n_crossed=230 | mean_crossed -0.0095 (not-crossed +0.0070) | excess -0.0162 (CI-hi -0.0046) | p 0.0120 (Holm gate 0.0167) -> **FADE EDGE (Holm-rejected; conditioning excess (crossed - not-crossed) upper bound < 0)**
- F2-cross-bear-days A: n_crossed=170 | mean_crossed -0.0018 (not-crossed +0.0042) | excess -0.0060 (CI-hi +0.0088) | p 0.4560 (Holm gate 0.0250) -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**
- F2-cross-bear-days C: n_crossed=13 | mean_crossed +0.0226 (not-crossed +0.0177) | excess +0.0047 (CI-hi +0.0735) | p 0.8980 (Holm gate 0.0500) -> **INCONCLUSIVE (<100 crossed OOS detections)**

## Verdicts — Family 3: avoidance bar (crossed subset vs baselines)

- F3-avoidance-bar B: n_crossed=2930 | mean_crossed -0.0004 (not-crossed +nan) | excess -0.0053 (CI-hi -0.0010) | p 0.0140 (Holm gate 0.0167) -> **FADE EDGE (Holm-rejected; excess vs random AND same-ticker upper bound < 0)**
- F3-avoidance-bar A: n_crossed=3477 | mean_crossed +0.0021 (not-crossed +nan) | excess -0.0028 (CI-hi +0.0015) | p 0.1840 (Holm gate 0.0250) -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**
- F3-avoidance-bar C: n_crossed=204 | mean_crossed +0.0104 (not-crossed +nan) | excess +0.0059 (CI-hi +0.0235) | p 0.4700 (Holm gate 0.0500) -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**

## Per-shape detail (OOS, primary N=10)

### Shape A

F1: crossed n=3477 of 5641 | mean crossed +0.0021 vs not-crossed +0.0070 | excess -0.0048 (95% CI -0.0157..+0.0018) | p=0.2540 -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**

F2 (bear days): crossed n=170 vs not-crossed n=155 | mean -0.0018 vs +0.0042 | excess -0.0060 (95% CI -0.0211..+0.0088) | p=0.4560 -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**

F3: mean +0.0021 (95% CI -0.1278..+0.1481) | p=0.1840 -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.497 | 0.481..0.514 |
| Sharpe (annualized) | 0.16 | -0.01..0.31 |
| max drawdown (trade curve) | -1.000 | -1.000..-1.000 |

| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | -0.0028 | -0.0028 | -0.0065..+0.0010 | 0.1420 |
| same_ticker | -0.0023 | -0.0023 | -0.0057..+0.0015 | 0.1840 |
| spy | -0.0037 | -0.0038 | -0.0062..-0.0012 | 0.0020 |

### Shape B

F1: crossed n=2930 of 7198 | mean crossed -0.0004 vs not-crossed +0.0000 | excess -0.0005 (95% CI -0.0040..+0.0032) | p=0.8100 -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**

F2 (bear days): crossed n=230 vs not-crossed n=726 | mean -0.0095 vs +0.0070 | excess -0.0162 (95% CI -0.0278..-0.0046) | p=0.0120 -> **FADE EDGE (Holm-rejected; conditioning excess (crossed - not-crossed) upper bound < 0)**

F3: mean -0.0004 (95% CI -0.1484..+0.1587) | p=0.0140 -> **FADE EDGE (Holm-rejected; excess vs random AND same-ticker upper bound < 0)**

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.486 | 0.469..0.505 |
| Sharpe (annualized) | -0.02 | -0.20..0.16 |
| max drawdown (trade curve) | -1.000 | -1.000..-1.000 |

| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | -0.0053 | -0.0053 | -0.0100..-0.0010 | 0.0140 |
| same_ticker | -0.0057 | -0.0057 | -0.0102..-0.0014 | 0.0080 |
| spy | -0.0063 | -0.0063 | -0.0092..-0.0031 | 0.0000 |

### Shape C

F1: crossed n=204 of 331 | mean crossed +0.0104 vs not-crossed -0.0004 | excess +0.0107 (95% CI -0.0068..+0.0301) | p=0.2300 -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**

F2 (bear days): crossed n=13 vs not-crossed n=20 | mean +0.0226 vs +0.0177 | excess +0.0047 (95% CI -0.0600..+0.0735) | p=0.8980 -> **INCONCLUSIVE (<100 crossed OOS detections)**

F3: mean +0.0104 (95% CI -0.1173..+0.2121) | p=0.4700 -> **NO EDGE (CI includes 0 or estimate >= 0, or Holm gate not cleared)**

| metric | estimate | 95% CI |
|---|---|---|
| hit rate | 0.540 | 0.471..0.608 |
| Sharpe (annualized) | 0.61 | -0.08..1.30 |
| max drawdown (trade curve) | -0.630 | -0.933..-0.476 |

| baseline | mean excess | median excess | 95% CI | p (two-sided) |
|---|---|---|---|---|
| random_entries | +0.0059 | +0.0058 | -0.0109..+0.0220 | 0.4640 |
| same_ticker | +0.0062 | +0.0064 | -0.0114..+0.0235 | 0.4700 |
| spy | +0.0044 | +0.0042 | -0.0077..+0.0164 | 0.4820 |


## IS record (2000-2015) — observation only, no verdicts

| shape | n crossed | mean crossed | n not-crossed | mean not-crossed |
|---|---|---|---|---|
| A | 5544 | +0.0063 | 3269 | +0.0065 |
| B | 3681 | -0.0004 | 4964 | +0.0041 |
| C | 380 | -0.0010 | 194 | +0.0061 |

## Sensitivities (exploratory — NO verdicts)

- L=5 (cross within 5 bars) — crossed subset means: A: n=1019 mean +0.0029 | B: n=808 mean +0.0025 | C: n=29 mean -0.0248
- k in [0,20] (cross on or before the signal bar) — crossed subset means: A: n=3477 mean +0.0021 | B: n=2932 mean -0.0003 | C: n=204 mean +0.0104
- zero-line cross AT the signal bar (pre-reg #3 reading, no signal there) — crossed subset means: A: n=0 (no detections match) | B: n=0 (no detections match) | C: n=0 (no detections match)
- zero-line cross within L=20 — crossed subset means: A: n=1385 mean +0.0051 | B: n=795 mean -0.0003 | C: n=107 mean +0.0084
- bullish signal-line cross within L=20 (opposite direction) — crossed subset means: A: n=3676 mean +0.0060 | B: n=5142 mean +0.0004 | C: n=275 mean +0.0061
- Non-bear regime conditioning (F1 within non-bear OOS days): A: crossed n=3307 mean +0.0023 excess -0.0048 (p 0.3280) | B: crossed n=2700 mean +0.0004 excess +0.0018 (p 0.3420) | C: crossed n=191 mean +0.0096 excess +0.0131 (p 0.1240)
- Bear-days crossed subset vs baselines (F3 regime form): A: n=170 mean -0.0018 vs random -0.0073 (p 0.4220) vs same -0.0053 (p 0.5020) | B: n=230 mean -0.0095 vs random -0.0145 (p 0.0740) vs same -0.0140 (p 0.0840) | C: n=13 mean +0.0226 vs random +0.0163 (p 0.4960) vs same +0.0189 (p 0.4940)
- N=5: A: crossed n=3483 mean -0.0010 (not-crossed -0.0007) | B: crossed n=2934 mean -0.0026 (not-crossed -0.0009) | C: crossed n=204 mean +0.0057 (not-crossed +0.0005)
- N=20: A: crossed n=3466 mean +0.0068 (not-crossed +0.0134) | B: crossed n=2902 mean +0.0024 (not-crossed -0.0019) | C: crossed n=201 mean +0.0199 (not-crossed +0.0096)
- Per-year crossed-subset means (OOS): 2016: n=808 mean +0.0128 | 2017: n=882 mean -0.0047 | 2018: n=743 mean -0.0045 | 2019: n=791 mean +0.0022 | 2020: n=455 mean +0.0111 | 2021: n=635 mean -0.0010 | 2022: n=340 mean -0.0201 | 2023: n=661 mean +0.0037 | 2024: n=697 mean +0.0034 | 2025: n=599 mean +0.0023

## Reproducibility

`python -X utf8 tools/measure_e03.py` regenerates this report; the seed is fixed, so bootstrap results are stable across runs.
Input fingerprints: detections 9b44f66160130c3a…, e03 file 5ac5a3a1c64a3015…, e03 code 305e22a28497d54c…, measure code 12d6bb45164efe51… (Phase-3 engine c7421fbf… imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
