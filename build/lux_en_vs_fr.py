#!/usr/bin/env python3
"""Which "Luxembourg" takes sound French rather than English? For each sentence with "Luxembourg" (not "Luxembourg
City"), compare the word (whisper word timing, MFCC+DTW) with two references by the SAME voice: English
("I live and work in Luxembourg...") and French-style ("J'habite au Luxembourg depuis dix ans.").
Flags takes closer to the French reference. python3 build/lux_en_vs_fr.py <key> [--fix]  (--fix: 3 new takes for
flagged sentences, keep the most English one = smallest d_en - d_fr). Report: build/el_test/lux_<key>.txt"""
import hashlib, importlib.util, json, os, re, sys
import numpy as np, librosa
spec = importlib.util.spec_from_file_location("el", os.path.join("build", "tts_elevenlabs.py"))
el = importlib.util.module_from_spec(spec); spec.loader.exec_module(el)
key = sys.argv[1]; FIX = "--fix" in sys.argv; lang = "en"
el.load_env(); api = os.environ["ELEVENLABS_API_KEY"].strip()
voices = json.loads(el.request("GET", "/voices", api))["voices"]
vids = {r: el.resolve_voice(r, lang, voices)[0] for r in ("Anna", "Tom")}
from faster_whisper import WhisperModel
wm = WhisperModel("small", device="cpu", compute_type="int8")
def tts(spk, body):
    h = hashlib.sha1(json.dumps([vids[spk], body], sort_keys=True).encode()).hexdigest()[:20] + ".mp3"; p = os.path.join(el.CACHE, h)
    if not os.path.exists(p): open(p, "wb").write(el.request("POST", f"/text-to-speech/{vids[spk]}", api, body, query="?output_format=mp3_44100_128"))
    return h
def locate(path, wlang, all_=False):
    segs, _ = wm.transcribe(path, language=wlang, word_timestamps=True, beam_size=5)
    spans = [(w.start, w.end) for s in segs for w in s.words if re.sub(r"\W", "", w.word).lower().startswith("luxemb")]
    return spans if all_ else (spans[0] if spans else None)
def mfcc(path, sp):
    y, sr = librosa.load(path, sr=16000, offset=max(0, sp[0] - 0.03), duration=sp[1] - sp[0] + 0.06)
    m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)[1:]; return (m - m.mean(1, keepdims=True)) / (m.std(1, keepdims=True) + 1e-6)
def dtw(a, b):
    D, wp = librosa.sequence.dtw(X=a, Y=b, metric="euclidean"); return float(D[-1, -1] / len(wp))
ref = {}
for spk in ("Anna", "Tom"):
    for tag, txt, wl in (("en", "I live and work in Luxembourg, a small country in Europe.", "en"), ("fr", "J'habite au Luxembourg depuis dix ans.", "fr")):
        p = os.path.join(el.CACHE, tts(spk, {"text": txt, "model_id": "eleven_multilingual_v2", "voice_settings": el.VOICE_SETTINGS, "seed": 1234}))
        ref[(spk, tag)] = mfcc(p, locate(p, wl))
def score(path, spk):   # worst (most French-like) "Luxembourg" in the sentence
    spans = locate(path, "en", True)
    if not spans: return None
    return max(dtw(m, ref[(spk, "en")]) - dtw(m, ref[(spk, "fr")]) for m in (mfcc(path, sp) for sp in spans))   # < 0: closer to English
rpath = os.path.join(el.CACHE, "reseed.json"); reseed = json.load(open(rpath)); out = []; i = -1
for spk, txt in el.read_turns(key, lang):
    sents = el.merge_short(el.split_sentences(txt))
    for j, s in enumerate(sents):
        i += 1
        if not re.search(r"\bLuxembourg\b", s): continue
        body = {"text": el.spoken(s, lang), "model_id": "eleven_multilingual_v2", "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
        if sents[max(0, j - 2):j]: body["previous_text"] = el.spoken(" ".join(sents[max(0, j - 2):j]), lang)
        if j + 1 < len(sents): body["next_text"] = el.spoken(sents[j + 1], lang)
        base = hashlib.sha1(json.dumps([vids[spk], body], sort_keys=True).encode()).hexdigest()[:20] + ".mp3"
        cur = reseed.get(base, base); sc = score(os.path.join(el.CACHE, cur), spk)
        line = f"#{i} {spk}: {'FRENCH-LIKE' if sc is not None and sc > 0 else 'english    '} {sc if sc is None else round(sc, 2)}  {s[:70]!r}"
        if FIX and sc is not None and sc > float(os.environ.get("THRESH", "0")):
            best = (sc, cur)
            for sd in (1271, 1272, 1273):
                c = tts(spk, dict(body, seed=sd)); p = os.path.join(el.CACHE, c)
                if el.is_cut(p) or el.asr_problem(body["text"], el.transcribe(p, lang, "small")): continue
                v = score(p, spk)
                if v is not None and v < best[0]: best = (v, c)
            if best[1] != cur:
                reseed[base] = best[1]; json.dump(reseed, open(rpath, "w"))
            line += f"  -> {'NEW take ' + str(round(best[0], 2)) if best[1] != cur else 'no better take'}"
        print(line, flush=True); out.append(line)
open(f"build/el_test/lux_{key}.txt", "w").write("\n".join(out) + "\n")
