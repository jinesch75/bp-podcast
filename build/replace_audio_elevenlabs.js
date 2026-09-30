#!/usr/bin/env node
// Swap in re-recorded ElevenLabs audio for an episode whose SCRIPT CHANGED since the last recording.
//
//   node build/replace_audio_elevenlabs.js <key[,key2,...]> en,fr,de
//
// Unlike update_audio_elevenlabs.js (text unchanged, timings only), this REPLACES the transcript:
// for each language it reads /tmp/<key>[_<lang>]_el_seg/{podcast_<key>[_<lang>].mp3, segdata_fixed.json}
// (written by tts_elevenlabs.py + `TEMPO=1.0 LOUDNORM=-20 rebuild.py`, or build/el_run_batch.py), then
//   1. checks the recorded sentences are exactly the current podcast_script_<key>[_<lang>].md
//      (same speakers, same text) — any mismatch aborts before anything is written;
//   2. copies the mp3 into the project root (same file name as before);
//   3. sets segments[_<lang>] (speaker, text, t) and duration[_<lang>] from the new recording;
//   4. rebuilds segments_lb (turn-level read-along) from podcast_script_<key>_lb.md, timed on the new English audio.
// Titles, descriptions, topics, quizzes and categories are untouched. A backup of episodes_data.js
// goes to ~/episodes_data.before_replace_<key>.js (outside the project). Run from the project root.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const [keyArg, langArg] = process.argv.slice(2);
if (!keyArg || !langArg) { console.log('usage: node build/replace_audio_elevenlabs.js <key[,key2]> en,fr,de'); process.exit(1); }
const keys = keyArg.split(',').map(s => s.trim()).filter(Boolean);
const langs = langArg.split(',').map(s => s.trim()).filter(Boolean);
for (const L of langs) if (!['en', 'fr', 'de'].includes(L)) { console.error('unsupported language: ' + L); process.exit(1); }

const ROOT = process.cwd();
const DATA = path.join(ROOT, 'episodes_data.js');
const src = fs.readFileSync(DATA, 'utf8');
const marker = src.indexOf('const EPISODES');
const banner = src.slice(0, marker);
const EPISODES = new Function(src + '\nreturn EPISODES;')();
const serialize = E => banner + 'const EPISODES = ' + JSON.stringify(E, null, 1) + ';\n';
if (serialize(EPISODES) !== src) { console.error('episodes_data.js does not round-trip exactly — aborting.'); process.exit(1); }

const probe = f => parseFloat(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString());
const norm = s => s.replace(/\s+/g, ' ').trim();
function turnsOf(file) {
  const out = [];
  for (const line of fs.readFileSync(file, 'utf8').split('\n')) {
    const m = line.trim().match(/^\*\*(ANNA|TOM)\s*:\*\*\s*(.*)$/);
    if (m && m[2].trim()) out.push({ speaker: m[1] === 'ANNA' ? 'Anna' : 'Tom', text: m[2].trim() });
  }
  return out;
}
// same mapping as build/lib_segments.py build_turns(): each turn starts where the matching speaker run starts
function buildTurns(enSegs, turns) {
  const runs = [];
  let last = null;
  for (const s of enSegs) if (s.speaker !== last) { runs.push([s.speaker, s.t]); last = s.speaker; }
  const times = [];
  let ri = 0;
  for (const tr of turns) {
    if (ri < runs.length && runs[ri][0] === tr.speaker) { times.push(runs[ri][1]); ri++; }
    else if (ri - 1 >= 0 && runs[ri - 1][0] === tr.speaker) times.push(runs[ri - 1][1]);
    else if (ri < runs.length) { times.push(runs[ri][1]); ri++; }
    else times.push(times.length ? times[times.length - 1] : 0);
  }
  for (let i = 1; i < times.length; i++) if (times[i] < times[i - 1]) times[i] = times[i - 1];
  return turns.map((tr, i) => ({ speaker: tr.speaker, text: tr.text, t: Math.round(times[i] * 100) / 100 }));
}

const plan = [];
let problems = 0;
for (const key of keys) {
  const ep = EPISODES.find(e => e.key === key);
  if (!ep) { console.error('no episode with key ' + key); problems++; continue; }
  for (const L of langs) {
    const sfx = L === 'en' ? '' : '_' + L;
    const work = `/tmp/${key}${sfx}_el_seg`;
    const mp3 = `${work}/podcast_${key}${sfx}.mp3`;
    const sdPath = `${work}/segdata_fixed.json`;
    if (!fs.existsSync(mp3) || !fs.existsSync(sdPath)) { console.error(`[${key} ${L}] missing recording in ${work}`); problems++; continue; }
    const sd = JSON.parse(fs.readFileSync(sdPath, 'utf8'));
    const turns = turnsOf(path.join(ROOT, `podcast_script_${key}${sfx}.md`));
    // the recording must be exactly the current script: same text, and each turn's speaker
    const recText = norm(sd.segments.map(s => s.text).join(' '));
    const scrText = norm(turns.map(t => t.text).join(' '));
    const bad = [];
    if (recText !== scrText) {
      let i = 0; while (i < recText.length && recText[i] === scrText[i]) i++;
      bad.push(`text differs near: …${scrText.slice(Math.max(0, i - 40), i + 40)}…`);
    }
    const recSpk = sd.segments.map(s => s.speaker).filter((s, i, a) => i === 0 || s !== a[i - 1]).join(',');
    const scrSpk = turns.map(t => t.speaker).filter((s, i, a) => i === 0 || s !== a[i - 1]).join(',');
    if (recSpk !== scrSpk) bad.push('speaker order differs from the script');
    const real = probe(mp3);
    if (Math.abs(real - sd.duration) > 0.2) bad.push(`duration: segdata ${sd.duration} vs mp3 ${real}`);
    const lastT = sd.segments[sd.segments.length - 1].t;
    if (!(lastT < sd.duration && sd.duration - lastT < 30)) bad.push(`last timestamp ${lastT} vs duration ${sd.duration}`);
    if (bad.length) { console.error(`[${key} ${L}] NOT OK:\n   ` + bad.join('\n   ')); problems++; continue; }
    plan.push({ ep, key, L, mp3, sd,
      segKey: L === 'en' ? 'segments' : 'segments_' + L,
      durKey: L === 'en' ? 'duration' : 'duration_' + L,
      dest: ep[L === 'en' ? 'audio' : 'audio_' + L] || `podcast_${key}${sfx}.mp3` });
  }
}
if (problems) { console.error('\nNothing was changed.'); process.exit(2); }

const backup = path.join(os.homedir(), `episodes_data.before_replace_${keys.length > 1 ? 'batch' : keys[0]}.js`);
if (!fs.existsSync(backup)) fs.copyFileSync(DATA, backup);

for (const p of plan) {
  fs.copyFileSync(p.mp3, path.join(ROOT, p.dest));
  const old = p.ep[p.durKey];
  p.ep[p.segKey] = p.sd.segments.map(s => ({ speaker: s.speaker, text: s.text, t: s.t }));
  p.ep[p.durKey] = p.sd.duration;
  if (p.L === 'en') p.ep.audio = p.dest; else p.ep['audio_' + p.L] = p.dest;
  console.log(`[${p.key} ${p.L}] ${p.dest}: ${p.sd.segments.length} sentences, duration ${old} -> ${p.sd.duration}`);
}
for (const key of keys) {
  if (!langs.includes('en')) break;
  const ep = EPISODES.find(e => e.key === key);
  const lbFile = path.join(ROOT, `podcast_script_${key}_lb.md`);
  if (fs.existsSync(lbFile)) {
    ep.segments_lb = buildTurns(ep.segments, turnsOf(lbFile));
    console.log(`[${key} lb] segments_lb rebuilt: ${ep.segments_lb.length} turns on the new English audio`);
  }
}
fs.writeFileSync(DATA, serialize(EPISODES));
console.log('episodes_data.js updated. Backup: ' + backup);
execFileSync(process.execPath, [path.join(__dirname, 'bump_version.js')], { stdio: 'inherit' });
