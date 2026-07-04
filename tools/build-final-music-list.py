import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-cleaned-after-review-v1.csv"
OUT_MD = ROOT / "output" / "final-music-list-v1.md"
OUT_CSV = ROOT / "output" / "final-music-list-v1.csv"


def main():
    with SOURCE_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    by_year = defaultdict(list)
    for row in rows:
        by_year[row["Year"]].append(row)

    final_rows = []
    lines = [
        "# Final Music List v1",
        "",
        "This list uses the cleaned metadata set: songs missing original metadata or cover/live version dates were removed; weak-source songs show year only.",
        "",
    ]

    for year in sorted(by_year):
        year_rows = by_year[year]
        lines.extend([f"## {year}", ""])
        lines.append("| Final # | Original rank | Song | Artist | Original |")
        lines.append("|---:|---:|---|---|---|")
        for index, row in enumerate(year_rows, start=1):
            original = row["OriginalLine"].replace("Original: ", "")
            final_row = {
                "Year": year,
                "FinalOrder": index,
                "OriginalRank": row["Rank"],
                "ChineseDisplayTitle": row["ChineseDisplayTitle"],
                "EnglishDisplayTitle": row["EnglishDisplayTitle"],
                "Song": row["Song"],
                "Artist": row["Artist"],
                "CoverVersionLine": row["CoverVersionLine"],
                "OriginalLine": row["OriginalLine"],
                "OriginalSourceURL": row.get("OriginalSourceURL", ""),
                "NeedsStrongerSource": row.get("NeedsStrongerSource", ""),
            }
            final_rows.append(final_row)

            song = row["Song"].replace("|", "/")
            artist = row["Artist"].replace("|", "/")
            original = original.replace("|", "/")
            lines.append(f"| {index} | {row['Rank']} | {song} | {artist} | {original} |")
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(final_rows[0].keys()))
        writer.writeheader()
        writer.writerows(final_rows)

    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"total rows: {len(final_rows)}")
    print({year: len(by_year[year]) for year in sorted(by_year)})


if __name__ == "__main__":
    main()
