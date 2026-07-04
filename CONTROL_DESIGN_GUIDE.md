# Music Control Design Guide

This document describes the final reusable music control pattern used in `control.html`, `control.css`, and `control.js`. Use it as a design and implementation reference when adapting this control to another website.

## Design Intent

The control is a compact, tactile music-memory object. It should feel like a small clay hardware player: soft, dimensional, warm to touch, and emotionally specific to the selected year.

The design has three jobs:

1. Let the user switch between years.
2. Let the user browse and play a short year-specific music list.
3. Show the year artist with rotating portraits and a scrollable source-backed intro.

Keep the first screen as the actual control, not a landing page. The control should sit centered in the viewport with a little breathing room around it.

## Core Anatomy

The control has four main regions:

1. Year tabs
   - Horizontal pill selector above the controller.
   - Years are simple buttons with `data-year`.
   - Active year changes `body[data-year]`, which drives the theme.

2. Music list panel
   - Left side of the main control.
   - Shows the year title and three visible song rows.
   - Internally renders five rows: two buffer rows, previous/current/next rows.
   - The visible order is reversed like a vertical wheel: higher or next songs sit above, lower or previous songs sit below.

3. Playback panel
   - Center section.
   - Contains ECG/waveform line, current song title, play mode, previous, play, next, volume, progress, and time.
   - Uses round tactile buttons and range sliders.

4. Artist intro panel
   - Right side.
   - Contains a portrait frame and artist text.
   - Portraits rotate every 30 seconds with a crossfade.
   - Intro text comes from the artist info CSV and auto-scrolls if it overflows.

## Layout Rules

Use a single horizontal grid for desktop:

```css
.clay-control {
  display: grid;
  grid-template-columns: minmax(150px, 1.18fr) minmax(270px, 2.35fr) minmax(220px, 1.82fr);
}
```

The control is intentionally dense. Avoid adding extra cards inside it. Each panel should feel embedded into one shared clay object.

Recommended constraints:

- Keep the whole control under the first viewport.
- Keep all controls reachable without scrolling the page.
- Hide the artist intro panel below the tablet breakpoint if space is too tight.
- Use stable fixed-format dimensions for buttons, rows, sliders, and portrait frames so animation does not shift layout.

## Visual Language

The shared style uses:

- Soft clay or molded plastic surfaces.
- Inset highlights and low shadows.
- Rounded controls, but not overly pill-heavy except for year tabs and knobs.
- Slight paper or texture background through `--control-bg-image`.
- Year-specific color tokens instead of one global palette.

Core theme variables:

```css
--page-bg
--base
--base-hi
--panel
--center
--accent
--muted
--signal
--text
--ink
--active-song-text
--control-bg-image
```

Each year is defined through `body[data-year="YYYY"]`.

## Year Themes

| Year | Mood | Main Palette | Notes |
| --- | --- | --- | --- |
| 2022 | warm memory archive | tan, amber, dark coffee | Scrollbar uses light brown; center panel is dark and nostalgic. |
| 2023 | live encore stage | dark blue-black, red, warm gold | Dark mode variant; panels and text need stronger contrast. |
| 2024 | quiet room | pale green, cream, muted sage | Softer and calmer; active text is light. |
| 2025 | neon chamber | black, charcoal, hot pink | Dark mode variant with stronger glow and saturated signal. |
| 2026 | open horizon | cream, teal, soft yellow | Current default; center panel is translucent teal. |

When adding a new year, create a new `body[data-year="YYYY"]` block and define all theme variables together.

## Song List Behavior

The list is a vertical wheel, not a regular ordered list.

Important behavior:

- Dragging down advances to the next song.
- Dragging up goes to the previous song.
- The current song stays centered.
- The visual stack reads like `next / current / previous`, so a downward drag feels natural.
- Song numbers still show original track order.
- Active row has larger padding, darker clay surface, and animated bars.

Implementation anchors:

- `bindSongListDrag()`
- `getVisibleSongList()`
- `getSongListPositionClass()`
- `moveTrack(direction)`

The list supports click selection and drag selection. When dragging, suppress the accidental click after release.

## Playback Behavior

Supported play modes:

1. Shuffle
2. Single loop
3. List loop

Use icon buttons for playback mode and transport actions. The central play button should be the most visually important button in the row.

The ECG line has two modes:

- If audio is playing and analyzer data is available, it reacts to audio energy.
- If no audio is available, it still animates gently using tempo metadata so the control never feels dead.

Track tempo comes from `TEMPO_BY_TITLE`, falling back to `DEFAULT_TEMPO_BY_YEAR`.

## Artist Portrait Carousel

Use two stacked image layers:

```html
<img id="singerImage" />
<img id="singerImageNext" aria-hidden="true" />
```

Every 30 seconds, preload the next image and fade it in over 900ms.

Each image should define its own `object-position` because artist photos vary heavily. Do not rely on center crop for all portraits.

Use this structure:

```js
images: artistImageList("path/to/artist-folder", ["01.jpg", "02.jpg"], ["60% 22%", "50% 18%"])
```

Rules:

- Keep faces and upper bodies inside the narrow frame.
- Skip non-portrait or cover-art images if they do not frame the person clearly.
- Use `object-fit: cover` plus per-image `--artist-image-position`.
- Preload before fading to avoid blank frames.

## Artist Info Database

Artist text should come from:

```text
output/artist-info-source-of-truth-v1.csv
```

Expected CSV columns:

```text
Artist,CountryRegion,Role,BriefArtistIntroEnglish,BriefArtistIntroChinese,Source
```

The control uses `BriefArtistIntroEnglish` for the visible artist intro.

Because direct `file://` pages may block CSV fetches, keep fallback rows for artists shown by the control. These fallback rows should be copied from the CSV so direct local preview and local server preview match.

Lookup rules:

- Match the full artist value, such as `Lala Hsu`.
- Also support mixed names like `Chinese Name (English Name)`.
- Normalize whitespace and case for lookup keys.

## Scrollable Artist Intro

The intro area is intentionally small, so long text must be scrollable.

Behavior:

- If text overflows, auto-scroll down after a short pause.
- When it reaches the bottom, pause, reset to top, and start again.
- If the user wheels, touches, clicks, focuses, or uses keyboard scroll, pause auto-scroll for several seconds.
- Always show a slim scrollbar so manual scrolling is discoverable.

Important CSS:

```css
.singer-intro {
  min-height: 0;
  overflow-y: auto;
  scrollbar-width: thin;
}
```

The `min-height: 0` is required because the intro lives inside a flex column. Without it, the parent can clip text while the paragraph does not become a proper scroll container.

Year-specific scrollbar styling is allowed. Example: 2022 uses a light brown thumb and track.

## Data Model

Minimum year data:

```js
const YEARS = [2022, 2023, 2024, 2025, 2026];

const FALLBACK_TRACKS = {
  2026: [
    { title: "...", englishTitle: "...", artist: "..." }
  ]
};

const SINGER_INFO = {
  2026: {
    artistKey: "Artist Name",
    cn: "",
    en: "Artist Name",
    image: "fallback-image-url",
    images: artistImageList("folder", ["01.jpg"], ["50% 22%"]),
    intro: "Fallback intro"
  }
};
```

For real audio, place files in:

```text
assets/audio/YYYY music/
```

The server endpoint `/api/local-music` scans audio files and the control matches files by year folder.

## Accessibility Notes

Keep these details when reusing the control:

- Year tabs are real buttons.
- Transport controls are real buttons with `aria-label`.
- Song list buttons are clickable and keyboard reachable.
- Artist intro is focusable with `tabindex="0"` so keyboard users can scroll it.
- `audio` element remains in the DOM for browser-native media behavior.
- Empty state uses `aria-live="polite"`.

## Responsive Behavior

Desktop:

- Full three-panel control.

Below roughly 1200px:

- Hide the artist intro panel.
- Keep music list and playback panel usable.

Below narrow mobile widths:

- Stack the control vertically or reduce to the essential playback surface.
- Do not let text overlap buttons.
- Keep row and button dimensions stable.

## Reuse Checklist

When adapting this control to another website:

1. Copy the HTML structure for year tabs, music list, playback panel, artist panel, and audio element.
2. Copy the CSS theme variable pattern and create new `body[data-year]` blocks.
3. Replace `FALLBACK_TRACKS` with the new site songs.
4. Replace `SINGER_INFO` artist keys and image folders.
5. Update or replace the artist info CSV.
6. Check portrait crops and define per-image `object-position` values.
7. Verify drag direction: down should advance to the next song.
8. Verify long artist intros show a scrollbar and auto-scroll.
9. Test with no local audio files and with real audio files.
10. Test desktop and mobile widths.

## Common Pitfalls

- Do not use plain center-crop portraits; people will drift out of the narrow frame.
- Do not remove `min-height: 0` from scrollable flex children.
- Do not let the list render as normal `1, 2, 3, 4` top-to-bottom if the intended gesture is dragging down first.
- Do not make the artist panel a separate floating card; it should feel embedded in the clay control.
- Do not depend only on remote images. Keep local images or graceful fallbacks.
- Do not rely on the local API when opening the page directly as `file://`; provide fallback data.

## File Map

```text
control.html
  Structural markup for the control.

control.css
  Visual system, themes, layout, scrollbars, portrait frame, responsive behavior.

control.js
  Year switching, song list rendering, drag behavior, audio playback, ECG animation,
  artist CSV loading, portrait carousel, and intro auto-scroll.

output/artist-info-source-of-truth-v1.csv
  Source-of-truth artist intro database.

output/artist-image-downloads-v1/
  Local artist portrait folders.

assets/control-backgrounds/
  Year-specific control background textures.
```

