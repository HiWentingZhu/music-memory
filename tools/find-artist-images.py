from __future__ import annotations

import csv
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "artist-info-source-of-truth-v1.csv"
OUT_CSV = ROOT / "output" / "artist-image-candidates-v1.csv"
OUT_MD = ROOT / "output" / "artist-image-candidates-v1.md"

USER_AGENT = "Mozilla/5.0 (compatible; MusicProjectArtistImageFinder/1.0)"

BAD_SOURCE_DOMAINS = [
    "pinterest.",
    "wallpaper",
    "alamy.",
    "shutterstock.",
    "gettyimages.",
    "dreamstime.",
    "depositphotos.",
    "amazon.",
    "ebay.",
]

QUERY_OVERRIDES = {
    "GALA": '"GALA乐队" "GALA band" 中国 摇滚 乐队 照片',
    "f(x) (에프엑스)": '"f(x)" "에프엑스" K-pop group official photo',
    "Tank": '"Tank" "吕建中" 台湾 歌手 照片',
    "Hugel": '"HUGEL" DJ producer official photo portrait',
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def english_alias(artist: str) -> str:
    match = re.search(r"\s\(([^()]*)\)\s*$", artist or "")
    return match.group(1).strip() if match else artist


def chinese_name(artist: str) -> str:
    return re.sub(r"\s\([^)]*\)\s*$", "", artist or "").strip()


def normalized(text: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", (text or "").lower())


def search_url(query: str) -> str:
    return "https://www.bing.com/images/search?q=" + urllib.parse.quote_plus(query) + "&form=HDRSC2&first=1"


def query_for_artist(row: dict[str, str]) -> str:
    artist = row["Artist"]
    if artist in QUERY_OVERRIDES:
        return QUERY_OVERRIDES[artist]
    alias = english_alias(artist)
    role = row.get("Role", "")
    if re.search(r"[\u4e00-\u9fff]", artist):
        return f'"{chinese_name(artist)}" "{alias}" 歌手 照片 photo'
    return f'"{alias}" singer artist photo portrait {role}'


def fetch_image_search(query: str) -> str:
    req = urllib.request.Request(search_url(query), headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=25) as response:
        return response.read().decode("utf-8", "ignore")


def parse_image_results(page: str) -> list[dict[str, str]]:
    results = []
    for match in re.finditer(r'class="iusc"[^>]*\sm="([^"]+)"', page):
        raw = html.unescape(match.group(1))
        try:
            data = json.loads(raw)
        except Exception:
            continue
        results.append(
            {
                "ImageURL": data.get("murl", ""),
                "ThumbnailURL": data.get("turl", ""),
                "SourcePageURL": data.get("purl", ""),
                "Title": html.unescape(data.get("t", "") or ""),
                "Description": html.unescape(data.get("desc", "") or ""),
            }
        )
    return results


def result_matches_artist(result: dict[str, str], artist: str) -> bool:
    text = f"{result['Title']} {result['Description']} {result['SourcePageURL']} {result['ImageURL']}"
    text_lower = text.lower()
    text_norm = normalized(text)
    alias = english_alias(artist)
    cn = chinese_name(artist)
    candidates = [artist, alias, cn]

    for candidate in candidates:
        candidate = (candidate or "").strip()
        if not candidate:
            continue
        # Avoid generic short aliases causing false positives.
        if re.fullmatch(r"[A-Za-z]{1,7}", candidate) and candidate.lower() not in {"laufey", "madcon", "gala", "hugel", "tank"}:
            continue
        if candidate.lower() in text_lower or normalized(candidate) in text_norm:
            return True
    return False


def score_result(result: dict[str, str], artist: str) -> int:
    text = f"{result['Title']} {result['Description']} {result['SourcePageURL']} {result['ImageURL']}".lower()
    score = 0
    if result_matches_artist(result, artist):
        score += 8
    for word in ["singer", "artist", "music", "band", "rapper", "official", "profile", "photo", "portrait"]:
        if word in text:
            score += 1
    if any(bad in text for bad in BAD_SOURCE_DOMAINS):
        score -= 4
    if "lyrics" in text:
        score -= 2
    if "wikipedia" in text or "baike" in text or "douban" in text or "music.apple" in text:
        score += 2
    return score


def unique_results(results: list[dict[str, str]]) -> list[dict[str, str]]:
    seen = set()
    unique = []
    for result in results:
        image_url = result["ImageURL"]
        if not image_url or image_url in seen:
            continue
        seen.add(image_url)
        unique.append(result)
    return unique


def main() -> None:
    rows = read_csv(SOURCE_CSV)
    output = []

    for index, row in enumerate(rows, start=1):
        artist = row["Artist"]
        query = query_for_artist(row)
        safe_artist = artist.encode("ascii", "backslashreplace").decode("ascii")
        print(f"[{index}/{len(rows)}] {safe_artist}")

        parsed = []
        status = "Search failed"
        try:
            page = fetch_image_search(query)
            parsed = parse_image_results(page)
            status = "Search parsed" if parsed else "No image results parsed"
            time.sleep(0.25)
        except Exception as exc:
            status = f"Search failed: {type(exc).__name__}"

        matched = [result for result in parsed if result_matches_artist(result, artist)]
        ranked = sorted(matched or parsed, key=lambda item: score_result(item, artist), reverse=True)
        selected = unique_results(ranked)[:5]

        count = len(selected)
        if count >= 5 and matched:
            image_status = "Found 5 image candidates"
        elif count >= 5:
            image_status = "Found 5 candidates but artist match needs review"
        elif count > 0 and matched:
            image_status = f"Only found {count} matched image candidates"
        elif count > 0:
            image_status = f"Only found {count} weak candidates - artist identity unclear"
        else:
            image_status = "No image candidates found"

        record = {
            "Artist": artist,
            "CountryRegion": row.get("CountryRegion", ""),
            "Role": row.get("Role", ""),
            "ImageSearchQuery": query,
            "ImageSearchURL": search_url(query),
            "SearchStatus": status,
            "ImageCandidateCount": str(count),
            "ImageStatus": image_status,
            "NeedsManualReview": "No" if image_status == "Found 5 image candidates" else "Yes",
        }
        for i in range(5):
            result = selected[i] if i < count else {"ImageURL": "", "ThumbnailURL": "", "SourcePageURL": "", "Title": "", "Description": ""}
            record[f"Image{i+1}URL"] = result["ImageURL"]
            record[f"Image{i+1}ThumbnailURL"] = result["ThumbnailURL"]
            record[f"Image{i+1}SourcePageURL"] = result["SourcePageURL"]
            record[f"Image{i+1}Title"] = result["Title"]
        output.append(record)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0].keys()))
        writer.writeheader()
        writer.writerows(output)

    lines = [
        "# Artist Image Candidates v1",
        "",
        "Up to 5 online image candidates per singer/group.",
        "Important: these are search candidates, not license-cleared website assets. Check rights/permissions before public use.",
        "",
    ]
    for row in output:
        lines.extend(
            [
                f"## {row['Artist']}",
                "",
                f"Status: {row['ImageStatus']}",
                "",
                f"Search: [{row['ImageSearchQuery']}]({row['ImageSearchURL']})",
                "",
            ]
        )
        for i in range(1, 6):
            url = row[f"Image{i}URL"]
            source = row[f"Image{i}SourcePageURL"]
            title = row[f"Image{i}Title"]
            if not url:
                continue
            lines.extend([f"{i}. [{title or 'Image candidate'}]({url})", f"   Source page: {source}", ""])

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"rows: {len(output)}")
    print(f"found 5 matched: {sum(1 for row in output if row['ImageStatus'] == 'Found 5 image candidates')}")
    print(f"needs review: {sum(1 for row in output if row['NeedsManualReview'] == 'Yes')}")


if __name__ == "__main__":
    main()
