"""Exploratory cost screen — what the OWNED data says about tradeable cost.

**This is a feasibility screen, NOT a pre-registered campaign: it produces
bounds and cost arithmetic, never verdicts.** Nothing here measures a claim
about the market; it measures the arithmetic a claim has to survive. House
rule for exploratory work applies (cf. the §6 sensitivity sections): label it,
pre-declare nothing, report no verdict.

Why it exists: every intraday verdict in the repo is a RECORDED-BAR result
(`(C[e+N] − O[e+1])/O[e+1] − COST`, COST = 0.15% round trip), and pre-reg #23
closed with the L-007 tradeable-price row empty — so no verdict has ever been
checked against a fill. Quotes data would settle it, but two of the three
decisive facts do not need quotes:

  1. **The tick floor.** One cent is a hard minimum price increment: crossing
     the spread costs at least one tick each way. That is a *lower bound* on
     round-trip cost, computable from price levels we already own — and it
     differs enormously between the index population (~$30-60 names) and the
     mover population (median ~$6.50).
  2. **Foresight bounds.** Within the recorded bars we can compute the best
     return any execution could have achieved (buy the window low, sell the
     window high). No execution achieves it — but if even that upper bound
     cannot clear the tick floor, no fill model, no quotes feed and no
     execution improvement can save the hypothesis.

Sections:
  S1  tick floors by price band (mover rosters + index intraday window)
  S2  break-even cost per archived family (gross = net + the frozen 0.15%)
  S3  range census: how much room exists per minute and per N-bar window
  S4  foresight bounds on the frozen #15 / #19 event sets, both directions

Run: python -X utf8 tools/cost_screen.py
Writes: analysis/cost_screen_2026-09-22.md (+ data/cache/cost_screen.json)
"""
from __future__ import annotations

import json
import pathlib
import sys
from datetime import date

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import measure_intraday as MI          # noqa: E402  (frozen; imported read-only)
import measure_intraday_entry as MIE   # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[1]
INTRA = REPO / "data" / "intraday"
MOVERS = REPO / "data" / "intraday_movers"
ROSTERS = REPO / "data" / "mover_rosters"
DAILY = REPO / "data" / "cache" / "bars"
MEAS = REPO / "data" / "measurements"
OUT_MD = REPO / "analysis" / "cost_screen_2026-09-22.md"
OUT_JSON = REPO / "data" / "cache" / "cost_screen.json"

COST_FROZEN = 0.0015          # the frozen round-trip cost (all four engines)
TICK = 0.01                   # ≥ $1.00 ; sub-$1 names use $0.0001
COST_TIERS = [0.0015, 0.0031, 0.005, 0.01, 0.02]
BANDS = [(0.0, 1.0, "<1"), (1.0, 2.0, "1-2"), (2.0, 5.0, "2-5"),
         (5.0, 10.0, "5-10"), (10.0, 20.0, "10-20"),
         (20.0, 1e9, ">20")]
M = []                        # markdown report lines


def md(s: str = "") -> None:
    M.append(s)
    print(s)


def tick_pct(price: float) -> float:
    """One tick as a fraction of price."""
    if price <= 0:
        return float("nan")
    return (0.0001 if price < 1.0 else TICK) / price


def band_of(p: float) -> str:
    for lo, hi, name in BANDS:
        if lo <= p < hi:
            return name
    return ">20"


def pct(a, q) -> float:
    return float(np.percentile(np.asarray(a, dtype=float), q))


# --------------------------------------------------------------------------
# S1 — tick floors
# --------------------------------------------------------------------------

def s1_tick_floors() -> dict:
    md("## S1 — the tick floor (a hard lower bound on round-trip cost)")
    md()
    md("One cent is the minimum price increment for names ≥ $1.00. Crossing "
       "the spread costs at least one tick on entry **and** one on exit, so "
       "`2 × tick` is the narrowest conceivable round trip — before any real "
       "spread, slippage, impact or locate fee.")
    md()

    out = {}
    # mover population: the 3 captured rosters (screener's session price)
    rows = []
    for f in sorted(ROSTERS.glob("*.csv")):
        rows.append(pd.read_csv(f))
    mv = pd.concat(rows, ignore_index=True)
    mv = mv[mv["price"] > 0]

    # index population: closes from the intraday archive itself. (The daily
    # cache is the 2000–2025 dataset and does not cover the 2026 window.)
    manifest = json.loads((INTRA / "manifest.json").read_text(encoding="utf-8"))
    win_dates = sorted({rel.split("/")[0] for rel in manifest["files"]
                        if rel.split("/")[0] >= "2026-08-19"})
    sample_dates = ([win_dates[0], win_dates[len(win_dates) // 2],
                     win_dates[-1]] if len(win_dates) > 2 else win_dates)
    px = []
    for d in sample_dates:
        for fp in sorted((INTRA / "raw" / d).glob("*.parquet")):
            try:
                cl = pd.read_parquet(fp, columns=["Close"])["Close"]
            except Exception:
                continue
            cl = cl[cl > 0]
            if len(cl):
                px.append(float(cl.median()))
    ix = pd.Series(px, dtype=float)
    ix = ix[ix > 0]
    n_index_names = len(sorted((INTRA / "raw" / sample_dates[-1]).glob(
        "*.parquet"))) if sample_dates else 0

    for label, series, n_names in (("mover (roster names)", mv["price"],
                                    mv["ticker"].nunique()),
                                   ("index (S&P 600 window)", ix,
                                    n_index_names)):
        md(f"**{label}** — {len(series):,} name-days, {n_names:,} names, "
           f"median price ${series.median():.2f}")
        md()
        md("| price band | name-days | median $ | 1 tick | round trip (2 ticks) |")
        md("|---|---|---|---|---|")
        rec = {}
        for lo, hi, name in BANDS:
            s = series[(series >= lo) & (series < hi)]
            if not len(s):
                continue
            med = float(s.median())
            t = tick_pct(med)
            rec[name] = {"n": int(len(s)), "median": med,
                         "tick_pct": t, "rt_pct": 2 * t}
            md(f"| {name} | {len(s):,} | {med:.2f} | {t*100:.3f}% | "
               f"**{2*t*100:.3f}%** |")
        md()
        out[label] = rec
    md(f"For reference, the frozen cost convention in every intraday engine "
       f"is **{COST_FROZEN*100:.2f}% round trip**.")
    md()
    return out


# --------------------------------------------------------------------------
# S2 — break-even cost per archived family
# --------------------------------------------------------------------------

def s2_breakeven() -> dict:
    md("## S2 — break-even cost for the archived families")
    md()
    md("`mean_ret` in the archived results is the **net** absolute mean "
       "(after the frozen 0.15%). Gross = net + 0.15%, and gross is exactly "
       "the round-trip cost at which the family breaks even. A negative gross "
       "means no cost assumption can help — the leg loses before costs.")
    md()
    md("| campaign / leg | n | net mean | implied gross | break-even cost |")
    md("|---|---|---|---|---|")

    out = {}
    src = [
        ("#15 B-01 long (index)",
         MEAS / "measure_intraday/intraday_measure_results.json",
         [("f1", "same_ticker")]),
        ("#19 reversal long (index)",
         MEAS / "measure_intraday_entry/intraday_entry_measure_results.json",
         [("f1", "long")]),
        ("#19 reversal short (index)",
         MEAS / "measure_intraday_entry/intraday_entry_measure_results.json",
         [("f1", "short")]),
    ]
    for label, fp, paths in src:
        if not fp.exists():
            md(f"| {label} | — | *missing* | — | — |")
            continue
        j = json.loads(fp.read_text(encoding="utf-8"))
        for p1, p2 in paths:
            node = j.get(p1, {})
            node = node.get(p2, node) if p2 else node
            if not isinstance(node, dict) or "mean_ret" not in node:
                continue
            net = float(node["mean_ret"])
            gross = net + COST_FROZEN
            out[label] = {"n": node.get("n"), "net": net, "gross": gross}
            md(f"| {label} | {node.get('n'):,} | {net*100:+.4f}% | "
               f"**{gross*100:+.4f}%** | {gross*100:+.4f}% |")
    md()
    md("The contrasts (#15 F2 reach-rate, #19 F2/F3, #21 veto slots, #22 F2, "
       "#27 gate slots) are *differences* between legs and carry no absolute "
       "level, so no tradeable break-even can be read off them — a contrast "
       "says which of two things is worse, not whether either makes money.")
    md()
    return out


# --------------------------------------------------------------------------
# S3 — range census
# --------------------------------------------------------------------------

def _file_ranges(fp: pathlib.Path, nwin: int) -> tuple:
    """Per-minute relative ranges + per-N-bar window ranges for one file."""
    try:
        df = pd.read_parquet(fp, columns=["High", "Low", "Close"])
    except Exception:
        return None
    if not len(df):
        return None
    hi = df["High"].to_numpy(dtype=float)
    lo = df["Low"].to_numpy(dtype=float)
    cl = df["Close"].to_numpy(dtype=float)
    ok = (cl > 0) & np.isfinite(hi) & np.isfinite(lo)
    if ok.sum() < 2:
        return None
    hi, lo, cl = hi[ok], lo[ok], cl[ok]
    minute = (hi - lo) / cl
    wins = []
    if len(cl) > nwin:
        # rolling window range relative to the window's first close
        s = pd.Series(hi)
        mn = pd.Series(lo).rolling(nwin).min().to_numpy()
        mx = pd.Series(hi).rolling(nwin).max().to_numpy()
        base = pd.Series(cl).shift(nwin - 1).to_numpy()
        w = (mx - mn) / base
        wins = w[np.isfinite(w)]
    return minute, wins


def s3_ranges() -> dict:
    md("## S3 — how much room exists per minute and per holding window")
    md()
    md("A trade can only pay if price moves more than the round trip costs. "
       "These are the distributions of the *available* relative range — "
       "per minute, and over the engines' N=60-bar horizon — so the share "
       "below a given cost tier is the share of moments that are untradeable "
       "by construction.")
    md()
    out = {}
    nwin = MI.N_PRIMARY
    for label, root, dates in (
            ("index (S&P 600, window ≥ 2026-08-19)", INTRA / "raw", None),
            ("mover archive (all bar-dates)", MOVERS / "raw", None)):
        files = sorted(root.glob("*/*.parquet"))
        if dates:
            files = [f for f in files if f.parent.name in dates]
        minute_all, win_all = [], []
        counts = {t: 0 for t in COST_TIERS}
        nmin = 0
        for i, fp in enumerate(files):
            r = _file_ranges(fp, nwin)
            if r is None:
                continue
            minute, wins = r
            minute_all.append(pct(minute, 50))
            if len(wins):
                win_all.append(pct(wins, 50))
            nmin += len(minute)
            for t in COST_TIERS:
                counts[t] += int((minute < t).sum())
            if (i + 1) % 4000 == 0:
                print(f"    ... {i+1}/{len(files)} files")
        if not minute_all:
            continue
        md(f"**{label}** — {len(files):,} files, {nmin:,} minutes")
        md()
        md("| statistic | per-minute (H−L)/C | over N=60 bars |")
        md("|---|---|---|")
        for name, arr in (("median of per-file medians", minute_all),
                          ("p10 of per-file medians", minute_all),
                          ("p90 of per-file medians", minute_all)):
            q = {"median of per-file medians": 50,
                 "p10 of per-file medians": 10,
                 "p90 of per-file medians": 90}[name]
            wq = pct(win_all, q) if win_all else float("nan")
            md(f"| {name} | {pct(arr, q)*100:.3f}% | {wq*100:.3f}% |")
        md()
        md("| round-trip cost tier | share of minutes with range BELOW it |")
        md("|---|---|")
        for t in COST_TIERS:
            md(f"| {t*100:.2f}% | {counts[t]/nmin*100:.1f}% |")
        md()
        out[label] = {"files": len(files), "minutes": nmin,
                      "minute_median_of_medians": pct(minute_all, 50),
                      "window_median_of_medians": (pct(win_all, 50)
                                                   if win_all else None),
                      "share_below": {f"{t}": counts[t] / nmin
                                      for t in COST_TIERS}}
    return out


# --------------------------------------------------------------------------
# S4 — foresight bounds on the frozen event sets
# --------------------------------------------------------------------------

def _bounds(mod, archive, event_attr: str, own: str = "long",
            dir_filter: str | None = None) -> dict:
    """Best-case bounds for a frozen event set.

    `own` is the direction the set actually bets — long for the B-01 detector,
    the per-event `dir` for the reversal detector (selected with
    `dir_filter`). The mirror is always the opposite direction on the same
    events. The two engines also name their event lists differently.
    """
    N = mod.N_PRIMARY
    events = [ev for ev in getattr(archive, event_attr)
              if ev.get("valid_n")
              and (dir_filter is None or ev.get("dir") == dir_filter)]
    acc = {k: [] for k in ("own_meas", "own_best", "own_foresight",
                           "mirror_meas", "mirror_foresight", "tick_rt")}
    for ev in events:
        rel = ev["rel"]
        df = archive.files[rel]
        pos = archive.wpos(rel)
        op = df["Open"].to_numpy()[pos]
        hi = df["High"].to_numpy()[pos]
        lo = df["Low"].to_numpy()[pos]
        cl = df["Close"].to_numpy()[pos]
        e = ev["e_pos"]
        a, b = e + 1, e + N
        if b >= len(cl) or a < 0:
            continue
        o = op[a]
        if not np.isfinite(o) or o <= 0:
            continue
        hiw, low, clw = hi[a:b + 1], lo[a:b + 1], cl[a:b + 1]
        if not (np.isfinite(hiw).all() and np.isfinite(low).all()
                and np.isfinite(clw).all()):
            continue
        long_meas = (cl[b] - o) / o
        long_best = (clw.max() - o) / o
        long_fs = (hiw.max() - low.min()) / low.min()
        short_meas = (o - cl[b]) / o
        short_best = (o - low.min()) / o
        short_fs = (hiw.max() - low.min()) / hiw.max()
        if own == "long":
            acc["own_meas"].append(long_meas)
            acc["own_best"].append(long_best)
            acc["own_foresight"].append(long_fs)
            acc["mirror_meas"].append(short_meas)
            acc["mirror_foresight"].append(short_fs)
        else:
            acc["own_meas"].append(short_meas)
            acc["own_best"].append(short_best)
            acc["own_foresight"].append(short_fs)
            acc["mirror_meas"].append(long_meas)
            acc["mirror_foresight"].append(long_fs)
        acc["tick_rt"].append(2 * tick_pct(o))
    out = {k: (float(np.mean(v)) if v else float("nan"))
           for k, v in acc.items()}
    out["n"] = len(acc["own_meas"])
    out["own"] = own
    out["tick_rt_median"] = (float(np.median(acc["tick_rt"]))
                             if acc["tick_rt"] else float("nan"))
    out["tick_rt_p10"] = (pct(acc["tick_rt"], 10) if acc["tick_rt"]
                          else float("nan"))
    out["tick_rt_p90"] = (pct(acc["tick_rt"], 90) if acc["tick_rt"]
                          else float("nan"))
    # The decisive per-event statistic: the share of signals whose
    # PERFECT-FORESIGHT gross is below a cost tier — i.e. trades that cannot
    # pay at any execution, whatever the fills.
    of = np.asarray(acc["own_foresight"], dtype=float)
    mf = np.asarray(acc["mirror_foresight"], dtype=float)
    tiers = [("frozen 0.15%", COST_FROZEN),
             ("median tick floor", out["tick_rt_median"]),
             ("2 × median tick floor", 2 * out["tick_rt_median"]),
             ("0.50%", 0.005), ("1.00%", 0.01)]
    out["unreachable_share"] = {
        name: {"own": float((of < t).mean()) if len(of) else float("nan"),
               "mirror": float((mf < t).mean()) if len(mf) else float("nan"),
               "tier": t}
        for name, t in tiers}
    return out


def s4_bounds() -> dict:
    md("## S4 — foresight bounds on the frozen event sets")
    md()
    md("Three columns, all **gross** (before cost), all on the exact frozen "
       "event sets:")
    md()
    md("- **as measured** — the repo's convention (`O[e+1] → C[e+N]`);")
    md("- **best exit** — realistic entry, but the *best close inside the "
       "holding window* (foresight on the exit only);")
    md("- **perfect foresight** — buy the window's lowest low, sell its "
       "highest high (short: sell the high, cover the low). No execution "
       "achieves this; it is a hard **upper bound** on what any fill model "
       "could deliver.")
    md()
    md("If the perfect-foresight column cannot clear the tick floor, the "
       "hypothesis is unreachable — no quotes feed, no execution skill and no "
       "parameter change can rescue it.")
    md()
    out = {}

    md("### #15 B-01 micro pullback (index, frozen detector — long-only set)")
    md()
    a = MI.Archive()
    res = _bounds(MI, a, "events", own="long")
    md("| direction | n | as measured | best exit / cover | perfect foresight |")
    md("|---|---|---|---|---|")
    md(f"| long (the claim) | {res['n']:,} | {res['own_meas']*100:+.4f}% | "
       f"{res['own_best']*100:+.4f}% | {res['own_foresight']*100:+.4f}% |")
    md(f"| short (its mirror) | {res['n']:,} | {res['mirror_meas']*100:+.4f}% | "
       f"— | {res['mirror_foresight']*100:+.4f}% |")
    md()
    md(f"Tick floor on this population: median **{res['tick_rt_median']*100:.3f}%** "
       f"round trip (p10 {res['tick_rt_p10']*100:.3f}%, "
       f"p90 {res['tick_rt_p90']*100:.3f}%).")
    md()
    _unreachable_table(res)
    out["b01"] = res
    del a

    md("### #19 reversal new-high (index, frozen detector — split by direction)")
    md()
    md("The detector emits both directions, so the rows below are split by the "
       "event's own `dir` (the archived families pair each direction against "
       "its own baselines).")
    md()
    ae = MIE.Archive()
    for d in ("long", "short"):
        r = _bounds(MIE, ae, "f1_events", own=d, dir_filter=d)
        other = "short" if d == "long" else "long"
        md(f"**events whose own direction is {d}**")
        md()
        md("| direction | n | as measured | best exit / cover | perfect foresight |")
        md("|---|---|---|---|---|")
        md(f"| {d} (the claim) | {r['n']:,} | {r['own_meas']*100:+.4f}% | "
           f"{r['own_best']*100:+.4f}% | {r['own_foresight']*100:+.4f}% |")
        md(f"| {other} (its mirror) | {r['n']:,} | {r['mirror_meas']*100:+.4f}% | "
           f"— | {r['mirror_foresight']*100:+.4f}% |")
        md()
        md(f"Tick floor for these events: median "
           f"**{r['tick_rt_median']*100:.3f}%** round trip "
           f"(p10 {r['tick_rt_p10']*100:.3f}%).")
        md()
        _unreachable_table(r)
        out[f"entry_{d}"] = r
    return out


def _unreachable_table(res: dict) -> None:
    """The decisive table: share of signals that cannot pay at any execution."""
    own = res.get("own", "long")
    other = "short" if own == "long" else "long"
    md("**Unreachable trades** — the share of signals whose perfect-foresight "
       "gross is below the cost tier. For these the trade cannot pay however "
       "well it is executed: the window simply does not contain enough range.")
    md()
    md(f"| cost tier | {own} (the claim) unreachable | {other} (mirror) unreachable |")
    md("|---|---|---|")
    for name, v in res["unreachable_share"].items():
        md(f"| {name} ({v['tier']*100:.3f}%) | {v['own']*100:.1f}% | "
           f"{v['mirror']*100:.1f}% |")
    md()


# --------------------------------------------------------------------------

def s5_mover_bounds() -> dict:
    """#33's population: roster-restricted events on the mover archive,
    measured against that population's own tick floors."""
    import measure_mover_entry as MME   # draft tool; import is side-effect free

    md("## S5 — the mover population (pre-reg #33's population of record)")
    md()
    md("The same bounds, on the mover archive with events restricted to each "
       "bar-date's captured roster (`measure_mover_entry.restrict_to_rosters`), "
       "so the tick floors below are that population's own. **Small samples:** "
       "roster capture began 2026-09-18, so this is a handful of sessions, not "
       "a measurement — read these as bounds on what is possible, not as "
       "estimates of anything.")
    md()
    rosters = MME.roster_sets()
    rd = sorted(rosters)
    entries = sum(len(v) for v in rosters.values())
    distinct = len(set().union(*rosters.values())) if rosters else 0
    md(f"Roster bar-dates: **{len(rd)}** ({rd[0]}…{rd[-1] if rd else '—'}); "
       f"{entries} roster entries over {distinct} distinct tickers.")
    md()
    out: dict = {"roster_bar_dates": rd, "roster_entries": entries}
    plan = (("B-01 (long-only set)", MI, "events", "long", None),
            ("#19 long-direction events", MIE, "f1_events", "long", "long"),
            ("#19 short-direction events", MIE, "f1_events", "short", "short"))
    for label, mod, attr, own, dflt in plan:
        MME._redirect(mod, "mover_screen_report.md", "mover_screen_results.json")
        mod.self_check()
        a = mod.Archive()
        pop = MME.restrict_to_rosters(a, rosters)
        res = _bounds(mod, a, attr, own=own, dir_filter=dflt)
        other = "short" if own == "long" else "long"
        md(f"### {label} — {res['n']:,} events on "
           f"{pop['dates_with_events']} of {pop['roster_bar_dates']} roster "
           f"bar-dates")
        md()
        md("| direction | n | as measured | best exit / cover | perfect foresight |")
        md("|---|---|---|---|---|")
        md(f"| {own} (the claim) | {res['n']:,} | {res['own_meas']*100:+.4f}% | "
           f"{res['own_best']*100:+.4f}% | {res['own_foresight']*100:+.4f}% |")
        md(f"| {other} (its mirror) | {res['n']:,} | "
           f"{res['mirror_meas']*100:+.4f}% | — | "
           f"{res['mirror_foresight']*100:+.4f}% |")
        md()
        med = res['tick_rt_median']
        md(f"Tick floor for these events: median **{med*100:.3f}%** round trip "
           f"(p10 {res['tick_rt_p10']*100:.3f}%, "
           f"p90 {res['tick_rt_p90']*100:.3f}%) — versus the frozen cost "
           f"convention of 0.150%.")
        md()
        if res["n"]:
            md(f"Perfect-foresight headroom over the tick floor: "
               f"**{res['own_foresight']*100:+.3f}%** for the {own} claim, "
               f"**{res['mirror_foresight']*100:+.3f}%** for its mirror.")
            md()
        _unreachable_table(res)
        out[label] = res
        del a
    return out


def _existing_interpretation() -> str:
    """Preserve the hand-written reading across re-runs (the tables are
    generated; the interpretation is not — and must be re-checked after any
    re-run, since the numbers move)."""
    if not OUT_MD.exists():
        return ""
    txt = OUT_MD.read_text(encoding="utf-8")
    i = txt.find("## Interpretation")
    return txt[i:].rstrip() if i >= 0 else ""


def main() -> int:
    md("# Cost screen — what the owned data says about tradeable cost")
    md()
    md("**EXPLORATORY SCREENING — NO VERDICTS.** Generated by "
       "`tools/cost_screen.py` on the archives and archived results as of "
       f"{date.today().isoformat()}. Bounds and arithmetic only; no claim "
       "about the market is tested here, and nothing in this document may be "
       "cited as a verdict. Interpretation follows the generated tables.")
    md()
    payload = {}
    payload["s1_tick_floors"] = s1_tick_floors()
    payload["s2_breakeven"] = s2_breakeven()
    payload["s3_ranges"] = s3_ranges()
    payload["s4_bounds"] = s4_bounds()
    payload["s5_mover_bounds"] = s5_mover_bounds()
    old = _existing_interpretation()
    if old:
        M.append(old)
        M.append("")
    else:
        md("## Interpretation")
        md()
        md("*(to be written — the tables above are generated; the reading is "
           "added by hand and must stay inside the bounds they establish.)*")
        md()
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(M) + "\n", encoding="utf-8")
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, default=str),
                        encoding="utf-8")
    print(f"\nwrote {OUT_MD.relative_to(REPO)} and "
          f"{OUT_JSON.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
