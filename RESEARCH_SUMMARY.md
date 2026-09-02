# Research Summary — measuring Ross Cameron's claims, 2026 cycle

**patternScanner** tests the public claims of a trading educator (Ross
Cameron / Warrior Trading) against market data under pre-registration
discipline. This document is the one-page result of the 2026-08→09 cycle:
a full claim scan of his YouTube corpus ("My Favorite Episodes", 26 videos,
2015–2026 — ledger §J) followed by nine pre-registered measurement
campaigns (#24–#31 daily bars, plus the frozen intraday backlog). Full
audit trail: `CLAIMS_LEDGER.md` (476 scanned rows, 8 verdict sections) and
`PREREGISTRATION.md` (32 pre-registrations, frozen tools, recorded
amendments).

## The method, in one paragraph

Every claim is transcribed verbatim (auto-captions, quote-verified) into a
ledger row with a status. Every testable claim becomes a **pre-registered
campaign**: translation table (claim → measurement, deviations fixed
before data), hypotheses with pre-assigned Holm slots, verdict rules,
baseline set (era-matched random entries, buy-and-hold, same-ticker),
0.15% round-trip cost, in-sample/out-of-sample split (IS 2000–2015, OOS
2016–2025), bootstrap CIs, count floors — all frozen before data is
touched, measured once (one-shot rule; every post-freeze tool fix is a
recorded amendment, never a silent change). Nothing counts until it
survives that.

## The nine campaigns (2026-09-01/02)

| # | Claim family | Verdict | Key evidence |
|---|---|---|---|
| #24 | RV conditioning at HIS stated parameters (5×/50-day) | **NO EDGE** | all four testable Holm slots; the earlier null (#8) is robust to his own definition |
| #25 | his newer price bands + float caps ($2–20/$1–20; ≤20M/≤10M float) | **EDGE ×4** | +0.40 to +0.52pp (price), +0.09/+0.25pp (float) — real, but diluted ~⅔ vs his 2017 $2–5 sweet spot (+1.11pp) |
| #26 | his market-structure beliefs (±4% days "rare"; 5–10 gainers/day; 2020–21 parabolic peak) | **CONTRADICTED ×2, PARTIAL** | 11% of ticker-days exceed ±4%; median 2 gainers/day; the parabolic peak year is 2009, not 2020–21 |
| #26 | 200DMA veto ("never buy right under the 200") | **NO EDGE** | right-under ≈ right-above (p 0.094) |
| #28 | gap-and-go | **FADE** | ≥+2% gappers' open→close UNDERPERFORMS flat opens (−0.22pp, p 0.008) — direction inverted |
| #28 | momentum continuation; round-number proximity | **NO EDGE ×2** | nominal p 0.038/0.056 in the claimed direction — whispers |
| #29 | "trade better with a tailwind" (regime conditioning) | **NO EDGE ×2** | hot-vs-cold +0.35pp at p 0.052 — the closest whisper; hot-regime entries still don't beat chance; cold-regime entries are bad (−0.22%) — loss avoidance, not alpha |
| #30 | sector sympathy | **EDGE (same-day) / NO EDGE (next-day)** | +0.28pp same-day (p 0.014), +0.08pp next-day (p 0.716) — real, visible, fully priced by the next open |
| #31 | "bigger winners = lower accuracy" | **FADE** | hit rate RISES with horizon: 44.4% (N=1) → 51.8% (N=20), +7.4pp, p≈0 — the mechanism is backwards on daily bars |

## The five findings

1. **His selection geometry is real — and diluted.** Every price band and
   float cap he has ever stated separates from its complement (monotone
   tiering: sub-$2 +6.3% → $2–5 +1.5% → $5–10 +0.5% → $10–20 +0.3% →
   >$20 −0.1%). But the drift is measurable: his 2022–24 bands earn ~⅓ of
   the edge his 2017 numbers implied, while the rhetoric escalated.
2. **His mechanism stories invert.** The two claims that explain his own
   style — gap-and-go continuation and "avoid givebacks by taking base
   hits" — are direction-inverted on daily bars: gap-ups mean-revert
   intraday; holding longer RAISES hit rate and mean return.
3. **His context beliefs are wrong.** The market-structure numbers he
   teaches as the world's shape (move rarity, gainer counts, the 2020–21
   melt-up memory) contradict the data — including his own survivor-biased
   data, where the bias runs against the contradiction.
4. **The directional whisper.** Five separate campaigns lean in his
   claimed direction with nominal p-values (0.038–0.65) that never clear
   Holm correction. This is itself a result: a corpus of 26 videos and a
   decade of teaching produces consistent *signs* and no *magnitudes* —
   the signature of a trader describing real but tiny effects (or of
   selection memory) rather than a testable edge.
5. **Effects are visible, not tradeable.** The strongest confirmed claim
   (sector contagion, EDGE) exists only inside the parabolic day — the
   exact window his 1-minute practice occupies and daily bars cannot
   capture. His craft is real at his resolution; it does not survive the
   round-trip to daily data. The intraday backlog (#15–#22, #27, #32 —
   frozen, firing when the paper-log floor opens) is the direct test of
   that residue.

## The corpus measures itself

The videos contain their own method critique, stated plainly: an
overfitting confession ("I was essentially creating a formula... that
perfectly matched a set of historical data" — GXl-06), "I don't actually
have the data on this chart" (GXl-14), and "everyone is posting their
P&Ls... most of them are only posting when they're green" (dkO-06). The
performance narrative escalates with the telling ($335K → $1M → $10M →
$12.6M → "nearly $24M") while the only stable figures are ~68–70%
accuracy and ~1:1 average win/loss — and "audited" rhetoric that is never
shown. This repo's discipline (pre-registration, one-shot measurement,
survivor-bias checks, the red-flag rubric) is the corrective his own
caveats point to.

## What's next

The intraday track: pre-regs #15–#22, #27 (the MACD crossover gate — his
primary untested rule), and #32 (intraday sympathy) are frozen and
§5-gated on the paper-log floor; they fire via `tools/gate_opener.py` when
≥20 full-universe 1-min bar-dates accumulate. Verdict recording follows
each fire. Nothing on the daily track remains: every claim from the §J
scan that daily bars can express has been tested.