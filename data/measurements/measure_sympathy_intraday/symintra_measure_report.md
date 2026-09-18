# Intraday sympathy measurement report (pre-registration #32)

- Pre-reg #32 (frozen per its freeze block); seed 20260907; entry set = #19 F1 reversal new-high entries (frozen #21 Archive)
- Leader spikes (>= +40% from session open): 0; unmapped tickers 2646
- Floors: {'window_bar_dates': 21, 'events_f1_valid': 43722, 'tickers': 600, 'dates_with_events': 21, 'met': True}

## F1 verdicts (Holm family of 2)

- sector-hot − sector-cold: n_a=0 n_b=30376 | est — (CI —..—, p 1.000) | gate 0.025 -> **INCONCLUSIVE**
- sector-hot − raw (net value): n_a=0 n_b=30376 | est — (CI —..—, p 1.000) | gate 0.05 -> **INCONCLUSIVE**

`python -X utf8 tools/measure_sympathy_intraday.py` regenerates this report (seed fixed). `--floors` is safe.
