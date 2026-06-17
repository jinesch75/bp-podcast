// Append 5 episodes (snj=19, enfance=20, cepas=21, fondseuropeens=22, zesumme=23).
const fs = require('fs');
const PROJ = '/sessions/keen-inspiring-planck/mnt/Podcast myguichet';
const TMP = '/tmp';
const OUT = '/sessions/keen-inspiring-planck/mnt/outputs';

let s = fs.readFileSync(PROJ + '/episodes_data.js', 'utf8');
const marker = s.indexOf('const EPISODES');
eval(s.replace('const EPISODES', 'var EPISODES'));

const en = JSON.parse(fs.readFileSync(OUT + '/new_content3_en.json', 'utf8'));
const frT = JSON.parse(fs.readFileSync(OUT + '/tr3_fr.json', 'utf8'));
const deT = JSON.parse(fs.readFileSync(OUT + '/tr3_de.json', 'utf8'));

const ORDER = [['amenagement',30],['aaa',31],['geoportail',32],['govcert',33],['culture',34],['demenz',35],['ess',36],['luxinnovation',37],['logement',38],['space',39]];

ORDER.forEach(function (pair) {
  const key = pair[0], id = pair[1];
  if (EPISODES.find(function (e) { return e.key === key; })) throw new Error(key + ' already present');
  const sd = JSON.parse(fs.readFileSync(TMP + '/' + key + '_seg/segdata_fixed.json', 'utf8'));
  const sdfr = JSON.parse(fs.readFileSync(TMP + '/' + key + '_fr_seg/segdata_fixed.json', 'utf8'));
  const sdde = JSON.parse(fs.readFileSync(TMP + '/' + key + '_de_seg/segdata_fixed.json', 'utf8'));
  const lb = JSON.parse(fs.readFileSync(TMP + '/' + key + '_lb_segments.json', 'utf8'));
  const c = en[key], f = frT[key], d = deT[key];

  EPISODES.push({
    id: id, key: key, number: 'Episode ' + id,
    title: c.title, description: c.description,
    audio: 'podcast_' + key + '.mp3', duration: sd.duration,
    topics: c.topics, segments: sd.segments, questions: c.questions,
    categories: c.categories,
    title_fr: f.title, description_fr: f.description, topics_fr: f.topics, questions_fr: f.questions,
    title_de: d.title, description_de: d.description, topics_de: d.topics, questions_de: d.questions,
    audio_fr: 'podcast_' + key + '_fr.mp3', duration_fr: sdfr.duration, segments_fr: sdfr.segments,
    audio_de: 'podcast_' + key + '_de.mp3', duration_de: sdde.duration, segments_de: sdde.segments,
    segments_lb: lb
  });
});

const banner = s.slice(0, marker).trimEnd();
fs.writeFileSync(PROJ + '/episodes_data.js', (banner ? banner + '\n' : '') + 'const EPISODES = ' + JSON.stringify(EPISODES, null, 1) + ';\n');

console.log('episodes now:', EPISODES.length);
ORDER.forEach(function (pair) {
  const e = EPISODES.find(function (x) { return x.key === pair[0]; });
  console.log(e.id, e.key, '| dur', e.duration, '| segEN', e.segments.length, 'FR', e.segments_fr.length, 'DE', e.segments_de.length, 'LB', e.segments_lb.length,
    '| qFR', e.questions_fr.length, 'qDE', e.questions_de.length, '| cats', JSON.stringify(e.categories),
    '| qOK', e.questions_fr.every(function (q, i) { return q.correct === e.questions[i].correct; }) && e.questions_de.every(function (q, i) { return q.correct === e.questions[i].correct; }));
});
