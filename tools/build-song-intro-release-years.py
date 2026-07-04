import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "sample-data" / "my-qq-music-2022-2026-design.csv"
SELECTED_CSV = ROOT / "output" / "top-50-songs-by-year-style-theme-revised-v2.csv"
OUT_CSV = ROOT / "output" / "song-release-years-lookup.csv"


def key(title, artist):
    return f"{title}\0{artist}"


def fetch_qq_song(song_mid):
    payload = {
        "comm": {"ct": 24, "cv": 0},
        "songinfo": {
            "method": "get_song_detail_yqq",
            "param": {"song_type": 0, "song_mid": song_mid, "song_id": 0},
            "module": "music.pf_song_detail_svr",
        },
    }
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg?data=" + urllib.parse.quote(
        json.dumps(payload, separators=(",", ":"))
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 MusicIntroReleaseLookup/1.0",
            "Referer": "https://y.qq.com/",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def extract_pub_date(data):
    song = data.get("songinfo", {}).get("data", {})
    track = song.get("track_info", {})
    for value in (
        track.get("time_public"),
        track.get("album", {}).get("time_public"),
    ):
        if value and re.search(r"\d{4}", value):
            return value
    pub_info = song.get("info", {}).get("pub_time", {}).get("content", [])
    for item in pub_info:
        value = item.get("value", "")
        if value and re.search(r"\d{4}", value):
            return value
    return ""


def main():
    with SOURCE_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        source_rows = list(csv.DictReader(f))
    source_by_key = {key(r["track_title"], r["artist_name"]): r for r in source_rows}

    with SELECTED_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        selected_rows = list(csv.DictReader(f))

    output = []
    cache = {}
    for index, selected in enumerate(selected_rows, start=1):
        source = source_by_key.get(key(selected["Song"], selected["Artist"]), {})
        song_mid = source.get("qq_track_id", "")
        pub_date = ""
        status = "missing_qq_track_id"
        if song_mid:
            try:
                if song_mid not in cache:
                    cache[song_mid] = fetch_qq_song(song_mid)
                    time.sleep(0.12)
                pub_date = extract_pub_date(cache[song_mid])
                status = "ok" if pub_date else "no_pub_date"
            except Exception as exc:
                status = f"error: {type(exc).__name__}: {exc}"
        output.append(
            {
                "Year": selected["Year"],
                "Rank": selected["Rank"],
                "Song": selected["Song"],
                "Artist": selected["Artist"],
                "QQTrackID": song_mid,
                "ReleaseDate": pub_date,
                "ReleaseYear": pub_date[:4] if re.match(r"\d{4}", pub_date) else "",
                "LookupStatus": status,
                "QQSongURL": source.get("qq_song_url", ""),
            }
        )
        if index % 25 == 0:
            print(f"looked up {index}/{len(selected_rows)}")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0].keys()))
        writer.writeheader()
        writer.writerows(output)
    print(f"saved {OUT_CSV}")
    missing = [r for r in output if not r["ReleaseYear"]]
    print(f"missing release years: {len(missing)}")


if __name__ == "__main__":
    main()
