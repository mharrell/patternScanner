# Next project — design sketch: a cost-first intraday research program on the mover population

**Status: DRAFT 2026-09-23, for review. Nothing here is frozen, pre-registered
or started; no data has been purchased and no capture has begun.** This is the
design half of a *new* project that would ask a different question from
`patternScanner`'s. It exists because the 2026 cycle's results prune the search
space hard enough to make a focused attempt cheap — and because the obvious
next move (buy quotes, test the timing rules properly) is the one the cost
screen has already ruled out.

**This is research design, not investment advice. Nothing here trades, and no
claim of profitability is made or implied.**

## 1. Why a new project, and what changes

`patternScanner` optimizes for falsifying claims: a null is a success and the
bar is statistical significance under pre-registration. Its output is a record
of what does not work, plus a handful of conditioning facts. A project with
*making money* as the objective has a different objective function, and it must
be honest about that rather than quietly relaxing the old one:

| | patternScanner | this project |
|---|---|---|
| Question | does the claim beat chance? | does the construction survive fills, cost and capacity? |
| Primary metric | excess return vs matched baselines | **net P&L per day, after observed fills** |
| Binding constraint | statistical power, count floors | **spread, capacity, PDT, no-fill** |
| Success | an honest verdict | a capacity number and positive expectancy — or a cheap kill |

The **discipline stays identical** — pre-registration, one-shot measurement,
floors, gates, archived evidence, recorded amendments — and it matters *more*
here, because a P&L target is the most effective overfitting engine available.

## 2. What the 2026 cycle already settles (the pruning)

This is the most valuable input, and it is why the project can be small. These
are **measured results**, not opinions, and each one closes a branch:

- **Entry confirmation does not work at the 1-minute level.** #19's reversal
  new-high is a FADE in *both* directions on 85,707 events; #15's B-01 entry is
  −0.21% after cost and bleeds monotonically with holding time. Entries mark
  local extremes: what the corpus reads as confirmation is where the move
  exhausts. → *Do not build pattern-confirmation entries.*
- **Waiting costs money.** The pullback-wait (#15 F3), the second candle
  (#19 F3) and the base hit (#31) each invert. → *Do not build patience rules.*
- **Filter stacks do not separate good entries from bad.** The two-filter veto
  (#21) and the MACD gate (#27) are NO EDGE on four slots each; the veto cuts
  ~70% of entries and keeps no better than it kills. → *Do not build filter
  stacks; that is where multiple-testing lives.*
- **Per-minute horizons are structurally expensive.** 83% of index minutes and
  63% of mover minutes have a range below 0.15%. → *Do not scalp single
  minutes.*
- **Both long legs lose before cost is charged** (gross −4.1bp #15, −4.4bp
  #19): unfixable by any fill model. **The best positive intraday leg earns
  +4.4bp gross against a 6.2bp median tick floor** on its own events. → *Taker
  timing strategies on the index population are closed by arithmetic.*
- **The exit, not the entry, owns the leverage**: within the same entry set and
  window, the exit choice spans ~60–70bp while the entry contributes ≈0. →
  *Spend the effort on exits and execution, not on entries.*
- **Selection is the only durable effect found**: the price-tier family is
  monotone across five bands and passes the §5 gate (#16); stop placement
  passes too (#14). Both are *conditioning* facts, and the tier effect is a
  daily-horizon cross-sectional fact — not a daytrading signal.

Sources: `CLAIMS_LEDGER.md` §K.1–§K.6, §I.11, §I.13, §J.8;
`analysis/cost_screen_2026-09-22.md`.

## 3. The one open question worth money

The cycle's structural finding is the **universe mismatch**: the +40% leader
claim had *zero* occurrences in 21 bar-dates × ~600 index names (#32); the
>25M-share population was 77 of 25,414 detections (#31); the price bands are
diluted ~⅔ on an index whose members only visit them briefly (#25). Every
timing null above was measured on the **S&P 600** — a pond the rules were never
about.

**The open question: do the rules have edge inside his own population, or was
the population the only edge?** That is what pre-reg #33 exists to test, and it
is the only hypothesis in the repo with a plausible money path. This design
does not replace it; it says what a money-seeking program would add around it.

## 4. What the new project would need that the old one did not

**4.1 Quotes.** Every verdict in the repo is a recorded-bar result; #23 closed
with the tradeable-price row empty because the input layer was manual. Nothing
about profitability is testable until entry and exit prices come from a bid/ask
source at the size contemplated. Narrow slice, not a market history: a few
weeks of top-of-book plus prints for the **mover roster names** (a few hundred
symbols) is enough to calibrate a cost model and a no-fill curve. Free
IEX-based feeds can supply the *shape* of the spread distribution at zero cost
with a known caveat (IEX's share of thin-name volume is small, so treat its
levels as a lower bound).

**4.2 A cost model that can be defended.** The cost screen shows the frozen
0.15% convention is conservative for the index (0.038% tick floor on 80% of
name-days) and optimistic by 2–9× for the movers (0.274% / 0.609% / 1.361% in
the $5–10 / $2–5 / $1–2 bands; 61% of roster name-days above 0.15%). Cost is
the primary object of study here, not a sensitivity.

**4.3 An account-regime statement.** PDT caps a sub-$25k margin account at
three day-trades per rolling five sessions (the corpus misstates this as
$225k). That constraint, and the capacity ceiling on thin names, may govern the
design more than signal quality does.

**4.4 A different success criterion.** Capacity — the size at which expectancy
crosses zero — is the headline number, not the Sharpe ratio.

## 5. Pre-declared hypotheses (five, then stop)

Small and mechanism-based, each motivated by a measured result above. Cap the
program at five; a sixth is a new project.

| # | Premise | Construction | Killed if |
|---|---|---|---|
| **H1** | **Flow ignition continues**: early-session relative-volume × price-velocity outliers keep running | Fixed clock/level entry on the top RVOL movers; no pattern, no confirmation | net ≤ 0 at 2× the measured cost, or the edge dies below 1% of expected minute volume |
| **H2** | **The local-extreme mirror**: if his entries are adverse by ~4bp, the fade of that minute is favourable | The literal inverse of a frozen entry set on the mover archive (one run on owned data) | mirror gross < 2× tick floor, or it disappears once spread is included |
| **H3** | **Structure for exits, not entries**: price *travels* (HOD retest 83.8%; obvious stops hold 47.5% vs 53% typical) | Fixed entry; exits/targets/stops placed by the structure facts | targets cannot clear cost after modelled slippage |
| **H4** | **Selection is the durable effect**: the price tier is monotone and gate-passed | Cross-sectional tilt (low price × mid-RVOL), hold to close | the tier effect is smaller than the spread paid on those names |
| **H5** | **Maker beats taker at the same levels**: the cost data implies takers pay the spread that makers could earn | Passive fills at structural levels | adverse selection swamps spread capture (fill-toxicity test) |

H2 and H3 are nearly free (owned archives). H5 is the most interesting and the
most dangerous — you get filled precisely when you are wrong, which is exactly
why it is pre-declared rather than discovered.

## 6. Measurement rules (the parts that must not be negotiated later)

- **Net, from the first run**: quotes-derived entry and exit at the intended
  size, fees, short-locate costs, halts/LULD, and **no-fill counted as
  no-trade** — an unfilled limit is not a trade.
- **Bootstrap on per-day P&L**, not per-trade. Intraday results inflate badly
  through pseudo-replication; the day is the honest unit.
- **Capacity as a headline**: report the size at which expectancy crosses zero,
  at 0.1% / 1% / 5% of expected minute volume.
- **Benchmarks**: hour-matched random *within the population* (keep), plus
  passively holding the same names and SPY. Daytrading must beat doing nothing
  with the same universe.
- **One attempt budget across the five hypotheses**, pre-declared, with every
  hypothesis registered before its data is touched.
- **Forward evidence beats backtest**: the capture is forward (no
  survivorship) — keep that property; it is the repo's best asset.

## 7. Staged roadmap

| Stage | Work | Cost | Exit criterion |
|---|---|---|---|
| **0** | Spread/capacity census on the mover roster from a narrow quotes slice (or free IEX for shape) | one small data purchase, or free | a defensible cost model, or a kill |
| **1** | H2/H3 triage on the **owned** archives (bounds, not estimates) | free | either dead, or earns a quotes-based test |
| **2** | Net-of-quotes measurement + capacity curves for survivors | time | expectancy and capacity numbers, or a kill |
| **3** | Forward paper with order-level simulation (fill/no-fill), L-007 gap as the headline | time | the gap measured, not assumed |
| **4** | Tiny real size under pre-registered risk limits | capital — **the operator's decision alone** | live-vs-paper gap |

Stages 0–2 producing a *cheap kill* is a successful outcome. Nothing in stages
0–3 requires capital or execution.

## 8. Decisions only the operator can make

1. **Data budget** — the quotes slice is the one unavoidable new cost.
2. **Capital and account regime** — because PDT and the thin-name capacity
   ceiling bind harder than signal quality here.
3. **Taker or maker** — pay the spread, or try to earn it (H5).
4. **Objective** — "learn the truth about this style" and "make money
   daytrading" are different projects. `patternScanner`'s value is that it has
   never confused them; this one must not either.

## 9. Limits, recorded up front

- No verdict in the parent repo has ever been checked against a fill; until
  Stage 0–2 produce a quote-based cost model, **every expectancy claim in this
  document is an upper bound**.
- The mover roster turns over nightly and covers a handful of sessions so far:
  the population is small, recent and regime-conditional.
- Taking the corpus's own caveats seriously ("I was essentially creating a
  formula that perfectly matched a set of historical data"): the failure mode of
  this project is a backtest that fits the last three months of movers. The
  attempt budget and the forward-capture requirement are the guardrails.
- Base rates for retail intraday net of costs are poor. The honest prior before
  Stage 0 is that H1 and H4 die on spread, H2 and H3 are the most likely to
  reach Stage 2, and H5 is a coin flip that costs little to test.
