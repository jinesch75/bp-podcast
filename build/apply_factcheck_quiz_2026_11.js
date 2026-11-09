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
// Digital Inclusion Q3 (2 Nov 2026): conditions from the main application page, 12+ rule
q('digitalinclusion', 'questions', 2, 'explanation', null, "You must live in Luxembourg and meet one condition – for example your household receives the cost-of-living allowance (allocation de vie chère), you are in a collective debt settlement procedure, you hold a 'vie privée' residence permit, or you are an asylum seeker, an unaccompanied minor or under temporary protection. Each household member aged 12 or older can get their own computer, as long as donations allow. See digital-inclusion.lu for the current conditions and waiting time.");
q('digitalinclusion', 'questions_fr', 2, 'explanation', null, "Vous devez vivre au Luxembourg et remplir une condition – par exemple votre ménage perçoit l'allocation de vie chère (AVC), vous bénéficiez d'un règlement collectif des dettes, vous avez un titre de séjour « vie privée », ou vous êtes demandeur d'asile, mineur non accompagné ou sous protection temporaire. Chaque membre du ménage âgé de 12 ans ou plus peut recevoir son propre ordinateur, tant que les dons le permettent. Consultez digital-inclusion.lu pour les conditions et le délai d'attente actuels.");
q('digitalinclusion', 'questions_de', 2, 'explanation', null, "Sie müssen in Luxemburg leben und eine Bedingung erfüllen – zum Beispiel bezieht Ihr Haushalt die Teuerungszulage (allocation de vie chère), Sie sind in einem kollektiven Schuldenregulierungsverfahren, Sie haben eine Aufenthaltserlaubnis „Privatleben“ (vie privée), oder Sie sind Asylsuchender, unbegleiteter Minderjähriger oder stehen unter vorübergehendem Schutz. Jedes Haushaltsmitglied ab 12 Jahren kann einen eigenen Computer bekommen, solange die Spenden reichen. Die aktuellen Bedingungen und die Wartezeit finden Sie auf digital-inclusion.lu.");
// Work in Luxembourg Q3 (2 Nov 2026): '11,000 candidates' no longer published -> pre-screened by ADEM
q('workinluxembourg', 'questions', 2, 0 + 2, 'and around 11,000 pre-selected candidates', 'and candidates pre-screened by ADEM');
q('workinluxembourg', 'questions', 2, 'explanation', 'and the pool already holds around 11,000 candidates pre-selected by ADEM.', 'and every candidate profile is pre-screened by ADEM. The board focuses on shortage occupations.');
q('workinluxembourg', 'questions_fr', 2, 0 + 2, 'et environ 11 000 candidats présélectionnés', "et des candidats présélectionnés par l'ADEM");
q('workinluxembourg', 'questions_fr', 2, 'explanation', "et le vivier compte déjà environ 11 000 candidats présélectionnés par l'ADEM.", "et chaque profil de candidat est présélectionné par l'ADEM. Le Job Board se concentre sur les métiers en pénurie.");
q('workinluxembourg', 'questions_de', 2, 0 + 2, 'und rund 11 000 vorausgewählten Kandidaten', 'und von ADEM vorab geprüften Kandidaten');
q('workinluxembourg', 'questions_de', 2, 'explanation', 'und der Pool umfasst bereits rund 11 000 von ADEM vorausgewählte Kandidaten.', 'und jedes Kandidatenprofil wird von ADEM vorab geprüft. Das Job Board konzentriert sich auf Mangelberufe.');
// DSP-CNS (9 Nov 2026): no 'about half' figure; DSP also opens in the MyGuichet eSpace
q('dsp_cns', 'questions', 2, 'explanation', 'About half of doctors now use immediate direct payment:', 'More and more doctors and dentists use immediate direct payment:');
q('dsp_cns', 'questions_fr', 2, 'explanation', 'Environ la moitié des médecins utilisent désormais le paiement immédiat direct :', 'De plus en plus de médecins et de dentistes utilisent le paiement immédiat direct :');
q('dsp_cns', 'questions_de', 2, 'explanation', 'Etwa die Hälfte der Ärzte nutzt inzwischen die sofortige Direktzahlung:', 'Immer mehr Ärzte und Zahnärzte nutzen die sofortige Direktzahlung:');
q('dsp_cns', 'questions_lb', 2, 'explanation', "Ongeféier d'Hallschent vun den Dokteren benotzt elo den direkte Paiement:", 'Ëmmer méi Dokteren an Zänndokteren benotzen den direkte Paiement:');
q('dsp_cns', 'questions', 4, 'explanation', 'you log in through the eSanté portal — or use', 'you open it in your MyGuichet eSpace or on the eSanté portal — or use');
q('dsp_cns', 'questions_fr', 4, 'explanation', 'vous vous connectez via le portail eSanté — ou', 'vous l\'ouvrez dans votre eSpace MyGuichet ou sur le portail eSanté — ou');
q('dsp_cns', 'questions_de', 4, 'explanation', 'melden Sie sich über das eSanté-Portal an — oder', 'öffnen Sie es in Ihrem MyGuichet-eSpace oder auf dem eSanté-Portal — oder');
q('dsp_cns', 'questions_lb', 4, 'explanation', 'loggt Dir Iech iwwer den eSanté-Portal an — oder', 'maacht Dir en an Ärem MyGuichet-eSpace oder um eSanté-Portal op — oder');

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
