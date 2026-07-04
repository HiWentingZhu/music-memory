from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USER_CSV = ROOT / "output" / "artist_intro_utf8.csv"
CANONICAL_CSV = ROOT / "output" / "all-singer-list-v1.csv"
OUT_CSV = ROOT / "output" / "artist-info-source-of-truth-v1.csv"
OUT_MD = ROOT / "output" / "artist-info-source-of-truth-v1.md"
ALL_LIST_CSV = ROOT / "output" / "all-singer-list-v2.csv"
ALL_LIST_MD = ROOT / "output" / "all-singer-list-v2.md"

NAME_MAP = {
    "f(x) (????)": "f(x) (에프엑스)",
    "凡清 (Fanish)": "凡清 (Fanish) (Fanish)",
    "银河快递 (Galaxy Express)": "银河快递 (Galaxy Express) (Galaxy Express)",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    user_rows = read_csv(USER_CSV)
    canonical_rows = read_csv(CANONICAL_CSV)
    canonical_names = [row["Artist"] for row in canonical_rows]

    user_by_artist = {}
    for row in user_rows:
        artist = NAME_MAP.get(row["Artist"], row["Artist"])
        normalized = dict(row)
        normalized["Artist"] = artist
        user_by_artist[artist] = normalized

    missing = [name for name in canonical_names if name not in user_by_artist]
    extras = [name for name in user_by_artist if name not in set(canonical_names)]

    fieldnames = [
        "Artist",
        "CountryRegion",
        "Role",
        "BriefArtistIntroEnglish",
        "BriefArtistIntroChinese",
        "Source",
    ]

    output_rows = []
    for name in canonical_names:
        row = user_by_artist[name]
        output_rows.append(
            {
                "Artist": name,
                "CountryRegion": row.get("CountryRegion", ""),
                "Role": row.get("Role", ""),
                "BriefArtistIntroEnglish": row.get("BriefArtistIntro (English)", ""),
                "BriefArtistIntroChinese": row.get("BriefArtistIntro (中文)", ""),
                "Source": row.get("Source", ""),
            }
        )

    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    with ALL_LIST_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    lines = [
        "# Artist Info Source Of Truth v1",
        "",
        "This file is generated from `output/artist_intro.csv`, normalized to UTF-8 and aligned to the canonical artist list.",
        "",
        f"Total artists/groups: {len(output_rows)}",
        "",
    ]
    if missing:
        lines += ["Missing canonical artists:", *[f"- {name}" for name in missing], ""]
    if extras:
        lines += ["Extra artists from user CSV:", *[f"- {name}" for name in extras], ""]

    for row in output_rows:
        lines.extend(
            [
                f"## {row['Artist']}",
                "",
                f"Country/region: {row['CountryRegion']}",
                "",
                f"Role: {row['Role']}",
                "",
                row["BriefArtistIntroChinese"],
                "",
                row["BriefArtistIntroEnglish"],
                "",
                f"Source: {row['Source'] or 'No source provided'}",
                "",
            ]
        )

    md_text = "\n".join(lines)
    OUT_MD.write_text(md_text, encoding="utf-8")
    ALL_LIST_MD.write_text(md_text, encoding="utf-8")

    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"wrote {ALL_LIST_CSV}")
    print(f"wrote {ALL_LIST_MD}")
    print(f"rows: {len(output_rows)}")
    print(f"missing: {len(missing)}")
    print(f"extras: {len(extras)}")


if __name__ == "__main__":
    main()
