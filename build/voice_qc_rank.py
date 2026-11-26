#!/usr/bin/env python3
"""Tighter pitch check on top of voice_qc.py (Zesumme Vereinfachen, 26 Nov 2026: Jacques heard Anna's
"And what did all those people tell the State?" as off — +3.3 robust z in pitch, below voice_qc's flag limit).

  python3 build/voice_qc_rank.py <key> <lang> [N] [--old episodes_data.<backup>.js]

Run after voice_qc.py, with the same EL_TMP. Ranks every sentence by its largest pitch deviation
(f0, spread, end-of-sentence movement; robust z per host) and prints the top N (default 15).
STD marks the standard intro/outro (first 6 / last 5 sentences). With --old, sentences whose text was
already in that data file are marked "old" (heard before), the others NEW.
Retake |zf0| >= ~2.5 with best_take.py; a very short line that stays off in every take gets joined to the
next sentence (colon / comma). Rising ends on yes/no questions are natural (esp. German)."""
import json, os, sys
import numpy as np

T = os.environ.get('EL_TMP', '/tmp')
args = [a for a in sys.argv[1:]]
old_file = None
if '--old' in args:
    i = args.index('--old'); old_file = args[i + 1]; del args[i:i + 2]
key, lang = args[0], args[1]
top = int(args[2]) if len(args) > 2 else 15
sfx = '' if lang == 'en' else '_' + lang
meta = json.load(open(f'{T}/{key}{sfx}_el_seg/meta.json'))['meta']
q = json.load(open(f'{T}/voice_qc_{key}_{lang}.json'))

old = set()
if old_file:
    src = open(old_file, encoding='utf-8').read()
    import subprocess
    js = ("const fs=require('fs');const s=fs.readFileSync(process.argv[1],'utf8');"
          "const E=new Function(s.slice(s.indexOf('const EPISODES'))+'\\nreturn EPISODES;')();"
          "const e=E.find(x=>x.key===process.argv[2]);"
          "console.log(JSON.stringify(e[process.argv[3]].map(x=>x.text.trim())))")
    seg = {'en': 'segments', 'fr': 'segments_fr', 'de': 'segments_de'}[lang]
    old = set(json.loads(subprocess.check_output(['node', '-e', js, old_file, key, seg])))

n = len(meta)
std = set(range(0, 6)) | set(range(n - 5, n))
for spk in ['Anna', 'Tom']:
    idx = [int(k) for k, v in q.items() if v['speaker'] == spk]
    for f in ['f0', 'spread', 'tail', 'rms']:
        a = np.array([q[str(i)][f] for i in idx]); med = np.median(a)
        mad = np.median(abs(a - med)) * 1.4826 or 1.0
        for i in idx:
            q[str(i)]['z_' + f] = (q[str(i)][f] - med) / mad
    print(spk, 'median f0 %.0f Hz' % np.median([q[str(i)]['f0'] for i in idx]))
rows = []
for k, v in q.items():
    i = int(k)
    score = max(abs(v['z_f0']), abs(v['z_spread']) * 0.8, abs(v['z_tail']) * 0.7)
    mark = ('old' if v['text'].strip() in old else 'NEW') if old_file else ''
    rows.append((score, i, v['speaker'], v['f0'], v['z_f0'], v['z_spread'], v['z_tail'], v['z_rms'],
                 mark, 'STD' if i in std else '', v['text'][:65]))
rows.sort(reverse=True)
print(len(q), '/', n, 'sentences measured')
for r in rows[:top]:
    print('%.1f #%d %s f0=%.0f zf0=%+.1f zsp=%+.1f ztail=%+.1f zrms=%+.1f %s %s %s' % r)
