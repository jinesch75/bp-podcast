// Biergerpakt Podcast — web server (Railway).
//
// 1. Serves the static site exactly as before (index.html, app.js, mp3 with seeking, review pages…).
// 2. /api/hit — anonymous counters. The browser sends only: what happened (site visit, episode
//    opened, listen started, listened to the end), which episode, which language. Nothing about the
//    person is received or stored: no IP address, no cookie, no device, no browser, no time of day.
//    Each request only adds 1 to a counter for that day.
// 3. /admin/ — the admin space (audience figures + episode status), protected by a password that
//    lives only in the Railway variable ADMIN_PASSWORD (never in the repository, which is public).
// 4. Validation: an episode marked "pending": true in episodes_data.js (every new episode, see
//    build/mark_pending.js) is left out of the public /episodes_data.js until it is validated in the
//    admin space. Validations are kept in the volume (admin.json), so they take effect at once,
//    without a deploy. Review pages have their own copy of the episode and are not affected.
//
// Data is kept in a Railway volume (variable RAILWAY_VOLUME_MOUNT_PATH, set by Railway when a
// volume is attached; DATA_DIR overrides it). Without a volume the data would be lost at every deploy.
// No dependencies: plain Node.js (>= 18).

'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');
const vm = require('vm');

const ROOT = __dirname;
const PORT = Number(process.env.PORT) || 8080;
const DATA_DIR = process.env.DATA_DIR || process.env.RAILWAY_VOLUME_MOUNT_PATH ||
  (fs.existsSync('/data') ? '/data' : path.join(ROOT, '.data'));
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || '';
const TZ = 'Europe/Luxembourg';
const LANGS = ['en', 'fr', 'de'];
const EVENTS = ['open', 'play', 'done'];   // episode opened, listen started, listened to the end

fs.mkdirSync(DATA_DIR, { recursive: true });
const STATS_FILE = path.join(DATA_DIR, 'stats.json');
const ADMIN_FILE = path.join(DATA_DIR, 'admin.json');

// ── Small helpers ────────────────────────────────────────
function readJson(file, fallback) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) { return fallback; }
}
function writeJsonAtomic(file, obj) {
  const tmp = file + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(obj));
  fs.renameSync(tmp, file);
}
const dayFmt = (() => {
  try { return new Intl.DateTimeFormat('en-CA', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit' }); }
  catch (e) { return null; }
})();
function today() {
  return dayFmt ? dayFmt.format(new Date()) : new Date().toISOString().slice(0, 10);
}
function send(res, status, body, headers) {
  res.writeHead(status, Object.assign({ 'Content-Type': 'text/plain; charset=utf-8', 'X-Content-Type-Options': 'nosniff' }, headers || {}));
  res.end(body);
}
function sendJson(res, status, obj) {
  send(res, status, JSON.stringify(obj), { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
}
function readBody(req, limit) {
  return new Promise((resolve, reject) => {
    let size = 0; const chunks = [];
    req.on('data', (c) => {
      size += c.length;
      if (size > limit) { reject(new Error('too large')); req.destroy(); return; }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

// ── Episodes (read from episodes_data.js) ────────────────
const DATA_FILE = path.join(ROOT, 'episodes_data.js');
let EPISODES = [], EP_KEYS = new Set(), REVIEW = {}, RAW = null, DATA_MTIME = 0;
function loadEpisodes() {
  try {
    DATA_MTIME = fs.statSync(DATA_FILE).mtimeMs;
    const code = fs.readFileSync(DATA_FILE, 'utf8');
    const list = vm.runInNewContext(code + '\n;EPISODES', {}, { timeout: 5000 });
    RAW = list;
    EPISODES = list.map((e) => ({
      id: e.id, key: e.key, number: Number(String(e.number).replace(/\D/g, '')) || e.id,
      title: e.title, title_fr: e.title_fr || '', pending: !!e.pending,
      duration: Math.round(e.duration || 0), duration_fr: Math.round(e.duration_fr || 0), duration_de: Math.round(e.duration_de || 0)
    }));
    EP_KEYS = new Set(EPISODES.map((e) => e.key));
  } catch (e) { RAW = null; console.error('Could not read episodes_data.js:', e.message); }
  // Review pages: folders review/<key>-<token>/
  REVIEW = {};
  try {
    fs.readdirSync(path.join(ROOT, 'review')).forEach((d) => {
      const i = d.lastIndexOf('-');
      if (i > 0) REVIEW[d.slice(0, i)] = '/review/' + d + '/';
    });
  } catch (e) { /* no review folder */ }
}
loadEpisodes();

// ── Anonymous counters ───────────────────────────────────
// stats.days["YYYY-MM-DD"] = { _v: site visits, <key>: [open en,fr,de, play en,fr,de, done en,fr,de] }
const stats = readJson(STATS_FILE, null) || { v: 1, since: today(), days: {} };
let statsDirty = false;
function saveStats() {
  if (!statsDirty) return;
  try { writeJsonAtomic(STATS_FILE, stats); statsDirty = false; }
  catch (e) { console.error('Could not save the counters:', e.message); }
}
setInterval(saveStats, 15000).unref();

// Overall safety cap (there is deliberately no per-visitor limit, as nothing identifies a visitor).
let hitWindow = 0, hitCount = 0;
const HIT_CAP_PER_MIN = 1200;

function countHit(ev, key, lang) {
  const now = Date.now();
  if (now - hitWindow > 60000) { hitWindow = now; hitCount = 0; }
  if (++hitCount > HIT_CAP_PER_MIN) return;
  const d = today();
  const day = stats.days[d] || (stats.days[d] = {});
  if (ev === 'visit') { day._v = (day._v || 0) + 1; statsDirty = true; return; }
  if (!EP_KEYS.has(key)) return;
  const li = Math.max(0, LANGS.indexOf(lang));
  const arr = day[key] || (day[key] = [0, 0, 0, 0, 0, 0, 0, 0, 0]);
  arr[EVENTS.indexOf(ev) * 3 + li]++;
  statsDirty = true;
}

async function handleHit(req, res) {
  // Answer at once; the browser does not wait for anything.
  let body = '';
  try { body = await readBody(req, 512); } catch (e) { return send(res, 413, ''); }
  let m = null;
  try { m = JSON.parse(body); } catch (e) { /* ignore */ }
  if (m && typeof m === 'object') {
    const ev = String(m.e || '');
    if (ev === 'visit' || EVENTS.includes(ev)) countHit(ev, String(m.k || ''), String(m.l || 'en'));
  }
  res.writeHead(204, { 'Cache-Control': 'no-store' });
  res.end();
}

// ── Episode status (admin) ───────────────────────────────
// admin.episodes[key] = { note: "", en: { script: { finished, finishedOn }, audio: { finished, finishedOn } }, fr: {…}, de: {…} }
// finishedOn = "YYYY-MM-DD". Older formats are read as: one status for the episode / per language → applies to script and audio.
const PARTS = ['script', 'audio'];
const adminData = readJson(ADMIN_FILE, null) || { episodes: {} };
function epStatus(key) {
  const cur = adminData.episodes[key] || {};
  const out = { note: typeof cur.note === 'string' ? cur.note : '' };
  const legacyEp = typeof cur.finished === 'boolean' ? { finished: cur.finished, finishedOn: cur.finishedOn || '' } : null;
  LANGS.forEach((l) => {
    const cl = cur[l] || null;
    const legacyLang = cl && typeof cl.finished === 'boolean' ? { finished: cl.finished, finishedOn: cl.finishedOn || '' } : null;
    out[l] = {};
    PARTS.forEach((part) => {
      const v = (cl && cl[part]) || legacyLang || legacyEp;
      out[l][part] = { finished: !!(v && v.finished), finishedOn: (v && v.finished && v.finishedOn) || '' };
    });
  });
  return out;
}
function allStatus() {
  const o = {};
  EPISODES.forEach((e) => { o[e.key] = epStatus(e.key); });
  return o;
}
function saveAdmin() { writeJsonAtomic(ADMIN_FILE, adminData); }

// ── Validation (pending episodes) ────────────────────────
// adminData.validated[key] = "YYYY-MM-DD" (day it was validated and put online).
if (!adminData.validated || typeof adminData.validated !== 'object') adminData.validated = {};
function isOnline(e) { return !e.pending || !!adminData.validated[e.key]; }
function reloadIfChanged() {
  try { if (fs.statSync(DATA_FILE).mtimeMs !== DATA_MTIME) loadEpisodes(); } catch (e) { /* keep what we have */ }
}
let pubCache = null;                 // { sig, body, gz, etag }
function publicData() {
  reloadIfChanged();
  if (!RAW) return null;
  const sig = DATA_MTIME + '|' + RAW.filter((e) => e.pending && adminData.validated[e.key]).map((e) => e.key).join(',');
  if (pubCache && pubCache.sig === sig) return pubCache;
  const list = RAW.filter(isOnline);
  const body = Buffer.from('// Biergerpakt Podcast — published episodes (episodes waiting for validation are left out)\n' +
    'const EPISODES = ' + JSON.stringify(list) + ';\n', 'utf8');
  pubCache = {
    sig, body, gz: zlib.gzipSync(body, { level: 6 }),
    etag: 'W/"p-' + crypto.createHash('sha1').update(body).digest('hex').slice(0, 16) + '"'
  };
  return pubCache;
}
function servePublicData(req, res) {
  const d = publicData();
  if (!d) return send(res, 503, 'Episodes unavailable');
  const headers = { 'Content-Type': MIME['.js'], 'ETag': d.etag, 'Cache-Control': 'no-cache', 'Vary': 'Accept-Encoding',
    'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'same-origin' };
  if (req.headers['if-none-match'] === d.etag) { res.writeHead(304, headers); return res.end(); }
  const gz = /\bgzip\b/.test(req.headers['accept-encoding'] || '');
  const buf = gz ? d.gz : d.body;
  if (gz) headers['Content-Encoding'] = 'gzip';
  headers['Content-Length'] = buf.length;
  res.writeHead(200, headers);
  res.end(req.method === 'HEAD' ? undefined : buf);
}

// ── Admin login ──────────────────────────────────────────
const sessions = new Map();          // token -> expiry (ms). In memory only: a redeploy logs out.
const SESSION_MS = 12 * 3600 * 1000;
const COOKIE = 'bp_admin';
let failTimes = [];                  // times of recent wrong passwords (no IP is kept)
let lockedUntil = 0;

function sha(s) { return crypto.createHash('sha256').update(String(s)).digest(); }
function passwordOk(p) {
  return ADMIN_PASSWORD.length > 0 && crypto.timingSafeEqual(sha(p), sha(ADMIN_PASSWORD));
}
function parseCookies(req) {
  const out = {};
  (req.headers.cookie || '').split(';').forEach((p) => {
    const i = p.indexOf('=');
    if (i > 0) out[p.slice(0, i).trim()] = decodeURIComponent(p.slice(i + 1).trim());
  });
  return out;
}
function isAdmin(req) {
  const tok = parseCookies(req)[COOKIE];
  if (!tok || !sessions.has(tok)) return false;
  if (sessions.get(tok) < Date.now()) { sessions.delete(tok); return false; }
  return true;
}
function cookieAttrs(req) {
  const https = (req.headers['x-forwarded-proto'] || '').split(',')[0].trim() === 'https';
  return '; Path=/; HttpOnly; SameSite=Strict' + (https ? '; Secure' : '');
}
const ADMIN_HEADERS = {
  'Cache-Control': 'no-store', 'X-Frame-Options': 'DENY', 'Referrer-Policy': 'no-referrer',
  'X-Robots-Tag': 'noindex, nofollow',
  'Content-Security-Policy': "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'; form-action 'self'"
};

function serveAdminPage(req, res) {
  const file = isAdmin(req) ? 'admin.html' : 'login.html';
  let html = fs.readFileSync(path.join(ROOT, 'server', file), 'utf8');
  if (!ADMIN_PASSWORD) html = html.replace('<!--NOPASS-->', '<p class="err" style="display:block">The admin space is switched off: set the variable ADMIN_PASSWORD in Railway first.</p>');
  send(res, 200, html, Object.assign({ 'Content-Type': 'text/html; charset=utf-8' }, ADMIN_HEADERS));
}

async function handleLogin(req, res) {
  const now = Date.now();
  failTimes = failTimes.filter((t) => now - t < 15 * 60000);
  if (now < lockedUntil) return sendJson(res, 429, { error: 'locked', minutes: Math.ceil((lockedUntil - now) / 60000) });
  let pass = '';
  try { pass = String((JSON.parse(await readBody(req, 2048)) || {}).password || ''); } catch (e) { /* empty */ }
  if (passwordOk(pass)) {
    failTimes = [];
    const tok = crypto.randomBytes(32).toString('hex');
    sessions.set(tok, now + SESSION_MS);
    res.setHeader('Set-Cookie', COOKIE + '=' + tok + cookieAttrs(req) + '; Max-Age=' + SESSION_MS / 1000);
    return sendJson(res, 200, { ok: true });
  }
  failTimes.push(now);
  if (failTimes.length >= 10) { lockedUntil = now + 15 * 60000; failTimes = []; }
  await new Promise((r) => setTimeout(r, 1500));   // slows down password guessing
  return sendJson(res, 401, { error: 'wrong' });
}

function handleLogout(req, res) {
  const tok = parseCookies(req)[COOKIE];
  if (tok) sessions.delete(tok);
  res.setHeader('Set-Cookie', COOKIE + '=' + cookieAttrs(req) + '; Max-Age=0');
  sendJson(res, 200, { ok: true });
}

async function handleAdminApi(req, res, p) {
  if (!isAdmin(req)) return sendJson(res, 401, { error: 'login' });
  if (req.method === 'GET' && p === '/api/admin/data') {
    reloadIfChanged();
    return sendJson(res, 200, {
      today: today(), since: stats.since, days: stats.days,
      episodes: EPISODES.map((e) => Object.assign({}, e, {
        review: REVIEW[e.key] || null, online: isOnline(e), validatedOn: (e.pending && adminData.validated[e.key]) || ''
      })),
      status: allStatus()
    });
  }
  if (req.method === 'POST' && p === '/api/admin/status') {
    if (req.headers['x-bp-admin'] !== '1') return sendJson(res, 403, { error: 'header' });
    let m = null;
    try { m = JSON.parse(await readBody(req, 8192)); } catch (e) { return sendJson(res, 400, { error: 'json' }); }
    if (!m || !EP_KEYS.has(m.key)) return sendJson(res, 400, { error: 'key' });
    const cur = epStatus(m.key);
    if (typeof m.finished === 'boolean') {
      if (!LANGS.includes(m.lang) || !PARTS.includes(m.part)) return sendJson(res, 400, { error: 'lang/part' });
      const st = cur[m.lang][m.part];
      if (m.finished && !st.finished) st.finishedOn = today();
      if (!m.finished) st.finishedOn = '';
      st.finished = m.finished;
    }
    if (typeof m.note === 'string') cur.note = m.note.slice(0, 1000);
    adminData.episodes[m.key] = cur;
    try { saveAdmin(); } catch (e) { return sendJson(res, 500, { error: 'save' }); }
    return sendJson(res, 200, { ok: true, status: cur });
  }
  if (req.method === 'POST' && p === '/api/admin/validate') {
    if (req.headers['x-bp-admin'] !== '1') return sendJson(res, 403, { error: 'header' });
    let m = null;
    try { m = JSON.parse(await readBody(req, 2048)); } catch (e) { return sendJson(res, 400, { error: 'json' }); }
    const ep = m && EPISODES.find((e) => e.key === m.key);
    if (!ep || typeof m.online !== 'boolean') return sendJson(res, 400, { error: 'key' });
    if (!ep.pending) return sendJson(res, 400, { error: 'not pending' });
    if (m.online) adminData.validated[ep.key] = adminData.validated[ep.key] || today();
    else delete adminData.validated[ep.key];
    try { saveAdmin(); } catch (e) { return sendJson(res, 500, { error: 'save' }); }
    return sendJson(res, 200, { ok: true, online: isOnline(ep), validatedOn: adminData.validated[ep.key] || '' });
  }
  return sendJson(res, 404, { error: 'not found' });
}

// ── Static files ─────────────────────────────────────────
const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.ico': 'image/x-icon', '.webp': 'image/webp', '.mp3': 'audio/mpeg', '.mp4': 'video/mp4',
  '.md': 'text/markdown; charset=utf-8', '.txt': 'text/plain; charset=utf-8', '.pdf': 'application/pdf',
  '.woff2': 'font/woff2', '.webmanifest': 'application/manifest+json'
};
const COMPRESSIBLE = new Set(['.html', '.js', '.css', '.json', '.svg', '.md', '.txt', '.webmanifest']);
// Never served: server code and data, hidden files, internal office documents (contact lists, Word files).
const BLOCKED_EXT = new Set(['.xlsx', '.xls', '.docx', '.doc', '.env', '.py', '.pyc']);
const BLOCKED_TOP = new Set(['server', 'node_modules', 'Relecture partenaires', 'archive']);
const gzCache = new Map();           // path -> { mtime, size, buf }

function serveStatic(req, res, urlPath, query) {
  let rel;
  try { rel = decodeURIComponent(urlPath); } catch (e) { return send(res, 400, 'Bad request'); }
  if (rel.includes('\0')) return send(res, 400, 'Bad request');
  const parts = rel.split('/').filter(Boolean);
  if (parts.some((s) => s.startsWith('.') || s === '..')) return send(res, 404, 'Not found');
  if (parts.length && BLOCKED_TOP.has(parts[0])) return send(res, 404, 'Not found');
  let file = path.join(ROOT, ...parts);
  if (file !== ROOT && !file.startsWith(ROOT + path.sep)) return send(res, 404, 'Not found');
  if (parts.length === 1 && /^(server\.js|package(-lock)?\.json)$/.test(parts[0])) return send(res, 404, 'Not found');
  // Old copies of the episode data (backups) would show episodes still waiting for validation.
  if (parts.length === 1 && /^episodes_data\..+\.js$/.test(parts[0])) return send(res, 404, 'Not found');

  let st;
  try { st = fs.statSync(file); } catch (e) { return send(res, 404, 'Not found'); }
  if (st.isDirectory()) {
    if (!urlPath.endsWith('/')) return send(res, 301, '', { Location: urlPath + '/' + (query ? '?' + query : '') });
    file = path.join(file, 'index.html');
    try { st = fs.statSync(file); } catch (e) { return send(res, 404, 'Not found'); }
  }
  if (!st.isFile()) return send(res, 404, 'Not found');
  const ext = path.extname(file).toLowerCase();
  if (BLOCKED_EXT.has(ext)) return send(res, 404, 'Not found');

  const type = MIME[ext] || 'application/octet-stream';
  const etag = 'W/"' + st.size.toString(16) + '-' + Math.floor(st.mtimeMs).toString(16) + '"';
  const headers = {
    'Content-Type': type, 'ETag': etag, 'Last-Modified': st.mtime.toUTCString(),
    'Accept-Ranges': 'bytes', 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'same-origin',
    // HTML/JS/data are revalidated every time (cheap 304s); audio, video and images may be kept an hour.
    'Cache-Control': COMPRESSIBLE.has(ext) ? 'no-cache' : 'public, max-age=3600'
  };
  if (req.headers['if-none-match'] === etag) { res.writeHead(304, headers); return res.end(); }

  // Range requests (needed to seek in audio/video, and by Safari to play at all).
  const range = req.headers.range;
  if (range && /^bytes=/.test(range)) {
    const m = /^bytes=(\d*)-(\d*)$/.exec(range.trim());
    let start, end;
    if (m && (m[1] !== '' || m[2] !== '')) {
      if (m[1] === '') { start = Math.max(0, st.size - Number(m[2])); end = st.size - 1; }
      else { start = Number(m[1]); end = m[2] === '' ? st.size - 1 : Math.min(Number(m[2]), st.size - 1); }
    }
    if (start === undefined || start > end || start >= st.size) {
      res.writeHead(416, { 'Content-Range': 'bytes */' + st.size }); return res.end();
    }
    headers['Content-Range'] = 'bytes ' + start + '-' + end + '/' + st.size;
    headers['Content-Length'] = end - start + 1;
    res.writeHead(206, headers);
    if (req.method === 'HEAD') return res.end();
    return fs.createReadStream(file, { start, end }).on('error', () => res.destroy()).pipe(res);
  }

  const gz = COMPRESSIBLE.has(ext) && /\bgzip\b/.test(req.headers['accept-encoding'] || '');
  if (COMPRESSIBLE.has(ext)) headers['Vary'] = 'Accept-Encoding';
  if (gz) {
    let c = gzCache.get(file);
    if (!c || c.mtime !== st.mtimeMs || c.size !== st.size) {
      c = { mtime: st.mtimeMs, size: st.size, buf: zlib.gzipSync(fs.readFileSync(file), { level: 6 }) };
      gzCache.set(file, c);
    }
    headers['Content-Encoding'] = 'gzip';
    headers['Content-Length'] = c.buf.length;
    res.writeHead(200, headers);
    return res.end(req.method === 'HEAD' ? undefined : c.buf);
  }
  headers['Content-Length'] = st.size;
  res.writeHead(200, headers);
  if (req.method === 'HEAD') return res.end();
  fs.createReadStream(file).on('error', () => res.destroy()).pipe(res);
}

// ── Router ───────────────────────────────────────────────
const server = http.createServer((req, res) => {
  const u = req.url || '/';
  const qi = u.indexOf('?');
  const p = qi >= 0 ? u.slice(0, qi) : u;
  const query = qi >= 0 ? u.slice(qi + 1) : '';
  Promise.resolve().then(() => {
    if (p === '/api/hit') return req.method === 'POST' ? handleHit(req, res) : send(res, 405, '');
    if (p === '/admin') return send(res, 301, '', { Location: '/admin/' });
    if (p === '/admin/') return req.method === 'GET' ? serveAdminPage(req, res) : send(res, 405, '');
    if (p === '/api/admin/login') return req.method === 'POST' ? handleLogin(req, res) : send(res, 405, '');
    if (p === '/api/admin/logout') return req.method === 'POST' ? handleLogout(req, res) : send(res, 405, '');
    if (p.startsWith('/api/admin/')) return handleAdminApi(req, res, p);
    if (req.method !== 'GET' && req.method !== 'HEAD') return send(res, 405, 'Method not allowed');
    if (p === '/episodes_data.js') return servePublicData(req, res);
    return serveStatic(req, res, p, query);
  }).catch((e) => {
    console.error('Error on', p, e.message);   // the address only; nothing about the visitor
    if (!res.headersSent) send(res, 500, 'Server error'); else res.destroy();
  });
});

function shutdown() { saveStats(); process.exit(0); }
process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

server.listen(PORT, '0.0.0.0', () => {
  console.log('Biergerpakt Podcast on port ' + PORT + ' — ' + EPISODES.length + ' episodes (' +
    EPISODES.filter((e) => !isOnline(e)).length + ' waiting for validation) — data in ' + DATA_DIR +
    (ADMIN_PASSWORD ? '' : ' — admin OFF (no ADMIN_PASSWORD)'));
});
