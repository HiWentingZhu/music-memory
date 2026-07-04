import csv
import json
import re
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v12-life-like-relatable.csv"
OUT_CSV = ROOT / "output" / "online-singer-profiles-v1.csv"
OUT_MD = ROOT / "output" / "online-singer-profiles-v1.md"

USER_AGENT = "MusicProjectSingerResearch/1.0 (public website singer intro sourcing)"

WIKI_TITLE_OVERRIDES = {
    "Charli xcx": "Charli XCX",
    "Tiger Hu": "Tiger Hu",
    "Curley G": "Curley G",
    "Diamond Zhang": "Zhang Bichen",
    "Silence Wang": "Silence Wang",
    "Eason Chan": "Eason Chan",
    "Aska Yang": "Aska Yang",
    "Lala Hsu": "Lala Hsu",
    "Wowkie Zhang": "Wowkie Zhang",
    "Chen Chusheng": "Chen Chusheng",
    "Zhou Shen": "Zhou Shen",
    "Mao Buyi": "Mao Buyi",
    "Jackson Yee": "Jackson Yee",
    "Jay Chou": "Jay Chou",
    "Jane Zhang": "Jane Zhang",
    "Vanessa Jin": "Vanessa Jin",
    "Accusefive": "Accusefive",
    "Lady Gaga": "Lady Gaga",
    "Chen Li": "Chen Li (singer)",
    "Eric Chou": "Eric Chou",
    "Angela Chang": "Angela Chang",
    "GALA": "Gala (band)",
    "Joker Xue": "Joker Xue",
    "S.H.E": "S.H.E",
    "JJ Lin": "JJ Lin",
    "Tan Jianci": "Tan Jianci",
    "Shin": "Shin (singer)",
    "Terry Lin": "Terry Lin",
    "Mayday": "Mayday (Taiwanese band)",
    "Khalil Fong": "Khalil Fong",
    "Na Ying": "Na Ying",
    "Stefanie Sun": "Stefanie Sun",
    "Nicholas Teo": "Nicholas Teo",
    "Mavis Hee": "Mavis Hee",
    "Li Yugang": "Li Yugang",
    "Miriam Yeung": "Miriam Yeung",
    "Hacken Lee": "Hacken Lee",
    "Cyndi Wang": "Cyndi Wang",
    "Hins Cheung": "Hins Cheung",
    "Della Ding": "Della Ding",
    "Hua Chenyu": "Hua Chenyu",
    "G.E.M.": "G.E.M.",
    "Phoenix Legend": "Phoenix Legend",
    "Chen Linong": "Chen Linong",
    "Waa Wei": "Waa Wei",
    "Jeff Chang": "Jeff Chang",
    "Bibi Zhou": "Bibi Zhou",
    "Bradley Cooper": "Bradley Cooper",
    "Leo Ku": "Leo Ku",
    "Mao Amin": "Mao Amin",
    "Faith Yang": "Faith Yang",
    "Nicky Lee": "Nicky Lee",
    "Laufey": "Laufey (singer)",
    "Bruno Mars": "Bruno Mars",
    "Sub Urban": "Sub Urban",
    "Bella Poarch": "Bella Poarch",
    "Pu Shu": "Pu Shu",
    "TIA RAY": "Tia Ray",
    "Madcon": "Madcon",
    "Ray Dalton": "Ray Dalton",
    "Leah Dou": "Leah Dou",
    "Jony J": "Jony J",
    "Yisa Yu": "Yisa Yu",
    "Hebe Tien": "Hebe Tien",
}


def request_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def api_url(base, params):
    return base + "?" + urllib.parse.urlencode(params)


def strip_parentheses_name(name):
    name = re.sub(r"\s*\([^)]*\)", "", name or "").strip()
    return name


def english_name(name):
    match = re.search(r"\(([^()]*)\)", name or "")
    if match:
        return match.group(1).strip()
    return strip_parentheses_name(name)


def split_artist_entry(entry):
    parts = re.split(r"\s*,\s*|\s*/\s*|、|，", entry or "")
    cleaned = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Avoid splitting parenthetical English aliases further.
        cleaned.append(part)
    return cleaned


def selected_singer(row):
    return (
        (row.get("VersionSingerEnglishDisplay") or "").strip()
        or (row.get("VersionSinger") or "").strip()
        or (row.get("Artist") or "").strip()
    )


def search_wikidata(query, language="en"):
    url = api_url(
        "https://www.wikidata.org/w/api.php",
        {
            "action": "wbsearchentities",
            "search": query,
            "language": language,
            "format": "json",
            "limit": "3",
        },
    )
    data = request_json(url)
    return data.get("search") or []


def search_url(query):
    return f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"


def first_words(text, limit=28):
    words = re.sub(r"\s+", " ", text or "").strip().split()
    if len(words) <= limit:
        return " ".join(words)
    return " ".join(words[:limit]).rstrip(",.;:") + "..."


def strip_html(text):
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def search_wikipedia(query):
    url = api_url(
        "https://en.wikipedia.org/w/api.php",
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": "3",
        },
    )
    data = request_json(url)
    return ((data.get("query") or {}).get("search") or [])


def wikipedia_summary(title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"
    return request_json(url)


def choose_search_terms(artist):
    terms = []
    en = english_name(artist)
    cn = strip_parentheses_name(artist)
    if en:
        terms.append(en)
    if cn and cn != en:
        terms.append(cn)
    terms.append(artist)
    seen = set()
    ordered = []
    for term in terms:
        term = term.strip()
        if term and term.lower() not in seen:
            seen.add(term.lower())
            ordered.append(term)
    return ordered


def normalized(text):
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", (text or "").lower())


def is_likely_artist_title(title, artist, term):
    title_norm = normalized(title)
    candidates = [
        normalized(term),
        normalized(english_name(artist)),
        normalized(strip_parentheses_name(artist)),
    ]
    return any(value and (value in title_norm or title_norm in value) for value in candidates)


def find_artist_profile(artist):
    for term in choose_search_terms(artist):
        title = WIKI_TITLE_OVERRIDES.get(term)
        if not title:
            continue
        try:
            summary = wikipedia_summary(title)
            time.sleep(0.2)
            extract = summary.get("extract", "")
            url = ((summary.get("content_urls") or {}).get("desktop") or {}).get("page", "")
            if extract:
                return {
                    "QID": "",
                    "OnlineLabel": title,
                    "OnlineDescription": first_words(extract),
                    "WikidataURL": "",
                    "WikipediaSearchURL": url or f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
                    "CareerStartSearchURL": search_url(f"{artist} when did they start singing debut career"),
                    "CareerStartYear": "",
                    "SourceStatus": "Matched Wikipedia override",
                }
        except Exception:
            return {
                "QID": "",
                "OnlineLabel": title,
                "OnlineDescription": "",
                "WikidataURL": "",
                "WikipediaSearchURL": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
                "CareerStartSearchURL": search_url(f"{artist} when did they start singing debut career"),
                "CareerStartYear": "",
                "SourceStatus": "Matched Wikipedia override URL only",
            }

    for term in choose_search_terms(artist):
        query = f"{term} singer"
        try:
            wiki_hits = search_wikipedia(query)
            time.sleep(0.2)
            if wiki_hits:
                title = wiki_hits[0].get("title", "")
                snippet = strip_html(wiki_hits[0].get("snippet", ""))
                extract = snippet
                url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
                if title and extract and is_likely_artist_title(title, artist, term):
                    return {
                        "QID": "",
                        "OnlineLabel": title,
                        "OnlineDescription": first_words(extract),
                        "WikidataURL": "",
                        "WikipediaSearchURL": url or search_url(query),
                        "CareerStartSearchURL": search_url(f"{artist} when did they start singing debut career"),
                        "CareerStartYear": "",
                        "SourceStatus": "Matched Wikipedia profile",
                    }
        except Exception:
            continue

    candidates = []
    terms = choose_search_terms(artist)
    primary = terms[0] if terms else artist
    try:
        candidates.extend(search_wikidata(primary, "en"))
        time.sleep(0.35)
    except Exception:
        candidates = []
    if not candidates and len(terms) > 1:
        try:
            candidates.extend(search_wikidata(terms[1], "zh"))
            time.sleep(0.35)
        except Exception:
            candidates = []
    if not candidates:
        return {
            "QID": "",
            "OnlineLabel": "",
            "OnlineDescription": "",
            "WikidataURL": "",
            "WikipediaSearchURL": search_url(f"{artist} singer biography"),
            "CareerStartSearchURL": search_url(f"{artist} when did they start singing debut career"),
            "CareerStartYear": "",
            "SourceStatus": "No online profile found",
        }

    # Prefer music-related descriptions.
    def score(candidate):
        text = f"{candidate.get('label','')} {candidate.get('description','')}".lower()
        music_words = ["singer", "musician", "band", "vocalist", "rapper", "songwriter", "歌手", "樂團", "乐团", "音樂", "音乐"]
        return sum(2 for word in music_words if word in text) + (1 if candidate.get("concepturi") else 0)

    chosen = sorted(candidates, key=score, reverse=True)[0]
    qid = chosen.get("id", "")
    label = chosen.get("label", "")
    description = chosen.get("description", "")
    return {
        "QID": qid,
        "OnlineLabel": label,
        "OnlineDescription": description,
        "WikidataURL": f"https://www.wikidata.org/wiki/{qid}" if qid else "",
        "WikipediaSearchURL": search_url(f"{artist} singer biography"),
        "CareerStartSearchURL": search_url(f"{artist} when did they start singing debut career"),
        "CareerStartYear": "",
        "SourceStatus": "Matched online profile" if qid else "No online profile found",
    }


def build_intro(artist, profile):
    label = profile.get("OnlineLabel") or artist
    description = profile.get("OnlineDescription") or "artist profile needs source review"
    start = profile.get("CareerStartYear")
    if start:
        return f"{artist} is introduced online as {description}. Their public career profile begins around {start}, based on structured online metadata."
    return f"{artist} is introduced online as {description}. Their exact debut or career-start year still needs source review before public website use."


def main():
    rows = list(csv.DictReader(SOURCE_CSV.open("r", encoding="utf-8-sig", newline="")))
    entry_counts = Counter(selected_singer(row) for row in rows)
    individual_counts = Counter()
    individual_to_entries = {}
    for entry, count in entry_counts.items():
        for artist in split_artist_entry(entry):
            individual_counts[artist] += count
            individual_to_entries.setdefault(artist, set()).add(entry)

    output_rows = []
    for index, (artist, count) in enumerate(individual_counts.most_common(), start=1):
        safe_artist = artist.encode("ascii", "replace").decode("ascii")
        print(f"[{index}/{len(individual_counts)}] {safe_artist}")
        profile = find_artist_profile(artist)
        output_rows.append(
            {
                "Artist": artist,
                "SongRowCount": count,
                "AppearsInSingerEntries": " | ".join(sorted(individual_to_entries.get(artist, []))),
                "OnlineLabel": profile["OnlineLabel"],
                "OnlineDescription": profile["OnlineDescription"],
                "CareerStartYear": profile["CareerStartYear"],
                "OnlineSingerIntroDraft": build_intro(artist, profile),
                "WikidataURL": profile["WikidataURL"],
                "WikipediaSearchURL": profile["WikipediaSearchURL"],
                "CareerStartSearchURL": profile["CareerStartSearchURL"],
                "SourceStatus": profile["SourceStatus"],
                "NeedsManualReview": "Yes",
            }
        )

    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)

    lines = [
        "# Online Singer Profiles v1",
        "",
        "Sourced singer profile draft generated from public Wikidata/Wikipedia metadata. Use this as a research layer before final public website copy.",
        "",
        "## Notes",
        "",
        "- This v1 uses one lightweight Wikidata search per artist to avoid API rate limits.",
        "- CareerStartYear is intentionally blank in this pass; use CareerStartSearchURL to verify debut/start facts.",
        "- OnlineDescription is a short public metadata description, not final website prose.",
        "",
    ]
    for row in output_rows:
        lines.extend(
            [
                f"## {row['Artist']}",
                "",
                row["OnlineSingerIntroDraft"],
                "",
                f"- Source: {row['WikidataURL'] or 'Not found'}",
                f"- Wikipedia search: {row['WikipediaSearchURL'] or 'Not found'}",
                f"- Career-start search: {row['CareerStartSearchURL'] or 'Not found'}",
                f"- Needs manual review: {row['NeedsManualReview'] or 'No'}",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")
    print(f"artist rows: {len(output_rows)}")
    print(Counter(row["SourceStatus"] for row in output_rows))
    print(f"needs manual review: {sum(1 for row in output_rows if row['NeedsManualReview'])}")


if __name__ == "__main__":
    main()
