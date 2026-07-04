# Full App Deployment

This project should be deployed as a Node web service when you want the API routes in `server.js` to work.

## Recommended Host: Render

1. Put this project in a GitHub repository.
2. In Render, create a new Blueprint or Web Service from that repository.
3. If using a manual Web Service setup, use:
   - Build command: `npm install`
   - Start command: `npm start`
   - Runtime: Node
4. Render will provide the public URL after the first successful deploy.

The app reads the host port from `PORT`, so cloud hosts can route traffic correctly.

## Before Publishing

- Remove personal data, private exports, and raw listening history you do not want public.
- Keep local audio files out of Git unless you own the rights to every file and want the hosted app to serve them.
- Add public/approved hosted tracks to `remote-audio.json` when the deployed app should play music from external URLs.
- Test the deployed URL's `/api/local-music` route. It should return JSON.
- Test the homepage and a room page from the deployed URL.

## Remote Audio

The deployed app first asks `/api/local-music` for audio files. If the host has no local audio files, it loads `remote-audio.json`.

Each entry needs:

- `name`: file-style display name, usually `Artist - Song title.mp3`
- `path`: placement in the app, such as `homepage music/Artist - Song title.mp3` or `2026 music/Artist - Song title.mp3`
- `url`: a direct playable/download URL

Use `remote-audio.example.json` as the template. A normal OneDrive sharing page link may not be enough; the browser needs a URL that the audio element can actually play.

## MP3 Copies

For web playback, keep the original FLAC files in `assets/audio/` and create MP3 copies in `assets/audio-mp3/`:

```bash
npm run convert:mp3
```

This requires `ffmpeg`. The script skips MP3s that already exist, preserves the folder structure, and never removes the source files. Useful options:

```bash
npm run convert:mp3 -- --dry-run
npm run convert:mp3 -- --folder "homepage music" --limit 5
npm run convert:mp3 -- --bitrate 160k
npm run convert:mp3 -- --output-root "assets/audio-mp3"
```

The local server scans both `assets/audio-mp3/` and `assets/audio/`. When both `Song.flac` and `Song.mp3` exist for the same logical track, the app prefers the MP3 for playback.

## Local Development

Run:

```bash
npm start
```

Then open:

```text
http://127.0.0.1:8765/
```
