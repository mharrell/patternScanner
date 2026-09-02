# Claims Ledger

Every testable claim extracted from the reference corpus, as stated, with a
timestamp so you can check the source. **Claims are hypotheses, not
evidence.** Nothing here is true because a teacher said it; per
DESIGN_BRIEF.md §6, a claim only counts after it is pre-registered, measured
against calibrated baselines, and survives multiple-testing correction.

**Status values** (per row):
- `candidate` — testable with the data we can get; worth pre-registering.
- `pre-registered` — frozen in PREREGISTRATION.md before any measurement; verdicts return here.
- `partial` — testable only in adapted form (e.g. intraday rule on daily bars).
- `red flag` — suspicious as stated (unverifiable, self-serving, or implausible); treat as advertisement until independently confirmed.
- `out of scope` — not measurable by this project (process, tax, platform claims).
- `todo` — needs a decision (see §8 Open decisions).
- `tested, rejected` — a pre-registered hypothesis that was measured and not
  supported; verdict and numbers in §B.5/§D.5, audit trail in PREREGISTRATION.md.
- `tested, inconclusive` — a pre-registered hypothesis that was measured but
  fell below the ≥100-detection floor (or cannot otherwise support a verdict);
  reported, never spun — verdict in §D.5, audit trail in PREREGISTRATION.md.

## Source

| Field | Value |
|---|---|
| Primary | "The Ultimate Day Trading Guide (Full Training Chapters 1 - 10)" — Ross Cameron (Warrior Trading), official channel, 2025-01-01, 3:06:12 |
| Transcript | `transcripts/ultimate-guide/oxob0x0Xz7s.md` (auto-captions; expect transcription errors — check timestamps against video) |
| Secondary | `transcripts/warrior-trading/` — the fan-curated "Class 1-12" playlist (2015-era classroom footage). **Claim-scanned 2026-08-14** — 53 new rows in §I (incl. third-party channels); 2 videos are not trading content (skipped); the Day Trading Station video is equipment content (nothing claim-worthy). |
| Standing question | Are the two courses the same strategy? (See §8.) Partial qualitative evidence in §I-Notes: the *rules* repeat a decade apart (first-new-high entry, first/second-pullback, 2:1–3:1 R:R, morning-is-best, 60%-is-enough); one flagged tension (breakout-chasing stance). |

The course teaches **intraday momentum trading on 1-min/5-min charts**.
patternScanner operates on **US equity daily bars**. So the closest-to-testable
claims here are the *stock-selection* (scanner) criteria and the *structural*
claims; the *entry* rule (micro pullback) needs intraday data or an adapted
daily-bar version.

---

## A. Performance claims — red flags

These are the self-referential ones: they are the teacher's only evidence
that the strategy "works", and several are not independently verifiable.
None are testable by this project; they are listed so the measurement
protocol has a benchmark to *not* be compared to, and so the claims can be
checked against public records if we ever do a diligence pass.

| # | Time | Claim as stated | Status |
|---|---|---|---|
| A-01 | [07:49–09:36] | Starting account $583.15 (2017) → $100K in 45 days during "the challenge" (2 trades/day) → $335K by December → ~$500K next year → ~$1M the year after → $10M+ during the pandemic. | `red flag` — nothing to measure here, but the trajectory is the claim's rhetorical engine. Public records could partially verify (challenge accounts were posted); not our job. |
| A-02 | [09:00ish] | "Just over $12.3 million of verified trading profits" in 2024; says a third-party accountant audited the accounts. | `red flag` — self-reported, and "verified" is doing a lot of work. Fatal ambiguity: profits in *what* periods, across *which* accounts (personal, Roth, firm)? An accountant's signature is not a research audit. |
| A-03 | [30:45–33:08] | "My accuracy is showing at 66% which is why I'm up $12.3 million" (average winner ≈ average loser, ≈$1,300 each). | `red flag` — if avg win ≈ avg loss, break-even win rate is 50%; 66% over thousands of trades would make the P&L claim *plausibly consistent*, but the accuracy number is unverifiable without the trade log. |
| A-04 | [33:47] | March: $10K month, avg win $700, avg loss $1,100, 61% accuracy; says losses were on stocks >$10, so April he traded $2–10 → $36K month. | `red flag` — same category. Useful as a *testable claim in disguise*: "stocks >$10 were unprofitable for me in March 202X" is a claim about price-tier edge. **Testable core measured (pre-reg #16):** the $2–10 vs >$10 split is **EDGE** (F1b +0.51%, CI 0.37–0.65, p=0.000, §I.13) — the disguised claim survives in relative form on small-caps. |
| A-05 | [06:00] | "A strategy that over the course of 100 trades is giving you profit 60% of the time, 70% of the time, that can be enough to be a very profitable trader." | `out of scope` as stated (true by arithmetic given R:R) — but this is the *only* quantitative claim about how good the strategy needs to be. Note the tension with A-03: 66% accuracy is the claim; 60–70% is the threshold he asserts is enough. |
| A-06 | [01:38:38–01:39:04] | On WKEY (a day when he "finished the day up about $116,000"): "the number one leading percentage gainer in the entire market." | `red flag` — performance anecdote; the *selection* claim underneath (top gainer day = best day) is testable and listed in §D. |
| A-07 | [01:40:09–01:40:26] | "This is a day where I made $98,654.39" (order-execution demo). | `red flag` — anecdote. Includes the standard disclaimer: "my results are not typical." |
| A-08 | [02:48:20–02:48:34] | Roth IRA: $188K of contributions (three × ~$6K) grown to "over $7 million in trading profits", projected "easily $20 million" by age 59½. | `red flag` — this is the 10,000× account again in retirement-account form. Do not let the dollar signs leak into protocol design. |

---

## B. Entry / setup rule — the core testable content

The strategy's actual entry rule, stated repeatedly in nearly identical form.

| # | Time | Claim as stated | Status |
|---|---|---|---|
| B-01 | [1:28:40–1:31:18] | **Micro pullback**: stock squeezes up (green candles), pulls back (confirmed by ≥2 red candles), bounces forming a double bottom; **entry = the first candle that makes a new high versus the high of the previous candle**; stop = low of the pullback; profit target = retest of the high of day; wants ≥2:1 reward:risk ("I always want to retest a high of day... 'when this setup works it goes to the high of day'"). | `candidate` — the single most machine-testable rule in the corpus: on 1-min bars, entry candle makes new high after a ≥2-candle pullback. Needs intraday data; on daily bars it becomes an *adapted* version (see B-05). **Daily adaptation (Shape B: pullback + new-high) measured 2026-08-13 → NO EDGE, significantly below baselines (§B.5-B); the intraday rule itself remains untested.** |
| B-02 | [1:29:17–1:29:40] | Don't buy the breakout move itself: "if I bought right here, what would be my max loss? ... it's really far away ... my profit target has to be two times that ... it's better to wait for the stock to pull back." | `candidate` — testable as a comparison: pullback entries vs chasing entries, same-day forward returns. Directly relevant to how patternScanner's Shape A (consolidation breakout) should be defined — he's claiming breakout-chasing has bad R:R. **Daily adaptation (Shape A: buy above tight range) measured 2026-08-13 → NO EDGE (§B.5-A); the pullback-vs-chase R:R comparison itself remains untested.** |
| B-03 | [1:35:20–1:36:07] | "My rule of thumb: I always like to trade the first and the second pullback... third and fourth pullback, it can be a little too risky." | `candidate` — testable: win rate / R:R by pullback number within the same day's move. |
| B-04 | [1:31:36–1:32:56] | Will relax the 2:1 requirement for wide-range stocks: "when you have a stock that has big ranges like this, I will sometimes take the risk of taking a trade even if it doesn't offer the perfect 2:1 profit-to-loss ratio." | `partial` — a defined exception (big ATR days), still formalizable. |
| B-05 | [1:10:53–1:11:22] | On reversal patterns: buy the *second* confirming candle, not the first ("usually when people take a trade in this area, they're going to be buying... the second candle as it confirms the trend"). | `candidate` — testable on daily bars: confirmation-candle entries vs first-candle entries. Same tension appears in patternScanner Shape C (double bottom) definition. **Confirmation-close adaptation (Shape C) measured 2026-08-13 → NO EDGE (§B.5-C); the first-vs-second-candle comparison remains untested.** |
| B-06 | [1:25:30–1:25:53] | "The best trades are when multiple time frames are aligning and giving you positive signals to buy" (daily → 5-min → 1-min alignment). | `candidate` — testable in adapted form: does daily-chart context (e.g. above VWAP-equivalent, MACD state) raise the hit rate of the intraday setup? This is a *conditioning* claim. |

---

## B.5 Shape-detector verdicts — pre-registration #2 campaign

Measured 2026-08-13 per [PREREGISTRATION.md](PREREGISTRATION.md) #2 (frozen
2026-08-13: N=10 primary, 0.15% round-trip cost, Holm across A/B/C at α=0.05,
OOS 2016–2025 only, baselines bootstrapped 1,000× at fixed seed, era-matched).
Full report: `data/cache/measure_report.md` (+ `measure_results.json`).

Scope note: these verdicts concern the shapes **unconditionally on daily
bars** — the daily-bar adaptations of the reference method's entry timing
(B-01's pullback/new-high and double-bottom, B-02's breakout-chase, B-05's
confirmation candle). They are **not** verdicts on the intraday claims as
stated, which remain untested (no intraday data).

| # | Shape (as measured) | Verdict | OOS evidence (2016–2025, N=10, after cost) |
|---|---|---|---|
| B.5-A | Shape A — consolidation breakout: buy above a tight K-bar range on volume | `tested, rejected` — **NO EDGE** | n=5,669; mean +0.42%; excess vs random −0.08pp (p=0.64), vs same-ticker −0.02pp (p=0.91) — indistinguishable from chance |
| B.5-B | Shape B — pullback to trend: new K-day high after a pullback to the MA | `tested, rejected` — **NO EDGE, significantly below baselines** | n=7,218; mean −0.02%; excess vs random −0.50pp (p=0.002), vs same-ticker −0.53pp (p<0.001), vs SPY −0.60pp — the confirmation is a fade signal on daily bars |
| B.5-C | Shape C — double bottom: close above the peak between two swing lows | `tested, rejected` — **NO EDGE** | n=368; mean +0.33%; excess vs random −0.16pp (p=0.80), vs same-ticker −0.14pp (p=0.83) — indistinguishable from chance |

Project-level consequence (DESIGN_BRIEF §1): no shape clears the bar, so the
result is a **rigorous null** — worth publishing, and Phase 5 (paper trading)
is not triggered. These verdicts stand unless a new pre-registration re-tests
with fresh parameters and a fresh window.

---

## C. Exit rules

| # | Time | Claim as stated | Status |
|---|---|---|---|
| C-01 | [1:34:02–1:35:15] | **Exit indicators** (chart-based): (1) high-volume red candle; (2) MACD crossover; (3) topping tail / doji at top; (4) break of VWAP going down; (5) break of 9 EMA going down. | `tested` (pre-reg #17, measured 2026-08-19, verified 2026-08-19) — the protocol question resolved: S1 (HV-red) and S2 (VWAP-break) timing EDGE in the primary but **fail the §5 gate** (NO EDGE on the 904-union) and do not reproduce under the fresh-seed baseline redraw; F1 system contrast NO EDGE (pooled) / FADE (Shape A). The exits are well-timed; the system isn't (§I.14). |
| C-02 | [2:31:08–2:31:27] | Exit indicator (6): "level 2 big seller or burst of red on the time and sales" (order-book data). | `out of scope` — we don't have level-2 data; note as a real edge risk: the strategy as practiced uses data we can't reproduce, so our backtest is of a *subset* of the claimed strategy. |
| C-03 | [1:12:02–1:12:34] | "When we make the full two steps down... it's basically when you have two candles that go lower and lower that we get out." | `tested` (pre-reg #17, measured 2026-08-19, verified 2026-08-19) — two-steps-down exit NO EDGE (n=195, est −0.0080, p=0.198) (§I.14). |
| C-04 | [1:33:19–1:33:48] | "I want to cap my losers, not my winners": exit immediately at max-loss point; hold winners until an exit indicator. | `tested` (pre-reg #17, measured 2026-08-19, verified 2026-08-19) — asymmetry claim: q90/q95 **FADE** (both windows), q99 **EDGE** and survives the §5 gate; F1 system contrast NO EDGE / FADE-A; trigger-check NOT TRIGGERED (§I.14). |
| C-05 | [2:05:37–2:06:58] | Order-book override: a 250,000-share sell order on level 2 means "that chart will never do what I thought it might have done" — i.e. book structure can veto a chart pattern. | `out of scope` (no level-2 data). Important honesty note: his edge may partly live in data we cannot see, so measured results won't reproduce his P&L — expected, not evidence of fraud. |

---

## D. Stock selection (scanner) criteria — most directly testable on daily bars

These are the pre-market / intraday stock-selection rules. The core claim is
the **"five pillars"**. He says of these: **"this is not opinion but it's
fact"** ([46:40–59:40]) — a strong falsifiable statement.

| # | Time | Claim as stated | Status |
|---|---|---|---|
| D-01 | [46:40–59:40] | Scanner criteria: price **$2–$20** ("$2–10 even better"); already **up 30%** on the day; **5× relative volume** vs average; **news catalyst** (flame age: red <2h, orange 2–12h, yellow 12–24h); **low float**. Backed, he says, by "$12M+ of trading data." | `tested, inconclusive` — **H1** in [PREREGISTRATION.md](PREREGISTRATION.md), measured 2026-08-13 → **INCONCLUSIVE by count floor** (§D.5): the AND-combined screen fired 7× in 26 years (all IS 2000–2010), 0 OOS detections — as a daily-bar operationalization it is effectively dead, so no verdict is possible. News leg excluded (brief §3); float ≤10M assumed (number unstated in this passage). The intraday claim remains untested. |
| D-02 | [2:23:07–2:23:37] | Sample plan restates the pillars with numbers: price **$1–$10**; float **<10M shares**; **up ≥25%**; relative volume **10×**; must be **top 3 leading percentage gainers** ("obvious" = others are watching). | `tested, inconclusive` — **H2** in [PREREGISTRATION.md](PREREGISTRATION.md), measured 2026-08-13 → **INCONCLUSIVE by count floor** (§D.5): 6 detections in 26 years (all IS 2000–2010), 0 OOS. Both variants H1/H2 earned separate Holm slots; neither could be tested. The intraday claim remains untested. |
| D-03 | [1:38:38–1:39:04] | "The days I do the best are when we have a stock like this that is super obvious... the number one leading percentage gainer in the entire market." | `tested, rejected` — **H3** in [PREREGISTRATION.md](PREREGISTRATION.md), measured 2026-08-13 → **NO EDGE** (§D.5): n=2,513 OOS at frozen N=1; the day-paired rank-1-vs-rank-2–10 claim test is precisely null (+0.00pp, p=0.986). On daily bars, the "obvious" top gainer buys nothing over ranks 2–10. |
| D-04 | [1:38:44–1:39:38] | "The reason these setups work": fast-moving stock + catalyst + low float → supply/demand imbalance; "I've seen stocks go up 100% in one day." | `partial` — the mechanism claim (catalyst+low float → continuation) is testable; the 100%/day anecdote is an observation, not a rule. |
| D-05 | [1:13:58–1:14:07] | Chart setup: 9/20/200 **exponential** MAs + VWAP + MACD + volume bars; "I use the same exact indicators on my 1-minute, 5-minute, daily... same across time frames." | `out of scope` as setup guidance; the MACD-conditional claims below are the testable residue. |
| D-06 | [1:24:41–1:25:06] | MACD used **only on the 1-minute chart** ("I don't use the MACD on my 5-minute or my daily chart"). | `out of scope` for daily-bar measurement; implies MACD state on *daily* bars is not part of his actual system. |

---

## D.5 Pillar verdicts — pre-registration #1 campaign

Measured 2026-08-13 per [PREREGISTRATION.md](PREREGISTRATION.md) #1 (frozen
2026-08-13: N=1 primary, 0.15% round-trip cost, Holm across H1–H3 at α=0.05,
OOS 2016–2025 only, baselines bootstrapped 1,000× at fixed seed, era-matched).
Full report: `data/cache/pillar_measure_report.md` (+ `pillar_measure_results.json`).
Detector: `tools/pillars.py` (code + input fingerprints recorded in the report).

Scope note: these verdicts concern the **daily-bar operationalizations** of the
scanner filters — close-to-close gain leg ("still up at close", the stronger
subset per the translation table); rank over the *full* frozen universe (a
stricter reading than his pre-filtered scanner — documented deviation); float =
frozen 2026-08-13 snapshot (brief §9 row 7 (a)). They are **not** verdicts on
the intraday claims as stated.

| # | Hypothesis (as measured) | Verdict | OOS evidence (2016–2025, N=1, after cost) |
|---|---|---|---|
| D.5-H1 | H1 — $2–20 close, +30% close-to-close, 5× rel-vol, float ≤10M | `tested, inconclusive` — **INCONCLUSIVE by count floor** | n=7 total (all IS 2000–2010), **0 OOS** — the AND-combined screen fired 7× in 26 years across 599 tickers. IS record (record only): mean −5.09%, hit 0.286. As a daily-bar filter it almost never fires, so no verdict is possible |
| D.5-H2 | H2 — $1–10 close, +25%, 10× rel-vol, rank ≤3, float ≤10M | `tested, inconclusive` — **INCONCLUSIVE by count floor** | n=6 total (all IS 2000–2010), **0 OOS**; IS record (record only): mean −5.54%, hit 0.500. Same count-floor outcome as H1 |
| D.5-H3 | H3 — rank-1 %-gainer cohort of the universe, unconditional | `tested, rejected` — **NO EDGE** | n=2,513; mean −0.19%; excess vs random −0.06pp (p=0.72), vs same-ticker −0.07pp (p=0.64), vs SPY −0.21pp (p=0.11). **Day-paired claim test (rank-1 vs rank-2–10, same day): diff +0.00pp, p=0.986, 95% CI ±0.25pp; hit rate 0.440 vs 0.455** — the top gainer is precisely indistinguishable from ranks 2–10 |

Project-level consequence: the "obvious" stock (D-03) buys nothing on daily
bars — the selection signal is not visible at the frozen N=1 horizon (the
closest analog to the source method's minutes–hours holds). Exploratory
context (pre-declared grid, never Holm-tested, no verdict): the N=1/3/5/10
raw means rise monotonically (−0.19/−0.03/+0.28/+1.63% after cost) —
consistent with the era's 2-week momentum drift (random OOS windows at N=10:
+0.64% raw; SPY +0.58%), not with a selection edge. A horizon-based follow-up
would need a new pre-registration and a fresh window.

---

## D.6 Momentum horizon follow-up — pre-registration #4 campaign

**Measurement-derived, not a direct corpus claim** — promoted from the
pre-declared exploratory N-grids of pre-regs #1/#2 (same entries, forward
returns rising with horizon: H3 −0.19%/−0.03%/+0.28%/+1.63% at N=1/3/5/10;
A +0.40%→+0.95%, C +0.62%→+1.39% at N=10→20). Frozen 2026-08-14 before any
measurement: N=20 primary, two verdict families, each Holm-corrected across
A/C/H3 at α=0.05, OOS 2016–2025, same engine and baselines as #1–3. Full
report: `data/cache/momentum_measure_report.md` (+
`momentum_measure_results.json`).

**Family 1 — absolute at N=20 (pattern vs era-matched baselines): all NO
EDGE.** A n=5,646 +0.95% (p_input 0.61); C n=364 +1.39% (p_input 0.88);
H3 n=2,494 +3.19% (p_input 0.47, Holm gate 0.0167). The H3 row is the
project's most interesting near-miss: **significantly above random entries
(+2.00pp, p=0.004) and SPY (+2.00pp, p=0.004), but indistinguishable from
same-ticker buy-and-hold (+0.66pp, p=0.47, CI −0.86..+2.44pp)** — the
selection adds nothing over simply owning the ticker.

**Family 2 — continuation (paired N=20 vs N=5 on identical entries): EDGE ×
3 — the project's first EDGE verdicts, recorded exactly per the frozen
rule** (Holm-rejected + paired-diff CI excluding 0, positive):

| entry set | n pairs | mean r5 | mean r20 | diff | 95% CI | p | verdict |
|---|---|---|---|---|---|---|---|
| A | 5,646 | −0.08% | +0.95% | **+1.03pp** | +0.66..+1.61pp | <0.001 | EDGE |
| C | 364 | +0.24% | +1.39% | **+1.15pp** | +0.10..+2.17pp | 0.038 | EDGE |
| H3 | 2,494 | +0.28% | +3.19% | **+2.91pp** | +1.78..+4.31pp | <0.001 | EDGE |

The paired diff is exactly the 15-bar close-to-close return after bar 5
(cost cancels in the difference), so F2 states: *after these signals, the
entry names kept moving up from bar 5 to bar 20 — significantly, on all
three entry sets.* Sensitivities agree: N=40 continuation strengthens
(A +1.59pp, C +2.65pp, H3 +7.11pp, all p<0.001); dedupe-20 holds
(H3 +2.91%); per-decade H3 rises (+1.30% 2016–19 → +4.47% 2020–25);
Shape B flat (−0.01%) — the pre-registered exclusion was validated.

**How the two families read together.** F2's EDGE is real as a statement
about the entry names' forward drift, but F1's same-ticker row explains it:
H3's N=20 mean is statistically indistinguishable from buying-and-holding
the same tickers over the same calendar span. The continuation gain is the
era's small-cap 2–4-week drift — available to **any** holder of the entry
names — not edge from the pattern's *selection*, which F1 shows is null
(selection vs same-ticker: all three CIs include 0). Per DESIGN_BRIEF §1,
the pattern-vs-chance trigger test is Family 1, and it is null on all
three → **Phase 5 remains not triggered**; the F2 EDGE is a holding-period
property of the era's drift, not a harvestable pattern edge (a system built
on it would be buying drift, not signal). The F2 verdicts stand as
recorded — this paragraph is the interpretation, not the verdict.

Sensitivities (no verdicts): N=40 absolute A +1.49% / C +2.86% /
H3 +7.38%; IS record (observation only) A +1.29% / C +0.31% / H3 +5.36%.

---

## D.7 Per-decade drift decomposition — pre-registration #5 campaign

Follow-up of §D.6, frozen 2026-08-14 before any measurement: is the N=20
drift uniform across the OOS era or concentrated in 2020–2025? Same engine
(c7421fbf…), same baselines at sub-era granularity (windows drawn only
from bars whose start date falls in the sub-era), N=20, two verdict
families, each Holm-corrected across A/C/H3 at α=0.05. Full report:
`data/cache/decade_measure_report.md` (+ `decade_measure_results.json`).

**Family 1 — sub-era excess difference (late 2020–25 minus early 2016–19,
two-sample bootstrap): NO EDGE × 3.** A +0.47pp (p=0.51), C +1.79pp
(p=0.30), H3 +3.48pp vs random (**p=0.008**, CI +0.80..+6.22pp) but +2.40pp
vs same-ticker (p=0.138) — p_input 0.138 fails Holm gate 0.0167.

**Family 2 — late-era absolute at N=20 (within-sub-era baselines): NO EDGE
× 3.** A n=2,403 +1.06% (p_input 0.97); C n=182 +2.11% (p_input 0.44);
H3 n=1,488 +4.47% — **significantly above late-era random (+3.38pp,
p=0.002, CI +1.34..+5.85pp) and SPY (p<0.001), but indistinguishable from
same-ticker buy-and-hold (+1.47pp, p=0.238)** — p_input 0.238 fails Holm
gate 0.0167.

**Answer to the campaign's question.** The late-era strengthening is
**real vs random entries** (F1 p=0.008, F2 p=0.002, continuation H3
late−early +2.81pp p=0.020; early-era H3 excess is ~0, p=0.94) — so the
drift is genuinely late-era-dominated. But it **never clears the same-
ticker control in either family**: within 2020–2025, H3's +4.47% is
statistically the same as buying-and-holding those tickers (p=0.238).
Per the pre-registered rule and consistent with §D.6: the drift is
**late-era beta, not selection edge** — the raw means that motivated this
campaign (+1.30% → +4.47%) are real and concentrated in the late era, and
the same-ticker control absorbs them. Phase 5 remains not triggered, now
with a dedicated decomposition behind it.

Nuance for the record: the late-era concentration is **not** a single
2020–21 mania episode — per-year N=20 means for H3: +9.1% (2020), +6.2%
(2021), +0.1% (2022), +6.1% (2023), +4.6% (2024), +0.4% (2025) — broad
late-era small-cap drift with two strong years and two flat ones. N=40
late-era H3: +9.82%.

Sensitivities (no verdicts): early-era absolute (H3 ~0 excess), N=40 by
sub-era, per-year means, dedupe-20 by sub-era — all in the report.

---

## E. The two-filter veto (his highest-specificity claim)

| # | Time | Claim as stated | Status |
|---|---|---|---|
| E-01 | [02:01–04:57] | Before entry, two filters: **MACD** (blue line crossed negative = no) and **volume** (high-volume selling on red candles = no). "If just one of them says no, I don't take the trade." | `tested, rejected` — **H-VA/VB/VC** in [PREREGISTRATION.md](PREREGISTRATION.md) #3, measured 2026-08-14 → **NO EDGE in both verdict families, all three shapes** (§E.5). Does conditioning on (MACD non-negative AND no high-volume red bar) improve forward returns vs the raw pattern? No — on A and C the veto cuts trades whose mean forward return was *higher* than the kept trades'. |
| E-02 | [04:29–05:54] (ultimate-guide/oxob0x0Xz7s.md) | "**80% chance of this working**" (of the setup when both filters pass). | `tested, rejected` — the literal 80% is falsified on all three shapes (win rates 48.7–52.9%, one-sided p ≤ 2e-24, CI upper ≤ 0.58); even his own softened 60% "enough to be profitable" floor fails at α=0.05 (C p=0.009); on A/B the pass set wins *below* chance (§E.7). The pre-registered expectation — fail honestly like most 80% claims — was met. |
| E-03 | [1:21:54–1:23:04] | "When the MACD actually crosses... more times than not, any attempt to break out will reject and the price will end up selling off." (Learned in the 2022 bear market; "very consistent especially during the bear market.") | `tested, partial support` — **FADE EDGE on Shape B** (bear days: −1.62pp, p=0.012; vs chance: p_input 0.014), NO EDGE × 6, INCONCLUSIVE × 1 — the project's first verdicts in a claim's favor, and they land on the shape that matches the described scenario, in the regime he emphasizes (§E.6). The unconditional form is null; the effect is a **fade signal** — it says *don't take* the trade, it does not make any pattern profitable. Phase 5 not triggered. |
| E-04 | [3:02:18–3:04:30] | Final quiz restates the veto: high-volume red candle = no; MACD negative = no; "if it's not a hard yes, then it's a no" (beginner rule). | `tested, rejected` — same campaign as E-01 ([PREREGISTRATION.md](PREREGISTRATION.md) #3), measured 2026-08-14. The kill-rate decomposition answers the "hard yes" question: the veto is a **trade-count reducer, not an edge enhancer** (A −30%, B −3%, C −15% of OOS trades; the killed sets had *higher* mean forward returns on A and C — §E.5). |

---

## E.5 Veto verdicts — pre-registration #3 campaign

Measured 2026-08-14 per [PREREGISTRATION.md](PREREGISTRATION.md) #3 (frozen
2026-08-14: N=10 primary — the frozen shape horizon — 0.15% round-trip cost,
two verdict families, each Holm-corrected across A/B/C at α=0.05, OOS
2016–2025 only, baselines bootstrapped 1,000× at fixed seed, era-matched).
Full report: `data/cache/veto_measure_report.md` (+ `veto_measure_results.json`).
Filter: `tools/veto.py` — kill = MACD(12,26) line < 0 OR (red candle with
volume ≥ 2× prior-20 mean); pass = both legs clear.

Scope note: the veto is applied to the **daily-bar shape detections** (the
entry-setup analogs); MACD is computed on daily bars, though the source says
he uses MACD on 1-min charts — the *rule* as stated (E-01/E-04) is
time-frame-agnostic. These are verdicts on the veto *mechanism*, not on his
intraday practice.

| # | Hypothesis (as measured) | Verdict | OOS evidence (2016–2025, N=10, after cost) |
|---|---|---|---|
| E.5-A | Veto on Shape A (consolidation breakout) | `tested, rejected` — **NO EDGE, both families** | F1 conditioning: pass n=3,941, mean +0.21% vs full +0.40% — the veto *lowers* the mean (excess −0.19pp, p=0.35). F2 absolute: excess vs random −0.27pp (p=0.15). Kills 30% of A's OOS trades, and the killed set made **more** (mean +0.83% vs +0.21% kept) |
| E.5-B | Veto on Shape B (pullback + new high) | `tested, rejected` — **NO EDGE, both families** | F1: pass n=6,940, mean −0.01% = full (excess 0.00pp, p=0.99) — the veto changes nothing. F2: **significantly below** random (−0.50pp, p=0.002) and same-ticker (−0.50pp, p=0.002) — the vetoed subset inherits Shape B's fade |
| E.5-C | Veto on Shape C (double bottom) | `tested, rejected` — **NO EDGE, both families** | F1: pass n=280, mean +0.46% vs full +0.62% (excess −0.17pp, p=0.80). F2: excess vs random −0.07pp (p=0.98). Killed set again higher (mean +1.54%) |

Project-level consequence: the answer to E-04's question is now measured —
**the veto does not rescue any pattern**. On A and C it systematically cuts
the *better* trades (killed-set means above kept-set means in both); on B it
changes nothing and the pattern remains a fade signal. As an edge-adding
mechanism the two-filter veto is rejected on daily bars at the frozen
horizon; as a trade-count reducer it is real (A −30%, B −3%, C −15% of OOS
trades).

---

## E.6 E-03 verdicts — pre-registration #6 campaign

Measured 2026-08-14 per [PREREGISTRATION.md](PREREGISTRATION.md) #6 (frozen
2026-08-14: N=10 primary — the frozen shape horizon — 0.15% round-trip cost,
**three** verdict families, each Holm-corrected across A/B/C at α=0.05, OOS
2016–2025 only, baselines bootstrapped 1,000× at fixed seed, era-matched).
Full report: `data/cache/e03_measure_report.md` (+ `e03_measure_results.json`).
Leg: `tools/e03.py` — **bearish signal-line MACD(12,26,9) crossover within
L=20 bars before the signal bar** (hist = line − 9-EMA signal; hist<sub>j</sub> < 0
AND hist<sub>j−1</sub> ≥ 0, k ∈ [1,20], cross strictly precedes the signal);
regime (pre-registered, the claim's own qualifier): **bear = SPY close < SPY
200-day SMA at t**.

Claim as measured: after a bearish MACD signal-line cross, breakout attempts
reject — crossed breakouts underperform their controls. Because the claim
is negative, the FADE EDGE rule required Holm rejection **and** the excess
CI **upper** bound < 0 (sign convention flipped vs #1–5).

| # | Hypothesis (as measured) | Verdict | OOS evidence (2016–2025, N=10, after cost) |
|---|---|---|---|
| E.6-F1 | Cross conditioning, all OOS (crossed vs not-crossed) | `tested, rejected` — **NO EDGE × 3** | A: crossed n=3,477, +0.21% vs +0.70% (excess −0.48pp, p=0.254). B: n=2,930, −0.04% vs +0.00% (p=0.810). C: n=204, +1.04% vs −0.04% (**+1.07pp — wrong direction**, p=0.230). Unconditioned, the cross does nothing |
| E.6-F2 | Cross conditioning, **bear days only** (the claim's emphasized regime) | `tested, partial support` — **FADE EDGE (B)**, NO EDGE (A), INCONCLUSIVE (C) | **B: crossed n=230, −0.95% vs not-crossed +0.70% — excess −1.62pp (95% CI −2.78..−0.46pp, p=0.012, Holm-rejected at gate 0.0167)**. A: n=170, −0.18% vs +0.42% (p=0.456). C: n=13 — below the count floor, reported never spun |
| E.6-F3 | Avoidance bar: crossed subset vs era-matched random + same-ticker baselines | `tested, partial support` — **FADE EDGE (B)**, NO EDGE × 2 | **B: n=2,930, mean −0.04%; excess vs random −0.53pp (CI −1.00..−0.10pp, p=0.014) and vs same-ticker −0.57pp (CI −1.02..−0.14pp, p=0.008) — p_input 0.014 vs Holm gate 0.0167, a narrow pass, noted honestly**; vs SPY −0.63pp (p<0.001). A: p=0.184. C: p=0.470 |

Interpretation: **the claim is supported in its emphasized regime for its
most faithful shape** — B (pullback + new high) is the shape whose structure
(strong move → compression → cross → new-high attempt) matches the described
scenario, and B is the only shape whose crossed breakouts underperform, in
bear days (F2, p=0.012) and vs chance over all OOS (F3, p_input 0.014). The
internal consistency is striking: F1-B is null (−0.05pp) while F2-B is
−1.62pp — the effect lives *entirely* in bear days, exactly as claimed
("very consistent especially during the bear market"), and the per-year
crossed-subset means put 2022 (the year he says he learned it) at −2.01%,
the strongest negative year. A and C show nothing; C is unmeasurable in
bear days (n=13).

The honest caveats: F3's pass margin is narrow (p_input 0.014 vs gate
0.0167 — 0.0027) and the bear-days F3 sensitivity is a near-miss (B
−1.45pp vs random, p=0.074). The zero-line reading (pre-reg #3) fired
**0 of 31,226 detections** on the signal bar — structurally impossible on
these detectors (breakout days are up-days), which is why the windowed
signal-line reading is operative. Implementation note: F3's same-ticker
baseline uses the shape's own ticker distribution per the #1–5 protocol
(an earlier pass used the combined crossed-set distribution inherited from
the measure_veto template; corrected before any verdict was written back;
verdicts unchanged, B's F3 margin widened from p=0.016 to 0.014). The
measure_veto record stands under its own implementation choice — all its
verdicts were far from the gates.

Project-level consequence: this is a **fade signal**, the first verdict in
a claim's favor. It does not make any pattern profitable — it identifies
B-breakouts worth *avoiding* (crossed-B bear-day breakouts lose ~1% while
their not-crossed counterparts gain +0.70%). The Phase 5 trigger test is
the positive-edge bar: unchanged, untouched, and untriggered. Verification:
deterministic (outputs byte-identical across two runs), data layer
independently recomputed row-by-row from bars (0 real mismatches).

---

## E.7 E-02 verdicts — pre-registration #7 campaign

Measured 2026-08-14 per [PREREGISTRATION.md](PREREGISTRATION.md) #7 (frozen
2026-08-14: N=10 primary — the frozen shape horizon — 0.15% round-trip cost,
**two** verdict families, each Holm-corrected across A/B/C at α=0.05, OOS
2016–2025 only, baselines bootstrapped 1,000× at fixed seed, era-matched).
Full report: `data/cache/e02_measure_report.md` (+ `e02_measure_results.json`).
No new legs: the setup IS the frozen veto-pass subset of pre-reg #3
(`veto_detections_v1.csv` — both filters pass). Win = forward return > 0
after cost, entry open t+1, exit close t+10.

Claim as measured: "we've got an 80% chance of this working" — win rate
≥ 0.80 on the veto-pass setup — falsification test via exact one-sided
binomial (H0: p ≥ 0.80), Holm across shapes; plus the complementary
win-rate-edge family vs chance.

| # | Hypothesis (as measured) | Verdict | OOS evidence (2016–2025, N=10, after cost) |
|---|---|---|---|
| E.7-F1 | Win rate ≥ 0.80 on the pass set (the literal claim) | `tested, rejected` — **REJECTED × 3** | A: n=3,941, win rate **0.4869** (p < 1e-308; one-sided CI upper 0.5002). B: n=6,940, **0.4899** (p < 1e-308; CI upper 0.4999). C: n=280, **0.5286** (p = 2.0e-24; CI upper 0.5790). The claimed 0.80 is off by ~30pp; the upper bound never reaches 0.58 |
| E.7-F2 | Pass-set win rate vs era-matched chance (win-rate edge) | `tested, rejected` — **NO EDGE × 3** | A: **−3.04pp vs random (p=0.004)** and −3.57pp vs same-ticker (p=0.004) — wins *below* chance, CI upper negative. B: **−2.76pp (p<0.001)**, −3.09pp (p<0.001) — below chance. C: +1.36pp (p=0.786) — null. p_input cleared no gate |

Interpretation: **the 80% number is false on daily bars.** The pass set
wins 48.7–52.9% of the time — a coin flip at best — and on A and B it
wins *significantly less often* than chance. His own hedge ("60% of the
time can be enough to be a very profitable trader") is also unreached:
even the 0.60 floor is falsified at α=0.05 on all three shapes (A
p=8.9e-47, B p=9.2e-77, C p=0.009). The veto does not raise the win rate
(pass-vs-kill excesses null; on A the killed set wins more often,
−2.64pp, p=0.066) — consistent with §E.5's mean-return verdict. No-cost
win rates (~0.50) and the IS record (0.52/0.50/0.51) show the 80% is not
visible under any reading. The pre-registered expectation — "expect it
to fail honestly like most 80% claims" — was met at astronomical
significance.

Project-level consequence: this is the second independent lens on the
same frozen setup (first was §E.5 mean returns, now win rates) — and
both say the veto-pass setup is not an edge; on frequency it is
significantly *below* chance for A and B. Phase 5's trigger test remains
the positive-edge bar: unchanged, untouched, untriggered. Verification:
deterministic (results 92669c58…, report 07e8a624…, byte-identical
across two runs); data layer independently recomputed row-by-row from
bars; F1 p-values and CI bounds cross-checked against scipy's exact
binomial AND a lgamma-free independent computation (agreed to 1e-13
relative where scipy didn't underflow; below 1e-308 the log10 values
were verified exactly).

---

## F. Market-structure / timing claims

| # | Time | Claim as stated | Status |
|---|---|---|---|
| F-01 | [1:44:58–1:47:07] | Best trading window 7–10 a.m. ET: "I kind of trade from 7 a.m. until about 10 a.m., and that's where I can capitalize on peak volatility and peak liquidity." | `out of scope` for daily bars; relevant only if intraday data is ever added. |
| F-02 | [1:45:30–1:46:32] | Pre-market moves are "typically cleaner" (no halts, no circuit breakers 4–9:30 a.m. and 4–8 p.m.); news breaks pre-market, not during regular hours. | `out of scope` (intraday); the daily-bar residue: gap direction + pre-market volume may matter for next-day behavior — worth a question in DESIGN_BRIEF §9, not a claim. |
| F-03 | [1:25:53–1:26:17] | "Most stocks will have support at the VWAP... at least for a moment"; support at the 9/20/200 MAs; "prior resistance, once the stock can break above it, becomes support." | `candidate` — testable on daily bars (MA levels, prior-resistance flip); these are the patternScanner-relevant structural claims. |
| F-04 | [1:41:22–1:44:46] | Stop orders are visible to brokers/market makers who "engage in stop hunting": they move price down to trigger stops, then buy. | `out of scope` — unfalsifiable with daily close data; would need tick data + a well-defined test. Note it, don't measure it. |

---

## G. Risk management / process guidance

Mostly sound, mostly out of scope for measurement — but they are the part
worth keeping as process reference (the user's stated use for the corpus).
Where they embed a measurable claim, it's flagged.

| # | Time | Claim as stated | Status |
|---|---|---|---|
| G-01 | [38:55–41:07] | Risk $100 to make $200 = 2:1; "you only need to be right 33% of the time to break even"; **exit price must be known before entry.** | `out of scope` as guidance; the 33% arithmetic is the break-even formula we'll use in measurement anyway (DESIGN_BRIEF §6 uses the same math). |
| G-02 | [2:16:54–2:18:11] | Risk = entry − stop, **not** total capital: "what you're really risking is the difference between your entry and where you would sell it for a loss." | `out of scope` — but adopt the definition for patternScanner position math. |
| G-03 | [42:34–45:33] | "Trader rehab": after a loss, cut share size to a level with no emotional response; minimum 10 days / two trading weeks. | `out of scope` (process). |
| G-04 | [2:24:19–2:26:21] | Size scaling: first trade at ¼–½ size; full size only after a winner; stay small after a loser; "three strikes you're out" (3 consecutive losers → stop for the day). | `out of scope` (process) — but note the embedded claim: first-trade result predicts day outcome ("if that first trade was... green... it's usually a winner" [2:27:38]). That *is* testable (serial correlation of trade outcomes) and would be a good pre-registered check if trade logs ever exist. |
| G-05 | [2:28:41–2:31:45] | Guard rails: quit at daily max loss; quit if you give back half of profits; abandon a stock that fails to keep going up. Phases: 1 = sim experience, 2 = sim proof-of-concept (**one trade/day for 10 days, green on ≥5 of 10**, "60% accuracy" positive result), 3 = real money same plan. | `out of scope` (process). Phase-2 criterion embeds the 60% target — same number as A-05; consistent with 66% claimed accuracy. |
| G-06 | [2:35:54–2:39:31] | Scale up slowly: +50 shares per 10 days; after a big loss, cut to ¼ size until 50% of the loss is recouped; ease off in "cold" markets, push in "hot" ones. | `out of scope` (process); embeds a regime-timing claim that's unmeasurable without his market-regime definition. |
| G-07 | [2:19:51–2:20:11] | Beginners: "trade as much as you can" in the simulator (experience phase) — before the 1-trade/day plan kicks in. | `out of scope`. |
| G-08 | [1:36:09–1:36:51] | Annie Duke / Thinking in Bets: play only the bread-and-butter setups when learning; stop-out and profit-target discipline beats shot-calling. | `out of scope` — this is the reference source for the project's own posture (calibrate before you claim). |

---

## H. Out-of-scope content logged for completeness

Tax strategy (Roth IRA day-trading, Puerto Rico Act 60, mark-to-market
accounting Form 3115/§475F, trader tax status, LLC/S-corp solo 401K),
platform reviews (Webull, ThinkOrSwim, Lightspeed, DAS Trader $175/mo), order
types and routing, hotkey setups. Not claims about markets; not measured.

One item worth a footnote: at [2:45:45] he states the Roth IRA annual
contribution limit as "$1,000" while [2:46:29] uses $7,000 for the same
example — the captions are unreliable here, and this is the kind of
verifiable-fact slip (if real) to check when auditing the corpus. Flagged,
not adjudicated.

---

## I. Warrior-trading corpus — 2015 "Class 1-12" playlist claims

Claim-extraction pass over the fan-curated playlist, 2026-08-14 (sections
A–H above are the 2025 ultimate-guide course). 13 unique videos; 8 are Ross
Cameron trading content (Class 1/3/4, Level 2/Time & Sales, the $583→$335K
and $1M Challenge retrospectives, Day Trading Station, Biggest Struggle);
5 are other channels (EatSleepProfit, Trading 212, Cameron Bennion,
NeoScribe, Chris Williamson). 2 videos are not trading content (graphene;
David Sinclair) and were skipped; the Day Trading Station video is
equipment/platform content (nothing claim-worthy). Quotes are verbatim
auto-captions (transcription errors expected — check timestamps against
the video); timestamps cite `video-id [mm:ss]`; each quote was re-verified
against the transcript during consolidation. Channel tag in parentheses
marks non-Ross claims. Statuses follow the same rubric as A–H.

### I-A. Performance red flags (self-reported, 2015–2019)

| # | Time | Claim as stated | Status |
|---|---|---|---|
| I-A-01 | xTPcI7HHu5w [00:25–00:35] | "I started with only 583 dollars in my account I finished the year with three hundred and thirty five thousand dollars in verified gains" (2017). | `red flag` — the same trajectory claimed in the ultimate-guide (A-01); "verified" is doing the same unverifiable work as A-02. |
| I-A-02 | xTPcI7HHu5w [04:24–04:37], [15:25–15:50] | $583 → $100K in 44 days (Jan 4 – Mar 8 2017); window stats: $101,280.47 profit, 75% accuracy, avg win $1,300 vs avg loss $1,100. | `red flag` — self-reported; see I-A-04 for the accuracy-window pattern. |
| I-A-03 | xTPcI7HHu5w [09:31–10:40] vs H82nRY9TYU4 [09:53–10:18] | First week: "I took 14 trades and I made money on all 14 of them accuracy was 100% I had a total profit of 1313 dollars" — but the later recap says day 1 +$124, week +$618, account "doubled". | `red flag` — **internal contradiction**: two different first-week figures for the same week ($1,313 vs $618). Same pattern as the E-02 lesson: round numbers vary with the window quoted. |
| I-A-04 | xTPcI7HHu5w [23:07–24:00]; H82nRY9TYU4 [26:28–26:40], [05:30–05:47]; dqrTrFpZdcI [18:07–18:22] | Accuracy across windows: 100% (n=14), 87% (n=47, "fourteen thousand dollars of profit"), 75% (44 days), 68% ("over 1,800 trades... average winning trade about a thousand dollars average losing trade also about a thousand dollars"), 70% ("my average winners... about nine hundred and thirty five dollars and my average losers have been nine hundred and eighty nine dollars"), 67% ("2873 trades"). | `red flag` — window-dependent self-reporting (100→87→75→68–70→67%); the stable core is ~68–70% long-run with ~1:1 avg win/loss, which matches A-03's arithmetic (break-even at 50%, profit via win rate). An accuracy number is only meaningful with its window and trade log — the E-02 lesson. |
| I-A-05 | xTPcI7HHu5w [30:17–30:35]; dqrTrFpZdcI [14:06–14:47]; H82nRY9TYU4 [11:59–12:20] | Drawdowns: 2017 max $22K; "at the beginning of 2016 and up through 2017 my biggest drawdown was about $10,000... reaching the all-time high of losing 46,000 dollars off of my highs" (2019); challenge max $22–24K. | `red flag` — self-reported, unverifiable without statements; consistent shape (drawdowns grow with account size). |
| I-A-06 | H82nRY9TYU4 [00:11–00:42], [00:57–01:37], [31:30–31:45] | $1M cumulative profit in 553 trading days ("averaging about 1,800 dollars per day"); arithmetic model: "getting 20 cents of profit out of the market... nine thousand shares is eighteen hundred dollars a day"; "it is mathematically impossible to take $583 and turn it into a million bucks that's a 170,000 percent return I just did". | `red flag` — the arithmetic is checkable ($583→$1M ≈ 1,715× ≈ +171,400%, internally consistent); the trade log behind it is not. |
| I-A-07 | xTPcI7HHu5w [17:34–18:00], [19:52–20:16]; H82nRY9TYU4 [11:06–11:15], [02:44–03:00] | Monthly P&L: Jan +$16K, Feb +$60K, Mar +$28K, Apr −$4,229; October "base hits" month: zero red days, +$35K; "I was consistently making forty fifty thousand dollars a month"; final challenge day +$14,157 on a $48K account ("a nice 30% gain on the account"). | `red flag` — self-reported narrative; the zero-red-days month is the kind of record a diligence pass could check against posted statements (not our measurement). |
| I-A-08 | dqrTrFpZdcI [00:26–00:38], [13:20–13:26], [22:50–23:05] | "I'm down seven thousand dollars I'm only up eighty five hundred on the month before today so you know I just gave back like ninety percent of my profit on the month"; "when I look at my detailed P&L I've got over 1.5 million dollars in profits there"; "over the last two years of trading since January 1st 2017 I've spent a hundred and forty three thousand dollars on commissions". | `red flag` — self-reported; the $143K-commission figure is *plausible* at his claimed trade count (~2,900 trades over 2.5 years ≈ $50 round-trip ≈ $145K) — internally consistent, still unverifiable. The 90% give-back day is the day he broke his own 3-red-trades rule (I-G-01). |

### I-B. Entry / setup rules (2015 classroom + retrospectives)

| # | Time | Claim as stated | Status |
|---|---|---|---|
| I-B-01 | txWaMpSzHhM [20:29–20:43] | "I trade the first and the second pullback okay... I never trade almost never trade the third" (after a breakout). | `candidate` — same rule as B-03 in the ultimate-guide (cross-course consistency, §I-Notes). Needs intraday data for the pullback-count form. |
| I-B-02 | jfe1Zl-5EQI [24:02–24:22]; pJuG5YtVF84 [02:00–02:26]; txWaMpSzHhM [28:34–29:43] | Reversal entry = "the first one minute or the first five minute candle to make a new high" after a decline (long); mirror for shorts: "shorting the first one minute candle to make a new high... your stop is 3780 and your short at 3766 so you're risking 14 cents" (ATVI). | `candidate` — the most repeated entry rule in the corpus (3 videos + ultimate-guide B-01). Needs intraday; the daily adaptation (Shape B: pullback + new high) was measured → **NO EDGE** (§B.5-B). The intraday rule itself remains untested. |
| I-B-03 | txWaMpSzHhM [13:56–14:11], [20:08–20:26], [26:40–27:25] | Breakout entries: "as soon as we break 3750 buyers come in and anyone that is short covers and you get that spike up"; "I wait for us to break the top of that resistance area that's gonna be the apex point that's the breakout"; "it either works instantly or it doesn't". | `candidate` (structural) — the buy is the break of resistance, not the consolidation. **Cross-course tension:** ultimate-guide B-02 says *don't* buy the breakout ("better to wait for the stock to pull back"). Shape A (break-above-consolidation) measured → NO EDGE (§B.5-A). |
| I-B-04 | txWaMpSzHhM [19:13–19:50] | Flag/stair-step: "three big candles going up it can be anywhere from 3 to 10... then you have a series of candles consolidating" then another move up. | `candidate` — a trend+consolidation continuation definition, distinct from Shapes A/B/C as defined; pre-register the operational definition if pursued. |
| I-B-05 | txWaMpSzHhM [39:03–39:28]; 7UZushUSpLQ [00:10–00:17]; xTPcI7HHu5w [24:53–24:56]; H82nRY9TYU4 [26:42–26:44] | Morning concentration: "9:30 to 12:00 that's when I'm the most aggressive that's when we have the most volume and momentum"; "the first 5 10 minutes of the day is when we have the most volume. That's when we make the most money"; "9:30 to 11:30 that's where all my profits are"; "I only trade for one hour a day 9:30 to 10:30". | `out of scope` for daily bars (intraday timing — same family as F-01). **Internal inconsistency:** four different windows across videos (9:30–12:00 / first 5–10 min / 9:30–11:30 / 9:30–10:30); the "morning is best" core is consistent, the exact window is not. |
| I-B-06 | jfe1Zl-5EQI [17:45–18:16], [23:16–23:55], [19:58–20:11]; txWaMpSzHhM [23:42–24:05] | Reversal checklist: "an RSI above 90 or below 10 are going to peak my interest a candle outside the bounzer bands is going to peak my interest and also five to ten consecutive candles ending with a pin bar or a doji"; volume "half a million in shares or higher I prefer a million", peaking at the sell-off bottom; the V5/V8 scanner screens "RSI below 20 and then... the green above 80". Class 1 caveat: RSI "is more condition to find stocks at extremes it's not by any means a buy or sell indicator". | `candidate` / `partial` — the RSI-extreme component measured via I-X-01 (§I.6): extremes carry directional information at the state level (EDGE × 3) but not at the event level — consistent with **both** Class 1's "not a buy or sell indicator" and Class 4's entry-condition reading; the 90/10-vs-20/80 discrepancy (trade threshold vs scanner threshold) is an internal tension; **Class 1 says RSI is not a signal while Class 4 treats RSI extremes as entry conditions** — within-corpus inconsistency. |
| I-B-07 | 7UZushUSpLQ [01:38–01:41], [05:03–05:27] | Continuation plays are riskier: on VLTC he sized down because "it was not um a fresh breakout. It was a continuation play. And we know that continuation plays can be very risky". | `candidate` (structural) — day-1 fresh-breakout entries vs day-2+ continuation entries of the same move; testable on daily bars (cross-ref pre-reg #4 F2: our signal sets' continuation 5→20 bars showed EDGE — different population, same question family). |
| I-B-08 | txWaMpSzHhM [32:41–33:27] | Reversal selectivity: "my favorite reversal trades are on stocks that are selling off because there's bad news out... a quick sell off because of bad news lots of people are gonna notice it and start watching it for a bottom bounce" — vs market-driven selloffs that "pop up 10 cents and then they sell off another 50 cents". | `partial` — the news/catalyst leg is out of scope (§3: no news in the loop); the market-vs-idiosyncratic regime leg is testable with daily data (cross-ref I-F-03). |

### I-C. Exit rules

| # | Time | Claim as stated | Status |
|---|---|---|---|
| I-C-01 | txWaMpSzHhM [29:44–29:49]; 7UZushUSpLQ [03:48–03:55]; jfe1Zl-5EQI [24:42–25:00] | "I set my stop at the lows... what is the low of the last five minute candle and have we broken that low because if we broke the low of the last five-minute candle in an uptrend then the trend may be starting to change"; "a stop either at the low of day or simply down twenty thirty cents". | `candidate` (needs intraday) — stop at last-candle low / low of day / fixed 20–30¢. Daily adaptation: exit on break of prior-day (or N-bar) low — a candidate exit rule for the shapes if ever tested as a system comparison (cross-ref C-01/C-03/C-04, still untested). |
| I-C-02 | jfe1Zl-5EQI [25:55–26:06], [05:01–05:20] | "If I get into the profit zone I can start adjusting my stop first to break even and then to the low of the last 5-minute candle"; "I just sold half at 2183 forty cents profit just my stop to definitely break even". | `candidate` (needs intraday) — trail-to-breakeven + scale-out-half; same family as ultimate-guide C-04 (cap losers, let winners run). |
| I-C-03 | jfe1Zl-5EQI [05:30–05:45] | Target ladder on reversal longs: "the nine moving average here coming down at 22 dollars and 20 cents that's the first target the 9 second target will be the twenty third target would be the volume weighted average price". | `candidate` (needs intraday) — 9MA → 20MA → VWAP targets; the daily adaptation (9/20-day MA targets) is testable, cross-ref F-03 (MA support/resistance). |
| I-C-04 | jfe1Zl-5EQI [25:34–25:51] | "If I get in I hold for a few minutes and the price stays flat I get out" (flat after entry = bear flag). | `candidate` (needs intraday) — no-move-within-N-bars exit. |

### I-D. Stock selection / scanner claims

| # | Time | Claim as stated | Status |
|---|---|---|---|
| I-D-01 | xTPcI7HHu5w [25:38–26:18]; H82nRY9TYU4 [20:16–20:26] | Price sweet spot: "stocks between $2 and $5 I made a quarter million dollars two hundred and forty thousand dollars profit... stocks over $5 40,000 bucks... above 20 I ignore it" (2017 P&L); 2019 filter: "I only trade stocks between $2 and $10 so this was off the list this was too cheap too expensive". | `tested` (pre-reg #16, measured 2026-08-19, verified 2026-08-19) — **EDGE × 4 + §5 gate PASSES** (§I.13): F1a $2–5 vs >$20 +1.11% (CI 0.86–1.37), F1b $2–10 vs >$10 +0.51% (CI 0.37–0.65), F1c $10–20 vs >$20 +0.29% (CI 0.21–0.37), F1d same-name control +7.92% (CI 7.68–8.18) — all p=0.000, Holm 0.0125; per-band means monotone (lt2 6.10% > 2-5 1.47% > 5-10 0.53% > 10-20 0.32% > gt20 −0.08%); gate on current 603 OOS 2016–2025: all four EDGE again (+2.33/+1.05/+0.50/+3.99%). **Internal inconsistency resolved in the measurement's favor:** both the $2–5 (F1a) and $2–10 (F1b) variants are EDGE, so the 2017/2019 band drift does not change the verdict. Phase-5 trigger-check held: **NOT TRIGGERED** (relative tiering effect, modest absolute size, no tradeable construction). |
| I-D-02 | xTPcI7HHu5w [26:40–26:52] | "Obviously making the most money on stocks that have a larger price range that move more than $1 per share". | `candidate` — testable-daily: daily high-low range ≥ $1 as a selection filter. |
| I-D-03 | xTPcI7HHu5w [27:28–28:24] | Volume band: "I do best on stocks where the total volume is between two million and at most 25 million shares of volume traded on the day that I traded that stock" (sub-250K band: −$7,600). | `candidate` — testable-daily: forward returns by day-volume band. |
| I-D-04 | xTPcI7HHu5w [28:27–29:36] | "I perform best on stocks where the relative volume is 500 percent or higher... what we're looking for are stocks that have news that came out this morning". | `candidate` / `partial` — the RV ≥ 500% leg (day volume vs own average) is testable-daily; the news leg is out of scope (§3). |
| I-D-05 | H82nRY9TYU4 [19:43–20:08] | Daily routine: "every day starts the same way it starts by looking at our scanners which are the gap scanners these tell us the stocks that are opening up the most out of the entire US market". | `candidate` — testable-daily: gap-% ranking as a selection filter (cross-ref F-02 on pre-market moves). |
| I-D-06 | pJuG5YtVF84 [07:07–07:37]; 7UZushUSpLQ [01:03–01:27] | "Stocks that have limited Supply will move a lot faster than stocks that have really big Supply that's why we look at the lower float stocks" (GE's ~10B float: "that's not going to move very quickly"). | `candidate` (structural) — float vs daily move size. **Directly relevant:** static float is already approved as a filter input (§9 decision 7). |
| I-D-07 | txWaMpSzHhM [25:49–26:36] | **"Pattern trading you have to remember does not work on all stocks... it only works on the stocks that have high relative volume"** (volume relative to the stock's own average). | `tested` (pre-reg #8, 2026-08-14) — **NO EDGE:** F1-A/B NO EDGE (excess vs same-ticker −0.22/−0.37pp), F1-C INCONCLUSIVE (count floor), F2-B NO EDGE (contrast +0.30pp, p=0.302 — the claimed direction, not significant), F2-C INCONCLUSIVE, F2-A INCONCLUSIVE by construction. Verdicts: §I.5. |
| I-D-08 | jfe1Zl-5EQI [19:58–20:11] | V5/V8 scanner: "a scanner looking simply for RSI extremes... looking for RSI below 20 and then... the green above 80". | `candidate` (testable-daily) — RSI-extreme screening; see I-B-06 for the 90/10-vs-20/80 tension. |

### I-E. Filters / vetoes

| # | Time | Claim as stated | Status |
|---|---|---|---|
| I-E-01 | txWaMpSzHhM [16:33–17:02], [20:57–21:10], [35:26–35:41], [37:00–37:20] | "If we trade the stocks that are dominated and much higher in high-frequency trading we're gonna lose money hands down every time"; "Apple or Priceline or coca-cola or IBM... very hard to day trade"; patterns are "meaningless" there; "we don't trade penny stocks we don't trade the OTC markets". | `tested` via I-D-07's F2 contrast (pre-reg #8, 2026-08-14) — **NO EDGE:** the low-RV side never significantly outperforms the high-RV side (B contrast +0.30pp, p=0.302 — the claimed direction, not significant). Daily bars cannot measure HFT dominance directly; the contrast is the proxy the data supports. Verdicts: §I.5. |
| I-E-02 | txWaMpSzHhM [24:19–24:40] | "I personally have high a day scanners but I don't find it to be a successful strategy just to buy a stock because it's hitting high a day I'm usually chasing when I do that and it doesn't work". | `candidate` (needs intraday) — chasing new highs fails. **Consistent with what we measured:** Shape B (buying the new-K-day high after a pullback) → NO EDGE, below baselines (§B.5-B) — the daily adaptation of "buying new highs" also fails. |
| I-E-03 | pJuG5YtVF84 [20:19–22:23] | "When we see double tops we know that these are typically um not the best pattern to buy because look at all this empty space here in the middle"; "a lot of people do like to short double tops with a stop right over this level". | `candidate` (structural) — after a big single-day pop, a second test of the high is followed by pullback more often than breakout; testable-daily with a pre-registered double-top definition. |
| I-E-04 | pJuG5YtVF84 [08:02–08:57] | "A day trader doesn't want to trade stocks that have huge spreads just because the risk is so much higher as soon as you get in you're down 30 cents" (30¢ spread needs 60¢ of favorable move to clear cost). | `partial` — no quote data; the embedded arithmetic (cost = spread + fees) is what COST 0.15% approximates for liquid names; motivates a spread-aware cost model if data is ever added. |
| I-E-05 | txWaMpSzHhM [02:51–03:20], [14:16–14:39]; pJuG5YtVF84 [03:37–03:41] | "A good set up means we might be risking $100 but we have the potential to make 300... we would call that a three-to-one profit loss ratio"; "risking $100 to make 10... negative risk reward ratio" — don't take; "using this strategy I can be wrong forty percent of the time and still make money"; "looking at setups that offer two to1 profit loss ratios that's really important with trading". | `candidate` (structural) — R:R-filtered setups vs sub-1:1 setups. Cross-course consistency: 2:1–3:1 R:R matches ultimate-guide B-01/B-04; the "wrong 40% still profitable" arithmetic matches A-05/G-01 (break-even win rate = 1/(R+1); at 2:1 that's 33%, so a 60% win rate is comfortably profitable). |

### I-F. Market-structure / timing claims

| # | Time | Claim as stated | Status |
|---|---|---|---|
| I-F-01 | jfe1Zl-5EQI [16:01–16:09] | "We know that almost all of the big moves will eventually be corrected" (rationale for reversal trading). | `tested` (pre-reg #11, 2026-08-14/15) — **split verdict** (§I.8): F1-UP **EDGE** (relative correction — big up-moves below both baselines: n=35,908, −0.48pp vs same-ticker, Holm-rejected; mean +0.03% after cost), F1-DOWN **NO EDGE** (p=0.950); **F2 FADE × 2** — big moves retrace ≥ half within 10 sessions *less* often than typical bars (−12.77pp / −15.53pp), the ledger's literal reading falsified. "Corrected" holds in the relative sense; "retrace half" does not; the DOWN leg's bounce exists only for weak moves (τ=2 +0.24pp → τ=5 −1.36pp). |
| I-F-02 | jfe1Zl-5EQI [28:28–28:47] | "The move up that may have taken hours can be all given back in a matter of minutes on the good top reversal... the Bulls take the stairs and the Bears take the window". | `tested` (pre-reg #12, 2026-08-15) — **split verdict** (§I.9): A1 **FADE × 3** (per-bar asymmetry INVERTED — up-bars ~6bp larger than down-bars: F1-UP FADE, F1-DOWN FADE knife-edge, F2 FADE), A2 **EDGE** (F4: big up-moves' retracements outpace the moves — n=35,997, +0.40pp/bar, p<0.001); the swing-scale version (S6) confirms the claim across bars (down-swings faster), the per-bar version does not. |
| I-F-03 | txWaMpSzHhM [31:55–32:38] | "Stocks will trend with the overall market unless they have a reason not to" — catalyst names buck the market ("running when the markets tanking"). | `tested` (pre-reg #18, measured 2026-08-21, verified 2026-08-21) — **half-true** (§I.15): F1 baseline **EDGE** (per-stock corr +0.46, CI 0.4521..0.4681, gate EDGE); "reason not to" splits by proxy — F2-vol **EDGE** (volume-spike decoupling −0.23, gate passes), F2-gap **FADE** (corr HIGHER on gap days +0.097), F3-gap **NO EDGE** (p=0.488); **F3-vol's down-day edge is the general catalyst up-bias, not a market-specific run** (S8 down−up negative). Phase-5 trigger-check held: NOT TRIGGERED (structural). |
| I-F-04 | txWaMpSzHhM [48:08–48:30] | "If you can see that we're trading at the top or a bottom of a macro channel you can expect a little bit of choppiness" (SPY); mid-channel → "nice clean moves". | `partial` — channel definition is subjective; testable only with a pre-registered operational definition of channel extremes. |
| I-F-05 | lMZv0K71HOg [04:12–04:25] (EatSleepProfit) | "The momentum side inside the intraday really doesn't carry over until multiple days sometimes it does sometimes it doesn't". | `candidate` — testable-daily adaptation: top-decile one-day gainers' next-day / multi-day forward returns. Cross-ref pre-reg #4 F2 (our signal sets continued drifting up 5→20 bars — EDGE × 3; different population, and that family's F1 absolute momentum at N=20 was NO EDGE — the carryover question is genuinely unresolved). |
| I-F-06 | xTPcI7HHu5w [29:40–29:55]; dqrTrFpZdcI [16:49–16:58] | "Most of my profits come when the market is just sort of sideways because most days the market is kind of sideways"; "red days for me are usually clustered together because the market becomes really slow". | `partial` — as stated they concern his P&L; the market-regime version (operationally define sideways days on SPY, then forward behavior) is testable. |
| I-F-07 | jfe1Zl-5EQI [07:48–08:26] | Declined to short ABY because "we've bounced off a really really solid support level I'm thinking that this is a better chance of trending up". | `partial` — "solid support" needs an operational definition; related to F-03's MA/level claims. |

### I-G. Risk / process rules

| # | Time | Claim as stated | Status |
|---|---|---|---|
| I-G-01 | dqrTrFpZdcI [25:02–25:17]; H82nRY9TYU4 [43:17–43:26], [43:30–43:40] | "I set the rule that three red trades walk away"; "if I have minus two thousand dollars in a loss I walk away"; "statistically when I have a day where I'm down more than two thousand dollars nine out of ten times I will not finish that day in the green"; early 2017: account auto-disabled at −$1,000/day. | `out of scope` (process) — but the embedded "down >$2K ⇒ 9/10 red finish" is a statistical claim about his own daily P&L, testable only with the trade log (cross-ref G-04's first-trade-predicts-day claim — same family). Note: on the dqrTrFpZdcI day he broke his own 3-red rule and gave back ~90% of the month (I-A-08). |
| I-G-02 | jfe1Zl-5EQI [08:38–09:21], [09:29–10:12] | "All of my risk on any trade is capped at about $500 with the profit potential to make 500 to a thousand"; build a $300–400 morning cushion, then "cap the day's give-back at a $100 daily profit floor". | `out of scope` (process) — testable only against a trade log. |
| I-G-03 | xTPcI7HHu5w [33:37–33:51] | "What's not uncommon for me is that my big red days follow big green days" (worst red day −$15K, Nov 27 2017, two days after a +$73K two-day stretch). | `partial` — serial-dependence claim about his P&L (cross-ref G-04); the market-level analog (index red days after green runs) is testable but is not the claim as stated. |
| I-G-04 | xTPcI7HHu5w [13:06–13:29], [32:00–32:44] | 2017: hotkey buys at "95 percent of my buying power" (6× margin); scalability: "for me to take $583 and turn it into a million bucks I had to use an average position size of about eight thousand shares"; $10M would need 80K shares — impossible in the small-cap names traded. | `out of scope` (process) — the 8,000-share average is checkable only against statements; the scalability arithmetic is sound (position size scales with account; float bounds it). |

### I-X. Third-party channel claims (not Ross Cameron)

| # | Time | Claim as stated | Status |
|---|---|---|---|
| I-X-01 | rgVdgR1y1Dg [03:16–03:24] (Trading 212) | RSI rule: "anything above seventy percent... the market is said to be overbought anything below thirty percent... the market is said to be over salt" (overbought ⇒ pullback due, oversold ⇒ bounce due). | `tested` (pre-reg #9, 2026-08-14) — **EDGE × 3 at the state level** (§I.6): F1-OB (RSI>70 below both baselines), F1-OS (RSI<30 above both), F2 (OS−OB contrast positive). The state-level significance is overlap-inflated: the pre-declared event-level view is null (OS p=0.166), so the Phase-5 trigger-check did not trigger. **Corpus tension (I-B-06):** both teachings compatible with the data — extremes carry directional information, but too weak to trade standalone. |
| I-X-02 | rgVdgR1y1Dg [05:33–05:39] (Trading 212) | "These divergence signals are a lot less common so arguably a bit more reliable". | `tested` (pre-reg #10, 2026-08-14) — **frequency CONFIRMED, reliability split** (§I.7): 37,929 divergences vs 124,298 crossings → ratio 0.3051 (CI 0.3022..0.3081), "a lot less common" trivially true; reliability: bullish divergence **EDGE × 2** vs oversold crossings (mean +0.18pp, hit +1.50pp), bearish divergence **FADE** on the mean (+0.21pp — *less* reliable than overbought crossings, the opposite direction) and NO EDGE on hit rate. **Re-checked against historical constituents (pre-reg #13, the §5 gate, measured 2026-08-15): frequency CONFIRMED (ratio 0.3012, CI 0.2972..0.3052); reliability flips on the bearish side — F2-BEAR-hit EDGE (hit rate −1.35pp vs overbought crossings), F2 BULL-mean/hit and BEAR-mean all NO EDGE (§I.10).** |
| I-X-03 | rgVdgR1y1Dg [05:51–06:15] (Trading 212) | Bullish divergence: price makes a lower low while "the RSI... we've got higher lows so this is a suggestion that maybe this weakness is running out of steam". | `tested` (pre-reg #10, 2026-08-14) — **F1-BULL EDGE** (§I.7): n=16,985 OOS; mean +0.80%; +0.34pp vs same-ticker (CI +0.15..+0.53, p=0.002, Holm-rejected) — the first event-level absolute EDGE in the project, the claim's bounce leg confirmed; robust across k=3/5, period 14, min-sep 10, extreme-gated; 9/10 OOS years positive. **Re-checked against historical constituents (pre-reg #13, the §5 gate, measured 2026-08-15): F1-BULL NO EDGE — n=9,384, +0.49pp vs same-ticker (CI −0.15..+0.87, p=0.072), p_input 0.072; the gate FAILS, the EDGE is corrected to the survivorship-resilient record, the family is closed (§I.10).** |
| I-X-04 | rgVdgR1y1Dg [06:39–07:03] (Trading 212) | Bearish divergence: "the market has pushed to a high pushes a little bit higher... we've got our lower high so that's a suggestion that maybe the strength is running out of steam". | `tested` (pre-reg #10, 2026-08-14) — **F1-BEAR NO EDGE** (§I.7): n=20,800 OOS; mean +0.46%; −0.04pp vs same-ticker (p=0.662) — the pullback leg is not confirmed; at N=20 it turns negative (−0.26pp). **Re-checked against historical constituents (pre-reg #13, the §5 gate, measured 2026-08-15): F1-BEAR NO EDGE holds (n=9,656, p=0.106; vs same-ticker −0.38pp, raw p=0.024, not Holm-significant); F2-BEAR-hit EDGE — bearish divergence hits positive *less* often than overbought crossings, "more reliable" in the claimed direction on the bearish side (§I.10).** |
| I-X-05 | rgVdgR1y1Dg [07:40–08:03] (Trading 212) | Stop placement for bullish divergence: "we have two obvious levels to place our stop loss beyond because by definition... the market shouldn't take out that prior extreme low". | `tested` (pre-reg #14, measured 2026-08-17, verified 2026-08-18) — **F1-BULL EDGE on the primary AND the §5 gate PASSES** (§I.11): n=16,984 OOS; breach rate of Low[t2] within N=10 47.54% vs 52.99%/53.28% → excess −5.46pp / −5.71pp (both CIs < 0, p=0.000) — the prior extreme low is breached substantially *less* often than typical fractal lows, the claim's "shouldn't" supported; F2-BULL EDGE vs OS crossings (−28.56pp). **Gate (historical-union re-run, all anchors PASSED): F1-BULL EDGE — n=9,384, breach 50.53% vs 55.37%/56.20% → −4.82pp/−5.70pp** — the first EDGE to survive the brief §5 survivorship re-check. Phase-5 trigger-check held: **NOT TRIGGERED** — a risk-placement property (where the obvious stop sits, how often it is hit), not a tradeable signal; the divergence events were already gated null on mean returns (#13). Recorded data-state deviation (the frozen #10 record is not regenerable on the 08-16-restated bars; 3 divergence events / 1 crossing across 5 year-legs, drift bound ~1.9e-4, verdicts not drift-sensitive) — recorded and quantified in the results JSON `anchor` block. |
| I-X-06 | lMZv0K71HOg [02:37–02:50] (EatSleepProfit) | "Most of the penny stocks and small caps hey these are horribly fundamentally run companies so over the long term these companies are going to fall drastically". | `tested, fade` (pre-reg #16, measured 2026-08-19, verified 2026-08-19) — **contradicted on the delisting-aware 2021 cohort** (§I.13): F2b 3y cumulative low <$10 +39.5% (n=35) vs high >$20 +6.0% (n=339), contrast +0.3352 (CI 0.009..0.727, p=0.040) **FADE** — the low-priced cohort *outperformed*, the gap accruing with horizon (1y +5.0% → 4y +42.2%); F2a index-exit NO EDGE (25.7% vs 28.0%, p=0.756); 147 no-bar death-proxy names (117 removed, 79.6%) counted, not substituted — the deaths do not flip the sign. The claim's broadest reading (literal penny stocks, <$2) is a thin slice on this data — pre-declared untested (§2). |
| I-X-07 | lMZv0K71HOg [06:56–07:04] (EatSleepProfit) | Per-trade target: "I usually like to aim for 88 to 10%" (caption garble for "8 to 10%"). | `out of scope` (process). |
| I-X-08 | kZNF5Hynk4E [06:35–07:23], [08:33–08:52] (Cameron Bennion) | Robinhood fills ~$0.05/share above the ask on a $1 stock (≈$50 per 1,000-share order); PFOF "profit of about three to four cents" per share. | `out of scope` — broker execution claims; no order data. Kept as the corpus's only execution-quality content. |
| I-X-09 | lMZv0K71HOg (whole video) (EatSleepProfit) | PDT-rule mechanics (90-day restriction, cash-account workarounds). | `out of scope` — regulatory process content. |

### I-Notes: cross-course and internal consistency (2026-08-14 scan)

> The formal course-drift comparison is now done — **§I.12** (paired rule
> map + language layer, 2026-08-18). Items 1–2 below were the informal
> precursor; item 2's tension is adjudicated in §I.12 row 2.

1. **Same core rules, repeated a decade apart:** first-new-high-candle entry
   (3 videos + B-01); first/second-pullback-only (I-B-01 + B-03); 2:1–3:1
   R:R requirement (I-E-05 + B-01/B-04); "wrong 40% still profitable" /
   "60% is enough" (I-E-05 + A-05/G-01); morning-is-best timing (I-B-05 +
   F-01). Partial answer to the standing question (are the two courses the
   same strategy?): the *rules* are consistent; the *numbers* are
   window-dependent.
2. **Cross-course tension:** B-02 (2025: "better to wait for the stock to
   pull back" — don't buy breakouts) vs I-B-03 (2015: "the apex point that's
   the breakout" — the breakout is the buy). Flagged, not adjudicated.
3. **The two 80% claims:** E-02 (ultimate-guide: "we've got an 80% chance of
   this working" — the veto-pass win-rate claim, **REJECTED × 3**, §E.7)
   and Class 1 [22:25–23:02] ("I would have a... an 80% chance of being
   right an 80% success rate... I would run that formula live for 60 days
   and... it would drop to 40%... I was writing a formula to match a
   certain set of back test results") — the teacher's own testimony that
   indicator backtests overfit and decay. Same number, opposite lessons:
   one is a claim we falsified; the other is his argument for why
   pre-registration (our §6) exists.
4. **Internal inconsistencies within the 2015–2019 corpus:** first-week P&L
   ($1,313 vs $618); trading window (9:30–12:00 vs 9:30–11:30 vs
   9:30–10:30); price filter ($2–5 in 2017 vs $2–10 in 2019); accuracy
   (100 → 87 → 75 → 68–70 → 67% across windows). Pattern: round-number
   self-reports drift with the window quoted — the E-02 lesson generalizes.
5. **Measured-findings cross-references:** I-E-02 (chasing new highs fails)
   is *consistent* with §B.5-B (Shape B, the new-high-buy adaptation, NO
   EDGE); I-F-01 (big moves get corrected; **measured**, §I.8) is the same
   mean-reversion family as §E.6's bear-day fade — the family verdict is
   split: relative correction confirmed on the UP leg, literal
   retracement falsified on both legs; I-F-02 (downside-speed asymmetry;
   **measured**, §I.9) is inverted at daily per-bar resolution (up-bars
   larger — FADE × 3) but confirmed at swing scale (S6) and on the
   reversal-speed half (F4 EDGE) — the "window" is a multi-bar property
   in this data, not a per-bar one; I-D-06 (low float) is testable with data
   already approved (§9 decision 7); I-F-05 (momentum carryover) is the
   open question family from pre-reg #4.

---

## I.5 RV-conditioning verdicts — pre-registration #8 campaign

Measured 2026-08-14 per [PREREGISTRATION.md](PREREGISTRATION.md) #8 (frozen
2026-08-14: N=10 primary — the frozen shape horizon — 0.15% round-trip cost,
**two** verdict families, Holm-corrected within each family at α=0.05, OOS
2016–2025 only, baselines bootstrapped 1,000× at fixed seed, era-matched).
Full report: `data/cache/rv_measure_report.md` (+ `rv_measure_results.json`).
No new legs: a conditioning layer on the frozen veto-pass detections
(`veto_detections_v1.csv`) — the identical input set to #3/#6/#7.

Claim as measured: "pattern trading... only works on the stocks that have
high relative volume" (Class 1 [25:49–26:36]) — RV_t = v_t / mean(v, prior
20 bars), the frozen detector's exact formula; primary threshold RV ≥ 2.0
(the frozen V = 2.0 multiplier). F1 (absolute): does the high-RV subset
beat era-matched random entries AND same-ticker? F2 (contrast): does the
high-RV subset beat the low-RV subset of the same shape? Shape A's
detector requires RV ≥ 2.0 by construction (V=2.0), so F2-A has no low-RV
cell — INCONCLUSIVE BY CONSTRUCTION, pre-declared in the pre-reg and
asserted empirically (min RV over A = 2.000000).

| # | Hypothesis (as measured) | Verdict | OOS evidence (2016–2025, N=10, after cost) |
|---|---|---|---|
| I.5-F1-A | High-RV Shape A detections beat chance + same-ticker (absolute) | `tested, no edge` — **NO EDGE** | n=3,941 high-RV; mean +0.21%; excess vs random −0.27pp (p=0.112), vs same-ticker −0.22pp (p=0.204); p_input 0.204, CI-low −0.0063 |
| I.5-F1-B | High-RV Shape B detections beat chance + same-ticker (absolute) | `tested, no edge` — **NO EDGE** | n=1,026; mean +0.24%; excess vs random −0.24pp (p=0.548), vs same −0.37pp (p=0.350); p_input 0.548, CI-low −0.0121 |
| I.5-F1-C | High-RV Shape C detections beat chance + same-ticker (absolute) | `tested, inconclusive` — **INCONCLUSIVE** | n=46 high-RV OOS — below the 100-detection floor (low cell: 234) |
| I.5-F2-A | High-RV beats low-RV Shape A (contrast) | `tested, inconclusive` — **INCONCLUSIVE BY CONSTRUCTION** | Shape A's detector requires RV ≥ 2.0; every A detection is high-RV (min asserted 2.000000); the low cell is empty |
| I.5-F2-B | High-RV beats low-RV Shape B (contrast) | `tested, no edge` — **NO EDGE** | high n=1,026 (+0.24%) vs low n=5,914 (−0.05%); excess **+0.30pp** (CI −0.27..+0.90pp, p=0.302) — the claimed direction, not significant |
| I.5-F2-C | High-RV beats low-RV Shape C (contrast) | `tested, inconclusive` — **INCONCLUSIVE** | high n=46 vs low n=234 — high cell below the floor |

Interpretation: **the claim's absolute leg — the only Phase-5-trigger
leg — is null.** On the two shapes with enough high-RV detections, the
high-RV subset does not beat random entries or same-ticker buy-and-hold
after costs; the excesses are negative on every baseline pair. The
differential leg shows a consistent but weak directional whisper in the
claim's favor: Shape B's high-minus-low contrast is positive at every
threshold (RV 2.0: +0.30pp; 1.0: +0.36pp; 3.0: +0.11pp; 5.0: +0.65pp),
but never approaches significance (best p = 0.058 at RV ≥ 1.0, a
sensitivity with no verdict) — the conditioning direction he describes
exists at the sign level in the data, on a base that never clears
chance. Shape C is starved at the primary threshold (46 of 767
detections have RV ≥ 2.0) — untestable, not refuted. The HFT-veto leg
(I-E-01) is not directly measurable on daily bars; the F2 contrast is
the proxy the data supports, and it does not clear. Near-miss
sensitivity, recorded without a verdict: at RV ≥ 1.0 — his literal
"above average for that stock" — B's subset is *below* random (−0.36pp,
p=0.048) and same-ticker (−0.40pp, p=0.040).

The pre-registered expectation was met: "F2 is the plausible family;
F1 expected NO EDGE against same-ticker" — F1 NO EDGE × 2 (+1
INCONCLUSIVE), F2 NO EDGE × 1 (+2 INCONCLUSIVE). Consistent with the
#4 lesson: selection layers (veto, RV) on these shapes have not once
cleared same-ticker buy-and-hold after costs in eight campaigns.

Project-level consequence: the first conditioning claim from the
warrior corpus is measured and null. Phase 5's trigger test remains the
positive-edge bar: unchanged, untouched, untriggered. Verification:
deterministic (results 961a65d9…, report e61a34a3…, byte-identical
across two runs); data layer independently recomputed with a separate
implementation (linear position scans, explicit prior-20 sums) —
distributions exact to 1e-9, min-A 2.000000 asserted, 0 undefined RV,
cell arithmetic consistent with the engine's standard drops.

---

## I.6 RSI 70/30 verdicts — pre-registration #9 campaign

Measured 2026-08-14 per [PREREGISTRATION.md](PREREGISTRATION.md) #9 (frozen
2026-08-14: N=10 primary — the frozen shape horizon — 0.15% round-trip cost,
**two** verdict families, Holm-corrected within F1 at α=0.05 across the two
legs, F2 a single test at α=0.05, OOS 2016–2025 only, baselines bootstrapped
1,000× at fixed seed, era-matched). Full report:
`data/cache/rsi_measure_report.md` (+ `rsi_measure_results.json`). No new
data: the frozen S&P 600 universe and bars. Cross-market caveat
pre-declared: the video demos GBP/USD; measured on US equities.

Claim as measured: "anything above seventy percent... overbought... anything
below thirty percent... oversold... due a bounce back" (Trading 212,
rgVdgR1y1Dg [03:16–03:27]) — simple-average (Cutler) RSI **as taught in the
video** (not Wilder), period 14, thresholds 70/30; legs are state-based
(every qualifying bar is a detection, matching the claim's reading "when
RSI is above 70, pullback is due"). F1 (absolute, directional per leg):
OB — does RSI > 70 give below-baseline forward returns (pullback)? OS —
does RSI < 30 give above-baseline (bounce)? F2 (contrast): does OS beat OB
(reversal symmetry)?

| # | Hypothesis (as measured) | Verdict | OOS evidence (2016–2025, N=10, after cost) |
|---|---|---|---|
| I.6-F1-OB | RSI > 70 ⇒ below-baseline 10-bar returns (pullback) | `tested, edge` — **EDGE** | n=201,419; mean +0.23%; excess vs random −0.26pp (CI −0.31..−0.20, p<0.001), vs same-ticker −0.30pp (CI −0.36..−0.25, p<0.001); p_input <0.001 (Holm gate 0.025); CI-upper −0.25pp < 0 |
| I.6-F1-OS | RSI < 30 ⇒ above-baseline 10-bar returns (bounce) | `tested, edge` — **EDGE** | n=150,236; mean +0.61%; excess vs random +0.12pp (CI +0.05..+0.19, p<0.001), vs same-ticker +0.14pp (CI +0.07..+0.23, p<0.001); p_input <0.001 (Holm gate 0.050); CI-low +0.05pp > 0 |
| I.6-F2 | OS beats OB (reversal symmetry) | `tested, edge` — **EDGE** | OB +0.23% vs OS +0.61%; contrast **+0.38pp** (CI +0.31..+0.45, p<0.001), single test at α=0.05 |

Interpretation: **the first campaign to confirm a claim's directional
structure at the state level.** Overbought detections reliably underperform
their own baselines (−0.30pp vs same-ticker) and oversold detections
reliably outperform (+0.14pp) — both Holm-rejected at p<0.001 with
150–200k detections — and the reversal symmetry is clean (+0.38pp). The
pre-registered expectation ("F1 legs expected NO EDGE") was **not met**:
the null was falsified in the claim's favor at the state level. The size is
small: +0.14pp per 10-bar trade after cost, on the OS leg.

Three caveats bound the finding before it can mean anything tradeable:

1. **Overlap (pre-reg §5; sensitivity S4).** State-based legs fire on
   consecutive bars; the iid bootstrap inflates significance. The
   pre-declared event-level view (first bar of each excursion, until
   re-entry): OB excess vs same-ticker −0.14pp (p=0.026), OS +0.10pp
   (p=0.166) — the OS bounce loses significance entirely at the event
   level; OB keeps only marginal significance, in the claim's direction.
2. **Parameter robustness (S2/S3).** The OS edge clears at 70/30 (p<0.001)
   and 90/10 (p=0.010) but **not** at 80/20 (p=0.138) or his preferred
   period 10 (p=0.286). It clears precisely at the textbook
   14/70/30 combination — the parameterization most likely to have been
   tuned on historical data.
3. **Size.** +0.14pp per 10-bar trade after cost; ~6.5 OS events per ticker
   per year (38,643 OOS crossings across 598 tickers in 10 years); the
   event-level effect is not distinguishable from noise.

Corpus tension (I-B-06) resolved toward compatibility: Class 1's "RSI is
not by any means a buy or sell indicator" vs Trading 212's reversal reading
— the state level says extremes carry directional information; the event
level says it is too weak and fragile to trade standalone. Both teachings
are consistent with the measured data.

**Phase-5 trigger-check conversation (pre-reg #9 §4: F1-OS EDGE is the sole
pre-registered trigger).** Held on this evidence. Trigger-check verdict:
**NOT TRIGGERED.** The state-level EDGE is overlap-inflated (the
pre-declared event-level correction is p=0.166), the parameter neighborhood
is fragile (80/20 and period 10 fail), and the absolute size is a fraction
of a percent per trade. The directional tendency is real — overbought
drifts below, oversold drifts above, the ticker's own baseline — and too
small to clear the brief §1 bar. Phase 5 remains **not triggered** after
nine campaigns. Revisiting this requires a fresh pre-registration under the
frozen trigger rules.

Verification: deterministic (results 93537c3f…, report 46c84b42…,
byte-identical across two runs); the data layer was independently recomputed
with a separate implementation (explicit per-bar loop RSI with window sums):
RSI exact to 2.8e-14, detection counts and forward-return means exact
(201,419 / 150,236; +0.00233325 / +0.00614773), warm-up count exact (7,409),
RSI bounds [0, 100] clean over all 598 tickers with bars.

---

## I.7 RSI divergence verdicts — pre-registration #10 campaign

> **UPDATED 2026-08-16 — superseded by the brief §5 survivorship re-check
> (pre-reg #13).** The verdicts below are the current-constituent record
> (OOS 2016–2025), retained verbatim — ledger verdicts are logged, never
> deleted. On the historical-constituent union (OOS 2022–2025) the F1-BULL
> EDGE is **NO EDGE** — the §5 gate FAILS and the family is closed — and
> F2-BEAR-hit flips to **EDGE** (reliability in the claimed direction on
> the bearish side); the frequency ratio 0.3012 holds. Full re-check
> table: §I.10.

Measured 2026-08-14 per [PREREGISTRATION.md](PREREGISTRATION.md) #10 (frozen
2026-08-14: simple-average RSI period 10 primary (14 sensitivity); strict
k=2 fractal swings on Low/High — ties never form a swing (k=3/5
sensitivities); consecutive swing pairs only, disjoint fractal windows
(min separation 5); **confirmation-bar timing** — a k-fractal at t2 is
knowable only at close t2+k, so the signal bar is t2+k, entry open t2+k+1,
exit close t2+k+N; the chartist's-eye variant (signal at the pivot) is
sensitivity S8 with its pre-declared selection-tilt caveat; N=10 primary,
0.15% round-trip cost, two verdict families, Holm at α=0.05, OOS 2016–2025
only, baselines bootstrapped 1,000× at fixed seed, era-matched). Full
report: `data/cache/divergence_measure_report.md`
(+ `divergence_measure_results.json`). No new data: the frozen S&P 600
universe and bars. Cross-market caveat pre-declared: the video demos
GBP/USD; measured on US equities.

Claim as measured: bullish divergence (price lower low + RSI higher low) ⇒
bounce (I-X-03); bearish divergence (price higher high + RSI lower high) ⇒
pullback (I-X-04); "a lot less common so arguably a bit more reliable" vs
the 70/30 signals (I-X-02). F1 (absolute, directional per leg): BULL — do
bullish divergences beat era-matched random entries AND same-ticker
buy-and-hold? BEAR — do bearish divergences underperform both? F2
(reliability contrast): divergence vs 70/30 crossings at the same period,
per leg, on mean return AND hit rate (ret > 0 after cost).

| # | Hypothesis (as measured) | Verdict | OOS evidence (2016–2025, N=10, after cost) |
|---|---|---|---|
| I.7-F1-BULL | Bullish divergence ⇒ above-baseline 10-bar returns (bounce) | `tested, edge` — **EDGE** | n=16,985; mean +0.80%; win 54.12%; excess vs random +0.31pp (CI +0.11..+0.50, p=0.002), vs same-ticker +0.34pp (CI +0.15..+0.53, p=0.002); p_input 0.002 (Holm gate 0.025); CI-low +0.11pp > 0 |
| I.7-F1-BEAR | Bearish divergence ⇒ below-baseline 10-bar returns (pullback) | `tested, no edge` — **NO EDGE** | n=20,800; mean +0.46%; win 50.83%; excess vs same-ticker −0.04pp (CI −0.20..+0.11, p=0.662); p_input 0.662 |
| I.7-F2-BULL-mean | Bullish divergence beats oversold crossings on the mean | `tested, edge` — **EDGE** | div +0.80% vs cross +0.62%; contrast **+0.18pp** (CI +0.03..+0.34, p=0.012), Holm gate 0.025 |
| I.7-F2-BULL-hit | Bullish divergence beats oversold crossings on hit rate | `tested, edge` — **EDGE** | hit 54.12% vs 52.63%; contrast **+1.50pp** (CI +0.63..+2.29, p<0.001), Holm gate 0.0125 |
| I.7-F2-BEAR-mean | Bearish divergence beats overbought crossings on the mean | `tested, fade` — **FADE** | div +0.46% vs cross +0.25%; contrast **+0.21pp** (CI +0.07..+0.34, p<0.001) — divergence's mean is *above* the crossing mean: less pullback, the opposite of "more reliable" |
| I.7-F2-BEAR-hit | Bearish divergence beats overbought crossings on hit rate | `tested, no edge` — **NO EDGE** | hit 50.83% vs 50.29%; contrast +0.54pp (CI −0.21..+1.30, p=0.176) |
| I.7-FREQ | "A lot less common" — the frequency half (measurement, no verdict) | `tested, measurement` — **CONFIRMED** | 37,929 divergences vs 124,298 crossings → ratio **0.3051** (ticker-cluster CI 0.3022..0.3081); ~2.8 BULL events per ticker per year; at period 14, 0.4287 |

Interpretation: **the first event-level absolute EDGE in the project's
history — and it lands on the bullish leg of the claim, exactly as taught.**
Bullish divergence (price lower low, RSI higher low) predicts a bounce:
+0.80% per 10-bar trade after cost, +0.34pp above the ticker's own
buy-and-hold, Holm-rejected with 16,985 events, robust across every
structural sensitivity (k=3 +0.39pp, k=5 +0.50pp, period 14 +0.23pp,
min-sep 10 +0.30pp, extreme-gated +0.45pp) and positive in 9/10 OOS years
(only 2018: −0.16%). The reliability contrast finds bullish divergence
genuinely more reliable than its own baseline — the oversold crossings,
which already carry the RSI-70/30 reversal tendency. The bearish leg fails
both tests: no absolute pullback tendency (NO EDGE; turns negative at
N=20, −0.26pp) and *less* reliable than overbought crossings on the mean
(FADE). The I-X-02 "more reliable" claim is half right: the bullish
divergence is more reliable; the bearish divergence is less.

Five caveats bound the finding before it can mean anything tradeable:

1. **Survivorship (brief §5 gate).** The universe is *current*
   constituents; the brief pre-registers that any positive result must be
   re-checked against historical constituents before being trusted. This
   is the first positive F1 result that gate exists for — the re-check is
   the explicit path forward (see the trigger-check below).
2. **Size.** +0.34pp per 10-bar trade after cost on ~2.8 BULL events per
   ticker per year — real but fractional, and execution friction is
   unvalidated.
3. **Half-confirmed claim.** F1-BEAR NO EDGE + F2-BEAR-mean FADE — the
   bearish teaching (I-X-04) is not confirmed and the reliability claim
   (I-X-02) fails on that side.
4. **Selection tilt (S8, pre-declared).** The chartist's-eye variant
   (signal at the pivot, entry +1) shows BULL +2.06pp / BEAR −1.66pp —
   far larger than the primary's honest confirmation-bar timing. The
   conservative number is the real one.
5. **Cross-market translation.** Taught on GBP/USD daily; measured on US
   equities (pre-declared).

Sensitivities (exploratory, no verdicts): S1 horizons — the BULL edge
accrues over the horizon (N=1 ≈ 0, N=5 +0.09pp, N=20 +0.53pp) while BEAR
goes negative at N=20; S5 per-year — BULL positive 9/10 OOS years; S6 IS
record — BULL +0.71% (win 53.3%), BEAR +0.41% (win 52.8%); period-14
frequency ratio 0.4287.

**Phase-5 trigger-check conversation (pre-reg #10 §4: F1-BULL EDGE is the
sole pre-registered trigger).** Held on this evidence. Trigger-check
verdict: **NOT TRIGGERED.** The brief §5 survivorship gate is unmet — a
positive result on current constituents must be re-checked against
historical constituents before being trusted, and that is the explicit
next step (a new data artifact, requiring a fresh pre-registration). The
size is a fraction of a percent per trade on ~2.8 events per ticker per
year, and the claim is only half-confirmed (bearish leg NO EDGE / FADE).
The bullish-divergence bounce is real, event-level, and robust within the
current-constituent universe — and unvalidated outside it. Phase 5 remains
**not triggered** after ten campaigns.

Verification: deterministic (results 674b2d95…, report 826f0bbf…,
byte-identical across two runs); the data layer was independently recomputed
with a separate implementation (explicit per-bar loop RSI with window sums,
explicit swing/event/crossing loops, engine-identical forward returns): all
22 checks exact — RSI vs the tool's rsi_series max diff 0.0 on 40 tickers;
per-leg OOS counts and means exact to 1e-12; frequency counts exact at
periods 10 and 14; min_t1=10 ≥ period; RSI bounds [0, 100] clean; 0 bad
signals.

---

## I.8 Big-move correction verdicts — pre-registration #11 campaign

Measured 2026-08-14, verified 2026-08-15 per [PREREGISTRATION.md](PREREGISTRATION.md) #11 (frozen 2026-08-14: **excursion-first event-level** definition — a big-move event at bar t iff |close_t − close_{t−L}| ≥ 3 × ATR_t, L=10 (τ=2/5, L=5 sensitivities); ATR_t = the simple mean of the 14 true ranges ending at t (no ATR teaching in the corpus — the definition is pre-registered; Wilder kept as a sensitivity); one event per maximal leg run; N=10 primary, 0.15% round-trip cost, **two** verdict families, Holm-corrected within each family across the two legs at α=0.05, OOS 2016–2025 only, baselines bootstrapped 1,000× at fixed seed, era-matched). Full report: `data/cache/bigmove_measure_report.md` (+ `bigmove_measure_results.json`). No new data: the frozen S&P 600 universe and bars. Cross-market caveat pre-declared: taught in a 2015 intraday classroom; measured on US equity daily bars.

Claim as measured: "almost all of the big moves will eventually be corrected" (jfe1Zl-5EQI [16:01–16:09]; "what goes up must come down and what goes down must come back up" [15:05–15:09]) — the rationale for the reversal strategy. F1 (absolute, directional per leg): UP — do big up-moves give **below-baseline** 10-bar returns (corrected)? DOWN — do big down-moves give **above-baseline** (recovered)? F2 (the ledger's literal reading, "retrace ≥ half within 5–10 sessions"): do big moves cross their own midpoint (close_t + close_{t−L})/2 within N=10 more often than era-matched typical bars?

| # | Hypothesis (as measured) | Verdict | OOS evidence (2016–2025, N=10, after cost) |
|---|---|---|---|
| I.8-F1-UP | Big up-moves ⇒ below-baseline 10-bar returns (corrected) | `tested, edge` — **EDGE** | n=35,908; mean +0.03%; win 49.00%; excess vs random −0.46pp (CI −0.59..−0.33, p<0.001), vs same-ticker −0.48pp (CI −0.61..−0.36, p<0.001); p_input <0.001 (Holm gate 0.025); CI-upper −0.36pp < 0 |
| I.8-F1-DOWN | Big down-moves ⇒ above-baseline 10-bar returns (recovered) | `tested, no edge` — **NO EDGE** | n=29,039; mean +0.48%; win 52.82%; excess vs random −0.01pp (CI −0.16..+0.15, p=0.950), vs same +0.01pp (CI −0.14..+0.17, p=0.866); p_input 0.950 |
| I.8-F2-UP | Big up-moves retrace ≥ half within 10 sessions more often than typical bars | `tested, fade` — **FADE** | 19.56% vs 32.34% (n_random 716,712); contrast **−12.77pp** (CI −13.08..−12.44, p<0.001), Holm gate 0.025 |
| I.8-F2-DOWN | Big down-moves recover ≥ half within 10 sessions more often than typical bars | `tested, fade` — **FADE** | 22.49% vs 38.01% (n_random 635,474); contrast **−15.53pp** (CI −15.89..−15.18, p<0.001), Holm gate 0.050 |
| I.8-FREQ | Frequency (measurement, no verdict) | `tested, measurement` — **REPORTED** | OOS events UP 35,997 / DOWN 29,110; all-era (warm-up excluded) UP 73,503 / DOWN 57,173; state-level OOS bars UP 111,016 / DOWN 87,803; warm-up UP 761 / DOWN 618 |

Interpretation: **the project's second event-level absolute EDGE — and it
lands on the correction leg, as a negative-return finding.** After ≥3-ATR
up-moves, 10-bar returns are +0.03% after cost — essentially flat —
versus +0.48% on the same tickers' buy-and-hold: the pop is followed by
underperformance, Holm-rejected below both baselines. The DOWN leg —
"what goes down must come back up" — is null at the 3-ATR threshold
(p=0.950) and *contradicted* at τ=5 (mean −0.90%; −1.36pp vs same-ticker,
p<0.001): extreme down-moves underperform their own baselines. And the
ledger's literal reading fails in both directions, decisively: big moves
cross their own midpoint within 10 sessions 12.8–15.5pp **less** often
than typical bars (at N=5, the claim's own "5–10 sessions" range,
−15.2pp/−18.1pp). The relative regularity ("corrected" = below-baseline
drift) is real; the literal regularity ("retrace half") is false. The
magnitude gradient on the DOWN leg (τ=2 +0.24pp, p<0.001 → τ=3 ≈ 0 →
τ=5 −1.36pp, p<0.001) shows "recovery" exists only for weak moves. The
state-level view (S5, overlap-inflated) has *both* legs below baselines
(UP −0.40pp / DOWN −0.23pp) — underperformance-after-extremes, coherent
with pre-reg #4's continuation EDGE × 3 on our breakout signals:
momentum populations drift relative to their tickers; they do not snap
back to the midpoint. The pre-registered expectation ("DOWN/bounce leg
the more likely; F1-UP expected NO EDGE or FADE") was **not met —
inverted on both legs**.

Three caveats bound the finding:

1. **Overlap (pre-declared).** Excursion-first events are separated by
   ≥ 1 bar, but N=10 windows can overlap for near runs; bootstrap CIs use
   iid resampling, so effective sample size is below the row count.
2. **Survivorship.** Current-constituent universe — strengthens these
   nulls; and this is a negative-return finding, so the brief §5
   positive-result gate does not apply.
3. **Intraday→daily translation.** Taught in a 2015 intraday classroom;
   measured on US equity daily bars.

Sensitivities (exploratory, no verdicts): S1 — the UP correction accrues
over the horizon (N=1 −0.06pp, N=5 −0.25pp, N=20 −0.71pp); S2 — τ=2 UP
−0.29pp / DOWN **+0.24pp** (p<0.001, the only positive DOWN excess), τ=5
UP −0.46pp (p=0.030) / DOWN −1.36pp (p<0.001); S3 L=5 UP −0.34pp / DOWN
−0.38pp; S4 ATR-7 UP −0.53pp, Wilder UP −0.45pp (DOWN n.s. in both);
S5 state-level UP −0.40pp / DOWN −0.23pp; S6 per-year — UP's OOS means
negative in 6/10 years (2022 −1.15%, 2018 −0.36%) and positive in 4
(2023 +0.98%, 2016 +0.87%); DOWN's positive in 8/10 (2021 +1.99%, 2024
+1.64%), with 2020's crash the single big negative (−2.26%); S7 IS
record — UP +0.31% (win 50.83%), DOWN +0.77% (win 52.71%); S8
extreme-midpoint F2 — UP −18.31pp / DOWN −21.24pp.

**Phase-5 trigger (pre-reg #11 §4: only an F1-DOWN EDGE is the sole
pre-registered trigger): did not fire — F1-DOWN is NO EDGE (p=0.950), so
no trigger-check conversation was held.** (F1-UP EDGE is a negative-return
finding and F2 is differential; neither can trigger by design.) Phase 5
remains **not triggered** after eleven campaigns.

Verification: deterministic (results 660F227C…, report CE1145F7…,
byte-identical across two runs); the data layer was independently
recomputed with a separate implementation — all 61 checks exact: per-bar
TR loop bit-exact vs the tool's tr_series (max diff 0.0 on 10 sampled
tickers); ATR-14 loop within 1 ulp (max 3.109e-15); the frozen
rolling-mean ATR bit-pattern is unreproducible by any per-bar summation
order (probed five orderings across 2.8M bars, worst 1.7e-13), so
detection was re-checked against the tool's own ATR values with every
differing event proven boundary-exact (at τ=2 exactly one flip — LEU
2019-04-10: move == 2×ATR bit-exact, rel=0.00e+00); all-era and OOS event
counts, F1 means/wins/CIs, F2 rates, and every pre-declared sensitivity
count exact; warm-up counts exact; 0 bad signals.

---

## I.9 Speed-asymmetry verdicts — pre-registration #12 campaign

Measured 2026-08-15, verified 2026-08-15 per [PREREGISTRATION.md](PREREGISTRATION.md) #12 (frozen 2026-08-15: **bar-geometry measurement, no forward returns** — speed = per-bar move size |close_t/close_{t−1} − 1|; A1 per-bar directional asymmetry via F1 (absolute, per leg vs the era-matched unconditional mean |r|, joint one-sample bootstrap, Holm across the two legs) + F2 (the DOWN−UP contrast, two-sample bootstrap); A2 reversal speed via F4 on the frozen pre-reg #11 UP events (L=10, τ=3, excursion-first; first crossing bar j ∈ [1,N] of the midpoint (close_t + close_{t−L})/2; paired contrast retrace-rate − move-rate; equivalence retrace-rate > move-rate ⇔ j < L/2 = 5); N=10, B=1,000, seed 20260813, α=0.05, OOS 2016–2025 only). Full report: `data/cache/speed_measure_report.md` (+ `speed_measure_results.json`). No new data: the frozen S&P 600 universe and bars. The Phase-3 engine's `measure_returns` was NOT invoked — the claim contains no return prediction; Phase 5 is not implicated by construction.

Claim as measured: "the Bulls take the stairs and the Bears take the window" (jfe1Zl-5EQI [28:28–28:47], corroborated [17:34–17:37]) — A1: down-bars' mean per-bar size exceeds up-bars' (the asymmetry, unconditional); A2: the retracement of a big up-move covers its distance faster than the move did ("hours up, minutes down").

| # | Hypothesis (as measured) | Verdict | OOS evidence (2016–2025, N=10) |
|---|---|---|---|
| I.9-F1-UP | Up-bars smaller than typical bars ("stairs") | `tested, fade` — **FADE** | n=1,371,291 bars (UP 689,944 / DOWN 660,952 / ZERO 20,395); mean up +0.0189 vs typical +0.0184; excess **+0.0006** (CI +0.0005..+0.0006, p<0.001), Holm gate 0.025 — up-bars *larger* than typical, claim contradicted |
| I.9-F1-DOWN | Down-bars larger than typical bars ("window") | `tested, fade` — **FADE (knife-edge)** | mean down +0.0183; excess **−0.00004** (CI −0.00009..−0.00000008, p=0.050 exactly at the gate) — CI-upper −8e-8 ≈ 0; boundary artifact, treat as NO EDGE substantively |
| I.9-F2 | Down-bars larger than up-bars (the asymmetry itself) | `tested, fade` — **FADE** | DOWN − UP **−0.0006** (CI −0.0007..−0.0005, p<0.001), Holm gate 0.050 — up-bars ~6bp larger, claim contradicted in sign |
| I.9-F4 | Big up-moves' retracements outpace the moves (A2) | `tested, edge` — **EDGE** | n=35,997 (retraced 11,113 = 30.9%, non 24,795, tail-dropped 89); mean j 5.40; **+0.0040** per bar (CI +0.0037..+0.0044, p<0.001) — given-back-fast, as claimed |
| I.9-FREQ | Frequency (measurement, no verdict) | `tested, measurement` — **REPORTED** | OOS UP 689,944 / DOWN 660,952 / ZERO 20,395 / all 1,371,291; down share 0.4820; index-0 excluded 599; bad prior 0 |

Interpretation: **A1 — the claim's per-bar half — is falsified in the
OPPOSITE direction of the claim.** Up-bars average ~6bp larger than
down-bars (F2, Holm-rejected), and the top-|r| decile is not
down-concentrated (down share 0.4795 vs 0.4820 overall, −0.25pp, S8) —
the "window" (a small number of very large fast down-bars) does not
exist at daily per-bar resolution. The pre-registered expectation
(negative-skew regularity ⇒ F1/F2 confirm, "possibly trivially") was
inverted; the stability of the inversion is the point — negative across
mean/median (S1 −0.0002)/candle-sign (S2 −0.0001)/per-ticker (S3:
146/599 tickers positive, mean −0.0008, cluster CI −0.0010..−0.0007,
all p<0.001)/IS (S4 −0.0014)/per-year (S5: 9/10 years negative, 2018
+0.06pp the only exception). The one structure-level corroboration of
the claim is S6: multi-bar down-swings cover distance faster per bar
than the preceding up-swings (rate contrast +0.0131/+0.0140/+0.0354 at
k=2/3/5, all p<0.001) — declines are faster *across* bars even though
no single daily down-bar is larger. That is the honest daily
reconciliation of the claim: the "window" is a multi-bar property in
this data, not a per-bar one. **A2 — the reversal-speed half — is
confirmed:** among the 30.9% of big up-moves that retrace ≥ half within
10 bars, the retracement outpaces the move (+0.40pp per bar,
Holm-rejected), concentrated in the claim's own short horizon (N=5
+0.0113, p<0.001; N=20 null, p=0.950) and robust across event
populations (τ=2 +0.0052, τ=5 +0.0034, both p<0.001). The mean j 5.40 >
5 with a positive contrast is the pre-registered convexity in 1/j — the
retraced set's bimodal j distribution (mass at j≈1–2 from overnight
gaps, mass at 6–9) — not a contradiction.

Caveats bound the finding:

1. **Intraday→daily translation (central, pre-declared).** The claim is
   about minutes vs hours; daily bars measure per-bar magnitude, and
   overnight gaps register as fast (they carry much of F4's j≈1–2 mass).
   This is the honest daily adaptation of the claim's size structure,
   not a test of intraday speed — the "window" may still hold intraday.
2. **Survivorship.** Current-constituent universe; the brief §5
   positive-result gate does not apply — no forward returns are
   measured.
3. **State-level per-bar statistics.** F1/F2 pool 1.37M serially
   dependent bars; iid bootstrap CIs — effective sample below row count.
4. **F1-DOWN's FADE is a knife-edge boundary artifact** (CI-upper −8e-8,
   p=0.050 exactly at the gate) — treat as NO EDGE substantively; only
   F1-UP FADE and F2 FADE carry the substantive A1 rejection.
5. **F4 is conditional.** It measures speed given a retracement (30.9%
   of events); the 69.1% that do not retrace are pre-reg #11 F2's FADE
   (big moves retrace half *less* often than typical bars).

Sensitivities (exploratory, no verdicts): S1 median contrast −0.0002
(p<0.001; the DOWN-leg median excess is +0.0001 — the median view
differs from the mean because zero bars sit below both leg medians);
S2 candle-sign F2 −0.0001 (red−green, p<0.001); S3 per-ticker cluster
CI −0.0010..−0.0007 (p<0.001); S4 IS F2 −0.0014 (p<0.001), IS F1-DOWN
not significant (p=0.078); S5 nine of ten OOS years negative (2020
−0.17pp, 2021 −0.15pp largest; 2018 +0.06pp the exception); S6
swing-scale contrast positive at k=2/3/5 (the claim confirmed across
bars); S7 F4 variants — N=5 EDGE (+0.0113), N=20 null (p=0.950), τ=2
+0.0052 (n=64,694), τ=5 +0.0034 (n=5,416); S8 tail decile not
down-concentrated (−0.25pp).

**Phase-5 trigger (pre-reg #12 §2: no family measures forward returns —
the claim is about bar geometry, not profitability): the trigger cannot
fire from this campaign by construction, so no trigger-check
conversation was held.** Phase 5 remains **not triggered** after twelve
campaigns.

Verification: deterministic (results 1B1DFC00…, report 528E205F…,
byte-identical across two runs); the data layer was independently
recomputed with a separate implementation — all 75 checks exact:
population counts and per-leg means bit-exact (n_all 1,371,291; mean_all
0.018366437482; down share 0.4819925165); leg-excess identity holds to
1e-9 including the zero-bar term (2.732e-04 = n_zero·mean_all/n_all);
the F4 population re-detected with an independent per-bar TR/ATR loop
(35,997 events; n_retraced 11,113, mean_j 5.4031314677, crossing share
0.309485351 all exact; 148 warm-up OOS events — post-2016-listed
tickers — proven excluded via the warmup flag); S2 candle counts/means;
S3 per-ticker contrasts exact (146/599 positive; mean −0.000842796413);
S5 per-year; S6 swing pair counts exact with analytic-vs-bootstrap means
within Monte Carlo error; S8 tail decile; verdict/Holm-gate consistency;
and every pre-declared sensitivity parity-checked with a fresh seed
(est/CI/p within tolerance); fingerprints exact (measure code
3fbdab9922c5…, universe 5e6f45a3c791…).

---

## I.10 RSI divergence re-check — pre-registration #13 campaign (the brief §5 survivorship gate)

Measured 2026-08-15, verified 2026-08-16 per [PREREGISTRATION.md](PREREGISTRATION.md) #13 (frozen 2026-08-15: **the historical-constituent re-check of pre-reg #10** — the brief §5 gate: "any positive result must be re-checked against historical constituents before being trusted". Universe = the union of 5 annual snapshots (2021-06-30 … 2025-06-30; revids 1030576925 / 1094398428 / 1161531950 / 1231006396 / 1297281645, 601/601/601/602/602 tickers) of the Wikipedia *List of S&P 600 companies* revision history = **904 names incl. ~330 delisted/removed** (artifact `data/cache/universe_sp600_hist_2026-08-15.csv` + `hist_universe_provenance.json`, builder `tools/build_hist_universe.py`; churn validated: adjacent-year overlaps 536/518/519/528, 2021-06→2026-08 survival 274). Measurement = the **frozen pre-reg #10 code byte-identical**, only runtime-rebound: universe CSV, `ERA_OOS` "2022-01-01" on both `measure.ERA_OOS` and `measure_divergence.ERA_OOS`, results/report paths; the pre-registered label patch list (§2). OOS = 2022–2025 only (4 years — every OOS month bracketed by a snapshot; the 2016–2021 OOS years are NOT measured, a documented §3 blind spot; IS 2000–2021 descriptive only). All parameters identical: simple-average RSI period 10 (14 as S3), strict k=2 fractal swings on Low/High, consecutive pairs, min-sep 5, signal bar t2+k (confirmation-bar timing), N=10, COST 0.0015, bootstrap B=1000 seed 20260813, Holm α=0.05, floor 100, warm-up 60, sensitivities S1–S8). Full report: `data/cache/divergence_hist_measure_report.md` (+ `divergence_hist_measure_results.json`).

Claim as measured: identical to §I.7 — bullish divergence ⇒ bounce (I-X-03); bearish divergence ⇒ pullback (I-X-04); "a lot less common so arguably a bit more reliable" vs the 70/30 signals (I-X-02). **Data limitation materialized (pre-registered §6): 199 of the 904 names are purged from Yahoo's data entirely** — the chart API 404s ("No data found, symbol may be delisted") at every window; the search API finds nothing for representative purged names (FL, CIVI, AMWD; CSWI re-tickered to CSW); a 45-minute per-minute probe recovered nothing, ruling out throttling. **None of the 199 are current S&P 600 members.** Measured on the 706 names with bars — flagged, NOT substituted.

| # | Hypothesis (as measured) | Verdict | OOS evidence (2022–2025, N=10, after cost) |
|---|---|---|---|
| I.10-F1-BULL | Bullish divergence ⇒ above-baseline 10-bar returns (bounce) — **the gate test** | `tested, no edge` — **NO EDGE** | n=9,384; mean +0.59%; win 50.98%; excess vs random +0.43pp (CI −0.10..+0.81, p=0.064), vs same-ticker +0.49pp (CI −0.15..+0.87, p=0.072); p_input 0.072 (Holm gate 0.025); CI-low −0.15pp < 0 |
| I.10-F1-BEAR | Bearish divergence ⇒ below-baseline 10-bar returns (pullback) | `tested, no edge` — **NO EDGE** | n=9,656; mean −0.12%; win 47.06%; excess vs same-ticker −0.38pp (CI −1.03..−0.05, p=0.024); p_input 0.106 (gate 0.050) — raw-significant, not Holm-significant |
| I.10-F2-BULL-mean | Bullish divergence beats oversold crossings on the mean | `tested, no edge` — **NO EDGE** | div +0.59% vs cross +0.47%; contrast +0.14pp (CI −0.34..+0.50, p=0.492) |
| I.10-F2-BULL-hit | Bullish divergence beats oversold crossings on hit rate | `tested, no edge` — **NO EDGE** | hit 50.98% vs 50.14%; contrast +0.83pp (CI −0.29..+1.97, p=0.140) |
| I.10-F2-BEAR-mean | Bearish divergence beats overbought crossings on the mean | `tested, no edge` — **NO EDGE** | div −0.12% vs cross −0.03%; contrast −0.10pp (CI −0.33..+0.12, p=0.410) |
| I.10-F2-BEAR-hit | Bearish divergence beats overbought crossings on hit rate | `tested, edge` — **EDGE** | hit 47.06% vs 48.40%; contrast **−1.35pp** (CI −2.41..−0.31, p=0.012), Holm gate 0.0125 — bearish divergence hits positive *less* often than overbought crossings: "more reliable", as claimed |
| I.10-FREQ | "A lot less common" — the frequency half (measurement, no verdict) | `tested, measurement` — **CONFIRMED** | 19,207 divergences vs 63,763 crossings → ratio **0.3012** (ticker-cluster CI 0.2972..0.3052); at period 14, 0.4286 |

**§5 gate decision: FAILS.** F1-BULL NO EDGE on the re-check window → **I-X-03's EDGE is corrected to the survivorship-resilient record: the direction persists (est +0.49pp vs same-ticker; 2022 +0.48 / 2023 +0.27 / 2024 +0.86 / 2025 +0.82pp — all four OOS years positive) but is not distinguishable from chance on the 4-year / 904-name window. The family is closed with the re-check as definitive; Phase 5 stays untriggered; no trigger-check conversation is held** (per pre-reg #13 §5, reserved for a surviving EDGE).

Interpretation: the re-check window halves the pre-reg #10 sample (n=16,985 → 9,384) and era-matches the baselines to 2022–2025 only, roughly doubling the confidence interval — the current-constituent excess (+0.34pp, CI-low +0.11pp) does not clear zero on the corrected universe, though its point estimate does not collapse. The §5 direction (survivorship inflates returns) is consistent with the outcome. F1-BEAR's per-ticker underperformance (−0.38pp, raw p=0.024) is not Holm-significant. The F2-BEAR-hit EDGE flips from pre-reg #10's NO EDGE — the bearish side's reliability shows in hit rate on the corrected window, while the bullish F2 contrasts (both EDGE in #10: +0.18pp / +1.50pp) become NO EDGE (+0.14pp / +0.83pp). The I-X-02 "more reliable" claim, half right on the current universe, is now supported on the bearish side and not on the bullish side.

Caveats bound the record:

1. **Partial correction (documented).** 199 of 904 names have no data (Yahoo purge); 0 are current members; the measured 706 include 229 sibling former members (AAON, ADC, ANF, …) — the gate's direction (missing delisted names understate the correction) is documented in pre-reg #13 §8.
2. **Blind spot.** 2016–2021 OOS is not measured (pre-reg #13 §3): tickers removed before the first snapshot are absent from the union, so those years would re-introduce the very bias the gate removes.
3. **IS descriptive only.** S6 IS rows (BULL n=33,111, +0.78%, win 53.54%) carry no verdict — no IS-era membership data.
4. **Selection tilt (S8, pre-declared).** chartist's-eye BULL +2.22pp (p=0.034) — the look-ahead tilt present as pre-registered; the honest number is the primary's confirmation-bar timing.

Sensitivities (exploratory, no verdicts): S1 N=20 BULL +0.75pp (p=0.082), BEAR −0.70pp (p=0.000); S2 k=3 BULL +0.63pp vs same (p=0.046), k=5 +0.64pp (p=0.080); S3 period 14 BULL NO EDGE (p=0.208), BEAR vs same −0.55pp (p<0.001); S4 min-sep 10 BULL +1.12pp (p=0.016); S7 extreme-gated BULL +0.54pp (p=0.092); S5 per-year above.

Verification: deterministic (results 45d6ebe9d882…, report 125ad2af14d5…, byte-identical across two runs); the data layer was independently recomputed with a separate implementation importing nothing from the frozen stack (per-bar Cutler-RSI loop, explicit swing/event loops, engine-identical forward returns, frozen-identical baseline construction — event-count-weighted same-ticker pools, whole-universe random pool, paired bootstrap with a fresh seed 20260815): BULL n=9,384 exact; mean_ret 0.005930043180491732 exact to 1e-8; excess bootstrap means 0.00493 vs driver 0.00490 (same-ticker) and 0.00393 vs 0.00431 (random), both within 6e-4; the verdict's CI-low −0.0015 lies inside the verifier's own CI ±1.5e-3 — **PASSED**. Input fingerprints: universe 62f681d58cdb…, measure code 85f2ae0d4a1e… (Phase-3 engine c7421fbf… imported unchanged — no frozen file modified).

---

## I.11 Stop-placement verdicts — pre-registration #14 campaign (I-X-05)

Claim (I-X-05, rgVdgR1y1Dg [07:40–08:03]): for a bullish divergence, "we
have two obvious levels to place our stop loss beyond because by
definition... the market shouldn't take out that prior extreme low".
Measured 2026-08-17, verified 2026-08-18, against the frozen pre-reg #10
BULL event set (pre-reg #14 §2): stop level L = Low[t2], breach ⇔
min(Low[s+1..s+N]) < L (intrabar, strict), N=10 primary, signal s = t2+2,
OOS 2016–2025.

| Verdict | Result (primary) | p_input / Holm | Gate (pre-reg §3, historical union) |
|---|---|---|---|
| **F1-BULL EDGE** | n=16,984 OOS; breach 47.54% vs random 52.99% / same-ticker 53.28% → excess −5.46pp (CI −6.47..−4.44) and −5.71pp (CI −6.75..−4.66), p=0.000 | 0.000, rejected (CI-upper −4.66pp < 0) | **PASSES** — n=9,384; breach 50.53% vs 55.37%/56.20% → −4.82pp (CI −6.28..−3.43) and −5.70pp (CI −6.98..−3.58), p=0.000; all event-set anchors PASSED |
| **F2-BULL EDGE** | contrast vs OS crossings −28.56pp (CI −29.58..−27.58, p=0.000); n_cross 57,427 | 0.000, rejected | −26.87pp (CI −28.20..−25.62, p=0.000); n_cross 31,509 |

**Reading.** The claim's "shouldn't" is supported: the divergence's prior
extreme low is breached within 10 bars substantially LESS often than
typical fractal lows (and far less than oversold-crossing references,
whose age asymmetry is documented conservative). The stop below the prior
extreme low is a genuinely tight, rarely-hit level — a defensive
risk-placement property. **The §5 gate PASSES** — the first EDGE in the
project to survive the historical-constituent re-check (distinct from
pre-reg #13, where I-X-03's mean-return EDGE failed on the corrected
universe). The Phase-5 trigger-check conversation was held with the
surviving evidence: **NOT TRIGGERED** — the finding is a risk-placement
property, not a tradeable signal (no entry/exit construction, no
per-trade size), and the divergence events themselves were already gated
null on mean returns (#13).

**Data-integrity deviation (recorded, quantified, guarded).** The frozen
#10 record is NOT regenerable on the current (08-16-restated) bars: the
frozen pipeline yields per_year BULL 34,075 / BEAR 42,757, fam1 n 16,984,
freq 17,016/20,910 vs the frozen 34,076/42,759/16,985/17,017/20,912 — a
3-divergence-event, 1-OB-crossing delta across 5 year-legs (2021 BULL −1;
2016/2017/2024 BEAR −1; 2025 BEAR +1); the frozen #13 hist record
regenerates exactly on the same data, bracketing the change to the
08-15→08-16 window, and the 08-13-era bytes are unrecoverable (fetch log
has no hashes; no raw downloads exist). Handled as a recorded DEVIATION:
the OOS BULL set under test differs from frozen by exactly 1 event;
drift-materiality bound ≈1.9e-4 (~60× below the bootstrap CI width);
neither family's decisive CI bound falls within it — verdicts not
drift-sensitive. NOT a parameter change; no frozen file modified.

Measurement rows (primary): stop distance open[s+1] → Low[t2] mean 5.28%
(median 4.24%, p10 1.30%, p90 10.30%) = 1.40 ATR14 units (median 1.28);
breach-loss −3.66% vs continue-gain +4.55% (combined +0.64%,
n_breached 8,075); all 26 per-year breach rates (0.37–0.52) below the OOS
random baseline 0.5299; IS descriptive n=17,091 breach 46.37%.

Sensitivities (primary, exploratory — no verdicts): S1 N=5 0.359 vs
0.403/0.405, N=20 0.595 vs 0.647/0.650 (edge persists at both horizons);
S2 stop = Low[t1] 0.728 vs 0.530/0.533 (the older, shallower low is
breached far more often — the claim's t2 choice is the tight one);
S3 period 14 0.473; S4 close-based breach 0.372; S5 BEAR mirror 0.892 vs
0.587/0.590 (exploratory; no bearish stop claim was pre-registered).
Gate sensitivities directionally consistent throughout (N=5 0.375, N=20
0.638, S2 0.749, S3 0.508, S4 0.405, S5 0.904).

Determinism: primary two runs byte-identical (results 1162e0c54457…,
report 11f7beb09d19…); gate two runs byte-identical (results
b761dfa9cfe2…, report 35a8b49ca7e2…). Independent verification
(from-scratch implementations importing nothing from the frozen stack,
fresh seeds 20260817/20260818): primary — BULL n=16,984 exact, breach
0.4754474799811587 exact, baseline rates exact, bootstrap excess within
6e-4, driver CI-upper within verifier CI ±1.5e-3, F2 exact — **PASSED**;
gate — n=9,384 exact, rates exact, excess within the data-derived 3σ MC
bound (max(3·√2·sd/√B, 6e-4)) — **PASSED**. Input fingerprints: universe
5e6f45a3c791… (primary) / 62f681d58cdb… (gate), measure code
a9ccedd16386…, Phase-3 engine c7421fbf… imported unchanged — no frozen
file modified. Reports: `data/cache/stop_placement_measure_report.md` /
`stop_placement_gate_measure_report.md` (+ `_results.json`). Outcome also
recorded in PREREGISTRATION.md pre-reg #14 §8.

---

## I.12 Course-drift comparison — the 2015–2019 playlist vs the 2025 Ultimate Guide (2026-08-18)

**Question:** same strategy a decade apart, or drifted? Two Ross Cameron
corpora, both claim-scanned: §A–H (2025 Ultimate Guide — one polished
3h06 course video, ~38.5k words) and §I (2015–2019 playlist — the 8 Ross
videos: 4 classroom teaching videos from 2015 + 4 retrospectives/
equipment). The 9 other-channel rows (I-X) are excluded from the
comparison. Method: (1) paired mapping of the ledger rows (the quotes
are the evidence); (2) targeted transcript verification of the pivotal
passages; (3) language-layer rates via
`tools/compare_courses.py` (per-1,000-word pattern counts, 6-gram
overlap — outputs only counts, no transcript text). Caveats: auto-caption
quality; genre mix within the playlist (teaching vs retrospective — the
accuracy/performance claims live in the retrospectives, the rules in the
classroom); n-gram rates measure vocabulary, not semantics.

### The paired rule map

| Family | 2015 (playlist, Ross videos) | 2025 (Ultimate Guide) | Verdict |
|---|---|---|---|
| Entry: first new-high candle after pullback | I-B-02 "the first one minute or the first five minute candle to make a new high" after a decline; I-B-01 first/second pullback after a breakout | B-01 micro pullback: entry = "the first candle that makes a new high versus the high of the previous candle" after a ≥2-red-candle pullback | **SAME** — identical rule; 2025 systematized the confirmation (≥2 red candles) |
| Entry: the breakout (apex) itself — **the §I-Notes flagged tension** | I-B-03 "as soon as we break 3750... the apex point that's the breakout"; "it either works instantly or it doesn't" — apex break is a live entry | B-02 "if I bought right here, what would be my max loss? ... it's really far away ... my profit target has to be two times that ... better to wait for the stock to pull back" | **CONTRADICTED** — adjudicated: 2015 taught the apex break as an entry (I-B-07 preferred the fresh break); 2025 repudiates it on R:R. The entry *family* survives (the new-high-after-pullback variant, row above); what died is the apex timing. 2015 was internally multi-variant; 2025 narrowed to one variant |
| Pullback count restriction | I-B-01 "I trade the first and the second pullback... I never trade almost never trade the third" | B-03 "I always like to trade the first and the second pullback... third and fourth pullback, it can be a little too risky" | **SAME** — near-verbatim, a decade apart |
| R:R requirement + win-rate threshold | I-E-05 3:1 good-setup bar, "2:1... really important", "wrong forty percent of the time and still make money" | B-01 ≥2:1; B-04 wide-range exception; G-01 2:1 + "only need to be right 33%... to break even" | **SAME core** — the 2:1 floor and the 60%-win arithmetic are identical (the family we measured: I-E-05 ↔ A-05/G-01 are the same math); 3:1 emphasis dropped, the 33% breakeven formula made explicit in 2025 |
| Trading window | I-B-05 four inconsistent windows (9:30–12:00 / first 5–10 min / 9:30–11:30 / 9:30–10:30) | F-01 7–10 a.m.; F-02 pre-market "typically cleaner" | **SAME core, DRIFTED specifics** — morning-is-best stable; the four 2015 windows collapsed to one in 2025 and the pre-market leg (7 a.m.) was added |
| Price band | I-D-01 $2–5 (2017 P&L), $2–10 (2019 filter), "above 20 I ignore it" | D-01 $2–20 ("$2–10 even better"); D-02 $1–10; A-04: >$10 unprofitable → $2–10 | **DRIFTED (widened)** — upper edge $5 → $10 → $20 across the decade; the $2–10 sweet spot persists in 2025's own examples; D-01 vs D-02 is an internal 2025 inconsistency |
| Relative volume threshold | I-D-04 "relative volume is 500 percent or higher" | D-01 "5× relative volume" (=500%); D-02 sample plan "10×" | **SAME** — D-01 matches 2015 exactly; the 10× restatement is an internal 2025 escalation |
| Absolute volume band | I-D-03 "total volume between two million and at most 25 million" | — | **DROPPED** — subsumed by relative volume |
| Float | I-D-06 "lower float stocks" (qualitative; GE ~10B counter-example) | D-02 float "<10M shares" | **SAME, quantified** — explicit <10M in 2025 |
| Anti-chasing | I-E-02 buying high-ADV = "usually chasing... it doesn't work" | B-02's R:R argument against buying the move | **SAME family** — reframed as the R:R argument; measured consistent with both eras (Shape B new-high buy: NO EDGE, below baselines, §B.5-B) |
| The two-filter veto (MACD + volume red candle) | — (MACD: zero mentions in all four 2015 classroom transcripts) | E-01/E-04; E-03's MACD-cross lesson self-dated "learned in the 2022 bear market" | **NEW 2025** — an added filter, not a drift of an existing rule; measured: NO EDGE on the daily adaptations (§E.5) |
| RSI-extreme screening | I-B-06 RSI 90/10 "peak my interest", V5/V8 scanner screens RSI<20/>80, with Class 1's caveat; I-D-08 | — (RSI: zero mentions in the entire 2025 transcript) | **DROPPED** — the 2015 indicator vocabulary vanished; MACD replaced it as the course's indicator |
| Exit rules | I-C-01 stop at last-candle low / low of day / 20–30¢; I-C-02 trail to breakeven + sell half; I-C-03 9MA→20MA→VWAP target ladder; I-C-04 flat = out | C-01 five numbered exit indicators (volume red candle, MACD cross, topping tail, VWAP break, 9EMA break); C-03 two-steps-down; C-04 cap losers not winners; C-02/C-05 level-2 exits | **SAME family, systematized** — chart-based trailing exits + breakeven stops + target ladders in both; 2015's ad-hoc list became the 2025 numbered checklist; the VWAP/MA-target family is stable (I-C-03 ↔ F-03); the level-2 exit leg exists in both |
| Market-structure teachings | I-F-01 big moves corrected; I-F-02 stairs/window; I-F-03 trend with market unless catalyst; I-F-04 macro channel; I-F-06 sideways-market profits | F-03 VWAP/MA support; F-04 stop hunting | **DROPPED as teaching** — the 2015 classroom's market-structure rationale is absent from 2025 (setup mechanics + process instead). Two of the dropped claims are measured: I-F-01 (relative correction EDGE, literal retracement FADE, §I.8), I-F-02 (split, §I.9) |
| Process / psychology layer | I-G-01 three red trades → walk away; I-G-02 risk capped ~$500; I-G-03 red days follow green days; I-G-04 95% buying power | G-03 trader rehab; G-04 size scaling + "three strikes you're out"; G-05 guard rails + 3 phases; G-06 +50 shares/10 days; G-07 simulator-first; G-08 Annie Duke | **EXPANDED** — the structured process layer is new in 2025 (simulator 1.04 vs 0.00/1k, phase 0.68 vs 0.05, plan 0.52 vs 0.05); I-G-01's rule survives as G-04's three-strikes |
| Accuracy claims | I-A-04 window chain 100→87→75→68–70→67% (retrospectives only; the 2015 classroom never quotes accuracy) | A-03 66% "which is why I'm up $12.3M"; A-05/G-05 60% threshold | **SAME range, stable** — 68–70% (2015 long-run) → 66% (2025); the 60%-enough floor identical in both; accuracy rhetoric moved from the retrospectives into the course itself (0.68 vs 0.00/1k classroom) |
| Performance narrative | I-A-01/02 $583→$335K 2017; I-A-06 $1M in 553 days 2019 | A-01 retells the same story; endpoint extended: $10M+ pandemic, A-02 "$12.3M verified", A-08 Roth $7M | **SAME story, growing endpoint** — the trajectory is stable and the "verified" rhetoric constant (2017: "verified gains"; 2025: "verified" + accountant); the numbers grew with the decade |

Tally: **8 SAME · 1 CONTRADICTED · 2 DRIFTED · 3 DROPPED · 1 NEW · 1
EXPANDED · 1 ESCALATED** (the 80%, below).

### The 80% escalation (the sharpest finding)

- **2015, Class 1 [22:25–23:38]** — his own cautionary tale (verified
  verbatim in the transcript): "when I back tested that formula I would
  have a you know an 80% chance of being right, an 80% success rate... I
  would run that formula live for 60 days... it was an 80% success rate
  would drop to 40%... I was writing a formula to match a certain set of
  back test results... the scanner was great backward testing but was
  impossible forward testing because the market is always changing".
  Lesson taught: overfit backtests decay; don't trust them.
- **2025, E-02 [04:29–05:54]** — "80% chance of this working" for the
  veto-pass setup: the same number, now the marketing claim.
- **Measured (pre-reg #7)**: REJECTED × 3 — actual pass-set win rates
  48.7–52.9% (§E.7). The 2015 passage predicted the decay directionally
  ("drop to 40%"; measured ~49–53%).
- Verdict: **same number, inverted epistemic use** — 2015's warning
  became 2025's pitch. Corroborated by the language layer: back-test
  vocabulary is 2015-only (0.28 vs 0.00/1k) — the cautionary frame
  vanished from the 2025 course.

### Language layer (per 1,000 words; UG 2025 | 2015 classroom; tools/compare_courses.py)

| Term | UG 2025 | 2015 cls | Read |
|---|---|---|---|
| RSI / MACD / VWAP / EMA | 0.00 / 0.78 / 0.23 / 0.36 | 0.56 / 0.00 / 0.00 / 0.00 | indicator vocabulary flipped |
| breakout / reversal / flag / apex | 0.10 / 0.26 / 0.05 / 0.00 | 0.83 / 2.08 / 0.46 / 0.09 | 2015 classroom vocabulary |
| pullback / squeeze | 1.01 / 0.29 | 0.46 / 0.05 | 2025's replacement terminology |
| "new high" / "high of day" / confirm* | 0.26 / 0.16 / 0.26 | 0.42 / 0.14 / 0.23 | stable entry/target language |
| relative volume / volume / scanner | 0.13 / 1.72 / 0.94 | 0.14 / 1.85 / 1.11 | stable selection language |
| float / catalyst / gap | 0.29 / 0.18 / 0.03 | 0.79 / 0.56 / 0.32 | 2015-heavy selection vocabulary |
| stop / risk / break even | 0.62 / 1.27 / 0.05 | 1.90 / 3.28 / 0.28 | 2015 classroom mechanics |
| simulator / phase / plan / rehab | 1.04 / 0.68 / 0.52 / 0.05 | 0.00 / 0.05 / 0.05 / 0.00 | 2025-only process layer |
| accuracy / verified | 0.68 / 0.05 | 0.00 / 0.00 | 2025 course claims accuracy; the classroom never did |
| back-test* | 0.00 | 0.28 | the overfit warning lives only in 2015 |
| 60% / 33% / 40% | 0.05 / 0.05 / 0.00 | 0.05 / 0.00 / 0.09 | the win-rate math, stable |
| 9:30 / 10:00 / 12:00 / 7:00 | 0.29 / 0.00 / 0.00 / 0.05 | 0.19 / 0.19 / 0.05 / 0.00 | 2015 regular-hours windows; 2025 adds 7 a.m. |

6-gram surface overlap (recomputed): UG 38,120 distinct 6-grams; max 26
shared with any one playlist video (xTPcI7HHu5w); 102 shared with the
combined WT set of 46,051 — essentially zero surface reuse (prior index
finding confirmed at the same order of magnitude). The rules are the
same; the words are not (polished deck vs raw classroom).

### Overall reading

**Same strategy, polished and narrowed.** Of the 16 rule families + the
80% escalation: 8 SAME (two near-verbatim — first/second-pullback, the
60%-win math), 1 CONTRADICTED (apex-break entry, repudiated on R:R), 2
DRIFTED parameters (price band widened $5→$10→$20; window narrowed +
pre-market added), 3 DROPPED (RSI-extreme screening, absolute volume
band, market-structure rationale), 1 NEW (MACD two-filter veto,
self-dated 2022), 1 EXPANDED (process/psychology layer), 1 ESCALATED
(the 80% number, inverted from warning to claim). The 2015 corpus was
multi-variant classroom teaching; the 2025 course is the same method
narrowed to one variant per rule, systematized into numbered checklists
and phases, with the performance story retold at a larger endpoint.

Project consequence: the claims pre-registered and measured from both
corpora were drawn from the *stable* core (pullback/new-high entry,
2:1/60% math, RSI extremes, MACD veto, big-moves-corrected) — the drift
analysis confirms those families genuinely persisted a decade, so the
measurements address the teacher's recurring teachings, not one-off
statements. The §I-Notes flagged tension (B-02 vs I-B-03) is now
adjudicated (row 2). The one escalated claim (E-02's 80%) is the one
the measurements rejected most decisively.

---

## I.13 Price-tier verdicts — pre-registration #16 campaign (I-D-01 / I-X-06 / A-04)

Claims: I-D-01 (xTPcI7HHu5w [25:38–26:18]; H82nRY9TYU4 [20:16–20:26]) —
"stocks between $2 and $5 I made a quarter million dollars... stocks over
$5 40,000 bucks... above 20 I ignore it" (2017 P&L), 2019 filter "$2–10";
A-04 cross-ref (losses on >$10, then traded $2–10); I-X-06
(lMZv0K71HOg [02:37–02:50], EatSleepProfit) — "penny stocks and small
caps... over the long term these companies are going to fall drastically".
Measured 2026-08-19, verified 2026-08-19, per [PREREGISTRATION.md](PREREGISTRATION.md)
#16 (frozen 2026-08-19: hist 904-union with bars OOS 2022–2025, N=10,
COST 0.0015, day-paired bootstrap seed 20260819, Holm per family, §5 gate
pre-registered within the campaign). Full reports:
`data/cache/pricetier_measure_report.md` (+ `pricetier_measure_results.json`)
and `pricetier_gate_measure_report.md` (+ `pricetier_gate_measure_results.json`).

| Verdict | Result (primary, OOS 2022–2025) | Holm gate | §5 gate (current 603, OOS 2016–2025) |
|---|---|---|---|
| **F1a $2–5 vs >$20 EDGE** | n=993 common bar-dates; est +1.11% (CI 0.86–1.37, p=0.000), 109 vs 618 names | 0.0125, rejected | **PASSES** — n=2,504; +2.33% (CI 2.06–2.62), EDGE |
| **F1b $2–10 vs >$10 EDGE** | est +0.51% (CI 0.37–0.65, p=0.000), 240 vs 686 names | 0.0125, rejected | **PASSES** — +1.05% (CI 0.95–1.15), EDGE |
| **F1c $10–20 vs >$20 EDGE** | est +0.29% (CI 0.21–0.37, p=0.000), 411 vs 618 names | 0.0125, rejected | **PASSES** — +0.50% (CI 0.45–0.55), EDGE |
| **F1d same-name control EDGE** | 35,451 pairs / 153 low names; est +7.92% (CI 7.68–8.18, p=0.000) | 0.0125, rejected | **PASSES** — 94,688 pairs; +3.99% (CI 3.85–4.12), EDGE |
| **F2a index-exit NO EDGE** | removal low 25.7% (n=35) vs high 28.0% (n=343); est −0.0227 (CI −0.169..0.132, p=0.756) | not rejected | not triggered (F2 not EDGE); 2022 cohort descriptive — INCONCLUSIVE (5/29 names, floors unmet) |
| **F2b 3y cumulative FADE** | low +39.5% (n=35) vs high +6.0% (n=339); est +0.3352 (CI 0.009..0.727, p=0.040) | 0.05, rejected — wrong direction | — |

**Reading.** The price-tier screen claim is **supported on both windows**:
within the S&P 600 small-cap universe, lower-priced tiers earn better
N=10 forward returns after cost, and the effect is perfectly monotone
across the five bands (lt2 +6.10% > 2-5 +1.47% > 5-10 +0.53% > 10-20
+0.32% > gt20 −0.08%, name-day collapsed). The same-name control (F1d) is
the sharpest form: the *same ticker* earns +7.9% per 10-bar window on its
<$10 bar-dates vs +0.1% on its own >$20 bar-dates — the band adds value
over the name. The effect survives the §5 gate on the frozen current
constituents across 2016–2025 — the first time the gate confirms in the
reverse direction (the primary is delisting-aware; the gate is the live
index). Sensitivities corroborate: N=5/20 escalate, LAG5/BAND10/REL hold,
every OOS year positive (2022 0.83% → 2025 0.31%). The long-term fall
claim (I-X-06) is **contradicted**: the 2021 low-priced cohort *outpaced*
the high-priced cohort on 3-year cumulative returns (+39.5% vs +6.0%,
FADE), the gap accruing with horizon (1y +5.0% → 4y +42.2%), with no
excess index-exit rate (F2a NO EDGE) and a 79.6% death-proxy row (147
no-bar names, 117 removed) that only strengthens the record — those names
are not the survivors. **The Phase-5 trigger-check was held: NOT
TRIGGERED** — the finding is a monotone *relative* tiering effect with
modest absolute size (+1.1% per 10-bar window after cost on the cheapest
band) and no tradeable construction; the claim's own "sweet spot" framing
(P&L anecdotes) is not a tradeable signal. Note the claim's internal
inconsistency is resolved in the measurement's favor: both the $2–5 (F1a)
and $2–10 (F1b) variants are EDGE, so the 2017/2019 band drift does not
change the verdict. The literal penny-stock population (<$2) is a thin
slice on this data (pre-declared, §2); lt2 is reported descriptively
(+6.10%, 33 names) — the claim's broadest reading remains untested.

**Verification.** Deterministic: primary three runs byte-identical
(results 732ccd01ca0b…, report 04b31aa10440…); gate two runs
byte-identical (ccb6f713a4d4… / 24b35d886452…). Independent
from-scratch verification (imports nothing from the frozen stack, fresh
seeds 20260820/21/22, 129 checks): freeze shas exact; census exact
(union 904, purged 198, current 603, cohort 601/259); per-band stats
exact; all slot/F2 ests exact to 1e-12 with CIs within fresh-seed MC
spread; Holm recomputed; gate ests exact — **PASSED**.

## I.14 C-exit comparison verdicts — pre-registration #17 campaign (C-01 / C-03 / C-04)

Claims: C-01 (exit indicators — HV-red, VWAP-break, 9-EMA-break, topping
tail, MACD), C-03 ("two steps down... two candles that go lower and lower
that we get out"), C-04 ("cap my losers, not my winners"). Measured
2026-08-19, verified 2026-08-19, per [PREREGISTRATION.md](PREREGISTRATION.md)
#17 (frozen 2026-08-19: OOS 2016–2025 by signal date, A/B/C detections
from the frozen pre-reg #2 set, same-entry two-arm contrast, R units,
day-paired bootstrap seed 20260819, Holm per family, §5 gate
pre-registered within the campaign). Full reports:
`data/cache/cexit_measure_report.md` (+ `cexit_measure_results.json`) and
`cexit_gate_measure_report.md` (+ `cexit_gate_measure_results.json`).

| Verdict | Result (primary, OOS 2016–2025) | Holm gate | §5 gate (904-union) |
|---|---|---|---|
| **F1 system contrast NO EDGE / FADE-A** | pooled −0.0215R (CI −0.0537..+0.0105, p=0.202); A **FADE** −0.0777R (CI −0.1320..−0.0307, p=0.000); B +0.0265 (p=0.172); C −0.0928 (p=0.038) | 0.0125 — A rejected (wrong direction) | A **FADE** −0.0616 (p=0.002); B/C/pooled NO EDGE |
| **F2 S1 HV-red timing EDGE (primary only)** | n=3,020; est +0.0043 (CI +0.0009..+0.0076, p=0.014) | 0.0125, rejected | **NO EDGE** — n=3,405; +0.0041 (p=0.028, not rejected) |
| **F2 S2 VWAP-break timing EDGE (primary only)** | n=9,082; est +0.0046 (CI +0.0014..+0.0078, p=0.006) | 0.0125, rejected | **NO EDGE** — n=10,414; +0.0039 (p=0.016, not rejected) |
| **F2 S3/S4 NO EDGE** | S3 n=150 +0.0030 (p=0.690); S4 n=195 −0.0080 (p=0.198) | not rejected | NO EDGE (n 162/216) |
| **F3 q90/q95 FADE** | est −1.4840 / −1.0385 (p=0.000) | 0.0167, rejected (wrong direction) | FADE −1.4922 / −1.0405 (p=0.000) |
| **F3 q99 EDGE — survives the gate** | est +0.6767 (CI +0.4584..+0.9178, p=0.000) | 0.0167, rejected | **EDGE** +0.6425 (CI +0.4463..+0.8897, p=0.000) |

**Reading.** The C-01 protocol question is answered: indicator exits are
well-timed but not a better *system*. S1/S2 fire at genuinely weak points
in the primary (post-exit 10-bar returns ~0.43/0.46pp below same-ticker
random baselines) but the edge is fragile — essentially unchanged
estimates on the 904-union land above the Holm gate (p 0.028/0.016), and
the fresh-seed baseline redraw fails to reproduce the verdicts (fresh p
0.126/0.024) — and as a system (F1) the indicator arm loses to the
corpus's own fixed-2R exits on Shape A and breaks even elsewhere (pooled
NO EDGE both windows). C-04's asymmetry holds only in its extreme
statistical form: q90/q95 FADE (the fixed cap beats the indicator arm's
typical winners) while q99 EDGE survives the gate (the very best
indicator-arm trades run ~0.64R beyond +2R). C-03's two-steps-down shows
no timing edge. **The Phase-5 trigger-check was held: NOT TRIGGERED** —
the surviving EDGE is a tail-quantile contrast of the same construction
that nets negative as a system (F1 pooled NO EDGE, A FADE); the tail
cannot be selected ex ante, so there is no tradeable version of "don't
cap winners."

**Verification.** Deterministic: three primary runs byte-identical
(results 71fbbd49…, report f896459d…); gate recorded (results 0a67241a…,
report b708fd85…). Independent verification re-implemented the
measurement from scratch (fresh code importing nothing from the frozen
stack, fresh seeds): counts/means/ests exact to 1e-9, CIs within the
fresh-seed MC spread, Holm + floors + verdicts stable, the frozen
detector re-run on the 904 union ⊇ the frozen detection set on the shared
names (extras only from the documented CWEN-A float-precision bar
regeneration, entries within 1e-6 relative). 215 checks, all PASS
(2026-08-19). Artifact note: 8 microscopic-R events (split-adjusted entry
≈ structural low; worst NSSC A 2016-01-29, COST_R ≈ 22,650R) — kept per
the frozen §3 contract, verdicts robust to their exclusion, R levels
reported with that caveat.

---

## I.15 I-F-03 market-trend verdicts — pre-registration #18 campaign

Claim: I-F-03 ("Stocks will trend with the overall market unless they have
a reason not to", txWaMpSzHhM [31:55–32:38]). Measured 2026-08-21, verified
2026-08-21, per [PREREGISTRATION.md](PREREGISTRATION.md) #18 (frozen
2026-08-21: OOS 2016–2025 by bar date, per-stock Pearson corr with SPY,
catalyst = gap |open/prior close − 1| ≥ 2% OR RV = vol/mean(vol, prior 20)
≥ 2.0, one-sample bootstrap seed 20260813, Holm per family, §5 gate
pre-registered within the campaign). **Structural campaign — no forward
returns, no entry/exit, no cost; Phase 5 not implicated by construction.**
Reports: `data/cache/if03_measure_report.md` (+ `if03_measure_results.json`)
and `if03_gate_measure_report.md` (+ `if03_gate_measure_results.json`).

| Verdict | Result (primary, OOS 2016–2025) | Holm gate | §5 gate (904-union) |
|---|---|---|---|
| **F1 baseline EDGE** | n=598; mean corr +0.4601 (CI +0.4521..+0.4681, p=0.000) | 0.0500, rejected | **EDGE** — n=703; +0.4455 (CI +0.4370..+0.4537, p=0.000) |
| **F2-gap FADE** | n=590; +0.0968 (CI +0.0864..+0.1080, p=0.000) | 0.0250, rejected (wrong direction) | FADE — n=698; +0.0858 (p=0.000) |
| **F2-vol EDGE** | n=589; −0.2253 (CI −0.2357..−0.2134, p=0.000) | 0.0500, rejected | **EDGE** — n=691; −0.2310 (p=0.000) |
| **F3-gap NO EDGE** | n=1,086; +0.0005 (CI −0.0009..+0.0019, p=0.488) | not rejected | NO EDGE — n=1,107; +0.0001 (p=0.894) |
| **F3-vol EDGE (up-bias caveat)** | n=1,080; +0.0021 (CI +0.0009..+0.0033, p=0.002) | 0.0250, rejected | **EDGE** — n=1,097; +0.0042 (p=0.000) |

**Reading.** The claim is half-true. F1 confirms the baseline half at the
strongest level — per-stock daily correlation with the market is +0.46,
uniformly positive across 598 of 599 stocks. The "reason not to" half
splits by catalyst proxy: volume-spike days decouple as claimed (−0.23,
p=0.000 — the mechanical effect of a large idiosyncratic move); gap days
move the OPPOSITE way (+0.10, p=0.000 — correlation HIGHER on gap days,
claim contradicted) and F3-gap shows no down-day contrast (p=0.488).
F3-vol's down-day edge is the general up-bias of catalyst stocks, not a
market-specific run: the pre-declared S8 control shows the up-day contrast
(+0.0100 gap / +0.0063 vol) exceeds the down-day contrast and down−up is
negative (−0.0095 / −0.0042, p=0.000). Catalyst stocks outperform
non-catalyst stocks on BOTH kinds of days — "running when the markets
tanking" is not a market-specific phenomenon. The IS record (2000–2015,
descriptive) shows the same signs at roughly twice the OOS magnitudes;
F3-gap was positive IS (+0.0025) but is null OOS. Phase-5 trigger-check
held: **NOT TRIGGERED** — structural, no forward returns.

**Verification.** Deterministic: two primary runs byte-identical (results
`5407f681…`, report `c391458c…`); gate recorded (results `a837df19…`,
report `8f21b9e9…`). Independent verification re-implemented the
measurement from scratch (`tools/verify_if03.py` — fresh code importing
nothing from the frozen stack, fresh seeds): counts/means exact to 1e-9,
CIs within the fresh-seed MC spread, Holm + floors + verdicts stable for
every family and every sensitivity (S1–S9). 258 checks, all PASS
(2026-08-21).

---

## What gets pre-registered next

Priority order for turning `candidate` rows into pre-registered hypotheses
(DESIGN_BRIEF §6):

1. **Shapes A/B/C (pre-reg #2)** — ✅ **measured 2026-08-13**: all **NO EDGE**
   on OOS (2016–2025, N=10, Holm at α=0.05); verdicts and numbers in §B.5,
   full report in `data/cache/measure_report.md`. First completed campaign.
2. **D-01/D-02/D-03 (stock-selection pillars)** — ✅ **measured 2026-08-13**:
   H1/H2 INCONCLUSIVE by count floor (7/6 detections in 26 years, 0 OOS);
   H3 NO EDGE (n=2,513 OOS; day-paired rank-1 vs rank-2–10: +0.00pp, p=0.99).
   Verdicts in §D.5, full report in `data/cache/pillar_measure_report.md`.
   Second completed campaign.
3. **E-01/E-04 (the two-filter veto)** — ✅ **measured 2026-08-14**: NO EDGE
   in both verdict families for all three shapes (§E.5) — the veto does not
   improve any pattern; on A/C it cuts the better trades; on B it changes
   nothing. Answer to its own question: it reduces trade count, not edge.
   Third completed campaign.
4. **Momentum horizon follow-up (pre-reg #4, N=20 primary)** — ✅ **measured
   2026-08-14**: Family 1 (absolute at N=20) **NO EDGE × 3** — selection
   adds nothing over same-ticker buy-and-hold; Family 2 (paired
   continuation N=20 vs N=5) **EDGE × 3** — the entry names kept drifting
   up 5→20 bars (first EDGE verdicts in the project, interpretation in
   §D.6). Fourth completed campaign.
5. **Per-decade drift decomposition (pre-reg #5)** — ✅ **measured
   2026-08-14**: both families **NO EDGE × 3** (§D.7) — the late-era
   strengthening is real vs random (F1 p=0.008, F2 p=0.002) but never
   clears the same-ticker control; the drift is late-era beta, not
   selection edge. Fifth completed campaign.
6. **E-03 (MACD-cross breakout rejection)** — ✅ **measured 2026-08-14**:
   **FADE EDGE × 2 on Shape B** (bear-day conditioning −1.62pp, p=0.012;
   avoidance bar p_input 0.014), NO EDGE × 6, INCONCLUSIVE × 1 — the first
   verdicts in a claim's favor, and they land on the shape/regime the claim
   describes (§E.6). Sixth completed campaign.
7. **E-02 ("80% chance of this working")** — ✅ **measured 2026-08-14**:
   **REJECTED × 3** (F1 claim test: pass-set win rates 48.7–52.9%, one-sided
   p ≤ 2e-24, CI upper ≤ 0.58; even the 0.60 softening fails, C p=0.009),
   **NO EDGE × 3** (F2 vs chance — A/B win *below* random, p=0.004/<0.001)
   (§E.7). Seventh completed campaign.
8. **B-01 (micro pullback)** — **pre-registered (pre-reg #15, frozen 2026-08-19)**;
   the daily-bar adaptation (Shape B: pullback + new-high) was already measured
   and **rejected** 2026-08-13 (§B.5-B). The intraday rule awaits the §5
   floor (~mid-September). **Also the shared entry set for pre-regs #20–#21.**
9. **B-02/B-03/B-05/C-01/C-03/C-04 (entry/exit variants)** — system-comparison
   questions. Daily adaptations of B-02 (Shape A) and B-05 (Shape C) measured
   and rejected (§B.5-A, §B.5-C); **C-01/C-03/C-04 measured 2026-08-19
   (pre-reg #17)** — exits well-timed but not a better system; F2 timing
   EDGEs fail the §5 gate; q99 tail EDGE survives, trigger-check NOT
   TRIGGERED (§I.14). **The B-03/I-B-01 pullback-count and B-05
   second-confirmation intraday forms are frozen in pre-reg #19; the
   C-01/C-03/C-04 1-min exit forms are frozen in pre-reg #20** (both
   await the §5 floor).
10. **I-D-07 + I-E-01 (high-relative-volume conditioning)** — ✅ MEASURED
    (pre-reg #8, 2026-08-14): F1-A/B **NO EDGE**, F2-B NO EDGE (contrast
    +0.30pp, p=0.302 — the claimed direction, never significant), F1-C/F2-C
    INCONCLUSIVE (count floor), F2-A INCONCLUSIVE by construction (every A
    detection is high-RV — the detector's V=2.0). The absolute leg is null;
    the differential leg whispers but never clears. Verdicts: §I.5.
11. **I-X-01 (RSI 70/30 daily-bar reversal bias)** — ✅ MEASURED (pre-reg #9,
    2026-08-14): **EDGE × 3 at the state level** — F1-OB (overbought below
    both baselines: −0.30pp vs same-ticker, p<0.001), F1-OS (oversold above
    both: +0.14pp vs same-ticker, p<0.001), F2 contrast OS−OB +0.38pp
    (p<0.001) — the first campaign to confirm a claim's direction; the
    pre-declared event-level view is null (OS p=0.166) and the Phase-5
    trigger-check did not trigger. Verdicts: §I.6.
12. **I-X-02/03/04 (RSI divergence frequency + reliability)** — ✅ MEASURED
    (pre-reg #10, 2026-08-14): **F1-BULL EDGE** — the project's first
    event-level absolute EDGE (n=16,985 OOS; +0.80% mean; +0.34pp vs
    same-ticker, Holm-rejected; robust across all structural
    sensitivities) — and **F1-BEAR NO EDGE** (p=0.662); F2: BULL EDGE × 2
    (mean +0.18pp, hit +1.50pp vs oversold crossings), BEAR-mean FADE
    (+0.21pp — less reliable, the opposite direction), BEAR-hit NO EDGE;
    frequency ratio 0.3051 confirms "a lot less common". Phase-5
    trigger-check held: **NOT TRIGGERED** — the brief §5 survivorship gate
    (historical-constituent re-check) is the explicit path forward.
    Verdicts: §I.7.
13. **I-F-01 (big moves get corrected)** — ✅ MEASURED (pre-reg #11,
    2026-08-14/15): **F1-UP EDGE** (relative correction — big up-moves
    below both baselines: −0.48pp vs same-ticker, p<0.001, Holm-rejected;
    mean +0.03% after cost), **F1-DOWN NO EDGE** (p=0.950); **F2 FADE × 2**
    — big moves retrace ≥ half within 10 sessions *less* often than
    typical bars (−12.77pp / −15.53pp, both Holm-rejected) — the ledger's
    literal reading falsified; the DOWN bounce exists only at τ=2
    (+0.24pp) and reverses at τ=5 (−1.36pp). Phase-5 trigger did not fire
    (only an F1-DOWN EDGE can trigger; it is null). Verdicts: §I.8.
14. **I-F-02 (bulls take the stairs, bears take the window)** — ✅
    MEASURED (pre-reg #12, 2026-08-15): **A1 FADE × 3** (per-bar
    asymmetry inverted — up-bars ~6bp larger: F1-UP FADE, F1-DOWN FADE
    knife-edge, F2 FADE), **A2 EDGE** (F4: retracements of big up-moves
    outpace the moves — n=35,997, +0.40pp/bar, p<0.001); swing-scale S6
    confirms the claim across bars, per-bar F1/F2 falsify it; Phase 5
    not implicated by construction (no forward returns). Verdicts: §I.9.
15. **I-D-01 (price-tier edge: $2–5 vs >$20)** — ✅ MEASURED (pre-reg #16,
    2026-08-19): **EDGE × 4 + §5 gate PASSES** (F1a +1.11%, F1b +0.51%,
    F1c +0.29%, F1d +7.92%, all p=0.000; gate +2.33/+1.05/+0.50/+3.99%) —
    the first candidate whose EDGE survives the *reverse* gate (the
    primary is delisting-aware; the gate is the live index). Phase-5
    trigger-check held: NOT TRIGGERED. Verdicts: §I.13.
16. **I-X-06 (penny/small-cap long-term fall)** — ✅ MEASURED (pre-reg #16,
    2026-08-19): **contradicted** — F2b **FADE** (+0.3352, p=0.040; low
    cohort +39.5% vs high +6.0% over 3y, accruing to +42.2% at 4y), F2a
    NO EDGE, death-proxy row counted (§I.13).
17. **I-F-03 (stocks trend with the market unless catalyst)** — ✅ MEASURED
    (pre-reg #18, 2026-08-21): **half-true** — F1 baseline **EDGE**
    (per-stock corr +0.46, §5 gate passes), F2-vol **EDGE** (volume-spike
    decoupling, gate passes), F2-gap **FADE** (corr HIGHER on gap days),
    F3-gap NO EDGE; F3-vol's down-day edge is the general catalyst
    up-bias, not a market-specific run (§I.15). **The final testable-daily
    item — the daily track is now exhausted; remaining candidates need
    intraday data (the §5 intraday floor: 2 of 20 bar-dates ≥ 2026-08-19,
    ~mid-September).**
18. **I-X-05 (stop placement for bullish divergence)** — ✅ MEASURED (pre-reg
    #14, 2026-08-17/18): **F1-BULL EDGE on the primary AND the §5 gate
    PASSES** — the first EDGE to survive the historical-constituent
    re-check (breach −5.46pp/−5.71pp primary, −4.82pp/−5.70pp gate,
    p=0.000 both); F2-BULL EDGE (−28.56pp/−26.87pp); Phase-5 trigger-check
    held: NOT TRIGGERED (risk-placement property). Verdicts: §I.11.

## Open work

- [x] Pre-register the Section D pillars — done 2026-08-13
  ([PREREGISTRATION.md](PREREGISTRATION.md), hypotheses H1–H3).
- [x] Measure the shape detectors (pre-reg #2) and write the verdicts back —
  done 2026-08-13: shapes A/B/C all **NO EDGE** on OOS (§B.5,
  `data/cache/measure_report.md`). First completed campaign.
- [x] Measure the pillars (pre-reg #1) and write the verdicts back — done
  2026-08-13: H1/H2 INCONCLUSIVE by count floor, H3 NO EDGE with a precisely
  null day-paired claim test (§D.5, `data/cache/pillar_measure_report.md`).
  Second completed campaign.
- [x] Measure the two-filter veto (pre-reg #3) and write the verdicts back —
  done 2026-08-14: NO EDGE in both families for A/B/C (§E.5,
  `data/cache/veto_measure_report.md`). Third completed campaign.
- [x] Measure the momentum horizon follow-up (pre-reg #4) and write the
  verdicts back — done 2026-08-14: F1 NO EDGE × 3, F2 EDGE × 3 (§D.6,
  `data/cache/momentum_measure_report.md`). Fourth completed campaign.
- [x] Measure the per-decade drift decomposition (pre-reg #5) and write the
  verdicts back — done 2026-08-14: both families NO EDGE × 3 (§D.7,
  `data/cache/decade_measure_report.md`). Fifth completed campaign.
- [x] Measure the E-03 MACD-cross breakout-rejection claim (pre-reg #6) and
  write the verdicts back — done 2026-08-14: FADE EDGE × 2 on Shape B,
  NO EDGE × 6, INCONCLUSIVE × 1 (§E.6,
  `data/cache/e03_measure_report.md`). Sixth completed campaign.
- [x] Measure the E-02 "80% chance of this working" claim (pre-reg #7) and
  write the verdicts back — done 2026-08-14: REJECTED × 3 (F1 claim test),
  NO EDGE × 3 (F2 vs chance) (§E.7,
  `data/cache/e02_measure_report.md`). Seventh completed campaign.
- [x] Measure the high-relative-volume conditioning claim (pre-reg #8) and
  write the verdicts back — done 2026-08-14: F1 NO EDGE × 2, INCONCLUSIVE
  × 3, F2-B NO EDGE (§I.5, `data/cache/rv_measure_report.md`). Eighth
  completed campaign.
- [x] Measure the RSI 70/30 reversal-bias claim (pre-reg #9) and write the
  verdicts back — done 2026-08-14: EDGE × 3 at the state level (§I.6,
  `data/cache/rsi_measure_report.md`); the Phase-5 trigger-check was held
  and did not trigger. Ninth completed campaign.
- [x] Measure the RSI divergence frequency + reliability claims (pre-reg
  #10) and write the verdicts back — done 2026-08-14: **F1-BULL EDGE**
  (the project's first event-level absolute EDGE), F1-BEAR NO EDGE,
  F2 BULL EDGE × 2 / BEAR-mean FADE / BEAR-hit NO EDGE, frequency ratio
  0.3051 (§I.7, `data/cache/divergence_measure_report.md`); the Phase-5
  trigger-check was held and did not trigger — the brief §5
  historical-constituent re-check is the explicit path forward. Tenth
  completed campaign.
- [x] Measure the big-move correction claim (pre-reg #11, I-F-01) and write
  the verdicts back — done 2026-08-15: **F1-UP EDGE** (relative
  correction — big up-moves below both baselines), F1-DOWN NO EDGE
  (p=0.950), **F2 FADE × 2** (literal retracement falsified), frequency
  reported (§I.8, `data/cache/bigmove_measure_report.md`); the Phase-5
  trigger did not fire (only an F1-DOWN EDGE can trigger; it is null).
  Eleventh completed campaign.
- [x] Measure the speed-asymmetry claim (pre-reg #12, I-F-02) and write
  the verdicts back — done 2026-08-15: **A1 FADE × 3** (per-bar asymmetry
  inverted — up-bars ~6bp larger than down-bars: F1-UP FADE, F1-DOWN FADE
  knife-edge, F2 FADE), **A2 EDGE** (retracements of big up-moves outpace
  the moves), frequency reported (§I.9, `data/cache/speed_measure_report.md`);
  Phase 5 not implicated by construction (no forward returns measured).
  Twelfth completed campaign.
- [x] Measure the stop-placement claim (pre-reg #14, I-X-05) and write the
  verdicts back — done 2026-08-17/18: **F1-BULL EDGE** (breach 47.54% vs
  52.99%/53.28%, excess −5.46pp/−5.71pp, p=0.000) **and the §5 gate
  PASSES** (n=9,384, breach 50.53% vs 55.37%/56.20%, −4.82pp/−5.70pp) —
  the first EDGE to survive the historical-constituent re-check; F2-BULL
  EDGE (−28.56pp primary, −26.87pp gate); Phase-5 trigger-check held:
  NOT TRIGGERED (risk-placement property, no tradeable size) (§I.11,
  `data/cache/stop_placement_measure_report.md` +
  `stop_placement_gate_measure_report.md`). Fourteenth completed campaign.
- [x] Measure the price-tier family (pre-reg #16, I-D-01 / I-X-06 / A-04)
  and write the verdicts back — done 2026-08-19: **F1 EDGE × 4 + §5 gate
  PASSES** (F1a +1.11%, F1b +0.51%, F1c +0.29%, F1d same-name +7.92%,
  p=0.000; gate on current 603 OOS 2016–2025 +2.33/+1.05/+0.50/+3.99%);
  **F2b FADE** (low +39.5% vs high +6.0%, p=0.040 — the long-term-fall
  claim contradicted), F2a NO EDGE; Phase-5 trigger-check held: NOT
  TRIGGERED (§I.13, `data/cache/pricetier_measure_report.md` +
  `pricetier_gate_measure_report.md`; independently verified 2026-08-19,
  129 checks). Fifteenth completed campaign.
- [x] Measure the C-exit comparison (pre-reg #17, C-01 / C-03 / C-04)
  and write the verdicts back — done 2026-08-19: F1 system contrast NO
  EDGE (pooled −0.0215R, p=0.202) / Shape A **FADE** (−0.0777R); F2 S1/S2
  timing EDGEs primary-only (p 0.014/0.006) **fail the §5 gate** (union p
  0.028/0.016, not rejected at 0.0125) and do not reproduce under the
  verifier's fresh-seed baseline redraw (p 0.126/0.024); F3 q90/q95
  FADE, **q99 EDGE survives the gate** (+0.6425, CI +0.4463..+0.8897,
  p=0.000); Phase-5 trigger-check held: NOT TRIGGERED (§I.14,
  `data/cache/cexit_measure_report.md` + `cexit_gate_measure_report.md`;
  independently verified 2026-08-19, 215 checks). Sixteenth completed
  campaign.
- [x] Measure the I-F-03 market-trend claim (pre-reg #18) and write the
  verdicts back — done 2026-08-21: **half-true** — F1 baseline **EDGE**
  (per-stock corr +0.46, §5 gate passes), F2-vol **EDGE** (volume-spike
  decoupling −0.23, gate passes), F2-gap **FADE** (corr HIGHER on gap days),
  F3-gap **NO EDGE** (p=0.488), F3-vol's down-day edge is the general
  catalyst up-bias not a market-specific run (S8 down−up negative);
  Phase-5 trigger-check held: NOT TRIGGERED (structural) (§I.15,
  `data/cache/if03_measure_report.md` + `if03_gate_measure_report.md`;
  independently verified 2026-08-21, 258 checks). Seventeenth completed
  campaign — and the final testable-daily one; the remaining candidates
  need intraday data (B-01, I-B-01, I-C-02/03/04, E-01/E-04, F-01/F-02,
  I-E-02), gated on the intraday §5 floor (~mid-September).
- [x] Pre-register the remaining intraday claims — done 2026-08-21: **pre-regs
  #19–#22 frozen** in [PREREGISTRATION.md](PREREGISTRATION.md) — **#19**
  intraday entry timing (I-B-02 reversal new-high long+short, B-03/I-B-01
  pullback-count, B-05 second-confirmation; seed 20260821), **#20** intraday
  exits (I-C-02 breakeven-trail + sell-half, I-C-03 9MA→20MA→VWAP ladder,
  I-C-04 flat-out, on the pre-reg #15 B-01 entry set; seed 20260821), **#21**
  the two-filter pre-entry veto on 1-min bars (E-01/E-04 — MACD negative +
  high-volume red candle; entry set = pre-reg #19 F1; seed 20260821), **#22**
  intraday regime (I-B-05 morning-is-best volatility/liquidity buckets,
  F-01/F-02 pre-market cleanliness; seed 20260821). All four share the
  pre-reg #15 §5 floor (≥ 20 full-universe bar-dates ≥ 2026-08-19, ~mid-
  September) — one-shot rule, Holm α=0.05, COST 0.15%, gate = the #15 §6
  archive-integrity audit. (I-D-05 gap-scanners is the one `testable-daily`
  orphan never prioritized — it is a $25k-playlist side comment, §I-D-05;
  deliberately not in the intraday prep batch.)
- [x] Build + freeze the intraday measurement tools (pre-regs #19–#22
  implementations) — done 2026-08-21, after the hypothesis freeze: each tool
  byte-locked at its fixed-point FROZEN_SHA — `tools/measure_intraday_entry.py`
  `cac0e7ed…`, `_exit.py` `544a1c0b…`, `_veto.py` `60569201e5…`,
  `_regime.py` `b1fe067d…` — with the frozen-input entry set / B-01 reference
  asserted at import, audit-only + §5 floor-refusal + determinism verified,
  dev harness green, and the §8 *Implementation freeze* + *Implementation
  reading* written into [PREREGISTRATION.md](PREREGISTRATION.md). All four
  await the shared §5 floor (~mid-September).
- [x] Pre-register the paper loop (pre-reg #23) — done 2026-08-23: the
  live-execution study frozen before any paper-log results — the five frozen
  tools' exact definitions run on each live tape day as it lands, logging
  fills/slippage vs. the recorded bar (three price columns: recorded
  reference, modeled fill, observed fill), the gate decisions, and a daily
  journal. Tool `tools/paper_loop.py` byte-locked (FROZEN_SHA `c08b3ca5…`),
  the five frozen inputs asserted at import, `data/paper/` append-only.
  Feeds the §5-gated L-007 comparison when the floor flips (~mid-September).
- [x] Build the five intraday standalone independent verifiers — done
  2026-08-22: `tools/verify_intraday.py` (imports nothing from the frozen
  stack; fresh bootstrap seeds; EXACT + MC-SPREAD check classes; exit 0/1)
  covers all five frozen intraday tools (pre-regs #15/#19/#20/#21/#22).
  Interim cross-validation against floor-bypassed dev dumps of each frozen
  tool: **#15 71/71, #19 84/84, #21 75/75, #22 66/66 green — and #20 red on
  exactly its CI-endpoint checks**, exposing a CI-recording bug in the
  frozen exit tool (see §I.14 note below).
- [ ] **#20 re-freeze (pre-measurement, no data touched)**: the independent
  verification pass caught that `tools/measure_intraday_exit.py` recorded
  `ci_low`/`ci_upper` swapped with the upper CI / p-value (`run_f1`, `run_f2`
  — the 5-tuple indices were 3/4 instead of 2/3). No measurement had run;
  the mappings were corrected, the tool re-frozen at FROZEN_SHA
  `0c798159ea3e93d9…` (§8 amendment in PREREGISTRATION #20), and the exit
  verifier re-ran clean (**#20 55/55**). This is open work in the sense of
  tool provenance only — the §5 floor is still unmet (~mid-September) and
  no intraday verdict exists yet. The paper loop's frozen-input assertion
  for the exit tool was re-recorded to the re-frozen sha 2026-08-25 as part
  of the main-branch reconcile (pre-reg #23 freeze-block amendment).
- [x] Scan `transcripts/warrior-trading/` (the 2015 "Class 1-12" playlist) for
  claims — done 2026-08-14: 53 rows in §I (I-A..I-X + §I-Notes), quotes
  re-verified against the transcripts, priority list updated (items 10–17).
  **Compare the two courses for drift** (same strategy 10 years apart?
  parameters changed? claims escalated?) — done 2026-08-18: **§I.12**
  (paired rule map of all 16 rule families + the 80% escalation,
  `tools/compare_courses.py` language layer, both tensions adjudicated).
  Verdict: same strategy, polished and narrowed — 8 SAME, 1 CONTRADICTED
  (apex-break entry), 2 DRIFTED (price band $5→$20, window + pre-market),
  3 DROPPED (RSI extremes, absolute volume, market structure), 1 NEW
  (MACD veto, self-dated 2022), 1 EXPANDED (process layer), 1 ESCALATED
  (the 80%: 2015's overfit warning became 2025's claim; measured
  REJECTED × 3).
- [x] Fill `topics`/`claims` frontmatter in transcript files as the ledger
  grows — done 2026-08-14 for all 13 transcript files (§I rows mapped back
  per video; non-trading videos get topics only).
- [ ] Record the *expected* failures: when a claim is measured and rejected,
  log the verdict here (status → `tested, rejected` + link to the pre-reg
  doc). **First exercised 2026-08-13 (§B.5).** The ledger is the audit trail;
  keep every row, never delete.
- [x] Scan `transcripts/warrior-trading-favorites/` (the official "My Favorite
  Episodes" playlist + standalone `Wd_iUsteoaw`) for claims — done 2026-09-01:
  §J pilot (11 rows, `mfGQr2tHoX0`) + 465 rows across the remaining 25 videos,
  every quote machine-verified against its transcript (977/978 + 1 by hand).
  §I.12-style drift follow-ups now queued: MACD escalation datable 2023→2024
  (GXl-09→2n2-05), price-band drift to $1–20/$2–20 with float 10M/20M/30M
  tension (GXl-12, 2n2-14, 5X_-05, 3rE-07), morning-window count now six
  variants (ZS8-03, UvX-25, e5R-04), RV threshold 5× vs the frozen 2.0 with
  his own lookback uncertain (yFo-14, 3rE-02), and the first regime claims
  with a usable operational proxy (Wd_-01/-02, leading-gainer strength).
  Next: pre-register the J-B-01 crossover-gate test (biggest unimplemented
  rule), the 30-minute window (2n2-07), and the HV-red-candle directional
  forecast (3rE-14).
- [x] Pre-registration #24 — RV lookback-matched re-measure at his stated
  parameters — done 2026-09-01: **NO EDGE** on all four testable slots,
  INCONCLUSIVE on Shape C (count floor); the §I.5 null is robust to his own
  definition. Verdicts in §J.1; the persistent +0.3–0.5pp directional whisper
  (now failed at 2×/20-bar and 5×/50-bar) stays exploratory.
- [ ] Pre-registration #25 — price-band + float drift adjudication
  ($1–20 vs $2–20 × float 10M/20M/30M; rows UvX-18, 4Pc-11, HYo-03, 5X_-05,
  3rE-07, GXl-12, 2n2-14) — next in queue.

## J. Warrior-trading corpus — "My Favorite Episodes" playlist claims

Claim-extraction pass over Ross Cameron's own-channel playlist
(25 videos, 2022–2024 era, plus standalone `Wd_iUsteoaw` 2026-09-01), opened
2026-09-01 with the pilot and **completed the same day for all 26 videos**
(pilot 11 rows + 465 rows below; every quote mechanically verified against
its transcript at consolidation — 977/978 fragments machine-matched, 1
verified by hand). Unlike the §I playlist this one is 100% Ross Cameron
content — no fan-mix, no non-trading videos. Rubric letters and statuses as
in §I; rows keep their per-video ids (`UvX-14`, `hz7-06b`, …) to preserve
the cross-references between them.

### J-Pilot: MACD step-by-step (`mfGQr2tHoX0`, 2024-05-20, 21:58)

**Settings claim (context for every MACD row):** "my macd settings are
standard they are default I do not change them... fast length is 12 our slow
length is 26 and our signal length is 9 and the source is close" —
`mfGQr2tHoX0 [06:01–06:30]`. Standard 12/26/9 EMA MACD on 1-min/5-min charts
(`[01:07–01:10]`). This matches the veto's `macd_at` (12/26 EMA line) except
that the signal line is unused there — see J-B-01 vs J-B-02.

| # | Time | Claim as stated | Status |
|---|---|---|---|
| J-A-01 | mfGQr2tHoX0 [00:40–00:45], [09:08–09:12] | "a stock that I traded uh just yesterday I locked up about $5,000 of profit on it" (SGBX); repeated at [09:08–09:12] "I actually made $5,000 on it". | `red flag` — self-reported single-day anecdote framing the lesson ("how I nailed"); unverifiable, same posture as I-A. |
| J-B-01 | mfGQr2tHoX0 [11:10–11:17], [11:17–11:30], [11:49–11:58], [16:33–16:42] | **MACD-open gate (primary rule):** "when I see this crossover I am no longer a buyer"; "as a beginner trader you'll find more accuracy if you're only trading when the macd is open"; no-trade sequence while "macd is against the position"; dip-buying gated the same way ("first pullback do we buy this dip the answer is yes because the macd is open"). Open = MACD line ≥ signal line (bearish cross closes it). | `candidate` — the primary intraday gate, **not implemented anywhere in the repo**: the veto's `macd_neg` leg tests the *line-below-zero* form (J-B-02), not the line-vs-signal crossover form. Testable on the intraday archive (MACD-state conditioning at candidate entries, vs same entries with the gate flipped — the pre-reg #8/#9 conditioning-campaign family). Advanced traders may trade against it ([11:30–11:45] "lower probability of success but... they can work well") — implies a directional asymmetry prediction, testable as J-B-01b. |
| J-B-02 | mfGQr2tHoX0 [14:46–14:52] | **MACD-negative variant:** "right here when the price popped back up the macd was still negative there was nothing to trade". | `candidate` — the form the paper loop's veto *does* implement (`macd_neg = MACD(12/26) line < 0`, kills the entry). His usage matches ours (negative-side no-trade), but note he treats it as the weaker, implied case of J-B-01; the crossover form is the stated primary. Intraday verdict pending (§5 floor unmet, ~mid-September). |
| J-B-03 | mfGQr2tHoX0 [15:37–15:47], [17:23–17:30] | **Front-side / pullback-count rule:** "I like to focus on trading the front side of the move the beginning of the move the first pullback the second pullback"; late re-pops are "a high-risk spot and you've got a higher likelihood of seeing a false breakout" ("in this spot I'd be done"). | `candidate` — **cross-course consistency data point**: same rule as I-B-01 (2015: "I trade the first and the second pullback... almost never trade the third") and ultimate-guide B-03; 9 years apart, unchanged. Strongest drift-map candidate for a §I.12-style update. |
| J-B-04 | mfGQr2tHoX0 [09:37–09:50] | **Gate boundary condition:** "when I first take a trade on something like this I'm not really looking at the macd in those first few minutes" — the initial breaking-news spike is exempt; the gate governs pullback/continuation entries only. | `candidate` (structural) — refines J-B-01: any MACD-gate test must stratify news-spike entries vs pullback entries or it will dilute both. Analogous stratification lesson to the I-B-06 RSI state-vs-event split. |
| J-C-01 | mfGQr2tHoX0 [16:57–17:11] | **Post-crossover stop-trading:** "imagine if you stopped trading it right there and you didn't trade it again for the rest of the day or at least until you got another crossover you would be in good position". | `candidate` — exit/re-entry side rule: after a bearish cross, stand down until the next bullish cross (not merely "skip this entry"). Distinct from J-B-01 (which gates individual entries); testable as a session-level trade-suppression rule on the intraday archive. |
| J-E-01 | mfGQr2tHoX0 [07:01–07:17], [07:17–07:41], [18:00–18:07] | **Standard-settings coordination mechanism:** "you want to see the same signals that everyone else is seeing"; traffic-light analogy ("if you say... I'm going to use a magenta light... you're going to crash your car"); "the people that are using macd will do better as a result if they use it consistently". | `candidate` (mechanism) — claims indicator profitability comes from *coordination* (everyone trading the same default signal), not from information in the indicator. Not directly measurable with bars; the measurable consequence is J-B-01 (default-parameter MACD state carries conditioning value). If J-B-01 shows no edge, this mechanism loses its support. Note: MACD is a NEW teaching vs the 2015 corpus (§I.12: "1 NEW (MACD veto, self-dated 2022)") — his own adoption story is [19:03–19:31]. |
| J-E-02 | mfGQr2tHoX0 [19:03–19:31] | **Regime-conditional utility:** MACD re-adopted during the 2022 bear market "because we were seeing a lot of false breakouts... I needed to focus on improving my accuracy". | `partial` — implicitly claims the gate's value concentrates in high-false-breakout (hostile) regimes. Testable only as an exploratory interaction (MACD-gate × regime); pre-register before any verdict. |
| J-G-01 | mfGQr2tHoX0 [20:03–20:17], [20:53–21:07], [21:16–21:33] | **Hot/cold hours rule** (via Annie Duke's *Quit*): "the best traders will trade longer... when the market's hot and will walk away even if they don't hit their daily goal when the market is cold"; "those are the days you should trade more hours"; reframe from consecutive green days to "consecutive days... you can maintain discipline". | `process guidance` — same family as I-G; not measurable on bars (would need the paper log's per-session outcomes and is self-fulfilling as stated). Logged for the process layer. |
| J-G-02 | mfGQr2tHoX0 [18:07–18:26] | Indicators "work when you follow them on every single trade you take... checking them intermittently does not work". | `process guidance` — a consistency precondition, not a testable market claim. |
| J-H-01 | mfGQr2tHoX0 [01:16–01:21], [05:18–05:26] | "it's valid on all time frames"; moving-average ribbon "all stacked above each other... very bullish". | `out of scope` — general TA framing; no operational rule beyond J-B rows. |

**Pilot summary:** 1 red flag, 5 candidates (three of which touch existing
machinery: J-B-02 = the implemented veto leg; J-B-01/J-C-01 = the unimplemented
crossover gate — the single biggest gap between his stated system and ours),
2 partial/process, 1 out of scope. Next video in priority order:
`2n2Jt0PEPss` (the $45k MACD-scalping day — will test whether the gate as
practiced matches the gate as taught).

<!-- §J-CORPUS-START -->

### 2n2Jt0PEPss — "+$45,546.52 TODAY with the 30 Minute MACD Scalping Strategy" (2024-07-23)

Topics: `macd-gate` `30-minute-window` `front-side` `pullback-count` `scanner-criteria` `red-flags` `exit-rules` `gate-as-practiced`

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| 2n2-01 | [00:53–01:15] | Day-1 headline: "traded about 12 different stocks and locked up a total of" ≈$45K (title: $45,546.52), "green day of the year". Also [52:48–53:01] "I would have had uh probably 20 trades 30 trades with 5 to 10,000 shares" and "I traded 20 two 277,000 shares" (ACTR alone) — $45.5K over ~277K shares ≈ $0.16/share, internally *plausible* arithmetic, still self-reported. | `red flag` | Same posture as I-A; single-day framing like J-A-01. |
| 2n2-02 | [04:29–05:23] | **Internal contradiction (order of magnitude):** on stock A ($2→$112) he says "I locked up just under $330,000 of profit" [04:37–04:40], but in the same segment: "I made about $118,000 on this profit in this like window right here", "I locked up 18,000 but I gave back a little bit off", "got myself to up $30,000" — and 2n2-01's day total is $45.5K. | `red flag` | The $330K figure cannot coexist with the $45.5K day total or the $118K/$30K window walk-through; "locked up" appears to mean different things (peak unrealized vs realized). Strongest self-report contradiction found in the corpus so far — worse than I-A-03's 2× discrepancy. |
| 2n2-03 | [56:18–56:31] | Cumulative: "this is $12.8 million of gross profit" (with the usual "results not typical"). | `red flag` | Trajectory escalation vs I-A-06 ($1M by 2019) and GXl's $10M (2023, GXl-02). |
| 2n2-04 | [56:52–57:11], [57:56–58:23] | **Accuracy asserted before the data exists:** "I can't import these right now I have to wait till tomorrow" — "have pretty good accuracy probably above 70%". Contrast: a losing month he "finished month um of March with $20,000" and calls "not a great month... a little embarrassing". | `red flag` | The >70% is an expectation, not a reading. Matches the corpus accuracy-window pattern (I-A-04); the +$20K "bad month" framing is itself a self-report anchor. |
| 2n2-05 | [16:39–16:52] | **Gate as stated (both forms in one passage):** "trading when macd is positive is a lot easier for me than trading when it's negative" + "initial gut check if the macd is negative which is from right here to here I'm not going to trade it". | `candidate` | J-B-01 (crossover form) AND J-B-02 (line<0 form, the repo's veto leg) stated together; here the negative-side form is the beginner "gut check". Gate-as-practiced evidence below (2n2-10, 2n2-12, 2n2-21). |
| 2n2-06 | [17:44–17:56], [18:49–18:56] | Settings: "the fast length is 12 the slow length is 26 the source is the close and the signal length is nine"; "I actually only have the macd on my one minute time frame" (charts: 10-sec/1-min/5-min/daily). | `candidate` | Identical to mfGQr2tHoX0 settings (J-E-01 coordination mechanism). Confirms veto's `macd_at` 12/26 EMA on 1-min bars. |
| 2n2-07 | [19:02–19:11], [20:22–20:52] | **New parameter — window length:** "I call this the 30 minute profit window because once the macd opens right here which was at about 8:46 it stayed open for about 30 minutes"; "generally for most stocks we have a window of you know about 30 minutes when we've got some really clean trading"; window closes at "once you get that first macd crossover for a lot of stocks that can be it you got one window it's crossing over and then from that point forward the stock is choppy". | `candidate` | Quantifies J-B-01 beyond the pilot: gate-open *duration* ≈30 min is a testable timing claim. Not stated in mfGQr2tHoX0. |
| 2n2-08 | [21:29–21:53] | **Front-side conjunct on the gate:** "the front side of the move means the stock should be making new highs around the time when we're trading it"; "even if the macd goes positive but we're not making new highs I would say it's no good" — he *rejects* a positive-MACD entry on A's late re-pop for exactly this reason. | `candidate` | Gate-as-practiced: MACD-positive is necessary but NOT sufficient; new-highs condition is a second conjunct the repo's veto does not have (J-B-02 is a single leg). Refines J-B-03. |
| 2n2-09 | [53:33–53:52] | **Exit ≠ cross; cross = trade-ban:** "so if you waited for the crossover to exit you would have held too long so I don't wait for the crossover to exit but once we have a crossover I don't want to trade it anymore" (PGHL went 4.50→10 before the cross caught up at 6). | `candidate` | Sharpens J-C-01: the bearish cross is a *stop-trading* trigger, never a *sell* trigger; exits are pre-cross weakness. |
| 2n2-10 | [51:30–52:36], [43:56–44:08] | **Walk-away behavior (J-C-01 as practiced):** "macd open stopped trading it very aggressively right here stopped trading it and I'm looking for something else"; "I'm not going to trade this one stock all day long I'm going to trade it while the windows open and then I'm going to look for the next one"; "I was up 32,000 on the day when I stopped trading" ACTR and rotated to SLRX. | `candidate` | The pilot's "stand down until the next bullish cross" (J-C-01) is practiced as stock-level session abandonment: window closed → rotate capital to the next screener hit. Second windows do reopen on fresh breakouts (A's, GFAI's in GXl-18). |
| 2n2-11 | [19:49–20:03] | Pullback count: "the third pullback ends up being a false breakout and I'm not just saying that because I'm running out of the Whiteboard it's actually true"; "usually I find that I do the best trading the first pullback right here and the second pullback right here". Also the leg skeleton: 3–5 green candles then 1–2 pullback candles ≈ 8 min into the move [19:23–19:38]. | `candidate` | Third repetition of the rule (I-B-01 2015, J-B-03 2024-05, now 2024-07) — most-stable rule in the corpus. Note the self-aware joke: the 3rd-pullback failure rate is asserted, never measured. |
| 2n2-12 | [22:48–23:21] | **New numeric veto — 50% retrace:** "we needed to at least hold the 50% line and we pulled back too much"; "although we got the crossover down here um the stock at this point was just it was not set up to make new highs". | `candidate` | Gate-as-practiced: a bullish MACD re-cross was *not sufficient* to re-open the trade because the pullback exceeded ~50% of the leg. Testable on 1-min bars (retrace-depth conditioning at re-cross entries). |
| 2n2-13 | [22:03–22:26] | Consolidation-position test: "we were holding in approximately the top you know 10 15% of the entire move"; "when a stock is consolidating at the very top of its range that is usually bullish for a breakout to the next level" (bull flag). | `candidate` | New numeric threshold: consolidation in the top ~10–15% of the move = continuation-qualified; deeper = backside. Pairs with 2n2-12's 50% floor. |
| 2n2-14 | [34:51–36:44] | Scanner criteria: "I know the stock has to be up 10% already at a minimum if it's not up at least 10% then I won't even consider it"; "I prefer to see if the stock has news breaking news news headline"; "if the float is higher than 20 million shares I won't consider it"; price "price of 2 and 20 is kind of my sweet spot" and RV 5× [35:09–35:12]. **Self-violated same day:** ACTR at "it's about $1.75 $180 but given that we've seen a lot of momentum on these lower PRC stocks" he traded it anyway. | `candidate` | Matches §D scanner rows. **Float band drift:** <20M hard here vs GXl-13's "<10M ideal, <20M fine" and D-02's <10M. The sub-$2 exception is a live internal tension with his own price floor. |
| 2n2-15 | [38:34–38:51], [55:27–55:37] | Identity veto: "I'm a little bit more skeptical because we've seen a lot of Chinese pump and dumps in the market"; on CJET ("People's Republic of China") "this is one that probably wouldn't trust unfortunately". | `candidate` (E) | An issuer-identity veto, distinct from the repo's two veto legs. Testable as a selection filter on gapper universes. |
| 2n2-16 | [14:12–14:22], [15:00–15:09] | Trend-change trigger and anti-average-down: "once we finally get the first candle that makes a new low and we step down now right here the trend has changed and we step off"; "the lower it goes the more they feel like it's a good deal to add more shares because the price is even lower and they get into the habit of averaging down". | `candidate` | Mirror of I-B-02's "first candle to make a new high": first 1-min candle to a new low = step off. Clean bar-testable exit rule. Anti-averaging-down is process (G family). |
| 2n2-17 | [42:56–43:25] | Market-structure mechanics: "those orders are only live starting at 9:30 a.m. good to cancel orders are 9:30 a.m. to 400 p.m so any price action that occurs pre-market or after hours is going past above those orders"; hence opening-bell bag-holder-sell risk, discounted because "light volume" on the daily. | `partial` | GTC mechanics are standard (F family); the *conditional* (light daily volume → few resting sellers) is the testable leg but needs float/turnover context. |
| 2n2-18 | [39:18–39:46], [41:55–42:11] | Daily-chart method: "if I Mark the top of that candle I'm not going to look at anything below it" (shadow rule — broken resistance is erased); gap-fill target: "if we break through $885 we have no resistance until $24.21 the bottom of this Gap this is called Gap fill". | `candidate` | Two daily-bars-testable structural claims: (a) resistance above a broken level is disregarded, (b) breakout above a prior gap-top implies clean air to the gap bottom. |
| 2n2-19 | [49:49–49:52], [46:44–46:52] | Execution parameters: hotkey "contrl P 10cent profit Target"; trading behavior "I'm buying on dips I'm taking profit into the move higher I'm buying on dips I'm adding on the breakout". | `partial` | 10-cent default scalp target (consistent with GXl-23's 10–15c); dip-buy/add-on-breakout scaling = I-C-02 family; needs a trade log. |
| 2n2-20 | [33:14–33:33], [31:42–31:52] | **News-spike exemption check (J-B-04) — HOLDS in practice:** the first ACTR entry on the 8:30 news was taken on price punch + volume, MACD cited as *moving*, not open: "right here it punched higher from $1.70 $180 $190 and the macd is moving the volume is increasing and I jumped in at $2". By contrast the WRNT pullback entry: "right here where I got in we were trading front side of the move right macd is open". | `candidate` | Direct confirmation of J-B-04 on trade-by-trade evidence: the gate governs pullback/continuation entries; the initial news spike is exempt. |
| 2n2-21 | [31:11–31:24] | Cross-timeframe veto application: "I could put the macd on here but certainly the macd was negative even though I'm not trading on the five minute time frame is very clear that this is not something I'd be interested in trading". | `candidate` | Supports J-B-02 robustness — the negative-side veto applied for stock *rejection* even off his trading timeframe. |
| 2n2-22 | [47:30–47:43] | Timeframe boundary of the gate: on 10-sec charts "you could put the macd on it um but it looks like you're getting you're getting some crossovers that are not actually helpful" — he removed it. | `partial` | The gate is 1-min-specific (sub-minute MACD crossovers claimed noisy). Bounds any gate test to the 1-min implementation. |
| 2n2-23 | [58:33–59:01] | Timing/metrics: "I didn't do well on Monday and Tuesday and I also didn't do well early and I didn't do well late I did well kind of in the middle of my window"; response: "in April I focused on trading during the time when I usually do better". | `process guidance` | I-B-05 family (window inconsistency); the metrics→refocus loop is process, same family as J-G-01. |

### GXl6IS4fSOE — "This Is My #1 Indicator For Trading" (2023-04-12)

Topics: `holy-grail-indicator` `macd-gate` `stock-selection` `pullback-entry` `scaling` `backtest-overfitting` `red-flags`

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| GXl-01 | [01:54–02:07] | Day framing: "up $8,530 and 96 cents this morning" "using the indicators that I'm going to share with you". | `red flag` | Self-reported single-session figure attributing the day to the lesson's indicators. |
| GXl-02 | [21:01–21:41] | "I turned an account with less than $600 into over $10 million of profit"; credibility offered as "I always have my uh my audited uh trading returns right here. This is a audit of my broker statements. My broker statements are on my website". | `red flag` | Escalation vs I-A-06 ($1M, 2017–19). Note "audit of my broker statements" conflates posted statements with an audit. |
| GXl-03 | [21:56–22:07], [1:10:20–1:10:26] | Student satisfaction: "92% of my students, this was uh over 2,200 students" gave five stars — later restated as "92% of our students who left us a testimonial said they love us". | `red flag` | The denominator shifts from 2,200 students to testimonial-leavers within the same video — a textbook selection-bias reveal. |
| GXl-04 | [59:00–59:20], [1:02:29–1:02:35] | Accuracy expectation: "have 60 70% accuracy if you have first gained experience trading in a simulator"; third-party proof: "this particular trader has verified over a million dollars of profitability. He's got a million-dollar badge" (8 months in sim first). | `red flag` | 60–70% matches the corpus long-run self-report (I-A-04) — the one stable number across the decade. The badge is Warrior-issued, unverifiable. |
| GXl-05 | [08:53–10:00] | **Abandoned automated-reversal formula (full parameters stated):** "I was looking for RSI um to be below five." + "I was looking for five consecutive red candles." + "I was looking for price to be outside Bollinger Bands." (+ a ≥50-cent move in 5 min), buy on all-met; "set a 20 cent stop and I set a 40 cent profit target. That's a two to one profit to loss ratio." | `candidate` (self-reported as failed) | Most parameter-dense rule statement in the corpus. Two tensions: RSI<5 here vs I-B-06's 90/10 (trade) and 20/80 (scanner); 2:1 R:R here vs the 10–15c/1:1 scalping plan (GXl-23) and the ~1:1 avg win/loss self-reports (I-A-04). He says automation failed on news he couldn't encode. |
| GXl-06 | [11:00–11:32] | Overfitting confession: "I would backtest them, they would show that they would have been profitable over a period of time, but then when I automated them and tried to run them forward, they didn't produce profits"; "I was essentially creating a formula and a set of indicators that perfectly matched a set of historical data." | `process guidance` | A textbook in-sample/overfitting confession — epistemically *aligned* with the repo's pre-registration posture (§6). Not a market claim; logged as the corpus's own method caveat. |
| GXl-07 | [1:05:51–1:06:00], [1:07:11–1:07:15], [13:25–13:39] | Anti-Holy-Grail thesis (the video's actual content vs its title): "the holy grail is not a indicator that's red light green light."; "Listen, prove me wrong. I'd be happy if you prove me wrong. I haven't seen it."; "I've never seen someone who's been able to take blind buy-sell indicators from an indicator, buy-sell signals from an indicator, and become a millionaire." | `process guidance` | Title/content tension: a "#1 Indicator" class whose thesis is that no such indicator exists. The universal claim is stated as invitation to falsify — the repo's exact posture. |
| GXl-08 | [04:46–05:36] | Consistency precondition: "Indicators are only helpful if they are used consistently."; "I think of an an indicator as something that I need to check consistently on every trade that I take". | `process guidance` | Verbatim family of J-G-02; a precondition on J-B-01 testing, not a market claim. |
| GXl-09 | [18:40–19:17] | Indicator stack (April 2023): "I'm using my nine EMA, exponential moving average. I've got my 20 EMA. I've got my 200 EMA" + VWAP + volume bars; MACD only "there are times that you'll see me add MACD, moving average convergence divergence indicator. I do think there are times when that can be helpful, especially in a choppy market". | `candidate` (settings) | Drift evidence for §I.12's "1 NEW (MACD veto)": in 2023 MACD is an occasional add-on; by May–Jul 2024 (mfGQr2tHoX0, 2n2Jt0PEPss) it is the core gate. The escalation is datable to ~2023→2024. |
| GXl-10 | [19:20–19:33] | MACD's role definition: MACD helps "visualize whether or not a stock is on the front side of the move, or it's going into a consolidation period." — "green light, because it tells me, "Is the stock on the front side of the move," | `candidate` | J-B-01's front-side function, one year earlier; regime qualifier ("choppy market") aligns with J-E-02 (2022 bear adoption). |
| GXl-11 | [50:33–51:02] | **The gate, line-vs-signal form, on the 5-min chart:** "the way I use MACD is if the MACD is above the signal line as it was all through here, I consider the stock to be on the front side of the move. And I'm interested in trading it."; "When we're on the backside during a bear market, I do not want to be messing around with it." | `candidate` | First explicit line>signal statement outside the pilot — confirms J-B-01's crossover form as primary (vs the J-B-02 negative-line form 2n2 emphasizes). Note the gate is here taught on the 5-min chart, on the 1-min in 2n2-06 — multi-timeframe in practice, with 2n2-22's sub-minute exclusion. |
| GXl-12 | [26:46–29:49] | **Five selection criteria:** "the stock should have five times relative volume. Now, that's that's what I prefer. Uh I I am willing to take make some exceptions to that, but my preference would be at least two times relative volume"; "the stock should already be up 10% today or higher."; "Number three, there should be a news event moving the stock higher."; "most day traders prefer stocks between $1 and $20."; float "the number of shares available to trade are less than 10 million. Less than 20 million is fine, less than 30 is okay". RV defined: "this is calculated by looking at the average volume over the last 30 days, and then what's the volume today?" Case: GFAI "Float on it was 1.28 million shares. So it traded almost 20 times the float in one day. That's called float rotation." | `candidate` **RV leg tested** NO EDGE at his stated parameters (pre-reg #24, §J.1); price/float/news/+10% legs untested. |
| §D family; RV definition (30-day average, today's volume) is operationalizable as stated. Tensions: 5×-preferred/2×-minimum here vs I-D-04's flat 5× and 2n2-14's flat 5×; float <10M ideal vs 2n2-14's <20M hard; price band $1–20 vs D-01's $2–20 and I-D-01's $2–5. |
| GXl-13 | [27:28–27:40] | **Unconditional anti-chop claim:** "It doesn't matter what indicator you use on those types of stocks, you will not find consistency." (stocks down 2–5% / up 2–3%). | `candidate` | Strong falsifiable form: indicator conditioning value ≈ 0 on non-gappers. Testable as a moderator on the veto/filter campaigns. |
| GXl-14 | [43:00–43:07], [47:30–47:38], [49:20–49:25] | Pullback count, with the data caveat stated: "Usually we see the first and second pullbacks are the best, and the third is where it gets choppy."; "The first worked. The second worked. The third failed. This is from I don't actually have the data on this chart."; and a counterexample owned: "first pullback. Second pullback, this one ended up working, and that's not common." | `candidate` | Fourth corpus repetition (I-B-01, J-B-03, 2n2-11) — but the admission "I don't actually have the data" makes explicit that the rule is anecdote, not measurement. The claimed failure mode (3rd pullback → head-and-shoulders at [47:56]) is a directional prediction testable intraday. |
| GXl-15 | [36:22–36:27], [37:13–37:53] | Operational pullback + entry spec: "The typical pullback will have two to three red candles and it can look like a bull flag."; "the perfect entry on something like this with confirmation is entering right here as soon as the first candle makes a new high with a max loss at the low of this candle"; "Your target is a retest of high of day." | `candidate` | The most complete entry spec in the corpus (I-B-02 + stop + target). Stop size is endogenous (low of confirmation candle). Needs intraday. |
| GXl-16 | [39:26–39:43] | Starter-before-confirmation: "the only reason that I do that is if I'm getting in so close to support of that moving average that it's essentially a no-brainer to take a starter because my stop is like 3 cents away". | `candidate` | Entry-location contingency (starter only when stop ≤ ~3c); I-C-02 family, needs a trade log. |
| GXl-17 | [38:45–38:51], [54:19–54:32] | Scaling/breakeven rule: "In a hot market, this is a scaling strategy that I use to add to winners."; "When I take a trade, as soon as I can adjust my stop to break even, I'm in the driver's seat." | `candidate` | I-C-02 family; note the regime qualifier ("in a hot market") — a stated regime interaction, pre-register if pursued. |
| GXl-18 | [49:31–49:37], [53:01–53:31] | **Negative-MACD stretch inside a trend, and re-entry:** "the MACD was open and then went negative during this period right here." (mid-trend consolidation); re-entry only on re-cross: "Could we get a crossover back to positive? Could. And that could give you a brand new opportunity for a trade back up to the highs."; regime context: "we've been seeing really nice moves in the morning, consolidation midday, and we've been seeing at power hour breakdown fades." | `candidate` | J-C-01 re-entry clause confirmed; the window model (2n2-07) plus re-open = a two-state gate. The morning/midday/power-hour-fade pattern is an I-B-05-family timing claim. |
| GXl-19 | [45:56–46:02] | 9EMA filter: "If a stock is below the nine moving average, that is a place to be cautious" (and "I don't usually trade if a stock is below them" re the MAs generally). | `candidate` (E-filter) | A third potential veto leg (price < 9EMA) not in the repo's two-leg veto; bar-testable intraday and as a daily adaptation. |
| GXl-20 | [46:09–46:38] | Volume leg of the veto: "You've got high volume green candles, light volume red candles. High volume green, light volume red. That's great."; and high-volume red predicts "note how this resulted in a longer, more sustained pullback." | `candidate` | The E-01 volume leg stated in its softest form (preference, not veto). Measured NO EDGE on the daily adaptation (E-01, §E.5) — this intraday form is the untested one. |
| GXl-21 | [54:07–54:13], [56:36–57:06] | Strength/weakness exit definitions: "green on the tape, the price moving quickly away from my entry, bid support, buyers on the level two."; weakness = "a sign of weakness can be a big seller appearing on the level two right where I got in or just a few pennies higher."; and "if the candle turns red while I'm in it" → out (plus hidden-seller, red-burst/false-breakout, topping-tail list at [56:43–56:58]). | `partial` | L2/tape components are out of scope (§3); the bar-testable subset: exit on first red-while-long candle; pop-then-reversal = topping tail. |
| GXl-22 | [58:30–59:08] | Small-account progression plan (chapter 14): "Focusing on one trade a day. That's it. Looking for 10 to 15 cents a share. Being very disciplined. One entry, one exit."; "If you have green days six or seven out of those 10 days of the first two weeks, which is 10 trading days, going into week three, you start to increase your share size". | `process guidance` | Needs a trade log. Note the 10–15c/1:1 geometry vs GXl-05's 20c-stop/40c-target 2:1 — two different risk models in one video. |
| GXl-23 | [41:31–41:52] | Anti-chasing: "This is called chasing. This is giving in to FOMO."; "you'll find yourself buying these tops and catching these flushes back down." | `candidate` | I-E-02 family — already measured *consistent* at daily resolution (Shape B new-high buy: NO EDGE, §B.5-B); the intraday form is untested. |
| GXl-24 | [1:05:03–1:05:10] | Setup families (chapter 8): "Blue sky daily setups. SPACs, these SPACs, recent SPACs, SPAC mergers. Low volume parabolic stocks." (+ recent reverse-split and recent-IPO setups at [1:04:46–1:05:03]). | `candidate` | Selection taxonomy; ACTR in 2n2-14 is a live example (recent 30:1 reverse split + tiny float). |
| GXl-25 | [24:23–24:29], [25:50–25:59] | Where he claims edge is absent: trading Apple daily — "I found that I was not able to develop edge."; biggest losses were impulse news trades: "a lot of the biggest losers were for me were trading on impulse when breaking news came out" (CPI prints, VIX, earnings opens). | `partial` | The large-cap no-edge claim is weakly testable (his 5-criteria universe vs mega-caps); the news-impulse ban coexists with news-as-criterion-3 (GXl-12) — catalyst wanted, *impulse* entry banned; consistent with J-B-04's stratified exemption. |
| GXl-26 | [24:53–24:56], [30:00–30:07] | Market-structure claim: "We know the majority of volume today is generated by high-frequency trading algorithms."; float-thickening: "That tends to happen more on lower price stocks for whatever reason, below $2.50." | `out of scope` | Not measurable with the repo's data; noted as his rationale for why discretionary pattern-reading beats signal-chasing on liquid names. |

### Notes (2n2Jt0PEPss, GXl6IS4fSOE)

## Summary

2n2Jt0PEPss: 23 rows (4 red flag, 16 candidate/partial, 3 process). It is the gate-as-practiced companion the pilot summary anticipated: the MACD gate is applied trade-by-trade exactly as taught (news-spike first entries exempt — J-B-04 holds in practice; pullback entries cite "macd is open"), with two *additional* conjuncts not in the pilot (new-highs requirement, ~50%-retrace floor) and a quantified window (~30 min from open to first bearish cross). Walk-away is stock-level abandonment and rotation, not "wait for the next cross on this stock". One severe internal contradiction: $330K "locked up" on one stock inside a $45.5K day.

GXl6IS4fSOE: 25 rows (4 red flag, 15 candidate/partial, 3 process, 1 out of scope). Headline findings: the earliest explicit line-vs-signal statement of J-B-01 (on the 5-min chart, a year before the pilot), a fully-parameterized *abandoned* reversal formula (RSI<5 + 5 red candles + outside-BB + 20c/40c), an explicit "I don't actually have the data on this chart" admission under the pullback-count rule, and a datable escalation of MACD from occasional add-on (2023) to core gate (2024) that supports §I.12's "1 NEW" tagging.

### UvXnnFPB1TY — How to Start Day Trading from ZERO (Full Training) (2024-04-28)

Topics: `micro-pullback` `scanner-criteria` `macd-gate` `guard-rails` `position-scaling` `morning-window` `performance-claims` `stop-placement`

Quotes mechanically grep-verified against the transcript by the extraction agent; to be re-verified at consolidation. All figures are CLAIMS, not evidence (DESIGN_BRIEF §6).

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| UvX-01 | [06:53–07:01] | "bought a cheap laptop for $1,000" … "over the next five days I made about" … "$660,000 using this laptop" | `red flag` | Narrative anecdote, unverifiable; same genre as I-A-01's $583 origin story — the "any equipment works" framing is the promotional payload around an eye-popping number. |
| UvX-02 | [52:29–53:03], [1:04:16–1:04:45] | "I have more than $12 million" … "going to show $12.6 million of gross" … "I lose too I lose about 30% of the" time; "my accuracy today well this is over" the $12M course is "68% accuracy I I'm right 68% of time and" … "$1,500 losers $1,400" "winners accuracy" 68% | `red flag` | **Internally consistent**: 30% losers ≈ 68% accuracy, $12M ≈ $12.6M. Matches the I-A-04 stable core (~68–70% long-run, ~1:1 avg win/loss) — the one figure in the corpus that has held shape across 2015→2024. Still self-reported. |
| UvX-03 | [1:04:04–1:04:14], [1:56:45–1:56:55] | First year "actually made money I made about $30,000"; second year "that all back I lost" $30,000; later: "year one I had taken the $330,000 of" "profit out to pay my cost of living so" | `red flag` | **Internal tension**: a $30K year cannot fund $330K of withdrawals — auto-caption ambiguity ($30K vs $330K, cf. the Bloomberg "$330,000" figure at [1:29:54]); the same number renders two ways in one video. Same round-number instability as I-A-03. |
| UvX-04 | [2:02:48–2:03:23] | "this is my audit report this is seven" "years of audited trading results this is"; "section $583 was day one January I made" "$116,000 that was January of uh" 2017; "2017 February 60,000 March 28,000 was" red in April; "$335,000 year 2 $499,000 year three so I" kept trading | `red flag` | Year-1 $335K matches I-A-01; Feb $60K / Mar $28K match I-A-07, but **Jan $116K conflicts with the 2015 corpus's Jan +$16K** (transcription or window shift). "Audited" is asserted, not shown. |
| UvX-05 | [1:12:00–1:12:07], [2:34:56–2:35:03] | "best year I actually made nearly $5" "million but more typically I'm averaging" less; "had a bare Market in 2022 I still made" "three quars of a million dollars or" "800,000 something like that" | `red flag` | No red year since "turning the corner" — even the 2022 bear. "Three-quarters of a million" vs "800,000" fuzz in the same breath is the signature of un-reconciled recall (E-02 lesson). |
| UvX-06 | [1:40:24–1:41:49] | $6→$36 stock day: "one went from $6 a share to $36 a share" … "where I finished up over" "$100,000 this is a insane move"; MSGM "up 3,000% in two days" multi-day continuation — "volume 17 million", "float 332,000 shares", RV "2,254 that's incredibly High" | `red flag` | Self-selected case study (the winning tail). The scanner-fields cited (price/float/RV) are the D-row criteria in action — note the case-study float (332K) is far below the stated 20M ceiling, i.e. the criteria are ceilings, not typicals. |
| UvX-07 | [2:07:34–2:07:37] | "I've got uh 10 students who" "have made over a million dollars it" works for them too — with the disclaimer that results are not typical and he doesn't track every student | `red flag` | Unverifiable survivor count; "results not typical" is doing the FTC work. n and denominator unknown. |
| UvX-08 | [1:24:42–1:26:08] | The five criteria: "price between two and 20 up" "at least 10% on the day relative volume" "of at least five" … "news cataly is preferred" … "five is float" "under 20 million shares" | `candidate` | The full pre-entry filter stack, presented as demand-side screens. Rows UvX-18/19/20 split the numeric legs for pre-registration. |
| UvX-09 | [57:10–59:50] | "the way I find stocks to trade" "each day is I'm using scanners"; "typically it is the top" "top leading percentage" gainer that gets the attention — "usually it's the number one" position "like first page of a Google Search"; "the days that I lose often" it's because I traded "that was not obvious maybe I thought it" was | `candidate` (structural) | Attention/liquidity thesis: the top gainer is the day's "allstar." Testable: rank-day-1 top-gainer performance vs #2–#5. His own loss attribution ("not the obvious stock") is a falsifiable selection claim. |
| UvX-10 | [1:34:05–1:35:00] | Fork: if the pullback "continue[s] to sell off in which case there" "is no trade and I would never press the" "buy button"; entry comes "soon as a candle makes a new high" — "this green candle breaks the high of" "this red candle that right there the" "second that I buy" | `candidate` | **Apex-break entry stated in the buy-the-break form** — the exact form the ultimate-guide §B row marks CONTRADICTED across courses. Same rule family as I-B-02 (first 1-min candle to new high). Intraday; untested as specified. |
| UvX-11 | [1:43:03–1:45:06] | Entry confirmation: at "a true Apex point then there should be a" "surge of buying because other people" see the same pattern; "and should go up like 203 cents a share" (≈20–30¢) immediately — "within the first 30 seconds if this was" the right trade; watch "orders going through right here which" (time & sales) — "I jump in I go ahead and buy this is" | `candidate` | Entry confirmation = volume surge + instant resolution; the 30-second-resolution claim is the J-B-03/I-B-03 "works instantly or it doesn't" family, now with a clock (30s) — testable as a post-entry drift window. **Volume appears here as confirmation, not as a veto leg.** |
| UvX-12 | [1:38:09–1:40:03] | "we're buying that first and second" "pullback and this is the example here of" the pattern; "this is the pattern that I trade almost" "every single day I'm using time frames" "of one minute charts primarily 1 minute" and 5-minute | `candidate` | Cross-course consistency with I-B-01 (never the third pullback — the third appears only in an example listing here, no prohibition stated). Needs intraday data. |
| UvX-13 | [1:21:32–1:21:54], [2:30:58–2:31:46] | "the stock has to be up" "10% minimum" — "instrument movement clearly shows that I" "make more money when the stock is up 10%"; Q&A: the 10% is "based on the movement of" "the entire day however the" 10% "is sort of a low threshold"; exception: "up 200% yesterday and today it's" "not up anything but it's holding" "yesterday's high I would look at that" for continuation | `candidate` | **Clarifies I-B-07**: the continuation carve-out is explicit — prior-day +200% and holding yesterday's high qualifies even at 0% today. The "10% measured on the full day" caveat matters for any scan-based backtest (look-ahead trap: the day's full range isn't known at entry time). |
| UvX-14 | [1:35:00–1:35:26] | Stop placement: "it's a 20 cent Max" "loss what's my profit Target going to be"; max loss = "loss on this position is the low of this" "red candle so that's my Max loss down" here; "Target is going to be 40 cents a share" | `candidate` | Stop = low of the pullback candle (structural, not a fixed %); explicit 2:1 reward:risk on the entry. Direct input for the §I.11 stop-placement campaign family. |
| UvX-15 | [1:48:06–1:50:53] | Exit indicators: "if I'm in a trade and I see" "stops or I see" price "sideways price" "dropping or big" "sellers these are all" "indicators to exit the" position; hierarchy: "stopping is sort of the yellow light" caution — "dropping that's when we've got the red" "light that's when we've got to get out" | `candidate` | Four exit triggers with an explicit severity ranking (stop/sideways/big-sellers = caution; dropping = exit). Testable as an exit-rule ablation against hold-to-target. |
| UvX-16 | [1:53:28–1:53:40] | "ultimate confirmation is when the candle" "makes a new low versus its" "previous candle that's when we're confirming that" the trend is shifting — time to get out | `candidate` | The exact mirror of I-B-02 (entry = first candle to a new high after a decline). Symmetric new-high/new-low rule pair; intraday-testable. |
| UvX-17 | [1:49:30–1:50:14] | Scale-out ladder: "maybe I'll sell half of" "my position to lock up a little bit of" profit when extended off the 9EMA, then more, and "I finally sell the rest" "when we get that first candle coming" "down here and now I'm out of the rest of" it | `candidate` | Partial-exit schedule tied to extension + first-red-candle; pairs with UvX-15/16 as the exit policy stack. |
| UvX-18 | [1:20:36–1:20:51], [2:00:04–2:00:10] | "I make uh the most money on stocks between" "two and $20 a share this is where I do" the best; Q&A from older data: "I should keep focusing on stocks between" "two and 10 and I should probably stop" — later expanded as time extended | `candidate` | **Price-band drift data point**: §I.12 logged $5→$20 drift across courses; this video states $2–$20 (and shows an internal $2–$10 snapshot he explicitly supersedes). Band edges are directly testable on the repo's daily bars. |
| UvX-19 | [1:22:53–1:24:13] | "that are trading with with five times" "relative volume right here"; definition: "the amount of volume that's average" "over a 30day period"; also shows the variant "relative to the 50-day" average | `candidate` | RV ≥ 5× is a core scanner leg — but **the video gives two inconsistent lookback definitions in one segment** (30-day stated, 50-day variant shown, prior-day also used). Any pre-registration must pin one definition; the discrepancy is itself a finding. |
| UvX-20 | [1:25:22–1:25:33] | "five is float" "under 20 million shares" — "when a company does an initial public offering" the shares sold are the supply available to trade | `candidate` | Float < 20M supply-side filter; consistent with the corpus (MSGM case study's 332K float is an extreme inside it). Standard data field; cheap to test. |
| UvX-21 | [49:56–50:09] | "the macd" "as a technical" "indicator is really good at helping me" "identify when I want to be focusing on" "uh trading a stock and when I want to" "just completely leave it alone all right" | `candidate` | **MACD as a trade/no-trade gate** — the J-Pilot J-B-01/J-B-02 family. Note what is ABSENT: no MACD settings or line/histogram thresholds anywhere in this video (unlike J-E-01's standard-settings coordination), and no volume-veto leg — the repo's two-filter veto (macd_neg + vol_spike) does NOT appear here; MACD is a chart-state gate, volume only an entry confirmation (UvX-11). |
| UvX-22 | [50:57–51:03] | "when that moving average" "crosses over then for me this is really" "not something that I'm going to be" "interested in any longer" | `candidate` | Post-crossover stand-down — same rule as J-C-01, here generalized to the 9/20 EMA crossover as well as the MACD convergence. |
| UvX-23 | [51:33–51:41] | "to focus on trading these on the front" "side of the move when they're making" "these really big squeezes" and "alone the rest of the day" | `candidate` | Front-side-only rule — matches J-B-03. Consistent across both corpora; a stock is tradeable only during its active squeeze phase. |
| UvX-24 | [2:34:30–2:34:38] | "I do find that I trade better" "when there's a Tailwind so when the" "overall Market is strong I'll trade" better; sluggish in weak markets | `candidate` | Market-regime filter, awareness-only (no numeric gate stated — he watches SPY "just to get a perspective"). Testable as an index-regime conditioning variable; same family as I-F-03 and the RV-conditioning campaign (§I.5). |
| UvX-25 | [1:59:36–1:59:46], [2:01:31–2:01:44], [2:04:35–2:04:40], [2:13:50–2:13:55] | From his trade log: "news was not for all of them um my best" "trades were uh" "9:30 a.m. and 11:00" "a.m. okay um"; metrics conclusion "should stop trading before 7 a.m. and I" "should stop trading after 12:00" p.m. (garbled — likely "start at 7"); routine: "around 9 a.m. I traded until 11:00 a.m."; "I learned to walk away at 11: a.m." every day | `out of scope` (daily bars) / `partial` | **I-B-05 family — THIS video states 9:30–11:00**, a fifth window variant (corpus: 9:30–12:00 / first 5–10 min / 9:30–11:30 / 9:30–10:30). The 7 a.m.–12 p.m. metrics-derived window contradicts it and is likely a transcription garble; the behavioral constant is "done by 11:00." |
| UvX-26 | [1:10:25–1:16:50] | Guard rail: "rule tools number one is Max" loss — "at minus $55,000" (transcription of $5,000); "I have a daily goal and my daily" "goal is also" $5,000; mentally allocates "up to four Max loss" "days per month one per week"; "weekly goal is actually my daily goal" "time 3 which equals" $15,000; monthly ~$50–60K; "loss is my daily goal all right so"; enforcement is externalized: "my broker and tell them to set that Max" "loss on my account so if I'm down more" "than that amount I cannot trade" | `candidate` (process, numeric) | **Transcription note**: "minus $55,000" must be $5,000 — resolved internally by "my Max loss is my daily goal" and the $5K daily goal. The rule set (max loss = daily goal, 4 red days/month budget, broker-set hard block) is self-consistent and fully parameterized. |
| UvX-27 | [1:17:01–1:17:46] | "than half of my profit after hitting my" "$5,000 daily goal I have to walk because" of the emotional response; and "I'm green on the day ,15 $1,200 and I go" "red the second I go red that for me is" "like okay it's time to walk away" | `candidate` | Two walk-away triggers: (a) give back >50% of a hit daily goal; (b) green-to-red after meaningful progress (threshold stated loosely: "a quarter or half of goal"). Mirrors the I-G red-day rule family. |
| UvX-28 | [1:45:32–1:47:20] | First-trade risk "I'll risk like $500 and if it's a winner and" up $500–$1,000 "I've broken the ice"; daily protocol: "capping my share size at about a quarter" of full size — "my starter size is 5,000 shares 20 cents is" "$11,000 of profit and until I'm up more" "than $1,000 I do not increase my share" size; then "move it up to 20,000 shares" | `candidate` | **Position-scaling rule with an unlock trigger** (¼ size → full only after +20¢/share ≈ +$1,000). Note "$11,000" is a transcription error for $1,000 (5,000 sh × $0.20; resolved by the adjacent "$1,000" figure). First trade sized so a stop-out cannot reach the daily max loss. |
| UvX-29 | [1:02:06–1:06:03] | Break-even math: 2:1 winners → "if you're right even just 33% of the" time; 1:1 → 50%; inverted → "you would have to be right 66% of the" "time in order to Break Even This is math"; advice: strive for "ratio of 2:1 aim for 2:1 where your" winners are 2× losers, "aim high for" 65–70% accuracy but "come in closer to 55"–"to 60% as a beginner and that's okay" | `process guidance` | The arithmetic is correct; note the tension — his own stated stats (68% accuracy, $1,500 losers vs $1,400 winners, UvX-02) sit in the slightly-inverted-ratio regime this framework warns beginners against; profitability rests entirely on the accuracy edge. |
| UvX-30 | [1:08:21–1:08:25] | "the bigger your" "winners typically the lower your" "accuracy will be because in order to hit" big winners you must hold through givebacks | `candidate` (structural) | Accuracy/P-L-ratio trade-off claim — the stated reason he runs base-hits (small avg wins, high accuracy). Testable as a holding-horizon sweep. |
| UvX-31 | [45:09–48:28] | Chart stack: "the moving averages I use" "are the nine the 20 and the 200" "these are all exponential moving" averages, plus VWAP and volume; pullback ladder: price "will pull back to the nine moving" "average and if it breaks that level your" "next level of support is the 20", then "the next level would be your" "volume weighted average price"; VWAP regime: "if the price is above it the Bulls are" "in control if the price is below it the" "Bears are in control" | `candidate` | Full indicator teaching with parameters (9/20/200 EMA + VWAP) — the 9EMA→20EMA→VWAP support ladder is the stop/target reference frame behind UvX-14/17. Self-fulfilling-prophecy framing ("traffic light") is his own stated mechanism. |
| UvX-32 | [2:29:45–2:30:47] | "if you can't make money in" "simulator there's no point in putting" "real money on the line"; go live after "if you have six weeks of consistent" "profitability a six week stretch of" "being green that's pretty good to" flip the switch with small size | `process guidance` | Sim-first gate with a numeric threshold (6 green weeks). Also his stated reason for pulling the live morning show off YouTube — relevant to selection bias in any corpus built from his public trading footage. |

### Notes (UvXnnFPB1TY)

## Notes for the ledger consolidation

- **Course-drift (§I.12 follow-up)**: this 2024 video ADDS a fifth morning-window variant (9:30–11:00, UvX-25) and RESTATES the price band at $2–$20 with an internal $2–$10 snapshot (UvX-18) — the band drift continues. RSI extremes are absent entirely (consistent with the 2015→ultimate-guide DROPPED verdict); MACD survives as a qualitative chart gate (UvX-21/22) with **no settings or numeric thresholds stated** — J-B-01's "line ≥ 9-signal" form is not restated here.
- **Rubric E finding**: no two-filter veto anywhere in this video. MACD = trade/no-trade gate; volume = entry confirmation only; the only hard vetoes are the five scanner criteria (UvX-08) and the "not the obvious stock" self-veto (UvX-09).
- **Internal-consistency checks that pass**: $12M≈$12.6M; 30% losers≈68% accuracy; year-1 $335K matches I-A-01. Checks that FAIL or are garbled: Jan-2017 $116K vs corpus $16K (UvX-04); $30K vs $330K year-one figures (UvX-03); "minus $55,000" max loss vs $5K daily goal (UvX-26); "$11,000" starter-size profit vs $1,000 arithmetic (UvX-28); "three quars" vs "800,000" (UvX-05). All five failures are transcription-ambiguity-shaped rather than substantive — auto-captions systematically mangle dollar figures, which argues for timestamp-checking any quote carrying a number.
- The video self-describes as a "cliffnotes version" of the Warrior Pro curriculum; several rules carry the explicit hedge that detail lives in the paid course.

### 5X_ZcifasBg — Simplest Day Trading Strategy (2022-03-27)

Topics: gap-and-go, scanner-criteria, leading-gainers, first-pullback, float, performance-claims, process-guidance

| # | Time | Claim as stated | Status | Cross-refs/notes |
|---|---|---|---|---|
| 5X_-01 | [02:56–03:02] | "you can see that i'm up uh over 12 thousand dollars i'm up 13 700 on pik" | `red flag` | Same-day self-reported P&L framing the lesson; unverifiable. |
| 5X_-02 | [03:18–03:23] | "i have over 10 million dollars in gross profit that stands behind me as a trader" | `red flag` | Endpoint growth continues (I-A-01 $335K 2017 → $10M 2022 → "audited" 2024, 3rE-01). |
| 5X_-03 | [10:57–11:05] | "it's it's up 177 right now which makes it officially and it's quarter of four the biggest gainer on wall street today and so i made 13 700" | `red flag` | Performance + rank-1-gainer selection fused into one anecdote. |
| 5X_-04 | [04:50–05:03] | "i call it the gap and go strategy that's that's kind of um … gap and go means the stock needs to be gapping up gapping up means it's opening higher than it closed the previous day" | `candidate` | Named setup definition (gap up on news → intraday continuation). Needs intraday bars. |
| 5X_-05 | [11:28–11:44] | "a lower price stock generally between two dollars and twenty dollars it's going to have an outstanding number of shares or a float typically less than 20 million shares so you can use 2020 as sort of a rule 20 million share float 20 million dollar 20 price 2020" | `candidate` | New numeric variant of the pillars: $2–$20 price AND <20M float as a paired "2020 rule". Float is **looser** than ultimate-guide D-02's <10M; price matches D-01. Drift data point for a §I.12-style update. |
| 5X_-06 | [12:41–12:48] | "i generally will look at the top five gappers so i'll look at the top five" | `candidate` | Scanner scope: top-5 gap screen. Consistent with 3rE-06's "top two or three" + D-03's rank-1 framing (which measured NO EDGE at rank 1 vs 2–10). |
| 5X_-06b | [13:31–13:42] | "one of the simplest strategies is to focus on the leading percentage gainer each day either the top two or three" | `candidate` | Softer than D-03's "number one leading percentage gainer"; the measured rank-1-vs-2–10 test didn't cover a top-2/3 definition. |
| 5X_-07 | [14:35–15:04] | "one of the safest entries is to find the first pullback so in this case this is a five minute pullback right here … this is a pullback that is right at the volume weighted average price which is our dotted line and it's right at the nine moving average … presents a really good opportunity for the first five minute candle to make a new high" | `candidate` | The corpus's core entry rule (I-B-01/I-B-02, B-01) with added VWAP+9EMA context conditions. Intraday; untested. |
| 5X_-08 | [15:18–15:28] | "this was the second pullback and it was it gave you a little continuation but it was a bit extended and this area here is now getting into sort of third pullback and it's getting uh pretty risky" | `candidate` | Pullback-count rule again (I-B-01, B-03, 3rE-16) — 2022 restatement, unchanged. |
| 5X_-09 | [15:31–15:36] | "you got a topping tail on this candle that's a little bit risky to be along following a topping tail" | `partial` | Categorical veto (topping tail after entry setup) — no parameters; kin of C-01's exit-3/topping-tail language but used pre-entry as a veto. |
| 5X_-10 | [08:23–08:32] | "a stock that is under ten dollars or under twenty dollars a share inherently is going to have a higher level of demand among retail traders because it's affordable" | `partial` | Mechanism claim behind the price pillar; the measurable consequence (lower price tiers → better forward returns) was measured **EDGE** (§I.13 F1a–F1d). |
| 5X_-11 | [09:47–09:57] | "let's see as of the last filing december 22nd the float was 7.6 million shares" | `process guidance` | Float sourced from SEC filings as daily watchlist research — process, not a threshold. |
| 5X_-12 | [16:33–16:46] | "less is more it's not a good idea to over trade it's not a good idea to take 100 trades a day it's a better idea to try to get one good trade a day because if you can get one trade a thousand shares in and out 20 cents a share that's 200 bucks" | `process guidance` | Beginner trade-frequency guardrail; G-family. |
| 5X_-13 | [15:53–16:00] | "i typically trade on the one minute and use the five minute for reference points" | `out of scope` | Execution time frame detail (D-06 family). |

### 3rEakODkiEg — ULTIMATE Beginners Guide (small-account challenge day 1) (2024-02-09)

Topics: five-characteristics, relative-volume-threshold, leading-gainers, price-tier, float, micro-pullback, exit-indicators, volume-profile, performance-claims

| # | Time | Claim as stated | Status | Cross-refs/notes |
|---|---|---|---|---|
| 3rE-01 | [00:05–00:10] | "$583 15 into more than $10 million in verified and audited trading profits" | `red flag` | Same trajectory as A-01/I-A-01 with a growing endpoint and a new **"audited"** claim; MiN-07 claims the statements are on his website. |
| 3rE-02 | [02:34–02:47] | `tested` (pre-reg #24, 2026-09-01) — **NO EDGE at his stated parameters** (50-day baseline, 5× threshold): §I.5's null is robust to his own definition (§J.1) | `red flag` | The yFo-01 claim's sibling. "500 times" is almost certainly "500 **percent**" (=5×) — see 3rE-08's "five times relative volume or [sic] 500 times higher than average". **RV threshold 5×, baseline = 50-day average volume.** §I.5 measured RV≥2.0 over prior-20 bars → NO EDGE (absolute leg); window and threshold both differ from the frozen measure. |
| 3rE-03 | [03:19–03:29] | "most stocks in the market trade within a standard deviation up or down of about 4 to 5% they rarely go up more than 4% in one day and they rarely go down more than 4% % in one day" | `candidate` | Directly testable on daily bars (distribution of |daily return|). Market-structure claim in the I-F family. |
| 3rE-04 | [03:41–03:52] | "out of thousands and thousands and thousands of stocks that are in this range of minus 4 to plus4 each day there may only be 5 to 10 stocks that are up more than 10%" | `candidate` | Measurable count claim (daily >+10% names per session); operationalizes the >10% scanner leg of 3rE-08. |
| 3rE-05 | [04:43–04:56] | "what I have found is that when a stock is up 40 50 100% even 200% 300% those are the stocks that have the highest likelihood of continuing to move higher so one of my Motts as a momentum day trader is buy high sell higher" + "I never buy a stock that's not already moving" ([05:02–05:06]) | `candidate` | Momentum-continuation selection claim; related to I-B-07 (but here continuation is the *preference*, within-day) and pre-reg #4 horizon family. |
| 3rE-06 | [06:34–06:42], [07:16–07:24] | "typically what I find is the best stocks to day trade are usually the number one or number two leading percentage gainer in the entire Market … usually when I look at my scan each day it is position one two and three these are the stocks that are going to have the most potential" | `candidate` | Rank-1 claim measured NO EDGE on daily bars (D-03, rank-1 vs 2–10, +0.00pp p=0.986); this restatement widens to top-2/top-3 — a rank-2/3-vs-rest test would be a fresh cell. |
| 3rE-07 | [10:52–11:00] | "the total number of shares available to trade is less than ideally 20 20 million shares" | `candidate` | Float ≤20M — matches 5X_-05's "2020 rule", looser than D-02's <10M. Float-parameter drift across the corpus (10M vs 20M). |
| 3rE-08 | [11:41–11:55] | "number one I want to see ideally it's got to be up at least 10% number two it should have five times relative volume number three it should have news number four I prefer stocks to be between $2 and $20" | `candidate` | A **third** pillar variant: up ≥10% (vs D-01's 30%, D-02's 25%), RV 5×, news, $2–20. The up-% threshold drifts 30%→25%→10%; news leg out of scope (brief §3). |
| 3rE-09 | [12:11–12:17] | "generally The Sweet Spot for me has been in my experience stocks between about $5 and $10 that spot is where we see big percentage gains" | `candidate` | Price-tier sweet spot. §I.13 measured the tiering direction in his favor (monotone: lt2 +6.10% > 2–5 +1.47% > 5–10 +0.53% > 10–20 +0.32% > >20 −0.08%), but the measured EDGE is *relative tiering*, not his $5–10 band specifically (5–10 earns +0.53%, less than the cheaper bands). |
| 3rE-09b | [14:47–14:57], [15:05–15:13] | "if my entry price is $6 and my Max loss is$ 5.90 I'm risking only 10 cents a share … in my opinion I should be making at least twice whatever I'm risking so if I'm going to risk a dollar I should have the potential to make a dollar" | `process guidance` | The stable 2:1 R:R floor (I-E-05 ↔ B-01 ↔ G-01). |
| 3rE-10 | [18:54–19:01] | "for beginner Traders I want to see this over 50% I'd like to see it around 65 to 70% that's around where I've been hovering for more than a decade of trading" | `red flag` | Accuracy claim, now inside the teaching itself. Same 65–70% figure as yFo-07/yFo-16, MiN-01. |
| 3rE-11 | [22:16–22:25] | "we're back in nexi it's up 29% we're coming into the open I put an order to buy at $19 this is called a half dooll whole dollar breakout" | `candidate` | Half/whole-dollar breakout entry — a distinct entry rule (psychological-level break); testable intraday. |
| 3rE-12 | [24:24–24:29] | "that means here I am three trades on day one one 8782 that's an 18% gain on day one" | `red flag` | Challenge-day self-report (+18% day 1 on a $1,000 account, 6× leverage). |
| 3rE-13 | [29:01–29:13] | "what we typically want to see on a chart pattern is that on the move up here we had high volume so the stock was cranking up on high volume and as it pulls back the volume is light" | `candidate` | The E-01 volume leg restated as a *confirmation* condition. Cross-ref §E.5: the HV-red veto leg showed NO EDGE / cut better trades on A and C — the confirmatory inverse is untested. |
| 3rE-14 | [35:41–35:50] | "I'm going to predict that because we have this really high volume red candle that the next candle is actually going to go lower significantly lower" | `candidate` | Directional event claim: HV-red candle at the top → next bar lower. The measurable core of the E-01 volume leg (§E.5 tested it as an entry *veto*, not a next-bar directional forecast — a different, cheaper test). |
| 3rE-15 | [37:53–37:58], [38:10–38:16] | "something I'll tell you is I will not trade the Third pullback … we often find by the time we come up to that third pullback that's when we start to see a longer term correction" | `candidate` | Third near-verbatim restatement of I-B-01/B-03 across 2015→2022→2024 (§I.12 row 3, SAME). Adds a mechanism: third pullback coincides with the head-and-shoulders top. |
| 3rE-16 | [41:03–41:18] | "1975 is my you know my cut that's my hard stop then what I'm going to do as it comes down to 1975 if I'm looking at 1975 on the bid and I'm seeing red on a tape and people selling I'm going to press the sell button" | `partial` | Hard-stop + tape-confirmation exit (C-04 family); the tape leg needs time-and-sales data. |
| 3rE-17 | [41:54–42:01], [44:17–44:24] | "as it comes up to to 1925 all of a sudden on the level two shows up a huge seller … if we see a stack of sellers let's say 10 or 15 sellers deep all at 1950 or at 20" | `out of scope` | Level-2 exits (C-02/C-05 family) — no book data. |
| 3rE-18 | [44:48–45:08] | "a jack knife is uh if you ever seen someone on a a diving board do a jack knife they jump up they go like this and then they go like this so when you have a stock that goes up and then goes like that in one candle that is a jack knife and we don't like to see that" | `candidate` | **New exit indicator** not in C-01's numbered five: the one-candle spike-and-reverse ("jack knife"), exit immediately. Operationalizable intraday. |
| 3rE-19 | [45:18–45:32] | "if I don't see any of those exit indicators the price is not stalling it's just going higher I'm going to hold the position as long as as possible … something I never want to do is Cap my winners" | `partial` | Hold-until-exit-indicator / never-cap-winners (C-04, which measured q99 EDGE). |
| 3rE-19b | [31:09–31:16] | "there's a 10,000 share buyer at that price that now tells me that there's bid support" | `out of scope` | Level-2 bid support at the max-loss level (C-05 family). |
| 3rE-20 | [40:52–41:00] | "when we take a trade we have a pre-established level of risk so if in the case where I get in a stock at 19 and drops down to 1975" | `process guidance` | Pre-set max loss before entry. |

### MiNV8UL18J4 — Trading was HARD Until These 3 Concepts (2024-07-27)

Topics: accuracy-claims, process-layer, macd-gate, indicator-stack, hot-cold-regime, scaling

| # | Time | Claim as stated | Status | Cross-refs/notes |
|---|---|---|---|---|
| MiN-01 | [02:59–03:04] | "my strategy right now over the last8 years of trading roughly my accuracy is like 68%" | `red flag` | Same ~68% long-run figure as I-A-04 (1,800 trades) and yFo-07/yFo-16; window here = "8 years". |
| MiN-02 | [04:05–04:13] | "those losses are part of a strategy that produces millions of dollars of profit for me" | `red flag` | Self-reported profitability used to justify the 32%-loss-rate framing. |
| MiN-03 | [01:50–01:54] | "once you have a strategy that is consistent the only difference between making $10 a day and making a 100 or a th000 is increasing your share size" | `process guidance` | Linear-scaling claim; quietly assumes the strategy is size-invariant. |
| MiN-04 | [08:22–08:30] | "there are times when the Market's colder that I'm going to say some of those strategies not worth trading and there's other times when the Market's really hot where I'm going to you know sort of fold them back in" | `partial` | Regime-conditional strategy switching (J-G-01 family); only testable as a pre-registered regime interaction. |
| MiN-05 | [08:53–08:56] | "doesn't it make sense that if 90% of Traders fail that we should try to understand the mistakes they're making" | `out of scope` | The "90% of traders fail" statistic (repeated [14:38–14:40]) is not measurable from bars. |
| MiN-06 | [13:20–13:27] | "what you do after having at least I generally would say 6 weeks of consistent profitability in a simulator that's when you flip the switch and you go live with real money" | `process guidance` | Simulator gate (G-07 family); matches e5R-09's cash-account ladder. |
| MiN-07 | [17:42–17:49] | "you can see my audited broker statements are on my website so if you're curious about my profitability it's right there for everyone to see" | `red flag` | Verifiability claim — same "verified/audited" rhetoric family; a diligence pass could check the posted statements, we do not measure it. |
| MiN-08 | [20:45–21:05] | "I I use um EMAs exponential moving averages I use the 9 the 20 and the 200 they're all EMAs that's it … I use volume weighted average price vwap so number one our EMAs number two is vwap number three I use macd" | `out of scope` | Chart stack — matches ultimate-guide D-05 exactly; 2024 restatement confirms the stack is stable. |
| MiN-09 | [21:40–21:53] | "when I pull up the macd that'll show me very clearly when the trend is Shifting so this is a spot right here where macd crossed over I see that crossover and I recognize okay it's time to step back" | `candidate` | Restates J-B-01's bearish-cross gate four months after the MACD video — cross-episode consistency for the unimplemented crossover form. |
| MiN-09b | [19:52–20:04] | "what's more important than indicators what's more important than reading an indicator is your ability to read understand and predict sentiment in the market" | `process guidance` | The anti-holy-grail frame; pairs with MiN-08 — indicators are a minority of the stated method. |
| MiN-10 | [25:30–25:41] | "you should just always trade with the exact same position size every single day rain or shine no matter what and I would argue that's a bad idea" | `process guidance` | Hot/cold sizing (J-G-01); self-fulfilling as stated. |

### e5RK1-IzFQc — I Wish I Knew This BEFORE I Started Day Trading (2024-08-24)

Topics: leverage, position-sizing-ladder, pre-market-timing, one-trade-focus, entry-exit-template, performance-claims, process-ladder

| # | Time | Claim as stated | Status | Cross-refs/notes |
|---|---|---|---|---|
| e5R-01 | [02:30–02:42] | "just in the last 3 weeks we've had multiple stocks that went up 600% which gave me two of my biggest green days that I had had in gosh must have been over a year" | `red flag` | Self-reported best-days anecdote framing the lesson. |
| e5R-02 | [03:15–03:25] | "the only reason a stock is going to go up that much in one day is because of some type of catalyst" | `partial` | Catalyst criterion (D-01 pillar 4). News leg out of scope; the *joint* claim is what made H1/H2 screens untestable — count-floor INCONCLUSIVE (§D.5). |
| e5R-03 | [11:25–11:35] | "I've been trayed my strategy for a decade so generally speaking when it comes to trading strategy if you find a strategy that's consistent you can more or less trade that strategy for a really long period of time" | `process guidance` | Strategy-stability claim; paired with the regime-change admission below (e5R-04). |
| e5R-04 | [13:37–13:50] | "my day just start earlier it used to be that I would start at 9:30 a.m. and now I start at 7:00 a.m. and the reason I start at 7: a.m. is because E Trade uh thinker swim Robin Hood a lot of these Brokers don't allow trading before 7: a.m." | `out of scope` (intraday) | Timing-drift claim: 9:30 → 7:00 start, attributed to post-2020 pre-market volume migration. Adds a fifth window to I-B-05's inconsistency list. Testable only on intraday data. |
| e5R-05 | [16:38–16:44] | "generally speaking I only take one trade at a time it's pretty rare that I'm holding two stocks at once" | `process guidance` | One-position discipline; process, not measurable on bars. |
| e5R-05b | [17:30–17:50] | "one entry based on a chart pattern and technical analysis that you understand like the first pullback on a fresh breakout following fresh breaking news … one entry first CLE to make a new high one exit as soon as you see an exit indicator such as a big seller on the level two uh coming up to psychological resistance half dollar whole dollar 200 moving average" | `candidate` | The full setup→signal→entry→exit template in one sentence: first pullback + fresh breakout + fresh news (I-B-01/B-01) → new-high entry → level-2/psych-level/200MA exits (C-01/C-02 family). Any test must stratify news-spike vs pullback entries (J-B-04). |
| e5R-06 | [18:30–18:40], [18:43–18:51] | "in the past I funded an account with like $500 $600 and used six times leverage which means with 600 bucks I've got $3,600 of buying power … that thing goes up to four I'm up 400 bucks in one trade that's nearly 100% account growth" | `red flag` | The challenge arithmetic model (I-A-06 family); internally consistent, unverifiable. |
| e5R-07 | [20:15–20:28] | "you could have a good month I want to see you make money have your first draw down where you're losing money for a couple weeks or whatever it is and recover all those losses and make new highs" | `process guidance` | Drawdown-recovery milestone before real money — a specific, checkable process gate. |
| e5R-07b | [21:06–21:17] | "you're going to take one trade a day cash account that's it one trade a day and prove to me just over the first 10 days right 10 days that's 10 trades prove to me that you can be right more than 50% of the time" | `process guidance` | First real-money gate: n=10, >50% accuracy bar. |
| e5R-08 | [21:41–21:48] | "now it's time to increase your share size by 100 shares a week so 100 shares a week just slowly bump up that share size" | `process guidance` | Sizing ramp **+100 shares/week** — drifts from ultimate-guide G-06's "+50 shares/10 days"; same family, faster ramp. |
| e5R-09 | [26:33–26:41] | "I funded an account at 25 Grand I had a lot of buying power and I had a single day where I lost $25,000" | `red flag` | Self-reported 100% single-day account blowup; same give-back genre as I-A-08's 90%-day. |
| e5R-10 | [30:54–31:05] | "maybe it's on stocks of a certain price range or it's a certain time a day or even a certain day of the week and to me when you find that little nugget of something that's working you want to lean in and double down on that" | `partial` | Self-mining prescription; operationalizable only against his own trade log, not market data. |
| e5R-11 | [32:34–32:46] | "when they take a trade they get like a 10 to1 profit to loss ratio so for instance they'll risk a th000 to make 10,000 and they might be wrong you know 70% of time but they're still making money" | `process guidance` | Break-even arithmetic internally consistent (10:1 → breakeven ≈9.1%). Same math family as I-E-05. |
| e5R-12 | [33:10–33:28] | "it's a lot easier to predict what a stock is going to do over the next 15 minutes 20 minutes 30 minutes especially if the stock has breaking news then what a stock is going to do over the next week two weeks 3 weeks so by focusing on really short intervals of time that's where I found my accuracy went up" | `out of scope` (intraday) | Horizon-decay claim; on daily bars only the *inverse* (momentum horizon decay) was measured (§D.6). |
| e5R-13 | [10:58–11:06] | "a good strategy is going to have preset um uh marks for you know your max loss your cut off when you stop when you slow down" | `process guidance` | Preset max-loss + stop-trading cutoffs (G-family; the I-G-01 three-strikes lineage). |
| e5R-13b | [25:31–25:45] | "some people think this is a rule that was put into place in 20 uh 2001 February 27th to protect individual Traders like you and I from blowing up their accounts but in fact this was a rule that was put into place to protect Brokers" | `out of scope` | PDT-rule history claim (dated February 27, 2001); regulatory trivia. |

### yFoBnM0iSlc — Relative Volume Trading Strategy (HIGH PRIORITY) (2020-07-11)

Topics: relative-volume, rv-threshold, stock-selection, coordination-mechanism, continuation, performance-by-rv, accuracy-claims, profit-loss-ratio

| # | Time | Claim as stated | Status | Cross-refs/notes |
|---|---|---|---|---|
| yFo-01 | [00:12–00:24] | `tested` (pre-reg #24, 2026-09-01) — **NO EDGE** on the falsifiable conditioning form; the 98%-of-profit form needs his trade log (§J.1) | `red flag` | **The core RV-conditioning claim: threshold RV ≥ 5, and ~98% of P&L attributed to that subset.** §I.5 (pre-reg #8) measured the analogous conditioning claim with the frozen RV≥2.0 formula: absolute leg NO EDGE × 2 (A, B); contrast leg (F2-B) +0.30pp in the claimed direction, p=0.302 — a directional whisper that never clears. His threshold (5×) is stricter than the frozen 2.0; the campaign's RV≥5.0 sensitivity also failed to reach significance. |
| yFo-02 | [04:12–04:26] | "probably the biggest indicator that a stock is going to have the potential to make a big move is relative volume" | `candidate` | RV as the primary *selection* screen (not an entry condition, not a veto). |
| yFo-03 | [05:01–05:09] | "relative volume is a measurement of today's volume versus what is normal for that stock" | `candidate` | Definition. **Parameter note:** his platform baseline is 30–50 days ([30:54–31:09]), and 3rE-02 says "50-day average" — the repo's frozen formula uses prior-20 bars (`measure_rv.py`), so the measured campaign tested a shorter lookback than he specifies. |
| yFo-04 | [05:25–05:47] | "I don't look at the total highest volume stocks … niño has the most volume today at 140 million shares" | `candidate` | RV-vs-absolute-volume contrast (NIO: most total volume, RV only 3.34). Same family as the 2015 anti-chasing I-E-02 claim. |
| yFo-05 | [07:15–07:21] | `tested` (pre-reg #24, 2026-09-01) — primary 5× **NO EDGE**; the "3 not high enough" gray zone exists only as a no-verdict sensitivity (§J.1) | `candidate` | **Internal threshold tension:** RV 3.34 "not high enough" here vs yFo-01's "5 or higher" — an unstated 3–5 gray zone. Note §I.5's near-miss sensitivity at RV≥1.0 went the *wrong* way (−0.36pp, p=0.048). |
| yFo-06 | [08:57–09:09] | "it's already a relative volume of 10 versus yesterday meaning it has 10 times more volume than it had yesterday" | `partial` | Pre-market proxy: platform doesn't populate RV premarket, so he eyeballs day-over-day volume — a *different* ratio than the 30–50-day RV he later screens on. |
| yFo-07 | [12:47–12:50] | "my act is about 68 to 70 percent" | `red flag` | Accuracy self-report; also "my accuracy is 71% right there" [31:44–31:50] and "I'm right only 68 70 percent" [27:45–27:47] — window-dependent (I-A-04 pattern). |
| yFo-08 | [18:18–18:27], [18:58–19:05] | "traditional patterns such as the first candle to make a new high will be well respected topping tail doji's will be shorted … the only reason the first candle make a new high works so well is because people respect it and they see that as an opportunity" | `candidate` (mechanism) | **The coordination mechanism, stated 4 years before the MACD video's J-E-01** ("the only reason that they work is because people believe in them" [18:41–18:53]). Cross-course consistency for the coordination mechanism — if J-B-01's default-MACD gate shows no edge, this loses support; the RV version here is the more testable form. |
| yFo-09 | [19:05–19:14], [37:47–37:57] | `tested` (pre-reg #24, 2026-09-01) — **NO EDGE**: contrasts +0.44pp (B, p 0.654) and +0.48pp (A, p 0.324) — his claimed direction again, never significant; C INCONCLUSIVE (count floor) (§J.1) | `candidate` | The inverse leg — precisely the F2 *contrast* family measured in §I.5 (high-RV vs low-RV same shape): direction consistent (+0.30pp at 2.0, +0.65pp at 5.0) but never significant. The claim as stated is the falsifiable form; his profit-concentration statements are the unfalsifiable form. |
| yFo-10 | [23:27–23:39] | "what we have to look for are stocks that have high relative volume that have really strong daily charts and that generally have some type of catalysts to justify the move" | `candidate` | Selection triad: RV + daily-chart strength + catalyst. Maps to D-01's pillars minus float/price; daily-chart leg is measurable on bars. |
| yFo-11 | [27:41–27:54] | "I suppose that happens whatever thirty percent of the time which is why I'm right only 68 70 percent but I'm still right more than I'm wrong and it's 100 percent because I focus on stocks with high relative volume" | `red flag` | Causal attribution ("it's 100 percent because") from self-reported P&L-by-bucket — observational, not causal (breakoutBot discipline); the attribution is the claim §I.5 actually tested. |
| yFo-12 | [28:32–28:37] | "so that's 3.1 million dollars trading stocks that have at least a relative volume of five" | `red flag` | The profitability-by-RV screenshot: the *measurable* form is "his profits concentrate in the RV≥5 bucket" — needs his trade log, not bars. |
| yFo-13 | [29:27–29:33], [31:24–31:31] | "this is performance by the prior day relative volume … my performance is always almost always on the stocks that have at least five times relative volume but not always five times versus the previous day because of continuation setups" | `partial` | Reconciles the threshold with continuation days: profit buckets by *prior-day* RV peak below 5× on day-2+ plays. Fresh-vs-continuation tension = I-B-07 family. |
| yFo-14 | [30:54–31:09] | `tested` (pre-reg #24, 2026-09-01) — parameters pinned (50 primary / 30 sensitivity); both lookbacks NO EDGE at 5× and 2× (§J.1) | `partial` | He is uncertain of his own platform's baseline window (30/14/50 days all floated in one breath) — the 20-bar frozen lookback is inside his stated uncertainty, so §I.5's threshold mismatch is smaller than yFo-01 suggests. |
| yFo-15 | [32:37–32:46], [33:15–33:26] | "my average winners are about a thousand my average losers are about a thousand so we would call that approximately a one to one ratio … if my profit loss ratio was two to one and my average winners were 2,000 and my average losers were only a thousand or yeah then I actually would only need to be right 33% at a time in order to break even" | `red flag` | Identical $1,000/$1,000 figures to I-A-04's 2019 self-report; breakeven math internally consistent — same arithmetic family as I-E-05/G-01. |
| yFo-16 | [35:13–35:19], [36:16–36:22] | "if you took profit every time you were up 20 cents you know what your accuracy would be pretty high … when you swing for bigger trades your accuracy goes down because you don't take the quick profit off the table when you have it" | `partial` | Accuracy-vs-P/L tradeoff as a *deliberate choice* — a mechanism explaining the 1:1 ratio; testable only on intraday trade data. |
| yFo-17 | [19:39–19:47] | "if you're trading this you're off in the weeds you're all by yourself over here" (low-RV stock) | `candidate` | Concrete low-RV case (1.1M shares); the population his veto excludes — the F2 low cell in §I.5. |

### Notes (5X_ZcifasBg, 3rEakODkiEg, MiNV8UL18J4, e5RK1-IzFQc, yFoBnM0iSlc)

## RV summary for §I.5 comparison

His RV usage is exclusively a *stock-selection screen* (premarket gap-scan → eyeball RV proxy → intraday confirmation), never an entry trigger and never a veto; the stated threshold is 5× (3× "not high enough") against a 30–50-day average baseline, with a day-over-day pre-market proxy at ~10×. The measured campaign (frozen RV = v / mean(prior 20 bars), V=2.0) therefore tests a *looser* threshold on a *shorter* lookback; both of his stated usages (yFo-01 absolute, yFo-09 contrast) were respectively NO-EDGE and directionally-positive-but-nonsignificant. The lookback uncertainty (yFo-14) means a threshold-stricter/lookback-matched re-measure would be a fresh pre-registration, not a contradiction of §I.5.

## Corpus-level observations for the consolidation pass

1. **Cross-course stability confirmed again:** first/second-pullback (5X_-08, 3rE-15), 2:1 R:R + 33%-breakeven math (3rE-09b, e5R-11, yFo-15), indicator stack 9/20/200-EMA+VWAP+MACD (MiN-08), and the coordination mechanism (yFo-08, 4 years pre-dating J-E-01) all reappear unchanged.
2. **New numeric drift:** float <20M (5X_-05, 3rE-07) vs 2025 course's <10M (D-02); up-% threshold ≥10% (3rE-08) vs D-01's 30%; sizing ramp +100/week (e5R-08) vs G-06's +50/10 days. The favorites playlist runs *looser* than the polished course.
3. **New testable candidates not in the ledger:** the 4–5% daily standard-deviation and 5–10-stocks-up-10% claims (3rE-03/04, daily-bar measurable); the HV-red-candle → next-candle-lower directional forecast (3rE-14, cheaper test than the §E.5 veto form); the half/whole-dollar breakout entry (3rE-11) and jack-knife exit (3rE-18).
4. **RV threshold conflict across videos:** 5× (yFo, 3rE) vs 10× (D-02 restatement) vs "RV 3 not high enough" (yFo-05) — the same threshold family as the I-B-06 90/10-vs-20/80 discrepancy.

### hz7vhSIXXSc — "Dip Trading was HARD Until I Learned These 3 Simple Tricks" (2024-04-24, 51:54)

Topics: dip-trading, volume-profile, 9-ema, macd-gate, micro-pullback, level-2, starter-add-scaling, daily-risk-rules

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| hz7-01 | [03:59–04:07] | "the profile that I look at I always want to see the volume is increasing as the price is moving higher that's the first step" | `candidate` | Dip checklist step 1 (B). Rising volume on the move up as buy-side confirmation; testable as volume trend before pullback low. |
| hz7-02 | [04:37–04:45] | "but the volume bar was steadily declining like that this for me um is a little bit of a red flag" | `candidate` | Price/volume divergence = veto flag (E). Operable on 1-min bars as declining volume into the high before the dip. |
| hz7-03 | [05:18–05:27] | "the macd has gone against the trade but the price is still moving higher I consider those to be sort of like caution flags" | `partial` | **Tension with J-B-01:** here MACD-against-price is a "caution flag"; later in the same video ([18:41–19:14]) MACD-open is a hard checklist item. Gate test must treat them as separate statements. |
| hz7-04 | [06:15–06:21] | "as this candle is forming I am watching the volume very closely what I do not want to see is a high volume selling candle" | `candidate` | Dip checklist step 2 (E veto): high-volume red candle on the pullback kills the setup. Operationalizable as pullback-bar volume vs prior up-bar volume. |
| hz7-05 | [14:07–14:16] | "I would say that this is an entry that has confirmation and when you ask for confirmation you pay a price" | `candidate` | Breakout entry = paying for confirmation; dip entry = pre-confirmation but better basis (B). Cross-course consistent with ultimate-guide B-02 (buy pullback, not breakout); contrasts with I-B-03. |
| hz7-06 | [15:14–15:19] | "that's offset by the fact that your max loss is the low of the pullback so if you get in right here where would you logically stop" | `candidate` | Stop placement on dip entries: stop = low of the pullback (C). Same rule restated at [23:56–24:03] ("my stop is right at the low here... that's my Max loss"). |
| hz7-06b | [23:55–24:03] | "whenever I'm taking that kind of dip entry my stop is right at the low here right whatever the low of this candle was that's my Max loss" | `candidate` | Merge with hz7-06 if consolidating; the dip-entry stop is the dip candle's low, not a fixed %. |
| hz7-07 | [17:54–18:02] | "so price should be at or above the 9 EMA if the price breaks below the 90 ma then this to me is a more sustained pullback and I don't like it" | `candidate` | 9 EMA (1-min) as dip level + veto below it (E/B). "90 ma" is a transcription of 9 EMA. Explicit flush exception at [18:04–18:08]: "it's not impossible for the price to dip below it just for a second and come back up". |
| hz7-08 | [18:41–18:53] | "I check the moving average convergence Divergence indicator and I want to see number three that Mac D is open open is when uh the average is above the signal line" | `candidate` | **Strong agreement with J-B-01** (longs only while MACD line ≥ 9-signal). Adds: "this has been a real uh game Cher for me especially trading through the bare Market of 2022 and 2023 to help me stay out of um trades that most likely we're going to fail" [19:05–19:14]. |
| hz7-09 | [20:10–20:21] | "I want to see we've come down we've sold off and I'm looking for green on the tape I want to see all of a sudden a burst of volume that's to the buy side" | `candidate` | Entry trigger = green prints on time-and-sales after the dip (B). Level-2/tape leg — needs intraday tick data; out of reach for daily bars. |
| hz7-10 | [20:41–20:47] | "I will also add that I prefer to take entries near half and whole dollars so I know that there is a significant amount of um psychological resistance" | `candidate` | Whole/half-dollar psychological levels as entry zones (B/D). Restated in the recap [51:30–51:32]: "preference is always going to be towards entries at half dollars and whole dollars". |
| hz7-11 | [22:05–22:24] | "actually like to buy in those spots because what often happens is if it can reclaim nine and hold above it then it's really a good indicator" | `candidate` | Dip-below-whole-dollar reclaim entry: burst of selling below $9 that immediately reclaims = buy (B). Related veto at [22:50–22:58]: 100,000-share seller sitting at the level = "no I'm not going to buy right". |
| hz7-12 | [22:58–23:07] | "whenever i'm looking at these dips i am naturally going to be checking the level two to confirm that we do not have huge sellers that are blocking the way" | `candidate` | Level-2 big-seller veto, listed as a "bonus" checklist item number four (E). Mirrors ywi-08; requires L2, not chart data. |
| hz7-13 | [25:16–25:30] | "I never do that because dip trading it does carry more risk the the success rate is lower but the profit loss ratio is higher" | `candidate` | Testable comparative claim: dip entries have lower hit rate but larger avg win/loss than breakouts (B/G). Same claim in ywi-12. Starter losses on failed stabs "usually those losses are less than 10 cents a share" [24:18–24:23]; "I don't mind taking a couple stabs" [24:39–24:44]. |
| hz7-14 | [25:03–25:08] | "as soon as we get our first candle that makes a new high there I often will add to my position" | `candidate` | Add trigger = first candle to make a new high after the dip (B). Same trigger used to add, not just enter — cross-ref I-B-02, J-B-03. Companion rule: "I always add to my winners I don't want to add to my losers so if it goes lower I want cut the loss and get out" [25:51–26:00]. |
| hz7-15 | [32:19–32:28] | "one of the things I always focus on is the first and the second pullback by the time we get up to the third pullback it can work but the risk is getting higher" | `candidate` | **Same rule as I-B-01** ("I never trade almost never trade the third") — cross-video consistency on pullback count. Also [46:19–46:24]: "trade just those first and second pullbacks". |
| hz7-16 | [34:00–34:08] | "this isn't a spot where I would have bought this dip you're below the N9 moving average your volume profile was higher on the selling your macd is negative I wouldn't have traded it" | `candidate` | The full no-dip bundle in one sentence (E): below 9 EMA + selling volume > buying volume + negative MACD. **Direct agreement with J-B-02** (macd_neg veto). |
| hz7-17 | [38:11–38:15] | "but once that macd crosses over right here then it's time to walk away take a break" | `candidate` | MACD crossover = session/stock exit signal, not just entry veto (E/C). He blames a $ give-back on ignoring it: "I ended up giving back a little bit off the top by trading this range with too much size" [38:04–38:11]. |
| hz7-18 | [27:55–28:01] | "ultimately being obvious usually means you need a catalyst you need some typ type of news that's bringing in the buyers" | `partial` | Stock-selection requirement: dip strategy needs a news catalyst; "if you try to trade you know like this on the S&P 500... you're just going to get chopped up" [28:06–28:12]. News leg out of scope (§3); the idiosyncratic-vs-index regime leg is testable. |
| hz7-19 | [39:10–39:19] | "now the the price is below the volume weight average price this just it's not the right place to be a buyer here" | `candidate` | Below-VWAP buyer veto (E). Cross-ref ywi-23 (same rule, stated as Q&A) and §J VWAP usage. |
| hz7-20 | [39:25–39:31] | "I focus on trading my window gener is from about 700 a.m. until uh 11:00 a.m." | `out of scope` | Intraday timing. **Fifth variant of the I-B-05 morning-window inconsistency** (9:30–12:00 / first 5–10 min / 9:30–11:30 / 9:30–10:30 / now 7:00–11:00). |
| hz7-21 | [41:15–41:24] | "I will not increase my share size until I have first made over $1,000 on the day which is 20 cents per share" | `process guidance` | Daily size cap: 5,000 shares until +$1,000 P&L (G). Cross-ref ywi-27 (small-account phase contradicts: "not to do starters, but to go all in"). |
| hz7-22 | [42:31–42:37] | "once I cross my daily goal right here I never want to give back more than half of my profit" | `process guidance` | Daily trailing-stop rule: give back >50% of peak day P&L → "I walk away I shut my computer off" [42:57–42:59]; give back 10–15% → put the cap back on [43:02–43:10]. |
| hz7-23 | [47:59–48:33] | "this is $12.6 million of profit real money accuracy 68.6%" — and "during the GameStop period I had one huge loss $240,000 loss which was terrible" | `red flag` | Self-reported, no window/log; the 68.6% matches the I-A-04 corpus band (68–70%) — internally consistent across videos but still unverifiable. Same row: avg win/loss "slightly negative it's close to 1 to one" [48:25–48:28]. |

### ywim_dUSXe4 — "How to Buy the Dip (with ZERO experience)" (2021-09-27, 95:15)

Topics: dip-trading, vwap, panic-flush, false-halt, reversal-entry, double-bottom, averaging-down, level-2, small-account

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| ywi-01 | [00:54–01:12] | "I took a tiny account less than 600 bucks and have now turned it into about 9.5 million dollars in gross profit That's gross before fees, taxes" | `red flag` | Gross-of-fees framing is itself the red flag; same trajectory family as I-A-01/A-02 and ultimate-guide A-01. Adjacent credibility claim: "you can check out my statements on warriortrading.com down at the bottom if you want to see those We do have them audited" [01:09–01:16]. |
| ywi-02 | [03:58–04:11] | "the first is buying what is uh really just simply a pullback So, a stock is generally strong but starts to pull back and you buy the pullback and then ride that momentum as it starts to curl back up through new highs" | `candidate` | Taxonomy: 3 dip styles — (1) pullback off support, (2) panic sell-off, (3) reversal off low of day [04:47–04:57]. The structural spine of the video; each style maps to separate rows below. |
| ywi-03 | [04:24–04:31] | "It drops really really hard and it can be anywhere from 5%, 10%, 20%, could even be 50%" | `candidate` | Numeric flush-depth range for style 2 (B). Also [41:53–41:59]: "the stock had just dropped from $16.00 to 14.26 That's a two point drop That's a big drop". Depth threshold is the testable parameter; no lower bound stated. |
| ywi-04 | [13:02–13:11] | "You have ascending support you have descending support you have double bottoms you have double bottoms at half dollars and whole dollars you have volume weighted average price" | `candidate` | Operational definition of a "dip": the entry is a bounce off a named support class (B/D). Enumerated again at [39:56–40:11] incl. "possibly around the 9 moving average". |
| ywi-05 | [13:26–13:32] | "Generally speaking I'm going to be more bullish buying dips when a stock is trading above the volume weighted average price" | `candidate` | Above-VWAP condition for styles 1–2 (E/B). Reaffirmed in Q&A: "my dips below VWAP would be pretty much just setup number three, reversal trades" [1:28:46–1:28:57]. |
| ywi-06 | [09:28–09:35] | "So, a dip at 773, logical stop is probably around 750. Risking around 23 cents a share" | `candidate` | Double-bottom dip entry with stop under the prior low + half-dollar level; ~23¢ risk (C). Full ladder in [09:40–10:02]: starter at 773, add at $8 (cost ~7.85), add at 823 (cost ~8.00) — add-on-strength scaling, cross-ref hz7-14. |
| ywi-07 | [14:38–14:46] | "some of the things that I look for will be a bid stack So on the level two I want to see a large buyer So if there's a big buyer at $4" | `candidate` | Positive level-2 condition: bid stack at the dip level gives entry confidence (B). Mirror of the big-seller veto (ywi-08). |
| ywi-08 | [15:09–15:21] | "there's a 50,000 share sell order at 4:05 and I'm thinking I don't know this is a double bottom but you know there's a big seller so I don't think I can go ahead" | `candidate` | Big-seller veto: chart pattern alone insufficient — "it's not just the chart pattern the level two also has to support the entry" [15:21–15:27]. Cross-ref hz7-12. |
| ywi-09 | [17:04–17:11] | "that's typically what I do when I'm buying a dip because sometimes these can dip lower and you have to be careful that you're not catching a falling knife" | `candidate` | Starter-position discipline on dip entries (G): 1,000-share hot-key starter [16:53–17:02]. Cross-ref hz7-13 ("never full size on the first entry") and the small-account contradiction (ywi-27). |
| ywi-10 | [18:12–18:21] | "So this is one of those areas where I know that there's enough people out there that are going to be buying around the VWAP and they already have orders ready to go" | `candidate` | Mechanism claim: VWAP support is self-fulfilling resting liquidity (F/structural). Testable as bounce-off-VWAP probability vs random control level. "VWAP is especially good" [18:10–18:12]. |
| ywi-11 | [18:48–19:00] | "I'd prefer to do dip trades when a stock is trending strongly when it's moving up quickly And so what you can see here your moving averages are pulling away your MACD would be opening up therefore" | `candidate` | Trend condition with MACD-open as its chart expression (B). **Agrees with J-B-01**; the inverse stated as veto: "when it starts to get into this sideways consolidation I'm really not interested" [19:10–19:14]. |
| ywi-12 | [22:24–22:38] | "I would also say that I think dip trading is a riskier strategy because general momentum trading where you're buying the first candle to make a new high, you're buying breakouts, those are easier to see on a chart" | `candidate` | Comparative claim, same as hz7-13: dips lower hit-rate vs breakouts. Cross-course tension with I-B-03 (ultimate-guide says don't buy the breakout; here breakouts are the safer baseline). |
| ywi-13 | [25:06–25:13] | "Typically in this scenario, I would be setting my stop at about $12, which means I'm risking 8 cents a share, less than 600 bucks" | `candidate` | Live dip-entry stop: whole dollar stacked on VWAP; 8¢/share risk on 6,000 shares (C). Entry mechanics at [24:32–24:41]: 6,000-share starter filled in 3 hot-key increments. |
| ywi-14 | [26:33–26:36] | "And so the first 5-minute candle to make a new high is what we would then be looking for" | `candidate` | Add/continuation trigger on the 5-min chart (B). Cross-ref I-B-02, J-B-03. He demotes 5-min setups for dips generally: "dip trading generally is not going to be focusing as much on 5-minute setups" [1:25:10–1:25:13]. |
| ywi-15 | [30:18–30:26] | "that began as a dip trade It was a dip off the volume weighted average price at 1208. And then I added into confirmation" | `candidate` | Dip → add into confirmation workflow (B/G); adds "a lot riskier... That's not something most beginner traders are going to do" [30:28–30:34]. Mid-trade profit-then-add-back: "I took half off the table at 1243... and then I added back" [28:07–29:15]. |
| ywi-16 | [39:41–39:51] | "Smaller share size, this is a stock that had pretty light volume and it was had pretty big spread, so it's a little bit a little bit riskier" | `candidate` | Liquidity/spread sizing filter (D/G): light volume + wide spread → smaller size. Positive pole at [24:07–24:11]: "It's got 10 million shares of volume, so you've got great volume". No numeric threshold given. |
| ywi-17 | [42:59–43:07] | "See right there, right there, it starts to thin out and that's where I add for a false halt trade" | `candidate` | False-halt entry: add when the book thins as price approaches the halt-down level (B). Market-structure dependent (halt mechanics); the example made "an instant trade from 14 from 13.96 up through 14.50" [43:08–43:14]. |
| ywi-18 | [46:09–46:15] | "a little cautious about not wanting to do too much bottom fishing in terms of trying to buy dips if it's just clearly going lower" | `candidate` | Repeated-dip-buying veto (E): stop re-buying a stock making persistent new lows. Companion lesson [46:17–46:21]: "not to just hold and hope that it's going to go back up cuz sometimes they don't". |
| ywi-19 | [1:01:17–1:01:30] | "what is very common is that they halt down and they open lower. In this case, it halted down and was showing to open flat So, I bought the dip at 10:31" | `candidate` | Halt-resumption read: flat projected reopen after halt-down = buy signal (F). The GME trade refused for the opposite reason: "it didn't show me a false halt, and I was like, 'I'm not stepping in front of this train'" [1:02:58–1:03:04]. |
| ywi-20 | [58:02–58:12] | "Where's the entry? The first candle to go green. When you've got five plus consecutive red candles, for me, I manage my risk that the first candle to go green is my entry and my stop is at the low" | `candidate` | Style-3 reversal entry rule: ≥5 consecutive red candles → buy first green candle, stop at the low (B/C). Trigger formulation differs from I-B-02's "first candle to make a new high" — same family, different trigger; both are stated in this video (see ywi-21). |
| ywi-21 | [1:13:59–1:14:09] | "There's a lot of traders who wait for the first candle to go green and then buy the second candle as it makes a new high That's a candle over candle pattern" | `candidate` | Conservative variant of ywi-20 (B). His stated preference on dips: "on dip trades, I usually like to have a better cost basis, which means I'm more likely to take a starter position around a half dollar whole dollar" [1:14:14–1:14:21]. Cross-ref I-B-02, J-B-03. |
| ywi-22 | [1:11:06–1:11:20] | "One, if it's the stock is panic flushing in response to a breaking news headline If news has just gotten posted and that's why the stock is dropping, I'm not going to be a buyer" | `candidate` | Primary veto (E): no dip-buying on breaking-news flushes — "that's true market reaction and algos responding to breaking news" [1:11:28–1:11:32]. **Distinct from J-B-04** (which exempts the initial news spike from the MACD gate): compatible but different boundary — here news-caused flushes are vetoed, there news-spike entries are gate-exempt. |
| ywi-23 | [1:11:37–1:11:45] | "The second, I'm generally going to be very cautious doing any type of dip trade below volume weighted average price except scenarios like GameStop" | `candidate` | Below-VWAP veto with explicit exception (E): allowed at low-of-day with "so much room to bounce back up to the volume weighted average price" [1:11:53–1:11:57]. Cross-ref hz7-19. |
| ywi-24 | [1:24:10–1:24:21] | "So, I am setting profit targets based on what I'm sort of looking at as the psychological levels So, I have usually half dollars and whole dollars and/or looking at the high of day" | `candidate` | Exit rule (C): scale out at half/whole dollars and high-of-day, not a fixed target. Holding exception: "if the range isn't too big and I'm not hitting my max dollar loss, I might be okay holding for a retest for a double bottom" [1:16:26–1:16:33]. |
| ywi-25 | [1:29:47–1:29:52] | "if it rolls over and double bottoms, then I might average down just a little bit because it's holding the support of that double bottom" | `process guidance` | **Internal contradiction on averaging down** — same answer: "then averaging down really is just making a bad trade worse" [1:29:21–1:29:24], and "I don't want to be holding it if it's then making new lows cuz that's when I get caught into the habit of averaging down" [1:12:56–1:13:02]. Related: "sometimes I will use the dip trade to help me manage my risk" [50:19–50:21] (re-buying to average cost down to breakeven). |
| ywi-26 | [1:07:08–1:07:16] | "So, I'm all out at 50. That was about a 45,000 40 about a $45,000 dip trade" | `red flag` | GME retrospective: $400 risked → $45,000 on one trade ("with a position of just 200 shares at 115 with a stop at 113.50, meaning I was really only risking like 400 bucks" [1:15:40–1:15:52]). Classic best-trade framing; "This is the day I was up 400 and 85,000 dollars" [1:07:32–1:07:36]. Same trade earlier tallied as "$10,776 of profit buying the dip" [1:04:26–1:04:30] — two windows on one trade, the I-A-03 pattern. |
| ywi-27 | [1:19:49–1:20:04] | "When I started with less than 600 bucks in my account, I went all in. So, my first trade I was all in and then I would take it all off the table once I had profit and I would take one trade a day. One trade a day. That's the small account way" | `process guidance` | Small-account sizing doctrine (G): "not to do starters, but to go all in... Once the account got bigger and was like 10, 15, 20,000 dollars, I started doing starters again" [1:21:35–1:21:49]. Contradicts hz7-21's 5,000-share cap-until-green rule — reconcilable only as account-size phases. |
| ywi-28 | [1:31:05–1:31:13] | "because what I'm primarily staring at is the level two And then I'm glancing at the chart" | `process guidance` | Execution primacy: L2/tape over charts on dip entries (G). Consistent with hz7-09/hz7-12 — the chart checklist is necessary but the trigger is the tape. Also "I always buy the dip at the ask Well, almost always" [1:26:15–1:26:19]. |

### Cross-reference synthesis

- **MACD gate agreement:** The 2024 video states the pilot's J-B-01 gate almost verbatim as dip-checklist item #3 (hz7-08) and the J-B-02 negative-MACD veto inside the full no-dip bundle (hz7-16). The 2021 video reaches the same condition via trend language — "MACD would be opening up" when trending strongly (ywi-11). One soft spot: hz7-03 calls MACD-against-price a "caution flag" minutes before making it a hard gate; a gate test should pre-register which form is being claimed.
- **Dip definition:** Consistent across both videos — a dip is a pullback to a *named* support class (VWAP, 9 EMA, half/whole dollars, prior low/double bottom, ascending/descending line), entered on the bounce with stop below that level, never a fixed percent.
- **Veto conditions are the more consistent content:** no high-volume selling candle on the pullback, no big seller at the level on L2, above VWAP (except low-of-day reversals), no breaking-news flushes, no sideways consolidation, stop after the third pullback.
- **Internal contradictions worth tracking:** averaging-down (ywi-25), morning window (hz7-20 adds a fifth variant to I-B-05), starter-vs-all-in sizing across account phases (ywi-27 vs hz7-21), and breakout-vs-dip risk ranking that sits in tension with ultimate-guide B-02/I-B-03.

### Source files

- C:\Users\Silver Pangolin\PycharmProjects\patternScanner\transcripts\warrior-trading-favorites\hz7vhSIXXSc.md
- C:\Users\Silver Pangolin\PycharmProjects\patternScanner\transcripts\warrior-trading-favorites\ywim_dUSXe4.md

### -0slMH7N6eI — How to Scalp Trade (with ZERO experience) (2022-04-11)

Topics: scalp-trading, breakout-entry, profit-taking, stop-placement, stock-selection, psychological-levels, morning-window, performance-claims

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| 0sl-01 | [05:55–06:16] | "Scalp traders will often have a one-to-one or even a negative profit-loss ratio... My average winners are about 1,300, average losers are about 1,300-1,400. It's about a one-to-one ratio." | `red flag` | Self-reported 1:1 win/loss — matches I-A-04 (68–70%, ~1:1) exactly; consistency across years, still unverifiable. |
| 0sl-02 | [06:19–06:45] | "you can be profitable with a one-to-one ratio as long as your accuracy is higher than 50%... a scalper typically will have a higher percentage of success... what that's attributed to? It's attributed to taking profits quickly." | `candidate` | Arithmetic is trivially true; the operational claim is *profit-taking speed raises hit rate* — testable as an exit-horizon sweep on the intraday archive. |
| 0sl-03 | [15:21–15:52] | "you do that same trade with 1 000 shares times 10 cents and you're up 100 bucks... that right there is 10% growth on your account in one day" | `red flag` | The 10%-per-day model ignores stop-outs; same arithmetic as I-A-06's 20-cents×9,000-shares model. |
| 0sl-04 | [1:19:03–1:19:18] | "I finished the day on JFIN up, uh, almost $100,000... $101,000 actually before fees and commissions." | `red flag` | Single-day self-report on a $12→$26 runner; cf. Airbnb IPO "$20 grand" [1:20:02–1:20:09]. |
| 0sl-05 | [1:33:48–1:34:01] | "for every time that happens, you're going to have 10 more times where the stock ends up tanking and you're going to be really glad you took your profit off the table" | `candidate` | Explicit 10:1 base rate claim for profit-taking-then-tank vs hold regret — directly testable on the exit-horizon data. |
| 0sl-06 | [05:39–05:54] | "a scalp trade should work instantly. If the scalper has a good read on the level two and the tape... the trade should work instantly." | `candidate` | Instant-resolution claim — same family as I-B-03; testable as time-to-favor post-entry. |
| 0sl-07 | [10:51–12:07] | "your entry is as it's coming up right here, you might be buying right as it it breaks this level... it goes to nine, then it goes to eight... and you punch that order" | `candidate` | Buy the break *as the offer is consumed*, not after resolution. Tension with ultimate-guide B-02 (don't buy the break); resolved by 0sl-11. |
| 0sl-08 | [12:29–12:39] | "we'll see a break of this level, a retest. So, it breaks, it retests and if it holds support, that's a long on the first pullback for a move higher." | `candidate` | Break + retest-as-second-entry; same first-pullback family as I-B-01 / J-B-03 / B-03. |
| 0sl-09 | [16:54–17:03] | "what I'm more inclined to do is to buy as it's breaking to the upside of that consolidation, which therefore is a breakout trade. You're buying for the break through the highs." | `candidate` | Explicit anti-consolidation-accumulation argument (liquidity risk of unwinding inside the range). Shape A (break-above-consolidation) measured → NO EDGE (§B.5-A). |
| 0sl-10 | [58:08–58:15] | "I bought as those were getting bought up. I waited first to see green on the tape and then I bought." | `candidate` | Green-on-tape trigger preceding the level break — the tape gate is a distinct entry-timing variable from the level itself (pairs with ZS8-09). |
| 0sl-11 | [1:00:27–1:00:38] | "I will have be happy to buy the retest after the breakout, but I'm also going to trade the breakout. So, I'm going to trade both." | `partial` | **Drift-map datum (2022)**: adjudicates the ultimate-guide B-02 tension ("better to wait for the pullback") — he trades both legs, prioritizing by momentum [1:00:52–1:01:01]. |
| 0sl-12 | [1:02:08–1:02:17] | "On this one I got in a little early to anticipate the break through that half dollar. I probably wouldn't have gotten in that early on a $2.50 stock, but on $12 stock, willing to be a little bit more aggressive." | `candidate` | Anticipation distance scales with price level — formalizable (early-entry offset as % of price). |
| 0sl-13 | [07:10–07:28] | "as a scalp trader, anytime you're right by at least 5 or 10 cents, it's going to be a winner, and that's what keeps your average so high." | `candidate` | 5–10¢ profit threshold = the scalp's exit target; testable (P(move ≥5¢ post-entry) vs P(≥20¢) with round-trip costs). |
| 0sl-14 | [12:51–13:18] | "you're taking profit, so you're long and then you take profit in this squeeze here... They'll be in a trade, they'll have 15, 20 cents of profit, they don't take any of it off the table and what ends up happening? It ends up turning into from a winning trade to a losing trade." | `candidate` | Scale-out-on-first-squeeze rule; the failure mode claim (win→loss without scale-out) is measurable as give-back distribution. |
| 0sl-15 | [23:06–23:14] | "So, as soon as you have small profit, sell half, adjust the stop to break even on the remainder of the position. So, that would be your average cost, your average entry." | `candidate` | Sell-half + trail-to-breakeven — verbatim same rule as I-C-02 (2015); cross-course consistency datum for §I.12. |
| 0sl-16 | [26:21–27:16] | "the next tip for scalp trading is to hold until the momentum slows down... as soon as I start seeing some red on the tape, or I I feel like it's a little extended, or maybe it's approaching a psychological resistance point like a half dollar or a whole dollar, that might be my cue to sell half" | `candidate` | Tape-red / extension / psych-level = partial-exit triggers; the level-2 leg is out of scope (C-02 family) but the psych-level leg is testable. |
| 0sl-17 | [27:41–28:02] | "Uh if the trade doesn't work out immediately, get out. Quick exits... if you're taking profit at 15 cents or 10 cents, you can't have 20 30 cent losses. They're going to ruin your profit loss ratio" | `candidate` | Asymmetric-loss veto: loss cap must be ≤ win target (~10–15¢) or the 1:1 model breaks — testable as stop-distance ≤ target-distance. |
| 0sl-18 | [09:19–09:27] | "scalp trades are typically, I mean, they're short. They can be one to two minutes long, sometimes longer, sometimes shorter. They could be as short as one second" | `candidate` | Holding-time claim (1–2 min modal); testable against measured GBR example ("a total trade of 20 seconds, I made $492" [57:31–57:34]). |
| 0sl-19 | [1:32:07–1:32:34] | "I might be okay with getting in at five and selling at 5:15 for $750 profit if I could do that within 1 minute. Because then I felt like I'm managing my risk by only holding this amount of money on leverage for a very short period of time. Because one of the ways you can calculate risk is your exposure time." | `candidate` | 1-minute time-stop on leveraged scalps; "risk = exposure time" is a testable holding-time proposition. |
| 0sl-20 | [43:58–44:35] | "your time frame generally for scalp trading is going to be when you have peak volume. That's typically going to be in the morning, the early hours... a stock that has a range of at least 10% today. It should have at least two times if not five times relative volume. The daily chart should be above the 90 EMA and above the 200 EMA." | `candidate` / `partial` | Scanner checklist (D/E). Note transcription "90 EMA" vs ZS8's "9 EMA" [09:05] — likely the same 9-EMA rule misheard; flag for video check. |
| 0sl-21 | [44:51–44:55] | "parabolic setups are also valid when the stock is up 50% or more." | `candidate` | Extension floor (not ceiling) — stocks ≥+50% on day remain tradeable; contrasts with 0sl-23's caution at +600%. |
| 0sl-22 | [1:16:10–1:16:29] | "one of the things that's really important as a scalp trader is to make sure you're taking profit along the way and reducing your share size the more you trade. Because the longer you get into the day, you start positioning yourself where, you know, one tr- one bad trade could really be bad." | `process guidance` | Intraday de-risking curve (size ↓ through the day) — same family as J-G-01 hot/cold hours. |
| 0sl-23 | [47:35–47:49] | "The only problem with it is that it's the wrong time of day perhaps to be taking that trade... it's not to say you can't take trades in the afternoon because you certainly can. Uh but I prefer to trade earlier in the day." | `out of scope` | **I-B-05 morning-window family, this video's variant: "peak volume... in the morning, the early hours" + "prefer earlier in the day"** — consistent core, still no fixed clock times here. |
| 0sl-24 | [48:56–49:11] | "It's easy... I do it by looking at what's the leading gainer today. And that points me almost every single day to the right stocks to trade." | `candidate` | Leading-gainer selection claim; testable as forward returns of intraday leading gainers vs market. |
| 0sl-25 | [24:55–25:31] | "I personally don't use stops in any of my orders, and the reason that I don't do that is because market makers can see your stop orders... I know how market makers will abuse retail traders through stop hunting. So... I never use live stops." | `process guidance` | No-live-stops policy (mental stop only) — repeated verbatim in ZS8x6xK8-Vk [27:55–28:57]; makes measured stop-placement a mental-stop simulation, not a resting-order backtest. |
| 0sl-26 | [21:26–22:33] | "If your accuracy through that 10-day period is 60 or 75% 60 70%, you're right on six or seven out of 10 trades, good. That's great. You should be green." | `process guidance` | 10-trade/60–70% accuracy gate for small accounts; the <50% → simulator branch is a stopping rule. |
| 0sl-27 | [1:42:06–1:42:11] | "if I was going to look at this trade, I would say not super great risk management. It came all the way back down to VWAP." | `candidate` | VWAP-retest = the accepted worst-case give-back on a scalp long; stop-placement reference level (pairs with ZS8-19, I-C-01). |

### ZS8x6xK8-Vk — Ultimate Beginners Guide to Timing Entries & Exits (2022-04-04)

Topics: momentum-checklist, first-candle-new-high, micro-pullback, max-loss, psychological-resistance, scale-out, sell-into-strength, morning-window, relative-volume

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| ZS8-01 | [04:22–04:32] | "I have uh over $11 million in gross profit trading a momentum day trading strategy that I'll be sharing a little bit with you today" | `red flag` | Same "broker statements on the footer" appeal as the corpus's "verified" claims (I-A-01); gross, not net. |
| ZS8-02 | [1:20:06–1:20:15] | "by continuing that strategy, as long as I'm maintaining 75 to 80% out of 10 trades with a 1:1 ratio, I'm going to be profitable. Anything over 50% is profitability in terms of accuracy." | `red flag` | 75–80% accuracy claim vs long-run 67–70% in I-A-04 — window-dependent accuracy again. |
| ZS8-03 | [05:51–06:13] | "I've always found that the first 2 hours are the best. And that's uh you know, it used to be from 9:30 until about 11:30. And more and more so, it's starting pre-market. So, from 7:38 until 10:30, 11:00." | `out of scope` | **I-B-05 family — this video's window: "first 2 hours," stated as 9:30–11:30 historically, now 7:38(AM)–10:30/11:30 incl. premarket.** Sixth window variant; the only one admitting premarket. Also "You can trade momentum at any time of the day" [05:42–05:51] — softens the hard-window reading. |
| ZS8-04 | [07:10–07:18] | "you want to look for stocks that have the potential to go up at least 10 to 20%, but really with a target of 50, 75, 100% or more." | `candidate` | Selection threshold: candidate stocks need ≥10–20% upside room. |
| ZS8-05 | [08:47–08:51] | "I focus on stocks with at least two times relative volume. I prefer five times relative volume." | `candidate` | RVOL ≥2 floor / 5 preferred — same numbers as -0slMH7N6eI [44:19–44:21]; cross-course consistency. |
| ZS8-06 | [09:05–09:19] | "The daily chart should be above the 9 EMA. We also would like to see it above the 200 EMA, but if it's below the 200 EMA, we'd like to see that has a lot of room to come up to the 200 EMA before it hits resistance there." | `candidate` | Daily-trend filter with a defined exception (below 200 EMA OK if room to it). Testable as a daily-gate on intraday setups. |
| ZS8-07 | [09:39–09:48] | "requirements, stock should have a catalyst or be a former runner, which is a former momentum stock. Price range between $1.50 and 20" | `candidate` | Catalyst/former-runner + $1.50–20 price band; no-news stocks vetoed later [25:36–25:45]. |
| ZS8-08 | [11:29–11:41] | "we've got this uh sell-off, the entry is the first candle to make a new high, right here. So, if you've got five, 10 plus red candles in a row, your entry is the first candle to make a new high." | `candidate` | The corpus's most-repeated entry rule (I-B-02, J-B-03, B-01/B-05): quantified here as ≥5 consecutive red candles then first new-high candle. |
| ZS8-09 | [12:56–13:04] | "what would be a bit of a more conservative entry would be waiting for the pullback to occur, and then buying the first candle to make a new high." | `candidate` | Two-tier entry: micro pullback (aggressive) vs full-pullback first-new-high (conservative). Same structure as B-01. |
| ZS8-10 | [13:20–13:50] | "if I see green on the tape... 4.95, 4.96, 4.97, 4.98, I may go ahead, and I likely will go ahead and buy to anticipate the break through this level. Sometimes I'll take a starter 5 cents or even 10 cents early, and then I will add as it approaches and comes through that level." | `candidate` | Starter-position 5–10¢ pre-level + add-through-scale-in; the anticipation window is stated in cents — testable as entry-offset sweep. |
| ZS8-11 | [24:37–24:46] | "enter the position then this is what I do. If there's high relative volume and green on the tape as it approaches the apex point" | `candidate` | The two-condition entry gate (RVOL + green tape at apex); pairs with 0sl-10's tape trigger. |
| ZS8-12 | [26:45–27:45] | "my order type is a marketable limit order... I always buy on the ask. I don't buy on the bid. I buy on the ask because if a stock is strong, I will not have the opportunity to get filled on the bid." | `candidate` | Buy-the-ask execution rule; limit capped at ~3% above ask [27:00–27:22]. Execution-slippage claims not measurable on bars alone. |
| ZS8-13 | [20:26–20:33] | "Then a question is, what is the proximity of the nearest half or whole dollar relative to the apex point? This is important because we have psychological resistance around half and whole dollars." | `candidate` | Round-number proximity as an entry-quality variable — testable: does |apex − nearest half/whole dollar| predict breakout follow-through? |
| ZS8-14 | [22:01–22:21] | "if the apex point of your chart or or of your pattern, for instance, is like $4.95, that presents a problem because the apex, the breakout spot, is just below a psychological resistance of a wall. We'd rather have an apex point be right at it or just above it." | `candidate` | **The most precise level-veto in either video**: apex within pennies *below* a round number → elevated false-breakout risk; apex at/above it → preferred. Directly testable on the intraday archive. |
| ZS8-15 | [18:07–18:15] | "First candle makes a new high right there. Max loss is the low of this pullback." | `candidate` | Stop = structural low of the pullback (not the candle low) — the B-01 stop rule restated; anchor for measure_stop_placement.py. |
| ZS8-16 | [22:52–23:20] | "if you're entering and the high here is $5, but this is $4.25, that's a 75 cent max loss. That's going to be too much risk, most likely... I'm just going to set an arbitrary stop on this at $4.75. So, you know, I'll risk 20 cents." | `candidate` | When the structural stop is too wide, override with a tighter *arbitrary* stop (75¢ → 20¢ here); admits the cost: "sometimes you get stopped out and then it'll end up ripping" [24:13–24:18]. |
| ZS8-17 | [23:50–24:07] | "If you're going to hold down 75 cents based on two to one profit loss ratio, you should have the potential to make a dollar 50. So, I'd rather hold down 15 cents with the potential to make 30 cents. 30 cents, especially on a three four dollar stock, is much more obtainable" | `candidate` | Explicit R:R sizing argument: prefers tight-stop/obtainable-target over wide-stop/wide-target. |
| ZS8-18 | [27:55–29:25] | "I do not use live stop orders, and I never have... Remember that broker dealers can see your stop order, and they can stop hunt... So, mental stop only, which means I need a button on my keyboard... It's basically a panic sell button." | `process guidance` | Identical to 0sl-25; note also [29:00–29:05] "prior to 9:30, stop orders uh aren't allowed" (factually wrong as stated; flag for correction). |
| ZS8-19 | [29:44–29:57] | "My highest risk is from the moment I am in with full size until I've taken some off the table. So, I'm going to be inclined to take some off the table. And then, I can look for continuation to add back to my position." | `candidate` | Risk-clock rationale for early partial exit + re-add; testable: is drawdown risk concentrated in the pre-first-scale-out window? |
| ZS8-20 | [30:26–30:44] | "depending on my cost basis and share size, if I see red on the tape, large sell orders, or a red candle on the 1-minute and certainly on the 5-minute, that may cause me um to go ahead and bail." | `candidate` | Exit-trigger list; the chart leg (red 1-min/5-min candle) is testable, the tape/level-2 legs out of scope (C-02 family). Same family as ultimate-guide C-01. |
| ZS8-21 | [30:46–31:14] | "using my hot keys, I sell into strength and I avoid hitting the bid at all costs because it feeds weakness and it will hurt my existing position... When I see red like that, I interpret weakness." | `process guidance` | Sell-into-strength doctrine; its measurable residue is the exit-price distribution, not bar timing. |
| ZS8-22 | [32:30–32:44] | "I can send order to take a uh quarter of my position off the table of 15 cents or 25 cents... Um stop the rest at average cost. All right. So, stop it which is break even." | `candidate` | Profit-target ladder (quarter off at +15/25¢) + breakeven stop on the remainder — same family as 0sl-15 / I-C-02. |
| ZS8-23 | [35:59–36:12] | "I would start by focusing on breakout trades. Breakout trades are where you're going to have high volume. It's where you're going to have breakout or bailout instant resolution. When they work, they work right away. When they don't work, they don't work. There's no guessing." | `candidate` / `partial` | Dip-trading veto for beginners ("dip trading is not the place to start" [35:37–35:40]) — same continuation/dip-riskier family as I-B-07, and in tension with his own repeated dip-buys in both videos' archives. |
| ZS8-24 | [38:37–38:52] | "Now, you pay a higher price for confirmation, but you avoid the risk of false breakout... if this drops back down to 11:60, you'd look back at the chart and you'd be like, 'Why did you even buy it?' You didn't get the first candle to make a new high." | `candidate` | Confirmation-price premium claim: anticipating costs ~5–10¢ but avoids false breakouts — testable as anticipation vs confirmation entry P&L on the same events. |
| ZS8-25 | [39:41–40:12] | "This is a chart that I would say is multi-time frame alignment... Now, there's a little bit of a red flag on the 5-minute chart and that is that the high of day volume uh the highest candle was a red doji, which is a reversal indicator, and it's on fairly high volume... It's also just a little extended off its nine moving average" | `candidate` | Three confluence filters: (1) 1-min+5-min agreement (B-06 family), (2) high-volume red doji at HOD = reversal veto, (3) extension off the 9MA — all conditionable on intraday bars. |
| ZS8-26 | [41:31–41:42] | "But of course, it'll break quickly because that's the apex point. So, I'll probably want to get in this around maybe 1245, 1248, just a little bit under that level to catch that break through that level." | `candidate` | Anticipatory entry 2–5¢ under the apex (12.50) — a concrete offset parameter for the entry-timing measurement. |
| ZS8-27 | [42:23–42:57] | "Well, your stop is 1250 because that's the pivot... So, 1250, because that's a place where a short seller will likely cover, you should see short covering to help propel the stock through that level." | `candidate` | Mechanism claim: resting short stops at the pivot supply the breakout fuel — testable as volume/velocity burst at round-number pivots vs non-pivot highs. |
| ZS8-28 | [45:10–45:17] | "And if you're aggressive, you could buy a dip off of 1250 or 1255 with a stop at 1248. Right? Because again, you're setting your stop right underneath psychological support." | `candidate` | Dip-buy stop = 2¢ below the psychological support level — a concrete stop-placement rule (just-under-level stops); pairs with 0sl-27's VWAP-retest risk frame. |
| ZS8-29 | [46:31–46:48] | "This is a 1-minute micro pullback. So, on the 5-minute, this is a 5-minute bull flag. We have resolution. And this on the 1-minute we would call the first pullback following the 5-minute breakout" | `candidate` | Nested-timeframe entry hierarchy: 5-min breakout → 1-min first pullback. |
| ZS8-30 | [53:19–53:25] | "To manage risk, I take a little off the table into that squeeze. Right? So, took a little off the table there, new orders ready to add back." | `candidate` | The scale-out-into-squeeze / re-add-on-micro-pullback cycle — the operational loop behind 0sl-14. |
| ZS8-31 | [56:41–57:03] | "We've got our clock right up here. It's showing 10:22 and 40 seconds. How many seconds do we have left on this 1-minute candle? We've got 20 seconds left... So, what we're looking at here is first candle to make a new high." | `candidate` | Intra-candle timing: entries cluster late in the candle; testable against entry-time-within-bar distribution. |
| ZS8-32 | [1:03:47–1:04:05] | "What's my max loss? Technically, the low of that candle, 1570-ish. But, I'd rather set the stop tighter at around $16. So, stop is 16, which means on this trade I'm risking 400 bucks... right here I'm up 200 bucks, which is okay cuz that's a one-to-one risk-to-reward ratio." | `candidate` | Third stop variant: structural candle-low (48¢) tightened to a round level (16.00, ~19¢) for a ~1:1 R:R; complements ZS8-15 (structural) and ZS8-16 (arbitrary). |
| ZS8-33 | [1:05:22–1:06:07] | "See that 10,000 share order right there?... if I buy here at 1654, 5,000 shares, I can always turn around and sell to 1648, the 10,000 share buyer. So, I'm really only risking a couple cents... that trade was based almost entirely on level two." | `out of scope` | Level-2-based entry with a defined exit-bid — no-level-2-data boundary (C-02/C-05 family); a strategy subset we cannot reproduce. |
| ZS8-34 | [1:09:19–1:09:31] | "This was a small account challenge, so I wanted to wait for confirmation and take a quick trade through the highs. So, the entry is going to be a little closer to 27. I need more confirmation to trust it. Paying a higher price for that, the winner will probably be a little smaller" | `candidate` | Account-size-dependent confirmation distance: small account → enter closer to the apex, accept smaller winners. |
| ZS8-35 | [1:17:52–1:18:12] | "one cent spread is not necessarily a good thing... a a a spread of three to five cents or five to 10 is totally fine. Uh that's not a big deal." | `candidate` | Spread-band selection filter (3–10¢ preferred over 1¢) — inverted from naive "tight spread good"; testable as a conditioning variable. |

### Notes (-0slMH7N6eI, ZS8x6xK8-Vk)

## Notes

- **Morning-window tally (I-B-05 drift check, both videos):** -0slMH7N6eI gives only "the morning, the early hours" [43:58–44:04] plus "I prefer to trade earlier in the day" [47:47–47:49] — no clock window; ZS8x6xK8-Vk gives the corpus's **sixth** window variant: "first 2 hours" = 9:30–11:30 historically, now 7:38–10:30/11:30 including premarket [05:51–06:13]. Neither conflicts with the existing four; the 2022 state of the claim is "earliest hours, window drifting premarket-ward."
- **I.12 drift data points (both 2022, between the 2015 corpus and the 2025 ultimate guide):** (1) first/second-pullback and first-candle-new-high rules unchanged (ZS8-08/09 ↔ I-B-01/J-B-03); (2) sell-half-to-breakeven unchanged (0sl-15 ↔ I-C-02); (3) RVOL 2/5 floor unchanged (ZS8-05 ↔ 0sl-20); (4) the breakout-vs-pullback tension of B-02 is explicitly adjudicated as "trade both" (0sl-11); (5) no-live-stops/stop-hunting doctrine already present in 2022 (0sl-25, ZS8-18); (6) daily-chart 9-EMA/200-EMA filter present in both 2022 videos — note the "90 EMA" transcription in -0sl [44:23] vs "9 EMA" in ZS8 [09:08].
- **Stop-placement taxonomy for measure_stop_placement.py (pre-reg #14 family):** three distinct anchors appear across these two videos — structural pullback low (ZS8-15), tightened arbitrary/round-level stop when the structural stop is too wide (ZS8-16, ZS8-32), and just-under-psychological-support (ZS8-28) — plus breakeven-after-scale-out (0sl-15, ZS8-22) and VWAP-retest as the accepted worst case (0sl-27).
- Everything above is a CLAIM, not evidence; nothing here is pre-registered or measured (DESIGN_BRIEF §6).

### ul34Jfh-LOk — How to Read Candlestick Charts (with ZERO experience) (2023-11-29)

Topics: `candle-anatomy` `bull-flag` `flat-top-breakout` `abcd` `vwap` `moving-averages` `volume-profile` `multi-timeframe` `daily-levels`

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| ul3-01 | [03:04–03:41], [03:55–04:29] | "at the top of that move if I ... see this candle right here I know that ... it's about to change directions ... this candle is called a shooting star ... it's a candle that shows a reversal may ... be coming"; hammer: "it occurs after the price has been ... declining it's considered to be ... hammering out the base ... indicating a possible reversal". | `candidate` | Single-candle reversal definitions; "same message whether it's red or green" ([03:43–03:52]). No body/wick proportions given — detector definition is incomplete as stated. Daily-bar shape campaign (§B.5) found NO EDGE for Shapes A/B/C; these are intraday-shape definitions, untested. |
| ul3-02 | [05:00–05:11] | "place that I really get interested in ... the shape of a candle is when the price ... is reaching really high levels we're ... getting really high extension". | `candidate` | Conditioning gate: reversal-candle shapes only signal at extension extremes. Same state-vs-event structure as I-B-06 (RSI extremes) — a pre-registered test must stratify extension vs mid-range occurrences. |
| ul3-03 | [07:15–07:26] | "what we look for in this pattern is for ... the price to break to the upside of this ... line here for the first candle to make a ... new high and then we look for the price ... to move back to New highs". | `candidate` | Bull-flag trigger = first candle to make a new high after the flag — the same trigger as I-B-02 and 4Pc-12. Most-repeated entry trigger in the corpus. |
| ul3-04 | [07:55–08:13], [08:31–08:41] | "three small body red k candles they're ... not a huge body red candle they're not ... communicating a massive reversal this is ... just an orderly pullback and so when we ... get this type of formation we look at ... this as a buying opportunity"; sideways: "it could just sort of slow down and go ... no trade there whatsoever". | `candidate` | Pullback-quality criterion (small-body red = orderly; big-body red = pattern break) + a sideways veto. Intraday-only as stated. |
| ul3-05 | [11:18–12:03] | "we'll see anywhere from one candle of ... pullback to three I don't usually like ... to see four candles of pullback I do not ... like to see the pullback here retrace ... more than 50% of this initial move"; 4–6 red candles = "out of steam that's not good either". | `candidate` | Numeric flag parameters: 1–3 pullback candles, ≤50% retrace. Identical 50% threshold in HYo-06 — cross-video consistent. |
| ul3-06 | [12:13–12:41] | "I like TR to trade the first ... pullback right here the first bull flag ... and I like to trade the second one right ... here I have often found that after the ... first two when you get into the third ... the fourth the fifth they're not as ... clean". | `candidate` | First/second-pullback rule — verbatim same rule as I-B-01 (2015) and J-B-03; third corpus-wide repetition. Strongest unchanged rule family across 9 years (§I.12 SAME). |
| ul3-07 | [13:26–13:53], [15:04–15:12] | "breakout pattern occurs when the price ... is hanging out right underneath the ... highs ... it pushes the stock through this level ... and when it finally breaks out we ... usually get a nice big longbody green ... candle"; "all of the price action is within like ... 10 15 cents it's like right underneath ... the high". | `candidate` | Flat-top-breakout definition with a numeric consolidation band (10–15¢ below the high). Intraday-only parameter. |
| ul3-08 | [14:49–15:37] | "so long as ... when it pulls back here it doesn't break ... below this price here so this becomes an ... ascending support line that has to hold"; "then is really a failed bull flag that"; verdict: "pattern is just fine I really like that ... one". | `candidate` | ABCD = failed bull flag with second pullback; he likes it. **Internal contradiction:** HYo-09 (2024-04) calls the same ABCD "not my favorite ... it fails on the first attempt". |
| ul3-09 | [17:29–20:05] | "if the price is below the ... equilibrium well that's when you've got ... the Bears ... if you're above the volume ... weight average price that's when you're ... bullish"; dip-off-VWAP is "essentially is buying very close to ... support with profit Target back up to ... high ... so your profit to loss ratio is ... great". | `candidate` | VWAP as regime filter + fade/dip setups with stop just beyond VWAP. Testable only intraday (VWAP is session-defined). |
| ul3-10 | [23:05–24:19] | 9 EMA: "represents during these flag patterns a ... good place to take that entry"; "take a starter right here at the 9 with ... my stop loss at the 20"; hold rule: "I'm happy to keep holding a position" while price "doesn't stay below it". | `candidate` | 9EMA entry / 20EMA stop bracket — same family as I-C-01/I-C-03 and repeated in 4Pc-05. |
| ul3-11 | [26:35–27:28] | "high volume ... green candles light volume red candles ... on the pullback and then volume coming ... back in for the next leg up"; failing it: "this is if anything a ... short with a stop at the high or it's ... not a trade at all". | `candidate` | Volume-profile rule (high-vol green / light-vol red on pullback) — repeated verbatim in HYo-04 and 4Pc-05. The veto leg (high-volume red on pullback → short-or-no-trade) is the testable form. |
| ul3-12 | [29:53–30:12] | "we like to see ... multi-time Frame Alignment where I could ... look at this on a one minute chart and ... say yes I like this trade ... say yes I like this trade I take it" (1-min and 5-min agree, else pass). | `candidate` | Multi-timeframe-alignment gate; also in HYo-14 (doji on 1-min blocks an add). Needs intraday data. |
| ul3-13 | [45:14–45:23] | "based on over 24,000 trades that I've ... taken so I have a lot of metrics that ... back up the choices I make". | `red flag` | Performance/authority claim; unverifiable, same posture as I-A. |
| ul3-14 | [47:39–48:32] | Checklist: "I check the float how much ... it's up on the day how many shares of ... volume it has uh the relative volume"; veto: "25% versus yesterday but it was up 50%" off the high means "I would say no that chart's ... broken"; daily chart: "if we have any gaps ... if we have any windows". | `candidate` | Stock-selection sequence (float, %up, volume, RV, news) + "broken chart" veto (down a lot from intraday high). Float as filter input already approved (§9 decision 7, I-D-06); the broken-chart veto is intraday. |
| ul3-15 | [50:07–50:33] | "the first level that that ... look at as resistance is that 200 moving ... average"; veto: "if ... we're right below it I'm not likely to ... trade because I know we're going to have ... resistance at that price". | `candidate` | Daily 200MA as first resistance for beaten-up names; don't buy within pennies of it. Testable-daily (distance-to-200MA at entry vs forward return) — cross-ref F-03, untested. |

### HYoQYCBW4sw — Master This ONE Candlestick Pattern TODAY (Full Training) (2024-04-01)

Topics: `micro-pullback` `bull-flag` `volume-profile` `first-red-candle` `green-tape-entry` `scanner-filters` `abcd` `risk-sizing` `whole-dollar-levels`

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| HYo-01 | [00:23–00:29], [52:00–52:06] | "if I could choose ... only one Candlestick pattern to use for ... the rest of my career it's the pattern" — and at the close: "because if I was only going to trade one ... chart pattern for the rest of my life ... the micro pullback". | `candidate` | **"The one" = micro pullback / bull flag.** Consistent with ul34's bull-flag primacy but narrower: ul34 (5 months earlier) elevates three patterns equally. |
| HYo-02 | [12:50–13:05], [16:29–16:35] | "bullish a big green candle that opens at ... the bottom and closes at the top ... high that is the strongest candle you ... could get" (no wicks = strongest); long upper wick = "showing that the sellers were able to ... push the stock back down within this ... Candlestick period". | `candidate` | Bullishness ranking by wick/body geometry — operationalizable as a shape score. Doji named as indecision at [16:58–17:09], consistent with ul3-01/ul3-02 naming. |
| HYo-03 | [27:14–28:24] | Scanner filters: "want to see if the price is up 10%" + "price is between $1 and $20" + "it's got high ... relative volume" + "the number of shares available to trade ... is less than 10 million" + "demand of course is created ... number five by news"; then "patiently for the first pullback" [29:26]. | `candidate` | Five-filter scanner. Price band here is **$1–20** — vs 4Pc's $2–20 and I-D-01's $2–5/$2–10 drift. Shares <10M ≈ low-float (I-D-06). |
| HYo-04 | [31:19–31:34], [41:50–41:57] | Definition: "couple of candles going up it could be ... one big candle it could be three or four ... but what I'm going to wait for is the ... first candle that goes ... red"; naming: "call that pattern a bull flag 10c time ... frame or 1 minute time frame this is ... going to be be uh a micro pullback" (≥5-min = bull flag, ≤1-min = micro pullback). | `candidate` | THE pattern, fully specified: impulse leg of 1 or 3–4 candles, entry armed on first red candle. Timeframe-dependent naming — any detector must be timeframe-aware. |
| HYo-05 | [32:06–33:03] | Confirmation: "relatively light volume on these green" candles but "the red candle candle a high volume red" = "that is not what I want to see"; wanted form: "high volume on ... green candles light volume on red ... candles". | `candidate` | Volume-profile confirmation + explicit CZ counterexample (high-vol red 774→668). Verbatim same rule as ul3-11 and 4Pc-05 — most consistent cross-video rule in all three videos. |
| HYo-06 | [34:07–34:20] | "a small red ... candle that's not bigger than previous ... candles and it's okay if there's two I ... would say however if there's three if ... there's four well now this is starting ... to not look so good". | `candidate` | Pullback-length parameter: ≤2 small red candles ok, 3–4 = degraded. Matches ul3-05's 1–3 (wobble: ul34 tolerates 3, HYo says "okay if there's two"). |
| HYo-07 | [34:24–34:51] | "as a rule of thumb I never want to see the price ... retrace more than ... 50% of the move"; "retrace more than 75%"; ideal "in the top 25% of the move". | `candidate` | **Internal wobble within one video:** hard veto 50%, soft preference >75%, preference top-25%. Three thresholds for the same rule; a pre-registration must pick one. Matches ul3-05's 50%. |
| HYo-08 | [35:36–35:54] | "I don't need to ... wait for this candle to actually close ... once I see green orders coming in that's ... when I initiate my buy order". | `candidate` | Entry trigger is tape-based (green prints), pre-candle-close — needs tick data, not bars; strictly finer than the first-new-high trigger (ul3-03). |
| HYo-09 | [36:05–36:41] | "my Max loss on this trade is now the ... low of this pullback"; worked example: "got in this at $6.60 and my stop is 650 ... my target on this most likely would be ... seven". | `candidate` | Stop = low of pullback (~10¢), target = prior high (~2:1). Same stop-placement family as I-C-01 and 4Pc-13. |
| HYo-10 | [38:20–38:36] | "this pattern is called an A B C ... D pattern it also looks like a w ... here"; "it's not my favorite ... reason it's not my favorite is cu it ... fails on the first attempt pulls back ... and it goes on the second". | `candidate` | **Internal contradiction with ul34:** ul3-08 "pattern is just fine I really like that one". Same corpus, 5 months apart, opposite preference. |
| HYo-11 | [39:23–39:27] | "we actually break the ... low of this last pivot at that point we ... know it's over". | `candidate` | Exit = break of last pivot low — trend-invalidation exit; same family as I-C-01 and 4Pc-15 (first candle to a new low). |
| HYo-12 | [42:14–42:19] | "even though I've made ... more than $10 million of verified and ... audited trading profits". | `red flag` | Self-reported performance framing the lesson; "verified and audited" is doing the same unverifiable work as I-A-01. |
| HYo-13 | [43:43–44:37] | "with small accounts you should only risk ... 3 to 5% on one trade okay ... I don't really follow that rule when it ... comes to trading in a small account"; sizing: "95% of my buying power", "realistically on this I'm risking ... about $300" on the $1,181 account (~25%). | `red flag` | Risk-process red flag: he states the standard rule and then exempts himself; ~25% account risk per trade vs the quoted 3–5% norm. G-family. |
| HYo-14 | [48:11–48:43] | "I would wager that the next ... area resistance will be at the next half ... dollar whole dollar"; "respect at half dollars and whole ... dollars"; mechanism: "orders to take profit at half dollar and ... whole dollars they're just very" memorable. | `candidate` | Round-number (50¢/$1) support/resistance clustering with a coordination mechanism. Testable-daily and intraday; untested. |
| HYo-15 | [50:20–50:58] | Doji on the 1-min: "because we have a dogee ... candle" → "I'm not confident to ... add back" even though the 10-sec "looks okay" → "we do not have multi-timeframe alignment". | `candidate` | Veto leg of multi-timeframe alignment (ul3-12): a weaker-timeframe conflict blocks adding even when the faster frame signals. Intraday-only. |
| HYo-16 | [52:09–52:12] | "the whole concept here is that we've got something that's moving" — pattern requires a news-catalyzed mover (sequence: news [23:14–23:27] → scanner [24:45–25:13] → wait for pullback). | `out of scope` / `partial` | The catalyst leg is out of scope (§3: no news in the loop); the price-reacts-first ordering is consistent with I-B-08's catalyst-first selection. |

### 4Pc_von1wS4 — Reading Candlestick Charts Was HARD Until I Learned This 3 Step Trick (2024-05-07)

Topics: `indicator-simplification` `macd-gate` `relative-volume` `first-new-high` `stop-placement` `exit-indicators` `sell-half-hotkey` `vwap`

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| 4Pc-01 | [02:04–02:12] | "more than 20 ... different indicators on this chart right"; step one: "fewer indicators is better". | `process guidance` | Chart-construction discipline; sets up 4Pc-02. |
| 4Pc-02 | [05:11–06:59] | Indicator set: "the 9 the 20 and the 200" EMAs; "and the 50 and the 100 I use the nine I ... actually like it just a little bit more ... than the 10". | `candidate` | 9/20/200 EMA set (9 not 10) — matches ul3-10 exactly. Parameter choice ties to the coordination mechanism J-E-01. |
| 4Pc-03 | [08:17–08:21] | "as a long biased Trader ... I'm going to focus on trading when the ... price is above vwap" (below VWAP = Bears, above = Bulls, [07:50–08:15]). | `candidate` | VWAP regime filter, long-bias-only — same claim as ul3-09, restated 5 months later. Intraday-only. |
| 4Pc-04 | [08:40–10:46] | Volume bars "have to be colored based on the close ... and open of um the candles"; "almost trade exclusively on ... volume bars without Candlestick charts ... at all they're that they're that ... significant". | `candidate` | Strong claim: colored volume profile is nearly sufficient without candles. Testable at the daily level as volume-colored-bar features vs price features; the detector could run on volume bars alone as a falsification test. |
| 4Pc-05 | [13:20–13:55] | Declining-volume rally prediction: "predict that the buying volume would be ... very low and that we would end up at ... best double topping at the high of day"; "would not be buying dips or pullbacks in ... this area here thinking it's going to ... move higher". | `candidate` | Volume-profile-based veto: declining buy-volume + heavy red volume → no dip-buying, expect double top. Mirror of ul3-11/HYo-05. |
| 4Pc-06 | [14:06–14:25] | "I should be a buyer near the ... support of the N9 moving average right ... here the volume profile tells me there's ... an imbalance to the buy side"; "stop at the low of this candle ... and I can add as the price ... moves higher". | `candidate` | 9MA-support entry + candle-low stop + pyramid-on-strength; same family as ul3-10 and I-C-01/I-C-02. |
| 4Pc-07 | [15:51–16:57] | "I focus on trading ... when the macd is above the signal line"; "when the macd is open that greatly ... reduced the number of false breakouts I ... had"; "macd is positive above the signal line ... if it's negative I'm not ... interested". | `candidate` | **MACD-open gate restated** — direct cross-video consistency with J-B-01 (same crossover form, not the line<0 form of J-B-02). Note the drift: ul34 (2023-11) teaches no MACD at all; this (2024-05) makes it a gate — matches J-E-02's 2022 self-dated adoption story. J-B-04's boundary condition still applies. |
| 4Pc-08 | [04:04–04:23], [37:12–37:18] | "$12.6 million of ... real money third party audited broker ... statements you can see it on my website"; "being right only ... 68.6% of the time"; "accuracy is about 68% and that's ... produced 12.6 million in gross profit". | `red flag` | Same ~68–70% long-run accuracy figure as I-A-04; the number is only meaningful with the window and trade log. "Audited" claim never shown. |
| 4Pc-09 | [19:41–19:52] | "things that I was familiar with I was ... not trading things that were actually ... volatile or worthy of my attention on ... that particular day". | `partial` | "Obvious" = volatile/RV leaders, not familiar names. The actionable leg (trade the RV leader) is 4Pc-10; the familiarity leg is not measurable without a familiarity metric. |
| 4Pc-10 | [22:12–23:17] | "my metrics is that I make the most money ... when the relative volume is five times ... higher than its average ... actually back this up with um with this ... $12.6 million in in profit"; "over $10 million of my profit ... came from stocks that had at least five"; "these are losses ... when I'm trading stocks that have lower ... relative volume". | `red flag` | Performance attribution to RV ≥ 5x vs 50-day avg, incl. a claimed loss-concentration below it. Testable leg (forward returns by RV band) overlaps I-D-04; the P&L attribution itself is unverifiable self-report. |
| 4Pc-11 | [27:06–28:18] | "we had high relative volume it was also ... when the ... instrument was up ... more than 10%", gap "being more than 2%"; "predominantly my profit is under $20 ... between 2 and 20 that's really my window". | `red flag` / `candidate` | Metrics-derived parameter set (+10% day, gap >2%, $2–20). **Third price-band variant in the corpus** ($2–5 → $2–10 → $2–20; HYo-03 says $1–20). I-D-01 measured both $2–5 and $2–10 as EDGE; $2–20 and the +10%/+2% gates are unregistered extensions. |
| 4Pc-11 | [32:09–32:28] | Worked entry: "you've got one two 3 four candles moving ... up we've got high volume green candles ... light volume pullback right here we dip ... back down the first candle makes the new ... high and for me that's the moment where ... I'm a buyer". | `candidate` | Entry = first candle to a new high after the light-volume pullback — third repetition of the trigger; cross-ref I-B-02, J-B-03. |
| 4Pc-12 | [33:50–35:01] | "what I begin to look for is ... the first candle to make a new high ... that breaks the high ... of the previous candle that's where I'm ... getting in"; veto: "if it keeps making new lows I'm not ... going to buy I'm not just going to get ... in down here I'm going to wait for the ... first candle to make a new high". | `candidate` | General statement of the same rule + the new-lows veto. The one stated entry rule of the whole video. |
| 4Pc-13 | [36:29–37:08] | "the low you bail out at the low"; "that's 10 ... cents a share now if I can make 20 cents ... a share on this position I'm going to ... have a 2:1 profit to loss ratio"; "you're right even just 33% of the time ... you're break even". | `candidate` | Stop at the low; 2:1 R:R. Arithmetic check: with 2:1, break-even win rate = 1/(1+2) = 33.3% — internally correct. |
| 4Pc-14 | [39:44–40:27] | Hotkey fix: "script on it to only sell half my ... position" (full-sell button re-scripted to half-sell to fight the bail-out instinct); "and after I've sold half I adjust my ... stop to break even on the rest of the ... position". | `process guidance` | Behavior-crutch + trail-to-breakeven; same scale-out family as I-C-02. |
| 4Pc-15 | [40:39–41:14] | "indicator is the first candle that makes a new low so if you've been holding this ... whole way up and you and you didn't sell ... any of it then as soon as you have a ... candle making new low that is an exit ... indicator". | `candidate` | Exit = first candle making a new low — the exit mirror of 4Pc-12's entry; same family as I-C-01/HYo-11. Daily adaptation is testable and untested. |
| 4Pc-16 | [42:17–43:46] | Post-entry checklist: "at least 10 cents within one minute of ... entering the trade" + "be in other words green on the tape"; inverted into exits: "if I got in right here and the price ... doesn't go up 10 cents in a minute I'm ... going to get out". | `candidate` | No-move-within-N-bars exit with a numeric threshold (+10¢/1 min) — the quantified form of I-C-04 ("price stays flat I get out"). Intraday-only. |

## Internal-consistency findings across the three videos

1. **"The one" pattern:** HYo (2024-04) crowns the **micro pullback / bull flag** as "the only one you'll ever need"; ul34 (2023-11) elevates **three** patterns equally (bull flag, flat top breakout, ABCD); 4Pc (2024-05) crowns no pattern but treats the first-new-high trigger as the universal entry. Bull flag is the constant; ABCD and flat-top get demoted/dropped in the later videos.
2. **ABCD flip:** ul34 "I really like that one" vs HYo "not my favorite ... it fails on the first attempt" — direct contradiction, 5 months apart.
3. **Retrace threshold drift:** 50% consistent (ul3-05, HYo-06), but HYo adds a softer 75% preference and a top-25% preference in the same breath — three thresholds, one video.
4. **Pullback-candle-count drift:** ul34 tolerates 1–3 pullback candles; HYo says "it's okay if there's two", 3–4 is degrading.
5. **Price-band drift:** $2–20 (4Pc-11) vs $1–20 (HYo-03) vs the corpus's earlier $2–5 / $2–10 (I-D-01, both measured EDGE).
6. **Volume-profile rule is the invariant:** high-vol green / light-vol red on pullbacks appears near-verbatim in all three videos (ul3-11, HYo-05, 4Pc-04/06) — the strongest cross-video consistency signal, and the cheapest candidate to pre-register on daily bars.
7. **MACD appears only in 4Pc** (2024-05) as a hard gate — consistent with J-E-02's self-dated 2022 adoption story and absent from ul34 five months earlier; the gate form matches J-B-01 (crossover), not the implemented J-B-02 (line<0).
8. **Naming stability:** "dogee" (misspelled identically in all three), shooting star, hammer definitions are consistent across all three; only the micro-pullback/bull-flag naming is timeframe-conditional (HYo-04).

### afNhgCc-LCw — Short Squeeze / Parabolic Momentum (2021-11-02)

Topics: `short-squeeze` `parabolic-momentum` `stock-selection` `float` `sympathy-momentum` `halts` `vwap` `scaling`

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| afN-01 | [02:31–02:34] | "if you noticed i'm up a little over 80 … 000 today" — day's P&L shown as frame for the lesson. | `red flag` | Self-reported single-day figure; the standard disclaimer follows at [02:39–02:53]. Same posture as I-A rows. |
| afN-02 | [12:23–12:26] | "i now find that they are actually the … stocks i make the most money on" (parabolic stocks). | `red flag` | Self-reported selection of his own most-profitable stock type; no log. |
| afN-03 | [08:55–09:01] | "i'm going to … be much more likely to take an abcd … setup on this stock than on one that's … not intraday parabolic" — stock type conditions entry quality. | `candidate` | Conditioning claim (stock-type as a filter on setup quality). Family of ultimate-guide B-06; testable intraday. |
| afN-04 | [09:08–09:10] | "it's a setup that we would … only trade on a stock that's been halted" (dip-and-rip). | `out of scope` | Requires halt-event data the repo's daily/intraday bars don't carry. |
| afN-05 | [13:12–13:18] | "recent reverse splits recent ipos … and spax are … some of the more common stocks that can … become parabolic". | `candidate` | Stock-type → parabolic-frequency claim; daily bars can test which listing/split cohorts produce >100% days. |
| afN-06 | [15:17–15:24] | "when you have one stock that's going … crazy you might have two three four … others that start kind of moving because … they're in the same sector" (sympathy momentum). | `candidate` | Notes: "when the main stock rolls the sympathy rolls even harder … that's almost always the case" [19:09–19:14] — a directional add-on (sympathy falls harder than leader), separately testable on daily bars. |
| afN-07 | [19:41–19:44] | "i've seen stocks go up as much as four … thousand percent in one day and that's … been with no news". | `out of scope` | No-news squeeze mechanics lean on short-interest/borrow data the repo lacks; companion claim — "when a stock has no news it's got a … little bit more risk of getting halted" [21:20–21:26] — needs halt data. |
| afN-08 | [22:34–22:40] | "you'll notice this pattern that this is … much more common for stocks listed with … the new york stock exchange then listed … with nasdaq" (no-news halts). | `out of scope` | Concrete and checkable, but only with a halt database. |
| afN-09 | [18:13–18:24] | Reverse-split float mechanics: "float a history of reducing float … reducing float reducing float often … followed by secondary offerings selling … more shares on the market increases … float and we see this cycle again and … again". | `out of scope` | Float/share-count series not in the repo's data; mechanics education, no trade rule. |
| afN-10 | [26:02–26:06] | "some pullback patterns along the … support of the nine moving average and … then it rallies back up". | `candidate` | 9-MA pullback-support claim on parabolic stocks; intraday testable; same indicator as dkO-18. |
| afN-11 | [42:17–42:28] | "trading stocks you know … three four dollars a share these ones … anywhere from you know two to twenty … seems to be the sweet spot for the type … of stock that can really make a big move". | `candidate` | Price-band criterion with numbers; same 2–20 band repeated in dkO-12; daily-testable. |
| afN-12 | [47:22–47:32] | "sls a quick trade on that for the break … of five it's a whole dollar half dollar … setup it's up 35 percent yeah take the … trade into the halt nothing huge on that … problem is it was too close to the haul … level". | `candidate` | Entry = whole/half-dollar level break, traded into the halt; explicit veto: too close to halt level. Level-break leg intraday-testable. |
| afN-13 | [48:38–48:40] | "so i take the profit as it breaks … through the critical level of 100" (round-number profit-taking); also "up to 540 and i'm taking … profit into that level because i know … it's extended" [53:00–53:03]. | `candidate` | Exit rule: profit into round-number/psychological and extended levels; intraday-testable. |
| afN-14 | [55:33–56:04] | "i put in order to take half off the … table 768 … and then i'm very likely to add back i'm … which would be a break back over 750". | `candidate` | Scale-half at target, re-add on reclaim of the broken level; live RHE example. Family of C-04 asymmetry and the scaling claims in dkO. |
| afN-15 | [56:55–56:57] | "it's bullish that it's showing an open … that's higher than the halt down" (halt resumption signal). | `out of scope` | Operational but requires halt/resumption data; daily bars can't express it. |
| afN-16 | [57:43–57:49] | "because we have had … multiple halts and because it's up as … much as it is … the risk would have been too high for an … entry" (skipping a dip-buy). | `candidate` | Extension veto: "is that it's up 170 percent" [57:06–57:10] + halt count disqualify an otherwise-valid dip. Intraday parameterizable. |
| afN-17 | [1:04:50–1:04:52] | "it is top heavy and we start to get … those false breaks as it gets a little … top heavy". | `candidate` | False-break frequency rises with extension — same structural claim as J-B-03's late-move false breakouts; testable intraday. |
| afN-18 | [1:10:53–1:11:05] | "accumulating here my mental stop was the … low of this pullback … but really it was about at the volume … weight average price which is the orange … dotted line … so stop at the v app in this case not a … live stop order just a mental stop". | `candidate` | Full entry anatomy (pre-market pivots 8.40/8.70, targets "looking for a breakthrough 840 and then … 870" [1:11:19–1:11:23]); VWAP stop is computable intraday. |
| afN-19 | [1:12:22–1:12:31] | "the actual entry first pullback … second pullback abcd half dollar whole … dollar micro pullback buying a break of … the high a day v breakout buying into or … out of a hall dip buy that's the … strategy of where i'm actually buying". | `candidate` | The full entry taxonomy in one place; stock-type criteria stated just before ("a certain type of float at a certain type of price … with some type of news" [1:12:14–1:12:20]). Cross-course consistency with I-B-01, B-01, B-03, J-B-03. |
| afN-20 | [1:13:28–1:13:30] | "don't use stop orders i don't use live … stock orders i have mental stops"; exits at the bid — "have to cut my loss i'm usually selling … at the bid price" [1:13:52–1:13:56]. | `process guidance` | Execution mechanics; the no-live-stop practice is a measurable risk-process divergence, not a market claim. |
| afN-21 | [1:28:59–1:29:07] | "selling half is one way that i uh … pay myself and then hold the rest for a … little bit of a bigger trade … and when the market is really hot i will … get more aggressive holding longer". | `partial` | Regime-conditional holding (hot market → hold longer); "hot" undefined — pre-register an operational proxy before any test. |
| afN-22 | [24:20–24:31] | "through 2020 2021 the frequency of … parabolic momentum stocks reached an … unprecedented level as overall trading … volumes increased and more traders have … been joining the markets i currently … expect this trend to continue". | `candidate` | Frequency claim about the market itself — countable with daily bars (multi-bagger days per year); testable trend/regime claim. |

### dkOyu_kLKjE — Day Trading Strategies for Beginners (2023-04-18)

Topics: `momentum-trading` `scanner-criteria` `relative-volume` `pullback-entry` `nine-ema` `exits` `risk-process` `backtesting`

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| dkO-01 | [01:50–01:52] | "of this uh class. I'm finishing the … morning up $4,480 and 9 cents". | `red flag` | Same-day P&L as the class frame; disclaimer at [01:59–02:11]. |
| dkO-02 | [04:11–04:19] | "I can see my average … winners, my average losers. I can see my … average percentage of success, 68.9% … right now." | `red flag` | Self-reported accuracy; notably consistent with the ~68–70% long-run figure of I-A-04. |
| dkO-03 | [05:48–05:54] | "You would need to be right 66% of … the time just to break even with that … kind of ratio." (1:2 losers) | `process guidance` | Arithmetic checks out; extends: "needs to be right 33% of the time in … order to break even" (2:1) and "closer to 60% in order to be profitable" (1:1) [06:14–06:29]. |
| dkO-04 | [07:33–08:15] | "out of the last six weeks, how many … weeks have you been green?" and "I would say you need to focus on … accuracy first." | `process guidance` | Consistency metric + fix-accuracy-first doctrine; self-fulfilling as stated (I-G family). |
| dkO-05 | [16:16–16:21] | "I turned less than $600 into over $10 … million day trading and that was with … real money." | `red flag` | The corpus's biggest cumulative claim; same trajectory family as A-01/I-A-01, now escalated to $10M. "Audit of my broker statements" asserted at [16:55–17:06], never shown. |
| dkO-06 | [30:37–31:01] | "everyone is posting their P&Ls on … YouTube, on Twitter, and most of them … are only posting when they're green. … people put out a much rosier picture of … themselves than is true." | `process guidance` | Survivorship/selection meta-claim about the social-media P&L environment — the exact bias the repo's red-flag rubric exists for; also a caveat on this corpus itself. |
| dkO-07 | [34:07–34:28] | "10, 15 cents a day, let's do the math … Let's say 15 cents per day. … And the goal is to eventually do that … with 1,000 shares, which equals $150 per … day." | `process guidance` | The class's central parameter (15c/share/day). Same per-share-arithmetic framing as I-A-06's model. |
| dkO-08 | [40:48–41:05] | "A strategy should be back tested with … historical data to prove profitability. … mine, you have to prove in a sim that … you can trade it profitably." | `process guidance` | Aligns with the repo's pre-registration discipline; note his own claims in this video are asserted, not back-tested (see dkO-10). |
| dkO-09 | [45:25–45:35] | "having above average volume, at least … five times higher than average, and … having a stock already up at least 10% … are pretty much minimum requirements for … me to be willing to trade a stock." | `candidate` | The two-filter scanner minimum (RVOL ≥ 5, +10%); same family as the §E two-filter veto and §D scanner criteria; daily-testable. |
| dkO-10 | [45:43–45:50] | "This is based on historical data. Right … here, this is all the historical data … that supports what I'm sharing with you … right now." — the "data" shown is his own performance charts. | `red flag` | Evidence claim: self-reported per-bucket P&L presented as the historical validation of the criteria. Observational, survivor-shaped, not causal (§breakoutBot discipline). |
| dkO-11 | [46:06–46:12] | "I make … more money on stocks that have more than … 25 million shares of volume." (profit-by-RVOL and %-gainer buckets shown as the proof). | `red flag` | Self-reported bucket P&L; encodes the D criteria but the profitability attribution is unverifiable. |
| dkO-12 | [46:50–47:27] | "This is where I make the most money, … right? So between two and 20." — buckets: "it's 12% … up to 50. Above 50, you know, 5%"; beginner guidance "focusing … between two and 20, two and 10, maybe … two and 12 is going to be a little bit … better." | `red flag` | Self-reported price-band profitability; the 2–20 band itself is daily-testable and matches afN-11 (three sub-bands given here). |
| dkO-13 | [48:41–48:51] | "so there's a certain number of shares … available to trade. And when that number … of shares is limited, then the the price … moves up very quickly as traders are … clamoring to get a piece of the action." | `out of scope` | Float/supply mechanics ("the float is fixed" [48:37]); no float series in the repo's data. |
| dkO-14 | [49:38–49:46] | "every single one of these stocks … are up more than 20% today. … These are naturally the type of stocks … that I would want to be looking at." | `partial` | Top-gainers watchlist selection. Directly touched by D-03 (rank-1 "obvious" gainer measured → NO EDGE on daily bars, §D.5); his own hedge follows: "they're not all going to hold up all day long" [49:48–49:49]. |
| dkO-15 | [50:46–51:00] | GFAI checklist: "The relative volume right here is 7.18. … check, it's up more than 10%. … Check, it's got relative volume of more … than five. … is yes. What's the price? Is it between … two and 20? Yes, the price is 12.70." | `candidate` | The scanner criteria applied live (adds news + float 1.28M vs 24M volume traded); the concrete instantiation of dkO-09 — pre-register as the two-filter pass-set definition. |
| dkO-16 | [53:01–53:32] | "typical pullback uh will usually have … two to three red candles. … focus on the first and the second … pullbacks." — and "the success rate on third pullbacks … is not as strong as first and second." [1:00:52–1:00:54]. | `candidate` | The pullback-count rule, now with an explicit success-rate claim. Triple-anchored across courses: I-B-01 (2015), B-03 (ultimate guide), J-B-03 (MACD video) — the corpus's most stable structural rule; intraday-testable. |
| dkO-17 | [53:47–53:58] | "I enter during the pullback, either as … close to the moving averages as … possible, that would be buying the dip … in a way, with a stop at the low. … Or I can buy as soon as the first candle … makes a new high" (stop at the low of the pullback). | `candidate` | The two canonical entries; the new-high form is B-01's micro pullback. Stop at the *pullback* low — consistent with ultimate-guide B-01. |
| dkO-18 | [54:44–54:49] | "that stocks will usually … pull back to around the nine moving … average before rallying back up." | `candidate` | 9 EMA as the pullback magnet; parameter given (9-period EMA). Same indicator as afN-10; complements D-05's indicator stack and J-E-01's coordination mechanism. |
| dkO-19 | [55:55–56:32] | Conservative entry: "buy … the second this candle breaks the high … of the last candle. … And more often … than not, this pattern resolves to the … upside, which is why I like it so much." | `candidate` | Break-of-previous-candle-high entry plus a directional win-rate claim (>50% resolution). Both intraday-testable. |
| dkO-20 | [55:26–55:31] | R:R example: "at nine with a stop at 9.80. … profit target of 9.40, 9.50." | `candidate` | **Transcription garble**: the stop must be *below* the 9.00 entry (whiteboard context says ~8.80); quote preserved as captioned. The 2:1-minimum structure is the testable R:R discipline of B-01. |
| dkO-21 | [58:25–58:33] | "it goes, it doesn't matter. I don't even … feel FOMO cuz it never gave me a good … I can only trade it if it gives me a … good entry." (no pullback → no trade, however far it runs). | `candidate` | Selection veto: the strategy only trades pullback-given entries — an explicit no-FOMO filter. |
| dkO-22 | [1:01:47–1:01:55] | "I want to take profit at or before the … first signs of weakness if I'm focusing … on this 15 cent per day goal."; weakness list includes "entering on a red candle. So, if the … candle turns red while I'm in the trade, … that indicates weakness." [1:04:17–1:04:20]. | `candidate` | Exit rule (profit at first sign of weakness); the red-candle leg is intraday-testable, the level-2 legs are not (see dkO-23). |
| dkO-23 | [1:01:59–1:02:56] | "to see strength. What does strength look … like? Green on the tape." and "As soon as I can set my stop to break … even, I'm in the driver's seat." | `out of scope` | Tape/level-2 components can't be measured (same data hole as C-02/C-05); the break-even-stop move-over is process, not a bars claim. |
| dkO-24 | [1:08:13–1:08:17] | "There are still only going to be maybe … 10% traders out there that find success." | `out of scope` | Population claim about trader survival — checkable only against external retail-trader studies. |

### Notes (afNhgCc-LCw, dkOyu_kLKjE)

## Notable findings

1. dkO-05 escalates the flagship performance claim to "$10 million" (vs $1M in the 2015 corpus, A-01's $583 trajectory) — flag for the §A escalation tracker.
2. dkO-10 is the corpus's most explicit "my own P&L is the historical evidence" move — the cleanest observational-not-causal teaching example in the file set.
3. The 2–20 price band (afN-11/dkO-12) and first/second-pullback rule (dkO-16) are the strongest cross-course consistency candidates.
4. The short-squeeze video yields mostly halt/float-dependent operational criteria (afN-04, afN-08, afN-15) that are unmeasurable without halt and float data, as anticipated.

### GMRmMf-RsfE — $600 small-account challenge (2024) (2024-03-19)

Topics: `small-account-challenge` · `performance-claims` · `stock-selection-criteria` · `momentum-continuation` · `leverage-pdt-workaround` · `trade-frequency` · `revenge-trading`

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| GMR-01 | [00:02–00:15], [36:08–36:14] | "in just 20 individual days I grew the account by over $166,000 of profit 16 times return on my initial deposit" … "I was up about 21,000 on the month and then you know had to settle for being up uh 16,000" | `red flag` | Title says $600 → $16,013.06. **Arithmetic contradictions**: (a) "$166,000" is 10× the title figure (almost certainly a caption of "$16,000", but as-written contradicts the title and the [36:08] "16,000"); (b) "16 times return" on a $600 deposit = $9,600, not $16,013 (that is 26.7×). Same-window figures vary — the I-A-03 pattern. |
| GMR-02 | [28:50–29:04], [29:19–29:28], [01:09], [41:09] | "day one I locked up $125 of profit which was solid now on day two I came in and locked up $187 of profit" … "my account is up $… 6846 this first week" | `red flag` | **Internal inconsistency**: [01:09] "$25.70 that's day one" vs $125 elsewhere; [41:09] "day two 1887 it was good" vs $187 at [29:00]; stated dailies (125+187+150+150 = $612) don't sum to the "6846" first-week figure. |
| GMR-03 | [29:35–29:46] | "do you think you'd be able to turn an account from $500 into a million again and the answer is absolutely" | `red flag` | Re-asserts the §I-A trajectory claim as repeatable; see I-A-06 and GMR-01 for the current challenge's actual (claimed) endpoint. |
| GMR-04 | [43:08–43:13] | "reflect accuracy of about it was over 80% they reflect a terrific profit loss ratio" | `red flag` | Accuracy-window pattern again: I-A-04 chain 100→87→75→68–70→67%; j1t-03 "right around 70 percent"; U0f-03 81–82%. No avg-win/avg-loss given here. |
| GMR-05 | [26:31–26:45] | "a 1,000 share position of this at $4.80 could have yielded $11,000 a profit on a position that was only $4,800 that's a 20% return" | `red flag` | **Arithmetic error**: 20% of $4,800 = $960; $11,000 on $4,800 = 229%. Likely caption of "$1,100" — but he then says "I made about $2,000 on this trade" ([26:45]), matching neither. |
| GMR-06 | [21:09–21:21], [10:18–10:29], [12:55–13:14], [14:55–15:00], [18:15–18:40] | "it's got to be up 10% have high relative volume have news be obvious have a float of under 10 million shares and be priced under 20" | `candidate` | Full scanner screen (D): up ≥10%, high RVOL, news catalyst, "obvious", float <10M, price <$20; week 1 tightened to <$10 / focus <$5. Note: "obvious" glossed both as "top three uh percent gainers" [14:55] and "top three positions" [20:58] — operationalize one. |
| GMR-07 | [10:31–10:40] | "once a stock is up 10% it has a much higher likelihood of going up to 20% and doubling its gain on the day then a stock that is at zero going to 10" | `candidate` | Intraday momentum-continuation claim; testable as conditional P(double-from-10%) vs P(0→10%). Distinct from I-B-07's day-2 continuation question. |
| GMR-08 | [13:17–13:25] | "it's a lot easier for a stock to go from $1 to $2 and be up 100% then it is for a stock to go from 20 to4" | `candidate` | Low-price percentage-move claim ("20 to4" = caption of "20 to 40"). Testable as price-bucket move distributions. |
| GMR-09 | [27:14–27:24] | "pullbacks that occur on this type of stock that meets these criteria my metrics have shown me that statistically they resolve in my favor" | `candidate` | Unquantified statistical claim (B). Needs the GMR-06 screen as population. |
| GMR-10 | [23:54–24:02], [24:20–24:24] | "if a stock is below it it's almost always going to have resistance at it" … "I would never buy a stock right under the 200" | `candidate` | 200-DMA daily-resistance veto (B/E). Testable on daily bars. |
| GMR-11 | [28:25–28:31], [28:39–28:44] | "what's better the perfect pattern or the perfect stock always going to be the perfect stock" … "the qualifier of whether or not to take a trade is the quality of the stock not the pattern" | `candidate` | Stock-quality-over-pattern claim (D) — testable by conditioning pattern quality within the screen. |
| GMR-12 | [30:37–30:45], [31:13–31:26] | "for my small account challenges I use international Brokers because they do not enforce the $25,000 PDT rule" … "I fund the account with well $600 just for instance and I get uh six times leverage" | `candidate` | PDT-mechanics (F). 600×6 = $3,600 checks; note 6× offshore exceeds the 4× US intraday max claimed in PtF-05/U0f-10. Cross-ref PtF-06, U0f-02. |
| GMR-13 | [34:13–34:19] | "my hot days are clustered together usually my big green days are are sort of all together" | `candidate` | Serial-dependence claim about his own P&L; mirror of I-G-03 ("big red days follow big green days"). Only testable against a trade log. |
| GMR-14 | [46:21–46:31] | "of profit to loss ratio they should at the very least be even and that way as long as I'm right 50% of time I break even" | `candidate` | Arithmetic correct (1:1 ratio → 50% breakeven). Direct complement to U0f-04's 2:1 → 33%; the two videos' stated P/L parameters differ. |
| GMR-15 | [43:39–43:53], [33:41–33:56] | "basically putting your whole account into one trade" … "I could lose 20% of the account in one day or conversely I could make grow the account by 20% in one day" | `process guidance` | Risk-sizing: full-account position, ±20% daily swing tolerance. **Contradicts PtF-11** ("the best I can do is to grow the account 10% in one day"). |
| GMR-16 | [39:48–39:57], [14:26–14:34] | "take only two trades most of those days and then walk away" … "number one I tell myself breakout or bailout" | `process guidance` | Two-trade/day discipline + stop rule. Cross-ref J-G-01 — he cites the same Annie Duke book at [38:56–40:02]. |

**§I-A comparison:** the 2024 challenge is the same template as 2017–19 — tiny deposit, offshore no-PDT broker, ~2 trades/day, month-one retrospective — but with **new, smaller figures** ($600 → $16,013 vs $583 → $100K in 44 days) and a *higher* claimed accuracy (>80% vs 75%). The escalation now lives in rhetoric rather than figures: GMR-03 ("$500 into a million again — absolutely") and PtF-08's "$10 million in profit". As in §I-A, no two retellings of the same period agree.

### j1tvgmKG9Vw — "I Wish I Knew This BEFORE I Started" (2019) (2019-11-30)

Topics: `performance-claims` · `accuracy-claims` · `one-strategy` · `trading-psychology` · `expectancy` · `offshore-broker` · `simulator-first` · `risk-guardrails`

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| j1t-01 | [00:46–01:00] | "when I started over in 2017 with 583 dollars in my account I set out to prove that you can become a millionaire with one strategy" | `red flag` | Same trajectory as I-A-01/A-01; "just over two years" to $1M here vs I-A-06's 553 days — consistent. |
| j1t-02 | [10:21–10:36], [10:43–10:48] | "I turned that 583 dollars into a million dollars and then had all of those broker statements audited by an independent auditor" … "a hundred and eighty three thousand percent return" | `red flag` | The A-02 "audited" rhetoric in 2019 form (Citrin Cooperman, named at [10:34]). Arithmetic *does* check: 183,000% on $583 = ×1,831 ≈ $1.067M ≈ "over a million". |
| j1t-03 | [01:56–02:00] | "my accuracy is right around 70 percent so in out of 100 trades I'll have 70 winners" | `red flag` | Fits I-A-04's accuracy-window chain (68–70% long-run 2015 → 70% here → 81–82% in U0f's 3-day window → >80% in GMR-04). |
| j1t-04 | [05:45–05:53], [15:22–15:27] | "I'm finished in the morning up two thousand four hundred seven dollars trading a stock that's currently up over a hundred and eighty percent" | `red flag` | Self-reported single-day anecdotes ($2,407; also "another day $708 before 8 a.m."); same posture as J-A-01. |
| j1t-05 | [05:40–05:43], [11:42–11:49] | "hard stop today is at 10:30 so I've got one hour to trade" … "it's 10:30 finished my one hour of trading may hit a thousand bucks and that's it done for the day" | `candidate` | Trading-window rule (F): 9:30–10:30 only. Matches I-B-05's fourth window and U0f-05; consistent across 2019–2020, while GMR (2024) states no window at all. |
| j1t-06 | [11:51–11:55] | "the more times you trade every single day the more you risk giving back profit" | `process guidance` | Trade-frequency discipline; operationalized as the 1–2 trades/day rule. |
| j1t-07 | [24:48–25:16], [25:56–25:59], [26:11–26:19] | "I ended up making $40,000 and I was thrilled I mean I was like $40,000 in August $42,000 this is incredible" … "in five days I made 45,000" … "finished in the month down $20,000" | `red flag` | **Internal contradiction**: $40,000 vs $42,000 for the same August in consecutive sentences. October: +$45K in 5 days → month −$20K. |
| j1t-08 | [35:27–35:37] | "if I only traded the small cap stocks moving up more than 30 percent guess what I would have been profitable over those last 18 months" | `candidate` | The origin criterion: small-caps up >30%. **Parameter drift**: the same strategy is "up at least 10%" by 2024 (GMR-06) — a 3× loosening; test both thresholds. |
| j1t-09 | [19:27–19:35] | "anywhere from a hundred shares to eight or 10,000 you're gonna be a pretty linear" | `candidate` | Share-size linearity/diminishing-returns claim (F/G) — same claim as U0f-08, stated a year earlier. |
| j1t-10 | [33:07–33:17] | "it's to call your broker and set up a max loss on your account so if you're down more than a certain amount on any given day you're done" | `process guidance` | Broker-enforced max daily loss + max share size ([33:17–33:25]). Precursor of 2025-course G-05 guard rails. |
| j1t-11 | [12:17–12:24] | "the importance of trading in a simulator before trading with real money" | `process guidance` | Simulator-first; matches G-07 and U0f-10's month-minimum. |
| j1t-12 | [27:54–28:03] | "I shouldn't look at my P&L every single day" | `process guidance` | Stop-tracking-daily-balance rule; pairs with the meditation routine at [31:10–31:13]. |

### PtFKChlL7wE — "How Much Money Do You REALLY Need" (2024) (2024-07-31)

Topics: `pdt-rule` · `offshore-brokers` · `leverage` · `settlement` · `performance-claims` · `short-selling-risk` · `account-sizing` · `process`

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| PtF-01 | [02:22–02:37], [03:36–03:50] | "the PDT rule requires active day traders to maintain a minimum balance in their account of $225,000" … "if you take three or more roundtrip trades in a five day period" | `candidate` | PDT mechanics (F). "$225,000" is a caption error for $25,000 (repeated at [23:37]); the restatement gives the standard 3 round-trips/5-business-days + 90-day lockout. "Enacted on February 27th 2001" [01:16–01:18] is externally checkable. Same date claim in U0f [11:54–12:14]. |
| PtF-02 | [02:37–02:42] | "this is not really uh about protecting the individual Trader it's about protecting the broker" | `candidate` | Claim about the rule's *purpose* — checkable against FINRA/NYSE rule text and rationale, not market data. |
| PtF-03 | [05:04–05:11] | "the pattern day trader rule the PDT rule only applies to margin accounts" | `candidate` | Correct mechanics; foundational for his cash-account recommendation (PtF-13). |
| PtF-04 | [19:17–19:27] | "then it changed to two days and just this year it changed to one day which means settlement is now overnight" | `candidate` | Settlement-cycle claim — **externally verifiable and correct** (T+1 effective May 28, 2024). Drives his "$2,500 cash account, one full-balance trade/day" recommendation. |
| PtF-05 | [17:01–17:11], [17:24–17:34] | "today when you fund an account with $25,000 you get four times leverage" … "you can only use two times leverage for overnight holds and you can use four times for day trading" | `candidate` | Reg-T margin mechanics — correct and checkable. Baseline against which GMR-12's 6× offshore figure is measured. |
| PtF-06 | [23:26–23:30], [23:40–23:43], [26:32–26:37] | "as it turns out the PDT rule is enforced by all us broker dealers" … "International Brokers are not required to enforce it" … "they therefore do not enforce the PDT rule but they accept a US resident" | `candidate` | Core market-structure claim underlying all three challenge videos (cross-ref GMR-12, U0f-02). The "non-US broker accepts US residents" leg is the load-bearing one for his $583/$500 challenges. |
| PtF-07 | [32:29–33:23], [32:23–32:26] | "7 years of audited trading results from January 1st uh 2017 through December of 2023" … "January I made $116,000 I made $116,000 in February I made 60 Grand" … "I had 119 trades and the total gain through March first was $76,000" | `red flag` | **Cross-video contradictions with §I-A**: day-1 "I actually made $156" vs I-A-03's day-1 +$124; $76,000 through Mar 1 vs I-A-02's $101,280.47 by Mar 8. In-video: caption "$116,000" for January is contradicted seconds later — "60,000 from um February plus 16,000 from January so about 76,000" ([33:20]) — so January was $16,000. 119 trades over 2 months ≈ 2/day. |
| PtF-08 | [34:32–34:36] | "this account has now grown to over $10 million in profit" | `red flag` | Same growing endpoint as A-01 and A-02 — endpoint keeps moving with the telling. |
| PtF-09 | [36:21–36:34] | "the previous year in 2016 I'd made almost A4 million dollars traded I was up 200 let's see it was 200 it was like $220,000 of profit in 2016" | `red flag` | **Internal contradiction in one breath**: "almost 4 million" then "$220,000" for the same year (likely caption of "$400,000", but as-written it is 18× off). |
| PtF-10 | [35:09–35:22] | "I paid a total of $4,800 in fees which you can see right here plus I paid an additional $2 2,200 in commissions so we'll just round it up to 567,000" | `red flag` | **Arithmetic**: $4,800 + $2,200 = $7,000, not "567,000" (caption garble). ~10%-of-profit fee claim on $76K profit — the fee drag on the offshore workaround is itself measurable. |
| PtF-11 | [20:18–20:28], [22:37–22:44] | "whenever I've done small account challenges I generally think the best I can do is to grow the account 10% in one day" … "if I had a $3,000 account and I had four times leverage on it then I would be focusing on 10% a day that's 300 a day" | `candidate` | Self-stated daily-growth ceiling. **Directly contradicts GMR-15** (±20%/day tolerance, same 2024 corpus) and GMR-01's 26.7× month. 10%-day is the clean pre-registerable form. |
| PtF-12 | [11:49–11:53], [11:37–11:41], [12:12–12:14], [12:18–12:24] | "5,000 share position could have produced a loss of $12.5 million" … "this stock went from $3 a share to $2,500 a share" … "a stock that went from $20 a share to 2500" … "Melvin Capital losing 6.8 billion on a position to the short side" | `candidate` | Short-selling unlimited-loss warning (E/G). $3→$2,500 × 5,000 sh ≈ $12.5M checks; but the same example is "$3 a share" at [11:37] and "$20 a share" at [12:14]. Melvin's $6.8B externally checkable. |
| PtF-13 | [48:52–48:55], [40:58–41:05], [42:01–42:08] | "I think a starting amount in the $2,500 range is more reasonable" … "is to trade with between uh like one and 10 shares" … "you need 100 trades of data to kind of understand what's my accuracy" | `process guidance` | The 2024 answer to the video's title question: $2,500 cash account, 1–10 shares, build a 100-trade track record before size. Note the reversal from U0f-10c ("$500 proven"). |
| PtF-14 | [44:07–44:11] | "we don't track the typical result of every Trader who takes our classes" | `out of scope` | Marketing disclosure, not a market claim — but a notable admission sitting directly beside the "proven strategy" pitch ([43:47–44:02]). |
| PtF-15 | [53:32–53:39] | "an incentive in the market from like the very top to encourage the people down at the bottom to be trading sometimes recklessly with more money than they should" | `candidate` | Market-structure claim (payment-for-order-flow / leverage economics); only weakly measurable. |

### U0fmwn7742A — "How to Start Day Trading for Beginners" LIVE (2020) (2020-04-05)

Topics: `small-account-challenge` · `performance-claims` · `profit-loss-ratio` · `trading-window` · `stock-selection` · `scalability` · `pdt-rule` · `share-size-scaling`

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| U0f-01 | [13:33–14:06] | "I funded an account with $500." … "during this challenge, I traded three times every day. Three trades per day" … "And by the end of the month, my account had grown to $53,000." | `red flag` | **New §I-A-class trajectory**: $500 → $53,000 (≈106×) in ~1 month, Dec 2019. Escalates the pattern: I-A-02's $583→$100K took 44 days; this claims ~$53K in ~21 trading days. Broker named: "the offshore broker um that I used in December is called uh CMEG" [15:33–15:38]. |
| U0f-02 | [14:47–14:50] | "I grew my account more than five times faster by using an offshore broker" | `candidate` | Offshore-vs-cash throughput comparison (F); the "5×" is derived from the U0f-01 claim plus a $250/day cash-account counterfactual — checkable only as broker-structure arithmetic. |
| U0f-03 | [20:34–20:46], [20:56–21:01], [22:16–22:36], [23:16–23:18] | "my average winners have been a little over $200. My average losers have been about 100 and my accuracy has been uh 81%" … "I have taken about 34 trades and my net profit right now is about $5,000. And that's in just three days" … "actually $247 are my average winners, $104 my average loser" … "So, that's $5,816 of profit on 32 trades so far." | `red flag` | **Internal contradiction, same screen, minutes apart**: 34 trades ≈ $5,000 vs 32 trades = $5,816; "a little over $200"/"about 100"/81% vs $247/$104/82%. Magnitude is arithmetically plausible — the discrepancy is in the stated pairs, i.e. recall, not math. |
| U0f-04 | [19:56–20:26], [21:24–21:26] | "I want to risk $1 to make $2." … "If you use a profit loss ratio of 2:1, your break even point is 33% accuracy." … "I'd have to be right closer to 60% of the time in order to break even" | `candidate` | Breakeven arithmetic — **both cases correct** (2:1→33.3%; 300-loss/200-win→60%). Cross-ref GMR-14 (1:1→50%). Note his own claimed stats (2.4:1 at 81–82%, U0f-03) sit far above the breakeven he teaches. |
| U0f-05 | [23:40–23:50], [24:15–24:24] | "the bulk of my profit is between 9:30 and 10:00 a.m." … "I trade for a really short period of time from about 9:30 to 10:30" … "This is $5,800 of uh profit in three days trading for about an hour a day" | `candidate` | Trading-window claim (F): 9:30–10:30, profit concentrated in the first 30 min. Matches I-B-05's 9:30–10:30 window and j1t-05's hard stop; the finest-grained version in the corpus. |
| U0f-06 | [39:37–40:16] | "stocks between a dollar and $20. So lower priced. Let's say number two, it's um we say trading 9:30 to 10:30 a.m. Eastern time only. And let's say number three, it's risk uh 100 to make 250" | `candidate` | The template strategy rules (B/C/D): price $1–$20, window 9:30–10:30 ET only, risk 100 to make 250 (2.5:1 — vs 2:1 in U0f-04, minor parameter drift). |
| U0f-07 | [29:16–29:20] | "stocks between uh $2 and $10 are the best for account growth" | `candidate` | **Drifts from his own rule 10 minutes earlier** ($1–$20, U0f-06) and from GMR-06's <$20 (2024). Price-band claim is bucket-testable. |
| U0f-08 | [04:34–04:46] | "as you scale up, you start to approach diminishing returns. to a certain point, it actually will start to decline. And the reason is due to liquidity in the market" | `candidate` | Scalability ceiling (F/G); same claim as j1t-09. Ladder given as 100 sh→$20, 1,000→$200, 2,000→$400, 4,000→$800 [04:02–04:21]. |
| U0f-09 | [02:10–02:21] | "the only difference between making 20 a day and making 200 a day is increasing the number of shares that you buy" | `candidate` | The linearity premise under all his scaling advice — the strong form of U0f-08; testable as per-share edge invariance across size buckets. |
| U0f-10 | [12:20–12:29], [12:41–12:44], [18:53–19:05] | "if you're going to day trade more than three times a week with any US broker on margin, you need a minimum of 25,000" … "when you have a cash account, you've got to wait two days for every trade to settle" … "I've proven through several small account challenges that even with as little as $500, you can easily um you know, set up an account" | `candidate` | PDT mechanics (F): his "more than three times a week" paraphrase is looser than PtF-01b's "three or more roundtrip trades in a five day period"; 2-day settlement correct for 2020 (T+2 → T+1 in PtF-04). |
| U0f-11 | [57:23–57:32] | "at the end of each week, you increase your share size by a small increment and just slowly increase it" | `process guidance` | Share-size ramp after sim→real transition; the 2020 ancestor of G-06's "+50 shares/10 days". |
| U0f-12 | [36:31–36:35] | "last year I made $370,000 and my day trading overhead" | `red flag` | Self-reported 2019 profit, spoken April 2020. Tension with the trajectory narrative — annual figures drift with the telling. |

### Notes (GMRmMf-RsfE, j1tvgmKG9Vw, PtFKChlL7wE, U0fmwn7742A)

## Cross-video observations for the ledger

- **The challenge figures never repeat consistently.** Day-1 of the 2017 challenge: $156 (PtF-07) vs $124 (I-A-03); Jan 2017: $16K (PtF-07, self-corrected from caption "$116,000") inside a $76K-through-Mar-1 total vs I-A-02's $101,280.47 through Mar 8. The 2024 challenge (GMR) is a *new* figure set ($600 → $16,013, >80% accuracy), not a retelling of the old ones.
- **Strategy-parameter drift is monotonic downward**: small-caps "up >30%" (j1t-08, 2019) → "$2–$10 best" (U0f-07, 2020) → "up at least 10%, under $20" (GMR-06, 2024). The selection threshold loosened 3× as the videos aged.
- **Daily-growth ceiling contradicts itself across the 2024 videos**: 10%-per-day "best I can do" (PtF-11) vs ±20%-per-day tolerance (GMR-15).
- **The audited/verified rhetoric is constant** (j1t-02 CPA audit, PtF-07 "7 years of audited trading results", A-02) while every audited figure quoted conflicts with at least one other retelling.

### KzVbXzkoZkA — Adding to Winners with Scaling (LIVE STREAM, 2023-04-04)

Topics: scaling-into-winners, averaging-up, starter-position, add-ladder, stop-to-breakeven, market-regime, stock-selection, relative-volume, self-reported-pnl

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| KzV-01 | [04:15–04:21] | Scaling thesis: "you can increase your position size … without increasing the risk you were taking on the trade." | `candidate` (structural) | The core claim of the video. Only true if the breakeven stop fills — he concedes the failure mode [06:50–07:09]: "and you got slippage … on the exit. So, you did end up taking" a loss. Relates to the paper loop's position-growth assumptions; risk-invariance is conditional, not structural. |
| KzV-02 | [06:01–06:38] | Worked-example add mechanics: "Instead of selling, they're" "adding another thousand shares." … "stop at break even. Which means now" "you're holding a two thousand share" position. | `candidate` | Most operational parameter set in the video: 1,000-share starter, stop 10¢ below ($100 risk); add equal size at +50¢; stop to breakeven; target +50¢ on 2,000 = $1,000. Needs intraday. |
| KzV-03 | [44:34–45:57] | Starter before confirmation: "If it works, I can add. If it doesn't, I cut the loss with small size and the loss is smaller." because "if I wait for confirmation," "I pay a high price for it." Starter = "1/4 or 1/5 of … whatever is your full size," | `candidate` | Anti-confirmation entry rule; ties the sizing ladder to an entry-timing claim. Cross-course tension with ultimate-guide B-02 (don't buy the breakout); here the starter IS the pre-breakout entry. |
| KzV-04 | [47:30–48:05] | No fixed add ratio: "I don't have a … sort of methodology that I use … I usually use 3,000 share … blocks. 3 3K is my sort of" block. | `process guidance` | Explicitly discretionary ("based on what I'm seeing on the price action"). Only fixed parameter offered: the 3K block. |
| KzV-05 | [48:20–48:37] | Add-distance limit: at high of day 50¢ above entry, "Probably … wouldn't do that" adding full blocks "Because the problem is that's 50 cents … away from my initial entry." — would add only a quarter position there. | `candidate` | Distance-from-cost-basis cap on adds. Inverse scaling of add size vs distance from entry — a formalizable parameter. |
| KzV-06 | [1:26:04–1:26:11] | Squeeze ladder: "What I will sometimes do on these types … of stocks is every 10 cents or so, I'll … keep adding as it's moving higher." | `candidate` | Fixed 10¢ add spacing during extension phase (OCEA archive). |
| KzV-07 | [1:19:58–1:20:21] | Exit ladder is geometric halving via hotkeys: orders "automatically calculate how many shares … So, if I press sell half and I'm … holding 10,000, I sell 5,000 shares." | `process guidance` | Sell-half/sell-half/sell-half ladder; pairs with add ladder of 6K→12K→+quarter (typical shape given at [48:43–48:57]). |
| KzV-08 | [54:40–56:36] | Keep-adding conditions: "Green on the tape. We want to see more" buying; number of shares "the level two decreasing"; "The stock should be hitting new highs and it should be on the high day scanner" — then "momentary dips to continue adding." | `partial` | Level-2/tape legs out of scope; the new-highs/high-of-day-scanner leg is bar-observable intraday. |
| KzV-09 | [53:29–53:45] | Add trigger: "as I like to see these sort of squeezes … up and then a momentary pause." — "That momentary pause can be the formation … of a micro pullback as you see right" there. | `candidate` | Micro-pullback = add trigger; same pullback family as I-B-01/J-B-03 at sub-candle resolution. |
| KzV-10 | [56:59–58:41] | When to stop adding "is going to … be very market dependent." Exit choice too: "If it's a hot market, I'm going to try … to hold it as long as I can. If we're in … a colder market, I'm going to be a bit … more conservative and take the profit … off sooner." | `candidate` | Regime-conditional hold time and add aggressiveness; regime undefined here (see Wd_-02 for his later definition). Cross-ref G-06, J-G-01. |
| KzV-11 | [58:15–58:33] | Weakness response is 3-mode: "sell the full position, … I could begin scaling out quickly, or … sell slowly and wait to … see if strength resumes. The … will be based on my cost basis, my total … profit, both realized and unrealized, … and market sentiment." | `process guidance` | Decision function over (cost basis, realized+unrealized P&L, regime) → exit mode. Not formalizable as stated. |
| KzV-12 | [27:50–30:50] | Requirements to scale: "you're seeing a stock that's only going … up, you know, 10, 15 cents, you don't … have enough room to scale in" — need "stocks squeezing up 50 … cents, a dollar a share or more"; plus volatility and "maybe perhaps another one is liquidity." | `candidate` (structural) | Testable shape: scaling benefits (size × win) concentrate on large-range/liquid days. |
| KzV-13 | [31:42–31:52] | Slippage mechanism: "scaling allows … you to move into and out of the market … with less slippage than one big block … order." | `candidate` (structural) | Market-microstructure claim; out of scope for daily bars; relevant to any large-position backtest. |
| KzV-14 | [1:04:29–1:09:08] | Selection checklist: "relative volume is a measurement of today's … volume compared to the average volume …"; "much better on stocks that have at least … two times higher volume today than … average"; "RV, needs to be at least two … or higher"; "be up at least 10% for me to even … consider it"; price "between $2 a share and kind of like $10 … a share, but up to up to 20 is okay"; float "under 50 million shares, … 50 million shares or less is fine." | `candidate` | Fully testable on daily bars (D-rubric). Note tension with Wd_-15 (his realized best bucket is RVOL ≥ 5×); 2× is the scanner floor, not the sweet spot. |
| KzV-15 | [59:09–1:00:43] | Exit indicators: "The obvious appearance of a hidden … seller."; "A large burst of red on the tape" forming a false-breakout topping tail; "I don't like entering on a red candle … unless that's my starter and I'm buying … a dip." | `partial` | Hidden-seller/big-seller legs out of scope (book data); red-candle-in-trade and topping-tail legs are bar-observable. Cross-ref C-02/C-05. |
| KzV-16 | [14:41–14:50] | "I really did take a $583 account and I did … turn it into over 100 grand in 45 days. … And I did it by taking one entry, one … exit." | `red flag` | Self-reported; **44 vs 45 days** vs I-A-02 ("$583 → $100K in 44 days") — same event, different day count, the I-A-03 window-dependence pattern. |
| KzV-17 | [11:28–11:52], [29:37–29:44] | "My average winners … are $1, 400." / "My average winners are 14 cents per … share." / "average share size is 10,000 shares." / "23,000 trades. 23,000 trades … over 12 million dollars of gross profit." | `red flag` | 14¢ × 10K = $1,400 — internally consistent arithmetic; trade count and gross profit unverifiable. Avg win $1,400 vs I-A-04's ~$1,000 — consistent with account growth. |
| KzV-18 | [1:35:11–1:35:19], [09:20–09:26] | "I'm over $10 million in in uh net … profit, and I started with less than 600 … in my account. And this is real money." / "over 2,200 of … these testimonials. Uh 92% are … excellent, five out of five." | `red flag` | "Audited broker statement" referenced but not verifiable from the video; testimonial stat is promotional and selection-biased. |

### IlsQCdU9JO0 — Inside My $280,000 Mobile Day Trading Station (2024-09-14)

Topics: equipment, mobile-trading, process-discipline, profit-cushion-gate, self-reported-pnl, simulator-first

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| Ils-01 | [02:42–02:58] | Mobile latency → slippage: "press the buy button and nothing would … happen for a second" then "I was in at a … much different price than what I was … expecting" | `out of scope` | Equipment content as expected (mostly H). One operational observation: connection latency converts to fill slippage — no measurable claim for bars-only data. |
| Ils-02 | [22:33–22:48] | Size down off-home-turf: "it's a good idea when you're outside … your typical workspace to bring share … size down a little bit" | `process guidance` | G-family. Contextual sizing rule. |
| Ils-03 | [22:51–23:01] | Daily profit gate on size: "The strategy I've been implementing as of late where I … don't take big size until I first … crossed $1,000 of profit on the day has … really helped me with consistency" | `process guidance` | Strongest operational content in the video. Same structure as G-04 (full size only after a winner) and KzV-10's "profit cushion" sizing input; names a concrete threshold ($1,000). |
| Ils-04 | [14:10–14:24], [23:55–24:02] | In-video P&L: "you'll see that I'm up … $1,553"; "Monday Tuesday … Wednesday I made 3,00 ,000 each day so I … did not hit my $5,000 daily goal" | `red flag` | Self-reported single-day/3-day figures framing the video. |
| Ils-04b | [24:35–24:46] | Equipment MVP: "total overhead in in equipment terms is … like a laptop a couple monitors and then … you know your trading account like … that's the money coming to table with … more money doesn't make you more … successful" | `out of scope` | Implicit claim that account size (beyond margin needs) adds nothing — unfalsifiable as stated, contradicted by his own KzV-17 sizing math. |
| Ils-05 | [25:21–25:39] | Sim-first ladder: "that is … where the simulated trading comes in" and only when "you can go back and say wow I actually … know what I'm doing I've got some … consistency here then that at that point … you say it's time to put some real money" | `process guidance` | Cross-ref G-07 (simulator-first) and G-05 phase structure. |

### Wd_iUsteoaw — Here's what's REALLY Happening... (2026-09-01)

Topics: market-regime, seller-control, point-of-control, leading-gainer-proxy, round-trips, regime-transition, session-review, red-day-discipline, relative-volume, self-reported-pnl

| # | Time | Claim as stated (verbatim quote embedded) | Status | Cross-refs/notes |
|---|---|---|---|---|
| Wd_-01 | [00:12–00:36] | Regime proxy via leader strength: "our leading gainer is up … only 58%. It's GoPro 160 million share … float stock" — "really says … something about the sentiment in the … market." | `candidate` | The most operational F-claim in the corpus: leading-gainer % (and its float size) as a breadth/sentiment gauge. Directly computable from daily data — register as the regime proxy. |
| Wd_-02 | [00:34–00:46] | Point-of-control shift: "this shift has been a shift … from control among buyers to control … among sellers. The point of control has … shifted from the buy side to the sell … side." | `candidate` | His regime variable ("sellers in control" / "buyers in control") never formally defined; observable correlates he cites: leading-gainer strength, round-trip frequency (Wd_-06/-07). Any test must pre-register the proxy, not the label. |
| Wd_-03 | [22:50–23:14] | Regime→size response: "feeling right now is that the sellers … are in control." … "sellers are in control, I've got to kind … of batten down the hatches. I've got to … trade with smaller size." — and "rather than … assume that things are going to work, … assume that they won't work." | `candidate` | Regime-conditional sizing now testable *if* Wd_-01/-02 give the regime definition — unlike G-06, which was unmeasurable for lack of one. Cross-ref G-06, KzV-10. |
| Wd_-04 | [23:48–23:58] | Cold-market veto: "wait for stocks that actually prove that … they can hold up because I'm going to … see more of these pops and reversals," | `candidate` (E-veto) | "Proof-of-hold" as an entry precondition in cold regimes; in-session stand-down family with J-C-01. Operationalizable: require N-bar hold above the pop before entry. |
| Wd_-05 | [25:04–25:18] | Late-cold dynamics: "stop buying, then the moves get smaller … and smaller. Shorts get more and more … aggressive until we reach a point where … the second something pops up, shorts are … hammering it and it actually ends up … going red in spite of having news." | `candidate` | Sharp testable prediction: in late-cold regime, news-day returns flip negative. Stratify news-pop next-day returns by regime phase. |
| Wd_-06 | [26:09–26:21] | Regime ignition mechanism: "typically the way these um shifts occur, … with one stock that makes makes just an … exceptional move." — "shorts got stuck." (+500–700% day). | `candidate` | Cold→hot transitions are single-stock short-squeeze ignition events; the transition date is identifiable ex post via the outlier stock. |
| Wd_-07 | [27:30–27:43] | Late-hot signature: buyers "so confident … they'll jump on even the most mundane … headlines" — "and the stock still goes up 50 or 100%." — after which shorts re-enter and control "shifts a little bit more subtly". | `candidate` | Hot-top proxy: mundane-headline movers producing large gains mark the late-hot phase. Needs a headline-quality proxy; otherwise exploratory. |
| Wd_-08 | [27:59–28:04] | Asymmetry claim: "shift from hot to cold is much more … subtle than the shift from cold back to … hot typically." | `partial` | Testable shape: breadth decay is gradual, breadth ignition is discontinuous. Vague — needs an operational asymmetry definition before pre-registration. |
| Wd_-09 | [28:40–28:49] | Cold-streak magnitude claim: "realistically the longer it's cold, the … bigger the move will be when that stock … does surprise us because shorts will be … so confident." | `candidate` | Testable: post-streak ignition magnitude vs cold-streak length (monotonicity). |
| Wd_-10 | [03:22–04:35] | Red-day stand-down counterfactual: "it is possible to … stop sooner when the day starts going … against you"; "the only thing is walk away when I'm … down 20 grand and not continue trading." — $74K + $66K red days; "None of these days where I'm green, I … was down more than 20 grand before … recovering to green." | `red flag` | Self-reported, but the arithmetic is checkable and consistent: −$54K/−$46K saved ≈ +$100K on $211K ≈ the claimed +50%. The "no green day ever dipped >$20K" claim is an intraday-drawdown statement we cannot verify; the rule joins I-G/three-strikes as process. |
| Wd_-11 | [07:19–07:38], [05:46–05:54] | After-10 no-trade: "high-risisk no trade zone"; "need to have a harder stop um at 9:30, … 10:00 a.m."; Fridays: "was tightening up my risk on Fridays and … therefore was able to avoid having a … repeat of those big red days I had". | `process guidance` | Notable cross-year tension with I-B-05 (2015: profits concentrated "9:30 to 11:30"; "9:30 to 10:30") — the profitable window has shifted/changed story; 7–10 a.m. remains the core (F-01). |
| Wd_-12 | [06:02–07:16] | Hour-of-day self-audit: "I'm losing money … between the hour of 10 and 11. In fact, … that I was making the most money between … 7 and 8." but over "last 12 months, I've done better between … 8 and 9." | `process guidance` | Window instability *within the same video* (1-month: 7–8 best; 12-month: 8–9 best) — the I-B-05 window-instability pattern recurring with his own data in hand. |
| Wd_-13 | [10:59–11:18] | Adjustment bundle worth "+50%": "if I stop trading when I'm down 20 … grand, I'm a little more cautious on … Fridays, I'm I'm careful about the time … of day I'm trading, and I'm avoiding … stocks with lower relative volume. Those … improve my profitability by as much as … 50%." | `red flag` | Counterfactual performance-improvement claim from one month's self-audit; same +50% figure as Wd_-10. |
| Wd_-14 | [09:41–10:01] | Volume/RVOL self-audit: "I did best on stocks that had … more than 25 million shares of volume" — "Lighter volume stocks I struggled on."; "on stocks that had at least five times … 500% five times higher volume on the day … I traded it versus the 50-day average." | `candidate` | Testable on daily bars. **Tension with KzV-14**: teaching threshold RVOL ≥ 2 vs realized best bucket ≥ 5×; also liquidity-preference drift between 2023 and 2026. |
| Wd_-15 | [16:44–16:59] | Biotech dilution mechanism: "notice here that they've got a shelf … registration, which they just filed. … there's a high likelihood that they're … going to take the opportunity to sell … shares on the open market to raise money" — which "has a real effect on the price of the stock." | `out of scope` | Needs SEC filings data, not bars. Family-relevant as an E-veto (fresh shelf registration → don't buy the squeeze); he used it to pass on BIAF [19:22–19:58]. |
| Wd_-16 | [19:32–20:01] | The pass itself: "Quality over quantity." on a squeeze where "it barely even … has half a million shares of volume. I … don't know. The volume's too light." — stock then doubled-topped and sold off. | `process guidance` | Anecdotal vindication of the light-volume veto (E-family); single case, hindsight-available. |
| Wd_-17 | [02:44–03:00], [04:49–05:11], [12:03–12:11] | Account stats: "this year with about $96,000 in my … account." → "had a balance of about $2.1 million."; August: "$287,000 of total … profit right here. Accuracy was about … 65%. Average winners were 6,000. Average … losers were 5,700."; "That's nearly $24 million … of trading profits and showing, you … know, 68% accuracy". | `red flag` | Self-reported; 68% long-run accuracy matches I-A-04's ~68–70% stable core (a rare cross-year consistency point); $96K→$2.1M in 8 months and $24M lifetime rest entirely on his posted statements. |

### Notes (KzVbXzkoZkA, IlsQCdU9JO0, Wd_iUsteoaw)

## Summary counts

KzVbXzkoZkA 18 rows (4 red flag, 9 candidate, 3 partial/process, 2 structural-candidate); IlsQCdU9JO0 6 rows (1 red flag, 3 process, 2 out of scope); Wd_iUsteoaw 17 rows (3 red flag, 8 candidate F/D-family — the first regime claims in the corpus with a usable operational proxy (Wd_-01 leading-gainer strength), 1 partial, 1 out of scope, 4 process).

Notable cross-video tensions: scaling requirements KzV-12 vs KzV-04 (no fixed methodology); RVOL floor 2× (KzV-14) vs realized-best 5× (Wd_-14); morning windows I-B-05 vs Wd_-11/-12; the $583→$100K run is 44 days in I-A-02 and 45 days here. All quotes are exact single-line substrings of the transcript files (splices marked with …); auto-caption errors preserved.

<!-- §J-CORPUS-END -->

## J.1 RV-conditioning re-measure verdicts — pre-registration #24 campaign (2026-09-01)

The §J scan established his *stated* RV parameters (threshold 5×, baseline
30–50 days, yFo-01/-05/-14, 3rE-02, GXl-12); pre-reg #8 had measured the
frozen detector's 20-bar/2.0 definition (§I.5: NO EDGE). Pre-reg #24
re-measured the identical conditioning question at his parameters
(`tools/measure_rv2.py`, frozen 2026-09-01 with two pre-results amendments
per the #20 precedent — rv-column propagation bug, then the missing RV30
column; no verdict was ever produced by a buggy tool). One Holm family of
five slots, OOS 2016–2025, count floor 100, bootstrap B=1000 seed 20260813.

| Slot | Hypothesis | Verdict | Evidence |
|---|---|---|---|
| H1 | Shape A, RV50 ≥ 5 beats random + same-ticker | `tested, no edge` — **NO EDGE** | n=347; mean +0.46%; excess −0.06pp (p 0.964) / −0.09pp (p 0.922); p_input 0.964 |
| H2 | Shape B, RV50 ≥ 5 beats both | `tested, no edge` — **NO EDGE** | n=133; mean +0.41%; excess −0.09pp (p 0.956) / −0.36pp (p 0.806) |
| H3 | Shape B contrast high ≥ 5 vs low < 2 | `tested, no edge` — **NO EDGE** | +0.44pp (CI −1.40..+2.38pp, p 0.654) |
| H4 | Shape C contrast | `tested, inconclusive` — **INCONCLUSIVE** | high cell n=7 < 100 floor |
| H5 | Shape A contrast (live under RV50) | `tested, no edge` — **NO EDGE** | +0.48pp (CI −0.40..+1.42pp, p 0.324) |

**Reading.** At the parameters he actually states, the RV-conditioning claim
shows **no edge anywhere it is testable** — the §I.5 null is robust to his
own definition, not an artifact of our frozen formula. Every contrast again
leans in his claimed direction (+0.28 to +0.48pp), exactly as in #8
(+0.30pp, p 0.302) — a persistent directional whisper that has now failed
significance at 2×/20-bar, 5×/50-bar, and every sensitivity cell. The
5×-subset is rare (11% of A detections, 2.6% of B), so his claim's practical
content — "trade only RV≥5 names" — would have filtered 89–97% of the
detector's own signals for no measured benefit. Sensitivities (no verdicts):
RV50@3.0 and @2.0, RV30@5.0/@2.0 — all NO-EDGE-shaped, one soft positive
(B contrast +0.69pp at RV30≥5). Cross-check: the RV20≥2.0 recomputation
reproduces §I.5's cells exactly (n = 3,941 / 1,026 / 46). Verdict rows
flipped: yFo-01/-05/-09/-14, 3rE-02 (tested); GXl-12's RV leg noted.
