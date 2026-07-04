const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const sourcePath = path.join(root, "output", "artist-info-source-of-truth-v1.csv");
const outputPath = path.join(root, "output", "artist-info-manifest.js");

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

const rows = fs.existsSync(sourcePath) ? parseCsv(fs.readFileSync(sourcePath, "utf8")) : [];

fs.writeFileSync(
  outputPath,
  `globalThis.LINGER_ARTIST_INFO_ROWS = ${JSON.stringify(rows, null, 2)};\n`,
  "utf8",
);

console.log(`Wrote ${path.relative(root, outputPath)} with ${rows.length} artist info row${rows.length === 1 ? "" : "s"}.`);
