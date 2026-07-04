import csv
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v2-english-singers.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v3-english-singers-dates.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v3-english-singers-dates.csv"
FINAL_MD = ROOT / "output" / "final-music-list-same-singer-moved-back-v3-english-singers-dates.md"
FINAL_CSV = ROOT / "output" / "final-music-list-same-singer-moved-back-v3-english-singers-dates.csv"


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def visible_same_singer_line(row):
    singer = row["VersionSingerEnglishDisplay"]
    date = row["VersionReleaseDate"]
    if date and date != "Needs review":
        return f"{singer}, {date}"
    return singer


def visible_credit(row):
    if row.get("MovedBackSameSinger") == "Yes":
        return row["SameSingerLineWithDate"]
    if row["CoverVersionLineEnglish"]:
        return row["CoverVersionLineEnglish"]
    return row["OriginalLineEnglish"].replace("Original: ", "")


def has_visible_time(row):
    lines = []
    if row.get("MovedBackSameSinger") == "Yes":
        lines.append(row["SameSingerLineWithDate"])
    else:
        if row["CoverVersionLineEnglish"]:
            lines.append(row["CoverVersionLineEnglish"])
        lines.append(row["OriginalLineEnglish"])
    return any(re.search(r"\d{4}(-\d{2}-\d{2})?$", line) for line in lines)


def main():
    rows = load_csv(SOURCE_CSV)
    for row in rows:
        row["SameSingerLineWithDate"] = visible_same_singer_line(row) if row.get("MovedBackSameSinger") == "Yes" else ""
        row["IntroCreditLineEnglishWithDate"] = visible_credit(row)

    lines = [
        "# Song Intros by Year - Same Singer Moved Back v3 English Singers Dates",
        "",
        "Same-singer moved-back songs show only the cover/live singer line, with version date when available.",
        "",
    ]

    current_year = None
    for row in rows:
        if row["Year"] != current_year:
            current_year = row["Year"]
            lines.extend(["", f"## {current_year}"])

        lines.extend(["", f"### {row['Year']}.{int(row['Rank']):02d}"])
        lines.extend(row["Intro"].splitlines())
        lines.append("")
        if row["ChineseDisplayTitle"]:
            lines.append(row["ChineseDisplayTitle"])
        lines.append(row["EnglishDisplayTitle"])
        lines.append("by")
        if row.get("MovedBackSameSinger") == "Yes":
            lines.append(row["SameSingerLineWithDate"])
        else:
            if row["CoverVersionLineEnglish"]:
                lines.append(row["CoverVersionLineEnglish"])
            lines.append(row["OriginalLineEnglish"])

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    fieldnames = []
    for row in rows:
        for name in row.keys():
            if name not in fieldnames:
                fieldnames.append(name)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    by_year = defaultdict(list)
    for row in rows:
        by_year[row["Year"]].append(row)

    final_rows = []
    final_lines = [
        "# Final Music List - Same Singer Moved Back v3 English Singers Dates",
        "",
        "Same-singer moved-back songs show only the cover/live singer line, with version date when available.",
        "",
    ]
    for year in sorted(by_year):
        final_lines.extend([f"## {year}", ""])
        final_lines.append("| Final # | Original rank | Song | Artist | Intro credit |")
        final_lines.append("|---:|---:|---|---|---|")
        for index, row in enumerate(by_year[year], start=1):
            credit = visible_credit(row)
            final_rows.append(
                {
                    "Year": year,
                    "FinalOrder": index,
                    "OriginalRank": row["Rank"],
                    "Song": row["Song"],
                    "Artist": row["Artist"],
                    "IntroCredit": credit,
                    "MovedBackSameSinger": row.get("MovedBackSameSinger", ""),
                    "OriginalShownInIntro": row.get("OriginalShownInIntro", ""),
                }
            )
            safe = [row["Song"], row["Artist"], credit]
            safe = [value.replace("|", "/") for value in safe]
            final_lines.append(f"| {index} | {row['Rank']} | {safe[0]} | {safe[1]} | {safe[2]} |")
        final_lines.append("")

    FINAL_MD.write_text("\n".join(final_lines), encoding="utf-8")
    with FINAL_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(final_rows[0].keys()))
        writer.writeheader()
        writer.writerows(final_rows)

    missing_time = [row for row in rows if not has_visible_time(row)]
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"wrote {FINAL_MD}")
    print(f"wrote {FINAL_CSV}")
    print(f"rows: {len(rows)}")
    print(f"entries with no visible time: {len(missing_time)}")
    print({year: len(by_year[year]) for year in sorted(by_year)})


if __name__ == "__main__":
    main()
