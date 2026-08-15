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
| 3 | Measurement + baselines | Full per-shape report — **done 2026-08-13** (see data/cache/measure_report.md; all three shapes: NO EDGE, OOS). Pillars (pre-reg #1) measured same day (data/cache/pillar_measure_report.md): H3 NO EDGE; H1/H2 INCONCLUSIVE by count floor. Two-filter veto (pre-reg #3) measured 2026-08-14 (data/cache/veto_measure_report.md): NO EDGE in both verdict families, all three shapes. Momentum horizon (pre-reg #4) measured 2026-08-14 (data/cache/momentum_measure_report.md): F1 NO EDGE × 3, F2 EDGE × 3. Per-decade drift (pre-reg #5) measured 2026-08-14 (data/cache/decade_measure_report.md): both families NO EDGE × 3 — the drift is late-era beta, not selection edge. E-03 (pre-reg #6) measured 2026-08-14 (data/cache/e03_measure_report.md): FADE EDGE × 2 on Shape B, NO EDGE × 6, INCONCLUSIVE × 1 — the first verdicts in a claim's favor, in the regime the claim names. E-02 (pre-reg #7) measured 2026-08-14 (data/cache/e02_measure_report.md): the "80% chance" claim REJECTED × 3 (win rates 48.7–52.9%; CI upper ≤ 0.58; even the 0.60 softening fails) and NO EDGE × 3 vs chance — A/B win *below* random. High-RV conditioning (pre-reg #8) measured 2026-08-14 (data/cache/rv_measure_report.md): F1-A/B NO EDGE, F1-C INCONCLUSIVE (count floor); F2-B NO EDGE (contrast +0.30pp, p=0.302), F2-C INCONCLUSIVE, F2-A INCONCLUSIVE by construction (every A detection is high-RV — the detector's V=2.0). The first warrior-corpus claim, null in absolute terms. RSI 70/30 (pre-reg #9) measured 2026-08-14 (data/cache/rsi_measure_report.md): **EDGE × 3 at the state level** — F1-OB (overbought below both baselines: −0.30pp vs same-ticker, p<0.001), F1-OS (oversold above both: +0.14pp vs same-ticker, p<0.001), F2 contrast OS−OB +0.38pp (p<0.001) — the first campaign to confirm a claim's directional structure; the pre-declared event-level (crossing) view is null (OS p=0.166); the Phase-5 trigger-check conversation was held and did not trigger. RSI divergence (pre-reg #10) measured 2026-08-14 (data/cache/divergence_measure_report.md): **F1-BULL EDGE** (the project's first event-level absolute EDGE — n=16,985 OOS, +0.34pp vs same-ticker, Holm-rejected, robust across all structural sensitivities, 9/10 OOS years positive), F1-BEAR NO EDGE, F2 BULL EDGE × 2 / BEAR-mean FADE / BEAR-hit NO EDGE, frequency ratio 0.3051 — the frequency half confirmed, the reliability claim half right. Big-move correction (pre-reg #11) measured 2026-08-14/15 (data/cache/bigmove_measure_report.md): F1-UP EDGE (relative correction — big up-moves below both baselines, Holm-rejected, mean +0.03% after cost), F1-DOWN NO EDGE (p=0.950), F2 FADE × 2 (big moves retrace half within N *less* often than typical bars: −12.77pp/−15.53pp — the ledger's literal retracement claim falsified), frequency reported. Speed asymmetry (pre-reg #12) measured 2026-08-15 (data/cache/speed_measure_report.md): bar-geometry campaign — no forward returns (the engine's measure_returns NOT invoked, per pre-reg §3); A1 FADE × 3 (per-bar asymmetry inverted — up-bars ~6bp larger than down-bars: F1-UP FADE, F1-DOWN FADE knife-edge, F2 FADE), A2 EDGE (F4: big up-moves' retracements outpace the moves — n=35,997, +0.40pp/bar) |
| 4 | Verdicts | Per shape: edge / no edge / inconclusive — **done 2026-08-13**: A/B/C all NO EDGE on OOS; verdicts written back to CLAIMS_LEDGER §B.5. Pillar verdicts H1–H3 written back to §D.5 (H3 rejected, H1/H2 inconclusive). Veto verdicts (E-01/E-04) written back to §E.5 2026-08-14: both families NO EDGE — the veto reduces trade count, not edge. Momentum verdicts (pre-reg #4) written back to §D.6 2026-08-14: F1 NO EDGE × 3 — selection adds nothing over same-ticker B&H; F2 EDGE × 3 — continuation drift of the entry names (first EDGE verdicts; interpretation in §D.6 — the pattern-vs-chance trigger test is F1, still null, Phase 5 not triggered). Per-decade verdicts (pre-reg #5) written back to §D.7 2026-08-14: both families NO EDGE × 3 — late-era strengthening real vs random (p=0.008/0.002) but never clears same-ticker; late-era beta, Phase 5 not triggered. E-03 verdicts (pre-reg #6) written back to §E.6 2026-08-14: **FADE EDGE × 2 on Shape B** (bear-days excess −1.62pp, p=0.012; avoidance bar p_input 0.014) — the first verdicts in a claim's favor; a fade signal — it says *don't take* the crossed-B trade, it does not make any pattern profitable; Phase 5 still not triggered. E-02 verdicts (pre-reg #7) written back to §E.7 2026-08-14: the "80% chance of this working" claim **REJECTED × 3** (pass-set win rates 48.7–52.9%, one-sided p ≤ 2e-24, CI upper ≤ 0.58; his own 60% floor also fails, C p=0.009) and **NO EDGE × 3** vs chance (A/B win below random, p=0.004/<0.001) — a round-number claim, falsified at astronomical significance; Phase 5 still not triggered. RV-conditioning verdicts (pre-reg #8) written back to §I.5 2026-08-14: **NO EDGE × 3, INCONCLUSIVE × 3** — F1-A/B NO EDGE (high-RV subsets beat neither chance nor same-ticker; excess vs same-ticker −0.22/−0.37pp), F1-C/F2-C INCONCLUSIVE (count floor), F2-B NO EDGE (contrast +0.30pp, p=0.302 — the claimed direction, never significant), F2-A INCONCLUSIVE by construction; "pattern trading only works on high-relative-volume stocks" is null in absolute terms; Phase 5 still not triggered. RSI 70/30 verdicts (pre-reg #9) written back to §I.6 2026-08-14: **EDGE × 3 at the state level** — F1-OB (pullback, as claimed), F1-OS (bounce, as claimed), F2 (reversal symmetry) — the first verdicts in a claim's absolute direction, all Holm-rejected at p<0.001; the Phase-5 trigger-check conversation was held (F1-OS EDGE is the sole pre-registered trigger, pre-reg #9 §4): **NOT TRIGGERED** — the state-level significance is overlap-inflated (pre-declared event-level correction p=0.166), the parameter neighborhood is fragile (80/20 and period-10 fail), size is +0.14pp per 10-bar trade after cost; Phase 5 still not triggered. RSI-divergence verdicts (pre-reg #10) written back to §I.7 2026-08-14: **F1-BULL EDGE** (the project's first event-level absolute EDGE — n=16,985 OOS, mean +0.80%, +0.34pp vs same-ticker, Holm-rejected, robust across all structural sensitivities, 9/10 OOS years), F1-BEAR NO EDGE (p=0.662), F2 BULL EDGE × 2 (mean +0.18pp, hit +1.50pp vs oversold crossings), F2 BEAR-mean **FADE** (+0.21pp — bearish divergence *less* reliable than overbought crossings, the opposite direction), F2 BEAR-hit NO EDGE; frequency ratio 0.3051 confirms "a lot less common". The Phase-5 trigger-check conversation was held (F1-BULL EDGE fired the sole pre-registered trigger, pre-reg #10 §4): **NOT TRIGGERED** — the brief §5 survivorship gate (any positive result must be re-checked against historical constituents before being trusted) is unmet and is the explicit path forward; Phase 5 still not triggered. Big-move verdicts (pre-reg #11) written back to §I.8 2026-08-15: **F1-UP EDGE** (the project's second event-level absolute EDGE — n=35,908 OOS, −0.48pp vs same-ticker, Holm-rejected — a *negative-return* finding: relative correction confirmed, mean +0.03% after cost), **F1-DOWN NO EDGE** (p=0.950), **F2 FADE × 2** (retrace-half within N less often than typical bars: −12.77pp/−15.53pp — the literal retracement claim falsified); the Phase-5 trigger did not fire (only an F1-DOWN EDGE can trigger — it is null); Phase 5 still not triggered. Speed-asymmetry verdicts (pre-reg #12) written back to §I.9 2026-08-15: **A1 FADE × 3** (F1-UP FADE, F1-DOWN FADE knife-edge — treat as NO EDGE substantively, F2 FADE — the per-bar asymmetry is inverted: up-bars ~6bp larger), **A2 EDGE** (F4 — retracements of big up-moves outpace the moves, as claimed); Phase 5 not implicated by construction (no forward returns measured in this campaign); Phase 5 still not triggered |
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
