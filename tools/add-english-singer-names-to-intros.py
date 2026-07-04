import csv
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v1.csv"
RELEASE_CSV = ROOT / "output" / "song-intros-by-year-release-years-v1.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v2-english-singers.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v2-english-singers.csv"
FINAL_MD = ROOT / "output" / "final-music-list-same-singer-moved-back-v2-english-singers.md"
FINAL_CSV = ROOT / "output" / "final-music-list-same-singer-moved-back-v2-english-singers.csv"
MAP_CSV = ROOT / "output" / "artist-english-name-map-v1.csv"


MANUAL_ARTIST_ENGLISH = {
    "亦然": "Yiran",
    "孟慧圆": "Meng Huiyuan",
    "丢火车乐队": "Lost Train Band",
    "丁一滕": "Ding Yiteng",
    "汪晨蕊": "Wang Chenrui",
    "周深": "Zhou Shen",
    "陈奕迅": "Eason Chan",
    "周杰伦": "Jay Chou",
    "李昂星": "Li Angxing",
    "杨宗纬": "Aska Yang",
    "王菀之": "Ivana Wong",
    "林俊杰": "JJ Lin",
    "苏打绿": "Sodagreen",
    "曾轶可": "Yico Zeng",
    "李玉刚": "Li Yugang",
    "剑网3": "JX3",
    "杨千嬅": "Miriam Yeung",
    "刘惜君": "Liu Xijun",
    "容祖儿": "Joey Yung",
    "F.I.R.飞儿乐团": "F.I.R.",
    "尤长靖": "You Zhangjing",
    "张靓颖": "Jane Zhang",
    "陈粒": "Chen Li",
    "毛不易": "Mao Buyi",
    "李克勤": "Hacken Lee",
    "Eric周兴哲": "Eric Chou",
    "周兴哲": "Eric Chou",
    "张韶涵": "Angela Chang",
    "檀健次": "Tan Jianci",
    "王心凌": "Cyndi Wang",
    "范逸臣": "Van Fan",
    "王靖雯": "Wang Jingwen",
    "唐汉霄": "Tang Hanxiao",
    "吴莫愁": "Momo Wu",
    "梁龙": "Liang Long",
    "苏见信 (信)": "Shin",
    "刘佳琪": "Liu Jiaqi",
    "赵紫骅": "Zhao Zihua",
    "许美静": "Mavis Hee",
    "五月天": "Mayday",
    "胡彦斌": "Tiger Hu",
    "张钰琪": "Zhang Yuqi",
    "吕方": "David Lui",
    "大张伟": "Wowkie Zhang",
    "翟潇闻": "Zhai Xiaowen",
    "汪苏泷": "Silence Wang",
    "薛之谦": "Joker Xue",
    "毕雯珺": "Bi Wenjun",
    "于文文": "Kelly Yu",
    "张碧晨": "Diamond Zhang",
    "希林娜依高": "Curley G",
    "后海大鲨鱼": "Queen Sea Big Shark",
    "孙燕姿": "Stefanie Sun",
    "莫文蔚": "Karen Mok",
    "梁静茹": "Fish Leong",
    "魏如萱": "Waa Wei",
    "姚晓棠": "Yao Xiaotang",
    "单依纯": "Shan Yichun",
    "刘宇宁": "Liu Yuning",
    "艾薇 Ivy": "Ivy Lee",
    "周菲戈": "Zhou Feige",
    "陈卓璇": "Chen Zhuoxuan",
    "Faye 詹雯婷": "Faye Chan",
    "张远": "Bird Zhang",
    "王栎鑫": "Wang Yuexin",
    "陆毅": "Lu Yi",
    "弹壳": "Danko",
    "宝石Gem": "Gem",
    "林志炫": "Terry Lin",
    "黄绮珊": "Susan Huang",
    "裁缝铺": "Tailor Shop Band",
    "邢晗铭": "Xing Hanming",
    "中国潮音": "China Chao Yin",
    "毛阿敏": "Mao Amin",
    "陈楚生": "Chen Chusheng",
    "八三夭阿璞": "A Pu",
    "古巨基": "Leo Ku",
    "于贞": "Yu Zhen",
    "阿达娃": "Adawa",
    "沙一汀EL": "Shayiting EL",
    "孙瑄阳Xtina": "Sun Xuanyang Xtina",
    "梁博": "Liang Bo",
    "三无Marblue": "Sanwu Marblue",
    "凡清 (Fanish)": "Fanish",
    "蔡国庆": "Cai Guoqing",
    "李玖哲": "Nicky Lee",
    "林忆莲": "Sandy Lam",
    "邓丽君": "Teresa Teng",
    "张国荣": "Leslie Cheung",
    "花儿乐队": "The Flowers",
    "陶晶莹": "Matilda Tao",
    "伍佰&China Blue": "Wu Bai & China Blue",
    "周华健": "Emil Wakin Chau",
    "朴树": "Pu Shu",
    "谭维维": "Sitar Tan",
    "苏诗丁": "Juno Su",
    "柏凝": "Baining",
    "霓虹花园NeonGarden": "NeonGarden",
    "黄誉博": "Huang Yubo",
    "赖美云": "Lai Meiyun",
    "张星特": "Zhang Xingte",
    "李承铉": "Nathan Lee",
    "陈冰": "Chen Bing",
    "艾热AIR": "Air",
    "王赫野": "Wang Heye",
    "徐佳莹": "Lala Hsu",
    "窦靖童": "Leah Dou",
    "张惠妹": "A-Mei",
    "宋冬野": "Song Dongye",
    "杨润泽": "Yang Runze",
    "呼和图拉嘎": "Huhe Tulaga",
    "郁可唯": "Yisa Yu",
    "李楚然": "Li Churan",
    "张栋梁": "Nicholas Teo",
    "银河快递 (Galaxy Express)": "Galaxy Express",
}


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def has_cjk(value):
    return bool(re.search(r"[\u3400-\u9fff]", value or ""))


def split_artists(value):
    return [part.strip() for part in re.split(r"\s*,\s*", value or "") if part.strip()]


def english_singer_from_display(value):
    if not value or " - " not in value:
        return ""
    return value.rsplit(" - ", 1)[1].strip()


def build_artist_map():
    artist_map = dict(MANUAL_ARTIST_ENGLISH)
    for row in load_csv(RELEASE_CSV):
        english_singer = english_singer_from_display(row["EnglishDisplayLine"])
        if not english_singer:
            continue
        chinese_parts = split_artists(row["Artist"])
        english_parts = split_artists(english_singer)
        artist_map.setdefault(row["Artist"], english_singer)
        if len(chinese_parts) == len(english_parts):
            for chinese, english in zip(chinese_parts, english_parts):
                if english and not has_cjk(english):
                    artist_map.setdefault(chinese, english)
    return artist_map


def singer_with_english(value, artist_map):
    parts = split_artists(value)
    if not parts:
        return value

    decorated = []
    for part in parts:
        english = artist_map.get(part, "")
        if not has_cjk(part) or not english or english == part:
            decorated.append(part)
        else:
            decorated.append(f"{part} ({english})")
    return ", ".join(decorated)


def cover_line_with_english(row, artist_map):
    singer = singer_with_english(row["VersionSinger"], artist_map)
    date = row["VersionReleaseDate"]
    if date and date != "Needs review":
        return f"{singer}, {date}"
    return singer


def original_line_with_english(row, artist_map):
    singer = singer_with_english(row["OriginalSinger"], artist_map)
    return f"Original: {singer}, {row['OriginalReleaseDate']}"


def display_credit(row):
    if row.get("MovedBackSameSinger") == "Yes":
        return row["IntroCreditLineEnglish"]
    if row["CoverVersionLine"]:
        return row["CoverVersionLineEnglish"]
    return row["OriginalLineEnglish"].replace("Original: ", "")


def main():
    artist_map = build_artist_map()
    rows = load_csv(SOURCE_CSV)

    for row in rows:
        row["VersionSingerEnglishDisplay"] = singer_with_english(row["VersionSinger"], artist_map)
        row["OriginalSingerEnglishDisplay"] = singer_with_english(row["OriginalSinger"], artist_map)
        row["CoverVersionLineEnglish"] = cover_line_with_english(row, artist_map) if row["CoverVersionLine"] else ""
        row["OriginalLineEnglish"] = original_line_with_english(row, artist_map)
        row["IntroCreditLineEnglish"] = row["VersionSingerEnglishDisplay"] if row.get("MovedBackSameSinger") == "Yes" else display_credit(row)

    lines = [
        "# Song Intros by Year - Same Singer Moved Back v2 English Singers",
        "",
        "Singer names are shown as Chinese name followed by English name when available.",
        "Songs moved back because the original singer and cover/live singer are the same still show only the cover/live singer line.",
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
        if row["ChineseDisplayTitle"]:
            lines.append(row["ChineseDisplayTitle"])
        lines.append(row["EnglishDisplayTitle"])
        lines.append("by")
        if row.get("MovedBackSameSinger") == "Yes":
            lines.append(row["VersionSingerEnglishDisplay"])
        else:
            if row["CoverVersionLine"]:
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

    by_year = defaultdict(list)
    for row in rows:
        by_year[row["Year"]].append(row)

    final_rows = []
    final_lines = [
        "# Final Music List - Same Singer Moved Back v2 English Singers",
        "",
        "Singer names are shown as Chinese name followed by English name when available.",
        "",
    ]
    for year in sorted(by_year):
        final_lines.extend([f"## {year}", ""])
        final_lines.append("| Final # | Original rank | Song | Artist | Intro credit |")
        final_lines.append("|---:|---:|---|---|---|")
        for index, row in enumerate(by_year[year], start=1):
            credit = display_credit(row)
            final_rows.append(
                {
                    "Year": year,
                    "FinalOrder": index,
                    "OriginalRank": row["Rank"],
                    "Song": row["Song"],
                    "Artist": row["Artist"],
                    "IntroCredit": credit,
                    "MovedBackSameSinger": row.get("MovedBackSameSinger", ""),
                    "OriginalShownInIntro": row.get("OriginalShownInIntro", ""),
                }
            )
            safe = [row["Song"], row["Artist"], credit]
            safe = [value.replace("|", "/") for value in safe]
            final_lines.append(f"| {index} | {row['Rank']} | {safe[0]} | {safe[1]} | {safe[2]} |")
        final_lines.append("")

    FINAL_MD.write_text("\n".join(final_lines), encoding="utf-8")
    with FINAL_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(final_rows[0].keys()))
        writer.writeheader()
        writer.writerows(final_rows)

    used_artists = sorted({part for row in rows for value in (row["VersionSinger"], row["OriginalSinger"]) for part in split_artists(value)})
    map_rows = [
        {"Artist": artist, "EnglishName": artist_map.get(artist, ""), "NeedsEnglishNameReview": "Yes" if has_cjk(artist) and not artist_map.get(artist, "") else ""}
        for artist in used_artists
    ]
    with MAP_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(map_rows[0].keys()))
        writer.writeheader()
        writer.writerows(map_rows)

    missing = sum(1 for row in map_rows if row["NeedsEnglishNameReview"])
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"wrote {FINAL_MD}")
    print(f"wrote {FINAL_CSV}")
    print(f"wrote {MAP_CSV}")
    print(f"rows: {len(rows)}")
    print(f"artist names needing english review: {missing}")
    print({year: len(by_year[year]) for year in sorted(by_year)})


if __name__ == "__main__":
    main()
