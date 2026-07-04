const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const root = path.join(__dirname, "..");
const audioRoot = path.join(root, "assets", "audio");
const outputRoot = path.resolve(root, getArgValue("--output-root") || path.join("assets", "audio-mp3"));
const sourceExtensions = new Set([".flac", ".m4a", ".wav", ".ogg", ".aac", ".opus"]);
const bitrate = getArgValue("--bitrate") || "192k";
const folderFilter = normalizePath(getArgValue("--folder") || "");
const limit = Number(getArgValue("--limit") || 0);
const dryRun = process.argv.includes("--dry-run");
const force = process.argv.includes("--force");
const ffmpeg = process.env.FFMPEG_PATH || "ffmpeg";

const inputs = collectAudioInputs(audioRoot)
  .filter((filePath) => !folderFilter || normalizePath(path.relative(audioRoot, filePath)).startsWith(folderFilter))
  .filter((filePath) => force || !fs.existsSync(getOutputPath(filePath)));

const selected = limit > 0 ? inputs.slice(0, limit) : inputs;

if (!selected.length) {
  console.log("No audio files need MP3 conversion.");
  process.exit(0);
}

if (!dryRun) {
  const check = spawnSync(ffmpeg, ["-version"], { encoding: "utf8" });
  if (check.error || check.status !== 0) {
    console.error("ffmpeg was not found. Install ffmpeg or set FFMPEG_PATH to ffmpeg.exe.");
    process.exit(1);
  }
}

let converted = 0;
const failed = [];
selected.forEach((inputPath, index) => {
  const outputPath = getOutputPath(inputPath);
  const relativeInput = normalizePath(path.relative(root, inputPath));
  const relativeOutput = normalizePath(path.relative(root, outputPath));
  console.log(`[${index + 1}/${selected.length}] ${relativeInput} -> ${relativeOutput}`);

  if (dryRun) return;

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  const result = spawnSync(
    ffmpeg,
    [
      force ? "-y" : "-n",
      "-hide_banner",
      "-loglevel",
      "quiet",
      "-i",
      inputPath,
      "-vn",
      "-codec:a",
      "libmp3lame",
      "-b:a",
      bitrate,
      outputPath,
    ],
    { stdio: "inherit" },
  );

  if (result.status !== 0) {
    console.error(`Failed to convert ${relativeInput}`);
    failed.push(relativeInput);
    return;
  }
  converted += 1;
});

console.log(dryRun
  ? `Dry run listed ${selected.length} file${selected.length === 1 ? "" : "s"}.`
  : `Converted ${converted} file${converted === 1 ? "" : "s"} to MP3 at ${bitrate}.`);
if (failed.length) {
  console.error(`Skipped ${failed.length} failed file${failed.length === 1 ? "" : "s"}:`);
  failed.forEach((filePath) => console.error(`- ${filePath}`));
  process.exit(1);
}

function collectAudioInputs(directory) {
  if (!fs.existsSync(directory)) return [];
  const entries = fs.readdirSync(directory, { withFileTypes: true });
  return entries.flatMap((entry) => {
    if (entry.name.startsWith(".")) return [];
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) return collectAudioInputs(fullPath);
    if (!entry.isFile()) return [];
    return sourceExtensions.has(path.extname(entry.name).toLowerCase()) ? [fullPath] : [];
  });
}

function getOutputPath(inputPath) {
  const relativePath = path.relative(audioRoot, inputPath);
  return path.join(outputRoot, relativePath).replace(/\.[^.]+$/, ".mp3");
}

function getArgValue(name) {
  const index = process.argv.indexOf(name);
  if (index === -1) return "";
  return process.argv[index + 1] || "";
}

function normalizePath(value) {
  return String(value || "").replace(/\\/g, "/").toLowerCase();
}
