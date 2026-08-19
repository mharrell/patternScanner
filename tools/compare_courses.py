"""Course-drift comparison: quantitative language layer.

Compares the two Ross Cameron corpora (a decade apart) on language, not
on claims:
  - UG  : transcripts/ultimate-guide/oxob0x0Xz7s.md   (2025-01-01, polished
          slide-deck course, ~3h06, ~38k words)
  - WT  : the 8 Ross-Cameron videos of the fan-curated playlist
          (2015-03-31 .. 2019-10-12, classroom footage + retrospectives)
          with a "WT-classroom" subset (the 4 teaching videos from 2015:
          Class 1/3/4, Level 2 & Time & Sales)

Outputs ONLY counts and rates — no transcript text is printed (the
transcripts are copyrighted, local-only content; the ledger rows carry
the quotes).

Measures:
  1. Corpus sizes (words after stripping timestamps/frontmatter).
  2. 6-word-gram overlap UG vs each WT video and vs the combined WT set
     (recomputation of the prior index check — prior finding: max 13 of
     38,166 grams shared).
  3. Per-1,000-word occurrence rates for curated regex patterns (indicators,
     rule phrases, parameters, process vocabulary), UG vs WT-classroom vs
     WT-all — the drift-discriminating language.

Usage: python -X utf8 tools/compare_courses.py
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UG = ROOT / "transcripts" / "ultimate-guide" / "oxob0x0Xz7s.md"
WT_DIR = ROOT / "transcripts" / "warrior-trading"

# the 8 Ross-Cameron videos of the playlist (index order)
WT_ROSS = ["txWaMpSzHhM", "7UZushUSpLQ", "jfe1Zl-5EQI", "xTPcI7HHu5w",
           "pJuG5YtVF84", "H82nRY9TYU4", "XzrpLOH0nwU", "dqrTrFpZdcI"]
# the 4 teaching videos from 2015 (cleanest classroom comparison)
WT_CLASSROOM = ["txWaMpSzHhM", "7UZushUSpLQ", "jfe1Zl-5EQI", "pJuG5YtVF84"]

# pattern -> label. Multi-word/percent patterns handled via regex on the
# whitespace-normalized lowercase text.
PATTERNS = [
    # indicators
    (r"\brsi\b", "RSI"),
    (r"\bmacd\b", "MACD"),
    (r"\bvwap\b", "VWAP"),
    (r"\bema\b", "EMA"),
    (r"moving average", "moving average"),
    # rule vocabulary
    (r"break\s?out", "breakout"),
    (r"pull\s?back", "pullback"),
    (r"reversal", "reversal"),
    (r"momentum", "momentum"),
    (r"consolidat", "consolidat*"),
    (r"retrace", "retrace"),
    (r"\bflag\b", "flag"),
    (r"double (top|bottom)", "double top/bottom"),
    (r"new high", "new high"),
    (r"high of (the )?day", "high of day"),
    (r"low of (the )?day", "low of day"),
    (r"first and (the )?second", "first and second"),
    (r"third.*pullback", "third pullback"),
    (r"confirm", "confirm*"),
    (r"squeeze", "squeeze"),
    (r"apex", "apex"),
    # selection vocabulary
    (r"float", "float"),
    (r"low float", "low float"),
    (r"catalyst", "catalyst"),
    (r"\bnews\b", "news"),
    (r"\bgap\b", "gap"),
    (r"relative volume", "relative volume"),
    (r"scanner", "scanner"),
    (r"volume", "volume"),
    (r"supply", "supply"),
    (r"demand", "demand"),
    # exit / risk vocabulary
    (r"stop loss", "stop loss"),
    (r"\bstop\b", "stop"),
    (r"profit target", "profit target"),
    (r"target", "target"),
    (r"break ?even", "break even"),
    (r"trailing", "trailing"),
    (r"scale out", "scale out"),
    (r"sell half", "sell half"),
    (r"risk", "risk"),
    (r"reward", "reward"),
    (r"2:1|two to one|two-to-one", "2:1 R:R"),
    (r"3:1|three to one|three-to-one", "3:1 R:R"),
    # process / psychology
    (r"simulator", "simulator"),
    (r"phase", "phase"),
    (r"rehab", "rehab"),
    (r"emotion", "emotion"),
    (r"discipline", "discipline"),
    (r"plan", "plan"),
    (r"strike", "strike(s)"),
    (r"losing streak", "losing streak"),
    (r"red candle", "red candle"),
    (r"give back", "give back"),
    # market structure / data
    (r"support", "support"),
    (r"resistance", "resistance"),
    (r"volume weighted", "volume weighted"),
    (r"pre[- ]?market", "pre-market"),
    (r"market maker", "market maker"),
    (r"level 2", "level 2"),
    (r"time and sales", "time and sales"),
    (r"liquidity", "liquidity"),
    (r"volatility", "volatility"),
    (r"overbought", "overbought"),
    (r"oversold", "oversold"),
    (r"high frequency", "high-frequency"),
    # time windows
    (r"9:30", "9:30"),
    (r"10:00", "10:00"),
    (r"10:30", "10:30"),
    (r"11:30", "11:30"),
    (r"12:00", "12:00"),
    (r"7:00", "7:00"),
    (r"first 5 minutes|first five minutes", "first 5 min"),
    (r"first 10 minutes|first ten minutes", "first 10 min"),
    (r"first hour", "first hour"),
    # accuracy / performance rhetoric
    (r"accuracy", "accuracy"),
    (r"win rate", "win rate"),
    (r"verified", "verified"),
    (r"back[- ]?test", "back-test*"),
    (r"overfit", "overfit"),
    (r"consistent", "consistent"),
    # numbers
    (r"\b33\s*%", "33%"),
    (r"\b40\s*%", "40%"),
    (r"\b60\s*%", "60%"),
    (r"\b66\s*%", "66%"),
    (r"\b70\s*%", "70%"),
    (r"\b80\s*%", "80%"),
    (r"\b85\s*%", "85%"),
    (r"\b90\s*%", "90%"),
    (r"\b100\s*%", "100%"),
    (r"\b500\s*%|five hundred percent", "500% RV"),
    (r"10 ?x|ten times", "10x"),
    (r"half a million", "half a million"),
    (r"two million", "two million"),
    (r"25 million", "25 million"),
    (r"583", "$583"),
    (r"\bmillion\b", "million"),
]


def load(path: Path) -> str:
    """Read a transcript .md, strip frontmatter, timestamps, links, blanks."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)  # frontmatter
    text = re.sub(r"\[Open video\]\([^)]*\)", " ", text)
    text = re.sub(r"\[https?://[^]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[\[?\d{1,2}:\d{2}(?::\d{2})?\]?\]", " ", text)  # [mm:ss]
    text = re.sub(r"[#*_>`~|]", " ", text)
    text = re.sub(r"\[Music\]", " ", text)
    return text


def norm(text: str) -> str:
    """lowercase, collapse whitespace, keep punctuation (%, :, $)."""
    return re.sub(r"\s+", " ", text.lower())


def words(text: str) -> list:
    return re.findall(r"[a-z0-9:.]+", text.lower())


def grams(tokens: list, n: int):
    return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def main() -> int:
    # normalized text (punctuation preserved) drives the pattern counts;
    # token streams drive the word counts and n-gram overlap
    ug_raw = norm(load(UG))
    ug_tok = words(ug_raw)
    ug_join = " ".join(ug_tok)

    wt_raw = {}
    wt_tok = {}
    for vid in WT_ROSS:
        p = WT_DIR / f"{vid}.md"
        if p.exists():
            wt_raw[vid] = norm(load(p))
            wt_tok[vid] = words(wt_raw[vid])
    missing = [v for v in WT_ROSS if v not in wt_raw]
    if missing:
        print(f"missing WT transcripts: {missing}")
        return 1

    cls_raw = " ".join(wt_raw[v] for v in WT_CLASSROOM)
    all_raw = " ".join(wt_raw[v] for v in WT_ROSS)
    cls_join = " ".join(" ".join(wt_tok[v]) for v in WT_CLASSROOM)
    all_join = " ".join(" ".join(wt_tok[v]) for v in WT_ROSS)
    n_ug, n_cls, n_all = len(ug_tok), len(words(cls_join)), len(words(all_join))

    print(f"corpus sizes (words): UG {n_ug:,} | WT-classroom {n_cls:,} | "
          f"WT-all {n_all:,}")
    for v in WT_ROSS:
        print(f"  WT {v}: {len(wt_tok[v]):,}")

    # ---- 6-gram overlap (recomputation of the index's prior check) ----
    ug_6 = Counter(grams(ug_tok, 6))
    print(f"\n6-gram overlap UG vs WT: UG has {len(ug_6):,} distinct 6-grams")
    for v in WT_ROSS:
        wt_6 = Counter(grams(wt_tok[v], 6))
        shared = sum((ug_6 & wt_6).values())
        print(f"  {v}: shared {shared} (video distinct {len(wt_6):,})")
    wt_6 = Counter(grams(words(all_join), 6))
    shared_all = sum((ug_6 & wt_6).values())
    print(f"  combined WT: shared {shared_all} of {len(wt_6):,} distinct")

    # ---- pattern rates per 1,000 words ----
    print("\npattern rates per 1,000 words (UG | WT-classroom | WT-all; "
          "delta UG-cls):")
    rows = []
    for pat, label in PATTERNS:
        c_ug = len(re.findall(pat, ug_raw))
        c_cls = len(re.findall(pat, cls_raw))
        c_all = len(re.findall(pat, all_raw))
        r_ug = 1000.0 * c_ug / n_ug
        r_cls = 1000.0 * c_cls / n_cls
        r_all = 1000.0 * c_all / n_all
        rows.append((label, r_ug, r_cls, r_all, pat))
    for label, r_ug, r_cls, r_all, pat in rows:
        # flag: presence flips (0 in one corpus, >0 in the other) or
        # >2x relative difference with a minimum absolute gap
        flips = (r_ug == 0) != (r_cls == 0)
        gap = abs(r_cls - r_ug) >= 0.15
        ratio = (r_cls / r_ug if r_ug > 0 else float("inf"))
        rel = (ratio >= 2.0 or ratio <= 0.5) if r_ug > 0 else flips
        mark = "  <--" if (flips or (gap and rel)) else ""
        print(f"  {label:>22}: {r_ug:7.2f} | {r_cls:7.2f} | {r_all:7.2f}"
              f"{mark}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
