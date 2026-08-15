# Big-move mean-reversion measurement report (pre-registration #11)

- Pre-registration #11 (frozen 2026-08-14): claim = 'almost all of the big moves will eventually be corrected'; 'what goes up must come down and what goes down must come back up' (I-F-01, jfe1Zl-5EQI [16:01-16:09], [15:05-15:09]). Big-move event at bar t iff |close_t - close_{t-L}| >= 3 x ATR_t, L = 10 primary, ATR = simple mean of the 14 true ranges ending at t (pre-registered — no ATR teaching in the corpus); UP leg iff close_t > close_{t-L}, DOWN leg iff close_t < close_{t-L}; event = the first bar of each leg excursion (the pre-reg #9 S4 rule). Signal at close t, entry open t+1, exit close t+10 (-cost 0.0015); bootstrap 1000 (seed 20260813); alpha 0.05; Holm within each family; count floor 100 OOS events per leg.
- Warm-up guard signal-bar index < 60 (frozen #3 convention — bounds the 10-bar move window and the 14-bar ATR lookback with margin): 1379 warm-up events and 4158 warm-up qualifying bars excluded and counted.
- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date). Intraday->daily translation pre-declared: the regularity is stated in a 2015 intraday-trading classroom; measured on US equity daily bars (the frozen S&P 600 universe). Only the regularity is measured — the reversal strategy is process content, not a claim.
- Events (L=10, tau=3, warm-up excluded): UP n=73414, DOWN n=57102 (drops at series end: {"UP": 89, "DOWN": 71}); state-level qualifying bars (S5 contrast): UP n=223723, DOWN n=169959
- F1 (absolute, directional per leg): OOS mean forward return vs era-matched random entries AND same-ticker (SPY reported), p_input = max, Holm across UP/DOWN. UP: EDGE iff Holm-rejected AND CI-upper < 0 (correction, as claimed); FADE iff CI-low > 0. DOWN: EDGE iff Holm-rejected AND CI-low > 0 (recovery, as claimed); FADE iff CI-upper < 0. F2 (retracement claim test): the leg's share of events with close_{t+N} past the move's midpoint within N=10 ('corrected half') minus the same share on era-matched random bars (each random bar's own trailing 10-bar move, direction-matched to the leg), Holm across UP/DOWN — the calibrated null, not an assumed 0.5.
- Phase-5 trigger (pre-reg #11 sec 4): ONLY an F1-DOWN EDGE can trigger the trigger-check conversation (F1-UP EDGE is a negative-return finding; F2 is a differential finding).

## Verdicts — Family 1: absolute (directional per leg)

- F1-UP: n=35908 | mean_ret +0.0003 | win_rate 0.4900 | excess vs random -0.0046 (CI -0.0059..-0.0033, p 0.000) | vs same -0.0048 (CI -0.0061..-0.0036, p 0.000) | vs spy -0.0055 (p 0.000) | p_input 0.000 | est -0.0046 (CI-low -0.0061..CI-upper -0.0036) | Holm gate 0.0250 -> **EDGE (Holm-rejected; excess CI-upper -0.0036 < 0 — big up-moves below both baselines, correction as claimed)**
- F1-DOWN: n=29039 | mean_ret +0.0048 | win_rate 0.5282 | excess vs random -0.0001 (CI -0.0016..+0.0015, p 0.950) | vs same +0.0001 (CI -0.0014..+0.0017, p 0.866) | vs spy -0.0010 (p 0.120) | p_input 0.950 | est +0.0001 (CI-low -0.0016..CI-upper +0.0015) | Holm gate 0.0500 -> **NO EDGE (p_input 0.950; est +0.0001; CI-low -0.0016..CI-upper +0.0015)**

## Verdicts — Family 2: retracement claim test (corrected-half within N=10 vs era-matched random bars)

- F2-UP: n_events=73,414 | n_random=716,712 | events retrace-half 0.1956 | random retrace-half 0.3234 | contrast -0.1277 (CI -0.1308..-0.1244, p 0.000) | Holm gate 0.0250 -> **FADE (Holm-rejected; contrast CI-upper -0.1244 < 0 — big up moves retrace half within N less often than typical bars, claim contradicted)**
- F2-DOWN: n_events=57,102 | n_random=635,474 | events retrace-half 0.2249 | random retrace-half 0.3801 | contrast -0.1553 (CI -0.1589..-0.1518, p 0.000) | Holm gate 0.0500 -> **FADE (Holm-rejected; contrast CI-upper -0.1518 < 0 — big down moves retrace half within N less often than typical bars, claim contradicted)**

## Frequency (measurement, not a verdict family)

- OOS events (excursion-firsts): UP 35,997 / DOWN 29,110; OOS qualifying bars (pre-collapse): UP 111,016 / DOWN 87,803 — the runs collapse view (typical runs span several qualifying bars).

## Sensitivities (exploratory — NO verdicts)

### S1: horizons N = 1 / 5 / 20

*Baselines rebuilt per horizon (era- AND horizon-matched N-bar window pools); the retracement metric reported at N = 5 (the claim's '5-10 sessions' range).*

**N=1** (drops {"UP": 0, "DOWN": 10}):
- F1-UP: n=35997 | mean -0.0020 | win 0.4520 | vs random -0.0006 (p 0.000) | vs same -0.0006 (p 0.000)
- F1-DOWN: n=29100 | mean -0.0009 | win 0.4695 | vs random +0.0005 (p 0.020) | vs same +0.0005 (p 0.022)

**N=5** (drops {"UP": 11, "DOWN": 45}):
- F1-UP: n=35986 | mean -0.0010 | win 0.4865 | vs random -0.0025 (p 0.000) | vs same -0.0026 (p 0.000)
- F1-DOWN: n=29065 | mean +0.0001 | win 0.5092 | vs random -0.0013 (p 0.012) | vs same -0.0013 (p 0.028)
- F2-UP (N=5): events 0.1273 vs random 0.2787 — contrast -0.1515 (p 0.000)
- F2-DOWN (N=5): events 0.1400 vs random 0.3205 — contrast -0.1805 (p 0.000)

**N=20** (drops {"UP": 373, "DOWN": 108}):
- F1-UP: n=35624 | mean +0.0050 | win 0.5027 | vs random -0.0071 (p 0.000) | vs same -0.0076 (p 0.000)
- F1-DOWN: n=29002 | mean +0.0144 | win 0.5499 | vs random +0.0024 (p 0.048) | vs same +0.0029 (p 0.024)

### S2: threshold tau = 2 / 5 (L = 10)

**tau=2** (drops {"UP": 179, "DOWN": 233}):
- F1-UP: n=64515 | mean +0.0021 | vs random -0.0028 (p 0.000) | vs same -0.0029 (p 0.000)
- F1-DOWN: n=55080 | mean +0.0072 | vs random +0.0022 (p 0.000) | vs same +0.0024 (p 0.000)
- F2-UP: events 0.2532 vs random 0.3234 — contrast -0.0702 (CI -0.0726..-0.0675, p 0.000)
- F2-DOWN: events 0.3031 vs random 0.3801 — contrast -0.0770 (CI -0.0798..-0.0738, p 0.000)

**tau=5** (drops {"UP": 10, "DOWN": 7}):
- F1-UP: n=5406 | mean +0.0013 | vs random -0.0038 (p 0.066) | vs same -0.0046 (p 0.030)
- F1-DOWN: n=4498 | mean -0.0090 | vs random -0.0138 (p 0.000) | vs same -0.0136 (p 0.000)
- F2-UP: events 0.1225 vs random 0.3234 — contrast -0.2007 (CI -0.2067..-0.1946, p 0.000)
- F2-DOWN: events 0.1236 vs random 0.3801 — contrast -0.2565 (CI -0.2630..-0.2500, p 0.000)

### S3: move window L = 5 (tau = 3)

Drops {"UP": 13, "DOWN": 24}:
- F1-UP: n=16980 | mean +0.0019 | vs random -0.0029 (p 0.002) | vs same -0.0034 (p 0.000)
- F1-DOWN: n=15491 | mean +0.0008 | vs random -0.0040 (p 0.000) | vs same -0.0038 (p 0.008)
- F2-UP: events 0.2034 vs random 0.3629 — contrast -0.1595 (p 0.000)
- F2-DOWN: events 0.2333 vs random 0.4232 — contrast -0.1899 (p 0.000)

### S4: ATR period 7 (simple) and Wilder's smoothing (L = 10, tau = 3)

**atr_period7** (drops {"UP": 114, "DOWN": 131}):
- F1-UP: n=39617 | mean -0.0002 | vs random -0.0051 (p 0.000) | vs same -0.0053 (p 0.000)
- F1-DOWN: n=31289 | mean +0.0053 | vs random +0.0004 (p 0.620) | vs same +0.0006 (p 0.428)

**atr_wilder** (drops {"UP": 77, "DOWN": 63}):
- F1-UP: n=34407 | mean +0.0007 | vs random -0.0042 (p 0.000) | vs same -0.0045 (p 0.000)
- F1-DOWN: n=28200 | mean +0.0047 | vs random -0.0002 (p 0.818) | vs same +0.0000 (p 0.946)

### S5: state-level view (every qualifying bar is an event)

*Overlap-inflated by construction — the pre-reg #9 S4 lesson; reported for contrast, not as evidence.*

Drops {"UP": 253, "DOWN": 183}:
- F1-UP: n=110763 | mean +0.0014 | vs random -0.0035 (p 0.000) | vs same -0.0040 (p 0.000)
- F1-DOWN: n=87620 | mean +0.0023 | vs random -0.0026 (p 0.000) | vs same -0.0023 (p 0.000)

### S6: per-year F1 leg mean returns (OOS)

| year | UP | DOWN |
|---|---|---|
| 2000 | -0.0083 (n=1589) | +0.0155 (n=1492) |
| 2001 | +0.0107 (n=2470) | +0.0103 (n=1703) |
| 2002 | +0.0029 (n=2051) | +0.0053 (n=1950) |
| 2003 | +0.0122 (n=2719) | +0.0241 (n=1292) |
| 2004 | +0.0032 (n=2466) | +0.0097 (n=1479) |
| 2005 | +0.0057 (n=2194) | +0.0022 (n=1790) |
| 2006 | +0.0044 (n=2288) | +0.0118 (n=1409) |
| 2007 | -0.0098 (n=1829) | -0.0046 (n=1780) |
| 2008 | -0.0149 (n=1537) | -0.0001 (n=2342) |
| 2009 | +0.0157 (n=2600) | +0.0087 (n=1569) |
| 2010 | +0.0054 (n=2892) | +0.0111 (n=1610) |
| 2011 | -0.0058 (n=2112) | +0.0018 (n=2082) |
| 2012 | +0.0071 (n=2543) | +0.0154 (n=1684) |
| 2013 | +0.0088 (n=3298) | +0.0162 (n=1354) |
| 2014 | +0.0025 (n=2476) | +0.0014 (n=2036) |
| 2015 | -0.0091 (n=2442) | +0.0082 (n=2491) |
| 2016 | +0.0087 (n=3346) | +0.0125 (n=2133) |
| 2017 | +0.0018 (n=3121) | +0.0094 (n=1980) |
| 2018 | -0.0036 (n=2600) | +0.0030 (n=3117) |
| 2019 | +0.0024 (n=4171) | +0.0060 (n=2239) |
| 2020 | -0.0006 (n=3732) | -0.0226 (n=2976) |
| 2021 | -0.0023 (n=3554) | +0.0199 (n=2441) |
| 2022 | -0.0115 (n=3243) | +0.0040 (n=4184) |
| 2023 | +0.0098 (n=4572) | -0.0006 (n=3293) |
| 2024 | -0.0047 (n=4091) | +0.0164 (n=3526) |
| 2025 | -0.0005 (n=3478) | +0.0056 (n=3150) |

### S7: IS record (descriptive — selection era)

| leg | n | mean_ret | win_rate |
|---|---|---|---|
| UP | 37506 | +0.0031 | 0.5083 |
| DOWN | 28063 | +0.0077 | 0.5271 |

### S8: retracement vs the move window's extreme (S8 midpoint)

*UP: midpoint of close_{t-L} and the window's max high; DOWN: midpoint of close_{t-L} and the window's min low — instead of the close-to-close midpoint, events and random bars alike.*

- F2-UP: events 0.2232 vs random 0.4063 — contrast -0.1831 (CI -0.1861..-0.1801, p 0.000)
- F2-DOWN: events 0.2579 vs random 0.4704 — contrast -0.2124 (CI -0.2162..-0.2086, p 0.000)

## Reproducibility

`python -X utf8 tools/measure_bigmove.py` regenerates this report; the seed is fixed, so results are stable across runs.
Assertions: ATR >= 0 everywhere (min 0.000000000000; PASS); no event with t - L < 0 (min signal bar 14 >= 10; PASS); no event whose signal bar lies beyond the ticker's series (PASS); F2 event-side drops equal the engine's drops per leg (PASS); no leg ticker missing an OOS window pool (PASS).
Input fingerprints: universe 5e6f45a3c791…, measure code 6917f3dc2437… (Phase-3 engine c7421fbf… imported unchanged; generic helpers from measure_divergence 85f2ae0d4a1e…).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
