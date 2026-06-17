// Append the Observatoire de l'Habitat episode (id 17, key 'lll') to episodes_data.js.
const fs = require('fs');
const PROJ = '/sessions/keen-inspiring-planck/mnt/Podcast myguichet';
const TMP = '/tmp';
const OUT = '/sessions/keen-inspiring-planck/mnt/outputs';

let s = fs.readFileSync(PROJ + '/episodes_data.js', 'utf8');
const marker = s.indexOf('const EPISODES');
eval(s.replace('const EPISODES', 'var EPISODES'));

if (EPISODES.find(function (e) { return e.key === 'lll'; })) throw new Error('lll already present');

const c = JSON.parse(fs.readFileSync(OUT + '/lll_content.json', 'utf8'));
const en = JSON.parse(fs.readFileSync(TMP + '/lll_seg/segdata_fixed.json', 'utf8'));
const fr = JSON.parse(fs.readFileSync(TMP + '/lll_fr_seg/segdata_fixed.json', 'utf8'));
const de = JSON.parse(fs.readFileSync(TMP + '/lll_de_seg/segdata_fixed.json', 'utf8'));
const lb = JSON.parse(fs.readFileSync(TMP + '/lll_lb_segments.json', 'utf8'));

const ep = {
  id: 40,
  key: 'lll',
  number: 'Episode 40',
  title: c.en.title,
  description: c.en.description,
  audio: 'podcast_lll.mp3',
  duration: en.duration,
  topics: c.en.topics,
  segments: en.segments,
  questions: c.en.questions,
  categories: ['work'],
  title_fr: c.fr.title, description_fr: c.fr.description, topics_fr: c.fr.topics, questions_fr: c.fr.questions,
  title_de: c.de.title, description_de: c.de.description, topics_de: c.de.topics, questions_de: c.de.questions,
  audio_fr: 'podcast_lll_fr.mp3', duration_fr: fr.duration, segments_fr: fr.segments,
  audio_de: 'podcast_lll_de.mp3', duration_de: de.duration, segments_de: de.segments,
  segments_lb: lb
};

EPISODES.push(ep);

const banner = s.slice(0, marker).trimEnd();
const body = 'const EPISODES = ' + JSON.stringify(EPISODES, null, 1) + ';\n';
fs.writeFileSync(PROJ + '/episodes_data.js', (banner ? banner + '\n' : '') + body);

console.log('episodes now:', EPISODES.length);
console.log('lll:', 'dur', ep.duration, '| segEN', ep.segments.length, 'FR', ep.segments_fr.length, 'DE', ep.segments_de.length, 'LB', ep.segments_lb.length,
  '| topics', ep.topics.length, 'qFR', ep.questions_fr.length, 'qDE', ep.questions_de.length, '| cats', JSON.stringify(ep.categories));
