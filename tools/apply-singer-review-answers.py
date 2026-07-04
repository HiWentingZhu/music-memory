from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "singer-summaries-v3.csv"
ANSWERS_CSV = ROOT / "output" / "singer-review-answers-v1.csv"
OUT_CSV = ROOT / "output" / "singer-summaries-confirmed-v1.csv"
OUT_MD = ROOT / "output" / "singer-summaries-confirmed-v1.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def article(phrase: str) -> str:
    return "An" if phrase[:1].lower() in {"a", "e", "i", "o", "u"} else "A"


def pronoun_type(value: str) -> str:
    value = (value or "").strip().lower()
    if value in {"male", "male-his", "his"}:
        return "male"
    if value in {"female", "female-her", "her"}:
        return "female"
    if value in {"group", "group-their", "their"}:
        return "group"
    return "unknown"


def possessive_pronoun(gender: str) -> str:
    if gender == "female":
        return "Her"
    if gender == "male":
        return "His"
    if gender == "group":
        return "Their"
    return "This artist's"


def identity_sentence(country: str, role: str) -> str:
    country_display = {
        "China": "Chinese",
        "Taiwan, China": "Taiwanese",
        "Hong Kong, China": "Hong Kong",
        "United States": "American",
        "United Kingdom": "British",
        "South Korea": "South Korean",
        "France": "French",
        "Norway": "Norwegian",
        "Singapore": "Singaporean",
        "Malaysia": "Malaysian",
    }.get(country, country)
    phrase = f"{country_display} {role}".strip()
    return f"{article(phrase)} {phrase}."


def rewrite_style(style_summary: str, pronoun: str) -> str:
    style_summary = style_summary or ""
    return re.sub(r"^(His|Her|Their|This artist's) style", f"{pronoun} style", style_summary)


def main() -> None:
    rows = read_csv(SOURCE_CSV)
    answers = {row["Artist"]: row for row in read_csv(ANSWERS_CSV)}

    output = []
    for row in rows:
        answer = answers.get(row["Artist"])
        if not answer:
            row["ReviewApplied"] = "No"
            output.append(row)
            continue

        gender = pronoun_type(answer["SelectedGenderPronounType"])
        pronoun = possessive_pronoun(gender)
        country = answer["SelectedCountryRegion"]
        role = answer["SelectedRole"]
        identity = identity_sentence(country, role)
        style = rewrite_style(row["StyleSummary"], pronoun)
        summary = " ".join([identity, style, row["CareerStartSummary"]])

        row["GenderPronounType"] = gender
        row["StylePronoun"] = pronoun
        row["CountryRegion"] = country
        row["Role"] = role
        row["SingerSummary"] = summary
        row["IdentitySentence"] = identity
        row["StyleSummary"] = style
        row["ReviewApplied"] = "Yes"
        row["ReviewNotes"] = answer.get("ReviewNotes", "")
        output.append(row)

    fieldnames = list(output[0].keys())
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output)

    lines = [
        "# Singer Summaries Confirmed v1",
        "",
        "Singer summaries after applying chat-reviewed country/region, pronoun, and role answers.",
        "",
    ]
    for row in output:
        lines.extend(
            [
                f"## {row['Artist']}",
                "",
                row["SingerSummary"],
                "",
                f"Country/region: {row['CountryRegion']}",
                "",
                f"Role: {row['Role']}",
                "",
                f"Pronoun type: {row['GenderPronounType']}",
                "",
                f"Review applied: {row['ReviewApplied']}",
                "",
                f"Source link: {row['SourceLink'] or row['CareerStartReviewLink'] or 'Needs source search'}",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"rows: {len(output)}")
    print(f"review applied: {sum(1 for row in output if row['ReviewApplied'] == 'Yes')}")
    print(f"country-to-confirm: {sum(1 for row in output if row['CountryRegion'] == 'country-to-confirm')}")
    print(f"unknown pronoun: {sum(1 for row in output if row['GenderPronounType'] == 'unknown')}")


if __name__ == "__main__":
    main()
