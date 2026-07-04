# Music Personality World

An interactive local prototype that turns QQ Music-shaped listening data into:

- a generated music personality figure
- data-backed persona hashtags
- yearly figure transformations
- personal album-cover timeline
- mood calendar
- listening rituals
- public-safe share reports
- opt-in gallery cards
- a persistent local listening database with search and export

## Run

Open `index.html` in a browser, or serve the folder locally.
For QQ Music playlist-link imports, run the local server so the app can call QQ
Music with the required referrer:

```powershell
.\start-music-site.ps1
```

If Node.js is already installed and available on your path, this also works:

```bash
node server.js
```

Then open `http://127.0.0.1:8765/`.

## Local Music Playback

Supported formats are `.mp3`, `.m4a`, `.wav`, `.ogg`, `.flac`, `.aac`, and `.opus`.

To let zoom-in room pages play music, put audio files directly in:

```text
assets/audio
```

Direct files in `assets/audio` appear in every zoom-in space. For year-specific
room music, use folders such as `assets/audio/2026 music/`.

To let the homepage player play music, put files in `assets/audio/homepage music/`.

After adding files, restart the local server. The app scans `assets/audio` and
uses the song title and artist from the filename where possible. Browsers require
a click before audible playback starts, so the music begins when the user presses
play or selects a playable song.

If you open `index.html` directly as a `file://` page, the app uses
`assets/audio/manifest.js` instead of the server scanner. Regenerate it after
audio changes:

```bash
npm run build:audio
```

Every open or refresh starts with sound off and shows the sound reminder. Choosing
`Turn sound on` in that reminder starts the homepage music. After that, the
`Sound on/off` toggle only mutes or unmutes site sound; play, pause, previous,
and next stay controlled by the music transport.

The website starts with a safe "Connect QQ Music" flow:

1. Open QQ Music and log in yourself.
2. Bring data back by upload, pasted copied rows, or annual report details.
   Public QQ Music playlist links and numeric playlist IDs can also be imported
   through the QQ Music API endpoint pattern documented by
   [`copws/qq-music-api`](https://github.com/copws/qq-music-api).
3. Generate the music personality world locally in the browser.

The prototype includes sample data and accepts JSON, CSV, pasted rows, or manual annual-report chapters with these fields:

```text
source, played_at/year, track_title, artist_name, album_name, duration_ms, play_count, genre_or_tags
```

The local account, saved listening database, share reports, and gallery cards are stored in browser `localStorage`.
Imported rows are merged into the local database and deduplicated by source, date/year, song, artist, and album.

## Personal QQ Music Database

Generated database:

```text
sample-data/my-qq-music-2022-2026.json
```

Design-facing exports:

```text
sample-data/my-qq-music-2022-2026-design.csv
sample-data/my-music-visual-summary.md
sample-data/color-palettes.svg
```

Source playlists:

```text
2022: 8535705502
2023: 8565876295
2024: 8989911780
2025: 9183390267
2026: 9497585558
```

The generated file contains 2,154 playlist entries with normalized website rows,
QQ song/artist/album IDs, source playlist metadata, lyric-derived themes and
keywords, inferred music type, mood/energy tags, QQ song URLs, album art URLs,
and review-search context. Full lyrics are not stored; the generator only stores
derived lyric analysis.

To regenerate it:

```bash
node tools/build-qq-music-database.js
node tools/export-music-design-database.js
```

For the required repeatable processing flow, see `MUSIC_DATABASE_WORKFLOW.md`.

QQ public song review/comment data was not available through unauthenticated web
endpoints during generation, so rows include a `review_status` and search query
instead of scraped review text.
