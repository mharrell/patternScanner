# E-02 measurement report (pre-registration #7)

- Pre-registration #7 (frozen 2026-08-14): claim = win rate >= 0.80 on the veto-pass setup (both filters pass), N=10 primary, cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260813)
- Era split: IS 2000-2015 / OOS 2016-2025 (by signal date)
- Inputs: veto_detections_v1.csv (pre-reg #3 output, 31570 rows, warm-up excluded 344)
- Win = forward return > 0 after cost (entry open t+1, exit close t+N). Two verdict families, Holm across A/B/C at alpha=0.05, OOS only; F1 = exact one-sided binomial vs 0.80; F2 = win-rate excess vs era-matched baselines.

## Verdicts — Family 1: the claim test (win rate >= 0.80)

- F1-claim-test A: n_pass=3941 | n_wins=1919 | win_rate 0.4869 | one-sided p <1e-308 (log10 -415.3) vs claim 0.8 (CI upper 0.5002) -> **REJECTED — claim falsified (one-sided p <1e-308 (log10 -415.3); CI upper 0.5002 < 0.80, Holm-rejected)**
- F1-claim-test B: n_pass=6940 | n_wins=3400 | win_rate 0.4899 | one-sided p <1e-308 (log10 -717.2) vs claim 0.8 (CI upper 0.4999) -> **REJECTED — claim falsified (one-sided p <1e-308 (log10 -717.2); CI upper 0.4999 < 0.80, Holm-rejected)**
- F1-claim-test C: n_pass=280 | n_wins=148 | win_rate 0.5286 | one-sided p 2.006e-24 vs claim 0.8 (CI upper 0.5790) -> **REJECTED — claim falsified (one-sided p 2.006e-24; CI upper 0.5790 < 0.80, Holm-rejected)**

## Verdicts — Family 2: win-rate edge vs baselines

- F2-win-rate-edge A: n_pass=3941 | win_rate 0.4869 | excess vs random -0.0304 (CI -0.0518..-0.0084, p 0.004) | vs same -0.0357 (p 0.004) | vs spy -0.1754 (p 0.000) | p_input 0.004 -> **NO EDGE (CI includes 0 or estimate <= 0, or Holm gate not cleared)**
- F2-win-rate-edge B: n_pass=6940 | win_rate 0.4899 | excess vs random -0.0276 (CI -0.0445..-0.0114, p 0.000) | vs same -0.0309 (p 0.000) | vs spy -0.1725 (p 0.000) | p_input 0.000 -> **NO EDGE (CI includes 0 or estimate <= 0, or Holm gate not cleared)**
- F2-win-rate-edge C: n_pass=280 | win_rate 0.5286 | excess vs random +0.0136 (CI -0.0679..+0.0964, p 0.786) | vs same +0.0129 (p 0.792) | vs spy -0.1338 (p 0.002) | p_input 0.792 -> **NO EDGE (CI includes 0 or estimate <= 0, or Holm gate not cleared)**

## Sensitivities (exploratory — NO verdicts)

| shape | no-cost wr | N=5 | N=20 | 0.70 p | 0.60 p | pass | kill | full | raw | IS |
|---|---|---|---|---|---|---|---|---|---|---|
| A | 0.5001 | 0.4752 | 0.5132 | 3.869e-171 | 8.907e-47 | 0.4869 | 0.5129 | 0.4948 | 0.4948 | 0.5200 |
| B | 0.5000 | 0.4794 | 0.4782 | 1.227e-291 | 9.244e-77 | 0.4899 | 0.5078 | 0.4906 | 0.4906 | 0.5017 |
| C | 0.5357 | 0.5143 | 0.5181 | 1.258e-09 | 0.009053 | 0.5286 | 0.5686 | 0.5347 | 0.5347 | 0.5051 |

Pass-vs-kill and pass-vs-full win-rate excesses (two-sample bootstrap): A: kill -0.0264 (p 0.066), full -0.0079 (p 0.468); B: kill -0.0191 (p 0.532), full -0.0009 (p 0.916); C: kill -0.0413 (p 0.588), full -0.0059 (p 0.868)

Per-year pass-set win rates (OOS): A: 2016 0.584, 2017 0.462, 2018 0.464, 2019 0.472, 2020 0.506, 2021 0.472, 2022 0.307, 2023 0.452, 2024 0.520, 2025 0.525; B: 2016 0.527, 2017 0.493, 2018 0.496, 2019 0.498, 2020 0.509, 2021 0.434, 2022 0.425, 2023 0.584, 2024 0.417, 2025 0.482; C: 2016 0.533, 2017 0.605, 2018 0.412, 2019 0.590, 2020 0.720, 2021 0.435, 2022 0.556, 2023 0.480, 2024 0.607, 2025 0.250

## Reproducibility

`python -X utf8 tools/measure_e02.py` regenerates this report; the seed is fixed and F1 is RNG-free, so results are stable across runs.
Input fingerprints: veto file eebdc6b11a19…, measure code a43f608133fa… (Phase-3 engine c7421fbf… imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
