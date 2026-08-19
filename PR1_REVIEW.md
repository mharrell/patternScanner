# PR #1 review — Intraday accumulation track: 1-min archive pipeline

**For:** the session that generated this branch (worktree-intraday-accumulation).
**From:** the main session (review of PR #1, 2026-08-18/19).
**Reviewed artifact:** commit `b550b29` (PR #1, 1 commit, +1466 across 38 files).
**Method:** independent verification — full read of both tools, byte-level
hash checks, pull-chain validation, and live re-runs of the QA tool on the
stored data. Nothing below is inferred; everything is reproduced.

**Verdict overall:** the design is sound (append-only immutability, atomic
writes, manifest-of-evidence, repair-first audit trail, blind full-universe
capture). Two P1 correctness bugs and a few integrity-reporting gaps should
be fixed before merge. None of them change the track's architecture.

---

## P1 — QA coverage gate measures the wrong window (`tools/qa_intraday.py:43`)

```python
RTH_OPEN, RTH_CLOSE = 9, 30     # 09:30 ET
return (t.hour * 60 + t.minute >= RTH_OPEN * 60 + RTH_OPEN) & \
       (t.hour * 60 + t.minute < RTH_END_H * 60 + RTH_END_M)
```

`RTH_OPEN * 60 + RTH_OPEN` = 549 = **09:09**, not 570 = 09:30. `RTH_CLOSE`
(= 30) is defined at line 42 and never used anywhere — it was clearly meant
for this expression.

**Reproduction (live, on the stored data):**

```
qa_intraday.check_one("2026-08-12/AAPL.parquet", {}, {})
    -> rth_rows = 411, rth_cov = 1.0538
same file, same mask with lower bound 570:
    -> 390 rows (exactly the 390 RTH minutes)
```

The committed `data/intraday/qa_report.md` therefore shows liquid names at
**105.4% RTH coverage** — a physically impossible number — in the same
document whose "Known expected patterns" section claims "AAPL/MSFT/SPY
390/390 RTH". The report contradicts itself because the gate is wrong.

**Consequences:** every RTH-coverage figure in the committed report is off;
the 98% completeness gate counts 21 pre-market minutes (09:09–09:29) as RTH.
The delta is data-dependent (AAPL/MSFT +21, SPY +6 — SPY's pre-market bars
start ~09:24), so it's not a constant offset.

**Fix (one line):** `RTH_OPEN * 60 + RTH_CLOSE`.

---

## P1 — crashed-pull orphan recovery is a dead end (`tools/fetch_intraday_bars.py:226–230` + `504–506`)

The orphan-walk error (lines 226–230) — the state after a crash mid-pull,
where some parquets were written but the manifest never was — tells the
operator:

> "If they came from a crashed pull they are valid data: **--repair each
> with a reason** and the next pull re-writes them from the window."

But `do_repair` refuses exactly these files (lines 504–506):

```python
if rel not in manifest["files"]:
    print(f"ABORT: {rel} has no manifest entry — nothing to repair", ...)
```

An orphan by definition has **no** manifest entry. There is no tool path
that removes or adopts an orphan: `verify_manifest` aborts while they
exist, `--repair` refuses them, and the only exit is hand-deleting files —
which the append-only contract forbids. Every subsequent pull aborts
forever.

**Fix options:** (a) let `--repair` accept an orphan (record the deletion in
`repairs.json` without a manifest entry), or (b) add an `--adopt` mode that
hashes + registers crashed-pull files after verification. Either way, the
error message must not prescribe a command that refuses the file.

---

## P2 — the envelope check can be silently vacuous (`tools/qa_intraday.py:123–140`, `144–155`)

- `daily_missing` (line 124) is set when the daily bar is absent, but it
  never surfaces: it's not a note, not in the anomaly table, not in the
  summary counts.
- `load_daily_cache` (lines 144–155) swallows **all** load errors
  (`except Exception: pass`) — if the cache fails to load, the envelope
  check silently does nothing.

**In the committed `qa_report.md`, this is exactly what happened:**
the daily cache ends **2025-12-31** (no 2026 daily bars exist for any
name), and AAPL/MSFT aren't in it at all. So the envelope/volume check did
not run for 27 of 30 files — yet the summary reads "envelope violations
(high/low): 0 / 0" and "volume-sum mismatches (> 2%): 0", indistinguishable
from "everything passed". (The "no daily bar for 2026-08-12" notes appear
only for names present in the cache with a stale date — SPY, AAMI, AAP,
AAT.)

**Fix:** surface a `daily_missing` count in the summary and/or per-file
notes; report cache load failures loudly.

---

## P2 — the crashed-repair zombie state (no recovery path)

`do_repair` performs three steps in sequence:
1. write `repairs.json` (atomic) — the repair record
2. `p.unlink()` — delete the file
3. write `manifest.json` (atomic) — drop the entry

A crash between steps 2 and 3 leaves: **file missing + manifest entry
present + repair record present.** In that state:

- `verify_manifest` line 200 (`if rel in repaired: continue`) silently
  skips the missing file — no error, no abort. The design's promise is
  "loud, not silent"; this is the one silent path.
- Once the bar-date ages out of the 7-day window, no drift note is emitted
  either — a completely silent, permanent zombie that counts as
  "verified-ok" in every pull record.
- No sanctioned recovery exists: `do_repair` refuses missing files
  (lines 507–511), and no other code path removes a manifest entry.

**Fix options:** (a) if a repair record exists but the file is missing
*and* the manifest entry exists, treat it as a completed repair and drop
the entry at load; or (b) give `--repair` a `--force` for the
manifest-entry-only state.

---

## P2 — README contradicts the code on repair semantics (`data/intraday/README.md:102–103`)

README: "Verification skips repaired paths (**the manifest entry is
retained** as historical evidence)."

Code: `do_repair` **removes** the manifest entry
(`manifest["files"].pop(rel)`, line 512) — its docstring says so, so the
next pull can re-write the (date, ticker) fresh. The README sentence is
stale relative to the code. Update the README to match the implemented
semantics (entry removed after the repair is recorded; the entry's full
record is preserved in `repairs.json`).

---

## P3 — `--qa` masks ticker failures (`tools/fetch_intraday_bars.py:445–447`)

```python
if args.qa:
    from qa_intraday import main as qa_main
    return qa_main([]) or EXIT_OK
```

The `--qa` path returns `EXIT_OK` regardless of `tickers_failed` /
`tickers_no_data` — the scheduled task (which uses `--qa`) reports success
while the pull record shows failures. Without `--qa`, the exit code is 1.
The scheduled task should see the pull's real exit status. Suggested:
`return qa_main([]) or EXIT_TICKER_FAILURES` (or a dedicated combination).

## P3 — committed `qa_report.md` bakes in an absolute path

The report's "Daily envelope source" line contains the worktree's absolute
path (`C:\...\patternScanner\.claude\worktrees\intraday-accumulation\data\cache\bars`).
Cosmetic — the report is regenerated nightly — but it's committed evidence;
a relative or generic label is cleaner.

---

## Verified non-findings (checked, all fine)

| Check | Result |
|---|---|
| Universe CSV (`universe_sp600_2026-08-13.csv`) tracked? | Yes — already in main (a5939a9) |
| LFS objects pushed to remote? | Yes — `media.githubusercontent.com` returns 200 (30,849 B for AAPL) |
| All 30 stored parquets SHA-match the manifest? | 0 mismatches |
| Pull-chain hashes valid (`prev_pull_sha256`)? | Yes, all 5 records |
| Worktree tool files == committed files? | Identical (CRLF noise only) |
| `to_parquet()` bytes call (pandas 3.0)? | pandas 3.0.1 installed — fine |
| Yahoo retry for-else logic | Correct |
| `complete_dates` span (8 days) vs 7-day window | Covers the edge |
| Manifest `files_verified` accounting | Consistent |

---

## Appendix (for the main session's follow-up, not this PR)

Separate review of `tools/compare_courses.py` (committed 7e0b1b6, the
course-drift comparison tool) surfaced — verified by re-run — that the
6-gram overlap numbers quoted in CLAIMS_LEDGER §I.12 and
`transcripts/ultimate-guide/_INDEX.md` are on a mixed basis:
occurrence-weighted "102 of 46,051" is 94 distinct, ~35 after removing
contraction-fragment artifacts, and 35 of the combined set span video
boundaries. The "essentially zero surface reuse" verdict survives; the
exact numbers need amending. Two table rows in §I.12 are also wrong:
"third pullback" (the pattern matched "third-party…", literal count 0 in
both corpora) and "60%" for the classroom (its sole "60%" hit is an HFT
market-share sentence, not win-rate language). No drift verdicts change.
