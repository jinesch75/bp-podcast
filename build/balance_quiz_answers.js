#!/usr/bin/env node
// Spread the correct quiz answers evenly over A/B/C/D (all episodes, all languages).
// Deterministic: re-running gives the same result. The same reordering is applied to
// questions, questions_fr, questions_de and questions_lb so every language stays aligned.
// Within an episode no letter is correct more than twice; over all episodes each letter ~25%.
// Run from the project root:  node build/balance_quiz_answers.js [--write]
const fs = require('fs');
const src = fs.readFileSync('episodes_data.js', 'utf8');
const marker = src.indexOf('const EPISODES');
const banner = src.slice(0, marker).trim();
const EPISODES = new Function(src.slice(marker) + '\nreturn EPISODES;')();
const serialize = E => (banner ? banner + '\n' : '') + 'const EPISODES = ' + JSON.stringify(E, null, 1) + ';\n';
if (serialize(EPISODES) !== src) throw new Error('episodes_data.js does not round-trip — aborting');

function rng(seed) { let h = 2166136261; for (const c of seed) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return () => ((h = Math.imul(h ^ (h >>> 15), 2246822507) ^ Math.imul(h ^ (h >>> 13), 3266489909)) >>> 0) / 4294967296; }
const LANGS = ['', '_fr', '_de', '_lb'];
const total = [0, 0, 0, 0];
EPISODES.forEach((ep, j) => {
  const base = ep.questions;
  const n = base.length;
  // targets: consecutive letters (so max 2 of one letter per 5 questions), shuffled with a per-episode seed
  const r = rng(ep.key);
  const targets = Array.from({ length: n }, (_, i) => (j * n + i) % 4);
  for (let i = n - 1; i > 0; i--) { const k = Math.floor(r() * (i + 1)); [targets[i], targets[k]] = [targets[k], targets[i]]; }
  for (const l of LANGS) {
    const qs = ep['questions' + l];
    if (!qs) continue;
    if (qs.length !== n) throw new Error(`${ep.key}${l}: question count differs`);
    qs.forEach((q, i) => {
      if (q.correct !== base[i].correct || q.options.length !== base[i].options.length) throw new Error(`${ep.key}${l} Q${i + 1}: not aligned with EN`);
    });
  }
  const perms = base.map((q, i) => {           // perm[newPos] = oldPos
    const others = q.options.map((_, k) => k).filter(k => k !== q.correct);
    const perm = [];
    for (let pos = 0; pos < q.options.length; pos++) perm.push(pos === targets[i] ? q.correct : others.shift());
    return perm;
  });
  for (const l of LANGS) {
    const qs = ep['questions' + l];
    if (!qs) continue;
    qs.forEach((q, i) => {
      const perm = perms[i];
      const oldCorrect = q.correct;
      q.options = perm.map(k => q.options[k]);
      q.correct = perm.indexOf(oldCorrect);
    });
  }
  ep.questions.forEach(q => total[q.correct]++);
  console.log(String(ep.id).padStart(2), ep.key.padEnd(18), ep.questions.map(q => 'ABCD'[q.correct]).join(''));
});
console.log('total A/B/C/D:', total.join('/'));
if (process.argv.includes('--write')) { fs.writeFileSync('episodes_data.js', serialize(EPISODES)); console.log('episodes_data.js written'); }
