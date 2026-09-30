#!/usr/bin/env node
// Put episodes in a new order and renumber them (id + "Episode N"). Keys listed in FIRST come first,
// in that order; all other episodes follow in their current order. Nothing else is changed.
// node build/reorder_episodes.js [--write]
const fs = require('fs');
const FIRST = ['myguichet', 'luxtrust', 'benevolat', 'eltereforum', 'digitalinclusion', 'workinluxembourg',
               'dsp_cns', 'lualert', 'maison_orientation', 'infosenior', 'accessibilite', 'granderegion', 'adem'];
const src = fs.readFileSync('episodes_data.js', 'utf8');
const marker = src.indexOf('const EPISODES');
const banner = src.slice(0, marker).trim();
const EPISODES = new Function(src.slice(marker) + '\nreturn EPISODES;')();
const serialize = E => (banner ? banner + '\n' : '') + 'const EPISODES = ' + JSON.stringify(E, null, 1) + ';\n';
if (serialize(EPISODES) !== src) throw new Error('episodes_data.js does not round-trip — aborting');
for (const k of FIRST) if (!EPISODES.find(e => e.key === k)) throw new Error('unknown key ' + k);
const ordered = [...FIRST.map(k => EPISODES.find(e => e.key === k)), ...EPISODES.filter(e => !FIRST.includes(e.key))];
ordered.forEach((e, i) => { e.id = i + 1; e.number = 'Episode ' + (i + 1); });
console.log(ordered.map(e => e.id + ':' + e.key).join('  '));
if (process.argv.includes('--write')) { fs.writeFileSync('episodes_data.js', serialize(ordered)); console.log('episodes_data.js written'); }
