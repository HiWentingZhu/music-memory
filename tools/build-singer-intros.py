import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v12-life-like-relatable.csv"
OUT_CSV = ROOT / "output" / "selected-song-singer-intros-v1.csv"
OUT_MD = ROOT / "output" / "selected-song-singer-intros-v1.md"


PROFILE_OVERRIDES = {
    "Charli xcx": {
        "start": "She began sharing music online in the late 2000s and broke through internationally in the 2010s.",
        "style": "sharp pop hooks, club textures, and experimental electronic energy",
        "confidence": "Needs source verification",
    },
    "陈奕迅 (Eason Chan)": {
        "start": "He entered the Hong Kong music scene in the mid-1990s and became one of Cantopop's defining modern voices.",
        "style": "conversational phrasing, emotional control, and a lived-in sense of storytelling",
        "confidence": "Needs source verification",
    },
    "徐佳莹 (Lala Hsu)": {
        "start": "She rose through televised singing competition in the late 2000s and built a career as both singer and songwriter.",
        "style": "intimate melodic writing, folk-pop softness, and clear emotional detail",
        "confidence": "Needs source verification",
    },
    "易烊千玺 (Jackson Yee)": {
        "start": "He debuted young as part of TFBOYS in the 2010s before expanding into solo music and acting.",
        "style": "restrained pop textures, controlled performance, and a quiet dramatic presence",
        "confidence": "Needs source verification",
    },
    "希林娜依高 (Curley G)": {
        "start": "She became widely known through Chinese singing programs in the late 2010s and early 2020s.",
        "style": "a bright, flexible voice with pop, R&B color, and stage-ready emotional lift",
        "confidence": "Needs source verification",
    },
    "周深 (Zhou Shen)": {
        "start": "He became widely recognized after appearing on major Chinese singing programs in the 2010s.",
        "style": "a clear, high, highly controlled voice that can feel delicate, cinematic, and theatrical",
        "confidence": "Needs source verification",
    },
    "周杰伦 (Jay Chou)": {
        "start": "He emerged around 2000 and helped reshape Mandopop with a songwriter-producer identity.",
        "style": "R&B, hip-hop, classical touches, Chinese melodic writing, and relaxed vocal phrasing",
        "confidence": "Needs source verification",
    },
    "汪苏泷 (Silence Wang)": {
        "start": "He first gained attention through online music in the late 2000s and early 2010s.",
        "style": "clean pop melody, youthful warmth, and easy-to-enter emotional storytelling",
        "confidence": "Needs source verification",
    },
    "张靓颖 (Jane Zhang)": {
        "start": "She became nationally known through a major Chinese singing competition in the mid-2000s.",
        "style": "vocal-forward pop, wide range, polish, and big emotional climaxes",
        "confidence": "Needs source verification",
    },
    "林俊杰 (JJ Lin)": {
        "start": "He debuted as a recording artist in the early 2000s and became a major Mandopop singer-songwriter.",
        "style": "polished pop production, R&B influence, and precise melodic songwriting",
        "confidence": "Needs source verification",
    },
    "S.H.E": {
        "start": "The group debuted in the early 2000s and became one of Mandopop's signature vocal groups.",
        "style": "bright group chemistry, pop immediacy, and harmonies that feel familiar quickly",
        "confidence": "Needs source verification",
    },
    "五月天 (Mayday)": {
        "start": "The band rose from Taiwan's late-1990s rock scene into one of Chinese pop-rock's biggest names.",
        "style": "stadium rock, youth memory, direct choruses, and communal emotional release",
        "confidence": "Needs source verification",
    },
    "Lady Gaga": {
        "start": "She broke through internationally in the late 2000s after years of New York performance and songwriting work.",
        "style": "dance-pop architecture, theatrical identity, and a strong instinct for reinvention",
        "confidence": "Needs source verification",
    },
    "孙燕姿 (Stefanie Sun)": {
        "start": "She debuted around 2000 and quickly became a defining Mandopop voice of her generation.",
        "style": "direct, clean, emotionally transparent singing that makes big feelings sound personal",
        "confidence": "Needs source verification",
    },
    "方大同 (Khalil Fong)": {
        "start": "He emerged in the mid-2000s as a singer-songwriter with a strong soul and R&B foundation.",
        "style": "groove-centered warmth, soul, R&B, and jazz-pop colors",
        "confidence": "Needs source verification",
    },
    "薛之谦 (Joker Xue)": {
        "start": "He became known in the mid-2000s and later built a strong identity around dramatic pop ballads.",
        "style": "theatrical melancholy, memorable hooks, and a confessional performance tone",
        "confidence": "Needs source verification",
    },
}


MOOD_STYLE = {
    "melancholic": "melancholic, intimate, and memory-driven",
    "healing": "warm, steady, and emotionally repairing",
    "energetic": "direct, bright, and performance-driven",
    "reflective": "thoughtful, restrained, and narrative-focused",
    "nostalgic": "nostalgic, soft-edged, and memory-led",
    "aspirational": "uplifting, clear, and forward-looking",
}


THEME_WORDS = {
    "love": "love songs",
    "heartbreak": "heartbreak",
    "memory": "memory",
    "healing": "healing",
    "growth": "growth",
    "city-night": "city-night emotion",
    "energy": "energy",
    "personal": "personal confession",
}


def clean(text):
    return (text or "").strip()


def selected_singer(row):
    return clean(row.get("VersionSingerEnglishDisplay")) or clean(row.get("VersionSinger")) or clean(row.get("Artist"))


def split_people(singer):
    parts = re.split(r"\s*,\s*|\s*/\s*|、|，", singer or "")
    return [part.strip() for part in parts if part.strip()]


def song_title(row):
    english = clean(row.get("EnglishDisplayTitle"))
    chinese = clean(row.get("ChineseDisplayTitle"))
    if english and chinese and english != chinese:
        return f"{chinese} / {english}"
    return english or chinese or clean(row.get("Song"))


def aggregate_profiles(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[selected_singer(row)].append(row)
    return grouped


def infer_style(rows):
    moods = Counter(clean(row.get("LyricMood")) for row in rows if clean(row.get("LyricMood")))
    themes = Counter()
    for row in rows:
        for theme in clean(row.get("LyricThemes")).split("|"):
            if theme:
                themes[theme] += 1
    mood = moods.most_common(1)[0][0] if moods else ""
    top_themes = [THEME_WORDS.get(theme, theme) for theme, _ in themes.most_common(3)]
    style = MOOD_STYLE.get(mood, "flexible and song-centered")
    if top_themes:
        return f"a {style} sound, often touching {', '.join(top_themes)}"
    return style


def profile_for_singer(singer, rows):
    if singer in PROFILE_OVERRIDES:
        return PROFILE_OVERRIDES[singer]
    people = split_people(singer)
    if len(people) > 1:
        return {
            "start": "This is a collaboration or group performance; each singer's career-start year should be verified separately before public use.",
            "style": infer_style(rows),
            "confidence": "Needs source verification",
        }
    return {
        "start": "Career-start year needs source verification before public website use.",
        "style": infer_style(rows),
        "confidence": "Needs source verification",
    }


def build_intro(singer, profile, row):
    title = song_title(row)
    if "collaboration or group performance" in profile["start"]:
        return (
            f"For {title}, the lineup of {singer} works as a shared stage moment rather than a single-voice portrait. "
            f"The performance brings together multiple voices around {profile['style']}. {profile['start']}"
        )
    return (
        f"{singer} is introduced through {profile['style']}. "
        f"{profile['start']} For {title}, this brief intro frames the voice before the song begins, "
        f"giving the audience both a sound profile and a career-start note."
    )


def main():
    with SOURCE_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    grouped = aggregate_profiles(rows)
    profiles = {singer: profile_for_singer(singer, singer_rows) for singer, singer_rows in grouped.items()}

    output_rows = []
    for row in rows:
        singer = selected_singer(row)
        profile = profiles[singer]
        output_rows.append(
            {
                "Year": row.get("Year", ""),
                "Rank": row.get("Rank", ""),
                "Song": clean(row.get("ChineseDisplayTitle")) or clean(row.get("Song")),
                "EnglishDisplayTitle": clean(row.get("EnglishDisplayTitle")),
                "SelectedSinger": singer,
                "SingerIntroBrief": build_intro(singer, profile, row),
                "SingerStyleNote": profile["style"],
                "CareerStartNote": profile["start"],
                "SourceStatus": profile["confidence"],
                "NeedsPublicWebsiteVerification": "Yes",
            }
        )

    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)

    lines = [
        "# Selected Song Singer Intros v1",
        "",
        "Brief singer-intro draft for each selected song. This version is useful for tone and structure, but career-start notes should be source-verified before public website use.",
        "",
    ]
    current_year = None
    for row in output_rows:
        if row["Year"] != current_year:
            current_year = row["Year"]
            lines.extend(["", f"## {current_year}"])
        lines.extend(
            [
                "",
                f"### {row['Year']}.{int(row['Rank']):02d} - {row['Song']}",
                row["SingerIntroBrief"],
                "",
                f"Source status: {row['SourceStatus']}",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    counts = Counter(row["Year"] for row in output_rows)
    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"rows: {len(output_rows)}")
    print(dict(sorted(counts.items())))
    print(f"unique singer entries: {len(grouped)}")


if __name__ == "__main__":
    main()
