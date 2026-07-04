const fs = require("fs");
const path = require("path");

const EXPECTED_WIDTH = 1680;
const EXPECTED_HEIGHT = 945;
const ASSETS_DIR = path.join(__dirname, "..", "assets");
const ROOM_IMAGE_PATTERN = /^music-space-zoom-\d{4}-final-space\.png$/;

function readPngSize(filePath) {
  const header = Buffer.alloc(24);
  const fd = fs.openSync(filePath, "r");
  try {
    fs.readSync(fd, header, 0, header.length, 0);
  } finally {
    fs.closeSync(fd);
  }

  const isPng = header.toString("ascii", 1, 4) === "PNG";
  if (!isPng) {
    throw new Error("Not a PNG file");
  }

  return {
    width: header.readUInt32BE(16),
    height: header.readUInt32BE(20),
  };
}

function main() {
  const roomImages = fs
    .readdirSync(ASSETS_DIR)
    .filter((name) => ROOM_IMAGE_PATTERN.test(name))
    .sort();

  if (!roomImages.length) {
    console.warn("No final room PNGs found.");
    process.exitCode = 1;
    return;
  }

  const mismatches = [];

  roomImages.forEach((name) => {
    const filePath = path.join(ASSETS_DIR, name);
    const size = readPngSize(filePath);
    if (size.width !== EXPECTED_WIDTH || size.height !== EXPECTED_HEIGHT) {
      mismatches.push(`${name}: ${size.width}x${size.height}`);
    }
  });

  if (mismatches.length) {
    console.warn(`Room asset size mismatch. Expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}.`);
    mismatches.forEach((message) => console.warn(`- ${message}`));
    process.exitCode = 1;
    return;
  }

  console.log(`All ${roomImages.length} final room PNGs are ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}.`);
}

main();
