# Music Database Processing Workflow

Use this workflow every time a new music database or new QQ Music playlist set is provided.

## Goal

Turn raw music data into backend design artifacts for the Music Personality World:

- normalized enriched music database
- design-facing CSV
- year-by-year visual summary
- connected transition arc
- year-specific harshtags
- year-specific color palettes
- color palette board

The website should consume final data and tags, but it should not show this backend reasoning process.

## Required Flow

1. Resolve source links.
   - For QQ Music short links, resolve each year into a playlist ID.
   - Preserve the source URL and resolved playlist URL.
   - Confirm whether any years accidentally point to the same playlist.

2. Fetch and normalize tracks.
   - Required website fields: `year`, `track_title`, `artist_name`, `album_name`, `duration_ms`, `play_count`, `genre_or_tags`.
   - Preserve QQ IDs: song ID, artist ID, album ID, playlist ID, source URL.
   - Do not remove cross-year repeats; they are meaningful memory loops.
   - Remove only duplicate songs inside the same year if they appear.

3. Enrich music DNA.
   - Infer music type.
   - Derive lyric themes, mood, energy, and keywords.
   - Do not store full lyrics.
   - Store review/search context when public review data is unavailable.

4. Compare years by difference, not raw frequency.
   - Use relative lift for artists, moods, themes, and types.
   - Identify scale shifts: track count, unique artists, repeat weight.
   - Identify scene shifts: density, motion, materials, character behavior.

5. Build the transition spine.
   - Write one connected arc across all years.
   - For the current 2022-2026 database, use:

```text
dense private archive -> live/rehearsal density -> solitude reconciliation -> kinetic charge -> open horizon nostalgia
```

   - Link years through one transforming motif, such as:

```text
archive thread -> microphone cable -> repair line -> neon rail -> wind path
```

6. Create yearly visual directions.
   - Each year must have a distinct scene concept.
   - Each year needs character action, scene materials, motion cues, album wall behavior, mood calendar behavior, and controller direction.
   - Adjacent years must inherit and transform at least one object or motion motif.

7. Create harshtags.
   - Keep each harshtag at 25 characters or fewer, including `#`.
   - Prefer 2-5 strong tags per year.
   - Tags must show what makes that year different.
   - Funny tags are allowed, but keep them clear and not mean.

8. Create color palettes.
   - Each year needs named colors, hex values, and a color behavior note.
   - Palettes should be visually distinct at a glance.
   - Colors should still connect through the transition arc.

9. Deliver artifacts.
   - Enriched JSON database.
   - Design CSV.
   - Visual summary markdown.
   - Color palette SVG board.

## Current Artifact Commands

```bash
node tools/build-qq-music-database.js
node tools/export-music-design-database.js
```

If the CSV is open or locked, the exporter writes a timestamped CSV copy and still updates the visual summary and palette board.

To update only the summary and palette board:

```bash
SUMMARY_ONLY=1 node tools/export-music-design-database.js
```

On PowerShell:

```powershell
$env:SUMMARY_ONLY='1'; node tools/export-music-design-database.js
```

## Current Outputs

```text
sample-data/my-qq-music-2022-2026.json
sample-data/my-qq-music-2022-2026-design.csv
sample-data/my-music-visual-summary.md
sample-data/color-palettes.svg
```

## Website Boundary

The website should show the resulting world, hashtags, and interactions. It should not explain:

- how year differences were computed
- the backend comparison process
- lyric-analysis internals
- prompt-engineering notes
- palette-generation reasoning

Those belong in backend artifacts and design documentation.
