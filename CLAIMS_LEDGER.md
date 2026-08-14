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
| Secondary | `transcripts/warrior-trading/` — the fan-curated "Class 1-12" playlist (2015-era classroom footage). **Not yet claim-scanned.** |
| Standing question | Are the two courses the same strategy? (See §8.) |

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
| A-04 | [33:47] | March: $10K month, avg win $700, avg loss $1,100, 61% accuracy; says losses were on stocks >$10, so April he traded $2–10 → $36K month. | `red flag` — same category. Useful as a *testable claim in disguise*: "stocks >$10 were unprofitable for me in March 202X" is a claim about price-tier edge. |
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
| C-01 | [1:34:02–1:35:15] | **Exit indicators** (chart-based): (1) high-volume red candle; (2) MACD crossover; (3) topping tail / doji at top; (4) break of VWAP going down; (5) break of 9 EMA going down. | `candidate` — each is a formalizable rule; on daily bars, (1), (4), (5) translate directly; (2) needs the 1-min MACD. The interesting protocol question: are exits as a *system* better than fixed-2R exits? |
| C-02 | [2:31:08–2:31:27] | Exit indicator (6): "level 2 big seller or burst of red on the time and sales" (order-book data). | `out of scope` — we don't have level-2 data; note as a real edge risk: the strategy as practiced uses data we can't reproduce, so our backtest is of a *subset* of the claimed strategy. |
| C-03 | [1:12:02–1:12:34] | "When we make the full two steps down... it's basically when you have two candles that go lower and lower that we get out." | `candidate` — simple, testable: exit on second lower-low candle. |
| C-04 | [1:33:19–1:33:48] | "I want to cap my losers, not my winners": exit immediately at max-loss point; hold winners until an exit indicator. | `candidate` — the asymmetry claim; testable as system comparison (trailing vs fixed target). |
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
| E-02 | [02:01–04:57] | "**80% chance of this working**" (of the setup when both filters pass). | `red flag` — a magic number with no stated measurement window or sample. Pre-register as the *specific* hypothesis H: win rate ≥ 0.80 on the defined setup; expect it to fail honestly like most 80% claims. |
| E-03 | [1:21:54–1:23:04] | "When the MACD actually crosses... more times than not, any attempt to break out will reject and the price will end up selling off." (Learned in the 2022 bear market; "very consistent especially during the bear market.") | `candidate` — testable on daily bars: breakout forward returns conditioned on MACD-cross-just-occurred. Note the *regime* qualifier ("especially during the bear market") — pre-register the conditioning variable, don't let it be added post-hoc. |
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
6. **E-03 (MACD-cross breakout rejection)** — regime-qualified; pre-register
   the conditioning (regime variable) explicitly to avoid post-hoc fitting.
   Note: the zero-crossing reading was already measured as a pre-reg #3
   sensitivity with no signal (§E.5); the verdict layer remains unrun.
7. **B-01 (micro pullback)** — needs intraday data; the daily-bar adaptation
   (Shape B: pullback + new-high) was already measured and **rejected**
   2026-08-13 (§B.5-B). The intraday rule remains a `partial` candidate.
8. **B-02/B-03/B-05/C-01/C-03/C-04 (entry/exit variants)** — system-comparison
   questions. Daily adaptations of B-02 (Shape A) and B-05 (Shape C) measured
   and rejected (§B.5-A, §B.5-C); the intraday and comparison forms remain
   untested.

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
- [ ] Scan `transcripts/warrior-trading/` (the 2015 "Class 1-12" playlist) for
  claims — then **compare the two courses for drift** (same strategy 10 years
  apart? parameters changed? claims escalated?). The user flagged this as a
  future task; both corpora are already ingested.
- [ ] Fill `topics`/`claims` frontmatter in transcript files as the ledger
  grows.
- [ ] Record the *expected* failures: when a claim is measured and rejected,
  log the verdict here (status → `tested, rejected` + link to the pre-reg
  doc). **First exercised 2026-08-13 (§B.5).** The ledger is the audit trail;
  keep every row, never delete.
