import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTRO_CSV = ROOT / "output" / "song-intros-by-year-release-years-v1.csv"
VERSION_CSV = ROOT / "output" / "song-version-metadata-v1.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-display-v3.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-display-v3.csv"


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def key(row):
    return row["Year"], row["Rank"], row["Song"], row["Artist"]


def has_cjk(value):
    return bool(re.search(r"[\u3400-\u9fff]", value or ""))


def full_date(value):
    if value and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return value
    return "Needs review"


def is_cover_or_special(version_type):
    return "cover/live/special" in (version_type or "")


def main():
    intros = load_csv(INTRO_CSV)
    versions = {key(r): r for r in load_csv(VERSION_CSV)}

    lines = [
        "# Song Intros by Year - Display Format v3",
        "",
        "Per-song structure:",
        "",
        "```text",
        "4-6 line English intro",
        "",
        "[if applied] Chinese display title line",
        "English display title line",
        "by",
        "[if applied] cover/version singer, YYYY-MM-DD",
        "Original: original singer, YYYY-MM-DD",
        "```",
        "",
        "`Needs review` means a full YYYY-MM-DD date was not available in the current metadata.",
    ]
    rows = []
    current_year = None
    for intro in intros:
        version = versions.get(key(intro), {})
        if intro["Year"] != current_year:
            current_year = intro["Year"]
            lines.extend(["", f"## {current_year}"])

        chinese_display = intro["Song"] if has_cjk(intro["Song"]) else ""
        english_display = intro["EnglishDisplayLine"].split(" - ")[0] if intro["EnglishDisplayLine"] else intro["Song"]
        version_type = version.get("VersionType", "")
        version_singer = version.get("VersionSinger") or intro["Artist"]
        version_date = full_date(version.get("VersionReleaseDate", ""))
        original_singer = version.get("OriginalSinger") or "Needs review"
        original_date = full_date(version.get("OriginalReleaseDate", ""))

        lines.extend(["", f"### {intro['Year']}.{int(intro['Rank']):02d}"])
        lines.extend(intro["Intro"].splitlines())
        lines.append("")
        if chinese_display:
            lines.append(chinese_display)
        lines.append(english_display)
        lines.append("by")
        cover_line = ""
        if is_cover_or_special(version_type):
            cover_line = f"{version_singer}, {version_date}"
            lines.append(cover_line)
        original_line = f"Original: {original_singer}, {original_date}"
        lines.append(original_line)

        out = {
            "Year": intro["Year"],
            "Rank": intro["Rank"],
            "ChineseDisplayTitle": chinese_display,
            "EnglishDisplayTitle": english_display,
            "CoverVersionLine": cover_line,
            "OriginalLine": original_line,
            "Song": intro["Song"],
            "Artist": intro["Artist"],
            "VersionType": version_type,
            "VersionSinger": version_singer,
            "VersionReleaseDate": version_date,
            "OriginalSongTitle": version.get("OriginalSongTitle", ""),
            "OriginalSinger": original_singer,
            "OriginalReleaseDate": original_date,
            "OriginalLookupMethod": version.get("OriginalLookupMethod", ""),
            "OriginalLookupNote": version.get("OriginalLookupNote", ""),
            "Intro": intro["Intro"],
            "QQSongURL": version.get("QQSongURL", intro.get("QQSongURL", "")),
        }
        rows.append(out)

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    version_needs_review = sum(1 for r in rows if r["CoverVersionLine"] and "Needs review" in r["CoverVersionLine"])
    original_needs_review = sum(1 for r in rows if "Needs review" in r["OriginalLine"])
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"records: {len(rows)}")
    print(f"cover/version date needs review: {version_needs_review}")
    print(f"original date/singer needs review: {original_needs_review}")


if __name__ == "__main__":
    main()
