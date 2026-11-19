#!/usr/bin/env python3
"""A sentence's last word comes out too soft ("…to build with knowledge" fading away)? Record 3 more takes and keep the one
whose last word is loudest relative to the rest of the sentence (and still heard correctly).
python3 build/last_word_take.py <key> <lang> "<start of sentence>"   -> writes build/el_cache/reseed.json"""
import hashlib, importlib.util, json, os, re, subprocess, sys
import numpy as np
spec = importlib.util.spec_from_file_location("el", os.path.join("build", "tts_elevenlabs.py"))
el = importlib.util.module_from_spec(spec); spec.loader.exec_module(el)
key, lang, start = sys.argv[1:4]
el.load_env(); api = os.environ["ELEVENLABS_API_KEY"].strip()
voices = json.loads(el.request("GET", "/voices", api))["voices"]
from faster_whisper import WhisperModel
wm = WhisperModel("small", device="cpu", compute_type="int8")
def last_word_gap(p):
    s, _ = wm.transcribe(p, language=lang, word_timestamps=True); ws = [w for x in s for w in x.words]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32)
    def db(a, b):
        seg = x[int(a * 16000):int(b * 16000)]; return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9) if len(seg) else -99
    body = db(ws[0].start, ws[-2].end); last = db(ws[-1].start, ws[-1].end)
    return last - body, " ".join(w.word.strip() for w in ws)
for spk, txt in el.read_turns(key, lang):
    sents = el.merge_short(el.split_sentences(txt))
    for j, s in enumerate(sents):
        if not s.startswith(start): continue
        vid = el.resolve_voice(spk, lang, voices)[0]
        body = {"text": el.spoken(s, lang), "model_id": "eleven_multilingual_v2", "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
        if sents[max(0, j - 2):j]: body["previous_text"] = el.spoken(" ".join(sents[max(0, j - 2):j]), lang)
        if j + 1 < len(sents): body["next_text"] = el.spoken(sents[j + 1], lang)
        h = lambda b: hashlib.sha1(json.dumps([vid, b], sort_keys=True).encode()).hexdigest()[:20] + ".mp3"
        base = h(body); rpath = os.path.join(el.CACHE, "reseed.json"); reseed = json.load(open(rpath)); cur = reseed.get(base, base); best = None
        for sd in (None, 1281, 1282, 1283):
            c = cur if sd is None else h(dict(body, seed=sd)); p = os.path.join(el.CACHE, c)
            if not os.path.exists(p):
                a = el.request("POST", f"/text-to-speech/{vid}", api, dict(body, seed=sd), query="?output_format=mp3_44100_128")
                open(p + ".part", "wb").write(a); os.replace(p + ".part", p)
            g, heard = last_word_gap(p)
            ok = not el.is_cut(p) and not el.asr_problem(body["text"], el.transcribe(p, lang, "small"))
            print(f"  {'current' if sd is None else 'seed ' + str(sd)}: last word {g:+.1f} dB vs the rest{'' if ok else '  (fails word check)'} | {heard}")
            if ok and (best is None or g > best[0] + (1.0 if sd else 0)): best = (g, c)
        if best[1] != cur:
            if best[1] == base: reseed.pop(base, None)
            else: reseed[base] = best[1]
            json.dump(reseed, open(rpath, "w"))
        print(f"{s!r} -> {'NEW take' if best[1] != cur else 'kept current'} ({best[0]:+.1f} dB)")
