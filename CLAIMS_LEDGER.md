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
