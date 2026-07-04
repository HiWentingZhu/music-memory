# Music Personality World Visual Rules

Use this document as the source of truth whenever working on visuals, image prompts, interface direction, 3D scenes, or showroom concepts for Music Personality World.

## Core Concept

The product is a personal music museum generated from a user's yearly music DNA.

After a user imports music data, they see yearly spaces arranged together as a fan-shaped collection of separate 3D modules. Each year is one fan-sector space. Show a maximum of five equal-size spaces at a time so every sector stays wide, balanced, and readable. Clicking a year zooms into that year's space, where the user can explore details and interact with music controls.

The experience should feel like:

- miniature 3D diorama
- album showroom
- music memory museum
- personal data portrait
- cinematic collectible scene

It should not feel like a dashboard, normal stats page, generic Spotify Wrapped clone, or static gallery.

## Visual Style

Follow the supplied reference image style:

- polished miniature 3D diorama
- cinematic isometric cutaway view
- premium lighting with soft glow and shadows
- detailed walls, props, album objects, music artifacts
- collectible music-room feeling
- rich but tasteful materials: glass, acrylic, paper, wood, metal, light panels, fabric
- small stylized human character with a soft rounded 3D collectible figure quality
- character should feel friendly, clay-like, and approachable, with simplified facial features, expressive proportions, clothing detail, hair shape, and personality
- realistic enough to feel spatial, stylized enough to feel magical

Do not copy the exact colors, typography, character, or layout from the reference. Borrow the spatial quality, lighting quality, level of detail, and music-room atmosphere.

Current visual lock:

- the entire overview visual should use a soft 3D / clay element style: rounded forms, matte or satin surfaces, tactile toy-like props, gentle shadows, and softened edges
- for the 2022-2026 overview, use `sample-data/color-palettes.svg` and `sample-data/my-music-visual-summary.md` as the source of truth for color and space design
- use the exact yearly palette logic from the source files, but render dark or high-contrast colors as controlled accents so the full overview still feels clean, airy, and softly dimensional
- use the supplied three-showroom reference as the strongest style source
- preserve its miniature showroom structure, cinematic lighting, material finish, room density, and album-wall language
- shift the atmosphere toward dreamy pastel sky/cloud colors: soft peach, warm cream, pale cyan, airy blue, lavender-shadow accents, and gentle sunrise/sunset gradients
- prefer a slightly lighter overall color value: more airy whites, pale blues, soft peach light, and less heavy dark contrast
- when no data palette is supplied, restrict the main color system to light milky pastels: milky pink, milky yellow, milky blue, milky green, and milky purple
- use white/cream only as neutral light and surface support
- use the newer cloud-world references for scene color and element styling: floating ivory rock forms, soft cloud fields, translucent glass HUD panels, rounded white borders, very sparse thin cyan interface lines, and luminous pastel atmosphere
- keep those HUD-like details abstract and non-readable inside the 3D scene; use real readable text only in the website UI layer
- keep the overview very clean: minimal light effects, minimal dots, no dense sparkle texture, no busy particle fields
- keep contrast and data-driven scene differences, but avoid harsh dark-heavy rooms unless the music DNA clearly requires it
- when exploring new directions, do not invent a totally new palette or scene language
- adapt the existing reference language into the fan-shaped geometry
- add new yearly spaces as siblings of the existing three spaces, not as a different visual universe

## Fan-Shaped Geometry

Every yearly space uses a fan-shaped floor plan, not a square room.

Required geometry:

- floor plan resembles a folding fan sector
- use one repeated fan-sector template cloned five times
- do not scale, stretch, crop, taper, or visually enlarge individual sectors in the overview
- each sector uses the exact same size, same footprint, same arc width, same depth, and same visual weight
- each sector is wide enough to hold a full miniature scene, not a narrow slice
- smooth curved outer back edge
- outer back edge must read as one uninterrupted circular fan arc across all five spaces, not five separate room caps stitched together
- sector dividers may touch the outer arc, but they should not create kinks, corners, or height breaks in the outer silhouette
- smooth curved front edge
- angled side boundaries
- all yearly spaces sit side-by-side along one shared fan arc, but they are not physically linked together
- keep small, consistent gaps between sectors so each space reads as its own collectible module
- each sector's back curve and front curve should align to the same larger fan geometry
- the overview should read as one curated fan-shaped collection, not a fused single shell and not random disconnected boxes
- show no more than five connected sectors in the main overview

Avoid:

- square rooms
- random disconnected pods with no shared fan alignment
- jagged front curves
- front railings, fences, barriers, or guardrails in the overview

## Overview State

The overview appears after music data is uploaded/imported.

It should show:

- all yearly fan-sector spaces arranged together
- separate fan-sector modules aligned along one smooth fan-shaped arc
- each yearly module should be exported and rendered as its own independent website layer/asset, not baked into one flattened overview image
- each module must have its own clickable hit area so selecting it can open that year's zoom-in space
- each module can receive independent browser-side lighting, hover lift, focus state, and motion
- maximum five visible spaces
- all visible spaces use the exact same size and identical fan-sector footprint
- spaces are cleaner and less crowded than zoomed-in views
- different scene designs for different years
- no front music controller
- no front railing or barrier
- clear clickability through visual focus, hover, glow, scale, or selection state

The overview is for browsing years, not inspecting every detail.

Overview density should be restrained. Show enough objects to communicate each year's music DNA, but avoid filling every surface. Save dense album walls, detailed labels, tracklists, and many small props for the zoom-in state.

Do not add any visual connection between overview modules. Avoid continuous lines, ribbons, cables, waveforms, routes, light paths, rails, bridges, or other elements that link one space to another. Each space can contain its own local music-related lines or objects, but they must stop inside that module and must not align into a cross-room connection.

Website implementation rule: use separate transparent PNG/WebP or true 3D/canvas objects for the overview spaces. The background should be a separate image/layer. Do not use one full composite overview image as the only interactive element, because the user needs to click, animate, light, and zoom each yearly space independently.

Clickable hit areas should follow each space silhouette, not the rectangular PNG bounds. Use CSS `clip-path`, SVG hit regions, canvas picking, or real 3D object picking so hover, focus, and click behavior feels attached to the fan-sector space edge.

## Zoom-In State

When a user clicks a yearly space, the selected fan-sector space zooms in.

The zoomed-in rooms must keep the same base scale across all years. Use the same room footprint, curved shell size, wall height, floor depth, front-edge controller footprint, camera distance, and isometric angle for every yearly zoom-in. A dense year can contain more objects and a quiet year can contain more negative space, but the room itself should not become larger, smaller, closer, farther away, taller, or wider than the others.

The zoomed view should show:

- richer detail
- interactive elements
- album covers
- wall-data plaques for active listening days and total music count
- listening ritual objects
- hashtag stickers/posters
- tracklist plaque
- curator note object
- year's character version
- foreground music controller

The music controller appears only in the zoomed-in state.

Website implementation rule:

- zoom-in spaces should be rendered as separate movable animated image layers, not one flattened bitmap
- keep at least these layers independently addressable as separate asset files: room shell, weather/window, each artist tile, each music-type tile, major props, character, and each controller section
- window placement, wall composition, and weather animation should vary by year

Zoomed wall-data rules:

- top artist wall shows a maximum of 10 artists
- if a year has fewer than 10 artists, show only the exact number of artists in that year
- do not add placeholder, duplicate, or filler artist tiles
- use an artist portrait/headshot image for each top artist tile when an authorized or acceptable source is available
- if a reliable artist portrait/headshot image cannot be found, use the artist's official or recognizable logo as the tile image
- artist tile labels must use only English display names or accepted romanized/stage names; do not show Chinese, Korean, or mixed-language artist names on the wall
- verify artist image references before use; if the artist identity or gender/presentation is uncertain and no reliable logo is available, use a labeled album-like card or symbolic tile instead of inventing a human portrait
- do not show solo portraits for bands, choirs, groups, or collaborations unless the source identifies the person shown
- top music-type wall shows a maximum of 10 music types
- if a year has fewer than 10 music types, show only the exact number of music types in that year
- do not add placeholder, duplicate, or filler type tiles
- active listening days should appear as a number-only wall plaque, not a calendar grid or decorative date installation
- if active listening day data is unavailable, placeholder-derived, or missing from the source data, omit active listening days entirely
- total music count should appear as a separate numeric wall plaque or counter
- vary wall display composition across years: archive shelves/drawers, pinned rehearsal posters, sparse rice-paper panels, diagonal neon flyer clusters, and open-horizon suspended frames should not collapse into the same repeated portrait grid
- wall diversity must change mounting method, depth, rhythm, materials, and placement while preserving the same max-10 data caps

## Music Controller

The controller is the main interaction anchor after zoom-in.

It should be integrated into the front edge of the selected fan space, like part of the architecture or display console.

It may include:

- play/pause button
- timeline slider
- volume knob
- year dial
- album-disc control
- mood/scene toggles
- detail hotspots
- yearly harshtag/persona chips from `sample-data/my-music-visual-summary.md`

Controller constraints:

- controller sections must read left to right: year, volume change, now-playing screen with song name/singer/progress, transport controls, song list, current album
- do not include a separate `Live Take` section
- do not show an ECG-like or waveform visualization area; use the former waveform area for the grouped transport controls
- embedded now-playing screen with music name, singer/artist name, duration, and play progress

Do not show the controller in the overview.

Controller content rules:

- show the exact harshtags generated for the selected year
- place harshtags as tactile chips on or immediately attached to the controller
- include a controller screen showing current music name, duration, and play progress
- keep the screen embedded in the physical controller, not as a floating overlay
- controller can switch the current album/focus group between wall artists and wall music types
- the former vinyl/disc section should show the current album/artist/type cover, not a generic vinyl record
- `pause`, `previous`, and `next` must sit together in one transport-control section
- the album-wall selector area should show the music list for the currently selected artist/type album

Character scale and placement rules:

- the zoom-in character should be about one-third smaller than earlier large drafts, roughly two-thirds of the prior height
- vary character placement across years; use left, center, right, foreground, and back-wall interaction zones instead of always placing the character on the right

## Scene Design And Music DNA

Each yearly space is generated from that year's music DNA. It does not need a fixed color theme per space. The full scene design should respond to the data.

Music DNA can affect:

- scene type
- lighting
- weather
- time of day
- materials
- density of objects
- motion behavior
- character outfit/accessories
- album wall arrangement
- mood calendar form
- ritual objects
- spatial openness or enclosure

Examples:

- Late-night listening: moonlit window, lamp glow, darker atmosphere, quiet objects, soft floating lights.
- High energy: bright kinetic lighting, sound-wave paths, club-like objects, sharper geometry, active movement.
- Nostalgia: archive boxes, warm paper textures, old posters, diary objects, faded light.
- Discovery: maps, portals, travel fragments, open doors, floating postcards, scattered new objects.
- Repetition: looping record rings, repeated frames, orbiting objects, circular motifs.
- Genre diversity: collage walls, mixed materials, layered props, hybrid room/scenery logic.
- Artist obsession: one oversized shrine-like album/poster/object, but avoid literal brand copying.

Yearly weather/time diversity guidance:

- 2022 should read as rainy late evening/night archive listening.
- 2023 should read as smoky after-show night or rehearsal-room haze.
- 2024 should read as misty dawn/quiet morning reconciliation.
- 2025 should read as electric late-night neon city/club air.
- 2026 should read as breezy late afternoon or golden-hour open horizon.

Do not make the five zoom-in rooms share the same weather, window state, or time-of-day lighting.

## Space Does Not Have To Be A Room

A yearly fan sector can become any scene generated by music DNA.

Allowed scene types:

- bedroom/listening nook
- album gallery
- archive/library
- neon sound chamber
- outdoor memory landscape
- portal/map room
- record cave
- floating constellation scene
- train/commute scene
- studio desk
- rainy window scene
- festival miniature
- surreal music stage

The fan-shaped boundary stays consistent even if the interior scene changes.

## Character Rules

The character represents the same user across years.

Use `C:\Users\zhuwt\OneDrive\000 - Side Projects\01 - Music\output\characters` as the required character design source for generated or implemented zoom-in spaces.

Reference files:

- `character-2022-rain-archive-amber.png`
- `character-2023-smoky-rehearsal-stage.png`
- `character-2024-quiet-reconciliation-corrected.png`
- `character-2025-neon-kinetic-charge.png`
- `character-2026-open-horizon-freedom.png`

Current overview rule:

- remove the character from the overview spaces
- overview should communicate each year through scene, objects, lighting, motion, and music-DNA installations only
- character may return in zoom-in views if requested, but should not appear in the overview unless explicitly asked

Keep consistent:

- base silhouette
- core identity shape
- general proportions
- character-to-space scale ratio across years
- recognizable face/hair/body logic
- one subtle recurring symbol or design cue
- soft rounded 3D collectible figure style, not stick figure, generic mannequin, or sharp action figure

Change by year:

- outfit
- accessories
- pose
- aura
- material/texture
- object held
- relationship to the environment
- motion behavior

Important:

- character must not stand statically in the center
- character should not be placed on a stage/pedestal by default
- no stage, pedestal, display block, or circular platform under the character unless the user explicitly asks
- character should interact with scene elements
- in zoomed-in spaces, character should be smaller so the environment has room to breathe
- in zoomed-in spaces, character height should occupy the same approximate percentage of room height and floor depth every year
- character should have real outfit/accessory detail and expressive body language, even when small
- preserve the matching reference character's base face, hair/body logic, proportions, and year-specific outfit/accessory language; do not redesign the character from scratch

Good interactions:

- reaching for a floating album
- adjusting a glowing music dial
- sitting near pulsing headphones
- walking through a portal
- pinning an album cover
- touching the mood calendar wall
- following a waveform ribbon
- holding a notebook or ticket
- opening an archive box

## Motion And Kinetic Elements

The space should feel alive, not static.

Use motion cues such as:

- floating album covers
- spinning records
- flowing waveform ribbons
- pulsing mood-calendar tiles
- glowing paths
- orbiting music objects
- moving light beams
- fluttering posters
- drifting particles
- animated portal edges
- shifting weather or room lighting

In static concept images, show motion using:

- motion trails
- ghosted repeated positions
- glow streaks
- curved paths
- dynamic character poses
- blurred object arcs

In the actual website, these can become subtle looping animations.

Keep sparkle/particle density extremely restrained. Avoid many bright dots across walls or scenes; use only a few purposeful light cues such as waveform glow, lamp glow, window glow, or soft edge lighting.

## Required Yearly Space Elements

Each zoomed-in yearly space should include these as visual objects:

- scene/environment generated from music DNA
- same-user character version
- album cover wall or album objects
- top singer/artist wall images should use real authorized artist portraits/headshots from the music data when available
- mood calendar installation
- listening ritual objects
- hashtag stickers/posters
- tracklist plaque
- curator note object
- interactive music controller

These do not all need to be literal flat panels. They can be transformed into objects, lights, textures, furniture, weather, sculptures, or animated installations.

## Text And Labels

Avoid putting lots of readable text inside the 3D scene.

Use real website UI outside or beside the scene for:

- year labels
- song names
- artist names
- explanations
- privacy controls
- share actions

Inside the scene, text-like elements should feel like posters, plaques, stickers, tracklists, or album markings. They can be abstract or partially readable, but should not clutter the scene.

## Hashtag / Harshtag Rules

Use short expressive hashtags as UI chips, share-card stickers, and optional tiny scene stickers. They should feel like music-DNA captions, not SEO tags.

Rules:

- Keep each hashtag at 25 characters or fewer, including `#`.
- Prefer 2-5 strong hashtags per year or card.
- Create multiple voices when useful: persona, space, data DNA, share, funny, and chaos.
- Funny/chaos tags should feel playful and self-aware, not mean, random, or hard to understand.
- Yearly hashtags should reveal what makes that year different, not repeat the same generic mood words every year.
- Use hashtags in website UI outside the 3D scene first. Inside the scene, use them sparingly as stickers, posters, or small plaques.
- Avoid filling the 3D scene with readable hashtag text. The fan-sector space should still be readable as a miniature environment.

Good examples:

- `#ArchiveBoss`
- `#MicCableMood`
- `#PortalPivot`
- `#NeonFeelings`
- `#TrainWindowMood`
- `#ReplayForScience`
- `#TinyClubInMyHead`

## Palette Rules

Do not force one color theme per year.

Colors should emerge from music DNA, scene type, lighting, mood, and materials.

Avoid:

- purple-dominant systems
- beige/cream-only systems
- generic Spotify green
- one-note monochrome palettes
- overly corporate dashboard colors

Prefer:

- cinematic contrast
- data-driven lighting
- warm/cool balance
- rich accent moments
- dreamy pastel atmosphere where appropriate
- light milky pink, yellow, blue, green, and purple
- scene-specific palettes
- album-art-inspired variety

## Website Behavior

The visual system should support this flow:

1. User connects/imports music data.
2. Site generates the full fan-shaped yearly museum.
3. User sees up to five wider yearly spaces arranged together in overview.
4. User clicks a yearly fan-sector space.
5. The selected space zooms in.
6. Controller appears.
7. User interacts with album wall, mood calendar, rituals, tracklist, hashtags, character, and curator note.
8. User can move between years or share one room / the full museum.

## Do Not Do

- Do not make a normal chart dashboard.
- Do not make square rooms.
- Do not place front railings/barriers in the overview.
- Do not show the music controller in the overview.
- Do not make the character static in the center.
- Do not place characters in the overview spaces.
- Do not use a stage/pedestal as the default character placement.
- Do not put characters on display platforms.
- Do not overuse bright dots, sparkles, or star-like particles.
- Do not make yearly rooms differ only by color.
- Do not let color theme replace music-DNA scene design.
- Do not overfill the 3D scene with readable labels.
- Do not copy exact reference visuals, brands, album art, or UI.

## Short Prompt Anchor

When generating or designing visuals, start from this anchor:

> A continuous fan-shaped 3D miniature music museum made of yearly fan-sector spaces, polished cinematic diorama style, each space generated from that year's music DNA, kinetic elements moving through the scene, same small character evolving and interacting with objects, no front railings in overview, controller only appears after zoom-in.
