# patternScanner — working notes for Claude sessions

Honest, pre-registered measurement of trading-pattern claims. **Nothing here
trades real money; this is research, and every positive claim is treated as
suspect until it survives the §5 survivorship gate.** Docs map:
[DESIGN_BRIEF.md](DESIGN_BRIEF.md) (scope + protocol),
[PREREGISTRATION.md](PREREGISTRATION.md) (frozen hypotheses — changing
parameters after results is a new hypothesis), [CLAIMS_LEDGER.md](CLAIMS_LEDGER.md)
(verdicts), [README.md](README.md) (status).

## The intraday track (live since 2026-08-19)

A nightly automation runs on this machine and is **not to be fought**:

- **22:05 MT** Task Scheduler `\patternScanner-intraday-pull`:
  `tools\fetch_intraday_bars.py --qa` — pulls the full S&P 600 1-minute
  archive (04:00–20:00 ET, Yahoo), appends to `data/intraday/`.
- **23:00 MT** `\patternScanner-intraday-push`: `tools\push_intraday_archive.cmd`
  — commits `data/intraday` only and pushes (log: `%TEMP%\intraday_push.log`).

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
faults.

## Discipline notes

- Pre-registration order: verdicts return to CLAIMS_LEDGER before a new
  hypothesis is frozen. §5 gates run before any EDGE is trusted.
- Task Scheduler XMLs are UTF-16 — don't reformat them.
- Worktree isolation is used for code changes; the scheduled tasks run in
  the main checkout and must keep working.
