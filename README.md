# patternScanner

Detect predefined chart shapes on US equity daily bars and measure, honestly,
whether they predict forward returns better than chance.

**Status:** Phase 4 — verdicts written back to the ledger 2026-08-14.
Four pre-registered campaigns are measured. **Shapes A/B/C** (pre-reg #2):
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
control; the drift is late-era beta, not selection edge. Per the brief §1,
Phase 5 (paper trading) is **not triggered** after five campaigns.
Verdicts:
[CLAIMS_LEDGER §B.5 / §D.5 / §E.5 / §D.6 / §D.7](CLAIMS_LEDGER.md);
reports:
`data/cache/measure_report.md`, `data/cache/pillar_measure_report.md`,
`data/cache/veto_measure_report.md`, `data/cache/momentum_measure_report.md`,
`data/cache/decade_measure_report.md`. Next candidates from the ledger:
E-03 (MACD-cross breakout rejection), or a year-concentration follow-up
(pre-reg #6) on the per-year drift detail.

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
  decomposition, frozen 2026-08-14. Verdicts return to the ledger.
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
