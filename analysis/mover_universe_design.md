# Mover-universe design — testing his rules on HIS population

**Status: DESIGN 2026-09-18, before any capture.** Implementation follows
only after this document is committed. The pre-registration (#33) is
written as DRAFT and frozen after a one-week pipeline shakedown — while
the archive is still young (the anti-look-ahead point of the house
regime).

## 1. Why this exists

The 2026 cycle's clearest structural finding is the **universe
mismatch**: every campaign whose population lives in "his" corner of the
market returned the same signature —

- #31 H2: his ">25M share volume days" claim — 77 of 25,414 daily
  detections; the claim's population is unreachable on this index;
- #32: the +40% intraday leader — **zero occurrences** in 21 bar-dates
  × ~600 S&P 600 names;
- #25: his price bands DO separate — but diluted ~⅔ vs his own 2017
  numbers, measured on an index whose members only visit his bands
  briefly.

Meanwhile the corpus's selection claims (#25's bands) carried the only
durable daily EDGE, and the timing rules (#15/#19/#21/#27) all nulled or
faded **on the S&P 600**. The open question the whole intraday track
cannot answer from its archive: **do his timing rules have edge inside
his own population** — sub-$5 (today, $1–$20) high-volume movers — or
is the population itself the only edge? This design builds the archive
that can answer it.

## 2. The population — a frozen roster rule

His scanner (Trade Ideas-style gapper/mover scans) is operationalized as
a **public, rule-defined, nightly roster capture**:

- **Source**: Yahoo's public day-gainers screener (the free equivalent
  of a retail momentum scanner), fetched once each evening after the
  session closes and the screener reflects the completed session.
- **Filters (frozen before first capture)**:
  1. last price **$1.00–$20.00** (his current stated bands, #25 §J.2);
  2. day volume **≥ 1,000,000 shares** (the retail-scanner floor; his
     own ">25M" mega cell is a sensitivity, not the population);
  3. listed exchanges only — **NMS (Nasdaq), NYQ (NYSE), ASE (AMEX)**;
     OTC/pinks excluded (his teaching centers listed small caps; the
     exclusion is a documented limitation, not an oversight);
  4. **top 100 by % change** after the filters (the "top of scan" his
     practice actually watches).
- **Evidence**: the raw screener response (JSON) and the derived roster
  CSV are archived every night — `data/mover_rosters/<date>.json` +
  `<date>.csv`. **Empty-roster nights are recorded as empty** — the
  roster is never silently skipped, and "no qualifiers today" is itself
  population data.
- **Blindness**: the roster rule above is fixed before the first
  capture and never edited afterward. No roster is ever hand-amended;
  a Yahoo screener schema change is an *incident* (recorded, roster
  halted) — not a silent filter tweak. Any rule change afterward
  defines a NEW population and a NEW pre-registration.

Deliberately NOT in the rule: float caps (Yahoo screener float fields
are unreliable; #25's float families stay daily-track), gap size
(endogenous — the day's % change IS the outcome), RVOL ratio (needs a
baseline universe we do not have whole-market).

## 3. Archive mechanics — the proven pattern, second instance

`data/intraday_movers/`, mirroring `data/intraday/` exactly
(`analysis/mover_universe_design.md` §3 = `data/intraday/README.md`):

- same immutable `(bar-date, ticker)` parquet layout, atomic writes,
  SHA-256 manifest chain, `--repair`/`--adopt` with recorded reasons,
  night-completeness rule, tz-normalization, split recording;
- same Yahoo 1m driver (rolling 7-day window, extended hours);
- implementation: `tools/fetch_intraday_bars.py` gains an
  **`--archive-root`** flag (default `data/intraday` — byte-identical
  behavior for the existing nightly task) and the mover pull runs it
  with `--universe data/mover_rosters/<date>.csv --archive-root
  data/intraday_movers`;
- **overlap is expected and allowed**: a name in both the S&P 600 and
  the roster lands in both archives. They answer different questions
  (index population vs scanner-output population) and cross-checks
  between them are a feature;
- **backfill slack**: because Yahoo keeps a rolling 7-day window, the
  roster captured on night N can fetch bars for its own session (night
  N) and back to N−6. The pipeline back-fills any missing (roster-date,
  ticker) day files on every run until they age out — no special mode.
- ops: nightly task after the S&P 600 pull (proposed 22:35 MT), QA
  chained (`--qa`), same 23:00 push sweeps both archives.

## 4. What will be tested (pre-reg sketch — NOT frozen)

The point is **within-population contrasts of his timing rules**, using
the SAME frozen detectors (imports, never modifications):

- **#33 (planned)**: B-01 micro pullback + the #19 reversal entry, on
  the mover archive — the exact #15/#19 families re-run on the mover
  population. Baselines: hour-matched same-ticker and random *within
  the mover archive* (the right null is "other moments of the same
  movers," not "the index").
- The #32 sympathy test finally has its population: +40% leaders will
  occur here.
- The #25 daily bands re-measured *within* movers (does the band edge
  survive when every name is already in-band?).
- Floors: same shape (≥20 mover bar-dates, ≥2,000 events, ≥100
  tickers, ≥15 dates) — expected to open in weeks, not months: typical
  sessions have dozens of $1–$20, ≥1M-share listed gainers.

Freeze discipline: #33 freezes after the one-week shakedown (rosters
look sane, backfill works, QA clean) and BEFORE any forward-return is
computed on the archive. Measurement reuses the frozen engines;
`verify_intraday`-style integrity audit carries over.

## 5. Known limitations (recorded, not hidden)

1. **Yahoo screener top-100**: his real scanner watches more names;
   truncation at 100 biases toward the biggest gainers of the day.
   Recorded per night; a cap sensitivity can be declared at freeze.
2. **No OTC**: a large share of true sub-$5 volume trades OTC; excluded
   by design (limitation 3 above).
3. **Screener = Yahoo's snapshot**: percent-change/volume figures are
   Yahoo's, taken once nightly; intraday timing of the snapshot is
   recorded. The roster defines the population; bar-level measurement
   never uses screener numbers.
4. **Forward-only**: the archive accumulates whatever regimes come;
   small-cap mover regimes are seasonal (his own "hot sector" talk).
   Verdicts are conditional on the captured window, as everywhere in
   this repo.
5. **Roster ≠ tradability**: no spread/HTB/shrink modeling at capture;
   the 0.15% cost model applies at measurement as in every campaign.

## 6. Build order

1. `tools/mover_roster.py` — the nightly screener (fetch → filters →
   roster CSV + raw JSON evidence), smoke-testable any trading day.
2. `fetch_intraday_bars.py --archive-root` generalization (default
   behavior byte-identical; existing nightly task untouched).
3. One-week shakedown (rosters + backfill + QA), then **pre-reg #33
   freeze**, then the scheduler entries (user-registered, as before).

*No capture begins before this document and the roster rule are
committed to main.*
