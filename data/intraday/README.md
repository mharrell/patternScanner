# Intraday accumulation track — 1-minute OHLCV archive (v1)

**Status: pipeline merged to main 2026-08-19 (PR #1, merge `3541eea`);
nightly pull scheduled (Task Scheduler `\patternScanner-intraday-pull`,
22:05 MT, `--qa`) plus a nightly push (`\patternScanner-intraday-push`,
23:00 MT, `tools\push_intraday_archive.cmd`); the archive is accumulating
forward — the first scheduled pull is 2026-08-19 22:05 MT. Operations
(morning checks, failure modes, re-creating the tasks): see
[INTRAday_OPERATIONS.md](../../INTRAday_OPERATIONS.md).**

The intraday track extends patternScanner beyond daily bars: the untested
ledger claims (B-01 micro pullback, I-B-01, I-C-02/03/04, E-01/E-04 1-min
MACD, F-01 7–10 a.m. window, F-02 pre-market, I-E-02) are stated on 1-minute
charts. The archive is accumulated forward, nightly, from the free Yahoo
1-minute series (rolling 7-day window — Yahoo's hard cap), with extended
hours (04:00–20:00 ET) included.

**This archive is a research artifact, not investment advice. No execution,
no real money.**

## Why accumulate instead of backfill

Decided with Mike, 2026-08-18. A forward-accumulated archive captures every
name **while it is alive** — a name that later delists stays in the archive,
in full, including its final weeks. Deaths are captured at capture time, not
erased retroactively, so the classic survivorship bias of *retrospective*
reconstruction does not exist here; the archive is exactly the set of names a
day trader could actually have traded *going forward*. The cost is time: the
archive only contains whatever regimes the market delivers next.

## Pre-registration #15 design note — §5 gate for the intraday track

Frozen 2026-08-18 (design note only; the full pre-registration is written
before any measurement):

> **§5 gate (intraday track):** the universe is the live S&P 600 membership,
> pulled blindly and continuously; membership is tracked per pull date (the
> universe file used and its SHA-256 are recorded in every pull record);
> names are captured until they stop trading and are **never dropped
> retroactively**. The retrospective historical-constituent gate (pre-reg
> #13/#14) is replaced by continuous capture, per Mike's decision 2026-08-18.

The one discipline this demands: the pull list is always the full membership
file — no cherry-picking "interesting" names — because selective inclusion
is how the bias sneaks back in. The pull script enforces this by taking the
whole CSV every run. When membership changes, a **new** universe CSV is
created (`universe_sp600_<date>.csv`); the frozen snapshot is never edited.

The full pre-registration is **PREREGISTRATION.md §Pre-registration #15**
(frozen 2026-08-19): B-01 micro pullback on 1-minute bars (primary), the
B-02/I-E-02 pullback-vs-chase contrast (F3), and the F-01/F-02 time-of-day
measurement rows. Measurement is gated on its §5 floors (≥ 20
full-universe bar-dates ≥ 2026-08-19).

## Layout

| Path | Contents | Git |
|---|---|---|
| `raw/<YYYY-MM-DD>/<TICKER>.parquet` | Immutable day bars: tz-aware `America/New_York` DatetimeIndex, floored to the minute, OHLCV unadjusted, extended hours included | **LFS-tracked** |
| `manifest.json` | Cumulative ledger: per-file SHA-256 + rows + span + pull-id; one pull record per run | tracked |
| `repairs.json` | Deliberate deletions (path, sha-before, reason, UTC time) — evidence | tracked |
| `splits.json` | Recorded split events (see procedure below) | tracked |
| `qa_report.md` | Latest QA pass output — flags only, nothing fixed | tracked |
| `.lock` | Pull lock; a leftover lock aborts the next run with instructions | never committed |

## Design contract (the "can't corrupt it" rules)

1. **Append-only immutability.** Each (bar-date, ticker) file is written
   once, by the first pull that sees the bar-date complete; never modified.
2. **Atomic writes.** Temp file → fsync → `os.replace`; a crash mid-write
   can never leave a partial file as the visible state.
3. **Manifest of evidence.** Every run re-hashes **all** recorded files and
   walks `raw/` for orphans **before** writing anything. A missing, corrupt,
   or unrecorded file aborts the pull with a loud error — it is **never
   silently regenerated**. Crashed-pull orphans are recovered with
   `--adopt` (kept, hash-verified) or `--repair` (deleted with a record).
4. **No partial days.** A bar-date is written only after its full
   04:00–20:00 ET session has closed (D < today(ET), or D == today(ET) and
   now(ET) ≥ 20:01). Data is only ever written after the fact.
5. **Idempotent.** Re-running the same day produces the same files
   (first-write-wins; later windows skip and drift-check). A failed pull
   retries the missing pieces next run.
6. **Timezone discipline.** Timestamps are tz-aware `America/New_York`,
   floored to the minute. A naive timestamp is an error at load.
7. **Blind full-universe capture.** See the §5 gate note above.
8. **Unadjusted + recorded splits.** Intraday OHLCV is stored raw. Split
   events are recorded in `splits.json`, never folded into stored data;
   renormalization is a measurement-time concern and never rewrites files.
9. **Loud failures.** Failed tickers land in the pull record and print;
   drift (possible Yahoo restatement) is reported, never auto-fixed.

## Nightly schedule (Windows Task Scheduler)

Two tasks, both with `StartWhenAvailable` (if the machine is off, they run
at next wake):

| Task | When | What |
|---|---|---|
| `\patternScanner-intraday-pull` | daily 22:05 MT | `C:\Python312\python.exe -X utf8 <repo>\tools\fetch_intraday_bars.py --qa` (Start in: repo root) |
| `\patternScanner-intraday-push` | daily 23:00 MT | `tools\push_intraday_archive.cmd` — commits `data/intraday` only, fast-forwards main first, pushes, logs to `%TEMP%\intraday_push.log` |

The pull runs after the 04:00–20:00 ET session close (session ends 20:00 ET
= 18:00 MT) and outside DeepSeek peak pricing. The push script skips itself
if a pull is still running (`.lock` present) and never touches files
outside `data/intraday`.

## Operations

### Repair (the only sanctioned way to remove data)

```bat
python -X utf8 tools\fetch_intraday_bars.py --repair "2026-08-18/AAP.parquet" --reason "what happened, who decided"
```

Records the deletion in `repairs.json` **first**, then deletes the file and
removes the manifest entry. The full manifest record (sha256, rows, span,
pull-id) is preserved inside the repair record — the entry itself is removed
so the next pull can re-write the (date, ticker) fresh if the window still
covers it. `--repair` also works on crashed-pull orphans (no manifest entry):
the deletion is recorded, nothing else changes. Anything deleted without a
repair record aborts the next pull loudly.

If a crash interrupts a repair (record written, file deleted, entry not yet
dropped), the next pull detects the state and completes the recorded repair
loudly — a manifest entry whose file is gone is never counted as verified.

### Adopting crashed-pull orphans

A pull that crashed mid-run may leave valid parquet files the manifest never
recorded. The next pull aborts on them (files without a ledger are never
trusted). Two sanctioned recoveries:

```bat
python -X utf8 tools\fetch_intraday_bars.py --adopt "2026-08-18/XYZ.parquet" --reason "crashed-pull file, hash-verified"
python -X utf8 tools\fetch_intraday_bars.py --repair "2026-08-18/XYZ.parquet" --reason "orphan from crashed pull, re-fetch"
```

`--adopt` schema-checks the file (tz-aware, minute-floored, sorted, unique,
single bar-date, OHLCV columns) and registers it in the manifest — it becomes
a normal, permanently verified archive member, drift-checked like any other.
`--repair` deletes it with a record; the next pull re-fetches it from the
7-day window while the window lasts. Adopt preserves the data; repair is for
files you don't trust or want re-fetched.

### Recording a split event

When a split is detected (sustained envelope/volume breaks in
`qa_report.md`, or announced): append to `splits.json` (edit the tracked
file, commit):

```json
{"ticker": "XYZ", "ex_date": "2026-09-01", "ratio": 2.0, "source": "announcement/qa-signature", "recorded_utc": "..."}
```

Stored bars are never rewritten; the split table is applied at measurement
time only.

### Membership changes

Create `data/cache/universe_sp600_<date>.csv` (same schema), commit it, and
start passing `--universe` that path in the scheduled task. The old CSV and
all pull records remain — the universe history is reconstructible from the
manifest.

### Restoring a corrupt file

The manifest records the SHA-256 and the file is LFS-tracked in git: restore
from the last push (`git lfs pull`), or — if the corruption predates the
archive's LFS history and the file is irrecoverable — `--repair` it with a
reason. Never re-fetch to "fix" stored data.

## Testing notes (2026-08-18, worktree)

The pipeline was live-tested with `--limit 3` in the worktree: first pull,
idempotent re-run (byte-identical files, only the pull record grows),
corruption abort (tampered parquet → SHA-256 failure → nothing written),
`--repair` flow, and QA report generation. See the worktree branch commit
for the test artifacts.

## LFS notes

`raw/**` is LFS-tracked (`.gitattributes`). GitHub free tier: 1 GB LFS
storage / 1 GB bandwidth per month. Measured on the first full-universe pull
(2026-08-19, 603 tickers): ~11.2 KB per file, ~6.9 MB per pull — about
**2.5 GB/year**, i.e. a **~4.7-month storage horizon** on the free quota
(the earlier 1 GB/year estimate was optimistic). Bandwidth is fine
(~210 MB/month). Local disk remains the primary store; revisit (releases,
pruning, or a vendor backfill) before the cap.

**Windows reserved device names.** The S&P 600 contains a ticker literally
named `CON`, which Windows treats as a reserved device name: Python writes
`CON.parquet` fine, but git-for-Windows refuses to open it unless
`core.protectNTFS` is `false` (repo-local). The push script sets it
self-healing on every run; a fresh clone of the archive needs the same
setting before `git lfs pull` restores `CON.parquet`.
