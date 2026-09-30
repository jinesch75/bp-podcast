#!/usr/bin/env node
// Mark episodes as not yet finalised (the site shows an "In progress" badge + notice), or clear it.
//   node build/set_status.js in_progress <from-id>-<to-id> | <key,key,...>
//   node build/set_status.js final <from-id>-<to-id> | <key,key,...>
const fs = require('fs'), path = require('path');
const [status, which] = process.argv.slice(2);
if (!['in_progress', 'final'].includes(status) || !which) { console.log('usage: node build/set_status.js in_progress|final 14-42 | key,key'); process.exit(1); }
const DATA = path.join(process.cwd(), 'episodes_data.js');
const src = fs.readFileSync(DATA, 'utf8'); const i = src.indexOf('const EPISODES'); const banner = src.slice(0, i);
const E = new Function(src + '\nreturn EPISODES;')();
const ser = d => banner + 'const EPISODES = ' + JSON.stringify(d, null, 1) + ';\n';
if (ser(E) !== src) { console.error('round-trip check failed'); process.exit(1); }
const m = which.match(/^(\d+)-(\d+)$/);
const pick = m ? E.filter(e => e.id >= +m[1] && e.id <= +m[2]) : E.filter(e => which.split(',').includes(e.key));
pick.forEach(e => { if (status === 'final') delete e.status; else e.status = 'in_progress'; });
fs.writeFileSync(DATA, ser(E));
console.log(`${status}: ${pick.map(e => e.id + ':' + e.key).join(', ')}`);
