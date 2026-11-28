// Marks episodes as "waiting for validation" (field pending: true in episodes_data.js).
// A pending episode is NOT on the public list: the server leaves it out of /episodes_data.js until
// Jacques validates it in the admin space (/admin/ → Validation). Its review page keeps working.
//   node build/mark_pending.js inll,nationalite        → mark as pending
//   node build/mark_pending.js inll --off              → remove the flag (episode always public)
// finish_episode.py --new calls this automatically for every new episode.
// Run from the project root.
'use strict';
const fs = require('fs');
const src = fs.readFileSync('episodes_data.js', 'utf8');
const marker = src.indexOf('const EPISODES');
const banner = src.slice(0, marker);
const EPISODES = new Function(src.slice(marker) + '\nreturn EPISODES;')();
const serialize = E => banner + 'const EPISODES = ' + JSON.stringify(E, null, 1) + ';\n';
if (serialize(EPISODES) !== src) { console.error('episodes_data.js does not round-trip exactly — aborting.'); process.exit(1); }

const keys = String(process.argv[2] || '').split(',').map(s => s.trim()).filter(Boolean);
const off = process.argv.includes('--off');
if (!keys.length) { console.error('usage: node build/mark_pending.js key1,key2 [--off]'); process.exit(1); }
let changed = 0;
for (const k of keys) {
  const e = EPISODES.find(x => x.key === k);
  if (!e) { console.error('unknown key: ' + k); process.exit(1); }
  if (off) { if (e.pending) { delete e.pending; changed++; } }
  else if (!e.pending) {
    // put the flag right after "number" so it is easy to see in the file
    const out = {};
    for (const [f, v] of Object.entries(e)) { out[f] = v; if (f === 'number') out.pending = true; }
    if (!('pending' in out)) out.pending = true;
    Object.keys(e).forEach(f => delete e[f]); Object.assign(e, out); changed++;
  }
  console.log((off ? 'public (no validation needed): ' : 'waiting for validation: ') + e.number + ' ' + k);
}
if (changed) fs.writeFileSync('episodes_data.js', serialize(EPISODES));
