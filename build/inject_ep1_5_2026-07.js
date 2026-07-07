// Replace episodes 1-5 (new scripts July 2026): new audio/segments/content EN+FR+DE+LB,
// and swap order/ids: benevolat -> Episode 2, dsp_cns -> Episode 4.
const fs = require('fs');
const PROJ = '/sessions/gifted-practical-wozniak/mnt/Podcast myguichet';
const TMP = '/tmp';

let s = fs.readFileSync(PROJ + '/episodes_data.js', 'utf8');
const marker = s.indexOf('const EPISODES');
eval(s.replace('const EPISODES', 'var EPISODES'));

const en = JSON.parse(fs.readFileSync(PROJ + '/build/en_content_ep1_5_2026-07.json', 'utf8'));
const frT = JSON.parse(fs.readFileSync(PROJ + '/build/tr_new_fr.json', 'utf8'));
const deT = JSON.parse(fs.readFileSync(PROJ + '/build/tr_new_de.json', 'utf8'));
const lbT = JSON.parse(fs.readFileSync(PROJ + '/build/tr_new_lb.json', 'utf8'));

// New id/number per key (order swap 2<->4)
const NEWID = { myguichet: 1, benevolat: 2, eltereforum: 3, dsp_cns: 4, lualert: 5 };

Object.keys(NEWID).forEach(function (key) {
  const ep = EPISODES.find(function (e) { return e.key === key; });
  if (!ep) throw new Error(key + ' not found');
  const sd = JSON.parse(fs.readFileSync(TMP + '/' + key + '_seg/segdata_fixed.json', 'utf8'));
  const sdfr = JSON.parse(fs.readFileSync(TMP + '/' + key + '_fr_seg/segdata_fixed.json', 'utf8'));
  const sdde = JSON.parse(fs.readFileSync(TMP + '/' + key + '_de_seg/segdata_fixed.json', 'utf8'));
  const lb = JSON.parse(fs.readFileSync(TMP + '/' + key + '_lb_segments.json', 'utf8'));
  const c = en[key], f = frT[key], d = deT[key], l = lbT[key];

  ep.id = NEWID[key];
  ep.number = 'Episode ' + NEWID[key];
  ep.title = c.title; ep.description = c.description; ep.topics = c.topics; ep.questions = c.questions;
  ep.duration = sd.duration; ep.segments = sd.segments;
  ep.title_fr = f.title; ep.description_fr = f.description; ep.topics_fr = f.topics; ep.questions_fr = f.questions;
  ep.title_de = d.title; ep.description_de = d.description; ep.topics_de = d.topics; ep.questions_de = d.questions;
  ep.title_lb = l.title; ep.description_lb = l.description; ep.topics_lb = l.topics; ep.questions_lb = l.questions;
  ep.audio_fr = 'podcast_' + key + '_fr.mp3'; ep.duration_fr = sdfr.duration; ep.segments_fr = sdfr.segments;
  ep.audio_de = 'podcast_' + key + '_de.mp3'; ep.duration_de = sdde.duration; ep.segments_de = sdde.segments;
  ep.segments_lb = lb;
});

// Reorder array by id
EPISODES.sort(function (a, b) { return a.id - b.id; });

const banner = s.slice(0, marker).trimEnd();
fs.writeFileSync(PROJ + '/episodes_data.js', (banner ? banner + '\n' : '') + 'const EPISODES = ' + JSON.stringify(EPISODES, null, 1) + ';\n');

console.log('episodes:', EPISODES.length);
EPISODES.slice(0, 5).forEach(function (e) {
  console.log(e.id, e.key, '|', e.title.slice(0, 45), '| dur', e.duration, '/', e.duration_fr, '/', e.duration_de,
    '| seg EN', e.segments.length, 'FR', e.segments_fr.length, 'DE', e.segments_de.length, 'LB', e.segments_lb.length,
    '| lastT', e.segments[e.segments.length - 1].t.toFixed(1),
    '| qOK', ['questions_fr', 'questions_de', 'questions_lb'].every(function (k) {
      return e[k].length === 5 && e[k].every(function (q, i) { return q.correct === e.questions[i].correct; });
    }));
});
