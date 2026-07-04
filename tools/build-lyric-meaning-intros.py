import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v7-moment-focused.csv"
LYRIC_JSON = ROOT / "sample-data" / "my-qq-music-2022-2026.json"
OUT_MD = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v10-varied-openings.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v10-varied-openings.csv"
REVIEW_CSV = ROOT / "output" / "song-intros-lyric-meaning-review-v1.csv"

OBSOLETE_INTRO_FIELDS = {
    "Intro",
    "ChineseIntro",
    "ChineseIntroMoment",
    "EnglishIntroMoment",
}


THEME_CN = {
    "love": "爱里的靠近、等待和回应",
    "heartbreak": "失去之后仍然留在心里的酸楚",
    "memory": "回忆反复回来时留下的牵挂",
    "healing": "伤口慢慢变轻的过程",
    "growth": "终于学会和自己站在一起",
    "city-night": "夜色里没说出口的心事",
    "energy": "把情绪推向前方的力量",
    "personal": "贴近内心的自我独白",
}


THEME_EN = {
    "love": "the reaching, waiting, and answering inside love",
    "heartbreak": "the ache that remains after loss",
    "memory": "the pull of memory when it keeps returning",
    "healing": "the slow process of becoming less wounded",
    "growth": "learning how to stand with yourself",
    "city-night": "the unsaid feelings held by the night",
    "energy": "emotion turning into forward motion",
    "personal": "a private monologue spoken inward",
}


MOOD_CN = {
    "melancholic": "它的底色是克制的酸楚。",
    "healing": "它的语气带着缓慢的修复感。",
    "energetic": "它的情绪带着明亮的冲劲。",
    "reflective": "它更像一次回头看的整理。",
    "nostalgic": "它带着回望时才会出现的温度。",
    "aspirational": "它的声音里有一种向前看的亮光。",
}


MOOD_EN = {
    "melancholic": "The emotional color is restrained and aching.",
    "healing": "The voice carries a slow sense of repair.",
    "energetic": "The feeling arrives with bright momentum.",
    "reflective": "The song feels like looking back with steadier eyes.",
    "nostalgic": "There is warmth here that only appears when looking back.",
    "aspirational": "The voice carries a clear light pointed forward.",
}


ENERGY_CN = {
    "low": "所以它适合轻轻开口，让每个字都贴近听的人。",
    "medium": "所以它不是静止的，它在情绪里慢慢往前走。",
    "high": "所以它一进入，就把压住的情绪推到更亮的地方。",
}


ENERGY_EN = {
    "low": "It should enter softly, close enough for every word to land.",
    "medium": "It does not stand still; it moves through the feeling step by step.",
    "high": "It pushes the held-back emotion into brighter air.",
}


TITLE_CN_HINTS = [
    (("想念", "思念"), "歌里的思念不是远远看着，而是已经住进日常的缝隙。"),
    (("晚安",), "一句道别在这里不只是结束，也像是把脆弱暂时安放好。"),
    (("我想要",), "歌词里的“想要”更像一次坦白，把压住的渴望推到面前。"),
    (("爱", "喜欢"), "它说的不是完整无缺的爱，而是爱里那些犹豫、靠近和不甘心。"),
    (("再见", "离开", "逃亡"), "离开在这里不是潇洒转身，而是带着仍然未冷的牵挂。"),
    (("光", "星", "月"), "那些光亮不是装饰，而是情绪里还没有熄灭的方向。"),
    (("梦",), "梦在这里像一个缓冲地带，让现实里说不出口的事先停一停。"),
    (("青春", "少年"), "青春不是被美化的旧照片，而是仍然会发烫的冲动。"),
    (("普通", "平庸"), "它把平凡人的心事放大，让日常不再等于轻描淡写。"),
    (("浪费",), "它没有急着否定那段付出，而是承认有些认真也会落空。"),
    (("雨",), "雨不是天气，而像情绪终于找到可以落下来的方式。"),
    (("夜",), "夜色把人变得诚实，也把没说出口的话放得更近。"),
]


TITLE_EN_HINTS = [
    (("missing", "miss", "想念"), "Missing someone is not distant here; it has already moved into ordinary habits."),
    (("goodnight", "晚安"), "The farewell is not only an ending; it is a temporary place to set the hurt down."),
    (("want", "我想要"), "Wanting becomes a confession, bringing a long-held desire into the open."),
    (("love", "喜欢", "爱"), "The song is not about perfect love, but about hesitation, closeness, and what still pulls."),
    (("goodbye", "leave", "离开", "再见"), "Leaving does not sound clean; something warm is still being carried away."),
    (("light", "moon", "star", "光", "月", "星"), "The light is not decoration; it is the direction still alive inside the feeling."),
    (("dream", "梦"), "The dream becomes a pause where the unsaid can briefly rest."),
    (("youth", "少年", "青春"), "Youth is not polished nostalgia; it is an impulse that still runs hot."),
    (("ordinary", "平庸", "普通"), "The song enlarges everyday feeling until it can no longer be dismissed."),
    (("waste", "浪费"), "It does not deny the devotion; it admits that sincerity can still fall through."),
    (("rain", "雨"), "The rain is less weather than a way for feeling to finally fall."),
    (("night", "夜"), "Night makes the speaker more honest and brings the unsaid closer."),
]


CN_OPENINGS = [
    "有些情绪一出现，先不是答案，而是{core}。",
    "声音靠近时，最先浮出来的是{core}。",
    "这里没有把感情讲成大道理，只把{core}放到我们面前。",
    "一个人最诚实的时候，往往会听见{core}。",
    "这段歌词像把镜头停住，让{core}慢慢清楚。",
    "真正进入情绪之前，先抵达的是{core}。",
    "它把话说得很轻，却把{core}说得很深。",
    "最先打动人的不是情节，而是{core}。",
    "这不是一次直接的告白，更像是{core}在慢慢靠近。",
    "情绪被放低之后，{core}反而更清楚。",
    "这一段声音没有急着推进，它先让{core}站出来。",
    "听感最贴近人的地方，是{core}没有被藏起来。",
    "旋律还没完全展开，{core}已经先到了。",
    "它像在很近的地方说话，把{core}留给听的人。",
    "真正让人停下来的，是{core}被唱得没有距离。",
    "开场的情绪很克制，却已经露出{core}。",
    "这段表达不靠戏剧化，而靠{core}慢慢加深。",
    "它把复杂的心事收紧，只留下{core}。",
    "最柔软的入口，是{core}被轻轻托起来。",
    "歌词的重心不在解释，而在让{core}被听见。",
    "一切都没有说满，{core}却已经在场。",
    "这首歌的呼吸里，先有{core}。",
    "情绪没有绕远路，它直接靠近{core}。",
    "它像一盏小灯，照到的是{core}。",
    "听进去以后，最难忽略的是{core}。",
    "这里的温柔并不轻，它托住的是{core}。",
    "声音落下来的地方，正好是{core}。",
    "这段歌词把热闹推远，只留下{core}。",
    "被反复听见的，不是漂亮句子，而是{core}。",
    "它把心里的暗处翻开一点，让{core}透出来。",
    "情绪一靠近，{core}就变得具体。",
    "这段声音像一次停顿，让{core}有了形状。",
    "它没有把痛说破，却让{core}浮到表面。",
    "真正被留下的，是{core}带来的余温。",
    "每一次转折都在靠近{core}。",
    "它把所有用力都收住，只让{core}慢慢出现。",
    "当声音放轻，{core}就变得更重。",
    "这段情绪不是向外张扬，而是向内照见{core}。",
    "听到这里，会先被{core}轻轻拉住。",
    "它把某种说不清的反应，落在{core}上。",
]


CN_TURNS = [
    "它没有急着给答案，只让每一次停顿都带着重量。",
    "它把话说得很近，像一个人终于愿意承认自己的真实反应。",
    "它的情绪不是爆发，而是慢慢抵达最难绕开的地方。",
    "它让听的人明白，真正难的不是说出口，而是承认自己还在乎。",
    "它把柔软和不甘放在同一个呼吸里，让情绪有了更清楚的轮廓。",
]


EN_OPENINGS = [
    "The feeling arrives first as {core}.",
    "Before the song explains anything, it gives us {core}.",
    "What comes into focus is {core}.",
    "The lyric moves quietly toward {core}.",
    "This is not built on drama; it rests on {core}.",
    "The first emotional shape is {core}.",
    "What stays closest to the listener is {core}.",
    "The voice keeps its distance from spectacle and moves toward {core}.",
    "The lyric lets {core} appear without forcing it.",
    "Under the surface, the song is carrying {core}.",
    "The scene opens softly, and {core} is already there.",
    "What makes the moment feel honest is {core}.",
    "The emotion narrows until only {core} remains.",
    "The song does not overstate itself; it lets {core} breathe.",
    "Everything begins with the quiet pressure of {core}.",
    "The lyric holds back just enough for {core} to surface.",
    "The voice leans inward, toward {core}.",
    "The most human part of the song is {core}.",
    "What we hear first is not an answer, but {core}.",
    "The song places a small light on {core}.",
    "The lyric keeps returning to {core}.",
    "The heart of the moment is {core}.",
    "The song opens a narrow space for {core}.",
    "What lingers is {core}, held close to the voice.",
    "The lyric does not decorate the feeling; it reveals {core}.",
    "The first thing to settle in the room is {core}.",
    "The song lowers its voice and finds {core}.",
    "What rises through the melody is {core}.",
    "The emotion becomes clearer when it reaches {core}.",
    "The lyric keeps the camera close to {core}.",
    "No grand explanation is needed; {core} is enough.",
    "The song turns inward and finds {core}.",
    "The moment is held together by {core}.",
    "The feeling is quiet, but {core} gives it weight.",
    "The lyric leaves space around {core}.",
    "The voice does not chase resolution; it stays with {core}.",
    "The song begins where {core} becomes hard to ignore.",
    "The lyric draws a small circle around {core}.",
    "The emotional pull comes from {core}.",
    "The melody gives {core} somewhere to stand.",
]


EN_TURNS = [
    "It does not rush toward an answer; every pause carries weight.",
    "The words stay close, like someone finally admitting what they truly feel.",
    "The emotion does not explode; it slowly reaches the place that cannot be avoided.",
    "What hurts is not only saying it aloud, but realizing the feeling still matters.",
    "Tenderness and resistance share the same breath, giving the feeling a sharper outline.",
]


CN_OPENING_DETAILS = [
    "像有人把灯光调低了一点",
    "像一句话终于停在嘴边",
    "像手指碰到旧信封的边缘",
    "像窗外的声音忽然近了",
    "像一口气被轻轻放出来",
    "像眼神避开之后又回来",
    "像把某个名字暂时收好",
    "像人群散开后还亮着一盏灯",
    "像门没有关紧，情绪还在里面",
    "像夜色把声音慢慢放低",
    "像一次没有说完的停顿",
    "像心里某个位置被轻轻碰到",
    "像把沉默从角落里扶起来",
    "像旧画面忽然有了温度",
    "像一段路走到最安静的地方",
    "像把委屈折好放进口袋",
    "像眼泪还没落下就被接住",
    "像一束光没有照远，只照近处",
    "像呼吸停了一拍又继续",
    "像把答案先放在一边",
    "像一个人终于不再逞强",
    "像回忆自己找到了座位",
    "像掌心里还留着一点余温",
    "像把热闹关小，只听见心跳",
    "像声音贴着耳边慢慢展开",
    "像旧日子从背后走近",
    "像一阵风把话题带回来",
    "像灯下的影子忽然变清楚",
    "像很轻的一句话压住了整段情绪",
    "像把所有解释都暂时撤掉",
    "像时间在这一秒放慢",
    "像有人把脆弱放到桌面上",
    "像远处的光终于落到身边",
    "像一段沉默有了回声",
    "像心事不再躲进背景里",
    "像告别之前最后一次回头",
    "像被藏起来的感觉终于透气",
    "像把不甘心轻轻摊开",
    "像身体比语言更早明白",
    "像情绪找到了可以落脚的地方",
    "像一条线慢慢牵回心里",
    "像有人替沉默留了一把椅子",
    "像夜晚把复杂的事放轻",
    "像一句承认终于有了声音",
    "像心里的门被推开一条缝",
    "像把旧痛放到更柔软的位置",
    "像灯光照见了没有说破的部分",
    "像一场小小的退让",
    "像情绪从很深的地方浮上来",
    "像把自己交还给自己",
]


EN_OPENING_DETAILS = [
    "as if the light has been lowered slightly",
    "as if a sentence has stopped at the mouth",
    "as if a hand has found the edge of an old envelope",
    "as if the sound outside the window has moved closer",
    "as if one held breath has finally been released",
    "as if a glance turns away and then returns",
    "as if a name has been carefully put aside",
    "as if one lamp remains after the room empties",
    "as if the door has not fully closed on the feeling",
    "as if the night has lowered the volume",
    "as if a pause has learned how to speak",
    "as if a hidden place in the heart has been touched",
    "as if silence has been lifted from the corner",
    "as if an old image has regained warmth",
    "as if the road has reached its quietest part",
    "as if hurt has been folded into a pocket",
    "as if tears are caught before they fall",
    "as if the light stays close instead of reaching far",
    "as if breath misses a beat and continues",
    "as if the answer can wait outside the room",
    "as if someone no longer needs to pretend strength",
    "as if memory has found a seat",
    "as if a little warmth is still held in the palm",
    "as if the noise fades until only the pulse remains",
    "as if the voice unfolds close to the ear",
    "as if an old day has walked up from behind",
    "as if the wind has brought the subject back",
    "as if a shadow under the lamp becomes clear",
    "as if one quiet line carries the whole feeling",
    "as if every explanation has stepped aside",
    "as if time slows for a single breath",
    "as if vulnerability has been placed on the table",
    "as if distant light has finally landed nearby",
    "as if a silence has gained an echo",
    "as if the feeling refuses to stay in the background",
    "as if goodbye turns around one last time",
    "as if something hidden finally gets air",
    "as if resistance has been unfolded gently",
    "as if the body understands before language does",
    "as if the emotion has found a place to stand",
    "as if one thread has been pulled back to the heart",
    "as if silence has been given a chair",
    "as if the night makes the complicated thing lighter",
    "as if an admission has finally found a voice",
    "as if a door inside the heart opens slightly",
    "as if old hurt has been moved somewhere softer",
    "as if the light finds the part left unsaid",
    "as if a small surrender has begun",
    "as if the feeling rises from somewhere deep",
    "as if the self is being returned to itself",
]


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def pick(items, seed, offset=0):
    digest = hashlib.sha256(f"{seed}:{offset}".encode("utf-8")).hexdigest()
    return items[int(digest[:8], 16) % len(items)]


def clean_title(row):
    title = row["ChineseDisplayTitle"] or row["Song"]
    title = re.sub(r"\s*\([^)]*\)", "", title)
    title = re.sub(r"\s*（[^）]*）", "", title)
    return title.strip() or row["Song"]


def lyric_index():
    data = json.loads(LYRIC_JSON.read_text(encoding="utf-8"))
    return {
        (str(row["year"]), row["track_title"], row["artist_name"]): row.get("lyric_analysis") or {}
        for row in data["rows"]
    }


def title_hint(title, english_title, hints):
    text = f"{title} {english_title}".lower()
    for keys, line in hints:
        if any(key.lower() in text for key in keys):
            return line
    return ""


def core_theme(themes, lang):
    mapping = THEME_CN if lang == "cn" else THEME_EN
    preferred_orders = [
        ("love", "heartbreak"),
        ("memory", "healing"),
        ("heartbreak", "healing"),
        ("love", "memory"),
        ("growth", "healing"),
        ("energy", "personal"),
        ("city-night", "memory"),
    ]
    theme_set = set(themes)
    for first, second in preferred_orders:
        if first in theme_set and second in theme_set:
            if lang == "cn":
                return f"{mapping[first]}，以及{mapping[second]}"
            return f"{mapping[first]} and {mapping[second]}"
    if themes:
        return mapping.get(themes[0], "一段正在靠近的情绪" if lang == "cn" else "a feeling coming closer")
    return "一段正在靠近的情绪" if lang == "cn" else "a feeling coming closer"


def chinese_intro(row, lyric, used_openings, used_prefixes):
    seed = f"{row['Year']}-{row['Rank']}-{row['Song']}-lyric"
    title = clean_title(row)
    themes = lyric.get("themes") or []
    mood = lyric.get("mood") or ""
    energy = lyric.get("energy") or ""
    core = core_theme(themes, "cn")
    hint = title_hint(title, row["EnglishDisplayTitle"], TITLE_CN_HINTS)

    opening = ""
    for attempt in range(len(CN_OPENINGS)):
        candidate = CN_OPENINGS[(int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8], 16) + attempt) % len(CN_OPENINGS)].format(title=title, core=core)
        prefix = candidate[:8]
        if candidate not in used_openings and prefix not in used_prefixes:
            opening = candidate
            break
    if not opening:
        start = len(used_openings)
        for attempt in range(len(CN_OPENING_DETAILS) * len(CN_OPENING_DETAILS)):
            first = CN_OPENING_DETAILS[(start + attempt) % len(CN_OPENING_DETAILS)]
            second = CN_OPENING_DETAILS[(start * 3 + attempt * 7) % len(CN_OPENING_DETAILS)]
            candidate = f"{first}，也{second}，{core}在这一刻变得清楚。"
            prefix = candidate[:8]
            if candidate not in used_openings and prefix not in used_prefixes:
                opening = candidate
                break
    if not opening:
        for attempt in range(len(CN_OPENING_DETAILS) * len(CN_OPENING_DETAILS)):
            first = CN_OPENING_DETAILS[(len(used_openings) + attempt) % len(CN_OPENING_DETAILS)]
            second = CN_OPENING_DETAILS[(len(used_openings) * 5 + attempt * 11) % len(CN_OPENING_DETAILS)]
            candidate = f"{first}，也{second}，{core}在这一刻变得清楚。"
            if candidate not in used_openings:
                opening = candidate
                break
    used_openings.add(opening)
    used_prefixes.add(opening[:8])

    lines = [opening]
    if hint:
        lines.append(hint)
    else:
        lines.append(pick(CN_TURNS, seed, 2))
    lines.append(MOOD_CN.get(mood, pick(CN_TURNS, seed, 3)))
    lines.append(ENERGY_CN.get(energy, pick(CN_TURNS, seed, 4)))
    return "\n".join(lines)


def english_intro(row, lyric, used_openings, used_prefixes):
    seed = f"{row['Year']}-{row['Rank']}-{row['Song']}-lyric"
    title = row["EnglishDisplayTitle"] or clean_title(row)
    themes = lyric.get("themes") or []
    mood = lyric.get("mood") or ""
    energy = lyric.get("energy") or ""
    core = core_theme(themes, "en")
    hint = title_hint(clean_title(row), title, TITLE_EN_HINTS)

    opening = ""
    for attempt in range(len(EN_OPENINGS)):
        candidate = EN_OPENINGS[(int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8], 16) + attempt) % len(EN_OPENINGS)].format(title=title, core=core)
        prefix = " ".join(candidate.split()[:4])
        if candidate not in used_openings and prefix not in used_prefixes:
            opening = candidate
            break
    if not opening:
        start = len(used_openings)
        for attempt in range(len(EN_OPENING_DETAILS) * len(EN_OPENING_DETAILS)):
            first = EN_OPENING_DETAILS[(start + attempt) % len(EN_OPENING_DETAILS)]
            second = EN_OPENING_DETAILS[(start * 3 + attempt * 7) % len(EN_OPENING_DETAILS)]
            candidate = f"{first.capitalize()}, and {second}, {core} becomes clear."
            prefix = " ".join(candidate.split()[:4])
            if candidate not in used_openings and prefix not in used_prefixes:
                opening = candidate
                break
    if not opening:
        for attempt in range(len(EN_OPENING_DETAILS) * len(EN_OPENING_DETAILS)):
            first = EN_OPENING_DETAILS[(len(used_openings) + attempt) % len(EN_OPENING_DETAILS)]
            second = EN_OPENING_DETAILS[(len(used_openings) * 5 + attempt * 11) % len(EN_OPENING_DETAILS)]
            candidate = f"{first.capitalize()}, and {second}, {core} becomes clear."
            if candidate not in used_openings:
                opening = candidate
                break
    used_openings.add(opening)
    used_prefixes.add(" ".join(opening.split()[:4]))

    lines = [opening]
    if hint:
        lines.append(hint)
    else:
        lines.append(pick(EN_TURNS, seed, 2))
    lines.append(MOOD_EN.get(mood, pick(EN_TURNS, seed, 3)))
    lines.append(ENERGY_EN.get(energy, pick(EN_TURNS, seed, 4)))
    return "\n".join(lines)


def visible_time_lines(row):
    if row.get("MovedBackSameSinger") == "Yes":
        return [row["SameSingerLineWithDate"]]
    lines = []
    if row["CoverVersionLineEnglish"]:
        lines.append(row["CoverVersionLineEnglish"])
    lines.append(row["OriginalLineEnglish"])
    return lines


def main():
    rows = load_csv(SOURCE_CSV)
    lyrics = lyric_index()
    review_rows = []
    used_cn_openings = set()
    used_en_openings = set()
    used_cn_prefixes = set()
    used_en_prefixes = set()

    for row in rows:
        lyric = lyrics.get((row["Year"], row["Song"], row["Artist"]), {})
        available = bool(lyric.get("available"))
        row["LyricThemes"] = "|".join(lyric.get("themes") or [])
        row["LyricMood"] = lyric.get("mood", "")
        row["LyricEnergy"] = lyric.get("energy", "")
        row["LyricMeaningSource"] = lyric.get("source", "")
        row["NeedsLyricMeaningReview"] = "" if available else "Yes"
        row["ChineseIntroLyricMeaning"] = chinese_intro(row, lyric, used_cn_openings, used_cn_prefixes)
        row["EnglishIntroLyricMeaning"] = english_intro(row, lyric, used_en_openings, used_en_prefixes)
        if not available:
            review_rows.append(row)

    lines = [
        "# Song Intros by Year - Same Singer Moved Back v10 Varied Openings",
        "",
        "Chinese intro appears before English intro. Intros are based on lyric-derived meaning, avoid repeated opening patterns, and do not quote lyrics or repeat song titles.",
        "",
    ]

    current_year = None
    for row in rows:
        if row["Year"] != current_year:
            current_year = row["Year"]
            lines.extend(["", f"## {current_year}"])

        lines.extend(["", f"### {row['Year']}.{int(row['Rank']):02d}"])
        lines.extend(row["ChineseIntroLyricMeaning"].splitlines())
        lines.append("")
        lines.extend(row["EnglishIntroLyricMeaning"].splitlines())
        lines.append("")
        if row["ChineseDisplayTitle"]:
            lines.append(row["ChineseDisplayTitle"])
        lines.append(row["EnglishDisplayTitle"])
        lines.append("by")
        lines.extend(visible_time_lines(row))

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    fieldnames = []
    for row in rows:
        for name in row.keys():
            if name not in OBSOLETE_INTRO_FIELDS and name not in fieldnames:
                fieldnames.append(name)
    output_rows = [
        {name: row.get(name, "") for name in fieldnames}
        for row in rows
    ]
    review_output_rows = [
        {name: row.get(name, "") for name in fieldnames}
        for row in review_rows
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    with REVIEW_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(review_output_rows)

    by_year = defaultdict(int)
    for row in rows:
        by_year[row["Year"]] += 1
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"wrote {REVIEW_CSV}")
    print(f"rows: {len(rows)}")
    print(f"lyric meaning review rows: {len(review_rows)}")
    print(dict(sorted(by_year.items())))


if __name__ == "__main__":
    main()
