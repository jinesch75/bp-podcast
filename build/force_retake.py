#!/usr/bin/env python3
"""Redo sentences that Jacques heard as wrong: the current take is NOT allowed to win.
python3 build/force_retake.py <key> <lang> <i,i,...> [seeds, default 1244,1245,1246]
(indices = sentence numbers from voice_qc.py; needs $EL_TMP/voice_qc_<key>_<lang>.json, like best_take.py)
For each sentence: new seeds are generated and measured like best_take.py (distance to the host's normal voice,
whisper must hear the right words, no cut-off end) plus a check for a long pause INSIDE the sentence (a sign of a
false start). The best NEW take is written to build/el_cache/reseed.json. Then run finish_episode.py <key> <lang> --reset
(the rebuild is 0 credits). Written 27 Nov 2026 (infohandicap FR)."""
import hashlib, importlib.util, json, os, re, sys
import numpy as np, librosa
spec = importlib.util.spec_from_file_location("el", os.path.join("build", "tts_elevenlabs.py"))
el = importlib.util.module_from_spec(spec); spec.loader.exec_module(el)
key, lang, idx = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")]
SEEDS = [int(x) for x in (sys.argv[4] if len(sys.argv) > 4 else "1244,1245,1246").split(",")]
qc = json.load(open(f"{os.environ.get('EL_TMP', '/tmp')}/voice_qc_{key}_{lang}.json"))
FIELDS = ("rate", "f0", "spread", "rms", "voiced")
prof = {}
for spk in ("Anna", "Tom"):
    rows = [v for v in qc.values() if v["speaker"] == spk]
    prof[spk] = {f: (np.median([r[f] for r in rows]), np.median(np.abs(np.array([r[f] for r in rows]) - np.median([r[f] for r in rows]))) * 1.4826 + 1e-6) for f in FIELDS}
def feats(p, text):
    y, sr = librosa.load(p, sr=16000); yt, _ = librosa.effects.trim(y, top_db=35); dur = len(yt) / sr
    f0, _, _ = librosa.pyin(yt, fmin=70, fmax=420, sr=sr, frame_length=1024); f = f0[~np.isnan(f0)]
    st = 12 * np.log2(f / np.median(f)) if len(f) > 5 else np.array([0.0])
    tail = st[-max(3, len(st) // 6):]
    return {"tail": float(np.mean(tail) - np.median(st)), "rate": len(re.sub(r"\W", "", text)) / max(dur, 0.1), "f0": float(np.median(f)) if len(f) else 0,
            "spread": float(np.std(st)), "rms": float(20 * np.log10(np.sqrt(np.mean(yt ** 2)) + 1e-9)), "voiced": len(f) / max(len(f0), 1)}
TAIL = {}
for spk in ("Anna", "Tom"):   # end-of-sentence melody of statements: a rising end sounds like a question
    a = np.array([v["tail"] for v in qc.values() if v["speaker"] == spk and v["text"].rstrip().endswith(".")])
    TAIL[spk] = (np.median(a), np.median(np.abs(a - np.median(a))) * 1.4826 + 1e-6)
def dist(fe, spk, statement=False):
    d = sum(((fe[f] - prof[spk][f][0]) / prof[spk][f][1]) ** 2 for f in FIELDS)
    if statement: d += max(0.0, (fe["tail"] - TAIL[spk][0]) / TAIL[spk][1]) ** 2
    return float(np.sqrt(d))
el.load_env(); api = os.environ["ELEVENLABS_API_KEY"].strip()
voices = json.loads(el.request("GET", "/voices", api))["voices"]
vids = {r: el.resolve_voice(r, lang, voices)[0] for r in ("Anna", "Tom")}
model = "eleven_multilingual_v2"
segs = []
for spk, txt in el.read_turns(key, lang):
    sents = el.merge_short(el.split_sentences(txt))
    for j, s in enumerate(sents):
        segs.append({"speaker": spk, "text": s, "prev": " ".join(sents[max(0, j - 2):j]), "next": sents[j + 1] if j + 1 < len(sents) else ""})
rpath = os.path.join(el.CACHE, "reseed.json"); reseed = json.load(open(rpath)) if os.path.exists(rpath) else {}
def hpath(spk, body): return hashlib.sha1(json.dumps([vids[spk], body], sort_keys=True).encode()).hexdigest()[:20] + ".mp3"

def max_gap(p):
    y, sr = librosa.load(p, sr=16000); iv = librosa.effects.split(y, top_db=35)
    gaps = [(iv[k + 1][0] - iv[k][1]) / sr for k in range(len(iv) - 1)]
    return max(gaps) if gaps else 0.0
credits = 0
for i in idx:
    s = segs[i]; spoken = el.spoken(s["text"], lang)
    body = {"text": spoken, "model_id": model, "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
    if s["prev"]: body["previous_text"] = el.spoken(s["prev"], lang)
    if s["next"]: body["next_text"] = el.spoken(s["next"], lang)
    base = hpath(s["speaker"], body); cur = reseed.get(base, base)
    rows = []
    for sd in [None] + SEEDS:
        c = cur if sd is None else hpath(s["speaker"], dict(body, seed=sd)); p = os.path.join(el.CACHE, c)
        if not os.path.exists(p):
            audio = el.request("POST", f"/text-to-speech/{vids[s['speaker']]}", api, dict(body, seed=sd), query="?output_format=mp3_44100_128")
            open(p + ".part", "wb").write(audio); os.replace(p + ".part", p); credits += len(spoken)
        heard = el.transcribe(p, lang, "small"); bad = el.asr_problem(spoken, heard); g = max_gap(p)
        d = dist(feats(p, spoken), s["speaker"], s["text"].rstrip().endswith(".")) + (100 if bad else 0) + (100 if el.is_cut(p) else 0) + (50 if g > 0.7 else 0)
        rows.append((d, c, sd, g, heard))
    for d, c, sd, g, heard in rows:
        print(f"#{i} {'current' if sd is None else 'seed ' + str(sd)}: dist {d:6.1f}  longest pause {g:.2f}s  heard: {heard[:90]}")
    d, c, sd, g, heard = min((r for r in rows if r[2] is not None and r[1] != cur), key=lambda r: r[0])
    if c == base: reseed.pop(base, None)
    else: reseed[base] = c
    el.save_json(rpath, reseed)
    print(f"#{i} {s['speaker']}: {s['text'][:60]!r} -> NEW take seed {sd} (dist {d:.1f})")
el.save_json(rpath, reseed); el.save_cut_cache()
print(f"≈ {credits} credits")
