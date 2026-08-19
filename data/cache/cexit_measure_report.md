# Pre-registration #17 — C-exit comparison: indicator exits vs fixed-2R on the same entries (C-01/C-03/C-04)

mode: **measure** — frozen pre-reg #2 A/B/C detections, OOS 2016-01-01..2025-12-31 by signal date
tool: tools/measure_cexit.py (frozen 2026-08-19, FROZEN_SHA afcc0222fcd4…)

## Input fingerprints
- detectors.py — e93ddf7a… (frozen; asserted at import)
- detections_v1.csv — 9b44f661… (frozen; asserted at import)
- universe_sp600_hist_2026-08-15.csv — 62f681d58cdb… (gate universe)
- bars parquets — 597

## Contract (pre-reg #17 §3–§4)
- entries: frozen A/B/C detections; entry = open of signal+1
- stops: A min(low i-10..i-1) · B min(low i-3..i-1) · C min(l1, l2)
- R = E − S; outcome = (fill − E)/R − 0.0015·E/R
- fixed arm: +2R target / −1R stop, trigger fills
- indicator arm: −1R stop, no target; exit = first of S1 high-volume red / S2 anchored-VWAP break / S3 9-EMA break / S4 two-steps-down; fills at signal close; same-bar stop+signal → stop; max-hold e+20
- validity: i+20 < n; R ≤ 0 or out-of-range events dropped (counted)
- F1 est = mean(ind) − mean(fix); F2 est = mean(baseline) − mean(post-exit); F3 est = quantile(ind) − quantile(fix)
- date-paired bootstrap B=1000, seed 20260819; Holm α=0.05 per family; floors 100 events / 20 dates per slot

## Drops (events excluded and why)
| reason | n |
| --- | --- |
| end | 121 |
| no_bars | 0 |
| r_le_0 | 84 |

## F1 — system contrast, est = mean(ind R) − mean(fix R) (Holm 0.05/4)
| slot | n | dates | mean ind | mean fix | est | CI low | CI high | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 5605 | 1646 | -4.0582 | -3.9805 | -0.0777 | -0.1320 | -0.0307 | 0.0000 | FADE (Holm-rejected; CI-upper < 0 — claim contradicts) |
| B | 7105 | 1623 | -0.0422 | -0.0687 | +0.0265 | -0.0118 | +0.0630 | 0.1720 | NO EDGE (p 0.172; est +0.0265; CI -0.0118..+0.0630) |
| C | 364 | 321 | +0.0013 | +0.0941 | -0.0928 | -0.1799 | -0.0055 | 0.0380 | NO EDGE (p 0.038; est -0.0928; CI -0.1799..-0.0055) |
| pooled | 13074 | 2114 | -1.7627 | -1.7412 | -0.0215 | -0.0537 | +0.0105 | 0.2020 | NO EDGE (p 0.202; est -0.0215; CI -0.0537..+0.0105) |

## F2 — per-signal exit timing, est = mean(baseline) − mean(post-exit) (Holm 0.05/4)
| signal | n | dates | drops_end | n_baseline | mean post | mean base | est | CI low | CI high | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| s1 | 3020 | 1285 | 1 | 30200 | +0.0040 | +0.0083 | +0.0043 | +0.0009 | +0.0076 | 0.0140 | EDGE (Holm-rejected; CI-low > 0 — claim holds) |
| s2 | 9082 | 1923 | 0 | 90820 | +0.0025 | +0.0071 | +0.0046 | +0.0014 | +0.0078 | 0.0060 | EDGE (Holm-rejected; CI-low > 0 — claim holds) |
| s3 | 150 | 126 | 0 | 1500 | +0.0034 | +0.0064 | +0.0030 | -0.0103 | +0.0162 | 0.6900 | NO EDGE (p 0.690; est +0.0030; CI -0.0103..+0.0162) |
| s4 | 195 | 156 | 0 | 1950 | +0.0118 | +0.0038 | -0.0080 | -0.0193 | +0.0050 | 0.1980 | NO EDGE (p 0.198; est -0.0080; CI -0.0193..+0.0050) |

## F3 — C-04 upper tail, est = quantile(ind R) − quantile(fix R), pooled (Holm 0.05/3)
| slot | q | n | dates | est | CI low | CI high | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| q90 | 0.90 | 13074 | 2114 | -1.4840 | -1.5318 | -1.4389 | 0.0000 | FADE (Holm-rejected; CI-upper < 0 — claim contradicts) |
| q95 | 0.95 | 13074 | 2114 | -1.0385 | -1.1144 | -0.9569 | 0.0000 | FADE (Holm-rejected; CI-upper < 0 — claim contradicts) |
| q99 | 0.99 | 13074 | 2114 | +0.6767 | +0.4584 | +0.9178 | 0.0000 | EDGE (Holm-rejected; CI-low > 0 — claim holds) |

## Measurements
- bind_s1_frac: +0.2310
- bind_s2_frac: +0.6947
- bind_s3_frac: +0.0115
- bind_s4_frac: +0.0149
- fix_frac_ge1r: +0.2218
- fix_frac_ge2r: +0.0000
- fix_frac_maxhold: +0.3980
- fix_frac_pos: +0.4253
- fix_frac_s1: +0.0000
- fix_frac_s2: +0.0000
- fix_frac_s3: +0.0000
- fix_frac_s4: +0.0000
- fix_frac_stop: +0.4325
- fix_frac_target: +0.1695
- fix_hold_maxhold: +20.0000
- fix_hold_stop: +7.7257
- fix_hold_target: +9.8619
- fix_mean_r: -1.7412
- fix_median_r: -0.3211
- fix_n: 13074
- geo_A_mean_E: +45.9433
- geo_A_mean_R: +3.5830
- geo_A_median_R: +2.2270
- geo_A_n: 5605
- geo_B_mean_E: +49.5909
- geo_B_mean_R: +2.8930
- geo_B_median_R: +1.7478
- geo_B_n: 7105
- geo_C_mean_E: +22.4713
- geo_C_mean_R: +2.7459
- geo_C_median_R: +2.0778
- geo_C_n: 364
- geo_pooled_mean_E: +47.2721
- geo_pooled_mean_R: +3.1847
- geo_pooled_median_R: +1.9500
- geo_pooled_n: 13074
- ind_frac_ge1r: +0.0458
- ind_frac_ge2r: +0.0170
- ind_frac_maxhold: +0.0054
- ind_frac_pos: +0.3259
- ind_frac_s1: +0.2310
- ind_frac_s2: +0.6947
- ind_frac_s3: +0.0115
- ind_frac_s4: +0.0149
- ind_frac_stop: +0.0426
- ind_frac_target: +0.0000
- ind_hold_maxhold: +20.0000
- ind_hold_s1: +2.5745
- ind_hold_s2: +2.1926
- ind_hold_s3: +12.9333
- ind_hold_s4: +9.7846
- ind_hold_stop: +1.6589
- ind_mean_r: -1.7627
- ind_median_r: -0.1175
- ind_n: 13074
- nd_A_fix_mean: -3.9805
- nd_A_fix_n: 5605
- nd_A_ind_mean: -4.0582
- nd_A_ind_n: 5605
- nd_B_fix_mean: -0.0687
- nd_B_fix_n: 7105
- nd_B_ind_mean: -0.0422
- nd_B_ind_n: 7105
- nd_C_fix_mean: +0.0941
- nd_C_fix_n: 364
- nd_C_ind_mean: +0.0013
- nd_C_ind_n: 364
- nd_pooled_fix_mean: -1.8016
- nd_pooled_fix_n: 12644
- nd_pooled_ind_mean: -1.8219
- nd_pooled_ind_n: 12644
- year_2016_fix: -15.4358
- year_2016_ind: -15.5551
- year_2016_n: 1456
- year_2017_fix: +0.0325
- year_2017_ind: -0.0452
- year_2017_n: 1691
- year_2018_fix: -0.0992
- year_2018_ind: -0.0605
- year_2018_n: 1290
- year_2019_fix: -0.0173
- year_2019_ind: -0.0059
- year_2019_n: 1630
- year_2020_fix: +0.1439
- year_2020_ind: +0.0216
- year_2020_n: 913
- year_2021_fix: -0.0867
- year_2021_ind: -0.0426
- year_2021_n: 1215
- year_2022_fix: -0.2950
- year_2022_ind: -0.0989
- year_2022_n: 969
- year_2023_fix: +0.0563
- year_2023_ind: +0.0075
- year_2023_n: 1452
- year_2024_fix: +0.0729
- year_2024_ind: -0.0687
- year_2024_n: 1288
- year_2025_fix: -0.0893
- year_2025_ind: -0.0235
- year_2025_n: 1170

## Sensitivities (plain per-slot estimates, pre-reg #17 §7)
| sensitivity | slot | n | dates | est (ind − fix) |
| --- | --- | --- | --- | --- |
| S-1R5 | A | 5605 | 1646 | -0.0597 |
| S-1R5 | B | 7105 | 1623 | +0.0160 |
| S-1R5 | C | 364 | 321 | -0.0579 |
| S-1R5 | pooled | 13074 | 2114 | -0.0185 |
| S-3R | A | 5605 | 1646 | -0.1098 |
| S-3R | B | 7105 | 1623 | +0.0367 |
| S-3R | C | 364 | 321 | -0.1181 |
| S-3R | pooled | 13074 | 2114 | -0.0304 |
| S-C05 | A | 5605 | 1646 | -0.0777 |
| S-C05 | B | 7105 | 1623 | +0.0265 |
| S-C05 | C | 364 | 321 | -0.0928 |
| S-C05 | pooled | 13074 | 2114 | -0.0215 |
| S-C30 | A | 5605 | 1646 | -0.0777 |
| S-C30 | B | 7105 | 1623 | +0.0265 |
| S-C30 | C | 364 | 321 | -0.0928 |
| S-C30 | pooled | 13074 | 2114 | -0.0215 |
| S-CLOSE | A | 5605 | 1646 | -0.0929 |
| S-CLOSE | B | 7105 | 1623 | +0.0360 |
| S-CLOSE | C | 364 | 321 | -0.1000 |
| S-CLOSE | pooled | 13074 | 2114 | -0.0231 |
| S-DOJI | A | 5605 | 1646 | -0.0798 |
| S-DOJI | B | 7105 | 1623 | +0.0280 |
| S-DOJI | C | 364 | 321 | -0.0940 |
| S-DOJI | pooled | 13074 | 2114 | -0.0216 |
| S-IS | A | 8865 | 2862 | +9.8493 |
| S-IS | B | 8649 | 2388 | +35.5536 |
| S-IS | C | 687 | 576 | -0.0692 |
| S-IS | pooled | 18201 | 3399 | +21.6894 |
| S-N10 | A | 5628 | 1653 | -0.0444 |
| S-N10 | B | 7175 | 1632 | +0.0032 |
| S-N10 | C | 368 | 324 | -0.0425 |
| S-N10 | pooled | 13171 | 2123 | -0.0184 |
| S-N60 | A | 5538 | 1621 | -0.1145 |
| S-N60 | B | 7044 | 1602 | -0.0001 |
| S-N60 | C | 358 | 316 | -0.2563 |
| S-N60 | pooled | 12940 | 2078 | -0.0561 |
| S-OPX | A | 5603 | 1645 | -0.0900 |
| S-OPX | B | 7103 | 1622 | +0.0471 |
| S-OPX | C | 364 | 321 | -0.0998 |
| S-OPX | pooled | 13070 | 2113 | -0.0157 |
| S-PCT | A | 5605 | 1646 | -0.0049 |
| S-PCT | B | 7105 | 1623 | -0.0003 |
| S-PCT | C | 364 | 321 | -0.0116 |
| S-PCT | pooled | 13074 | 2114 | -0.0026 |
| S-UNI | s1 | 3020 | 1285 | +0.0022 |
| S-UNI | s2 | 9082 | 1923 | +0.0048 |
| S-UNI | s3 | 150 | 126 | +0.0022 |
| S-UNI | s4 | 195 | 156 | -0.0030 |
| S-VOL2 | A | 5605 | 1646 | -0.0723 |
| S-VOL2 | B | 7105 | 1623 | +0.0277 |
| S-VOL2 | C | 364 | 321 | -0.0938 |
| S-VOL2 | pooled | 13074 | 2114 | -0.0185 |
| S-VWAP5 | A | 5605 | 1646 | -0.0759 |
| S-VWAP5 | B | 7105 | 1623 | +0.0190 |
| S-VWAP5 | C | 364 | 321 | -0.0814 |
| S-VWAP5 | pooled | 13074 | 2114 | -0.0245 |

## Notes
- F2 baseline: 10 seeded random bars per binding event, same ticker, OOS era, binding-exit bars excluded; post-exit return measured from the exit close over 10 bars.
- S-DOJI topping tail: h[t] within 0.25R of the run's max high since entry (entry price as baseline), body ≤ 0.1·range, upper shadow ≥ 0.6·range; S-DOJI is a sensitivity only.
- S-UNI: F2's random-universe baseline leg — the baseline drawn from any ticker's bars in the event universe instead of the same ticker; S-IS uses the in-sample window (before 2016-01-01).
- One-shot rule (pre-reg #17 §5): this file is the first measurement; verdicts are fixed here and returned to the ledger before any parameter change becomes a new hypothesis.

results sha256: 71fbbd4918e26f744343c7da082f81a362f7efbf87b63b1d67231970bcf2ea89
