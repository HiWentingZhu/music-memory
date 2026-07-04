const fs = require("fs/promises");
const path = require("path");

const inputPath = path.join(__dirname, "..", "sample-data", "my-qq-music-2022-2026.json");
const csvPath = path.join(__dirname, "..", "sample-data", "my-qq-music-2022-2026-design.csv");
const summaryPath = path.join(__dirname, "..", "sample-data", "my-music-visual-summary.md");
const palettePath = path.join(__dirname, "..", "sample-data", "color-palettes.svg");

const columns = [
  "year",
  "playlist_year",
  "playlist_id",
  "playlist_name",
  "track_order",
  "track_title",
  "artist_name",
  "album_name",
  "duration_ms",
  "play_count",
  "genre_or_tags",
  "music_type_primary",
  "music_type_traits",
  "music_type_confidence",
  "lyric_available",
  "lyric_theme_tags",
  "lyric_keywords",
  "lyric_mood",
  "lyric_energy",
  "line_count",
  "character_role",
  "character_outfit",
  "character_accessory",
  "character_action",
  "space_scene_type",
  "space_lighting",
  "space_materials",
  "space_ritual_objects",
  "space_motion_cues",
  "album_wall_role",
  "mood_calendar_design",
  "controller_design",
  "curator_note",
  "visual_prompt_seed",
  "qq_track_id",
  "qq_artist_id",
  "qq_album_mid",
  "qq_song_url",
  "qq_album_cover",
  "source_short_url",
  "source_playlist_url",
  "appears_in_years",
  "review_status",
  "review_search_query",
];

const sceneMap = {
  melancholic: {
    scene: "rainy window listening nook",
    lighting: "low moonlight, warm desk lamp, soft reflections",
    materials: "glass, dark wood, paper tickets, fabric cushions",
    objects: "tear-shaped light beads, diary box, headphone nest",
    motion: "slow waveform ribbon, drifting rain shadows, orbiting record ring",
    outfit: "layered coat, soft scarf, muted reflective fabric",
    accessory: "notebook or folded lyric card",
    action: "adjusting a glowing music dial beside the window",
    calendar: "cool-to-warm rain tile wall with brighter repeat-listen cells",
    controller: "front-edge glass console with a soft waveform slider",
  },
  healing: {
    scene: "quiet archive garden inside a fan-sector room",
    lighting: "gentle morning glow, warm backlit shelves",
    materials: "paper, pale wood, translucent acrylic, woven fabric",
    objects: "comfort playlist boxes, pressed-flower album sleeves, lamp pool",
    motion: "floating album pages, breathing calendar tiles, soft light pulses",
    outfit: "cardigan-like jacket, relaxed pants, warm accent pin",
    accessory: "small lamp, bookmark, or tea-colored music charm",
    action: "pinning a recovered album cover to the wall",
    calendar: "soft square tiles arranged like a memory quilt",
    controller: "wood-and-acrylic listening console with round volume knob",
  },
  energetic: {
    scene: "neon sound chamber",
    lighting: "high-contrast kinetic light, bright accent beams",
    materials: "metal, acrylic, glossy black panels, LED strips",
    objects: "sound-wave paths, bright discs, beat markers",
    motion: "fast waveform trails, spinning records, moving light beams",
    outfit: "cropped jacket, sharper silhouette, reflective trim",
    accessory: "glowing headphones or beat baton",
    action: "following a waveform ribbon across the fan floor",
    calendar: "pulsing equalizer-like calendar blocks",
    controller: "front-edge DJ-style disc control with waveform lights",
  },
  nostalgic: {
    scene: "album archive and memory library",
    lighting: "amber shelf light, faded sunset edge glow",
    materials: "warm paper, aged posters, wood drawers, matte metal labels",
    objects: "archive boxes, ticket stubs, old posters, stacked records",
    motion: "fluttering posters, slow dust-like light, looping record rings",
    outfit: "retro jacket, soft worn textures, recurring symbol patch",
    accessory: "ticket bundle or archive key",
    action: "opening an archive box with album covers rising out",
    calendar: "paper-tag calendar clipped to an archive wall",
    controller: "catalog-card console with a small turntable dial",
  },
  aspirational: {
    scene: "portal map room",
    lighting: "clear horizon light with glowing door edges",
    materials: "glass map panels, brushed metal, bright paper, travel stickers",
    objects: "maps, open doors, floating postcards, compass-like discs",
    motion: "animated portal edge, postcards drifting along curved fan paths",
    outfit: "travel jacket, light sneakers, bright lining",
    accessory: "map ribbon or compass charm",
    action: "walking through a small glowing door while holding an album",
    calendar: "route-map calendar with highlighted journey days",
    controller: "front-edge compass dial with timeline path",
  },
  reflective: {
    scene: "minimal album gallery with listening desk",
    lighting: "balanced gallery glow, one warm accent lamp",
    materials: "matte wall panels, acrylic stands, paper plaques, soft wood",
    objects: "curated album frames, note cards, headphones, small plants",
    motion: "subtle album hover, slow light sweep, gentle calendar pulse",
    outfit: "clean layered outfit with one recurring symbol",
    accessory: "small curator notebook",
    action: "placing an album object into a wall slot",
    calendar: "restrained grid of softly lit mood tiles",
    controller: "quiet museum-style front console",
  },
};

async function main() {
  const db = JSON.parse(await fs.readFile(inputPath, "utf8"));
  const rows = db.rows.map(enrichForDesign);
  if (process.env.SUMMARY_ONLY !== "1") {
    const csv = "\uFEFF" + [columns.join(","), ...rows.map(toCsvRow)].join("\n");
    const actualCsvPath = await writeWithFallback(csvPath, csv);
    console.log(`Wrote ${rows.length} CSV rows to ${actualCsvPath}`);
  }
  await fs.writeFile(summaryPath, buildSummary(db, rows), "utf8");
  await fs.writeFile(palettePath, buildPaletteSvg(db), "utf8");
  console.log(`Wrote visual summary to ${summaryPath}`);
  console.log(`Wrote color palette board to ${palettePath}`);
}

async function writeWithFallback(targetPath, content) {
  try {
    await fs.writeFile(targetPath, content, "utf8");
    return targetPath;
  } catch (error) {
    if (error.code !== "EBUSY") throw error;
    const parsed = path.parse(targetPath);
    const fallbackPath = path.join(parsed.dir, `${parsed.name}-${Date.now()}${parsed.ext}`);
    await fs.writeFile(fallbackPath, content, "utf8");
    console.warn(`Target file was locked, wrote ${fallbackPath} instead.`);
    return fallbackPath;
  }
}

function enrichForDesign(row) {
  const mood = row.lyric_analysis?.mood || "reflective";
  const scene = sceneMap[mood] || sceneMap.reflective;
  const themes = row.lyric_analysis?.themes || [];
  const keywords = row.lyric_analysis?.keywords || [];
  const tags = splitTags(row.genre_or_tags);
  const title = row.track_title;
  const artist = row.artist_name;
  const recurringCue = "small glowing music-note pin";

  return {
    ...row,
    design: {
      character_role: `${row.year} version of the same listener figure`,
      character_outfit: `${scene.outfit}; keep base silhouette and ${recurringCue}`,
      character_accessory: scene.accessory,
      character_action: scene.action,
      space_scene_type: scene.scene,
      space_lighting: scene.lighting,
      space_materials: scene.materials,
      space_ritual_objects: scene.objects,
      space_motion_cues: scene.motion,
      album_wall_role: `feature "${title}" as a small album object; cluster nearby albums from ${row.year}`,
      mood_calendar_design: scene.calendar,
      controller_design: scene.controller,
      curator_note: buildCuratorNote(row, themes, keywords, tags),
      visual_prompt_seed: [
        `${row.year} fan-sector miniature music museum`,
        scene.scene,
        `${mood} mood`,
        `${row.music_type?.primary || "playlist-pop"} music type`,
        themes.slice(0, 3).join(" + ") || "personal listening",
        `character interacts by ${scene.action}`,
        `track cue: ${title} by ${artist}`,
      ].join("; "),
    },
  };
}

function toCsvRow(row) {
  const values = {
    year: row.year,
    playlist_year: row.playlist_year,
    playlist_id: row.playlist_id,
    playlist_name: row.playlist_name,
    track_order: row.track_order,
    track_title: row.track_title,
    artist_name: row.artist_name,
    album_name: row.album_name,
    duration_ms: row.duration_ms,
    play_count: row.play_count,
    genre_or_tags: row.genre_or_tags,
    music_type_primary: row.music_type?.primary || "",
    music_type_traits: (row.music_type?.traits || []).join("|"),
    music_type_confidence: row.music_type?.confidence || "",
    lyric_available: row.lyric_analysis?.available ? "yes" : "no",
    lyric_theme_tags: (row.lyric_analysis?.themes || []).join("|"),
    lyric_keywords: (row.lyric_analysis?.keywords || []).join("|"),
    lyric_mood: row.lyric_analysis?.mood || "",
    lyric_energy: row.lyric_analysis?.energy || "",
    line_count: row.lyric_analysis?.line_count || 0,
    character_role: row.design.character_role,
    character_outfit: row.design.character_outfit,
    character_accessory: row.design.character_accessory,
    character_action: row.design.character_action,
    space_scene_type: row.design.space_scene_type,
    space_lighting: row.design.space_lighting,
    space_materials: row.design.space_materials,
    space_ritual_objects: row.design.space_ritual_objects,
    space_motion_cues: row.design.space_motion_cues,
    album_wall_role: row.design.album_wall_role,
    mood_calendar_design: row.design.mood_calendar_design,
    controller_design: row.design.controller_design,
    curator_note: row.design.curator_note,
    visual_prompt_seed: row.design.visual_prompt_seed,
    qq_track_id: row.qq_track_id,
    qq_artist_id: row.qq_artist_id,
    qq_album_mid: row.qq_album_mid,
    qq_song_url: row.online_context?.qq_song_url || "",
    qq_album_cover: row.online_context?.qq_album_cover || "",
    source_short_url: row.online_context?.source_short_url || "",
    source_playlist_url: row.online_context?.source_playlist_url || "",
    appears_in_years: (row.online_context?.appears_in_years || []).join("|"),
    review_status: row.online_context?.review_status || "",
    review_search_query: row.online_context?.review_search_query || "",
  };
  return columns.map((column) => escapeCsv(values[column])).join(",");
}

function buildSummary(db, rows) {
  const lines = [
    "# 2022-2026 Visual Rules Summary",
    "",
    "Generated from `sample-data/my-qq-music-2022-2026.json` and aligned to `VISUAL_RULES.md`.",
    "Use this as the design brief for yearly fan-sector spaces, character evolution, and zoom-in details.",
    "",
    "## 2022-2026 Transition Arc",
    "",
    "The five-year arc should read as one continuous museum where each sector inherits something from the previous year and transforms it. The music starts huge and archival in 2022, narrows into a performance/live-memory bridge in 2023, turns inward into solitude and reconciliation in 2024, spikes into kinetic neon energy in 2025, then opens into a freer 2026 horizon chapter with fewer songs, clearer hero anchors, live-version nostalgia, and more air around the character. The main difference is interior density and motion, not room size: 2022 stores everything, 2023 re-performs it, 2024 sits alone with it and makes peace, 2025 accelerates it, and 2026 releases it into open space.",
    "",
    "Canonical transition spine: dense private archive -> live/rehearsal density -> solitude reconciliation -> kinetic charge -> open horizon nostalgia.",
    "",
    "Spatial translation: archive room -> live room -> quiet reconciliation nook -> neon chamber -> open horizon listening deck.",
    "",
    "Color arc: 2022 starts with paper amber and rain blue, 2023 shifts darker into smoky stage indigo and red marquee accents, 2024 softens into mist blue, quiet sage, rice-paper white, and candle gold, 2025 spikes into electric cyan/hot pink/glossy black, and 2026 opens into horizon sky, sea-glass teal, and sunlit gold. The palette should feel like light transforming through the same waveform line, but each sector must remain visually distinct at a glance.",
    "",
    "Continuous linking motif: a single glowing waveform ribbon runs through all five fan sectors. In 2022 it is tucked inside archive drawers as a thin thread. In 2023 it becomes a microphone cable. In 2024 it curls inward into a quiet repair line around a solo listening seat. In 2025 it turns into a bright neon rail. In 2026 it loosens into a wind path across an open horizon. This one motif makes the rooms feel connected even as the scene language changes.",
    "",
    "Character continuity: keep the same small listener figure across all years. The character carries one recurring music-note pin, but the object in their hand evolves: archive key in 2022 -> microphone cable/poster pin in 2023 -> repaired album tile or folded note in 2024 -> glowing headphones in 2025 -> wind-map ticket or open-air record charm in 2026.",
    "",
    "Zoom-in scale lock: every yearly zoom-in must use the same room footprint, curved shell size, wall height, floor depth, front-edge controller footprint, camera distance, isometric angle, and outside margin. Dense or quiet years should differ through interior object density, lighting, materials, and motion while preserving the same base room size.",
    "",
    "Character reference lock: use the matching character design from `output/characters` for each year, and keep the character-to-space scale ratio consistent across all yearly zoom-ins.",
    "",
    "Spatial continuity: the back wall curve and front floor curve must connect smoothly across all sectors. Repeated songs should appear as small echo rings crossing sector boundaries, especially from 2022 into 2023 and lightly into later years. Do not restart the visual language from scratch at each year.",
    "",
    "Shift notes:",
    "",
    "- 2022 dense private archive -> 2023 live/rehearsal density: the archive does not disappear; it opens. Drawer handles, ticket boxes, and record rings stretch outward into poster walls, stage lights, and microphone cables. The emotional behavior shifts from storing feelings to re-performing them. Because repeated-year songs carry heavily into 2023, this boundary should be the most visibly linked.",
    "- 2023 live/rehearsal density -> 2024 solitude reconciliation: the microphone cable no longer projects outward; it curls inward around a single listening seat. Performance clutter becomes quiet repair: posters reduce into soft album panels, stage beams become candle-like reflection lines, and rehearsal tape becomes a folded note or mended lyric card. The emotional behavior shifts from re-performing everything to sitting alone with it and making peace.",
    "- 2024 solitude reconciliation -> 2025 kinetic charge: the quiet repair line suddenly straightens into a neon rail. Rice-paper surfaces become glossy black acrylic, soft album panels become club-flyer cards, and the single listening seat gives way to a moving waveform path. The emotional behavior shifts from calm self-facing acceptance to release, speed, and visible motion.",
    "- 2025 kinetic charge -> 2026 open horizon nostalgia: the neon rail unwinds into a wind path. Beat markers become spaced hero records floating like waypoints, club flyers become open-air live posters, and glossy momentum becomes horizon light moving across the fan sector. The emotional behavior shifts from loud expansion to freedom, breath, and focused return.",
    "- Full-chain read: archive thread -> microphone cable -> repair line -> neon rail -> wind path. This is the core transition grammar. Every year changes the form of the same line, so the viewer can follow one emotional signal across the entire fan museum.",
    "",
    "Transition harshtags: `#ArchiveToNeon`, `#ReplayGrewUp`, `#MuseumWithFeelings`, `#FromRainToBass`, `#FiveYearMainQuest`.",
    "",
  ];

  for (const yearInfo of db.years) {
    const yearRows = rows.filter((row) => row.year === yearInfo.year);
    const topArtists = topCounts(yearRows, (row) => row.artist_name, "play_count", 10);
    const topTypes = topCounts(yearRows, (row) => row.music_type?.primary || "unknown", "play_count", 10);
    const topMoods = topCounts(yearRows, (row) => row.lyric_analysis?.mood || "unknown", "play_count", 6);
    const topThemes = topMultiCounts(yearRows, (row) => row.lyric_analysis?.themes || [], 8);
    const topKeywords = topMultiCounts(yearRows, (row) => row.lyric_analysis?.keywords || [], 8);
    const distinctiveArtists = topLift(rows, yearRows, (row) => row.artist_name, 8);
    const distinctiveTypes = topLift(rows, yearRows, (row) => row.music_type?.primary || "unknown", 5);
    const distinctiveMoods = topLift(rows, yearRows, (row) => row.lyric_analysis?.mood || "unknown", 5);
    const distinctiveThemes = topLift(rows, yearRows, (row) => row.lyric_analysis?.themes || [], 6);
    const dominantMood = topMoods[0]?.[0] || "reflective";
    const yearDirection = yearVisualDirection(yearInfo.year);
    const scene = yearDirection.scene;
    const density = yearRows.length > 700 ? "dense archive wall with cleaner overview objects" : yearRows.length > 250 ? "medium-density album showroom" : "airier low-density sector with larger hero anchors";
    const repeated = yearRows.filter((row) => (row.online_context?.appears_in_years || []).length > 1).length;
    const artistCount = new Set(yearRows.map((row) => row.artist_name).filter(Boolean)).size;
    const typeCount = new Set(yearRows.map((row) => row.music_type?.primary).filter(Boolean)).size;
    const hasActiveDays = hasActiveListeningData(yearRows);
    const activeDays = hasActiveDays ? new Set(yearRows.map((row) => String(row.played_at).slice(0, 10))).size : null;
    const topArtistTileCount = Math.min(10, artistCount);
    const topTypeTileCount = Math.min(10, typeCount);
    const nowPlaying = yearNowPlaying(yearRows);
    const currentAlbum = yearCurrentAlbum(yearRows, topArtists, topTypes);

    lines.push(`## ${yearInfo.year}`);
    lines.push("");
    lines.push(`- Source playlist: ${yearInfo.playlist_id} (${yearInfo.track_count} entries)`);
    lines.push(`- Space name: ${yearDirection.spaceName}`);
    lines.push(`- Dominant music DNA: ${formatList(topMoods)} moods; ${formatList(topThemes)} themes; ${formatList(topTypes)} types`);
    lines.push(`- What makes this year different: ${yearDirection.difference}`);
    lines.push(`- Harshtags: ${yearDirection.harshtags.map((tag) => `\`${tag}\``).join(", ")}`);
    lines.push(`- Color palette: ${yearDirection.palette.name}; ${yearDirection.palette.colors.map((color) => `${color.name} ${color.hex}`).join(", ")}. Color behavior: ${yearDirection.palette.behavior}`);
    lines.push(`- Relative lift signals: artists ${formatLift(distinctiveArtists)}; moods ${formatLift(distinctiveMoods)}; themes ${formatLift(distinctiveThemes)}; types ${formatLift(distinctiveTypes)}`);
    lines.push(`- Top artists for visual anchors: ${formatList(topArtists)}`);
    lines.push(`- Top artist wall: show exactly ${topArtistTileCount} artist image tiles, capped at 10 and never padded; use checked artist portrait/headshot images where available; if a reliable artist image cannot be found, use that artist's official or recognizable logo; if neither is reliable, use a labeled album-like card or symbolic tile instead of inventing a face; wall labels must use English display names or accepted romanized/stage names only; artists: ${formatList(topArtists)}.`);
    lines.push(`- Music type wall: show exactly ${topTypeTileCount} music-type tiles, capped at 10 and never padded; types: ${formatList(topTypes)}.`);
    lines.push(`- Wall layout diversity: ${scene.wallLayout}; vary mounting method, tile depth, rhythm, and material so this year's wall does not look like the same rectangular grid as the other years, while preserving the exact artist/type tile counts above.`);
    lines.push(`- Year-specific object vocabulary: ${yearDirection.objects}; supporting lyric objects: ${topKeywords.map(([item]) => item).join(", ") || "none"}`);
    lines.push(`- Overview fan-sector: ${yearDirection.overview}; ${density}; no front controller or railing; use equal sector width with the other years.`);
    lines.push(`- Zoom-in environment: ${scene.lighting}; weather/time cue: ${scene.weatherTime}; materials: ${scene.materials}; ritual objects: ${scene.objects}; keep the same zoom-room footprint, camera distance, wall height, floor depth, and front-edge controller scale as every other year.`);
    lines.push(`- Same-user character: use \`output/characters/${yearCharacterReference(yearInfo.year)}\` as the character design reference; ${scene.outfit}; recurring small glowing music-note pin; action: ${scene.action}; accessory: ${scene.accessory}; make the character about one-third smaller than earlier large drafts, keep the character-to-space scale ratio consistent, and vary placement across left/center/right interaction zones instead of always placing the character on the right.`);
    lines.push(`- Wall numeric data: ${hasActiveDays ? `active listening days should show only the number ${activeDays}; ` : "active listening days are unavailable from this source and should not be shown; "}total music should show ${yearRows.length}; keep numeric data as clear wall plaques/counters, not calendar grids.`);
    lines.push(`- Album/music count behavior: ${yearRows.length} playlist entries, ${new Set(yearRows.map((row) => row.track_title)).size} unique songs; make repeated-year songs (${repeated}) appear as loop/ring/archive echoes instead of duplicate text labels.`);
    lines.push(`- Kinetic elements: ${scene.motion}; keep particles restrained and purposeful.`);
    lines.push(`- Zoom-in controller: ${scene.controller}; only visible after selecting this year; show the exact harshtags ${yearDirection.harshtags.map((tag) => `\`${tag}\``).join(", ")} as controller chips; controller sections read left to right as year, volume change, now-playing screen, transport controls, song list, current album; screen shows music name "${nowPlaying.title}", singer/artist name, duration ${nowPlaying.duration}, and play progress ${nowPlaying.progressLabel}; replace any ECG/waveform controller area with exactly three grouped transport buttons: previous, pause/play, next; controller switches albums between wall artists and wall music types; current album cover shows "${currentAlbum.name}"; song list area shows the current album music list: ${currentAlbum.tracks.join(" / ")}.`);
    lines.push(`- Curator note direction: emphasize ${yearDirection.curator}; connect this sector to adjacent years through the continuous fan geometry.`);
    lines.push("");
  }

  return `${lines.join("\n")}\n`;
}

function buildPaletteSvg(db) {
  const years = db.years.map((yearInfo) => ({
    year: yearInfo.year,
    direction: yearVisualDirection(yearInfo.year),
  }));
  const width = 1600;
  const height = 920;
  const margin = 80;
  const gap = 40;
  const cardWidth = Math.floor((width - margin * 2 - gap * (years.length - 1)) / years.length);
  const cardHeight = 620;
  const cardY = 170;

  const cards = years.map(({ year, direction }, index) => {
    const x = margin + index * (cardWidth + gap);
    const palette = direction.palette;
    const colors = palette.colors;
    const swatches = colors.map((color, colorIndex) => {
      const row = Math.floor(colorIndex / 2);
      const col = colorIndex % 2;
      const swatchWidth = colorIndex === 0 ? cardWidth - 48 : Math.floor((cardWidth - 66) / 2);
      const swatchX = colorIndex === 0 ? 24 : 24 + col * (swatchWidth + 18);
      const swatchY = colorIndex === 0 ? 108 : 234 + row * 126;
      const labelY = swatchY + 102;
      return `
        <rect x="${swatchX}" y="${swatchY}" width="${swatchWidth}" height="76" rx="6" fill="${color.hex}" ${color.hex === "#EEF1EA" ? 'stroke="#CCD7D5"' : ""}/>
        <text x="${swatchX}" y="${labelY}" fill="#161514" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="14" font-weight="800">${escapeXml(color.hex)}</text>
        <text x="${swatchX}" y="${labelY + 20}" fill="#6B655D" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="13">${escapeXml(color.name)}</text>
      `;
    }).join("");

    return `
      <g transform="translate(${x} ${cardY})">
        <rect x="0" y="0" width="${cardWidth}" height="${cardHeight}" rx="8" fill="#FFFCF4" stroke="#DDD2BF" filter="url(#shadow)"/>
        <text x="24" y="44" fill="#161514" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="28" font-weight="800">${year}</text>
        <text x="24" y="76" fill="#6B655D" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="15">${escapeXml(palette.name)}</text>
        ${swatches}
        <text x="24" y="568" fill="#6B655D" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="14">${escapeXml(direction.scene.scene || direction.overview).slice(0, 36)}</text>
      </g>
    `;
  }).join("");

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
  <rect width="${width}" height="${height}" fill="#F7F3EA"/>
  <text x="80" y="78" fill="#161514" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="42" font-weight="800">Music Museum Color Palettes</text>
  <text x="80" y="118" fill="#6B655D" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="20">dense private archive -> live/rehearsal density -> solitude reconciliation -> kinetic charge -> open horizon nostalgia</text>
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#161514" flood-opacity="0.12"/>
    </filter>
  </defs>
  ${cards}
  <path d="M210 835 C390 790, 480 790, 570 835 S780 880, 840 835 S1060 790, 1145 835 S1330 880, 1450 835" fill="none" stroke="#161514" stroke-width="3" stroke-linecap="round" opacity="0.55"/>
  <text x="80" y="870" fill="#6B655D" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="18">Palette movement: paper/rain -> stage/smoke -> mist/sage/candle -> neon/black -> horizon/sunlight</text>
</svg>
`;
}

function yearCharacterReference(year) {
  const references = {
    2022: "character-2022-rain-archive-amber.png",
    2023: "character-2023-smoky-rehearsal-stage.png",
    2024: "character-2024-quiet-reconciliation-corrected.png",
    2025: "character-2025-neon-kinetic-charge.png",
    2026: "character-2026-open-horizon-freedom.png",
  };
  return references[year] || "matching-year-character-reference.png";
}

function yearNowPlaying(rows) {
  const counts = new Map();
  for (const row of rows) {
    const key = `${row.track_title}|||${row.artist_name}`;
    counts.set(key, (counts.get(key) || 0) + (Number(row.play_count) || 1));
  }
  const [key] = [...counts.entries()].sort((a, b) => b[1] - a[1])[0] || ["Untitled|||Unknown Artist"];
  const [title, artist] = key.split("|||");
  const row = rows.find((item) => item.track_title === title && item.artist_name === artist) || {};
  const durationMs = Number(row.duration_ms) || 0;
  const progressRatio = 0.42;
  return {
    title: `${title} - ${artist}`,
    duration: formatDuration(durationMs),
    progressLabel: `${formatDuration(Math.round(durationMs * progressRatio))} / ${formatDuration(durationMs)}`,
  };
}

function formatDuration(durationMs) {
  const totalSeconds = Math.max(0, Math.round(Number(durationMs) / 1000));
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = String(totalSeconds % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
}

function hasActiveListeningData(rows) {
  if (!rows.length) return false;
  return rows.some((row) => {
    const source = String(row.source || "");
    const playedAt = String(row.played_at || "");
    const isGeneratedPlaylistRow = source === "qq_music_yearly_playlist";
    const isPlaceholderMidday = /^\d{4}-01-01T12:00:00/.test(playedAt);
    return playedAt && !(isGeneratedPlaylistRow && isPlaceholderMidday);
  });
}

function yearCurrentAlbum(rows, topArtists, topTypes) {
  const artistName = topArtists[0]?.[0];
  const typeName = topTypes[0]?.[0];
  const selectedRows = artistName
    ? rows.filter((row) => row.artist_name === artistName)
    : rows.filter((row) => (row.music_type?.primary || "unknown") === typeName);
  const tracks = topCounts(selectedRows.length ? selectedRows : rows, (row) => row.track_title, "play_count", 5)
    .map(([title]) => title);
  return {
    name: artistName || typeName || "current album",
    tracks: tracks.length ? tracks : ["current music list"],
  };
}

function yearVisualDirection(year) {
  const directions = {
    2022: {
      spaceName: "Rain Archive",
      difference: "the largest and most archival year, with the strongest broad catalog density, pop/OST/live mass, and many repeated-year echoes.",
      overview: "oversized memory archive sector with layered album drawers, a rainy listening window, and a dense but carefully thinned overview wall",
      objects: "archive drawers, ticket boxes, stacked live-record discs, rain glass, old poster sleeves, loop rings for songs that return in later years",
      curator: "a heavy first archive chapter, emotional breadth, and the feeling of building the museum's foundation",
      harshtags: ["#ArchiveBoss", "#RainyReplay", "#BigMoodMuseum", "#LoopRingEra", "#TicketStubFeels"],
      palette: {
        name: "Rain Archive Amber",
        colors: [
          { name: "aged paper amber", hex: "#B9823A" },
          { name: "rain-window blue", hex: "#426F8A" },
          { name: "deep drawer wood", hex: "#4B3327" },
          { name: "library cream", hex: "#E6D5B3" },
          { name: "faded stamp red", hex: "#9D4B3E" },
        ],
        behavior: "warm paper/wood base with cool rain-blue shadows; red appears as small poster and ticket accents.",
      },
      scene: {
        ...sceneMap.nostalgic,
        scene: "rainy archive-library listening room",
        lighting: "amber archive light mixed with blue rain-window glow",
        weatherTime: "rainy late evening/night outside the window, visible raindrops and city reflections, warm archive lamps inside",
        wallLayout: "asymmetric archive salon wall: staggered framed artist cards mixed with shallow shelves and catalog drawer labels; music types appear as vertical file-card tabs on the side wall",
        objects: "archive boxes, ticket stubs, live-record stacks, diary drawers, rain-lit headphones",
        action: "opening an archive drawer while record rings lift into the room",
      },
    },
    2023: {
      spaceName: "Encore Stage",
      difference: "a performance-heavy bridge year: live-show energy, nostalgia lift, and variety-show duet/group artist anchors stand out.",
      overview: "live memory theatre sector, still intimate but with more stage-light traces and performance posters than 2022",
      objects: "microphone cable paths, duet posters, rehearsal tape, live-set lights, memory ribbons, returned-song rings",
      curator: "public performance feeling, nostalgic callbacks, and songs returning as live-room echoes",
      harshtags: ["#MicCableMood", "#EncoreMemory", "#DuetDrama", "#LivePosterEra", "#StageLightFeels"],
      palette: {
        name: "Smoky Rehearsal Stage",
        colors: [
          { name: "stage indigo", hex: "#252E5A" },
          { name: "marquee red", hex: "#C83E4D" },
          { name: "spotlight gold", hex: "#F2B84B" },
          { name: "cable black", hex: "#191B20" },
          { name: "brushed mic silver", hex: "#A5AAB2" },
        ],
        behavior: "darker and more theatrical than 2022; indigo/black/mic silver dominate, with gold only as sharp stage light and red as marquee/poster hits.",
      },
      scene: {
        ...sceneMap.nostalgic,
        scene: "miniature live-memory rehearsal room",
        lighting: "smoky indigo room light with red marquee hits and narrow gold spotlights",
        weatherTime: "after-show night with a dark exterior, smoky rehearsal haze, narrow spotlights cutting through the room",
        wallLayout: "rehearsal pinboard wall: artist tiles mounted as varied-size pinned posters and cable-suspended frames; music types appear as marquee strips and amplifier-rack plaques",
        materials: "black cable lines, brushed mic silver, dark acoustic panels, glossy poster paper",
        objects: "microphone stand, cable coils, pinned duet posters, rehearsal tape boxes, low stage-light bars",
        motion: "fluttering posters, slow spotlight sweep, looping live-record rings",
        action: "pinning a live poster while a microphone cable becomes a waveform",
        controller: "front-edge rehearsal console with a current-album cover control",
      },
    },
    2024: {
      spaceName: "Quiet Reconcile",
      difference: "a smaller solitude/reconciliation year, with reflective and healing lift, fewer songs, and distinct hero anchors that feel self-facing rather than outward-facing.",
      overview: "quiet reconciliation nook sector with more negative space, one solo listening seat, soft album panels, folded-note objects, and a curved mist backdrop",
      objects: "solo listening seat, folded notes, mended lyric cards, soft album panels, quiet lamp, mist-glass calendar tiles",
      curator: "a self-facing chapter about solitude, 独处, and 和解: fewer objects, quieter light, and a character making peace with selected songs",
      harshtags: ["#SoloReconcile", "#QuietRoom", "#SoftAlbumPanel", "#FoldedNoteMood", "#MakingPeace"],
      palette: {
        name: "Quiet Reconciliation",
        colors: [
          { name: "quiet sage", hex: "#8FA889" },
          { name: "mist blue", hex: "#9DB8C8" },
          { name: "rice-paper white", hex: "#F2EBDD" },
          { name: "candle gold", hex: "#D9B56A" },
          { name: "ink stone gray", hex: "#4A4F55" },
        ],
        behavior: "softest and most inward year; mist blue and sage create solitude, rice paper and candle gold create reconciliation, and gray keeps the scene grounded.",
      },
      scene: {
        ...sceneMap.reflective,
        scene: "quiet reconciliation listening nook",
        lighting: "soft mist-blue ambient light with a small candle-gold lamp and gentle window reflection",
        weatherTime: "misty dawn or quiet morning, fogged glass, pale window glow, low soft shadows",
        wallLayout: "sparse folding-screen wall: artist panels arranged on rice-paper screens with generous breathing room; music types appear as small fabric tags and soft translucent plaques",
        materials: "rice paper, misted glass, pale wood, soft fabric, matte ink-gray metal",
        objects: "solo listening seat, folded notes, mended lyric cards, soft album panels, quiet lamp, mist-glass calendar tiles",
        motion: "slow inward waveform loop, barely moving album panels, soft lamp pulse, folded notes lifting slightly",
        action: "sitting beside the quiet lamp and repairing a folded lyric note",
        controller: "front-edge quiet console with a small album dial and breathing waveform line",
      },
    },
    2025: {
      spaceName: "Neon Chamber",
      difference: "the strongest energetic lift, with a Charli xcx/dance-pop edge, more reflective contrast, and a brighter kinetic turn.",
      overview: "neon sound-chamber sector with sharper geometry, glossy surfaces, and visible waveform paths",
      objects: "LED waveform rails, club flyer album cards, reflective black acrylic, moving light strips, beat markers",
      curator: "the year where the museum gets louder, faster, and more kinetic while keeping emotional lyrics underneath",
      harshtags: ["#NeonFeelings", "#BassFeelingsOnly", "#TinyClubInMyHead", "#GlowUpPlaylist", "#KineticCrisis"],
      palette: {
        name: "Neon Kinetic Charge",
        colors: [
          { name: "electric cyan", hex: "#00B8D9" },
          { name: "hot pink", hex: "#FF4F9A" },
          { name: "glossy black", hex: "#121318" },
          { name: "acid yellow", hex: "#E7F24A" },
          { name: "warm lyric amber", hex: "#D98F3F" },
        ],
        behavior: "highest contrast year; cyan/pink/yellow drive motion while amber keeps the emotional thread from earlier rooms.",
      },
      scene: {
        ...sceneMap.energetic,
        scene: "neon club-archive sound chamber",
        lighting: "bright kinetic beams with glossy reflections and warm emotional side light",
        weatherTime: "electric late night with neon city glow outside, dry club air, high-contrast reflections",
        wallLayout: "diagonal neon flyer wall: artist tiles layered as acrylic club flyers along slanted LED rails; music types appear as stacked light-box modules and glowing material swatches",
        objects: "sound-wave rails, club flyer cards, beat markers, glossy album discs, small reflective archive boxes",
        action: "following a bright waveform rail while holding glowing headphones",
      },
    },
    2026: {
      spaceName: "Horizon Deck",
      difference: "a freer open-horizon year, with nostalgic and melancholic lift softened by travel, air, and clearer hero songs.",
      overview: "open horizon listening-deck sector with more negative space, wind-path waveform lines, floating hero records, and a curved sky/sea backdrop",
      objects: "wind-map ribbon, open-air live posters, floating hero records, sea-glass calendar tiles, small travel tickets, horizon light strips",
      curator: "a focused return chapter that feels less enclosed: live echoes, travel air, and freedom after the high-energy 2025 chamber",
      harshtags: ["#OpenHorizon", "#FreeReplay", "#GalaxyOnRepeat", "#LiveVersionHitHard", "#WindPathMood"],
      palette: {
        name: "Open Horizon Freedom",
        colors: [
          { name: "horizon sky", hex: "#7CCFEA" },
          { name: "sea-glass teal", hex: "#2FAE9B" },
          { name: "sunlit gold", hex: "#F3C45B" },
          { name: "cloud paper", hex: "#F3EBDD" },
          { name: "dusk violet", hex: "#7B6BB2" },
        ],
        behavior: "airier and more free than 2025; sky/teal create openness, sunlit gold keeps the live-memory warmth, and violet preserves a small night-music echo.",
      },
      scene: {
        ...sceneMap.aspirational,
        scene: "open horizon listening deck",
        lighting: "wide sky glow with sunlit edge light, soft sea-glass reflections, and a small dusk-violet music halo",
        weatherTime: "breezy golden hour or late afternoon, clear horizon sky, soft wind through open wall panels",
        wallLayout: "open-air horizon wall: artist records and postcards suspended on curved rails at varied depths; music types appear as sea-glass wayfinding signs and translucent hanging tags",
        materials: "translucent acrylic, sea-glass panels, pale wood, paper tickets, light fabric ribbons",
        objects: "floating hero records, open-air live posters, wind-map ribbon, sea-glass calendar tiles, small travel tickets",
        motion: "waveform ribbon moving like wind, records drifting as waypoints, soft horizon light sweeping across the fan curve",
        action: "walking along the wind-path ribbon while holding an open-air record charm",
        controller: "front-edge horizon console with a compass-like record dial and breeze-shaped waveform slider",
      },
    },
  };
  return directions[year] || {
    difference: "balanced personal archive year.",
    overview: sceneMap.reflective.scene,
    objects: sceneMap.reflective.objects,
    curator: "balanced personal archive",
    harshtags: ["#PersonalArchive", "#MusicMuseum", "#SoundtrackSelf"],
    palette: {
      name: "Balanced Archive",
      colors: [
        { name: "paper light", hex: "#E8D8B8" },
        { name: "soft teal", hex: "#287C89" },
        { name: "warm accent", hex: "#F0B441" },
      ],
      behavior: "neutral fallback palette.",
    },
    scene: sceneMap.reflective,
  };
}

function escapeXml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&apos;",
  })[character]);
}

function buildCuratorNote(row, themes, keywords, tags) {
  const bits = [
    `${row.track_title} anchors a ${row.lyric_analysis?.mood || "reflective"} corner`,
    themes.length ? `themes: ${themes.slice(0, 3).join(", ")}` : "",
    keywords.length ? `objects from keywords: ${keywords.slice(0, 4).join(", ")}` : "",
    tags.length ? `playlist tags: ${tags.slice(0, 4).join(", ")}` : "",
  ].filter(Boolean);
  return bits.join("; ");
}

function topCounts(rows, keyFn, weightKey, limit) {
  const counts = new Map();
  rows.forEach((row) => {
    const key = keyFn(row);
    const weight = Number(row[weightKey] || 1);
    if (!key) return;
    counts.set(key, (counts.get(key) || 0) + weight);
  });
  return [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit);
}

function topMultiCounts(rows, valuesFn, limit) {
  const counts = new Map();
  rows.forEach((row) => {
    valuesFn(row).forEach((value) => {
      counts.set(value, (counts.get(value) || 0) + Number(row.play_count || 1));
    });
  });
  return [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit);
}

function topLift(allRows, yearRows, valuesFn, limit) {
  const otherRows = allRows.filter((row) => row.year !== yearRows[0]?.year);
  const yearCounts = multiCount(yearRows, valuesFn);
  const otherCounts = multiCount(otherRows, valuesFn);
  const yearTotal = sumCounts(yearCounts);
  const otherTotal = sumCounts(otherCounts);

  return [...yearCounts.entries()]
    .map(([item, count]) => {
      const otherCount = otherCounts.get(item) || 0.5;
      const ratio = (count / yearTotal) / (otherCount / otherTotal);
      return [item, count, ratio];
    })
    .filter(([, count]) => count >= 5)
    .sort((a, b) => b[2] - a[2])
    .slice(0, limit);
}

function multiCount(rows, valuesFn) {
  const counts = new Map();
  rows.forEach((row) => {
    const values = valuesFn(row);
    (Array.isArray(values) ? values : [values]).filter(Boolean).forEach((value) => {
      counts.set(value, (counts.get(value) || 0) + Number(row.play_count || 1));
    });
  });
  return counts;
}

function sumCounts(counts) {
  return [...counts.values()].reduce((sum, value) => sum + value, 0);
}

function formatList(entries) {
  return entries.map(([item, count]) => `${item} (${count})`).join(", ") || "none";
}

function formatLift(entries) {
  return entries.map(([item, count, ratio]) => `${item} (${ratio.toFixed(1)}x, ${count})`).join(", ") || "none";
}

function splitTags(value) {
  return String(value || "")
    .split(/[,;|/]/)
    .map((tag) => tag.trim())
    .filter(Boolean);
}

function escapeCsv(value) {
  const text = value === undefined || value === null ? "" : String(value);
  return /[",\n\r]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
