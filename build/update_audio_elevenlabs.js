#!/usr/bin/env node
// Swap in re-recorded (ElevenLabs) audio for an EXISTING episode whose text is unchanged.
//
//   node build/update_audio_elevenlabs.js <key> en,fr,de
//
// For each language it reads /tmp/<key>[_<lang>]_el_seg/podcast_<key>[_<lang>].mp3 and its
// segdata_fixed.json (written by `TEMPO=1.0 LOUDNORM=-20 python3 build/rebuild.py ...`), then:
//   1. verifies every sentence (count, speaker, text) is IDENTICAL to the live transcript —
//      any mismatch aborts before anything is written;
//   2. backs up episodes_data.js to episodes_data.pre_el_<key>.js (first run only);
//   3. copies the mp3s into the project root (same file names as before);
//   4. updates ONLY duration[_<lang>] and the `t` timestamps of segments[_<lang>].
// Titles, descriptions, topics, quizzes, categories, segments_lb and all other episodes are untouched.
// Run from the project root.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const [key, langArg] = process.argv.slice(2);
if (!key || !langArg) { console.log('usage: node build/update_audio_elevenlabs.js <key> en,fr,de'); process.exit(1); }
const langs = langArg.split(',').map(s => s.trim()).filter(Boolean);
for (const L of langs) if (!['en', 'fr', 'de'].includes(L)) { console.error('unsupported language: ' + L); process.exit(1); }

const ROOT = process.cwd();
const DATA = path.join(ROOT, 'episodes_data.js');
if (!fs.existsSync(DATA)) { console.error('episodes_data.js not found — run from the project root.'); process.exit(1); }
const src = fs.readFileSync(DATA, 'utf8');
const marker = src.indexOf('const EPISODES');
const banner = src.slice(0, marker).trim();
const EPISODES = new Function(src.slice(marker) + '\nreturn EPISODES;')();
const serialize = E => (banner ? banner + '\n' : '') + 'const EPISODES = ' + JSON.stringify(E, null, 1) + ';\n';
if (serialize(EPISODES) !== src) {
  console.error('episodes_data.js does not round-trip exactly through JSON — aborting so nothing else changes.');
  process.exit(1);
}
const ep = EPISODES.find(e => e.key === key);
if (!ep) { console.error('no episode with key ' + key); process.exit(1); }

const probe = f => parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());

// ---- 1. verify everything first ----
const plan = [];
let problems = 0;
for (const L of langs) {
  const sfx = L === 'en' ? '' : '_' + L;
  const work = `/tmp/${key}${sfx}_el_seg`;
  const mp3 = `${work}/podcast_${key}${sfx}.mp3`;
  const sdPath = `${work}/segdata_fixed.json`;
  const segKey = L === 'en' ? 'segments' : 'segments_' + L;
  const durKey = L === 'en' ? 'duration' : 'duration_' + L;
  const audioKey = L === 'en' ? 'audio' : 'audio_' + L;
  if (!fs.existsSync(mp3) || !fs.existsSync(sdPath)) { console.error(`[${L}] missing ${mp3} or segdata_fixed.json — run tts_elevenlabs.py + rebuild.py first`); problems++; continue; }
  const sd = JSON.parse(fs.readFileSync(sdPath, 'utf8'));
  const live = ep[segKey] || [];
  const neu = sd.segments;
  const bad = [];
  if (live.length !== neu.length) bad.push(`sentence count: live ${live.length} vs new ${neu.length}`);
  for (let i = 0; i < Math.min(live.length, neu.length); i++) {
    if (live[i].speaker !== neu[i].speaker) bad.push(`#${i} speaker: live ${live[i].speaker} vs new ${neu[i].speaker}`);
    else if (live[i].text.trim() !== neu[i].text.trim()) bad.push(`#${i} text:\n      live: ${live[i].text}\n      new:  ${neu[i].text}`);
  }
  if (bad.length) {
    console.error(`[${L}] SENTENCE MISMATCH (${bad.length}):`);
    bad.slice(0, 10).forEach(b => console.error('   ' + b));
    problems++; continue;
  }
  const real = probe(mp3);
  if (Math.abs(real - sd.duration) > 0.2) { console.error(`[${L}] duration mismatch: segdata ${sd.duration} vs mp3 ${real}`); problems++; continue; }
  const last = neu[neu.length - 1].t;
  if (!(last < sd.duration && sd.duration - last < 30)) { console.error(`[${L}] last timestamp ${last} looks wrong for duration ${sd.duration}`); problems++; continue; }
  plan.push({ L, mp3, segKey, durKey, dest: ep[audioKey] || `podcast_${key}${sfx}.mp3`, sd, oldDur: ep[durKey] });
}
if (problems) { console.error('\nNothing was changed.'); process.exit(2); }

// ---- 2. backup ----
const backup = path.join(ROOT, `episodes_data.pre_el_${key}.js`);
if (!fs.existsSync(backup)) { fs.copyFileSync(DATA, backup); console.log('backup: ' + path.basename(backup)); }
else console.log('backup already exists (kept): ' + path.basename(backup));

// ---- 3 + 4. copy audio, update timings ----
for (const p of plan) {
  fs.copyFileSync(p.mp3, path.join(ROOT, p.dest));
  ep[p.durKey] = p.sd.duration;
  ep[p.segKey].forEach((s, i) => { s.t = p.sd.segments[i].t; });
  console.log(`[${p.L}] ${p.dest}: ${p.sd.segments.length} sentences OK, duration ${p.oldDur} -> ${p.sd.duration}`);
}
fs.writeFileSync(DATA, serialize(EPISODES));
console.log('episodes_data.js updated (timings + durations only).');
// new ?v= on the index.html script tags so browsers load the new episodes_data.js
execFileSync(process.execPath, [path.join(__dirname, 'bump_version.js')], { stdio: 'inherit' });
