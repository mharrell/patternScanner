# Stop-placement measurement report (pre-registration #14)

- Pre-registration #14 (frozen 2026-08-16): claim = the I-X-05 stop-placement claim — after a bullish divergence the market "shouldn't take out that prior extreme low" (rgVdgR1y1Dg [07:40-08:03]); stop level L = Low[t2]; breach ⇔ min(Low[s+1..s+N]) < L; N=10 primary ([5, 20] sensitivity); cost 0.0015, alpha 0.05, bootstrap 1000 (seed 20260816)
- Events: the frozen pre-reg #10 bullish-divergence detection recomputed with the frozen functions (measure_divergence.py sha 85f2ae0d4a1e…, measure.py sha c7421fbf… — asserted at import). **Anchor DEVIATION — see the Data-integrity section below**: the frozen primary record cannot be regenerated from the current bars (BULL 34,075 vs frozen 34,076, BEAR 42,757 vs frozen 42,759, fam1 BULL n 16,984 vs frozen 16,985).
- Warm-up guard: signal/confirmation bar index < 60 (frozen #3 convention); warm-up events excluded and counted (baseline bars 4,336)
- Era split: IS 2000-2015 (descriptive) / OOS 2016-2025 (by signal date).
- Breach: intrabar — min(Low[s+1..s+N]) < L; a stop placed "beyond" the low triggers on a strictly lower trade; an equal low survives.
- F1 baselines: fractal-low confirmation bars (c = f + 2 of every strict k=2 fractal low f, reference Low[f]) — the event template minus the divergence condition; the OOS divergence event bars are excluded (16,984); random = whole universe uniform, same-ticker = event tickers event-count-weighted (the frozen make_sample_same convention).
- F2: OS crossings (pre-reg #9 S4 rule, period 10); reference = the most recent strict k=2 fractal low at bar ≤ c within the 60-bar lookback (crossings without one dropped and counted). Age asymmetry documented conservative: the divergence reference is exactly 2 bars old; a crossing's reference averages older, and older levels are less likely to be breached.

## Data integrity — anchor deviation (primary record)

Pre-registration #14 §2 requires the event set to BE the frozen pre-reg #10 event set (anchored to the frozen divergence_measure_results.json per-year counts). On the current bars that anchor CANNOT be satisfied: the frozen pipeline — and md.main() itself, run with outputs rebound and shas asserted — yields BULL 34075 / BEAR 42757 / fam1 16984 vs the frozen 34076 / 42759 / 16985. The frozen #13 hist record (2026-08-16) regenerates EXACTLY on the same data, bracketing the change to the 08-15 → 08-16 window (the vendor restated or re-derived the bars). The 08-13-era bytes are unrecoverable: fetch_log.json records only rows/dates — no hashes — and no raw downloads exist.

Quantified deviation (per-year deltas, observed − frozen):

| year | BULL | BEAR |
|---|---|---|
| 2016 | +0 | -1 |
| 2017 | +0 | -1 |
| 2021 | -1 | +0 |
| 2024 | +0 | -1 |
| 2025 | +32 | +113 |

- Totals: BULL -1 (sum 34,075 vs frozen 34,076), BEAR -2 (sum 42,757 vs frozen 42,759); raw OOS BULL 17,016 vs frozen 17,017, BEAR 20,910 vs frozen 20,912; fam1 BULL n 16,984 vs frozen 16,985.
- The OOS BULL event set under test differs from the frozen record by exactly 1 event (≈6e-5 of the event count). The drift-materiality guard bounds any rate shift by 1.95e-04 (F1) / 1.94e-04 (F2) — ~60× below the bootstrap CI width at n≈17k — and flags a verdict drift-sensitive if its decisive CI bound falls within that bound of zero.
- This is a data-state deviation, NOT a parameter change; no frozen file was modified; the deviation is recorded here and in the results JSON (`anchor` block), and will be logged in the claims ledger.

## Verdicts — Family 1: absolute (F1-BULL)

- F1-BULL: n=16,984 | breach_rate 0.4754 | random base 0.5299 (pool 165,376) | excess vs random -0.0546 (CI -0.0647..-0.0444, p 0.000) | vs same -0.0571 (CI -0.0675..-0.0466, p 0.000) | same base 0.5328 | p_input 0.000 | est -0.0546 (CI-low -0.0675..CI-upper -0.0466) | Holm gate 0.0500 -> **EDGE (Holm-rejected; excess CI-upper -0.0466 < 0 — divergence lows hold better than typical lows, as claimed)**

## Verdicts — Family 2: contrast vs oversold crossings (F2-BULL)

- F2-BULL: n_div=16,984 | n_cross=57,427 | div rate 0.4754 | cross rate 0.7609 | contrast -0.2856 (CI -0.2958..-0.2758, p 0.000) | Holm gate 0.0500 -> **EDGE (Holm-rejected; contrast CI-upper -0.2758 < 0 — divergence lows hold better than oversold-crossing references)**

## Measurement rows (no verdicts)

- Stop distance open[s+1] → Low[t2]: mean 0.0528 (5.28%), median 0.0424, p10 0.0130, p90 0.1030; in ATR14 units: mean 1.397, median 1.280, p10 0.438, p90 2.496 (n=16,984)
- Outcome decomposition (events, n=16,984): breach-loss -0.0366 | continue-gain +0.0455 | combined +0.0064 (n_breached 8,075, rate 0.4754)
- Same decomposition, same-ticker baseline (weighted): breach-loss -0.0450 | continue-gain +0.0039 | combined +0.0036
- Same decomposition, random baseline (pooled): breach-loss -0.0447 | continue-gain +0.0041 | combined +0.0038

| year | n | breach rate |
|---|---|---|
| 2000 | 680 | 0.4838 |
| 2001 | 678 | 0.4307 |
| 2002 | 981 | 0.4862 |
| 2003 | 732 | 0.4221 |
| 2004 | 849 | 0.4641 |
| 2005 | 1,141 | 0.4987 |
| 2006 | 979 | 0.4617 |
| 2007 | 1,250 | 0.4960 |
| 2008 | 1,412 | 0.5113 |
| 2009 | 1,018 | 0.4037 |
| 2010 | 1,072 | 0.3685 |
| 2011 | 1,411 | 0.4826 |
| 2012 | 1,144 | 0.4607 |
| 2013 | 993 | 0.3666 |
| 2014 | 1,410 | 0.4837 |
| 2015 | 1,341 | 0.5227 |
| 2016 ** | 1,276 | 0.3958** |
| 2017 ** | 1,511 | 0.4653** |
| 2018 ** | 1,736 | 0.5058** |
| 2019 ** | 1,474 | 0.3772** |
| 2020 ** | 1,624 | 0.4631** |
| 2021 ** | 1,540 | 0.4883** |
| 2022 ** | 2,083 | 0.5180** |
| 2023 ** | 2,053 | 0.5032** |
| 2024 ** | 1,677 | 0.5182** |
| 2025 ** | 2,010 | 0.4716** |

## Sensitivities (exploratory — NO verdicts)

- S1 N=5: event 0.3590 vs random 0.4028 vs same 0.4049 (n=17,000)
- S1 N=20: event 0.5946 vs random 0.6471 vs same 0.6498 (n=16,952)
- S2 stop = Low[t1] (the first, higher low): event 0.7283 vs random 0.5299 vs same 0.5328 (n=16,984; the level is ≥ 7 bars old at the window start vs 2 for the baselines — age asymmetry documented)
- S3 period 14: event 0.4729 vs random 0.5299 vs same 0.5328 (n=16,853; baselines unchanged — fractal lows are RSI-independent)
- S4 close-based breach: event 0.3724 vs random 0.4143 vs same 0.4171 (n=16,984)
- S5 BEAR mirror (High[t2] stop, max > ref): event 0.8918 vs random 0.5872 vs same 0.5901 (n=20,798)

## Reproducibility

`python -X utf8 tools/measure_stop_placement.py` regenerates this report; the seed is fixed, so results are stable across runs.
Assertions: frozen shas (measure.py c7421fbf…, measure_divergence.py 85f2ae0d4a1e…) PASS; RSI within [0, 100] (min 0.000000000000, max 100.000000000000) PASS; min t1 10 ≥ period PASS; n_bad_signal 0 PASS; drops (BULL 32) and crossing drops match PASS; every event ticker has a non-empty OOS baseline pool PASS; per-year anchor: DEVIATION (see the Data-integrity section) — BULL 34,075 vs frozen 34,076, BEAR 42,757 vs frozen 42,759, fam1 16,984 vs frozen 16,985.
Input fingerprints: universe 5e6f45a3c791…, measure code a9ccedd16386… (Phase-3 engine c7421fbf… imported unchanged).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
