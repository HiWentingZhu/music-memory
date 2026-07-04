import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTED_CSV = ROOT / "output" / "top-50-songs-by-year-style-theme-revised-v2.csv"
SOURCE_CSV = ROOT / "sample-data" / "my-qq-music-2022-2026-design.csv"
RELEASE_LOOKUP_CSV = ROOT / "output" / "song-release-years-lookup.csv"
OUT_CSV = ROOT / "output" / "song-version-metadata-v1.csv"
CACHE_PATH = ROOT / "output" / "qq-search-cache-song-version-metadata.json"


MANUAL_VERSION_YEARS = {
    ("2022", "16", "带我走 (Live)", "苏打绿"): "",
    ("2023", "41", "我就不爱唱情歌 (Live)", "大张伟, 汪苏泷, 刘宇宁"): "2022",
    ("2024", "2", "有没有一首歌会让你想起我 (Live)", "胡彦斌, 陆毅, 弹壳, 宝石Gem"): "2023",
    ("2024", "7", "黑夜问白天 (Live)", "胡兵, 品冠, 胡彦斌, 魏巡"): "2023",
    ("2024", "8", "破茧 (2023披荆斩棘的哥哥第三季现场)", "胡彦斌, 魏巡, 伯远"): "2023",
    ("2024", "12", "华山论剑：冠世一战 (Live)", "方锦龙, 郭雅志, 李延亮, 赵兆交响乐团"): "2023",
    ("2024", "13", "阳光开朗大男孩 (Live)", "李昂星"): "",
    ("2024", "20", "三生三世 (2021时光音乐会第6期现场)", "林志炫"): "2021",
}


MANUAL_ORIGINALS = {
    ("2022", "16", "带我走 (Live)", "苏打绿"): ("带我走", "杨丞琳", "2008", "manual"),
    ("2023", "41", "我就不爱唱情歌 (Live)", "大张伟, 汪苏泷, 刘宇宁"): ("我就不爱唱情歌", "大张伟", "2011", "manual"),
    ("2024", "2", "有没有一首歌会让你想起我 (Live)", "胡彦斌, 陆毅, 弹壳, 宝石Gem"): ("有没有一首歌会让你想起我", "周华健", "2001", "manual"),
    ("2024", "7", "黑夜问白天 (Live)", "胡兵, 品冠, 胡彦斌, 魏巡"): ("黑夜问白天", "林俊杰", "2017", "manual"),
    ("2024", "8", "破茧 (2023披荆斩棘的哥哥第三季现场)", "胡彦斌, 魏巡, 伯远"): ("破茧", "张韶涵", "2020", "manual"),
    ("2024", "12", "华山论剑：冠世一战 (Live)", "方锦龙, 郭雅志, 李延亮, 赵兆交响乐团"): ("华山论剑：冠世一战", "方锦龙, 郭雅志, 李延亮, 赵兆交响乐团", "2023", "manual"),
    ("2024", "13", "阳光开朗大男孩 (Live)", "李昂星"): ("阳光开朗大男孩", "卦者灵风", "2021", "manual"),
    ("2024", "20", "三生三世 (2021时光音乐会第6期现场)", "林志炫"): ("三生三世", "张杰", "2017", "manual"),
}


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def normalize_title(title):
    value = title or ""
    value = re.sub(r"（[^）]*）", "", value)
    value = re.sub(r"\([^)]*\)", "", value)
    value = re.sub(r"\[[^\]]*\]", "", value)
    value = re.sub(r"《[^》]*》", "", value)
    value = re.sub(r"(?i)\b(live|explicit|single version|soundtrack version|outtake)\b", "", value)
    value = re.sub(r"(?i)from .*", "", value)
    value = re.sub(r"(?i)202\d.*现场", "", value)
    value = re.sub(r"(纯歌版|伴奏|现场|第\d+期|电视剧.*主题曲|电影.*主题曲)", "", value)
    value = re.sub(r"[\s\p{P}\p{S}]", "", value) if False else re.sub(r"[\s·・,，.。:：;；!！?？'\"“”‘’/\\|_\-—~～#]+", "", value)
    return value.strip().lower()


def base_title(title):
    value = title or ""
    value = re.sub(r"（[^）]*）", "", value)
    value = re.sub(r"\([^)]*\)", "", value)
    value = re.sub(r"\[[^\]]*\]", "", value)
    value = re.sub(r"《[^》]*》", "", value)
    value = value.replace("：", ":")
    return value.strip()


def is_version_title(title):
    return bool(re.search(r"(?i)live|现场|披荆斩棘|时光音乐会|第\d+期|重唱版|single version|soundtrack version|纯歌版|rock version|摇滚版|funk版", title or ""))


def singer_names(item):
    singers = item.get("singer") or []
    return ", ".join(s.get("name", "") for s in singers if s.get("name"))


def item_title(item):
    return item.get("title") or item.get("name") or ""


def search_qq(query, cache):
    if query in cache:
        return cache[query]
    payload = {
        "comm": {"ct": 24, "cv": 0},
        "req_1": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "query": query,
                "num_per_page": 30,
                "page_num": 1,
                "search_type": 0,
            },
        },
    }
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg?data=" + urllib.parse.quote(
        json.dumps(payload, separators=(",", ":"))
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 MusicIntroOriginalLookup/1.0",
            "Referer": "https://y.qq.com/",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        data = json.load(response)
    items = data.get("req_1", {}).get("data", {}).get("body", {}).get("song", {}).get("list", [])
    cache[query] = items
    time.sleep(0.12)
    return items


def choose_original(selected, cache):
    manual = MANUAL_ORIGINALS.get((selected["Year"], selected["Rank"], selected["Song"], selected["Artist"]))
    if manual:
        title, artist, year, method = manual
        return title, artist, "", year, method, "manual fallback"

    query = base_title(selected["Song"])
    if not query:
        query = selected["Song"]
    try:
        items = search_qq(query, cache)
    except Exception as exc:
        return query, "", "", "", "search_error", f"{type(exc).__name__}: {exc}"

    target_norm = normalize_title(query)
    candidates = []
    for item in items:
        title = item_title(item)
        norm = normalize_title(title)
        if norm != target_norm:
            continue
        pub = item.get("time_public") or item.get("album", {}).get("time_public", "")
        year_match = re.match(r"\d{4}", pub or "")
        year = year_match.group(0) if year_match else ""
        if not year:
            continue
        version_penalty = 1 if is_version_title(title) else 0
        album_title = item.get("album", {}).get("title", "")
        selected_artist_match = 0 if singer_names(item) == selected["Artist"] else 1
        candidates.append(
            {
                "title": title,
                "artist": singer_names(item),
                "year": year,
                "date": pub,
                "version_penalty": version_penalty,
                "selected_artist_match": selected_artist_match,
                "album": album_title,
            }
        )
    if not candidates:
        return query, selected["Artist"], "", "", "not_found", "no exact QQ search candidate with date"

    candidates.sort(key=lambda c: (c["version_penalty"], c["year"], c["selected_artist_match"]))
    chosen = candidates[0]
    method = "qq_search_exact_non_live" if chosen["version_penalty"] == 0 else "qq_search_exact"
    return chosen["title"], chosen["artist"], chosen["date"], chosen["year"], method, f"QQ search query: {query}"


def main():
    selected_rows = load_csv(SELECTED_CSV)
    source_rows = load_csv(SOURCE_CSV)
    release_rows = load_csv(RELEASE_LOOKUP_CSV)
    source_map = {(r["year"], r["track_title"], r["artist_name"]): r for r in source_rows}
    release_map = {(r["Year"], r["Rank"], r["Song"], r["Artist"]): r for r in release_rows}

    cache = {}
    if CACHE_PATH.exists():
        cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))

    output = []
    for idx, selected in enumerate(selected_rows, 1):
        source = source_map.get((selected["Year"], selected["Song"], selected["Artist"]), {})
        release = release_map.get((selected["Year"], selected["Rank"], selected["Song"], selected["Artist"]), {})
        manual_version_year = MANUAL_VERSION_YEARS.get((selected["Year"], selected["Rank"], selected["Song"], selected["Artist"]))
        version_year = manual_version_year if manual_version_year is not None else release.get("ReleaseYear", "")
        version_date = release.get("ReleaseDate", "")
        version_source = "manual fallback" if manual_version_year is not None else release.get("LookupStatus", "")
        original_title, original_singer, original_date, original_year, original_method, original_note = choose_original(selected, cache)
        if not original_year and not is_version_title(selected["Song"]):
            original_year = version_year
            original_date = version_date
            original_singer = selected["Artist"]
            original_title = selected["Song"]
            original_method = "selected_version_assumed_original"
            original_note = "no separate cover/live marker"
        output.append(
            {
                "Year": selected["Year"],
                "Rank": selected["Rank"],
                "Song": selected["Song"],
                "Artist": selected["Artist"],
                "VersionType": "cover/live/special version" if is_version_title(selected["Song"]) else "original or selected studio version",
                "VersionSinger": selected["Artist"],
                "VersionReleaseYear": version_year,
                "VersionReleaseDate": version_date,
                "VersionReleaseSource": version_source,
                "OriginalSongTitle": original_title,
                "OriginalSinger": original_singer,
                "OriginalReleaseDate": original_date,
                "OriginalReleaseYear": original_year,
                "OriginalLookupMethod": original_method,
                "OriginalLookupNote": original_note,
                "QQTrackID": source.get("qq_track_id", ""),
                "QQSongURL": source.get("qq_song_url", ""),
            }
        )
        if idx % 25 == 0:
            print(f"processed {idx}/{len(selected_rows)}")

    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0].keys()))
        writer.writeheader()
        writer.writerows(output)
    missing_original = [r for r in output if not r["OriginalReleaseYear"] or not r["OriginalSinger"]]
    missing_version = [r for r in output if not r["VersionReleaseYear"]]
    print(f"wrote {OUT_CSV}")
    print(f"missing original metadata: {len(missing_original)}")
    print(f"missing version year: {len(missing_version)}")


if __name__ == "__main__":
    main()
