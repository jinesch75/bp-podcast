#!/usr/bin/env node
// Quiz updates from the LuxTrust fact-check of 2 Nov 2026, validated by Jacques.
// Usage: node build/apply_factcheck_quiz_2026_11.js [--write]
// Each edit replaces one substring in one quiz field; re-running is safe.
const fs = require('fs');
const path = require('path');
const FILE = path.join(__dirname, '..', 'episodes_data.js');

const Q = []; // [key, field, questionIndex(0-based), part ('text'|'explanation'|optionIndex), old, new]
const q = (...a) => Q.push(a);

// LuxTrust Q1: 'qualified' provider instead of 'European-certified'
q('luxtrust', 'questions', 0, 'explanation', 'provided by a European-certified Certificate Authority and trust service provider.', "provided by a Certificate Authority and trust service provider officially recognised as 'qualified' in the European Union.");
q('luxtrust', 'questions_fr', 0, 'explanation', 'fournie par une autorité de certification et un prestataire de services de confiance certifiés au niveau européen.', 'fournie par une autorité de certification et un prestataire de services de confiance officiellement reconnu comme « qualifié » dans l\'Union européenne.');
q('luxtrust', 'questions_de', 0, 'explanation', 'bereitgestellt von einer europäisch zertifizierten Zertifizierungsstelle und einem Vertrauensdiensteanbieter.', 'bereitgestellt von einer Zertifizierungsstelle und einem Vertrauensdiensteanbieter, der in der Europäischen Union offiziell als „qualifiziert" anerkannt ist.');
// LuxTrust Q4: where you can be identified in person (correct option kept short so it is not the longest)

q('luxtrust', 'questions', 3, 'explanation', 'face-to-face with an agent or remotely by video identification.', 'in person (at LuxTrust, at a partner such as your bank, or at a notary) or remotely by video identification.');
q('luxtrust', 'questions_fr', 3, 'explanation', 'en face à face avec un agent ou à distance par identification vidéo.', 'en personne (chez LuxTrust, chez un partenaire comme votre banque, ou chez un notaire) ou à distance par identification vidéo.');
q('luxtrust', 'questions_de', 3, 'explanation', 'persönlich bei einem Agenten oder aus der Ferne per Video-Identifikation.', 'persönlich (bei LuxTrust, bei einem Partner wie Ihrer Bank oder bei einem Notar) oder aus der Ferne per Video-Identifikation.');
q('luxtrust', 'questions', 3, 3, 'in person with an agent, or remotely', 'in person, or remotely');
q('luxtrust', 'questions_fr', 3, 3, 'en personne avec un agent, ou à distance', 'en personne, ou à distance');
q('luxtrust', 'questions_de', 3, 3, 'persönlich bei einem Agenten oder aus der Ferne', 'persönlich oder aus der Ferne');

const src = fs.readFileSync(FILE, 'utf8');
const i = src.indexOf('const EPISODES');
const banner = src.slice(0, i);
const E = new Function(src + ';return EPISODES;')();
const ser = (data) => banner + 'const EPISODES = ' + JSON.stringify(data, null, 1) + ';\n';
if (ser(E) !== src) { console.error('Round-trip check failed – file format differs, aborting.'); process.exit(1); }

let applied = 0, skipped = 0; const problems = [];
for (const [key, field, qi, part, oldS, newS] of Q) {
  const ep = E.find(e => e.key === key);
  const qq = ep && ep[field] && ep[field][qi];
  if (!qq) { problems.push(`${key} ${field} Q${qi + 1}: not found`); continue; }
  const get = () => (typeof part === 'number' ? qq.options[part] : qq[part]);
  const set = (v) => { if (typeof part === 'number') qq.options[part] = v; else qq[part] = v; };
  const cur = get();
  if (oldS === null) { if (cur === newS) skipped++; else { set(newS); applied++; } continue; }
  const n = cur.split(oldS).length - 1;
  if (n === 0 && cur.includes(newS)) { skipped++; continue; }
  if (n !== 1) { problems.push(`${key} ${field} Q${qi + 1} ${part}: found ${n}x "${oldS}"`); continue; }
  set(cur.replace(oldS, newS)); applied++;
}
problems.forEach(p => console.log('PROBLEM', p));
console.log(`quiz edits: ${applied} applied, ${skipped} already done, ${problems.length} problems`);
if (problems.length) process.exit(1);

// sanity: every question still has 4 distinct options and a valid answer
let bad = 0;
for (const e of E) for (const f of ['questions', 'questions_fr', 'questions_de', 'questions_lb']) (e[f] || []).forEach((x, n) => {
  if (x.options.length !== 4 || new Set(x.options).size !== 4 || !(x.correct >= 0 && x.correct < 4)) { bad++; console.log('BAD', e.key, f, n + 1); }
});
if (bad) process.exit(1);
if (process.argv.includes('--write')) { fs.writeFileSync(FILE, ser(E)); console.log('written', FILE); }
