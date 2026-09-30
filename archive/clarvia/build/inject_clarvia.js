// Append episode 42: Clarvia (bereavement guidance service).
const fs = require('fs');
const PROJ = '/sessions/gifted-practical-wozniak/mnt/Podcast myguichet';
const TMP = '/tmp';
const key = 'clarvia', id = 42;

let s = fs.readFileSync(PROJ + '/episodes_data.js', 'utf8');
const marker = s.indexOf('const EPISODES');
eval(s.replace('const EPISODES', 'var EPISODES'));
if (EPISODES.find(e => e.key === key)) throw new Error(key + ' already present');

const c = JSON.parse(fs.readFileSync(PROJ + '/build/clarvia_content.json', 'utf8'))[key];
const f = JSON.parse(fs.readFileSync(PROJ + '/build/clarvia_tr_fr.json', 'utf8'));
const d = JSON.parse(fs.readFileSync(PROJ + '/build/clarvia_tr_de.json', 'utf8'));
const l = JSON.parse(fs.readFileSync(PROJ + '/build/clarvia_tr_lb.json', 'utf8'));
const fc = f[key] || f, dc = d[key] || d, lc = l[key] || l;

const sd = JSON.parse(fs.readFileSync(TMP + '/clarvia_seg/segdata_fixed.json', 'utf8'));
const sdfr = JSON.parse(fs.readFileSync(TMP + '/clarvia_fr_seg/segdata_fixed.json', 'utf8'));
const sdde = JSON.parse(fs.readFileSync(TMP + '/clarvia_de_seg/segdata_fixed.json', 'utf8'));
const lb = JSON.parse(fs.readFileSync(TMP + '/clarvia_lb_segments.json', 'utf8'));

EPISODES.push({
  id: id, key: key, number: 'Episode ' + id,
  title: c.title, description: c.description,
  audio: 'podcast_' + key + '.mp3', duration: sd.duration,
  topics: c.topics, segments: sd.segments, questions: c.questions,
  categories: c.categories,
  title_fr: fc.title, description_fr: fc.description, topics_fr: fc.topics, questions_fr: fc.questions,
  title_de: dc.title, description_de: dc.description, topics_de: dc.topics, questions_de: dc.questions,
  title_lb: lc.title, description_lb: lc.description, topics_lb: lc.topics, questions_lb: lc.questions,
  audio_fr: 'podcast_' + key + '_fr.mp3', duration_fr: sdfr.duration, segments_fr: sdfr.segments,
  audio_de: 'podcast_' + key + '_de.mp3', duration_de: sdde.duration, segments_de: sdde.segments,
  segments_lb: lb
});

const banner = s.slice(0, marker).trimEnd();
fs.writeFileSync(PROJ + '/episodes_data.js', (banner ? banner + '\n' : '') + 'const EPISODES = ' + JSON.stringify(EPISODES, null, 1) + ';\n');

const e = EPISODES[EPISODES.length - 1];
console.log('episodes:', EPISODES.length, '| added', e.id, e.key, '| dur', e.duration, '/', e.duration_fr, '/', e.duration_de,
  '| seg EN', e.segments.length, 'FR', e.segments_fr.length, 'DE', e.segments_de.length, 'LB', e.segments_lb.length,
  '| cats', JSON.stringify(e.categories),
  '| qOK', ['questions_fr', 'questions_de', 'questions_lb'].every(k => e[k].length === 5 && e[k].every((q, i) => q.correct === e.questions[i].correct)));
