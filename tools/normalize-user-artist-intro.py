from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "output" / "artist_intro.csv"
OUT = ROOT / "output" / "artist_intro_utf8.csv"


def main() -> None:
    raw = SOURCE.read_bytes()
    text = raw.decode("gb18030")
    reader = csv.reader(text.splitlines())
    header = next(reader)
    rows = []
    for row in reader:
        if not row:
            continue
        fixed = {
            "Artist": row[0] if len(row) > 0 else "",
            "CountryRegion": row[1] if len(row) > 1 else "",
            "Role": row[2] if len(row) > 2 else "",
            "BriefArtistIntro (English)": row[3] if len(row) > 3 else "",
            "BriefArtistIntro (中文)": row[4] if len(row) > 4 else "",
            "Source": row[5] if len(row) > 5 else "",
        }

        # Repair rows where an unquoted comma split "Taiwan, China" or "Hong Kong, China".
        if len(row) >= 7 and row[1].strip() in {"Taiwan", "Hong Kong"} and row[2].strip() == "China":
            fixed = {
                "Artist": row[0],
                "CountryRegion": f"{row[1].strip()}, China",
                "Role": row[3],
                "BriefArtistIntro (English)": row[4],
                "BriefArtistIntro (中文)": row[5],
                "Source": row[6],
            }

        rows.append(fixed)

    fieldnames = [name for name in header if name]

    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})

    print(f"wrote {OUT}")
    print(f"rows: {len(rows)}")
    print(f"columns: {fieldnames}")


if __name__ == "__main__":
    main()
