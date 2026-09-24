# patternScanner — working notes for Claude sessions

Honest, pre-registered measurement of trading-pattern claims. **Nothing here
trades real money; this is research, and every positive claim is treated as
suspect until it survives the §5 survivorship gate.** Docs map:
[DESIGN_BRIEF.md](DESIGN_BRIEF.md) (scope + protocol),
[PREREGISTRATION.md](PREREGISTRATION.md) (frozen hypotheses — changing
parameters after results is a new hypothesis), [CLAIMS_LEDGER.md](CLAIMS_LEDGER.md)
(verdicts), [README.md](README.md) (status).

## The intraday tracks (S&P 600 live since 2026-08-19; movers since 2026-09-18)

A nightly automation runs on this machine and is **not to be fought** — five
registered tasks, all `StartWhenAvailable`:

- **22:05 MT** Task Scheduler `\patternScanner-intraday-pull`:
  `tools\fetch_intraday_bars.py --qa` — pulls the full S&P 600 1-minute
  archive (04:00–20:00 ET, Yahoo), appends to `data/intraday/`.
- **22:30 MT** `\patternScanner-intraday-paper`: `tools\paper_loop.py --latest`
  — the pre-reg #23 paper log into `data/paper/`.
- **22:35 MT** `\patternScanner-mover-pull`: `tools\mover_pull.cmd` — the
  mover-universe roster + `data/intraday_movers/` pull (pre-reg #33 draft).
- **23:00 MT** `\patternScanner-intraday-push`: `tools\push_intraday_archive.cmd`
  — commits `data/intraday` + `data/paper` + `data/intraday_movers` +
  `data/mover_rosters` and pushes (log: `%TEMP%\intraday_push.log`).
- **23:45 MT** `\patternScanner-gate-opener`: `tools\gate_opener.cmd` — runs
  each §5-gated campaign in full mode; an unmet floor REFUSES (exit 2) without
  consuming the one-shot, so it is safe nightly (`%TEMP%\gate_opener.log`).

Status 2026-09-23: the shared §5 floor opened 2026-09-18 and six campaigns are
measured (#15/#19/#21/#22/#27/#32 → ledger §K.1–§K.6). **#20 is the last
unmeasured frozen campaign** (1,601/2,000 F1-evaluable events, ~2026-10-01).
**#23's §5-gated comparison RAN 2026-09-22 and its one-shot is
CONSUMED** — the modeled gap came out exactly as pre-declared (−0.000999 ≈
−2s) and the **L-007 row is empty** because the operator-fill layer was never
populated, so the campaign's declared finding was not captured; a
quotes-based successor pre-registration is the path to a real backtest-live
gap. The mover track's shakedown blockers are resolved in the draft tool, and
the **cost screen** (`analysis/cost_screen_2026-09-22.md`) now shows the first
positive recorded-bar preview on that population (+0.68% gross B-01 vs −0.04%
on the index) — below every floor, recorded-bar only, no verdict. Its freeze
decision on the cost model is the live one (1,601 → 2,000 events is not).

**The archive is append-only and must never be regenerated or edited.**
Each (bar-date, ticker) file is written once and immutable; every run
re-verifies a SHA-256 manifest before writing anything, and a missing,
corrupt, or unrecorded file aborts the pull loudly. Recovery is only via the
script's own sanctioned paths: `--adopt` (hash+schema-verified keep) or
`--repair` (deletion with a recorded reason). **Never re-fetch to "fix"
stored data**, never edit `manifest.json`/`repairs.json`/`splits.json` by
hand. Splits are recorded in `splits.json`, applied at measurement time.

Ops manual: [INTRAday_OPERATIONS.md](INTRAday_OPERATIONS.md) (monitoring,
failure modes, re-creating the scheduled tasks from `tools/tasks/*.xml`).
Data contract: [data/intraday/README.md](data/intraday/README.md).

Gotchas: ticker `CON` is a Windows reserved device name — git needs
`core.protectNTFS false` (the push script self-heals it). LFS free-tier
storage is a ~4.7-month horizon at measured ~2.5 GB/yr — local disk is the
primary store. Thin-name RTH minute gaps are data reality, not pipeline
faults. Recurring Yahoo drift notes are data reality too (54–179/pull is the
settled background; the one bulk episode was 2026-08-25, 2,412 files) — the
stored file is final, only `--repair` + re-pull refreshes.

**Amending a frozen intraday tool breaks the paper loop.** `paper_loop.py`
asserts the five frozen tools' shas at import, so any amendment to
`measure_intraday*.py` (even a report-writer fix) kills the 22:30 paper task
until its table is re-recorded AND pre-reg #23 §10 gets an amendment record.
That is how 2026-09-18→09-22 went unlogged. Amendment discipline, not a
silent table edit — and backfill with `paper_loop.py --all`.

## Discipline notes

- Pre-registration order: verdicts return to CLAIMS_LEDGER before a new
  hypothesis is frozen. §5 gates run before any EDGE is trusted.
- Task Scheduler XMLs are UTF-16 — don't reformat them.
- Worktree isolation is used for code changes; the scheduled tasks run in
  the main checkout and must keep working.
