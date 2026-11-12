#!/usr/bin/env python3
"""Keep, for every sentence that contains a French name, the take whose pronunciation of that name is closest
to an approved reference recording by the same voice (Jacques chose them by ear in an A/B test).
python3 build/match_pron.py <key> <lang>
How: whisper (word timestamps) finds the name in each take; MFCC + DTW distance to the reference word (same
voice, so this compares pronunciation, not voice). Candidates: current take + seeds 1251-1253. The take must still
pass the word check and not be cut. Winner goes to build/el_cache/reseed.json. Report: build/el_test/match_pron_<key>_<lang>.txt"""
import difflib, hashlib, importlib.util, json, os, re, sys
import numpy as np, librosa
spec = importlib.util.spec_from_file_location("el", os.path.join("build", "tts_elevenlabs.py"))
el = importlib.util.module_from_spec(spec); spec.loader.exec_module(el)
key, lang = sys.argv[1], sys.argv[2]
START = int(sys.argv[3]) if len(sys.argv) > 3 else 0   # resume from this sentence index
# name -> (pattern in the script, carrier sentence of the approved reference, words to locate)
TERMS = {"en": [("maison de l'orientation", r"(?i)maison de l.orientation", "It's called the Maison de l'Orientation, in Luxembourg City."),
                ("lycée", r"(?i)\blycées?\b", "You can ask how to get back into a leessay.")]}[lang]
el.load_env(); api = os.environ["ELEVENLABS_API_KEY"].strip()
voices = json.loads(el.request("GET", "/voices", api))["voices"]
vids = {r: el.resolve_voice(r, lang, voices)[0] for r in ("Anna", "Tom")}
from faster_whisper import WhisperModel
wm = WhisperModel("small", device="cpu", compute_type="int8")
def norm(t): return re.sub(r"[^a-zàâçéèêëîïôûùü' ]", "", t.lower().replace("’", "'"))
ALT = {"lycée": ["lycée", "lycées", "lice", "licy", "lisa", "lisae", "lices", "lysee", "lisée", "leessay", "lissay", "lease", "lisse", "lessay", "lisey"]}
def locate(path, target):
    segs, _ = wm.transcribe(path, language=lang, word_timestamps=True, beam_size=5)
    words = [w for s in segs for w in s.words]
    best = (0, None)
    for i in range(len(words)):
        for k in range(1, 5):
            if i + k > len(words): break
            txt = norm("".join(w.word for w in words[i:i + k])).strip()
            r = max(difflib.SequenceMatcher(None, txt, t).ratio() for t in ALT.get(target, [target]))
            if r > best[0]: best = (r, (words[i].start, words[i + k - 1].end))
    return best[1] if best[0] > 0.6 else None
def mfcc(path, span):
    y, sr = librosa.load(path, sr=16000, offset=max(0, span[0] - 0.03), duration=span[1] - span[0] + 0.06)
    m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)[1:]
    return (m - m.mean(1, keepdims=True)) / (m.std(1, keepdims=True) + 1e-6)
def dtw(a, b):
    D, wp = librosa.sequence.dtw(X=a, Y=b, metric="euclidean"); return float(D[-1, -1] / len(wp))
def tts(spk, body):
    h = hashlib.sha1(json.dumps([vids[spk], body], sort_keys=True).encode()).hexdigest()[:20] + ".mp3"
    p = os.path.join(el.CACHE, h)
    if not os.path.exists(p):
        open(p, "wb").write(el.request("POST", f"/text-to-speech/{vids[spk]}", api, body, query="?output_format=mp3_44100_128")); tts.credits += len(body["text"])
    return h
tts.credits = 0
ref = {}
for name, pat, carrier in TERMS:
    for spk in ("Anna", "Tom"):
        body = {"text": carrier, "model_id": "eleven_multilingual_v2", "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
        p = os.path.join(el.CACHE, tts(spk, body)); sp = locate(p, name); assert sp, (name, spk)
        ref[(name, spk)] = mfcc(p, sp)
segs = []
for spk, txt in el.read_turns(key, lang):
    sents = el.merge_short(el.split_sentences(txt))
    for j, s in enumerate(sents):
        segs.append({"speaker": spk, "text": s, "prev": " ".join(sents[max(0, j - 2):j]), "next": sents[j + 1] if j + 1 < len(sents) else ""})
rpath = os.path.join(el.CACHE, "reseed.json"); reseed = json.load(open(rpath)) if os.path.exists(rpath) else {}
lines = []
for i, s in enumerate(segs):
    if i < START: continue
    terms = [(n, p) for n, p, _ in TERMS if re.search(p, s["text"])]
    if not terms: continue
    spoken = el.spoken(s["text"], lang)
    body = {"text": spoken, "model_id": "eleven_multilingual_v2", "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
    if s["prev"]: body["previous_text"] = el.spoken(s["prev"], lang)
    if s["next"]: body["next_text"] = el.spoken(s["next"], lang)
    base = hashlib.sha1(json.dumps([vids[s["speaker"]], body], sort_keys=True).encode()).hexdigest()[:20] + ".mp3"
    if not os.path.exists(os.path.join(el.CACHE, base)): continue      # not recorded yet: run el_run_batch first
    cur = reseed.get(base, base)
    cands = list(dict.fromkeys([cur] + [tts(s["speaker"], dict(body, seed=sd)) for sd in (1251, 1252, 1253)]))
    scored = []
    for c in cands:
        p = os.path.join(el.CACHE, c)
        if el.is_cut(p) or el.asr_problem(spoken, el.transcribe(p, lang, "small")):
            scored.append((99, c)); continue
        ds = []
        for name, _ in terms:
            sp = locate(p, name)
            ds.append(dtw(mfcc(p, sp), ref[(name, s["speaker"])]) if sp else 9)
        scored.append((float(np.mean(ds)), c))
    d_cur = dict((c, d) for d, c in scored)[cur]
    d_best, best = min(scored)
    if best != cur and d_best < d_cur - 0.05:
        if best == base: reseed.pop(base, None)
        else: reseed[base] = best
        verdict = "NEW take"
    else:
        verdict = "kept current"
    lines.append(f"#{i} {s['speaker']}: {s['text'][:60]!r}  current {d_cur:.2f} | takes " + " ".join(f"{d:.2f}" for d, _ in scored[1:]) + f"  -> {verdict}")
    print(lines[-1], flush=True)
    json.dump(reseed, open(rpath, "w"))
el.save_cut_cache()
open(f"build/el_test/match_pron_{key}_{lang}.txt", "w").write("\n".join(lines) + "\n")
print(f"≈ {tts.credits} credits")
