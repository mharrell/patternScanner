# RV measurement report (pre-registration #8)

- Pre-registration #8 (frozen 2026-08-14): claim = pattern trading only works on high-relative-volume stocks (RV >= 2.0, the frozen V = 2.0 multiplier); N=10 primary, cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260813)
- RV_t = v_t / mean(v, prior 20 bars) — the frozen detector's exact formula (rolling(20).mean().shift(1), mean > 0 guard). Primary threshold 2.0; sensitivities 1.0, 3.0, 5.0 (no verdicts)
- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)
- Inputs: veto_detections_v1.csv (pre-reg #3 output, 31570 rows, warm-up excluded 344; RV undefined 0 — expected 0)
- F1 (absolute): high-RV subset vs era-matched random entries AND same-ticker, p_input = max, Holm across A/B/C. F2 (contrast): high-RV minus low-RV two-sample excess, Holm across B/C — F2-A INCONCLUSIVE BY CONSTRUCTION (every A detection has RV >= 2.0; min 2.000 asserted).

## Verdicts — Family 1: absolute edge of the high-RV subset

- F1-absolute A: n_high=3941 | mean_ret +0.0021 | excess vs random -0.0027 (CI -0.0063..+0.0006, p 0.112) | vs same -0.0022 (CI -0.0057..+0.0010, p 0.204) | vs spy -0.0036 (p 0.006) | p_input 0.204 | Holm gate 0.0167 -> **NO EDGE (p_input 0.204; est -0.0022; CI-low -0.0063)**
- F1-absolute B: n_high=1026 | mean_ret +0.0024 | excess vs random -0.0024 (CI -0.0103..+0.0053, p 0.548) | vs same -0.0037 (CI -0.0121..+0.0041, p 0.350) | vs spy -0.0033 (p 0.232) | p_input 0.548 | Holm gate 0.0250 -> **NO EDGE (p_input 0.548; est -0.0024; CI-low -0.0121)**
- F1-absolute C: n_high=46 | mean_ret +0.0036 | excess vs random -0.0011 (CI -0.0344..+0.0303, p 0.938) | vs same -0.0027 (CI -0.0364..+0.0305, p 0.868) | vs spy -0.0027 (p 0.798) | p_input 0.938 | Holm gate 0.0500 -> **INCONCLUSIVE (<100 high-RV OOS detections; n=46)**

## Verdicts — Family 2: high-RV minus low-RV contrast

- F2-contrast A: **INCONCLUSIVE by construction (Shape A detector requires RV >= 2.0; min RV asserted)** — min RV over A detections 2.000000 >= 2.0 (asserted); the RV < 2.0 cell is empty
- F2-contrast B: n_high=1026 | n_low=5914 | high +0.0024 | low -0.0005 | excess +0.0030 (CI -0.0027..+0.0090, p 0.302) | Holm gate 0.025 -> **NO EDGE (contrast est +0.0030; p 0.302)**
- F2-contrast C: n_high=46 | n_low=234 | high +0.0036 | low +0.0048 | excess -0.0015 (CI -0.0244..+0.0230, p 0.914) | Holm gate 0.05 -> **INCONCLUSIVE (<100 OOS detections in a cell; high 46, low 234)**

## Sensitivities (exploratory — NO verdicts)

### Threshold RV >= 1.0

| shape | n_high | mean_ret | vs random (CI, p) | vs same (CI, p) | p_input |
|---|---|---|---|---|---|
| A | 3941 | +0.0021 | -0.0027 (-0.0064..+0.0010, 0.154) | -0.0024 (-0.0058..+0.0011, 0.150) | 0.154 |
| B | 4225 | +0.0013 | -0.0036 (-0.0074..-0.0000, 0.048) | -0.0040 (-0.0078..-0.0002, 0.040) | 0.048 |
| C | 166 | +0.0099 | +0.0046 (-0.0139..+0.0223, 0.614) | +0.0047 (-0.0131..+0.0229, 0.610) | 0.614 |

F2 (contrast): A: n_high 3941, n_low 0, excess — (p —); B: n_high 4225, n_low 2715, excess +0.0036 (p 0.058); C: n_high 166, n_low 114, excess +0.0129 (p 0.21)

### Threshold RV >= 3.0

| shape | n_high | mean_ret | vs random (CI, p) | vs same (CI, p) | p_input |
|---|---|---|---|---|---|
| A | 1440 | +0.0011 | -0.0037 (-0.0090..+0.0020, 0.210) | -0.0037 (-0.0093..+0.0018, 0.178) | 0.210 |
| B | 426 | +0.0011 | -0.0039 (-0.0159..+0.0084, 0.502) | -0.0061 (-0.0185..+0.0068, 0.348) | 0.502 |
| C | 19 | +0.0155 | +0.0112 (-0.0451..+0.0609, 0.662) | +0.0092 (-0.0562..+0.0701, 0.732) | 0.732 |

F2 (contrast): A: n_high 1440, n_low 6283, excess — (p —); B: n_high 426, n_low 6514, excess +0.0011 (p 0.806); C: n_high 19, n_low 261, excess +0.0124 (p 0.506)

### Threshold RV >= 5.0

| shape | n_high | mean_ret | vs random (CI, p) | vs same (CI, p) | p_input |
|---|---|---|---|---|---|
| A | 403 | +0.0043 | -0.0007 (-0.0123..+0.0110, 0.898) | -0.0014 (-0.0136..+0.0105, 0.834) | 0.898 |
| B | 147 | +0.0060 | +0.0011 (-0.0215..+0.0227, 0.920) | -0.0013 (-0.0267..+0.0224, 0.914) | 0.920 |
| C | 7 | +0.0144 | +0.0090 (-0.0942..+0.1128, 0.906) | +0.0091 (-0.1045..+0.1301, 0.886) | 0.906 |

F2 (contrast): A: n_high 403, n_low 9001, excess — (p —); B: n_high 147, n_low 6793, excess +0.0065 (p 0.454); C: n_high 7, n_low 273, excess +0.0099 (p 0.83)

### Full (non-vetoed) set at RV >= 2.0 — F1 only

| shape | n_high | mean_ret | vs random (p) | vs same (p) |
|---|---|---|---|---|
| A | 5641 | +0.0040 | -0.0011 (0.570) | -0.0003 (0.826) |
| B | 1163 | +0.0018 | -0.0032 (0.370) | -0.0042 (0.274) |
| C | 56 | +0.0129 | +0.0074 (0.620) | +0.0070 (0.698) |

### Per-year high-RV mean returns (OOS)

| year | A | B | C |
|---|---|---|---|
| 2016 | +0.0198 (n=500) | -0.0086 (n=111) | +0.0417 (n=2) |
| 2017 | +0.0003 (n=710) | -0.0146 (n=99) | -0.0227 (n=5) |
| 2018 | -0.0045 (n=509) | -0.0048 (n=98) | -0.0193 (n=8) |
| 2019 | -0.0020 (n=638) | -0.0032 (n=120) | -0.0137 (n=8) |
| 2020 | +0.0014 (n=162) | +0.0420 (n=89) | +0.0882 (n=7) |
| 2021 | +0.0016 (n=320) | -0.0089 (n=121) | -0.0111 (n=3) |
| 2022 | -0.0198 (n=114) | +0.0054 (n=71) | +0.0511 (n=2) |
| 2023 | -0.0030 (n=310) | +0.0080 (n=146) | -0.0422 (n=3) |
| 2024 | +0.0090 (n=421) | +0.0113 (n=102) | +0.0031 (n=4) |
| 2025 | +0.0023 (n=257) | +0.0057 (n=69) | -0.0281 (n=4) |

### IS record at RV >= 2.0 (descriptive — selection era)

| shape | n | mean_ret | win_rate |
|---|---|---|---|
| A | 6365 | +0.0070 | 0.5200 |
| B | 1490 | +0.0026 | 0.5054 |
| C | 87 | -0.0087 | 0.5172 |

### Shape-level RV distributions (veto-pass detections)

| shape | n | median RV | min RV | share >= 2.0 | >= 3.0 | >= 5.0 |
|---|---|---|---|---|---|---|
| A | 10313 | 2.687 | 2.000 | 1.0000 | 0.3905 | 0.1265 |
| B | 15400 | 1.139 | 0.000 | 0.1635 | 0.0737 | 0.0255 |
| C | 767 | 1.087 | 0.000 | 0.1734 | 0.0769 | 0.0196 |

## Reproducibility

`python -X utf8 tools/measure_rv.py` regenerates this report; the seed is fixed, so results are stable across runs.
Assertions: min RV over Shape A detections 2.000000 >= 2.0 - 1e-9 (detector construction check, PASS); RV undefined for 0 detections (expected 0).
Input fingerprints: veto file eebdc6b11a19…, measure code aac62e56b78c… (Phase-3 engine c7421fbf… imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
