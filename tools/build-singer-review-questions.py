from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "singer-summaries-v3.csv"
OUT_CSV = ROOT / "output" / "singer-review-questions-v1.csv"
OUT_MD = ROOT / "output" / "singer-review-questions-v1.md"


CHINESE_NAME_RE = re.compile(r"[\u4e00-\u9fff]")
GROUP_HINT_RE = re.compile(r"(乐队|樂隊|组合|組合|乐团|樂團|团|團|band|group|duo|f\(x\)|NZBZ|GALA)", re.I)


KNOWN_COUNTRY_SUGGESTIONS = {
    "Amber Van Day": "United Kingdom",
    "Assen捷 (Assen Jie)": "China",
    "Chris James": "United States",
    "Eric周兴哲 (Eric Chou)": "Taiwan, China",
    "Faye 詹雯婷 (Faye Chan)": "Taiwan, China",
    "Hugel": "France",
    "Madcon": "Norway",
    "Ray Dalton": "United States",
    "Spencer Stewart": "United States",
    "Sub Urban": "United States",
    "Tank": "Taiwan, China",
    "f(x) (에프엑스)": "South Korea",
    "丁当 (Della Ding)": "Taiwan, China",
    "于文文 (Kelly Yu)": "China",
    "五月天 阿信 (Ashin)": "Taiwan, China",
    "八三夭乐团 (831)": "Taiwan, China",
    "八三夭阿璞 (A Pu)": "Taiwan, China",
    "方大同 (Khalil Fong)": "Hong Kong, China",
    "杨千嬅 (Miriam Yeung)": "Hong Kong, China",
    "林宥嘉": "Taiwan, China",
    "王心凌 (Cyndi Wang)": "Taiwan, China",
    "王菀之 (Ivana Wong)": "Hong Kong, China",
    "许美静 (Mavis Hee)": "Singapore",
    "魏如萱 (Waa Wei)": "Taiwan, China",
}


KNOWN_ROLE_SUGGESTIONS = {
    "Amber Van Day": "singer-songwriter",
    "Assen捷 (Assen Jie)": "singer",
    "Chris James": "singer-songwriter",
    "Eric周兴哲 (Eric Chou)": "singer-songwriter",
    "Faye 詹雯婷 (Faye Chan)": "singer",
    "Hugel": "DJ and record producer",
    "Madcon": "duo",
    "Ray Dalton": "singer-songwriter",
    "Spencer Stewart": "songwriter and producer",
    "Sub Urban": "singer-songwriter",
    "Tank": "singer-songwriter",
    "f(x) (에프엑스)": "girl group",
    "五月天 阿信 (Ashin)": "singer-songwriter",
    "八三夭乐团 (831)": "band",
    "八三夭阿璞 (A Pu)": "singer",
    "方大同 (Khalil Fong)": "singer-songwriter",
    "杨千嬅 (Miriam Yeung)": "singer and actress",
    "林宥嘉": "singer",
    "王心凌 (Cyndi Wang)": "singer and actress",
    "王菀之 (Ivana Wong)": "singer-songwriter",
    "许美静 (Mavis Hee)": "singer-songwriter",
    "魏如萱 (Waa Wei)": "singer-songwriter",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def has_chinese_name(artist: str) -> bool:
    return bool(CHINESE_NAME_RE.search(artist or ""))


def looks_like_group(artist: str, role: str, gender_type: str) -> bool:
    return gender_type == "group" or "group" in role.lower() or "band" in role.lower() or bool(GROUP_HINT_RE.search(artist or ""))


def needs_review(row: dict[str, str]) -> bool:
    return (
        row["CountryRegion"] == "country-to-confirm"
        or row["GenderPronounType"] == "unknown"
        or row["Role"] == "artist"
    )


def country_choices(row: dict[str, str]) -> str:
    artist = row["Artist"]
    if artist in KNOWN_COUNTRY_SUGGESTIONS:
        first = KNOWN_COUNTRY_SUGGESTIONS[artist]
        base = ["China", "Taiwan, China", "Hong Kong, China", "Singapore", "Malaysia", "United States", "United Kingdom", "Other"]
        ordered = [first] + [item for item in base if item != first]
        return " / ".join(ordered[:6] + ["Other"])

    if has_chinese_name(artist):
        return "China / Taiwan, China / Hong Kong, China / Singapore / Malaysia / Other"

    return "United States / United Kingdom / Canada / South Korea / Norway / France / Other"


def gender_choices(row: dict[str, str]) -> str:
    if looks_like_group(row["Artist"], row["Role"], row["GenderPronounType"]):
        return "group-their / male-his / female-her / unknown-this artist's"
    return "male-his / female-her / group-their / unknown-this artist's"


def role_choices(row: dict[str, str]) -> str:
    artist = row["Artist"]
    if artist in KNOWN_ROLE_SUGGESTIONS:
        first = KNOWN_ROLE_SUGGESTIONS[artist]
        base = ["singer", "singer-songwriter", "band", "group", "duo", "rapper", "producer", "actor and singer", "online music creator"]
        ordered = [first] + [item for item in base if item != first]
        return " / ".join(ordered[:7] + ["Other"])

    if looks_like_group(artist, row["Role"], row["GenderPronounType"]):
        return "band / group / duo / girl group / vocal group / online music group / Other"

    return "singer / singer-songwriter / rapper / actor and singer / producer / online music creator / Other"


def suggested_country(row: dict[str, str]) -> str:
    return KNOWN_COUNTRY_SUGGESTIONS.get(row["Artist"], "")


def suggested_role(row: dict[str, str]) -> str:
    if row["Role"] != "artist":
        return row["Role"]
    if row["Artist"] in KNOWN_ROLE_SUGGESTIONS:
        return KNOWN_ROLE_SUGGESTIONS[row["Artist"]]
    if looks_like_group(row["Artist"], row["Role"], row["GenderPronounType"]):
        return "group"
    return ""


def main() -> None:
    rows = [row for row in read_csv(SOURCE_CSV) if needs_review(row)]
    output = []

    for index, row in enumerate(rows, start=1):
        output.append(
            {
                "ReviewID": f"S{index:03d}",
                "Artist": row["Artist"],
                "CurrentCountryRegion": row["CountryRegion"],
                "SuggestedCountryRegion": suggested_country(row),
                "CountryRegionChoices": country_choices(row),
                "CurrentGenderPronounType": row["GenderPronounType"],
                "GenderPronounChoices": gender_choices(row),
                "CurrentRole": row["Role"],
                "SuggestedRole": suggested_role(row),
                "RoleChoices": role_choices(row),
                "Question": (
                    f"Confirm {row['Artist']}: country/region, pronoun type, and role. "
                    f"Choose from the listed options or enter a corrected value."
                ),
                "SourceLink": row["SourceLink"] or row["CareerStartReviewLink"],
                "SelectedCountryRegion": "",
                "SelectedGenderPronounType": "",
                "SelectedRole": "",
                "ReviewNotes": "",
            }
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0].keys()))
        writer.writeheader()
        writer.writerows(output)

    lines = [
        "# Singer Review Questions v1",
        "",
        "Use this to confirm country/region, pronoun, and role for singers/groups that still need review.",
        "",
        "For Chinese-name artists, the main country/region choices are: `China`, `Taiwan, China`, `Hong Kong, China`, plus `Singapore`, `Malaysia`, or `Other` when needed.",
        "",
        "Fill in `SelectedCountryRegion`, `SelectedGenderPronounType`, and `SelectedRole` in the CSV, or answer directly from this Markdown list.",
        "",
        f"Total review items: {len(output)}",
        "",
    ]

    for row in output:
        lines.extend(
            [
                f"## {row['ReviewID']} - {row['Artist']}",
                "",
                f"Question: {row['Question']}",
                "",
                f"Country/region choices: {row['CountryRegionChoices']}",
                "",
                f"Suggested country/region: {row['SuggestedCountryRegion'] or 'none'}",
                "",
                f"Pronoun choices: {row['GenderPronounChoices']}",
                "",
                f"Current pronoun type: {row['CurrentGenderPronounType']}",
                "",
                f"Role choices: {row['RoleChoices']}",
                "",
                f"Suggested role: {row['SuggestedRole'] or 'none'}",
                "",
                f"Source link: {row['SourceLink']}",
                "",
            ]
        )

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"review items: {len(output)}")
    print(f"chinese-name items: {sum(1 for row in output if has_chinese_name(row['Artist']))}")


if __name__ == "__main__":
    main()
