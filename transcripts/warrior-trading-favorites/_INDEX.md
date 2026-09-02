# My Favorite Episodes — Reference Index

Source material for scrutiny and process/technique reference. **These are
claims, not evidence** — per DESIGN_BRIEF.md §6, anything claimed here that
looks testable gets pre-registered and measured against the calibrated
baselines before it counts for anything.

## Provenance (read before trusting anything)

| Field | Value |
|---|---|
| Playlist | [My Favorite Episodes](https://www.youtube.com/playlist?list=PL1xI23WKVWifjpSXo2rw7-mfPfWVFZ7Wk) |
| Playlist owner | **Ross Cameron - Warrior Trading** (official — unlike the fan-curated Class 1-12 list) |
| Videos | 25 in the playlist + 1 standalone (`Wd_iUsteoaw`, added 2026-09-01) |
| Non-Ross videos | 0 — the whole corpus is his own channel |
| Caption source | YouTube auto-generated (asr), fetched via `yt-dlp` 2026.7.4 on 2026-09-01 |
| Reproducibility | `python -X utf8 -m yt_dlp --skip-download --write-auto-subs --sub-langs "en.*" --sub-format vtt --write-info-json --output "transcripts/warrior-trading-favorites/raw/%(id)s.%(ext)s" <playlist-url> https://www.youtube.com/watch?v=Wd_iUsteoaw` then `python tools/vtt_to_md.py warrior-trading-favorites` |

**Caveats:**
- Transcripts are **auto-generated captions**: expect transcription errors
  (homophones, tickers, numbers) and `[Music]` markers. Timestamps per
  segment let you check any line against the source video.
- `txWaMpSzHhM` (Class 1) duplicates the copy already in
  [`../warrior-trading/`](../warrior-trading/_INDEX.md) — it is re-converted
  here so this folder is self-contained. Several 2022-2024 "beginners guide"
  videos substantially re-teach the same material as the 2015 classes
  (`ul34Jfh-LOk` is even exactly Class 1's length, 55:18 — topic overlap is
  heavy but it is a different recording, no "class one" framing).
- `Wd_iUsteoaw` ("Here's what's REALLY Happening...", uploaded 2026-09-01) is
  not a tutorial but a **market-regime trade recap**: seller control taking
  over from buyer control, leading-gainer breadth shrinking, monthly review
  discipline. Most current-dated source in the repo.
- Transcript files are **copyrighted content, kept local**: `raw/`, `*.md`,
  and `_meta.json` are gitignored. Only this index is tracked.

## Relevance to the repo (why this playlist)

Several episodes target machinery patternScanner already measures:

| Episodes | Repo hook |
|---|---|
| `mfGQr2tHoX0` (MACD step-by-step), `2n2Jt0PEPss` ($45k day, "30 minute MACD scalping") | the intraday veto's `macd_neg` leg — check his stated MACD rule against ours |
| `yFoBnM0iSlc` (relative volume) | `measure_rv.py`, `measure_speed.py` — his RV thresholds vs our calibrated ones |
| `hz7vhSIXXSc`, `ywim_dUSXe4` (dip trading / buying the dip) | entry-side measures (`measure_intraday_entry.py`) |
| `ZS8x6xK8-Vk`, `-0slMH7N6eI` (timing entries & exits, scalping) | exit-side measures (`measure_intraday_exit.py`, `measure_stop_placement.py`) |
| `KzVbXzkoZkA` (adding to winners / scaling) | position-growth assumptions in the paper loop |
| `afNhgCc-LCw` (short squeezes), `HYoQYCBW4sw`, `ul34Jfh-LOk`, `4Pc_von1wS4` (candlesticks) | candidate pattern definitions — v1 detector stays rule-based per DESIGN_BRIEF §3 |
| `GMRmMf-RsfE`, `j1tvgmKG9Vw`, `e5RK1-IzFQc` (small-account challenges) | claim-scan targets, same posture as `$583 → $335k` in ledger §I |
| `UvXnnFPB1TY` (157 min full training) | largest single source here; overlaps the ultimate-guide course |

## The corpus

| # | ID | Title | Uploaded | Duration | Transcript |
|---|---|---|---|---|---|
| 1 | `ul34Jfh-LOk` | How to Read Candlestick Charts (with ZERO experience) | 2023-11-29 | 55:18 | [ul34Jfh-LOk.md](ul34Jfh-LOk.md) |
| 2 | `5X_ZcifasBg` | The Simplest Day Trading Strategy for Beginners (with ZERO experience) | 2022-03-27 | 18:26 | [5X_ZcifasBg.md](5X_ZcifasBg.md) |
| 3 | `3rEakODkiEg` | The ULTIMATE Beginners Guide to Trading (with ZERO experience) | 2024-02-09 | 49:02 | [3rEakODkiEg.md](3rEakODkiEg.md) |
| 4 | `GMRmMf-RsfE` | How I turned $600 into $16,013.06 in 20 days \| SMALL ACCOUNT CHALLENGE | 2024-03-19 | 48:08 | [GMRmMf-RsfE.md](GMRmMf-RsfE.md) |
| 5 | `UvXnnFPB1TY` | How to Start Day Trading from ZERO (Full Training) | 2024-04-28 | 157:50 | [UvXnnFPB1TY.md](UvXnnFPB1TY.md) |
| 6 | `mfGQr2tHoX0` | How I Nailed Trading with the MACD Indicator (Step-by-Step Guide) | 2024-05-20 | 21:58 | [mfGQr2tHoX0.md](mfGQr2tHoX0.md) |
| 7 | `txWaMpSzHhM` | Ultimate Day Trading Strategy Guide 📚🍏 for Beginners *(= Class 1)* | 2015-03-31 | 55:18 | [txWaMpSzHhM.md](txWaMpSzHhM.md) |
| 8 | `hz7vhSIXXSc` | Dip Trading was HARD Until I Learned These 3 Simple Tricks... | 2024-04-24 | 51:54 | [hz7vhSIXXSc.md](hz7vhSIXXSc.md) |
| 9 | `ZS8x6xK8-Vk` | Ultimate Beginners Guide to Timing Entries & Exits for Momentum/Trend Trading | 2022-04-04 | 83:10 | [ZS8x6xK8-Vk.md](ZS8x6xK8-Vk.md) |
| 10 | `-0slMH7N6eI` | How to Scalp Trade (with ZERO experience) | 2022-04-11 | 106:54 | [-0slMH7N6eI.md](-0slMH7N6eI.md) |
| 11 | `afNhgCc-LCw` | Ultimate Guide to Trading a Short Squeeze for Beginner Traders | 2021-11-02 | 92:58 | [afNhgCc-LCw.md](afNhgCc-LCw.md) |
| 12 | `ywim_dUSXe4` | How to Buy the Dip (with ZERO experience) | 2021-09-27 | 95:15 | [ywim_dUSXe4.md](ywim_dUSXe4.md) |
| 13 | `U0fmwn7742A` | How to Start Day Trading for Beginners (LIVE STREAM) | 2020-04-05 | 59:20 | [U0fmwn7742A.md](U0fmwn7742A.md) |
| 14 | `dkOyu_kLKjE` | Day Trading Strategies for Beginners (Ultimate Step-by-Step Guide) | 2023-04-18 | 75:50 | [dkOyu_kLKjE.md](dkOyu_kLKjE.md) |
| 15 | `HYoQYCBW4sw` | Master This ONE Candlestick Pattern TODAY (Full Training) | 2024-04-01 | 55:11 | [HYoQYCBW4sw.md](HYoQYCBW4sw.md) |
| 16 | `GXl6IS4fSOE` | This Is My #1 Indicator For Trading 🍏 (Full Training) | 2023-04-12 | 73:45 | [GXl6IS4fSOE.md](GXl6IS4fSOE.md) |
| 17 | `KzVbXzkoZkA` | Ultimate Guide on ADDING to Winners with Scaling 🍏 (LIVE STREAM) | 2023-04-04 | 97:30 | [KzVbXzkoZkA.md](KzVbXzkoZkA.md) |
| 18 | `j1tvgmKG9Vw` | I Wish I Knew This BEFORE I Started Day Trading 🤦‍♂️ Small Account Challenge | 2019-11-30 | 39:38 | [j1tvgmKG9Vw.md](j1tvgmKG9Vw.md) |
| 19 | `yFoBnM0iSlc` | How to use the Relative Volume Trading Strategy (with ZERO experience) | 2020-07-11 | 39:34 | [yFoBnM0iSlc.md](yFoBnM0iSlc.md) |
| 20 | `4Pc_von1wS4` | Reading Candlestick Charts Was HARD Until I Learned This 3 Step Trick | 2024-05-07 | 48:14 | [4Pc_von1wS4.md](4Pc_von1wS4.md) |
| 21 | `PtFKChlL7wE` | NEW 💥How Much Money Do You REALLY Need To Start Trading?! | 2024-07-31 | 59:14 | [PtFKChlL7wE.md](PtFKChlL7wE.md) |
| 22 | `2n2Jt0PEPss` | +$45,546.52 TODAY with the 30 Minute MACD Scalping Strategy | 2024-07-23 | 59:55 | [2n2Jt0PEPss.md](2n2Jt0PEPss.md) |
| 23 | `MiNV8UL18J4` | Trading was HARD Until I Learned These 3 SIMPLE Concepts | 2024-07-27 | 26:48 | [MiNV8UL18J4.md](MiNV8UL18J4.md) |
| 24 | `e5RK1-IzFQc` | NEW 💥 I Wish I Knew This BEFORE I Started Day Trading | 2024-08-24 | 38:57 | [e5RK1-IzFQc.md](e5RK1-IzFQc.md) |
| 25 | `IlsQCdU9JO0` | Inside My $280,000 Mobile Day Trading Station (Solar, Starlink & 5G) | 2024-09-14 | 26:02 | [IlsQCdU9JO0.md](IlsQCdU9JO0.md) |
| — | `Wd_iUsteoaw` | Here's what's REALLY Happening... *(standalone, market-regime recap)* | 2026-09-01 | 29:55 | [Wd_iUsteoaw.md](Wd_iUsteoaw.md) |

## How to use this for scrutiny

1. **Read with the expert-claim posture.** The red-flag titles are the ones to
   test first: the small-account-challenge episodes (#4, #18, #24) and the
   "$45,546.52 TODAY" episode (#22) are exactly the kind of claim DESIGN_BRIEF
   §6 says to measure against buy-and-hold after costs — not to take on faith.
2. **File structure.** Each `*.md` has YAML frontmatter with `topics` and
   `claims` arrays, filled from the 2026-09-01 claim scan (ledger §J: pilot
   11 rows + 465 rows across the other 25 videos; all quotes machine-verified
   against the transcripts). Headline findings: his primary MACD gate
   (line-vs-signal "open", J-B-01) is *not* what our veto implements
   (`macd_neg` = line < 0) and is untested; the gate as practiced adds two
   conjuncts (new-highs, ~50% retrace floor) plus a ~30-minute window
   (2n2-07/08/12); RV is used as a selection screen at 5× vs the frozen 2.0;
   and the first regime claims with an operational proxy (leading-gainer
   strength, Wd_-01) arrive in the newest video.
3. **Extracting testable claims.** When a video states a concrete, computable
   rule (setup → signal → entry/exit), pre-register it in
   [CLAIMS_LEDGER.md](../../CLAIMS_LEDGER.md) and measure against the
   calibrated baselines before it counts. The MACD (#6, #22) and RV (#19)
   episodes are the fastest paths to claims that touch existing measurement
   code.
4. **Process/technique only.** Nothing here feeds the detector at runtime.

## Files

```
transcripts/warrior-trading-favorites/
├── _INDEX.md        ← this file (tracked)
├── _meta.json       ← machine-readable metadata (local only)
├── raw/             ← original .vtt captions + yt-dlp info jsons (local only)
└── <id>.md          ← clean timestamped transcripts (local only)
```