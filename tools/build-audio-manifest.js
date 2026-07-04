const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const audioRoot = path.join(root, "assets", "audio");
const audioMp3Root = path.join(root, "assets", "audio-mp3");
const outputPath = path.join(audioRoot, "manifest.js");
const audioLibraries = [
  { root: audioMp3Root, publicRoot: "assets/audio-mp3" },
  { root: audioRoot, publicRoot: "assets/audio" },
];
const audioExtensions = new Set([".mp3", ".m4a", ".wav", ".ogg", ".flac", ".aac", ".opus"]);

const files = [];

function collectAudioFiles(library, directory = library.root) {
  if (!fs.existsSync(directory)) return;
  const entries = fs.readdirSync(directory, { withFileTypes: true });

  entries.forEach((entry) => {
    if (entry.name.startsWith(".")) return;
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      collectAudioFiles(library, fullPath);
      return;
    }
    if (!entry.isFile()) return;
    if (!audioExtensions.has(path.extname(entry.name).toLowerCase())) return;

    const relativePath = path.relative(library.root, fullPath).split(path.sep).join("/");
    const urlPath = relativePath.split("/").map(encodeURIComponent).join("/");
    const stats = fs.statSync(fullPath);
    files.push({
      name: entry.name,
      path: relativePath,
      url: `${library.publicRoot}/${urlPath}`,
      size: stats.size,
    });
  });
}

audioLibraries.forEach((library) => collectAudioFiles(library));

const manifest = {
  root: audioLibraries.map((library) => library.publicRoot),
  files,
};

fs.writeFileSync(
  outputPath,
  `globalThis.LINGER_AUDIO_MANIFEST = ${JSON.stringify(manifest, null, 2)};\n`,
  "utf8",
);

console.log(`Wrote ${path.relative(root, outputPath)} with ${files.length} audio file${files.length === 1 ? "" : "s"}.`);
