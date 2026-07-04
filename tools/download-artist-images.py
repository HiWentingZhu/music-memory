from __future__ import annotations

import csv
import mimetypes
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "artist-image-candidates-v1.csv"
OUT_DIR = ROOT / "output" / "artist-image-downloads-v1"
MANIFEST_CSV = ROOT / "output" / "artist-image-download-manifest-v1.csv"
MANIFEST_MD = ROOT / "output" / "artist-image-download-manifest-v1.md"

USER_AGENT = "Mozilla/5.0 (compatible; MusicProjectImageDownloader/1.0)"
MAX_BYTES = 12 * 1024 * 1024
MAX_WORKERS = 12
DOWNLOAD_TIMEOUT_SECONDS = 12


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def safe_name(value: str, max_len: int = 90) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", value or "").strip()
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return (cleaned or "unknown")[:max_len]


def extension_from(url: str, content_type: str) -> str:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(urllib.parse.unquote(parsed.path)).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        return ".jpg" if suffix == ".jpeg" else suffix
    guessed = mimetypes.guess_extension((content_type or "").split(";")[0].strip())
    if guessed in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        return ".jpg" if guessed == ".jpeg" else guessed
    return ".jpg"


def download(url: str, path_without_ext: Path) -> tuple[str, str, int]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=DOWNLOAD_TIMEOUT_SECONDS) as response:
        content_type = response.headers.get("Content-Type", "")
        if content_type and not content_type.lower().startswith("image/"):
            return "", f"Skipped non-image content type: {content_type}", 0

        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            return "", "Skipped file larger than 12 MB", len(data)

        ext = extension_from(url, content_type)
        path = path_without_ext.with_suffix(ext)
        path.write_bytes(data)
        return str(path), "Downloaded", len(data)


def existing_download(path_without_ext: Path) -> Path | None:
    matches = sorted(path_without_ext.parent.glob(f"{path_without_ext.name}.*"))
    return matches[0] if matches else None


def build_tasks(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    tasks = []
    for artist_index, row in enumerate(rows, start=1):
        artist = row["Artist"]
        artist_dir = OUT_DIR / f"{artist_index:03d} - {safe_name(artist)}"
        artist_dir.mkdir(parents=True, exist_ok=True)
        for image_index in range(1, 6):
            image_url = row.get(f"Image{image_index}URL", "")
            if not image_url:
                continue
            tasks.append(
                {
                    "Artist": artist,
                    "ArtistIndex": str(artist_index),
                    "ImageNumber": str(image_index),
                    "PathWithoutExt": str(artist_dir / f"{image_index:02d}"),
                    "OriginalImageURL": image_url,
                    "ThumbnailURL": row.get(f"Image{image_index}ThumbnailURL", ""),
                    "SourcePageURL": row.get(f"Image{image_index}SourcePageURL", ""),
                    "Title": row.get(f"Image{image_index}Title", ""),
                }
            )
    return tasks


def process_task(task: dict[str, str]) -> dict[str, str]:
    path_without_ext = Path(task["PathWithoutExt"])
    existing = existing_download(path_without_ext)
    if existing:
        return {
            **task,
            "DownloadedPath": str(existing),
            "DownloadStatus": "Already downloaded",
            "Bytes": str(existing.stat().st_size),
            "UsedURL": task["OriginalImageURL"],
            "WebsiteUseStatus": "Needs license review",
        }

    downloaded_path = ""
    status = "Not downloaded"
    bytes_downloaded = 0
    used_url = task["OriginalImageURL"]

    try:
        downloaded_path, status, bytes_downloaded = download(task["OriginalImageURL"], path_without_ext)
    except Exception as exc:
        status = f"Full image failed: {type(exc).__name__}"

    if not downloaded_path and task["ThumbnailURL"]:
        used_url = task["ThumbnailURL"]
        try:
            downloaded_path, status, bytes_downloaded = download(task["ThumbnailURL"], path_without_ext)
            status = "Downloaded thumbnail fallback" if downloaded_path else status
        except Exception as exc:
            status = f"{status}; thumbnail failed: {type(exc).__name__}"

    time.sleep(0.03)
    return {
        **task,
        "DownloadedPath": downloaded_path,
        "DownloadStatus": status,
        "Bytes": str(bytes_downloaded),
        "UsedURL": used_url,
        "WebsiteUseStatus": "Needs license review",
    }


def main() -> None:
    rows = read_csv(SOURCE_CSV)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tasks = build_tasks(rows)

    manifest: list[dict[str, str]] = []
    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_task, task) for task in tasks]
        for future in as_completed(futures):
            item = future.result()
            completed += 1
            if completed % 25 == 0 or completed == len(tasks):
                print(f"processed {completed}/{len(tasks)}")
            manifest.append(item)

    manifest.sort(key=lambda item: (int(item["ArtistIndex"]), int(item["ImageNumber"])))

    with MANIFEST_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        fieldnames = [
            "Artist",
            "ImageNumber",
            "DownloadedPath",
            "DownloadStatus",
            "Bytes",
            "UsedURL",
            "OriginalImageURL",
            "ThumbnailURL",
            "SourcePageURL",
            "Title",
            "WebsiteUseStatus",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(manifest)

    lines = [
        "# Artist Image Download Manifest v1",
        "",
        "Downloaded image candidates for review only. These files are not automatically approved for public website use.",
        "",
    ]
    for item in manifest:
        lines.extend(
            [
                f"## {item['Artist']} - Image {item['ImageNumber']}",
                "",
                f"Status: {item['DownloadStatus']}",
                f"Local file: {item['DownloadedPath'] or 'Not downloaded'}",
                f"Source page: {item['SourcePageURL']}",
                f"Website use status: {item['WebsiteUseStatus']}",
                "",
            ]
        )

    MANIFEST_MD.write_text("\n".join(lines), encoding="utf-8")

    downloaded = sum(1 for item in manifest if item["DownloadedPath"])
    failed = len(manifest) - downloaded
    print(f"wrote {MANIFEST_CSV}")
    print(f"wrote {MANIFEST_MD}")
    print(f"downloaded: {downloaded}")
    print(f"failed: {failed}")


if __name__ == "__main__":
    main()
