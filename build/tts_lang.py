#!/usr/bin/env python3
"""Resumable per-sentence TTS generator for TRANSLATED Biergerpakt episodes.

Usage:  python3 build/tts_lang.py <key> <lang>   (lang = fr | de)
Reads:  <project>/podcast_script_<key>_<lang>.md   (run from project root, or SCRIPT_DIR env)
Writes: /tmp/<key>_<lang>_seg/seg_####.mp3 + meta.json   (resumable; re-run until "ALL SEGMENTS DONE")

Voices:
  fr: Anna=fr-FR-DeniseNeural, Tom=fr-FR-HenriNeural
  de: Anna=de-DE-KatjaNeural,  Tom=de-DE-ConradNeural
Rate -6%. Then assemble with build/rebuild.py (PCM concat, sample-accurate).
"""
import re, subprocess, os, json, sys

KEY = sys.argv[1]
LANG = sys.argv[2]
SCRIPT_DIR = os.environ.get("SCRIPT_DIR", os.getcwd())
SRC = os.path.join(SCRIPT_DIR, f"podcast_script_{KEY}_{LANG}.md")
WORK = f"/tmp/{KEY}_{LANG}_seg"
os.makedirs(WORK, exist_ok=True)

VOICES = {
    "fr": {"Anna": "fr-FR-DeniseNeural", "Tom": "fr-FR-HenriNeural"},
    "de": {"Anna": "de-DE-KatjaNeural",  "Tom": "de-DE-ConradNeural"},
}
VOICE = VOICES[LANG]
RATE = "-6%"

turns = []
for line in open(SRC):
    m = re.match(r'\*\*(ANNA|TOM)\s*:\*\*\s*(.*)', line.strip())
    if m:
        spk = "Anna" if m.group(1) == "ANNA" else "Tom"
        txt = m.group(2).strip()
        if txt:
            turns.append((spk, txt))

def split_sentences(t):
    t = t.replace("...", "<ELL>")
    parts = re.split(r'(?<=[.!?])\s+', t)
    return [p.replace("<ELL>", "...").strip() for p in parts if p.strip()]

segments = []
for spk, txt in turns:
    for s in split_sentences(txt):
        segments.append((spk, s))
print("turns", len(turns), "sentences", len(segments))

env = os.environ.copy()
env["PATH"] = env["PATH"] + ":" + os.path.expanduser("~/.local/bin") + ":/root/.local/bin"

meta = []
for i, (spk, txt) in enumerate(segments):
    fn = f"{WORK}/seg_{i:04d}.mp3"
    if not (os.path.exists(fn) and os.path.getsize(fn) > 500):
        for _ in range(6):
            subprocess.run(["edge-tts", "--voice", VOICE[spk], f"--rate={RATE}",
                            "--text", txt.replace("**", ""), "--write-media", fn],
                           capture_output=True, text=True, env=env)
            if os.path.exists(fn) and os.path.getsize(fn) > 500:
                break
    if not (os.path.exists(fn) and os.path.getsize(fn) > 500):
        print("FAILED", i, txt[:40]); raise SystemExit(1)
    meta.append({"speaker": spk, "text": txt})
    if i % 25 == 0:
        print("done", i)
json.dump({"meta": meta, "n": len(segments)}, open(WORK + "/meta.json", "w"), ensure_ascii=False)
print("ALL SEGMENTS DONE", len(segments))
