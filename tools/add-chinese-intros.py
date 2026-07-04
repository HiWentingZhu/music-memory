import csv
import hashlib
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v4-english-singers-dates.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v5-bilingual-intros.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v5-bilingual-intros.csv"


YEAR_THEMES = {
    "2022": {
        "space": "雨夜档案",
        "tone": "把私人的回声一层层收进抽屉",
        "light": "潮湿而温柔的灯光",
    },
    "2023": {
        "space": "返场舞台",
        "tone": "让旧歌在新的灯下重新呼吸",
        "light": "排练厅一样微亮的光",
    },
    "2024": {
        "space": "清醒的声场",
        "tone": "把力量、克制和告别重新排成队形",
        "light": "更锋利也更明亮的光",
    },
    "2025": {
        "space": "流动的夜色",
        "tone": "在速度、热度和温柔之间换气",
        "light": "霓虹和晨光交错的光",
    },
    "2026": {
        "space": "新的远方",
        "tone": "把已经走过的情绪推向更开阔的地方",
        "light": "像远处天色一样展开的光",
    },
}


IMAGE_RULES = [
    (("rain", "window", "glass"), ("雨声", "窗边", "水汽")),
    (("night", "dark", "midnight"), ("夜色", "未熄的灯", "安静的深处")),
    (("archive", "drawer", "shelf", "paper"), ("旧档案", "纸页", "抽屉")),
    (("stage", "live", "light", "lamp"), ("舞台灯", "返场", "光束")),
    (("road", "walk", "leave", "ticket"), ("路口", "车票", "远行")),
    (("sea", "water", "river"), ("潮水", "海边", "水面")),
    (("dream", "sleep"), ("梦", "半醒的时刻", "枕边")),
    (("fire", "heat", "burn"), ("火光", "余温", "热烈")),
    (("time", "clock", "years"), ("时间", "旧日历", "回声")),
    (("moon", "sky", "star", "light"), ("月光", "天空", "星点")),
    (("dance", "beat", "pulse"), ("节拍", "身体", "律动")),
    (("love", "heart", "tender"), ("心事", "温柔", "爱意")),
]


OPENINGS = [
    "《{title}》像一次轻轻推开的门，先让情绪站在门口。",
    "听到《{title}》，那份心事并不急着说破。",
    "《{title}》把一个很小的瞬间，慢慢放大成一整段风景。",
    "这首《{title}》一响起，就像有人把旧灯重新点亮。",
    "《{title}》不是直接抵达的歌，它先绕过一段沉默。",
    "在《{title}》里，情绪有了更清楚的轮廓。",
    "《{title}》像从记忆深处递来的一封短笺。",
    "这首歌把《{title}》里的名字，唱成可以停留的地方。",
]


IMAGE_LINES = [
    "它带着{a}、{b}和{c}，把没有说完的话慢慢铺开。",
    "{a}在旁边亮着，{b}轻轻靠近，{c}把回忆托住。",
    "那些{a}和{b}没有散去，只是在{c}里换了一种形状。",
    "它不靠用力推进，而是让{a}、{b}、{c}一点点浮出来。",
    "{a}先落下，随后是{b}，最后{c}把情绪接住。",
    "像{a}掠过{b}，又在{c}里留下很轻的一道痕。",
]


YEAR_LINES = [
    "放进{space}里，它让这一年的主题更清楚：{tone}。",
    "在{space}中，它把这一年的气质唱得更柔软，也更坚定。",
    "这一年需要这样的声音，替{space}留下一处可以回头的坐标。",
    "它让{space}不再只是背景，而像一次被认真听见的整理。",
    "于是{space}里那束{light}，也因为它多了一点温度。",
]


CLOSINGS = [
    "等最后一个音落下，留下来的不是结论，而是余韵。",
    "它适合在这里出现，因为它让记忆多了一次转身。",
    "这一段介绍之后，歌声刚好可以接过话题。",
    "它不把情绪推满，只把最该被听见的部分留下。",
    "所以轮到它时，整个年份像是忽然安静了一秒。",
    "它让下一首歌到来之前，空气里还有一点未散的光。",
]


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def clean_title(row):
    title = row["ChineseDisplayTitle"] or row["Song"]
    title = re.sub(r"\s*\([^)]*\)", "", title)
    title = re.sub(r"\s*（[^）]*）", "", title)
    return title.strip() or row["Song"]


def pick(items, seed, offset=0):
    digest = hashlib.sha256(f"{seed}:{offset}".encode("utf-8")).hexdigest()
    return items[int(digest[:8], 16) % len(items)]


def pick_images(intro, title, seed):
    text = f"{intro} {title}".lower()
    matches = []
    for keys, images in IMAGE_RULES:
        if any(key in text for key in keys):
            matches.extend(images)
    if len(matches) < 3:
        matches.extend(["灯光", "回声", "风", "旧照片", "人群", "远处"])

    unique = []
    for item in matches:
        if item not in unique:
            unique.append(item)
    first = pick(unique, seed, 11)
    remaining = [item for item in unique if item != first]
    second = pick(remaining, seed, 12)
    remaining = [item for item in remaining if item != second]
    third = pick(remaining, seed, 13)
    return first, second, third


def chinese_intro(row):
    title = clean_title(row)
    seed = f"{row['Year']}-{row['Rank']}-{row['Song']}"
    theme = YEAR_THEMES[row["Year"]]
    a, b, c = pick_images(row["Intro"], title, seed)

    opening = pick(OPENINGS, seed, 1).format(title=title)
    image_line = pick(IMAGE_LINES, seed, 2).format(a=a, b=b, c=c)
    year_line = pick(YEAR_LINES, seed, 3).format(**theme)
    closing = pick(CLOSINGS, seed, 4)
    return "\n".join([opening, image_line, year_line, closing])


def main():
    rows = load_csv(SOURCE_CSV)
    for row in rows:
        row["ChineseIntro"] = chinese_intro(row)

    lines = [
        "# Song Intros by Year - Same Singer Moved Back v5 Bilingual Intros",
        "",
        "English intro is kept. A fluent Chinese intro version is added for each song.",
        "",
    ]

    current_year = None
    for row in rows:
        if row["Year"] != current_year:
            current_year = row["Year"]
            lines.extend(["", f"## {current_year}"])

        lines.extend(["", f"### {row['Year']}.{int(row['Rank']):02d}"])
        lines.extend(row["Intro"].splitlines())
        lines.append("")
        lines.append("中文介绍")
        lines.extend(row["ChineseIntro"].splitlines())
        lines.append("")
        if row["ChineseDisplayTitle"]:
            lines.append(row["ChineseDisplayTitle"])
        lines.append(row["EnglishDisplayTitle"])
        lines.append("by")
        if row.get("MovedBackSameSinger") == "Yes":
            lines.append(row["SameSingerLineWithDate"])
        else:
            if row["CoverVersionLineEnglish"]:
                lines.append(row["CoverVersionLineEnglish"])
            lines.append(row["OriginalLineEnglish"])

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
