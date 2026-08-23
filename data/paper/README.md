# Paper log — live-execution study of the frozen intraday signals (pre-reg #23)

**Status: pre-registration #23 frozen 2026-08-23, before any paper-log
results exist; the paper loop runs nightly (Task Scheduler
`\patternScanner-intraday-paper`, 22:30 MT) on each bar-date as it lands.
The §5-gated comparison opens when the shared §5 floor is met
(~mid-September).**

The intraday measurement tools (pre-regs #15, #19–#22) compute close-vs-close
returns on recorded bars — `(C[e+N] − O[e+1])/O[e+1] − COST`. The archive is
1-minute OHLCV prints with **no bid/ask**: it records what traded, not what a
trader could have gotten. The paper loop closes that gap — the L-007
backtest-live gap — by running the **five frozen tools' exact definitions** on
each live tape day and logging (1) fills & slippage vs. the recorded bar, (2)
the entry/exits the veto/regime gates would actually have taken, (3) a daily
journal for the operator-process muscle.

**This is a research artifact, not investment advice. No execution, no real
money.**

## Layout

| Path | Contents | Git |
|---|---|---|
| `<YYYY-MM-DD>.json` | Deterministic decision path + modeled fills for one bar-date (byte-deterministic, append-only) | tracked |
| `journal/<YYYY-MM-DD>.md` | Daily journal: automated facts (tool-generated) + operator notes (human-edited) | tracked |
| `observed/<YYYY-MM-DD>.json` | Operator-entered observed fills (frozen schema) | tracked |

## Design contract

1. **Append-only.** Each bar-date's JSON is written once, by the first
   paper-loop run that sees the bar-date complete; never modified. Re-runs must
   reproduce it byte-for-byte (`tools/paper_loop.py --check` enforces this).
2. **Frozen inputs.** The paper loop imports the five frozen measurement tools
   and asserts their LF-normalized sha256 at import — a change to any frozen
   input aborts loudly (pre-reg #23 §3).
3. **Three price columns** (pre-reg #23 §4): the recorded-bar reference
   (deterministic), the modeled fill (frozen slippage model, `s = 0.0005` per
   side primary), and the observed fill (operator, ground truth, in
   `observed/`). The modeled-fill comparison is a sensitivity; the observed-fill
   comparison is the L-007 measurement.
4. **The journal is human-edited.** The tool writes the skeleton (automated
   facts + empty operator notes) once; the operator appends observations and
   lessons. The tool never overwrites the operator's notes.
5. **No LFS.** The paper log is tracked text (the parquet archive is the LFS
   store). Measured ~2.3 MB per bar-date (the reversal-new-high candidates
   dominate, ~80%) — ~575 MB/year at 250 trading days. The schema is frozen
   (pre-reg #23); if the size becomes a problem, a schema change is a new
   pre-registration.

## The `<date>.json` schema

```json
{
  "bar_date": "YYYY-MM-DD",
  "frozen_inputs": {"measure_intraday.py": "<lf-sha>", "...": "..."},
  "fill_model": {"s_primary": 0.0005, "s_sens": [0.0015, 0.003]},
  "files": {
    "YYYY-MM-DD/TICKER.parquet": {
      "b01": [{"signal_et", "entry_et", "dir", "entry_open", "stop",
               "target", "hour", "regime",
               "exits": {"breakeven_trail|ladder|flat_out|fixed_n|fixed_2r":
                         {"exit_price", "recorded_ret", "entry_fill",
                          "exit_fill", "modeled_ret", "half_fired|legs|flat"}}}],
      "reversal": [{"signal_et", "entry_et", "dir", "entry_open", "stop",
                    "target", "hour", "regime",
                    "veto": {"evaluable", "pass", "macd_neg", "vol_spike",
                             "legs"}}],
      "pullback": [{"signal_et", "entry_et", "k", "entry_open", "hour",
                    "regime"}],
      "second_conf": [{"c1_et", "e1_open", "e2_open", "hour", "regime"}],
      "regime": {"B1": n, "B2": n, "outside": n}
    }
  }
}
```

## The `observed/<date>.json` schema (operator-entered)

```json
{
  "bar_date": "YYYY-MM-DD",
  "fills": [
    {"ticker": "XYZ", "signal_et": "10:23:00", "dir": "long",
     "entry_fill": 12.34, "exit_fill": 12.55, "source": "live-tape",
     "note": "watched the print; got 2c slippage"}
  ]
}
```

Observed fills are matched to deterministic entries by `(ticker, signal_et,
dir)` with a ±2-minute tolerance; unmatched fills are counted and reported,
never silently dropped (pre-reg #23 §6).

## Operations

The paper loop runs nightly at 22:30 MT (after the 22:05 pull, before the
23:00 push), processing the latest bar-date. It skips if the pull is still
running (`data\intraday\.lock` present). The push task commits `data/paper`
with the archive. Manual runs:

```bat
python -X utf8 tools\paper_loop.py --all      rem backfill all window bar-dates
python -X utf8 tools\paper_loop.py --check    rem determinism check
python -X utf8 tools\paper_loop.py --compare  rem the §5-gated comparison (refuses until the floor)
```

The operator's daily practice: review the previous bar-date's journal skeleton,
append observations (what the tape looked like, whether the modeled fills were
realistic, any observed fills, lessons), and record structured observed fills in
`observed/<date>.json` where the live tape was watched.
