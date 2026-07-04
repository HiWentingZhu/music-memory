from __future__ import annotations

import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "singer-summaries-confirmed-v1.csv"
OUT_CSV = ROOT / "output" / "singer-summaries-source-reviewed-v1.csv"
OUT_MD = ROOT / "output" / "singer-summaries-source-reviewed-v1.md"

USER_AGENT = "MusicProjectSingerSourceReview/1.0"

SOURCE_TITLE_OVERRIDES = {
    "GALA": ("GALA乐队", "https://zh.wikipedia.org/wiki/GALA%E4%B9%90%E9%98%9F"),
    "Sub Urban": ("Sub Urban (musician)", "https://en.wikipedia.org/wiki/Sub_Urban_%28musician%29"),
    "张信哲 (Jeff Chang)": ("Jeff Chang (singer)", "https://en.wikipedia.org/wiki/Jeff_Chang_%28singer%29"),
    "李玖哲 (Nicky Lee)": ("Nicky Lee (singer)", "https://en.wikipedia.org/wiki/Nicky_Lee_%28singer%29"),
    "金玟岐 (Vanessa Jin)": ("金玟岐", "https://zh.wikipedia.org/wiki/%E9%87%91%E7%8E%9F%E5%B2%90"),
}

MANUAL_FACT_NOTES = {
    "GALA": "GALA's public profile is shaped by their identity as a Chinese band founded in 2004, with songs such as Young for You and 追梦赤子心 becoming major markers of their rock-band image.",
    "Sub Urban": "Sub Urban's public profile is shaped by his 2019 breakout single Cradles and a dark, theatrical pop sound that mixes singer-songwriter, production, and visual-worldbuilding instincts.",
    "张信哲 (Jeff Chang)": "Jeff Chang's public profile is shaped by a long-running Mandopop career since the late 1980s and his reputation for sentimental Mandarin ballads.",
    "李玖哲 (Nicky Lee)": "Nicky Lee's public profile is shaped by his Taiwan-based Mandarin pop career, his earlier visibility with Machi, and his 2005 Mandarin solo album Shadow.",
    "方大同 (Khalil Fong)": "Khalil Fong's public profile is shaped by his role in bringing R&B, soul, and neo-soul color into Chinese pop music after his 2005 debut.",
    "朴树 (Pu Shu)": "Pu Shu's public profile is shaped by his folk-rock songwriting, his 1999 debut album I Am Going to 2000, and the later cultural reach of The Ordinary Road.",
    "李克勤 (Hacken Lee)": "Hacken Lee's public profile is shaped by a Cantopop career active since the 1980s, marked by precise live singing, television work, and long-standing Hong Kong music awards recognition.",
    "李玉刚 (Li Yugang)": "Li Yugang's public profile is shaped by his blend of Mandopop, stage performance, and nandan tradition, where male performers portray female roles in Peking opera.",
    "杨乃文 (Faith Yang)": "Faith Yang's public profile is shaped by Taiwanese rock and C-pop, with a career that began in the mid-1990s and a Golden Melody Award win for Best Female Mandarin Singer.",
    "杨千嬅 (Miriam Yeung)": "Miriam Yeung's public profile is shaped by a Hong Kong singing and acting career that began after the 1995 New Talent Singing Awards.",
    "毛阿敏 (Mao Amin)": "Mao Amin's public profile is shaped by her rise in the late 1980s as one of mainland China's earliest prominent pop singers, known for a rich and dignified vocal presence.",
    "王心凌 (Cyndi Wang)": "Cyndi Wang's public profile is shaped by her 2003 debut album Begin..., her sweet-pop image, and a television career that made her widely recognizable across Mandopop audiences.",
    "田馥甄 (Hebe Tien)": "Hebe Tien's public profile is shaped by her early-2000s fame with S.H.E and her later solo career, beginning with the 2010 album To Hebe.",
    "薛之谦 (Joker Xue)": "Joker Xue's public profile is shaped by his Chinese singer-songwriter identity and his emotionally direct Mandopop ballads, often associated with the so-called Xue-style love song.",
    "袁娅维TIA RAY (TIA RAY)": "Tia Ray's public profile is shaped by R&B, soul, and jazz influences, her 2012 rise through The Voice of China, and later cross-border collaborations.",
    "许美静 (Mavis Hee)": "Mavis Hee's public profile is shaped by Singaporean Mandopop and Cantopop ballads, with regional attention growing after her 1990s albums Knowingly and Regret.",
    "那英 (Na Ying)": "Na Ying's public profile is shaped by a career active since the late 1980s, major Mandopop influence, and long-running visibility as both singer and music-show coach.",
    "郁可唯 (Yisa Yu)": "Yisa Yu's public profile is shaped by her 2009 Super Girl breakthrough and a Mandopop career that grew from bar singing and competition stages.",
    "陈粒 (Chen Li)": "Chen Li's public profile is shaped by Chinese folk and independent music, including her early work with Dreamer Band and her rise as a singer-songwriter in the mid-2010s.",
    "魏如萱 (Waa Wei)": "Waa Wei's public profile is shaped by Taiwanese indie-pop songwriting, her earlier role as lead vocalist of Natural Q, and later Golden Melody recognition.",
    "弹壳 (Danko)": "Danko's public profile is shaped by his Chinese rapper identity and performance-driven presence in contemporary Chinese pop and hip-hop contexts.",
}

IDENTITY_OVERRIDES = {
    "GALA": ("China", "band", "group"),
    "李玖哲 (Nicky Lee)": ("United States", "singer and actor based in Taiwan", "male"),
    "弹壳 (Danko)": ("China", "rapper", "male"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def request_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def wikipedia_title_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if "wikipedia.org" not in parsed.netloc:
        return ""
    title = parsed.path.rsplit("/", 1)[-1]
    return urllib.parse.unquote(title).replace("_", " ")


def wikipedia_summary(title: str, lang: str = "en") -> dict:
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"
    return request_json(url)


def wikipedia_extract_fallback(title: str, lang: str = "en") -> str:
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode(
        {
            "action": "query",
            "prop": "extracts",
            "exintro": "1",
            "explaintext": "1",
            "redirects": "1",
            "titles": title,
            "format": "json",
        }
    )
    data = request_json(url)
    pages = ((data.get("query") or {}).get("pages") or {}).values()
    for page in pages:
        extract = page.get("extract", "")
        if extract:
            return extract
    return ""


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [part.strip() for part in parts if part.strip()]


def clean_name_for_note(artist: str) -> str:
    match = re.search(r"\(([^()]*)\)", artist)
    if match:
        return match.group(1).strip()
    return re.sub(r"\s+", " ", artist).strip()


def source_fact_note(artist: str, extract: str) -> str:
    sentences = split_sentences(extract)
    if not sentences:
        return "Direct source does not provide enough summary detail for a factual career note."

    preferred_keywords = [
        "debut",
        "began",
        "released",
        "rose",
        "known",
        "won",
        "winner",
        "member",
        "formed",
        "founded",
        "appeared",
        "gained attention",
        "popular",
        "influential",
    ]

    chosen = ""
    for keyword in preferred_keywords:
        for sentence in sentences[1:4] + sentences[:1]:
            if keyword in sentence.lower():
                chosen = sentence
                break
        if chosen:
            break

    if not chosen:
        chosen = sentences[0]

    name = clean_name_for_note(artist)
    chosen = re.sub(r"\[[^\]]+\]", "", chosen)
    chosen = re.sub(r"\s+", " ", chosen).strip()
    chosen = chosen.rstrip(".")

    # Keep this as a brief source-based note rather than copying long passages.
    if len(chosen) > 180:
        chosen = chosen[:177].rsplit(" ", 1)[0].rstrip(",;:") + "..."

    return f"{name}'s public profile is shaped by this source detail: {chosen}."


def source_looks_valid(title: str, extract: str) -> tuple[bool, str]:
    text = f"{title} {extract}".lower()
    if not extract:
        return False, "source summary empty"
    if "may refer to" in text:
        return False, "source is a disambiguation page"
    music_terms = [
        "singer",
        "songwriter",
        "musician",
        "rapper",
        "band",
        "duo",
        "girl group",
        "record producer",
        "performer",
        "vocal",
        "album",
        "song",
        "music",
        "actor",
        "actress",
    ]
    if not any(term in text for term in music_terms):
        return False, "source does not look like an artist/music page"
    return True, "valid artist/music source"


def is_placeholder_career(text: str) -> bool:
    lower = (text or "").lower()
    return "career-start timing needs source verification" in lower or "needs source verification" in lower


def build_reviewed_summary(row: dict[str, str], fact_note: str) -> str:
    summary = row["SingerSummary"]
    career = row.get("CareerStartSummary", "")
    if career and career in summary:
        return summary.replace(career, fact_note)
    if is_placeholder_career(summary):
        summary = re.sub(
            r"\s*Career-start timing needs source verification before public website use\.",
            "",
            summary,
        )
    return f"{summary} {fact_note}".strip()


def article(phrase: str) -> str:
    return "An" if phrase[:1].lower() in {"a", "e", "i", "o", "u"} else "A"


def country_display(country: str) -> str:
    return {
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


def identity_sentence(country: str, role: str) -> str:
    phrase = f"{country_display(country)} {role}".strip()
    return f"{article(phrase)} {phrase}."


def possessive_pronoun(gender: str) -> str:
    if gender == "female":
        return "Her"
    if gender == "male":
        return "His"
    if gender == "group":
        return "Their"
    return "This artist's"


def rewrite_style(style_summary: str, pronoun: str) -> str:
    return re.sub(r"^(His|Her|Their|This artist's) style", f"{pronoun} style", style_summary or "")


def rebuild_summary_from_parts(row: dict[str, str], fact_note: str, include_fact: bool) -> str:
    identity = identity_sentence(row["CountryRegion"], row["Role"])
    style = rewrite_style(row["StyleSummary"], row["StylePronoun"])
    parts = [identity, style]
    if include_fact:
        parts.append(fact_note)
    return " ".join(part for part in parts if part).strip()


def clean_public_summary(row: dict[str, str]) -> str:
    summary = row["SingerSummary"]
    summary = re.sub(
        r"\s*Career-start timing needs source verification before public website use\.",
        "",
        summary,
    )
    return summary.strip()


def language_from_url(url: str) -> str:
    netloc = urllib.parse.urlparse(url).netloc
    if netloc.startswith("zh."):
        return "zh"
    return "en"


def main() -> None:
    rows = read_csv(SOURCE_CSV)
    output = []

    for index, row in enumerate(rows, start=1):
        source_link = row.get("SourceLink", "")
        corrected_link = ""
        title = wikipedia_title_from_url(source_link)
        if row["Artist"] in SOURCE_TITLE_OVERRIDES:
            title, corrected_link = SOURCE_TITLE_OVERRIDES[row["Artist"]]
            source_link = corrected_link
        lang = language_from_url(source_link)
        extract = ""
        status = "Search link only - direct source still needed"
        fact_note = "Direct source still needed before replacing the factual career note."

        if row["Artist"] in MANUAL_FACT_NOTES:
            status = "Manual source note applied from reviewed source"
            fact_note = MANUAL_FACT_NOTES[row["Artist"]]
        elif title:
            print(f"[{index}/{len(rows)}] reading {title}")
            try:
                summary = wikipedia_summary(title, lang)
                time.sleep(0.15)
                extract = summary.get("extract", "")
            except Exception as exc:
                try:
                    extract = wikipedia_extract_fallback(title, lang)
                    time.sleep(0.15)
                except Exception:
                    status = f"Direct Wikipedia source read failed: {type(exc).__name__}"

            if extract:
                valid, validation_note = source_looks_valid(title, extract)
                if valid:
                    status = "Direct Wikipedia source read"
                else:
                    status = f"Direct Wikipedia source suspicious: {validation_note}"
                fact_note = source_fact_note(row["Artist"], extract)
            elif status == "Search link only - direct source still needed":
                status = "Direct Wikipedia source found but summary empty"

        reviewed = dict(row)
        if corrected_link:
            reviewed["SourceLink"] = corrected_link
        reviewed["CorrectedSourceLink"] = corrected_link
        if row["Artist"] in IDENTITY_OVERRIDES:
            country, role, gender = IDENTITY_OVERRIDES[row["Artist"]]
            reviewed["CountryRegion"] = country
            reviewed["Role"] = role
            reviewed["GenderPronounType"] = gender
            reviewed["StylePronoun"] = possessive_pronoun(gender)
            reviewed["IdentitySentence"] = identity_sentence(country, role)
            reviewed["StyleSummary"] = rewrite_style(reviewed["StyleSummary"], reviewed["StylePronoun"])
        reviewed["SourceReadingStatus"] = status
        reviewed["SourceFactNote"] = fact_note
        if status in {"Direct Wikipedia source read", "Manual source note applied from reviewed source"}:
            reviewed["SourceReviewedSummary"] = rebuild_summary_from_parts(reviewed, fact_note, include_fact=True)
        else:
            reviewed["SourceReviewedSummary"] = rebuild_summary_from_parts(reviewed, fact_note, include_fact=False)
        output.append(reviewed)

    fieldnames = list(output[0].keys())
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output)

    lines = [
        "# Singer Summaries Source Reviewed v1",
        "",
        "Direct Wikipedia source links have been read and used to replace generic career-review wording with a source-based factual note.",
        "Rows with search links only are kept unchanged and marked as needing a direct source.",
        "",
    ]

    for row in output:
        lines.extend(
            [
                f"## {row['Artist']}",
                "",
                row["SourceReviewedSummary"],
                "",
                f"Country/region: {row['CountryRegion']}",
                "",
                f"Role: {row['Role']}",
                "",
                f"Pronoun type: {row['GenderPronounType']}",
                "",
                f"Source reading status: {row['SourceReadingStatus']}",
                "",
                f"Source link: {row['SourceLink'] or row['CareerStartReviewLink'] or 'Needs source search'}",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"rows: {len(output)}")
    print(f"direct wikipedia read: {sum(1 for row in output if row['SourceReadingStatus'] == 'Direct Wikipedia source read')}")
    print(f"search links only: {sum(1 for row in output if row['SourceReadingStatus'] == 'Search link only - direct source still needed')}")


if __name__ == "__main__":
    main()
