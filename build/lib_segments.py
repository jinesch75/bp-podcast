#!/usr/bin/env python3
"""Helpers for building translated TURN-level segments aligned to the English audio.

- turns_of(md_path): parse a script .md into [(speaker, text)] (handles FR `**ANNA :**` and DE/LB `**ANNA:**`).
- run_starts(segs): from EN sentence-level segments, list (speaker, start_t) for each consecutive same-speaker run.
- build_turns(en_segments, turns): map each translated turn onto the start time of the matching run.
  Handles the rare same-speaker-twice case (reuses previous run start). Returns [{speaker,text,t}].

Used to fill segments_fr / segments_de / segments_lb from podcast_script_<key>_<lang>.md.
"""
import re


def turns_of(md_path):
    out = []
    for line in open(md_path):
        m = re.match(r'\*\*(ANNA|TOM)\s*:\*\*\s*(.*)', line.strip())
        if m:
            out.append(("Anna" if m.group(1) == "ANNA" else "Tom", m.group(2).strip()))
    return out


def run_starts(segs):
    runs = []
    last = None
    for sg in segs:
        if sg["speaker"] != last:
            runs.append((sg["speaker"], sg["t"]))
            last = sg["speaker"]
    return runs


def build_turns(en_segments, turns):
    runs = run_starts(en_segments)
    times = []
    ri = 0
    for spk, _ in turns:
        if ri < len(runs) and runs[ri][0] == spk:
            times.append(runs[ri][1]); ri += 1
        elif ri - 1 >= 0 and runs[ri - 1][0] == spk:
            times.append(runs[ri - 1][1])
        elif ri < len(runs):
            times.append(runs[ri][1]); ri += 1
        else:
            times.append(times[-1] if times else 0.0)
    for i in range(1, len(times)):
        if times[i] < times[i - 1]:
            times[i] = times[i - 1]
    return [{"speaker": sp, "text": tx, "t": round(t, 2)} for (sp, tx), t in zip(turns, times)]
