// Assign topic-category tags to every episode. Tags are category ids defined in app.js CATEGORIES.
const fs = require('fs');
const PROJ = '/sessions/keen-inspiring-planck/mnt/Podcast myguichet';

let s = fs.readFileSync(PROJ + '/episodes_data.js', 'utf8');
const marker = s.indexOf('const EPISODES');
eval(s.replace('const EPISODES', 'var EPISODES'));

const TAGS = {
  myguichet: ['digital'],
  dsp_cns: ['health', 'digital'],
  eltereforum: ['family'],
  benevolat: ['civic'],
  lualert: ['safety', 'digital'],
  luxtrust: ['digital'],
  maison_orientation: ['work', 'family'],
  infosenior: ['seniors', 'social'],
  accessibilite: ['inclusion', 'digital'],
  zukunftskeess: ['family', 'social'],
  fns: ['social'],
  granderegion: ['crossborder'],
  digitalinclusion: ['digital', 'inclusion'],
  onis: ['social', 'work'],
  workinluxembourg: ['work', 'crossborder']
};

EPISODES.forEach(function (ep) {
  ep.categories = TAGS[ep.key] || [];
});

const missing = EPISODES.filter(function (e) { return !e.categories.length; });
if (missing.length) throw new Error('untagged: ' + missing.map(function (e) { return e.key; }).join(','));

const banner = s.slice(0, marker).trimEnd();
const body = 'const EPISODES = ' + JSON.stringify(EPISODES, null, 1) + ';\n';
fs.writeFileSync(PROJ + '/episodes_data.js', (banner ? banner + '\n' : '') + body);
console.log('tagged ' + EPISODES.length + ' episodes');
EPISODES.forEach(function (e) { console.log('  ' + e.id + ':' + e.key + ' -> ' + e.categories.join(', ')); });
