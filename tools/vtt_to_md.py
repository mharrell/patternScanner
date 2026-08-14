"""Convert YouTube auto-caption .vtt files into clean, timestamped markdown.

Input : transcripts/<series>/_meta.json (playlist metadata, see below) and
        transcripts/<series>/raw/<video_id>.en.vtt (raw captions).
Output: transcripts/<series>/<video_id>.md per unique video.

The raw .vtt is YouTube's auto-caption format: every spoken segment appears
twice (a word-timed rolling line and a plain snapshot line). This converter
strips all markup, then merges the rolling overlaps back into readable prose
while keeping a [MM:SS] timestamp per segment, so every line stays traceable
to the video.

_meta.json shape (see build step in the ingestion flow):
{
  "playlist_title": "...", "playlist_owner": "...", "playlist_url": "...",
  "retrieved": "YYYY-MM-DD", "captions_source": "...",
  "videos": [ {"id","title","channel","upload_date","duration","url","playlist_index"}, ... ]
}
"""
import html
import json
import re
import sys
from pathlib import Path

TRANSCRIPTS = Path(__file__).resolve().parent.parent / "transcripts"

CUE_TS = re.compile(
    r"(\d{1,2}):(\d{2}):(\d{2})[.,](\d{3})\s+-->\s+"
)
TAG = re.compile(r"<[^>]*>")


def clean(text: str) -> str:
    """Strip VTT markup, unescape entities, collapse whitespace."""
    text = TAG.sub("", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_cues(vtt: str):
    """Yield (start_seconds, cleaned_text) for every non-empty cue."""
    for block in re.split(r"\n[ \t]*\n", vtt):
        lines = block.strip().split("\n")
        if not lines:
            continue
        m = CUE_TS.match(lines[0])
        if not m:
            continue  # WEBVTT header, kind/lang lines, stray text
        h, mm, s, frac = (int(x) for x in m.groups())
        start = h * 3600 + mm * 60 + s + frac / 1000.0
        body = " ".join(lines[1:]).strip()
        if not body:
            continue
        text = clean(body)
        if text:
            yield start, text


def overlap_len(prev: str, cur: str) -> int:
    """Longest suffix of prev that is a prefix of cur."""
    maxk = min(len(prev), len(cur))
    for k in range(maxk, 0, -1):
        if prev[-k:] == cur[:k]:
            return k
    return 0


def merge_cues(cues):
    """Merge rolling YouTube captions into (start, displayed_text) segments."""
    out = []
    prev = ""
    for start, text in cues:
        if not text or text == prev:
            continue
        overlap = overlap_len(prev, text)
        if overlap == len(text) and overlap >= 3:
            # text is just a redundant snapshot of what we already have
            continue
        if overlap >= 3 and (text[overlap] in " .,;:!?-" or overlap == len(text)):
            add = text[overlap:]
            if add.strip():
                out.append((start, add.strip()))
        else:
            out.append((start, text))
        prev = text
    return out


def mmss(sec: float) -> str:
    s = int(round(sec))
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def yaml_val(v):
    """Format a value for YAML frontmatter (None -> null)."""
    return "null" if v is None else repr(v)


def main() -> int:
    series = sys.argv[1] if len(sys.argv) > 1 else "warrior-trading"
    series_dir = TRANSCRIPTS / series
    meta = json.loads((series_dir / "_meta.json").read_text(encoding="utf-8"))

    # Dedupe by video id, keep first playlist index.
    by_id = {}
    for v in meta["videos"]:
        by_id.setdefault(v["id"], v)

    n = 0
    for vid, v in by_id.items():
        vtt_path = series_dir / "raw" / f"{vid}.en.vtt"
        if not vtt_path.exists():
            print(f"SKIP {vid}: no raw vtt", file=sys.stderr)
            continue
        cues = list(parse_cues(vtt_path.read_text(encoding="utf-8")))
        segments = merge_cues(cues)
        words = sum(len(text.split()) for _, text in segments)

        fm = {
            "id": vid,
            "title": v["title"],
            "channel": v["channel"],
            "url": v["url"],
            "playlist": meta.get("playlist_title"),
            "playlist_owner": meta.get("playlist_owner"),
            "playlist_index": v.get("playlist_index"),
            "published": v["upload_date"],
            "retrieved": meta["retrieved"],
            "duration_sec": v["duration"],
            "captions": meta["captions_source"],
            "words": words,
            "topics": [],
            "claims": [],
        }
        header = "---\n" + "".join(f"{k}: {yaml_val(fm[k])}\n" for k in fm) + "---\n\n"
        loc = ""
        if meta.get("playlist_title") and v.get("playlist_index") is not None:
            loc = (f" · Playlist index {v['playlist_index']} "
                   f"of {meta['playlist_title']}")
        body_lines = [f"# {v['title']}", "",
                      f"_Channel: {v['channel']} · Uploaded: {v['upload_date']} · "
                      f"Duration: {mmss(v['duration'])}{loc}_", "",
                      f"[Open video]({v['url']})", "",
                      "---", ""]
        body_lines += [f"**[{mmss(start)}]** {text}" for start, text in segments]
        body = "\n".join(body_lines) + "\n"

        out_path = series_dir / f"{vid}.md"
        out_path.write_text(header + body, encoding="utf-8")
        n += 1
        print(f"wrote {out_path.name}: {len(segments)} segments, {words} words")

    print(f"\n{series}: {n} unique videos converted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
