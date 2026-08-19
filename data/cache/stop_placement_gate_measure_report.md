# Stop-placement measurement report (pre-registration #14)

- **Gate run (pre-reg #14 §3 — the brief §5 survivorship re-check)**: universe = the pre-reg #13 historical-constituent union (904 names, 5 annual S&P 600 snapshots 2021-2025; bars for 706 — 199 former members purged from Yahoo's data, 0 of them current members, flagged and NOT substituted); OOS 2022-2025.
- Pre-registration #14 (frozen 2026-08-16): claim = the I-X-05 stop-placement claim — after a bullish divergence the market "shouldn't take out that prior extreme low" (rgVdgR1y1Dg [07:40-08:03]); stop level L = Low[t2]; breach ⇔ min(Low[s+1..s+N]) < L; N=10 primary ([5, 20] sensitivity); cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260816)
- Events: the frozen pre-reg #10 bullish-divergence detection recomputed with the frozen functions (measure_divergence.py sha 85f2ae0d4a1e…, measure.py sha c7421fbf… — asserted at import); per-leg all-era counts anchored to divergence_hist_measure_results.json's per_year sums: BULL 42,495, BEAR 52,057 — PASS
- Warm-up guard: signal/confirmation bar index < 60 (frozen #3 convention); warm-up events excluded and counted (baseline bars 5,082)
- Era split: IS 2000-2021 (descriptive only — no IS-era membership data) / OOS 2022-2025 (by signal date).
- Breach: intrabar — min(Low[s+1..s+N]) < L; a stop placed "beyond" the low triggers on a strictly lower trade; an equal low survives.
- F1 baselines: fractal-low confirmation bars (c = f + 2 of every strict k=2 fractal low f, reference Low[f]) — the event template minus the divergence condition; the OOS divergence event bars are excluded (9,384); random = whole universe uniform, same-ticker = event tickers event-count-weighted (the frozen make_sample_same convention).
- F2: OS crossings (pre-reg #9 S4 rule, period 10); reference = the most recent strict k=2 fractal low at bar ≤ c within the 60-bar lookback (crossings without one dropped and counted). Age asymmetry documented conservative: the divergence reference is exactly 2 bars old; a crossing's reference averages older, and older levels are less likely to be breached.

## Verdicts — Family 1: absolute (F1-BULL)

- F1-BULL: n=9,384 | breach_rate 0.5053 | random base 0.5537 (pool 82,299) | excess vs random -0.0482 (CI -0.0628..-0.0343, p 0.000) | vs same -0.0570 (CI -0.0698..-0.0436, p 0.000) | same base 0.5620 | p_input 0.000 | est -0.0482 (CI-low -0.0698..CI-upper -0.0436) | Holm gate 0.0500 -> **EDGE (Holm-rejected; excess CI-upper -0.0436 < 0 — divergence lows hold better than typical lows, as claimed)**

## Verdicts — Family 2: contrast vs oversold crossings (F2-BULL)

- F2-BULL: n_div=9,384 | n_cross=31,509 | div rate 0.5053 | cross rate 0.7736 | contrast -0.2687 (CI -0.2820..-0.2562, p 0.000) | Holm gate 0.0500 -> **EDGE (Holm-rejected; contrast CI-upper -0.2562 < 0 — divergence lows hold better than oversold-crossing references)**

## Measurement rows (no verdicts)

- Stop distance open[s+1] → Low[t2]: mean 0.0553 (5.53%), median 0.0459, p10 0.0142, p90 0.1065; in ATR14 units: mean 1.374, median 1.245, p10 0.408, p90 2.478 (n=9,384)
- Outcome decomposition (events, n=9,384): breach-loss -0.0388 | continue-gain +0.0505 | combined +0.0054 (n_breached 4,742, rate 0.5053)
- Same decomposition, same-ticker baseline (weighted): breach-loss -0.0491 | continue-gain -0.0016 | combined +0.0010
- Same decomposition, random baseline (pooled): breach-loss -0.0481 | continue-gain -0.0004 | combined +0.0019

| year | n | breach rate |
|---|---|---|
| 2000 | 874 | 0.4886 |
| 2001 | 903 | 0.4408 |
| 2002 | 1,231 | 0.4866 |
| 2003 | 885 | 0.4136 |
| 2004 | 1,101 | 0.4587 |
| 2005 | 1,407 | 0.4940 |
| 2006 | 1,188 | 0.4781 |
| 2007 | 1,583 | 0.4978 |
| 2008 | 1,776 | 0.5006 |
| 2009 | 1,250 | 0.3952 |
| 2010 | 1,339 | 0.3712 |
| 2011 | 1,801 | 0.4686 |
| 2012 | 1,511 | 0.4871 |
| 2013 | 1,324 | 0.3769 |
| 2014 | 1,799 | 0.4875 |
| 2015 | 1,785 | 0.5356 |
| 2016 | 1,612 | 0.4045 |
| 2017 | 1,887 | 0.4822 |
| 2018 | 2,130 | 0.5038 |
| 2019 | 1,833 | 0.3983 |
| 2020 | 2,011 | 0.4630 |
| 2021 | 1,881 | 0.4758 |
| 2022 | 2,491 | 0.5267 |
| 2023 | 2,468 | 0.5036 |
| 2024 | 2,087 | 0.5266 |
| 2025 | 2,338 | 0.4654 |

## Sensitivities (exploratory — NO verdicts)

- S1 N=5: event 0.3753 vs random 0.4187 vs same 0.4245 (n=9,407)
- S1 N=20: event 0.6376 vs random 0.6762 vs same 0.6842 (n=9,340)
- S2 stop = Low[t1] (the first, higher low): event 0.7488 vs random 0.5537 vs same 0.5620 (n=9,384; the level is ≥ 7 bars old at the window start vs 2 for the baselines — age asymmetry documented)
- S3 period 14: event 0.5076 vs random 0.5537 vs same 0.5620 (n=9,328; baselines unchanged — fractal lows are RSI-independent)
- S4 close-based breach: event 0.4045 vs random 0.4465 vs same 0.4542 (n=9,384)
- S5 BEAR mirror (High[t2] stop, max > ref): event 0.9039 vs random 0.5629 vs same 0.5713 (n=9,656)

## Reproducibility

`python -X utf8 tools/measure_stop_placement.py` --gate regenerates this report; the seed is fixed, so results are stable across runs.
Assertions: frozen shas (measure.py c7421fbf…, measure_divergence.py 85f2ae0d4a1e…) PASS; RSI within [0, 100] (min 0.000000000000, max 100.000000000000) PASS; min t1 10 ≥ period PASS; n_bad_signal 0 PASS; drops (BULL 49) and crossing drops match PASS; every event ticker has a non-empty OOS baseline pool PASS; per-year anchor sums BULL 42,495 / BEAR 52,057 match the frozen JSON PASS; OOS BULL n 9,384 matches PASS.
Input fingerprints: universe 62f681d58cdb…, measure code a9ccedd16386… (Phase-3 engine c7421fbf… imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
