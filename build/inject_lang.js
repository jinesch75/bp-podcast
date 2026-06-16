// Inject FR/DE audio + sentence segments + FR/DE/LB content translations into episodes 1-2.
const fs = require('fs');
const PROJ = '/sessions/keen-inspiring-planck/mnt/Podcast myguichet';
const TMP = '/tmp';
const OUT = '/sessions/keen-inspiring-planck/mnt/outputs';

let s = fs.readFileSync(PROJ + '/episodes_data.js', 'utf8');
const marker = s.indexOf('const EPISODES');
eval(s.replace('const EPISODES', 'var EPISODES'));

const tr = JSON.parse(fs.readFileSync(OUT + '/translations.json', 'utf8'));

const TARGETS = ['myguichet', 'dsp_cns'];
TARGETS.forEach(function (key) {
  const ep = EPISODES.find(function (e) { return e.key === key; });
  if (!ep) throw new Error('no ep ' + key);

  // Per-language audio + sentence-level segments from segdata_fixed.json
  ['fr', 'de'].forEach(function (lang) {
    const sd = JSON.parse(fs.readFileSync(TMP + '/' + key + '_' + lang + '_seg/segdata_fixed.json', 'utf8'));
    ep['audio_' + lang] = 'podcast_' + key + '_' + lang + '.mp3';
    ep['duration_' + lang] = sd.duration;
    ep['segments_' + lang] = sd.segments;  // sentence-level, synced to that language's audio
  });

  // Content translations (title / description / topics / questions) for fr/de/lb
  ['fr', 'de', 'lb'].forEach(function (lang) {
    const t = tr[key][lang];
    ep['title_' + lang] = t.title;
    ep['description_' + lang] = t.description;
    ep['topics_' + lang] = t.topics;
    ep['questions_' + lang] = t.questions;
  });
});

const banner = s.slice(0, marker).trimEnd();
const body = 'const EPISODES = ' + JSON.stringify(EPISODES, null, 1) + ';\n';
fs.writeFileSync(PROJ + '/episodes_data.js', (banner ? banner + '\n' : '') + body);

// Report
TARGETS.forEach(function (key) {
  const ep = EPISODES.find(function (e) { return e.key === key; });
  console.log(key,
    '| audio_fr', ep.audio_fr, ep.duration_fr,
    '| audio_de', ep.audio_de, ep.duration_de,
    '| segEN', ep.segments.length, 'segFR', ep.segments_fr.length, 'segDE', ep.segments_de.length, 'segLB', ep.segments_lb.length,
    '| qFR', ep.questions_fr.length, 'qLB', ep.questions_lb.length,
    '| title_lb', JSON.stringify(ep.title_lb).slice(0, 40));
});
