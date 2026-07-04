from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTRO_CSV = ROOT / "output" / "selected-song-singer-intros-v1.csv"
PROFILE_CSV = ROOT / "output" / "online-singer-profiles-v1.csv"
OUT_CSV = ROOT / "output" / "singer-summaries-v3.csv"
OUT_MD = ROOT / "output" / "singer-summaries-v3.md"

COLLAB_SPLIT = re.compile(r"\s*(?:,|，|、|/|&| and | feat\. | ft\. | with | x )\s*", re.I)

LABEL_IDENTITY_OVERRIDES = {
    "Accusefive": ("Taiwanese", "band"),
    "Bella Poarch": ("Filipino-American", "singer and media personality"),
    "Bradley Cooper": ("American", "actor and singer"),
    "Bruno Mars": ("American", "singer-songwriter and performer"),
    "Charli XCX": ("British", "singer-songwriter and pop artist"),
    "Curley G": ("Chinese", "singer-songwriter"),
    "Eason Chan": ("Hong Kong", "singer and actor"),
    "G.E.M.": ("Hong Kong", "singer-songwriter"),
    "Hacken Lee": ("Hong Kong", "singer and actor"),
    "Hebe Tien": ("Taiwanese", "singer"),
    "Hins Cheung": ("Hong Kong", "singer-songwriter"),
    "Jay Chou": ("Taiwanese", "singer-songwriter and producer"),
    "JJ Lin": ("Singaporean", "singer-songwriter"),
    "Jackson Yee": ("Chinese", "singer and actor"),
    "Joker Xue": ("Chinese", "singer-songwriter"),
    "Jeff Chang": ("Taiwanese", "singer"),
    "Lady Gaga": ("American", "singer-songwriter and performer"),
    "Lala Hsu": ("Taiwanese", "singer-songwriter"),
    "Laufey (singer)": ("Icelandic-Chinese", "singer-songwriter"),
    "Li Yugang": ("Chinese", "singer and performer"),
    "Mao Amin": ("Chinese", "singer"),
    "Mayday (Taiwanese band)": ("Taiwanese", "band"),
    "Mavis Hee": ("Singaporean", "singer-songwriter"),
    "Miriam Yeung": ("Hong Kong", "singer and actress"),
    "Na Ying": ("Chinese", "singer"),
    "Nicholas Teo": ("Malaysian", "singer"),
    "Phoenix Legend": ("Chinese", "duo"),
    "Pu Shu": ("Chinese", "singer-songwriter"),
    "S.H.E": ("Taiwanese", "girl group"),
    "Smile_小千 (Smile Xiao Qian)": ("Chinese", "online music creator and self-media blogger"),
    "Stefanie Sun": ("Singaporean", "singer-songwriter"),
    "Tia Ray": ("Chinese", "singer-songwriter"),
    "Waa Wei": ("Taiwanese", "singer-songwriter"),
    "Yisa Yu": ("Chinese", "singer"),
    "Zhang Bichen": ("Chinese", "singer"),
}

GENDER_OVERRIDES = {
    "Amber Van Day": "female",
    "Bella Poarch": "female",
    "Bradley Cooper": "male",
    "Bruno Mars": "male",
    "Charli xcx": "female",
    "Chris James": "male",
    "Eric周兴哲 (Eric Chou)": "male",
    "Faye 詹雯婷 (Faye Chan)": "female",
    "G.E.M. 邓紫棋 (G.E.M.)": "female",
    "GALA": "group",
    "Hugel": "male",
    "JX3暗箱组合 (JX3 Anxiang Group)": "group",
    "Jony J": "male",
    "Lady Gaga": "female",
    "Laufey": "female",
    "Madcon": "group",
    "Ray Dalton": "male",
    "S.H.E": "group",
    "Smile_小千 (Smile Xiao Qian)": "male",
    "Spencer Stewart": "male",
    "Sub Urban": "male",
    "Tank": "male",
    "f(x) (에프엑스)": "group",
    "丁当 (Della Ding)": "female",
    "丢火车乐队 (Lost Train Band)": "group",
    "中国潮音 (China Chao Yin)": "group",
    "于文文 (Kelly Yu)": "female",
    "于贞 (Yu Zhen)": "female",
    "五月天 (Mayday)": "group",
    "五月天 阿信 (Ashin)": "male",
    "八三夭乐团 (831)": "group",
    "八三夭阿璞 (A Pu)": "male",
    "凡清 (Fanish) (Fanish)": "female",
    "凤凰传奇 (Phoenix Legend)": "group",
    "刘惜君 (Liu Xijun)": "female",
    "华晨宇 (Hua Chenyu)": "male",
    "单依纯 (Shan Yichun)": "female",
    "南征北战NZBZ (NZBZ)": "group",
    "古巨基 (Leo Ku)": "male",
    "司夏 (Sixia)": "female",
    "后海大鲨鱼 (Queen Sea Big Shark)": "group",
    "吕方 (David Lui)": "male",
    "吴莫愁 (Momo Wu)": "female",
    "告五人 (Accusefive)": "group",
    "周云蓬 (Zhou Yunpeng)": "male",
    "周杰伦 (Jay Chou)": "male",
    "周深 (Zhou Shen)": "male",
    "周笔畅 (Bibi Zhou)": "female",
    "唐汉霄 (Tang Hanxiao)": "male",
    "唐禹哲 (Danson Tang)": "male",
    "大张伟 (Wowkie Zhang)": "male",
    "孙燕姿 (Stefanie Sun)": "female",
    "孟慧圆 (Meng Huiyuan)": "female",
    "宝石Gem (Gem)": "male",
    "小时姑娘 (Xiaoshi Guniang)": "female",
    "小霞 (Xiao Xia)": "female",
    "尤长靖 (You Zhangjing)": "male",
    "希林娜依高 (Curley G)": "female",
    "张信哲 (Jeff Chang)": "male",
    "张敬轩 (Hins Cheung)": "male",
    "张栋梁 (Nicholas Teo)": "male",
    "张碧晨 (Diamond Zhang)": "female",
    "张远 (Bird Zhang)": "male",
    "张钰琪 (Zhang Yuqi)": "female",
    "张靓颖 (Jane Zhang)": "female",
    "张韶涵 (Angela Chang)": "female",
    "弹壳 (Danko)": "male",
    "徐佳莹 (Lala Hsu)": "female",
    "戴燕妮 (Dai Yanni)": "female",
    "方大同 (Khalil Fong)": "male",
    "早安 (Good Morning)": "male",
    "易烊千玺 (Jackson Yee)": "male",
    "曹杨 (Cao Yang)": "male",
    "朴树 (Pu Shu)": "male",
    "李克勤 (Hacken Lee)": "male",
    "李承铉 (Nathan Lee)": "male",
    "李玉刚 (Li Yugang)": "male",
    "李玖哲 (Nicky Lee)": "male",
    "李雪琴 (Li Xueqin)": "female",
    "杨乃文 (Faith Yang)": "female",
    "杨千嬅 (Miriam Yeung)": "female",
    "杨和苏KeyNG (KeyNG)": "male",
    "杨宗纬 (Aska Yang)": "male",
    "林俊杰 (JJ Lin)": "male",
    "林宥嘉": "male",
    "林志炫 (Terry Lin)": "male",
    "梁博 (Liang Bo)": "male",
    "梁龙 (Liang Long)": "male",
    "檀健次 (Tan Jianci)": "male",
    "毕雯珺 (Bi Wenjun)": "male",
    "毛不易 (Mao Buyi)": "male",
    "毛阿敏 (Mao Amin)": "female",
    "汪苏泷 (Silence Wang)": "male",
    "沙一汀EL (Shayiting EL)": "male",
    "洪佩瑜 (Pei-Yu Hung)": "female",
    "焦迈奇 (Jiao Maiqi)": "male",
    "王心凌 (Cyndi Wang)": "female",
    "王栎鑫 (Wang Yuexin)": "male",
    "王菀之 (Ivana Wong)": "female",
    "王靖雯 (Wang Jingwen)": "female",
    "田馥甄 (Hebe Tien)": "female",
    "窦靖童 (Leah Dou)": "female",
    "简单对话 A Little Conversation (A Little Conversation)": "group",
    "翟潇闻 (Zhai Xiaowen)": "male",
    "耿斯汉 (Geng Sihan)": "male",
    "胡彦斌 (Tiger Hu)": "male",
    "艾热AIR (Air)": "male",
    "艾薇 Ivy (Ivy Lee)": "female",
    "苏见信 (信) (Shin)": "male",
    "苏诗丁 (Juno Su)": "female",
    "范逸臣 Van Fan (Van Fan)": "male",
    "莫非定律乐团 (MFLD)": "group",
    "蔡国庆 (Cai Guoqing)": "male",
    "蔡旻佑 (Evan Yo)": "male",
    "薛之谦 (Joker Xue)": "male",
    "袁娅维TIA RAY (TIA RAY)": "female",
    "裁缝铺 (Tailor Shop Band)": "group",
    "许美静 (Mavis Hee)": "female",
    "谭维维 (Sitar Tan)": "female",
    "赖美云 (Lai Meiyun)": "female",
    "赵磊 (Zhao Lei)": "male",
    "那英 (Na Ying)": "female",
    "郁可唯 (Yisa Yu)": "female",
    "金玟岐 (Vanessa Jin)": "female",
    "银河快递 (Galaxy Express) (Galaxy Express)": "group",
    "阿达娃 (Adawa)": "female",
    "陆毅 (Lu Yi)": "male",
    "陈冰 (Chen Bing)": "female",
    "陈卓璇 (Chen Zhuoxuan)": "female",
    "陈奕迅 (Eason Chan)": "male",
    "陈婧霏 (Chen Jingfei)": "female",
    "陈楚生 (Chen Chusheng)": "male",
    "陈立农 (Chen Linong)": "male",
    "陈粒 (Chen Li)": "female",
    "陈雪燃 (Chen Xueran)": "male",
    "霓虹花园NeonGarden (NeonGarden)": "group",
    "魏如萱 (Waa Wei)": "female",
    "黄绮珊 (Susan Huang)": "female",
    "黄誉博 (Huang Yubo)": "male",
}

SUMMARY_OVERRIDES = {
    "Smile_小千 (Smile Xiao Qian)": (
        "A Chinese online music creator and self-media blogger. "
        "His style is rooted in guofeng music and ACG culture, with a strong focus on bringing traditional Chinese culture into online music communities. "
        "Beyond music, he is also known for an unusual dual identity: his main profession is as a civil servant."
    ),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def split_artist_entry(entry: str) -> list[str]:
    protected = re.sub(r"\(([^)]*)\)", lambda m: "(" + m.group(1).replace(",", "§") + ")", entry or "")
    return [part.replace("§", ",").strip() for part in COLLAB_SPLIT.split(protected) if part.strip()]


def source_link(profile: dict[str, str]) -> str:
    return (
        profile.get("WikipediaSearchURL")
        or profile.get("WikidataURL")
        or profile.get("GeneralSearchURL")
        or profile.get("CareerStartSearchURL")
        or ""
    )


def article(phrase: str) -> str:
    return "An" if phrase[:1].lower() in {"a", "e", "i", "o", "u"} else "A"


def country_from_text(text: str, label: str) -> str:
    label_key = label.strip()
    if label_key in LABEL_IDENTITY_OVERRIDES:
        return LABEL_IDENTITY_OVERRIDES[label_key][0]

    lower = (text or "").lower()
    country_terms = [
        ("Hong Kong", "hong kong"),
        ("Taiwanese", "taiwanese"),
        ("Singaporean", "singaporean"),
        ("Chinese", "chinese"),
        ("British", "british"),
        ("American", "american"),
        ("Canadian", "canadian"),
        ("Norwegian", "norwegian"),
        ("South Korean", "south korean"),
        ("Filipino-American", "filipino-american"),
        ("Filipino", "filipino"),
        ("Icelandic", "icelandic"),
        ("Danish", "danish"),
        ("French", "french"),
    ]
    for country, token in country_terms:
        if token in lower:
            return country
    return "country-to-confirm"


def role_from_text(text: str, label: str) -> str:
    label_key = label.strip()
    if label_key in LABEL_IDENTITY_OVERRIDES:
        return LABEL_IDENTITY_OVERRIDES[label_key][1]

    lower = f"{text or ''} {label or ''}".lower()
    if "girl group" in lower:
        return "girl group"
    if "band" in lower:
        return "band"
    if "rapper" in lower and "singer" in lower:
        return "singer and rapper"
    if "rapper" in lower:
        return "rapper"
    if "record producer" in lower or "songwriter" in lower:
        if "actor" in lower or "actress" in lower:
            return "singer-songwriter and screen performer"
        return "singer-songwriter"
    if "actor" in lower or "actress" in lower:
        return "singer and screen performer"
    if "musician" in lower:
        return "musician"
    if "singer" in lower:
        return "singer"
    return "artist"


def identity(profile: dict[str, str]) -> tuple[str, str, str]:
    description = profile.get("OnlineDescription") or ""
    label = profile.get("OnlineLabel") or profile.get("Artist") or ""
    country = country_from_text(description, label)
    role = role_from_text(description, label)
    phrase = f"{country} {role}"
    return f"{article(phrase)} {phrase}.", country, role


def make_identity_sentence(country: str, role: str) -> str:
    phrase = f"{country} {role}"
    return f"{article(phrase)} {phrase}."


def gender_for_artist(artist: str, role: str, profile: dict[str, str]) -> str:
    if artist in GENDER_OVERRIDES:
        return GENDER_OVERRIDES[artist]

    lower_role = (role or "").lower()
    lower_label = f"{profile.get('OnlineLabel', '')} {profile.get('OnlineDescription', '')}".lower()
    if any(word in lower_role for word in ["band", "group", "duo"]) or any(word in lower_label for word in ["band", "group", "duo"]):
        return "group"
    if "actress" in lower_label:
        return "female"
    if "actor" in lower_label:
        return "male"
    return "unknown"


def possessive_pronoun(gender: str) -> str:
    if gender == "female":
        return "Her"
    if gender == "male":
        return "His"
    if gender == "group":
        return "Their"
    return "This artist's"


def clean_style(style: str) -> str:
    style = (style or "").strip()
    if not style:
        return ""
    style = re.sub(r"^an?\s+", "", style, flags=re.I)
    return style.rstrip(".")


def style_summary(styles: list[str], pronoun: str) -> str:
    cleaned = [clean_style(style) for style in styles if clean_style(style)]
    if not cleaned:
        return f"{pronoun} style should be finalized after reviewing more public performance material."

    counts = Counter(cleaned)
    most_common = [item for item, _ in counts.most_common(2)]
    if len(most_common) == 1:
        return f"{pronoun} style leans toward {most_common[0]}."
    return f"{pronoun} style moves between {most_common[0]} and {most_common[1]}."


def career_note(notes: list[str], profile: dict[str, str]) -> str:
    start_year = (profile.get("CareerStartYear") or "").strip()
    if start_year:
        return f"Career-start year currently recorded as {start_year}, pending final source review."

    usable = []
    for note in notes:
        note = (note or "").strip()
        lower_note = note.lower()
        if (
            note
            and "needs source verification" not in lower_note
            and "collaboration or group performance" not in lower_note
            and "verified separately" not in lower_note
        ):
            usable.append(note.rstrip("."))
    if usable:
        return Counter(usable).most_common(1)[0][0] + "."

    return "Career-start timing needs source verification before public website use."


def main() -> None:
    intro_rows = read_csv(INTRO_CSV)
    profile_rows = read_csv(PROFILE_CSV)
    profiles_by_artist = {row["Artist"]: row for row in profile_rows}

    artist_data: dict[str, dict[str, object]] = defaultdict(
        lambda: {"song_count": 0, "years": set(), "styles": [], "career_notes": []}
    )

    for row in intro_rows:
        for artist in split_artist_entry(row.get("SelectedSinger", "")):
            data = artist_data[artist]
            data["song_count"] = int(data["song_count"]) + 1
            data["years"].add(row.get("Year", ""))
            data["styles"].append(row.get("SingerStyleNote", ""))
            data["career_notes"].append(row.get("CareerStartNote", ""))

    out_rows = []
    for artist in sorted(artist_data):
        data = artist_data[artist]
        profile = profiles_by_artist.get(artist, {})
        styles = list(data["styles"])
        career_notes = list(data["career_notes"])
        identity_sentence, country, role = identity(profile)
        gender = gender_for_artist(artist, role, profile)
        if gender == "group" and role == "artist":
            role = "group"
            identity_sentence = make_identity_sentence(country, role)
        pronoun = possessive_pronoun(gender)
        style = style_summary(styles, pronoun)
        career = career_note(career_notes, profile)
        summary = SUMMARY_OVERRIDES.get(artist) or " ".join([identity_sentence, style, career])

        out_rows.append(
            {
                "Artist": artist,
                "GenderPronounType": gender,
                "StylePronoun": pronoun,
                "CountryRegion": country,
                "Role": role,
                "SongRowCount": str(data["song_count"]),
                "Years": ", ".join(sorted(year for year in data["years"] if year)),
                "SingerSummary": summary,
                "IdentitySentence": identity_sentence,
                "StyleSummary": style,
                "CareerStartSummary": career,
                "OnlineLabel": profile.get("OnlineLabel", ""),
                "OnlineSourceStatus": profile.get("SourceStatus") or "No online profile row found",
                "SourceLink": source_link(profile),
                "CareerStartReviewLink": profile.get("CareerStartSearchURL", ""),
                "NeedsPublicWebsiteVerification": "Yes",
            }
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)

    lines = [
        "# Singer Summaries v3",
        "",
        "One summary per individual singer or group from the selected music list.",
        "Each summary follows: `A [country/region] [role]. [His/Her/Their/This artist's] style...`",
        "",
        "Rows marked `NeedsPublicWebsiteVerification = Yes` need final source review before publishing.",
        "",
    ]

    for row in out_rows:
        lines.extend(
            [
                f"## {row['Artist']}",
                "",
                row["SingerSummary"],
                "",
                f"Gender/pronoun type: {row['GenderPronounType']}",
                "",
                f"Country/region: {row['CountryRegion']}",
                "",
                f"Role: {row['Role']}",
                "",
                f"Years in selected list: {row['Years']}",
                "",
                f"Selected song rows: {row['SongRowCount']}",
                "",
                f"Source status: {row['OnlineSourceStatus']}",
                "",
                f"Source link: {row['SourceLink'] or row['CareerStartReviewLink'] or 'Needs source search'}",
                "",
                f"Needs public website verification: {row['NeedsPublicWebsiteVerification']}",
                "",
            ]
        )

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"artist rows: {len(out_rows)}")
    print(f"male: {sum(1 for row in out_rows if row['GenderPronounType'] == 'male')}")
    print(f"female: {sum(1 for row in out_rows if row['GenderPronounType'] == 'female')}")
    print(f"group: {sum(1 for row in out_rows if row['GenderPronounType'] == 'group')}")
    print(f"unknown: {sum(1 for row in out_rows if row['GenderPronounType'] == 'unknown')}")


if __name__ == "__main__":
    main()
