#!/usr/bin/env python3
"""Find the spelling that makes the EN/DE voices say French names the French way (Maison de l'Orientation, lycée).
Each variant is read by both hosts inside a carrier sentence; a French speech recogniser (whisper small, language fr)
scores how French it sounds. Writes build/el_test/pron_fr_words_<lang>.mp3 (A/B listening file) + scores.
python3 build/pron_fr_words_test.py <en|de>"""
import difflib, hashlib, importlib.util, json, os, re, subprocess, sys
spec = importlib.util.spec_from_file_location("el", os.path.join("build", "tts_elevenlabs.py"))
el = importlib.util.module_from_spec(spec); spec.loader.exec_module(el)
lang = sys.argv[1]
V = {"en": {"maison": ["Maison de l'Orientation", "Mayzon duh Lor-yon-tah-syon", "Meh-zon de Lor-ee-on-tah-see-on",
                       "Maizon de l'Oriyantasyon", "Mezon duh Loriontasion"],
            "lycee": ["lycée", "lee-say", "leessay", "lee-SAY", "lissay"]},
     "de": {"maison": ["Maison de l'Orientation", "Mäsong dö l'Orjangtasjong", "Mesong de Lorjantasjon"],
            "lycee": ["Lycée", "Lissee", "Lisseh"]}}[lang]
CARRIER = {"en": {"maison": "It's called the {x}, in Luxembourg City.", "lycee": "You can ask how to get back into a {x}."},
           "de": {"maison": "Sie heißt {x}, in Luxemburg-Stadt.", "lycee": "Sie fragen, wie man wieder in ein {x} kommt."}}[lang]
TARGET = {"maison": "maison de l'orientation", "lycee": "lycée"}
el.load_env(); key = os.environ["ELEVENLABS_API_KEY"].strip()
voices = json.loads(el.request("GET", "/voices", key))["voices"]
from faster_whisper import WhisperModel
wm = WhisperModel("small", device="cpu", compute_type="int8")
os.makedirs("build/el_test/pfw", exist_ok=True)
def norm(t): return re.sub(r"[^a-zàâçéèêëîïôûùüÿ' ]", "", t.lower().replace("’", "'"))
res, parts, chars = {}, [], 0
for role in ("Anna", "Tom"):
    vid, vname = el.resolve_voice(role, lang, voices)
    for word, variants in V.items():
        for n, v in enumerate(variants):
            text = CARRIER[word].format(x=v)
            body = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
            h = hashlib.sha1(json.dumps([vid, body], sort_keys=True).encode()).hexdigest()[:16]
            p = f"build/el_test/pfw/{h}.mp3"
            if not os.path.exists(p):
                open(p, "wb").write(el.request("POST", f"/text-to-speech/{vid}", key, body, query="?output_format=mp3_44100_128")); chars += len(text)
            segs, _ = wm.transcribe(p, language="fr", beam_size=5)
            heard = norm(" ".join(s.text for s in segs)); tgt = TARGET[word]
            words = heard.split(); k = len(tgt.split())
            score = max([difflib.SequenceMatcher(None, " ".join(words[i:i + k]), tgt).ratio() for i in range(max(1, len(words) - k + 1))] + [0])
            res.setdefault(word, {}).setdefault(v, []).append(round(score, 2))
            print(f"{role:4} {word:6} {chr(65+n)} {v!r:40} score {score:.2f}  heard: {heard}")
            parts.append(p)
for word, d in res.items():
    best = max(d, key=lambda v: sum(d[v]))
    print(f"BEST {word}: {best!r}  ({d[best]})")
# A/B file: for each word, each variant read by Anna then Tom, with a pause
inputs = []
for p in parts: inputs += ["-i", p]
filt = "".join(f"[{i}:a]aresample=44100,apad=pad_dur=0.8[a{i}];" for i in range(len(parts)))
filt += "".join(f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1,loudnorm=I=-20[o]"
out = f"build/el_test/pron_fr_words_{lang}.mp3"
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", filt, "-map", "[o]", "-b:a", "128k", out], check=True)
print(f"≈ {chars} credits ->", out)
