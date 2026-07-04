(() => {
  const spaces = Array.from(document.querySelectorAll(".hero-space"));
  const alphaMaps = new Map();
  const SOUND_COOLDOWN_MS = 90;
  const HOVER_SOUND = { pitch: 320, gain: 0.045, duration: 0.045, noise: 0.012, filter: 1450 };
  const SOUND_CHANGE_EVENT = "linger:soundchange";
  const HOMEPAGE_AUDIO_READY_EVENT = "linger:homepageready";
  const SOUND_CHOICE_KEY = "linger:sound-choice";
  const MUSIC_AUTOPLAY_KEY = "linger:music-autoplay-enabled";
  const MUSIC_PLAY_STATE_KEY = "linger:music-playing";
  const HOMEPAGE_PLAYBACK_KEY = "linger:playback:homepage";
  const YEAR_PLAYBACK_KEY_PREFIX = "linger:playback:year:";
  let activeSpace = null;
  let audioContext = null;
  let hoverSoundEnabled = false;
  let lastSoundAt = 0;
  let hitTestingStarted = false;

  resetSoundChoiceOnRefresh();

  function isPageRefresh() {
    const navigation = performance.getEntriesByType?.("navigation")?.[0];
    return navigation?.type === "reload";
  }

  function resetSoundChoiceOnRefresh() {
    if (!isPageRefresh()) return;
    try {
      // A reload triggered by the in-page back-to-homepage link is treated
      // as navigation: keep the sound choice and playback state.
      // (app.js consumes/removes the flag afterwards.)
      if (window.sessionStorage.getItem("linger:internal-home-nav") === "1") return;
    } catch {
      // fall through to the normal reset below
    }
    try {
      window.sessionStorage.removeItem(SOUND_CHOICE_KEY);
      window.sessionStorage.removeItem(MUSIC_AUTOPLAY_KEY);
      window.sessionStorage.removeItem(MUSIC_PLAY_STATE_KEY);
      window.localStorage.removeItem(MUSIC_PLAY_STATE_KEY);
      window.sessionStorage.removeItem(HOMEPAGE_PLAYBACK_KEY);
      [...Array(window.sessionStorage.length).keys()]
        .map((index) => window.sessionStorage.key(index))
        .filter((key) => key?.startsWith(YEAR_PLAYBACK_KEY_PREFIX))
        .forEach((key) => window.sessionStorage.removeItem(key));
    } catch {
      // Session storage can be unavailable in some embedded/private contexts.
    }
  }

  function readSoundChoice() {
    try {
      const value = window.sessionStorage.getItem(SOUND_CHOICE_KEY);
      return value === "on" || value === "off" ? value : null;
    } catch {
      return null;
    }
  }

  function writeSoundChoice(enabled) {
    try {
      window.sessionStorage.setItem(SOUND_CHOICE_KEY, enabled ? "on" : "off");
    } catch {
      // Session storage can be unavailable in some embedded/private contexts.
    }
  }

  function ensureAudioContext() {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return null;
    audioContext ||= new AudioContextClass();
    if (audioContext.state === "suspended") {
      audioContext.resume().catch(() => {});
    }
    return audioContext;
  }

  function unlockHoverAudio() {
    ensureAudioContext();
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

  function broadcastSoundChoice(initialChoice = false) {
    writeSoundChoice(hoverSoundEnabled);
    window.dispatchEvent(new CustomEvent(SOUND_CHANGE_EVENT, {
      detail: { enabled: hoverSoundEnabled, initialChoice },
    }));
  }

  function startCurrentPageMusic() {
    if (typeof window.startLingerPageAudio === "function") {
      const result = window.startLingerPageAudio();
      if (result && typeof result.catch === "function") {
        result.catch(() => clickMusicPlayFallback());
      }
      window.setTimeout(clickMusicPlayFallback, 120);
      return;
    }
    if (typeof window.startLingerHomepageAudio === "function") {
      const result = window.startLingerHomepageAudio();
      if (result && typeof result.catch === "function") {
        result.catch(() => clickMusicPlayFallback());
      }
      window.setTimeout(clickMusicPlayFallback, 120);
      return;
    }

    clickMusicPlayFallback();
  }

  function clickMusicPlayFallback() {
    const audio = document.querySelector("#repeatAudio");
    const playButton = document.querySelector("#repeatPlayButton");
    if (audio?.paused && playButton && !playButton.disabled) {
      playButton.click();
    }
  }

  function playHoverSound() {
    if (!hoverSoundEnabled) return;

    const nowMs = window.performance?.now?.() ?? Date.now();
    if (nowMs - lastSoundAt < SOUND_COOLDOWN_MS) return;

    const audio = ensureAudioContext();
    if (!audio) return;
    if (audio.state === "suspended") {
      audio.resume().then(() => playHoverSound()).catch(() => {});
      return;
    }
    if (audio.state !== "running") return;

    lastSoundAt = nowMs;
    const now = audio.currentTime;
    const master = audio.createGain();
    master.gain.setValueAtTime(0.0001, now);
    master.gain.exponentialRampToValueAtTime(HOVER_SOUND.gain, now + 0.008);
    master.gain.exponentialRampToValueAtTime(0.0001, now + HOVER_SOUND.duration);
    master.connect(audio.destination);

    const oscillator = audio.createOscillator();
    oscillator.type = "triangle";
    oscillator.frequency.setValueAtTime(HOVER_SOUND.pitch, now);
    oscillator.frequency.exponentialRampToValueAtTime(HOVER_SOUND.pitch * 0.58, now + HOVER_SOUND.duration);
    oscillator.connect(master);
    oscillator.start(now);
    oscillator.stop(now + HOVER_SOUND.duration + 0.02);

    const bufferSize = Math.max(1, Math.floor(audio.sampleRate * HOVER_SOUND.duration));
    const buffer = audio.createBuffer(1, bufferSize, audio.sampleRate);
    const data = buffer.getChannelData(0);
    for (let index = 0; index < data.length; index += 1) {
      data[index] = (Math.random() * 2 - 1) * (1 - index / data.length) * HOVER_SOUND.noise;
    }

    const noiseSource = audio.createBufferSource();
    const lowpass = audio.createBiquadFilter();
    noiseSource.buffer = buffer;
    lowpass.type = "lowpass";
    lowpass.frequency.value = HOVER_SOUND.filter;
    noiseSource.connect(lowpass).connect(master);
    noiseSource.start(now);
  }

  function updateSoundToggle(button) {
    button.classList.toggle("is-on", hoverSoundEnabled);
    button.setAttribute("aria-pressed", String(hoverSoundEnabled));
    button.textContent = hoverSoundEnabled ? "Sound on" : "Sound off";
    button.title = hoverSoundEnabled ? "Turn hover sound off" : "Turn hover sound on";
  }

  function createSoundToggle() {
    if (document.querySelector(".hover-sound-toggle")) return;

    const savedChoice = readSoundChoice();
    let soundChoiceSettled = savedChoice !== null;
    hoverSoundEnabled = savedChoice === "on";

    const button = document.createElement("button");
    button.type = "button";
    button.className = "hover-sound-toggle";
    button.setAttribute("aria-label", "Toggle site sound");
    updateSoundToggle(button);
    button.addEventListener("click", () => {
      const isFirstSoundChoice = !soundChoiceSettled;
      hoverSoundEnabled = !hoverSoundEnabled;
      soundChoiceSettled = true;
      writeSoundChoice(hoverSoundEnabled);
      updateSoundToggle(button);
      if (isFirstSoundChoice && hoverSoundEnabled) enableMusicAutoplay();
      broadcastSoundChoice(isFirstSoundChoice);
      if (hoverSoundEnabled) {
        if (isFirstSoundChoice) startCurrentPageMusic();
        window.setTimeout(() => {
          unlockHoverAudio();
          playHoverSound();
        }, 180);
      }
    });
    (document.querySelector(".nav-right") || document.body).append(button);

    window.addEventListener(SOUND_CHANGE_EVENT, (event) => {
      if (typeof event.detail?.enabled !== "boolean") return;
      hoverSoundEnabled = event.detail.enabled;
      soundChoiceSettled = true;
      writeSoundChoice(hoverSoundEnabled);
      updateSoundToggle(button);
      document.querySelector(".hover-sound-prompt")?.remove();
    });

    if (!soundChoiceSettled) createSoundPrompt(button);
  }

  function createSoundPrompt(toggleButton) {
    const prompt = document.createElement("section");
    prompt.className = "hover-sound-prompt";
    prompt.setAttribute("aria-label", "Sound preference");
    prompt.innerHTML = `
      <p>Let the museum play sound?</p>
      <small>A music playback make the memory feel more alive. You can turn it off anytime.</small>
      <div>
        <button type="button" data-sound-choice="on">Turn sound on</button>
        <button type="button" data-sound-choice="off">Not now</button>
      </div>
    `;
    prompt.addEventListener("click", (event) => {
      const choiceButton = event.target.closest("[data-sound-choice]");
      if (!choiceButton) return;

      hoverSoundEnabled = choiceButton.dataset.soundChoice === "on";
      writeSoundChoice(hoverSoundEnabled);
      updateSoundToggle(toggleButton);
      if (hoverSoundEnabled) enableMusicAutoplay();
      broadcastSoundChoice(true);
      if (hoverSoundEnabled) {
        startCurrentPageMusic();
        window.setTimeout(() => {
          unlockHoverAudio();
          playHoverSound();
        }, 180);
      }
      prompt.remove();
    });
    (toggleButton.parentElement || document.body).append(prompt);
  }

  function loadAlphaMap(space) {
    const img = space.querySelector("img");
    if (!img) return Promise.resolve(null);

    return new Promise((resolve) => {
      const source = new Image();
      source.onload = () => {
        const canvas = document.createElement("canvas");
        canvas.width = source.naturalWidth;
        canvas.height = source.naturalHeight;
        const context = canvas.getContext("2d", { willReadFrequently: true });
        context.drawImage(source, 0, 0);
        const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
        const alphaMap = {
          width: canvas.width,
          height: canvas.height,
          pixels,
        };
        alphaMaps.set(space, alphaMap);
        resolve(alphaMap);
      };
      source.onerror = () => resolve(null);
      source.src = img.currentSrc || img.src;
    });
  }

  function hasVisiblePixel(space, clientX, clientY) {
    const alphaMap = alphaMaps.get(space);
    if (!alphaMap) return true;

    const parent = space.offsetParent;
    const parentRect = parent?.getBoundingClientRect();
    if (!parentRect || !space.offsetWidth || !space.offsetHeight) return false;

    const style = getComputedStyle(space);
    const transform = style.transform === "none" ? new DOMMatrix() : new DOMMatrix(style.transform);
    const [originX, originY] = style.transformOrigin
      .split(" ")
      .map((value) => Number.parseFloat(value) || 0);
    const matrix = new DOMMatrix()
      .translate(space.offsetLeft, space.offsetTop)
      .translate(originX, originY)
      .multiply(transform)
      .translate(-originX, -originY);
    const localPoint = new DOMPoint(
      clientX - parentRect.left,
      clientY - parentRect.top,
    ).matrixTransform(matrix.inverse());

    const x = Math.floor((localPoint.x / space.offsetWidth) * alphaMap.width);
    const y = Math.floor((localPoint.y / space.offsetHeight) * alphaMap.height);
    if (x < 0 || y < 0 || x >= alphaMap.width || y >= alphaMap.height) return false;

    return alphaMap.pixels[(y * alphaMap.width + x) * 4 + 3] > 24;
  }

  function topVisibleSpace(event) {
    return document
      .elementsFromPoint(event.clientX, event.clientY)
      .filter((element) => element.classList?.contains("hero-space"))
      .find((space) => hasVisiblePixel(space, event.clientX, event.clientY));
  }

  function updateHover(event) {
    const active = topVisibleSpace(event);
    spaces.forEach((space) => {
      space.classList.toggle("is-alpha-hit", space === active);
    });
    if (active && active !== activeSpace) {
      playHoverSound();
    }
    activeSpace = active;
  }

  function startHitTesting() {
    if (hitTestingStarted) return;
    hitTestingStarted = true;
    createSoundToggle();
    if (!spaces.length) return;

    document.addEventListener("pointermove", updateHover);
    document.addEventListener("pointerleave", () => {
      activeSpace = null;
      spaces.forEach((space) => space.classList.remove("is-alpha-hit"));
    });

    document.addEventListener(
      "click",
      (event) => {
        const targetSpace = event.target.closest?.(".hero-space");
        if (!targetSpace) return;

        const visibleSpace = topVisibleSpace(event);
        if (!visibleSpace) {
          event.preventDefault();
          return;
        }

        if (typeof window.lingerOpenMemoryRoomFromHomepage === "function"
          && window.lingerOpenMemoryRoomFromHomepage(visibleSpace.href)) {
          event.preventDefault();
          return;
        }

        if (visibleSpace !== targetSpace) {
          event.preventDefault();
          window.location.href = visibleSpace.href;
        }
      },
      true,
    );
  }

  function waitForHomepageAudioReady() {
    if (window.lingerHomepageAudioReady || !document.querySelector("#repeatAudio")) {
      startHitTesting();
      return;
    }

    window.addEventListener(HOMEPAGE_AUDIO_READY_EVENT, startHitTesting, { once: true });
    window.setTimeout(startHitTesting, 2200);
  }

  Promise.all(spaces.map(loadAlphaMap)).then(() => {
    waitForHomepageAudioReady();
  });
})();
