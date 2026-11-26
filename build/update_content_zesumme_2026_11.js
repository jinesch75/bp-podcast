#!/usr/bin/env node
// Zesumme Vereinfachen, partner feedback (26 Nov 2026): description, topics and quiz follow the new script
// (less digital focus; examples Guichet.lu on tour + 4th water management plan). EN/FR/DE.
// Also updates the Q5 wrong answers in build/quiz_distractors/batch3.json so apply_quiz_distractors.js keeps them.
// Idempotent. Run from the project root:  node build/update_content_zesumme_2026_11.js
const fs = require('fs');
const src = fs.readFileSync('episodes_data.js', 'utf8');
const marker = src.indexOf('const EPISODES');
const banner = src.slice(0, marker).trim();
const EPISODES = new Function(src.slice(marker) + '\nreturn EPISODES;')();
const serialize = E => (banner ? banner + '\n' : '') + 'const EPISODES = ' + JSON.stringify(E, null, 1) + ';\n';
if (serialize(EPISODES) !== src) throw new Error('episodes_data.js does not round-trip — aborting');
const ep = EPISODES.find(e => e.key === 'zesumme');

const C = {
  '': {
    description: "What the 'Zesumme Vereinfachen' platform is, and why it is about administrative steps in general, not only digital ones: how citizens and businesses can submit ideas and take part — online, on paper or in person — in one or several phases, who runs it (the Ministry for Digitalisation), and two real examples: the Guichet.lu on tour bus and the 4th water management plan.",
    topics: ['What Zesumme Vereinfachen is', 'Administrative steps in general', 'Run by the Ministry for Digitalisation',
      'Submit ideas, join one phase or many', 'Online, on paper or in person', 'Example: the Guichet.lu bus',
      'Example: the water management plan', 'Everyday democracy'],
    q1exp: ['is an online platform', 'is a participation platform'],
    q5: {
      text: 'What came out of the public consultation on local reception desks?',
      right: 'Guichet.lu on tour, a bus that brings help with procedures to the regions',
      wrong: ['A new mobile app that replaces all the reception desks in the country',
        'A phone line that answers questions about procedures at night and on weekends',
        'A rule that every commune must open its own Guichet.lu office by law'],
      explanation: 'Nearly eight thousand people took part — online, on paper, in workshops and at stands. The results showed that public services should be closer to people, especially to those who find it hard to do their procedures online. The answer was Guichet.lu on tour: a fully electric bus, fitted out like a reception desk, that travels to the regions of the country.'
    }
  },
  _fr: {
    description: "Ce qu'est la plateforme « Zesumme Vereinfachen », et pourquoi elle concerne les démarches administratives en général, pas seulement le numérique : comment les citoyens et les entreprises peuvent soumettre des idées et participer — en ligne, sur papier ou en personne — à une ou plusieurs phases, qui la gère (le Ministère de la Digitalisation), et deux exemples concrets : le bus Guichet.lu on tour et le 4e plan de gestion de l'eau.",
    topics: ["Ce qu'est Zesumme Vereinfachen", 'Les démarches administratives en général', 'Géré par le Ministère de la Digitalisation',
      'Soumettre des idées, participer à une phase ou plusieurs', 'En ligne, sur papier ou en personne', 'Exemple : le bus de Guichet.lu',
      "Exemple : le plan de gestion de l'eau", 'La démocratie au quotidien'],
    q1exp: ['est une plateforme en ligne', 'est une plateforme participative'],
    q5: {
      text: "Qu'est-ce qui est sorti de la consultation publique sur les guichets de proximité ?",
      right: "Guichet.lu on tour, un bus qui apporte de l'aide pour les démarches dans les régions",
      wrong: ['Une nouvelle application mobile qui remplace tous les guichets d\'accueil du pays',
        'Une ligne téléphonique qui répond aux questions sur les démarches la nuit et le week-end',
        'Une règle qui oblige chaque commune à ouvrir son propre bureau Guichet.lu'],
      explanation: "Près de huit mille personnes ont participé — en ligne, sur papier, lors d'ateliers et à des stands. Les résultats ont montré que les services publics doivent être plus proches des gens, surtout de ceux qui ont du mal à faire leurs démarches en ligne. La réponse : Guichet.lu on tour, un bus cent pour cent électrique, aménagé comme un guichet d'accueil, qui se déplace dans les régions du pays."
    }
  },
  _de: {
    description: 'Was die Plattform „Zesumme Vereinfachen“ ist und warum es um Verwaltungsschritte im Allgemeinen geht, nicht nur um digitale: wie Bürgerinnen, Bürger und Unternehmen Ideen einreichen und mitmachen können – online, auf Papier oder persönlich – in einer oder mehreren Phasen, wer sie betreibt (das Ministerium für Digitalisierung), und zwei konkrete Beispiele: der Bus Guichet.lu on tour und der 4. Wasserbewirtschaftungsplan.',
    topics: ['Was Zesumme Vereinfachen ist', 'Verwaltungsschritte im Allgemeinen', 'Betrieben vom Ministerium für Digitalisierung',
      'Ideen einreichen, an einer oder mehreren Phasen teilnehmen', 'Online, auf Papier oder persönlich', 'Beispiel: der Bus von Guichet.lu',
      'Beispiel: der Wasserbewirtschaftungsplan', 'Demokratie im Alltag'],
    q1exp: ['ist eine Online-Plattform', 'ist eine Beteiligungsplattform'],
    q5: {
      text: 'Was ist aus der öffentlichen Konsultation zu Schaltern in der Nähe entstanden?',
      right: 'Guichet.lu on tour, ein Bus, der Hilfe bei Verfahren in die Regionen bringt',
      wrong: ['Eine neue mobile App, die alle Empfangsschalter im Land ersetzt',
        'Eine Telefonhotline, die nachts und am Wochenende Fragen zu Verfahren beantwortet',
        'Eine Regel, nach der jede Gemeinde ein eigenes Guichet.lu-Büro eröffnen muss'],
      explanation: 'Fast achttausend Menschen haben mitgemacht – online, auf Papier, in Workshops und an Ständen. Die Ergebnisse zeigten, dass die öffentlichen Dienste näher bei den Menschen sein sollen, vor allem bei denen, denen es schwerfällt, ihre Verfahren online zu erledigen. Die Antwort: Guichet.lu on tour, ein vollelektrischer Bus, eingerichtet wie ein Empfangsschalter, der in die Regionen des Landes fährt.'
    }
  }
};

for (const [sfx, c] of Object.entries(C)) {
  ep['description' + sfx] = c.description;
  if (c.topics.length !== 8) throw new Error('need 8 topics');
  ep['topics' + sfx] = c.topics;
  const qs = ep['questions' + sfx];
  qs[0].explanation = qs[0].explanation.replace(c.q1exp[0], c.q1exp[1]);
  const q = qs[4];
  const pos = q.correct; // keep the answer position (balance_quiz_answers.js may move it)
  let w = 0;
  q.text = c.q5.text;
  q.options = q.options.map((_, k) => (k === pos ? c.q5.right : c.q5.wrong[w++]));
  q.explanation = c.q5.explanation;
}
fs.writeFileSync('episodes_data.js', serialize(EPISODES));

const dp = 'build/quiz_distractors/batch3.json';
const d = JSON.parse(fs.readFileSync(dp, 'utf8'));
for (const [sfx, lang] of [['', 'en'], ['_fr', 'fr'], ['_de', 'de']]) d.zesumme[4][lang] = C[sfx].q5.wrong;
fs.writeFileSync(dp, JSON.stringify(d, null, 1));
console.log('zesumme: description, topics, Q1 explanation and Q5 updated (EN/FR/DE); distractors file updated');
