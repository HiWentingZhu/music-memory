import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTRO_CSV = ROOT / "output" / "song-intros-by-year-release-years-v1.csv"
VERSION_CSV = ROOT / "output" / "song-version-metadata-v1.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-version-metadata-v2.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-version-metadata-v2.csv"


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def key(row):
    return row["Year"], row["Rank"], row["Song"], row["Artist"]


def clean(value):
    return value if value else "Needs review"


def main():
    intros = load_csv(INTRO_CSV)
    versions = {key(r): r for r in load_csv(VERSION_CSV)}
    rows = []
    lines = [
        "# Song Intros by Year with Original and Version Metadata - v2",
        "",
        "Structure for each song:",
        "",
        "1. 4-6 line English intro",
        "2. English display title line when needed",
        "3. Original song singer and release year",
        "4. Selected version singer and release year",
        "",
        "`Needs review` means QQ Music did not expose a reliable canonical original result through the automated lookup.",
    ]
    current_year = None
    for intro in intros:
        version = versions.get(key(intro), {})
        if intro["Year"] != current_year:
            current_year = intro["Year"]
            lines.extend(["", f"## {current_year}"])

        original_singer = clean(version.get("OriginalSinger", ""))
        original_year = clean(version.get("OriginalReleaseYear", ""))
        original_title = clean(version.get("OriginalSongTitle", ""))
        version_singer = clean(version.get("VersionSinger", intro["Artist"]))
        version_year = version.get("VersionReleaseYear", "")
        version_year_display = version_year if version_year else "Needs review"
        version_type = version.get("VersionType", "")

        lines.extend(["", f"### {intro['Year']}.{int(intro['Rank']):02d} - {intro['Song']} - {intro['Artist']}"])
        lines.extend(intro["Intro"].splitlines())
        if intro["EnglishDisplayLine"]:
            lines.extend(["", intro["EnglishDisplayLine"]])
        lines.extend(
            [
                "",
                f"Original song: {original_title} - {original_singer}",
                f"Original release year: {original_year}",
                f"Version used: {intro['Song']} - {version_singer}",
                f"Version release year: {version_year_display}",
            ]
        )
        out = dict(intro)
        out.update(
            {
                "VersionType": version_type,
                "OriginalSongTitle": original_title,
                "OriginalSinger": original_singer,
                "OriginalReleaseYear": original_year,
                "OriginalLookupMethod": version.get("OriginalLookupMethod", ""),
                "OriginalLookupNote": version.get("OriginalLookupNote", ""),
                "VersionSinger": version_singer,
                "VersionReleaseYear": version_year_display,
                "VersionReleaseDate": version.get("VersionReleaseDate", ""),
                "VersionReleaseSource": version.get("VersionReleaseSource", ""),
                "QQSongURL": version.get("QQSongURL", intro.get("QQSongURL", "")),
            }
        )
        rows.append(out)

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    missing_original = [r for r in rows if r["OriginalSinger"] == "Needs review" or r["OriginalReleaseYear"] == "Needs review"]
    missing_version = [r for r in rows if r["VersionReleaseYear"] == "Needs review"]
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"records: {len(rows)}")
    print(f"original metadata needs review: {len(missing_original)}")
    print(f"version year needs review: {len(missing_version)}")


if __name__ == "__main__":
    main()
