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
