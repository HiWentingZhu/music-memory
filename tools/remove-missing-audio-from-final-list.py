from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
FINAL_CSV = OUTPUT / "FINAL_MUSIC_LIST.csv"
FINAL_MD = OUTPUT / "FINAL_MUSIC_LIST.md"
COPY_REPORT = OUTPUT / "audio-copy-report-v1.csv"

BACKUP_CSV = OUTPUT / "FINAL_MUSIC_LIST_WITH_MISSING_AUDIO_BACKUP.csv"
BACKUP_MD = OUTPUT / "FINAL_MUSIC_LIST_WITH_MISSING_AUDIO_BACKUP.md"
AUDIO_READY_CSV = OUTPUT / "final-music-list-audio-ready-v1.csv"
AUDIO_READY_MD = OUTPUT / "final-music-list-audio-ready-v1.md"
REMOVED_CSV = OUTPUT / "final-music-list-removed-missing-audio-v1.csv"
REMOVED_MD = OUTPUT / "final-music-list-removed-missing-audio-v1.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (row["Year"], row["FinalOrder"], row["Song"], row["Artist"])


def write_music_md(path: Path, rows: list[dict[str, str]], removed_count: int) -> None:
    lines = [
        "# Final Music List - Audio Ready",
        "",
        f"This list removes {removed_count} songs whose audio files are currently missing.",
        "",
    ]
    for year in sorted({row["Year"] for row in rows}):
        year_rows = [row for row in rows if row["Year"] == year]
        lines.extend(
            [
                f"## {year}",
                "",
                "| Final # | Original rank | Song | Artist | Intro credit |",
                "|---:|---:|---|---|---|",
            ]
        )
        for row in year_rows:
            lines.append(
                f"| {row['FinalOrder']} | {row['OriginalRank']} | {row['Song']} | {row['Artist']} | {row['IntroCredit']} |"
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_removed_md(path: Path, rows: list[dict[str, str]]) -> None:
    lines = [
        "# Removed From Final Music List - Missing Audio",
        "",
        f"Removed songs: {len(rows)}",
        "",
        "| Year | Old final # | Song | Artist |",
        "|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['Year']} | {row['FinalOrder']} | {row['Song']} | {row['Artist']} |")
    path.write_text("\n".join(lines), encoding="utf-8")


def new_audio_path(old_path: Path, new_order: str) -> Path:
    old_name = old_path.name
    if len(old_name) >= 5 and old_name[:2].isdigit() and old_name[2:5] == " - ":
        return old_path.with_name(f"{int(new_order):02d}{old_name[2:]}")
    return old_path.with_name(f"{int(new_order):02d} - {old_name}")


def rename_audio_files(rows: list[dict[str, str]], report_by_key: dict[tuple[str, str, str, str], dict[str, str]]) -> None:
    moves: list[tuple[Path, Path]] = []
    for row in rows:
        old_key = (row["Year"], row["OldFinalOrder"], row["Song"], row["Artist"])
        report = report_by_key.get(old_key)
        if not report or not report.get("CopiedTo"):
            continue
        source = ROOT / report["CopiedTo"]
        if not source.exists():
            continue
        target = new_audio_path(source, row["FinalOrder"])
        if source == target:
            continue
        moves.append((source, target))

    temp_moves = []
    for index, (source, target) in enumerate(moves, start=1):
        temp = source.with_name(f"__renaming_{index:03d}__{source.name}")
        source.rename(temp)
        temp_moves.append((temp, target))

    for temp, target in temp_moves:
        if target.exists():
            target.unlink()
        temp.rename(target)


def main() -> None:
    final_rows = read_csv(FINAL_CSV)
    report_rows = read_csv(COPY_REPORT)
    report_by_key = {key(row): row for row in report_rows}

    if not BACKUP_CSV.exists():
        shutil.copy2(FINAL_CSV, BACKUP_CSV)
    if FINAL_MD.exists() and not BACKUP_MD.exists():
        shutil.copy2(FINAL_MD, BACKUP_MD)

    kept = []
    removed = []
    year_counts: dict[str, int] = {}
    for row in final_rows:
        report = report_by_key.get(key(row))
        if report and report.get("Status") == "Copied":
            year_counts[row["Year"]] = year_counts.get(row["Year"], 0) + 1
            updated = {**row, "OldFinalOrder": row["FinalOrder"], "FinalOrder": str(year_counts[row["Year"]])}
            kept.append(updated)
        else:
            removed.append(row)

    final_fieldnames = ["Year", "FinalOrder", "OriginalRank", "Song", "Artist", "IntroCredit", "MovedBackSameSinger", "OriginalShownInIntro"]
    kept_final_rows = [{name: row.get(name, "") for name in final_fieldnames} for row in kept]
    removed_fieldnames = final_fieldnames

    rename_audio_files(kept, report_by_key)

    write_csv(AUDIO_READY_CSV, kept_final_rows, final_fieldnames)
    write_music_md(AUDIO_READY_MD, kept_final_rows, len(removed))
    write_csv(REMOVED_CSV, removed, removed_fieldnames)
    write_removed_md(REMOVED_MD, removed)

    write_csv(FINAL_CSV, kept_final_rows, final_fieldnames)
    write_music_md(FINAL_MD, kept_final_rows, len(removed))

    print(f"original rows: {len(final_rows)}")
    print(f"kept rows: {len(kept_final_rows)}")
    print(f"removed rows: {len(removed)}")
    for year in sorted(year_counts):
        print(f"{year}: {year_counts[year]}")
    print(f"wrote {FINAL_CSV}")
    print(f"wrote {FINAL_MD}")
    print(f"wrote {AUDIO_READY_CSV}")
    print(f"wrote {AUDIO_READY_MD}")
    print(f"wrote {REMOVED_CSV}")
    print(f"wrote {REMOVED_MD}")


if __name__ == "__main__":
    main()
