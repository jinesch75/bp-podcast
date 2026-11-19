#!/usr/bin/env python3
"""A/B listening file for one French word in the English voices (Jacques picks by ear).
python3 build/pron_ab.py <name> "<French reference sentence>" "<English carrier with {x}>" opt1 opt2 ...
-> build/el_test/pron_<name>_en_AB.mp3 : reference in REF_LANG (default fr), then each option by Anna, then Tom; timestamps printed."""
import hashlib, importlib.util, json, os, subprocess, sys
spec = importlib.util.spec_from_file_location("el", "build/tts_elevenlabs.py"); el = importlib.util.module_from_spec(spec); spec.loader.exec_module(el)
name, fr_ref, carrier, opts = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
el.load_env(); key = os.environ["ELEVENLABS_API_KEY"].strip(); voices = json.loads(el.request("GET", "/voices", key))["voices"]
os.makedirs("build/el_test/pfw", exist_ok=True)
def clip(role, lang, text):
    vid, _ = el.resolve_voice(role, lang, voices)
    body = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
    if lang == "lb":   # Luxembourgish reference: eleven_v3 supports lb (REF_LANG=lb)
        body = {"text": text, "model_id": "eleven_v3", "voice_settings": el.VOICE_SETTINGS, "seed": 1234, "language_code": "lb"}
    h = hashlib.sha1(json.dumps([vid, body], sort_keys=True).encode()).hexdigest()[:16]; p = f"build/el_test/pfw/{h}.mp3"
    if not os.path.exists(p): open(p, "wb").write(el.request("POST", f"/text-to-speech/{vid}", key, body, query="?output_format=mp3_44100_128"))
    return p
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout)
REF = os.environ.get("REF_LANG", "fr"); REF_ROLE = os.environ.get("REF_ROLE", "Anna")   # REF_LANG=en REF_ROLE=Tom: Tom's English voice as reference
parts = [(f"{REF.upper()} reference ({REF_ROLE}'s {REF} voice)", clip(REF_ROLE, REF, fr_ref))]
for i, o in enumerate(opts):
    parts += [(f"{chr(65+i)} Anna: {o}", clip("Anna", "en", carrier.format(x=o))), (f"{chr(65+i)} Tom: {o}", clip("Tom", "en", carrier.format(x=o)))]
t = 0.0; inputs = []; lines = []
for lab, p in parts:
    lines.append(f"{int(t//60)}:{t%60:04.1f}  {lab}"); t += dur(p) + 1.0; inputs += ["-i", p]
n = len(parts)
filt = "".join(f"[{i}:a]aresample=44100,apad=pad_dur=1.0[a{i}];" for i in range(n)) + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,loudnorm=I=-20[o]"
out = f"build/el_test/pron_{name}_en_AB.mp3"
subprocess.run(["ffmpeg","-y","-v","error",*inputs,"-filter_complex",filt,"-map","[o]","-b:a","128k",out], check=True)
print(out); print("\n".join(lines))
