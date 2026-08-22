# I-F-03 §5 gate report (pre-registration #18) — historical-constituent re-check

- Pre-registration #18 (frozen 2026-08-21): claim = 'Stocks will trend with the overall market unless they have a reason not to' (txWaMpSzHhM [31:55-32:38]). Ledger row I-F-03; priority-list item 17 (the final testable-daily item).
- Structural campaign: no forward returns, no entry/exit, no cost. The Phase-3 engine's measure_returns is NOT invoked — the claim is about co-movement, not profitability. Phase 5 cannot fire from this campaign by construction.
- Universe: hist union 904 (706 with bars) — §5 gate. Market factor: SPY daily close-to-close (equal-weight S&P 600 mean = sensitivity S7). Era split: IS 2000-2015 / OOS 2016-2025 (by bar date).
- Bootstrap B=1000, seed 20260813, alpha 0.05, Holm within each family; catalyst = gap |open/prior close - 1| >= 0.02 OR RV = vol/mean(vol, prior 20) >= 2.0.

## Verdicts — Family 1 (market-trending baseline)

- **F1** (trend): n_stocks=703 | mean corr +0.4455 | CI +0.4370..+0.4537 | p 0.0000 (gate 0.0500) -> **EDGE (Holm-rejected; CI-low +0.4370 > 0 — stocks trend with the market, as claimed)**

## Verdicts — Family 2 (catalyst decoupling)

- **F2-gap** (decoupling): n_stocks=698 | mean diff +0.0858 | CI +0.0757..+0.0949 | p 0.0000 (gate 0.0250) -> **FADE (Holm-rejected; CI-low +0.0757 > 0 — correlation HIGHER on catalyst days, claim contradicted)**
- **F2-vol** (decoupling): n_stocks=691 | mean diff -0.2310 | CI -0.2416..-0.2207 | p 0.0000 (gate 0.0500) -> **EDGE (Holm-rejected; CI-upper -0.2207 < 0 — correlation lower on catalyst days, decoupling as claimed)**

## Verdicts — Family 3 (buck-the-trend)

- **F3-gap** (buck-the-run): n_down=1107 (excl 6) | mean contrast +0.0001 | CI -0.0012..+0.0016 | p 0.8940 (gate 0.0500) -> **NO EDGE (p 0.8940; est +0.0001; CI -0.0012..+0.0016)**
- **F3-vol** (buck-the-run): n_down=1097 (excl 16) | mean contrast +0.0042 | CI +0.0029..+0.0056 | p 0.0000 (gate 0.0250) -> **EDGE (Holm-rejected; CI-low +0.0029 > 0 — catalyst stocks run when the market runs, as claimed)**

## Census

| measure | value |
|---|---|
| n_stocks | 706 |
| oos_stock_days | 1646824 |
| cat_gap_stock_days | 133709 |
| cat_vol_stock_days | 90944 |
| f1_candidates | 703 |
| f2_gap_candidates | 698 |
| f2_vol_candidates | 691 |
| n_down_days_total | 1113 |


## Reproducibility

`python -X utf8 tools/measure_if03.py [--gate]` regenerates this report; the seed is fixed, so bootstrap results are stable across runs.
- Tool sha256: 86e382c4b6e7ebeb61babde9721b667830cfa19591b8fa1b40cda4676372e9f3 (frozen fixed-point sha 779861550ad3fc27…)
- Engine sha (measure.py, NOT invoked): 2d2c6b2ec85787c0
- Report sha256: 8f21b9e9435db4bbddebb2453d74d92c33a7748c382b8509ec0334cb27a06f52

