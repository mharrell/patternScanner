# Pre-registration #15 intraday measure report — B-01 micro pullback (1-min)

- Mode: measure
- FROZEN_SHA: 765ff1df23c80c006104d2f28b754593e3401e256132115207a161ebf5fdc6f5
- Window: bar-dates >= 2026-08-19

## F1 — absolute forward returns (N=60, COST 0.15%)

Family verdict: **FADE**
- same_ticker: n=1963, mean -0.0021, excess -0.0023 (CI -0.0031..-0.0016, p=0.000, Holm 0.025, rejected) — FADE
- universe: n=1963, mean -0.0021, excess -0.0016 (CI -0.0022..-0.0009, p=0.000, Holm 0.050, rejected) — FADE

## F2 — HOD-retest reach rate

Family verdict: **EDGE**
- same_ticker: n=2622, reach 0.8375, excess +0.5344 (CI +0.5130..+0.5557, p=0.000) — EDGE
- universe: n=2622, reach 0.8375, excess +0.5704 (CI +0.5488..+0.5923, p=0.000) — EDGE

## F3 — pullback vs chase (B-02/I-E-02)

Family verdict: **FADE**
- same_ticker_pairs: n=1959 / chase 46962, pullback -0.0020678219303968304, excess -0.001775453624390289, p=0.0 — FADE
- universe: n=1963 / chase 137858, pullback -0.002067835348687134, excess -0.0011696415686284429, p=0.002 — FADE

## Measurement rows (no verdicts)

- R:R geometry: mean 3.47, median 0.60, frac ≥2:1 0.229 (n=1780, degenerate entry≤stop 842)
- Name-day collapse: 1552 name-days, mean-of-means -0.0023
- Entry gaps (min): median 1, frac >2min 0.019
- Reach rate (events): 0.8375

### Time-of-day profile (F-01 row)

| bucket (ET) | mean |r| | mean (H-L)/O | vol share |
|---|---|---|---|
| 04:00-07:00 | 0.002749 | 0.001460 | 0.000 |
| 07:00-09:30 | 0.004499 | 0.002570 | 0.000 |
| 09:30-10:00 | 0.002420 | 0.002216 | 0.084 |
| 10:00-11:00 | 0.001251 | 0.001047 | 0.117 |
| 11:00-12:00 | 0.000841 | 0.000697 | 0.100 |
| 12:00-13:00 | 0.000693 | 0.000565 | 0.086 |
| 13:00-14:00 | 0.000625 | 0.000524 | 0.087 |
| 14:00-15:00 | 0.000628 | 0.000553 | 0.103 |
| 15:00-16:00 | 0.000755 | 0.000885 | 0.274 |
| 16:00-20:00 | 0.003037 | 0.000578 | 0.147 |

### Pre-market vs RTH (F-02 row)

- premarket_04_0930: mean |r| 0.003900, median 0.000459, tail 0.1991, vol share 0.000
- rth_0930_1600: mean |r| 0.000926, median 0.000536, tail 0.1320, vol share 0.851

## Sensitivities (exploratory, NO verdicts)

- S-R4: {'n_events': 994, 'f1': 'FADE', 'f2': 'EDGE', 'f3': 'FADE', 'mean_f1_ret': -0.0017100381458486943}
- S-R2: {'n_events': 7350, 'f1': 'FADE', 'f2': 'EDGE', 'f3': 'FADE', 'mean_f1_ret': -0.002023147130753254}
- S-P3: {'n_events': 997, 'f1': 'FADE', 'f2': 'EDGE', 'f3': 'FADE', 'mean_f1_ret': -0.002208541106791061}
- S-DB: {'n_events': 11302, 'f1': 'FADE', 'f2': 'EDGE', 'f3': 'FADE', 'mean_f1_ret': -0.001864537029820123}
- S-WIN: {'n_events': 325, 'f1': 'INCONCLUSIVE', 'f2': 'EDGE', 'f3': 'INCONCLUSIVE', 'mean_f1_ret': 0.00014774342560661976}
- S-GAP: {'n_events': 2372, 'f1': 'FADE', 'f2': 'EDGE', 'f3': 'FADE', 'mean_f1_ret': -0.00204548736610092}
- S-N15: {'n_events': 2378, 'mean_ret': -0.0016859444159413094}
- S-N120: {'n_events': 1636, 'mean_ret': -0.0026924350437327795}
- S-N240: {'n_events': 955, 'mean_ret': -0.0033810890529427412}
- S-C05: {'n_events': 1963, 'mean_ret': -0.001067835348687134}
- S-C30: {'n_events': 1963, 'mean_ret': -0.0035678353486871344}

## §6 audit

- Audit: **PASSED**

