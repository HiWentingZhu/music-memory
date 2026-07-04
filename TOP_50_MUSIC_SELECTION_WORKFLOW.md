# Top 50 Music Selection Workflow

Use this document whenever a new music database is provided and each year needs a final set of 50 songs for the music intro / yearly music world.

The goal is not only to choose the most-played songs. The final 50 for each year should represent that year's listening identity, visual room style, and emotional transition in the five-year arc.

## Required Input

Use the enriched design database CSV as the main source.

Required fields:

- `year`
- `track_title`
- `artist_name`
- `album_name`
- `track_order`
- `play_count`
- `music_type_primary`
- `music_type_traits`
- `lyric_theme_tags`
- `lyric_mood`
- `lyric_energy`
- `appears_in_years`

If the database also has a visual summary file, use it to confirm each year's style, space name, dominant moods, themes, and music types.

## Output Files

Create two files:

- `output/top-50-songs-by-year-style-theme-revised.csv`
- `output/top-50-songs-by-year-style-theme-revised.md`

If a previous version exists and the selection changes materially, create a new versioned file instead, such as:

- `output/top-50-songs-by-year-style-theme-revised-v2.csv`
- `output/top-50-songs-by-year-style-theme-revised-v2.md`

## Core Selection Rule

Select exactly 50 songs for each year.

Rank songs within each year only. Do not rank all years together.

The base score should balance:

- Listening strength: `play_count`
- Year style fit: mood, theme, type, and energy
- Memory loop value: whether the song appears across multiple years
- Playlist priority: earlier `track_order` wins close ties

Suggested base weighting:

```text
listening strength: 40-45%
style/theme fit: 35-45%
cross-year memory: 5-10%
playlist priority: 5-10%
```

This means a lower-play song can be selected if it strongly defines the year's emotional or visual identity, but very low-signal songs should not replace strong anchors without a clear reason.

## Duplicate Rules

Remove duplicates inside the same year.

Check both:

- Exact duplicate: same `track_title` + same `artist_name`
- Variant duplicate: same core song with labels removed

When checking variant duplicates, normalize titles by removing labels such as:

- `(Live)`
- pure-song / vocal-only version labels
- `(Single Version)`
- `(Soundtrack Version)`
- `(Explicit)`
- `(Outtake)`
- brackets, punctuation, and extra whitespace

Examples of same-year variant repeats to avoid:

- a studio version and a live version of the same song
- a regular version and a pure-song / vocal-only version of the same song

If two variants appear, keep the one that best fits the year's style. If both fit similarly, keep the higher `play_count`; if still tied, keep the earlier `track_order`.

## Year Style Profiles

Use the latest visual summary to refresh these profiles when the database changes. For the current 2022-2026 arc, use:

### 2022 - Rain Archive

Identity: dense private archive, rainy memory, catalog foundation.

Prioritize:

- melancholic, healing, nostalgic, reflective
- memory, heartbreak, healing, city-night, love, growth
- pop, OST, live
- low or medium energy
- songs that feel like archive drawers, old tickets, rain-window listening, and repeated memory loops

### 2023 - Encore Stage

Identity: live/rehearsal bridge, softer stage light, slow memories, fewer deep-beat moments.

Prioritize:

- healing, nostalgic, reflective, melancholic, bright
- memory, healing, love, growth, city-night, heartbreak
- live, playlist-pop, OST, rock
- low or medium energy
- soft live performances, warm stage-memory songs, nostalgic callbacks

Reduce:

- too many high-energy songs
- deep beat / heavy groove songs
- hip-hop, electronic, and R&B unless kept intentionally as a small accent

Keep only a few stage peaks so the year still has performance shape.

### 2024 - Quiet Reconcile

Identity: solitude, repair, soft self-facing reconciliation.

Prioritize:

- healing, reflective, melancholic, aspirational
- healing, growth, personal, memory, love, heartbreak
- playlist-pop, live, OST
- low or medium energy
- songs that feel like folded notes, repair lines, quiet rooms, and making peace

### 2025 - Neon Chamber

Identity: kinetic neon charge, English/K-pop/dance-pop edge, emotional release, bright motion.

Prioritize:

- energetic, aspirational, reflective, sharp melancholic
- energy, city-night, growth, personal, love
- playlist-pop, live, OST, hip-hop, R&B
- high or medium energy
- English tracks, K-pop, dance-pop, club-motion songs, glossy high-contrast songs

Reduce:

- low-energy songs
- very soft, light, slow, or overly sensitive ballads
- too many quiet healing songs

For the current direction, 2025 should have no low-energy songs unless the user explicitly asks for a softer version.

### 2026 - Horizon Deck

Identity: open horizon, freedom, nostalgic return, airy live-memory hero songs.

Prioritize:

- nostalgic, melancholic, healing, aspirational, energetic
- memory, healing, growth, love, heartbreak, energy, city-night
- playlist-pop, live, OST, rock
- medium energy first, with some low/high contrast
- songs that feel open-air, free, live-version nostalgic, and horizon-facing

## Manual Taste Adjustments

After the first algorithmic selection, review each year by ear/style logic.

Ask:

- Does this year sound different from the previous year?
- Are there too many songs with the same mood?
- Are there too many slow songs or too many beat-heavy songs?
- Does the list match the visual room?
- Are the first 10 songs strong enough to introduce the year?
- Are repeated-year songs meaningful memory loops, not accidental duplication?

Manual swaps are allowed when the user gives a direction, such as:

- "Add more English/K-pop for 2025."
- "Remove slow/light/sensitive music from 2025."
- "For 2023, add slow/light music and reduce deep beat music."

Record manual choices in the `SelectionReason` column.

## Validation Checklist

Before finalizing:

- Each year has exactly 50 songs.
- No exact same-year duplicates.
- No same-year variant duplicates.
- Every selected song has a clear reason.
- 2025 follows the latest user direction: more English/K-pop/high-energy, fewer soft low-energy songs.
- 2023 follows the latest user direction: more slow/light stage-memory songs, fewer deep beat songs.
- The final Markdown and CSV match each other.

## Final Explanation

When presenting the result, summarize:

- where the output files are
- the high-level selection logic
- any important manual tuning
- duplicate validation result
- quick energy or mood mix for years that were adjusted

Do not describe the list as an objective public music chart. It is a personal yearly music-world selection based on the database and the intended intro story.
