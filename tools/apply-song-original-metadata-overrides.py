import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_CSV = ROOT / "output" / "song-intros-by-year-display-v3.csv"
OVERRIDES_CSV = ROOT / "output" / "song-original-metadata-external-overrides-v1.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-display-v3-sourced.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-display-v3-sourced.csv"


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def key(row):
    return row["Year"], row["Rank"], row["Song"], row["Artist"]


def main():
    rows = load_csv(DISPLAY_CSV)
    overrides = {key(row): row for row in load_csv(OVERRIDES_CSV)}

    applied = 0
    for row in rows:
        override = overrides.get(key(row))
        if not override:
            row["OriginalSourceURL"] = ""
            row["NeedsStrongerSource"] = ""
            continue

        applied += 1
        row["OriginalSongTitle"] = override["OriginalSongTitle"]
        row["OriginalSinger"] = override["OriginalSinger"]
        row["OriginalReleaseDate"] = override["OriginalReleaseDate"]
        row["OriginalLine"] = f"Original: {override['OriginalSinger']}, {override['OriginalReleaseDate']}"
        row["OriginalLookupMethod"] = "external_source"
        row["OriginalLookupNote"] = override["SourceNote"]
        row["OriginalSourceURL"] = override["SourceURL"]
        needs_stronger = "needs stronger" in override["SourceNote"].lower()
        row["NeedsStrongerSource"] = "Yes" if needs_stronger else ""

    lines = [
        "# Song Intros by Year - Display Format v3 Sourced",
        "",
        "This version applies external-source metadata to rows previously marked for review.",
        "Rows with weak or approximate evidence remain marked with `Needs stronger source` in the CSV and review file.",
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
        if row["CoverVersionLine"]:
            lines.append(row["CoverVersionLine"])
        lines.append(row["OriginalLine"])
        if row["NeedsStrongerSource"]:
            lines.append("Needs stronger source")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    fieldnames = list(rows[0].keys())
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    strong_applied = sum(1 for row in rows if row["OriginalLookupMethod"] == "external_source" and not row["NeedsStrongerSource"])
    weak_applied = sum(1 for row in rows if row["OriginalLookupMethod"] == "external_source" and row["NeedsStrongerSource"])
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"records: {len(rows)}")
    print(f"external overrides applied: {applied}")
    print(f"resolved with external source: {strong_applied}")
    print(f"still needs stronger source: {weak_applied}")


if __name__ == "__main__":
    main()
