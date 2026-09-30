#!/usr/bin/env node
// Quiz updates from the fact-check of 30 Sept 2026 (episodes 1-13), validated by Jacques.
// Each edit replaces one substring in one quiz field; re-running is safe.
// Only quiz text changes: transcripts (segments) stay in sync with the recorded audio.
// Usage: node build/apply_factcheck_quiz_2026_09.js [--write]
const fs = require('fs');
const path = require('path');
const FILE = path.join(__dirname, '..', 'episodes_data.js');

const Q = []; // [key, field, questionIndex(0-based), part ('text'|'explanation'|optionIndex), old, new]
const q = (...a) => Q.push(a);

// 1A MyGuichet Q3: registration needs a computer
q('myguichet', 'questions', 2, 'explanation', 'an email address, a device,', 'an email address, a computer (a laptop or desktop for the first registration),');
q('myguichet', 'questions_fr', 2, 'explanation', 'une adresse e-mail, un appareil,', 'une adresse e-mail, un ordinateur (portable ou fixe pour la première inscription),');
q('myguichet', 'questions_de', 2, 'explanation', 'eine E-Mail-Adresse, ein Gerät', 'eine E-Mail-Adresse, einen Computer (für die erste Registrierung einen Laptop oder Desktop-PC)');
q('myguichet', 'questions_lb', 2, 'explanation', 'eng E-Mail-Adress, en Apparat,', 'eng E-Mail-Adress, e Computer (fir déi éischt Aschreiwung e Laptop oder en Desktop),');

// 2B LuxTrust Q5: official wording
q('luxtrust', 'questions', 4, 1, 'never ask to access your device', 'never call you for sensitive data');
q('luxtrust', 'questions', 4, 'explanation', 'never requests access to your computer or phone', 'never calls you to ask for sensitive information, never asks you to confirm a payment or banking operation');
q('luxtrust', 'questions_fr', 4, 1, null, 'LuxTrust ne vous demandera jamais vos codes, ne vous appellera jamais pour des données sensibles et ne viendra jamais chez vous');
q('luxtrust', 'questions_fr', 4, 'explanation', 'ne demande jamais à accéder à votre ordinateur ou à votre téléphone', "ne vous appelle jamais pour demander des informations sensibles, ne vous demande jamais de confirmer un paiement ou une opération bancaire");
q('luxtrust', 'questions_de', 4, 1, null, 'LuxTrust fragt niemals nach Ihren Codes, ruft Sie niemals wegen sensibler Daten an und kommt niemals zu Ihnen nach Hause');
q('luxtrust', 'questions_de', 4, 'explanation', 'verlangt niemals Zugriff auf Ihren Computer oder Ihr Handy', 'ruft Sie niemals an, um nach sensiblen Informationen zu fragen, bittet Sie niemals, eine Zahlung oder Bankoperation zu bestätigen,');

// 3A Volunteering Q4: examples
q('benevolat', 'questions', 3, 'explanation', 'manning a barbecue', 'helping at a summer party');
q('benevolat', 'questions_fr', 3, 'explanation', 'tenir un barbecue', "donner un coup de main à une fête d'été");
q('benevolat', 'questions_de', 3, 'explanation', 'den Grill übernehmen', 'bei einem Sommerfest mithelfen');
q('benevolat', 'questions_lb', 3, 'explanation', 'de Grill bedéngen', 'bei engem Summerfest mat upaken');

// 5A Digital Inclusion Q3: hedged conditions (null = replace the whole field)
q('digitalinclusion', 'questions', 2, 'explanation', null, 'You must live in Luxembourg and meet one condition – for example your household receives the cost-of-living allowance (allocation de vie chère), or you are an asylum seeker or under temporary protection. See digital-inclusion.lu for the full, current conditions and waiting times.');
q('digitalinclusion', 'questions_fr', 2, 'explanation', null, "Vous devez vivre au Luxembourg et remplir une condition – par exemple votre ménage perçoit l'allocation de vie chère (AVC), ou vous êtes demandeur d'asile ou sous protection temporaire. Consultez digital-inclusion.lu pour les conditions complètes et actuelles et les délais d'attente.");
q('digitalinclusion', 'questions_de', 2, 'explanation', null, 'Sie müssen in Luxemburg leben und eine Bedingung erfüllen – zum Beispiel bezieht Ihr Haushalt die Teuerungszulage (allocation de vie chère), oder Sie sind Asylsuchender oder stehen unter vorübergehendem Schutz. Die vollständigen, aktuellen Bedingungen und Wartezeiten finden Sie auf digital-inclusion.lu.');

// 7A/7B DSP-CNS Q3: immediate direct payment, payment times
q('dsp_cns', 'questions', 2, 1, null, 'Either you pay only your share (immediate direct payment), or you pay first and the CNS reimburses most of it');
q('dsp_cns', 'questions', 2, 'explanation', null, 'About half of doctors now use immediate direct payment: you pay only your own share and the CNS pays the doctor the rest. Otherwise you pay first, send the invoice to the CNS, and it reimburses most of it (around 80–100%) – usually within a few weeks for a paper bill, or a few days for a digital one.');
q('dsp_cns', 'questions_fr', 2, 1, null, "Soit vous ne payez que votre part (paiement immédiat direct), soit vous payez d'abord et la CNS vous rembourse la plus grande partie");
q('dsp_cns', 'questions_fr', 2, 'explanation', null, "Environ la moitié des médecins utilisent désormais le paiement immédiat direct : vous ne payez que votre part et la CNS paie le reste au médecin. Sinon, vous payez d'abord, vous envoyez la facture à la CNS, et elle vous rembourse la plus grande partie (environ 80 à 100 %) – en général en quelques semaines pour une facture papier, ou en quelques jours pour une facture digitale.");
q('dsp_cns', 'questions_de', 2, 1, null, 'Entweder zahlen Sie nur Ihren Anteil (Direktzahlung), oder Sie zahlen zuerst und die CNS erstattet das meiste');
q('dsp_cns', 'questions_de', 2, 'explanation', null, 'Etwa die Hälfte der Ärzte nutzt inzwischen die sofortige Direktzahlung: Sie zahlen nur Ihren Anteil, und die CNS zahlt dem Arzt den Rest. Sonst zahlen Sie zuerst, schicken die Rechnung an die CNS, und diese erstattet das meiste (etwa 80–100 %) – meist innerhalb weniger Wochen bei einer Papierrechnung oder weniger Tage bei einer digitalen Rechnung.');
q('dsp_cns', 'questions_lb', 2, 1, null, "Entweder just Ären Undeel (direkte Paiement), oder fir d'éischt bezuelen an d'CNS rembourséiert dat meescht");
q('dsp_cns', 'questions_lb', 2, 'explanation', null, "Ongeféier d'Hallschent vun den Dokteren benotzt elo den direkte Paiement: Dir bezuelt just Ären Undeel, an d'CNS bezilt dem Dokter de Rescht. Soss bezuelt Dir fir d'éischt, schéckt d'Rechnung un d'CNS, a si rembourséiert dat meescht (ronn 80–100%) – meeschtens bannent e puer Wochen fir eng Rechnung op Pabeier, oder e puer Deeg fir eng digital Rechnung.");

// 8A LU-Alert Q4: monthly siren test
q('lualert', 'questions', 3, 'explanation', 'the app, websites and the media.', 'the app, websites and the media. The sirens are tested on the first Monday of each month, around noon.');
q('lualert', 'questions_fr', 3, 'explanation', "l'application, les sites internet et les médias.", "l'application, les sites internet et les médias. Les sirènes sont testées le premier lundi de chaque mois, vers midi.");
q('lualert', 'questions_de', 3, 'explanation', 'die App, Websites und die Medien.', 'die App, Websites und die Medien. Die Sirenen werden am ersten Montag jedes Monats gegen Mittag getestet.');
q('lualert', 'questions_lb', 3, 'explanation', "d'App, d'Websäiten an d'Medien.", "d'App, d'Websäiten an d'Medien. D'Sirene ginn den éischte Méindeg vun all Mount géint Mëtteg getest.");

// 10 Info-Senior Q2 (law date) and Q5 (Senioren-Telefon, SIMPA)
q('infosenior', 'questions', 1, 'explanation', 'The register is based on the law in force since 1 March 2024 and is updated regularly.', 'The register is based on the law of 23 August 2023, has been online since 1 March 2024 and is updated regularly.');
q('infosenior', 'questions_fr', 1, 'explanation', 'Le registre repose sur la loi en vigueur depuis le 1er mars 2024 et est mis à jour régulièrement.', 'Le registre repose sur la loi du 23 août 2023, est en ligne depuis le 1er mars 2024 et est mis à jour régulièrement.');
q('infosenior', 'questions_de', 1, 'explanation', 'Das Register beruht auf dem seit dem 1. März 2024 geltenden Gesetz und wird regelmäßig aktualisiert.', 'Das Register beruht auf dem Gesetz vom 23. August 2023, ist seit dem 1. März 2024 online und wird regelmäßig aktualisiert.');
// Q5 correct option kept without the name, so it is not the longest option (SIMPA is named in the explanation)
q('infosenior', 'questions', 4, 1, null, 'A national information and mediation service that can guide you and help find a solution');
q('infosenior', 'questions', 4, 'explanation', null, 'Besides the website and the register, you can call the Senioren-Telefon (247-86000) for information and advice, and SIMPA, the national information and mediation service for older people, can guide you and help resolve a disagreement with a service – so you are never left on your own.');
q('infosenior', 'questions_fr', 4, 1, null, "Un service national d'information et de médiation qui peut vous orienter et vous aider à trouver une solution");
q('infosenior', 'questions_fr', 4, 'explanation', null, "Outre le site web et le registre, vous pouvez appeler le Senioren-Telefon (247-86000) pour vous informer et vous faire conseiller, et le SIMPA, le service national d'information et de médiation pour personnes âgées, peut vous orienter et vous aider à résoudre un désaccord avec un service – vous n'êtes donc jamais laissé seul.");
q('infosenior', 'questions_de', 4, 1, null, 'Ein nationaler Informations- und Mediationsdienst, der Sie orientieren und bei der Suche nach einer Lösung helfen kann');
q('infosenior', 'questions_de', 4, 'explanation', null, 'Neben der Webseite und dem Register können Sie das Senioren-Telefon (247-86000) für Information und Beratung anrufen, und SIMPA, der nationale Informations- und Mediationsdienst für ältere Menschen, kann Sie orientieren und helfen, eine Meinungsverschiedenheit mit einem Dienst zu lösen – so werden Sie nie allein gelassen.');

// 12 Greater Region Q3 (who is in the House) and Q5 (UniGR)
q('granderegion', 'questions', 2, 'explanation', 'the representation of Rhineland-Palatinate and the Espace Culturel.', 'the representation of Rhineland-Palatinate, EuRegio SaarLorLux+, QuattroPole and the Institut de la Grande Région.');
q('granderegion', 'questions_fr', 2, 'explanation', "la représentation de la Rhénanie-Palatinat et l'Espace Culturel.", "la représentation de la Rhénanie-Palatinat, EuRegio SaarLorLux+, QuattroPole et l'Institut de la Grande Région.");
q('granderegion', 'questions_de', 2, 'explanation', 'die Vertretung von Rheinland-Pfalz und den Espace Culturel beherbergt.', 'die Vertretung von Rheinland-Pfalz, EuRegio SaarLorLux+, QuattroPole und das Institut der Großregion beherbergt.');
q('granderegion', 'questions', 4, 'explanation', 'links six universities', 'links seven universities');
q('granderegion', 'questions_fr', 4, 'explanation', 'relie six universités', 'relie sept universités');
q('granderegion', 'questions_de', 4, 'explanation', 'verbindet sechs Universitäten', 'verbindet sieben Universitäten');

// 13 ADEM Q5: Youth Guarantee age
q('adem', 'questions', 4, 'explanation', 'aged 15 to 30', 'aged 16 to 30');
q('adem', 'questions_fr', 4, 'explanation', 'de 15 à 30 ans', 'de 16 à 30 ans');
q('adem', 'questions_de', 4, 'explanation', 'zwischen 15 und 30 Jahren', 'zwischen 16 und 30 Jahren');

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
