# Pre-registration #1 — "Five Pillars" Stock Selection (Section D of CLAIMS_LEDGER)

**Frozen:** 2026-08-13 · **Status:** FROZEN — no parameter may be changed
after this date. Any change is a new hypothesis requiring a fresh
pre-registration and a fresh test window (DESIGN_BRIEF.md §4, §6).

Source claim: Ross Cameron, "The Ultimate Day Trading Guide",
[07:49]–[59:40] and [2:23:07]–[2:23:37]; ledger rows **D-01, D-02, D-03**.
As stated, his scanner picks stocks that are already moving: price range,
percent gain on the day, relative volume, news catalyst, low float; "not
opinion but it's fact" ([46:40]). We test the **computable legs** of that
claim on daily bars. This pre-registration follows DESIGN_BRIEF §6
(measurement protocol), §7 (bias checklist), and the S&P 600 universe
decision (2026-08-13 sign-off).

---

## 1. Translation table — as stated → as measured

Every mapping is fixed here, before data is touched. Deviations are
*defined*, not discovered.

| Claim leg (as stated) | As measured (daily bars) | Deviation / note |
|---|---|---|
| Price $2–$20 (P1) / $1–$10 (P2) | Closing price `c_t` in range | Close-based; his scan sees live quotes |
| "Already up 30% on the day" (P1) / "up 25%" (P2) | `c_t / c_{t−1} − 1 ≥ threshold` (close-to-close) | Intraday-tag-then-fade names excluded — we test the stronger subset (still up at close). Documented, not adjusted post-hoc |
| "5× relative volume" (P1) / "10×" (P2) | `v_t ≥ V × mean(v, prior 20 bars)` | Same formula as Shape A (§4) |
| "Low float" | Yahoo `floatShares` ≤ 10,000,000 shares | Number unstated in the P1 passage; his own P2 number (<10M) used for both. Proxy: shares outstanding if floatShares missing |
| "News catalyst" (both) | **Not measured** | DESIGN_BRIEF §3 excludes news from the loop. A null result therefore tests the 4-leg subset, not the full claim |
| "Top 3 leading percentage gainers" (P2) / "number one gainer" (D-03) | Rank of `c_t / c_{t−1} − 1` among the universe on day t | His scanner universe is pre-filtered; ours is the full 600-name universe — a stricter reading. Deviation fixed here |
| Intraday entry on 1-min signal | Signal at close t; entry at open of t+1 | Per brief §4 convention (no look-ahead) |
| Holds minutes–hours | Exit at close of t+1 (N = 1) | Closest daily-bar analog; N = 3, 5, 10 are pre-declared exploratory |

## 2. Hypotheses (pre-registered, each with a Holm slot)

Universe U: current S&P 600 constituents, daily bars 2000-01-01 → 2025-12-31
(IS: 2000–2015, OOS: 2016–2025). Detection at (ticker i, day t) when all of
the row's conditions hold on day t (AND-combined, per "all five pillars"):

**H1 — P1 filter set** (ledger D-01): `$2 ≤ c_t ≤ $20` AND `c_t/c_{t−1}−1 ≥ 0.30`
AND `v_t ≥ 5 × mean(v, prior 20)` AND `floatShares ≤ 10M`.

**H2 — P2 filter set** (ledger D-02): `$1 ≤ c_t ≤ $10` AND `c_t/c_{t−1}−1 ≥ 0.25`
AND `v_t ≥ 10 × mean(v, prior 20)` AND `floatShares ≤ 10M` AND daily %-gain
rank ≤ 3 in U.

**H3 — gainer-rank effect** (ledger D-03): forward return of the rank-1
cohort (top %-gainer of U on day t, unconditional of other filters) exceeds
that of the rank-2–10 cohort. Direction per claim: "the days I do the best
are when we have a stock that is super obvious."

Both parameter variants H1 and H2 are pre-registered *as stated by the
source*; the source is internally inconsistent (two different number sets),
so no data is used to choose between them — each earns its own Holm slot.

## 3. Measurement (per DESIGN_BRIEF §6)

- **Forward return:** `(c_{t+1} − o_{t+1}) / o_{t+1}` — enter at open of t+1,
  exit at close of t+1. (Adjusted prices; no look-ahead.)
- **Costs:** 0.15% round-trip deducted from every detection (brief §9 #4
  draft value — applies to all pre-registered tests).
- **Baselines:** (1) random entries — same number of detections, random
  (ticker, day) pairs from U, 1,000 bootstrap resamples → 95% CIs;
  (2) SPY buy-and-hold over matching windows; (3) same-ticker buy-and-hold
  (held for the same calendar span).
- **Metrics:** mean and median excess return vs each baseline, hit rate,
  max drawdown, all with bootstrap CIs (L-014: no point estimate without an
  interval). Per-decade breakdown (2000s/2010s/2020s) for non-stationarity.
- **Multiple testing:** Holm correction across H1–H3 at α = 0.05, on OOS
  only. IS is for observation only and yields no verdict.
- **Sensitivity (pre-declared, exploratory, no verdicts):** N = 3, 5, 10;
  high-based trigger (`h_t ≥ 1.30 × c_{t−1}`); $2–10 sub-range; one
  detection per ticker per 20-bar window.

## 4. Verdicts (pre-registered decision rules)

| Outcome | Rule (applied on OOS) |
|---|---|
| **Edge** | Holm-corrected mean excess vs same-ticker B&H excludes 0 (positive) AND vs random-entries excludes 0 |
| **No edge** | OOS point estimate ≤ 0, or CI includes 0 with ≥ 100 detections |
| **Inconclusive** | < 100 detections in OOS — reported, never spun |

Verdicts are written back into CLAIMS_LEDGER rows D-01/D-02/D-03 as the
audit trail. A verdict is a statement about the 4-leg computable subset on
S&P 600 daily bars, **not** a verdict on Ross Cameron's actual trading.

## 5. Data & bias handling (§7 checklist)

- **Source:** yfinance, adjusted closes; universe = S&P 600 membership
  snapshot **as of 2026-08-13** (Wikipedia S&P 600 list or IJR holdings —
  whichever is cleanest at Phase 1; the snapshot date is fixed, the list is
  never updated). Float: Yahoo `floatShares` (falls back to shares
  outstanding — documented per-ticker).
- **Survivorship:** current constituents only (§5(b)); bias inflates
  returns, so a **null is strengthened**; any positive result gets re-checked
  against historical constituents before trust.
- **Look-ahead:** signal uses data ≤ t only; entry open t+1.
- **Data quality:** flag delistings, gaps, and adjusted-price discontinuities
  in the Phase-1 pipeline report.
- **Detection clustering:** a momentum run can yield many detections on one
  ticker; they are not independent. All-detections is the primary analysis;
  per-window capping is the pre-declared sensitivity above. Bootstrap
  intervals treat detections as resampled events.

## 6. Scope note — §3 exception (needs sign-off)

The float leg requires Yahoo fundamentals (`floatShares`), which DESIGN_BRIEF
§3 ("no fundamentals in the loop") nominally excludes. This pre-registration
proposes a narrow exception: **static float as a screening filter input,
retrieved once at universe snapshot** — not a per-day fundamental feature
and not part of shape detection. All other §3 exclusions (news, sentiment,
LLM, intraday) stand.

**✅ Approved 2026-08-13** — DESIGN_BRIEF §9 row 7 settled as option (a).
The float values frozen with the 2026-08-13 universe snapshot (603/603
coverage) are the only float data this campaign may use.

## 7. Freeze

- Frozen 2026-08-13, before any data pipeline work (Phase 1).
- Amendments require a new pre-registration and a fresh window. Exploratory
  results may be reported but never drive a verdict or a claim.
- Registered against: PREREGISTRATION #1 · hypotheses H1–H3 · universe S&P
  600 · N = 1 primary.

## 8. Campaign outcome (recorded after measurement — parameters unchanged)

Measured 2026-08-13 with the frozen parameters above. **H1/H2: INCONCLUSIVE
by the ≥100-detection count floor** — the AND-combined screens fired 7/6
times in 26 years across 599 tickers, all in IS (2000–2010), zero OOS
detections; no verdict possible, reported never spun. **H3: NO EDGE on OOS
2016–2025** — n=2,513 at N=1, mean −0.19%, excess vs random −0.06pp
(p=0.72), vs same-ticker −0.07pp (p=0.64); the day-paired rank-1-vs-rank-2–10
claim test is precisely null (diff +0.00pp, p=0.986, 95% CI ±0.25pp).
Verdicts written to CLAIMS_LEDGER §D.5; full report in
`data/cache/pillar_measure_report.md` (+ `pillar_measure_results.json`).

Exploratory sensitivities (N=3/5/10, high trigger, $2–10 sub-range, 20-bar
dedupe) are reported there with no verdicts; the pre-declared N-grid rises
monotonically with horizon (−0.19/−0.03/+0.28/+1.63% after cost at
N=1/3/5/10), consistent with the era's 2-week momentum drift (random OOS
windows at N=10: +0.64% raw; SPY +0.58%) — a horizon-based follow-up would
require a new pre-registration and a fresh window. Project consequence per
DESIGN_BRIEF §1: the second completed campaign is also a rigorous null at
the frozen horizon; Phase 5 remains not triggered.

---

# Pre-registration #2 — shape detectors A/B/C

**Frozen 2026-08-13** (Mr. Mike's sign-off: N=10 primary; draft parameters
locked as-is; raw adjusted bars kept — no clamping). Frozen before any
Phase 3 measurement.

## 1. Translation table (as-stated → as-measured)

The reference method pairs the Section D pillars (selection) with chart
shapes (entry timing). This pre-registration measures the shapes
**unconditionally on the whole universe** — the question "does the shape
itself predict forward returns?" comes first; the combined pillars × shapes
system is a later pre-registration with its own Holm slots.

| As-stated (reference course) | As-measured |
|---|---|
| Intraday pattern scan | Daily bars; multi-day shapes A/B/C (brief §4) |
| Manual chart reading | Detector code as spec: `tools/detectors.py` v1, manifest hash `e93ddf7a…` (locked with this pre-reg) |
| Entry on signal | Open of t+1 (no look-ahead) |
| Exit "on the trade working" | Time-based: close of t+N (N per §3) |
| — | Costs 0.15% round-trip deducted (brief §9#4, draft) |

## 2. Hypotheses and parameters (frozen)

Signal at bar t per §1 definitions; forward return measured
`(c_{t+N} − o_{t+1}) / o_{t+1}` minus costs, per detection.

- **A — consolidation breakout:** K closes ending t−1 span [lo, hi] with
  (hi−lo)/lo ≤ W, and c_t > hi, and v_t ≥ V × mean(v, prior 20).
  Draft: **K=10, W=0.05, V=2.0**
- **B — pullback to trend:** ≥T consecutive closes above the M-day SMA
  ending t−P−1; P closes (t−P..t−1) above the SMA with net decline
  (c_{t−1} < c_{t−P}); c_t above the previous K highs.
  Draft: **M=20, T=5, P=3, K=20**
- **C — double bottom:** swing lows L1 (b1), L2 (b2) — center-window minima
  over 2S+1 bars — with b2−b1 ≥ D, |L1−L2|/L1 ≤ X, peak P = max high
  between them, P > both lows; signal = first close > P at t ≥ b2+S
  (L2 confirmed — no look-ahead), one signal per pattern.
  Draft: **S=5, D=5, X=0.03**

Operationalization judgment calls are documented in `tools/detectors.py`
docstring and this section; they are part of the frozen spec.

## 3. Exit horizon N (frozen)

Primary N = **10** (brief §9#3 resolved). N ∈ {5, 20} are pre-declared
exploratory sensitivities only — no verdicts, no Holm slots.

## 4. OHLC artifact handling (frozen)

Phase 1 QA documented Yahoo adjusted-OHLC inconsistencies (High < Open/Close)
on isolated bars in 306 tickers (data/README.md artifact 2). **Decision:
keep raw adjusted bars as-is.** The detector remains a pure function of the
frozen raw series; B's new-high feature is conservatively biased (a
distorted-low High suppresses signals, never invents them); C's peak can be
distorted on isolated bars — documented, not corrected. No clamping.

## 5. Measurement protocol (identical to pre-reg #1)

- Baselines: random entries (bootstrap 1,000), SPY buy-and-hold over
  matching windows, same-ticker buy-and-hold. Metrics with bootstrap CIs.
- Walk-forward: IS 2000–2015 (parameter selection only), OOS 2016–2025
  (evaluation; verdicts from OOS).
- Multiple testing: **one Holm slot per shape (A/B/C)** at α = 0.05.
  Parameter grid searches, N variants, and pillars×shapes are exploratory.
- Verdicts: **Edge** — Holm-corrected mean excess over both same-ticker B&H
  and random entries, OOS, with ≥100 detections; **No edge** — ≤0 or CI
  includes 0 with ≥100 detections; **Inconclusive** — <100 detections.
- Data: Phase 1 dataset as frozen (universe snapshot, bars, artifacts
  documented). Per-decade breakdown reported.

## 6. Freeze

- Frozen 2026-08-13, before any Phase 3 measurement.
- Parameters §2, horizon §3, OHLC handling §4, and the detector manifest
  hash (`e93ddf7a…`, recorded in `data/cache/detections_v1.manifest.json`)
  are immutable for this campaign. Any change = new pre-registration +
  fresh window.
- Registered against: PREREGISTRATION #2 · shapes A/B/C · universe S&P 600 ·
  N = 10 primary.

## 7. Campaign outcome (recorded after measurement — parameters unchanged)

Measured 2026-08-13 with the frozen parameters above. **All three shapes:
NO EDGE on OOS 2016–2025** (Shape B significantly *below* its baselines).
Verdicts written to CLAIMS_LEDGER §B.5; full report in
`data/cache/measure_report.md`. Project consequence per DESIGN_BRIEF §1: a
rigorous null — Phase 5 is not triggered. Re-testing with different
parameters requires a new pre-registration and a fresh window.

---

# Pre-registration #3 — the two-filter veto (ledger rows E-01/E-04)

**Frozen:** 2026-08-14 · **Status:** FROZEN — no parameter may be changed
after this date. Any change is a new hypothesis requiring a fresh
pre-registration and a fresh test window (DESIGN_BRIEF.md §4, §6).

Source claim: Ross Cameron, "The Ultimate Day Trading Guide", [02:01–04:57]
and [3:02:18–3:04:30]; ledger rows **E-01, E-04**. Before entry, two filters
veto the trade: **MACD** ("blue line crossed negative = no"; "MACD negative
= no") and **volume** ("high-volume selling on red candles = no"); "if just
one of them says no, I don't take the trade" (E-01); "if it's not a hard
yes, then it's a no" (E-04). The testable question (ledger annotation on
E-01): *does conditioning the entry on (MACD non-negative AND no high-volume
red bar) improve forward returns vs the raw pattern?* — and, per
DESIGN_BRIEF §1, does the vetoed subset clear the calibrated bar.

## 1. Translation table — as stated → as measured

| Claim leg (as stated) | As measured (daily bars) | Deviation / note |
|---|---|---|
| Veto applied "before entry" | Conditions the *signal* at day t; entry remains open of t+1 (no look-ahead) | Same entry convention as all campaigns |
| "MACD negative = no" / "blue line crossed negative = no" (E-01 vs E-04 wording) | Primary: MACD(12,26) **line < 0 at t** (state). Sensitivity: **zero-crossing** (line<sub>t</sub> < 0 AND line<sub>t−1</sub> ≥ 0) — the stricter reading of "crossed" | The source itself mixes the two wordings (E-01 crossing, E-04 state); state is primary (more events, matches the distilled quiz rule), crossing is pre-declared |
| "Blue line" | MACD line (12−26 EMA difference), standard (12,26,9), on adjusted closes, `ewm(adjust=False)` | D-06 says he uses MACD only on 1-min charts — the daily MACD is a documented adaptation of the *rule*; the veto as stated (E-01/E-04) is time-frame-agnostic |
| "High-volume selling on red candles = no" | Red candle: `c_t < o_t`. High volume: `v_t ≥ V × mean(v, prior 20)`, primary **V = 2.0**; sensitivities V = 1.5, 3.0 | Number unstated in the corpus; V=2.0 reused from the shape campaign (frozen, not tuned). "Selling" is operationalized as the red candle itself — OHLCV cannot separate selling from buying pressure beyond candle color |
| "If just one of them says no" | Veto kill = MACD-negative **OR** high-volume-red; veto pass = both legs clear | The AND-combined requirement to *pass* |
| The raw pattern (what the veto conditions) | Shape detections A/B/C from pre-reg #2 — the frozen entry-setup analogs on daily bars; one hypothesis per shape | The veto is an entry rule; shapes are the entry patterns. No new detector parameters — the veto only *filters* the frozen detections |
| MACD warm-up | Detections at bar index < 60 from series start are excluded from the campaign (counted) | EMA seed weight is non-negligible early in a series; with the 20-bar vol lookback and K=10 shape lookbacks, expected count ≈ 0 |

## 2. Hypotheses (pre-registered, each with Holm slots)

Base: detections_v1.csv (pre-reg #2, frozen manifest e93ddf7a…), N=10
primary, costs and walk-forward split identical to #1/#2.

**H-VA / H-VB / H-VC** — for shape S ∈ {A, B, C}, the veto-passing subset of
S's OOS detections has higher forward returns than the full S detection set
(the conditioning claim as stated). Each shape earns its own Holm slot.

**Two pre-registered verdict families** (each Holm-corrected across A/B/C
at α = 0.05, OOS only):
- **Family 1 — conditioning** (the claim as stated): mean(veto-pass) −
  mean(full set) > 0, two-sample bootstrap.
- **Family 2 — absolute bar** (brief §1: a rule must beat buy-and-hold after
  costs): veto-pass subset vs random-entries AND same-ticker, era-matched —
  the same verdict machinery as campaigns #1/#2.

Both families are registered before measurement; a verdict in one does not
borrow from the other.

## 3. Measurement (identical protocol to #1/#2 where shared)

- Forward return `(c_{t+N} − o_{t+1}) / o_{t+1}` − 0.15% COST, N = 10
  primary (frozen with pre-reg #2; the veto does not change the horizon).
  N = 5/20 are pre-declared exploratory.
- Conditioning test: two-sample bootstrap (B = 1,000, seed 20260813),
  mean(selected) − mean(full), 95% percentile CI, two-sided p.
- Absolute test: `bootstrap_excess` vs the three era-matched baselines
  (random entries −COST, same-ticker −COST, SPY raw) — identical to #1/#2.
- Kill-rate table per shape (answers E-04's "filters killing setups vs
  setups working"): detections killed by the MACD leg alone, the volume leg
  alone, both, and passing — plus the mean return of the killed set.
- Metrics with bootstrap CIs (hit rate, Sharpe, maxDD) on the veto-passing
  subset, per shape.
- Warm-up guard: detections at bar index < 60 are excluded (counted).

## 4. Verdicts (pre-registered decision rules, applied on OOS)

| Outcome | Rule |
|---|---|
| **Edge** | Holm-corrected positive (CI-low > 0) AND ≥ 100 veto-passing OOS detections |
| **No edge** | Mean ≤ 0 or CI includes 0, with ≥ 100 veto-passing OOS detections |
| **Inconclusive** | < 100 veto-passing OOS detections — reported, never spun |

Applied identically to both families (the family-1 "effect" is the
conditioning excess; family-2 is the absolute excess).

## 5. Data & bias handling (§7 checklist)

- Inputs: detections_v1.csv (frozen, pre-reg #2), bars (frozen, Phase 1),
  universe snapshot (frozen 2026-08-13). No new data is fetched.
- MACD from adjusted closes per §1; EMA warm-up guard §1 (bar index ≥ 60).
- Look-ahead: all veto legs use data ≤ t only; entry open t+1.
- Multiple testing: two pre-registered families, Holm within each at α=0.05.
- The veto-passing subset is a strict subset of the frozen detections
  (asserted byte-for-byte in the measurement); the comparison is
  "what the veto selects" vs "the pattern un-vetoed".

## 6. Sensitivities (pre-declared, exploratory, NO verdicts)

- N = 5, 20 (same detections).
- MACD zero-crossing reading (line crossed < 0 at t).
- Volume leg V = 1.5 and 3.0.
- The veto applied to the H3 rank-1 cohort (pre-reg #1 detections, N=1) —
  exploratory check on the selection side of the claim.

## 7. Freeze

- Frozen 2026-08-14, before any measurement. Registered against:
  PREREGISTRATION #3 · shapes A/B/C with the two-filter veto · N = 10
  primary · two verdict families.
- Amendments require a new pre-registration and a fresh window. Exploratory
  results may be reported but never drive a verdict or a claim.

## 8. Campaign outcome (recorded after measurement — parameters unchanged)

Measured 2026-08-14 with the frozen parameters above. **All six verdicts:
NO EDGE** — the veto does not improve any pattern, in either verdict family
(A/B/C: F1-conditioning p = 0.354 / 0.988 / 0.798; F2-absolute vs random
p = 0.148 / 0.002 / 0.888 — Shape B's veto-passing subset is significantly
*below* random, p=0.002). On A and C the veto systematically cuts the
better trades (killed-set means +0.83% / +1.54% vs kept +0.21% / +0.46%);
on B it changes nothing (−0.01% both). The kill-rate decomposition answers
E-04's question: the veto is a **trade-count reducer (A −30%, B −3%,
C −15% of OOS trades), not an edge enhancer**. Verdicts written to
CLAIMS_LEDGER §E.5; full report in `data/cache/veto_measure_report.md`
(+ `veto_measure_results.json`).

Exploratory sensitivities (N=5/20, MACD zero-crossing reading, V=1.5/3.0,
veto on the H3 rank-1 cohort) are reported there with no verdicts — none
changes the conclusion. Project consequence per DESIGN_BRIEF §1: the third
completed campaign is again a rigorous null; Phase 5 remains not
triggered. Next candidate in the ledger priority order: E-03 (MACD-cross
breakout rejection).
