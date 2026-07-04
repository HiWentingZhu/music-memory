const fs = require("fs");
const http = require("http");
const https = require("https");
const path = require("path");

const root = __dirname;
const port = Number(process.env.PORT || 8765);
const host = process.env.HOST || (process.env.PORT ? "0.0.0.0" : "127.0.0.1");
const audioRoot = path.join(root, "assets", "audio");
const audioMp3Root = path.join(root, "assets", "audio-mp3");
const audioLibraries = [
  { root: audioMp3Root, publicRoot: "/assets/audio-mp3", label: "assets/audio-mp3" },
  { root: audioRoot, publicRoot: "/assets/audio", label: "assets/audio" },
];
const audioExtensions = new Set([".mp3", ".m4a", ".wav", ".ogg", ".flac", ".aac", ".opus"]);
const protectedAudioExtensions = new Set([".mgg", ".mflac", ".qmc0", ".qmc2", ".qmc3", ".qmcflac", ".qmcogg"]);
const configuredQqRadioLink = "https://c6.y.qq.com/base/fcgi-bin/u?__=tKfnNW9l7BxK";

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".csv": "text/csv; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml; charset=utf-8",
  ".mp3": "audio/mpeg",
  ".m4a": "audio/mp4",
  ".wav": "audio/wav",
  ".ogg": "audio/ogg",
  ".flac": "audio/flac",
  ".aac": "audio/aac",
  ".opus": "audio/ogg",
};

const server = http.createServer((request, response) => {
  const requestUrl = new URL(request.url, `http://${request.headers.host}`);

  if (requestUrl.pathname.startsWith("/api/qq-playlist/")) {
    proxyQqPlaylist(requestUrl.pathname.split("/").pop(), response);
    return;
  }

  if (requestUrl.pathname === "/api/local-music") {
    listLocalMusic(response);
    return;
  }

  if (requestUrl.pathname === "/api/configured-qq-radio") {
    loadConfiguredQqRadio(response);
    return;
  }

  if (requestUrl.pathname.startsWith("/api/qq-song-url/")) {
    loadQqSongUrl(requestUrl.pathname.split("/").pop(), response);
    return;
  }

  if (requestUrl.pathname.startsWith("/api/qq-audio/")) {
    streamQqAudio(requestUrl.pathname.split("/").pop(), request, response);
    return;
  }

  serveStatic(requestUrl.pathname, response);
});

function errorMessage(error, fallback) {
  const message = String(error?.message || error || "").trim();
  return message || fallback;
}

function serveStatic(pathname, response) {
  const safePath = pathname === "/" ? "/index.html" : pathname;
  const filePath = path.resolve(root, `.${decodeURIComponent(safePath)}`);
  const relativePath = path.relative(root, filePath);

  if (relativePath.startsWith("..") || path.isAbsolute(relativePath)) {
    response.writeHead(403);
    response.end("Forbidden");
    return;
  }

  fs.readFile(filePath, (error, content) => {
    if (error) {
      response.writeHead(404);
      response.end("Not found");
      return;
    }

    response.writeHead(200, {
      "content-type": mimeTypes[path.extname(filePath)] || "application/octet-stream",
    });
    response.end(content);
  });
}

function proxyQqPlaylist(playlistId, response) {
  if (!/^\d{5,}$/.test(playlistId || "")) {
    response.writeHead(400, { "content-type": "application/json; charset=utf-8" });
    response.end(JSON.stringify({ error: "Invalid QQ playlist ID" }));
    return;
  }

  const endpoint = new URL("https://i.y.qq.com/qzone-music/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg");
  endpoint.search = new URLSearchParams({
    type: "1",
    json: "1",
    utf8: "1",
    onlysong: "0",
    nosign: "1",
    disstid: playlistId,
    g_tk: "5381",
    loginUin: "0",
    hostUin: "0",
    format: "json",
    inCharset: "GB2312",
    outCharset: "utf-8",
    notice: "0",
    platform: "yqq",
    needNewCode: "0",
  }).toString();

  https
    .get(endpoint, { headers: { referer: "https://y.qq.com/" } }, (qqResponse) => {
      let body = "";
      qqResponse.setEncoding("utf8");
      qqResponse.on("data", (chunk) => {
        body += chunk;
      });
      qqResponse.on("end", () => {
        response.writeHead(qqResponse.statusCode || 502, {
          "content-type": "application/json; charset=utf-8",
        });
        response.end(body);
      });
    })
    .on("error", (error) => {
      response.writeHead(502, { "content-type": "application/json; charset=utf-8" });
      response.end(JSON.stringify({ error: errorMessage(error, "QQ playlist request was blocked.") }));
    });
}

async function loadConfiguredQqRadio(response) {
  try {
    const playlistId = await resolveQqPlaylistId(configuredQqRadioLink);
    if (!playlistId) {
      response.writeHead(502, { "content-type": "application/json; charset=utf-8" });
      response.end(JSON.stringify({ error: "Could not resolve configured QQ playlist." }));
      return;
    }

    fetchQqPlaylist(playlistId, response, { configured: true });
  } catch (error) {
    response.writeHead(502, { "content-type": "application/json; charset=utf-8" });
    response.end(JSON.stringify({ error: errorMessage(error, "Configured QQ playlist could not be loaded.") }));
  }
}

function fetchQqPlaylist(playlistId, response, extra = {}) {
  if (!/^\d{5,}$/.test(playlistId || "")) {
    response.writeHead(400, { "content-type": "application/json; charset=utf-8" });
    response.end(JSON.stringify({ error: "Invalid QQ playlist ID" }));
    return;
  }

  const endpoint = qqPlaylistEndpoint(playlistId);

  https
    .get(endpoint, { headers: { referer: "https://y.qq.com/" } }, (qqResponse) => {
      let body = "";
      qqResponse.setEncoding("utf8");
      qqResponse.on("data", (chunk) => {
        body += chunk;
      });
      qqResponse.on("end", () => {
        response.writeHead(qqResponse.statusCode || 502, {
          "content-type": "application/json; charset=utf-8",
        });
        if (Object.keys(extra).length) {
          try {
            const parsed = JSON.parse(body);
            response.end(JSON.stringify({ ...parsed, ...extra, resolved_playlist_id: playlistId }));
          } catch {
            response.end(body);
          }
          return;
        }
        response.end(body);
      });
    })
    .on("error", (error) => {
      response.writeHead(502, { "content-type": "application/json; charset=utf-8" });
      response.end(JSON.stringify({ error: errorMessage(error, "QQ playlist request was blocked.") }));
    });
}

function qqPlaylistEndpoint(playlistId) {
  const endpoint = new URL("https://i.y.qq.com/qzone-music/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg");
  endpoint.search = new URLSearchParams({
    type: "1",
    json: "1",
    utf8: "1",
    onlysong: "0",
    nosign: "1",
    disstid: playlistId,
    g_tk: "5381",
    loginUin: "0",
    hostUin: "0",
    format: "json",
    inCharset: "GB2312",
    outCharset: "utf-8",
    notice: "0",
    platform: "yqq",
    needNewCode: "0",
  }).toString();
  return endpoint;
}

function loadQqSongUrl(songMid, response) {
  if (!/^[A-Za-z0-9]+$/.test(songMid || "")) {
    response.writeHead(400, { "content-type": "application/json; charset=utf-8" });
    response.end(JSON.stringify({ error: "Invalid QQ song MID" }));
    return;
  }

  resolveQqSongUrl(songMid)
    .then((result) => {
      response.writeHead(200, { "content-type": "application/json; charset=utf-8" });
      response.end(JSON.stringify({
        songMid,
        quality: result.quality,
        playable: true,
        url: `/api/qq-audio/${encodeURIComponent(songMid)}`,
        error: "",
      }));
    })
    .catch((error) => {
      response.writeHead(200, { "content-type": "application/json; charset=utf-8" });
      response.end(JSON.stringify({
        songMid,
        quality: "m4a",
        playable: false,
        url: "",
        error: errorMessage(error, "QQ Music did not return a playable audio URL."),
      }));
    });
}

function resolveQqSongUrl(songMid) {
  const quality = "m4a";
  const filename = `C400${songMid}.m4a`;
  const requestBody = JSON.stringify({
    req_1: {
      module: "vkey.GetVkeyServer",
      method: "CgiGetVkey",
      param: {
        filename: [filename],
        guid: "10000",
        songmid: [songMid],
        songtype: [0],
        uin: "0",
        loginflag: 1,
        platform: "20",
      },
    },
    loginUin: "0",
    comm: {
      uin: "0",
      format: "json",
      ct: 24,
      cv: 0,
    },
  });

  return new Promise((resolve, reject) => {
    const qqRequest = https.request("https://u.y.qq.com/cgi-bin/musicu.fcg", {
      method: "POST",
      headers: {
        accept: "application/json, text/plain, */*",
        "content-type": "application/json;charset=UTF-8",
        "content-length": Buffer.byteLength(requestBody),
        referer: "https://y.qq.com/",
        "user-agent": "Mozilla/5.0",
      },
    }, (qqResponse) => {
      let body = "";
      qqResponse.setEncoding("utf8");
      qqResponse.on("data", (chunk) => {
        body += chunk;
      });
      qqResponse.on("end", () => {
        try {
          const data = JSON.parse(body);
          const urlInfo = data?.req_1?.data?.midurlinfo?.[0];
          const sip = data?.req_1?.data?.sip?.[0] || "";
          const purl = urlInfo?.purl || "";
          const playUrl = purl && /^https?:\/\//i.test(purl) ? purl : (purl ? `${sip}${purl}` : "");
          if (!playUrl) {
            reject(new Error(urlInfo?.result === 0 ? "No playable URL returned" : urlInfo?.msg || "No playable URL returned"));
            return;
          }
          resolve({ quality, url: playUrl });
        } catch (error) {
          reject(error);
        }
      });
    });

    qqRequest.on("error", reject);
    qqRequest.write(requestBody);
    qqRequest.end();
  });
}

function streamQqAudio(songMid, request, response) {
  if (!/^[A-Za-z0-9]+$/.test(songMid || "")) {
    response.writeHead(400, { "content-type": "application/json; charset=utf-8" });
    response.end(JSON.stringify({ error: "Invalid QQ song MID" }));
    return;
  }

  resolveQqSongUrl(songMid)
    .then((result) => {
      const headers = {
        referer: "https://y.qq.com/",
        "user-agent": "Mozilla/5.0",
      };
      if (request.headers.range) headers.range = request.headers.range;

      https.get(result.url, { headers }, (qqResponse) => {
        const responseHeaders = {
          "content-type": qqResponse.headers["content-type"] || "audio/mp4",
          "accept-ranges": qqResponse.headers["accept-ranges"] || "bytes",
        };
        ["content-length", "content-range"].forEach((name) => {
          if (qqResponse.headers[name]) responseHeaders[name] = qqResponse.headers[name];
        });
        response.writeHead(qqResponse.statusCode || 200, responseHeaders);
        qqResponse.pipe(response);
      }).on("error", (error) => {
        response.writeHead(502, { "content-type": "application/json; charset=utf-8" });
        response.end(JSON.stringify({ error: errorMessage(error, "QQ audio stream unavailable") }));
      });
    })
    .catch((error) => {
      response.writeHead(502, { "content-type": "application/json; charset=utf-8" });
      response.end(JSON.stringify({ error: errorMessage(error, "QQ audio unavailable") }));
    });
}

function resolveQqPlaylistId(sourceUrl) {
  return new Promise((resolve, reject) => {
    const directId = extractPlaylistId(sourceUrl);
    if (directId) {
      resolve(directId);
      return;
    }

    https
      .get(sourceUrl, {
        headers: {
          "user-agent": "Mozilla/5.0",
          referer: "https://y.qq.com/",
        },
      }, (qqResponse) => {
        const location = qqResponse.headers.location;
        if (location) {
          resolve(extractPlaylistId(location));
          qqResponse.resume();
          return;
        }

        let body = "";
        qqResponse.setEncoding("utf8");
        qqResponse.on("data", (chunk) => {
          body += chunk;
        });
        qqResponse.on("end", () => {
          resolve(extractPlaylistId(body));
        });
      })
      .on("error", reject);
  });
}

function extractPlaylistId(value) {
  const text = String(value || "");
  const match = text.match(/(?:playlist\/|[?&](?:id|disstid)=)(\d{5,})/) || text.match(/(\d{8,})/);
  return match?.[1] || "";
}

function listLocalMusic(response) {
  const files = [];
  const unsupportedFiles = [];

  audioLibraries.forEach((library) => {
    if (fs.existsSync(library.root)) {
      collectAudioFiles(library, files, unsupportedFiles);
    }
  });

  response.writeHead(200, { "content-type": "application/json; charset=utf-8" });
  response.end(JSON.stringify({ root: audioLibraries.map((library) => library.label), files, unsupportedFiles }));
}

function collectAudioFiles(library, output, unsupportedOutput, directory = library.root) {
  const entries = fs.readdirSync(directory, { withFileTypes: true });

  entries.forEach((entry) => {
    if (entry.name.startsWith(".")) return;
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      collectAudioFiles(library, output, unsupportedOutput, fullPath);
      return;
    }
    if (!entry.isFile()) return;

    const relativePath = path.relative(library.root, fullPath);
    const extension = path.extname(entry.name).toLowerCase();
    if (!audioExtensions.has(extension)) {
      if (protectedAudioExtensions.has(extension)) {
        unsupportedOutput.push({
          name: entry.name,
          path: relativePath,
          reason: "Protected QQ Music format",
        });
      }
      return;
    }

    const urlPath = relativePath.split(path.sep).map(encodeURIComponent).join("/");
    const stats = fs.statSync(fullPath);
    output.push({
      name: entry.name,
      path: relativePath,
      url: `${library.publicRoot}/${urlPath}`,
      size: stats.size,
    });
  });
}

server.listen(port, host, () => {
  const displayHost = host === "0.0.0.0" ? "127.0.0.1" : host;
  console.log(`Music Personality World running at http://${displayHost}:${port}/`);
});
