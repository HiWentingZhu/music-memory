from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_CSV = ROOT / "output" / "singer-summaries-source-reviewed-v1.csv"
REVIEW_CSV = ROOT / "output" / "artist-review-online-sources-v2.csv"
OUT_CSV = ROOT / "output" / "artist-brief-intros-from-review-sources-v2.csv"
OUT_MD = ROOT / "output" / "artist-brief-intros-from-review-sources-v2.md"

GENERIC_STYLE_PATTERNS = [
    r"(His|Her|Their|This artist's) style leans toward melancholic, intimate, and memory-driven sound, often touching [^.]+\.",
    r"(His|Her|Their|This artist's) style leans toward warm, steady, and emotionally repairing sound, often touching [^.]+\.",
    r"(His|Her|Their|This artist's) style leans toward thoughtful, restrained, and narrative-focused sound, often touching [^.]+\.",
    r"(His|Her|Their|This artist's) style leans toward direct, bright, and performance-driven sound, often touching [^.]+\.",
    r"(His|Her|Their|This artist's) style moves between melancholic, intimate, and memory-driven sound[^.]+\.",
    r"(His|Her|Their|This artist's) style moves between warm, steady, and emotionally repairing sound[^.]+\.",
]

ARTIST_STYLE_OVERRIDES = {
    "Bruno Mars": "His music is known for retro showmanship, tight pop hooks, funk and R&B influences, and a stage presence built for live performance.",
    "Charli xcx": "Her music sits at the edge of pop and club culture, moving between glossy hooks, electronic experimentation, and a restless sense of reinvention.",
    "Eric周兴哲 (Eric Chou)": "His songs often center on clean Mandopop melodies, romantic restraint, and ballad writing that feels intimate without becoming overdone.",
    "G.E.M. 邓紫棋 (G.E.M.)": "Her music is driven by strong vocal control, autobiographical writing, and a pop sound that can move from piano balladry to arena-sized drama.",
    "GALA": "Their sound carries the directness of Chinese rock bands: bright guitar energy, youthful urgency, and choruses made for shouting together.",
    "Jony J": "His work is rooted in Chinese hip-hop, with plainspoken delivery, grounded rhythm, and a focus on personal reflection.",
    "Lady Gaga": "Her music is built on reinvention, theatrical pop, dance-floor scale, and a performer’s instinct for turning vulnerability into spectacle.",
    "Laufey": "Her songs blend jazz-pop, classical training, and old-romance phrasing, giving her music a soft but carefully composed emotional world.",
    "Mayday": "Their music is built around communal rock choruses, youth memory, friendship, and the feeling of thousands of people singing one line together.",
    "S.H.E": "Their strength is vocal chemistry: bright Mandopop melodies, group harmony, and an easy familiarity that helped define a generation of Chinese pop.",
    "Sub Urban": "His music leans into dark pop, theatrical production, and visual worldbuilding, often making unease feel catchy.",
    "周杰伦 (Jay Chou)": "His sound blends R&B, hip-hop, classical color, and Chinese melodic writing into a relaxed but highly recognizable Mandopop language.",
    "周深 (Zhou Shen)": "His voice is known for its clear upper register, delicate control, and a cinematic quality that can make a small phrase feel expansive.",
    "大张伟 (Wowkie Zhang)": "His music favors playful pop-rock energy, quick hooks, humor, and a deliberately colorful public persona.",
    "孙燕姿 (Stefanie Sun)": "Her singing is clean, direct, and emotionally transparent, often making big Mandopop feelings sound conversational.",
    "张靓颖 (Jane Zhang)": "Her music is vocal-forward, polished, and dramatic, with a wide range and a taste for big emotional climaxes.",
    "希林娜依高 (Curley G)": "Her voice is bright and flexible, with pop and R&B color that fits both competition stages and polished Mandopop arrangements.",
    "徐佳莹 (Lala Hsu)": "Her songs often rely on intimate melodic writing, folk-pop softness, and small emotional details that land quietly.",
    "易烊千玺 (Jackson Yee)": "His performance style is restrained and controlled, with quiet dramatic presence across pop music, dance, and screen work.",
    "林俊杰 (JJ Lin)": "His music is known for polished Mandopop craft, R&B color, precise melody, and emotionally clear songwriting.",
    "毛不易 (Mao Buyi)": "His songwriting feels plainspoken and observant, often turning ordinary loneliness and daily life into gentle Mandopop confession.",
    "汪苏泷 (Silence Wang)": "His music uses clean pop melody, youthful warmth, and easy-to-enter emotional storytelling.",
    "陈奕迅 (Eason Chan)": "His singing is conversational and deeply controlled, often making a lyric feel lived-in rather than performed at a distance.",
    "薛之谦 (Joker Xue)": "His songs lean into theatrical melancholy, memorable hooks, and a confessional performance tone that has become closely tied to his Mandopop identity.",
    "霓虹花园NeonGarden (NeonGarden)": "Their sound sits in Chinese indie rock, with guitar-driven momentum, youthful release, and choruses that favor live-band energy.",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def compact_intro(text: str, max_sentences: int = 3) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    text = re.sub(r"\s*Career-start timing needs source verification before public website use\.", "", text)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    if len(sentences) <= max_sentences:
        return " ".join(sentences)
    return " ".join(sentences[:max_sentences])


def remove_source_profile_phrase(text: str) -> str:
    text = re.sub(
        r"\s*[^.]+?'s public profile is shaped by this source detail:\s*",
        " ",
        text,
    )
    text = re.sub(
        r"\s*[^.]+?'s public profile is shaped by\s*",
        " ",
        text,
    )
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_leftover_source_sentence(text: str) -> str:
    text = re.sub(r"\s*[^.]+?'s public profile is shaped by this source detail:\s*", " ", text)
    text = re.sub(r"\s*[^.]+?'s public profile is shaped by\s*", " ", text)
    text = re.sub(r"\s*his Chinese singer-songwriter identity and\s*", " His songs are shaped by ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_generic_style(text: str) -> str:
    for pattern in GENERIC_STYLE_PATTERNS:
        text = re.sub(pattern, "", text)
    return re.sub(r"\s+", " ", text).strip()


def refined_intro(summary: dict[str, str]) -> str:
    artist = summary["Artist"]
    identity = summary.get("IdentitySentence", "").strip()
    source_text = summary.get("SourceReviewedSummary") or summary.get("SingerSummary", "")
    source_text = remove_source_profile_phrase(source_text)
    source_text = clean_leftover_source_sentence(source_text)
    source_text = remove_generic_style(source_text)
    source_text = compact_intro(source_text, max_sentences=3)

    style = ARTIST_STYLE_OVERRIDES.get(artist)
    if style:
        parts = [identity, style]
        # Keep one factual sentence from the source text when it is not duplicating the identity/style opening.
        for sentence in re.split(r"(?<=[.!?])\s+", source_text):
            sentence = sentence.strip()
            if not sentence or sentence == identity or sentence == style:
                continue
            if "public profile is shaped" in sentence or "source detail" in sentence:
                continue
            if "style " in sentence.lower() and "music" not in sentence.lower():
                continue
            parts.append(sentence)
            break
        return " ".join(dict.fromkeys(parts))

    return source_text or identity


def source_status(summary_row: dict[str, str], review_row: dict[str, str]) -> str:
    if review_row.get("ReviewSource1URL"):
        return "Online review/profile source found"
    if summary_row.get("SourceReadingStatus") in {"Direct Wikipedia source read", "Manual source note applied from reviewed source"}:
        return "Online biography/profile source used"
    return "Needs stronger online review source"


def main() -> None:
    summaries = read_csv(SUMMARY_CSV)
    reviews = {row["Artist"]: row for row in read_csv(REVIEW_CSV)}

    output = []
    for summary in summaries:
        artist = summary["Artist"]
        review = reviews.get(artist, {})
        review_url = review.get("ReviewSource1URL", "")
        review_title = review.get("ReviewSource1Title", "")
        fallback_url = summary.get("SourceLink") or summary.get("CareerStartReviewLink") or review.get("ReviewSearchURL", "")
        intro = refined_intro(summary)

        output.append(
            {
                "Artist": artist,
                "CountryRegion": summary["CountryRegion"],
                "Role": summary["Role"],
                "BriefArtistIntro": intro,
                "ReviewSourceTitle": review_title,
                "ReviewSourceURL": review_url,
                "FallbackSourceURL": fallback_url,
                "ReviewSearchURL": review.get("ReviewSearchURL", ""),
                "SourceBasis": source_status(summary, review),
                "NeedsManualReview": "Yes" if not review_url else "Review recommended",
            }
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0].keys()))
        writer.writeheader()
        writer.writerows(output)

    lines = [
        "# Artist Brief Intros From Review Sources v2",
        "",
        "One brief intro per artist. This version removes stiff source phrasing and reduces repeated generic style buckets.",
        "Rows marked `Needs stronger online review source` should be reviewed with the search URL before final publishing.",
        "",
    ]

    for row in output:
        source_url = row["ReviewSourceURL"] or row["FallbackSourceURL"] or row["ReviewSearchURL"]
        source_label = row["ReviewSourceTitle"] or row["SourceBasis"]
        lines.extend(
            [
                f"## {row['Artist']}",
                "",
                row["BriefArtistIntro"],
                "",
                f"Source basis: {row['SourceBasis']}",
                "",
                f"Source: [{source_label}]({source_url})" if source_url else "Source: Needs manual source search",
                "",
            ]
        )

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"rows: {len(output)}")
    print(f"review/profile source found: {sum(1 for row in output if row['ReviewSourceURL'])}")
    print(f"needs stronger source: {sum(1 for row in output if row['SourceBasis'] == 'Needs stronger online review source')}")


if __name__ == "__main__":
    main()
