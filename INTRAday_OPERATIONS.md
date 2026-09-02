# Intraday track — operations runbook

**What this is:** the operating manual for the intraday accumulation track —
its role, the nightly machinery, how to monitor it, and how to recover when
something breaks. The *data design contract* (the "can't corrupt it" rules)
lives in [data/intraday/README.md](data/intraday/README.md); this document is
about the running system around it.

## Role — why the track exists

The untested claims in the course ledger are stated on **1-minute charts**
(B-01 micro pullback, I-B-01, I-C-02/03/04, E-01/E-04 1-min MACD, F-01
7–10 a.m. window, F-02 pre-market, I-E-02) — daily bars cannot test them.
The intraday track accumulates the raw material: a forward-captured 1-minute
OHLCV archive of the **live S&P 600** (extended hours 04:00–20:00 ET, Yahoo
free series, 7-day rolling window).

**Why forward capture:** every name is captured *while it is alive* — a name
that later delists stays in the archive, in full, including its final weeks.
Deaths are captured at capture time, not erased retroactively, so the
survivorship bias that plagues retrospective reconstruction does not exist
here. The archive is exactly the set of names a day trader could have traded
*going forward*.

**Measurement:** pre-registration #15 (PREREGISTRATION.md, frozen
2026-08-19) — B-01 micro pullback on 1-minute bars (primary), the
B-02/I-E-02 pullback-vs-chase contrast, and the F-01/F-02 time-of-day rows.
Its §5 gate (frozen): ≥ 20 full-universe bar-dates ≥ 2026-08-19 before any
measurement. Tool SHAs are frozen in the pre-registration record — parameter
changes after results are a new hypothesis.

## Function — what runs nightly

Three Windows Task Scheduler tasks (all `StartWhenAvailable`: if the machine
is off at the trigger time, they run at next wake). XML templates are
versioned in `tools/tasks/` — see "Recreating the scheduled tasks" below.

| Task | Trigger | Runs | Log / evidence |
|---|---|---|---|
| `\patternScanner-intraday-pull` | daily 22:05 MT | `C:\Python312\python.exe -X utf8 <repo>\tools\fetch_intraday_bars.py --qa` (Start in: repo root) | pull record in `data/intraday/manifest.json`; QA pass → `data/intraday/qa_report.md` |
| `\patternScanner-intraday-paper` | daily 22:30 MT | `C:\Python312\python.exe -X utf8 <repo>\tools\paper_loop.py --latest` (Start in: repo root) | `data/paper/<YYYY-MM-DD>.json` + `data/paper/journal/<YYYY-MM-DD>.md` |
| `\patternScanner-intraday-push` | daily 23:00 MT | `<repo>\tools\push_intraday_archive.cmd` | `%TEMP%\intraday_push.log` (append-only) |
| `\patternScanner-gate-opener` | daily 23:45 MT | `<repo>\tools\gate_opener.cmd` | `%TEMP%\gate_opener.log` (append-only); NOT yet registered — see recreate block |

- 22:05 MT is after the 04:00–20:00 ET session closes (20:00 ET = 18:00 MT)
  and outside DeepSeek peak pricing.
- The paper task skips itself if a pull is still running (`data\intraday\.lock`
  present) — the paper loop runs the five frozen definitions on the latest
  bar-date and logs fills/slippage, gate decisions, and the daily journal
  (pre-reg #23; see [data/paper/README.md](data/paper/README.md)).
- The push task skips itself if a pull is still running (`data\intraday\.lock`
  present) and commits **only** `data/intraday` + `data/paper`; it
  fast-forwards `main` first so a rejected push self-heals. The pull script
  itself never pushes.

**Pieces of the system:**

| File | Function |
|---|---|
| `tools/fetch_intraday_bars.py` | Pull: full-universe fetch, append-only writes, manifest verification, drift checks, `--adopt` / `--repair` recovery, `--limit N` for tests. Run `--qa` appends the QA pass. |
| `tools/qa_intraday.py` | QA pass: flags only, fixes nothing. RTH coverage, OHLC sanity, interior gaps, envelope vs daily bars, volume sums. |
| `tools/push_intraday_archive.cmd` | Nightly commit+push of `data/intraday` + `data/paper` (skips on `.lock`; `git config core.protectNTFS false` self-heal for ticker CON). |
| `tools/paper_loop.py` | Paper loop (pre-reg #23): runs the five frozen intraday definitions on a bar-date, logs the decision path + three price columns, writes `data/paper/`. Modes `--date`/`--latest`/`--all`/`--check`/`--compare`. |
| `tools/tasks/pull_task.xml`, `paper_task.xml`, `push_task.xml` | Task Scheduler import templates (UTF-16; `schtasks /create /xml`). |
| `data/paper/` | Paper-log store: `<date>.json` (byte-deterministic decision path + modeled fills), `journal/<date>.md` (automated facts + operator notes), `observed/<date>.json` (operator fills). Contract: [data/paper/README.md](data/paper/README.md). |
| `data/intraday/manifest.json` | Cumulative ledger: per-file SHA-256 + rows + span + pull-id; one pull record per run (with universe file + SHA). |
| `data/intraday/repairs.json` | Recorded deletions (path, sha-before, reason, UTC) — the only sanctioned removals. |
| `data/intraday/splits.json` | Recorded split events, applied at measurement time only. |
| `data/intraday/qa_report.md` | Latest QA output — flags only, nothing fixed. |
| `data/intraday/raw/<YYYY-MM-DD>/<TICKER>.parquet` | Immutable day bars (LFS-tracked). |

## Behavior — the discipline (what the system refuses to do)

1. **Append-only.** Each (bar-date, ticker) file is written once, by the
   first pull that sees the bar-date complete; never modified. A bar-date is
   written only after its session has fully closed.
2. **No silent regeneration.** Every run re-hashes **all** recorded files and
   walks `raw/` for orphans *before* writing anything. A missing, corrupt, or
   unrecorded file **aborts the pull with a loud error**. Files are never
   re-fetched to "fix" stored data — `--repair` (recorded deletion) or
   `--adopt` (verified keep) are the only recoveries, and both are deliberate,
   human-initiated acts.
3. **Blind full-universe capture.** The pull list is always the whole
   membership CSV — no cherry-picking. Membership changes create a **new**
   universe CSV (`universe_sp600_<date>.csv`); the frozen snapshot is never
   edited. The universe file and its SHA-256 are recorded in every pull
   record.
4. **Drift is reported, never auto-fixed.** Possible Yahoo restatement is
   flagged in the pull record; QA flags are notes, never corrections.
5. **Repairs leave evidence.** Anything deleted without a repair record
   aborts the next pull loudly.

## Monitoring — 2-minute morning check

1. Push log tail — last line should be `exit=0`:
   `tail -20 "%TEMP%\intraday_push.log"`
2. QA report shows the previous bar-date present:
   `python -X utf8 tools\qa_intraday.py` (or read `data/intraday/qa_report.md`)
3. Manifest pull records grew by one (script prints `ok=N no_data=0 failed=0`).
4. Paper log present for the previous bar-date:
   `python -X utf8 tools\paper_loop.py --check` (determinism check) and
   `data/paper/<previous-bar-date>.json` exists.

Expected data reality, not defects: **thin-name minute sparsity** — Yahoo 1m
emits a bar only when a name prints a trade/quote, so thinly-traded S&P 600
names show large real RTH gaps (e.g. ~30–55% RTH coverage) while liquid names
are complete. Measurement on thin names must resample (e.g. 5-min) or count
RTH coverage.

## Failure modes and recovery

| Symptom | Cause | Action |
|---|---|---|
| Pull aborts: "orphan file not in manifest" | A previous pull crashed mid-run | `--adopt "<rel>" --reason "crashed-pull file, hash-verified"` (keeps it) or `--repair "<rel>" --reason "..."` (deletes with record; window re-fetches if still open) |
| Pull aborts: hash mismatch on a recorded file | Disk corruption or tampering | Restore from the last push (`git lfs pull`); if irrecoverable, `--repair` with a reason. Never re-fetch to "fix". |
| Pull aborts: leftover `.lock` | Pull crashed | Remove `data\intraday\.lock` only after confirming no pull is running (stale-lock check in the script). |
| Pull aborts: recorded repair not completed | Crash between repair record and deletion | The next pull completes the recorded repair loudly — no action needed. |
| Push log shows `SKIP: pull still running` | Pull overran 23:00 | Normal; the push skips that night. Verify the pull finished and push manually if the archive is unreplicated for several days. |
| Paper log missing for a bar-date | Paper task skipped (pull overran 22:30) or failed | Run `python -X utf8 tools\paper_loop.py --all` to backfill (idempotent); the operator fills the journal. |
| Paper loop aborts: "frozen input must not move" | A frozen measurement tool changed | Restore the frozen tool (its sha is recorded in PREREGISTRATION.md); the paper loop refuses to log until it matches. |
| Push log shows `ff-only pull failed` | Local `main` diverged from origin | Resolve the divergence (usually nothing but the archive; a merge or rebase of `data/intraday` only), then re-run the script. |
| Push fails: `error: open('...CON.parquet'): No such file or directory` | Ticker `CON` is a Windows reserved device name | The script self-heals (`git config core.protectNTFS false`, repo-local). A fresh clone needs the same setting before `git lfs pull` restores `CON.parquet`. |
| LFS push rejected (quota) | GitHub free-tier storage cap | Measured ~2.5 GB/yr, ~4.7-month horizon from 2026-08-19 (bandwidth fine, ~210 MB/month). Local disk is the primary store; plan (releases, pruning, or vendor) before the cap. |
| QA flags: envelope/volume breaks across many files | Signature of an unrecorded split | Record it in `data/intraday/splits.json` (procedure in the README); stored bars are never rewritten. |

## Recreating the scheduled tasks

If the machine is rebuilt or the tasks are lost, re-import the versioned
templates (they set `StartWhenAvailable`, `InteractiveToken`,
`LeastPrivilege`, `ExecutionTimeLimit` PT4H/PT30M, `MultipleInstancesPolicy
IgnoreNew`):

```bat
schtasks /create /tn "patternScanner-intraday-pull" /xml "tools\tasks\pull_task.xml" /f
schtasks /create /tn "patternScanner-intraday-paper" /xml "tools\tasks\paper_task.xml" /f
schtasks /create /tn "patternScanner-intraday-push" /xml "tools\tasks\push_task.xml" /f
schtasks /create /tn "patternScanner-gate-opener" /xml "tools\tasks\gate_opener_task.xml" /f
```

The gate opener (added 2026-09-02) runs `tools/gate_opener.py`: each
§5-gated campaign (#15/#19, #20, #21, #22, #27, in pre-reg order) is run
in full mode — every tool REFUSES (exit 2) on unmet floors WITHOUT
consuming its one-shot, so the opener is safe to schedule daily. Exit 0
= measured (once; the state file `data/cache/gate_opener_state.json`
prevents double-firing), and results/reports are archived under
`data/measurements/<tool>/` (tracked). The opener never writes
verdicts — pre-reg §8 + ledger flips are session work. **Registration
of this task was left to the user (machine-level persistence is a user
decision): run the schtasks line above.**

Update the absolute paths inside the XMLs if the repo moves.

## As-built history

- 2026-08-18: pipeline built and adversarially reviewed (worktree); test
  artifacts committed with the merge PR.
- 2026-08-19: PR #1 merged (`3541eea`); first **full-universe** pull:
  603 tickers, 3000 files, ok=603 / no_data=0 / failed=0; QA 3030 files.
  Real-world findings: CWEN-A base-symbol fallback exercised; ticker `CON`
  blocked git until `core.protectNTFS false`; measured LFS economics
  (~11.2 KB/file, ~6.9 MB/pull). Tasks scheduled: pull 22:05, push 23:00.
- Pre-reg #15 frozen 2026-08-19 (design note and full pre-registration;
  tool SHAs recorded in `PREREGISTRATION.md` §9).
- Pre-reg #23 (the paper loop) frozen 2026-08-23: `tools/paper_loop.py`
  byte-locked (FROZEN_SHA `c08b3ca5…`), the five frozen inputs asserted at
  import, `data/paper/` append-only; paper task scheduled 22:30 MT; the push
  now commits `data/paper` with the archive.
