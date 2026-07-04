from __future__ import annotations

import csv
import shutil
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MUSIC_LIST = ROOT / "output" / "FINAL_MUSIC_LIST.csv"
AUDIO_DIR = ROOT / "assets" / "audio"
REPORT_CSV = ROOT / "output" / "audio-copy-report-v1.csv"
MISSING_MD = ROOT / "output" / "audio-missing-after-copy-v1.md"

AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".opus", ".wma"}
YEARS = {"2022", "2023", "2024", "2025", "2026"}


def strip_brackets(value: str) -> str:
    pairs = {"(": ")", "（": "）", "[": "]", "【": "】"}
    closers = set(pairs.values())
    stack: list[str] = []
    out: list[str] = []
    for char in value:
        if char in pairs:
            stack.append(pairs[char])
            continue
        if stack and char == stack[-1]:
            stack.pop()
            continue
        if stack or char in closers:
            continue
        out.append(char)
    return "".join(out)


def normalize(value: str, *, remove_brackets: bool = True) -> str:
    value = unicodedata.normalize("NFKC", value or "").lower()
    if remove_brackets:
        value = strip_brackets(value)
    for char in "_-－—–·•!！?？,，.。:：;；'\"“”‘’/\\|":
        value = value.replace(char, " ")
    return "".join(
        char
        for char in value
        if ("a" <= char <= "z") or ("0" <= char <= "9") or ("\u4e00" <= char <= "\u9fff")
    )


def tokens(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", value or "")
    for char in "_-－—–·•!！?？,，.。:：;；'\"“”‘’/\\|()+（）[]【】":
        normalized = normalized.replace(char, " ")
    return [token.lower() for token in normalized.split() if token.strip()]


def artist_parts(artist: str) -> list[str]:
    parts = []
    current = ""
    for char in artist:
        if char in ",，、/&+":
            if current.strip():
                parts.append(current.strip())
            current = ""
        else:
            current += char
    if current.strip():
        parts.append(current.strip())
    expanded = []
    for part in parts or [artist]:
        expanded.append(part)
        if "(" in part:
            expanded.append(strip_brackets(part))
    return [part for part in expanded if normalize(part)]


def read_music_list() -> list[dict[str, str]]:
    with MUSIC_LIST.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def source_audio_files() -> list[Path]:
    return sorted(path for path in AUDIO_DIR.iterdir() if path.is_file() and path.suffix.lower() in AUDIO_EXTS)


def score_candidate(row: dict[str, str], path: Path) -> tuple[int, str]:
    song = row["Song"]
    artist = row["Artist"]
    stem = path.stem
    stem_norm = normalize(stem)
    song_norm = normalize(song)
    song_full_norm = normalize(song, remove_brackets=False)
    stem_tokens = set(tokens(stem))
    song_tokens = set(tokens(song))

    score = 0
    reasons = []
    if song_full_norm and song_full_norm in stem_norm:
        score += 110
        reasons.append("full song title")
    elif song_norm and song_norm in stem_norm:
        score += 95
        reasons.append("song title")
    elif stem_norm and stem_norm in song_norm:
        score += 50
        reasons.append("short filename title")

    if song_tokens:
        overlap = len(stem_tokens & song_tokens)
        if overlap:
            score += overlap * 8
            reasons.append(f"{overlap} title token(s)")

    artist_matched = False
    for part in artist_parts(artist):
        part_norm = normalize(part)
        if part_norm and part_norm in stem_norm:
            score += 32
            artist_matched = True
            reasons.append(f"artist: {part}")
            break

    ratio = SequenceMatcher(None, song_norm, stem_norm).ratio() if song_norm and stem_norm else 0
    if ratio > 0.45:
        score += int(ratio * 20)
        reasons.append("fuzzy title")

    title_is_short = len(song_norm) <= 3 or len(song_tokens) <= 1
    if title_is_short and not artist_matched:
        score = min(score, 70)
        reasons.append("short title without artist match")

    return score, "; ".join(reasons)


def unique_target_path(year_dir: Path, order: str, song: str, artist: str, source: Path) -> Path:
    base = f"{int(order):02d} - {safe_filename(artist)} - {safe_filename(song)}"
    target = year_dir / f"{base}{source.suffix.lower()}"
    counter = 2
    while target.exists():
        if target.stat().st_size == source.stat().st_size:
            return target
        target = year_dir / f"{base} ({counter}){source.suffix.lower()}"
        counter += 1
    return target


def safe_filename(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").strip()
    for char in '<>:"/\\|?*\x00':
        value = value.replace(char, "_")
    value = " ".join(value.split()).strip(" .")
    return value[:120] or "unknown"


def main() -> None:
    rows = read_music_list()
    files = source_audio_files()
    report = []

    for year in YEARS:
        (AUDIO_DIR / f"{year} music").mkdir(parents=True, exist_ok=True)

    for row in rows:
        candidates = []
        for path in files:
            score, reason = score_candidate(row, path)
            if score > 0:
                candidates.append((score, reason, path))
        candidates.sort(key=lambda item: (item[0], item[2].name), reverse=True)

        best = candidates[0] if candidates else None
        matched = bool(best and best[0] >= 95)
        status = "Copied" if matched else "Missing"
        source_path = best[2] if matched else None
        target_path = None

        if source_path:
            year_dir = AUDIO_DIR / f"{row['Year']} music"
            target_path = unique_target_path(year_dir, row["FinalOrder"], row["Song"], row["Artist"], source_path)
            if not target_path.exists():
                shutil.copy2(source_path, target_path)

        report.append(
            {
                "Year": row["Year"],
                "FinalOrder": row["FinalOrder"],
                "Song": row["Song"],
                "Artist": row["Artist"],
                "Status": status,
                "MatchedSource": str(source_path.relative_to(ROOT)) if source_path else "",
                "CopiedTo": str(target_path.relative_to(ROOT)) if target_path else "",
                "Score": str(best[0]) if best else "0",
                "MatchReason": best[1] if best else "",
                "BestCandidate": best[2].name if best else "",
            }
        )

    with REPORT_CSV.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(report[0].keys()))
        writer.writeheader()
        writer.writerows(report)

    missing = [item for item in report if item["Status"] != "Copied"]
    lines = [
        "# Audio Missing After Copy v1",
        "",
        f"Total songs in final list: {len(report)}",
        f"Copied: {sum(1 for item in report if item['Status'] == 'Copied')}",
        f"Missing: {len(missing)}",
        "",
    ]
    if missing:
        lines.append("## Missing Songs")
        lines.append("")
        for item in missing:
            lines.append(
                f"- {item['Year']} #{item['FinalOrder']}: {item['Song']} - {item['Artist']}"
                + (f" (best candidate: {item['BestCandidate']}, score {item['Score']})" if item["BestCandidate"] else "")
            )
    else:
        lines.append("No missing songs found.")
    MISSING_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"rows: {len(report)}")
    print(f"copied: {sum(1 for item in report if item['Status'] == 'Copied')}")
    print(f"missing: {len(missing)}")
    print(f"wrote: {REPORT_CSV}")
    print(f"wrote: {MISSING_MD}")


if __name__ == "__main__":
    main()
