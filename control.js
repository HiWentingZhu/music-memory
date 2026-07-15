const AUDIO_EXTENSIONS = /\.(mp3|m4a|wav|ogg|flac|aac|opus)$/i;

const YEARS = [2022, 2023, 2024, 2025, 2026];
const PLAY_MODES = ["shuffle", "single", "list"];
const PLAY_MODE_LABELS = {
  shuffle: "SHUFFLE",
  single: "SINGLE LOOP",
  list: "LIST LOOP",
};

const SONG_LIST_DRAG_SCALE = 0.86;
const SONG_LIST_SWITCH_RATIO = 1;
const SONG_LIST_WHEEL_COOLDOWN_MS = 260;
const SONG_LIST_WHEEL_THRESHOLD = 18;
const ARTIST_IMAGE_ROTATE_MS = 30000;
const ARTIST_IMAGE_FADE_MS = 900;
const ARTIST_INFO_CSV_PATH = "output/artist-info-source-of-truth-v1.csv";
const YEAR_MUSIC_MAX_GAIN = 0.20;
const DEFAULT_MUSIC_VOLUME = 50;
const ENABLE_REAL_AUDIO_ANALYSER = false;
const SHARED_VOLUME_KEY = "linger:music-volume";
const VOLUME_CHANGE_EVENT = "linger:volumechange";
const SOUND_CHOICE_KEY = "linger:sound-choice";
const SOUND_CHANGE_EVENT = "linger:soundchange";
const MUSIC_AUTOPLAY_KEY = "linger:music-autoplay-enabled";
const MUSIC_PLAY_STATE_KEY = "linger:music-playing";
const MUSIC_PLAY_STATE_CHANGE_EVENT = "linger:musicplaystatechange";
const MUSIC_COMMAND_EVENT = "linger:music-command";
const YEAR_CONTROL_PLAYBACK_EVENT = "linger:year-control-playback";
const YEAR_PARENT_PLAYBACK_EVENT = "linger:year-parent-playback";
const YEAR_PARENT_COMMAND_EVENT = "linger:year-parent-command";
const YEAR_PLAYBACK_SAVE_EVENT = "linger:year-playback-save";
const YEAR_PLAYBACK_RESTORE_EVENT = "linger:year-playback-restore";
const PLAYBACK_KEY_PREFIX = "linger:playback:year:";
const SINGER_INTRO_SCROLL_START_MS = 1200;
const SINGER_INTRO_SCROLL_SPEED = 24;
const SINGER_INTRO_SCROLL_PAUSE_MS = 2200;
const SINGER_INTRO_MANUAL_PAUSE_MS = 8000;

const queryParams = new URLSearchParams(window.location.search);
const TREBLE_CURSOR_ASSET = "assets/cursor/treble-note-clay-cutout-bright.png";
const TREBLE_CURSOR_TRAIL_ASSETS = [
  "single-note-dark.png",
  "single-note-light.png",
  "curly-rest-dark.png",
  "curly-rest-light.png",
  "bass-clef-dark.png",
  "bass-clef-light.png",
  "double-note-teal.png",
  "double-note-warm.png",
  "double-note-dark.png",
  "double-note-pale.png",
  "flat-symbol.png",
  "sharp-symbol.png",
  "ring-teal.png",
  "ring-warm.png",
].map((fileName) => `assets/cursor/trail-elements/${fileName}`);

const PLAY_MODE_ICONS = {
  shuffle: `
    <svg class="mode-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M3 7h3.5c2.7 0 4.3 2 5.6 4.6 1.4 2.8 2.8 5.4 5.9 5.4h3"></path>
      <path d="M18 14l3 3-3 3"></path>
      <path d="M3 17h3.5c1.7 0 2.9-.8 3.9-2.1"></path>
      <path d="M13.6 8.8C14.7 7.7 16 7 18 7h3"></path>
      <path d="M18 4l3 3-3 3"></path>
    </svg>
  `,
  single: `
    <svg class="mode-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M18.7 9.5a7 7 0 0 0-12.1-2.2"></path>
      <path d="M6.6 7.3H3.9V4.6"></path>
      <path d="M5.3 14.5a7 7 0 0 0 12.1 2.2"></path>
      <path d="M17.4 16.7h2.7v2.7"></path>
      <path d="M12 10.2v5.2"></path>
      <path d="M10.7 11.4 12 10.2v5.2"></path>
    </svg>
  `,
  list: `
    <svg class="mode-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M18.7 9.5a7 7 0 0 0-12.1-2.2"></path>
      <path d="M6.6 7.3H3.9V4.6"></path>
      <path d="M5.3 14.5a7 7 0 0 0 12.1 2.2"></path>
      <path d="M17.4 16.7h2.7v2.7"></path>
      <path d="M10.2 10.4h3.5"></path>
      <path d="M10.2 13h3.5"></path>
      <path d="M10.2 15.6h3.5"></path>
    </svg>
  `,
};

const DEFAULT_TEMPO_BY_YEAR = {
  2022: 78,
  2023: 126,
  2024: 76,
  2025: 132,
  2026: 88,
};

const TEMPO_BY_TITLE = {
  [u("\\u65c5\\u884c\\u4e2d\\u5fd8\\u8bb0")]: 78,
  [u("\\u8bf4\\u7ed9\\u4f60\\u542c")]: 72,
  [u("\\u60f3\\u5bf9\\u4f60\\u8bf4")]: 74,
  [u("\\u521d\\u8877")]: 70,
  MASCARA: 126,
  [u("\\u5927\\u96e8 (Live)")]: 82,
  [u("\\u5fc3\\u5b89\\u7684\\u9b54\\u50cf")]: 94,
  [u("\\u5bf9\\u7684\\u4eba")]: 76,
  [u("\\u4e00\\u591c")]: 74,
  [u("\\u610f\\u6e21")]: 80,
  [u("\\u4f60\\u597d\\uff0c\\u6211\\u662f___")]: 84,
  [u("\\u4e94\\u5149\\u5341\\u8272")]: 92,
  "Everything Is Romantic": 120,
  "Talk talk": 125,
  "Sympathy is a knife": 118,
  "Von dutch": 130,
  [u("\\u4fee\\u70bc\\u7231\\u60c5 (Live)")]: 84,
  [u("\\u8389\\u8389\\u5b89 (Live)")]: 82,
  [u("\\u6d6a\\u8d39 (Live)")]: 76,
  [u("\\u76f8\\u7231\\u540e\\u52a8\\u7269\\u611f\\u4f24")]: 88,
};

function u(value) {
  return value.replace(/\\u[\dA-Fa-f]{4}/g, (match) => String.fromCharCode(parseInt(match.slice(2), 16)));
}

const ENGLISH_TITLE_BY_CHINESE = {
  [u("\\u65c5\\u884c\\u4e2d\\u5fd8\\u8bb0")]: "Forgotten on the Journey",
  [u("\\u8bf4\\u7ed9\\u4f60\\u542c")]: "Tell It to You",
  [u("\\u60f3\\u5bf9\\u4f60\\u8bf4")]: "What I Want to Say",
  [u("\\u521d\\u8877")]: "Original Intention",
  [u("\\u5927\\u96e8 (Live)")]: "Heavy Rain (Live)",
  [u("\\u5fc3\\u5b89\\u7684\\u9b54\\u50cf")]: "The Idol of Peace",
  [u("\\u5bf9\\u7684\\u4eba")]: "The Right Person",
  [u("\\u4e00\\u591c")]: "One Night",
  [u("\\u610f\\u6e21")]: "Crossing of Thought",
  [u("\\u4f60\\u597d\\uff0c\\u6211\\u662f___")]: "Hello, I Am ___",
  [u("\\u4e94\\u5149\\u5341\\u8272")]: "Dazzling Colors",
  [u("\\u4fee\\u70bc\\u7231\\u60c5 (Live)")]: "Practice Love (Live)",
  [u("\\u8389\\u8389\\u5b89 (Live)")]: "Lillian (Live)",
  [u("\\u6d6a\\u8d39 (Live)")]: "Waste (Live)",
  [u("\\u76f8\\u7231\\u540e\\u52a8\\u7269\\u611f\\u4f24")]: "Animal Sentiment After Love",
};

const ARTIST_DISPLAY_OVERRIDES = {
  gala: { cn: "GALA乐队", en: "GALA" },
};

const ARTIST_IMAGE_NAME_FALLBACKS = new Map([
  [normalizeArtistKey(u("\\u4ea6\\u7136")), { cn: u("\\u4ea6\\u7136"), en: "Yiran" }],
  [normalizeArtistKey("Yiran"), { cn: u("\\u4ea6\\u7136"), en: "Yiran" }],
  [normalizeArtistKey(u("\\u4ea6\\u7136 (Yiran)")), { cn: u("\\u4ea6\\u7136"), en: "Yiran" }],
]);

function getTitleTranslationMap() {
  return window.LINGER_TITLE_TRANSLATIONS?.titles || {};
}

function getEnglishTitleFromLookup(title) {
  const normalizedTitle = String(title || "").trim();
  if (!normalizedTitle) return "";
  return getTitleTranslationMap()[normalizedTitle] || ENGLISH_TITLE_BY_CHINESE[normalizedTitle] || "";
}

function hasChineseText(value) {
  return /[\u3400-\u9fff]/.test(String(value || ""));
}

function artistImageList(folder, filenames, positions = []) {
  return filenames.map((filename, index) => ({
    src: encodeURI(`${folder}/${filename}`),
    position: positions[index] || "50% 28%",
  }));
}

const FALLBACK_TRACKS = {
  2022: [
    { title: u("\\u65c5\\u884c\\u4e2d\\u5fd8\\u8bb0"), englishTitle: "Forgotten on the Journey", artist: u("\\u8881\\u5a05\\u7ef4 TIA RAY") },
    { title: u("\\u8bf4\\u7ed9\\u4f60\\u542c"), englishTitle: "Tell It to You", artist: "Aska Yang" },
    { title: u("\\u60f3\\u5bf9\\u4f60\\u8bf4"), englishTitle: "What I Want to Say", artist: "Aska Yang" },
    { title: u("\\u521d\\u8877"), englishTitle: "Original Intention", artist: "Archive" },
  ],
  2023: [
    { title: "MASCARA", artist: "XG" },
    { title: u("\\u5927\\u96e8 (Live)"), englishTitle: "Heavy Rain (Live)", artist: "Encore Stage" },
    { title: u("\\u5fc3\\u5b89\\u7684\\u9b54\\u50cf"), englishTitle: "The Idol of Peace", artist: "Encore Stage" },
    { title: u("\\u5bf9\\u7684\\u4eba"), englishTitle: "The Right Person", artist: "Encore Stage" },
  ],
  2024: [
    { title: u("\\u4e00\\u591c"), englishTitle: "One Night", artist: u("\\u9648\\u695a\\u751f") },
    { title: u("\\u610f\\u6e21"), englishTitle: "Crossing of Thought", artist: "Quiet Room" },
    { title: u("\\u4f60\\u597d\\uff0c\\u6211\\u662f___"), englishTitle: "Hello, I Am ___", artist: "Quiet Room" },
    { title: u("\\u4e94\\u5149\\u5341\\u8272"), englishTitle: "Dazzling Colors", artist: "Quiet Room" },
  ],
  2025: [
    { title: "Everything Is Romantic", artist: "Charli xcx" },
    { title: "Talk talk", artist: "Charli xcx" },
    { title: "Sympathy is a knife", artist: "Charli xcx" },
    { title: "Von dutch", artist: "Charli xcx" },
  ],
  2026: [
    { title: u("\\u4fee\\u70bc\\u7231\\u60c5 (Live)"), englishTitle: "Practice Love (Live)", artist: u("\\u5f90\\u4f73\\u83b9") },
    { title: u("\\u8389\\u8389\\u5b89 (Live)"), englishTitle: "Lillian (Live)", artist: u("\\u5f90\\u4f73\\u83b9") },
    { title: u("\\u6d6a\\u8d39 (Live)"), englishTitle: "Waste (Live)", artist: u("\\u5f90\\u4f73\\u83b9") },
    { title: u("\\u76f8\\u7231\\u540e\\u52a8\\u7269\\u611f\\u4f24"), englishTitle: "Animal Sentiment After Love", artist: u("\\u5f90\\u4f73\\u83b9") },
  ],
};

const SINGER_INFO = {
  2022: {
    artistKey: u("\\u6768\\u5b97\\u7eac (Aska Yang)"),
    cn: u("\\u6768\\u5b97\\u7eac"),
    en: "Aska Yang",
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/%E5%A4%A7%E7%94%B2%E5%AA%BD%E7%A5%96%E4%B9%8B%E5%85%89%E6%BC%94%E5%94%B1%E6%9C%83_%E6%A5%8A%E5%AE%97%E7%B7%AF_20140405.jpg/500px-%E5%A4%A7%E7%94%B2%E5%AA%BD%E7%A5%96%E4%B9%8B%E5%85%89%E6%BC%94%E5%94%B1%E6%9C%83_%E6%A5%8A%E5%AE%97%E7%B7%AF_20140405.jpg",
    images: artistImageList("output/artist-image-downloads-v1/102 - " + u("\\u6768\\u5b97\\u7eac") + " (Aska Yang)", ["01.jpg", "02.jpg", "03.jpg", "04.jpg", "05.jpg"], ["55% 24%", "68% 24%", "52% 24%", "52% 20%", "52% 24%"]),
    intro: "A Taiwanese singer known for a clear, emotive voice and dramatic ballad phrasing. His songs often feel intimate, rain-soaked, and memory-heavy.",
  },
  2023: {
    artistKey: u("\\u6768\\u5b97\\u7eac (Aska Yang)"),
    cn: u("\\u6768\\u5b97\\u7eac"),
    en: "Aska Yang",
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/%E5%A4%A7%E7%94%B2%E5%AA%BD%E7%A5%96%E4%B9%8B%E5%85%89%E6%BC%94%E5%94%B1%E6%9C%83_%E6%A5%8A%E5%AE%97%E7%B7%AF_20140405.jpg/500px-%E5%A4%A7%E7%94%B2%E5%AA%BD%E7%A5%96%E4%B9%8B%E5%85%89%E6%BC%94%E5%94%B1%E6%9C%83_%E6%A5%8A%E5%AE%97%E7%B7%AF_20140405.jpg",
    images: artistImageList("output/artist-image-downloads-v1/102 - " + u("\\u6768\\u5b97\\u7eac") + " (Aska Yang)", ["01.jpg", "02.jpg", "03.jpg", "04.jpg", "05.jpg"], ["55% 24%", "68% 24%", "52% 24%", "52% 20%", "52% 24%"]),
    intro: "A vocalist with a stage-first presence and polished emotional control. This year frames him like an encore archive: warmer lights, darker room, stronger live energy.",
  },
  2024: {
    artistKey: u("\\u6613\\u70ca\\u5343\\u73ba (Jackson Yee)"),
    cn: u("\\u6613\\u70ca\\u5343\\u73ba"),
    en: "Jackson Yee",
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/2024_Jackson_Yee.jpg/500px-2024_Jackson_Yee.jpg",
    images: artistImageList("output/artist-image-downloads-v1/088 - " + u("\\u6613\\u70ca\\u5343\\u73ba") + " (Jackson Yee)", ["01.jpg", "02.jpg", "03.jpg", "04.jpg", "05.jpg"], ["50% 22%", "52% 22%", "52% 20%", "42% 26%", "62% 22%"]),
    intro: "A Chinese singer, actor, and performer whose work often carries a quiet, restrained intensity. This space treats him as calm, careful, and close to the page.",
  },
  2025: {
    artistKey: "Charli xcx",
    cn: "",
    en: "Charli xcx",
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Charli_xcx_at_Berlinale_2026-1.jpg/500px-Charli_xcx_at_Berlinale_2026-1.jpg",
    images: artistImageList("output/artist-image-downloads-v1/006 - Charli xcx", ["01.jpg", "02.jpg", "03.jpg", "04.jpg", "05.jpg"], ["42% 22%", "52% 22%", "50% 24%", "52% 22%", "50% 22%"]),
    intro: "A British pop artist known for sharp electronic textures, club energy, and restless reinvention. The 2025 control leans into her neon, kinetic side.",
  },
  2026: {
    artistKey: u("\\u5f90\\u4f73\\u83b9 (Lala Hsu)"),
    cn: u("\\u5f90\\u4f73\\u83b9"),
    en: "Lala Hsu",
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Lala_Hsu_in_2023_%282%29.jpg/500px-Lala_Hsu_in_2023_%282%29.jpg",
    images: artistImageList("output/artist-image-downloads-v1/084 - " + u("\\u5f90\\u4f73\\u83b9") + " (Lala Hsu)", ["01.jpg", "02.jpg", "03.jpg", "05.jpg"], ["68% 24%", "50% 22%", "50% 18%", "60% 22%"]),
    intro: "A Taiwanese singer-songwriter with a bright, expressive voice and lyrical warmth. This year feels open-air: gentle, horizon-facing, and sunlit.",
  },
};

const ARTIST_INFO_FALLBACK = [
  {
    Artist: "Charli xcx",
    CountryRegion: "British",
    Role: "singer-songwriter and pop artist",
    BriefArtistIntroEnglish: "British pop experimentalist. Her music sits at the intersection of glossy pop hooks, club culture, and restless electronic production. She co-wrote and featured on Icona Pop's \"I Love It\" in 2012, which topped the UK charts. She released her debut album True Romance in 2013 and later defined the hyperpop genre with Pop 2 (2017) and Charli (2019). Her forward-thinking production has influenced a generation of pop artists.",
    BriefArtistIntroChinese: "",
    Source: "https://en.wikipedia.org/wiki/Charli_XCX",
  },
  {
    Artist: u("\\u5f90\\u4f73\\u83b9 (Lala Hsu)"),
    CountryRegion: "Taiwanese",
    Role: "singer-songwriter",
    BriefArtistIntroEnglish: "Taiwanese singer-songwriter who won the Golden Melody Award for Best New Artist in 2010 and Best Mandarin Female Singer in 2018. Her style is intimate folk-pop with delicate melodic writing and emotionally honest lyrics. Hits include \"Lost in the City\" and \"The Body\".",
    BriefArtistIntroChinese: "",
    Source: "https://en.wikipedia.org/wiki/Lala_Hsu",
  },
  {
    Artist: u("\\u6613\\u70ca\\u5343\\u73ba (Jackson Yee)"),
    CountryRegion: "China",
    Role: u("\\u6b4c\\u624b\\u3001\\u6f14\\u5458\\u3001\\u821e\\u8005"),
    BriefArtistIntroEnglish: "Chinese singer, actor, and dancer. Joined TFBOYS in 2013. Solo music is known for conceptual depth and genre exploration. Album Liu Yanfen (2023) is a music novel blending jazz, Bossa Nova, waltz, indie rock, and ambient storytelling. Vocal delivery is gentle and narrative-driven.",
    BriefArtistIntroChinese: "",
    Source: "https://music.douban.com/review/15157095/; http://ent.ycwb.com/2023-05/14/content_51945232.htm",
  },
  {
    Artist: u("\\u6768\\u5b97\\u7eac (Aska Yang)"),
    CountryRegion: "Taiwanese",
    Role: "singer",
    BriefArtistIntroEnglish: "Taiwanese Mandopop singer who rose to fame in 2007 on One Million Star with his rich, emotional vocal style. His voice is distinctive with a nasal timbre, and he is known for heartfelt ballad interpretations. Hits include \"One Light\" and \"The Other Shore\".",
    BriefArtistIntroChinese: "",
    Source: "https://en.wikipedia.org/wiki/Aska_Yang",
  },
];

const state = {
  year: getInitialYear(),
  localAudioFiles: [],
  artistInfoByKey: new Map(),
  trackIndex: 0,
  playModeIndex: 2,
  playing: false,
  soundEnabled: queryParams.get("autoplay") === "1",
  soundChoiceSettled: queryParams.get("autoplay") === "1",
  volume: DEFAULT_MUSIC_VOLUME,
  listMotion: 0,
  singerImageIndex: 0,
  singerImageYear: null,
  singerImageKey: "",
  singerFadeLayer: 0,
  singerImageTimer: null,
  singerIntroText: "",
  singerIntroYear: null,
  singerIntroKey: "",
  singerIntroScrollFrame: null,
  singerIntroScrollTimer: null,
  singerIntroScrollLastTime: 0,
  singerIntroManualPauseUntil: 0,
  singerIntroScrollAttempts: 0,
  singerIntroResizeObserver: null,
  audioStartRequested: queryParams.get("autoplay") === "1",
  externalPlayback: null,
  preloadBlocked: queryParams.get("preload") === "1",
  applyingSharedPlayState: false,
  parentPlaybackStates: {},
  progressDragging: false,
};

const audio = document.querySelector("#controlAudio");
const songList = document.querySelector("#controlSongList");
const singerImages = [
  document.querySelector("#singerImage"),
  document.querySelector("#singerImageNext"),
];
const singerPanel = document.querySelector(".singer-panel");
const singerImageNameFallback = document.querySelector("#singerImageNameFallback");
const singerIntro = document.querySelector("#singerIntro");
const emptyState = document.querySelector("#emptyState");
const progressSlider = document.querySelector("#progressSlider");
const volumeSlider = document.querySelector("#volumeSlider");
const ecgMainPath = document.querySelector("#ecgMainPath");
const ecgShadowPath = document.querySelector("#ecgShadowPath");
const ecgBeatDot = document.querySelector("#ecgBeatDot");

const ecgState = {
  audioContext: null,
  analyser: null,
  source: null,
  frequencyData: null,
  timeData: null,
  energy: 0,
  bassEnergy: 0,
  midEnergy: 0,
  trebleEnergy: 0,
  bassAverage: 0.18,
  rhythmPulse: 0,
  lastOnsetAt: 0,
  lastBeatIndex: -1,
  flash: 0,
  beatPos: 0,
  lastFrameAt: 0,
  liveTempo: 0,
  onsetBpms: [],
  cssTempo: 0,
};

const songListDrag = {
  pointerId: null,
  startY: 0,
  lastY: 0,
  dragged: false,
  suppressClick: false,
  lastSwitchAt: 0,
  lockedAfterSwitch: false,
  wheelDelta: 0,
  lastWheelAt: 0,
};

init();

async function init() {
  initTrebleNoteCursor();
  const embedMode = queryParams.get("embed");
  if (embedMode) document.body.dataset.embed = embedMode;
  document.body.dataset.year = String(state.year);
  clearPlaybackStateOnRefresh();
  initSharedVolume();
  initSoundAndPlaybackMessaging();
  window.setLingerControlYear = setControlYear;
  bindEvents();
  await Promise.all([
    loadLocalMusic(),
    loadArtistInfoDatabase(),
  ]);
  restoreControlPlaybackState();
  render();
  if (!state.preloadBlocked && hasSoundChoice() && (queryParams.get("autoplay") === "1" || isMusicPlaybackRequested() || state.audioStartRequested)) {
    requestControlAudioStart();
  }
  preloadPausedPosition();
  state.singerImageTimer = window.setInterval(showNextSingerImage, ARTIST_IMAGE_ROTATE_MS);
  requestAnimationFrame(updateEcg);
}

function clampVolume(value) {
  return Math.max(0, Math.min(100, Math.round(Number(value) || 0)));
}

function readSharedVolume() {
  try {
    const saved = window.sessionStorage.getItem(SHARED_VOLUME_KEY);
    return saved === null ? DEFAULT_MUSIC_VOLUME : clampVolume(saved);
  } catch {
    return DEFAULT_MUSIC_VOLUME;
  }
}

function writeSharedVolume(value) {
  const volume = clampVolume(value);
  try {
    window.sessionStorage.setItem(SHARED_VOLUME_KEY, String(volume));
  } catch {
    // Session storage can be unavailable in some embedded/private contexts.
  }
  return volume;
}

function initSharedVolume() {
  state.volume = readSharedVolume();
  window.addEventListener("message", (event) => {
    if (event.data?.type === VOLUME_CHANGE_EVENT) {
      applySharedVolume(event.data.volume, { broadcast: false });
      return;
    }
    if (event.data?.type === MUSIC_PLAY_STATE_CHANGE_EVENT) {
      applySharedMusicPlayState(Boolean(event.data.playing));
    }
  });
  window.addEventListener("storage", (event) => {
    if (event.key === SHARED_VOLUME_KEY) {
      applySharedVolume(event.newValue, { broadcast: false });
      return;
    }
    if (event.key === MUSIC_PLAY_STATE_KEY) {
      applySharedMusicPlayState(event.newValue === "1");
    }
  });
}

function applySharedVolume(value, options = {}) {
  state.volume = writeSharedVolume(value);
  audio.volume = getYearAudioVolume();
  if (volumeSlider) volumeSlider.value = String(state.volume);
  renderRangeFills();
  if (options.broadcast !== false) broadcastSharedVolume();
}

function broadcastSharedVolume() {
  const message = { type: VOLUME_CHANGE_EVENT, volume: state.volume };
  window.parent?.postMessage(message, "*");
}

function getSoundChoice() {
  try {
    const choice = window.sessionStorage.getItem(SOUND_CHOICE_KEY);
    return choice === "on" || choice === "off" ? choice : null;
  } catch {
    return null;
  }
}

function writeSoundChoice(enabled) {
  try {
    window.sessionStorage.setItem(SOUND_CHOICE_KEY, enabled ? "on" : "off");
  } catch {
    // Session storage can be unavailable in private or embedded browsing contexts.
  }
}

function hasSoundChoice() {
  return state.soundChoiceSettled || getSoundChoice() !== null;
}

function isMusicAutoplayEnabled() {
  try {
    return window.sessionStorage.getItem(MUSIC_AUTOPLAY_KEY) === "1";
  } catch {
    return false;
  }
}

function isMusicPlaybackRequested() {
  try {
    const sessionValue = window.sessionStorage.getItem(MUSIC_PLAY_STATE_KEY);
    if (sessionValue === "1" || sessionValue === "0") return sessionValue === "1";
    return window.localStorage.getItem(MUSIC_PLAY_STATE_KEY) === "1";
  } catch {
    return false;
  }
}

function setMusicPlaybackRequested(playing, options = {}) {
  if (isMemoryEmbed()) {
    if (options.broadcast === false || state.applyingSharedPlayState) return;
    window.parent?.postMessage({ type: MUSIC_PLAY_STATE_CHANGE_EVENT, playing: Boolean(playing) }, "*");
    return;
  }
  try {
    window.sessionStorage.setItem(MUSIC_PLAY_STATE_KEY, playing ? "1" : "0");
    window.localStorage.setItem(MUSIC_PLAY_STATE_KEY, playing ? "1" : "0");
  } catch {
    // Session storage can be unavailable in some embedded/private contexts.
  }
  if (options.broadcast === false || state.applyingSharedPlayState) return;
  window.parent?.postMessage({ type: MUSIC_PLAY_STATE_CHANGE_EVENT, playing: Boolean(playing) }, "*");
}

function applySharedMusicPlayState(playing) {
  state.applyingSharedPlayState = true;
  setMusicPlaybackRequested(playing, { broadcast: false });
  try {
    if (playing) {
      requestControlAudioStart();
      return;
    }
    if (!audio.paused) audio.pause();
    state.playing = false;
    state.audioStartRequested = false;
    renderPlayback();
    renderProgress();
    saveControlPlaybackState();
  } finally {
    state.applyingSharedPlayState = false;
  }
}

function isPageRefresh() {
  const navigation = performance.getEntriesByType?.("navigation")?.[0];
  return navigation?.type === "reload";
}

function clearPlaybackStateOnRefresh() {
  if (queryParams.get("resetPlayback") !== "1" && !isPageRefresh()) return;
  try {
    [...Array(window.sessionStorage.length).keys()]
      .map((index) => window.sessionStorage.key(index))
      .filter((key) => key?.startsWith(PLAYBACK_KEY_PREFIX))
      .forEach((key) => window.sessionStorage.removeItem(key));
  } catch {
    // Session storage can be unavailable in some embedded/private contexts.
  }
}

function initSoundAndPlaybackMessaging() {
  applyControlSoundPreference();
  window.applyLingerControlSoundPreference = (enabled, choiceSettled = true) => {
    applyControlSoundPreference(enabled, { choiceSettled });
  };
  window.startLingerControlAudio = () => requestControlAudioStart();
  window.toggleLingerControlAudio = () => togglePlayback();
  window.addEventListener("message", (event) => {
    if (event.data?.type === SOUND_CHANGE_EVENT) {
      applyControlSoundPreference(Boolean(event.data.enabled), {
        choiceSettled: Boolean(event.data.choiceSettled),
      });
      return;
    }
    if (event.data?.type === MUSIC_COMMAND_EVENT && event.data.command === "start") {
      if (typeof event.data.enabled === "boolean") {
        applyControlSoundPreference(event.data.enabled, { choiceSettled: event.data.choiceSettled });
      }
      requestControlAudioStart();
      return;
    }
    if (event.data?.type === MUSIC_COMMAND_EVENT && event.data.command === "toggle") {
      togglePlayback();
      return;
    }
    if (event.data?.type === MUSIC_COMMAND_EVENT && event.data.command === "pause") {
      stopAudio();
      renderPlayback();
      return;
    }
    if (event.data?.type === YEAR_PARENT_PLAYBACK_EVENT) {
      applyParentPlaybackState(event.data);
      return;
    }
    if (event.data?.type === YEAR_PLAYBACK_RESTORE_EVENT) {
      applyParentPlaybackStates(event.data.states);
    }
  });
  window.addEventListener("pagehide", saveControlPlaybackState);
  window.addEventListener("beforeunload", saveControlPlaybackState);
}

function applyControlSoundPreference(enabled = getSoundChoice() === "on", options = {}) {
  const storedChoice = getSoundChoice();
  state.soundEnabled = Boolean(enabled);
  if (options.choiceSettled || state.soundEnabled) {
    writeSoundChoice(state.soundEnabled);
  }
  if (typeof options.choiceSettled === "boolean") {
    state.soundChoiceSettled = options.choiceSettled;
  } else if (storedChoice !== null) {
    state.soundChoiceSettled = true;
  }
  if (state.soundEnabled) state.soundChoiceSettled = true;
  audio.muted = !state.soundEnabled;
  if (!state.preloadBlocked && hasSoundChoice() && (isMusicPlaybackRequested() || state.audioStartRequested) && !state.playing) {
    requestControlAudioStart();
  }
}

function getPlaybackKey() {
  return `${PLAYBACK_KEY_PREFIX}${state.year}`;
}

function readControlPlaybackState() {
  try {
    const raw = window.sessionStorage.getItem(getPlaybackKey());
    if (raw) return JSON.parse(raw);
  } catch {
    // Session storage can be unavailable in some embedded/private contexts.
  }
  // Fall back to the copy the parent page keeps for this iframe (needed on
  // file:// pages, where the iframe loses its own storage between loads).
  return state.parentPlaybackStates?.[state.year] || {};
}

function saveControlPlaybackState() {
  const external = getExternalPlaybackState();
  const payload = {
    index: state.trackIndex,
    time: external ? external.currentTime : Number.isFinite(audio.currentTime) ? audio.currentTime : 0,
    playing: state.playing,
  };
  state.parentPlaybackStates[state.year] = payload;
  try {
    window.sessionStorage.setItem(getPlaybackKey(), JSON.stringify(payload));
  } catch {
    // Session storage can be unavailable in some embedded/private contexts.
  }
  if (window.parent && window.parent !== window) {
    try {
      window.parent.postMessage({ type: YEAR_PLAYBACK_SAVE_EVENT, year: state.year, ...payload }, "*");
    } catch {
      // The parent copy is an extra safety net; local state still works.
    }
  }
}

function applyParentPlaybackStates(states) {
  state.parentPlaybackStates = { ...(states || {}), ...state.parentPlaybackStates };
  const saved = state.parentPlaybackStates[state.year];
  if (!saved) return;
  let hasOwnState = false;
  try {
    hasOwnState = Boolean(window.sessionStorage.getItem(getPlaybackKey()));
  } catch {
    hasOwnState = false;
  }
  // If this iframe's own storage already restored the state, don't disturb it.
  if (hasOwnState) return;
  const tracks = getTracks();
  if (!tracks.length || !Number.isFinite(Number(saved.index))) return;
  // Only re-apply while nothing meaningful has played yet.
  if (state.playing && Number.isFinite(audio.currentTime) && audio.currentTime > 3) return;
  state.trackIndex = Math.max(0, Math.min(Number(saved.index), tracks.length - 1));
  const restoreTime = Math.max(0, Number(saved.time) || 0);
  if (restoreTime) {
    const apply = () => {
      if (Number.isFinite(audio.duration) && audio.duration > restoreTime + 1) {
        audio.currentTime = restoreTime;
        renderProgress();
      }
    };
    if (Number.isFinite(audio.duration) && audio.duration > 0) {
      apply();
    } else {
      audio.addEventListener("loadedmetadata", apply, { once: true });
    }
  }
  if (state.playing || state.audioStartRequested) {
    startAudio();
  } else {
    render();
    preloadPausedPosition();
  }
}

function restoreControlPlaybackState() {
  const saved = readControlPlaybackState();
  const tracks = getTracks();
  if (!tracks.length || !Number.isFinite(Number(saved.index))) return;
  state.trackIndex = Math.max(0, Math.min(Number(saved.index), tracks.length - 1));
  const restoreTime = Math.max(0, Number(saved.time) || 0);
  if (!restoreTime) return;
  const apply = () => {
    if (Number.isFinite(audio.duration) && audio.duration > restoreTime + 1) {
      audio.currentTime = restoreTime;
      renderProgress();
    }
  };
  audio.addEventListener("loadedmetadata", apply, { once: true });
}

function preloadPausedPosition() {
  // When arriving on a page with paused music, load the saved song so the
  // progress bar shows the paused position and play resumes from there.
  if (state.preloadBlocked || state.playing || state.audioStartRequested) return;
  const saved = readControlPlaybackState();
  if (Math.max(0, Number(saved.time) || 0) > 0) syncAudioSource();
}

function initTrebleNoteCursor() {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const trail = document.createElement("div");
  trail.className = "treble-cursor-trail";
  trail.setAttribute("aria-hidden", "true");

  const cursor = document.createElement("div");
  cursor.className = "treble-cursor is-hidden";
  cursor.setAttribute("aria-hidden", "true");
  cursor.innerHTML = `<img src="${TREBLE_CURSOR_ASSET}" alt="" draggable="false" />`;

  document.body.append(trail, cursor);
  document.documentElement.classList.add("has-treble-cursor");
  document.body.classList.add("has-treble-cursor");

  const liveParticles = [];
  let lastTrailAt = 0;
  let pressTimer = 0;
  const hoverSelector = "a, button, input, textarea, select, label, summary, [role='button'], [tabindex]:not([tabindex='-1'])";

  const removeParticle = (particle) => {
    const index = liveParticles.indexOf(particle);
    if (index >= 0) liveParticles.splice(index, 1);
    particle.remove();
  };

  const spawnParticle = (clientX, clientY) => {
    const now = window.performance?.now?.() ?? Date.now();
    if (now - lastTrailAt < 38) return;
    lastTrailAt = now;

    const particle = document.createElement("img");
    const asset = TREBLE_CURSOR_TRAIL_ASSETS[Math.floor(Math.random() * TREBLE_CURSOR_TRAIL_ASSETS.length)];
    const size = 12 + Math.random() * 10;
    const driftX = -18 - Math.random() * 28;
    const driftY = -26 - Math.random() * 38;
    const rotate = -14 + Math.random() * 28;

    particle.className = "treble-cursor-particle";
    particle.src = asset;
    particle.alt = "";
    particle.draggable = false;
    particle.style.setProperty("--particle-x", `${clientX - 6}px`);
    particle.style.setProperty("--particle-y", `${clientY - 8}px`);
    particle.style.setProperty("--particle-size", `${size.toFixed(1)}px`);
    particle.style.setProperty("--particle-drift-x", `${driftX.toFixed(1)}px`);
    particle.style.setProperty("--particle-drift-y", `${driftY.toFixed(1)}px`);
    particle.style.setProperty("--particle-rotate", `${rotate.toFixed(1)}deg`);

    trail.append(particle);
    liveParticles.push(particle);
    particle.addEventListener("animationend", () => removeParticle(particle), { once: true });

    while (liveParticles.length > 22) {
      removeParticle(liveParticles[0]);
    }
  };

  document.addEventListener("pointermove", (event) => {
    if (event.pointerType && event.pointerType !== "mouse") return;
    cursor.classList.remove("is-hidden");
    cursor.style.setProperty("--cursor-x", `${event.clientX - 7}px`);
    cursor.style.setProperty("--cursor-y", `${event.clientY - 6}px`);
    cursor.classList.toggle("is-hovering", Boolean(event.target?.closest?.(hoverSelector)));
    spawnParticle(event.clientX, event.clientY);
  }, { passive: true });

  document.addEventListener("pointerleave", () => {
    cursor.classList.add("is-hidden");
  });

  document.addEventListener("pointerdown", (event) => {
    if (event.pointerType && event.pointerType !== "mouse") return;
    window.clearTimeout(pressTimer);
    cursor.classList.add("is-pressing");
  }, { passive: true });

  document.addEventListener("pointerup", () => {
    window.clearTimeout(pressTimer);
    pressTimer = window.setTimeout(() => cursor.classList.remove("is-pressing"), 90);
  }, { passive: true });
}

function getInitialYear() {
  const year = Number(queryParams.get("year"));
  return YEARS.includes(year) ? year : 2026;
}

let gestureAudioRetryBound = false;

function scheduleGestureAudioRetry() {
  if (gestureAudioRetryBound) return;
  gestureAudioRetryBound = true;
  const retry = (event) => {
    document.removeEventListener("pointerdown", retry, true);
    document.removeEventListener("keydown", retry, true);
    gestureAudioRetryBound = false;
    // Let explicit transport interactions handle playback themselves.
    if (event.target?.closest?.(".transport-row button, .year-tabs button")) return;
    if (!state.playing && state.audioStartRequested && hasSoundChoice() && isMusicPlaybackRequested()) {
      startAudio();
    }
  };
  document.addEventListener("pointerdown", retry, true);
  document.addEventListener("keydown", retry, true);
}

function bindEvents() {
  document.addEventListener("keydown", (event) => {
    if (!isPlaybackSpaceKey(event) || shouldIgnorePlaybackKeyTarget(event.target)) return;
    event.preventDefault();
    togglePlayback();
  });

  // Resume the analyser context on the first available user gesture so the
  // ECG can read the real audio signal without ever muting playback.
  ["pointerdown", "keydown"].forEach((eventName) => {
    document.addEventListener(eventName, () => {
      if (!ENABLE_REAL_AUDIO_ANALYSER) return;
      if (ecgState.audioContext?.state === "suspended") {
        ecgState.audioContext.resume().then(() => setupAudioAnalyser()).catch(() => {});
      } else if (state.playing && !ecgState.source) {
        setupAudioAnalyser();
      }
    }, { passive: true });
  });

  document.querySelectorAll(".year-tabs button").forEach((button) => {
    button.addEventListener("click", () => {
      const year = Number(button.dataset.year);
      if (!YEARS.includes(year) || year === state.year) return;
      setControlYear(year, { autoplay: state.playing || state.audioStartRequested });
    });
  });

  document.querySelector("#playModeButton").addEventListener("click", () => {
    const nextMode = PLAY_MODES[(state.playModeIndex + 1) % PLAY_MODES.length];
    if (requestParentPlaybackCommand("mode", { mode: nextMode })) return;
    state.playModeIndex = (state.playModeIndex + 1) % PLAY_MODES.length;
    renderPlayback();
  });

  document.querySelector("#prevButton").addEventListener("click", () => {
    if (!requestParentPlaybackCommand("prev")) moveTrack(-1);
  });
  document.querySelector("#nextButton").addEventListener("click", () => {
    if (!requestParentPlaybackCommand("next")) moveTrack(1);
  });
  document.querySelector("#playButton").addEventListener("click", () => {
    if (!requestParentPlaybackCommand("toggle")) togglePlayback();
  });
  bindSongListDrag();
  bindSingerIntroScroll();

  volumeSlider.addEventListener("input", () => {
    applySharedVolume(volumeSlider.value);
  });

  // While the visitor drags the progress slider, playback must not keep
  // snapping the thumb back to the current time.
  progressSlider.addEventListener("pointerdown", () => {
    state.progressDragging = true;
  });
  ["pointerup", "pointercancel"].forEach((eventName) => {
    document.addEventListener(eventName, () => {
      state.progressDragging = false;
    });
  });
  progressSlider.addEventListener("change", () => {
    state.progressDragging = false;
  });

  progressSlider.addEventListener("input", () => {
    const external = getExternalPlaybackState();
    if (external) {
      requestParentPlaybackCommand("seek", {
        time: (Number(progressSlider.value) / 1000) * external.duration,
      });
      return;
    }
    if (!Number.isFinite(audio.duration) || audio.duration <= 0) {
      // No metadata yet (e.g. the song was never started on this page):
      // load the current track so the next drag can seek into it.
      syncAudioSource();
      return;
    }
    audio.currentTime = (Number(progressSlider.value) / 1000) * audio.duration;
    saveControlPlaybackState();
  });

  audio.addEventListener("timeupdate", () => {
    renderProgress();
    saveControlPlaybackState();
  });
  audio.addEventListener("loadedmetadata", renderProgress);
  audio.addEventListener("ended", handleEnded);
}

function isPlaybackSpaceKey(event) {
  return !event.repeat
    && !event.altKey
    && !event.ctrlKey
    && !event.metaKey
    && !event.shiftKey
    && (event.code === "Space" || event.key === " ");
}

function shouldIgnorePlaybackKeyTarget(target) {
  if (!target?.closest) return false;
  if (target.closest("textarea, select, [contenteditable='true']")) return true;
  const input = target.closest("input");
  return Boolean(input && input.type !== "range" && input.type !== "checkbox" && input.type !== "radio");
}

function bindSongListDrag() {
  songList.addEventListener("keydown", (event) => {
    handleSongListKeyboardEvent(event);
  });

  document.addEventListener("keydown", (event) => {
    if (songList.contains(document.activeElement)) return;
    if (!songList.matches(":hover")) return;
    handleSongListKeyboardEvent(event);
  });

  songList.addEventListener("wheel", (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    if (getTracks().length < 2) return;
    const direction = getSongListWheelDirection(event);
    if (!direction) return;
    event.preventDefault();
    moveTrackFromSongListInput(direction);
  }, { passive: false });

  songList.addEventListener("pointerdown", (event) => {
    if (event.button !== undefined && event.button !== 0) return;
    if (getTracks().length < 2) return;
    event.preventDefault();
    songListDrag.pointerId = event.pointerId;
    songListDrag.startY = event.clientY;
    songListDrag.lastY = event.clientY;
    songListDrag.dragged = false;
    songListDrag.lastSwitchAt = 0;
    songListDrag.lockedAfterSwitch = false;
    setSongListDragOffset(0);
    songList.classList.remove("drag-next", "drag-prev");
    songList.classList.add("dragging");
    songList.setPointerCapture?.(event.pointerId);
  });

  songList.addEventListener("pointermove", (event) => {
    if (songListDrag.pointerId !== event.pointerId) return;
    event.preventDefault();
    if (songListDrag.lockedAfterSwitch) return;
    const totalDelta = event.clientY - songListDrag.startY;
    const direction = totalDelta > 0 ? 1 : -1;
    const switchDistance = getSongListSwitchDistance(direction);
    const visualOffset = clamp(
      totalDelta * SONG_LIST_DRAG_SCALE,
      -switchDistance,
      switchDistance,
    );
    const dragProgress = switchDistance
      ? clamp(Math.abs(visualOffset) / switchDistance, 0, 1)
      : 0;
    songList.classList.toggle("drag-next", totalDelta > 2);
    songList.classList.toggle("drag-prev", totalDelta < -2);
    setSongListDragOffset(visualOffset, dragProgress);
    if (Math.abs(totalDelta) > 6) songListDrag.dragged = true;
    if (Math.abs(visualOffset) < switchDistance * SONG_LIST_SWITCH_RATIO) return;
    const now = performance.now();
    if (now - songListDrag.lastSwitchAt < 150) return;
    songListDrag.lastSwitchAt = now;
    songListDrag.startY = event.clientY;
    songListDrag.lastY = event.clientY;
    songListDrag.suppressClick = true;
    songListDrag.lockedAfterSwitch = true;
    songList.classList.remove("drag-next", "drag-prev");
    moveTrack(direction);
    window.requestAnimationFrame(() => {
      setSongListDragOffset(0);
    });
  });

  ["pointerup", "pointercancel", "lostpointercapture"].forEach((eventName) => {
    songList.addEventListener(eventName, (event) => {
      if (songListDrag.pointerId !== event.pointerId && eventName !== "lostpointercapture") return;
      if (songListDrag.dragged) {
        songListDrag.suppressClick = true;
        window.setTimeout(() => {
          songListDrag.suppressClick = false;
        }, 180);
      }
      songListDrag.pointerId = null;
      songListDrag.lockedAfterSwitch = false;
      songList.classList.remove("dragging", "drag-next", "drag-prev");
      setSongListDragOffset(0);
    });
  });
}

function handleSongListKeyboardEvent(event) {
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return false;
  const direction = getSongListKeyboardDirection(event);
  if (!direction || getTracks().length < 2) return false;
  event.preventDefault();
  moveTrackFromSongListInput(direction);
  return true;
}

function getSongListKeyboardDirection(event) {
  if (event.key === "ArrowUp" || event.key === "Up") return -1;
  if (event.key === "ArrowDown" || event.key === "Down") return 1;
  return 0;
}

function getSongListWheelDirection(event) {
  const delta = Math.abs(event.deltaY) >= Math.abs(event.deltaX) ? event.deltaY : event.deltaX;
  if (!delta) return 0;
  songListDrag.wheelDelta += delta;
  if (Math.abs(songListDrag.wheelDelta) < SONG_LIST_WHEEL_THRESHOLD) return 0;
  const now = performance.now();
  if (now - songListDrag.lastWheelAt < SONG_LIST_WHEEL_COOLDOWN_MS) return 0;
  songListDrag.lastWheelAt = now;
  const direction = songListDrag.wheelDelta > 0 ? 1 : -1;
  songListDrag.wheelDelta = 0;
  return direction;
}

function moveTrackFromSongListInput(direction) {
  const command = direction > 0 ? "next" : "prev";
  if (!requestParentPlaybackCommand(command)) moveTrack(direction);
}

function setSongListDragOffset(offset, progress = 0) {
  songList.style.setProperty("--drag-offset", `${offset.toFixed(1)}px`);
  songList.style.setProperty("--drag-progress", progress.toFixed(3));
  songList.style.setProperty("--drag-progress-percent", `${(progress * 100).toFixed(1)}%`);
  songList.style.setProperty("--leaving-scale", (1 - progress * 0.1).toFixed(3));
  songList.style.setProperty("--incoming-scale", (0.92 + progress * 0.08).toFixed(3));
  songList.style.setProperty("--leaving-opacity", (1 - progress * 0.2).toFixed(3));
  songList.style.setProperty("--leaving-active-pct", `${((1 - progress) * 100).toFixed(1)}%`);
  songList.style.setProperty("--incoming-active-pct", `${(progress * 100).toFixed(1)}%`);
}

function getSongListSwitchDistance(direction) {
  const rows = [...songList.querySelectorAll("li")];
  const activeRow = songList.querySelector("button.active")?.closest("li");
  const activeIndex = rows.indexOf(activeRow);
  const targetRow = rows[activeIndex - Math.sign(direction)];
  if (!activeRow || !targetRow) return 38;

  const activeRect = activeRow.querySelector("button")?.getBoundingClientRect();
  const targetTitleRect = targetRow.querySelector(".title")?.getBoundingClientRect();
  if (!activeRect || !targetTitleRect) return 38;

  const currentOffset = getSongListDragOffset();
  const targetTop = targetTitleRect.top - currentOffset;
  const targetBottom = targetTitleRect.bottom - currentOffset;
  const requiredDistance = direction > 0
    ? activeRect.top - targetTop
    : targetBottom - activeRect.bottom;
  return clamp(requiredDistance + 2, 16, 42);
}

function getSongListDragOffset() {
  return Number.parseFloat(songList.style.getPropertyValue("--drag-offset")) || 0;
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

async function loadLocalMusic() {
  let files = [];
  try {
    const response = await fetch("/api/local-music");
    if (!response.ok) throw new Error("Local music API unavailable");
    const data = await response.json();
    files = Array.isArray(data.files) ? data.files : [];
  } catch {
    files = [];
  }
  const remoteFiles = await getRemoteAudioManifestFiles();
  const manifestFiles = getAudioManifestFiles();
  files = preferWebAudioFiles(normalizeAudioManifestFiles([
    ...files,
    ...remoteFiles,
    ...manifestFiles,
  ]));
  state.localAudioFiles = files;
}

async function getRemoteAudioManifestFiles() {
  try {
    const response = await fetch("remote-audio.json", { cache: "no-store" });
    if (!response.ok) return [];
    const manifest = await response.json();
    return normalizeAudioManifestFiles(manifest?.files);
  } catch {
    return [];
  }
}

function getAudioManifestFiles() {
  const manifest = window.LINGER_AUDIO_MANIFEST;
  return normalizeAudioManifestFiles(manifest?.files);
}

function normalizeAudioManifestFiles(files) {
  if (!Array.isArray(files)) return [];
  return files
    .map((file) => {
      if (!file?.url) return null;
      const name = String(file.name || file.title || file.url.split("/").pop() || "").trim();
      const path = String(file.path || name).replace(/\\/g, "/").trim();
      if (!name || !path) return null;
      return {
        ...file,
        name,
        path,
        url: file.url,
      };
    })
    .filter(Boolean);
}

function preferWebAudioFiles(files) {
  const extensionRank = new Map([
    [".mp3", 7],
    [".m4a", 6],
    [".aac", 5],
    [".opus", 4],
    [".ogg", 3],
    [".wav", 2],
    [".flac", 1],
  ]);
  const bestByBasePath = new Map();
  files.forEach((file) => {
    const normalizedPath = String(file.path || file.name || "").replace(/\\/g, "/");
    const extension = normalizedPath.match(/\.[^./]+$/)?.[0]?.toLowerCase() || "";
    const key = normalizedPath.replace(/\.[^./]+$/, "").toLowerCase();
    const current = bestByBasePath.get(key);
    if (!current || (extensionRank.get(extension) || 0) > (extensionRank.get(current.extension) || 0)) {
      bestByBasePath.set(key, { file, extension });
    }
  });
  return [...bestByBasePath.values()].map((entry) => entry.file);
}

async function loadArtistInfoDatabase() {
  state.artistInfoByKey = createArtistInfoMap(ARTIST_INFO_FALLBACK);
  if (Array.isArray(window.LINGER_ARTIST_INFO_ROWS) && window.LINGER_ARTIST_INFO_ROWS.length) {
    state.artistInfoByKey = createArtistInfoMap(window.LINGER_ARTIST_INFO_ROWS);
    return;
  }
  try {
    const response = await fetch(ARTIST_INFO_CSV_PATH);
    if (!response.ok) return;
    const rows = parseCsv(await response.text());
    const liveMap = createArtistInfoMap(rows);
    if (liveMap.size) state.artistInfoByKey = liveMap;
  } catch {
    // Direct file:// views often block fetch; fallback rows are copied from the CSV.
  }
}

function createArtistInfoMap(rows) {
  const map = new Map();
  rows.forEach((row) => {
    if (!row?.Artist) return;
    artistLookupKeys(row.Artist).forEach((key) => map.set(key, row));
  });
  return map;
}

function artistLookupKeys(value) {
  const raw = String(value || "").trim();
  if (!raw) return [];
  const keys = new Set([normalizeArtistKey(raw)]);
  const parentheticalMatches = [...raw.matchAll(/\(([^()]+)\)/g)];
  parentheticalMatches.forEach((match) => keys.add(normalizeArtistKey(match[1])));

  let withoutLastParenthetical = raw;
  while (/\s*\([^()]+\)\s*$/.test(withoutLastParenthetical)) {
    withoutLastParenthetical = withoutLastParenthetical.replace(/\s*\([^()]+\)\s*$/, "").trim();
    keys.add(normalizeArtistKey(withoutLastParenthetical));
  }
  return [...keys].filter(Boolean);
}

function normalizeArtistKey(value) {
  return String(value || "")
    .normalize("NFKC")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let insideQuotes = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const nextChar = text[index + 1];

    if (insideQuotes) {
      if (char === "\"" && nextChar === "\"") {
        field += "\"";
        index += 1;
      } else if (char === "\"") {
        insideQuotes = false;
      } else {
        field += char;
      }
    } else if (char === "\"") {
      insideQuotes = true;
    } else if (char === ",") {
      row.push(field);
      field = "";
    } else if (char === "\n") {
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
    } else if (char !== "\r") {
      field += char;
    }
  }

  if (field || row.length) {
    row.push(field);
    rows.push(row);
  }

  const headers = rows.shift()?.map((header) => header.trim()) || [];
  return rows
    .filter((values) => values.some((value) => String(value).trim()))
    .map((values) => Object.fromEntries(headers.map((header, index) => [header, values[index] || ""])));
}

function getTracks(year = state.year) {
  const folderPrefix = `${year} music/`;
  const localTracks = state.localAudioFiles
    .filter((file) => {
      const path = String(file.path || "").replace(/\\/g, "/");
      return path.toLowerCase().startsWith(folderPrefix.toLowerCase()) && AUDIO_EXTENSIONS.test(file.name || path);
    })
    .map(fileToTrack);

  if (localTracks.length) return localTracks;
  return FALLBACK_TRACKS[year].map((track) => ({ ...track, audioSrc: "" }));
}

function fileToTrack(file) {
  const base = String(file.name || "").replace(/\.[^.]+$/, "");
  const parts = base.split(/\s+-\s+/);
  if (/^\d+$/.test(parts[0])) parts.shift();
  const [artist, ...titleParts] = parts;
  const title = titleParts.length ? titleParts.join(" - ").trim() : base;
  return {
    title,
    englishTitle: getEnglishTitleFromLookup(title),
    artist: titleParts.length ? artist.trim() : "Local Archive",
    audioSrc: file.url,
  };
}

function currentTrack() {
  const tracks = getTracks();
  state.trackIndex = Math.max(0, Math.min(state.trackIndex, tracks.length - 1));
  return tracks[state.trackIndex] || null;
}

function render() {
  renderTabs();
  renderSinger();
  renderSongList();
  renderPlayback();
  renderProgress();
  renderRangeFills();
}

function renderTabs() {
  document.querySelectorAll(".year-tabs button").forEach((button) => {
    button.classList.toggle("active", Number(button.dataset.year) === state.year);
  });
}

function renderSinger() {
  const singer = getCurrentSingerInfo();
  const singerKey = singer.lookupKey || singer.artistKey || singer.en || singer.cn || String(state.year);
  const name = [singer.cn, singer.en].filter(Boolean).join(" ");
  const imageNameFallback = singer.imageNameFallback || null;
  setSingerImageNameFallback(imageNameFallback);
  const sources = imageNameFallback ? [] : getSingerImageSources(singer);
  if (state.singerImageYear !== state.year || state.singerImageKey !== singerKey) {
    state.singerImageYear = state.year;
    state.singerImageKey = singerKey;
    state.singerImageIndex = 0;
    state.singerFadeLayer = 0;
    setSingerImageInstant(imageNameFallback ? null : sources[0], imageNameFallback ? "" : name);
  } else {
    singerImages.forEach((image, index) => {
      image.alt = !imageNameFallback && index === state.singerFadeLayer ? name : "";
    });
  }
  document.querySelector("#singerDisplayName").textContent = name;
  if (state.singerIntroText !== singer.intro || state.singerIntroYear !== state.year || state.singerIntroKey !== singerKey) {
    state.singerIntroText = singer.intro;
    state.singerIntroYear = state.year;
    state.singerIntroKey = singerKey;
    const textTrack = document.createElement("span");
    textTrack.className = "singer-intro-scroll";
    textTrack.textContent = singer.intro;
    singerIntro.replaceChildren(textTrack);
    resetSingerIntroAutoScroll();
  }
}

function getCurrentSingerInfo() {
  return getSingerInfoForTrack(currentTrack(), state.year);
}

function bindSingerIntroScroll() {
  ["wheel", "pointerdown", "touchstart", "keydown"].forEach((eventName) => {
    singerIntro.addEventListener(eventName, pauseSingerIntroAutoScroll, { passive: true });
  });
  if ("ResizeObserver" in window) {
    state.singerIntroResizeObserver = new ResizeObserver(() => {
      if (!state.singerIntroText) return;
      resetSingerIntroAutoScroll();
    });
    state.singerIntroResizeObserver.observe(singerIntro);
    state.singerIntroResizeObserver.observe(singerIntro.parentElement);
  }
}

function resetSingerIntroAutoScroll() {
  stopSingerIntroAutoScroll();
  state.singerIntroManualPauseUntil = 0;
  state.singerIntroScrollAttempts = 0;
  state.singerIntroScrollTimer = window.setTimeout(() => {
    window.requestAnimationFrame(refreshSingerIntroAutoScroll);
  }, SINGER_INTRO_SCROLL_START_MS);
}

function pauseSingerIntroAutoScroll() {
  state.singerIntroManualPauseUntil = performance.now() + SINGER_INTRO_MANUAL_PAUSE_MS;
  singerIntro.classList.add("is-paused");
  window.setTimeout(() => {
    if (performance.now() >= state.singerIntroManualPauseUntil) {
      singerIntro.classList.remove("is-paused");
    }
  }, SINGER_INTRO_MANUAL_PAUSE_MS + 20);
}

function stopSingerIntroAutoScroll() {
  if (state.singerIntroScrollFrame) {
    window.cancelAnimationFrame(state.singerIntroScrollFrame);
    state.singerIntroScrollFrame = null;
  }
  if (state.singerIntroScrollTimer) {
    window.clearTimeout(state.singerIntroScrollTimer);
    state.singerIntroScrollTimer = null;
  }
  state.singerIntroScrollLastTime = 0;
  singerIntro.classList.remove("is-scrollable", "is-paused");
  singerIntro.style.setProperty("--intro-scroll-distance", "0px");
}

function startSingerIntroAutoScroll() {
  refreshSingerIntroAutoScroll();
}

function refreshSingerIntroAutoScroll() {
  state.singerIntroScrollTimer = null;
  const scrollTrack = singerIntro.querySelector(".singer-intro-scroll");
  if (!scrollTrack || !singerIntroNeedsScroll()) {
    state.singerIntroScrollAttempts += 1;
    if (state.singerIntroScrollAttempts <= 6) {
      state.singerIntroScrollTimer = window.setTimeout(refreshSingerIntroAutoScroll, 450);
    }
    return;
  }
  state.singerIntroScrollAttempts = 0;
  const distance = Math.max(0, scrollTrack.scrollHeight - singerIntro.clientHeight + 8);
  const duration = Math.max(14, distance / SINGER_INTRO_SCROLL_SPEED + 5);
  singerIntro.style.setProperty("--intro-scroll-distance", `${distance.toFixed(1)}px`);
  singerIntro.style.setProperty("--intro-scroll-duration", `${duration.toFixed(1)}s`);
  singerIntro.classList.add("is-scrollable");
}

function singerIntroNeedsScroll() {
  const scrollTrack = singerIntro.querySelector(".singer-intro-scroll");
  return Boolean(scrollTrack && scrollTrack.scrollHeight > singerIntro.clientHeight + 2);
}

function stepSingerIntroAutoScroll(timestamp) {
  if (!singerIntroNeedsScroll()) {
    stopSingerIntroAutoScroll();
    return;
  }

  if (timestamp < state.singerIntroManualPauseUntil) {
    state.singerIntroScrollLastTime = timestamp;
    state.singerIntroScrollFrame = window.requestAnimationFrame(stepSingerIntroAutoScroll);
    return;
  }

  if (!state.singerIntroScrollLastTime) state.singerIntroScrollLastTime = timestamp;
  const elapsedSeconds = (timestamp - state.singerIntroScrollLastTime) / 1000;
  state.singerIntroScrollLastTime = timestamp;
  const maxScrollTop = singerIntro.scrollHeight - singerIntro.clientHeight;

  if (singerIntro.scrollTop >= maxScrollTop - 1) {
    stopSingerIntroAutoScroll();
    state.singerIntroScrollTimer = window.setTimeout(() => {
      singerIntro.scrollTop = 0;
      state.singerIntroScrollTimer = window.setTimeout(startSingerIntroAutoScroll, SINGER_INTRO_SCROLL_PAUSE_MS);
    }, SINGER_INTRO_SCROLL_PAUSE_MS);
    return;
  }

  singerIntro.scrollTop = Math.min(maxScrollTop, singerIntro.scrollTop + elapsedSeconds * SINGER_INTRO_SCROLL_SPEED);
  state.singerIntroScrollFrame = window.requestAnimationFrame(stepSingerIntroAutoScroll);
}

function getSingerInfoForYear(year) {
  const base = SINGER_INFO[year];
  const databaseRow = getArtistInfoRow(base.artistKey || base.en || base.cn);
  if (!databaseRow) return base;

  return mergeSingerInfo(base, databaseRow);
}

function getSingerInfoForTrack(track, year) {
  const base = SINGER_INFO[year];
  const primaryArtist = getPrimaryArtistName(track?.artist);
  const databaseRow = getArtistInfoRow(primaryArtist);
  const imageNameFallback = getArtistImageNameFallback(primaryArtist, databaseRow?.Artist);
  const imageFrames = imageNameFallback ? [] : getArtistImageFrames(primaryArtist);
  if (!databaseRow) {
    const parsedName = parseArtistDisplayName(primaryArtist || base.artistKey || base.en || base.cn);
    return {
      ...base,
      cn: parsedName.cn,
      en: parsedName.en,
      images: imageFrames.length ? imageFrames : imageNameFallback ? [] : base.images,
      image: imageFrames[0]?.src || (imageNameFallback ? "" : base.image),
      imageNameFallback,
      intro: primaryArtist ? `${primaryArtist} is the artist for the current song.` : base.intro,
      lookupKey: normalizeArtistKey(primaryArtist || base.artistKey || base.en || base.cn),
    };
  }

  const merged = mergeSingerInfo(base, databaseRow);

  return {
    ...merged,
    images: imageFrames.length ? imageFrames : imageNameFallback ? [] : merged.images,
    image: imageFrames[0]?.src || (imageNameFallback ? "" : merged.image),
    imageNameFallback,
    lookupKey: normalizeArtistKey(primaryArtist),
  };
}

function getPrimaryArtistName(artist) {
  const raw = String(artist || "").trim();
  if (!raw) return "";
  return raw.split(/\s*(?:,|，|、|\/|&|\+)\s*/).find(Boolean)?.trim() || raw;
}

function getArtistImageNameFallback(...artistValues) {
  for (const value of artistValues.filter(Boolean)) {
    for (const key of artistLookupKeys(value)) {
      const fallback = ARTIST_IMAGE_NAME_FALLBACKS.get(key);
      if (fallback) return fallback;
    }
  }
  return null;
}

function getArtistImageFrames(artist) {
  const manifest = window.LINGER_ARTIST_IMAGE_MANIFEST;
  const artists = Array.isArray(manifest?.artists) ? manifest.artists : [];
  if (!artist || !artists.length) return [];
  const lookupKeys = new Set(artistLookupKeys(artist));
  const match = artists.find((entry) => artistLookupKeys(entry.name).some((key) => lookupKeys.has(key)));
  return Array.isArray(match?.images) ? match.images.filter((image) => image?.src) : [];
}

function mergeSingerInfo(base, databaseRow) {
  const parsedName = parseArtistDisplayName(databaseRow.Artist);
  const displayOverride = getArtistDisplayOverride(databaseRow.Artist);
  const hasParsedName = Boolean(parsedName.cn || parsedName.en);
  return {
    ...base,
    cn: displayOverride?.cn ?? parsedName.cn ?? (hasParsedName ? "" : base.cn),
    en: displayOverride?.en ?? parsedName.en ?? base.en,
    intro: databaseRow.BriefArtistIntroEnglish || base.intro,
    introChinese: databaseRow.BriefArtistIntroChinese || "",
    countryRegion: databaseRow.CountryRegion || "",
    role: databaseRow.Role || "",
    source: databaseRow.Source || "",
  };
}

function getArtistDisplayOverride(value) {
  return artistLookupKeys(value)
    .map((key) => ARTIST_DISPLAY_OVERRIDES[key])
    .find(Boolean) || null;
}

function getArtistInfoRow(value) {
  return artistLookupKeys(value).map((key) => state.artistInfoByKey.get(key)).find(Boolean) || null;
}

function parseArtistDisplayName(value) {
  const raw = String(value || "").trim();
  const match = raw.match(/^(.*?)\s*\(([^()]+)\)\s*$/);
  if (!match) {
    return hasChineseText(raw) ? { cn: raw, en: "" } : { cn: "", en: raw };
  }
  const cn = match[1].replace(new RegExp(`\\s*\\(${escapeRegExp(match[2])}\\)\\s*$`), "").trim();
  return {
    cn: hasChineseText(cn) ? cn : "",
    en: match[2].trim(),
  };
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function getSingerImageSources(singer) {
  const images = Array.isArray(singer.images) ? singer.images.filter(Boolean) : [];
  const sources = images.length ? images : [singer.image].filter(Boolean);
  return sources.map(normalizeSingerImageFrame);
}

function normalizeSingerImageFrame(image) {
  if (typeof image === "string") {
    return { src: image, position: "50% 18%", scale: 1.28 };
  }
  return {
    src: image.src || "",
    position: image.position || "50% 18%",
    scale: image.scale || 1.28,
  };
}

function setSingerImageInstant(frame, alt) {
  singerImages.forEach((image, index) => {
    image.src = frame?.src || "";
    image.alt = index === 0 ? alt : "";
    image.style.setProperty("--artist-image-position", frame?.position || "50% 18%");
    image.style.setProperty("--artist-image-scale", String(frame?.scale || 1.28));
    image.classList.toggle("active", index === 0);
  });
}

function setSingerImageNameFallback(fallback) {
  singerPanel?.classList.toggle("has-name-fallback", Boolean(fallback));
  if (!singerImageNameFallback) return;
  singerImageNameFallback.querySelector(".singer-image-name-cn").textContent = fallback?.cn || "";
  singerImageNameFallback.querySelector(".singer-image-name-en").textContent = fallback?.en || "";
  singerImageNameFallback.setAttribute("aria-hidden", fallback ? "false" : "true");
}

function showNextSingerImage() {
  const year = state.year;
  const singer = getCurrentSingerInfo();
  if (singer.imageNameFallback) return;
  const singerKey = singer.lookupKey || singer.artistKey || singer.en || singer.cn || String(state.year);
  const sources = getSingerImageSources(singer);
  if (sources.length < 2) return;

  const nextIndex = (state.singerImageIndex + 1) % sources.length;
  const nextFrame = sources[nextIndex];
  const nextLayer = state.singerFadeLayer ? 0 : 1;
  const currentLayer = state.singerFadeLayer;
  const nextImage = singerImages[nextLayer];
  const currentImage = singerImages[currentLayer];
  const name = [singer.cn, singer.en].filter(Boolean).join(" ");

  const preload = new Image();
  preload.onload = () => {
    if (state.year !== year || state.singerImageKey !== singerKey) return;
    nextImage.src = nextFrame.src;
    nextImage.alt = name;
    nextImage.style.setProperty("--artist-image-position", nextFrame.position);
    nextImage.style.setProperty("--artist-image-scale", String(nextFrame.scale || 1.28));
    window.requestAnimationFrame(() => {
      nextImage.classList.add("active");
      currentImage.classList.remove("active");
      window.setTimeout(() => {
        if (!currentImage.classList.contains("active")) currentImage.alt = "";
      }, ARTIST_IMAGE_FADE_MS);
    });
    state.singerImageIndex = nextIndex;
    state.singerFadeLayer = nextLayer;
  };
  preload.src = nextFrame.src;
}

function renderSongList() {
  const tracks = getTracks();
  document.querySelector("#musicListTitle").textContent = `${state.year} MUSIC LIST`;
  const visibleTracks = getVisibleSongList(tracks);
  const currentVisibleIndex = visibleTracks.findIndex(({ index }) => index === state.trackIndex);
  songList.classList.remove("slide-up", "slide-down");
  if (state.listMotion) {
    songList.classList.add(state.listMotion > 0 ? "slide-down" : "slide-up");
  }
  songList.replaceChildren(...visibleTracks.map(({ track, index, offset, isBuffer }, visibleIndex) => {
    const item = document.createElement("li");
    if (isBuffer) {
      item.className = offset < 0 ? "song-buffer song-buffer-before" : "song-buffer song-buffer-after";
    }
    item.style.setProperty("--row-delay", `${Math.abs(offset ?? index - state.trackIndex) * 34}ms`);
    const button = document.createElement("button");
    button.type = "button";
    const positionClass = typeof offset === "number"
      ? getSongListPositionClass(offset)
      : visibleIndex < currentVisibleIndex
        ? "list-position-prev"
        : visibleIndex > currentVisibleIndex
          ? "list-position-next"
          : "list-position-current";
    button.className = [positionClass, index === state.trackIndex ? "active" : ""].filter(Boolean).join(" ");
    button.innerHTML = `
      <span class="num">${index + 1}</span>
      <span class="title"><span class="title-cn"></span><span class="title-en"></span></span>
      <span class="bars" aria-hidden="true">${index === state.trackIndex ? "<i></i><i></i><i></i>" : ""}</span>
    `;
    button.querySelector(".title-cn").textContent = track.title;
    const englishTitle = getEnglishTitle(track);
    const englishLine = button.querySelector(".title-en");
    englishLine.textContent = englishTitle;
    englishLine.hidden = !englishTitle;
    button.title = `${track.title} - ${track.artist}`;
    if (!isBuffer) {
      button.addEventListener("click", (event) => {
        if (songListDrag.suppressClick) {
          event.preventDefault();
          event.stopPropagation();
          return;
        }
        state.listMotion = getTrackMotion(index, state.trackIndex, tracks.length);
        state.trackIndex = index;
        if (requestParentPlaybackCommand("select", { index })) {
          render();
          return;
        }
        if (state.playing) {
          startAudio();
        } else {
          syncAudioSource();
          render();
          saveControlPlaybackState();
        }
      });
    }
    item.append(button);
    return item;
  }));

  const localCount = getTracks().filter((track) => track.audioSrc).length;
  emptyState.textContent = document.body.dataset.embed === "memory"
    ? ""
    : localCount
      ? `${state.year} controller is using ${localCount} local audio file${localCount === 1 ? "" : "s"}.`
      : `Demo track list shown. Add audio files to assets/audio/${state.year} music/ to make this year play real music.`;
  state.listMotion = 0;
}

function getVisibleSongList(tracks) {
  if (tracks.length <= 3) {
    return tracks.map((track, index) => ({
      track,
      index,
      offset: index - state.trackIndex,
      isBuffer: false,
    })).reverse();
  }

  const currentIndex = state.trackIndex;
  return [2, 1, 0, -1, -2].map((offset) => {
    const index = (currentIndex + offset + tracks.length) % tracks.length;
    return { track: tracks[index], index, offset, isBuffer: Math.abs(offset) > 1 };
  });
}

function getSongListPositionClass(offset) {
  if (offset < -1) return "list-position-prev-extra";
  if (offset < 0) return "list-position-prev";
  if (offset > 1) return "list-position-next-extra";
  if (offset > 0) return "list-position-next";
  return "list-position-current";
}

function getTrackMotion(nextIndex, currentIndex, total) {
  if (nextIndex === currentIndex || total <= 1) return 0;
  const forward = (nextIndex - currentIndex + total) % total;
  const backward = (currentIndex - nextIndex + total) % total;
  return forward <= backward ? 1 : -1;
}

function getEnglishTitle(track) {
  if (!hasChineseText(track?.title)) return "";
  return track.englishTitle || getEnglishTitleFromLookup(track.title);
}

function renderPlayback() {
  const track = currentTrack();
  renderCurrentTitle(track);
  document.querySelector(".playback-panel").style.setProperty("--beat-duration", `${60 / getTrackTempo(track)}s`);
  const mode = PLAY_MODES[state.playModeIndex];
  const modeButton = document.querySelector("#playModeButton");
  modeButton.innerHTML = PLAY_MODE_ICONS[mode];
  modeButton.setAttribute("aria-label", `Play mode: ${PLAY_MODE_LABELS[mode].toLowerCase()}`);
  modeButton.title = PLAY_MODE_LABELS[mode].toLowerCase();
  const playButton = document.querySelector("#playButton");
  playButton.querySelector("span").textContent = state.playing ? "II" : String.fromCharCode(9654);
  playButton.setAttribute("aria-label", state.playing ? "Pause" : "Play");

  const hasAudio = Boolean(track?.audioSrc);
  document.querySelector("#prevButton").disabled = getTracks().length < 2;
  document.querySelector("#nextButton").disabled = getTracks().length < 2;
  playButton.disabled = !hasAudio;
  progressSlider.disabled = !hasAudio;
}

function getTrackTempo(track = currentTrack()) {
  const baseTempo = track
    ? (track.tempo || TEMPO_BY_TITLE[track.title] || DEFAULT_TEMPO_BY_YEAR[state.year] || 90)
    : (DEFAULT_TEMPO_BY_YEAR[state.year] || 90);
  // Prefer the tempo measured from the actual audio signal while it plays.
  if (state.playing && ecgState.analyser && ecgState.liveTempo) {
    return ecgState.liveTempo;
  }
  return baseTempo;
}

function getCurrentTitleText(track) {
  const englishTitle = getEnglishTitle(track);
  return englishTitle ? `${track.title} / ${englishTitle}` : track.title;
}

function renderCurrentTitle(track) {
  const title = document.querySelector("#currentSongTitle");
  title.replaceChildren();

  if (!track) {
    title.textContent = "No local music";
    return;
  }

  const englishTitle = getEnglishTitle(track);
  const cnSpan = document.createElement("span");
  cnSpan.className = hasChineseText(track.title) ? "current-title-cn" : "current-title-en";
  cnSpan.textContent = track.title;
  title.append(cnSpan);

  if (!englishTitle) return;

  const separator = document.createElement("span");
  separator.className = "current-title-separator";
  separator.textContent = " / ";
  title.append(separator);

  const enSpan = document.createElement("span");
  enSpan.className = "current-title-en";
  enSpan.textContent = englishTitle;
  title.append(enSpan);
}

function renderProgress() {
  const external = getExternalPlaybackState();
  const currentTime = external ? external.currentTime : audio.currentTime;
  const duration = external ? external.duration : audio.duration;
  const hasDuration = Number.isFinite(duration) && duration > 0;
  const percent = hasDuration ? Math.max(0, Math.min(1, currentTime / duration)) : 0;
  // Never move the thumb under the visitor's finger while they drag it.
  if (!state.progressDragging) {
    progressSlider.value = String(Math.round(percent * 1000));
  }
  document.querySelector("#currentTime").textContent = hasDuration ? formatTime(currentTime) : "0:00";
  document.querySelector("#durationTime").textContent = hasDuration ? formatTime(duration) : "0:00";
  renderRangeFills();
}

function applyParentPlaybackState(data) {
  if (Number(data.year) !== state.year) return;
  const previousIndex = state.trackIndex;
  state.externalPlayback = {
    active: Boolean(data.active),
    bridge: Boolean(data.bridge),
    currentTime: Math.max(0, Number(data.currentTime) || 0),
    duration: Math.max(0, Number(data.duration) || 0),
    playing: Boolean(data.playing),
    year: Number(data.year),
  };
  if (Number.isFinite(Number(data.index))) {
    state.trackIndex = Math.max(0, Math.min(Number(data.index), getTracks().length - 1));
  }
  if (PLAY_MODES.includes(data.playMode)) {
    state.playModeIndex = PLAY_MODES.indexOf(data.playMode);
  }
  state.playing = Boolean(data.playing);
  if (state.trackIndex !== previousIndex) {
    renderSinger();
    renderSongList();
  }
  renderPlayback();
  renderProgress();
  renderRangeFills();
}

function getExternalPlaybackState() {
  if (!state.externalPlayback?.active || state.externalPlayback.year !== state.year) return null;
  return state.externalPlayback;
}

function isMemoryEmbed() {
  return document.body.dataset.embed === "memory";
}

function setControlYear(year, options = {}) {
  const nextYear = Number(year);
  if (!YEARS.includes(nextYear)) return false;
  const shouldAutoplay = Boolean(options.autoplay || state.playing || state.audioStartRequested || isMusicPlaybackRequested());
  state.preloadBlocked = false;
  if (nextYear === state.year) {
    if (shouldAutoplay) requestControlAudioStart();
    return true;
  }

  saveControlPlaybackState();
  if (!audio.paused) audio.pause();
  state.playing = false;
  state.audioStartRequested = shouldAutoplay;
  state.externalPlayback = null;
  state.year = nextYear;
  state.trackIndex = 0;
  state.listMotion = 0;
  document.body.dataset.year = String(nextYear);
  if (audio.src) {
    audio.removeAttribute("src");
    audio.load();
  }
  restoreControlPlaybackState();
  render();
  if (shouldAutoplay) requestControlAudioStart();
  preloadPausedPosition();
  return true;
}

function requestParentPlaybackCommand(command, payload = {}) {
  const external = getExternalPlaybackState();
  if (isMemoryEmbed()) return false;
  if (!isMemoryEmbed() && !external?.bridge) return false;
  if (!isMemoryEmbed()) {
    if (command === "play") setMusicPlaybackRequested(true);
    if (command === "pause") setMusicPlaybackRequested(false);
    if (command === "toggle") setMusicPlaybackRequested(!state.playing);
  }
  window.parent?.postMessage({
    type: YEAR_PARENT_COMMAND_EVENT,
    year: state.year,
    command,
    ...payload,
  }, "*");
  return true;
}

function applyOptimisticParentCommand(command, payload = {}) {
  const tracks = getTracks();
  if (!tracks.length) return;
  if (command === "select" && Number.isFinite(Number(payload.index))) {
    state.trackIndex = Math.max(0, Math.min(Number(payload.index), tracks.length - 1));
    state.externalPlayback = { active: true, currentTime: 0, duration: 0, playing: true, year: state.year };
    state.playing = true;
    render();
    return;
  }
  if (command === "prev" || command === "next") {
    const direction = command === "next" ? 1 : -1;
    state.trackIndex = getNextTrackIndex(direction, tracks, { manual: true });
    state.externalPlayback = { active: true, currentTime: 0, duration: 0, playing: state.playing, year: state.year };
    render();
    return;
  }
  if (command === "mode") {
    const requestedMode = PLAY_MODES.find((mode) => mode === payload.mode);
    if (requestedMode) state.playModeIndex = PLAY_MODES.indexOf(requestedMode);
    renderPlayback();
    return;
  }
  if (command === "toggle") {
    state.playing = !state.playing;
    renderPlayback();
  }
}

function renderRangeFills() {
  volumeSlider.value = String(state.volume);
  progressSlider.style.setProperty("--progress", `${Number(progressSlider.value) / 10}%`);
  volumeSlider.style.setProperty("--volume", `${state.volume}%`);
}

function formatTime(seconds) {
  const safeSeconds = Math.max(0, Math.floor(seconds || 0));
  const minutes = Math.floor(safeSeconds / 60);
  return `${minutes}:${String(safeSeconds % 60).padStart(2, "0")}`;
}

function syncAudioSource() {
  const track = currentTrack();
  if (!track?.audioSrc) return false;
  audio.volume = getYearAudioVolume();
  const resolved = new URL(track.audioSrc, window.location.href).href;
  if (audio.src !== resolved) {
    if (!audio.paused) audio.pause();
    audio.src = track.audioSrc;
    audio.load();
    // A new song means a new rhythm: re-learn tempo from its audio signal.
    ecgState.liveTempo = 0;
    ecgState.onsetBpms.length = 0;
  }
  return true;
}

function getYearAudioVolume() {
  return (state.volume / 100) * YEAR_MUSIC_MAX_GAIN;
}

function requestControlAudioStart() {
  if (state.preloadBlocked) return false;
  state.audioStartRequested = true;
  setMusicPlaybackRequested(true);
  return startAudio();
}

async function startAudio() {
  if (!hasSoundChoice()) {
    state.playing = false;
    render();
    postPlaybackStatus(false);
    return false;
  }
  if (!syncAudioSource()) {
    state.playing = false;
    render();
    postPlaybackStatus(false);
    return false;
  }
  let started = false;
  const wantsAudiblePlayback = state.soundEnabled;
  const hasUserActivation = navigator.userActivation ? navigator.userActivation.isActive : false;
  try {
    // Without a user gesture, start muted so autoplay policies allow playback.
    audio.muted = hasUserActivation ? !wantsAudiblePlayback : true;
    await audio.play();
    state.playing = true;
    state.audioStartRequested = true;
    audio.muted = !wantsAudiblePlayback;
    started = true;
    try {
      if (ecgState.audioContext?.state === "suspended") {
        await ecgState.audioContext.resume().catch(() => {});
      }
      setupAudioAnalyser();
    } catch {
      // Playback should still start even if the visual analyser is blocked.
    }
  } catch {
    state.playing = false;
    audio.muted = !state.soundEnabled;
    scheduleGestureAudioRetry();
  }
  render();
  saveControlPlaybackState();
  postPlaybackStatus(started);
  return started;
}

function postPlaybackStatus(started) {
  window.parent?.postMessage({
    type: YEAR_CONTROL_PLAYBACK_EVENT,
    year: state.year,
    embed: isMemoryEmbed(),
    started: Boolean(started),
    playing: state.playing,
  }, "*");
}

function setupAudioAnalyser() {
  if (!ENABLE_REAL_AUDIO_ANALYSER || ecgState.source) return;
  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  if (!AudioContextClass) return;
  ecgState.audioContext ||= new AudioContextClass();
  const context = ecgState.audioContext;
  if (context.state === "suspended") {
    context.resume().catch(() => {});
  }
  // Never reroute the audio element through a context that is not running,
  // otherwise playback becomes silent while the context stays suspended.
  if (context.state !== "running") return;
  try {
    ecgState.analyser = context.createAnalyser();
    ecgState.analyser.fftSize = 256;
    ecgState.analyser.smoothingTimeConstant = 0.54;
    ecgState.frequencyData = new Uint8Array(ecgState.analyser.frequencyBinCount);
    ecgState.timeData = new Uint8Array(ecgState.analyser.fftSize);
    ecgState.source = context.createMediaElementSource(audio);
    ecgState.source.connect(ecgState.analyser);
    ecgState.analyser.connect(context.destination);
  } catch {
    // Keep default element output; the synthetic ECG fallback still runs.
    ecgState.analyser = null;
  }
}

function updateEcg() {
  const track = currentTrack();
  const tempo = getTrackTempo(track);
  const beatDuration = 60 / tempo;
  const now = performance.now() / 1000;
  const dt = ecgState.lastFrameAt ? Math.min(0.1, now - ecgState.lastFrameAt) : 0;
  ecgState.lastFrameAt = now;
  // Integrate the beat position so tempo changes stay visually continuous.
  ecgState.beatPos += (dt / beatDuration) * (state.playing ? 1 : 0.55);
  const metrics = readAudioMetrics();
  // Gently pull the beat grid into phase with real detected onsets.
  if (metrics.onset) {
    const phase = ecgState.beatPos - Math.floor(ecgState.beatPos);
    ecgState.beatPos += phase > 0.5 ? (1 - phase) * 0.35 : -phase * 0.35;
  }
  const beatPosition = ecgState.beatPos;
  const beatIndex = Math.floor(beatPosition);
  const beatPhase = beatPosition - beatIndex;
  // Keep the CSS pulse animation in step with the measured tempo.
  if (Math.abs(tempo - ecgState.cssTempo) > 3) {
    ecgState.cssTempo = tempo;
    document.querySelector(".playback-panel")?.style.setProperty("--beat-duration", `${(60 / tempo).toFixed(3)}s`);
  }

  if (beatIndex !== ecgState.lastBeatIndex) {
    ecgState.lastBeatIndex = beatIndex;
    ecgState.flash = state.playing ? 1 : 0.56;
  }

  if (metrics.onset) ecgState.flash = 0.82;

  const beatKick = Math.max(0, 1 - beatPhase * 3.1);
  const targetEnergy = state.playing
    ? Math.max(metrics.energy * 0.72, metrics.bass * 0.68, beatKick * 0.26)
    : beatKick * 0.16;
  ecgState.energy += (targetEnergy - ecgState.energy) * 0.16;
  ecgState.bassEnergy += (metrics.bass - ecgState.bassEnergy) * 0.16;
  ecgState.midEnergy += (metrics.mid - ecgState.midEnergy) * 0.14;
  ecgState.trebleEnergy += (metrics.treble - ecgState.trebleEnergy) * 0.1;
  ecgState.rhythmPulse = Math.max(beatKick * 0.42, metrics.onset ? 0.58 : ecgState.rhythmPulse * 0.9);
  ecgState.flash *= 0.91;

  drawEcg(beatPosition, tempo, {
    energy: ecgState.energy,
    bass: ecgState.bassEnergy,
    mid: ecgState.midEnergy,
    treble: ecgState.trebleEnergy,
    pulse: ecgState.rhythmPulse,
    flash: ecgState.flash,
  });
  requestAnimationFrame(updateEcg);
}

function readAudioMetrics() {
  if (!state.playing) {
    return { energy: 0, bass: 0, mid: 0, treble: 0, onset: false };
  }
  if (!ecgState.analyser || !ecgState.frequencyData || !ecgState.timeData || ecgState.audioContext?.state === "suspended") {
    return readSyntheticAudioMetrics();
  }
  ecgState.analyser.getByteFrequencyData(ecgState.frequencyData);
  ecgState.analyser.getByteTimeDomainData(ecgState.timeData);
  const bins = ecgState.frequencyData;
  const bass = averageBins(bins, 1, Math.max(4, Math.floor(bins.length * 0.12)));
  const mid = averageBins(bins, Math.floor(bins.length * 0.12), Math.floor(bins.length * 0.48));
  const treble = averageBins(bins, Math.floor(bins.length * 0.48), bins.length);
  let rms = 0;
  for (let index = 0; index < ecgState.timeData.length; index += 1) {
    const value = (ecgState.timeData[index] - 128) / 128;
    rms += value * value;
  }
  rms = Math.sqrt(rms / ecgState.timeData.length);
  const energy = Math.min(1, rms * 2.6 + bass * 0.35 + mid * 0.18);
  ecgState.bassAverage += (bass - ecgState.bassAverage) * 0.035;
  const now = performance.now();
  const onset = bass > Math.max(0.2, ecgState.bassAverage * 1.36) && now - ecgState.lastOnsetAt > 220;
  if (onset) {
    updateLiveTempo(now - ecgState.lastOnsetAt);
    ecgState.lastOnsetAt = now;
  }
  return { energy, bass, mid, treble, onset };
}

function updateLiveTempo(gapMs) {
  if (!Number.isFinite(gapMs) || gapMs < 240 || gapMs > 2400) return;
  let bpm = 60000 / gapMs;
  while (bpm < 65) bpm *= 2;
  while (bpm > 170) bpm /= 2;
  ecgState.onsetBpms.push(bpm);
  if (ecgState.onsetBpms.length > 9) ecgState.onsetBpms.shift();
  if (ecgState.onsetBpms.length < 4) return;
  const sorted = [...ecgState.onsetBpms].sort((a, b) => a - b);
  const median = sorted[Math.floor(sorted.length / 2)];
  ecgState.liveTempo = ecgState.liveTempo
    ? ecgState.liveTempo + (median - ecgState.liveTempo) * 0.25
    : median;
}

function readSyntheticAudioMetrics() {
  const tempo = getTrackTempo();
  const beatDuration = 60 / tempo;
  const currentTime = Number.isFinite(audio.currentTime) ? audio.currentTime : performance.now() / 1000;
  const phase = (currentTime / beatDuration) % 1;
  const kick = Math.max(0, 1 - phase * 4.2);
  const wave = (Math.sin(currentTime * 5.2) + 1) / 2;
  const now = performance.now();
  const onset = kick > 0.72 && now - ecgState.lastOnsetAt > Math.max(180, beatDuration * 650);
  if (onset) ecgState.lastOnsetAt = now;
  return {
    energy: 0.22 + kick * 0.24 + wave * 0.08,
    bass: 0.2 + kick * 0.34,
    mid: 0.16 + wave * 0.16,
    treble: 0.12 + (1 - wave) * 0.12,
    onset,
  };
}

function averageBins(bins, start, end) {
  const safeStart = Math.max(0, Math.min(bins.length - 1, start));
  const safeEnd = Math.max(safeStart + 1, Math.min(bins.length, end));
  let total = 0;
  for (let index = safeStart; index < safeEnd; index += 1) total += bins[index];
  return Math.min(1, total / ((safeEnd - safeStart) * 255));
}

function drawEcg(beatPosition, tempo, metrics) {
  const { energy, bass, mid, treble, pulse, flash } = metrics;
  const baseline = 37;
  const minY = 8;
  const maxY = 62;
  const left = 8;
  const right = 612;
  const beatSpacing = Math.max(64, Math.min(132, 7600 / tempo));
  const scroll = (beatPosition * beatSpacing) % beatSpacing;
  const amplitude = 0.42 + energy * 0.46 + bass * 0.62 + pulse * 0.2;
  const points = [[left, baseline]];

  for (let x = left + beatSpacing - scroll; x < right + beatSpacing; x += beatSpacing) {
    addBeat(points, x, baseline, amplitude, { bass, mid, treble, pulse });
  }

  const path = points
    .filter(([x]) => x >= left - 28 && x <= right + 28)
    .sort((a, b) => a[0] - b[0])
    .map(([x, y], index) => `${index ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`)
    .join(" ");

  ecgMainPath.setAttribute("d", path);
  ecgShadowPath.setAttribute("d", path);

  const newestBeatX = left + beatSpacing - scroll;
  const dotX = Math.max(left + 22, Math.min(right - 18, newestBeatX + beatSpacing * 2));
  const dotY = baseline - (8 + energy * 8 + bass * 5) * Math.max(0.25, flash);
  ecgBeatDot.setAttribute("cx", dotX.toFixed(1));
  ecgBeatDot.setAttribute("cy", Math.max(12, Math.min(58, dotY)).toFixed(1));
  ecgBeatDot.setAttribute("r", (2.8 + flash * 1.35 + energy * 0.9 + bass * 0.75).toFixed(1));
  ecgMainPath.style.strokeWidth = (2.55 + energy * 1.15 + bass * 0.55 + flash * 0.35).toFixed(2);
  ecgMainPath.style.opacity = String(Math.min(0.9, 0.56 + energy * 0.2 + bass * 0.12 + flash * 0.08));

  ecgMainPath.setAttribute("d", clampEcgPath(path, minY, maxY));
  ecgShadowPath.setAttribute("d", clampEcgPath(path, minY, maxY));
}

function addBeat(points, x, baseline, amplitude, metrics) {
  const qrsLift = 1 + metrics.bass * 0.22 + metrics.pulse * 0.16;
  const tremble = metrics.treble * 1.2;
  const shape = [
    [-54, 0],
    [-38, 0],
    [-29, (-2 - tremble * 0.12) * amplitude],
    [-21, (2 + metrics.mid * 2) * amplitude],
    [-13, 0],
    [3, 0],
    [13, -13 * amplitude * qrsLift],
    [22, 14 * amplitude * qrsLift],
    [33, -18 * amplitude * qrsLift],
    [44, (5 + metrics.mid * 2) * amplitude],
    [58, 0],
    [86, 0],
    [96, (-4 - tremble * 0.18) * amplitude],
    [109, (3 + metrics.treble * 1.2) * amplitude],
    [122, 0],
  ];

  shape.forEach(([offset, y]) => {
    points.push([x + offset, Math.max(8, Math.min(62, baseline + y))]);
  });
}

function clampEcgPath(path, minY, maxY) {
  return path.replace(/(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)/g, (_, x, y) => {
    const clampedY = Math.max(minY, Math.min(maxY, Number(y)));
    return `${x} ${clampedY.toFixed(1)}`;
  });
}

function stopAudio() {
  if (!audio.paused) audio.pause();
  setMusicPlaybackRequested(false);
  state.playing = false;
  state.audioStartRequested = false;
  saveControlPlaybackState();
}

function togglePlayback() {
  if (state.playing) {
    stopAudio();
    renderPlayback();
    return;
  }
  startAudio();
}

function moveTrack(direction) {
  const tracks = getTracks();
  if (!tracks.length) return;
  const nextIndex = getNextTrackIndex(direction, tracks, { manual: true });
  state.listMotion = getTrackMotion(nextIndex, state.trackIndex, tracks.length);
  state.trackIndex = nextIndex;
  if (state.playing) {
    startAudio();
  } else {
    syncAudioSource();
    render();
    saveControlPlaybackState();
  }
}

function getNextTrackIndex(direction, tracks, options = {}) {
  const mode = PLAY_MODES[state.playModeIndex];
  if (mode === "single" && !options.manual) return state.trackIndex;
  if (mode === "shuffle" && tracks.length > 1) {
    let nextIndex = state.trackIndex;
    while (nextIndex === state.trackIndex) {
      nextIndex = Math.floor(Math.random() * tracks.length);
    }
    return nextIndex;
  }
  return (state.trackIndex + direction + tracks.length) % tracks.length;
}

function handleEnded() {
  const mode = PLAY_MODES[state.playModeIndex];
  const tracks = getTracks();
  if (!tracks.length) return;
  if (mode === "single") {
    audio.currentTime = 0;
    startAudio();
    return;
  }
  const nextIndex = getNextTrackIndex(1, tracks);
  state.listMotion = getTrackMotion(nextIndex, state.trackIndex, tracks.length);
  state.trackIndex = nextIndex;
  startAudio();
}
