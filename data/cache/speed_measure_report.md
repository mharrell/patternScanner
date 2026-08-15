# Speed-asymmetry measurement report (pre-registration #12)

- Pre-registration #12 (frozen 2026-08-15): claim = 'the move up that may have taken hours can be all given back in a matter of minutes on the good top reversal... the Bulls take the stairs and the Bears take the window so the sell offs can be very quick' (I-F-02, jfe1Zl-5EQI [28:28-28:47], corroborated [17:34-17:37]). Daily translation: speed = price distance per bar. Per-bar size = |close_t/close_{t-1} - 1|; UP bars (r > 0), DOWN bars (r < 0), zero bars (r = 0) excluded from the legs and counted. A1 (F1/F2): down-bars larger than up-bars; A2 (F4): retracements of the frozen pre-reg #11 big up-moves (L=10, tau=3, excursion-first) outpace the moves themselves. N = 10 crossing window; bootstrap 1000 (seed 20260813); alpha 0.05; Holm within each family; count floor 100 events.
- No forward returns are measured: the Phase-3 engine's measure_returns is NOT invoked (pre-reg #12 sec 3) — the claim is about bar geometry, not profitability. Phase 5 is not implicated by construction.
- Era split: IS 2000-2015 / OOS 2016-2025 (by bar date). Intraday->daily translation pre-declared: daily 'speed' is per-bar magnitude; overnight gaps register as fast. Measured on US equity daily bars (the frozen S&P 600 universe).
- OOS bar population: 1371291 bars (UP 689944, DOWN 660952, ZERO 20395); 599 ticker-first bars excluded; down-bar share 0.4820.

## Verdicts — Family 1: absolute, per leg vs the typical-bar baseline

- F1-UP: n=1371291 (UP 689944, DOWN 660952, ZERO 20395) | mean all +0.0184 | mean up +0.0189 | excess +0.0006 (CI +0.0005..+0.0006, p 0.000) | Holm gate 0.0250 -> **FADE (Holm-rejected; excess CI-low +0.0005 > 0 — up-bars larger than typical, claim contradicted)**
- F1-DOWN: n=1371291 (UP 689944, DOWN 660952, ZERO 20395) | mean all +0.0184 | mean down +0.0183 | excess -0.0000 (CI -0.0001..-0.0000, p 0.050) | Holm gate 0.0500 -> **FADE (Holm-rejected; excess CI-upper -0.0000 < 0 — down-bars smaller than typical, claim contradicted)**

## Verdicts — Family 2: the asymmetry contrast (DOWN - UP)

- F2: n_down=660952 n_up=689944 | mean down +0.0183 vs mean up +0.0189 | contrast -0.0006 (CI -0.0007..-0.0005, p 0.000) | Holm gate 0.0500 -> **FADE (contrast CI-upper -0.0005 < 0 — up-bars larger than down-bars, claim contradicted)**

## Verdicts — Family 4: retracement speed on big up-moves (A2)

- F4: n_events=35997 (retraced 11113, non-retraced 24795, tail-dropped 89); share crossing within 10 bars 0.3095; mean j 5.40 bars; mean contrast +0.0040 per bar (CI +0.0037..+0.0044, p 0.000) -> **EDGE (contrast CI-low +0.0037 > 0 — big up-moves' retracements outpace the moves, given-back-fast as claimed)**

## Frequency (measurement, not a verdict family)

- OOS bars: UP 689944 / DOWN 660952 / ZERO 20395 / all 1371291; down-bar share 0.4820; index-0 excluded 599; bad prior 0.

## Sensitivities (exploratory — NO verdicts)

### S1: median |r| (skew-robust)

- F1-UP: median up +0.0126 / median down +0.0124 | excess +0.0004 (CI +0.0003..+0.0004, p 0.000)
- F1-DOWN: median up +0.0126 / median down +0.0124 | excess +0.0001 (CI +0.0001..+0.0001, p 0.000)
- F2 (median contrast): -0.0002 (CI -0.0003..-0.0002, p 0.000)

### S2: candle-sign version (red = close < open)

*Bad priors 0, dojis (close == open) 21410.*
- F1-UP: mean body +0.0167 | excess +0.0003 (CI +0.0003..+0.0004, p 0.000)
- F1-DOWN: mean body +0.0165 | excess +0.0002 (CI +0.0002..+0.0002, p 0.000)
- F2 (red - green): -0.0001 (CI -0.0002..-0.0001, p 0.000)

### S3: per-ticker contrasts (ticker-cluster CI)

- n_tickers=599; share positive 0.2437; mean per-ticker contrast -0.0008 (cluster CI -0.0010..-0.0007, p 0.000)

### S4: IS-era (descriptive — selection era)

- F1-UP: n=1426483 | excess +0.0015 (CI +0.0014..+0.0016, p 0.000)
- F1-DOWN: n=1426483 | excess +0.0001 (CI -0.0000..+0.0002, p 0.078)
- F2 (IS): -0.0014 (CI -0.0016..-0.0012, p 0.000)

### S5: per-year (OOS)

| year | mean UP | mean DOWN | contrast (pp) |
|---|---|---|---|
| 2016 | +0.0170 (n=61571) | +0.0165 (n=54975) | -0.06 |
| 2017 | +0.0141 (n=61817) | +0.0137 (n=57294) | -0.04 |
| 2018 | +0.0158 (n=63600) | +0.0165 (n=61893) | +0.06 |
| 2019 | +0.0156 (n=70011) | +0.0154 (n=60904) | -0.01 |
| 2020 | +0.0302 (n=68754) | +0.0285 (n=66162) | -0.17 |
| 2021 | +0.0196 (n=72225) | +0.0182 (n=68204) | -0.15 |
| 2022 | +0.0216 (n=70020) | +0.0214 (n=73450) | -0.03 |
| 2023 | +0.0181 (n=73644) | +0.0170 (n=70758) | -0.12 |
| 2024 | +0.0177 (n=74675) | +0.0168 (n=72945) | -0.09 |
| 2025 | +0.0190 (n=73627) | +0.0181 (n=74367) | -0.09 |

### S6: swing-scale A1 (strict k-fractal swings on Close)

*Paired contrast: down-swing rate (size/duration) - preceding up-swing rate; same-type pivot runs coalesced to the more extreme; completed swings, swing-end date in OOS.*
- k=2: n_pairs=161320 (up 161741, down 161796) | mean contrast +0.0131 (CI +0.0072..+0.0195, p 0.000)
- k=3: n_pairs=110487 (up 110865, down 110966) | mean contrast +0.0140 (CI +0.0063..+0.0216, p 0.000)
- k=5: n_pairs=67319 (up 67624, down 67810) | mean contrast +0.0354 (CI +0.0262..+0.0450, p 0.000)

### S7: F4 variants

- N=5: retraced 5966 / total 35997; mean j 3.31 | mean contrast +0.0113 (CI +0.0108..+0.0118, p 0.000)
- N=20: retraced 16375 / total 35997; mean j 8.49 | mean contrast +0.0000 (CI -0.0002..+0.0003, p 0.950)
- tau=2: retraced 26358 / total 64694; mean j 4.74 | mean contrast +0.0052 (CI +0.0051..+0.0054, p 0.000)
- tau=5: retraced 896 / total 5416; mean j 5.98 | mean contrast +0.0034 (CI +0.0013..+0.0054, p 0.000)

### S8: tail concentration (largest-|r| decile)

- threshold 0.0397; n_top=137131, down share in top decile 0.4795 vs overall 0.4820 (diff -0.25pp)

## Reproducibility

`python -X utf8 tools/measure_speed.py` regenerates this report; the seed is fixed, so results are stable across runs.
Assertions: no bad prior closes (0); zero bars counted (20395); leg partition covers the full OOS population (PASS); F4 signal bars >= 60 (min 60, PASS); no event whose signal bar lies beyond the ticker's series (PASS); F4 crossing j in [1, N] (by construction).
Input fingerprints: universe 5e6f45a3c791…, measure code 3fbdab9922c5… (engine c7421fbffeaf… NOT invoked — no forward returns; generic helpers from measure_divergence 85f2ae0d4a1e…, measure_veto 214c907131d0…, measure_bigmove 6917f3dc2437…).
Any change to the detector, data, or measurement code changes the frozen inputs and requires a new pre-registration before it can drive a verdict.
