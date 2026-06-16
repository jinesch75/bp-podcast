#!/usr/bin/env python3
"""TEMPLATE: append (or replace) one episode in episodes_data.js with EN/FR/DE/LB segments + quiz.

Run from the PROJECT ROOT (the folder containing episodes_data.js).
Edit KEY, the topics list, and the 5 questions, then run.
Requires: /tmp/<KEY>_seg/segdata_fixed.json (from build/rebuild.py) and
          podcast_script_<KEY>_fr.md / _de.md / _lb.md in the project root.
"""
import json, shutil, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "build"))
from lib_segments import turns_of, build_turns

KEY = "REPLACE_ME"
TITLE = "Episode Title"
DESCRIPTION = "One-paragraph description."
TOPICS = ["t1","t2","t3","t4","t5","t6","t7","t8"]
QUESTIONS = [
  {"text":"Q1?","options":["A","B (correct)","C","D"],"correct":1,"explanation":"..."},
  # ...5 total...
]

fixed = json.load(open(f"/tmp/{KEY}_seg/segdata_fixed.json"))   # {duration, segments(EN sentence-level)}
fr = turns_of(f"podcast_script_{KEY}_fr.md")
de = turns_of(f"podcast_script_{KEY}_de.md")
lb = turns_of(f"podcast_script_{KEY}_lb.md")

s = open("episodes_data.js").read()
prefix = s[:s.index('[')]
arr = json.loads(s[s.index('['):s.rindex(']')+1])
arr = [e for e in arr if e.get("key") != KEY]            # replace if exists
nextid = max([e["id"] for e in arr], default=0) + 1
ep = {
  "id": nextid, "key": KEY, "number": f"Episode {nextid}",
  "title": TITLE, "description": DESCRIPTION,
  "audio": f"podcast_{KEY}.mp3", "duration": fixed["duration"],
  "topics": TOPICS,
  "segments": fixed["segments"],
  "segments_fr": build_turns(fixed["segments"], fr),
  "segments_de": build_turns(fixed["segments"], de),
  "segments_lb": build_turns(fixed["segments"], lb),
  "questions": QUESTIONS,
}
arr.append(ep)
open("episodes_data.js", "w").write(prefix + json.dumps(arr, ensure_ascii=False) + ";\n")
shutil.copy(f"/tmp/{KEY}_seg/podcast_{KEY}.mp3", f"podcast_{KEY}.mp3")
print("injected episode", nextid, KEY, "| episodes now", len(arr), "| duration", ep["duration"])
