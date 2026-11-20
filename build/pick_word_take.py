#!/usr/bin/env python3
"""Pick the take where one English word sounds most English (start "*" + MIN_P=0.8: scan all sentences with the word) (e.g. "German" read with a French accent after a
French name). python3 build/pick_word_take.py <key> <lang> "<start of sentence>" <word>
Candidates: current take + seeds 1261-1263. Score = whisper (small, language=<lang>) word probability of <word>;
the take must pass the normal word check. Winner -> build/el_cache/reseed.json; re-run el_run_batch.py afterwards."""
import hashlib, importlib.util, json, os, re, sys
spec = importlib.util.spec_from_file_location("el", os.path.join("build", "tts_elevenlabs.py"))
el = importlib.util.module_from_spec(spec); spec.loader.exec_module(el)
key, lang, start, word = sys.argv[1:5]
# start "*" = every sentence containing <word>; then only sentences whose current take scores below MIN_P are retaken
MIN_P = float(os.environ.get("MIN_P", "1.1"))
el.load_env(); api = os.environ["ELEVENLABS_API_KEY"].strip()
voices = json.loads(el.request("GET", "/voices", api))["voices"]
from faster_whisper import WhisperModel
wm = WhisperModel("small", device="cpu", compute_type="int8")
for spk, txt in el.read_turns(key, lang):
    sents = el.merge_short(el.split_sentences(txt))
    for j, s in enumerate(sents):
        if start == "*":
            if not re.search(r"\b" + re.escape(word) + r"\b", s): continue
        elif not s.startswith(start): continue
        vid = el.resolve_voice(spk, lang, voices)[0]
        body = {"text": el.spoken(s, lang), "model_id": "eleven_multilingual_v2", "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
        if sents[max(0, j - 2):j]: body["previous_text"] = el.spoken(" ".join(sents[max(0, j - 2):j]), lang)
        if j + 1 < len(sents): body["next_text"] = el.spoken(sents[j + 1], lang)
        h = lambda b: hashlib.sha1(json.dumps([vid, b], sort_keys=True).encode()).hexdigest()[:20] + ".mp3"
        base = h(body); rpath = os.path.join(el.CACHE, "reseed.json"); reseed = json.load(open(rpath))
        cur = reseed.get(base, base); best = None
        for sd in (None, 1261, 1262, 1263):
            if sd and best and best[0] >= MIN_P: break
            c = cur if sd is None else h(dict(body, seed=sd)); p = os.path.join(el.CACHE, c)
            if not os.path.exists(p):
                open(p, "wb").write(el.request("POST", f"/text-to-speech/{vid}", api, dict(body, seed=sd), query="?output_format=mp3_44100_128"))
            segs, _ = wm.transcribe(p, language=lang, word_timestamps=True, beam_size=5)
            ws = [w for x in segs for w in x.words]
            pr = max([w.probability for w in ws if re.fullmatch(word, re.sub(r"\W", "", w.word), re.I)] + [0])   # <word> may be a regex, e.g. "Bee?"
            ok = not el.is_cut(p) and not el.asr_problem(body["text"], el.transcribe(p, lang, "small"))
            print(f"  {'current' if sd is None else 'seed ' + str(sd)}: p({word}) = {pr:.2f}{'' if ok else '  (fails word check)'}  heard: {' '.join(w.word.strip() for w in ws)}")
            if ok and (best is None or pr > best[0] + (0.05 if sd else 0)): best = (pr, c)
        if best and best[1] != cur:
            if best[1] == base: reseed.pop(base, None)
            else: reseed[base] = best[1]
            el.save_json(rpath, reseed)
        print(f"{s!r} -> {'NEW take' if best and best[1] != cur else 'kept current'} (p={best[0]:.2f})")
