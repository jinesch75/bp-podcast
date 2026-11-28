#!/usr/bin/env python3
"""Voice audition: the first N turns of an episode, ALL read by one voice (Anna's lines too).
python3 build/voice_sample.py <key> <lang> <voice_id> <n_turns> <out.mp3>
Same text, pronunciation rules, model, settings and context (previous/next text) as the real recordings;
takes are cached in build/el_cache (by voice id). Pauses: 0.14 s between sentences, 0.45 s between turns;
the result is levelled to -20 LUFS like the episodes. Written 27 Nov 2026 (French voice tests)."""
import hashlib, importlib.util, json, os, subprocess, sys, tempfile
spec = importlib.util.spec_from_file_location("el", os.path.join("build", "tts_elevenlabs.py"))
el = importlib.util.module_from_spec(spec); spec.loader.exec_module(el)
key, lang, vid, n, out = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
el.load_env(); api = os.environ["ELEVENLABS_API_KEY"].strip()
turns = el.read_turns(key, lang)[:n]
tmp = tempfile.mkdtemp(); parts = []; credits = 0
def sil(sec):
    p = os.path.join(tmp, f"sil{sec}.wav")
    if not os.path.exists(p):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(sec), p], check=True)
    return p
for ti, (spk, txt) in enumerate(turns):
    sents = el.merge_short(el.split_sentences(txt))
    for j, s in enumerate(sents):
        body = {"text": el.spoken(s, lang), "model_id": "eleven_multilingual_v2", "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
        if j: body["previous_text"] = el.spoken(" ".join(sents[max(0, j - 2):j]), lang)
        if j + 1 < len(sents): body["next_text"] = el.spoken(sents[j + 1], lang)
        p = os.path.join(el.CACHE, hashlib.sha1(json.dumps([vid, body], sort_keys=True).encode()).hexdigest()[:20] + ".mp3")
        if not os.path.exists(p):
            a = el.request("POST", f"/text-to-speech/{vid}", api, body, query="?output_format=mp3_44100_128")
            open(p + ".part", "wb").write(a); os.replace(p + ".part", p); credits += len(body["text"])
        w = os.path.join(tmp, f"{ti:03d}_{j:02d}.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-i", p, "-af", "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse", "-ar", "44100", "-ac", "1", w], check=True)
        parts += [w, sil(0.14 if j + 1 < len(sents) else 0.45)]
lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-20:TP=-1.5:LRA=11", "-ar", "44100", "-b:a", "128k", out], check=True)
print(f"{out}: {len(turns)} turns, ≈ {credits} credits")
