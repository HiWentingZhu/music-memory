from __future__ import annotations

import base64
import csv
import html
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "singer-summaries-source-reviewed-v1.csv"
OUT_CSV = ROOT / "output" / "artist-review-online-sources-v2.csv"
OUT_MD = ROOT / "output" / "artist-review-online-sources-v2.md"

USER_AGENT = "Mozilla/5.0 (compatible; MusicProjectArtistReviewSourceFinder/2.0)"

GOOD_DOMAINS = [
    "allmusic.com",
    "pitchfork.com",
    "rollingstone.com",
    "billboard.com",
    "nme.com",
    "theguardian.com",
    "grammy.com",
    "metacritic.com",
    "albumoftheyear.org",
    "rateyourmusic.com",
    "music.apple.com",
    "spotify.com",
    "genius.com",
    "last.fm",
    "bandwagon.asia",
    "scmp.com",
    "radii.co",
    "timeout.com",
    "chinadaily.com.cn",
    "globaltimes.cn",
    "sixthtone.com",
    "thebeijinger.com",
    "douban.com",
    "music.douban.com",
    "y.qq.com",
    "music.163.com",
    "baike.baidu.com",
    "zh.wikipedia.org",
    "en.wikipedia.org",
]

BAD_DOMAINS = [
    "tiktok.com",
    "instagram.com",
    "facebook.com",
    "youtube.com",
    "bilibili.com",
    "twitter.com",
    "x.com",
    "pinterest.com",
    "amazon.com",
    "ebay.com",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def clean_artist_query_name(artist: str) -> str:
    return re.sub(r"\s+", " ", artist).strip()


def english_alias(artist: str) -> str:
    match = re.search(r"\(([^()]*)\)", artist or "")
    return match.group(1).strip() if match else artist


def chinese_name(artist: str) -> str:
    return re.sub(r"\s*\([^)]*\)", "", artist or "").strip()


def normalized(text: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", (text or "").lower())


def result_matches_artist(result: dict[str, str], artist: str) -> bool:
    haystack = f"{result['Title']} {result['Snippet']} {result['URL']}".lower()
    hay_norm = normalized(haystack)
    alias = english_alias(artist)
    cn = chinese_name(artist)
    candidates = [candidate for candidate in [artist, alias, cn] if candidate]

    for candidate in candidates:
        candidate = candidate.strip()
        if not candidate:
            continue
        # Avoid generic one-word names creating false matches, e.g. Amber, Gala, Air, Seven.
        if re.fullmatch(r"[A-Za-z]{1,7}", candidate) and candidate.lower() not in {"laufey", "madcon"}:
            continue
        if candidate.lower() in haystack or normalized(candidate) in hay_norm:
            return True
    return False


def bing_search(query: str) -> str:
    req = urllib.request.Request(search_url(query), headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read().decode("utf-8", "ignore")


def search_url(query: str) -> str:
    return "https://www.bing.com/search?q=" + urllib.parse.quote_plus(query)


def decode_bing_url(url: str) -> str:
    parsed = urllib.parse.urlparse(html.unescape(url))
    params = urllib.parse.parse_qs(parsed.query)
    encoded = (params.get("u") or [""])[0]
    if encoded.startswith("a1"):
        encoded = encoded[2:]
        padding = "=" * (-len(encoded) % 4)
        try:
            return base64.urlsafe_b64decode(encoded + padding).decode("utf-8", "ignore")
        except Exception:
            return url
    return url


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def parse_bing_results(page: str) -> list[dict[str, str]]:
    results = []
    blocks = re.findall(r'<li class="b_algo".*?</li>', page, flags=re.S)
    for block in blocks:
        match = re.search(r'<h2[^>]*>\s*<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', block, flags=re.S)
        if not match:
            continue
        url = decode_bing_url(match.group(1))
        title = strip_tags(match.group(2))
        snippet_match = re.search(r"<p>(.*?)</p>", block, flags=re.S)
        snippet = strip_tags(snippet_match.group(1) if snippet_match else "")
        results.append({"Title": title, "URL": url, "Snippet": snippet})
    return results


def domain(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.lower().replace("www.", "")


def score_result(result: dict[str, str], artist: str) -> int:
    url = result["URL"]
    host = domain(url)
    text = f"{result['Title']} {result['Snippet']} {url}".lower()
    score = 0

    if any(bad in host for bad in BAD_DOMAINS):
        score -= 10
    if any(good in host for good in GOOD_DOMAINS):
        score += 5
    for word in ["review", "interview", "profile", "biography", "artist", "singer", "songwriter", "music", "style", "album"]:
        if word in text:
            score += 1

    alias = english_alias(artist).lower()
    artist_lower = artist.lower()
    if alias and alias in text:
        score += 4
    if artist_lower and artist_lower in text:
        score += 4
    if "lyrics" in text:
        score -= 2
    return score


def query_for_artist(row: dict[str, str]) -> str:
    artist = clean_artist_query_name(row["Artist"])
    alias = english_alias(row["Artist"])
    role = row.get("Role") or "artist"
    if re.search(r"[\u4e00-\u9fff]", artist):
        return f'"{artist}" "{alias}" 音乐人 音乐 风格 采访 评价'
    return f'"{alias}" "music" artist review interview style {role}'


def main() -> None:
    rows = read_csv(SOURCE_CSV)
    output = []

    for index, row in enumerate(rows, start=1):
        artist = row["Artist"]
        query = query_for_artist(row)
        safe_artist = artist.encode("ascii", "backslashreplace").decode("ascii")
        print(f"[{index}/{len(rows)}] {safe_artist}")

        found = []
        status = "No search results parsed"
        try:
            page = bing_search(query)
            found = parse_bing_results(page)
            status = "Search results parsed" if found else "No search results parsed"
            time.sleep(0.25)
        except Exception as exc:
            status = f"Search failed: {type(exc).__name__}"

        ranked = sorted(found, key=lambda item: score_result(item, artist), reverse=True)
        ranked = [item for item in ranked if score_result(item, artist) > 0 and result_matches_artist(item, artist)][:5]

        record = {
            "Artist": artist,
            "CountryRegion": row["CountryRegion"],
            "Role": row["Role"],
            "Query": query,
            "ReviewSearchURL": search_url(query),
            "SearchStatus": status,
            "NeedsManualReview": "Yes",
        }
        for i in range(5):
            item = ranked[i] if i < len(ranked) else {"Title": "", "URL": "", "Snippet": ""}
            record[f"ReviewSource{i+1}Title"] = item["Title"]
            record[f"ReviewSource{i+1}URL"] = item["URL"]
            record[f"ReviewSource{i+1}Snippet"] = item["Snippet"]
        output.append(record)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0].keys()))
        writer.writeheader()
        writer.writerows(output)

    lines = [
        "# Artist Review Online Sources v2",
        "",
        "Online review/profile/interview source candidates for each singer or group.",
        "These are candidate links. Open each source before using any wording in public copy.",
        "",
    ]
    for row in output:
        lines.extend(
            [
                f"## {row['Artist']}",
                "",
                f"Search: [{row['Query']}]({row['ReviewSearchURL']})",
                "",
                f"Status: {row['SearchStatus']}",
                "",
            ]
        )
        has_source = False
        for i in range(1, 6):
            title = row[f"ReviewSource{i}Title"]
            url = row[f"ReviewSource{i}URL"]
            snippet = row[f"ReviewSource{i}Snippet"]
            if not url:
                continue
            has_source = True
            lines.extend([f"{i}. [{title}]({url})", "", snippet, ""])
        if not has_source:
            lines.extend(["No clean candidate parsed. Use the search link above for manual review.", ""])

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"rows: {len(output)}")
    print(f"with candidate sources: {sum(1 for row in output if row['ReviewSource1URL'])}")


if __name__ == "__main__":
    main()
