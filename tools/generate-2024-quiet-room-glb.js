const fs = require("fs");
const path = require("path");

const outDir = path.join(__dirname, "..", "assets", "models", "rooms");
fs.mkdirSync(outDir, { recursive: true });

const materials = [];
const materialIndex = new Map();
const meshes = [];

function material(name, color, extras = {}) {
  if (materialIndex.has(name)) return materialIndex.get(name);
  const index = materials.length;
  materialIndex.set(name, index);
  const entry = {
    name,
    pbrMetallicRoughness: {
      baseColorFactor: color,
      roughnessFactor: extras.roughness ?? 0.72,
      metallicFactor: extras.metallic ?? 0,
    },
  };
  if (extras.emissive) entry.emissiveFactor = extras.emissive;
  if (extras.alpha !== undefined) {
    entry.alphaMode = "BLEND";
    entry.pbrMetallicRoughness.baseColorFactor[3] = extras.alpha;
  }
  materials.push(entry);
  return index;
}

const MAT = {
  cream: material("soft_cream_shell", [0.88, 0.82, 0.72, 1], { roughness: 0.58 }),
  inner: material("warm_plaster_wall", [0.78, 0.75, 0.66, 1]),
  floor: material("sage_clay_floor", [0.52, 0.62, 0.48, 1]),
  sage: material("sage_lounge_fabric", [0.55, 0.66, 0.5, 1]),
  pillow: material("cream_pillow", [0.88, 0.84, 0.76, 1]),
  blanket: material("soft_blanket", [0.7, 0.74, 0.62, 1]),
  wood: material("light_walnut", [0.54, 0.38, 0.22, 1]),
  paper: material("paper_notes", [0.86, 0.82, 0.7, 1]),
  gold: material("muted_gold_frame", [0.75, 0.55, 0.24, 1], { roughness: 0.42, metallic: 0.18 }),
  mountain: material("misty_mountain_relief", [0.48, 0.57, 0.47, 1]),
  glass: material("muted_glass_calendar", [0.62, 0.8, 0.74, 0.46], { alpha: 0.46, roughness: 0.2 }),
  record: material("record_black", [0.015, 0.014, 0.013, 1], { roughness: 0.35 }),
  label: material("record_label_warm", [0.78, 0.58, 0.26, 1]),
  lamp: material("lamp_glow_material", [1, 0.83, 0.42, 1], { emissive: [1, 0.7, 0.25] }),
  wave: material("wave_line_glow", [1, 0.88, 0.44, 1], { emissive: [1, 0.78, 0.22], roughness: 0.25 }),
};

function rotate([x, y, z], [rx = 0, ry = 0, rz = 0]) {
  let cy = Math.cos(rx), sy = Math.sin(rx);
  let y1 = y * cy - z * sy;
  let z1 = y * sy + z * cy;
  y = y1; z = z1;
  cy = Math.cos(ry); sy = Math.sin(ry);
  let x1 = x * cy + z * sy;
  z1 = -x * sy + z * cy;
  x = x1; z = z1;
  cy = Math.cos(rz); sy = Math.sin(rz);
  x1 = x * cy - y * sy;
  y1 = x * sy + y * cy;
  return [x1, y1, z];
}

function transformVertex(vertex, position, rotation = [0, 0, 0]) {
  const r = rotate(vertex, rotation);
  return [r[0] + position[0], r[1] + position[1], r[2] + position[2]];
}

function addMesh(name, positions, normals, mat) {
  meshes.push({ name, positions, normals, material: mat });
}

function box(name, position, size, mat, rotation = [0, 0, 0]) {
  const [w, h, d] = size.map((v) => v / 2);
  const faces = [
    { n: [0, 0, 1], v: [[-w, -h, d], [w, -h, d], [w, h, d], [-w, -h, d], [w, h, d], [-w, h, d]] },
    { n: [0, 0, -1], v: [[w, -h, -d], [-w, -h, -d], [-w, h, -d], [w, -h, -d], [-w, h, -d], [w, h, -d]] },
    { n: [1, 0, 0], v: [[w, -h, d], [w, -h, -d], [w, h, -d], [w, -h, d], [w, h, -d], [w, h, d]] },
    { n: [-1, 0, 0], v: [[-w, -h, -d], [-w, -h, d], [-w, h, d], [-w, -h, -d], [-w, h, d], [-w, h, -d]] },
    { n: [0, 1, 0], v: [[-w, h, d], [w, h, d], [w, h, -d], [-w, h, d], [w, h, -d], [-w, h, -d]] },
    { n: [0, -1, 0], v: [[-w, -h, -d], [w, -h, -d], [w, -h, d], [-w, -h, -d], [w, -h, d], [-w, -h, d]] },
  ];
  const positions = [];
  const normals = [];
  for (const face of faces) {
    const n = rotate(face.n, rotation);
    for (const v of face.v) {
      positions.push(...transformVertex(v, position, rotation));
      normals.push(...n);
    }
  }
  addMesh(name, positions, normals, mat);
}

function cylinder(name, position, radius, height, mat, options = {}) {
  const segments = options.segments ?? 32;
  const rotation = options.rotation ?? [0, 0, 0];
  const positions = [];
  const normals = [];
  for (let i = 0; i < segments; i += 1) {
    const a = (i / segments) * Math.PI * 2;
    const b = ((i + 1) / segments) * Math.PI * 2;
    const p1 = [Math.cos(a) * radius, -height / 2, Math.sin(a) * radius];
    const p2 = [Math.cos(b) * radius, -height / 2, Math.sin(b) * radius];
    const p3 = [Math.cos(b) * radius, height / 2, Math.sin(b) * radius];
    const p4 = [Math.cos(a) * radius, height / 2, Math.sin(a) * radius];
    const sideNormalA = rotate([Math.cos(a), 0, Math.sin(a)], rotation);
    const sideNormalB = rotate([Math.cos(b), 0, Math.sin(b)], rotation);
    for (const [p, n] of [[p1, sideNormalA], [p2, sideNormalB], [p3, sideNormalB], [p1, sideNormalA], [p3, sideNormalB], [p4, sideNormalA]]) {
      positions.push(...transformVertex(p, position, rotation));
      normals.push(...n);
    }
    for (const [tri, n] of [
      [[[0, -height / 2, 0], p2, p1], rotate([0, -1, 0], rotation)],
      [[[0, height / 2, 0], p4, p3], rotate([0, 1, 0], rotation)],
    ]) {
      for (const p of tri) {
        positions.push(...transformVertex(p, position, rotation));
        normals.push(...n);
      }
    }
  }
  addMesh(name, positions, normals, mat);
}

function floorFan() {
  const positions = [];
  const normals = [];
  const steps = 36;
  const inner = 0.52;
  const outer = 1.56;
  const start = -1.05;
  const end = 1.05;
  for (let i = 0; i < steps; i += 1) {
    const a = start + (i / steps) * (end - start);
    const b = start + ((i + 1) / steps) * (end - start);
    const verts = [
      [Math.sin(a) * inner, 0, Math.cos(a) * inner - 0.86],
      [Math.sin(b) * inner, 0, Math.cos(b) * inner - 0.86],
      [Math.sin(b) * outer, 0, Math.cos(b) * outer - 0.86],
      [Math.sin(a) * inner, 0, Math.cos(a) * inner - 0.86],
      [Math.sin(b) * outer, 0, Math.cos(b) * outer - 0.86],
      [Math.sin(a) * outer, 0, Math.cos(a) * outer - 0.86],
    ];
    for (const v of verts) {
      positions.push(...v);
      normals.push(0, 1, 0);
    }
  }
  addMesh("fan_sector_sage_floor", positions, normals, MAT.floor);
}

function tube(name, points, radius, mat) {
  const positions = [];
  const normals = [];
  const segs = 10;
  const rings = points.map((p, i) => {
    const prev = points[Math.max(0, i - 1)];
    const next = points[Math.min(points.length - 1, i + 1)];
    const tangent = normalize([next[0] - prev[0], next[1] - prev[1], next[2] - prev[2]]);
    let n = normalize(cross([0, 1, 0], tangent));
    if (length(n) < 0.001) n = [1, 0, 0];
    const b = normalize(cross(tangent, n));
    const ring = [];
    for (let j = 0; j < segs; j += 1) {
      const a = (j / segs) * Math.PI * 2;
      const normal = normalize(add(scale(n, Math.cos(a)), scale(b, Math.sin(a))));
      ring.push({ p: add(p, scale(normal, radius)), n: normal });
    }
    return ring;
  });
  for (let i = 0; i < rings.length - 1; i += 1) {
    for (let j = 0; j < segs; j += 1) {
      const a = rings[i][j];
      const b = rings[i][(j + 1) % segs];
      const c = rings[i + 1][(j + 1) % segs];
      const d = rings[i + 1][j];
      for (const v of [a, d, c, a, c, b]) {
        positions.push(...v.p);
        normals.push(...v.n);
      }
    }
  }
  addMesh(name, positions, normals, mat);
}

function add(a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; }
function scale(a, s) { return [a[0] * s, a[1] * s, a[2] * s]; }
function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
function length(a) { return Math.hypot(a[0], a[1], a[2]); }
function normalize(a) { const l = length(a) || 1; return [a[0] / l, a[1] / l, a[2] / l]; }

function buildRoom() {
  floorFan();

  for (let i = 0; i < 9; i += 1) {
    const t = -1 + (i / 8) * 2;
    const x = t * 0.9;
    const z = -0.92 - Math.abs(t) * 0.09;
    box(`curved_back_wall_panel_${i + 1}`, [x, 1.05, z], [0.24, 1.9, 0.07], MAT.inner, [0, -t * 0.22, 0]);
  }
  box("left_thick_cream_side_frame", [-1.1, 0.98, -0.45], [0.18, 2.05, 0.82], MAT.cream, [0, 0.22, 0]);
  box("right_thick_cream_side_frame", [1.1, 0.98, -0.45], [0.18, 2.05, 0.82], MAT.cream, [0, -0.22, 0]);
  box("rounded_top_cream_cap", [0, 1.98, -0.76], [1.82, 0.18, 0.18], MAT.cream);
  tube("curved_front_cream_plinth", [[-1.08, 0.07, 0.62], [-0.5, 0.08, 0.8], [0, 0.08, 0.86], [0.5, 0.08, 0.8], [1.08, 0.07, 0.62]], 0.07, MAT.cream);

  cylinder("sage_lounge_chair_seat", [-0.34, 0.2, 0.08], 0.36, 0.16, MAT.sage, { segments: 36 });
  box("sage_lounge_chair_back", [-0.34, 0.44, -0.1], [0.7, 0.36, 0.12], MAT.sage, [0.22, 0, 0]);
  box("cream_pillow_on_chair", [-0.26, 0.43, 0.04], [0.3, 0.13, 0.22], MAT.pillow, [0, 0.08, -0.08]);
  box("soft_blanket_on_chair", [-0.02, 0.28, 0.12], [0.18, 0.05, 0.44], MAT.blanket, [0.18, -0.05, 0]);

  box("small_side_table", [-0.82, 0.25, -0.12], [0.22, 0.32, 0.22], MAT.wood);
  cylinder("lamp_stem", [-0.82, 0.55, -0.12], 0.025, 0.42, MAT.gold, { segments: 18 });
  cylinder("lamp_glow", [-0.82, 0.8, -0.12], 0.13, 0.18, MAT.lamp, { segments: 32 });

  for (let row = 0; row < 3; row += 1) {
    for (let col = 0; col < 3; col += 1) {
      box(`calendar_tile_${row * 3 + col + 1}`, [0.58 + col * 0.16, 0.86 + row * 0.19, -0.79], [0.12, 0.14, 0.025], MAT.glass);
    }
  }

  box("left_wall_art_frame", [-0.42, 1.36, -0.86], [0.26, 0.38, 0.03], MAT.gold);
  box("left_wall_art_paper", [-0.42, 1.36, -0.84], [0.2, 0.31, 0.025], MAT.paper);
  box("center_wall_art_frame", [-0.05, 1.48, -0.86], [0.24, 0.34, 0.03], MAT.gold);
  box("center_wall_art_paper", [-0.05, 1.48, -0.84], [0.18, 0.27, 0.025], MAT.paper);
  cylinder("wall_record_disc_1", [-0.68, 1.05, -0.84], 0.14, 0.025, MAT.record, { rotation: [Math.PI / 2, 0, 0] });
  cylinder("wall_record_label_1", [-0.68, 1.05, -0.815], 0.05, 0.015, MAT.label, { rotation: [Math.PI / 2, 0, 0] });

  tube("mountain_relief_line_1", [[-0.82, 1.14, -0.81], [-0.52, 1.32, -0.81], [-0.22, 1.18, -0.81], [0.05, 1.38, -0.81], [0.32, 1.2, -0.81]], 0.01, MAT.mountain);
  tube("mountain_relief_line_2", [[-0.86, 0.98, -0.8], [-0.58, 1.12, -0.8], [-0.3, 1.02, -0.8], [0.0, 1.2, -0.8], [0.34, 1.05, -0.8]], 0.008, MAT.mountain);

  box("paper_note_1", [0.26, 0.04, 0.47], [0.28, 0.018, 0.18], MAT.paper, [0, 0.3, 0]);
  box("paper_note_2", [0.52, 0.045, 0.34], [0.22, 0.018, 0.15], MAT.paper, [0, -0.25, 0]);
  box("small_tea_cup", [0.55, 0.18, 0.08], [0.12, 0.12, 0.12], MAT.pillow);

  tube("wave_line", [[-0.86, 0.62, 0.18], [-0.55, 0.6, 0.08], [-0.22, 0.68, 0.16], [0.1, 0.58, 0.02], [0.44, 0.67, 0.12], [0.86, 0.6, 0.02]], 0.018, MAT.wave);
}

function makeGlb() {
  buildRoom();
  const bufferViews = [];
  const accessors = [];
  const meshDefs = [];
  const nodeDefs = [];
  const chunks = [];

  function addBuffer(floatArray) {
    const byteOffset = chunks.reduce((sum, b) => sum + b.length, 0);
    const pad = (4 - (byteOffset % 4)) % 4;
    if (pad) chunks.push(Buffer.alloc(pad));
    const offset = chunks.reduce((sum, b) => sum + b.length, 0);
    const buffer = Buffer.from(new Float32Array(floatArray).buffer);
    chunks.push(buffer);
    const view = bufferViews.length;
    bufferViews.push({ buffer: 0, byteOffset: offset, byteLength: buffer.length, target: 34962 });
    return view;
  }

  function positionBounds(values) {
    const min = [Infinity, Infinity, Infinity];
    const max = [-Infinity, -Infinity, -Infinity];
    for (let i = 0; i < values.length; i += 3) {
      for (let j = 0; j < 3; j += 1) {
        min[j] = Math.min(min[j], values[i + j]);
        max[j] = Math.max(max[j], values[i + j]);
      }
    }
    return { min, max };
  }

  meshes.forEach((mesh) => {
    const positionView = addBuffer(mesh.positions);
    const normalView = addBuffer(mesh.normals);
    const bounds = positionBounds(mesh.positions);
    const positionAccessor = accessors.length;
    accessors.push({ bufferView: positionView, componentType: 5126, count: mesh.positions.length / 3, type: "VEC3", min: bounds.min, max: bounds.max });
    const normalAccessor = accessors.length;
    accessors.push({ bufferView: normalView, componentType: 5126, count: mesh.normals.length / 3, type: "VEC3" });
    const meshIndex = meshDefs.length;
    meshDefs.push({
      name: mesh.name,
      primitives: [{ attributes: { POSITION: positionAccessor, NORMAL: normalAccessor }, material: mesh.material, mode: 4 }],
    });
    nodeDefs.push({ name: mesh.name, mesh: meshIndex });
  });

  const bin = Buffer.concat(chunks);
  const gltf = {
    asset: { version: "2.0", generator: "Linger 2024 Quiet Room generator" },
    scene: 0,
    scenes: [{ nodes: nodeDefs.map((_, i) => i) }],
    nodes: nodeDefs,
    meshes: meshDefs,
    materials,
    buffers: [{ byteLength: bin.length }],
    bufferViews,
    accessors,
  };

  const json = Buffer.from(JSON.stringify(gltf), "utf8");
  const jsonPad = Buffer.concat([json, Buffer.alloc((4 - (json.length % 4)) % 4, 0x20)]);
  const binPad = Buffer.concat([bin, Buffer.alloc((4 - (bin.length % 4)) % 4)]);
  const total = 12 + 8 + jsonPad.length + 8 + binPad.length;
  const header = Buffer.alloc(12);
  header.writeUInt32LE(0x46546c67, 0);
  header.writeUInt32LE(2, 4);
  header.writeUInt32LE(total, 8);
  const jsonHeader = Buffer.alloc(8);
  jsonHeader.writeUInt32LE(jsonPad.length, 0);
  jsonHeader.writeUInt32LE(0x4e4f534a, 4);
  const binHeader = Buffer.alloc(8);
  binHeader.writeUInt32LE(binPad.length, 0);
  binHeader.writeUInt32LE(0x004e4942, 4);
  return Buffer.concat([header, jsonHeader, jsonPad, binHeader, binPad]);
}

const outFile = path.join(outDir, "2024-quiet-room.glb");
fs.writeFileSync(outFile, makeGlb());
console.log(`Wrote ${outFile}`);
