from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTRO_CSV = ROOT / "output" / "selected-song-singer-intros-v1.csv"
PROFILE_CSV = ROOT / "output" / "online-singer-profiles-v1.csv"
OUT_CSV = ROOT / "output" / "selected-song-singer-intros-online-v2.csv"
OUT_MD = ROOT / "output" / "selected-song-singer-intros-online-v2.md"


COLLAB_SPLIT = re.compile(r"\s*(?:,|，|&| and | feat\. | ft\. | with | x )\s*", re.I)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def split_artist_entry(entry: str) -> list[str]:
    if not entry:
        return []

    protected = re.sub(r"\(([^)]*)\)", lambda m: "(" + m.group(1).replace(",", "§") + ")", entry)
    parts = [p.replace("§", ",").strip() for p in COLLAB_SPLIT.split(protected) if p.strip()]
    return parts or [entry.strip()]


def source_link(profile: dict[str, str]) -> str:
    return (
        profile.get("WikipediaSearchURL")
        or profile.get("WikidataURL")
        or profile.get("GeneralSearchURL")
        or profile.get("CareerStartSearchURL")
        or ""
    )


def needs_review(profiles: list[dict[str, str]]) -> str:
    if not profiles:
        return "Yes"
    if any(p.get("NeedsManualReview") == "Yes" for p in profiles):
        return "Yes"
    if any("No online profile" in p.get("SourceStatus", "") for p in profiles):
        return "Yes"
    return "No"


def artist_intro_only(row: dict[str, str]) -> str:
    singer = row["SelectedSinger"]
    style = (row.get("SingerStyleNote") or "").strip()
    career = (row.get("CareerStartNote") or "").strip()

    sentences = []
    if style:
        sentences.append(f"{singer} is introduced here through {style}.")
    else:
        sentences.append(f"{singer} is introduced here through their vocal character and public musical identity.")

    if career:
        sentences.append(career)

    return " ".join(sentences)


def main() -> None:
    intro_rows = read_csv(INTRO_CSV)
    profile_rows = read_csv(PROFILE_CSV)
    profiles_by_artist = {row["Artist"]: row for row in profile_rows}

    out_rows: list[dict[str, str]] = []
    for row in intro_rows:
        artists = split_artist_entry(row["SelectedSinger"])
        profiles = [profiles_by_artist[a] for a in artists if a in profiles_by_artist]

        online_drafts = []
        source_statuses = []
        source_links = []
        online_labels = []
        career_searches = []
        for profile in profiles:
            online_labels.append(profile.get("OnlineLabel") or profile.get("Artist", ""))
            online_drafts.append(profile.get("OnlineSingerIntroDraft", ""))
            source_statuses.append(profile.get("SourceStatus", ""))
            link = source_link(profile)
            if link:
                source_links.append(link)
            career_search = profile.get("CareerStartSearchURL", "")
            if career_search:
                career_searches.append(career_search)

        out_rows.append(
            {
                "Year": row["Year"],
                "Rank": row["Rank"],
                "Song": row["Song"],
                "EnglishDisplayTitle": row["EnglishDisplayTitle"],
                "SelectedSinger": row["SelectedSinger"],
                "SingerIntroOnly": artist_intro_only(row),
                "OnlineArtistLabels": " | ".join(online_labels),
                "OnlineSingerIntroEvidence": " | ".join(online_drafts),
                "OnlineSourceStatus": " | ".join(source_statuses) if source_statuses else "No online profile row found",
                "OnlineSourceLinks": " | ".join(dict.fromkeys(source_links)),
                "CareerStartReviewLinks": " | ".join(dict.fromkeys(career_searches)),
                "NeedsPublicWebsiteVerification": needs_review(profiles),
            }
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(out_rows[0].keys())
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    lines: list[str] = [
        "# Selected Song Singer Intros - Online Source Review v2",
        "",
        "Per-song singer-intro draft joined with online profile evidence. This version keeps the singer section focused on the artist only and does not include song-intro wording.",
        "",
        "Note: rows marked `NeedsPublicWebsiteVerification = Yes` still need human review for exact career-start wording and source reliability.",
        "",
    ]

    current_year = None
    for row in out_rows:
        if row["Year"] != current_year:
            current_year = row["Year"]
            lines.extend(["", f"## {current_year}", ""])

        title = row["Song"]
        english = row["EnglishDisplayTitle"]
        if english and english != title:
            title = f"{title} / {english}"

        lines.extend(
            [
                f"### {row['Year']}.{int(row['Rank']):02d} - {title}",
                "",
                f"**Singer:** {row['SelectedSinger']}",
                "",
                row["SingerIntroOnly"],
                "",
                f"**Online evidence:** {row['OnlineSingerIntroEvidence'] or 'No online profile evidence found yet.'}",
                "",
                f"**Source status:** {row['OnlineSourceStatus']}",
                "",
                f"**Source links:** {row['OnlineSourceLinks'] or row['CareerStartReviewLinks'] or 'No source link found.'}",
                "",
                f"**Needs public website verification:** {row['NeedsPublicWebsiteVerification']}",
                "",
            ]
        )

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"song rows: {len(out_rows)}")
    print(f"needs review: {sum(1 for r in out_rows if r['NeedsPublicWebsiteVerification'] == 'Yes')}")


if __name__ == "__main__":
    main()
