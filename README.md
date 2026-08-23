# patternScanner

Detect predefined chart shapes on US equity daily bars and measure, honestly,
whether they predict forward returns better than chance.

**Status:** Phase 4 — verdicts written back to the ledger 2026-08-21.
Seventeen pre-registered campaigns are measured. **Shapes A/B/C** (pre-reg #2):
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
**Stop placement** (pre-reg #14, I-X-05 — "the market shouldn't take out
that prior extreme low", measured 2026-08-17): **F1-BULL EDGE** — the
divergence's prior extreme low (Low[t2]) is breached within N=10 in
47.54% of 16,984 OOS events vs 52.99% random / 53.28% same-ticker
(excess −5.46pp, CI −6.47..−4.44, and −5.71pp, CI −6.75..−4.66, p=0.000
both) — the claim's "shouldn't" is supported; F2-BULL EDGE vs OS
crossings (−28.56pp, CI −29.58..−27.58). **The §5 survivorship gate
PASSES** — the first EDGE to survive the historical-constituent re-check
(n=9,384, breach 50.53% vs 55.37%/56.20%, excess −4.82pp/−5.70pp,
p=0.000; all anchors PASSED). Phase-5 trigger-check held with the
surviving evidence: **not triggered** — the finding is a risk-placement
property (where the obvious stop sits and how often it is hit), not a
tradeable signal, and the divergence events were already gated null on
mean returns. A recorded data-state deviation (the frozen #10 event
record is not regenerable on the 08-16-restated bars; quantified, drift
bound ~1.9e-4, verdicts not drift-sensitive) is documented in the
results JSON `anchor` block. **Price-tier** (pre-reg #16,
I-D-01/I-X-06/A-04 — "my sweet spot is $2–5", measured 2026-08-19):
**F1 EDGE × 4 + the §5 gate PASSES** — within the S&P 600 small-cap
universe lower-priced tiers earn better N=10 forward returns after cost,
perfectly monotone across five bands (lt2 +6.10% > 2-5 +1.47% > 5-10
+0.53% > 10-20 +0.32% > gt20 −0.08%, name-day collapsed); the sharpest
form is the same-name control (F1d): the *same ticker* earns +7.9% on
its <$10 bar-dates vs +0.1% on its own >$20 bar-dates. The gate on the
frozen current constituents (OOS 2016–2025) confirms in the reverse
direction (the primary is delisting-aware, the gate is the live index):
+2.33/+1.05/+0.50/+3.99%. The long-term-fall claim (I-X-06) is
**contradicted**: the 2021 low-priced cohort *outpaced* the high-priced
cohort on 3-year cumulative returns (+39.5% vs +6.0%, F2b FADE; gap
accruing with horizon, 1y +5.0% → 4y +42.2%), with no excess index-exit
rate (F2a NO EDGE). Phase-5 trigger-check held: **NOT TRIGGERED** — a
monotone *relative* tiering effect with modest absolute size (+1.1% per
10-bar window after cost on the cheapest band) and no tradeable
construction; the literal penny-stock population (<$2) is a thin slice,
reported descriptively (+6.10%, 33 names). **C-exit comparison** (pre-reg
#17, C-01/C-03/C-04 — indicator exits vs fixed-2R on the same entries,
measured 2026-08-19): **the exits are well-timed; the system isn't.**
F1 system contrast NO EDGE (pooled −0.0215R, p=0.202) with Shape A
**FADE** (−0.0777R, both windows) — the indicator arm loses to the
corpus's own fixed-2R exits on A and breaks even elsewhere. F2 S1
(HV-red) / S2 (VWAP-break) timing **EDGE** in the primary (p 0.014/0.006
— post-exit 10-bar returns ~0.43/0.46pp below same-ticker random
baselines) but **fail the §5 gate** (union p 0.028/0.016) and do not
reproduce under the verification's fresh-seed baseline redraw (p
0.126/0.024). F3 q90/q95 **FADE**, q99 **EDGE and survives the gate**
(+0.6425, CI +0.4463..+0.8897) — the "cap losers, not winners"
asymmetry holds only at the extreme tail. Phase-5 trigger-check held:
**NOT TRIGGERED** — the surviving EDGE is a tail-quantile contrast of a
construction that nets negative as a system; the tail cannot be selected
ex ante. **I-F-03 market-trend** (pre-reg #18, I-F-03 — "stocks will trend
with the overall market unless they have a reason not to", measured
2026-08-21): **half-true.** F1 baseline **EDGE** — per-stock daily
correlation with SPY +0.4601 (CI +0.4521..+0.4681, p=0.000), uniformly
positive across 598 of 599 stocks, and the §5 gate passes (union n=703,
+0.4455). The "reason not to" half splits by catalyst proxy: volume-spike
days decouple as claimed (F2-vol −0.2253, p=0.000; gate passes), but gap
days show the OPPOSITE — F2-gap **FADE** (+0.0968, correlation HIGHER on
gap days), and F3-gap NO EDGE (p=0.488). F3-vol's down-day edge (+0.0021)
does **not** mean "running when the markets tanking": the pre-declared S8
control shows the up-day contrast (+0.0063) *exceeds* the down-day one
(down−up −0.0042, p=0.000) — the effect is the general up-bias of
catalyst stocks, not a market-specific run. Phase-5 trigger-check held:
**NOT TRIGGERED** — a structural co-movement campaign with no forward
returns; Phase 5 cannot fire by construction. **The daily track is now
exhausted** — the remaining untested ledger claims all need intraday data.
Phase 5 remains **not triggered** after seventeen campaigns.

**Intraday track (live since 2026-08-19):** a forward-accumulated 1-minute
archive of the live S&P 600 is capturing the data the remaining untested
ledger claims need (they are stated on 1-minute charts — B-01 micro pullback,
I-B-01, I-C-02/03/04, 1-min MACD, F-01/F-02 time-of-day, I-E-02). Pre-regs
#15 (B-01), #19 (entry timing: reversal new-high / pullback-count /
second-confirmation), #20 (intraday exits: breakeven-trail + sell-half, the
9MA→20MA→VWAP ladder, flat-out), #21 (the two-filter veto on 1-min bars) and
#22 (intraday regime: morning window, pre-market cleanliness) are frozen,
each with the shared §5 floor (≥ 20 full-universe bar-dates ≥ 2026-08-19)
before any measurement; the measurement tools are frozen too (implementation
freeze 2026-08-21, fixed-point FROZEN_SHA in each §8 block). **Pre-reg #23
(the paper loop, frozen 2026-08-23)** runs the five frozen definitions on
each live tape day as it lands and logs fills/slippage vs. the recorded bar,
the gate decisions, and a daily journal — the L-007 backtest-live gap feed for
the §5-gated comparison (see [data/paper/README.md](data/paper/README.md)).
Nightly pull (22:05) + paper loop (22:30) + push (23:00) run under Task
Scheduler. See [data/intraday/README.md](data/intraday/README.md) and
[INTRAday_OPERATIONS.md](INTRAday_OPERATIONS.md).
Verdicts:
[CLAIMS_LEDGER §B.5 / §D.5 / §E.5 / §D.6 / §D.7 / §E.6 / §E.7 / §I.5 / §I.6 / §I.7 / §I.8 / §I.9 / §I.10 / §I.11 / §I.13 / §I.14 / §I.15](CLAIMS_LEDGER.md);
reports:
`data/cache/measure_report.md`, `data/cache/pillar_measure_report.md`,
`data/cache/veto_measure_report.md`, `data/cache/momentum_measure_report.md`,
`data/cache/decade_measure_report.md`, `data/cache/e03_measure_report.md`,
`data/cache/e02_measure_report.md`, `data/cache/rv_measure_report.md`,
`data/cache/rsi_measure_report.md`,
`data/cache/divergence_measure_report.md`,
`data/cache/bigmove_measure_report.md`,
`data/cache/speed_measure_report.md`,
`data/cache/divergence_hist_measure_report.md`,
`data/cache/stop_placement_measure_report.md`,
`data/cache/stop_placement_gate_measure_report.md`,
`data/cache/pricetier_measure_report.md`,
`data/cache/pricetier_gate_measure_report.md`,
`data/cache/cexit_measure_report.md`,
`data/cache/cexit_gate_measure_report.md`,
`data/cache/if03_measure_report.md`,
`data/cache/if03_gate_measure_report.md`.
Next candidates: the remaining untested ledger items all need intraday data
— the **intraday track** now accumulates nightly. Pre-regs **#15, #19–#23
are frozen** (2026-08-19 / 2026-08-21 / 2026-08-23) with the shared §5 floor
(≥ 20 full-universe bar-dates ≥ 2026-08-19, ~mid-September) before any
measurement; each awaits the floor (see
[data/intraday/README.md](data/intraday/README.md) and
[INTRAday_OPERATIONS.md](INTRAday_OPERATIONS.md)).

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
  2026-08-16, **measured 2026-08-17: F1-BULL EDGE on the primary AND the
  §5 gate PASSES** — the first EDGE to survive the historical-constituent
  re-check (§I.11); Phase-5 trigger-check held: NOT TRIGGERED (a
  risk-placement property, not a tradeable signal). Verdicts return to
  the ledger. Pre-registration #15: the B-01 micro-pullback claim on
  1-minute bars ("the first candle that makes a new high versus the high
  of the previous candle"; secondary rows B-02/I-E-02; intraday track),
  frozen 2026-08-19 — measurement awaits the archive's §5 floor (≥ 20
  full-universe bar-dates ≥ 2026-08-19, ~mid-September). Pre-registration
  #16: the price-tier family (I-D-01 "$2–5 sweet spot" + I-X-06
  penny/small-cap long-term fall, A-04 cross-ref), frozen 2026-08-19,
  **measured 2026-08-19: F1 EDGE × 4 with the §5 gate PASSING; F2b FADE;
  Phase-5 trigger-check NOT TRIGGERED (§I.13)**. Pre-registration #17:
  the C-exit comparison (C-01/C-03/C-04 — indicator exits vs fixed-2R on
  the same entries), frozen 2026-08-19, **measured 2026-08-19: F1 NO EDGE
  / FADE-A; F2 S1/S2 timing EDGEs primary-only (fail the §5 gate, fragile
  under fresh seeds); F3 q99 EDGE survives the gate; NOT TRIGGERED
  (§I.14)**. Pre-registration #18: the I-F-03 market-trend family ("stocks
  will trend with the overall market unless they have a reason not to"),
  frozen 2026-08-21, **measured 2026-08-21: F1 EDGE (gate passes); F2-gap
  FADE, F2-vol EDGE (gate passes); F3-gap NO EDGE, F3-vol EDGE (does not
  mean "running when the markets tanking" — the S8 up-day control shows the
  effect is a general up-bias); NOT TRIGGERED (§I.15)** — the final
  testable-daily campaign. Pre-registration #19: the intraday entry-timing
  family (I-B-02 reversal new-high long+short, B-03/I-B-01 pullback-count,
  B-05 second-confirmation), frozen 2026-08-21, awaits the shared §5 floor.
  Pre-registration #20: the intraday exit rules (I-C-02 breakeven-trail +
  sell-half, I-C-03 9MA→20MA→VWAP target ladder, I-C-04 flat-out, on the
  pre-reg #15 B-01 entry set), frozen 2026-08-21, awaits the shared §5
  floor. Pre-registration #21: the two-filter pre-entry veto on 1-min bars
  (E-01/E-04 — MACD negative + high-volume red candle), frozen 2026-08-21,
  awaits the shared §5 floor. Pre-registration #22: the intraday regime
  (I-B-05 morning-is-best volatility/liquidity buckets, F-01/F-02
  pre-market cleanliness), frozen 2026-08-21, awaits the shared §5 floor.
  Pre-registration #23: the paper loop as a live-execution study (runs the
  five frozen intraday definitions on each live tape day as it lands; logs
  fills/slippage vs. the recorded bar, gate decisions, and a daily journal —
  the L-007 backtest-live gap feed for the §5-gated comparison), frozen
  2026-08-23, awaits the shared §5 floor.
- [data/README.md](data/README.md) — Phase 1 data: frozen S&P 600 snapshot,
  per-ticker bars, QA report, documented gaps and artifacts.
- [data/intraday/README.md](data/intraday/README.md) — the intraday track:
  forward-accumulated 1-minute archive of the live S&P 600 (no survivorship
  bias by construction), append-only ledger discipline, nightly pull + push
  (pre-regs #15, #19–#22 frozen, awaiting the §5 floor).
- [INTRAday_OPERATIONS.md](INTRAday_OPERATIONS.md) — intraday runbook: what
  runs nightly, monitoring, failure modes and recovery, re-creating the
  scheduled tasks.
- [transcripts/warrior-trading/_INDEX.md](transcripts/warrior-trading/_INDEX.md) —
  reference corpus of a day-trading "expert" education series (fan-curated
  playlist), for scrutiny and technique reference. Transcript files are
  copyrighted and kept local (gitignored); only the index is tracked.
- [transcripts/ultimate-guide/_INDEX.md](transcripts/ultimate-guide/_INDEX.md) —
  the same expert's official 3-hour "Ultimate Day Trading Guide" from his own
  channel — a separate course, not a compilation of the playlist (verified via
  n-gram overlap); the 2026-08-18 course-drift analysis ([CLAIMS_LEDGER
  §I.12](CLAIMS_LEDGER.md)) shows the *rules* are the same strategy a decade
  apart (8 of 16 families SAME, incl. two near-verbatim), with narrowed/
  dropped/added layers and one escalated accuracy claim.
- Not investment advice. No execution, no real money.
- Methodology lineage: [BreakoutBot](https://github.com/mharrell/BreakoutBot) —
  the backtest is the custom engine; live trading is the ALE. Calibrate before
  you claim.
