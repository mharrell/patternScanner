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
| I-B-06 | jfe1Zl-5EQI [17:45–18:16], [23:16–23:55], [19:58–20:11]; txWaMpSzHhM [23:42–24:05] | Reversal checklist: "an RSI above 90 or below 10 are going to peak my interest a candle outside the bounzer bands is going to peak my interest and also five to ten consecutive candles ending with a pin bar or a doji"; volume "half a million in shares or higher I prefer a million", peaking at the sell-off bottom; the V5/V8 scanner screens "RSI below 20 and then... the green above 80". Class 1 caveat: RSI "is more condition to find stocks at extremes it's not by any means a buy or sell indicator". | `candidate` / `partial` — the RSI-extreme component is testable on daily bars (see I-X-01); the 90/10-vs-20/80 discrepancy (trade threshold vs scanner threshold) is an internal tension; **Class 1 says RSI is not a signal while Class 4 treats RSI extremes as entry conditions** — within-corpus inconsistency. |
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
| I-D-01 | xTPcI7HHu5w [25:38–26:18]; H82nRY9TYU4 [20:16–20:26] | Price sweet spot: "stocks between $2 and $5 I made a quarter million dollars two hundred and forty thousand dollars profit... stocks over $5 40,000 bucks... above 20 I ignore it" (2017 P&L); 2019 filter: "I only trade stocks between $2 and $10 so this was off the list this was too cheap too expensive". | `candidate` — testable-daily: forward returns by price tier (cross-ref A-04's ">$10 was unprofitable" anecdote). **Internal inconsistency:** $2–5 (2017) vs $2–10 (2019); the claim needs its year. |
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
| I-F-01 | jfe1Zl-5EQI [16:01–16:09] | "We know that almost all of the big moves will eventually be corrected" (rationale for reversal trading). | `candidate` — testable-daily: large multi-day moves (≥3 ATR) retrace ≥ half within 5–10 sessions. Same mean-reversion family as what we already measured: crossed-B breakouts in bear days *fade* (§E.6). |
| I-F-02 | jfe1Zl-5EQI [28:28–28:47] | "The move up that may have taken hours can be all given back in a matter of minutes on the good top reversal... the Bulls take the stairs and the Bears take the window". | `candidate` — testable-daily: per-bar downside moves are larger/faster than upside moves (speed asymmetry). |
| I-F-03 | txWaMpSzHhM [31:55–32:38] | "Stocks will trend with the overall market unless they have a reason not to" — catalyst names buck the market ("running when the markets tanking"). | `candidate` — testable-daily: daily-return correlation with the index; catalyst proxies (gap, volume spike) reduce correlation / raise idiosyncratic move size. |
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
| I-X-01 | rgVdgR1y1Dg [03:16–03:24] (Trading 212) | RSI rule: "anything above seventy percent... the market is said to be overbought anything below thirty percent... the market is said to be over salt" (overbought ⇒ pullback due, oversold ⇒ bounce due). | `candidate` — testable-daily: RSI(14) > 70 → below-average forward returns; < 30 → above-average. **Corpus tension:** Class 1 says RSI is "not by any means a buy or sell indicator" (I-B-06). |
| I-X-02 | rgVdgR1y1Dg [05:33–05:39] (Trading 212) | "These divergence signals are a lot less common so arguably a bit more reliable". | `candidate` — testable-daily: divergence frequency vs 70/30 crossing frequency, and directional hit rates of each. |
| I-X-03 | rgVdgR1y1Dg [05:51–06:15] (Trading 212) | Bullish divergence: price makes a lower low while "the RSI... we've got higher lows so this is a suggestion that maybe this weakness is running out of steam". | `candidate` — testable-daily: price lower-low + RSI higher-low → above-average forward returns. |
| I-X-04 | rgVdgR1y1Dg [06:39–07:03] (Trading 212) | Bearish divergence: "the market has pushed to a high pushes a little bit higher... we've got our lower high so that's a suggestion that maybe the strength is running out of steam". | `candidate` — testable-daily: price higher-high + RSI lower-high → below-average forward returns. |
| I-X-05 | rgVdgR1y1Dg [07:40–08:03] (Trading 212) | Stop placement for bullish divergence: "we have two obvious levels to place our stop loss beyond because by definition... the market shouldn't take out that prior extreme low". | `candidate` — testable-daily: post-signal breach of the prior extreme low. |
| I-X-06 | lMZv0K71HOg [02:37–02:50] (EatSleepProfit) | "Most of the penny stocks and small caps hey these are horribly fundamentally run companies so over the long term these companies are going to fall drastically". | `candidate` — testable-daily: sub-$5 cohorts' multi-year forward returns / delisting rates (cross-ref A-04, I-D-01 price-tier family). |
| I-X-07 | lMZv0K71HOg [06:56–07:04] (EatSleepProfit) | Per-trade target: "I usually like to aim for 88 to 10%" (caption garble for "8 to 10%"). | `out of scope` (process). |
| I-X-08 | kZNF5Hynk4E [06:35–07:23], [08:33–08:52] (Cameron Bennion) | Robinhood fills ~$0.05/share above the ask on a $1 stock (≈$50 per 1,000-share order); PFOF "profit of about three to four cents" per share. | `out of scope` — broker execution claims; no order data. Kept as the corpus's only execution-quality content. |
| I-X-09 | lMZv0K71HOg (whole video) (EatSleepProfit) | PDT-rule mechanics (90-day restriction, cash-account workarounds). | `out of scope` — regulatory process content. |

### I-Notes: cross-course and internal consistency (2026-08-14 scan)

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
   EDGE); I-F-01 (big moves get corrected) is the same mean-reversion
   family as §E.6's bear-day fade; I-D-06 (low float) is testable with data
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
8. **B-01 (micro pullback)** — needs intraday data; the daily-bar adaptation
   (Shape B: pullback + new-high) was already measured and **rejected**
   2026-08-13 (§B.5-B). The intraday rule remains a `partial` candidate.
9. **B-02/B-03/B-05/C-01/C-03/C-04 (entry/exit variants)** — system-comparison
   questions. Daily adaptations of B-02 (Shape A) and B-05 (Shape C) measured
   and rejected (§B.5-A, §B.5-C); the intraday and comparison forms remain
   untested.
10. **I-D-07 + I-E-01 (high-relative-volume conditioning)** — ✅ MEASURED
    (pre-reg #8, 2026-08-14): F1-A/B **NO EDGE**, F2-B NO EDGE (contrast
    +0.30pp, p=0.302 — the claimed direction, never significant), F1-C/F2-C
    INCONCLUSIVE (count floor), F2-A INCONCLUSIVE by construction (every A
    detection is high-RV — the detector's V=2.0). The absolute leg is null;
    the differential leg whispers but never clears. Verdicts: §I.5.
11. **I-X-01 (RSI 70/30 daily-bar reversal bias)** — testable-daily on the
    existing universe; large sample; classic claim with a specific teaching
    ("overbought ⇒ pullback due, oversold ⇒ bounce due").
12. **I-X-02/03/04 (RSI divergence frequency + reliability)** — testable-daily;
    needs a pre-registered divergence definition (swing scanning on daily
    bars) before measurement.
13. **I-F-01 (big moves get corrected)** — testable-daily mean reversion of
    ≥3-ATR moves; same family as §E.6's fade finding.
14. **I-F-02 (bulls take the stairs, bears take the window)** — daily-bar
    downside-speed asymmetry.
15. **I-D-01 (price-tier edge: $2–5 vs >$20)** — testable-daily; ties to
    A-04; the 2017/2019 band inconsistency must be handled in the pre-reg.
16. **I-X-06 (penny/small-cap long-term fall)** — testable-daily multi-year
    horizon; needs delisting-aware data work.
17. **I-F-03 (stocks trend with the market unless catalyst)** — correlation
    decomposition; cheap but lower value.

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
- [x] Scan `transcripts/warrior-trading/` (the 2015 "Class 1-12" playlist) for
  claims — done 2026-08-14: 53 rows in §I (I-A..I-X + §I-Notes), quotes
  re-verified against the transcripts, priority list updated (items 10–17).
  **Compare the two courses for drift** (same strategy 10 years apart?
  parameters changed? claims escalated?) — still open; §I-Notes has partial
  qualitative evidence (rules consistent, one flagged tension). The formal
  n-gram/parameter comparison remains a future task; both corpora are
  ingested.
- [x] Fill `topics`/`claims` frontmatter in transcript files as the ledger
  grows — done 2026-08-14 for all 13 transcript files (§I rows mapped back
  per video; non-trading videos get topics only).
- [ ] Record the *expected* failures: when a claim is measured and rejected,
  log the verdict here (status → `tested, rejected` + link to the pre-reg
  doc). **First exercised 2026-08-13 (§B.5).** The ledger is the audit trail;
  keep every row, never delete.
