const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const imageRoot = path.join(root, "output", "artist-image-downloads-v1");
const outputPath = path.join(root, "output", "artist-image-manifest.js");
const curationPath = path.join(root, "output", "artist-image-curation.json");
const imageExtensions = new Set([".jpg", ".jpeg", ".png", ".webp"]);

function stripIndexPrefix(name) {
  return String(name || "").replace(/^\d+\s*-\s*/, "").trim();
}

function encodeUrlPath(relativePath) {
  return relativePath.split(path.sep).map(encodeURIComponent).join("/");
}

const artists = [];
const curation = fs.existsSync(curationPath)
  ? JSON.parse(fs.readFileSync(curationPath, "utf8"))
  : {};

function getCurationRule(name) {
  const keys = new Set([name]);
  const withoutIndex = stripIndexPrefix(name);
  keys.add(withoutIndex);
  const withoutParenthetical = withoutIndex.replace(/\s*\([^()]+\)\s*$/g, "").trim();
  keys.add(withoutParenthetical);
  const parenthetical = withoutIndex.match(/\(([^()]+)\)/)?.[1]?.trim();
  if (parenthetical) keys.add(parenthetical);
  return [...keys].map((key) => curation[key]).find(Boolean) || {};
}

function curatedFiles(files, rule) {
  if (Array.isArray(rule.include) && rule.include.length) {
    const include = new Set(rule.include);
    return files.filter((file) => include.has(file.name));
  }
  if (Array.isArray(rule.exclude) && rule.exclude.length) {
    const exclude = new Set(rule.exclude);
    return files.filter((file) => !exclude.has(file.name));
  }
  return files;
}

if (fs.existsSync(imageRoot)) {
  fs.readdirSync(imageRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && !entry.name.startsWith("."))
    .forEach((entry) => {
      const directory = path.join(imageRoot, entry.name);
      const rule = getCurationRule(entry.name);
      const files = fs.readdirSync(directory, { withFileTypes: true })
        .filter((file) => file.isFile() && imageExtensions.has(path.extname(file.name).toLowerCase()))
        .sort((a, b) => a.name.localeCompare(b.name, "en", { numeric: true }));
      const images = curatedFiles(files, rule)
        .map((file) => {
          const relativePath = path.join("output", "artist-image-downloads-v1", entry.name, file.name);
          return {
            src: encodeUrlPath(relativePath),
            position: rule.position || "50% 18%",
            scale: rule.scale || 1.28,
          };
        });

      if (images.length) {
        artists.push({
          name: stripIndexPrefix(entry.name),
          images,
        });
      }
    });
}

const manifest = { artists };

fs.writeFileSync(
  outputPath,
  `globalThis.LINGER_ARTIST_IMAGE_MANIFEST = ${JSON.stringify(manifest, null, 2)};\n`,
  "utf8",
);

console.log(`Wrote ${path.relative(root, outputPath)} with ${artists.length} artist image folder${artists.length === 1 ? "" : "s"}.`);
