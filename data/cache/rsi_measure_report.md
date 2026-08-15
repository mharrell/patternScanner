# RSI 70/30 measurement report (pre-registration #9)

- Pre-registration #9 (frozen 2026-08-14): claim = RSI > 70 overbought (pullback due) / RSI < 30 oversold (bounce due); simple-average RSI, period 14 primary (10 sensitivity), thresholds 70/30; N=10 primary, cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260813)
- RSI_t = 100 - 100/(1 + RS) with RS = mean(gains over the 14 daily changes ending at t) / mean(|losses|, same window) — the simple-average formula the video teaches; conventions: avg_loss = 0 -> 100, avg_gain = 0 and avg_loss > 0 -> 0
- Legs are state-based (every qualifying bar is a detection); warm-up guard bar index < 60 (frozen #3 convention, also bounds the lookback); 7409 warm-up detections excluded and counted
- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date). Cross-market caveat pre-declared: the video demos GBP/USD; measured on US equities.
- Detections (period 14, 70/30, warm-up excluded): OB n=399513, OS n=291321 (drops at series end: {"OB": 933, "OS": 454})
- F1 (absolute, directional per leg): OOS mean forward return vs era-matched random entries AND same-ticker (SPY reported), p_input = max, Holm across OB/OS. OB: EDGE iff CI-upper < 0 (pullback); FADE iff CI-low > 0. OS: EDGE iff CI-low > 0 (bounce); FADE iff CI-upper < 0. F2 (contrast): two-sample excess mean(OS) - mean(OB), single test at alpha = 0.05.

## Verdicts — Family 1: absolute (directional per leg)

- F1-OB: n=201419 | mean_ret +0.0023 | excess vs random -0.0026 (CI -0.0031..-0.0020, p 0.000) | vs same -0.0030 (CI -0.0036..-0.0025, p 0.000) | vs spy -0.0035 (p 0.000) | p_input 0.000 | est -0.0026 (CI-low -0.0036..CI-upper -0.0025) | Holm gate 0.0250 -> **EDGE (Holm-rejected; excess CI-upper -0.0025 < 0 — overbought, pullback as claimed)**
- F1-OS: n=150236 | mean_ret +0.0061 | excess vs random +0.0012 (CI +0.0005..+0.0019, p 0.000) | vs same +0.0014 (CI +0.0007..+0.0023, p 0.000) | vs spy +0.0003 (p 0.304) | p_input 0.000 | est +0.0014 (CI-low +0.0005..CI-upper +0.0019) | Holm gate 0.0500 -> **EDGE (Holm-rejected; excess CI-low +0.0005 > 0 — oversold, bounce as claimed)**

## Verdict — Family 2: contrast (reversal symmetry, OS minus OB)

- F2: n_ob=201419 | n_os=150236 | OB mean +0.0023 | OS mean +0.0061 | excess +0.0038 (CI +0.0031..+0.0045, p 0.000) -> **EDGE (contrast CI-low +0.0031 > 0 — OS beats OB, reversal symmetry holds)**

## Sensitivities (exploratory — NO verdicts)

### S1: horizons N = 1 / 5 / 20

*Baselines rebuilt per horizon (era- AND horizon-matched N-bar window pools).*

**N=1** (drops {"OB": 31, "OS": 124}):
- F1-OB: n=202321 | mean -0.0017 | vs random -0.0003 (p 0.000) | vs same -0.0003 (p 0.000)
- F1-OS: n=150566 | mean -0.0008 | vs random +0.0005 (p 0.000) | vs same +0.0006 (p 0.000)
- F2: OS -0.0008 minus OB -0.0017 = +0.0008 (p 0.000)

**N=5** (drops {"OB": 388, "OS": 265}):
- F1-OB: n=201964 | mean -0.0005 | vs random -0.0019 (p 0.000) | vs same -0.0021 (p 0.000)
- F1-OS: n=150425 | mean +0.0024 | vs random +0.0010 (p 0.002) | vs same +0.0010 (p 0.000)
- F2: OS +0.0024 minus OB -0.0005 = +0.0029 (p 0.000)

**N=20** (drops {"OB": 2869, "OS": 624}):
- F1-OB: n=199483 | mean +0.0054 | vs random -0.0067 (p 0.000) | vs same -0.0077 (p 0.000)
- F1-OS: n=150066 | mean +0.0187 | vs random +0.0066 (p 0.000) | vs same +0.0070 (p 0.000)
- F2: OS +0.0187 minus OB +0.0054 = +0.0133 (p 0.000)

### S2: thresholds 80/20, 90/10, 60/40 (period 14)

**80/20** (drops {"OB": 288, "OS": 123}):
- F1-OB: n=64237 | mean +0.0026 | vs random -0.0024 (p 0.000) | vs same -0.0033 (p 0.000)
- F1-OS: n=42624 | mean +0.0061 | vs random +0.0012 (p 0.118) | vs same +0.0012 (p 0.176)
- F2: OS +0.0061 minus OB +0.0026 = +0.0035 (p 0.000)

**90/10** (drops {"OB": 27, "OS": 25}):
- F1-OB: n=11004 | mean +0.0067 | vs random +0.0019 (p 0.258) | vs same -0.0014 (p 0.528)
- F1-OS: n=6162 | mean +0.0139 | vs random +0.0091 (p 0.004) | vs same +0.0080 (p 0.030)
- F2: OS +0.0139 minus OB +0.0067 = +0.0072 (p 0.030)

**60/40** (drops {"OB": 2146, "OS": 1227}):
- F1-OB: n=433923 | mean +0.0029 | vs random -0.0020 (p 0.000) | vs same -0.0022 (p 0.000)
- F1-OS: n=353413 | mean +0.0061 | vs random +0.0012 (p 0.000) | vs same +0.0014 (p 0.000)
- F2: OS +0.0061 minus OB +0.0029 = +0.0032 (p 0.000)

### S3: period 10 at 70/30

Drops {"OB": 1038, "OS": 942}:
- F1-OB: n=261073 | mean +0.0021 | vs random -0.0028 (p 0.000) | vs same -0.0031 (p 0.000)
- F1-OS: n=206739 | mean +0.0051 | vs random +0.0002 (p 0.526) | vs same +0.0003 (p 0.284)
- F2: OS +0.0051 minus OB +0.0021 = +0.0030 (p 0.000)

### S4: crossing-based events (first bar of each excursion)

Events: OB 96008, OS 76006 (drops {"OB": 187, "OS": 196}):
- F1-OB: n=47730 | mean +0.0037 | vs random -0.0011 (p 0.060) | vs same -0.0013 (p 0.016)
- F1-OS: n=38643 | mean +0.0057 | vs random +0.0008 (p 0.250) | vs same +0.0009 (p 0.144)
- F2: OS +0.0057 minus OB +0.0037 = +0.0020 (p 0.000)

### S5: per-year F1 leg mean returns (OOS)

| year | OB | OS |
|---|---|---|
| 2000 | -0.0034 (n=6380) | +0.0177 (n=5946) |
| 2001 | +0.0131 (n=11684) | +0.0226 (n=7382) |
| 2002 | -0.0005 (n=9353) | +0.0122 (n=8672) |
| 2003 | +0.0161 (n=13459) | +0.0175 (n=5839) |
| 2004 | +0.0171 (n=13098) | +0.0125 (n=7224) |
| 2005 | +0.0074 (n=10779) | +0.0262 (n=9313) |
| 2006 | +0.0066 (n=11986) | +0.0048 (n=7057) |
| 2007 | -0.0042 (n=9305) | +0.0007 (n=10069) |
| 2008 | -0.0066 (n=7058) | +0.0069 (n=12772) |
| 2009 | +0.0125 (n=12694) | +0.0442 (n=8465) |
| 2010 | +0.0072 (n=16384) | +0.0201 (n=7805) |
| 2011 | -0.0110 (n=9492) | +0.0043 (n=9053) |
| 2012 | +0.0090 (n=15767) | +0.0099 (n=8864) |
| 2013 | +0.0048 (n=20909) | +0.0167 (n=7265) |
| 2014 | -0.0006 (n=16423) | +0.0039 (n=12316) |
| 2015 | -0.0044 (n=13323) | +0.0027 (n=13043) |
| 2016 | +0.0096 (n=22253) | +0.0230 (n=12384) |
| 2017 | +0.0034 (n=19520) | +0.0097 (n=12309) |
| 2018 | -0.0008 (n=17070) | +0.0099 (n=17011) |
| 2019 | +0.0008 (n=24191) | +0.0123 (n=12093) |
| 2020 | +0.0059 (n=19284) | -0.0321 (n=14635) |
| 2021 | +0.0017 (n=19358) | +0.0173 (n=11258) |
| 2022 | -0.0086 (n=16284) | +0.0046 (n=19378) |
| 2023 | +0.0097 (n=23815) | -0.0015 (n=17747) |
| 2024 | -0.0035 (n=20964) | +0.0126 (n=16225) |
| 2025 | +0.0010 (n=18680) | +0.0122 (n=17196) |

### S6: IS record at 70/30 (descriptive — selection era)

| leg | n | mean_ret | win_rate |
|---|---|---|---|
| OB | 198094 | +0.0050 | 0.5134 |
| OS | 141085 | +0.0128 | 0.5347 |

### S7: RSI distribution over OOS bars

- OOS bars with RSI defined: 1,369,590 | share > 70 (OB): 0.1486 | share < 30 (OS): 0.1104 | share in [30, 70]: 0.7410
- RSI min 0.0000 / max 100.0000 over OOS bars

## Reproducibility

`python -X utf8 tools/measure_rsi.py` regenerates this report; the seed is fixed, so results are stable across runs.
Assertions: RSI within [0, 100] everywhere (min 0.000000000000, max 100.000000000000; PASS); no detections with < 14 prior closes (PASS); no leg ticker missing an OOS window pool (PASS).
Input fingerprints: universe 5e6f45a3c791…, measure code cfc225253f71… (Phase-3 engine c7421fbf… imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
