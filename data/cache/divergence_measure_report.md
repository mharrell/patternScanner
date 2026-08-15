# RSI divergence measurement report (pre-registration #10)

- Pre-registration #10 (frozen 2026-08-14): claims = bullish divergence (price lower low + RSI higher low) => bounce; bearish divergence (price higher high + RSI lower high) => pullback; 'a lot less common so arguably a bit more reliable' vs the 70/30 signals (I-X-02/03/04); simple-average RSI, period 10 primary (14 sensitivity), k=2 fractal, min separation 5, signal at the confirmation bar t2+2; N=10 primary, cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260813)
- Swings: strict k-fractals on Low (bull) / High (bear) — ties never form a swing; consecutive swing pairs only, disjoint fractal windows (t2 - t1 >= 5). Signal bar = t2 + k (the fractal is only knowable at close t2+k — strict no-look-ahead); entry open t2+k+1, exit close t2+k+N.
- Crossings (the I-X-02 baseline): first bar of each excursion above 70 / below 30 (pre-reg #9 S4 rule), same period.
- Warm-up guard signal-bar index < 60 (frozen #3 convention, also bounds the lookback): 601 divergence and 2872 crossing warm-up events excluded and counted
- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date). Cross-market caveat pre-declared: the video demos GBP/USD and USD/JPY; measured on US equities.
- Events (period 10, k=2, min-sep 5, warm-up excluded): BULL n=34076, BEAR n=42759 (drops at series end: {"BULL": 32, "BEAR": 112}); crossings: OB n=133878, OS n=114031 (drops: {"OB": 211, "OS": 314})
- F1 (absolute, directional per leg): OOS mean forward return vs era-matched random entries AND same-ticker (SPY reported), p_input = max, Holm across BULL/BEAR. BULL: EDGE iff CI-low > 0 (bounce); FADE iff CI-upper < 0. BEAR: EDGE iff CI-upper < 0 (pullback); FADE iff CI-low > 0. F2 (reliability contrast, I-X-02): divergence minus 70/30 crossings at the same period, per leg on mean return AND hit rate (ret > 0 after cost), Holm across the 4 tests.

## Verdicts — Family 1: absolute (directional per leg)

- F1-BULL: n=16985 | mean_ret +0.0080 | win_rate 0.5412 | excess vs random +0.0031 (CI +0.0011..+0.0050, p 0.002) | vs same +0.0034 (CI +0.0015..+0.0053, p 0.000) | vs spy +0.0022 (p 0.002) | p_input 0.002 | est +0.0034 (CI-low +0.0011..CI-upper +0.0050) | Holm gate 0.0250 -> **EDGE (Holm-rejected; excess CI-low +0.0011 > 0 — bullish divergence, bounce as claimed)**
- F1-BEAR: n=20800 | mean_ret +0.0046 | win_rate 0.5083 | excess vs random -0.0004 (CI -0.0020..+0.0013, p 0.662) | vs same -0.0004 (CI -0.0020..+0.0011, p 0.634) | vs spy -0.0013 (p 0.056) | p_input 0.662 | est -0.0004 (CI-low -0.0020..CI-upper +0.0011) | Holm gate 0.0500 -> **NO EDGE (p_input 0.662; est -0.0004; CI-low -0.0020..CI-upper +0.0011)**

## Verdicts — Family 2: reliability contrast (I-X-02, divergence minus 70/30 crossings)

- F2-BULL-mean: n_div=16985 | n_cross=57442 | div mean +0.0080 | cross mean +0.0062 | div hit 0.5412 | cross hit 0.5263 | contrast +0.0018 (CI +0.0003..+0.0034, p 0.012) | Holm gate 0.0250 -> **EDGE (contrast CI-low +0.0003 > 0 — bullish divergence more reliable than oversold crossings)**
- F2-BULL-hit: n_div=16985 | n_cross=57442 | div mean +0.0080 | cross mean +0.0062 | div hit 0.5412 | cross hit 0.5263 | contrast +0.0150 (CI +0.0063..+0.0229, p 0.000) | Holm gate 0.0125 -> **EDGE (contrast CI-low +0.0063 > 0 — bullish divergence more reliable than oversold crossings)**
- F2-BEAR-mean: n_div=20800 | n_cross=66331 | div mean +0.0046 | cross mean +0.0025 | div hit 0.5083 | cross hit 0.5029 | contrast +0.0021 (CI +0.0007..+0.0034, p 0.000) | Holm gate 0.0167 -> **FADE (contrast CI-low +0.0007 > 0 — bearish divergence less reliable than overbought crossings)**
- F2-BEAR-hit: n_div=20800 | n_cross=66331 | div mean +0.0046 | cross mean +0.0025 | div hit 0.5083 | cross hit 0.5029 | contrast +0.0054 (CI -0.0021..+0.0130, p 0.176) | Holm gate 0.0500 -> **NO EDGE (contrast est +0.0054, p 0.176)**

## Frequency (I-X-02 first half — measurement, not a verdict)

- OOS divergence events: 37,929 (BULL 17,017, BEAR 20,912) vs 70/30 crossing events: 124,298 (OB 66,542, OS 57,756) — ratio 0.3051 (ticker-cluster bootstrap CI 0.3022..0.3081); CI-upper < 1 confirms "a lot less common"

## Sensitivities (exploratory — NO verdicts)

### S1: horizons N = 1 / 5 / 20

*Baselines rebuilt per horizon (era- AND horizon-matched N-bar window pools); crossings re-measured at the horizon for the F2 contrast.*

**N=1** (drops {"BULL": 1, "BEAR": 8}):
- F1-BULL: n=17016 | mean -0.0012 | win 0.4615 | vs random +0.0002 (p 0.528) | vs same +0.0002 (p 0.468)
- F1-BEAR: n=20904 | mean -0.0017 | win 0.4579 | vs random -0.0003 (p 0.212) | vs same -0.0003 (p 0.192)
- F2-BULL-mean: contrast -0.0002 (p 0.438); div hit 0.4615 vs cross hit 0.4717
- F2-BULL-hit: contrast -0.0104 (p 0.010); div hit 0.4615 vs cross hit 0.4717
- F2-BEAR-mean: contrast +0.0000 (p 0.840); div hit 0.4579 vs cross hit 0.4519
- F2-BEAR-hit: contrast +0.0060 (p 0.120); div hit 0.4579 vs cross hit 0.4519

**N=5** (drops {"BULL": 16, "BEAR": 50}):
- F1-BULL: n=17001 | mean +0.0022 | win 0.5164 | vs random +0.0008 (p 0.276) | vs same +0.0009 (p 0.198)
- F1-BEAR: n=20862 | mean +0.0020 | win 0.4991 | vs random +0.0006 (p 0.286) | vs same +0.0005 (p 0.350)
- F2-BULL-mean: contrast +0.0009 (p 0.124); div hit 0.5164 vs cross hit 0.5080
- F2-BULL-hit: contrast +0.0085 (p 0.054); div hit 0.5164 vs cross hit 0.5080
- F2-BEAR-mean: contrast +0.0018 (p 0.000); div hit 0.4991 vs cross hit 0.4917
- F2-BEAR-hit: contrast +0.0075 (p 0.050); div hit 0.4991 vs cross hit 0.4917

**N=20** (drops {"BULL": 64, "BEAR": 236}):
- F1-BULL: n=16953 | mean +0.0168 | win 0.5562 | vs random +0.0048 (p 0.000) | vs same +0.0053 (p 0.002)
- F1-BEAR: n=20676 | mean +0.0095 | win 0.5170 | vs random -0.0026 (p 0.044) | vs same -0.0027 (p 0.032)
- F2-BULL-mean: contrast +0.0029 (p 0.012); div hit 0.5562 vs cross hit 0.5448
- F2-BULL-hit: contrast +0.0114 (p 0.008); div hit 0.5562 vs cross hit 0.5448
- F2-BEAR-mean: contrast +0.0012 (p 0.208); div hit 0.5170 vs cross hit 0.5139
- F2-BEAR-hit: contrast +0.0029 (p 0.500); div hit 0.5170 vs cross hit 0.5139

### S2: swing scale k = 3 / 5 (period 10)

**k=3** (drops {"BULL": 28, "BEAR": 125}):
- F1-BULL: n=16046 | mean +0.0086 | vs random +0.0038 (p 0.000) | vs same +0.0039 (p 0.000)
- F1-BEAR: n=19633 | mean +0.0044 | vs random -0.0005 (p 0.586) | vs same -0.0005 (p 0.560)
- F2-BULL-mean: contrast +0.0024 (p 0.000)
- F2-BULL-hit: contrast +0.0175 (p 0.000)
- F2-BEAR-mean: contrast +0.0019 (p 0.000)
- F2-BEAR-hit: contrast +0.0047 (p 0.252)

**k=5** (drops {"BULL": 30, "BEAR": 97}):
- F1-BULL: n=12465 | mean +0.0096 | vs random +0.0047 (p 0.000) | vs same +0.0050 (p 0.000)
- F1-BEAR: n=15159 | mean +0.0030 | vs random -0.0019 (p 0.044) | vs same -0.0020 (p 0.064)
- F2-BULL-mean: contrast +0.0034 (p 0.000)
- F2-BULL-hit: contrast +0.0163 (p 0.000)
- F2-BEAR-mean: contrast +0.0006 (p 0.472)
- F2-BEAR-hit: contrast +0.0102 (p 0.030)

### S3: period 14 (textbook default; crossings at 14)

Drops {"BULL": 28, "BEAR": 105}:
- F1-BULL: n=16854 | mean +0.0069 | vs random +0.0020 (p 0.036) | vs same +0.0023 (p 0.018)
- F1-BEAR: n=20205 | mean +0.0035 | vs random -0.0015 (p 0.064) | vs same -0.0015 (p 0.092)
- F2-BULL-mean: contrast +0.0012 (p 0.166); div hit 0.5395 vs cross hit 0.5330
- F2-BULL-hit: contrast +0.0066 (p 0.156); div hit 0.5395 vs cross hit 0.5330
- F2-BEAR-mean: contrast -0.0002 (p 0.802); div hit 0.5079 vs cross hit 0.5030
- F2-BEAR-hit: contrast +0.0048 (p 0.240); div hit 0.5079 vs cross hit 0.5030
- Frequency at period 14: divergence 37,192 vs crossings 86,756 — ratio 0.4287 (CI 0.4221..0.4373)

### S4: min separation >= 10 bars

Drops {"BULL": 5, "BEAR": 28}:
- F1-BULL: n=3953 | mean +0.0077 | vs random +0.0028 (p 0.196) | vs same +0.0030 (p 0.152)
- F1-BEAR: n=5150 | mean +0.0042 | vs random -0.0007 (p 0.712) | vs same -0.0010 (p 0.540)
- F2-BULL-mean: contrast +0.0015 (p 0.336)
- F2-BULL-hit: contrast +0.0213 (p 0.012)
- F2-BEAR-mean: contrast +0.0017 (p 0.182)
- F2-BEAR-hit: contrast +0.0019 (p 0.830)

### S5: per-year F1 leg mean returns (OOS)

| year | BULL | BEAR |
|---|---|---|
| 2000 | +0.0014 (n=680) | +0.0038 (n=733) |
| 2001 | +0.0159 (n=678) | +0.0087 (n=1174) |
| 2002 | +0.0048 (n=981) | +0.0023 (n=1035) |
| 2003 | +0.0136 (n=732) | +0.0161 (n=1398) |
| 2004 | +0.0100 (n=849) | +0.0028 (n=1349) |
| 2005 | +0.0044 (n=1141) | +0.0053 (n=1289) |
| 2006 | +0.0047 (n=979) | +0.0109 (n=1419) |
| 2007 | -0.0045 (n=1250) | -0.0034 (n=1221) |
| 2008 | -0.0074 (n=1412) | -0.0169 (n=1110) |
| 2009 | +0.0377 (n=1018) | +0.0286 (n=1382) |
| 2010 | +0.0148 (n=1072) | +0.0025 (n=1569) |
| 2011 | -0.0004 (n=1411) | -0.0160 (n=1306) |
| 2012 | +0.0038 (n=1144) | +0.0068 (n=1642) |
| 2013 | +0.0228 (n=993) | +0.0117 (n=1937) |
| 2014 | +0.0121 (n=1410) | -0.0035 (n=1726) |
| 2015 | -0.0032 (n=1341) | -0.0004 (n=1669) |
| 2016 | +0.0242 (n=1276) | +0.0101 (n=2104) |
| 2017 | +0.0060 (n=1511) | +0.0012 (n=1898) |
| 2018 | -0.0016 (n=1736) | -0.0035 (n=1856) |
| 2019 | +0.0220 (n=1474) | +0.0030 (n=2204) |
| 2020 | +0.0146 (n=1624) | +0.0267 (n=2118) |
| 2021 | +0.0052 (n=1541) | +0.0075 (n=2217) |
| 2022 | +0.0061 (n=2083) | -0.0087 (n=1853) |
| 2023 | +0.0011 (n=2053) | +0.0073 (n=2167) |
| 2024 | +0.0078 (n=1677) | +0.0014 (n=2330) |
| 2025 | +0.0032 (n=2010) | -0.0022 (n=2053) |

### S6: IS record (descriptive — selection era)

| leg | n | mean_ret | win_rate |
|---|---|---|---|
| BULL | 17091 | +0.0071 | 0.5334 |
| BEAR | 21959 | +0.0041 | 0.5276 |

### S7: extreme-gated divergence (first swing's RSI beyond 70/30)

Drops {"BULL": 18, "BEAR": 85}:
- F1-BULL: n=10436 | mean +0.0091 | vs random +0.0042 (p 0.000) | vs same +0.0045 (p 0.000)
- F1-BEAR: n=13520 | mean +0.0038 | vs random -0.0011 (p 0.254) | vs same -0.0013 (p 0.204)

### S8: chartist's-eye timing (signal at the pivot bar, entry open t2+1)

*Pre-declared caveat: the swing's future-side fractal condition is then a selection input — it excludes pivots followed by continuation, tilting toward the claim.*

Drops {"BULL": 32, "BEAR": 86}:
- F1-BULL: n=16977 | mean +0.0252 | vs random +0.0203 (p 0.000) | vs same +0.0206 (p 0.000)
- F1-BEAR: n=20812 | mean -0.0117 | vs random -0.0166 (p 0.000) | vs same -0.0167 (p 0.000)

## Reproducibility

`python -X utf8 tools/measure_divergence.py` regenerates this report; the seed is fixed, so results are stable across runs.
Assertions: RSI within [0, 100] everywhere (min 0.000000000000, max 100.000000000000; PASS); no event with first-swing RSI undefined (min t1 10; PASS); no event whose fractal lacks confirmation bars (PASS); no leg ticker missing an OOS window pool (PASS).
Input fingerprints: universe 5e6f45a3c791…, measure code 85f2ae0d4a1e… (Phase-3 engine c7421fbf… imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
