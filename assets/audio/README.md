# Local Music Library

Use these folders to control where music appears:

```text
assets/audio/homepage music/
assets/audio/2022 music/
assets/audio/2023 music/
assets/audio/2024 music/
assets/audio/2025 music/
assets/audio/2026 music/
```

Put homepage music in `assets/audio/homepage music/`. The homepage controller shuffles and plays music from this folder.

Generated MP3 web copies live separately in:

```text
assets/audio-mp3
```

Keep FLAC/source files in `assets/audio/`; use `npm run convert:mp3` to create matching MP3 files in `assets/audio-mp3/`.

Supported formats: `.mp3`, `.m4a`, `.wav`, `.ogg`, `.flac`, `.aac`, `.opus`.

The local server scans this folder and nested folders at `/api/local-music`.
File names that include the song title and/or artist are matched to repeated songs.

When opening `index.html` directly as a `file://` page, browsers cannot scan this
folder. The page falls back to `assets/audio/manifest.js`. After adding or
removing audio files, regenerate that manifest:

```powershell
node tools/build-audio-manifest.js
```

For zoom-in room music, you can start by putting files directly in `assets/audio/`:

```text
assets/audio/Artist - Song.flac
```

Files placed directly in `assets/audio/` appear in every zoom-in room, which is useful while testing.

When you want each year to have its own room soundtrack, put files inside year folders:

```text
assets/audio/2024 music/Artist - Song.flac
assets/audio/2025 music/Artist - Song.mp3
```

Room pages show direct `assets/audio/` songs plus songs from their matching year music folder. The homepage controller only uses files in `homepage music/`.
