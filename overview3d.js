import * as THREE from "./vendor/three.module.min.js";
import { GLTFLoader } from "./vendor/loaders/GLTFLoader.js";

const MODEL = {
  year: 2024,
  href: "room.html?year=2024",
  url: "assets/models/rooms/2024-quiet-room.glb?v=blender-v3-showcase",
};

function initMount(mount) {
  if (!mount || mount.dataset.overview3d === "ready" || !window.WebGLRenderingContext) return;
  mount.dataset.overview3d = "loading";

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: "high-performance" });
  } catch {
    mount.dataset.overview3d = "failed";
    return;
  }

  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.8));
  renderer.setClearColor(0x000000, 0);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.domElement.className = "overview-3d-canvas";
  renderer.domElement.setAttribute("aria-label", "Interactive 3D 2024 music room");
  mount.append(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  camera.position.set(0, 1.35, 5.4);
  camera.lookAt(0, 0.94, -0.34);

  const ambient = new THREE.HemisphereLight(0xfff6e6, 0xb9c7bb, 2.5);
  scene.add(ambient);

  const key = new THREE.DirectionalLight(0xffffff, 2.4);
  key.position.set(-2.8, 4.5, 4.2);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  scene.add(key);

  const mouseLight = new THREE.PointLight(0xfff0b6, 0, 5.2);
  mouseLight.position.set(0, 1.2, 1.5);
  scene.add(mouseLight);

  const floorShadow = new THREE.Mesh(
    new THREE.CircleGeometry(1.7, 64),
    new THREE.ShadowMaterial({ opacity: 0.18 }),
  );
  floorShadow.rotation.x = -Math.PI / 2;
  floorShadow.position.set(0, -0.03, 0);
  floorShadow.receiveShadow = true;
  scene.add(floorShadow);

  const loader = new GLTFLoader();
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2(-10, -10);
  const animated = {
    group: null,
    lamp: null,
    wave: null,
    calendarTiles: [],
    records: [],
    hover: 0,
    targetHover: 0,
  };

  function resize() {
    const rect = mount.getBoundingClientRect();
    renderer.setSize(rect.width, rect.height, false);
    camera.aspect = rect.width / Math.max(rect.height, 1);
    camera.updateProjectionMatrix();
  }

  function setPointer(event) {
    const rect = renderer.domElement.getBoundingClientRect();
    pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -(((event.clientY - rect.top) / rect.height) * 2 - 1);
  }

  function pickRoom() {
    if (!animated.group) return null;
    raycaster.setFromCamera(pointer, camera);
    return raycaster.intersectObjects(animated.group.children, true)[0] || null;
  }

  function setHover(value) {
    animated.targetHover = value ? 1 : 0;
    mount.classList.toggle("is-pointing-space", !!value);
  }

  renderer.domElement.addEventListener("pointermove", (event) => {
    setPointer(event);
    setHover(!!pickRoom());
  });

  renderer.domElement.addEventListener("pointerleave", () => {
    pointer.set(-10, -10);
    setHover(false);
  });

  renderer.domElement.addEventListener("click", (event) => {
    setPointer(event);
    if (pickRoom()) window.location.href = MODEL.href;
  });

  loader.load(
    MODEL.url,
    (gltf) => {
      const room = gltf.scene;
      room.name = "real_3d_2024_quiet_room";
      room.position.set(0, -0.12, 0);
      room.rotation.set(-0.03, 0.02, 0);
      room.scale.setScalar(1.28);

      room.traverse((child) => {
        if (!child.isMesh) return;
        child.castShadow = true;
        child.receiveShadow = true;
        child.userData.clickable = true;
        if (child.material) {
          child.material.side = THREE.DoubleSide;
          child.material.needsUpdate = true;
        }
      });

      animated.group = room;
      animated.lamp = room.getObjectByName("lamp_glow");
      animated.wave = room.getObjectByName("wave_line");
      animated.calendarTiles = room.children.filter((child) => child.name.startsWith("calendar_tile_"));
      animated.records = room.children.filter((child) => child.name.includes("record_disc"));

      scene.add(room);
      mount.classList.add("has-3d", "has-real-3d-model");
      mount.closest(".hero")?.classList.add("has-image-overview", "has-real-3d-overview");
      mount.dataset.overview3d = "ready";
    },
    undefined,
    () => {
      mount.dataset.overview3d = "failed";
      renderer.domElement.remove();
    },
  );

  resize();
  window.addEventListener("resize", resize);

  const clock = new THREE.Clock();
  function animate() {
    const time = clock.getElapsedTime();
    animated.hover += (animated.targetHover - animated.hover) * 0.1;

    if (animated.group) {
      animated.group.position.y = -0.12 + animated.hover * 0.08 + Math.sin(time * 0.5) * 0.01;
      animated.group.rotation.x = -0.03 - animated.hover * 0.018;
      animated.group.rotation.y = 0.02 + pointer.x * 0.018 + animated.hover * 0.02;
      animated.group.scale.setScalar(1.28 + animated.hover * 0.035);
    }

    if (animated.lamp) {
      const pulse = 1 + Math.sin(time * 1.8) * 0.08 + animated.hover * 0.08;
      animated.lamp.scale.set(pulse, pulse, pulse);
      if (animated.lamp.material?.emissive) {
        animated.lamp.material.emissiveIntensity = 0.75 + Math.sin(time * 1.8) * 0.18 + animated.hover * 0.55;
      }
    }

    if (animated.wave) {
      animated.wave.position.y = Math.sin(time * 1.15) * 0.025;
      animated.wave.scale.y = 1 + Math.sin(time * 1.2) * 0.035;
      if (animated.wave.material?.emissive) {
        animated.wave.material.emissiveIntensity = 1.0 + Math.sin(time * 1.2) * 0.2 + animated.hover * 0.65;
      }
    }

    animated.calendarTiles.forEach((tile, index) => {
      const shimmer = 0.82 + Math.sin(time * 1.1 + index * 0.6) * 0.12 + animated.hover * 0.16;
      tile.scale.setScalar(shimmer);
      if (tile.material?.emissive) tile.material.emissiveIntensity = animated.hover * 0.22;
    });

    animated.records.forEach((record, index) => {
      record.rotation.z += 0.004 + index * 0.001;
    });

    if (animated.targetHover) {
      mouseLight.intensity += (2.1 - mouseLight.intensity) * 0.12;
      mouseLight.position.x += (pointer.x * 1.6 - mouseLight.position.x) * 0.14;
      mouseLight.position.y += ((1.2 + pointer.y * 0.75) - mouseLight.position.y) * 0.14;
      mouseLight.position.z += (1.6 - mouseLight.position.z) * 0.14;
    } else {
      mouseLight.intensity += (0 - mouseLight.intensity) * 0.1;
    }

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  animate();
}

function initializeOverviewMounts() {
  document.querySelectorAll(".hero-spaces").forEach((mount) => initMount(mount));
}

initializeOverviewMounts();

new MutationObserver(() => initializeOverviewMounts()).observe(document.body, {
  childList: true,
  subtree: true,
});
