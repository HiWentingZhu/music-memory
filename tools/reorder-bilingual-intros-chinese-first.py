import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v5-bilingual-intros.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v6-chinese-first.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v6-chinese-first.csv"


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    rows = load_csv(SOURCE_CSV)
    lines = [
        "# Song Intros by Year - Same Singer Moved Back v6 Chinese First",
        "",
        "Chinese intro appears before English intro.",
        "",
    ]

    current_year = None
    for row in rows:
        if row["Year"] != current_year:
            current_year = row["Year"]
            lines.extend(["", f"## {current_year}"])

        lines.extend(["", f"### {row['Year']}.{int(row['Rank']):02d}"])
        lines.extend(row["ChineseIntro"].splitlines())
        lines.append("")
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
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    by_year = defaultdict(int)
    for row in rows:
        by_year[row["Year"]] += 1
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"rows: {len(rows)}")
    print(dict(sorted(by_year.items())))


if __name__ == "__main__":
    main()
