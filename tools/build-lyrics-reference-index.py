import csv
import re
from pathlib import Path
from urllib.parse import quote_plus


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v12-life-like-relatable.csv"
OUT_CSV = ROOT / "output" / "selected-song-lyrics-reference-index.csv"
OUT_MD = ROOT / "output" / "selected-song-lyrics-reference-guide.md"


def has_cjk(text):
    return bool(re.search(r"[\u3400-\u9fff]", text or ""))


def clean_live_marker(text):
    text = text or ""
    text = re.sub(r"\s*\([^)]*(live|Live|LIVE)[^)]*\)", "", text)
    text = re.sub(r"\s*（[^）]*(live|Live|LIVE)[^）]*）", "", text)
    return text.strip()


def search_url(query):
    return f"https://www.google.com/search?q={quote_plus(query)}"


def lyric_query(row, title, singer):
    title = clean_live_marker(title) or row.get("Song", "")
    singer = singer or row.get("OriginalSinger") or row.get("Artist", "")
    return f"{title} {singer} lyrics"


def language_guess(row):
    text = " ".join(
        [
            row.get("ChineseDisplayTitle", ""),
            row.get("Song", ""),
            row.get("OriginalSinger", ""),
            row.get("VersionSinger", ""),
            row.get("Artist", ""),
        ]
    )
    if has_cjk(text):
        return "Chinese or C-pop"
    return "English or non-Chinese"


def load_rows():
    with SOURCE_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    rows = load_rows()
    output_rows = []

    for row in rows:
        original_title = row.get("OriginalSongTitle") or row.get("ChineseDisplayTitle") or row.get("Song", "")
        selected_title = row.get("ChineseDisplayTitle") or row.get("Song", "")
        original_singer = row.get("OriginalSingerEnglishDisplay") or row.get("OriginalSinger") or ""
        selected_singer = row.get("VersionSingerEnglishDisplay") or row.get("VersionSinger") or row.get("Artist", "")
        lang = language_guess(row)
        original_query = lyric_query(row, original_title, original_singer)
        selected_query = lyric_query(row, selected_title, selected_singer)

        output_rows.append(
            {
                "Year": row.get("Year", ""),
                "Rank": row.get("Rank", ""),
                "ChineseDisplayTitle": row.get("ChineseDisplayTitle", ""),
                "EnglishDisplayTitle": row.get("EnglishDisplayTitle", ""),
                "SelectedSinger": selected_singer,
                "OriginalSongTitle": original_title,
                "OriginalSinger": original_singer,
                "OriginalLanguageGuess": lang,
                "QQSongURL": row.get("QQSongURL", ""),
                "OriginalSourceURL": row.get("OriginalSourceURL", ""),
                "OriginalLyricsSearchQuery": original_query,
                "OriginalLyricsSearchURL": search_url(original_query),
                "SelectedVersionLyricsSearchQuery": selected_query,
                "SelectedVersionLyricsSearchURL": search_url(selected_query),
                "ChineseLyricsNeeded": "Yes" if "Chinese" in lang else "",
                "EnglishTranslationNeeded": "Yes, meaning summary only; do not store full translated lyrics"
                if "Chinese" in lang
                else "",
                "FullLyricStorageStatus": "Do not store full lyrics or full translations in project files",
                "SafeUseForIntro": "Use themes, mood, keywords, and short paraphrase only; do not quote lyric lines",
            }
        )

    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)

    counts = {}
    for row in output_rows:
        counts[row["Year"]] = counts.get(row["Year"], 0) + 1

    lines = [
        "# Selected Song Lyrics Reference Guide",
        "",
        "This file is a safe reference index for lyric research. It intentionally does not store full lyrics or full translated lyrics.",
        "",
        "Use the CSV for per-song lyric lookup links. For original Chinese songs, collect or read the Chinese lyrics from licensed sources and write only short English meaning summaries or intro notes in project files.",
        "",
        "## Rules",
        "",
        "- Do not paste full lyrics into project files.",
        "- Do not paste full English translations of Chinese lyrics into project files.",
        "- For intro writing, use lyric themes, mood, keywords, and short paraphrases only.",
        "- If exact lyric text is needed for performance, keep it in the licensed music platform or approved rights-cleared source, not in this repository.",
        "",
        "## Files",
        "",
        f"- CSV index: `{OUT_CSV.name}`",
        f"- Source selected songs: `{SOURCE_CSV.name}`",
        "",
        "## Counts",
        "",
    ]
    for year in sorted(counts):
        lines.append(f"- {year}: {counts[year]} songs")
    lines.extend(["", f"- Total: {len(output_rows)} songs", ""])

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"rows: {len(output_rows)}")
    print(counts)


if __name__ == "__main__":
    main()
