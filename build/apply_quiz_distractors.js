#!/usr/bin/env node
// Replace the WRONG quiz options (distractors) with the rewritten ones in build/quiz_distractors/*.json.
// Goal: wrong answers about as long and specific as the right one, so the longest option is no giveaway.
// JSON: { "<key>": [ {"en":[3], "fr":[3], "de":[3], "lb":[3]}  x5 questions ] } — the 3 texts fill the
// wrong positions in A→D order. Correct answers, question texts and explanations are never touched.
// Run from the project root:  node build/apply_quiz_distractors.js [--write]
const fs = require('fs'), path = require('path');
const src = fs.readFileSync('episodes_data.js', 'utf8');
const marker = src.indexOf('const EPISODES');
const banner = src.slice(0, marker).trim();
const EPISODES = new Function(src.slice(marker) + '\nreturn EPISODES;')();
const serialize = E => (banner ? banner + '\n' : '') + 'const EPISODES = ' + JSON.stringify(E, null, 1) + ';\n';
if (serialize(EPISODES) !== src) throw new Error('episodes_data.js does not round-trip — aborting');
const dir = path.join('build', 'quiz_distractors');
const data = {};
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.json')).sort()) Object.assign(data, JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')));
const LANGS = { en: '', fr: '_fr', de: '_de', lb: '_lb' };
let applied = 0;
for (const [key, qs] of Object.entries(data)) {
  const ep = EPISODES.find(e => e.key === key);
  if (!ep) throw new Error('unknown episode ' + key);
  if (qs.length !== ep.questions.length) throw new Error(key + ': expected ' + ep.questions.length + ' questions');
  qs.forEach((d, i) => {
    for (const [lang, suf] of Object.entries(LANGS)) {
      const q = (ep['questions' + suf] || [])[i];
      if (!q) continue;
      const texts = d[lang];
      if (!texts || texts.length !== q.options.length - 1) throw new Error(`${key} Q${i + 1} ${lang}: need ${q.options.length - 1} wrong answers`);
      let t = 0;
      q.options = q.options.map((o, k) => (k === q.correct ? o : texts[t++]));
      applied++;
    }
  });
}
// report: how often is the correct answer the (strictly) longest option?
for (const [lang, suf] of Object.entries(LANGS)) {
  let n = 0, longest = 0;
  for (const ep of EPISODES) for (const q of ep['questions' + suf] || []) {
    n++; const L = q.options.map(o => o.length);
    if (L.filter((x, k) => k !== q.correct).every(x => x < L[q.correct])) longest++;
  }
  console.log(`${lang}: correct answer is the longest in ${longest}/${n} questions`);
}
console.log('episodes with new wrong answers:', Object.keys(data).length, '| question-languages updated:', applied);
if (process.argv.includes('--write')) { fs.writeFileSync('episodes_data.js', serialize(EPISODES)); console.log('episodes_data.js written'); }
