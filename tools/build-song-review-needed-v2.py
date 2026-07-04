import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_CSV = ROOT / "output" / "song-intros-by-year-display-v3-sourced.csv"
OUT_MD = ROOT / "output" / "song-intros-review-needed-v2.md"
OUT_CSV = ROOT / "output" / "song-intros-review-needed-v2.csv"


def main():
    with DISPLAY_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    review_rows = []
    for row in rows:
        issues = []
        if "Needs review" in row["CoverVersionLine"]:
            issues.append("cover/version date")
        if "Needs review" in row["OriginalLine"]:
            issues.append("original singer/date")
        if row.get("NeedsStrongerSource") == "Yes":
            issues.append("needs stronger source")
        if issues:
            out = dict(row)
            out["ReviewIssues"] = "; ".join(issues)
            review_rows.append(out)

    fieldnames = list(review_rows[0].keys()) if review_rows else list(rows[0].keys()) + ["ReviewIssues"]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(review_rows)

    lines = [
        "# Songs Needing Metadata Review - v2",
        "",
        "These rows still need review after applying the first batch of external-source metadata.",
        "",
        f"Total review rows: {len(review_rows)}",
        "",
    ]

    current_year = None
    for row in review_rows:
        if row["Year"] != current_year:
            current_year = row["Year"]
            lines.extend(["", f"## {current_year}"])
            lines.extend(["", "| Rank | Song | Artist | Review needed | Current cover/version line | Current original line | Source |"])
            lines.append("|---:|---|---|---|---|---|---|")
        song = row["Song"].replace("|", "/")
        artist = row["Artist"].replace("|", "/")
        cover = row["CoverVersionLine"].replace("|", "/")
        original = row["OriginalLine"].replace("|", "/")
        issues = row["ReviewIssues"].replace("|", "/")
        source = row.get("OriginalSourceURL", "").replace("|", "/")
        lines.append(f"| {row['Rank']} | {song} | {artist} | {issues} | {cover} | {original} | {source} |")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"review rows: {len(review_rows)}")
    by_year = {}
    by_issue = {}
    for row in review_rows:
        by_year[row["Year"]] = by_year.get(row["Year"], 0) + 1
        for issue in row["ReviewIssues"].split("; "):
            by_issue[issue] = by_issue.get(issue, 0) + 1
    print(f"by year: {by_year}")
    print(f"by issue: {by_issue}")


if __name__ == "__main__":
    main()
