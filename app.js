const YEARS = [2022, 2023, 2024, 2025, 2026];
const AUDIO_EXTENSIONS = /\.(mp3|m4a|wav|ogg|flac|aac|opus)$/i;
const PLAY_MODES = [
  { id: "shuffle", label: "\u968f\u673a\u64ad\u653e" },
  { id: "single", label: "\u5355\u66f2\u5faa\u73af" },
  { id: "list", label: "\u5217\u8868\u5faa\u73af" },
];
const HOMEPAGE_INTRO_KEY = "linger-homepage-intro-seen";
const SOUND_CHANGE_EVENT = "linger:soundchange";
const SOUND_CHOICE_KEY = "linger:sound-choice";
const MUSIC_AUTOPLAY_KEY = "linger:music-autoplay-enabled";
const MUSIC_PLAY_STATE_KEY = "linger:music-playing";
const MUSIC_PLAY_STATE_CHANGE_EVENT = "linger:musicplaystatechange";
const MUSIC_COMMAND_EVENT = "linger:music-command";
const YEAR_CONTROL_PLAYBACK_EVENT = "linger:year-control-playback";
const YEAR_PARENT_PLAYBACK_EVENT = "linger:year-parent-playback";
const YEAR_PARENT_COMMAND_EVENT = "linger:year-parent-command";
const HOMEPAGE_PLAYBACK_KEY = "linger:playback:homepage";
const YEAR_PLAYBACK_KEY_PREFIX = "linger:playback:year:";
const YEAR_PLAYBACK_SAVE_EVENT = "linger:year-playback-save";
const YEAR_PLAYBACK_RESTORE_EVENT = "linger:year-playback-restore";
const INTERNAL_HOME_NAV_KEY = "linger:internal-home-nav";
const HOMEPAGE_AUDIO_READY_EVENT = "linger:homepageready";
const HOMEPAGE_INTRO_DONE_EVENT = "linger:homeintrodone";
const HOMEPAGE_LAYOUT_REFRESH_EVENT = "linger:homepagelayoutrefresh";
const HOMEPAGE_MUSIC_MAX_GAIN = 0.20;
const HOMEPAGE_DEFAULT_VOLUME = 50;
const YEAR_MUSIC_MAX_GAIN = 0.20;
const SHARED_VOLUME_KEY = "linger:music-volume";
const VOLUME_CHANGE_EVENT = "linger:volumechange";
const SOFT_HOMEPAGE_SONGS = [
  "diamond heart",
  "shallow",
  "i forgot that you existed",
  "lover",
];
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
const ROOM_INFO = {
  2022: {
    title: "2022 Rain Archive",
    tone: "dark",
    summary: "Amber rain archive, vinyl records, and remembered live recordings.",
    image: "assets/music-space-zoom-2022-v8-no-controller-transparent.png",
    background: "assets/zoom-bg-2022.png",
    tags: ["#ArchiveBoss", "#RainyReplay", "#BigMoodMuseum", "#LoopRingEra", "#TicketStubFeels"],
  },
  2023: {
    title: "2023 Encore Stage",
    tone: "dark",
    summary: "A live-stage memory room with marquee light, posters, and rehearsal cases.",
    image: "assets/music-space-zoom-2023-v8-no-controller-transparent.png",
    background: "assets/zoom-bg-2023.png",
    tags: ["#MicCableMood", "#EncoreMemory", "#DuetDrama", "#LivePosterEra", "#StageLightFeels"],
  },
  2024: {
    title: "2024 Quiet Reconciliation",
    tone: "light",
    summary: "Soft notes, folded lyrics, plants, and quiet handmade listening.",
    image: "assets/music-space-zoom-2024-v8-no-controller-transparent.png",
    background: "assets/zoom-bg-2024.png",
    tags: ["#SoloReconcile", "#QuietRoom", "#SoftAlbumPanel", "#FoldedNoteMood", "#MakingPeace"],
  },
  2025: {
    title: "2025 Neon Kinetic Charge",
    tone: "dark",
    summary: "Glossy neon club energy, beat files, and kinetic listening movement.",
    image: "assets/music-space-zoom-2025-v8-no-controller-transparent.png",
    background: "assets/zoom-bg-2025.png",
    tags: ["#NeonFeelings", "#BassFeelingsOnly", "#TinyClubInMyHead", "#GlowUpPlaylist", "#KineticCrisis"],
  },
  2026: {
    title: "2026 Open Horizon",
    tone: "light",
    summary: "Sunlit horizon room with sea-glass tags, compass details, and open air.",
    image: "assets/music-space-zoom-2026-v8-no-controller-transparent.png",
    background: "assets/zoom-bg-2026.png",
    tags: ["#OpenHorizon", "#FreeReplay", "#GalaxyOnRepeat", "#LiveVersionHitHard", "#WindPathMood"],
  },
};

const ROOM_LIVE_EFFECTS = {
  2022: [
    { type: "rain", x: 7.2, y: 9.8, w: 18.8, h: 31.5, rotate: -2, opacity: 0.7, delay: -0.4 },
    { type: "glow", x: 9.2, y: 43.2, w: 10.4, h: 12.8, color: "#f2b84b", opacity: 0.45, delay: -1.2 },
    { type: "record", x: 60.6, y: 54.8, w: 12.6, h: 10.6, color: "#f2b84b", opacity: 0.5, delay: -0.8 },
    { type: "spark", x: 27.5, y: 24.5, w: 45, h: 19, color: "#d9a24a", opacity: 0.3, delay: -2.2 },
  ],
  2023: [
    { type: "smoke", x: 22.5, y: 8.5, w: 55, h: 35, opacity: 0.45, delay: -0.7 },
    { type: "glow", x: 29.5, y: 38.5, w: 42, h: 7.5, color: "#f2b84b", opacity: 0.48, delay: -1.6 },
    { type: "neon", x: 75.5, y: 16.5, w: 12.8, h: 24, color: "#c83e4d", opacity: 0.52, delay: -0.5 },
    { type: "spark", x: 45.5, y: 49.5, w: 31, h: 20, color: "#f2b84b", opacity: 0.34, delay: -2.4 },
  ],
  2024: [
    { type: "mist", x: 8, y: 11, w: 20, h: 32, opacity: 0.55, delay: -0.9 },
    { type: "glow", x: 25.8, y: 49.5, w: 12.5, h: 13.2, color: "#d9b56a", opacity: 0.5, delay: -1.4 },
    { type: "breeze", x: 36, y: 56, w: 34, h: 15, color: "#f2ebdd", opacity: 0.32, delay: -2 },
    { type: "spark", x: 50, y: 25, w: 30, h: 14, color: "#d9b56a", opacity: 0.18, delay: -0.3 },
  ],
  2025: [
    { type: "neon", x: 21, y: 42, w: 55, h: 19, color: "#ff4f9a", opacity: 0.65, delay: -0.8 },
    { type: "neon", x: 22, y: 50, w: 50, h: 18, color: "#00b8d9", opacity: 0.5, delay: -2.1 },
    { type: "spark", x: 25, y: 18, w: 57, h: 36, color: "#e7f24a", opacity: 0.42, delay: -1.5 },
    { type: "glow", x: 75, y: 33, w: 16, h: 16, color: "#ff4f9a", opacity: 0.48, delay: -0.4 },
  ],
  2026: [
    { type: "breeze", x: 27, y: 25, w: 49, h: 19, color: "#f3ebdd", opacity: 0.46, delay: -1 },
    { type: "spark", x: 50, y: 13, w: 35, h: 22, color: "#f3c45b", opacity: 0.44, delay: -2.3 },
    { type: "record", x: 55, y: 29, w: 31, h: 24, color: "#7b6bb2", opacity: 0.28, delay: -0.7 },
    { type: "glow", x: 65, y: 31, w: 17, h: 13, color: "#f3c45b", opacity: 0.34, delay: -1.8 },
  ],
};
const state = {
  selectedYear: 2022,
  localAudioFiles: [],
  homepageTracks: [],
  homepageMusicIndex: 0,
  homepageMusicPlaying: false,
  homepageMusicPendingStart: false,
  homepageMusicSeeded: false,
  homepageAutoplayBlocked: false,
  homepageRestoreTime: 0,
  roomMusicIndex: 0,
  roomMusicPlaying: false,
  roomMusicSeededYear: null,
  roomPlayMode: "list",
  roomPendingMusicStart: false,
  roomRestoreTime: 0,
  roomLastPlaybackSaveAt: 0,
  applyingSharedPlayState: false,
  volume: HOMEPAGE_DEFAULT_VOLUME,
  soundEnabled: false,
};

let roomAudio = document.querySelector("#roomAudio");
const repeatAudio = document.querySelector("#repeatAudio");

function bootLingerApp() {
  clearPlaybackStateOnRefresh();
  initTrebleNoteCursor();
  initSharedVolume();
  initGlobalSoundPreference();
  bindGlobalKeyboardPlayback();
  bindHomeLinkRecovery();
  if (document.body.dataset.page === "overview") {
    initHomepagePage();
  } else if (document.body.dataset.page === "room") {
    initRoomPage();
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", bootLingerApp, { once: true });
} else {
  bootLingerApp();
}

function clampVolume(value) {
  return Math.max(0, Math.min(100, Math.round(Number(value) || 0)));
}

function readSharedVolume() {
  try {
    const saved = window.sessionStorage.getItem(SHARED_VOLUME_KEY);
    return saved === null ? HOMEPAGE_DEFAULT_VOLUME : clampVolume(saved);
  } catch {
    return HOMEPAGE_DEFAULT_VOLUME;
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
    if (event.data?.type === YEAR_CONTROL_PLAYBACK_EVENT) {
      handleYearControlPlaybackStatus(event.data);
      return;
    }
    if (event.data?.type === YEAR_PARENT_COMMAND_EVENT) {
      handleYearParentCommand(event.data);
      return;
    }
    if (event.data?.type === MUSIC_PLAY_STATE_CHANGE_EVENT) {
      applySharedMusicPlayState(Boolean(event.data.playing), {
        broadcast: false,
        fromCurrentControl: event.source === getMusicControlFrameWindow(),
      });
      return;
    }
    if (event.data?.type === YEAR_PLAYBACK_SAVE_EVENT) {
      storeYearPlaybackState(event.data);
    }
  });
  window.addEventListener("storage", (event) => {
    if (event.key === SHARED_VOLUME_KEY) {
      applySharedVolume(event.newValue, { broadcast: false });
      return;
    }
    if (event.key === MUSIC_PLAY_STATE_KEY) {
      applySharedMusicPlayState(event.newValue === "1", { broadcast: false });
    }
  });
  window.addEventListener("pagehide", saveHomepagePlaybackState);
  window.addEventListener("beforeunload", saveHomepagePlaybackState);
}

function applySharedVolume(value, options = {}) {
  state.volume = writeSharedVolume(value);
  if (repeatAudio) repeatAudio.volume = getHomepageAudioVolume();
  if (roomAudio) roomAudio.volume = getYearMusicAudioVolume();
  if (document.body.dataset.page === "overview") renderHomepageMusicPlayer();
  if (document.body.dataset.page === "room") renderRoomMusicPlayer();
  if (options.broadcast !== false) broadcastSharedVolume();
}

function broadcastSharedVolume() {
  const message = { type: VOLUME_CHANGE_EVENT, volume: state.volume };
  window.dispatchEvent(new CustomEvent(VOLUME_CHANGE_EVENT, { detail: message }));
  getMusicControlFrameWindow()?.postMessage(message, "*");
}

function initTrebleNoteCursor() {
  const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (motionQuery.matches) return;

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

  const hoverSelector = [
    "a",
    "button",
    "input",
    "textarea",
    "select",
    "label",
    "summary",
    "[role='button']",
    "[tabindex]:not([tabindex='-1'])",
    ".hero-space",
    ".space-hotspot",
  ].join(",");

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

function initGlobalSoundPreference() {
  state.soundEnabled = getGlobalSoundEnabled();
  applyGlobalSoundPreference();
  window.startLingerHomepageAudio = () => startHomepageAudio();
  window.startLingerPageAudio = () => startCurrentPageMusic();
  window.stopLingerHomepageAudio = () => {
    setMusicPlaybackRequested(false);
    stopHomepageAudio();
    renderHomepageMusicPlayer();
  };
  window.addEventListener(SOUND_CHANGE_EVENT, (event) => {
    state.soundEnabled = Boolean(event.detail?.enabled);
    applyGlobalSoundPreference(state.soundEnabled);
    postMusicFrameMessage({
      type: SOUND_CHANGE_EVENT,
      enabled: isActiveSoundEnabled(),
      choiceSettled: hasActiveSoundChoice(),
    });
    if (event.detail?.initialChoice && state.soundEnabled) {
      enableMusicAutoplay();
      startCurrentPageMusic();
    }
    if (document.body.dataset.page === "overview") {
      renderHomepageMusicPlayer();
    }
  });
}

function bindGlobalKeyboardPlayback() {
  if (window.lingerKeyboardPlaybackBound) return;
  window.lingerKeyboardPlaybackBound = true;
  document.addEventListener("keydown", (event) => {
    if (!isPlaybackSpaceKey(event) || shouldIgnorePlaybackKeyTarget(event.target)) return;
    event.preventDefault();
    toggleCurrentPagePlayback();
  });
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

function safeHistoryPushState(url) {
  try {
    window.history.pushState({}, "", url);
  } catch {
    // file:// pages cannot rewrite the URL; keep the in-page state instead.
  }
}

function bindHomeLinkRecovery() {
  document.addEventListener("click", (event) => {
    const link = event.target.closest?.("a[href*='index.html']");
    if (!link || document.body.dataset.page !== "room") return;
    let target;
    try {
      target = new URL(link.getAttribute("href"), window.location.href);
    } catch {
      return;
    }
    if (!target.pathname.endsWith("index.html")) return;
    // Only intercept when the link points at the document we are already on
    // (the in-place room view); a hash-only difference would otherwise
    // make the back-to-homepage link do nothing. A hash-only change is a
    // same-document navigation, so a real reload is required here.
    if (target.pathname !== window.location.pathname) return;
    event.preventDefault();
    try {
      window.sessionStorage.setItem(INTERNAL_HOME_NAV_KEY, "1");
    } catch {
      // Without storage the reload still works; sound choice may reset.
    }
    window.location.reload();
  });
}

function toggleCurrentPagePlayback() {
  if (document.body.dataset.page === "overview") {
    toggleHomepageAudio();
    return;
  }
  try {
    const frameWindow = getMusicControlFrameWindow();
    if (typeof frameWindow?.toggleLingerControlAudio === "function") {
      frameWindow.toggleLingerControlAudio();
      return;
    }
  } catch {
    // If the controller is still loading, fall back to the shared play state.
  }
  if (isMusicPlaybackRequested()) {
    applySharedMusicPlayState(false);
  } else {
    startYearControlMusic();
  }
}

function getGlobalSoundEnabled() {
  try {
    return window.sessionStorage.getItem(SOUND_CHOICE_KEY) === "on";
  } catch {
    return false;
  }
}

function getSoundChoice() {
  try {
    const choice = window.sessionStorage.getItem(SOUND_CHOICE_KEY);
    return choice === "on" || choice === "off" ? choice : null;
  } catch {
    return null;
  }
}

function hasSoundChoice() {
  return getSoundChoice() !== null;
}

function hasActiveSoundChoice() {
  return hasSoundChoice()
    || state.soundEnabled
    || document.querySelector(".hover-sound-toggle")?.getAttribute("aria-pressed") === "true";
}

function isActiveSoundEnabled() {
  const toggle = document.querySelector(".hover-sound-toggle");
  if (toggle) return toggle.getAttribute("aria-pressed") === "true";
  return state.soundEnabled;
}

function isPageRefresh() {
  const navigation = performance.getEntriesByType?.("navigation")?.[0];
  return navigation?.type === "reload";
}

function consumeInternalHomeNavFlag() {
  try {
    if (window.sessionStorage.getItem(INTERNAL_HOME_NAV_KEY) !== "1") return false;
    window.sessionStorage.removeItem(INTERNAL_HOME_NAV_KEY);
    return true;
  } catch {
    return false;
  }
}

function clearPlaybackStateOnRefresh() {
  if (!isPageRefresh()) return;
  // A reload triggered by the in-page back-to-homepage link is navigation,
  // not a fresh start: keep sound choice and playback state.
  if (consumeInternalHomeNavFlag()) return;
  try {
    window.sessionStorage.removeItem(HOMEPAGE_PLAYBACK_KEY);
    window.sessionStorage.removeItem(MUSIC_PLAY_STATE_KEY);
    window.localStorage.removeItem(MUSIC_PLAY_STATE_KEY);
    [...Array(window.sessionStorage.length).keys()]
      .map((index) => window.sessionStorage.key(index))
      .filter((key) => key?.startsWith(YEAR_PLAYBACK_KEY_PREFIX))
      .forEach((key) => window.sessionStorage.removeItem(key));
  } catch {
    // Session storage can be unavailable in some embedded/private contexts.
  }
}

function enableMusicAutoplay() {
  try {
    window.sessionStorage.setItem(MUSIC_AUTOPLAY_KEY, "1");
    window.sessionStorage.setItem(MUSIC_PLAY_STATE_KEY, "1");
    window.localStorage.setItem(MUSIC_PLAY_STATE_KEY, "1");
  } catch {
    // Session storage can be unavailable in some embedded/private contexts.
  }
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
  try {
    window.sessionStorage.setItem(MUSIC_PLAY_STATE_KEY, playing ? "1" : "0");
    window.localStorage.setItem(MUSIC_PLAY_STATE_KEY, playing ? "1" : "0");
  } catch {
    // Session storage can be unavailable in some embedded/private contexts.
  }
  if (options.broadcast === false || state.applyingSharedPlayState) return;
  const message = { type: MUSIC_PLAY_STATE_CHANGE_EVENT, playing: Boolean(playing) };
  getMusicControlFrameWindow()?.postMessage(message, "*");
}

function applySharedMusicPlayState(playing, options = {}) {
  state.applyingSharedPlayState = true;
  setMusicPlaybackRequested(playing, { broadcast: false });
  try {
    if (!hasActiveSoundChoice()) return;
    if (playing) {
      if (document.body.dataset.page === "overview") {
        startHomepageAudio();
      } else if (!options.fromCurrentControl) {
        startYearControlMusic();
      }
      if (options.broadcast !== false) getMusicControlFrameWindow()?.postMessage({ type: MUSIC_PLAY_STATE_CHANGE_EVENT, playing: true }, "*");
      return;
    }
    if (repeatAudio && !repeatAudio.paused) repeatAudio.pause();
    if (roomAudio && !roomAudio.paused) roomAudio.pause();
    state.homepageMusicPlaying = false;
    state.roomMusicPlaying = false;
    renderHomepageMusicPlayer();
    renderRoomMusicPlayer();
    if (options.broadcast !== false) getMusicControlFrameWindow()?.postMessage({ type: MUSIC_PLAY_STATE_CHANGE_EVENT, playing: false }, "*");
  } finally {
    state.applyingSharedPlayState = false;
  }
}

function startCurrentPageMusic() {
  if (!hasActiveSoundChoice()) return false;
  setMusicPlaybackRequested(true);
  if (document.body.dataset.page === "overview") {
    return startHomepageAudio();
  }
  startYearControlMusic();
  return true;
}

function startYearControlMusic() {
  const frame = document.querySelector("#memoryControlFrame");
  const soundEnabled = isActiveSoundEnabled();
  const choiceSettled = hasActiveSoundChoice();
  state.roomPendingMusicStart = true;
  if (!frame) return;
  frame.dataset.pendingMusicStart = "1";

  try {
    const frameWindow = getMusicControlFrameWindow();
    if (typeof frameWindow?.startLingerControlAudio === "function") {
      if (typeof frameWindow.applyLingerControlSoundPreference === "function") {
        frameWindow.applyLingerControlSoundPreference(soundEnabled, choiceSettled);
      }
      frameWindow.startLingerControlAudio();
      return;
    }
  } catch {
    // Local file iframes can be treated as separate contexts in some browsers.
  }

  postMusicFrameMessage({
    type: MUSIC_COMMAND_EVENT,
    command: "start",
    enabled: soundEnabled,
    choiceSettled,
  });
}

function handleYearControlPlaybackStatus(status) {
  if (document.body.dataset.page !== "room") return;
  if (status.embed === true) return;
  if (status.started || status.playing) {
    state.roomPendingMusicStart = false;
    if (roomAudio && !roomAudio.paused) roomAudio.pause();
    state.roomMusicPlaying = false;
    return;
  }
}

function handleYearParentCommand(message) {
  if (document.body.dataset.page !== "room") return;
  if (Number(message.year) !== state.selectedYear) return;
  const tracks = getRoomMusicTracks();
  if (!tracks.length) return;

  if (message.command === "toggle") {
    toggleRoomMusicPlayback();
    return;
  }
  if (message.command === "play") {
    startRoomMusicAudio();
    return;
  }
  if (message.command === "pause") {
    setMusicPlaybackRequested(false);
    stopRoomMusicAudio();
    renderRoomMusicPlayer();
    postParentRoomPlaybackState();
    return;
  }
  if (message.command === "prev") {
    moveRoomMusicTrack(-1);
    return;
  }
  if (message.command === "next") {
    moveRoomMusicTrack(1);
    return;
  }
  if (message.command === "select") {
    const index = Math.max(0, Math.min(Number(message.index) || 0, tracks.length - 1));
    if (roomAudio && !roomAudio.paused) roomAudio.pause();
    state.roomRestoreTime = 0;
    state.roomMusicIndex = index;
    syncRoomMusicAudioSource(getCurrentRoomMusicTrack());
    renderRoomMusicPlayer();
    postParentRoomPlaybackState();
    saveRoomPlaybackState({ force: true });
    startRoomMusicAudio();
    return;
  }
  if (message.command === "seek" && roomAudio && Number.isFinite(Number(message.time))) {
    roomAudio.currentTime = Math.max(0, Number(message.time));
    renderRoomMusicPlayer();
    postParentRoomPlaybackState();
    saveRoomPlaybackState({ force: true });
    return;
  }
  if (message.command === "mode") {
    const requestedMode = PLAY_MODES.find((mode) => mode.id === message.mode)?.id;
    if (requestedMode) {
      state.roomPlayMode = requestedMode;
    } else {
      cycleRoomPlayMode();
      return;
    }
    renderRoomMusicPlayer();
    postParentRoomPlaybackState();
    saveRoomPlaybackState({ force: true });
  }
}

function postMusicFrameMessage(message) {
  try {
    getMusicControlFrameWindow()?.postMessage(message, "*");
  } catch {
    // The controller may still be loading; it will retry from the iframe load path.
  }
}

// The control iframe can lose its own storage between loads (notably on
// file:// pages, where iframes are isolated origins). The parent page keeps
// the per-year playback positions instead and hands them back on load.
function storeYearPlaybackState(data) {
  const year = Number(data?.year);
  if (!YEARS.includes(year)) return;
  try {
    window.sessionStorage.setItem(`${YEAR_PLAYBACK_KEY_PREFIX}${year}`, JSON.stringify({
      index: Number(data.index) || 0,
      time: Math.max(0, Number(data.time) || 0),
      playing: Boolean(data.playing),
    }));
  } catch {
    // Storage can be unavailable; the in-iframe copy remains the fallback.
  }
}

function postYearPlaybackStates() {
  const states = {};
  try {
    YEARS.forEach((year) => {
      const raw = window.sessionStorage.getItem(`${YEAR_PLAYBACK_KEY_PREFIX}${year}`);
      if (raw) states[year] = JSON.parse(raw);
    });
  } catch {
    return;
  }
  if (!Object.keys(states).length) return;
  postMusicFrameMessage({ type: YEAR_PLAYBACK_RESTORE_EVENT, states });
}

function getMusicControlFrameWindow() {
  return document.querySelector("#memoryControlFrame, #homepageMemoryControlFrame")?.contentWindow || null;
}

function readStorageFlag(key) {
  try {
    return window.localStorage.getItem(key) === "1";
  } catch {
    return false;
  }
}

function writeStorageFlag(key) {
  try {
    window.localStorage.setItem(key, "1");
  } catch {
    // Storage can be blocked in private or embedded browsing contexts.
  }
}

function applyGlobalSoundPreference(enabled = getGlobalSoundEnabled()) {
  state.soundEnabled = enabled;
  document.querySelectorAll("audio").forEach((audio) => {
    audio.muted = !enabled;
  });
}

async function initHomepagePage() {
  state.volume = readSharedVolume();
  initHomepageScrollText();
  initHomepageOverviewSpacing();
  initHomepageIntro();
  bindHomepageRoomLinks();
  await loadLocalMusic();
  state.homepageTracks = getHomepageMusicTracks();
  seedRandomHomepageTrack();
  restoreHomepagePlaybackState();
  bindHomepageAudio();
  syncHomepageAudioSource(getCurrentHomepageTrack());
  renderHomepageMusicPlayer();
  window.lingerHomepageAudioReady = true;
  window.dispatchEvent(new CustomEvent(HOMEPAGE_AUDIO_READY_EVENT));
  if (hasActiveSoundChoice() && isMusicPlaybackRequested()) startHomepageAudio();
}

function bindHomepageRoomLinks() {
  window.lingerOpenMemoryRoomFromHomepage = (href) => {
    const year = Number(new URL(href, window.location.href).searchParams.get("year"));
    if (!YEARS.includes(year)) return false;
    if (!isActiveSoundEnabled() || !hasActiveSoundChoice() || !isMusicPlaybackRequested()) return false;
    enterRoomFromHomepage(year);
    return true;
  };
  document.querySelector(".hero-spaces")?.addEventListener("click", (event) => {
    const link = event.target.closest(".hero-space");
    if (!link) return;
    const year = Number(new URL(link.href, window.location.href).searchParams.get("year"));
    if (!YEARS.includes(year)) return;
    if (!window.lingerOpenMemoryRoomFromHomepage?.(link.href)) return;
    event.preventDefault();
  });
}

function ensureHomepageMemoryControlFrame() {
  if (document.body.dataset.page !== "overview") return null;
  let frame = document.querySelector("#homepageMemoryControlFrame, #memoryControlFrame");
  if (frame) return frame;
  frame = document.createElement("iframe");
  frame.id = "homepageMemoryControlFrame";
  frame.className = "memory-control-frame";
  frame.title = "Memory Space music control";
  frame.loading = "eager";
  frame.allow = "autoplay";
  frame.setAttribute("aria-hidden", "true");
  Object.assign(frame.style, {
    position: "fixed",
    left: "-9999px",
    top: "0",
    width: "1px",
    height: "1px",
    opacity: "0",
    pointerEvents: "none",
  });
  frame.addEventListener("load", () => {
    postMusicFrameMessage({
      type: SOUND_CHANGE_EVENT,
      enabled: isActiveSoundEnabled(),
      choiceSettled: hasActiveSoundChoice(),
    });
    postYearPlaybackStates();
  });
  frame.src = "control.html?year=2022&embed=memory&preload=1&v=direct-year-play-49";
  document.body.append(frame);
  return frame;
}

function enterRoomFromHomepage(year) {
  state.selectedYear = year;
  state.roomMusicIndex = 0;
  state.roomMusicSeededYear = null;
  state.roomRestoreTime = 0;
  const shouldAutoplay = hasActiveSoundChoice() && isMusicPlaybackRequested();
  state.roomPendingMusicStart = shouldAutoplay;
  stopHomepageAudio();
  const room = ROOM_INFO[year] || ROOM_INFO[2022];
  document.body.dataset.page = "room";
  document.body.classList.remove("is-empty", "home-intro-active");
  document.body.classList.add("has-museum");

  const main = document.querySelector("main");
  if (!main) return;
  main.innerHTML = `
    <section id="room" class="zoom-shell room-page-shell" aria-label="Selected yearly memory room">
      <div class="room-heading">
        <div>
          <p class="eyebrow">Zoom-in space</p>
          <h2 id="roomTitle">Loading room</h2>
          <div id="personaTags" class="tag-cloud room-heading-tags" aria-label="Space hashtags"></div>
          <p id="roomSummary" class="room-summary"></p>
        </div>
      </div>
      <div id="zoomRoom" class="zoom-room" aria-live="polite"></div>
    </section>
    <audio id="roomAudio" preload="metadata"></audio>
  `;

  updateRoomShell(room);
  renderRoom(room);
  const visibleFrame = document.querySelector("#memoryControlFrame");
  if (!visibleFrame) return;
  roomAudio = document.querySelector("#roomAudio");
  document.querySelector("#homepageMemoryControlFrame")?.remove();
  bindRoomYearNavigation();
  bindRoomAudio();
  renderRoomMusicPlayer();
  safeHistoryPushState(`room.html?year=${year}`);
  postMusicFrameMessage({
    type: SOUND_CHANGE_EVENT,
    enabled: isActiveSoundEnabled(),
    choiceSettled: hasActiveSoundChoice(),
  });
  const syncVisibleControl = () => {
    postMusicFrameMessage({
      type: SOUND_CHANGE_EVENT,
      enabled: isActiveSoundEnabled(),
      choiceSettled: hasActiveSoundChoice(),
    });
    postYearPlaybackStates();
    if (shouldAutoplay) {
      startYearControlMusic();
    }
  };
  visibleFrame.addEventListener("load", syncVisibleControl, { once: true });
  visibleFrame.src = `control.html?year=${year}&embed=memory${shouldAutoplay ? "&autoplay=1" : ""}&v=direct-year-play-49`;
}

function initHomepageOverviewSpacing() {
  const heroCopy = document.querySelector(".hero-copy");
  const spaces = document.querySelector(".hero-spaces");
  const journeyLine = document.querySelector(".hero-journey-line");
  const transport = document.querySelector(".repeat-transport");
  const transportCaption = document.querySelector(".repeat-transport-caption");
  if (!heroCopy || !spaces) return;
  const safeGap = 5;

  const getSpaceUnionRect = () => {
    const rects = [...spaces.querySelectorAll(".hero-space, .hero-space-label")]
      .map((space) => space.getBoundingClientRect())
      .filter((rect) => rect.width && rect.height);
    if (!rects.length) return spaces.getBoundingClientRect();
    return {
      top: Math.min(...rects.map((rect) => rect.top)),
      bottom: Math.max(...rects.map((rect) => rect.bottom)),
    };
  };

  const setRootPixels = (name, value) => {
    document.documentElement.style.setProperty(name, `${Math.max(0, Math.round(value))}px`);
  };

  const applyBaseSpacing = () => {
    document.documentElement.style.setProperty("--hero-overview-y", "0px");
    const overviewWidth = spaces.getBoundingClientRect().width;
    const minimumGap = Math.round(Math.max(42, Math.min(104, overviewWidth * 0.055)));
    const journeyGap = Math.round(Math.max(-40, Math.min(-20, overviewWidth * 0.02)));
    const copyBottom = heroCopy.getBoundingClientRect().bottom;
    const overviewRect = getSpaceUnionRect();
    const neededOffset = Math.round(copyBottom + minimumGap - overviewRect.top);
    document.documentElement.style.setProperty("--hero-copy-overview-gap", `${minimumGap}px`);
    document.documentElement.style.setProperty("--hero-overview-y", `${neededOffset}px`);
    document.documentElement.style.setProperty("--hero-overview-journey-gap", `${journeyGap}px`);
    document.documentElement.style.setProperty("--hero-journey-y", `${Math.round(getSpaceUnionRect().bottom + journeyGap)}px`);
  };

  const getControlRect = () => {
    const rects = [transportCaption, transport]
      .filter(Boolean)
      .map((element) => element.getBoundingClientRect())
      .filter((rect) => rect.width && rect.height);
    if (!rects.length) return null;
    return {
      top: Math.min(...rects.map((rect) => rect.top)),
      bottom: Math.max(...rects.map((rect) => rect.bottom)),
    };
  };

  const getJourneyCollision = () => {
    if (!journeyLine) return { overlap: 0 };
    const controlRect = getControlRect();
    if (!controlRect) return { overlap: 0 };
    const journeyRect = journeyLine.getBoundingClientRect();
    return {
      controlRect,
      journeyRect,
      overlap: Math.max(0, Math.ceil(journeyRect.bottom + safeGap - controlRect.top)),
    };
  };

  let overviewShrinkReviewFrame = 0;

  const resolveJourneyControlOverlap = (allowOverviewShrink = false) => {
    document.documentElement.style.setProperty("--hero-journey-scale", "1");
    setRootPixels("--repeat-transport-drop", 0);
    setRootPixels("--hero-overview-shrink", 0);
    applyBaseSpacing();

    let collision = getJourneyCollision();
    if (!collision.overlap) return;

    const viewportHeight = window.innerHeight || document.documentElement.clientHeight || 0;
    const maxControllerDrop = Math.max(0, viewportHeight - collision.controlRect.bottom - safeGap);
    const controllerDrop = Math.min(collision.overlap, maxControllerDrop);
    setRootPixels("--repeat-transport-drop", controllerDrop);
    collision = getJourneyCollision();
    if (!collision.overlap) return;

    const journeyHeight = Math.max(1, collision.journeyRect.height);
    const targetBottom = collision.controlRect.top - safeGap;
    const requiredScale = (targetBottom - collision.journeyRect.top) / journeyHeight;
    // Make the text visibly smaller before allowing the overview to shrink.
    const visibleJourneyScale = 0.78;
    const journeyScale = requiredScale < 1 ? visibleJourneyScale : 1;
    document.documentElement.style.setProperty("--hero-journey-scale", journeyScale.toFixed(3));
    collision = getJourneyCollision();
    if (!collision.overlap) return;
    if (!allowOverviewShrink) {
      window.cancelAnimationFrame(overviewShrinkReviewFrame);
      overviewShrinkReviewFrame = window.requestAnimationFrame(() => {
        overviewShrinkReviewFrame = window.requestAnimationFrame(() => {
          resolveJourneyControlOverlap(true);
        });
      });
      return;
    }

    let overviewShrink = 0;
    while (collision.overlap && overviewShrink < 220) {
      overviewShrink = Math.min(220, overviewShrink + Math.max(12, collision.overlap));
      setRootPixels("--hero-overview-shrink", overviewShrink);
      applyBaseSpacing();
      collision = getJourneyCollision();
    }
  };

  const updateSpacing = () => {
    resolveJourneyControlOverlap();
  };

  window.refreshLingerHomepageOverviewSpacing = updateSpacing;

  const scheduleUpdate = () => {
    window.requestAnimationFrame(() => {
      window.requestAnimationFrame(updateSpacing);
    });
  };

  scheduleUpdate();
  window.addEventListener("resize", scheduleUpdate);
  window.addEventListener("load", scheduleUpdate, { once: true });
  window.addEventListener(HOMEPAGE_INTRO_DONE_EVENT, scheduleUpdate);
  window.addEventListener(HOMEPAGE_LAYOUT_REFRESH_EVENT, scheduleUpdate);
  spaces.querySelectorAll("img").forEach((image) => {
    if (!image.complete) image.addEventListener("load", scheduleUpdate, { once: true });
  });
}

function initHomepageIntro() {
  const spaces = [...document.querySelectorAll(".hero-space")];
  const journeyLine = document.querySelector(".hero-journey-line");
  const textNode = [...(journeyLine?.childNodes || [])]
    .find((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim());
  if (!spaces.length || !journeyLine || !textNode) return;

  const introText = textNode.textContent.trim().replace(/\s+/g, " ");
  const replayRequested = new URLSearchParams(window.location.search).has("introReplay");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const introSeen = readStorageFlag(HOMEPAGE_INTRO_KEY);
  if (reduceMotion || (introSeen && !replayRequested)) {
    textNode.textContent = introText;
    return;
  }

  window.refreshLingerHomepageOverviewSpacing?.();
  document.body.classList.add("home-intro-active");
  journeyLine.classList.add("is-typing");
  journeyLine.setAttribute("aria-label", introText);
  textNode.textContent = "";
  spaces.forEach((space) => space.classList.remove("is-intro-visible"));

  spaces.forEach((space, index) => {
    window.setTimeout(() => {
      space.classList.add("is-intro-visible");
    }, 260 + index * 400);
  });

  const letters = Array.from(introText);
  const typeDuration = Math.min(5600, Math.max(3400, letters.length * 28));
  const typeStartDelay = 160;
  let startedAt = null;

  const typeFrame = (timestamp) => {
    if (!startedAt) startedAt = timestamp;
    const elapsed = Math.max(0, timestamp - startedAt - typeStartDelay);
    const progress = clamp01(elapsed / typeDuration);
    const visibleCount = Math.min(letters.length, Math.floor(progress * letters.length));
    textNode.textContent = letters.slice(0, visibleCount).join("");

    if (progress < 1) {
      window.requestAnimationFrame(typeFrame);
      return;
    }

    textNode.textContent = introText;
    journeyLine.classList.remove("is-typing");
    document.body.classList.remove("home-intro-active");
    writeStorageFlag(HOMEPAGE_INTRO_KEY);
    window.dispatchEvent(new CustomEvent(HOMEPAGE_INTRO_DONE_EVENT));
  };

  window.requestAnimationFrame(typeFrame);
}

function initHomepageScrollText() {
  const hero = document.querySelector("#home");
  const story = document.querySelector("#story");
  if (!hero || !story) return;

  const updateTextFade = () => {
    const viewportHeight = Math.max(1, window.innerHeight || document.documentElement.clientHeight);
    const maxScroll = document.documentElement.scrollHeight - viewportHeight;
    const scrollProgress = clamp01(window.scrollY / maxScroll);
    const heroFadeProgress = smoothStep(fadeRange(scrollProgress, 0.06, 0.55));
    const storyFadeProgress = smoothStep(fadeRange(scrollProgress, 0.58, 0.98));

    document.documentElement.style.setProperty("--hero-copy-opacity", String(1 - heroFadeProgress));
    document.documentElement.style.setProperty("--story-copy-opacity", String(storyFadeProgress));
  };

  updateTextFade();
  window.addEventListener("scroll", updateTextFade, { passive: true });
  window.addEventListener("resize", updateTextFade);
}

async function initRoomPage() {
  state.selectedYear = getSelectedYear();
  const room = ROOM_INFO[state.selectedYear] || ROOM_INFO[2022];
  document.body.dataset.roomYear = String(state.selectedYear);
  document.body.dataset.roomTone = room.tone;
  document.body.style.setProperty("--room-bg-image", `url("${room.background}")`);
  document.querySelector("#roomTitle").textContent = room.title;
  document.querySelector("#roomSummary").textContent = room.summary;
  document.querySelector("#personaTags").replaceChildren(...room.tags.map((tag) => {
    const item = document.createElement("span");
    item.textContent = tag;
    return item;
  }));

  await loadLocalMusic();
  restoreRoomPlaybackState();
  renderRoom(room);
  renderMemoryControlFrame();
  bindRoomYearNavigation();
  bindRoomAudio();
  renderRoomMusicPlayer();
}

function getSelectedYear() {
  const year = Number(new URLSearchParams(window.location.search).get("year"));
  return YEARS.includes(year) ? year : 2022;
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
  if (!files.length) files = await getRemoteAudioManifestFiles();
  if (!files.length) files = getAudioManifestFiles();
  files = preferWebAudioFiles(normalizeAudioManifestFiles(files));
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

function getTitleTranslationMap() {
  return window.LINGER_TITLE_TRANSLATIONS?.titles || {};
}

function hasChineseText(value) {
  return /[\u3400-\u9fff]/.test(String(value || ""));
}

function getLocalTrackEnglishTitle(title) {
  const normalizedTitle = String(title || "").trim();
  if (!hasChineseText(normalizedTitle)) return "";
  return getTitleTranslationMap()[normalizedTitle] || "";
}

function getLocalTrackTitleText(track) {
  if (!track) return "";
  const englishTitle = track.englishTitle || getLocalTrackEnglishTitle(track.title);
  return englishTitle ? `${track.title} / ${englishTitle}` : track.title;
}

function getHomepageMusicTracks() {
  return state.localAudioFiles
    .filter((file) => {
      const normalized = String(file.path || "").replace(/\\/g, "/").toLowerCase();
      return normalized.startsWith("homepage music/");
    })
    .filter((file) => AUDIO_EXTENSIONS.test(file.name || file.path || ""))
    .map(fileToLocalAudioTrack);
}

function fileToLocalAudioTrack(file) {
  const base = String(file.name || "").replace(/\.[^.]+$/, "");
  const parts = base.split(/\s+-\s+/);
  if (/^\d+$/.test(parts[0])) parts.shift();
  const [artist, ...titleParts] = parts;
  const title = titleParts.length ? titleParts.join(" - ").trim() : (parts.join(" - ").trim() || base);
  return {
    title,
    englishTitle: getLocalTrackEnglishTitle(title),
    artist: titleParts.length ? artist.trim() : "Local Archive",
    audioSrc: file.url,
  };
}

function isSoftEnglishHomepageTrack(track) {
  const text = `${track.artist || ""} ${track.title || ""}`.toLowerCase();
  return SOFT_HOMEPAGE_SONGS.some((song) => text.includes(song));
}

function seedRandomHomepageTrack() {
  if (state.homepageMusicSeeded || !state.homepageTracks.length) return;
  const softEnglishIndexes = state.homepageTracks
    .map((track, index) => (isSoftEnglishHomepageTrack(track) ? index : -1))
    .filter((index) => index >= 0);
  const openingPool = softEnglishIndexes.length ? softEnglishIndexes : state.homepageTracks.map((_, index) => index);
  state.homepageMusicIndex = openingPool[Math.floor(Math.random() * openingPool.length)];
  state.homepageMusicSeeded = true;
}

function bindHomepageAudio() {
  document.querySelector("#repeatPlayButton")?.addEventListener("click", toggleHomepageAudio);
  document.querySelector("#repeatPrevButton")?.addEventListener("click", () => moveHomepageTrack(-1));
  document.querySelector("#repeatNextButton")?.addEventListener("click", () => moveHomepageTrack(1));
  document.querySelector("#repeatVolumeControl")?.addEventListener("input", (event) => {
    applySharedVolume(event.target.value);
  });
  repeatAudio?.addEventListener("timeupdate", () => {
    renderHomepageMusicPlayer();
    saveHomepagePlaybackState();
  });
  repeatAudio?.addEventListener("loadedmetadata", renderHomepageMusicPlayer);
  repeatAudio?.addEventListener("ended", handleHomepageAudioEnded);
}

function getCurrentHomepageTrack() {
  if (!state.homepageTracks.length) return null;
  state.homepageMusicIndex = Math.max(0, Math.min(state.homepageMusicIndex, state.homepageTracks.length - 1));
  return state.homepageTracks[state.homepageMusicIndex] || state.homepageTracks[0];
}

function renderHomepageMusicPlayer() {
  const current = getCurrentHomepageTrack();
  const hasTracks = Boolean(current);
  const displayTitle = getHomepageDisplayTitle(current);
  setText("#repeatTransportTitle", trimText(displayTitle || "Finding the songs that returned", 40), displayTitle || "");
  setText("#repeatTransportArtist", getDisplayArtist(current?.artist || ""));
  setText("#repeatTransportYears", hasTracks ? "Homepage memory music" : "");
  setText("#repeatPlaybackStatus", getHomepagePlaybackStatus(hasTracks));
  setText("#repeatLibraryStatus", hasTracks ? `${state.homepageTracks.length} local songs` : "No local music found");
  setText("#repeatVolumeValue", `${state.volume}%`);
  setDisabled("#repeatPlayButton", !hasTracks);
  setDisabled("#repeatPrevButton", state.homepageTracks.length < 2);
  setDisabled("#repeatNextButton", state.homepageTracks.length < 2);

  const playButton = document.querySelector("#repeatPlayButton");
  if (playButton) {
    playButton.innerHTML = state.homepageMusicPlaying ? "&#10074;&#10074;" : "&#9654;";
    playButton.setAttribute("aria-label", state.homepageMusicPlaying ? "Pause repeated song sequence" : "Play repeated song sequence");
  }

  const volume = document.querySelector("#repeatVolumeControl");
  if (volume) {
    volume.disabled = !hasTracks;
    volume.value = String(state.volume);
  }

  const hasDuration = hasTracks && Number.isFinite(repeatAudio?.duration) && repeatAudio.duration > 0;
  const transport = document.querySelector(".repeat-transport");
  if (transport) {
    transport.style.setProperty(
      "--repeat-progress",
      `${hasDuration ? clampPercent((repeatAudio.currentTime / repeatAudio.duration) * 100) : 0}%`,
    );
  }
}

function getHomepagePlaybackStatus(hasTracks) {
  if (!hasTracks) return "No music";
  if (state.homepageMusicPlaying) return "Playing";
  if (state.homepageAutoplayBlocked) return "Tap play to start";
  return "Paused";
}

function syncHomepageAudioSource(track) {
  if (!repeatAudio || !track?.audioSrc) return false;
  const soundEnabled = isActiveSoundEnabled();
  applyGlobalSoundPreference(soundEnabled);
  repeatAudio.autoplay = soundEnabled;
  if (soundEnabled) {
    repeatAudio.setAttribute("autoplay", "");
  } else {
    repeatAudio.removeAttribute("autoplay");
  }
  repeatAudio.volume = getHomepageAudioVolume();
  const resolved = new URL(track.audioSrc, window.location.href).href;
  if (repeatAudio.src !== resolved) {
    repeatAudio.src = track.audioSrc;
    repeatAudio.load();
  }
  applyHomepageRestoreTime();
  return true;
}

function applyHomepageRestoreTime() {
  if (!repeatAudio || !state.homepageRestoreTime) return;
  const restoreTime = state.homepageRestoreTime;
  const apply = () => {
    if (Number.isFinite(repeatAudio.duration) && repeatAudio.duration > restoreTime + 1) {
      repeatAudio.currentTime = restoreTime;
    }
    state.homepageRestoreTime = 0;
  };
  if (repeatAudio.readyState >= 1) {
    apply();
  } else {
    repeatAudio.addEventListener("loadedmetadata", apply, { once: true });
  }
}

function getHomepageAudioVolume() {
  return (state.volume / 100) * HOMEPAGE_MUSIC_MAX_GAIN;
}

function getHomepageDisplayTitle(track) {
  if (!track) return "";
  const title = getLocalTrackTitleText(track);
  const artist = getDisplayArtist(track.artist);
  return artist ? `${title} / ${artist}` : title;
}

function getDisplayArtist(artist) {
  return String(artist || "")
    .replace(/\s*_\s*/g, " & ")
    .replace(/\s*&\s*/g, " & ")
    .replace(/\s+/g, " ")
    .trim();
}

async function startHomepageAudio() {
  if (!hasActiveSoundChoice()) {
    state.homepageMusicPlaying = false;
    renderHomepageMusicPlayer();
    return;
  }
  setMusicPlaybackRequested(true);
  const track = getCurrentHomepageTrack();
  if (!track || !syncHomepageAudioSource(track)) {
    state.homepageMusicPlaying = false;
    state.homepageMusicPendingStart = true;
    renderHomepageMusicPlayer();
    return;
  }

  state.homepageMusicPendingStart = false;
  state.homepageAutoplayBlocked = false;
  try {
    await repeatAudio.play();
    state.homepageMusicPlaying = true;
    window.lingerLastHomepageAudioError = "";
  } catch {
    try {
      await waitForAudioReady(repeatAudio);
      await repeatAudio.play();
      state.homepageMusicPlaying = true;
      window.lingerLastHomepageAudioError = "";
    } catch (error) {
      window.lingerLastHomepageAudioError = error?.message || String(error || "Audio play failed");
      state.homepageAutoplayBlocked = error?.name === "NotAllowedError" || /gesture|allowed|permission|interact/i.test(window.lingerLastHomepageAudioError);
      state.homepageMusicPlaying = false;
      if (state.homepageAutoplayBlocked) scheduleHomepageGestureResume();
    }
  }
  renderHomepageMusicPlayer();
  saveHomepagePlaybackState();
}

function waitForAudioReady(audio) {
  if (!audio) return Promise.reject(new Error("Missing audio element"));
  if (audio.readyState >= 3) return Promise.resolve();

  return new Promise((resolve, reject) => {
    const cleanup = () => {
      audio.removeEventListener("canplay", handleReady);
      audio.removeEventListener("loadeddata", handleReady);
      audio.removeEventListener("error", handleError);
    };
    const handleReady = () => {
      cleanup();
      resolve();
    };
    const handleError = () => {
      cleanup();
      reject(new Error("Audio could not load"));
    };
    audio.addEventListener("canplay", handleReady, { once: true });
    audio.addEventListener("loadeddata", handleReady, { once: true });
    audio.addEventListener("error", handleError, { once: true });
  });
}

let homepageGestureResumeBound = false;

function scheduleHomepageGestureResume() {
  if (homepageGestureResumeBound) return;
  homepageGestureResumeBound = true;
  const resume = (event) => {
    document.removeEventListener("pointerdown", resume, true);
    document.removeEventListener("keydown", resume, true);
    homepageGestureResumeBound = false;
    // Let explicit transport / sound-toggle interactions handle playback themselves.
    if (event.target?.closest?.(".repeat-transport button, .hover-sound-toggle, .hover-sound-prompt")) return;
    if (!state.homepageMusicPlaying && hasActiveSoundChoice() && isMusicPlaybackRequested()) {
      startHomepageAudio();
    }
  };
  document.addEventListener("pointerdown", resume, true);
  document.addEventListener("keydown", resume, true);
}

function stopHomepageAudio() {
  if (repeatAudio && !repeatAudio.paused) repeatAudio.pause();
  state.homepageMusicPlaying = false;
  saveHomepagePlaybackState();
}

function toggleHomepageAudio() {
  state.homepageAutoplayBlocked = false;
  if (state.homepageMusicPlaying) {
    setMusicPlaybackRequested(false);
    stopHomepageAudio();
    renderHomepageMusicPlayer();
    return;
  }
  startHomepageAudio();
}

function moveHomepageTrack(direction) {
  if (!state.homepageTracks.length) return;
  const shouldResume = state.homepageMusicPlaying;
  stopHomepageAudio();
  state.homepageMusicIndex = direction > 0
    ? getRandomHomepageTrackIndex()
    : (state.homepageMusicIndex + direction + state.homepageTracks.length) % state.homepageTracks.length;
  renderHomepageMusicPlayer();
  if (shouldResume) startHomepageAudio();
}

function handleHomepageAudioEnded() {
  if (!state.homepageTracks.length) return;
  state.homepageMusicIndex = getRandomHomepageTrackIndex();
  renderHomepageMusicPlayer();
  if (state.homepageMusicPlaying) startHomepageAudio();
}

function getRandomHomepageTrackIndex() {
  if (state.homepageTracks.length < 2) return 0;
  let nextIndex = state.homepageMusicIndex;
  while (nextIndex === state.homepageMusicIndex) {
    nextIndex = Math.floor(Math.random() * state.homepageTracks.length);
  }
  return nextIndex;
}

function readHomepagePlaybackState() {
  try {
    return JSON.parse(window.sessionStorage.getItem(HOMEPAGE_PLAYBACK_KEY) || "{}");
  } catch {
    return {};
  }
}

function saveHomepagePlaybackState() {
  if (!repeatAudio) return;
  try {
    window.sessionStorage.setItem(HOMEPAGE_PLAYBACK_KEY, JSON.stringify({
      index: state.homepageMusicIndex,
      time: Number.isFinite(repeatAudio.currentTime) ? repeatAudio.currentTime : 0,
      playing: state.homepageMusicPlaying,
    }));
  } catch {
    // Session storage can be unavailable in some embedded/private contexts.
  }
}

function restoreHomepagePlaybackState() {
  const saved = readHomepagePlaybackState();
  if (!Number.isFinite(Number(saved.index)) || !state.homepageTracks.length) return;
  state.homepageMusicIndex = Math.max(0, Math.min(Number(saved.index), state.homepageTracks.length - 1));
  state.homepageRestoreTime = Math.max(0, Number(saved.time) || 0);
}

function renderRoom(room) {
  const visual = document.querySelector("#zoomRoom");
  if (!visual) return;
  visual.innerHTML = `
    <article class="zoom-page">
      <div class="zoom-visual">
        <div class="room-visual-stack">
          <div class="static-room-frame">
            <img src="${room.image}" alt="${escapeHtml(room.title)} space" />
            ${renderRoomLiveLayer(state.selectedYear)}
          </div>
          <section class="memory-control-shell" aria-label="Year music control">
            <iframe
              id="memoryControlFrame"
              class="memory-control-frame"
              title="Memory Space music control"
              loading="eager"
              allow="autoplay"
            ></iframe>
          </section>
        </div>
      </div>
      ${roomBottomActionsMarkup()}
    </article>
  `;
}

function renderMemoryControlFrame() {
  const frame = document.querySelector("#memoryControlFrame");
  if (!frame) return;
  frame.addEventListener("load", () => {
    postMusicFrameMessage({
      type: SOUND_CHANGE_EVENT,
      enabled: isActiveSoundEnabled(),
      choiceSettled: hasActiveSoundChoice(),
    });
    postYearPlaybackStates();
    if ((hasActiveSoundChoice() && isMusicPlaybackRequested()) || state.roomPendingMusicStart || frame.dataset.pendingMusicStart === "1") {
      startYearControlMusic();
    }
  }, { once: true });
  const resetPlayback = isPageRefresh() ? "&resetPlayback=1" : "";
  frame.src = `control.html?year=${state.selectedYear}&embed=memory${resetPlayback}&v=direct-year-play-49`;
}

function bindRoomYearNavigation() {
  document.querySelector(".room-bottom-actions")?.addEventListener("click", (event) => {
    const link = event.target.closest(".year-jump-button");
    if (!link) return;
    const year = Number(new URL(link.href, window.location.href).searchParams.get("year"));
    if (!YEARS.includes(year)) return;
    event.preventDefault();
    navigateRoomYear(year, { userInitiated: true });
  });
  window.addEventListener("popstate", () => {
    navigateRoomYear(getSelectedYear(), { push: false });
  });
}

function navigateRoomYear(year, options = {}) {
  if (!YEARS.includes(year)) return;
  if (year === state.selectedYear) {
    if (options.userInitiated && isMusicAutoplayEnabled()) {
      startYearControlMusic();
    }
    return;
  }

  state.selectedYear = year;
  state.roomMusicIndex = 0;
  state.roomMusicSeededYear = null;
  state.roomRestoreTime = 0;
  const room = ROOM_INFO[year] || ROOM_INFO[2022];
  updateRoomShell(room);
  renderRoomMusicPlayer();

  if (options.push !== false) {
    safeHistoryPushState(`room.html?year=${year}`);
  }

  const shouldAutoplay = hasActiveSoundChoice() && isMusicPlaybackRequested();
  setControlFrameYear(year, { autoplay: shouldAutoplay });
}

function updateRoomShell(room) {
  document.body.dataset.roomYear = String(state.selectedYear);
  document.body.dataset.roomTone = room.tone;
  document.body.style.setProperty("--room-bg-image", `url("${room.background}")`);
  setText("#roomTitle", room.title);
  setText("#roomSummary", room.summary);
  document.querySelector("#personaTags")?.replaceChildren(...room.tags.map((tag) => {
    const item = document.createElement("span");
    item.textContent = tag;
    return item;
  }));

  const staticFrame = document.querySelector(".static-room-frame");
  const image = staticFrame?.querySelector("img");
  if (image) {
    image.src = room.image;
    image.alt = `${room.title} space`;
  }
  staticFrame?.querySelector(".room-live-layer")?.remove();
  const liveMarkup = renderRoomLiveLayer(state.selectedYear).trim();
  if (staticFrame && liveMarkup) {
    const template = document.createElement("template");
    template.innerHTML = liveMarkup;
    staticFrame.append(template.content);
  }

  document.querySelectorAll(".year-jump-button").forEach((link) => {
    const linkYear = Number(new URL(link.href, window.location.href).searchParams.get("year"));
    link.classList.toggle("active", linkYear === state.selectedYear);
  });
}

function setControlFrameYear(year, options = {}) {
  const frame = document.querySelector("#memoryControlFrame");
  if (!frame) return;
  const autoplay = options.autoplay ? "&autoplay=1" : "";
  frame.addEventListener("load", () => {
    postMusicFrameMessage({
      type: SOUND_CHANGE_EVENT,
      enabled: isActiveSoundEnabled(),
      choiceSettled: hasActiveSoundChoice(),
    });
    postYearPlaybackStates();
    if (options.autoplay) startYearControlMusic();
  }, { once: true });
  frame.src = `control.html?year=${year}&embed=memory${autoplay}&v=direct-year-play-49`;
}

function roomBottomActionsMarkup() {
  const yearLinks = YEARS.map((year) => {
    const active = year === state.selectedYear ? " active" : "";
    return `<a class="secondary-button year-jump-button${active}" href="room.html?year=${year}" aria-label="Open ${year} room">${year}</a>`;
  }).join("");
  return `
    <div class="room-bottom-actions room-actions" aria-label="Room year navigation">
      <a class="secondary-button room-back-icon" href="index.html#home" aria-label="Back to overview">&#8592;</a>
      ${yearLinks}
    </div>
  `;
}

function renderRoomLiveLayer(year) {
  const effects = ROOM_LIVE_EFFECTS[year] || [];
  if (!effects.length) return "";
  return `
    <div class="room-live-layer" aria-hidden="true">
      ${effects.map((effect, index) => liveEffectMarkup(effect, index)).join("")}
    </div>
  `;
}

function liveEffectMarkup(effect, index) {
  const style = [
    `left:${effect.x}%`,
    `top:${effect.y}%`,
    `width:${effect.w}%`,
    `height:${effect.h}%`,
    `--live-rotate:${effect.rotate || 0}deg`,
    `--live-opacity:${effect.opacity ?? 0.5}`,
    `--live-delay:${effect.delay || 0}s`,
    effect.color ? `--live-color:${effect.color}` : "",
  ].filter(Boolean).join("; ");
  return `<span class="live-effect live-${effect.type}" style="${style}" data-live-index="${index}"></span>`;
}

function controllerMarkup() {
  const tracks = getRoomMusicTracks();
  const current = tracks[state.roomMusicIndex] || tracks[0] || null;
  const title = current?.title || "No local music";
  const artist = current?.artist || "assets/audio";
  const visibleTracks = (tracks.length ? tracks : [{ title: "Add music to audio folder" }]).slice(0, 5);
  return `
    <section class="room-controller-shell" aria-label="${state.selectedYear} music controller">
      <div class="room-control-layer year-control"><small>YEAR</small><strong>${state.selectedYear}</strong></div>
      <div class="room-control-layer volume-control"><small>VOLUME</small><label class="volume-clay-control" for="roomMusicVolumeControl"><span class="volume-clay-ring" aria-hidden="true"><span class="volume-clay-knob"></span></span>${volumeIconMarkup()}<span id="roomMusicVolumeValue">${state.volume}%</span><input id="roomMusicVolumeControl" class="room-volume-range" type="range" min="0" max="100" value="${state.volume}" aria-label="Room music volume" /></label></div>
      <div class="room-control-layer current-music-control"><small>CURRENT MUSIC</small><div class="current-music-title-line"><strong id="roomNowPlayingTitle" title="${escapeHtml(title)}">${escapeHtml(trimText(title, 34))}</strong><span id="roomNowPlayingArtist" title="${escapeHtml(artist)}">${escapeHtml(trimText(artist, 24))}</span><em id="roomMusicStatus" class="sr-only">${current ? "Ready" : "No audio"}</em></div><div class="current-music-progress-line"><span id="roomMusicCurrentTime">0:00</span><div class="progress-track transport-progress-track"><i id="roomMusicProgressFill"></i></div><span id="roomMusicDurationTime">0:00</span></div></div>
      <div class="room-control-layer transport-control"><small>TRANSPORT</small><button id="roomPlayModeButton" class="play-mode-button" type="button" aria-label="Change room play mode">${getRoomPlayModeLabel()}</button><div class="transport-buttons"><button id="roomMusicRestartButton" class="transport-side-button" type="button" aria-label="Restart room song">&#8634;</button><button id="roomMusicPrevButton" class="transport-side-button" type="button" aria-label="Previous room song">&#10073;&#9664;</button><button id="roomMusicPlayButton" class="transport-play-button" type="button" aria-label="Play room music">&#9654;</button><button id="roomMusicNextButton" class="transport-side-button" type="button" aria-label="Next room song">&#9654;&#10073;</button></div></div>
      <div class="room-control-layer song-list-control"><small>MUSIC LIST</small><ol id="roomMusicSongList">${visibleTracks.map((track) => `<li title="${escapeHtml(track.title)}">${escapeHtml(trimText(track.title, 34))}</li>`).join("")}</ol></div>
    </section>
  `;
}

function volumeIconMarkup() {
  return `
    <span class="room-volume-icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" focusable="false">
        <path d="M4 9.5h4l5-4v13l-5-4H4z"></path>
        <path d="M16 8.5c1.2 1 2 2.1 2 3.5s-.8 2.5-2 3.5"></path>
        <path d="M18.5 6c1.9 1.6 3 3.6 3 6s-1.1 4.4-3 6"></path>
      </svg>
    </span>
  `;
}

function bindRoomAudio() {
  document.querySelector("#roomPlayModeButton")?.addEventListener("click", cycleRoomPlayMode);
  document.querySelector("#roomMusicRestartButton")?.addEventListener("click", restartRoomMusicTrack);
  document.querySelector("#roomMusicPrevButton")?.addEventListener("click", () => moveRoomMusicTrack(-1));
  document.querySelector("#roomMusicPlayButton")?.addEventListener("click", toggleRoomMusicPlayback);
  document.querySelector("#roomMusicNextButton")?.addEventListener("click", () => moveRoomMusicTrack(1));
  document.querySelector("#roomMusicVolumeControl")?.addEventListener("input", (event) => setRoomVolume(Number(event.target.value)));
  roomAudio?.addEventListener("timeupdate", () => {
    renderProgress(Boolean(getCurrentRoomMusicTrack()));
    postParentRoomPlaybackState();
    saveRoomPlaybackState();
  });
  roomAudio?.addEventListener("loadedmetadata", postParentRoomPlaybackState);
  roomAudio?.addEventListener("play", () => {
    postParentRoomPlaybackState();
    saveRoomPlaybackState({ force: true });
  });
  roomAudio?.addEventListener("pause", () => {
    postParentRoomPlaybackState();
    saveRoomPlaybackState({ force: true });
  });
  roomAudio?.addEventListener("ended", handleRoomMusicEnded);
  window.addEventListener("pagehide", () => saveRoomPlaybackState({ force: true }));
  window.addEventListener("beforeunload", () => saveRoomPlaybackState({ force: true }));
}

function getRoomMusicTracks() {
  return state.localAudioFiles
    .filter((file) => {
      const normalized = String(file.path || "").replace(/\\/g, "/").toLowerCase();
      return isRoomMusicFilePath(normalized);
    })
    .filter((file) => AUDIO_EXTENSIONS.test(file.name || file.path || ""))
    .map(fileToLocalAudioTrack);
}

function isRoomMusicFilePath(normalizedPath) {
  if (!normalizedPath) return false;
  if (normalizedPath.startsWith(`${state.selectedYear} music/`) || normalizedPath.startsWith(`${state.selectedYear}/`)) {
    return true;
  }
  return !normalizedPath.includes("/");
}

function getCurrentRoomMusicTrack() {
  const tracks = getRoomMusicTracks();
  if (!tracks.length) return null;
  state.roomMusicIndex = Math.max(0, Math.min(state.roomMusicIndex, tracks.length - 1));
  return tracks[state.roomMusicIndex] || tracks[0];
}

function renderRoomMusicPlayer() {
  const tracks = getRoomMusicTracks();
  document.body.classList.toggle("room-has-local-music", Boolean(tracks.length));
  if (tracks.length && state.roomMusicSeededYear !== state.selectedYear) {
    state.roomMusicIndex = 0;
    state.roomMusicSeededYear = state.selectedYear;
  }
  const current = getCurrentRoomMusicTrack();
  const hasTracks = Boolean(current);
  const currentTitle = getLocalTrackTitleText(current) || "No local music";
  setText("#roomNowPlayingTitle", trimText(currentTitle, 52), currentTitle);
  setText("#roomNowPlayingArtist", trimText(current?.artist || `Add files to assets/audio`, 24), current?.artist || "");
  setText("#roomMusicStatus", hasTracks ? (state.roomMusicPlaying ? "Playing" : "Ready") : "No audio");
  setText("#roomPlayModeButton", getRoomPlayModeLabel());
  setDisabled("#roomPlayModeButton", !hasTracks);
  setDisabled("#roomMusicRestartButton", !hasTracks);
  setDisabled("#roomMusicPlayButton", !hasTracks);
  setDisabled("#roomMusicPrevButton", tracks.length < 2);
  setDisabled("#roomMusicNextButton", tracks.length < 2);
  const playButton = document.querySelector("#roomMusicPlayButton");
  if (playButton) {
    playButton.innerHTML = state.roomMusicPlaying ? "&#10074;&#10074;" : "&#9654;";
    playButton.setAttribute("aria-label", state.roomMusicPlaying ? "Pause room music" : "Play room music");
  }
  renderSongList(tracks);
  renderProgress(hasTracks);
  const volume = document.querySelector("#roomMusicVolumeControl");
  if (volume) {
    volume.disabled = !hasTracks;
    volume.value = String(state.volume);
  }
  setText("#roomMusicVolumeValue", `${state.volume}%`);
}

function renderSongList(tracks) {
  const list = document.querySelector("#roomMusicSongList");
  if (!list) return;
  list.replaceChildren(...(tracks.length ? tracks : [{ title: `Add music to audio folder` }]).slice(0, 5).map((track, index) => {
    const item = document.createElement("li");
    if (!tracks.length) {
      item.textContent = track.title;
      return item;
    }
    const button = document.createElement("button");
    button.type = "button";
    button.className = index === state.roomMusicIndex ? "active" : "";
    const displayTitle = getLocalTrackTitleText(track);
    button.textContent = trimText(displayTitle, 52);
    button.title = displayTitle;
    button.addEventListener("click", () => {
      state.roomMusicIndex = index;
      startRoomMusicAudio();
    });
    item.append(button);
    return item;
  }));
}

function renderProgress(hasTracks) {
  const hasDuration = hasTracks && Number.isFinite(roomAudio?.duration) && roomAudio.duration > 0;
  const progress = hasDuration ? clampPercent((roomAudio.currentTime / roomAudio.duration) * 100) : 0;
  const fill = document.querySelector("#roomMusicProgressFill");
  if (fill) fill.style.width = `${progress}%`;
  setText("#roomMusicCurrentTime", hasDuration ? formatTime(roomAudio.currentTime) : "0:00");
  setText("#roomMusicDurationTime", hasDuration ? formatTime(roomAudio.duration) : "0:00");
}

function postParentRoomPlaybackState() {
  if (document.body.dataset.page !== "room") return;
  const current = getCurrentRoomMusicTrack();
  postMusicFrameMessage({
    type: YEAR_PARENT_PLAYBACK_EVENT,
    year: state.selectedYear,
    index: state.roomMusicIndex,
    title: current?.title || "",
    artist: current?.artist || "",
    currentTime: Number.isFinite(roomAudio?.currentTime) ? roomAudio.currentTime : 0,
    duration: Number.isFinite(roomAudio?.duration) ? roomAudio.duration : 0,
    playing: Boolean(state.roomMusicPlaying && roomAudio && !roomAudio.paused),
    playMode: state.roomPlayMode,
    active: Boolean(roomAudio?.src),
  });
}

function getRoomPlaybackKey() {
  return `${YEAR_PLAYBACK_KEY_PREFIX}${state.selectedYear}`;
}

function readRoomPlaybackState() {
  try {
    return JSON.parse(window.sessionStorage.getItem(getRoomPlaybackKey()) || "{}");
  } catch {
    return {};
  }
}

function saveRoomPlaybackState(options = {}) {
  if (document.body.dataset.page !== "room") return;
  const now = window.performance?.now?.() ?? Date.now();
  if (!options.force && now - state.roomLastPlaybackSaveAt < 1500) return;
  state.roomLastPlaybackSaveAt = now;
  try {
    window.sessionStorage.setItem(getRoomPlaybackKey(), JSON.stringify({
      index: state.roomMusicIndex,
      time: Number.isFinite(roomAudio?.currentTime) ? roomAudio.currentTime : 0,
      playing: Boolean(state.roomMusicPlaying && roomAudio && !roomAudio.paused),
      playMode: state.roomPlayMode,
    }));
  } catch {
    // Session storage can be unavailable in some embedded/private contexts.
  }
}

function restoreRoomPlaybackState() {
  const saved = readRoomPlaybackState();
  const tracks = getRoomMusicTracks();
  if (!tracks.length) return;
  if (Number.isFinite(Number(saved.index))) {
    state.roomMusicIndex = Math.max(0, Math.min(Number(saved.index), tracks.length - 1));
    state.roomMusicSeededYear = state.selectedYear;
  }
  const savedMode = PLAY_MODES.find((mode) => mode.id === saved.playMode)?.id;
  if (savedMode) state.roomPlayMode = savedMode;
  state.roomRestoreTime = Math.max(0, Number(saved.time) || 0);
}

function applyRoomRestoreTime() {
  if (!roomAudio || !state.roomRestoreTime) return;
  const restoreTime = state.roomRestoreTime;
  const apply = () => {
    if (Number.isFinite(roomAudio.duration) && roomAudio.duration > restoreTime + 1) {
      roomAudio.currentTime = restoreTime;
    }
    state.roomRestoreTime = 0;
    renderRoomMusicPlayer();
    postParentRoomPlaybackState();
  };
  if (Number.isFinite(roomAudio.duration) && roomAudio.duration > 0) {
    apply();
    return;
  }
  roomAudio.addEventListener("loadedmetadata", apply, { once: true });
}

function syncRoomMusicAudioSource(track) {
  if (!roomAudio || !track?.audioSrc) return false;
  applyGlobalSoundPreference();
  roomAudio.volume = getYearMusicAudioVolume();
  const resolved = new URL(track.audioSrc, window.location.href).href;
  if (roomAudio.src !== resolved) {
    if (!roomAudio.paused) roomAudio.pause();
    roomAudio.src = track.audioSrc;
    roomAudio.load();
  }
  applyRoomRestoreTime();
  return true;
}

async function startRoomMusicAudio() {
  if (!hasActiveSoundChoice()) {
    state.roomMusicPlaying = false;
    renderRoomMusicPlayer();
    return;
  }
  const track = getCurrentRoomMusicTrack();
  if (!track || !syncRoomMusicAudioSource(track)) {
    state.roomMusicPlaying = false;
    renderRoomMusicPlayer();
    return;
  }
  const wantsAudiblePlayback = isActiveSoundEnabled();
  setMusicPlaybackRequested(true);
  try {
    roomAudio.muted = true;
    await roomAudio.play();
    state.roomMusicPlaying = true;
    state.roomPendingMusicStart = false;
    roomAudio.muted = !wantsAudiblePlayback;
  } catch {
    state.roomMusicPlaying = false;
    roomAudio.muted = !isActiveSoundEnabled();
  }
  renderRoomMusicPlayer();
  postParentRoomPlaybackState();
  saveRoomPlaybackState({ force: true });
}

function stopRoomMusicAudio() {
  if (roomAudio && !roomAudio.paused) roomAudio.pause();
  state.roomMusicPlaying = false;
  postParentRoomPlaybackState();
  saveRoomPlaybackState({ force: true });
}

function toggleRoomMusicPlayback() {
  if (state.roomMusicPlaying) {
    setMusicPlaybackRequested(false);
    stopRoomMusicAudio();
    renderRoomMusicPlayer();
    return;
  }
  startRoomMusicAudio();
}

function restartRoomMusicTrack() {
  if (!roomAudio) return;
  roomAudio.currentTime = 0;
  if (state.roomMusicPlaying) startRoomMusicAudio();
  renderRoomMusicPlayer();
  postParentRoomPlaybackState();
  saveRoomPlaybackState({ force: true });
}

function moveRoomMusicTrack(direction) {
  const tracks = getRoomMusicTracks();
  if (!tracks.length) return;
  const shouldResume = state.roomMusicPlaying;
  stopRoomMusicAudio();
  state.roomMusicIndex = getNextRoomMusicIndex(direction, tracks, { manual: true });
  state.roomRestoreTime = 0;
  renderRoomMusicPlayer();
  postParentRoomPlaybackState();
  saveRoomPlaybackState({ force: true });
  if (shouldResume) startRoomMusicAudio();
}

function handleRoomMusicEnded() {
  const tracks = getRoomMusicTracks();
  if (!tracks.length) return;
  if (state.roomPlayMode === "single") {
    roomAudio.currentTime = 0;
  } else {
    state.roomMusicIndex = getNextRoomMusicIndex(1, tracks);
  }
  renderRoomMusicPlayer();
  postParentRoomPlaybackState();
  saveRoomPlaybackState({ force: true });
  if (state.roomMusicPlaying) startRoomMusicAudio();
}

function getNextRoomMusicIndex(direction, tracks, options = {}) {
  if (state.roomPlayMode === "single" && !options.manual) return state.roomMusicIndex;
  if (state.roomPlayMode === "shuffle" && direction > 0 && tracks.length > 1) {
    let next = state.roomMusicIndex;
    while (next === state.roomMusicIndex) next = Math.floor(Math.random() * tracks.length);
    return next;
  }
  return (state.roomMusicIndex + direction + tracks.length) % tracks.length;
}

function getRoomPlayModeLabel() {
  return PLAY_MODES.find((mode) => mode.id === state.roomPlayMode)?.label || PLAY_MODES[0].label;
}

function cycleRoomPlayMode() {
  const currentIndex = PLAY_MODES.findIndex((mode) => mode.id === state.roomPlayMode);
  state.roomPlayMode = PLAY_MODES[(currentIndex + 1 + PLAY_MODES.length) % PLAY_MODES.length].id;
  renderRoomMusicPlayer();
  postParentRoomPlaybackState();
  saveRoomPlaybackState({ force: true });
}

function setRoomVolume(value) {
  applySharedVolume(value);
}

function getYearMusicAudioVolume() {
  return (state.volume / 100) * YEAR_MUSIC_MAX_GAIN;
}

function setText(selector, value, title = null) {
  const element = document.querySelector(selector);
  if (!element) return;
  element.textContent = value;
  if (title !== null) element.title = title;
}

function setDisabled(selector, disabled) {
  const element = document.querySelector(selector);
  if (element) element.disabled = disabled;
}

function trimText(value, maxLength) {
  const text = String(value ?? "").trim();
  return text.length <= maxLength ? text : `${text.slice(0, Math.max(0, maxLength - 3)).trimEnd()}...`;
}

function formatTime(value) {
  const seconds = Math.max(0, Math.floor(Number(value) || 0));
  return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
}

function clampPercent(value) {
  return Math.max(0, Math.min(100, Number.isFinite(value) ? value : 0));
}

function clamp01(value) {
  return Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0));
}

function fadeRange(value, start, end) {
  return clamp01((value - start) / (end - start));
}

function smoothStep(value) {
  const progress = clamp01(value);
  return progress * progress * (3 - 2 * progress);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[character]);
}
