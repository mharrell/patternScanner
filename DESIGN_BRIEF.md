# Daytrading Pattern Detector — Design Brief v0.1

**Date:** 2026-08-13
**Status:** DRAFT — pending Mr. Mike's sign-off on Section 9
**Repo:** patternScanner (public)

## 1. Purpose

A research project, not a trading system. Detect predefined chart shapes on US
equity daily bars and measure, honestly, whether those detections predict
forward returns better than chance. No execution, no real money in v1.

The aspiration ("something I could *theoretically* make money with") sets the
bar, not the roadmap: **a shape is only interesting if it beats buy-and-hold
after transaction costs.** If no shape clears that bar, the project's result is
a rigorous null — which is still worth publishing.

## 2. Goals (v1)

1. Operational, code-computable definitions of 2–3 chart shapes.
2. A detector that scans ~25 years of daily bars across the S&P 500 universe.
3. Every detection logged (ticker, date, shape, parameters, price).
4. Forward-return base rates per shape, measured against calibrated baselines.
5. Walk-forward validation: parameters fixed on one era, evaluated on another.

## 3. Non-Goals (v1)

- No order execution, no broker API, no live loop. (Alpaca paper trading is a
  later phase, and only to verify plumbing after a shape shows edge.)
- Daily bars only — no intraday data. These shapes are multi-day structures.
- No news, fundamentals, sentiment, or LLM in the loop.
- No ML model. v1 is pure rule-based detection. ML earns a place later only if
  a shape clears the bar and needs exploitation, not discovery.
- Not investment advice; nothing here ever trades real money without a separate
  decision.

## 4. Shape Definitions (DRAFT)

Each shape needs: a computable definition, an entry rule, an exit rule, and a
parameter set. **Parameters are pre-registered** (Section 6): changing them
after seeing results is a new hypothesis, requiring a fresh test window.

Notation: closes c_t, highs h_t, lows l_t, volume v_t. Entry is always the next
open after the signal bar (no look-ahead). Exit is time-based after N bars —
v1 has no shape-based exits; keep it simple.

### Shape A — Consolidation breakout
- Setup: the last K bars' closes stay within [lo, hi] where (hi − lo) / lo ≤ W.
- Signal: bar t closes above hi AND v_t ≥ V × mean(v, prior 20 bars).
- Entry: open of t+1. Exit: N bars later (draft N = 10).

### Shape B — Pullback-to-trend
- Setup: uptrend — c_t above its M-day simple MA for T consecutive bars.
- Pullback: price falls toward the MA but every close of the last P bars stays
  above it (the trend holds).
- Signal: first close making a new K-day high after the pullback.
- Entry: open of t+1. Exit: N bars later (draft N = 10).

### Shape C — Double bottom
- Setup: two swing lows L1, L2 with |L1 − L2| / L1 ≤ X, separated by ≥ D bars,
  with a local peak P between them.
- Signal: close above P.
- Entry: open of t+1. Exit: N bars later (draft N = 10).

Draft values are placeholders; final values are decided in Phase 2 and
pre-registered before the first measurement run.

## 5. Universe & Data

- **Source:** yfinance (Yahoo-sourced), **adjusted** closes (splits/dividends).
- **Universe:** S&P 500 constituents, daily bars, 2000-01-01 → 2025-12-31.
- **Survivorship bias:** backtesting on *current* constituents only sees
  survivors. Options: (a) historical constituent lists (archived Wikipedia
  snapshots or a data vendor); (b) current list, bias documented and reported.
  Recommendation: (b) for v1 — cheap, and the bias direction is known: it
  inflates returns, so any **null** result is strengthened, and any positive
  result must be re-checked against (a) before being trusted. (Open decision,
  Section 9.)

## 6. Measurement Protocol

For every detection at bar t (per shape, per ticker):

- **Forward return:** (c_{t+N} − c_t) / c_t, entering at open of t+1, exiting
  at close of t+N. No look-ahead.
- **Costs:** 0.15% round-trip (commission + slippage; open decision, Section 9)
  deducted from every trade.
- **Baselines (calibrated, BreakoutBot F-001 style):**
  1. Random entries — same count, random bars, same universe, bootstrapped
     (1,000 resamples) → report confidence intervals.
  2. Buy-and-hold SPY over matching windows.
  3. Buy-and-hold the same ticker (does the shape beat just holding?).
- **Metrics per shape:** mean/median excess return vs each baseline, hit rate,
  max drawdown, Sharpe — all with bootstrap CIs (L-014: no point estimate
  without an interval).
- **Walk-forward split:** in-sample 2000–2015 (parameter selection only),
  out-of-sample 2016–2025 (evaluation). Nothing learned out-of-sample flows
  back into parameters.
- **Multiple testing:** K shapes × parameterizations inflate false positives.
  Mitigation: one pre-registered parameterization per shape; Bonferroni/Holm-
  corrected significance; anything else labeled exploratory.

## 7. Bias Checklist (trading's L-###)

| Bias | Rule |
|---|---|
| Look-ahead | Signal at close t uses only data ≤ t; enter at open t+1 |
| Survivorship | Documented (Section 5); positive results require historical constituents |
| Costs & slippage | Every backtest includes round-trip cost; otherwise results are fiction |
| Multiple testing | Pre-registered params + correction (Section 6) |
| Non-stationarity | Walk-forward split + per-decade result breakdown |
| Data quality | Adjusted closes; flag delistings/gaps |

## 8. Phases

| Phase | Work | Exit criterion |
|---|---|---|
| 0 | Repo + this brief | Brief sign-off |
| 1 | Data pipeline + universe | Clean 2000–2025 daily bars, documented gaps |
| 2 | 3 detectors + pre-registered params | Detections reproducible from raw data |
| 3 | Measurement + baselines | Full per-shape report |
| 4 | Verdicts | Per shape: edge / no edge / inconclusive |
| 5 | Paper trading (only if a shape clears) | Plumbing verified; backtest-live gap measured (L-007) |
| 6 | Micro-live (only if it survives paper) | Separate decision — out of scope here |

## 9. Open Decisions (need Mr. Mike's sign-off)

| # | Decision | Options | Recommendation |
|---|---|---|---|
| 1 | Repo name / visibility | — | **Settled: patternScanner, public** |
| 2 | Survivorship handling | (a) historical constituents, (b) current + documented | (b) for v1 |
| 3 | Exit horizon N | 5 / 10 / 20 bars | 10 |
| 4 | Round-trip cost | 0.05% / 0.15% / 0.30% | 0.15% |
| 5 | History window | 1995+ / 2000+ / 2005+ | 2000–2025 |
| 6 | Shapes A/B/C definitions | as written / revise | as written |

## 10. Lessons Imported from BreakoutBot

| Trading concept | BreakoutBot precedent |
|---|---|
| Backtest ≠ live | L-007: custom engine → ALE, 99.1% drop |
| Calibrate before claiming | F-001: dead-baseline calibration |
| Small samples prove nothing | Rule 13 |
| Point estimates need intervals | L-014: bootstrap CIs |
| Trust only same-source data | Rule 12 |
| Pre-registration | New — the trading version of "never move the finish line" |
| Every claim traceable to raw data | EXPERIMENTS.md discipline |
