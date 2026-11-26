#!/usr/bin/env node
// Temporary access password for the site (see "Access password" in app.js and BUILD_GUIDE.md).
//   node build/set_password.js "the password"   -> the site asks for this password
//   node build/set_password.js --off            -> the site is open again
// Only a SHA-256 fingerprint is written to app.js (the repository is public: never write the password
// itself into a file). Afterwards the asset version is bumped; then commit and push.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const arg = process.argv[2];
if (!arg) { console.error('usage: node build/set_password.js "<password>"   |   --off'); process.exit(1); }
const file = path.join(__dirname, '..', 'app.js');
let js = fs.readFileSync(file, 'utf8');
const re = /const ACCESS_HASH = '[0-9a-f]*';/;
if (!re.test(js)) { console.error('ACCESS_HASH line not found in app.js — nothing written'); process.exit(1); }
const off = arg === '--off';
const pw = String(arg).trim();
if (!off && pw.length < 8) { console.error('Please use at least 8 characters.'); process.exit(1); }
const hash = off ? '' : crypto.createHash('sha256').update('bp-podcast-access:' + pw, 'utf8').digest('hex');
fs.writeFileSync(file, js.replace(re, "const ACCESS_HASH = '" + hash + "';"));
console.log(off ? 'Password removed: the site is open.' : 'Password set: the site now asks for it.');
require('child_process').execFileSync('node', [path.join(__dirname, 'bump_version.js')], { stdio: 'inherit' });
