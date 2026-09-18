# MACD gate measurement report (pre-registration #27)

- Pre-reg #27 (frozen per its freeze block); seed 20260902, B=1000, alpha 0.05, N=60, cost 0.0015; entry set = #19 F1 reversal new-high entries (reusing the frozen #21 Archive)
- Floors: {'window_bar_dates': 21, 'events_f1_valid': 43722, 'tickers': 600, 'dates_with_events': 21, 'met': True}

## F1 verdicts (Holm family of 4)

- open − closed (primary claim): n_a=10333 n_b=31162 | est 0.0000 (CI -0.0002..0.0002, p 0.920) | gate 0.05 -> **INCONCLUSIVE**
- open − raw (net filter value): n_a=10333 n_b=41495 | est 0.0000 (CI -0.0002..0.0002, p 0.904) | gate 0.025 -> **INCONCLUSIVE**
- ≤30min-after-cross − >30min: n_a=983 n_b=9350 | est -0.0004 (CI -0.0011..0.0003, p 0.210) | gate 0.0125 -> **INCONCLUSIVE**
- at-running-high − below (gate-open only): n_a=2011 n_b=8322 | est -0.0002 (CI -0.0007..0.0003, p 0.444) | gate 0.016666666666666666 -> **INCONCLUSIVE**

## Strata (news-spike exemption, J-B-04 — descriptive)

- early_<=30min: n=3321, gate-open share 0.2818
- late_>30min: n=38174, gate-open share 0.2462

## F2 descriptives

- gate-open 10333 / closed 31162 of 41495 evaluable entries; line<0 share 0.6710; closed∩line<0 share 0.7042

## Reproducibility

`python -X utf8 tools/measure_macd_gate.py` regenerates this report (seed fixed). `--floors` reports floor status only.
Manifest sha 40c5b385554c…; veto engine 6989330642d0… imported unchanged.
