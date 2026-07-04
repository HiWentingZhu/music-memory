# Zoom-In Space Visual Rules

Use this document whenever designing, generating, or implementing the zoom-in view for a selected yearly space.

The overview rules remain in `VISUAL_RULES.md`. This document only covers the detailed single-year space after the user clicks one fan-sector room.

## Core Purpose

The zoom-in space is the detailed interactive showroom for one year of a user's music DNA.

It should show:

- the selected year's scene
- interactive music controller
- yearly album/singer wall
- yearly music-type wall
- active listening days
- most common listening time in a day
- character interaction
- ritual objects
- mood/data installations
- hashtag personas

The zoom-in space should feel like entering one yearly album showroom from the larger fan-shaped museum.

## Geometry And Style

Follow the locked visual style:

- polished miniature 3D music showroom
- cinematic isometric cutaway view
- fan-shaped floor plan
- curved front edge
- curved back wall
- angled side boundaries
- same camera distance, room footprint, wall height, floor depth, and front-console footprint across all yearly zoom-in spaces
- dark neutral product-render background
- premium soft lighting
- glass/acrylic/wood/metal/paper material quality
- clean but detailed visual density
- same soft rounded 3D collectible character style as the overview

Do not make the zoom-in view a flat dashboard. All data should become spatial objects, displays, walls, plaques, lights, or controls inside the showroom.

## Scale Consistency

All yearly zoom-in spaces must feel like equal-size sibling rooms from the same fan-shaped museum.

Keep consistent across years:

- room footprint and overall visual size
- curved front edge width
- curved back wall height and radius
- side boundary angle
- controller footprint and placement along the front edge
- camera distance and isometric angle
- amount of empty margin around the outside shell

Do not make one year feel like a larger room, a smaller diorama, a closer crop, a taller wall, or a wider stage just because its music DNA is denser or quieter. Express yearly differences through interior objects, materials, lighting, wall density, and motion cues while preserving the same room scale.

## Controller

The controller appears only in the zoom-in space.

It should be integrated into the curved front edge of the fan sector, like a physical console built into the architecture.

Required controller functions:

- **Year:** selected year control or year dial.
- **Space Name:** name/title of the yearly space.
- **Now Playing Screen:** display the current music name, duration, and play progress.
- **Volume Adjustment:** volume knob, slider, or dial.
- **Change Songs:** next/previous song control, track selector, or album-disc control.
- **Albums From The Wall:** selector or focus control for the artist and music-type albums shown on the wall.
- **Hashtag Personas:** visible yearly harshtag/persona chips from that year's visual summary.

Controller visual form may include:

- play/pause button
- small screen with song title, duration, and progress bar
- current album cover display in the former vinyl/disc section
- year dial
- volume knob
- song skip buttons
- wall-album selector
- hashtag persona chips
- small hotspot lights

The controller should feel tactile, premium, and physical, not like a flat overlay.

Required controller left-to-right layout:

1. Year block or year dial
2. Volume change control
3. Now-playing screen with song name, singer/artist name, and play progress
4. Transport controls with exactly three grouped buttons: previous, pause/play, next
5. Song list in the current album
6. Current album cover/control

The screen should use a progress bar, ring, or timeline for progress. Do not use an ECG-like or waveform-style controller panel; the former waveform area should become the grouped transport section.

Controller harshtag rules:

- show the exact harshtags listed for the selected year in `sample-data/my-music-visual-summary.md`
- do not invent replacement hashtags when the year already has generated harshtags
- keep the chips on or immediately attached to the physical controller
- use short chip labels; avoid filling the 3D scene walls with hashtags

Controller screen rules:

- include a visible now-playing screen on the controller
- show the current music name
- show the current singer/artist name
- show the duration
- show play progress as a bar, ring, or timeline
- the screen can use short readable text, but it should not dominate the room
- keep the screen embedded in the controller, not floating as a UI overlay

Controller album-switching rules:

- the controller must let the user switch the current album/focus group
- albums are the top artists and music types shown on the walls
- selecting an artist album shows the songs by that artist
- selecting a music-type album shows songs in that music type
- the former vinyl/disc section should display the current album cover or current artist/type cover art, not a generic vinyl record
- the album-wall selector area should show the music list for the current album/focus group
- keep `pause`, `previous`, and `next` buttons together in one transport-control section
- do not scatter transport buttons across the controller
- do not include a separate `Live Take` section in the controller
- do not show any ECG/waveform-style controller area; represent progress with a simple bar, ring, or timeline instead

## Wall Data Displays

The curved back wall and side walls are the main data display surfaces.

### Wall Layout Diversity

Do not reuse the same rectangular portrait-grid wall layout for every year.

Every yearly zoom-in should keep the same wall footprint and data rules, but vary how the wall displays are composed:

- 2022 can use an archive salon layout with shelves, drawers, catalog labels, staggered frames, and file-card genre tabs.
- 2023 can use a rehearsal/live wall with pinned posters, cable-suspended frames, marquee strips, and amplifier-rack genre plaques.
- 2024 can use a sparse folding-screen or rice-paper-panel layout with fewer, calmer album panels and soft fabric genre tags.
- 2025 can use a diagonal neon club-flyer layout with layered acrylic tiles, LED rails, and stacked light-box genre modules.
- 2026 can use an open horizon display with floating records, postcard rails, suspended frames, and sea-glass wayfinding genre signs.

Wall diversity must come from composition, mounting method, depth, materials, and rhythm, not from adding extra artist/type tiles. The item limits still apply: max 10 artists and max 10 music types.

### Top Singer Albums Wall

Show a maximum of 10 album/display tiles representing the **top 10 singers/artists with the most songs in that year**.

Rules:

- maximum 10 items
- if the year has fewer than 10 artists, show only the exact number of artists that exist in that year
- do not add placeholder, decorative, duplicate, or filler artist tiles to reach 10
- ranked visually by size, placement, glow, or ordering
- each item should use the real top singer/artist portrait or headshot image from the music data or from an online source when an authorized or acceptable reference image URL/file is available
- if a reliable artist portrait/headshot image cannot be found, use that artist's official or recognizable logo as the tile image
- wall labels for artist tiles must show only the artist's English display name or accepted romanized/stage name; do not show Chinese, Korean, or mixed-language artist names on the wall
- artist image references must be checked before use; confirm the artist identity, gender/presentation, and whether the tile is a solo artist, group, choir, band, or duet/collaboration
- if no verified artist image or logo is available, or if the online result is ambiguous, use a labeled album-like card or symbolic tile instead of inventing a face
- each item can look like a wall painting, album cover, framed disc, portrait tile, or collectible card
- use real labels in UI if needed, but avoid cluttering the 3D wall with lots of readable text
- do not invent a fake real-person portrait and present it as the actual singer
- do not show a solo-person portrait for a band, choir, group, or collaboration tile unless the data/source identifies that specific person
- do not swap gender/presentation; when uncertain, avoid a human portrait
- online artist images should be used as wall tile references only; do not turn the whole room into a celebrity collage

### Music Type Albums Wall

Show a maximum of 10 album/display tiles representing the **top 10 music types/genres/tags in that year**.

Rules:

- maximum 10 items
- if the year has fewer than 10 music types, show only the exact number of music types that exist in that year
- do not add placeholder, decorative, duplicate, or filler music-type tiles to reach 10
- visual style can differ from singer wall, but must still belong to the same room
- can appear as color/material swatches, album-cover-like cards, vinyl labels, wall tiles, or genre plaques
- music type should affect material, light, and object style, not only color

### Active Listening Days

Show how many days in the year had active listening.

This should appear on the wall as a clear numeric plaque only.

Required form:

- show only the active listening day count
- do not render a full calendar grid, day-by-day tiles, 365 dots, or decorative date cards
- keep the numeric display readable in the wall-data layer
- if active listening day data is unavailable, placeholder-derived, or not present in the source data, do not show active listening days on the wall at all

### Total Music Count

Show the total number of music entries for that year on the wall.

Required form:

- show a clear numeric plaque or counter for total music
- place it near the active-days plaque or wall-data cluster
- keep this display separate from artist tiles and music-type tiles
- do not use the total count as a reason to add more wall tiles

### Most Common Listening Time

Show the user's most common listening time in a day: `most listened time of day`.

This can be represented as:

- clock object
- light beam angle
- sun/moon window state
- 24-hour ring
- timeline strip
- desk clock
- wall clock
- sky color or lighting cue

Use the Chinese concept `最常听歌时间` as a product meaning, but avoid filling the scene with readable Chinese labels unless needed in the actual UI layer.

### Weather And Time-Of-Day Diversity

Vary the outdoor/weather cue and time-of-day lighting across yearly zoom-in spaces while keeping the same room scale and camera.

Use weather and time as data atmosphere:

- 2022: rainy late evening or night, blue rain window plus warm archive lamp.
- 2023: smoky after-show night, indoor haze, spotlight beams, darker exterior.
- 2024: misty dawn or quiet morning, soft fogged window, candle/lamp warmth.
- 2025: electric late night, city-light glow or dry neon air, high-contrast club energy.
- 2026: open golden hour or breezy late afternoon, clear sky/sea-glass light, airy horizon.

Avoid making all years rainy, all years night, or all years warm indoor light. The weather/time cue should be visible through windows, wall openings, light direction, shadows, props, and sky color.

## Character

The character represents the same user across years.

Use the character designs in `C:\Users\zhuwt\OneDrive\000 - Side Projects\01 - Music\output\characters` as the required character reference source.

Current character reference files:

- `character-2022-rain-archive-amber.png`
- `character-2023-smoky-rehearsal-stage.png`
- `character-2024-quiet-reconciliation-corrected.png`
- `character-2025-neon-kinetic-charge.png`
- `character-2026-open-horizon-freedom.png`

In zoom-in:

- character should be smaller than the main room objects
- character should be about one-third smaller than earlier large zoom-in drafts, roughly two-thirds of the prior character height
- character-to-room scale ratio should stay consistent across years
- character height should occupy the same approximate percentage of the room height and floor depth in every yearly zoom-in
- character should not stand statically in the center
- character placement should vary by year across left, center, right, foreground, and back-wall interaction zones; do not place the character on the right side in every yearly space
- no stage, pedestal, display block, or circular platform under the character
- character should actively interact with room elements
- outfit/accessories/pose should reflect that year's music DNA
- character should have a friendly clay-like 3D figure quality with simplified facial features and rounded proportions
- preserve the referenced character's base face, hair/body logic, proportions, and year-specific outfit/accessory language; do not redesign the character from scratch

Good actions:

- adjusting the controller
- selecting a song
- touching the active-listening calendar wall
- arranging top singer album tiles
- pulling a record from a shelf
- selecting or inspecting albums from the wall
- pinning hashtag persona stickers
- looking toward the most-listened-time clock/window

## Hashtag Personas

Hashtag personas are part of the zoom-in controller and can also appear as stickers/posters inside the room.

Examples:

- `#MidnightLooper`
- `#ComfortRepeater`
- `#GenreWanderer`
- `#HighEnergyEscape`
- `#FocusArchivist`
- `#SoftDramaMain`

They should be data-backed, not random decoration.

Visual forms:

- sticker strips
- small posters
- badge chips on controller
- projected labels
- pinned notes
- light-up tags

## Music DNA Mapping

The zoom-in space should be more data-rich than the overview, but still not cluttered.

Use music DNA to influence:

- scene type
- lighting
- material
- album wall density
- active-day installation density
- controller state
- character outfit and action
- ritual objects
- animation/motion

Examples:

- Late-night year: controller glows softly, most-listened-time clock points to night, window moonlight, character adjusts lamp/headphones.
- High-energy year: waveform strip is brighter, records spin faster, character adjusts volume or lights.
- Nostalgia year: active days shown as paper date cards, archive boxes, warm lighting.
- Discovery year: music types appear as map fragments or portal cards.
- Repetition year: same singer wall has repeated motifs and orbiting discs.
- Genre-diverse year: music type wall uses mixed materials and layered display tiles.

## Motion And Interaction

The zoom-in space should feel alive.

For the website implementation, zoom-in spaces should be built from separate movable image layers rather than one flattened background or large cropped screenshot chunks. At minimum, keep the room shell, weather/window, each artist tile, each music-type tile, major props, character, and each controller section as independently positioned image assets so the user can drag or animate them.

Animate or imply:

- controller waveform
- spinning album/disc
- glowing active-day calendar tiles
- wall-album selector
- album wall hover states
- character idle interaction
- light changes based on selected song/type
- hashtag persona filter changes

Motion should be subtle and premium, not noisy.

## Do Not Do

- Do not show the controller in overview.
- Do not make the zoom-in view a flat dashboard.
- Do not exceed 10 singer/artist wall items.
- Do not exceed 10 music-type wall items.
- Do not use unauthorized artist images; use provided/licensed image URLs or fallback symbolic tiles.
- Do not use a stage or pedestal for the character.
- Do not place the character statically in the center.
- Do not use only color to represent music types.
- Do not overcrowd the wall with readable text.
- Do not overuse bright dots, sparkles, or particle noise.

## Short Prompt Anchor

When creating zoom-in visuals, start from this:

> A selected yearly fan-sector music showroom zoomed in, polished miniature 3D diorama style, dreamy pastel lighting where appropriate, curved controller console at the front with year/name/volume/song/wall-album/persona controls, curved walls showing max 10 top singer album tiles, max 10 top music-type tiles, active listening days installation, most-listened-time clock or light cue, same small soft rounded 3D collectible character interacting with the data objects, no stage, clean but detailed.

Scale addendum: keep the zoomed room size, camera distance, controller footprint, and character-to-room ratio consistent across all years. Use the matching year character reference from `output/characters`.
