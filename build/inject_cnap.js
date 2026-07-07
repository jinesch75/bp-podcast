const fs = require('fs');
const PROJ = '/sessions/keen-practical-euler/mnt/Podcast myguichet';
let s = fs.readFileSync(PROJ + '/episodes_data.js', 'utf8');
const marker = s.indexOf('const EPISODES');
eval(s.replace('const EPISODES', 'var EPISODES'));
if (EPISODES.find(e => e.key === 'cnap')) throw new Error('cnap already present');

const c = JSON.parse(fs.readFileSync('/tmp/cnap_content.json', 'utf8'));
const en = JSON.parse(fs.readFileSync('/tmp/cnap_seg/segdata_fixed.json', 'utf8'));
const fr = JSON.parse(fs.readFileSync('/tmp/cnap_fr_seg/segdata_fixed.json', 'utf8'));
const de = JSON.parse(fs.readFileSync('/tmp/cnap_de_seg/segdata_fixed.json', 'utf8'));
const lb = JSON.parse(fs.readFileSync('/tmp/cnap_lb_segments.json', 'utf8'));

const ep = {
  id: 41, key: 'cnap', number: 'Episode 41',
  title: c.en.title, description: c.en.description,
  audio: 'podcast_cnap.mp3', duration: en.duration,
  topics: c.en.topics, segments: en.segments, questions: c.en.questions,
  categories: ['seniors', 'social', 'crossborder'],
  title_fr: c.fr.title, description_fr: c.fr.description, topics_fr: c.fr.topics, questions_fr: c.fr.questions,
  title_de: c.de.title, description_de: c.de.description, topics_de: c.de.topics, questions_de: c.de.questions,
  audio_fr: 'podcast_cnap_fr.mp3', duration_fr: fr.duration, segments_fr: fr.segments,
  audio_de: 'podcast_cnap_de.mp3', duration_de: de.duration, segments_de: de.segments,
  segments_lb: lb
};
EPISODES.push(ep);
const banner = s.slice(0, marker).trimEnd();
fs.writeFileSync(PROJ + '/episodes_data.js', (banner ? banner + '\n' : '') + 'const EPISODES = ' + JSON.stringify(EPISODES, null, 1) + ';\n');
console.log('episodes now:', EPISODES.length);
console.log('cnap dur', ep.duration, '| segEN', ep.segments.length, 'FR', ep.segments_fr.length, 'DE', ep.segments_de.length, 'LB', ep.segments_lb.length);
