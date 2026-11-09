#!/usr/bin/env python3
"""Show the turns of podcast_script_<key>[_fr|_de|_lb].md whose EN text contains any of the given phrases.
Usage: python3 build/show_turns.py <key> "phrase" ["phrase" ...]  (prints turn index, speaker, text per language)"""
import re, sys
key = sys.argv[1]; pats = sys.argv[2:]
def turns(path):
    return [(m.group(1), m.group(2)) for l in open(path, encoding="utf-8").read().split("\n")
            for m in [re.match(r"\*\*(ANNA|TOM)\s?:\*\*\s?(.*)", l)] if m]
en = turns(f"podcast_script_{key}.md")
idx = [k for k, (sp, t) in enumerate(en) if any(p in t for p in pats)]
for L in ["", "_fr", "_de", "_lb"]:
    t = turns(f"podcast_script_{key}{L}.md"); print("=====", L or "en", len(t))
    for k in idx: print(k, t[k][0], t[k][1])
