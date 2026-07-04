import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REMOVED_CSV = ROOT / "output" / "song-intros-removed-after-review-v1.csv"
OUT_MD = ROOT / "output" / "song-intros-move-back-candidates-v1.md"
OUT_CSV = ROOT / "output" / "song-intros-move-back-candidates-v1.csv"


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def normalize_name(value):
    value = value or ""
    value = value.replace("（", "(").replace("）", ")")
    value = re.sub(r"\s+", "", value)
    value = value.replace("蘇打綠", "苏打绿")
    return value


def split_artists(value):
    value = normalize_name(value)
    parts = re.split(r"[,，/&、]| and | feat\.? | ft\.? ", value)
    return {part for part in parts if part}


def match_type(original, version):
    original_norm = normalize_name(original)
    version_norm = normalize_name(version)
    if original_norm == version_norm:
        return "exact same singer"

    original_parts = split_artists(original)
    version_parts = split_artists(version)
    if original_parts and original_parts == version_parts:
        return "same singer set"
    if original_parts and version_parts and original_parts.intersection(version_parts):
        return "partial singer overlap"
    return ""


def main():
    rows = load_csv(REMOVED_CSV)
    candidates = []
    for row in rows:
        kind = match_type(row["OriginalSinger"], row["VersionSinger"])
        if not kind:
            continue
        out = {
            "Year": row["Year"],
            "OriginalRank": row["Rank"],
            "Song": row["Song"],
            "VersionSinger": row["VersionSinger"],
            "OriginalSinger": row["OriginalSinger"],
            "VersionReleaseDate": row["VersionReleaseDate"],
            "OriginalReleaseDate": row["OriginalReleaseDate"],
            "RemovalReason": row["RemovalReason"],
            "MatchType": kind,
            "Recommendation": "move back candidate" if kind != "partial singer overlap" else "review before moving back",
        }
        candidates.append(out)

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(candidates[0].keys()))
        writer.writeheader()
        writer.writerows(candidates)

    lines = [
        "# Move-Back Candidates v1",
        "",
        "These songs were removed during metadata cleanup, but the original singer matches the cover/live version singer.",
        "They can be considered for moving back even when the original release date is incomplete.",
        "",
        f"Total candidates: {len(candidates)}",
        "",
    ]

    current_year = None
    for row in candidates:
        if row["Year"] != current_year:
            current_year = row["Year"]
            lines.extend([f"## {current_year}", ""])
            lines.append("| Original rank | Song | Version singer | Original singer | Version date | Original date | Match | Reason removed |")
            lines.append("|---:|---|---|---|---|---|---|---|")
        values = [
            row["OriginalRank"],
            row["Song"],
            row["VersionSinger"],
            row["OriginalSinger"],
            row["VersionReleaseDate"],
            row["OriginalReleaseDate"],
            row["MatchType"],
            row["RemovalReason"],
        ]
        safe = [value.replace("|", "/") for value in values]
        lines.append(f"| {safe[0]} | {safe[1]} | {safe[2]} | {safe[3]} | {safe[4]} | {safe[5]} | {safe[6]} | {safe[7]} |")
        if current_year != row["Year"]:
            lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    by_year = {}
    by_match = {}
    for row in candidates:
        by_year[row["Year"]] = by_year.get(row["Year"], 0) + 1
        by_match[row["MatchType"]] = by_match.get(row["MatchType"], 0) + 1

    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"candidates: {len(candidates)}")
    print(f"by year: {by_year}")
    print(f"by match: {by_match}")


if __name__ == "__main__":
    main()
