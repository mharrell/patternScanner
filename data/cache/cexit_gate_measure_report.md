# Pre-registration #17 — C-exit comparison: indicator exits vs fixed-2R on the same entries (C-01/C-03/C-04)

mode: **gate** — frozen pre-reg #2 A/B/C detections, OOS 2016-01-01..2025-12-31 by signal date
tool: tools/measure_cexit.py (frozen 2026-08-19, FROZEN_SHA afcc0222fcd4…)

## Input fingerprints
- detectors.py — e93ddf7a… (frozen; asserted at import)
- detections_v1.csv — 9b44f661… (frozen; asserted at import)
- universe_sp600_hist_2026-08-15.csv — 62f681d58cdb… (gate universe)
- bars parquets — 702

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
| end | 126 |
| no_bars | 0 |
| r_le_0 | 109 |

## F1 — system contrast, est = mean(ind R) − mean(fix R) (Holm 0.05/4)
| slot | n | dates | mean ind | mean fix | est | CI low | CI high | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 6214 | 1677 | -14.1766 | -14.1150 | -0.0616 | -0.1063 | -0.0210 | 0.0020 | FADE (Holm-rejected; CI-upper < 0 — claim contradicts) |
| B | 8278 | 1711 | -0.0384 | -0.0739 | +0.0356 | -0.0020 | +0.0741 | 0.0620 | NO EDGE (p 0.062; est +0.0356; CI -0.0020..+0.0741) |
| C | 435 | 372 | +0.0241 | +0.0615 | -0.0374 | -0.1164 | +0.0499 | 0.3920 | NO EDGE (p 0.392; est -0.0374; CI -0.1164..+0.0499) |
| pooled | 14927 | 2160 | -5.9222 | -5.9152 | -0.0070 | -0.0401 | +0.0227 | 0.6240 | NO EDGE (p 0.624; est -0.0070; CI -0.0401..+0.0227) |

## F2 — per-signal exit timing, est = mean(baseline) − mean(post-exit) (Holm 0.05/4)
| signal | n | dates | drops_end | n_baseline | mean post | mean base | est | CI low | CI high | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| s1 | 3405 | 1379 | 1 | 34050 | +0.0036 | +0.0077 | +0.0041 | +0.0003 | +0.0078 | 0.0280 | NO EDGE (p 0.028; est +0.0041; CI +0.0003..+0.0078) |
| s2 | 10414 | 1975 | 0 | 104140 | +0.0021 | +0.0060 | +0.0039 | +0.0009 | +0.0069 | 0.0160 | NO EDGE (p 0.016; est +0.0039; CI +0.0009..+0.0069) |
| s3 | 162 | 134 | 0 | 1620 | +0.0003 | +0.0045 | +0.0042 | -0.0070 | +0.0168 | 0.5220 | NO EDGE (p 0.522; est +0.0042; CI -0.0070..+0.0168) |
| s4 | 216 | 177 | 0 | 2160 | +0.0056 | +0.0094 | +0.0037 | -0.0086 | +0.0158 | 0.5100 | NO EDGE (p 0.510; est +0.0037; CI -0.0086..+0.0158) |

## F3 — C-04 upper tail, est = quantile(ind R) − quantile(fix R), pooled (Holm 0.05/3)
| slot | q | n | dates | est | CI low | CI high | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| q90 | 0.90 | 14927 | 2160 | -1.4922 | -1.5348 | -1.4492 | 0.0000 | FADE (Holm-rejected; CI-upper < 0 — claim contradicts) |
| q95 | 0.95 | 14927 | 2160 | -1.0405 | -1.1016 | -0.9689 | 0.0000 | FADE (Holm-rejected; CI-upper < 0 — claim contradicts) |
| q99 | 0.99 | 14927 | 2160 | +0.6425 | +0.4463 | +0.8897 | 0.0000 | EDGE (Holm-rejected; CI-low > 0 — claim holds) |

## Measurements
- bind_s1_frac: +0.2281
- bind_s2_frac: +0.6977
- bind_s3_frac: +0.0109
- bind_s4_frac: +0.0145
- fix_frac_ge1r: +0.2181
- fix_frac_ge2r: +0.0000
- fix_frac_maxhold: +0.3989
- fix_frac_pos: +0.4192
- fix_frac_s1: +0.0000
- fix_frac_s2: +0.0000
- fix_frac_s3: +0.0000
- fix_frac_s4: +0.0000
- fix_frac_stop: +0.4369
- fix_frac_target: +0.1642
- fix_hold_maxhold: +20.0000
- fix_hold_stop: +7.7239
- fix_hold_target: +9.7707
- fix_mean_r: -5.9152
- fix_median_r: -0.3542
- fix_n: 14927
- geo_A_mean_E: +45.6419
- geo_A_mean_R: +3.6643
- geo_A_median_R: +2.1400
- geo_A_n: 6214
- geo_B_mean_E: +49.9754
- geo_B_mean_R: +3.1252
- geo_B_median_R: +1.6896
- geo_B_n: 8278
- geo_C_mean_E: +22.6579
- geo_C_mean_R: +3.1289
- geo_C_median_R: +1.9930
- geo_C_n: 435
- geo_pooled_mean_E: +47.3753
- geo_pooled_mean_R: +3.3497
- geo_pooled_median_R: +1.8731
- geo_pooled_n: 14927
- ind_frac_ge1r: +0.0454
- ind_frac_ge2r: +0.0164
- ind_frac_maxhold: +0.0059
- ind_frac_pos: +0.3267
- ind_frac_s1: +0.2281
- ind_frac_s2: +0.6977
- ind_frac_s3: +0.0109
- ind_frac_s4: +0.0145
- ind_frac_stop: +0.0430
- ind_frac_target: +0.0000
- ind_hold_maxhold: +20.0000
- ind_hold_s1: +2.5125
- ind_hold_s2: +2.1812
- ind_hold_s3: +13.1605
- ind_hold_s4: +10.0000
- ind_hold_stop: +1.6464
- ind_mean_r: -5.9222
- ind_median_r: -0.1170
- ind_n: 14927
- nd_A_fix_mean: -14.1150
- nd_A_fix_n: 6214
- nd_A_ind_mean: -14.1766
- nd_A_ind_n: 6214
- nd_B_fix_mean: -0.0739
- nd_B_fix_n: 8278
- nd_B_ind_mean: -0.0384
- nd_B_ind_n: 8278
- nd_C_fix_mean: +0.0615
- nd_C_fix_n: 435
- nd_C_ind_mean: +0.0241
- nd_C_ind_n: 435
- nd_pooled_fix_mean: -6.1094
- nd_pooled_fix_n: 14453
- nd_pooled_ind_mean: -6.1161
- nd_pooled_ind_n: 14453
- year_2016_fix: +0.0850
- year_2016_ind: -0.0298
- year_2016_n: 1762
- year_2017_fix: -0.0008
- year_2017_ind: -0.0439
- year_2017_n: 1967
- year_2018_fix: -4.2268
- year_2018_ind: -4.1496
- year_2018_n: 1551
- year_2019_fix: -42.8332
- year_2019_ind: -42.8019
- year_2019_n: 1905
- year_2020_fix: +0.1433
- year_2020_ind: +0.0423
- year_2020_n: 1019
- year_2021_fix: -0.0646
- year_2021_ind: -0.0729
- year_2021_n: 1354
- year_2022_fix: -0.2801
- year_2022_ind: -0.0850
- year_2022_n: 1106
- year_2023_fix: +0.0190
- year_2023_ind: +0.0119
- year_2023_n: 1614
- year_2024_fix: +0.0245
- year_2024_ind: -0.0725
- year_2024_n: 1366
- year_2025_fix: -0.0814
- year_2025_ind: -0.0458
- year_2025_n: 1283

## Sensitivities (plain per-slot estimates, pre-reg #17 §7)
| sensitivity | slot | n | dates | est (ind − fix) |
| --- | --- | --- | --- | --- |
| S-1R5 | A | 6214 | 1677 | -0.0435 |
| S-1R5 | B | 8278 | 1711 | +0.0270 |
| S-1R5 | C | 435 | 372 | -0.0107 |
| S-1R5 | pooled | 14927 | 2160 | -0.0034 |
| S-3R | A | 6214 | 1677 | -0.0869 |
| S-3R | B | 8278 | 1711 | +0.0423 |
| S-3R | C | 435 | 372 | -0.0532 |
| S-3R | pooled | 14927 | 2160 | -0.0143 |
| S-C05 | A | 6214 | 1677 | -0.0616 |
| S-C05 | B | 8278 | 1711 | +0.0356 |
| S-C05 | C | 435 | 372 | -0.0374 |
| S-C05 | pooled | 14927 | 2160 | -0.0070 |
| S-C30 | A | 6214 | 1677 | -0.0616 |
| S-C30 | B | 8278 | 1711 | +0.0356 |
| S-C30 | C | 435 | 372 | -0.0374 |
| S-C30 | pooled | 14927 | 2160 | -0.0070 |
| S-CLOSE | A | 6214 | 1677 | -0.0605 |
| S-CLOSE | B | 8278 | 1711 | +0.0420 |
| S-CLOSE | C | 435 | 372 | -0.0273 |
| S-CLOSE | pooled | 14927 | 2160 | -0.0027 |
| S-DOJI | A | 6214 | 1677 | -0.0644 |
| S-DOJI | B | 8278 | 1711 | +0.0331 |
| S-DOJI | C | 435 | 372 | -0.0398 |
| S-DOJI | pooled | 14927 | 2160 | -0.0096 |
| S-IS | A | 10461 | 3026 | +8.3353 |
| S-IS | B | 10814 | 2616 | +28.4232 |
| S-IS | C | 863 | 700 | -0.0982 |
| S-IS | pooled | 22138 | 3513 | +17.8191 |
| S-N10 | A | 6236 | 1683 | -0.0422 |
| S-N10 | B | 8348 | 1720 | +0.0029 |
| S-N10 | C | 440 | 376 | -0.0213 |
| S-N10 | pooled | 15024 | 2169 | -0.0165 |
| S-N60 | A | 6151 | 1650 | -0.0898 |
| S-N60 | B | 8202 | 1686 | +0.0046 |
| S-N60 | C | 429 | 367 | -0.1118 |
| S-N60 | pooled | 14782 | 2124 | -0.0381 |
| S-OPX | A | 6212 | 1676 | -0.0577 |
| S-OPX | B | 8276 | 1710 | +0.0462 |
| S-OPX | C | 435 | 372 | -0.0234 |
| S-OPX | pooled | 14923 | 2159 | +0.0009 |
| S-PCT | A | 6214 | 1677 | -0.0047 |
| S-PCT | B | 8278 | 1711 | -0.0005 |
| S-PCT | C | 435 | 372 | -0.0066 |
| S-PCT | pooled | 14927 | 2160 | -0.0024 |
| S-UNI | s1 | 3405 | 1379 | +0.0033 |
| S-UNI | s2 | 10414 | 1975 | +0.0045 |
| S-UNI | s3 | 162 | 134 | +0.0092 |
| S-UNI | s4 | 216 | 177 | -0.0010 |
| S-VOL2 | A | 6214 | 1677 | -0.0553 |
| S-VOL2 | B | 8278 | 1711 | +0.0338 |
| S-VOL2 | C | 435 | 372 | -0.0366 |
| S-VOL2 | pooled | 14927 | 2160 | -0.0054 |
| S-VWAP5 | A | 6214 | 1677 | -0.0633 |
| S-VWAP5 | B | 8278 | 1711 | +0.0289 |
| S-VWAP5 | C | 435 | 372 | -0.0344 |
| S-VWAP5 | pooled | 14927 | 2160 | -0.0113 |

## Notes
- F2 baseline: 10 seeded random bars per binding event, same ticker, OOS era, binding-exit bars excluded; post-exit return measured from the exit close over 10 bars.
- S-DOJI topping tail: h[t] within 0.25R of the run's max high since entry (entry price as baseline), body ≤ 0.1·range, upper shadow ≥ 0.6·range; S-DOJI is a sensitivity only.
- S-UNI: F2's random-universe baseline leg — the baseline drawn from any ticker's bars in the event universe instead of the same ticker; S-IS uses the in-sample window (before 2016-01-01).
- One-shot rule (pre-reg #17 §5): this file is the first measurement; verdicts are fixed here and returned to the ledger before any parameter change becomes a new hypothesis.

results sha256: 0a67241a1f86e17b82cc5ba23a5a6b1d1d61147ec7cb89cead15077d0e20d2ea
