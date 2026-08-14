# Daytrading Pattern Detector — Design Brief v1.0

**Date:** 2026-08-13
**Status:** FINAL — all Section 9 decisions settled (last: row 7, 2026-08-13)
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
| 1 | Data pipeline + universe | Clean 2000–2025 daily bars, documented gaps — **done 2026-08-13** (see data/README.md) |
| 2 | 3 detectors + pre-registered params | Detections reproducible from raw data — **done 2026-08-13** (see data/cache/detections_report.md, PREREGISTRATION #2) |
| 3 | Measurement + baselines | Full per-shape report — **done 2026-08-13** (see data/cache/measure_report.md; all three shapes: NO EDGE, OOS). Pillars (pre-reg #1) measured same day (data/cache/pillar_measure_report.md): H3 NO EDGE; H1/H2 INCONCLUSIVE by count floor. Two-filter veto (pre-reg #3) measured 2026-08-14 (data/cache/veto_measure_report.md): NO EDGE in both verdict families, all three shapes. Momentum horizon (pre-reg #4) measured 2026-08-14 (data/cache/momentum_measure_report.md): F1 NO EDGE × 3, F2 EDGE × 3 |
| 4 | Verdicts | Per shape: edge / no edge / inconclusive — **done 2026-08-13**: A/B/C all NO EDGE on OOS; verdicts written back to CLAIMS_LEDGER §B.5. Pillar verdicts H1–H3 written back to §D.5 (H3 rejected, H1/H2 inconclusive). Veto verdicts (E-01/E-04) written back to §E.5 2026-08-14: both families NO EDGE — the veto reduces trade count, not edge. Momentum verdicts (pre-reg #4) written back to §D.6 2026-08-14: F1 NO EDGE × 3 — selection adds nothing over same-ticker B&H; F2 EDGE × 3 — continuation drift of the entry names (first EDGE verdicts; interpretation in §D.6 — the pattern-vs-chance trigger test is F1, still null, Phase 5 not triggered) |
| 5 | Paper trading (only if a shape clears) | Plumbing verified; backtest-live gap measured (L-007) — **not triggered 2026-08-13: no shape cleared** |
| 6 | Micro-live (only if it survives paper) | Separate decision — out of scope here |

## 9. Open Decisions (need Mr. Mike's sign-off)

| # | Decision | Options | Recommendation |
|---|---|---|---|
| 1 | Repo name / visibility | — | **Settled: patternScanner, public** |
| 2 | Survivorship handling | (a) historical constituents, (b) current + documented | (b) for v1 |
| 3 | Exit horizon N | 5 / 10 / 20 bars | **Settled: 10** (pre-reg #2, 2026-08-13) |
| 4 | Round-trip cost | 0.05% / 0.15% / 0.30% | **Settled: 0.15%** (pre-reg #1 protocol) |
| 5 | History window | 1995+ / 2000+ / 2005+ | **Settled: 2000–2025** (Phase 1 dataset) |
| 6 | Shapes A/B/C definitions | as written / revise | **Settled: as written** (operationalized in detectors.py, pre-reg #2) |
| 7 | Float as filter input (§3 exception) | (a) allow static `floatShares` in the selection filter, (b) drop the float leg | **Settled: (a)** — 2026-08-13. Static `floatShares` retrieved once at universe snapshot (frozen 2026-08-13, 603/603 coverage) is allowed as a screening-filter input for pre-registration #1 H1/H2. Not a per-day feature; not part of shape detection; all other §3 exclusions (news, sentiment, LLM, intraday) stand |

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
