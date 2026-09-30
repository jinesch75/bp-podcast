#!/usr/bin/env python3
"""A/B listening test for hard names: each item is read as written (A) and with a phonetic spelling (B).
python3 build/pron_names_test.py <lang>   ->  build/el_test/pron_names_<lang>.mp3  (Anna's voice)"""
import importlib.util, json, os, subprocess, sys, tempfile
spec = importlib.util.spec_from_file_location("el", os.path.join("build", "tts_elevenlabs.py"))
el = importlib.util.module_from_spec(spec); spec.loader.exec_module(el)

ITEMS = {
    "en": [("Zukunftskeess", "Tsoo-koonfts-kayss"), ("Pensiounskeess", "Pen-see-ouns-kayss"),
           ("Eltereforum", "Elteruh-forum"), ("Info-Zenter Demenz", "Info-Tsenter Deh-ments"),
           ("Zesumme Vereinfachen", "Tsuh-zoo-muh Fer-ine-fakhen"), ("Lëtzebuerg", "Letze-boo-erg"),
           ("CePAS", "Seh-pass"), ("Kannergeld", "Kanner-gelt")],
    "fr": [("Zukunftskeess", "Tsoukounftskéss"), ("Pensiounskeess", "Pènnsiounskéss"),
           ("Eltereforum", "Eltèreu-forum"), ("Info-Zenter Demenz", "Info-Tsènnteur Démènnts"),
           ("Zesumme Vereinfachen", "Tsézoumeu Fèraïnnfarènn"), ("Lëtzebuerg", "Lètzebouerg"),
           ("Kannergeld", "Kannerguèlt")],
}
CARRIER = {"en": ("Number {n}.", "Option A: {a}.", "Option B: {b}."),
           "fr": ("Numéro {n}.", "Option A : {a}.", "Option B : {b}.")}

lang = sys.argv[1]
el.load_env()
key = os.environ["ELEVENLABS_API_KEY"].strip()
voices = json.loads(el.request("GET", "/voices", key))["voices"]
vid, vname = el.resolve_voice("Anna", lang, voices)
print("voice:", vname)
tmp = tempfile.mkdtemp()
parts, chars = [], 0
for n, (a, b) in enumerate(ITEMS[lang], 1):
    text = " ".join(t.format(n=n, a=a, b=b) for t in CARRIER[lang])
    chars += len(text)
    body = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
    audio = el.request("POST", f"/text-to-speech/{vid}", key, body, query="?output_format=mp3_44100_128")
    p = os.path.join(tmp, f"{n:02d}.mp3"); open(p, "wb").write(audio); parts.append(p)
    print(f"  {n}. A = {a}   |   B = {b}")
os.makedirs(os.path.join("build", "el_test"), exist_ok=True)
out = os.path.join("build", "el_test", f"pron_names_{lang}.mp3")
inputs = []
for p in parts:
    inputs += ["-i", p]
filt = "".join(f"[{i}:a]aresample=44100,apad=pad_dur=0.9[a{i}];" for i in range(len(parts)))
filt += "".join(f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1,loudnorm=I=-20[o]"
subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", filt, "-map", "[o]", "-b:a", "128k", out], check=True)
print(f"≈ {chars} credits ->", out)
