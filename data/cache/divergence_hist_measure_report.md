# RSI divergence measurement report (pre-registration #13 — the historical-constituent re-check)

- Pre-registration #13 (frozen 2026-08-15; the brief §5 historical-constituent re-check of pre-reg #10, pre-reg #10 §8; universe = union of 5 annual S&P 600 snapshots 2021-2025, 904 names incl. ~330 delisted/removed; OOS 2022-2025): claims = bullish divergence (price lower low + RSI higher low) => bounce; bearish divergence (price higher high + RSI lower high) => pullback; 'a lot less common so arguably a bit more reliable' vs the 70/30 signals (I-X-02/03/04); simple-average RSI, period 10 primary (14 sensitivity), k=2 fractal, min separation 5, signal at the confirmation bar t2+2; N=10 primary, cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260813)
- Swings: strict k-fractals on Low (bull) / High (bear) — ties never form a swing; consecutive swing pairs only, disjoint fractal windows (t2 - t1 >= 5). Signal bar = t2 + k (the fractal is only knowable at close t2+k — strict no-look-ahead); entry open t2+k+1, exit close t2+k+N.
- Crossings (the I-X-02 baseline): first bar of each excursion above 70 / below 30 (pre-reg #9 S4 rule), same period.
- Warm-up guard signal-bar index < 60 (frozen #3 convention, also bounds the lookback): 695 divergence and 3355 crossing warm-up events excluded and counted
- Era split: IS 2000-2021 (descriptive only — no IS-era membership data) / OOS 2022-2025 (by signal date). Cross-market caveat pre-declared: the video demos GBP/USD and USD/JPY; measured on US equities.
- Events (period 10, k=2, min-sep 5, warm-up excluded): BULL n=42495, BEAR n=52057 (drops at series end: {"BULL": 49, "BEAR": 118}); crossings: OB n=163921, OS n=142577 (drops: {"OB": 238, "OS": 383})
- F1 (absolute, directional per leg): OOS mean forward return vs era-matched random entries AND same-ticker (SPY reported), p_input = max, Holm across BULL/BEAR. BULL: EDGE iff CI-low > 0 (bounce); FADE iff CI-upper < 0. BEAR: EDGE iff CI-upper < 0 (pullback); FADE iff CI-low > 0. F2 (reliability contrast, I-X-02): divergence minus 70/30 crossings at the same period, per leg on mean return AND hit rate (ret > 0 after cost), Holm across the 4 tests.

## Verdicts — Family 1: absolute (directional per leg)

- F1-BULL: n=9384 | mean_ret +0.0059 | win_rate 0.5098 | excess vs random +0.0043 (CI -0.0010..+0.0081, p 0.064) | vs same +0.0049 (CI -0.0015..+0.0087, p 0.072) | vs spy +0.0013 (p 0.320) | p_input 0.072 | est +0.0049 (CI-low -0.0015..CI-upper +0.0081) | Holm gate 0.0250 -> **NO EDGE (p_input 0.072; est +0.0049; CI-low -0.0015..CI-upper +0.0081)**
- F1-BEAR: n=9656 | mean_ret -0.0012 | win_rate 0.4706 | excess vs random -0.0030 (CI -0.0081..+0.0005, p 0.106) | vs same -0.0038 (CI -0.0103..-0.0005, p 0.024) | vs spy -0.0059 (p 0.000) | p_input 0.106 | est -0.0030 (CI-low -0.0103..CI-upper -0.0005) | Holm gate 0.0500 -> **NO EDGE (p_input 0.106; est -0.0030; CI-low -0.0103..CI-upper -0.0005)**

## Verdicts — Family 2: reliability contrast (I-X-02, divergence minus 70/30 crossings)

- F2-BULL-mean: n_div=9384 | n_cross=31509 | div mean +0.0059 | cross mean +0.0047 | div hit 0.5098 | cross hit 0.5014 | contrast +0.0014 (CI -0.0034..+0.0050, p 0.492) | Holm gate 0.0500 -> **NO EDGE (contrast est +0.0014, p 0.492)**
- F2-BULL-hit: n_div=9384 | n_cross=31509 | div mean +0.0059 | cross mean +0.0047 | div hit 0.5098 | cross hit 0.5014 | contrast +0.0083 (CI -0.0029..+0.0197, p 0.140) | Holm gate 0.0167 -> **NO EDGE (contrast est +0.0083, p 0.140)**
- F2-BEAR-mean: n_div=9656 | n_cross=31633 | div mean -0.0012 | cross mean -0.0003 | div hit 0.4706 | cross hit 0.4840 | contrast -0.0010 (CI -0.0033..+0.0012, p 0.410) | Holm gate 0.0250 -> **NO EDGE (contrast est -0.0010, p 0.410)**
- F2-BEAR-hit: n_div=9656 | n_cross=31633 | div mean -0.0012 | cross mean -0.0003 | div hit 0.4706 | cross hit 0.4840 | contrast -0.0135 (CI -0.0241..-0.0031, p 0.012) | Holm gate 0.0125 -> **EDGE (contrast CI-upper -0.0031 < 0 — bearish divergence more reliable than overbought crossings)**

## Frequency (I-X-02 first half — measurement, not a verdict)

- OOS divergence events: 19,207 (BULL 9,433, BEAR 9,774) vs 70/30 crossing events: 63,763 (OB 31,871, OS 31,892) — ratio 0.3012 (ticker-cluster bootstrap CI 0.2972..0.3052); CI-upper < 1 confirms "a lot less common"

## Sensitivities (exploratory — NO verdicts)

### S1: horizons N = 1 / 5 / 20

*Baselines rebuilt per horizon (era- AND horizon-matched N-bar window pools); crossings re-measured at the horizon for the F2 contrast.*

**N=1** (drops {"BULL": 3, "BEAR": 5}):
- F1-BULL: n=9430 | mean -0.0017 | win 0.4542 | vs random -0.0005 (p 0.580) | vs same -0.0005 (p 0.672)
- F1-BEAR: n=9769 | mean -0.0014 | win 0.4679 | vs random -0.0003 (p 0.854) | vs same -0.0002 (p 0.986)
- F2-BULL-mean: contrast -0.0018 (p 0.322); div hit 0.4542 vs cross hit 0.4606
- F2-BULL-hit: contrast -0.0059 (p 0.300); div hit 0.4542 vs cross hit 0.4606
- F2-BEAR-mean: contrast -0.0000 (p 0.912); div hit 0.4679 vs cross hit 0.4561
- F2-BEAR-hit: contrast +0.0118 (p 0.042); div hit 0.4679 vs cross hit 0.4561

**N=5** (drops {"BULL": 26, "BEAR": 45}):
- F1-BULL: n=9407 | mean +0.0007 | win 0.4897 | vs random +0.0006 (p 0.488) | vs same +0.0007 (p 0.392)
- F1-BEAR: n=9729 | mean -0.0004 | win 0.4765 | vs random -0.0006 (p 0.868) | vs same -0.0008 (p 0.578)
- F2-BULL-mean: contrast -0.0015 (p 0.388); div hit 0.4897 vs cross hit 0.4939
- F2-BULL-hit: contrast -0.0041 (p 0.514); div hit 0.4897 vs cross hit 0.4939
- F2-BEAR-mean: contrast +0.0004 (p 0.608); div hit 0.4765 vs cross hit 0.4792
- F2-BEAR-hit: contrast -0.0024 (p 0.634); div hit 0.4765 vs cross hit 0.4792

**N=20** (drops {"BULL": 93, "BEAR": 254}):
- F1-BULL: n=9340 | mean +0.0115 | win 0.5153 | vs random +0.0060 (p 0.080) | vs same +0.0075 (p 0.082)
- F1-BEAR: n=9520 | mean -0.0002 | win 0.4653 | vs random -0.0055 (p 0.014) | vs same -0.0070 (p 0.000)
- F2-BULL-mean: contrast +0.0024 (p 0.366); div hit 0.5153 vs cross hit 0.5011
- F2-BULL-hit: contrast +0.0139 (p 0.024); div hit 0.5153 vs cross hit 0.5011
- F2-BEAR-mean: contrast -0.0038 (p 0.012); div hit 0.4653 vs cross hit 0.4865
- F2-BEAR-hit: contrast -0.0211 (p 0.000); div hit 0.4653 vs cross hit 0.4865

### S2: swing scale k = 3 / 5 (period 10)

**k=3** (drops {"BULL": 35, "BEAR": 138}):
- F1-BULL: n=8845 | mean +0.0071 | vs random +0.0052 (p 0.072) | vs same +0.0063 (p 0.046)
- F1-BEAR: n=9116 | mean -0.0005 | vs random -0.0023 (p 0.220) | vs same -0.0026 (p 0.076)
- F2-BULL-mean: contrast +0.0024 (p 0.264)
- F2-BULL-hit: contrast +0.0136 (p 0.034)
- F2-BEAR-mean: contrast -0.0002 (p 0.822)
- F2-BEAR-hit: contrast -0.0059 (p 0.292)

**k=5** (drops {"BULL": 39, "BEAR": 108}):
- F1-BULL: n=6932 | mean +0.0073 | vs random +0.0058 (p 0.060) | vs same +0.0064 (p 0.080)
- F1-BEAR: n=7075 | mean +0.0001 | vs random -0.0017 (p 0.470) | vs same -0.0021 (p 0.296)
- F2-BULL-mean: contrast +0.0025 (p 0.262)
- F2-BULL-hit: contrast +0.0126 (p 0.046)
- F2-BEAR-mean: contrast +0.0004 (p 0.784)
- F2-BEAR-hit: contrast +0.0034 (p 0.610)

### S3: period 14 (textbook default; crossings at 14)

Drops {"BULL": 42, "BEAR": 117}:
- F1-BULL: n=9328 | mean +0.0029 | vs random +0.0012 (p 0.420) | vs same +0.0018 (p 0.208)
- F1-BEAR: n=9409 | mean -0.0032 | vs random -0.0049 (p 0.000) | vs same -0.0055 (p 0.000)
- F2-BULL-mean: contrast -0.0005 (p 0.716); div hit 0.5029 vs cross hit 0.5038
- F2-BULL-hit: contrast -0.0011 (p 0.894); div hit 0.5029 vs cross hit 0.5038
- F2-BEAR-mean: contrast -0.0051 (p 0.000); div hit 0.4680 vs cross hit 0.4882
- F2-BEAR-hit: contrast -0.0203 (p 0.000); div hit 0.4680 vs cross hit 0.4882
- Frequency at period 14: divergence 18,896 vs crossings 44,085 — ratio 0.4286 (CI 0.4234..0.4363)

### S4: min separation >= 10 bars

Drops {"BULL": 10, "BEAR": 30}:
- F1-BULL: n=2242 | mean +0.0109 | vs random +0.0092 (p 0.026) | vs same +0.0112 (p 0.016)
- F1-BEAR: n=2353 | mean -0.0022 | vs random -0.0039 (p 0.282) | vs same -0.0050 (p 0.128)
- F2-BULL-mean: contrast +0.0061 (p 0.118)
- F2-BULL-hit: contrast +0.0141 (p 0.180)
- F2-BEAR-mean: contrast -0.0018 (p 0.370)
- F2-BEAR-hit: contrast -0.0069 (p 0.526)

### S5: per-year F1 leg mean returns (OOS)

| year | BULL | BEAR |
|---|---|---|
| 2000 | +0.0008 (n=874) | +0.0049 (n=890) |
| 2001 | +0.0145 (n=903) | +0.0080 (n=1431) |
| 2002 | +0.0023 (n=1231) | +0.0068 (n=1279) |
| 2003 | +0.0172 (n=885) | +0.0210 (n=1782) |
| 2004 | +0.0096 (n=1101) | +0.0030 (n=1704) |
| 2005 | +0.0038 (n=1407) | +0.0063 (n=1586) |
| 2006 | +0.0052 (n=1188) | +0.0115 (n=1764) |
| 2007 | -0.0046 (n=1583) | -0.0042 (n=1497) |
| 2008 | -0.0055 (n=1776) | -0.0163 (n=1409) |
| 2009 | +0.0397 (n=1250) | +0.0316 (n=1771) |
| 2010 | +0.0131 (n=1339) | +0.0027 (n=2028) |
| 2011 | +0.0005 (n=1801) | -0.0175 (n=1670) |
| 2012 | +0.0024 (n=1511) | +0.0058 (n=2079) |
| 2013 | +0.0210 (n=1324) | +0.0119 (n=2421) |
| 2014 | +0.0102 (n=1799) | -0.0034 (n=2138) |
| 2015 | -0.0039 (n=1785) | +0.0001 (n=2009) |
| 2016 | +0.0245 (n=1612) | +0.0093 (n=2599) |
| 2017 | +0.0061 (n=1887) | +0.0013 (n=2348) |
| 2018 | -0.0043 (n=2130) | -0.0049 (n=2275) |
| 2019 | +0.0207 (n=1833) | +0.0025 (n=2586) |
| 2020 | +0.0120 (n=2011) | +0.0233 (n=2513) |
| 2021 | +0.0026 (n=1881) | +0.0063 (n=2622) |
| 2022 | +0.0048 (n=2491) | -0.0101 (n=2165) |
| 2023 | +0.0027 (n=2468) | +0.0067 (n=2485) |
| 2024 | +0.0086 (n=2087) | -0.0025 (n=2612) |
| 2025 | +0.0082 (n=2338) | +0.0001 (n=2394) |

### S6: IS record (descriptive only — no IS-era membership data)

| leg | n | mean_ret | win_rate |
|---|---|---|---|
| BULL | 33111 | +0.0078 | 0.5354 |
| BEAR | 42401 | +0.0055 | 0.5253 |

### S7: extreme-gated divergence (first swing's RSI beyond 70/30)

Drops {"BULL": 24, "BEAR": 91}:
- F1-BULL: n=6042 | mean +0.0062 | vs random +0.0045 (p 0.058) | vs same +0.0054 (p 0.092)
- F1-BEAR: n=6267 | mean -0.0042 | vs random -0.0059 (p 0.000) | vs same -0.0071 (p 0.000)

### S8: chartist's-eye timing (signal at the pivot bar, entry open t2+1)

*Pre-declared caveat: the swing's future-side fractal condition is then a selection input — it excludes pivots followed by continuation, tilting toward the claim.*

Drops {"BULL": 46, "BEAR": 84}:
- F1-BULL: n=9384 | mean +0.0232 | vs random +0.0214 (p 0.028) | vs same +0.0222 (p 0.034)
- F1-BEAR: n=9673 | mean -0.0176 | vs random -0.0195 (p 0.000) | vs same -0.0199 (p 0.000)

## Reproducibility

`python -X utf8 tools/measure_divergence_hist.py` regenerates this report; the seed is fixed, so results are stable across runs.
Assertions: RSI within [0, 100] everywhere (min 0.000000000000, max 100.000000000000; PASS); no event with first-swing RSI undefined (min t1 10; PASS); no event whose fractal lacks confirmation bars (PASS); no leg ticker missing an OOS window pool (PASS).
Input fingerprints: universe 62f681d58cdb…, measure code 85f2ae0d4a1e… (Phase-3 engine c7421fbf… imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
