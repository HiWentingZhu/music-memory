import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-display-v3-sourced.csv"
REVIEW_CSV = ROOT / "output" / "song-intros-review-needed-v2.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-cleaned-after-review-v1.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-cleaned-after-review-v1.csv"
REMOVED_CSV = ROOT / "output" / "song-intros-removed-after-review-v1.csv"


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def key(row):
    return row["Year"], row["Rank"], row["Song"], row["Artist"]


def year_only(value):
    match = re.search(r"\d{4}", value or "")
    return match.group(0) if match else value


def main():
    rows = load_csv(SOURCE_CSV)
    reviews = {key(row): row for row in load_csv(REVIEW_CSV)}

    kept = []
    removed = []
    for row in rows:
        review = reviews.get(key(row))
        issues = review.get("ReviewIssues", "") if review else ""
        case_1_or_2 = "original singer/date" in issues or "cover/version date" in issues

        out = dict(row)
        out["ReviewIssues"] = issues
        if case_1_or_2:
            out["RemovalReason"] = issues
            removed.append(out)
            continue

        if "needs stronger source" in issues:
            original_year = year_only(out["OriginalReleaseDate"])
            out["OriginalReleaseDate"] = original_year
            out["OriginalLine"] = f"Original: {out['OriginalSinger']}, {original_year}"
            out["NeedsStrongerSource"] = "Year only"

        kept.append(out)

    lines = [
        "# Song Intros by Year - Cleaned After Metadata Review v1",
        "",
        "Rows with missing original metadata or missing cover/live version date were removed.",
        "Rows with weaker source confidence are kept, but show release year only.",
        "",
    ]

    current_year = None
    for row in kept:
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
        if row["CoverVersionLine"]:
            lines.append(row["CoverVersionLine"])
        lines.append(row["OriginalLine"])

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    fieldnames = list(kept[0].keys()) if kept else list(rows[0].keys())
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(kept)

    removed_fieldnames = list(removed[0].keys()) if removed else fieldnames + ["RemovalReason"]
    with REMOVED_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=removed_fieldnames)
        writer.writeheader()
        writer.writerows(removed)

    by_year = {}
    removed_by_year = {}
    for row in kept:
        by_year[row["Year"]] = by_year.get(row["Year"], 0) + 1
    for row in removed:
        removed_by_year[row["Year"]] = removed_by_year.get(row["Year"], 0) + 1

    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"wrote {REMOVED_CSV}")
    print(f"kept rows: {len(kept)}")
    print(f"removed rows: {len(removed)}")
    print(f"kept by year: {by_year}")
    print(f"removed by year: {removed_by_year}")
    print(f"year-only rows: {sum(row.get('NeedsStrongerSource') == 'Year only' for row in kept)}")


if __name__ == "__main__":
    main()
