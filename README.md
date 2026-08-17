# patternScanner

Detect predefined chart shapes on US equity daily bars and measure, honestly,
whether they predict forward returns better than chance.

**Status:** Phase 4 — verdicts written back to the ledger 2026-08-16.
Thirteen pre-registered campaigns are measured. **Shapes A/B/C** (pre-reg #2):
all **NO EDGE** out-of-sample (2016–2025, N=10, Holm-corrected; Shape B
significantly *below* its baselines). **Pillars H1–H3** (pre-reg #1):
**H3 NO EDGE** at the frozen N=1 — the day-paired rank-1-vs-rank-2–10 claim
test is precisely null (+0.00pp, p=0.99); **H1/H2 INCONCLUSIVE by count
floor** — the AND-combined screens fired 7/6 times in 26 years (0 in OOS),
untestable as daily-bar filters. **Two-filter veto** (pre-reg #3,
E-01/E-04): **NO EDGE in both verdict families, all three shapes** — the
veto (MACD ≥ 0 and no high-volume red candle) is a trade-count reducer,
not an edge enhancer; on A/C it cuts the better trades. **Momentum horizon**
(pre-reg #4, N=20): Family 1 (absolute) **NO EDGE × 3** — selection adds
nothing over same-ticker buy-and-hold; Family 2 (paired continuation,
N=20 vs N=5) **EDGE × 3** — after these signals the entry names kept
drifting up 5→20 bars (the project's first EDGE verdicts; the pattern-vs-
chance trigger test is Family 1, still null). **Per-decade drift**
(pre-reg #5): both families **NO EDGE × 3** — the late-era strengthening
is real vs random entries (p=0.008/0.002) but never clears the same-ticker
control; the drift is late-era beta, not selection edge. **E-03**
(pre-reg #6, MACD-cross breakout rejection): **FADE EDGE × 2 on Shape B**
— the project's first verdicts in a claim's favor. Bear-day conditioning
(F2): crossed-B breakouts −0.95% vs not-crossed +0.70% (excess −1.62pp,
p=0.012); avoidance bar (F3): −0.53pp vs random (p=0.014) and −0.57pp vs
same-ticker (p=0.008); NO EDGE × 6, INCONCLUSIVE × 1. The effect lives
entirely in bear days, exactly as claimed, and peaks in 2022 — the year he
says he learned it. It is a **fade signal**: it identifies B-breakouts
worth *avoiding*, it does not make any pattern profitable. **E-02**
(pre-reg #7, "80% chance of this working"): **REJECTED × 3** — the
literal 80% is falsified on all three shapes: veto-pass win rates are
**0.4869 / 0.4899 / 0.5286** (one-sided p ≤ 2e-24, CI upper ≤ 0.58); even
his own softened "60% is enough to be profitable" floor fails at α=0.05
(C p=0.009); **NO EDGE × 3** vs chance, and on A/B the pass set wins
*significantly below* random entries (p=0.004/<0.001). The round-number
claim failed honestly, as pre-registered. **High relative volume**
(pre-reg #8, I-D-07/I-E-01 — the first warrior-corpus claim measured,
2026-08-14): **NO EDGE × 3, INCONCLUSIVE × 3** — F1-A/B NO EDGE (high-RV
subsets beat neither chance nor same-ticker; excess vs same-ticker
−0.22/−0.37pp, p_input 0.204/0.548), F1-C INCONCLUSIVE (46 high-RV OOS
< 100 floor); F2-B NO EDGE (high +0.24% vs low −0.05%, contrast +0.30pp,
p=0.302 — the claimed direction, never significant), F2-C INCONCLUSIVE,
F2-A INCONCLUSIVE by construction (every A detection is high-RV — the
detector's V=2.0). "Pattern trading only works on high-relative-volume
stocks" is null in absolute terms; the differential whisper exists but
never clears. **RSI 70/30** (pre-reg #9, I-X-01 — Trading 212, measured
2026-08-14): **EDGE × 3 at the state level** — the first campaign to
confirm a claim's directional structure. F1-OB (RSI>70 ⇒ pullback):
n=201,419, excess vs random −0.26pp and vs same-ticker −0.30pp, p<0.001,
Holm-rejected; F1-OS (RSI<30 ⇒ bounce): n=150,236, excess +0.12pp/+0.14pp,
p<0.001, Holm-rejected; F2 (OS−OB): +0.38pp (CI +0.31..+0.45, p<0.001).
The size is small (+0.14pp per 10-bar trade after cost) and the
pre-declared event-level correction is null (OS p=0.166), the parameter
neighborhood is fragile (80/20 and period 10 fail), so the **Phase-5
trigger-check conversation was held and did not trigger** — the edge is a
real directional tendency, not a tradeable one. **RSI divergence**
(pre-reg #10, I-X-02/03/04 — Trading 212, measured 2026-08-14): **split
verdict — the project's first event-level absolute EDGE, on the bullish
leg.** F1-BULL (price lower low + RSI higher low ⇒ bounce): n=16,985 OOS,
mean +0.80%, win 54.12%, excess vs random +0.31pp and vs same-ticker
+0.34pp (CI +0.15..+0.53, p=0.002), Holm-rejected; robust across every
structural sensitivity (k=3/5, period 14, min-sep 10, extreme-gated:
+0.23..+0.50pp) and positive in 9/10 OOS years. F1-BEAR (price higher
high + RSI lower high ⇒ pullback): **NO EDGE** (n=20,800, p=0.662). F2
(reliability vs the 70/30 crossings): BULL **EDGE × 2** (mean +0.18pp,
hit +1.50pp), BEAR-mean **FADE** (+0.21pp — *less* reliable, the opposite
direction), BEAR-hit NO EDGE. Frequency: 37,929 divergences vs 124,298
crossings, ratio 0.3051 (CI 0.3022..0.3081) — "a lot less common"
confirmed. The **Phase-5 trigger-check conversation was held (F1-BULL
EDGE fired the pre-registered trigger) and did not trigger** — the brief
§5 survivorship gate (current-constituent universe) requires a
historical-constituent re-check before any positive result is trusted;
size is +0.34pp per 10-bar trade on ~2.8 events per ticker per year; and
the claim is half-confirmed (bearish leg null/faded). **The re-check was
run (pre-reg #13, the brief §5 gate, measured 2026-08-15, verified
2026-08-16): the gate FAILS.** On the historical-constituent union (904
names — 5 annual S&P 600 snapshots 2021–2025 incl. ~330 delisted, OOS
2022–2025, n=9,384) F1-BULL is **NO EDGE** (mean +0.59%, +0.49pp vs
same-ticker, CI −0.15..+0.87, p=0.072, p_input 0.072) — the direction
persists (all four OOS years positive) but no longer clears chance; the
EDGE is corrected to the survivorship-resilient record and the family is
closed. F1-BEAR NO EDGE holds. F2-BEAR-hit **EDGE** (hit rate −1.35pp vs
overbought crossings, p=0.012 — "more reliable" on the bearish side on
the corrected window); frequency ratio 0.3012 (CI 0.2972..0.3052) holds.
Data limitation per the pre-registered §6: 199 of 904 names are purged
from Yahoo entirely (0 of them current members), measured on 706,
flagged not substituted. **Big-move
correction** (pre-reg #11, I-F-01 — 2015 intraday classroom tapes,
measured 2026-08-14/15): **split verdict — the project's second
event-level absolute EDGE, on the UP (correction) leg, as a
negative-return finding.** F1-UP (≥3-ATR up-moves ⇒ below-baseline
10-bar returns): n=35,908 OOS, mean +0.03% after cost, excess vs random
−0.46pp and vs same-ticker −0.48pp (CI −0.61..−0.36, p<0.001),
Holm-rejected — "corrected" holds in the relative sense. F1-DOWN ("what
goes down must come back up"): **NO EDGE** (n=29,039, p=0.950); at τ=5
extreme down-moves *underperform* their baselines (−1.36pp, p<0.001).
F2 (the ledger's literal reading, "retrace ≥ half within 5–10
sessions"): **FADE × 2** — big moves cross their own midpoint within 10
sessions 19.6% vs 32.3% (UP) and 22.5% vs 38.0% (DOWN) on typical bars
(−12.77pp / −15.53pp, both Holm-rejected) — the literal retracement
claim is falsified; the DOWN bounce exists only for weak moves (τ=2
+0.24pp, p<0.001, vanishing at τ=3). The Phase-5 trigger did not fire
(only an F1-DOWN EDGE can trigger; it is null). **Speed asymmetry**
(pre-reg #12, I-F-02 — the bulls-take-the-stairs claim, measured
2026-08-15): **split verdict — A1 falsified in the opposite direction,
A2 confirmed.** F1-UP FADE (up-bars larger than typical: +0.06pp
excess, Holm-rejected), F1-DOWN FADE (knife-edge: −0.00004, p=0.050
exactly at the gate — treat as NO EDGE), F2 FADE (DOWN−UP −0.06pp,
Holm-rejected) — at daily per-bar resolution up-bars average ~6bp
larger than down-bars, the "window" absent (top-|r| decile not
down-concentrated, −0.25pp), stable across mean/median/candle-sign/
per-ticker (75.6% of tickers negative)/IS/per-year (9/10 years). F4
EDGE (A2): of the 35,997 frozen pre-reg #11 UP events, the 30.9% that
retrace ≥ half within 10 bars do so faster than the move (+0.40pp/bar,
Holm-rejected), concentrated in N≤5, robust to τ=2/5; swing-scale S6
corroborates the claim across bars (down-swings faster, k=2/3/5 all
p<0.001) — the "window" is a multi-bar property, not a per-bar one. No
forward returns measured; the Phase-5 trigger cannot fire from this
campaign by construction. The **RSI-divergence historical-constituent
re-check** (pre-reg #13, the brief §5 survivorship gate, measured
2026-08-15): **the gate FAILS** — F1-BULL NO EDGE on the 904-name
historical union (2022–2025, n=9,384, p_input 0.072), the EDGE corrected
to the survivorship-resilient record, the family closed with the re-check
as definitive; F2-BEAR-hit EDGE (re-recorded); frequency 0.3012 holds.
Phase 5 remains **not triggered** after thirteen campaigns.
Verdicts:
[CLAIMS_LEDGER §B.5 / §D.5 / §E.5 / §D.6 / §D.7 / §E.6 / §E.7 / §I.5 / §I.6 / §I.7 / §I.8 / §I.9 / §I.10](CLAIMS_LEDGER.md);
reports:
`data/cache/measure_report.md`, `data/cache/pillar_measure_report.md`,
`data/cache/veto_measure_report.md`, `data/cache/momentum_measure_report.md`,
`data/cache/decade_measure_report.md`, `data/cache/e03_measure_report.md`,
`data/cache/e02_measure_report.md`, `data/cache/rv_measure_report.md`,
`data/cache/rsi_measure_report.md`,
`data/cache/divergence_measure_report.md`,
`data/cache/bigmove_measure_report.md`,
`data/cache/speed_measure_report.md`,
`data/cache/divergence_hist_measure_report.md`.
Next candidates: pre-registration #14 (the I-X-05 stop-placement claim —
"the market shouldn't take out that prior extreme low", measured as the
breach rate of the divergence's lower low within N=10, with the §5
survivorship gate pre-registered within the campaign) is **frozen
2026-08-16, measurement pending**. After it, the top remaining candidate
is the I-X-06/I-D-01 price-tier family (sub-$5 cohorts' forward returns —
needs a small-cap universe beyond the S&P 600). The remaining untested
ledger items need intraday data.

- [DESIGN_BRIEF.md](DESIGN_BRIEF.md) — scope, shape definitions, measurement
  protocol, bias checklist, phases.
- [CLAIMS_LEDGER.md](CLAIMS_LEDGER.md) — every testable claim from the
  reference corpus, as stated and timestamped, with a status and a
  pre-registration priority order. Claims are hypotheses, not evidence.
- [PREREGISTRATION.md](PREREGISTRATION.md) — pre-registration #1: the
  "five pillars" stock-selection claim (H1–H3), frozen 2026-08-13 before any
  measurement. Pre-registration #2: shape detectors A/B/C (parameters,
  horizon N=10, OHLC handling), frozen 2026-08-13 before any measurement.
  Pre-registration #3: the two-filter veto (E-01/E-04), frozen 2026-08-14.
  Pre-registration #4: the momentum horizon follow-up (N=20 primary),
  frozen 2026-08-14. Pre-registration #5: the per-decade drift
  decomposition, frozen 2026-08-14. Pre-registration #6: the E-03
  MACD-cross breakout-rejection claim (bearish signal-line cross within
  L=20 bars, regime SPY < SMA200, three verdict families), frozen
  2026-08-14. Pre-registration #7: the E-02 "80% chance of this working"
  claim (win rate ≥ 0.80 on the veto-pass setup; exact binomial claim
  test + win-rate-edge family), frozen 2026-08-14. Pre-registration #8:
  the high-relative-volume conditioning claim (I-D-07/I-E-01 — RV ≥ 2.0
  subsets vs below on the frozen detections; absolute + contrast
  families), frozen 2026-08-14. Pre-registration #9: the RSI 70/30
  reversal-bias claim (I-X-01 — simple-average RSI as taught in the
  video, period 14, thresholds 70/30, state-based OB/OS legs; directional
  F1 families + F2 reversal-symmetry contrast), frozen 2026-08-14.
  Pre-registration #10: the RSI divergence frequency + reliability claims
  (I-X-02/03/04 — simple-average RSI period 10 as taught in the video,
  strict k=2 fractal swings on Low/High, confirmation-bar timing at t2+k
  (no look-ahead), divergence vs 70/30 crossings per leg on mean return
  and hit rate; frequency ratio as a measurement, not a verdict family),
  frozen 2026-08-14. Pre-registration #11: the big-move correction claim
  (I-F-01 — a big-move event at bar t iff |close_t − close_{t−L}| ≥ 3×ATR_t,
  L=10, excursion-first event-level definition; ATR_t = the simple mean of
  the 14 true ranges ending at t, pre-registered because the corpus teaches
  no ATR formula; F1 absolute per leg + F2 literal retracement-contrast
  families), frozen 2026-08-14. Pre-registration #12: the
  bulls-take-the-stairs speed-asymmetry claim (I-F-02 — A1 per-bar
  move-size asymmetry via F1 absolute-per-leg + F2 DOWN−UP contrast on
  |close-to-close| bars; A2 reversal-speed via F4 on the frozen pre-reg
  #11 UP events with a midpoint first-crossing rule, N=10; no forward
  returns measured — the claim is about bar geometry, so Phase 5 is not
  implicated), frozen 2026-08-15. Pre-registration #13: the brief §5
  historical-constituent re-check of the pre-reg #10 F1-BULL EDGE (a new
  data artifact — the union of 5 annual snapshots of the Wikipedia *List
  of S&P 600 companies* revision history, 904 names incl. ~330
  delisted/removed; the frozen pre-reg #10 measurement code byte-identical,
  runtime-rebound to the historical universe with OOS 2022–2025; the §5
  gate: F1-BULL EDGE survives ⇒ PASSED, NO EDGE/FADE ⇒ FAILS and the
  family is closed), frozen 2026-08-15, **measured: gate FAILS, family
  closed (§I.10)**. Pre-registration #14: the I-X-05 stop-placement claim
  (bullish divergence — "the market shouldn't take out that prior extreme
  low": breach rate of the divergence's lower low Low[t2] within N=10
  after the frozen pre-reg #10 BULL event set, vs fractal-low
  confirmation-bar baselines and vs OS crossings; the §5 survivorship gate
  (historical-union re-run) pre-registered within the campaign, frozen
  2026-08-16, measurement pending. Verdicts return to the ledger.
- [data/README.md](data/README.md) — Phase 1 data: frozen S&P 600 snapshot,
  per-ticker bars, QA report, documented gaps and artifacts.
- [transcripts/warrior-trading/_INDEX.md](transcripts/warrior-trading/_INDEX.md) —
  reference corpus of a day-trading "expert" education series (fan-curated
  playlist), for scrutiny and technique reference. Transcript files are
  copyrighted and kept local (gitignored); only the index is tracked.
- [transcripts/ultimate-guide/_INDEX.md](transcripts/ultimate-guide/_INDEX.md) —
  the same expert's official 3-hour "Ultimate Day Trading Guide" from his own
  channel — a separate course, not a compilation of the playlist (verified via
  n-gram overlap).
- Not investment advice. No execution, no real money.
- Methodology lineage: [BreakoutBot](https://github.com/mharrell/BreakoutBot) —
  the backtest is the custom engine; live trading is the ALE. Calibrate before
  you claim.
