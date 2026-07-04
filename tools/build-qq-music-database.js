const fs = require("fs/promises");
const path = require("path");

const playlists = {
  2022: {
    short_url: "https://c6.y.qq.com/base/fcgi-bin/u?__=t5fo7hla70ot",
    playlist_id: "8535705502",
  },
  2023: {
    short_url: "https://c6.y.qq.com/base/fcgi-bin/u?__=VExB93la7Buz",
    playlist_id: "8565876295",
  },
  2024: {
    short_url: "https://c6.y.qq.com/base/fcgi-bin/u?__=pDkmDcla7UOS",
    playlist_id: "8989911780",
  },
  2025: {
    short_url: "https://c6.y.qq.com/base/fcgi-bin/u?__=cZegxnla76oT",
    playlist_id: "9183390267",
  },
  2026: {
    short_url: "https://c6.y.qq.com/base/fcgi-bin/u?__=EMkof1la7v3Z",
    playlist_id: "9497585558",
  },
};

const headers = {
  referer: "https://y.qq.com/",
  "user-agent": "Mozilla/5.0",
};

const themePatterns = [
  ["love", /爱|喜欢|想你|心动|拥抱|亲爱|情人|恋|吻|romance|love/i],
  ["heartbreak", /分手|离开|眼泪|泪|孤独|寂寞|遗憾|难过|心碎|失去|伤|sad|alone/i],
  ["memory", /回忆|从前|曾经|后来|青春|旧|过去|记得|怀念|memory/i],
  ["healing", /治愈|温柔|晚安|陪|安静|月光|星|梦|希望|释怀|自由/i],
  ["growth", /成长|勇敢|未来|远方|路|追|飞|光|梦想|明天/i],
  ["city-night", /城市|街|夜|霓虹|雨|车|酒|灯|midnight|night/i],
  ["energy", /跳舞|燃|热|party|dance|boom|fire|rock|beat|electric/i],
];

const typePatterns = [
  ["r&b", /r&b|节奏布鲁斯|灵魂|soul/i],
  ["hip-hop", /rap|rapper|hip.?hop|嘻哈|说唱/i],
  ["rock", /rock|摇滚|band|乐队|吉他/i],
  ["electronic", /edm|electro|电子|dance|dj|remix/i],
  ["folk", /folk|民谣|acoustic|木吉他/i],
  ["ost", /ost|原声|影视|剧集|电影|主题曲|插曲/i],
  ["live", /live|现场/i],
  ["pop", /pop|流行|华语|国语|mandopop/i],
];

async function main() {
  const yearCollections = [];
  const workItems = [];
  const seenTrackYears = new Map();

  for (const [year, source] of Object.entries(playlists)) {
    const playlist = await fetchPlaylist(source.playlist_id);
    const cd = playlist.cdlist?.[0];
    if (!cd?.songlist?.length) throw new Error(`No songs returned for ${year}`);

    const playlistTags = (cd.tags || []).map((tag) => tag.name || tag).filter(Boolean);
    console.log(`Fetched ${year}: ${cd.dissname} (${cd.songlist.length} songs)`);

    for (let index = 0; index < cd.songlist.length; index += 1) {
      const song = cd.songlist[index];
      workItems.push({
        year: Number(year),
        source,
        playlist: cd,
        playlistTags,
        song,
        index,
      });
    }

    yearCollections.push({
      year: Number(year),
      playlist_id: source.playlist_id,
      short_url: source.short_url,
      resolved_url: `https://i.y.qq.com/n2/m/share/details/taoge.html?id=${source.playlist_id}`,
      playlist_name: cd.dissname || String(year),
      playlist_tags: playlistTags,
      track_count: cd.songlist.length,
      source_created_at: cd.ctime || "",
      source_updated_at: cd.mtime || "",
    });
  }

  console.log(`Fetching lyric analysis for ${workItems.length} playlist entries...`);
  const lyricCache = new Map();
  const rows = await mapLimit(workItems, 16, async (item, index) => {
    const songmid = item.song.songmid || item.song.mid || "";
    if (!lyricCache.has(songmid)) {
      lyricCache.set(songmid, fetchLyricAnalysis(songmid));
    }
    const lyricInfo = await lyricCache.get(songmid);
    if ((index + 1) % 100 === 0) console.log(`Enriched ${index + 1}/${workItems.length}`);
    return createRow({ ...item, lyricInfo });
  });

  rows.forEach((row) => {
    const key = `${row.qq_track_id || row.track_title}::${row.artist_name}`;
    const years = seenTrackYears.get(key) || [];
    years.push(row.year);
    seenTrackYears.set(key, years);
  });

  rows.forEach((row) => {
    const key = `${row.qq_track_id || row.track_title}::${row.artist_name}`;
    row.online_context.appears_in_years = [...new Set(seenTrackYears.get(key) || [row.year])].sort();
  });

  const database = {
    schema_version: 1,
    generated_at: new Date().toISOString(),
    source: "QQ Music yearly playlists",
    notes: [
      "Lyrics are analyzed for themes and keywords, but full lyric text is not stored.",
      "QQ public song review/comment data was not available through unauthenticated web endpoints during generation.",
    ],
    years: yearCollections,
    rows,
  };

  const outputPath = path.join(__dirname, "..", "sample-data", "my-qq-music-2022-2026.json");
  await fs.writeFile(outputPath, `${JSON.stringify(database, null, 2)}\n`, "utf8");
  console.log(`Wrote ${rows.length} rows to ${outputPath}`);
}

async function fetchPlaylist(playlistId) {
  const endpoint = new URL("https://i.y.qq.com/qzone-music/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg");
  endpoint.search = new URLSearchParams({
    type: "1",
    json: "1",
    utf8: "1",
    onlysong: "0",
    nosign: "1",
    disstid: playlistId,
    g_tk: "5381",
    loginUin: "0",
    hostUin: "0",
    format: "json",
    inCharset: "GB2312",
    outCharset: "utf-8",
    notice: "0",
    platform: "yqq",
    needNewCode: "0",
  }).toString();

  const response = await fetch(endpoint, { headers });
  if (!response.ok) throw new Error(`Playlist ${playlistId} returned ${response.status}`);
  return response.json();
}

async function fetchLyricAnalysis(songmid) {
  if (!songmid) return emptyLyricAnalysis("missing songmid");
  const endpoint = `https://i.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?songmid=${encodeURIComponent(songmid)}&g_tk=5381&format=json&inCharset=utf8&outCharset=utf-8&nobase64=1`;

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);
    const response = await fetch(endpoint, { headers, signal: controller.signal });
    clearTimeout(timeout);
    if (!response.ok) return emptyLyricAnalysis(`lyric endpoint returned ${response.status}`);
    const data = await response.json();
    const lyric = data.lyric || "";
    const trans = data.trans || "";
    if (!lyric.trim()) return emptyLyricAnalysis("no public lyric returned");
    return analyzeLyric(lyric, trans);
  } catch (error) {
    return emptyLyricAnalysis(error.message);
  }
}

function createRow({ year, source, playlist, playlistTags, song, index, lyricInfo }) {
  const singers = song.singer || song.singers || [];
  const artistName = Array.isArray(singers)
    ? singers.map((singer) => singer.name || singer.title).filter(Boolean).join(", ")
    : "";
  const title = song.songname || song.songorig || song.name || song.title || `QQ Music track ${index + 1}`;
  const albumName = song.albumname || song.album?.name || "Unknown Album";
  const songmid = song.songmid || song.mid || "";
  const type = inferMusicType({ title, albumName, playlistTags, lyricInfo, song });
  const moodTags = inferMoodTags({ title, playlistTags, lyricInfo });

  return {
    source: "qq_music_yearly_playlist",
    played_at: `${year}-01-01T12:00:00`,
    year,
    track_title: title,
    artist_name: artistName || song.singername || "Unknown Artist",
    album_name: albumName,
    duration_ms: Number(song.interval || song.duration || 220) * 1000,
    play_count: Math.max(1, Math.round((playlist.songlist.length - index) / Math.max(24, playlist.songlist.length / 12))),
    genre_or_tags: [...new Set([...playlistTags, type.primary, ...moodTags])].filter(Boolean).join(", "),
    qq_track_id: songmid,
    qq_artist_id: Array.isArray(singers) ? singers.map((singer) => singer.mid).filter(Boolean).join(",") : "",
    qq_album_mid: song.albummid || song.album?.mid || "",
    playlist_year: year,
    playlist_id: source.playlist_id,
    playlist_name: playlist.dissname || String(year),
    track_order: index + 1,
    music_type: type,
    lyric_analysis: lyricInfo,
    online_context: {
      qq_song_url: songmid ? `https://y.qq.com/n/ryqq/songDetail/${songmid}` : "",
      qq_album_cover: song.albummid ? `https://y.gtimg.cn/music/photo_new/T002R300x300M000${song.albummid}.jpg` : "",
      source_short_url: source.short_url,
      source_playlist_url: `https://y.qq.com/n/ryqq/playlist/${source.playlist_id}`,
      review_status: "public QQ reviews not available without login",
      review_search_query: `${title} ${artistName || ""} song review`,
      appears_in_years: [year],
    },
  };
}

function analyzeLyric(lyric, trans) {
  const cleanLines = lyric
    .split(/\r?\n/)
    .map((line) => line.replace(/\[[^\]]*\]/g, "").trim())
    .filter((line) => line && !/^(词|曲|编曲|制作|和声|录音|混音|母带|OP|SP|发行)[:：]/i.test(line));
  const cleanText = cleanLines.join(" ");
  const themes = themePatterns
    .filter(([, pattern]) => pattern.test(cleanText))
    .map(([theme]) => theme);
  const keywords = pickKeywords(cleanText);
  const hasTranslation = Boolean(trans && trans.trim());

  return {
    available: true,
    line_count: cleanLines.length,
    has_translation: hasTranslation,
    themes: themes.length ? themes : ["personal"],
    keywords,
    mood: inferLyricMood(themes, cleanText),
    energy: inferLyricEnergy(themes, cleanText),
    source: "QQ Music lyric endpoint",
  };
}

function emptyLyricAnalysis(reason) {
  return {
    available: false,
    line_count: 0,
    has_translation: false,
    themes: [],
    keywords: [],
    mood: "unknown",
    energy: "unknown",
    source: "QQ Music lyric endpoint",
    note: reason,
  };
}

function inferMusicType({ title, albumName, playlistTags, lyricInfo, song }) {
  const haystack = [title, albumName, playlistTags.join(" "), song.subtitle || "", song.albumdesc || ""].join(" ");
  const matched = typePatterns.find(([, pattern]) => pattern.test(haystack));
  const primary = matched?.[0] || (playlistTags.includes("流行") ? "pop" : "playlist-pop");
  const traits = [];
  if (/live/i.test(haystack)) traits.push("live");
  if (lyricInfo.themes?.includes("heartbreak")) traits.push("emotional");
  if (lyricInfo.themes?.includes("energy")) traits.push("high-energy");
  if (lyricInfo.themes?.includes("healing")) traits.push("healing");
  return {
    primary,
    traits: [...new Set(traits)],
    confidence: matched || playlistTags.length ? "medium" : "low",
    basis: "QQ playlist tags, title/album text, and lyric-derived themes",
  };
}

function inferMoodTags({ title, playlistTags, lyricInfo }) {
  const tags = [...playlistTags];
  if (lyricInfo.mood && lyricInfo.mood !== "unknown") tags.push(lyricInfo.mood);
  if (/live/i.test(title)) tags.push("live");
  return [...new Set(tags)];
}

function inferLyricMood(themes, text) {
  if (themes.includes("heartbreak")) return "melancholic";
  if (themes.includes("healing")) return "healing";
  if (themes.includes("energy")) return "energetic";
  if (themes.includes("memory")) return "nostalgic";
  if (themes.includes("growth")) return "aspirational";
  if (/快乐|开心|笑|甜|阳光/.test(text)) return "bright";
  return "reflective";
}

function inferLyricEnergy(themes, text) {
  if (themes.includes("energy")) return "high";
  if (/安静|温柔|晚安|孤独|寂寞/.test(text)) return "low";
  return "medium";
}

function pickKeywords(text) {
  const candidates = [
    "爱", "想你", "离开", "眼泪", "回忆", "青春", "夜", "雨", "光", "梦",
    "自由", "城市", "孤独", "温柔", "未来", "勇敢", "遗憾", "心动",
  ];
  return candidates.filter((word) => text.includes(word)).slice(0, 8);
}

async function mapLimit(items, limit, worker) {
  const results = new Array(items.length);
  let nextIndex = 0;
  const workers = Array.from({ length: limit }, async () => {
    while (nextIndex < items.length) {
      const currentIndex = nextIndex;
      nextIndex += 1;
      results[currentIndex] = await worker(items[currentIndex], currentIndex);
    }
  });
  await Promise.all(workers);
  return results;
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
