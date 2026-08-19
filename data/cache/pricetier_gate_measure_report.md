# Pre-registration #16 measure report — price-tier family (I-D-01 / I-X-06 / A-04)

- Mode: gate
- FROZEN_SHA: 675106eb8b31431566e8188828692b7a5624d1ae13a5df138c7c2197663e6e89
- measure_code_sha256: 8a717d52de909acb7af620549f68a499b596f96ae4e8e1e93b0b380d1dec779d

## F1 — price-tier screen (I-D-01/A-04)

- Universe: current 603 (frozen 2026-08-13); N = 10; era OOS 2016-2025; COST 0.0015.

### F1 floors (pre-reg §2: >=100 bar-dates/slot AND >=10 distinct names/band-slot)

| slot | bar-dates | names (low/high) | met |
|---|---|---|---|
| F1a_2_5_vs_gt20 | 2504 | 119/566 | yes |
| F1b_2_10_vs_gt10 | 2504 | 282/597 | yes |
| F1c_10_20_vs_gt20 | 2504 | 469/566 | yes |
| F1d_same_name | 94688 pairs | 249 (low) | yes |

### F1 verdicts (Holm at 0.05 across the 4 slots; EDGE iff Holm-rejected AND CI-low > 0)

| slot | n | est | CI-low | CI-high | p | gate | verdict |
|---|---|---|---|---|---|---|---|
| F1a_2_5_vs_gt20 | 2504 | 0.0233 | 0.0206 | 0.0262 | 0.000 | 0.013 | EDGE |
| F1b_2_10_vs_gt10 | 2504 | 0.0105 | 0.0095 | 0.0115 | 0.000 | 0.013 | EDGE |
| F1c_10_20_vs_gt20 | 2504 | 0.0050 | 0.0045 | 0.0055 | 0.000 | 0.013 | EDGE |
| F1d_same_name | 94688 | 0.0399 | 0.0385 | 0.0412 | 0.000 | 0.013 | EDGE |

### F1 rows (per band — reported regardless of verdict; name-day collapse; lt2 descriptive)

| band | n_pairs | names | mean | median | p10 | p90 |
|---|---|---|---|---|---|---|
| lt2 | 2263 | 31 | 0.1198 | 0.0149 | -0.1444 | 0.3637 |
| 2-5 | 26318 | 119 | 0.0347 | 0.0135 | -0.1200 | 0.1997 |
| 5-10 | 112700 | 282 | 0.0151 | 0.0073 | -0.0956 | 0.1302 |
| 10-20 | 283772 | 469 | 0.0089 | 0.0050 | -0.0887 | 0.1107 |
| gt20 | 940379 | 566 | 0.0022 | 0.0018 | -0.0828 | 0.0880 |

Per-year per-band means (measurement row):
- lt2: 2016 0.0595 (n=501), 2017 0.0583 (n=278), 2018 0.0783 (n=53), 2019 0.0091 (n=126), 2020 0.1834 (n=512), 2021 0.3981 (n=228), 2022 0.0830 (n=104), 2023 0.0386 (n=228), 2024 0.1260 (n=149), 2025 -0.0121 (n=84)
- 2-5: 2016 0.0346 (n=4322), 2017 0.0169 (n=2819), 2018 0.0293 (n=2333), 2019 0.0274 (n=2849), 2020 0.0552 (n=5948), 2021 0.0483 (n=1395), 2022 0.0202 (n=1993), 2023 0.0290 (n=2009), 2024 0.0386 (n=1158), 2025 0.0210 (n=1492)
- 5-10: 2016 0.0217 (n=15404), 2017 0.0103 (n=11705), 2018 0.0046 (n=10201), 2019 0.0130 (n=11088), 2020 0.0231 (n=15077), 2021 0.0214 (n=8518), 2022 0.0118 (n=10636), 2023 0.0123 (n=11551), 2024 0.0205 (n=8485), 2025 0.0084 (n=10035)
- 10-20: 2016 0.0162 (n=32166), 2017 0.0082 (n=27517), 2018 0.0010 (n=29473), 2019 0.0087 (n=31079), 2020 0.0188 (n=32601), 2021 0.0120 (n=21448), 2022 -0.0018 (n=26255), 2023 0.0086 (n=28595), 2024 0.0075 (n=29671), 2025 0.0079 (n=24967)
- gt20: 2016 0.0090 (n=66814), 2017 0.0036 (n=81079), 2018 -0.0042 (n=86816), 2019 0.0064 (n=87778), 2020 0.0056 (n=82185), 2021 0.0052 (n=110279), 2022 -0.0069 (n=105675), 2023 0.0025 (n=103433), 2024 0.0038 (n=109544), 2025 0.0001 (n=106776)

IS window 2021-06-30–2021-12-31 (descriptive only):
- lt2: mean 0.5639 (n=163)
- 2-5: mean 0.0308 (n=623)
- 5-10: mean 0.0141 (n=4201)
- 10-20: mean 0.0069 (n=11191)
- gt20: mean 0.0019 (n=57484)

- Name-day collapse: 1365432 (name, bar-date) pairs across 599 distinct names.
- Drops (t+N beyond bars): {'lt2': 10, '2-5': 59, '5-10': 361, '10-20': 1030, 'gt20': 4530}

## F2 — long-term fall (I-X-06), cohort 2022-06 (2022-06 cohort), primary horizon 3.5y

### F2a — index-exit rate (removed at least once; exact from the frozen artifact: n_snapshots < max_n)

- low (<$10): n=5, rate 0.4000 | high (>$20): n=29, rate 0.2759
- contrast (low - high): - (CI -..-, p=1.000) — INCONCLUSIVE (floors unmet: 5/29 names); floor >=30 names/leg: UNMET

### F2b — cumulative returns (names with bars only; no-bar names excluded and counted)

- low (<$10): n=5, mean 0.4494 | high (>$20): n=29, mean -0.0572
- contrast (low - high): - (CI -..-, p=1.000) — INCONCLUSIVE (floors unmet: 5/29 names); floor: UNMET

### F2 rows (per band: removal + returns; purge share; no-bar row)

| band | n | n_removed | removal_rate | 1y ret | 2y ret | 3y ret | 3.5y ret |
|---|---|---|---------------|
| 2-5 | 1 | 1 | 1.0000 | -0.4935 | -0.7354 | -0.4707 | -0.4593 |
| 5-10 | 4 | 1 | 0.2500 | 0.3950 | 0.4712 | 0.5926 | 0.6766 |
| 10-20 | 15 | 2 | 0.1333 | 0.1469 | 0.1797 | 0.4564 | 0.5408 |
| gt20 | 29 | 8 | 0.2759 | -0.0294 | -0.1494 | -0.1587 | -0.0572 |
| no_bars | 16 | 8 | 0.5000 | - | - | - | - |

## §5 gate outcome

- F1 gate: a slot is INCONCLUSIVE when its floors are unmet (pre-reg §3 — gate UNMET with a documented data limitation); PASSED iff an EDGE survives with floors met.
- F1 gate: PASSED
- F2 gate: UNMET

## Determinism

- report sha256: 24b35d886452593a476da268c68510c137e8fb550e0b343a45fe5bea7da250f1
