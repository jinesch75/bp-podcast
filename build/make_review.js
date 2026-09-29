// Generate fully isolated per-episode review pages under review/<key>-<token>/.
// Each page contains ONLY that episode's data (episodes_data.js is sliced to one episode).
// Audio, app.js and svg assets are referenced from the repo root via ../../ so nothing is duplicated.
// Tokens persist in build/review_tokens.json so links stay stable across regenerations.
// Usage: node build/make_review.js key1,key2,...   (default: myguichet,benevolat,eltereforum,dsp_cns,lualert)
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const PROJ = path.join(__dirname, '..');
const BASE_URL = 'https://bp-podcast-production.up.railway.app';

const KEYS = (process.argv[2] || 'myguichet,benevolat,eltereforum,dsp_cns,lualert').split(',');

const src = fs.readFileSync(path.join(PROJ, 'episodes_data.js'), 'utf8');
let EPISODES; eval(src.replace('const EPISODES', 'EPISODES'));

const tokPath = path.join(__dirname, 'review_tokens.json');
const tokens = fs.existsSync(tokPath) ? JSON.parse(fs.readFileSync(tokPath, 'utf8')) : {};

let html = fs.readFileSync(path.join(PROJ, 'index.html'), 'utf8');
// Point shared assets at the repo root; keep episodes_data.js local (the one-episode slice).
html = html
  .replace('href="favicon.svg"', 'href="../../favicon.svg"')
  .replace('src="app.js"', 'src="../../app.js"')
  .replace(/src="gov-light\.svg"/g, 'src="../../gov-light.svg"');
// Small review banner just after <body...>
html = html.replace(/(<body[^>]*>)/, '$1\n<div style="background:#b7791f;color:#fff;text-align:center;padding:6px 12px;font:600 13px/1.4 system-ui,sans-serif;">Preview for review — single episode. Please do not share this link.</div>');

const links = [];
KEYS.forEach(function (key) {
  const ep = EPISODES.find(function (e) { return e.key === key; });
  if (!ep) throw new Error('unknown key ' + key);
  if (!tokens[key]) tokens[key] = crypto.randomBytes(5).toString('hex');
  const slug = key.replace(/_/g, '-') + '-' + tokens[key];
  const dir = path.join(PROJ, 'review', slug);
  fs.mkdirSync(dir, { recursive: true });

  // One-episode copy with audio paths pointing at the repo root
  const copy = JSON.parse(JSON.stringify(ep));
  copy.audio = '../../' + copy.audio;
  if (copy.audio_fr) copy.audio_fr = '../../' + copy.audio_fr;
  if (copy.audio_de) copy.audio_de = '../../' + copy.audio_de;
  fs.writeFileSync(path.join(dir, 'episodes_data.js'), 'const EPISODES = ' + JSON.stringify([copy], null, 1) + ';\n');
  fs.writeFileSync(path.join(dir, 'index.html'), html);
  links.push({ key: key, title: ep.title, url: BASE_URL + '/review/' + slug + '/' });
});

fs.writeFileSync(tokPath, JSON.stringify(tokens, null, 1));
links.forEach(function (l) { console.log(l.key + '\n  ' + l.title + '\n  ' + l.url + '\n'); });
