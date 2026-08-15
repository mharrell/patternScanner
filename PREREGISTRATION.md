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


