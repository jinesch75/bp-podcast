#!/usr/bin/env node
// Cache-busting: sets ?v=<timestamp> on the episodes_data.js and app.js <script> tags in index.html,
// so browsers fetch the new files after a change instead of using a stale cached copy.
// Run after changing app.js or episodes_data.js (update_audio_elevenlabs.js runs it automatically),
// then regenerate any review pages you share (node build/make_review.js <key>).
// Audio needs no bump: app.js appends ?v=<duration> to each mp3, which changes whenever it is re-recorded.
const fs = require('fs');
const path = require('path');
const file = path.join(__dirname, '..', 'index.html');
const d = new Date();
const v = d.toISOString().replace(/[-:T]/g, '').slice(0, 12); // YYYYMMDDHHMM (UTC)
let html = fs.readFileSync(file, 'utf8');
let n = 0;
html = html.replace(/src="(episodes_data\.js|app\.js)(\?v=[^"]*)?"/g, (m, f) => { n++; return `src="${f}?v=${v}"`; });
if (n !== 2) { console.error(`expected 2 script tags in index.html, found ${n} — nothing written`); process.exit(1); }
fs.writeFileSync(file, html);
console.log('index.html asset version -> ' + v);
