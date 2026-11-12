#!/usr/bin/env python3
"""Re-take sentences that sound odd, and keep the take closest to that host's normal voice.
python3 build/best_take.py <key> <lang> <i,i,...>     (indices = sentence numbers from build/voice_qc.py)
Needs /tmp/voice_qc_<key>_<lang>.json (run voice_qc.py first, on the recording BEFORE the script is changed
or after a rebuild). For each sentence: 3 new seeds (1241-1243) + the current take are measured (pace, pitch,
pitch spread, loudness, voicing; whisper must still hear the right words); the take with the smallest distance
to the speaker's median profile wins and is written to build/el_cache/reseed.json, which tts_elevenlabs.py
already follows. Re-run el_run_batch.py afterwards to rebuild the episode (0 credits)."""
import hashlib, importlib.util, json, os, re, sys
import numpy as np, librosa
spec = importlib.util.spec_from_file_location("el", os.path.join("build", "tts_elevenlabs.py"))
el = importlib.util.module_from_spec(spec); spec.loader.exec_module(el)
key, lang, idx = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")]
qc = json.load(open(f"/tmp/voice_qc_{key}_{lang}.json"))
FIELDS = ("rate", "f0", "spread", "rms", "voiced")
prof = {}
for spk in ("Anna", "Tom"):
    rows = [v for v in qc.values() if v["speaker"] == spk]
    prof[spk] = {f: (np.median([r[f] for r in rows]), np.median(np.abs(np.array([r[f] for r in rows]) - np.median([r[f] for r in rows]))) * 1.4826 + 1e-6) for f in FIELDS}
def feats(p, text):
    y, sr = librosa.load(p, sr=16000); yt, _ = librosa.effects.trim(y, top_db=35); dur = len(yt) / sr
    f0, _, _ = librosa.pyin(yt, fmin=70, fmax=420, sr=sr, frame_length=1024); f = f0[~np.isnan(f0)]
    st = 12 * np.log2(f / np.median(f)) if len(f) > 5 else np.array([0.0])
    return {"rate": len(re.sub(r"\W", "", text)) / max(dur, 0.1), "f0": float(np.median(f)) if len(f) else 0,
            "spread": float(np.std(st)), "rms": float(20 * np.log10(np.sqrt(np.mean(yt ** 2)) + 1e-9)), "voiced": len(f) / max(len(f0), 1)}
def dist(fe, spk):
    return float(np.sqrt(sum(((fe[f] - prof[spk][f][0]) / prof[spk][f][1]) ** 2 for f in FIELDS)))
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
credits = 0
for i in idx:
    s = segs[i]; spoken = el.spoken(s["text"], lang)
    body = {"text": spoken, "model_id": model, "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
    if s["prev"]: body["previous_text"] = el.spoken(s["prev"], lang)
    if s["next"]: body["next_text"] = el.spoken(s["next"], lang)
    base = hpath(s["speaker"], body)
    cur = reseed.get(base, base)
    cands = [cur] + [hpath(s["speaker"], dict(body, seed=sd)) for sd in (1241, 1242, 1243)]
    best = None; report = []
    for c in dict.fromkeys(cands):
        p = os.path.join(el.CACHE, c)
        if not os.path.exists(p):
            sd = json.loads(json.dumps(body)); sd["seed"] = [1241, 1242, 1243][cands.index(c) - 1]
            open(p, "wb").write(el.request("POST", f"/text-to-speech/{vids[s['speaker']]}", api, sd, query="?output_format=mp3_44100_128")); credits += len(spoken)
        heard = el.transcribe(p, lang, "small"); bad = el.asr_problem(spoken, heard)
        d = dist(feats(p, spoken), s["speaker"]) + (100 if bad else 0) + (100 if el.is_cut(p) else 0)
        report.append(f"{d:6.1f}{' *' if c == cur else '  '}"); 
        if best is None or d < best[0] - (0.5 if c != cur else 0): best = (d, c)
    if best[1] != cur:
        if best[1] == base: reseed.pop(base, None)
        else: reseed[base] = best[1]
    print(f"#{i} {s['speaker']}: {s['text'][:55]!r}  takes {' '.join(report)}  -> {'NEW take' if best[1] != cur else 'kept current'}")
json.dump(reseed, open(rpath, "w")); el.save_cut_cache()
print(f"≈ {credits} credits")
