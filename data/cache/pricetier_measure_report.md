# Pre-registration #16 measure report — price-tier family (I-D-01 / I-X-06 / A-04)

- Mode: measure
- FROZEN_SHA: 675106eb8b31431566e8188828692b7a5624d1ae13a5df138c7c2197663e6e89
- measure_code_sha256: 8a717d52de909acb7af620549f68a499b596f96ae4e8e1e93b0b380d1dec779d

## F1 — price-tier screen (I-D-01/A-04)

- Universe: hist union 904 (names with bars); N = 10; era OOS 2022-2025 (IS 2021-06-30-2021-12-31 descriptive); COST 0.0015.

### F1 floors (pre-reg §2: >=100 bar-dates/slot AND >=10 distinct names/band-slot)

| slot | bar-dates | names (low/high) | met |
|---|---|---|---|
| F1a_2_5_vs_gt20 | 993 | 109/618 | yes |
| F1b_2_10_vs_gt10 | 993 | 240/686 | yes |
| F1c_10_20_vs_gt20 | 993 | 411/618 | yes |
| F1d_same_name | 35451 pairs | 153 (low) | yes |

### F1 verdicts (Holm at 0.05 across the 4 slots; EDGE iff Holm-rejected AND CI-low > 0)

| slot | n | est | CI-low | CI-high | p | gate | verdict |
|---|---|---|---|---|---|---|---|
| F1a_2_5_vs_gt20 | 993 | 0.0111 | 0.0086 | 0.0137 | 0.000 | 0.013 | EDGE |
| F1b_2_10_vs_gt10 | 993 | 0.0051 | 0.0037 | 0.0065 | 0.000 | 0.013 | EDGE |
| F1c_10_20_vs_gt20 | 993 | 0.0029 | 0.0021 | 0.0037 | 0.000 | 0.013 | EDGE |
| F1d_same_name | 35451 | 0.0792 | 0.0768 | 0.0818 | 0.000 | 0.013 | EDGE |

### F1 rows (per band — reported regardless of verdict; name-day collapse; lt2 descriptive)

| band | n_pairs | names | mean | median | p10 | p90 |
|---|---|---|---|---|---|---|
| lt2 | 5657 | 33 | 0.0610 | 0.0078 | -0.1682 | 0.2885 |
| 2-5 | 26809 | 110 | 0.0147 | 0.0028 | -0.1434 | 0.1697 |
| 5-10 | 68513 | 244 | 0.0053 | -0.0003 | -0.1173 | 0.1247 |
| 10-20 | 155791 | 422 | 0.0032 | -0.0002 | -0.1029 | 0.1102 |
| gt20 | 516196 | 628 | -0.0008 | -0.0017 | -0.0934 | 0.0926 |

Per-year per-band means (measurement row):
- lt2: 2021 -0.0039 (n=129), 2022 0.0072 (n=418), 2023 0.0640 (n=1031), 2024 0.0815 (n=1771), 2025 0.0574 (n=2308)
- 2-5: 2021 0.0118 (n=1068), 2022 0.0118 (n=4869), 2023 0.0197 (n=5633), 2024 0.0143 (n=6204), 2025 0.0136 (n=9035)
- 5-10: 2021 0.0086 (n=5158), 2022 0.0025 (n=12595), 2023 0.0073 (n=16703), 2024 0.0071 (n=16579), 2025 0.0026 (n=17478)
- 10-20: 2021 0.0053 (n=15239), 2022 -0.0004 (n=34777), 2023 0.0030 (n=36772), 2024 0.0045 (n=36522), 2025 0.0047 (n=32481)
- gt20: 2021 0.0009 (n=65329), 2022 -0.0084 (n=118099), 2023 0.0017 (n=111692), 2024 0.0020 (n=113769), 2025 0.0008 (n=107307)

IS window 2021-06-30–2021-12-31 (descriptive only):
- lt2: mean -0.0039 (n=129)
- 2-5: mean 0.0118 (n=1068)
- 5-10: mean 0.0086 (n=5158)
- 10-20: mean 0.0053 (n=15239)
- gt20: mean 0.0009 (n=65329)

- Name-day collapse: 772966 (name, bar-date) pairs across 706 distinct names.
- Drops (t+N beyond bars): {'lt2': 96, '2-5': 380, '5-10': 712, '10-20': 1264, 'gt20': 4608}

## F2 — long-term fall (I-X-06), cohort 2021-06 (2021-06 cohort), primary horizon 3y

### F2a — index-exit rate (removed at least once; exact from the frozen artifact: n_snapshots < max_n)

- low (<$10): n=35, rate 0.2571 | high (>$20): n=343, rate 0.2799
- contrast (low - high): -0.0227 (CI -0.1686..0.1324, p=0.756) — NO EDGE; floor >=30 names/leg: met

### F2b — cumulative returns (names with bars only; no-bar names excluded and counted)

- low (<$10): n=35, mean 0.3947 | high (>$20): n=339, mean 0.0596
- contrast (low - high): 0.3352 (CI 0.0094..0.7268, p=0.040) — FADE; floor: met

### F2 rows (per band: removal + returns; purge share; no-bar row)

| band | n | n_removed | removal_rate | 1y ret | 2y ret | 3y ret | 4y ret |
|---|---|---|---------------|
| 2-5 | 5 | 2 | 0.4000 | -0.0736 | -0.0493 | 0.0880 | 0.0801 |
| 5-10 | 30 | 7 | 0.2333 | -0.1310 | 0.0982 | 0.4458 | 0.6264 |
| 10-20 | 76 | 37 | 0.4868 | -0.0936 | 0.0085 | 0.1057 | 0.1843 |
| gt20 | 343 | 96 | 0.2799 | -0.1727 | -0.0678 | 0.0596 | 0.1265 |
| no_bars | 147 | 117 | 0.7959 | - | - | - | - |

## Sensitivities (exploratory, NO verdicts)

- S-N5: F1a_2_5_vs_gt20 0.0056 (n=998); F1b_2_10_vs_gt10 0.0025 (n=998); F1c_10_20_vs_gt20 0.0017 (n=998); F1d_same_name 0.0414 (n=-)
- S-N20: F1a_2_5_vs_gt20 0.0191 (n=983); F1b_2_10_vs_gt10 0.0097 (n=983); F1c_10_20_vs_gt20 0.0051 (n=983); F1d_same_name 0.1319 (n=-)
- S-BAND10: est 0.0057 (n=993)
- S-LAG5: est 0.0057 (n=993)
- S-REL: est 0.0060 (n=993)
- S-ERA: 2022 0.0083 (n=251); 2023 0.0062 (n=250); 2024 0.0053 (n=252); 2025 0.0031 (n=240)
- F2-horizons: 1y 0.0499 (n=35/336); 2y 0.1450 (n=35/337); 3y 0.3352 (n=35/339); 4y 0.4219 (n=35/342)

## Determinism

- report sha256: 04b31aa104406fe3f9f2a471bec8070a935b16bdb7e1ef776fb13c8f3280dcdb
