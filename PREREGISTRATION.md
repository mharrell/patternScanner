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

---

# Pre-registration #4 — momentum horizon follow-up (N=20 primary)

**Frozen:** 2026-08-14 · **Status:** FROZEN — no parameter may be changed
after this date. Any change is a new hypothesis requiring a fresh
pre-registration and a fresh test window (DESIGN_BRIEF.md §4, §6).

**Origin — a measurement-derived follow-up, not a direct corpus claim.** The
pre-declared exploratory N-grids of campaigns #1/#2 (pre-reg #1 §3, #2 §3)
showed the *same entry sets* earning more at longer holds on OOS 2016–2025:
H3 rank-1 −0.19% / −0.03% / +0.28% / **+1.63%** at N=1/3/5/10; Shape A
+0.40% (N=10) → **+0.95%** (N=20); Shape C +0.62% → **+1.39%**; Shape B flat
at ≈ 0. At N=10, H3's +1.63% exceeded its era-matched baselines (random
+0.64%, SPY +0.58%) by ~1pp. Exploratory results never drive a verdict —
this pre-registration promotes the horizon-momentum reading to a primary
claim, with fresh frozen parameters, measured on the same frozen
detections. It supersedes the "next = E-03" note in pre-reg #3 §8 (E-03's
crossing reading was already measured there as a sensitivity with no
signal; the reorder decision is Mr. Mike's 2026-08-14 campaign choice).

## 1. Translation — claim as motivated → as measured

| As motivated | As measured |
|---|---|
| "Winners keep winning; holding longer earns more" | Forward return of the same frozen entry set at N=20 primary: `(c_{t+20} − o_{t+1}) / o_{t+1} − 0.15%` cost |
| "The N-grid rise is real, not era drift" | Family 1 (absolute): N=20 excess vs era-matched baselines — random entries and same-ticker buy-and-hold (both pay cost; SPY raw, reported not gating) |
| "Longer holds compound the same trades" | Family 2 (continuation): paired N=20 vs N=5 on **identical entries**, paired bootstrap over entries |
| Entry sets | Shape A, Shape C, H3 rank-1 cohort (pre-reg #2 / #1 frozen detections) |

Shape B is **excluded from primary hypotheses by pre-registration** (not by
result): its exploratory record is flat at both measured horizons (−0.01% at
N=10 and N=20). It is measured as an exploratory row only, no verdict —
including it as a primary slot would be post-hoc hypothesis selection.

## 2. Hypotheses (two families, each Holm-corrected across its 3 slots at α=0.05, OOS only)

Family 1 — absolute at N=20 vs baselines (p_input = max(p_random, p_same)):

- **M-A20** — Shape A detections at N=20 beat era-matched baselines.
- **M-C20** — Shape C detections at N=20 beat era-matched baselines.
- **M-H20** — H3 rank-1 detections at N=20 beat era-matched baselines.

Family 2 — continuation (paired, identical entries):

- **M-Acont** — Shape A entries: mean(r20) − mean(r5) > 0.
- **M-Ccont** — Shape C entries: same.
- **M-Hcont** — H3 rank-1 entries: same.

## 3. Measurement (identical protocol to #1–3 where shared)

- Entry open t+1, exit close t+N; era by signal date; OOS 2016–2025 verdicts,
  IS record only; 0.15% round-trip on every strategy trade; baselines as in
  pre-reg #1 §3 (random / same-ticker pay cost, SPY raw); bootstrap B=1000,
  seed 20260813, two-sided p; Holm per family on OOS only.
- Family 2 paired diffs: per entry `d = r20 − r5` on entries valid at both
  horizons; bootstrap resamples the entry set; p = 2·min(Pr(d̄ ≤ 0), Pr(d̄ ≥ 0)).

## 4. Verdicts (pre-registered decision rules, applied on OOS)

| Outcome | Rule |
|---|---|
| **Edge** | Holm-corrected mean excess vs same-ticker B&H excludes 0 (positive) AND vs random-entries excludes 0 (Family 1); paired mean diff CI excludes 0 (positive) at Holm gate (Family 2) |
| **No edge** | OOS point estimate ≤ 0, or CI includes 0 with ≥ 100 detections |
| **Inconclusive** | < 100 detections in OOS — reported, never spun |

## 5. Data & bias handling (§7 checklist)

- **No new data:** frozen inputs only — `detections_v1.csv` (sha
  9b44f66160130c3a…), `pillar_detections_v1.csv` (d5f80746f14f53fd…),
  universe snapshot and bars exactly as cached. No fetch, no edits.
- **Overlapping-window dependence:** at N=20 consecutive detections on the
  same ticker share exit bars; the bootstrap resamples entries and preserves
  the dependence structure, but effective independence < nominal. Documented,
  not adjusted — same engine as #1–3 (Phase-3 engine c7421fbf… frozen, never
  modified).
- **Detection clustering:** momentum runs cluster detections on one ticker;
  addressed by the dedupe-20 sensitivity (no verdicts).
- **Look-ahead:** unchanged (signal ≤ t, entry open t+1). Survivorship: same
  documented caveat — a null is strengthened, a positive requires historical
  constituents.

## 6. Sensitivities (pre-declared, exploratory, NO verdicts)

- N=40 absolute and continuation (same entries).
- Dedupe-20 (one detection per ticker per 20-bar window) at N=20.
- Per-decade OOS breakdown (2016–2019 / 2020–2025).
- Shape B at N=20 (absolute only, no verdict).
- Full per-entry metric tables (hit rate, Sharpe, maxDD) at N=20.

## 7. Freeze

- Frozen 2026-08-14, before any measurement. Registered against:
  PREREGISTRATION #4 · shapes A/C + H3 rank-1 · N=20 primary · two verdict
  families · baselines and verdict rules identical to #1–3.
- Amendments require a new pre-registration and a fresh window. Exploratory
  results may be reported but never drive a verdict or a claim.

## 8. Campaign outcome (recorded after measurement — parameters unchanged)

Measured 2026-08-14 with the frozen parameters above. **Family 1 (absolute
at N=20 vs era-matched baselines): NO EDGE × 3** — A n=5,646 +0.95%
(p_input 0.61), C n=364 +1.39% (p_input 0.88), H3 n=2,494 +3.19% (p_input
0.47, Holm gate 0.0167). The H3 row is the project's most interesting
near-miss: **significantly above random entries (+2.00pp, p=0.004) and SPY
(+2.00pp, p=0.004) but indistinguishable from same-ticker buy-and-hold
(+0.66pp, p=0.47)** — the selection adds nothing over owning the ticker.

**Family 2 (continuation, paired N=20 vs N=5 on identical entries): EDGE ×
3 — the project's first EDGE verdicts**, recorded exactly per the frozen
rule: A diff +1.03pp (CI +0.66..+1.61, p<0.001), C +1.15pp (CI +0.10..+2.17,
p=0.038), H3 +2.91pp (CI +1.78..+4.31, p<0.001) — after these signals the
entry names kept moving up from bar 5 to bar 20, significantly, on all
three entry sets (the paired diff is exactly the 15-bar close-to-close
return after bar 5; cost cancels in the difference).

How the two families read together: F1's same-ticker row explains F2 — the
continuation gain is the era's small-cap 2–4-week drift available to any
holder of the entry names, not edge from the patterns' selection, which F1
shows is null (selection vs same-ticker: all three CIs include 0). Per
DESIGN_BRIEF §1 the pattern-vs-chance trigger test is Family 1 and it is
null → **Phase 5 remains not triggered**. The F2 EDGE verdicts stand as
recorded; the interpretation is not the verdict. Verdicts written to
CLAIMS_LEDGER §D.6; full report in `data/cache/momentum_measure_report.md`
(+ `momentum_measure_results.json`).

Exploratory sensitivities (N=40, dedupe-20, per-decade, Shape B) are
reported there with no verdicts — all consistent with the primary result
(N=40 continuation H3 +7.11pp; dedupe-20 H3 +2.91%; H3 per-decade +1.30% →
+4.47%; Shape B flat −0.01%, the pre-registered exclusion validated).
Input fingerprints: detections 9b44f66160130c3a…, pillar detections
d5f80746f14f53fd…, engine c7421fbf… imported unchanged; outputs
deterministic (results d4b91fd5…, report 838bf373…, verified byte-identical
across two runs and independently recomputed row-by-row from bars).

---

# Pre-registration #5 — per-decade drift decomposition (sub-era claim)

**Frozen:** 2026-08-14 · **Status:** FROZEN — no parameter may be changed
after this date. Any change is a new hypothesis requiring a fresh
pre-registration and a fresh test window (DESIGN_BRIEF.md §4, §6).

**Origin — follow-up of pre-reg #4, measurement-derived.** Pre-reg #4's F2
EDGE (continuation, all three entry sets) and H3's F1 near-miss (+2.00pp vs
random at N=20) raise the question that decides their interpretation: is the
drift **uniform across the OOS era, or concentrated in 2020–2025**? Raw N=20
means from the pre-reg #4 sensitivity rows suggest later-era strengthening
(H3 +1.30% → +4.47%; C +0.66% → +2.11%; A +0.87% → +1.06%). If the *excess
over era-matched baselines* is late-era only, the effect is fragile beta
going forward (2020–21 small-cap mania era) — a red flag against Phase 5.
If it holds in both sub-eras, the drift is more robust. Exploratory
per-decade rows earn no verdicts — this pre-registration promotes the
sub-era claims to primary hypotheses with fresh frozen parameters, measured
on the same frozen detections and bars.

## 1. Translation — claim as motivated → as measured

| As motivated | As measured |
|---|---|
| "The drift strengthened in the recent half of the OOS era" | Family 1: mean N=20 excess vs **within-sub-era** era-matched baselines in 2020–2025 **minus** in 2016–2019 > 0, two-sample bootstrap |
| "The late-era drift clears the absolute bar on its own" | Family 2: within 2020–2025 alone, N=20 excess vs within-sub-era baselines > 0 |
| "Era-matched" at sub-era granularity | Baseline windows drawn only from bars whose **start date** falls in the same sub-era (same window formula as #1–4; exit may cross the sub-era boundary, era by signal date as always) |
| Entry sets | Shape A, Shape C, H3 rank-1 — the pre-reg #4 sets, same frozen detections |

Sub-eras: 2016-01-01 → 2020-01-01 ("early") and 2020-01-01 → 2026-01-01
("late") — the pre-reg #4 per-decade sensitivity boundaries, fixed here.

## 2. Hypotheses (two families, each Holm-corrected across A/C/H3 at α=0.05, OOS only)

Family 1 — sub-era excess difference (claim: late > early):

- **S-A**: Shape A: excess_late − excess_early > 0.
- **S-C**: Shape C: same.
- **S-H**: H3 rank-1: same.

Family 2 — late-era absolute (claim: clears the bar within its own era):

- **L-A / L-C / L-H**: N=20 excess vs within-sub-era baselines in 2020–2025
  only > 0.

p_input = max(p_random, p_same) in both families, as in #1–4.

## 3. Measurement (identical protocol to #1–4 where shared)

- Entry open t+1, exit close t+N=20; −0.15% cost; era by signal date;
  bootstrap B=1000, seed 20260813, two-sided p; Holm per family, OOS only.
- Family 1 two-sample bootstrap: per draw, resample entries within each
  sub-era and baseline windows within that sub-era; excess_late_b −
  excess_early_b; p = 2·min(Pr(d ≤ 0), Pr(d ≥ 0)); CI from the draw
  distribution. Point estimate = excess_late − excess_early (each the
  simple mean minus the baseline pool mean).
- Family 2: identical verdict-block structure to #1–4, restricted to late
  sub-era entries and late sub-era baseline pools.
- Count floor: ≥100 OOS detections per sub-era per slot (early C n=182,
  early H3 n=1,006, early A n=3,243 — all clear; counts from pre-reg #4
  sensitivities, fixed inputs, not re-measured).

## 4. Verdicts (pre-registered decision rules, applied on OOS)

| Outcome | Rule |
|---|---|
| **Edge** | Holm-rejected AND CI excludes 0 in the claim's direction (Family 1: later-excess CI-lo > 0; Family 2: excess CI-lo > 0) |
| **No edge** | OOS point estimate ≤ 0, or CI includes 0, with ≥ 100 detections |
| **Inconclusive** | < 100 detections in OOS — reported, never spun |

## 5. Data & bias handling (§7 checklist)

- **No new data:** same frozen inputs as #4 — detections_v1.csv
  (9b44f661…), pillar_detections_v1.csv (d5f80746…), universe and bars as
  cached. No fetch, no edits.
- **Overlapping windows and clustering:** as documented in #4 §5 — the
  bootstrap preserves dependence; effective independence < nominal;
  documented, not adjusted. Dedupe-20 is a sensitivity, no verdict.
- **Sub-era pool sizes:** late-era pools are smaller than full-OOS pools
  (≈ 60% of bars); the two-sample test resamples within-era, so era
  balance is by construction.
- **Look-ahead / survivorship:** unchanged from #1–4.

## 6. Sensitivities (pre-declared, exploratory, NO verdicts)

- Sub-era continuation diffs (d̄_late − d̄_early, paired N=20 vs N=5).
- Early-era (2016–2019) absolute at N=20 vs within-sub-era baselines.
- N=40 within sub-eras (absolute means).
- Per-year N=20 means (2016…2025) per entry set — where the drift lives.
- Dedupe-20 per sub-era.

## 7. Freeze

- Frozen 2026-08-14, before any measurement. Registered against:
  PREREGISTRATION #5 · shapes A/C + H3 · N=20 · two sub-era verdict
  families · identical engine and baselines to #1–4 (engine c7421fbf…,
  never modified).
- Amendments require a new pre-registration and a fresh window. Exploratory
  results may be reported but never drive a verdict or a claim.

## 8. Campaign outcome (recorded after measurement — parameters unchanged)

Measured 2026-08-14 with the frozen parameters above. **Both verdict
families: NO EDGE × 3.**

**Family 1 (sub-era excess difference, late minus early, N=20):** A +0.47pp
(p=0.51), C +1.79pp (p=0.30), H3 +3.48pp vs random (**p=0.008**, CI
+0.80..+6.22pp) but +2.40pp vs same-ticker (p=0.138) — p_input 0.138 fails
Holm gate 0.0167.

**Family 2 (late-era absolute, within-sub-era baselines):** A n=2,403
+1.06% (p_input 0.97), C n=182 +2.11% (p_input 0.44), H3 n=1,488 +4.47% —
significantly above late-era random (+3.38pp, p=0.002, CI +1.34..+5.85pp)
and SPY (p<0.001), indistinguishable from same-ticker buy-and-hold
(+1.47pp, p=0.238) — p_input 0.238 fails Holm gate 0.0167.

Answer to the campaign's question: the late-era strengthening is real vs
random entries (F1 p=0.008; F2 p=0.002; continuation H3 late−early
+2.81pp, p=0.020; early-era H3 excess ≈ 0) — the drift is genuinely
late-era-dominated — but it never clears the same-ticker control in either
family. Per the pre-registered rule and consistent with pre-reg #4: the
drift is late-era beta, not selection edge; **Phase 5 remains not
triggered**, now with a dedicated decomposition behind it. The late-era
concentration is not a single mania episode (H3 per-year N=20: +9.1% 2020,
+6.2% 2021, +0.1% 2022, +6.1% 2023, +4.6% 2024, +0.4% 2025). Verdicts
written to CLAIMS_LEDGER §D.7; full report in
`data/cache/decade_measure_report.md` (+ `decade_measure_results.json`).

Sensitivities (early-era absolute, N=40 by sub-era, per-year means,
dedupe-20 by sub-era) are reported there with no verdicts — all consistent
with the primary result. Input fingerprints: detections 9b44f661…, pillar
detections d5f80746…, engine c7421fbf… imported unchanged; outputs
deterministic (results 5b7f7317…, report ade0fd3c…, verified
byte-identical across two runs and independently recomputed row-by-row
from bars).

---

# Pre-registration #6 — E-03: MACD-cross breakout rejection

**Frozen:** 2026-08-14 · **Status:** FROZEN — no parameter may be changed
after this date. Any change is a new hypothesis requiring a fresh
pre-registration and a fresh test window (DESIGN_BRIEF.md §4, §6).

Source claim: Ross Cameron, "The Ultimate Day Trading Guide",
[1:21:54–1:23:04]; ledger row **E-03**. As stated: "when the MACD actually
crosses... more times than not, any attempt to break out will reject and the
price will end up selling off" — learned in the 2022 bear market, "very
consistent especially during the bear market." Context (same segment): a
stock with a strong move whose moving averages converge into a tight range;
the cross "signifies the end of the front side of this move"; breakout
attempts after it fail. At [1:34:29–1:34:43] he lists **"MACD crossover"**
as an exit indicator ("the reversal is in a way already begun"). The ledger
annotation fixes the open design problem in advance: **pre-register the
crossing definition and the regime variable explicitly, so neither can be
added post-hoc.**

## 1. Translation table — as stated → as measured

| Claim leg (as stated) | As measured (daily bars) | Deviation / note |
|---|---|---|
| "The MACD actually crosses" | **Bearish signal-line crossover**: hist = MACD line − signal line; cross at bar j = hist<sub>j</sub> < 0 AND hist<sub>j−1</sub> ≥ 0. MACD(12,26,9), `ewm(adjust=False)`, adjusted closes — identical MACD machinery to pre-reg #3 | "MACD crossover" is conventionally the signal-line cross (his listed exit indicator, [1:34:33]); the *zero-line* cross reading was already measured as a pre-reg #3 sensitivity with no signal (§E.5) — the signal-line reading is what E-03 adds |
| "When... crosses" (event, not state) | Cross within **L = 20 bars before** the signal bar: crossed(t) = ∃ k ∈ [1, 20]: cross at t−k | The described sequence is cross → sideways compression → breakout attempt fails; the cross strictly precedes the signal. L=5 is a pre-declared sensitivity |
| "Any attempt to break out" | The frozen shape detections A/B/C from pre-reg #2 (consolidation breakout / pullback-to-new-high / double-bottom break) — one hypothesis per shape | The shapes ARE the project's breakout-attempt analogs; no new detector parameters |
| "Will reject and the price will end up selling off" | Crossed subset mean forward return **below** the not-crossed subset (F1/F2) and **below** the calibrated baselines (F3) | The claim is negative — verdicts are defined in the claim's direction (fade), see §4 |
| "Very consistent especially during the bear market" | **Regime variable (pre-registered): bear = SPY close < SPY 200-day simple moving average at signal date t.** SPY from the frozen Phase-1 cache; SMA over the prior 200 closes including t | The market proxy is SPY (the baseline benchmark throughout this project). Where the SMA is undefined (SPY history < 200 bars, all pre-2000-11 — IS only), the detection is excluded from the F2 regime family and counted |
| MACD warm-up | Detections at bar index < 60 from series start are excluded from the campaign (counted), as in pre-reg #3 | EMA seed weight is non-negligible early in a series |

## 2. Hypotheses (three verdict families, each Holm-corrected across A/B/C at α=0.05, OOS only)

Base: detections_v1.csv (pre-reg #2, frozen manifest e93ddf7a…), N=10
primary, costs and walk-forward split identical to #1–#5.

- **Family 1 — cross conditioning, all OOS** (the claim without regime):
  for each shape S, mean(S-crossed) − mean(S-not-crossed) < 0 — the claim
  predicts crossed breakouts underperform their same-shape control.
- **Family 2 — cross conditioning, bear-market OOS days only** (the
  emphasized regime): same comparison restricted to detections whose signal
  date t has SPY < its 200-day SMA. Within-regime control by construction —
  the cross must add something beyond the regime itself.
- **Family 3 — avoidance bar** (the "reject and sell off" reading vs
  chance): the crossed subset's N=10 excess vs era-matched random-entries
  AND same-ticker buy-and-hold is significantly **below** 0 — the cross
  identifies breakouts worth avoiding (trades that underperform both chance
  and just holding the ticker). p_input = max(p_random, p_same), as in
  #1–#5.

A verdict in one family does not borrow from another. Bullish crosses and
the zero-line cross are pre-declared sensitivities (§6), never verdict
slots.

## 3. Measurement (identical protocol to #1–5 where shared)

- Forward return `(c_{t+N} − o_{t+1}) / o_{t+1}` − 0.15% COST, N = 10
  primary. N = 5/20 pre-declared exploratory.
- Conditioning tests (F1/F2): two-sample bootstrap (B = 1,000, seed
  20260813), mean(crossed) − mean(not-crossed), 95% percentile CI,
  two-sided p — the veto campaign's `two_sample_excess` machinery.
- Absolute test (F3): `bootstrap_excess` vs the three era-matched baselines
  (random −COST, same-ticker −COST, SPY raw) — identical to #1–5.
- Crossed/not-crossed is a **partition** of each shape's OOS detections
  (no overlap — unlike the veto's subset-vs-full comparison); counts are
  asserted in the measurement.
- Warm-up guard: detections at bar index < 60 excluded (counted).
- Metrics with bootstrap CIs (hit rate, Sharpe, maxDD) on the crossed
  subset, per shape. The hit rate answers "more times than not" directly;
  it is reported, not a verdict.
- IS record only, no verdicts — as always.

## 4. Verdicts (pre-registered decision rules, applied on OOS)

The claim is negative, so the Edge vocabulary is applied in the claim's
direction:

| Outcome | Rule |
|---|---|
| **Fade edge (claim supported)** | Holm-rejected AND the excess CI **upper** bound < 0 (F1/F2: conditioning excess; F3: excess vs random AND same-ticker, p_input = max(p_random, p_same)) — the crossed breakouts underperform their control/baselines, significantly, at the Holm gate |
| **No edge** | CI includes 0, or point estimate ≥ 0, with ≥ 100 crossed OOS detections |
| **Inconclusive** | < 100 crossed OOS detections (F2: < 100 crossed on bear days) — reported, never spun |

Note the sign flip vs campaigns #1–5: there the excess CI-low > 0 was
required; here the claim predicts the crossed set *loses*, so the CI-high
< 0 is required.

## 5. Data & bias handling (§7 checklist)

- **No new data:** frozen inputs only — detections_v1.csv (sha
  9b44f66160130c3a…), bars and universe snapshot as cached, SPY bars from
  the same frozen cache (SPY is also the baseline benchmark). No fetch, no
  edits.
- **Look-ahead:** the cross window, MACD, and SMA all use data ≤ t only;
  entry remains open of t+1.
- **Multiple testing:** three pre-registered families, Holm within each at
  α=0.05 on OOS only. The crossing reading, window, and regime variable are
  fixed here, before measurement — no post-hoc fitting.
- **Overlapping windows and clustering:** as documented in #4 §5 — bootstrap
  preserves dependence; effective independence < nominal; documented, not
  adjusted.
- **Scope note (carried from pre-reg #3):** the source uses MACD on 1-min
  charts; the daily-bar MACD is a documented adaptation of the *rule* as
  stated (time-frame-agnostic). These are verdicts on the mechanism, not on
  his intraday practice.
- **Survivorship / era-matching:** unchanged from #1–5.

## 6. Sensitivities (pre-declared, exploratory, NO verdicts)

- L = 5 (tight window: cross within the last week before the signal).
- k ∈ [0, 20] (cross on or before the signal bar — the cross-day reading).
- Zero-line cross reading (line<sub>t</sub> < 0 AND line<sub>t−1</sub> ≥ 0
  within the window) — already measured with no signal in pre-reg #3;
  recomputed here on the same frozen data for the record.
- Bullish signal-line cross (hist crosses **up** within the window) — the
  opposite-direction cross, exploratory.
- Non-bear regime conditioning (F1 within non-bear OOS days).
- Crossed subset vs baselines within bear days only (F3's regime form).
- N = 5, 20 (same detections/legs); per-year OOS means of the crossed
  subset.

## 7. Freeze

- Frozen 2026-08-14, before any measurement. Registered against:
  PREREGISTRATION #6 · shapes A/B/C with the bearish signal-line MACD cross
  (L=20) · regime SPY < SMA200 · N = 10 primary · three verdict families ·
  identical engine and baselines to #1–5 (engine c7421fbf…, never
  modified).
- Amendments require a new pre-registration and a fresh window. Exploratory
  results may be reported but never drive a verdict or a claim.

## 8. Campaign outcome (recorded after measurement — parameters unchanged)

Measured 2026-08-14 with the frozen parameters above. **FADE EDGE × 2 (both
Shape B), NO EDGE × 6, INCONCLUSIVE × 1** — the project's first verdicts in
a claim's favor, and they land exactly where the claim pointed.

**Family 1 (cross conditioning, all OOS): NO EDGE × 3** — A: crossed n=3,477
mean +0.21% vs not-crossed +0.70% (excess −0.48pp, p=0.254); B: n=2,930,
−0.04% vs +0.00% (p=0.810); C: n=204, +1.04% vs −0.04% (**+1.07pp — the
wrong direction**, p=0.230). Unconditioned, the cross does nothing.

**Family 2 (bear-market days only — the claim's emphasized regime):
FADE EDGE (B), NO EDGE (A), INCONCLUSIVE (C)** — **B: crossed n=230, mean
−0.95% vs not-crossed +0.70% — excess −1.62pp (95% CI −2.78..−0.46pp,
p=0.012, Holm-rejected at gate 0.0167)**. In bear markets, pullback-to-
new-high breakouts within 20 bars after a bearish MACD cross LOSE ~1% on
average while their not-crossed counterparts gain +0.70%. A: n=170, −0.18%
vs +0.42% (p=0.456); C: n=13 — INCONCLUSIVE by count floor, reported
never spun.

**Family 3 (avoidance bar): FADE EDGE (B), NO EDGE × 2** — **B: crossed
n=2,930, mean −0.04%, excess vs random −0.53pp (CI −1.00..−0.10pp,
p=0.014) and vs same-ticker −0.57pp (CI −1.02..−0.14pp, p=0.008) — p_input
0.014 vs Holm gate 0.0167, a narrow pass, noted honestly**; vs SPY −0.63pp
(p<0.001). The crossed-B breakouts significantly underperform chance and
just holding the ticker over all OOS. A: p=0.184; C: p=0.470.

Answer to the campaign's question: **the MACD-cross breakout-rejection
claim is supported in its emphasized regime for its most faithful shape** —
Shape B's structure (strong move → compression → cross → new-high attempt)
is the described scenario, and B is the only shape whose crossed breakouts
underperform — in bear days (F2, p=0.012) and vs chance over all OOS (F3,
p_input 0.014). The unconditional form (F1) is null for all three shapes;
A and C show nothing; the effect concentrates exactly in the year he names
(per-year crossed-subset means: 2022 −2.01%, the strongest negative year).

**Interpretation (recorded, not the verdict):** this is a **fade signal** —
the cross identifies B-breakouts worth *avoiding*; it does not make any
pattern profitable. The trigger test for Phase 5 remains the positive-edge
bar, untouched and untriggered. The zero-line reading (pre-reg #3
sensitivity) fired **0 of 31,226 detections** on the signal bar — the at-t
reading is structurally impossible on these detectors (breakout days are
up-days; the MACD line crosses down only after down-days), which is why
the windowed signal-line reading is the operative one. Note on
implementation: F3's same-ticker baseline uses the shape's own ticker
distribution per the #1–5 protocol (an earlier pass used the combined
crossed-set distribution inherited from the veto template; corrected
before any verdict was written back; verdicts unchanged, B's F3 margin
widened from p=0.016 to 0.014). Verdicts written to CLAIMS_LEDGER §E.6;
full report in `data/cache/e03_measure_report.md`
(+ `e03_measure_results.json`).

Sensitivities (L=5, k∈[0,20], zero-line at-t and within-window, bullish
cross, non-bear F1, bear-only F3, N=5/20, per-year) are reported in the
report with no verdicts — consistent with the primary result (bear-days
F3 regime form: B n=230 −0.95% vs random −1.45pp p=0.074, a near-miss on
a sensitivity; non-bear F1 for B flips to +0.18pp p=0.342 — the effect is
bear-market-specific). Input fingerprints: detections 9b44f661…, e03 file
5ac5a3a1…, e03 code 305e22a2…, measure code 12d6bb45…, engine c7421fbf…
imported unchanged; outputs deterministic (results 1d3feec5…, report
17ac9d73…, verified byte-identical across two runs and independently
recomputed row-by-row from bars).

---

# Pre-registration #7 — "80% chance of this working" (ledger row E-02)

Source: transcripts/ultimate-guide/oxob0x0Xz7s.md [04:29–05:54]. The ledger
row cites [02:01–04:57]; the setup language ("the MACD is positive... the
entry is right here as that first candle makes a new high versus the high
of the last one") is at [04:29–04:57], and the exact "80% chance of this
working" is at [05:54]. FROZEN 2026-08-14 before any measurement.

## 1. Translation table — as stated → as measured

As stated: "we've got high volume and the volume is on green candles, the
MACD is positive... we had light volume selling, the MACD was positive and
the entry is right here as that first candle makes a new high versus the
high of the last one — that's the setup I'm going to teach you... where we
feel we've got an **80% chance of this working**." Qualified immediately
after: "there's no such thing as a strategy that works 100% of the time
but if you have a strategy that over the course of 100 trades is giving
you profit 60% of the time, 70% of the time, that can be enough to be a
very profitable trader."

| As stated | As measured |
|---|---|
| "The setup": MACD positive, volume on green candles (no high-volume selling on red), first candle makes a new high vs the prior high | The **veto-pass subset** of the frozen shape detections (pre-reg #3: MACD line ≥ 0 AND no high-volume red candle within the lookback) — the exact frozen operationalization of "both filters pass" already measured in campaign #3. The new-high entry maps most directly to Shape B; per-shape decomposition covers all three. |
| "80% chance of this working" | **Win rate** (proportion of forward returns > 0 after cost, N=10) ≥ 0.80 on the pass set, OOS 2016–2025 only |
| "Profit 60% of the time, 70% of the time... can be enough" | Reference thresholds 0.70 / 0.60 run through the same test — the claim's own softening, reported **without verdicts** (and note: "enough to be profitable" also depends on the untested reward:risk, see §5) |
| No stated sample or measurement window | All OOS pass detections per shape at the frozen horizon: n_A=3,941, n_B=6,940, n_C=280 — all above the count floor |
| No regime qualifier | The claim is unconditional — tested unconditionally; per-year split reported as a sensitivity |

## 2. Hypotheses (two verdict families, each Holm-corrected across A/B/C at α=0.05, OOS only)

**Family 1 — the claim test (the literal 80%):** per shape, exact one-sided
binomial test of H0: p ≥ 0.80 (the claim holds) vs H1: p < 0.80 on the
pass-set win rate. This is the falsification test of the number itself.

**Family 2 — the win-rate edge test (complementary):** win-rate excess of
the pass set vs era-matched random entries AND same-ticker windows —
"does this setup win more often than chance?" p_input = max(p_random,
p_same); EDGE requires Holm rejection AND the excess CI-low > 0.

The pass set is the same frozen subset measured in #3 on mean returns;
here the outcome variable is the win rate. Complementary, not redundant:
a distribution can win often but lose big, or win rarely but win big.

## 3. Measurement (identical protocol to #1–6 where shared)

- **Frozen inputs only:** `data/cache/veto_detections_v1.csv` (pre-reg #3
  output; input detections sha 9b44f66160130c3a…, veto code sha
  162bab437e0dc95f…), bars and universe as cached, SPY from the same cache.
  No fetch, no edits. The `veto_pass` flag IS the setup — no new legs.
- **Win definition:** forward return = c_{t+N} / o_{t+1} − 1 − COST
  (COST 0.0015), entry open of t+1, exit close of t+N, N=10 primary; win
  = ret > 0. Era by signal date; verdicts on OOS 2016–2025 only.
- **Win rate** = mean of the (ret > 0) indicator on the pass subset, per
  shape, warm-up rows excluded (counted), exits beyond series end counted.
- **F1 test:** exact binomial p = Σ_{k≤n_wins} C(n,k)·0.8^k·0.2^(n−k),
  computed in logspace via math.lgamma — deterministic, no RNG. One-sided
  95% upper bound (Clopper–Pearson, inverted exact test) reported.
- **F2 test:** bootstrap_excess(win indicators, sample_base) — identical
  machinery to #3's F2, B=1,000, seed 20260813; the mean of a baseline
  draw IS its win rate, so the difference is a win-rate excess.
  Baselines from build_pools(N, universe): random pool = all-universe OOS
  windows; same-ticker pool = per-ticker windows count-weighted by the
  **pass set's own ticker distribution per shape** (the #6-corrected
  protocol); SPY raw as reference. Baselines pay COST; SPY raw.
- **Count floor:** n ≥ 100 pass OOS per shape (F1/F2).

## 4. Verdicts (pre-registered decision rules, applied on OOS)

| Family | Outcome | Rule |
|---|---|---|
| F1 (claim test) | `rejected` (claim falsified) | Holm-rejected at α=0.05 across shapes AND one-sided 95% CI upper < 0.80 |
| F1 | `supported` | CI includes 0.80 (cannot reject the claim), n ≥ 100 |
| F1 | `inconclusive` | n < 100 |
| F2 (win-rate edge) | EDGE | Holm-rejected AND excess CI-low > 0 — the pass set wins significantly more often than chance |
| F2 | NO EDGE | CI includes 0, or estimate ≤ 0, or Holm gate not cleared, n ≥ 100 |
| F2 | INCONCLUSIVE | n < 100 |

Vocabulary note: F1's verdict concerns the claimed *number* (supported /
rejected); F2 uses the EDGE vocabulary of #1–6. Expected outcome stated
up front: with n in the thousands and plausible win rates near 0.5,
rejection of the 0.80 claim is near-certain; the campaign's information is
in the size of the gap, the F2 result, and the 0.60/0.70 references.

## 5. Data & bias handling (§7 checklist)

- **No new data** (frozen pre-reg #3 output; the pass flag was created
  before this campaign existed). **Look-ahead:** all legs use data ≤ t;
  entry remains open of t+1. **Multiple testing:** two families, Holm
  within each, α=0.05, OOS only, all thresholds fixed here before
  measurement — no post-hoc fitting.
- **Overlapping windows / clustering:** as #4 §5 — bootstrap preserves
  dependence; effective independence < nominal; documented, not adjusted.
- **Scope note (carried from #3):** the source uses MACD on 1-min charts
  and intraday entries; the daily-bar veto-pass setup is the documented
  adaptation. This is a verdict on the *mechanism* (does the pass-set win
  rate approach 0.80?), not on his intraday practice.
- **"Enough to be profitable" (0.60/0.70) is NOT tested as a verdict:** it
  depends on the reward:risk and stop discipline, which are untested here.
  Reported as reference thresholds only.
- **Survivorship / era-matching:** unchanged from #1–6.

## 6. Sensitivities (pre-declared, exploratory, NO verdicts)

- Win rate excluding cost (COST removed from the win definition).
- N = 5, 20 (same pass subsets, re-measured returns).
- Reference thresholds 0.70 / 0.60 (one-sided tests — his own language).
- Pass-vs-kill and pass-vs-full win rates (E-01/E-04's conditioning
  question in win-rate terms).
- Win rate on the raw (unfiltered) detection set per shape.
- Per-year pass-set win rates (OOS); IS record (2000–2015, observation).

## 7. Freeze

- Frozen 2026-08-14, before any measurement. Registered against:
  PREREGISTRATION #7 · shapes A/B/C · veto-pass subset (pre-reg #3) ·
  win = ret > 0 after cost, N=10 · F1 exact one-sided binomial vs 0.80
  (Holm across shapes) · F2 win-rate excess vs random and same-ticker
  (p_input = max) · engine c7421fbf…, never modified.
- Amendments require a new pre-registration and a fresh window. Exploratory
  results may be reported but never drive a verdict or a claim.

## 8. Campaign outcome (recorded after measurement — parameters unchanged)

Measured 2026-08-14 with the frozen parameters above. **REJECTED × 3
(F1 — the literal 80% is falsified on every shape), NO EDGE × 3 (F2 —
the pass set does not win more often than chance)**. The "red flag"
expectation was met honestly: an 80% claim, falsified at astronomical
significance.

**Family 1 (the claim test): REJECTED × 3** — A: n=3,941, win rate
**0.4869** (one-sided p < 1e-308, log10 −415.3; CI upper 0.5002); B:
n=6,940, **0.4899** (p < 1e-308, log10 −717.2; CI upper 0.4999); C:
n=280, **0.5286** (p = 2.0e-24; CI upper 0.5790). The pass set wins
roughly half the time — the claimed 0.80 is off by ~30 percentage points,
and the one-sided 95% upper bound is ≤ 0.58 on every shape.

**Family 2 (win-rate edge vs chance): NO EDGE × 3** — and worse: A and B's
pass sets win **significantly LESS often** than era-matched random entries
(A: −3.04pp, p=0.004; B: −2.76pp, p<0.001; same-ticker −3.57pp/−3.09pp,
both p≤0.004) — the CI upper bounds are negative, a *negative* win-rate
excess vs chance. C: +1.36pp (p=0.786), null. The p_input gate was
cleared nowhere, so no EDGE.

**Sensitivities (no verdicts), all reported in the full report:**
no-cost win rates 0.5001/0.5000/0.5357 — even ignoring cost, ~50%, not
80%. His own softening thresholds are falsified too: 0.70 (p = 1.3e-9 to
1.2e-291) and 0.60 (p = 9.2e-77, 8.9e-47, **0.009** — C's 60% "enough to
be profitable" floor fails at α=0.05 as well). Pass-vs-kill win-rate
excesses are null (kill vs pass: A −2.64pp p=0.066, B −1.91pp p=0.532,
C −4.13pp p=0.588) — the veto does not raise the win rate, consistent
with #3's mean-return verdict; on A the killed set wins *more* often
(near-significant). Per-year pass win rates: A's worst year is 2022
(0.307); nothing reaches 0.60 in any year of any shape. IS record:
0.52/0.50/0.51 — the 80% is not visible in-sample either.

Answer to the campaign's question: **the 80% number is false on daily
bars** — the veto-pass setup wins 48.7–52.9% of the time after cost,
statistically indistinguishable from (and on A/B *below*) chance. The
claim's own hedge — "60% of the time can be enough to be a very
profitable trader" — is also unreached; even the 60% floor is falsified
at α=0.05 on all three shapes (C at p=0.009).

**Interpretation (recorded, not the verdict):** the "80% chance" is the
kind of round-number success-rate claim that trading education generates
without a measurement window — and the first honest measurement of the
identical setup (same frozen pass subsets, #3) shows it is a coin flip
at best. Consistent with #3's mean-return verdict (B significantly
*below* random), the win-rate lens adds: on A and B the pass set also
wins *less often* than chance — the veto-pass setup is not an edge in
either return or frequency terms. Verification: outputs deterministic
(results 92669c58…, report 07e8a624…, byte-identical across two runs);
data layer independently recomputed row-by-row from bars; F1 p-values
and CI bounds cross-checked against two independent exact methods
(scipy exact binomial + a lgamma-free product/recurrence computation).
Verdicts written to CLAIMS_LEDGER §E.7; full report in
`data/cache/e02_measure_report.md` (+ `e02_measure_results.json`).

---

# Pre-registration #8 — High relative volume (ledger rows I-D-07 / I-E-01)

**Frozen 2026-08-14, before any measurement.** No parameters below may be
changed after this date; any change is a new hypothesis requiring a fresh
pre-registration and a fresh evaluation window.

## 1. Translation — claim as stated → as measured

| Claim as stated | Source | Translation (as measured) |
|---|---|---|
| "Pattern trading you have to remember does not work on all stocks… it only works on the stocks that have high relative volume… volume is relative… we just look for what's above average for that stock" | Class 1, txWaMpSzHhM [25:49–26:36] | **RV_t** = v_t / mean(v, prior 20 bars), computed exactly as the frozen detector's `_vol_ratio_ok`: mean of the *prior* 20 bars only (`rolling(20).mean().shift(1)`), guard mean > 0. "Above average for that stock" = RV ≥ 1.0. Primary high-RV threshold **RV ≥ 2.0** — the V = 2.0 multiplier reused from the shape campaign (pre-reg #3 convention: frozen, not tuned). |
| "If we trade the stocks that are dominated and much higher in high-frequency trading, we're gonna lose money hands down every time" | Class 1, txWaMpSzHhM [16:33–17:02] | The veto leg, mirrored: low-RV detections (the thin/liquid-flows set) must not beat their high-RV counterparts. Measured as the F2 contrast below — no separate HFT data exists on daily bars (out of scope, §3). |
| "Relative volume is 500 percent or higher" | xTPcI7HHu5w [28:27–29:36] (I-D-04) | Kept as a **sensitivity** at RV ≥ 5.0, **no verdict** — the source context is a P&L-concentration statement about his own trading, not a pattern-edge claim. |
| The claim's scope | — | The RV filter is a **conditioning layer on the frozen detections** — no new detection legs, no new data. Input set identical to pre-regs #3/#6/#7: `veto_detections_v1.csv`, `camp=warmup==False`, `sel=veto_pass`. |

## 2. Hypotheses — two verdict families

Measured on OOS detections (signal date ≥ 2016-01-01) at N = 10, after
COST = 0.0015. Family 1 tests the claim's absolute leg, Family 2 its
differential leg. Holm–Bonferroni at α = 0.05 applied **within each family**
across the shapes with a testable contrast.

**F1 — absolute:** per shape, mean OOS forward return of the RV ≥ 2.0 subset
vs the three calibrated baselines (era-matched random entries, same-ticker,
SPY reported). Same convention as #6/#7: p_input = max(p_random, p_same),
est = max(est_random, est_same), ci_low = min(ci_random, ci_same). Holm
across A/B/C. **EDGE** requires Holm rejection *and* excess CI-low > 0
(vs both random and same-ticker — the brief §1 bar). The claim is supported
in absolute form only if a shape's high-RV subset clears the same-ticker bar.

**F2 — contrast (the claim's differential leg):** per shape, two-sample
bootstrap excess of the RV ≥ 2.0 subset minus the RV < 2.0 subset of the
same shape's detections (OOS, era-matched by construction). Holm across the
shapes with a testable contrast. **EDGE** (claim supported) requires Holm
rejection and CI-low > 0; **FADE** (claim contradicted) requires Holm
rejection and CI-upper < 0; **NO EDGE** otherwise.

**Structural pre-declaration — Shape A:** the frozen Shape A detector
requires v_t ≥ 2.0 × mean(v, prior 20) at the signal bar (`PARAMS["A"]["V"] =
2.0`). Every A detection therefore has RV ≥ 2.0 by construction; the RV < 2.0
contrast cell is empty at the primary threshold. **F2-A is INCONCLUSIVE by
construction** — pre-declared now, asserted empirically in measurement (min
RV over A detections must be ≥ 2.0; a violated assertion is a red flag, not
a verdict). F1-A at the primary threshold *is* the unconditional veto-pass
set, already measured NO EDGE vs same-ticker ×2 (#3, #7) — re-reported for
completeness, contributes nothing new.

**Count floor:** any cell with < 100 OOS detections → INCONCLUSIVE (the
established protocol, e.g. #6's C-in-bear-days handling). Reported as counts
per cell, never hidden.

## 3. Measurement

Identical to pre-regs #1–#7 where shared: N = 10 (the frozen shape horizon),
COST = 0.0015 round-trip deducted from every trade, B = 1,000 bootstrap
resamples, seed 20260813, era split by signal date (IS 2000–2015 / OOS
2016–2025), warm-up guard bar index < 60 excluded (counted, from #3), engine
`measure.py` (frozen, sha c7421fbf…). RV computed in the measurement tool
from the same parquet bars the detector reads, using the detector's exact
formula (prior-20 mean, mean > 0 guard). Two independent assertions: (a) min
RV over A detections ≥ 2.0 − 1e-9 (construction check); (b) no detection
with < 20 prior bars (RV undefined; expected 0, warm-up covers it).

## 4. Verdicts — pre-registered decision rules (applied on OOS only)

| Verdict | Rule |
|---|---|
| **EDGE (F1)** | Holm-rejected AND excess CI-low > 0 (vs both random and same-ticker) — claim's absolute leg supported |
| **EDGE (F2)** | Holm-rejected AND contrast CI-low > 0 — claim's differential leg supported |
| **FADE (F2)** | Holm-rejected AND contrast CI-upper < 0 — claim contradicted: the low-RV subset outperforms |
| **NO EDGE** | otherwise |
| **INCONCLUSIVE** | < 100 OOS detections in a cell (or F2-A by construction, §2) |

Phase 5 (paper trading) trigger per brief §1: a *positive absolute* edge
after costs — only an **F1 EDGE** can trigger the trigger-check conversation.

## 5. Data & bias handling

No new data. No look-ahead: RV uses bars ≤ t only (prior-20 mean, entry
open t+1). Survivorship: the frozen current-constituent universe (documented
bias, brief §5 — strengthens nulls). The "500 percent" claim carries no
verdict (§1). HFT vetoes are not modeled on daily bars — the F2 contrast is
the proxy the data supports. Detections with RV undefined (< 20 prior bars)
are excluded and counted (expected 0).

## 6. Sensitivities — pre-declared, NO verdicts

| # | Sensitivity | Report |
|---|---|---|
| S1 | RV thresholds **1.0 / 3.0 / 5.0** | F1 + F2 tables at each threshold (counts per cell included) |
| S2 | Full (non-vetoed) detection set at RV ≥ 2.0 | F1 table, no F2 (the input set differs from §2's) |
| S3 | Per-year high-RV F1 mean returns (OOS) | table |
| S4 | In-sample record at RV ≥ 2.0 | F1 table (selection era — descriptive only) |
| S5 | Shape-level RV distributions | median RV; share of detections ≥ 2.0 / ≥ 3.0 / ≥ 5.0 |

## 7. Freeze

Frozen 2026-08-14. Registered against: ledger rows I-D-07 / I-E-01
(CLAIMS_LEDGER §I); inputs `data/cache/veto_detections_v1.csv` (from #3,
frozen); engine `measure.py` c7421fbf (frozen). Measurement tool:
`tools/measure_rv.py`; outputs `data/cache/rv_measure_results.json` +
`data/cache/rv_measure_report.md`.

**Pre-registered expectations (recorded, not hypotheses):** F2 is the
plausible family — RV as hotness/liquidity proxy, B/C high-RV subsets may
beat their low-RV counterparts. F1 expected **NO EDGE** against same-ticker:
the #4 lesson (selection adds nothing over same-ticker B&H) plus every
absolute family to date has been NO EDGE vs same-ticker.

## 8. Campaign outcome

Measured 2026-08-14, parameters unchanged. Verdicts (OOS 2016–2025, N=10,
cost, Holm-corrected within family):

| Family | Verdicts | Evidence |
|---|---|---|
| F1 (absolute) | **NO EDGE × 2, INCONCLUSIVE × 1** | A: n=3,941, excess vs same-ticker −0.22pp (p_input 0.204). B: n=1,026, −0.37pp (p_input 0.548). C: n=46 < 100 floor. High-RV detections beat neither chance nor same-ticker |
| F2 (contrast) | **NO EDGE × 1, INCONCLUSIVE × 1, INCONCLUSIVE-by-construction × 1** | B: high +0.24% vs low −0.05%, excess +0.30pp (CI −0.27..+0.90pp, p=0.302) — the claimed direction, not significant. C: high cell n=46 < floor. A: every detection RV ≥ 2.0 (min asserted 2.000000) — low cell empty, as pre-declared |

Pre-registered expectations met: F1 NO EDGE vs same-ticker (the #4 lesson
holds), F2 the plausible family (sign positive on B at every threshold,
never significant). Sensitivities recorded, no verdicts: at RV ≥ 1.0 — the
claim's literal "above average" — B's subset is *below* random (−0.36pp,
p=0.048) and same-ticker (−0.40pp, p=0.040), a near-miss in the opposite
direction. Full report: `data/cache/rv_measure_report.md` (+
`rv_measure_results.json`). Verification: byte-identical across two runs;
independent recompute (separate implementation) exact to 1e-9. Verdicts
written back to CLAIMS_LEDGER §I.5. Phase 5 not triggered (no F1 EDGE).

---

# Pre-registration #9 — RSI 70/30 reversal bias (ledger row I-X-01)

**Frozen 2026-08-14, before any measurement.** No parameters below may be
changed after this date; any change is a new hypothesis requiring a fresh
pre-registration and a fresh evaluation window.

## 1. Translation — claim as stated → as measured

| Claim as stated | Source | Translation (as measured) |
|---|---|---|
| "Anything above seventy percent… the market is said to be overbought… anything below thirty percent… the market is said to be oversold… it's a suggestion that maybe the strength has gone a little bit too far… maybe the market has gone down too far and is due a bounce back" | rgVdgR1y1Dg [03:16–03:27] (Trading 212) | **RSI_t** computed at close t from the **simple-average formula the video itself teaches**: RS_t = mean(gains, the 14 daily changes ending at t) / mean(\|losses\|, the 14 daily changes ending at t) — *simple* averages, not Wilder smoothing ("the average of X number of days up divided by the average of X number of days down"); RSI_t = 100 − 100/(1 + RS_t); conventions: avg_loss = 0 → RSI = 100 (covers the all-gain and flat cases, TA-Lib rule); avg_gain = 0 and avg_loss > 0 → RSI = 0. Leg **OB**: RSI_t > 70 (pullback due). Leg **OS**: RSI_t < 30 (bounce due). |
| "It defaults to the textbook version 14-day RSI" | rgVdgR1y1Dg [02:50–02:55] | Primary period **14** (the textbook default the video says to keep). |
| "Me I like a ten-day RSI because it's two weeks" | rgVdgR1y1Dg [02:54–02:56] | Period 10 kept as a **sensitivity** (his stated preference), no verdict. |
| "Let's stick with the textbook 70 and 30%" | rgVdgR1y1Dg [03:00–03:02] | Primary thresholds 70/30. |
| Corpus tension (I-B-06): Class 1 — RSI "is more condition to find stocks at extremes it's not by any means a buy or sell indicator" | txWaMpSzHhM [23:42–24:05] | Recorded, not adjudicated: we measure the Trading 212 form (the specific, testable one). A null result is consistent with BOTH (Class 1's caveat AND Trading 212's claim falsified); a positive result adjudicates between them. |
| Demo context | rgVdgR1y1Dg (whole video) | The claim is demonstrated on **GBP/USD forex daily candles**; measured here on **US equity daily bars** (the frozen S&P 600 universe) — a cross-market translation, declared. |

## 2. Hypotheses — two verdict families

Measured on OOS detections (signal date ≥ 2016-01-01) at N = 10, after
COST = 0.0015. Signal = every bar with RSI_t in the leg's range (state-based
primary — each day in the leg is a detection, matching the claim's reading
"when RSI is above 70, pullback is due"). Family 1 tests each leg's
absolute directional claim; Family 2 tests the reversal symmetry between
the legs. Holm–Bonferroni at α = 0.05 within each family.

**F1 — absolute (per leg, directional):** per leg, mean OOS forward return
of the leg's detections vs the calibrated baselines (era-matched random
entries, same-ticker, SPY reported). Convention as #6/#7/#8: p_input =
max(p_random, p_same), est = max, ci_low = min. Holm across the **two legs**
(OB, OS). The claim is directional, so the verdict rules are direction-
specific:
- **OB leg** (claims pullback): **EDGE** iff Holm-rejected AND excess
  CI-upper < 0 (significantly *below* both baselines); **FADE** iff
  Holm-rejected AND CI-low > 0 (significantly above — the overbought
  side keeps going up); NO EDGE otherwise.
- **OS leg** (claims bounce): **EDGE** iff Holm-rejected AND excess CI-low
  > 0; **FADE** iff Holm-rejected AND CI-upper < 0; NO EDGE otherwise.

**F2 — contrast (the reversal symmetry):** two-sample bootstrap excess of
the OS leg's mean OOS forward return minus the OB leg's (era-matched by
construction). Reversal holds iff the difference is positive. Single test
at α = 0.05 (one Holm slot). **EDGE** iff CI-low > 0; **FADE** iff CI-upper
< 0; NO EDGE otherwise.

**Count floor:** any leg with < 100 OOS detections → INCONCLUSIVE.
Expected far above the floor (RSI extremes are common on daily bars);
reported as counts per leg, never hidden.

## 3. Measurement

Identical to pre-regs #1–#8 where shared: N = 10 (the frozen shape
horizon), COST = 0.0015 round-trip, B = 1,000 bootstrap resamples, seed
20260813, era split by signal date (IS 2000–2015 / OOS 2016–2025),
warm-up guard bar index < 60 excluded (frozen #3 convention — also bounds
the simple-average RSI's exact 14-bar lookback with margin), engine
`measure.py` (frozen, sha c7421fbf…). RSI computed in the measurement
tool from the frozen parquet closes (bar index t; deltas t−13..t; signal
uses bars ≤ t only). Forward returns via the engine's `measure_returns`
on a detection frame with `shape` = leg label. Two structural checks:
(a) RSI values within [0, 100] everywhere; (b) no detections with
< 14 prior closes (the lookback) — expected 0, warm-up covers it.

## 4. Verdicts — pre-registered decision rules (applied on OOS only)

| Verdict | Rule |
|---|---|
| **EDGE (F1-OB)** | Holm-rejected AND excess CI-upper < 0 — overbought ⇒ below-baseline forward returns (pullback, as claimed) |
| **EDGE (F1-OS)** | Holm-rejected AND excess CI-low > 0 — oversold ⇒ above-baseline forward returns (bounce, as claimed) |
| **FADE (F1-OB)** | Holm-rejected AND CI-low > 0 — overbought detections beat the baselines (claim contradicted) |
| **FADE (F1-OS)** | Holm-rejected AND CI-upper < 0 — oversold detections lose to the baselines (claim contradicted) |
| **EDGE (F2)** | CI-low > 0 — OS beats OB (reversal symmetry holds) |
| **FADE (F2)** | CI-upper < 0 — OB beats OS (reversal contradicted) |
| **NO EDGE** | otherwise |
| **INCONCLUSIVE** | < 100 OOS detections in a leg |

Phase 5 (paper trading) trigger per brief §1: a *positive absolute* edge
after costs — **only an F1-OS EDGE can trigger the trigger-check
conversation** (F1-OB EDGE is a negative-return finding; F2 is a
differential finding).

## 5. Data & bias handling

No new data; same frozen universe and bars as every prior campaign.
No look-ahead: RSI uses closes ≤ t; entry open t+1. **Overlap caveat,
pre-declared:** state-based legs fire on consecutive bars, so forward
windows overlap and rows are not independent; the bootstrap CIs are
computed under iid resampling, so the effective sample size is smaller
than the row count — the crossing-based sensitivity (S4, first bar of
each excursion only) shows the event-level view. Cross-market caveat
declared (§1). The all-gain/all-loss conventions (RSI = 100/0) are part
of the frozen formula. Survivorship: frozen current-constituent
universe (documented bias, brief §5 — strengthens nulls).

## 6. Sensitivities — pre-declared, NO verdicts

| # | Sensitivity | Report |
|---|---|---|
| S1 | Horizons **N = 1 / 5 / 20** | F1 + F2 tables (entry next open, exit close t+N, cost) |
| S2 | Thresholds **80/20** (I-D-08's V5/V8 scanner), **90/10** (I-B-06's reversal checklist), **60/40** (weak reference) | F1 + F2 tables, period 14 |
| S3 | Period **10** (his stated preference) at 70/30 | F1 + F2 tables |
| S4 | **Crossing-based** events (first bar of each excursion above 70 / below 30, until re-entry) at 70/30 | F1 + F2 tables |
| S5 | Per-year F1 leg mean returns (OOS) | table |
| S6 | IS record at 70/30 | F1 table (descriptive — selection era) |
| S7 | RSI distribution: share of OOS bars in each leg; min/max RSI | table |

## 7. Freeze

Frozen 2026-08-14. Registered against: ledger row I-X-01 (CLAIMS_LEDGER
§I); inputs: the frozen S&P 600 universe + bars (Phase-1 dataset, see
data/README.md); engine `measure.py` c7421fbf (frozen). Measurement tool:
`tools/measure_rsi.py`; outputs `data/cache/rsi_measure_results.json` +
`data/cache/rsi_measure_report.md`.

**Pre-registered expectations (recorded, not hypotheses):** the reversal
family has shown up only in E-03's regime-specific bear-day fade — expect
weak or null effects on the broad daily-bar 70/30 state claim post-cost;
F2 (the differential) is the cleaner test; F1 legs expected NO EDGE.

## 8. Campaign outcome

*(Recorded after measurement — parameters unchanged.)*

Measured 2026-08-14. **EDGE × 3 at the state level** — the first campaign
to confirm a claim's directional structure:

- **F1-OB EDGE**: n=201,419 OOS; mean +0.23%; excess vs random −0.26pp
  (CI −0.31..−0.20, p<0.001) and vs same-ticker −0.30pp (CI −0.36..−0.25,
  p<0.001); Holm-rejected (gate 0.025), CI-upper −0.25pp < 0 — overbought
  ⇒ pullback, as claimed.
- **F1-OS EDGE**: n=150,236 OOS; mean +0.61%; excess vs random +0.12pp
  (CI +0.05..+0.19, p<0.001) and vs same-ticker +0.14pp (CI +0.07..+0.23,
  p<0.001); Holm-rejected (gate 0.050), CI-low +0.05pp > 0 — oversold ⇒
  bounce, as claimed.
- **F2 EDGE**: OS − OB = +0.38pp (CI +0.31..+0.45, p<0.001) — reversal
  symmetry holds.

Bounding caveats (full detail in the report): (S4, pre-declared) the
event-level view is null — OS excess vs same-ticker +0.10pp, p=0.166; OB
−0.14pp, p=0.026; (S2/S3) the OS edge clears at 70/30 and 90/10 but not
80/20 (p=0.138) or period 10 (p=0.286); size is +0.14pp per 10-bar trade
after cost. The pre-registered expectation ("F1 legs expected NO EDGE")
was not met — falsified in the claim's favor at the state level.

**Phase-5 trigger-check conversation held (F1-OS EDGE is the sole
pre-registered trigger): NOT TRIGGERED** — the state-level significance is
overlap-inflated (event-level correction p=0.166), the parameter
neighborhood is fragile, and the absolute size is a fraction of a percent
per trade. Phase 5 remains not triggered. Verdicts written back to
CLAIMS_LEDGER §I.6; report `data/cache/rsi_measure_report.md`
(+ `rsi_measure_results.json`). Verification: byte-identical across runs
(results 93537c3f…, report 46c84b42…); independent implementation exact
(RSI to 2.8e-14; counts and means exact).

# Pre-registration #10 — RSI divergence: frequency + reliability (ledger rows I-X-02/03/04)

**Frozen 2026-08-14, before any measurement.** No parameters below may be
changed after this date; any change is a new hypothesis requiring a fresh
pre-registration and a fresh evaluation window.

## 1. Translation — claims as stated → as measured

| Claim as stated | Source | Translation (as measured) |
|---|---|---|
| Bullish divergence: "the market slips lower rallies but slips lower again… we've got lower lows but look at what the RSI is doing… hits a low again but we've got higher lows so this is a suggestion… that maybe this weakness is running out of steam… known as bullish divergence" | rgVdgR1y1Dg [05:51–06:15] (Trading 212) | **Bullish divergence event** on a pair of **consecutive swing lows** (t1 < t2) iff (a) **price**: low_t2 < low_t1 (lower low); (b) **RSI**: RSI_t2 > RSI_t1 (higher low). Swing lows are strict **k=2 fractals** (low_t < the lows of the 2 bars on each side; ties never form a swing), pairs must have **disjoint fractal windows** (t2 − t1 ≥ 5). Claim: weakness running out of steam ⇒ above-baseline forward returns (bounce). |
| Bearish divergence: "the market has pushed to a high pushes a little bit higher… we've got our lower high so that's a suggestion that maybe the strength is running out of steam" | rgVdgR1y1Dg [06:39–07:03] | **Bearish divergence event** on a pair of **consecutive swing highs** (strict k=2 fractal on highs, disjoint windows) iff (a) **price**: high_t2 > high_t1 (higher high); (b) **RSI**: RSI_t2 < RSI_t1 (lower high). Claim: strength running out of steam ⇒ below-baseline forward returns (pullback). |
| "These divergence signals are a lot less common so arguably a bit more reliable" — with context [04:44–04:58]: "you do get quite a few overbought oversold signals and they're maybe not as reliable as another way of using the RSI… divergence" | rgVdgR1y1Dg [05:33–05:39], [04:44–04:58] | The comparison baseline is **the 70/30 overbought/oversold signals themselves**. Two measurements. **(i) Frequency:** OOS count of divergence events (bull + bear) vs count of **70/30 crossing events** (first bar of each excursion above 70 / below 30 — the pre-reg #9 S4 rule) over the same OOS bars and same period; reported as counts, ratio, and bootstrap CI on the ratio (CI-upper < 1 ⇒ "less common" confirmed). **(ii) Reliability:** per leg, the **two-sample contrast** of divergence events vs crossing events — on **mean forward return** and on **directional hit rate** (share of events with positive forward return after cost). Verdict family F2. |
| "Daily chart again ten day RSI" (the demo charts for both divergence setups) | rgVdgR1y1Dg [06:25] | Primary RSI period **10** — the period the setups are demonstrated on (also the video's stated preference, [02:54–02:56]). Period 14 kept as a sensitivity (textbook default; cross-campaign comparability with pre-reg #9's primary). |
| RSI formula | rgVdgR1y1Dg [03:16–03:27] | Same frozen **simple-average (Cutler) RSI** as pre-reg #9: RS_t = mean(gains, the `period` daily changes ending at t) / mean(\|losses\|, same window); RSI = 100 − 100/(1+RS); conventions: avg_loss = 0 → 100 (all-gain and flat); avg_gain = 0 and avg_loss > 0 → 0. No formula change. |
| "The market pushes out to fresh highs for the up move but the RSI doesn't follow it" (gloss on the bearish example) | rgVdgR1y1Dg [07:05–07:11] | Recorded, not gated: the consecutive-swing-high definition with high_t2 > high_t1 is the operative reading; the gloss describes the example's market structure, not an additional rule. |
| Swing confirmation timing | — | A k=2 fractal is only *knowable* at close t+2 (the two bars after the pivot). Per the bias checklist's strict rule ("signal at close t uses only data ≤ t"), the **signal bar is the confirmation bar t2+2**: entry open t2+3, exit close t2+2+N. The chartist's-eye variant — signal at the pivot bar t2, entry open t2+1 — is a pre-declared sensitivity (S8) with its selection-tilt caveat; it is not the primary. |
| Demo context | rgVdgR1y1Dg (whole video) | Setups demonstrated on GBP/USD and USD/JPY daily candles; measured here on US equity daily bars (the frozen S&P 600 universe) — cross-market translation, declared. |
| Not measured here | — | I-X-05 (stop placement at the prior extreme low) remains `candidate` — a risk-rule claim, not a direction claim; no verdict in this campaign. |

## 2. Hypotheses — verdict families

Measured on OOS events (signal date ≥ 2016-01-01; signal bar = t2+2) at
N = 10, after COST = 0.0015. Event-level by construction (one event per
qualifying swing pair; event bars separated by ≥ 5 bars). Family 1 tests
each leg's absolute directional claim (I-X-03/04); Family 2 tests the
reliability contrast vs the 70/30 crossing baseline (I-X-02).
Holm–Bonferroni at α = 0.05 within each family.

**F1 — absolute (per leg, directional):** mean OOS forward return of the
leg's events vs the calibrated baselines (era-matched random entries,
same-ticker, SPY reported). Convention as pre-reg #9 §2: p_input =
max(p_random, p_same), est = max, ci_low = min, ci_upper = min. Holm
across the **two legs** (BULL, BEAR):
- **BULL leg** (claims bounce): **EDGE** iff Holm-rejected AND excess
  CI-low > 0 (significantly *above* both baselines); **FADE** iff
  Holm-rejected AND CI-upper < 0; NO EDGE otherwise.
- **BEAR leg** (claims pullback): **EDGE** iff Holm-rejected AND excess
  CI-upper < 0 (significantly *below* both baselines); **FADE** iff
  Holm-rejected AND CI-low > 0; NO EDGE otherwise.

**F2 — reliability contrast (I-X-02), per leg, per metric:** two-sample
bootstrap contrast of the divergence leg's events **minus** the 70/30
crossing events at the same period (oversold crossings vs the BULL leg;
overbought crossings vs the BEAR leg — the claim's own comparison
baseline). Metrics: **(a) mean forward return**, **(b) directional hit
rate** (share of events with ret > 0 after cost). Holm across the
**four tests** (2 legs × 2 metrics):
- **F2-BULL-mean**: EDGE iff CI-low > 0 (divergence bounces more than
  oversold crossings); FADE iff CI-upper < 0.
- **F2-BEAR-mean**: EDGE iff CI-upper < 0 (divergence pulls back more
  than overbought crossings); FADE iff CI-low > 0.
- **F2-BULL-hit**: EDGE iff hit-rate contrast CI-low > 0; FADE iff
  CI-upper < 0.
- **F2-BEAR-hit**: EDGE iff hit-rate contrast CI-upper < 0; FADE iff
  CI-low > 0.

**Count floor:** any leg with < 100 OOS events → INCONCLUSIVE for that
leg (F1 and F2 both). Expected far above the floor (swings are dense on
daily bars; pre-reg #9 measured ~350k OOS state detections); reported as
event counts per leg, never hidden.

**Frequency claim (I-X-02 first half):** reported as OOS counts (divergence
events vs 70/30 crossing events), the ratio, and a bootstrap CI on the
ratio — a measurement, not a verdict family (it is a rate claim, not a
return claim). Reported at both period 10 (primary) and period 14 (S3).

## 3. Measurement

Identical to pre-reg #9 where shared: N = 10, COST = 0.0015 round-trip,
B = 1,000 bootstrap resamples, seed 20260813, era split by signal date
(IS 2000–2015 / OOS 2016–2025), warm-up guard signal-bar index < 60
excluded (frozen #3 convention — also bounds the RSI's 10-bar lookback
and the fractal's 2-bar confirmation with margin), engine `measure.py`
(frozen, sha c7421fbf…). RSI, swings, and events computed in the
measurement tool from the frozen parquet bars (signal inputs ≤ signal
bar only). Forward returns via the engine's `measure_returns` on a
detection frame with `shape` = leg label (placeholder mapping BULL→"A",
BEAR→"B", and "C" for the crossing frame — the engine's ABC-only dropped
dict; rows relabeled after, as in pre-reg #9). Structural checks:
(a) RSI values within [0, 100] everywhere; (b) no event with t1 < period
(the first swing's RSI undefined) — expected 0; (c) no event with
t2 > n_bars − 3 (fractal needs its two confirmation bars) — expected 0;
(d) no signal bar < 60 — warm-up covers it.

## 4. Verdicts — pre-registered decision rules (applied on OOS only)

| Verdict | Rule |
|---|---|
| **EDGE (F1-BULL)** | Holm-rejected AND CI-low > 0 — bullish divergence ⇒ above-baseline forward returns (bounce, as claimed) |
| **EDGE (F1-BEAR)** | Holm-rejected AND CI-upper < 0 — bearish divergence ⇒ below-baseline forward returns (pullback, as claimed) |
| **FADE (F1-BULL)** | Holm-rejected AND CI-upper < 0 — bullish divergence loses to the baselines (claim contradicted) |
| **FADE (F1-BEAR)** | Holm-rejected AND CI-low > 0 — bearish divergence beats the baselines (claim contradicted) |
| **EDGE (F2-·)** | per §2 — divergence more reliable than the 70/30 crossing baseline on that metric/leg |
| **FADE (F2-·)** | per §2 — divergence less reliable than the 70/30 crossing baseline on that metric/leg |
| **NO EDGE** | otherwise |
| **INCONCLUSIVE** | < 100 OOS events in a leg |

Phase 5 (paper trading) trigger per brief §1: a *positive absolute* edge
after costs — **only an F1-BULL EDGE can trigger the trigger-check
conversation** (F1-BEAR EDGE is a negative-return finding; F2 is a
differential finding).

## 5. Data & bias handling

No new data; same frozen universe and bars as every prior campaign. No
look-ahead: the signal bar t2+2 uses only bars ≤ t2+2 (RSI_t2, lows/highs
through t2+2); entry open t2+3. **Overlap caveat, pre-declared:** event
bars are ≥ 5 bars apart but N=10 forward windows can overlap; bootstrap
CIs are computed under iid resampling, so effective sample size is below
the row count. **F2 timing asymmetry, pre-declared:** divergence events
enter at open t2+3 (fractal confirmation), crossing events at open
cross+1 — each at its own earliest honest entry; the 2-bar difference is
reported alongside the contrast (S8 shows the effect of the alternate
timing). Cross-market caveat declared (§1). Survivorship: frozen
current-constituent universe (documented bias, brief §5 — strengthens
nulls). The all-gain/all-loss RSI conventions (100/0) are part of the
frozen formula.

## 6. Sensitivities — pre-declared, NO verdicts

| # | Sensitivity | Report |
|---|---|---|
| S1 | Horizons **N = 1 / 5 / 20** | F1 + F2 tables (baselines rebuilt per horizon — era- AND horizon-matched pools) |
| S2 | Swing scale **k = 3** (7-bar fractal) and **k = 5** (11-bar fractal) | F1 + F2 tables, period 10 |
| S3 | Period **14** (textbook default; cross-campaign comparability with pre-reg #9) | F1 + F2 tables, crossings recomputed at 14; frequency counts at 14 |
| S4 | Minimum swing separation **t2 − t1 ≥ 10** bars | F1 + F2 tables, period 10, k=2 |
| S5 | Per-year F1 leg mean returns (OOS) | table |
| S6 | IS record at period 10, k=2 | F1 table (descriptive — selection era) |
| S7 | **Extreme-gated** divergence (first swing's RSI beyond 70/30: RSI_t1 > 70 for bearish, RSI_t1 < 30 for bullish) — the video's bearish example notes the RSI "blips briefly into overbought" at the first high | F1 tables |
| S8 | **Chartist's-eye timing**: signal at the pivot bar t2, entry open t2+1 (pre-declared caveat: the swing's future-side fractal condition is then a *selection* input — it excludes pivots followed by continuation, tilting toward the claim) | F1 tables |

## 7. Freeze

Frozen 2026-08-14. Registered against: ledger rows I-X-02/03/04
(CLAIMS_LEDGER §I); inputs: the frozen S&P 600 universe + bars (Phase-1
dataset, see data/README.md); engine `measure.py` c7421fbf (frozen).
Measurement tool: `tools/measure_divergence.py`; outputs
`data/cache/divergence_measure_results.json` +
`data/cache/divergence_measure_report.md`.

**Pre-registered expectations (recorded, not hypotheses):** divergence
events are sparse and event-level by construction, and the 70/30 campaign
found the event-level view null — expect weak or null F1 effects post-cost
(and F1-BULL EDGE — the Phase-5 trigger — very unlikely). The frequency
ratio should trivially confirm "less common" (one event per swing pair vs
one per excursion). F2 (the reliability contrast) is the claim's own
comparison — expect small or null: the crossing baseline already carries
the measured reversal tendency (pre-reg #9 S4: OS +0.10pp, OB −0.14pp vs
same-ticker).

## 8. Campaign outcome

*(Recorded after measurement — parameters unchanged.)*

Measured 2026-08-14. **A split verdict — the first event-level absolute
EDGE in the project's history, on the bullish leg; NO EDGE on the bearish
leg:**

- **F1-BULL EDGE**: n=16,985 OOS; mean +0.80%; win 54.12%; excess vs random
  +0.31pp (CI +0.11..+0.50, p=0.002) and vs same-ticker +0.34pp (CI
  +0.15..+0.53, p=0.002); Holm-rejected (gate 0.025), CI-low +0.11pp > 0 —
  bullish divergence ⇒ bounce, as claimed (I-X-03).
- **F1-BEAR NO EDGE**: n=20,800 OOS; mean +0.46%; win 50.83%; excess vs
  same-ticker −0.04pp (CI −0.20..+0.11, p=0.662) — bearish divergence does
  not predict pullbacks (I-X-04 not confirmed).
- **F2-BULL EDGE × 2** (reliability vs oversold crossings, I-X-02):
  mean contrast +0.18pp (CI +0.03..+0.34, p=0.012); hit-rate contrast
  +1.50pp (CI +0.63..+2.29, p<0.001) — "more reliable" confirmed on the
  bullish side.
- **F2-BEAR-mean FADE**: contrast +0.21pp (CI +0.07..+0.34, p<0.001) —
  bearish divergence's mean is *above* the overbought-crossing mean, i.e.
  *less* pullback than the crossing baseline; "more reliable" fails on the
  bearish side, in the opposite direction. F2-BEAR-hit NO EDGE (+0.54pp,
  CI −0.21..+1.30, p=0.176).
- **Frequency** (I-X-02 first half; a measurement, not a verdict family):
  n_div=37,929 vs n_cross=124,298 → ratio **0.3051** (ticker-cluster CI
  0.3022..0.3081) — "a lot less common" trivially confirmed (~2.8 BULL
  events per ticker per year; period-14 ratio 0.4287).

The pre-registered expectation ("weak or null F1 effects post-cost, F1-BULL
EDGE — the Phase-5 trigger — very unlikely") was **not met** — falsified in
the claim's favor on the bullish leg. The S8 selection-tilt caveat was
confirmed empirically: the chartist's-eye variant (signal at the pivot,
entry +1) shows BULL +2.06pp / BEAR −1.66pp vs the primary's honest
confirmation-bar timing — the pre-declared tilt is real and large, and the
conservative primary is the small number. Robustness across structural
sensitivities (exploratory, no verdicts): BULL excess vs same-ticker holds
at k=3 (+0.39pp), k=5 (+0.50pp), period 14 (+0.23pp), min-sep 10 (+0.30pp),
extreme-gated (+0.45pp); S1 shows the edge accrues over the horizon (N=1
≈ 0, N=5 +0.09pp, N=20 +0.53pp) while BEAR turns negative at N=20
(−0.26pp); S5: BULL positive in 9/10 OOS years (only 2018: −0.16%). IS
record: BULL +0.71% (win 53.3%), BEAR +0.41% (win 52.8%).

**Phase-5 trigger-check conversation held (pre-reg §4: F1-BULL EDGE is the
sole pre-registered trigger): NOT TRIGGERED.** For: the first event-level
absolute EDGE in the project's history — no overlap inflation (the killer
of the RSI-70/30 state edge), robust across every structural sensitivity,
positive in 9/10 OOS years, conservative timing. Against: (1) **the brief
§5 survivorship gate** — the universe is current constituents, and the
brief pre-registers that "any positive result must be re-checked against
(a) [historical constituents] before being trusted"; this is exactly the
case that gate exists for, and the re-check has not been done; (2) size —
+0.34pp per 10-bar trade after cost on ~2.8 events per ticker per year;
(3) the claim is only half-confirmed (F1-BEAR NO EDGE; F2-BEAR-mean FADE —
bearish divergence *less* reliable than overbought crossings);
(4) cross-market translation (taught on GBP/USD daily, measured on US
equities). The explicit path forward, pre-registered in the brief: a
**fresh pre-registration against historical constituents** (§5 option (a),
a new data artifact) before this family can be trusted. Phase 5 remains
**not triggered** after ten campaigns. Verdicts written back to
CLAIMS_LEDGER §I.7; report `data/cache/divergence_measure_report.md`
(+ `divergence_measure_results.json`). Verification: byte-identical across
two runs (results 674b2d95…, report 826f0bbf…); independent implementation
exact on all 22 checks (per-bar RSI loop vs the tool's rsi_series: max diff
0.0 on 40 tickers; per-leg counts and means exact to 1e-12; frequency
counts exact at periods 10 and 14; min_t1=10 ≥ period; RSI bounds [0, 100]
clean; 0 bad signals).



---

# Pre-registration #11 — "almost all of the big moves will eventually be corrected" (ledger row I-F-01)

**Frozen 2026-08-14, before any measurement.** No parameters below may be
changed after this date; any change is a new hypothesis requiring a fresh
pre-registration and a fresh evaluation window.

## 1. Translation — claims as stated → as measured

| Claim as stated | Source | Translation (as measured) |
|---|---|---|
| "We know that almost all of the big moves will eventually be corrected" — the rationale for the reversal trading strategy; "what goes up must come down and what goes down must come back up" | jfe1Zl-5EQI [16:01–16:09], [15:05–15:09] | **Big-move event** at bar t: the absolute close-to-close move over the prior **L = 10 bars**, |close_t − close_{t−L}|, is **≥ 3 × ATR_t** (a "move" of three average true ranges). Direction by sign of the net move: **UP leg** iff close_t > close_{t−L} (big up-move); **DOWN leg** iff close_t < close_{t−L} (big down-move). Claims: an UP move ⇒ **below-baseline** forward returns (corrected); a DOWN move ⇒ **above-baseline** forward returns (recovered — his "what goes down must come back up"). |
| ATR formula | — (no ATR teaching found in the corpus — full transcript scan) | **ATR_t = simple mean of the 14 true ranges ending at t** (Cutler-style, consistent with the project's simple-average RSI): TR_t = max(high_t − low_t, |high_t − close_{t−1}|, |low_t − close_{t−1}|); ATR_t = mean(TR_{t−13..t}). The definition is pre-registered here because the corpus teaches none; textbook default. Wilder's smoothing kept as a sensitivity (S4). |
| "Big move" magnitude | — (ledger operationalization: "large multi-day moves (≥3 ATR)") | Threshold **τ = 3** (primary); τ = 2 / 5 sensitivities (S2). Move window **L = 10** (primary — a two-week move; his examples are multi-day runs); L = 5 sensitivity (S3). |
| Event-level resolution | — | **First bar of each leg excursion** — a leg excursion is a maximal run of consecutive bars all satisfying that leg's condition; the event is the run's first bar (the move "has happened" at close t; entry open t+1, no look-ahead). One event per qualifying run, mirroring the pre-reg #9 S4 crossing rule and the pre-reg #10 divergence conventions. The state-level view — every qualifying bar is an event — is a pre-declared sensitivity (S5) with its overlap caveat; it is NOT the primary (the RSI-70/30 lesson: state-level significance is overlap-inflated). |
| "Corrected" — reading 1 | — | **Below/above-baseline forward returns** (F1): the calibrated absolute test — UP events' mean OOS N-bar return vs era-matched random entries AND same-ticker buy-and-hold (SPY reported); DOWN events' likewise. |
| "Corrected" — reading 2 (the ledger's literal operationalization: "retrace ≥ half within 5–10 sessions") | — | **Retracement claim test** (F2): per event, retrace-frac = (close_t − close_{t+N})/(close_t − close_{t−L}) for UP, (close_{t+N} − close_t)/(close_{t−L} − close_t) for DOWN. "Corrected half" ⇔ close_{t+N} on the far side of the move's **midpoint** (close_t + close_{t−L})/2 (UP: ≤ midpoint; DOWN: ≥ midpoint). F2 contrasts the share of events corrected-half within **N = 10** sessions against the same share on era-matched **random bars** (each random bar's own trailing L-bar move) — the calibrated null ("what share of *typical* bars retrace half their trailing move within N"); the claim predicts big-move bars do so more often. N = 5 reported in S1 (the claim's "5–10 sessions" range). |
| Timing | — | Signal at close t (uses only bars ≤ t: the move window closes at t, ATR_t ends at t); entry open t+1; exit close t+N. No look-ahead, per the bias checklist. |
| Trading context | jfe1Zl-5EQI (whole video) | The regularity is stated in a 2015 intraday-trading classroom as the rationale for shorting tops / buying bottoms. Measured here on **US equity daily bars** (the frozen S&P 600 universe) — intraday→daily translation, declared. Only the *regularity* is measured; the reversal *strategy* (resistance calculation, pin-bar entry, 6:1 R:R) is process content, not a claim. I-F-02 (downside speed asymmetry) is a separate claim, not measured here. |
| Cross-campaign context (recorded, not gated) | — | Pre-reg #4 F2 measured **continuation** EDGE × 3 (our breakout signals kept drifting up 5→20 bars) on a different population; §E.6 measured **fades** of crossed-B breakouts in bear days. This claim predicts mean reversion on a third population (large multi-day moves). The three findings adjudicate each other's scope; noted in the interpretation, not a hypothesis gate. |

## 2. Hypotheses — verdict families

Measured on OOS events (signal date ≥ 2016-01-01) at N = 10, after
COST = 0.0015. Event-level by construction (first bar of each leg
excursion; runs collapse to single events). Family 1 tests each leg's
absolute directional claim; Family 2 tests the literal retracement claim.
Holm–Bonferroni at α = 0.05 within each family.

**F1 — absolute (per leg, directional):** mean OOS forward return of the
leg's events vs the calibrated baselines (era-matched random entries,
same-ticker, SPY reported). Convention as pre-reg #9/10 §2: p_input =
max(p_random, p_same), est = max, ci_low = min, ci_upper = min. Holm
across the **two legs** (UP, DOWN):
- **UP leg** (claims correction): **EDGE** iff Holm-rejected AND excess
  CI-upper < 0 (significantly *below* both baselines); **FADE** iff
  Holm-rejected AND CI-low > 0; NO EDGE otherwise.
- **DOWN leg** (claims bounce): **EDGE** iff Holm-rejected AND excess
  CI-low > 0 (significantly *above* both baselines); **FADE** iff
  Holm-rejected AND CI-upper < 0; NO EDGE otherwise.

**F2 — retracement claim test (per leg):** two-sample bootstrap contrast
of the leg's corrected-half-within-10 rate **minus** the era-matched
random-bar rate (same N, same universe, random bars' own trailing L-bar
moves). Holm across the **two legs**:
- **F2-UP**: EDGE iff Holm-rejected AND CI-low > 0 (big up-moves retrace
  half more often than typical bars — "corrected", as claimed); FADE iff
  CI-upper < 0.
- **F2-DOWN**: EDGE iff Holm-rejected AND CI-low > 0 (big down-moves
  recover half more often than typical bars — "come back up", as
  claimed); FADE iff CI-upper < 0.

**Count floor:** any leg with < 100 OOS events → INCONCLUSIVE for that
leg (F1 and F2 both). Expected far above the floor (3-ATR moves are
common across ~600 tickers × 10 years; runs collapse to single events,
but counts are reported per leg, never hidden).

**Frequency:** OOS event counts per leg (and the OOS excursion counts) —
reported, not a verdict family (the claim carries no frequency content).

## 3. Measurement

Identical to pre-regs #9/#10 where shared: N = 10, COST = 0.0015
round-trip, B = 1,000 bootstrap resamples, seed 20260813, era split by
signal date (IS 2000–2015 / OOS 2016–2025), warm-up guard signal-bar
index < 60 excluded and counted (frozen #3 convention — bounds the
10-bar move window and the 14-bar ATR lookback with margin), engine
`measure.py` (frozen, sha c7421fbf…). ATR, moves, and excursions computed
in the measurement tool from the frozen parquet bars (the engine's
`load_bars` exposes only Open/Close; the tool reads full OHLCV directly —
signal inputs ≤ signal bar only, same frozen Close column). Forward
returns via the engine's `measure_returns` on a detection frame with
`shape` = leg label (placeholder mapping UP→"A", DOWN→"B" — the engine's
ABC-only dropped dict; rows relabeled after, as in pre-regs #9/#10).
F2's retracement indicators computed in the tool from the raw bars
(events and random bars alike). Structural checks: (a) ATR ≥ 0 everywhere
(TR ≥ 0 by construction; a zero-ATR bar can occur on a zero-range day —
the threshold is compared in price units, never a divisor);
(b) no event with signal bar < 60 — warm-up covers it; (c) no event
with t − L < 0 — impossible under (b); (d) no event with signal bar
> n_bars − 1 (n_bad_signal) — expected 0 (series-end drops are the
engine's standard drops, counted).

## 4. Verdicts — pre-registered decision rules (applied on OOS only)

| Verdict | Rule |
|---|---|
| **EDGE (F1-UP)** | Holm-rejected AND CI-upper < 0 — big up-moves ⇒ below-baseline forward returns (correction, as claimed) |
| **EDGE (F1-DOWN)** | Holm-rejected AND CI-low > 0 — big down-moves ⇒ above-baseline forward returns (recovery, as claimed) |
| **FADE (F1-UP)** | Holm-rejected AND CI-low > 0 — big up-moves beat the baselines (claim contradicted) |
| **FADE (F1-DOWN)** | Holm-rejected AND CI-upper < 0 — big down-moves lose to the baselines (claim contradicted) |
| **EDGE (F2-·)** | Holm-rejected AND CI-low > 0 — the leg's big moves retrace half within N more often than typical bars |
| **FADE (F2-·)** | Holm-rejected AND CI-upper < 0 — the leg's big moves retrace half within N *less* often than typical bars |
| **NO EDGE** | otherwise |
| **INCONCLUSIVE** | < 100 OOS events in a leg |

Phase 5 (paper trading) trigger per brief §1: a *positive absolute* edge
after costs — **only an F1-DOWN EDGE can trigger the trigger-check
conversation** (F1-UP EDGE is a negative-return finding; F2 is a
differential finding).

## 5. Data & bias handling

No new data; same frozen universe and bars as every prior campaign. No
look-ahead: the signal at close t uses only bars ≤ t (the move window
closes at t; ATR_t ends at t); entry open t+1. **Overlap caveat,
pre-declared:** excursion-first events are separated by ≥ 1 bar but N=10
forward windows can overlap when runs are close; bootstrap CIs are
computed under iid resampling, so effective sample size is below the row
count. (Runs are typically long — the 10-bar window stays ≥ 3 ATR for
several bars in a strong trend — so overlap is light, but it is declared
and the state-level view (S5) shows the inflated version by contrast.)
Survivorship: frozen current-constituent universe (documented bias,
brief §5 — strengthens nulls). Intraday→daily translation declared (§1).
F2's null is calibrated (the era-matched random-bar rate), not an assumed
"0.5" — a high absolute retracement rate with no contrast is NO EDGE.
The retracement midpoint uses the move window's closes (close_t,
close_{t−L}); the extreme-based variant (window high/low) is S8.

## 6. Sensitivities — pre-declared, NO verdicts

| # | Sensitivity | Report |
|---|---|---|
| S1 | Horizons **N = 1 / 5 / 20** | F1 tables (baselines rebuilt per horizon — era- AND horizon-matched pools); the retracement metric reported at **N = 5** (the claim's "5–10 sessions" range) |
| S2 | Threshold **τ = 2** and **τ = 5** ATR | F1 + F2 tables, L=10 |
| S3 | Move window **L = 5** bars | F1 + F2 tables, τ = 3 |
| S4 | ATR: period **7**, and **Wilder's smoothing** (RMA of TR, the other textbook variant) | F1 tables, L=10, τ = 3 |
| S5 | **State-level view**: every qualifying bar is an event (overlap-inflated by construction — the pre-reg #9 S4 lesson; reported for contrast, not as evidence) | F1 tables |
| S6 | Per-year F1 leg mean returns (OOS) | table |
| S7 | IS record at L=10, τ=3 | F1 table (descriptive — selection era) |
| S8 | Retracement vs the **move window's extreme** (UP: midpoint of close_{t−L} and the window's max high; DOWN: midpoint of close_{t−L} and the window's min low) instead of the close-to-close midpoint | F2 tables |

## 7. Freeze

Frozen 2026-08-14. Registered against: ledger row I-F-01 (CLAIMS_LEDGER
§I-F); inputs: the frozen S&P 600 universe + bars (Phase-1 dataset, see
data/README.md); engine `measure.py` c7421fbf (frozen). Measurement tool:
`tools/measure_bigmove.py`; outputs `data/cache/bigmove_measure_results.json`
+ `data/cache/bigmove_measure_report.md`.

**Pre-registered expectations (recorded, not hypotheses):** this is the
project's first pure mean-reversion claim measured at the event level on
daily bars, on a momentum-selected population (3-ATR moves are big
winners/losers by construction). The campaign history points both ways:
pre-reg #4 F2 measured *continuation* EDGE × 3 on our breakout signals
(a different population), while §E.6 and the RSI-70/30 campaign found
reversal tendencies in bear days and oversold states. Honest expectation:
**null-to-weak F1 effects post-cost** — a 10-bar mean-reversion edge of
the size seen in prior campaigns (0.1–0.5pp) is real but small against
the 0.15% cost; if either leg clears, the **DOWN/bounce leg is the more
likely** (the bounce direction has been the stronger one in every
campaign: RSI-70/30 OS +0.14pp vs OB −0.30pp; E-03's fades). F1-UP
(correction) expected NO EDGE or FADE — continuation after strong up-moves
is the market's other well-known regularity, and our own pre-reg #4 F2
found it in our signal populations. F2 is the claim's literal reading:
expect a modest positive contrast if F1 shows mean reversion at all.
F1-DOWN EDGE (the Phase-5 trigger) judged unlikely, consistent with the
pre-registered posture of every campaign so far.

## 8. Campaign outcome

*(Recorded after measurement — parameters unchanged.)*

Measured 2026-08-14; verification completed 2026-08-15. **Split verdict —
the project's second event-level absolute EDGE, on the UP (correction)
leg, which the pre-registered expectation rated NO EDGE or FADE — and NO
EDGE on the DOWN (recovery) leg; the ledger's literal retracement reading
is decisively falsified on both legs:**

- **F1-UP EDGE**: n=35,908 OOS; mean +0.03%; win 49.00%; excess vs random
  −0.46pp (CI −0.59..−0.33, p<0.001) and vs same-ticker −0.48pp (CI
  −0.61..−0.36, p<0.001); p_input <0.001 (Holm gate 0.025); CI-upper
  −0.36pp < 0 — after ≥3-ATR up-moves, 10-bar returns sit at ~0 after
  cost, *below* both baselines: "corrected" confirmed in the relative
  sense (I-F-01's up leg).
- **F1-DOWN NO EDGE**: n=29,039 OOS; mean +0.48%; win 52.82%; excess vs
  random −0.01pp (CI −0.16..+0.15, p=0.950) and vs same-ticker +0.01pp
  (CI −0.14..+0.17, p=0.866); p_input 0.950 — "what goes down must come
  back up" is null at the 3-ATR threshold.
- **F2-UP FADE**: n_events=73,414 vs n_random=716,712; corrected-half
  within 10 sessions 19.56% vs 32.34% on typical bars; contrast **−12.77pp**
  (CI −13.08..−12.44, p<0.001), Holm-rejected — big up-moves retrace half
  *less* often than typical bars, the literal claim contradicted.
- **F2-DOWN FADE**: n_events=57,102 vs n_random=635,474; 22.49% vs 38.01%;
  contrast **−15.53pp** (CI −15.89..−15.18, p<0.001), Holm-rejected — big
  down-moves recover half *less* often than typical bars, the literal
  claim contradicted.
- **Frequency** (measurement, not a verdict family): OOS events UP 35,997
  / DOWN 29,110; all-era (warm-up excluded) UP 73,503 / DOWN 57,173;
  warm-up UP 761 / DOWN 618; state-level OOS qualifying bars UP 111,016 /
  DOWN 87,803.

The pre-registered expectation ("null-to-weak F1 effects post-cost; if
either leg clears, the DOWN/bounce leg is the more likely; F1-UP expected
NO EDGE or FADE") was **not met — inverted on both legs**: the UP leg
cleared and the DOWN leg was the null. The claim is half right, in the
relative sense: after big up-moves, forward returns are below the
ticker's own baseline — the F1-UP "EDGE" is a negative-return finding
(+0.03% after cost vs +0.48% buy-and-hold; it confirms underperformance,
not a tradeable positive edge). The literal reading the ledger carried
("retrace ≥ half within 5–10 sessions") fails in both directions and at
the claim's own horizon: big moves cross their midpoint within 10
sessions 12.8–15.5pp *less* often than typical bars (F2@N=5: −15.2pp /
−18.1pp). The DOWN leg's magnitude gradient tells the same story: τ=2
shows a small above-baseline bounce (+0.24pp, p<0.001) that vanishes at
τ=3 and reverses at τ=5 (mean −0.90%; −1.36pp vs same-ticker, p<0.001) —
"recovery" exists only for weak moves; extreme down-moves underperform
their own baselines. Robustness (exploratory, no verdicts): the UP
correction accrues over the horizon (N=1 −0.06pp → N=20 −0.71pp), holds
under both ATR variants (period-7 −0.53pp, Wilder −0.45pp), and the
state-level view (S5, overlap-inflated) shows *both* legs below baselines
(UP −0.40pp / DOWN −0.23pp) — underperformance-after-extremes, coherent
with pre-reg #4's continuation EDGE × 3 on our breakout signals:
momentum populations drift relative to their tickers; they do not snap
back to the midpoint. IS record: UP +0.31% (win 50.83%), DOWN +0.77%
(win 52.71%).

Caveats, as pre-declared: excursion-first events keep overlap light but
N=10 windows can overlap for near runs (iid bootstrap CIs — effective
sample below row count); current-constituent universe (survivorship
strengthens these nulls, and this is a negative-return finding — the
brief §5 positive-result gate does not apply); intraday→daily
translation (taught in a 2015 intraday classroom, measured on US equity
daily bars).

**Phase-5 trigger (pre-reg §4): only an F1-DOWN EDGE can trigger the
trigger-check conversation — did not fire (F1-DOWN NO EDGE, p=0.950), so
no trigger-check conversation was held.** Phase 5 remains **not
triggered** after eleven campaigns. Verdicts written back to
CLAIMS_LEDGER §I.8; report `data/cache/bigmove_measure_report.md`
(+ `bigmove_measure_results.json`). Verification: deterministic (results
660F227C…, report CE1145F7…, byte-identical across two runs); independent
implementation, all 61 checks exact — per-bar TR loop bit-exact vs the
tool's tr_series (max diff 0.0 on 10 sampled tickers); ATR-14 loop within
1 ulp (max 3.109e-15; the frozen rolling-mean bit-pattern is
unreproducible by any per-bar summation order — probed five orderings
across 2.8M bars, worst 1.7e-13 — so detection was re-checked against
the tool's own ATR values, and every differing event proven boundary-
exact: at τ=2 exactly one flip, LEU 2019-04-10, move == 2×ATR bit-exact,
rel=0.00e+00); all-era and OOS event counts, F1 means/wins/CIs, F2
rates, and every pre-declared sensitivity count exact; warm-up counts
exact; 0 bad signals.



---

# Pre-registration #12 — "the Bulls take the stairs and the Bears take the window" (ledger row I-F-02)

**Frozen 2026-08-15, before any measurement.** No parameters below may be
changed after this date; any change is a new hypothesis requiring a fresh
pre-registration and a fresh evaluation window.

## 1. Translation — claims as stated → as measured

| Claim as stated | Source | Translation (as measured) |
|---|---|---|
| "The move up that may have taken hours can be all given back in a matter of minutes on the good top reversal... the Bulls take the stairs and the Bears take the window so the sell offs can be very quick" — the reversal-strategy rationale; corroborated by "oftentimes these stocks will give up hours worth of progress in a matter of minutes" | jfe1Zl-5EQI [28:28–28:47], [17:34–17:37] | On daily bars, each bar is one time unit, so **speed = price distance per bar**. Two assertions, both measured: **(A1) directional asymmetry (unconditional)** — down-bars' mean per-bar move size exceeds up-bars' ("stairs" small/slow vs "window" large/fast); **(A2) reversal speed (contextual)** — the retracement of a big up-move covers its distance faster than the move did ("hours up, minutes down"). |
| "Speed" on daily bars | — | Per-bar close-to-close move size, |r_t| where r_t = close_t/close_{t−1} − 1 (percent). Leg by sign of r_t: **UP bars** (r_t > 0), **DOWN bars** (r_t < 0); zero-move bars (r_t = 0 exactly) excluded and counted. (The trader's own red/green candle vocabulary, close-vs-open sign, is a sensitivity — S2.) |
| A1 — "the Bulls take the stairs" | same | **F1-UP**: up-bars' mean |r| is *below* the era-matched typical-bar size (the calibrated null = the unconditional mean |r| over all OOS bars). |
| A1 — "the Bears take the window" | same | **F1-DOWN**: down-bars' mean |r| is *above* typical-bar size. |
| A1 — the asymmetry itself | same | **F2**: the direct contrast DOWN − UP (mean |r|). |
| A2 — "hours up, minutes down" | same | **F4**: on the frozen pre-reg #11 UP events (L=10, τ=3 ATR, excursion-first — the "move up that may have taken [10] bars"), for events that retrace ≥ half within N=10 bars, the retracement's per-bar rate vs the move's per-bar rate — paired contrast. Claim: retracement faster. |
| Timing | — | No entry/exit is measured: this campaign measures bar geometry only (sizes, durations, rates). All quantities use bars ≤ t. |
| Trading context | jfe1Zl-5EQI (whole video) | Stated in a 2015 intraday-trading classroom as the rationale for shorting top reversals (doji at top, stop at high-a-day). Measured on **US equity daily bars** (the frozen S&P 600 universe) — intraday→daily translation, declared: daily "speed" conflates per-bar magnitude with true speed; overnight gaps register as fast. The reversal *strategy* (doji/pin-bar entry, stop placement, 2:1 R:R) is process content, not measured. |
| Cross-campaign context (recorded, not gated) | — | A2's population is exactly pre-reg #11's (I-F-01) UP events, whose F2 already showed big moves retrace half *less* often than typical bars (FADE × 2). F4 measures the speed of the retracement *conditional on it happening* — a separate, pre-registered view. A1's daily translation is the well-documented negative-skew regularity of equity daily returns; the pre-registered posture is that confirmation may be trivial at the per-bar level and the context level (F4) is the sharper test. |

## 2. Hypotheses — verdict families

Measured on OOS bars (bar date ≥ 2016-01-01) at the frozen parameters.
Holm–Bonferroni at α = 0.05 within each family. All CIs bootstrapped
B = 1,000, seed 20260813.

**F1 — absolute, per leg vs the typical-bar baseline (A1's two halves):**
for each leg, the mean per-bar |r| minus the era-matched unconditional
mean |r| over all OOS bars (the calibrated null — "typical bar size").
Joint one-sample bootstrap on the OOS bar population: resample bars with
replacement; recompute the all-bars, up, and down means jointly; form
both excesses. CI = 2.5/97.5 percentiles of the resample excesses;
p = 2×min(null-side mass) clamped to [1/B, 1]. Convention: est = excess,
ci_low/ci_upper = CI bounds, p_input = the p. Holm across the **two
legs**:
- **F1-UP** (claim: up-bars are *smaller* than typical — "stairs"):
  **EDGE** iff Holm-rejected AND CI-upper < 0; **FADE** iff Holm-rejected
  AND CI-low > 0; NO EDGE otherwise.
- **F1-DOWN** (claim: down-bars are *larger* than typical — "window"):
  **EDGE** iff Holm-rejected AND CI-low > 0; **FADE** iff Holm-rejected
  AND CI-upper < 0; NO EDGE otherwise.

Structural note, pre-declared: the all-bars mean is the weighted average
of the legs (plus zeros), so the two sample excesses are mechanically
opposite-signed; the legs are reported because the claim asserts both
halves, and Holm across them is conservative. The interpretable single
number is F2.

**F2 — the asymmetry contrast (A1's single number):** DOWN − UP mean
|r|, two-sample bootstrap (independent resamples of the down and up bar
populations). Single test at α = 0.05. **EDGE** iff CI-low > 0 (down-bars
larger than up-bars, as claimed); **FADE** iff CI-upper < 0; NO EDGE
otherwise.

**F4 — retracement speed on big up-moves (A2, "hours up, minutes
down"):** per pre-reg #11 UP event (frozen detection: L=10, τ=3, ATR-14
simple, excursion-first, warm-up 60) with OOS signal date, let j = the
first bar in [t+1, t+N] whose close ≤ the move's midpoint
(close_t + close_{t−L})/2 (first *crossing* bar — finer than pre-reg #11
F2's t+N-close check; both pre-registered). Events with no crossing
within N are excluded from F4 and counted (their non-retracement is
pre-reg #11 F2's result). move-rate = (close_t − close_{t−L}) / L;
retrace-rate = (close_t − mid) / j — both as percent of close_{t−L} per
bar. Contrast per event: retrace-rate − move-rate; paired one-sample
bootstrap over events. **EDGE** iff CI-low > 0 (the retracement outpaces
the move — "given back in a matter of minutes", as claimed); **FADE**
iff CI-upper < 0; NO EDGE otherwise. Count floor: < 100 events →
INCONCLUSIVE.

Equivalence, pre-registered for the interpretation: retrace-rate >
move-rate ⇔ j < L/2 = 5 bars — the claim is that the midpoint is reached
in fewer bars than the move's half-duration.

**Frequency** (measurement, not a verdict family): OOS counts of UP /
DOWN / ZERO bars; the down-bar share.

**Phase 5, pre-registered:** no family in this campaign measures forward
returns — the claim is about bar geometry (speed/size), not
profitability. The Phase-5 trigger (a positive absolute *return* edge,
brief §1) **cannot fire from this campaign by construction**; Phase 5 is
not implicated.

## 3. Measurement

The tool reads the frozen parquet bars directly (as every measurement
tool does) and computes bar geometry; **the Phase-3 engine's
`measure_returns` is not invoked — no forward returns are measured in
this campaign** (the claim contains no return prediction; the engine's
COST/N conventions therefore do not apply). Quantities: r_t =
close_t/close_{t−1} − 1 for every bar with a prior close (bar index ≥ 1;
index-0 bars excluded and counted); leg by sign; size = |r_t|. OOS
population = bars with date ≥ 2016-01-01. F4 inherits the frozen pre-reg
#11 detection and midpoint rule. Structural checks: (a) every F1/F2 bar
has a finite prior close (any NaN/zero prior closes counted);
(b) zero-move bars counted, never dropped silently; (c) F4 events'
signal bar ≥ 60 and ≤ n_bars − 1 (inherited from the frozen detector);
(d) crossing index j ∈ [1, N].

## 4. Verdicts — pre-registered decision rules (applied on OOS only)

| Verdict | Rule |
|---|---|
| **EDGE (F1-UP)** | Holm-rejected AND CI-upper < 0 — up-bars' mean size below typical (stairs, as claimed) |
| **FADE (F1-UP)** | Holm-rejected AND CI-low > 0 — up-bars *larger* than typical (claim contradicted) |
| **EDGE (F1-DOWN)** | Holm-rejected AND CI-low > 0 — down-bars' mean size above typical (window, as claimed) |
| **FADE (F1-DOWN)** | Holm-rejected AND CI-upper < 0 — down-bars *smaller* than typical (claim contradicted) |
| **EDGE (F2)** | CI-low > 0 — down-bars larger than up-bars (the asymmetry, as claimed) |
| **FADE (F2)** | CI-upper < 0 — up-bars larger than down-bars (claim contradicted) |
| **EDGE (F4)** | CI-low > 0 — big up-moves' retracements outpace the moves (given-back-fast, as claimed) |
| **FADE (F4)** | CI-upper < 0 — retracements slower than the moves (claim contradicted) |
| **NO EDGE** | otherwise |
| **INCONCLUSIVE** | < 100 events in a family's population (F4 only; F1/F2 populations are ~1.5M bars each) |

Phase 5: see §2 — not implicated by construction.

## 5. Data & bias handling

No new data; same frozen universe and bars as every prior campaign. No
look-ahead: r_t uses closes ≤ t; F4's move and crossing use bars ≤ the
crossing bar. Survivorship: current-constituent universe (documented
bias, brief §5). **Intraday→daily translation, pre-declared and
central:** the claim is about minutes vs hours; daily bars cannot see
intraday duration — daily "speed" is per-bar magnitude, and overnight
gaps register as fast moves. The measurement is the honest daily
adaptation of the claim's *size* structure; it is not a test of intraday
speed. No adjustment is made. A1's null is calibrated (the unconditional
OOS bar-size distribution — no assumed "typical"). Zero bars excluded
and counted. F4's conditioning on retracing events is pre-declared (the
complementary non-retracement result is pre-reg #11 F2).

## 6. Sensitivities — pre-declared, NO verdicts

| # | Sensitivity | Report |
|---|---|---|
| S1 | **Median** |r| per leg + DOWN − UP contrast (skew-robust — bar sizes are highly skewed) | F1/F2 tables |
| S2 | **Candle-sign version**: red bar = close_t < open_t (the trader's vocabulary), body size |close_t − open_t|; same F1/F2 structure | F1/F2 tables |
| S3 | **Per-ticker** F1/F2 contrasts (within-ticker up/down means) + ticker-cluster CI on F2 | tables |
| S4 | **IS-era** (2000–2015) F1/F2 (descriptive — selection era) | F1/F2 tables |
| S5 | Per-year F1/F2 (OOS) | table |
| S6 | **Swing-scale** A1: k=2 fractal swings on Close (strict — ties never form a swing, as pre-reg #10); completed swings; paired contrast down-swing rate (size/duration) − preceding up-swing rate; k=3/5 variants | tables |
| S7 | F4 variants: N = 5 / 20; event population τ = 2 / 5 | F4 tables |
| S8 | **Tail concentration**: the share of the largest-|r| decile of OOS bars that are down-bars, vs the overall down-bar share | table |

## 7. Freeze

Frozen 2026-08-15. Registered against: ledger row I-F-02 (CLAIMS_LEDGER
§I-F); inputs: the frozen S&P 600 universe + bars (Phase-1 dataset, see
data/README.md); no engine call (no forward returns — §3). Measurement
tool: `tools/measure_speed.py`; outputs
`data/cache/speed_measure_results.json` + `data/cache/speed_measure_report.md`.

**Pre-registered expectations (recorded, not hypotheses):** A1's daily
translation is the negative-skew regularity of equity daily returns — a
documented property of the market; honest expectation is that **F1/F2
confirm** (down-bars average larger than up-bars), possibly trivially,
with the interesting quantities being the size of the asymmetry and
whether it concentrates in the tails (S8). A2 is the sharper test: pre-reg
#11 F2 showed big up-moves retrace half *less* often than typical bars —
the population is momentum-driven; among the ~20% that DO retrace within
10 bars, the retracement being faster than the move is plausible but not
certain — expectation: **small positive or null**. Confirmation is a
measurement, not a tradeable edge; and no Phase-5 implication by
construction (§2).

## 8. Campaign outcome

*(Recorded after measurement — parameters unchanged.)*

Measured 2026-08-15; verification completed 2026-08-15. **Split verdict —
A1 (per-bar asymmetry) is falsified in the OPPOSITE direction of the
claim: up-bars are ~6bp LARGER than down-bars (FADE × 3, F1-UP / F1-DOWN
/ F2) — the "window" is not visible at daily per-bar resolution. A2
(reversal speed) is CONFIRMED: when big up-moves retrace, the
retracement outpaces the move (F4 EDGE):**

- **F1-UP FADE**: n=1,371,291 OOS bars (UP 689,944 / DOWN 660,952 / ZERO
  20,395); mean up +0.0189 vs typical +0.0184; excess **+0.0006** (CI
  +0.0005..+0.0006, p<0.001), Holm-rejected (gate 0.025) — up-bars are
  *larger* than typical, the "stairs" half contradicted.
- **F1-DOWN FADE (knife-edge)**: mean down +0.0183; excess **−0.00004**
  (CI −0.00009..−0.00000008, p=0.050 exactly at the Holm gate 0.05) — the
  CI-upper sits at −8e-8 ≈ 0; a boundary artifact of the FADE rule, to be
  treated as NO EDGE substantively (see caveat 4).
- **F2 FADE**: DOWN − UP contrast **−0.0006** (CI −0.0007..−0.0005,
  p<0.001), Holm-rejected — up-bars ~6bp larger than down-bars, the
  asymmetry claim contradicted in sign. The two F1 legs are mechanically
  opposite-signed (the all-bars mean is the legs' weighted average — the
  pre-declared structural note); the interpretable single number is F2's
  −6bp.
- **F4 EDGE**: n=35,997 UP events (the frozen pre-reg #11 population —
  exactly I-F-01's 35,908 measured + 89 tail-dropped); retraced 11,113
  (30.9%), non-retraced 24,795; mean j 5.40 bars; mean contrast
  **+0.0040** per bar (CI +0.0037..+0.0044, p<0.001) — retracements of
  big up-moves outpace the moves themselves: "given back in a matter of
  minutes", confirmed on its daily adaptation.
- **Frequency** (measurement, not a verdict family): OOS bars UP 689,944
  / DOWN 660,952 / ZERO 20,395 / all 1,371,291; down-bar share 0.4820;
  index-0 excluded 599; bad prior 0.

The pre-registered expectation (A1's daily translation "is the
negative-skew regularity of equity daily returns — honest expectation is
that F1/F2 confirm, possibly trivially") was **not met — inverted in
sign**: up-bars average 6bp LARGER than down-bars. The claim's "window" —
a small number of very large fast down-bars — is falsified at the
per-bar level: the top-|r| decile is NOT down-concentrated (down share
0.4795 vs 0.4820 overall, −0.25pp, S8), and the asymmetry is stable
negative across mean/median (S1 −0.0002)/candle-sign (S2 −0.0001)/
per-ticker (S3: 146/599 tickers positive, mean −0.0008, cluster CI
−0.0010..−0.0007)/IS (S4 −0.0014)/per-year (S5: 9/10 OOS years negative,
2018 +0.06pp the only exception). The one structure-level corroboration
is S6: multi-bar down-swings cover distance FASTER per bar than the
preceding up-swings (rate contrast +0.0131/+0.0140/+0.0354 at k=2/3/5,
all p<0.001) — declines are faster *across bars*, without any single
daily down-bar being larger. That is the honest daily reconciliation:
the "window" is a multi-bar property in this data, not a per-bar one.

A2 is confirmed and robust: F4 EDGE at the primary parameters, with the
effect concentrated in the claim's own short horizon (N=5 +0.0113/bar,
p<0.001; N=20 null, p=0.950) and across event-population definitions
(τ=2 +0.0052, n=64,694; τ=5 +0.0034, n=5,416 — both p<0.001). The
equivalence reading is subtle: mean j 5.40 > 5 yet the contrast is
positive, because the per-event contrast is convex in 1/j — the retraced
set's bimodal j distribution (mass at j≈1–2, largely overnight gaps,
and at 6–9) yields mean j > 5 with a positive weighted contrast; this
is distribution shape, not a contradiction of the pre-registered
equivalence. Conditioning is pre-declared: only 30.9% of big up-moves
retrace ≥ half within 10 bars — the complementary non-retracement is
pre-reg #11 F2's FADE (big moves retrace half *less* often than typical
bars); F4 measures speed given the retracement.

Caveats, as pre-declared: (1) the intraday→daily translation is central
— the claim is about minutes vs hours; daily bars measure per-bar
magnitude, and overnight gaps register as fast (they carry much of F4's
j≈1–2 mass); this is the honest daily adaptation of the claim's *size*
structure, not a test of intraday speed — the "window" may still hold
intraday; (2) current-constituent universe (survivorship; the brief §5
positive-result gate does not apply — no forward returns are measured);
(3) F1/F2 are per-bar state-level statistics — iid bootstrap CIs on
serially dependent bars, effective sample below row count; (4) F1-DOWN's
FADE is a knife-edge boundary artifact (CI-upper −8e-8, p=0.050 exactly
at the gate) — treat as NO EDGE substantively; only F1-UP FADE and F2
FADE carry the substantive A1 rejection; (5) F4's effect is conditional
on retracing (30.9% of events) — it says nothing about the 69.1% that
do not retrace.

**Phase-5 trigger (pre-reg §2): no family in this campaign measures
forward returns — the claim is about bar geometry, not profitability;
the Phase-5 trigger cannot fire from this campaign by construction, so
no trigger-check conversation was held.** Phase 5 remains **not
triggered** after twelve campaigns. Verdicts written back to
CLAIMS_LEDGER §I.9; report `data/cache/speed_measure_report.md`
(+ `speed_measure_results.json`). Verification: deterministic (results
1B1DFC00…, report 528E205F…, byte-identical across two runs);
independent implementation, all 75 checks exact — population counts and
per-leg means bit-exact (n_all 1,371,291; mean_all 0.018366437482; down
share 0.4819925165); leg-excess identity holds to 1e-9 including the
zero-bar term (2.732e-04 = n_zero·mean_all/n_all); the F4 population
re-detected with an independent per-bar TR/ATR loop (35,997 events;
n_retraced 11,113, mean_j 5.4031314677, crossing share 0.309485351 all
exact; 148 warm-up OOS events — post-2016-listed tickers — proven
excluded via the warmup flag); S2 candle counts/means; S3 per-ticker
contrasts exact (146/599 positive, mean −0.000842796413); S5 per-year;
S6 swing pair counts exact with analytic-vs-bootstrap means within
Monte Carlo error; S8 tail decile; verdict/Holm-gate consistency; and
every pre-declared sensitivity parity-checked with a fresh seed
(est/CI/p within tolerance); fingerprints exact (measure code
3fbdab9922c5…, universe 5e6f45a3c791…).

# Pre-registration #13 — historical-constituent re-check of the RSI-divergence bullish EDGE (brief §5 survivorship gate; pre-reg #10 §8)

**Frozen 2026-08-15, before any measurement.** No parameters below may be
changed after this date; any change is a new hypothesis requiring a fresh
pre-registration and a fresh evaluation window.

**§1/§3 AMENDED 2026-08-15 (artifact construction evidence; no measurement
performed yet).** The frozen schedule assumed the page carried S&P 600
membership from its creation. Construction disproved that: the page was
created 2018-08-27 as an "S&P 1000" page (S&P 400 + S&P 600 combined) and
kept a 1000-row table until March 2021 — a sloppy list containing ghost
members (delisted names AKRX, AKS, AVP still listed 2021-01-26). The
set-difference reconstruction "S&P 600 = S&P 1000 table − S&P 400 table"
(S&P 400 list page has a clean parallel history) was probed and REJECTED:
validated at 2021-01-26 it yields 755 names vs the 600 real (155 ghosts —
the 1000 table's staleness is uncontrolled, so the reconstruction's
composition cannot be trusted). The page's first true S&P 600 list is the
revision of 2021-03-12 (revid 1011745109, 600 rows). §1/§3 amended
accordingly; everything else (measurement, verdicts, gate rules) unchanged.

## 0. Why this campaign exists (pre-registered context)

Pre-reg #10 measured the I-X-02/03/04 RSI-divergence claims on the
current-constituent S&P 600 universe and found **F1-BULL EDGE** (n=16,985
OOS, mean +0.80%, +0.34pp vs same-ticker, Holm-rejected — the project's
first event-level absolute EDGE). The brief §5 survivorship gate is
explicit: current-constituent backtests see only survivors, and **"any
positive result must be re-checked against (a) [historical constituent
lists] before being trusted"**. Pre-reg #10 §8 recorded the path: "a fresh
pre-registration against historical constituents (§5 option (a), a new data
artifact) before this family can be trusted." This campaign is that
re-check.

## 1. The new data artifact — historical constituents (frozen definition)

Source (brief §5 option (a), first branch — "archived Wikipedia
snapshots"): the Wikipedia article *List of S&P 600 companies*, served
from **the page's own revision history** — the canonical archive (every
revision is immutable and exact-dated, gap-free from page creation).

Feasibility probed 2026-08-15, pre-registered (this is why the artifact is
defined as it is): the dedicated list page has Wayback Machine captures
only from 2022; the S&P 600 main article never carried a constituent table
(probed 2007–2021 snapshots: annual-returns tables only); S&P's own
factsheet/constituent download endpoints have zero Wayback captures;
iShares IJS holdings archives exist only from 2025-11; Morningstar never
captured IJS holdings pages. The list page's revision history (page
created 2018-08-27) is the only gap-free free source of historical S&P 600
membership.

Snapshot schedule (amended, frozen): **5 snapshots** — for each year
2021–2025, the most recent revision dated before Y-07-01T00:00:00Z (the
membership as of June 30 of that year): revids 1030576925 / 1094398428 /
1161531950 / 1231006396 / 1297281645, 601 / 601 / 601 / 602 / 602
tickers. The 2021-03-12 earliest 600-row list is subsumed by the 2021-06
snapshot (it adds only names removed before 2021-06, which have no
OOS-window events). Each snapshot's rendered table is parsed with the
same normalization as `tools/build_universe.py` (`yahoo_ticker`: strip
footnote markers, "." → "-", drop placeholder cells) — the symbol column
is matched as "symbol" **or** "ticker symbol" (the page renamed it
mid-era) — with a row-count sanity gate (550–750) that distinguishes the
S&P 600 table from the S&P 1000-era table, and recorded with its
revision id and timestamp. **The re-check universe = the union of the
five snapshots' ticker sets = 904 names** (2021-06 cohort 601, additions
65 / 83 / 81 / 74 in 2022–2025), including ~330 names delisted or
removed since 2021 — that is the survivorship correction. Churn
validated before freezing: adjacent-year overlaps 536 / 518 / 519 / 528,
2021-06 → 2025-06 survival 344, 2021-06 → 2026-08 survival 274 — a
stable ~64 removals/year, matching the S&P 600's known ~10%/yr turnover;
the residual between-snapshot gap is bounded and documented in §3.

Artifact files (new, tracked): `tools/build_hist_universe.py` (builder),
`data/cache/universe_sp600_hist_2026-08-15.csv` (union universe),
`data/cache/hist_universe_provenance.json` (per-snapshot revision id,
timestamp, ticker count, parse QA). Bars: fetched with the frozen Phase-1
fetcher (`tools/fetch_daily_bars.py --universe <hist csv>`, 2000-01-01 →
2026-01-01, auto_adjust) into the existing `data/cache/bars/` (resumable,
keyed by ticker); delisted tickers fetch like any other name; **fetch
failures are flagged and NOT substituted** (the Phase-1 convention for the
4 no-data names).

## 2. Measurement (identical to pre-reg #10; one pre-registered era change)

The measurement is the **frozen pre-reg #10 code, byte-identical**
(`tools/measure_divergence.py`, sha 85f2ae0d4a1e…; Phase-3 engine
c7421fbf… imported unchanged; measure.py never modified — only
process-local rebinding at runtime). The driver
`tools/measure_divergence_hist.py`:

1. rebinds four module-level inputs before invoking the frozen `main()`:
   - `UNIVERSE_CSV` → the historical-union CSV;
   - `ERA_OOS` → **"2022-01-01"** on **both** `measure.ERA_OOS` (tags the
     engine's `is_oos` rows) and `measure_divergence.ERA_OOS` (the
     frequency function) — the era boundary is the only parameter change,
     forced by the artifact's coverage (§3);
   - `RESULTS` / `REPORT` → `divergence_hist_measure_results.json` /
     `divergence_hist_measure_report.md`.
2. then patches **only** the pre-registered presentation labels (no
   numeric content), each listed verbatim in the tool's docstring:
   JSON `"pre_reg": "#10"` → `"#13"`; JSON `"claim"` → the re-check
   descriptor; the report's header line; the "Pre-registration #10
   (frozen 2026-08-14): …" block; the era-split line ("IS 2000-2015 /
   OOS 2016-2025" → "IS 2000-2021 (descriptive only) / OOS 2022-2025");
   the S6 section header (annotated "descriptive only — no IS-era
   membership data"); and the reproducibility line (`python -X utf8
   tools/measure_divergence_hist.py`).

All frozen parameters carry over unchanged: simple-average RSI period 10
(14 as S3), strict k=2 fractal swings on Low/High, consecutive pairs with
disjoint windows (t2−t1 ≥ 5), signal bar t2+k (confirmation-bar timing, no
look-ahead), N=10, COST 0.0015, bootstrap B=1000 seed 20260813, Holm at
α=0.05 within each family, count floor 100 OOS events per leg, warm-up
guard signal-bar index < 60, 70/30 crossings (pre-reg #9 S4 rule) as the
F2 baseline, and all verdict rules, frequency, and sensitivities S1–S8
identical.

## 3. Era handling (pre-registered, forced by the artifact)

The artifact's membership data covers the five snapshots 2021-06-30 …
2025-06-30 (the earliest true S&P 600 list, 2021-03-12, is subsumed —
§1). The re-check measures with **OOS = signal date ≥ 2022-01-01 through
2025-12-31** (4 years) — every OOS month is bracketed by a snapshot on
each side, and the 2021-07..2021-12 half-year (which would rest on a
single trailing snapshot) is excluded to keep the window conservative.
Consequences, pre-registered:

- **All verdicts (F1, F2, frequency) are computed on the 2022–2025 OOS
  window.** The 2016–2021 OOS years are NOT measured: tickers removed
  before the first snapshot are absent from the union, so those years
  would re-introduce the very survivorship bias this gate exists to
  remove. The 2016–2021 blind spot is a documented residual limitation.
- **Residual membership gap:** a name joining and leaving between two
  consecutive snapshots appears in no snapshot and is absent from the
  union. Bounded by the validated ~64 removals/year churn — at most a
  few dozen names per year, and only for events strictly inside their
  ~1-year window.
- **IS (2000–2021) statistics are reported descriptively only (S6), NOT
  as verdicts**: the union universe has no IS-era membership data, so its
  IS rows are biased by construction. Nothing in the IS block can carry a
  verdict in this campaign.
- The count floor (100 OOS events per leg) applies to the 2022–2025
  window.

## 4. Verdicts (identical rules to pre-reg #10, applied on the re-check window)

**F1 (absolute, directional per leg)** — OOS mean forward return of the
leg vs era-matched baselines (random entries −COST, same-ticker −COST,
SPY raw); p_input = max(p_rand, p_same), est = max, ci_low = min, ci_upper
= min; Holm across BULL/BEAR:

- **F1-BULL**: EDGE iff Holm-rejected AND excess CI-low > 0 (bounce, as
  claimed); FADE iff Holm-rejected AND CI-upper < 0; NO EDGE otherwise.
- **F1-BEAR**: EDGE iff Holm-rejected AND excess CI-upper < 0 (pullback,
  as claimed); FADE iff Holm-rejected AND CI-low > 0; NO EDGE otherwise.

**F2 (reliability contrast, I-X-02)** — divergence minus 70/30 crossings
at the same period, per leg on (a) mean forward return and (b) hit rate
(ret > 0 after cost); two-sample bootstrap; Holm across the four tests.
BULL-mean / BULL-hit: EDGE iff CI-low > 0; FADE iff CI-upper < 0.
BEAR-mean / BEAR-hit: EDGE iff CI-upper < 0; FADE iff CI-low > 0.

**Frequency** (measurement, not a verdict family): OOS counts + ratio +
ticker-cluster CI, at periods 10 and 14.

## 5. Pre-declared expectations and gate decision rules

Direction: survivorship inflates returns, so the EDGE may shrink or vanish
on the historical union. Both outcomes are informative.

- **F1-BULL EDGE** on the re-check window (Holm-rejected, CI-low > 0,
  floor met) → the §5 gate is **PASSED**: the positive result survives
  re-check against historical constituents; the Phase-5 trigger-check
  conversation is then held with the surviving evidence (the last
  pre-registered gate for I-X-03).
- **F1-BULL NO EDGE or FADE** → the gate **FAILS**: I-X-03's EDGE is
  corrected to the survivorship-resilient record; the family is closed
  with the re-check as definitive; Phase 5 stays untriggered.
- **F1-BULL INCONCLUSIVE** (count floor on the restricted window) → the
  gate is **UNMET** with a documented data limitation; Phase 5 stays
  untriggered.
- F1-BEAR and F2 are re-recorded on the re-check window (the bearish leg
  was NO EDGE / F2-BEAR-mean FADE on the current universe; the re-check
  records whether that holds).

## 6. Data & bias handling (§7 checklist)

- **Look-ahead:** unchanged frozen rules (signal at close t2+k, entry
  open t2+k+1).
- **Survivorship:** this campaign IS the §5 gate; the residual 2016–2018
  OOS blind spot and IS-out-of-scope are documented in §3.
- **Costs:** identical COST 0.0015 on every measured trade.
- **Multiple testing:** identical Holm families; nothing new tested.
- **Non-stationarity:** per-year S5 on the re-check window; the era
  boundary change is pre-registered here, not tuned.
- **Data quality:** revision snapshots are exact-dated and immutable;
  delisted names flagged on fetch failure (not substituted); artifact QA
  shipped with the provenance record; determinism check (two runs,
  byte-compare) and an independent verification pass before write-back.

## 7. Freeze

The artifact definition (§1), measurement rebinding and label patch list
(§2), era handling (§3), verdict rules (§4), and gate decision rules (§5)
above are frozen as of 2026-08-15, before any measurement. Implementation
must not change any of them.

## 8. Campaign outcome

*(Recorded after measurement — parameters unchanged; gate outcome per §5.)*

Measured 2026-08-15, verified 2026-08-16. **The §5 gate FAILS: the
F1-BULL EDGE does not survive the survivorship-corrected universe.** The
claim's direction persists qualitatively but is no longer distinguishable
from chance on the re-check window:

- **F1-BULL NO EDGE** (the gate test): n=9,384 OOS (2022–2025, 4 years);
  mean +0.59%; win 50.98%; excess vs random +0.43pp (CI −0.10..+0.81,
  p=0.064), vs same-ticker +0.49pp (CI −0.15..+0.87, p=0.072); p_input
  0.072, est +0.49pp, CI-low −0.15pp < 0 — the Holm gate 0.025 is not
  reached.
- **F1-BEAR NO EDGE**: n=9,656; mean −0.12%; win 47.06%; excess vs random
  −0.30pp (CI −0.81..+0.05, p=0.106), vs same-ticker −0.38pp (CI
  −1.03..−0.05, p=0.024); p_input 0.106 — the per-ticker underperformance
  is raw-significant but not Holm-significant (gate 0.050).
- **F2-BEAR-hit EDGE** (re-recorded; F2 carries no gate rule): contrast
  −1.35pp (CI −2.41..−0.31, p=0.012, Holm gate 0.0125) — bearish
  divergence hits positive *less* often than overbought crossings:
  "more reliable" in the claimed direction on the bearish side, on the
  re-check window. F2-BULL-mean NO EDGE (+0.14pp, p=0.492),
  F2-BULL-hit NO EDGE (+0.83pp, p=0.140), F2-BEAR-mean NO EDGE (−0.10pp,
  p=0.410).
- **Frequency** (measurement, not a verdict): n_div=19,207 vs
  n_cross=63,763 → ratio **0.3012** (ticker-cluster CI 0.2972..0.3052) —
  "a lot less common" holds on the historical union; period-14 ratio
  0.4286 (consistent with pre-reg #10's 0.4287).

**Gate decision (per §5): FAILS.** F1-BULL NO EDGE → **I-X-03's EDGE is
corrected to the survivorship-resilient record: the claim's direction
survives qualitatively (est +0.49pp vs same-ticker; all four OOS years
positive — 2022 +0.48pp, 2023 +0.27pp, 2024 +0.86pp, 2025 +0.82pp) but
is not statistically distinguishable from chance on the 4-year /
904-name window. The family is closed with the re-check as definitive;
Phase 5 stays untriggered.** No trigger-check conversation is held —
per §5, it is reserved for a surviving EDGE.

Why it moved: the re-check window halves the pre-reg #10 sample
(n=16,985 → 9,384) and era-matches the baselines to 2022–2025 only,
roughly doubling the confidence interval; the pre-registered §5 direction
(survivorship inflates returns) is consistent with the outcome — the
current-constituent excess (+0.34pp, CI-low +0.11pp) does not clear zero
on the corrected universe, though its point estimate does not collapse
either. The 2016–2021 OOS blind spot (§3) is a documented residual
limitation: the corrected record rests on 2022–2025.

Exploratory sensitivities (no verdicts): S2 k=3 BULL +0.63pp vs same
(p=0.046) and S4 min-sep 10 BULL +1.12pp (p=0.016) echo the direction;
S8 chartist's-eye BULL +2.22pp (p=0.034) shows the pre-declared selection
tilt present as pre-registered (the primary's confirmation-bar timing is
the honest number); S1 N=20 BULL +0.75pp (p=0.082), BEAR −0.70pp
(p=0.000); S3 period 14 BULL NO EDGE (p=0.208), BEAR vs same −0.55pp
(p<0.001); S7 extreme-gated BULL +0.54pp (p=0.092).

**Data limitation (pre-registered §6, materialized):** of the 904-name
union, **199 former-member tickers are purged from Yahoo's data
entirely** — the chart API 404s ("No data found, symbol may be delisted")
at every window and the search API finds nothing for representative
purged names (Foot Locker FL, Civitas CIVI, American Woodmark AMWD;
CSWI was re-tickered to CSW). Verified NOT throttling: a 45-minute
per-minute probe never recovered a single name. **None of the 199 are
current S&P 600 members.** Measurement ran on the 706 names with bars;
the 199 are flagged and NOT substituted, per §6. The 706-name universe
includes 229 sibling former members (AAON, ADC, ANF, …) that still
serve, so the survivorship correction is partial — the gate's direction
(missing delisted names understate the correction) is documented here.

Determinism: two runs byte-identical (results 45d6ebe9d882…, report
125ad2af14d5…). Independent verification (from-scratch implementation,
imports nothing from the frozen stack): BULL n=9,384 exact; mean_ret
0.005930043180491732 exact to 1e-8; excess vs same-ticker 0.00493
(driver 0.00490) and vs random 0.00393 (driver 0.00431), both within
6e-4 of the driver's bootstrap means; the driver's CI-low −0.0015 lies
within the verifier's own CI ±1.5e-3 — **PASSED**. Input fingerprints:
universe 62f681d58cdb…, measure code 85f2ae0d4a1e… (Phase-3 engine
c7421fbf… imported unchanged — no frozen file was modified). Report:
`data/cache/divergence_hist_measure_report.md`
(+ `divergence_hist_measure_results.json`). Verdicts written back to
CLAIMS_LEDGER §I.7 (superseded-by note) and §I.10 (re-check table).

---

# Pre-registration #14 — I-X-05 stop placement: "the market shouldn't take out that prior extreme low" (ledger row I-X-05)

**Frozen 2026-08-16, before any measurement.** No parameters below may be
changed after this date; any change is a new hypothesis requiring a fresh
pre-registration and a fresh evaluation window.

## 1. Translation — claim as stated → as measured

| Claim as stated | Source | Translation (as measured) |
|---|---|---|
| "good thing with the divergence... we have two higher lows so if we're buying because there's bullish divergence we have two obvious levels to place our stop loss beyond because by definition if the divergence is going to work out bullish divergence the market shouldn't take out that prior extreme low so we have a very sensible point I think to place the stop-loss so potential low risk but a potential high reward trade" | rgVdgR1y1Dg [07:40–08:03] (Trading 212) | **The stop-placement claim, measured on the frozen pre-reg #10 bullish-divergence event set.** For each BULL event (signal bar s = t2+k — the confirmation bar; the divergence's two swing lows at t1 < t2, with Low[t2] < Low[t1] and RSI[t2] > RSI[t1]), the "prior extreme low" = **Low[t2]** (the pair's second, lower low — the level the chartist places the stop beyond). The claim: after the signal, the market should not take out that prior extreme low. Measured as the **breach rate** — the fraction of events with min(Low[s+1..s+N]) < Low[t2] (intrabar low trades *beyond* the level, the way a stop placed beyond the low triggers) — vs era-matched baselines, and vs the 70/30 oversold crossings (the alternate bounce signal). The second "obvious level" (Low[t1], the pair's first, higher low) is sensitivity S2. The "low risk, high reward" half is a measurement row (stop distance + outcome decomposition), NOT a verdict family. |

## 2. Measurement

- **Events**: the frozen pre-reg #10 bullish-divergence detection, unchanged —
  simple-average (Cutler) RSI period 10; strict k=2 fractal swings on Low;
  consecutive swing pairs, t2 − t1 ≥ 5; BULL condition (Low[t2] < Low[t1]
  AND RSI[t2] > RSI[t1], both RSI finite); signal bar s = t2 + k
  (confirmation-bar timing — the fractal is only knowable at close t2+k, no
  look-ahead); warm-up guard s < 60. The tool recomputes the detection with
  the FROZEN detection functions (`measure_divergence.swing_idx`,
  `measure_divergence._pair_events` — the module's sha is asserted at
  import, nothing modified) and asserts per-leg all-era event counts equal
  the frozen pre-reg #10 JSON's `sensitivities.per_year` sums — the event
  set is the #10 event set by construction.
- **Stop level**: L = Low[t2] (primary). Breach window: bars s+1 .. s+N
  (entry open s+1 through exit close s+N — the frozen forward-return
  window). Breach ⇔ min(Low[s+1..s+N]) < L (a stop placed "beyond" the low
  triggers when price trades strictly below it; an equal low survives).
- **N = 10** primary (house). S1: N = 5 / 20.
- **F1 (absolute — the claim's core)**: BULL breach rate vs era-matched
  baselines:
  - *random (whole universe)*: every OOS confirmation bar c = f + 2 of every
    strict k=2 fractal low f in the universe (warm-up c ≥ 60; c + N beyond
    the series end dropped and counted), reference Low[f], breach ⇔
    min(Low[c+1..c+N]) < Low[f]; rate = breached / pool size. The fractal-low
    confirmation bar is the divergence event's own geometric template minus
    the divergence condition — same structure, same 2-bar age of the
    reference level. The pool EXCLUDES the divergence event bars: the
    comparison is "the divergence condition adds value over the same low
    without it".
  - *same-ticker*: the same baseline restricted to the event tickers, bars
    weighted by per-ticker BULL event counts (the frozen make_sample_same
    convention).
  - Contrast = event rate − baseline rate via paired bootstrap (B=1000,
    seed **20260816**): resample M events with replacement → rate; resample
    M baseline bars (ticker-weighted for same-ticker, uniform for random) →
    rate; contrast over B draws → (est, ci_low, ci_high, p_two_sided).
    p_input = max(p_rand, p_same), est = max, ci_low = min, ci_upper = min.
    Holm at α=0.05 across the F1 family (a single test → gate 0.05).
  - **EDGE** iff Holm-rejected AND CI-upper < 0 (the low holds better than
    typical lows — the claim); **FADE** iff Holm-rejected AND CI-low > 0
    (taken out *more* often — the claim contradicted); NO EDGE otherwise.
    Count floor 100 OOS events.
- **F2 (contrast vs the alternate bounce signal)**: OS crossings (the frozen
  pre-reg #9 S4 rule — first bar of each RSI<30 excursion, period 10;
  `measure_divergence.cross_frame`, sha-asserted). For crossing bar c,
  reference = the most recent strict k=2 fractal low at bar ≤ c within the
  60-bar lookback (crossings without one are dropped and counted); breach ⇔
  min(Low[c+1..c+N]) < reference. Contrast = divergence rate − crossing
  rate, same bootstrap. **EDGE** iff Holm-rejected AND CI-upper < 0
  (divergence lows hold better than crossing references); gate 0.05. *Age
  asymmetry documented:* the divergence reference is exactly 2 bars old; a
  crossing's reference averages older, and older levels are less likely to
  be breached — a conservative direction for the claim.
- **Measurement rows (no verdicts)**: stop distance (open[s+1] → Low[t2],
  mean/median/percentiles, % and in 14-bar ATR units); breach-loss (the
  entry → Low[t2] return when breached); continue-gain (mean N-bar return −
  COST when NOT breached); combined expected outcome = (1−br)·continue +
  br·loss; the same decomposition on the same-ticker baseline for
  comparison; per-year breach rates (all years reported, 2016–2025 the
  verdict rows).
- **Era**: OOS by signal date ≥ 2016-01-01 (the frozen `measure.ERA_OOS`;
  house standard); IS 2000–2015 descriptive only. Universe and bars: the
  frozen pre-reg #10 inputs (S&P 600 current constituents,
  universe_sp600_2026-08-13.csv, cached bars) — unchanged.
- **Integrity**: the tool sha-asserts `measure.py` (c7421fbf…) and
  `measure_divergence.py` (85f2ae0d4a1e…) at import; the event-set anchor
  (§2, per_year sums); determinism check (two runs, byte-compare) and an
  independent verification pass before any write-back.

## 3. The §5 survivorship gate (pre-registered within this campaign)

The brief §5 rule — "any positive result must be re-checked against (a)
[historical constituents] before being trusted" — is pre-registered here
so the re-check needs no separate campaign:

- **If F1-BULL is EDGE on the primary** (current constituents, 2016–2025):
  the SAME measurement is re-run against the pre-reg #13
  historical-constituent union (904 names, 5 annual S&P 600 snapshots
  2021–2025; bars present for 706 — 199 former members are purged from
  Yahoo's data, 0 of them current members, flagged and NOT substituted;
  OOS 2022–2025, the only era the artifact covers) with `measure.ERA_OOS`
  rebound to "2022-01-01". **Gate PASSED** iff F1-BULL EDGE survives on the
  corrected window (Holm-rejected, CI-upper < 0, floor met) → the
  Phase-5 trigger-check conversation is then held with the surviving
  evidence. **Gate FAILS** (NO EDGE or FADE on the corrected window) → the
  claim is corrected to the survivorship-resilient record and the family is
  closed with the re-check as definitive; Phase 5 stays untriggered.
- **If F1-BULL is NOT EDGE on the primary**: the campaign ends as NO EDGE /
  FADE; no re-check is needed (the brief gates only positive results) and
  none is run.
- **INCONCLUSIVE** (count floor on either window) → the gate is UNMET with
  a documented data limitation.

## 4. Pre-declared expectations

- **F1**: divergence lows are structural levels selected by the pattern —
  expect the breach rate at or below the fractal-low baseline, but small in
  magnitude. The claim's own "by definition" phrasing overstates the
  reliability; a modest, possibly null, effect is the honest expectation.
  Pre-reg #10's BULL events averaged +0.80% post-signal after cost on this
  universe, so the lows demonstrably hold often enough for a positive
  average trade — but that does not imply the rate beats the fractal-low
  baseline.
- **F2**: the same, vs crossings — small or null.
- **Gate**: the same survivorship caution as #13 — if the primary is
  positive, the re-check may fail it.

## 5. Data & bias handling

- **Look-ahead**: the event set and the stop level are fully knowable at
  the signal close (t2+k); the breach is measured after entry. No
  look-ahead.
- **Survivorship**: the §5 gate is pre-registered within this campaign
  (§3) — a positive primary triggers the historical-constituent re-check.
- **Costs**: COST 0.0015 enters the continue-gain / outcome measurement
  rows; breach rates themselves are cost-free.
- **Multiple testing**: two verdict families (F1 single test, F2 single
  test), Holm at α=0.05; all sensitivities exploratory.
- **Non-stationarity**: per-year breach rates (measurement row).
- **Data quality**: frozen bars; the 199 purged names flagged not
  substituted in the gate run; determinism + independent verification
  before write-back.

## 6. Freeze

§1–§5 are frozen as of 2026-08-16, before any measurement. Implementation
must not change any of them. §8 will record the campaign outcome.

## 8. Campaign outcome

*(Recorded after measurement — parameters unchanged; gate outcome per §3.)*

Measured 2026-08-17, verified 2026-08-18. **F1-BULL EDGE on the primary
AND the §5 gate PASSES** — the first claim whose EDGE survives the
historical-constituent re-check. The stop-placement claim — after a
bullish divergence "the market shouldn't take out that prior extreme
low" — is supported on both windows, on both verdict families:

- **F1-BULL EDGE (primary)**: n=16,984 OOS (2016–2025); breach rate of
  Low[t2] within N=10 = 47.54% vs 52.99% (random pool 165,376) and
  53.28% (same-ticker) → excess −5.46pp (CI −6.47..−4.44, p=0.000) and
  −5.71pp (CI −6.75..−4.66, p=0.000); p_input 0.000, est −5.46pp,
  CI-upper −4.66pp < 0 — Holm 0.05 cleared. The prior extreme low is
  breached substantially LESS often than typical fractal lows: the
  claim's "shouldn't" is supported (excess is negative in the claimed
  direction — breached less often).
- **F2-BULL EDGE (primary)**: contrast vs OS crossings −28.56pp (CI
  −29.58..−27.58, p=0.000) — divergence lows hold far better than
  oversold-crossing references (the crossing reference's age asymmetry
  is documented conservative, §2).
- **§5 gate (pre-registered §3)**: re-run on the historical-constituent
  union (904 names, 706 with bars; OOS 2022–2025). ALL event-set anchors
  PASSED — the frozen #13 record regenerates byte-exact (per_year BULL
  42,495 / BEAR 52,057; fam1 n 9,384; freq 9,433/9,774; drops 49/118;
  n_os 31,892; drops_cross 383). **F1-BULL EDGE**: n=9,384; breach
  50.53% vs 55.37% / 56.20% → excess −4.82pp (CI −6.28..−3.43, p=0.000)
  and −5.70pp (CI −6.98..−3.58, p=0.000) — **EDGE survives**. F2-BULL
  EDGE −26.87pp (CI −28.20..−25.62, p=0.000).

**Gate decision (per §3): PASSED.** The F1-BULL EDGE is
survivorship-resilient on the breach-rate measure — distinct from pre-reg
#13's mean-return gate (I-X-03 FAILED): the stop-level property holds on
the corrected universe even though the mean forward return does not. The
Phase-5 trigger-check conversation is held with the surviving evidence
(§3): **held, NOT TRIGGERED** — the finding is a risk-placement property
(where the "obvious" stop sits and how often it is hit), not a tradeable
signal: no entry/exit construction, no per-trade size, and the divergence
events themselves were already gated null on the mean-return re-check
(#13). Practical read: the stop below the prior extreme low is a
genuinely tight, rarely-hit level relative to typical fractal lows — a
defensive placement property, not an alpha source.

**Data-integrity note (recorded, quantified, guarded — the frozen #10
record is not regenerable on the current bars):** §2 anchors the event
set to the frozen pre-reg #10 record. On the current bars the frozen
pipeline — and md.main() itself, run with outputs rebound and shas
asserted — yields per_year BULL 34,075 / BEAR 42,757, fam1 BULL n
16,984, freq n_bull 17,016 / n_bear 20,910 vs the frozen 34,076 /
42,759 / 16,985 / 17,017 / 20,912: a 3-divergence-event, 1-OB-crossing
delta across 5 year-legs (2021 BULL −1; 2016/2017/2024 BEAR −1; 2025
BEAR +1). The frozen #13 hist record regenerates exactly on the same
data, bracketing the change to the 08-15 → 08-16 window (vendor
restatement of the bars); the 08-13-era bytes are unrecoverable
(fetch_log.json records only rows/dates — no hashes; no raw downloads
exist). The deviation is recorded in the results JSON (`anchor` block)
and guarded by a drift-materiality bound (1.9e-4, ~60× below the
bootstrap CI width; the OOS BULL set under test differs by exactly 1
event); a verdict is flagged drift-sensitive only if a decisive CI bound
falls within the bound — neither family's does. This is a data-state
deviation, NOT a parameter change; no frozen file was modified.

Measurement rows (primary): stop distance open[s+1] → Low[t2] mean 5.28%
(median 4.24%, p10 1.30%, p90 10.30%) = 1.40 ATR14 units (median 1.28);
outcome decomposition (events): breach-loss −3.66%, continue-gain
+4.55%, combined +0.64% (n_breached 8,075); same-ticker baseline
breach-loss −4.50% / continue-gain +0.39% / combined +0.36%; random
baseline −4.47% / +0.25% / +0.32%. IS record (descriptive) n=17,091,
breach 46.37% vs OOS 47.54%. All 26 per-year breach rates below the OOS
random baseline (0.37–0.52).

Exploratory sensitivities (primary; no verdicts): S1 N=5 0.359 vs
0.403/0.405, N=20 0.595 vs 0.647/0.650 — the edge persists at both
horizons; S2 stop = Low[t1] 0.728 vs 0.530/0.533 — the older, shallower
low is breached far more often; the claim's t2 choice is the tight one;
S3 period 14 0.473 vs 0.530/0.533; S4 close-based breach 0.372 vs
0.414/0.417; S5 BEAR mirror 0.892 vs 0.587/0.590 — the bearish mirror
(the divergence high) is taken out in ~89% of cases (exploratory; no
bearish stop claim was pre-registered). Gate sensitivities: consistent
directions throughout (N=5 0.375, N=20 0.638, S2 0.749, S3 0.508, S4
0.405, S5 0.904 — each below its baselines).

Determinism: primary two runs byte-identical (results 1162e0c54457…,
report 11f7beb09d19…); gate two runs byte-identical (results
b761dfa9cfe2…, report 35a8b49ca7e2…). Independent verification
(from-scratch implementations importing nothing from the frozen stack,
fresh seeds 20260817/20260818): primary — BULL n=16,984 exact, breach
0.4754474799811587 exact to 1e-16, baseline rates exact, bootstrap
excess points within 6e-4, driver CI-upper within the verifier CI
±1.5e-3, F2 n_cross/rate exact — **PASSED**; gate — n=9,384 exact,
rates exact, excess points within the data-derived 3σ MC bound —
**PASSED**. Input fingerprints: universe 5e6f45a3c791… (primary) /
62f681d58cdb… (gate), measure code a9ccedd16386…, engine c7421fbf…
imported unchanged. Reports:
`data/cache/stop_placement_measure_report.md`
(+ `stop_placement_measure_results.json`) and
`data/cache/stop_placement_gate_measure_report.md`
(+ `stop_placement_gate_measure_results.json`). Verdicts written back to
CLAIMS_LEDGER §I.11.

# Pre-registration #15 — B-01 micro pullback on 1-minute bars: "the first candle that makes a new high versus the high of the previous candle" (ledger row B-01; secondary rows B-02/I-E-02; intraday track)

**Frozen 2026-08-19, before any measurement.** No parameter below may be
changed after this date; any change is a new hypothesis requiring a fresh
pre-registration and a fresh evaluation window. The measurement window
opens only when §5's floors are met; the archive bar-dates before this
freeze (2026-08-12…18, the 6-ticker test cycle) are excluded by §2.

## 0. Why this campaign exists

The intraday accumulation track (PR #1, merged 2026-08-19) exists to test
the ledger claims stated on 1-minute charts. B-01 is the corpus's single
most machine-testable rule — its own ledger row says so — and it is the
track's first campaign. Its daily adaptation (Shape B: pullback + new
high) was measured and **rejected** 2026-08-13 (§B.5-B: NO EDGE,
significantly below baselines); the rule **as actually stated** — on 1-min
bars, with a ≥2-red-candle pullback, a double bottom, and entry on the
first candle making a new high versus the previous candle — has never been
measured. This campaign measures it, plus the two claims it embeds by
construction: B-02 ("better to wait for the stock to pull back" — pullback
entries vs chasing the breakout) and I-E-02 ("chasing… doesn't work" —
new-high chasing fails). F-01 (7–10 a.m. window) and F-02 (pre-market
cleanliness) are unverifiable on daily bars; the campaign measures their
factual basis as descriptive rows.

## 1. Translation — claims as stated → as measured

| Claim as stated | Source | Translation (as measured) |
|---|---|---|
| **B-01**: stock squeezes up (green candles), pulls back (confirmed by ≥2 red candles), bounces forming a double bottom; **entry = the first candle that makes a new high versus the high of the previous candle**; stop = low of the pullback; profit target = retest of the high of day; wants ≥2:1 reward:risk ("I always want to retest a high of day… when this setup works it goes to the high of day") | warrior-trading [1:28:40–1:31:18] | **The detector of §3, per bar-date file, RTH (09:30–16:00 ET).** Entry signal bar e: first bar after a ≥2-red-candle pullback (with double bottom) whose High exceeds the previous bar's high. Stop S = low of the pullback. Target T = the day's high so far (max High from day open through e). F1: mean N-bar forward return (entry open e+1, exit close e+N, COST deducted) vs hour-matched same-ticker and random-universe baselines. F2: the HOD-retest reach rate — fraction of events where max(High[e+1..session close]) ≥ T — vs the same baselines' retake rate of their own day-high-so-far. Measurement row (no verdict): the ≥2:1 geometry, (T − O[e+1])/(O[e+1] − S). |
| **B-02**: "if I bought right here, what would be my max loss?… it's really far away… my profit target has to be two times that… it's better to wait for the stock to pull back" (don't buy the breakout move itself) | warrior-trading [1:29:17–1:29:40] | **F3: the pullback-vs-chase contrast.** Chase events = every run-up bar c (run-up as defined in §3, no pullback) with High[c] > High[c−1] — the breakout-chase entries. Contrast = mean N-bar return of B-01 events − mean N-bar return of chase events, same bootstrap. The pre-registered verdict row for B-02 ("waiting beats chasing") and I-E-02 ("chasing doesn't work"): EDGE iff B-01 events beat chase events on both slots. |
| **I-E-02**: "I personally have high a day scanners but I don't find it to be a successful strategy just to buy a stock because it's hitting high a day… it doesn't work" | txWaMpSzHhM [24:19–24:40] | Same F3 row (chase leg). Consistent with the measured daily analog: Shape B (new-K-day-high after pullback) NO EDGE, below baselines (§B.5-B). |
| **F-01**: best trading window 7–10 a.m. ET — "peak volatility and peak liquidity" | warrior-trading [1:44:58–1:47:07] | **Measurement row (no verdict):** per hour-of-day bucket (ET) across the archive: mean \|r\| per bar, mean (H−L)/O, volume share. The claim is read against the 07–10 bucket's ranks, volatility AND liquidity jointly. |
| **F-02**: pre-market moves are "typically cleaner" (no halts, no circuit breakers 4–9:30 a.m.) | warrior-trading [1:45:30–1:46:32] | **Measurement row (no verdict):** pre-market (04:00–09:30 ET) vs RTH (09:30–16:00): per-bar \|r\| mean/median, tail frequency (\|r\| > 3× the file's median \|r\|), volume share. "Cleaner" read = lower per-bar volatility and rarer tail bars pre-market. Halts/circuit breakers are not directly observable from bars — proxy documented. |

## 2. The data artifact — the forward-accumulated 1-minute archive

- **Archive** (data/intraday/README.md): immutable (bar-date, ticker)
  parquet files, tz-aware America/New_York, minute-floored, unadjusted
  OHLCV, extended hours 04:00–20:00 ET, LFS-tracked; manifest.json is the
  SHA-256 ledger with a self-validating pull chain; repairs.json records
  every deliberate deletion; the nightly pull is blind full-universe
  (Task Scheduler 22:05 MT, `--qa`).
- **Universe per bar-date**: the pull takes the whole membership CSV every
  run and records the file + its SHA in the pull record. A name is
  measurable on a bar-date **iff** it is in that bar-date's pull-record
  universe. A membership change creates a new `universe_sp600_<date>.csv`;
  the frozen snapshot is never edited.
- **Excluded bar-dates**: 2026-08-12…18. The test cycle first captured
  6 hand-picked tickers (not the universe file); at 2026-08-19 06:19 MT —
  before this freeze — the full universe was blind-captured for those
  bar-dates as well (pull `20260819-121942`: 603 tickers, 3,000 files,
  universe `5e6f45a3…`), so the bar-dates are no longer test-only. They
  **remain excluded**: captured before this freeze, and the measurement
  window is bar-dates ≥ 2026-08-19 by §5's date rule. A recorded test pull
  (`20260819-052855`, `bad_universe.csv`, 0 files written) is retained as
  audit evidence. The 6 test-cycle names outside the universe file (AAPL,
  MSFT, SPY) are not measurable on any bar-date (the per-pull universe
  rule above).
- **Splits**: OHLCV is unadjusted; a recorded split (splits.json) falling
  inside a measured (ticker, bar-date) excludes that name-day, counted.
- **Sparsity reality**: Yahoo 1m emits a bar only when a trade prints —
  thin S&P 600 names show real RTH gaps. Detection runs on stored bars
  as-is (each stored bar is the tradable bar at its timestamp); the
  gap distribution at entry is a measurement row, and sensitivity S-GAP
  requires detection bars ≤ 2 min apart.

## 3. The detector — B-01 on 1-minute bars (frozen)

Per (bar-date, ticker) file, RTH bars only (primary; S-WIN:
07:00–10:00 ET, his stated best window):

- UP bar: Close > Open. DOWN bar: Close < Open. Others: neither.
- **Run-up**: R = 3 consecutive UP bars (S-R4: R = 4; S-R2: R = 2). Run-up
  high H = max(High of the run-up bars).
- **Pullback**: P = 2 consecutive DOWN bars immediately after the run-up
  ("confirmed by ≥2 red candles"; S-P3: P = 3). Pullback lows L1 (first
  DOWN bar), L2 (second DOWN bar). **Double bottom** (primary, required):
  L2 ≥ L1 — the second test does not break the first. Stop S = min(L1, L2)
  = L1 under the primary rule. (S-DB: no double-bottom requirement.)
- **Entry signal bar e**: the first bar after the pullback with
  High[e] > High[e−1] — "the first candle that makes a new high versus the
  high of the previous candle". All detection state (run-up, pullback,
  double bottom) is complete at the close of e−1; only High[e] vs High[e−1]
  completes at e. Entry = open of e+1 (house protocol; no look-ahead).
- **Target T** = max(High[day open .. e]) — the day's high so far (the
  run-up's high if the run-up made it; an earlier day high if not — either
  way, the retest level of the claim).
- **Validity**: e+1 must exist within the session; events with e+N beyond
  the last RTH bar are dropped and counted (house).

## 4. Measurement

All bootstraps B = 1000, seed **20260819** (freeze date). Three verdict
families; each slot is a contrast; Holm at α=0.05 within each family.

- **F1 (absolute forward returns — does the entry have edge?)**: forward
  return = (C[e+N] − O[e+1]) / O[e+1] − COST, N = **60** primary (one
  hour; S-N15: 15; S-N120: 120; S-N240: 240). Baselines (same convention,
  COST deducted):
  (a) *same-ticker hour-matched* — random RTH bars c in the same (bar-date,
  ticker) file, matched to the event's hour-of-day bucket (ET), c+N within
  the session, pool excludes event entry bars; (b) *random-universe
  hour-matched* — same across all files in the archive. EDGE iff both
  slots Holm-rejected with CI-low > 0; FADE iff both rejected with
  CI-upper < 0; mixed or unrejected → NO EDGE. Count floor 100.
- **F2 (the claim's geometry — the HOD retest)**: reach rate = fraction of
  events with max(High[e+1 .. session close]) ≥ T. Baseline (same-ticker,
  then random-universe): random RTH bars c with day-high-so-far
  T_c = max(High[day open..c]), reach = fraction with
  max(High[c+1..end]) ≥ T_c, hour-matched. Same contrast/bootstrap/EDGE
  rules as F1 (positive direction: setups retest the day's high more often
  than typical minutes). Floor 100.
- **F3 (B-02/I-E-02 — pullback vs chase)**: chase events = every run-up
  bar c with High[c] > High[c−1] (RTH, same files). Contrast = mean N=60
  return of B-01 events − mean of chase events, paired bootstrap
  (resample M events from each pool per draw). EDGE iff both slots
  (same-ticker pairs, then universe-wide pools) Holm-rejected with
  CI-low > 0 (waiting beats chasing); FADE iff CI-upper < 0; mixed → NO
  EDGE. Floors 100 per leg.
- **COST**: 0.15% round-trip (house, §6 protocol) on every return —
  deliberately the daily-tier cost; on 1-min bars it is a strict bar.
  S-C05 0.05% (intraday tier) and S-C30 0.30% are pre-declared
  sensitivities, NO verdicts.
- **Measurement rows (no verdicts)**: (a) the ≥2:1 R:R geometry —
  (T − O[e+1])/(O[e+1] − S), distribution and fraction ≥ 2.0; (b) name-day
  collapse — F1 means per (ticker, bar-date) (event-level multiplicity is
  correlated within a name-day; the collapsed row shows the verdict
  direction at the independent-unit level); (c) entry-bar gap distribution
  (sparse names); (d) F-01 time-of-day profile and (e) F-02 pre-market vs
  RTH (both per §1); (f) per-bar-date and per-ticker F1 breakdowns (the
  archive accumulates whatever regimes come next — every measured bar-date
  is reported; no year aggregation exists for a forward archive).
- **Era**: no IS/OOS split by date exists for a forward archive — the
  whole measured window is OOS-by-construction (everything post-freeze).

## 5. When measurement may begin (floors) — and the one-shot rule

- The measurement window is the complete full-universe bar-dates ≥
  2026-08-19. All floors must hold at the first measurement: (a) ≥ 20
  full-universe bar-dates; (b) ≥ 2,000 F1-evaluable events; (c) events
  across ≥ 100 distinct tickers; (d) events across ≥ 15 distinct
  bar-dates.
- **One-shot rule**: verdicts are recorded at the FIRST measurement meeting
  all floors. There is no second measurement on a larger archive within
  this campaign; later windows are new pre-registrations. No forward-return
  number is computed before the floors are met (detection event counts for
  the §6 audit are allowed).
- **INCONCLUSIVE** (floors unmet at an audit-clean measurement attempt, or
  count floor 100 unmet on a slot) → the campaign ends INCONCLUSIVE with
  the documented floors; a follow-up is a new pre-registration.

## 6. The §5 gate (intraday form)

The brief §5 rule — any positive result must be re-checked against
historical constituents before being trusted — cannot run for 1-minute
data: no vendor history exists, no retrospective archive can be built
(forward accumulation is the design, per Mike's decision 2026-08-18). The
frozen design note (data/intraday/README.md §"Pre-registration #15 design
note") replaces the retrospective gate with **continuous blind capture**.
Pre-registered gate mechanics:

- **EDGE verdicts require the archive-integrity audit to PASS at
  measurement time**: (1) every pull record lists the membership file + its
  SHA; (2) each measured name-day's universe = that bar-date's pull-record
  universe; (3) all measured files hash-match the manifest (pull chain
  valid end to end); (4) repairs.json contains no selection/trimming
  reasons (deletions only for corruption/mechanical causes); (5) no
  bar-date in the window was captured non-blindly (no `--limit` runs; any
  `--adopt` files' origins verified). Audit evidence (per-bar-date universe
  files + SHAs, repair list, adoption records) is recorded in the results
  JSON.
- **Gate PASSED** = audit clean → the EDGE is entered as the
  forward-accumulated record; the Phase-5 trigger-check conversation is
  then held with the surviving evidence (house).
- **Gate FAILS** = audit dirty → the campaign is **void** (results
  reported NULL/unusable); the pipeline is repaired and any re-measurement
  requires a new pre-registration (the one-shot rule of §5, applied to
  gate failures too).
- **INCONCLUSIVE** → the gate is UNMET with the documented data
  limitation (§5).

## 7. Pre-declared expectations

- **F1**: the daily adaptation of this rule was NO EDGE and below
  baselines; the true 1-min rule differs in structure (the pullback wait,
  the double bottom, the HOD target), but the honest expectation is small
  or null absolute edge after 0.15% COST on 1-min bars. This campaign's
  value is the first honest measurement of the corpus's flagship intraday
  rule, whatever the outcome.
- **F2**: the claim's own phrasing is conditional ("when this setup works
  it goes to the high of day") — it concedes selectivity. Expect reach
  rates above the random-minutes baseline if the setup has any structure,
  materially below 100% either way; small positive or null.
- **F3**: consistent with the measured daily analogs (Shape A breakout NO
  EDGE; Shape B NO EDGE, below baselines): small or null. I-E-02's
  direction says the chase leg fails — relative to the pullback leg, not
  that the setup wins.
- **F-01/F-02 rows**: descriptive; the rows exist because these claims
  cannot be tested at all on daily bars. If the 7–10 a.m. bucket is NOT
  the volatility/liquidity peak, F-01's factual basis is falsified at the
  row level (still no verdict family).
- **Regime caveat**: the measured window is weeks of whatever the market
  delivers next — a few regimes at most. Verdicts are conditional on the
  captured regime(s); documented, not corrected.

## 8. Data & bias handling

- **Look-ahead**: the signal is complete at the close of e; entry at open
  e+1; baselines use the same convention. Detection state uses only bars
  ≤ e−1 plus High[e]. None.
- **Survivorship**: none by construction — blind forward capture records
  every name while alive, deaths included (§2, §6). The audit is the gate.
  The residual exposure is the reverse: a short measured window with no
  era dimension (documented in §7).
- **Costs**: COST 0.15% on every return; the 0.05%/0.30% tiers are
  sensitivities (§4).
- **Multiple testing**: three families, one primary slot each (F1 N=60,
  F2, F3) with two baseline slots apiece, Holm at α=0.05 within each
  family; every other horizon/condition is exploratory with no verdicts.
- **Non-stationarity**: per-bar-date and per-ticker rows; regime caveat.
- **Data quality**: manifest-verified files only; unadjusted OHLCV with
  recorded splits excluding affected name-days; tz-aware timestamps;
  sparse bars measured as stored with the gap row (§2).
- **Integrity**: `tools/measure_intraday.py` implements exactly §3–§4 and
  nothing else; its sha is frozen before any forward-return computation
  and asserted at measurement; determinism check (two runs, byte-compare)
  and an independent from-scratch verification pass (fresh seed) before
  any write-back (house).

## 9. Freeze

§0–§8 are frozen as of 2026-08-19, before any measurement. Implementation
must not change any of them. §10 records the campaign outcome.

*Sensitivity labels uniquified 2026-08-19 (S-R4/S-R2/S-P3/S-DB/S-WIN/
S-GAP/S-N15/S-N120/S-N240/S-C05/S-C30) so the measurement tool can
reference each variant unambiguously — label change only, zero parameter
change.*

## 10. Campaign outcome

*(Recorded after measurement — parameters unchanged; gate outcome per §6.)*

*Measurement is gated on §5's floors (≥ 20 full-universe bar-dates ≥
2026-08-19, ≥ 2,000 events, ≥ 100 tickers, ≥ 15 bar-dates). At the current
archive state (first full-universe pull scheduled 2026-08-19 22:05 MT)
this section is empty by design.*
