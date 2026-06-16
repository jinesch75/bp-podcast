#!/usr/bin/env python3
"""Resumable batch TTS for many (key, lang) pairs within a wall-clock budget.

Usage:  python3 build/tts_batch.py            (run from project root; re-run until "ALL BATCHES DONE")
Edit KEYS below. Voices: fr=Denise/Henri, de=Katja/Conrad, rate -6%.
Writes /tmp/<key>_<lang>_seg/seg_####.mp3 + meta.json (same layout as tts_lang.py).
"""
import re, subprocess, os, json, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

KEYS = ["eltereforum", "benevolat", "lualert", "luxtrust", "maison_orientation",
        "infosenior", "accessibilite", "zukunftskeess", "fns", "granderegion",
        "digitalinclusion", "onis", "workinluxembourg"]
LANGS = ["fr", "de"]
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 40.0
if len(sys.argv) > 2:           # optional: restrict to comma-separated keys
    KEYS = sys.argv[2].split(",")

SCRIPT_DIR = os.getcwd()
VOICES = {
    "fr": {"Anna": "fr-FR-DeniseNeural", "Tom": "fr-FR-HenriNeural"},
    "de": {"Anna": "de-DE-KatjaNeural",  "Tom": "de-DE-ConradNeural"},
}
RATE = "-6%"
env = os.environ.copy()
env["PATH"] = env["PATH"] + ":" + os.path.expanduser("~/.local/bin") + ":/root/.local/bin"


def split_sentences(t):
    t = t.replace("...", "<ELL>")
    parts = re.split(r'(?<=[.!?])\s+', t)
    parts = [p.replace("<ELL>", "...").strip() for p in parts if p.strip()]
    # Merge any punctuation-only fragment (e.g. a lone « » ) into the previous sentence,
    # so edge-tts never gets a segment with no speakable text.
    merged = []
    for p in parts:
        if re.search(r'[0-9A-Za-zÀ-ÿ]', p):
            merged.append(p)
        elif merged:
            merged[-1] = merged[-1] + ' ' + p
        else:
            merged.append(p)
    return merged


def segments_for(key, lang):
    src = os.path.join(SCRIPT_DIR, "podcast_script_%s_%s.md" % (key, lang))
    turns = []
    for line in open(src):
        m = re.match(r'\*\*(ANNA|TOM)\s*:\*\*\s*(.*)', line.strip())
        if m:
            spk = "Anna" if m.group(1) == "ANNA" else "Tom"
            txt = m.group(2).strip()
            if txt:
                turns.append((spk, txt))
    segs = []
    for spk, txt in turns:
        for sentence in split_sentences(txt):
            segs.append((spk, sentence))
    return segs


start = time.time()
total_done = 0
total_all = 0
pending = []
for key in KEYS:
    for lang in LANGS:
        segs = segments_for(key, lang)
        work = "/tmp/%s_%s_seg" % (key, lang)
        os.makedirs(work, exist_ok=True)
        have = sum(1 for i in range(len(segs))
                   if os.path.exists("%s/seg_%04d.mp3" % (work, i)) and os.path.getsize("%s/seg_%04d.mp3" % (work, i)) > 500)
        total_done += have
        total_all += len(segs)
        if have < len(segs):
            pending.append((key, lang, segs, work))
        elif not os.path.exists(work + "/meta.json"):
            json.dump({"meta": [{"speaker": s, "text": t} for s, t in segs], "n": len(segs)},
                      open(work + "/meta.json", "w"), ensure_ascii=False)

WORKERS = 8

# Build a flat list of all missing (fn, voice, text) render tasks across all pending pairs.
tasks = []
for key, lang, segs, work in pending:
    voice = VOICES[lang]
    for i, (spk, txt) in enumerate(segs):
        fn = "%s/seg_%04d.mp3" % (work, i)
        if not (os.path.exists(fn) and os.path.getsize(fn) > 500):
            tasks.append((fn, voice[spk], txt.replace("**", "")))


def render(task):
    fn, v, txt = task
    for _ in range(6):
        subprocess.run(["edge-tts", "--voice", v, "--rate=" + RATE, "--text", txt, "--write-media", fn],
                       capture_output=True, text=True, env=env)
        if os.path.exists(fn) and os.path.getsize(fn) > 500:
            return (fn, True, txt)
        time.sleep(0.4)
    return (fn, False, txt)

failed = []
ex = ThreadPoolExecutor(max_workers=WORKERS)
inflight = set()
it = iter(tasks)
stop = False
while True:
    while len(inflight) < WORKERS * 2 and not stop:
        try:
            inflight.add(ex.submit(render, next(it)))
        except StopIteration:
            stop = True
    if not inflight:
        break
    done = next(as_completed(inflight))
    inflight.discard(done)
    fn, okk, txt = done.result()
    if okk:
        total_done += 1
    else:
        failed.append((fn, txt))
    if time.time() - start > BUDGET:
        break
ex.shutdown(wait=True, cancel_futures=True)

# Write meta.json for any pair now fully rendered.
for key, lang, segs, work in pending:
    if all(os.path.exists("%s/seg_%04d.mp3" % (work, i)) and os.path.getsize("%s/seg_%04d.mp3" % (work, i)) > 500
           for i in range(len(segs))):
        json.dump({"meta": [{"speaker": s, "text": t} for s, t in segs], "n": len(segs)},
                  open(work + "/meta.json", "w"), ensure_ascii=False)

if failed:
    for fn, txt in failed[:5]:
        print("FAILED", fn, repr(txt[:40]))
if total_done >= total_all:
    print("ALL BATCHES DONE %d/%d" % (total_done, total_all))
else:
    print("progress %d/%d sentences" % (total_done, total_all))
