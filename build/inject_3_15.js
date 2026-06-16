// Inject FR/DE audio + sentence segments + FR/DE content translations into episodes 3-15.
const fs = require('fs');
const PROJ = '/sessions/keen-inspiring-planck/mnt/Podcast myguichet';
const TMP = '/tmp';
const OUT = '/sessions/keen-inspiring-planck/mnt/outputs';

let s = fs.readFileSync(PROJ + '/episodes_data.js', 'utf8');
const marker = s.indexOf('const EPISODES');
eval(s.replace('const EPISODES', 'var EPISODES'));

const tr = JSON.parse(fs.readFileSync(OUT + '/lang_translations_3_15.json', 'utf8'));
const KEYS = Object.keys(tr); // the 13 episode keys

KEYS.forEach(function (key) {
  const ep = EPISODES.find(function (e) { return e.key === key; });
  if (!ep) throw new Error('no ep ' + key);

  ['fr', 'de'].forEach(function (lang) {
    const sd = JSON.parse(fs.readFileSync(TMP + '/' + key + '_' + lang + '_seg/segdata_fixed.json', 'utf8'));
    ep['audio_' + lang] = 'podcast_' + key + '_' + lang + '.mp3';
    ep['duration_' + lang] = sd.duration;
    ep['segments_' + lang] = sd.segments;  // sentence-level, synced to that language's audio

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
let bad = 0;
EPISODES.forEach(function (ep) {
  const need = ['audio_fr', 'audio_de', 'segments_fr', 'segments_de', 'title_fr', 'title_de', 'questions_fr', 'questions_de'];
  const miss = need.filter(function (k) { return !ep[k]; });
  if (miss.length) { bad++; console.log('EP', ep.id, ep.key, 'MISSING', miss.join(',')); }
});
console.log(bad === 0 ? 'ALL 15 EPISODES have FR+DE audio + segments + content' : bad + ' episodes incomplete');
