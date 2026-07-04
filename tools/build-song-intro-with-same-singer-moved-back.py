import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLEANED_CSV = ROOT / "output" / "song-intros-by-year-cleaned-after-review-v1.csv"
REMOVED_CSV = ROOT / "output" / "song-intros-removed-after-review-v1.csv"
CANDIDATES_CSV = ROOT / "output" / "song-intros-move-back-candidates-v1.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v1.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v1.csv"
FINAL_MD = ROOT / "output" / "final-music-list-same-singer-moved-back-v1.md"
FINAL_CSV = ROOT / "output" / "final-music-list-same-singer-moved-back-v1.csv"


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def key(row):
    return row["Year"], row.get("Rank", row.get("OriginalRank", "")), row["Song"]


def display_credit(row):
    if row.get("MovedBackSameSinger") == "Yes":
        return row["VersionSinger"]
    if row["CoverVersionLine"]:
        return row["CoverVersionLine"]
    return row["OriginalLine"].replace("Original: ", "")


def main():
    cleaned = load_csv(CLEANED_CSV)
    removed = load_csv(REMOVED_CSV)
    candidates = load_csv(CANDIDATES_CSV)

    exact_candidate_keys = {
        (row["Year"], row["OriginalRank"], row["Song"])
        for row in candidates
        if row["MatchType"] == "exact same singer"
    }

    moved_back = []
    for row in removed:
        if key(row) not in exact_candidate_keys:
            continue
        out = dict(row)
        out["MovedBackSameSinger"] = "Yes"
        out["IntroCreditLine"] = out["VersionSinger"]
        out["OriginalShownInIntro"] = "No"
        moved_back.append(out)

    combined = []
    for row in cleaned:
        out = dict(row)
        out["MovedBackSameSinger"] = ""
        out["IntroCreditLine"] = display_credit(out)
        out["OriginalShownInIntro"] = "Yes"
        combined.append(out)
    combined.extend(moved_back)
    combined.sort(key=lambda row: (int(row["Year"]), int(row["Rank"])))

    lines = [
        "# Song Intros by Year - Same Singer Moved Back v1",
        "",
        "Songs removed only because original release metadata was incomplete were moved back when the original singer matches the cover/live singer.",
        "For those moved-back songs, the intro credit shows only the cover/live singer.",
        "",
    ]

    current_year = None
    for row in combined:
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
            lines.append(row["VersionSinger"])
        else:
            if row["CoverVersionLine"]:
                lines.append(row["CoverVersionLine"])
            lines.append(row["OriginalLine"])

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    fieldnames = []
    for row in combined:
        for name in row.keys():
            if name not in fieldnames:
                fieldnames.append(name)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined)

    by_year = defaultdict(list)
    for row in combined:
        by_year[row["Year"]].append(row)

    final_rows = []
    final_lines = [
        "# Final Music List - Same Singer Moved Back v1",
        "",
        "This is the final list after moving back songs where the original singer and cover/live singer are the same.",
        "",
    ]
    for year in sorted(by_year):
        final_lines.extend([f"## {year}", ""])
        final_lines.append("| Final # | Original rank | Song | Artist | Intro credit |")
        final_lines.append("|---:|---:|---|---|---|")
        for index, row in enumerate(by_year[year], start=1):
            credit = display_credit(row)
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

    moved_by_year = defaultdict(int)
    for row in moved_back:
        moved_by_year[row["Year"]] += 1
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"wrote {FINAL_MD}")
    print(f"wrote {FINAL_CSV}")
    print(f"kept from cleaned: {len(cleaned)}")
    print(f"moved back: {len(moved_back)}")
    print(f"total: {len(combined)}")
    print(f"total by year: {dict((year, len(by_year[year])) for year in sorted(by_year))}")
    print(f"moved back by year: {dict(sorted(moved_by_year.items()))}")


if __name__ == "__main__":
    main()
