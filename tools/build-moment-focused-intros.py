import csv
import hashlib
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v4-english-singers-dates.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v7-moment-focused.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v7-moment-focused.csv"


FORBIDDEN_CN = (
    "这一年",
    "年份",
    "年度",
    "雨夜档案",
    "返场舞台",
    "清醒的声场",
    "流动的夜色",
    "新的远方",
)

FORBIDDEN_EN_RE = re.compile(r"\byear|years|year's\b", re.I)


IMAGE_RULES = [
    (("rain", "window", "glass"), ("雨声", "窗边", "水汽"), ("rain at the window", "the glass", "the quiet room")),
    (("night", "dark", "midnight"), ("夜色", "未熄的灯", "安静的深处"), ("the night air", "one small lamp", "the silence")),
    (("archive", "drawer", "shelf", "paper"), ("纸页", "抽屉", "旧物"), ("a loose page", "the open drawer", "the old shelf")),
    (("stage", "live", "light", "lamp"), ("舞台灯", "光束", "呼吸声"), ("the stage light", "the held breath", "the first note")),
    (("road", "walk", "leave", "ticket"), ("路口", "车票", "远行前的风"), ("the road ahead", "the ticket in hand", "the pause before leaving")),
    (("sea", "water", "river"), ("潮水", "海边", "水面"), ("the tide", "the shoreline", "the water's edge")),
    (("dream", "sleep"), ("梦", "半醒的时刻", "枕边"), ("the half-dream", "the pillow's edge", "the waking dark")),
    (("fire", "heat", "burn"), ("火光", "余温", "热烈"), ("the afterglow", "the heat still in the air", "a bright spark")),
    (("time", "clock", "years"), ("时间", "旧日历", "回声"), ("the clock", "the echo", "one suspended second")),
    (("moon", "sky", "star", "light"), ("月光", "天空", "星点"), ("moonlight", "the open sky", "a small star of light")),
    (("dance", "beat", "pulse"), ("节拍", "身体", "律动"), ("the beat", "the body", "the moving floor")),
    (("love", "heart", "tender"), ("心事", "温柔", "爱意"), ("the heart's small weather", "the tender edge", "the unsaid feeling")),
]


CN_OPENINGS = [
    "《{title}》一响起，画面先安静下来。",
    "《{title}》像把镜头推近，只留下眼前这一刻。",
    "听到《{title}》，情绪不是铺开，而是慢慢聚焦。",
    "《{title}》开口的时候，空气里像多了一层微光。",
    "这首《{title}》不急着解释，只把当下轻轻托住。",
    "《{title}》像一个短暂停顿，让心事有地方落脚。",
    "在《{title}》里，最动人的不是远处，而是眼前。",
]


CN_IMAGE_LINES = [
    "{a}、{b}和{c}靠得很近，像一句话还没说完。",
    "{a}先浮出来，{b}跟着亮起，{c}把情绪接住。",
    "它让{a}停在原处，也让{b}和{c}有了重量。",
    "{a}没有退场，{b}也没有解释，只剩{c}慢慢靠近。",
    "像{a}擦过{b}，又在{c}里留下一点余温。",
    "那一点{a}落下来，{b}变得清楚，{c}也跟着安静。",
]


CN_MOMENT_LINES = [
    "这一刻不用回头看太远，只要听见声音怎样落下。",
    "它不替谁总结，只让正在发生的心跳被听见。",
    "歌声停在眼前，像把某个瞬间轻轻按亮。",
    "情绪没有被推满，却刚好抵达最柔软的位置。",
    "它把一段很轻的感受，稳稳放在灯下。",
    "没有宏大的解释，只有此刻被照见的自己。",
]


CN_CLOSINGS = [
    "于是下一秒开始之前，空气还保留着它的温度。",
    "等旋律接上来，话就可以不用再说得太满。",
    "它把听的人留在这里，刚好够一首歌开始。",
    "这就是它最适合出现的地方：不远，不重，正好。",
    "然后歌声进来，把这个瞬间继续往前带。",
    "所有情绪都停在近处，等第一句歌词接过去。",
]


EN_MOMENT_LINES = [
    "The moment stays close enough to touch.",
    "No large explanation is needed here.",
    "The song lets the feeling arrive at eye level.",
    "Everything narrows to the breath before the next line.",
    "The room does not become bigger; it becomes clearer.",
    "What matters is not the distance, but the pulse in front of us.",
    "The first note is already holding the scene together.",
]


EN_CLOSINGS = [
    "Then the song can enter without forcing the door.",
    "It leaves just enough silence for the melody to begin.",
    "That is the exact place where the voice should arrive.",
    "The feeling stays near, bright, and unfinished.",
    "Nothing needs to be solved before the chorus comes in.",
    "The moment remains open, waiting for the first line.",
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


def pick_images(intro, title, seed):
    text = f"{intro} {title}".lower()
    cn_matches = []
    en_matches = []
    for keys, cn_images, en_images in IMAGE_RULES:
        if any(key in text for key in keys):
            cn_matches.extend(cn_images)
            en_matches.extend(en_images)
    if len(cn_matches) < 3:
        cn_matches.extend(["灯光", "回声", "风", "旧照片", "人群", "呼吸"])
        en_matches.extend(["the light", "the echo", "the air", "an old photograph", "the crowd", "one breath"])

    cn_unique = []
    en_unique = []
    for cn, en in zip(cn_matches, en_matches):
        if cn not in cn_unique:
            cn_unique.append(cn)
            en_unique.append(en)

    indexes = list(range(len(cn_unique)))
    first = pick(indexes, seed, 11)
    remaining = [i for i in indexes if i != first]
    second = pick(remaining, seed, 12)
    remaining = [i for i in remaining if i != second]
    third = pick(remaining, seed, 13)
    return (cn_unique[first], cn_unique[second], cn_unique[third]), (en_unique[first], en_unique[second], en_unique[third])


def chinese_intro(row):
    title = clean_title(row)
    seed = f"{row['Year']}-{row['Rank']}-{row['Song']}"
    cn_images, _ = pick_images(row["Intro"], title, seed)
    a, b, c = cn_images
    return "\n".join(
        [
            pick(CN_OPENINGS, seed, 1).format(title=title),
            pick(CN_IMAGE_LINES, seed, 2).format(a=a, b=b, c=c),
            pick(CN_MOMENT_LINES, seed, 3),
            pick(CN_CLOSINGS, seed, 4),
        ]
    )


def english_intro(row):
    seed = f"{row['Year']}-{row['Rank']}-{row['Song']}"
    lines = [line.strip() for line in row["Intro"].splitlines() if line.strip()]
    kept = [line for line in lines if not FORBIDDEN_EN_RE.search(line)]

    if len(kept) < 4:
        kept.append(pick(EN_MOMENT_LINES, seed, 21))
    if len(kept) < 5:
        kept.append(pick(EN_CLOSINGS, seed, 22))

    return "\n".join(kept[:6])


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
    for row in rows:
        row["ChineseIntroMoment"] = chinese_intro(row)
        row["EnglishIntroMoment"] = english_intro(row)

    lines = [
        "# Song Intros by Year - Same Singer Moved Back v7 Moment Focused",
        "",
        "Chinese intro appears before English intro. Intros focus on the song moment.",
        "",
    ]

    current_year = None
    for row in rows:
        if row["Year"] != current_year:
            current_year = row["Year"]
            lines.extend(["", f"## {current_year}"])

        lines.extend(["", f"### {row['Year']}.{int(row['Rank']):02d}"])
        lines.extend(row["ChineseIntroMoment"].splitlines())
        lines.append("")
        lines.extend(row["EnglishIntroMoment"].splitlines())
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
            if name not in fieldnames:
                fieldnames.append(name)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    by_year = defaultdict(int)
    for row in rows:
        by_year[row["Year"]] += 1
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"rows: {len(rows)}")
    print(dict(sorted(by_year.items())))


if __name__ == "__main__":
    main()
