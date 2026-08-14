# Warrior Trading Class 1-12 — Reference Index

Source material for scrutiny and process/technique reference. **These are
claims, not evidence** — per DESIGN_BRIEF.md §6, anything claimed here that
looks testable gets pre-registered and measured against the calibrated
baselines before it counts for anything.

## Provenance (read before trusting anything)

| Field | Value |
|---|---|
| Playlist | [Warrior Trading Class 1-12](https://www.youtube.com/playlist?list=PL1jLaiDiYWURwUjq29tDd4zKfNN1QFbas) |
| Playlist owner | **StephenMcElroy1** — a fan-curated list, *not* an official Warrior Trading playlist |
| Videos by Ross Cameron | 8 of 13 unique videos |
| Videos by other channels | 5 (EatSleepProfit, Trading 212, Cameron Bennion, NeoScribe, Chris Williamson) |
| Caption source | YouTube auto-generated (asr), fetched via `yt-dlp` 2026.7.4 on 2026-08-13 |
| Reproducibility | `python -X utf8 -m yt_dlp --skip-download --write-auto-subs --sub-langs "en.*" --sub-format vtt --output "transcripts/warrior-trading/raw/%(id)s.%(ext)s" <watch-url...>` then `python tools/vtt_to_md.py` |

**Caveats:**
- Transcripts are **auto-generated captions**: expect transcription errors
  (homophones, tickers, numbers) and zero punctuation confidence. Timestamps
  per segment let you check any line against the source video.
- The playlist has **14 slots for 13 unique videos**: `txWaMpSzHhM` appears
  twice (slots 1 and 2). It opens with "welcome to class one" — this is Class 1.
- Two videos are **not trading content at all** (slots 9, 10) — they slipped
  into the loose fan playlist. Kept per request, marked in the table.
- Transcript files are **copyrighted content, kept local**: `raw/`, `*.md`,
  and `_meta.json` are gitignored. Only this index is tracked.
- **Claim-scanned 2026-08-14**: 53 ledger rows extracted from this corpus into
  [CLAIMS_LEDGER.md §I](../../CLAIMS_LEDGER.md) (video-id `[mm:ss]` citations,
  quotes re-verified against the transcripts). The 2 non-trading videos were
  skipped; `XzrpLOH0nwU` (Day Trading Station) is equipment content — nothing
  claim-worthy. `topics`/`claims` frontmatter is filled in all 13 transcripts.

## The corpus

| # | ID | Title | Channel | Uploaded | Duration | Transcript |
|---|---|---|---|---|---|---|
| 1 | `txWaMpSzHhM` | Ultimate Day Trading Strategy Guide 📚🍏 for Beginners *(Class 1)* | Ross Cameron - Warrior Trading | 2015-03-31 | 55:18 | [txWaMpSzHhM.md](txWaMpSzHhM.md) |
| 2 | `txWaMpSzHhM` | *(duplicate of #1)* | — | — | — | → see #1 |
| 3 | `7UZushUSpLQ` | Day Trading Strategies for Beginners: Class 3 of 12 | Ross Cameron - Warrior Trading | 2015-04-11 | 08:58 | [7UZushUSpLQ.md](7UZushUSpLQ.md) |
| 4 | `jfe1Zl-5EQI` | Day Trading Strategy (reversals) for Beginners: Class 4 of 12 | Ross Cameron - Warrior Trading | 2015-08-05 | 31:26 | [jfe1Zl-5EQI.md](jfe1Zl-5EQI.md) |
| 5 | `xTPcI7HHu5w` | How I turned $583 into $335,027.71 in 1 YEAR | Ross Cameron - Warrior Trading | 2018-02-04 | 49:18 | [xTPcI7HHu5w.md](xTPcI7HHu5w.md) |
| 6 | `lMZv0K71HOg` | How To Get Around The PDT Rule | EatSleepProfit | 2017-06-08 | 12:12 | [lMZv0K71HOg.md](lMZv0K71HOg.md) |
| 7 | `pJuG5YtVF84` | How to use Level 2 and Time & Sales as a Momentum Day Trader | Ross Cameron - Warrior Trading | 2015-11-03 | 28:54 | [pJuG5YtVF84.md](pJuG5YtVF84.md) |
| 8 | `H82nRY9TYU4` | $1 Million Dollar Challenge Complete! | Ross Cameron - Warrior Trading | 2019-05-01 | 39:52 | [H82nRY9TYU4.md](H82nRY9TYU4.md) |
| 9 | `hI4t61yvdLE` | The Age of Graphene — **NOT trading content** | NeoScribe | 2017-12-30 | 06:02 | [hI4t61yvdLE.md](hI4t61yvdLE.md) |
| 10 | `J736mfy7KEg` | David Sinclair: Can Humans Live 1000 Years? — **NOT trading content** | Chris Williamson | 2019-04-22 | 74:39 | [J736mfy7KEg.md](J736mfy7KEg.md) |
| 11 | `rgVdgR1y1Dg` | Beginner Guide to the RSI Indicator | Trading 212 | 2017-12-21 | 09:05 | [rgVdgR1y1Dg.md](rgVdgR1y1Dg.md) |
| 12 | `kZNF5Hynk4E` | Why You Lose Money With Robinhood | Cameron Bennion | 2018-12-28 | 13:35 | [kZNF5Hynk4E.md](kZNF5Hynk4E.md) |
| 13 | `XzrpLOH0nwU` | My BRAND NEW Day Trading Station | Ross Cameron - Warrior Trading | 2019-10-12 | 19:51 | [XzrpLOH0nwU.md](XzrpLOH0nwU.md) |
| 14 | `dqrTrFpZdcI` | My Biggest Struggle as a Day Trader | Ross Cameron - Warrior Trading | 2019-10-10 | 29:18 | [dqrTrFpZdcI.md](dqrTrFpZdcI.md) |

## How to use this for scrutiny

1. **Read with the expert-claim posture.** The red-flag titles are the ones to
   test first: *"$583 → $335,027 in 1 YEAR"* (#5) and *"$1 Million Challenge"*
   (#8) are exactly the kind of claim DESIGN_BRIEF §6 says to measure against
   buy-and-hold after costs — not to take on faith.
2. **File structure.** Each `*.md` has YAML frontmatter with `topics` and
   `claims` arrays, filled by the 2026-08-14 claim scan (§I ledger rows mapped
   back per video). Add to them as the corpus is re-read.
3. **Extracting testable claims.** When a video states a concrete, computable
   rule (setup → signal → entry/exit), that's a candidate to pre-register as a
   hypothesis. Done: [CLAIMS_LEDGER.md §I](../../CLAIMS_LEDGER.md) — one row
   per claim with episode reference, the rule as stated, and a status; verdicts
   return there after measurement.
4. **Process/technique only.** Nothing here feeds the detector at runtime.
   These inform candidate definitions and how he thinks about risk — the v1
   detector stays rule-based per DESIGN_BRIEF §3.

## Files

```
transcripts/warrior-trading/
├── _INDEX.md        ← this file (tracked)
├── _meta.json       ← machine-readable metadata (local only)
├── raw/             ← original .vtt captions (local only)
└── <id>.md          ← clean timestamped transcripts (local only)
```
