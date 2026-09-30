#!/usr/bin/env python3
"""ElevenLabs per-sentence TTS generator for Biergerpakt episodes.

Drop-in replacement for tts_generate.py / tts_lang.py: it writes the same
seg_####.mp3 + meta.json layout, so build/rebuild.py (PCM concat, sample-accurate
timestamps) works unchanged. Run from the project root.

Usage
  python3 build/tts_elevenlabs.py <key> <lang> [--first N] [--yes]
      lang = en | fr | de | lb
      --first N   only the first N sentences (cheap listening test)
      --yes       required when the run would spend more than 3,000 credits
      --estimate  only print how many sentences/credits a run would need, then stop
  Env: EL_CONCURRENCY=N  generate N sentences in parallel (default 1; Pro plan allows more)

Examples
  python3 build/tts_elevenlabs.py myguichet en --first 25           # ~2-min test
  python3 build/tts_elevenlabs.py myguichet fr --yes                # full episode

Setup
  .env in the project root (NEVER committed; .env is in .gitignore):
      ELEVENLABS_API_KEY=sk_...
  Voices per language (defaults, names as in "My Voices"):
      en  Anna = Elizabeth   Tom = James
      fr  Anna = Lucie       Tom = Marcel
      de  Anna = Lola        Tom = Benjamin
      lb  uses the English pair unless overridden
  Optional overrides in .env, per language:
      ANNA_VOICE_FR=Lucie       TOM_VOICE_FR=Marcel      (names)
      ANNA_VOICE_ID_FR=...      TOM_VOICE_ID_FR=...      (exact ids win over names)
      EL_MODEL=eleven_multilingual_v2               (lb always uses eleven_v3)
  A library voice must be added to "My Voices" in ElevenLabs before it can be found.

Caching
  Every generated sentence is stored in build/el_cache/<hash>.mp3, keyed on
  voice + model + settings + text. Re-runs, crashes and script edits only pay for
  sentences that actually changed. build/el_cache/ is git-ignored.
"""
import hashlib, json, os, re, shutil, subprocess, sys, time, urllib.error, urllib.request

ROOT = os.getcwd()
API = "https://api.elevenlabs.io/v1"
CACHE = os.path.join(ROOT, "build", "el_cache")
TEST_DIR = os.path.join(ROOT, "build", "el_test")
CONFIRM_ABOVE = 3000  # credits

# Hosts per language (names as they appear in "My Voices"). lb falls back to the English pair.
DEFAULT_VOICES = {
    "en": {"Anna": "Elizabeth", "Tom": "James"},
    "fr": {"Anna": "Lucie",     "Tom": "Marcel"},
    "de": {"Anna": "Lola",      "Tom": "Benjamin"},  # Benjamin chosen over Felix 2026-09-30
}
VOICE_SETTINGS = {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0,
                  "use_speaker_boost": True, "speed": 1.0}
LANG_CODE = {"en": "en", "fr": "fr", "de": "de", "lb": "lb"}

# Pronunciation fixes applied ONLY to the text sent to ElevenLabs (the transcript keeps the
# written form). (regex, replacement) pairs per language. Editing these re-generates only the
# sentences they touch (the cache key includes the spoken text).
# Pronunciation rules (all languages) live in build/pronunciation.py:
# .lu addresses -> "dot L-U", acronyms, phone numbers, 112, stage directions, symbols ...
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pronunciation import PRONUNCIATION, spoken  # noqa: E402


# ---------- config ----------
def load_env():
    path = os.path.join(ROOT, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def die(msg):
    print("ERROR:", msg)
    sys.exit(1)


# ---------- script parsing (same rules as tts_batch.py) ----------
def split_sentences(t):
    t = t.replace("...", "<ELL>")
    parts = [p.replace("<ELL>", "...").strip() for p in re.split(r'(?<=[.!?])\s+', t) if p.strip()]
    merged = []
    months = r"(Januar|Jänner|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\b"
    for p in parts:  # glue punctuation-only fragments (a lone ») onto the previous sentence
        if merged and re.search(r"\b\d{1,2}\.$", merged[-1]) and re.match(months, p):
            merged[-1] += " " + p   # German dates "am 28. Mai 2019" are one sentence
        elif re.search(r'[0-9A-Za-zÀ-ÿ]', p) or not merged:
            merged.append(p)
        else:
            merged[-1] += " " + p
    return merged


def read_turns(key, lang):
    name = f"podcast_script_{key}.md" if lang == "en" else f"podcast_script_{key}_{lang}.md"
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        die(f"{name} not found — run this from the project root.")
    turns = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r'\*\*(ANNA|TOM)\s*:\*\*\s*(.*)', line.strip())
        if m and m.group(2).strip():
            turns.append(("Anna" if m.group(1) == "ANNA" else "Tom", m.group(2).strip()))
    return turns


def merge_short(sents):
    """Very short sentences ("Exactly.", "Ah.", "Oui.") sound odd when generated on their own:
    glue each one to the next sentence of the same turn so the voice reads them together."""
    out = []
    for p in sents:
        if out and len(re.findall(r"[\wÀ-ÿ'’-]+", out[-1])) <= 2:
            out[-1] = out[-1] + " " + p
        else:
            out.append(p)
    return out


_CUT = {}


def is_cut(path):
    """Cached wrapper (results are stored in el_cache/cut.json)."""
    cpath = os.path.join(CACHE, "cut.json")
    if not _CUT:
        _CUT.update(json.load(open(cpath)) if os.path.exists(cpath) else {"_": 0})
    k = os.path.basename(path)
    if k not in _CUT:
        _CUT[k] = _is_cut(path)
        if len(_CUT) % 25 == 0:
            json.dump(_CUT, open(cpath, "w"))
    return _CUT[k]


def save_cut_cache():
    if _CUT:
        json.dump(_CUT, open(os.path.join(CACHE, "cut.json"), "w"))


def _is_cut(path):
    """True when the speech runs right to the last sample (ElevenLabs cut the last sound off).
    A short stray sound after a pause is not a cut (rebuild.py CLEAN=1 removes it)."""
    try:
        import numpy as np
    except ImportError:
        return False
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", "24000", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    w = 240; n = len(x) // w
    if n < 10:
        return False
    env = 20 * np.log10(np.sqrt((x[:n * w].reshape(n, w) ** 2).mean(1)) + 1e-9)
    on = env > -42
    if not on[-2:].any() or env[-1] <= -38:
        return False
    j = n - 1                          # length of the final sound, and the pause before it
    while j >= 0 and on[j]:
        j -= 1
    k = j
    while k >= 0 and not on[k]:
        k -= 1
    stray = (n - 1 - j) < 25 and (j - k) >= 12 and k >= 0
    return not stray


# ---------- listening check (speech recognition) ----------
# ElevenLabs occasionally adds a word that is not in the text (e.g. "Jamais !" after a question) or
# garbles one. Every generated sentence is transcribed with faster-whisper ("base", then "small" to
# confirm) and compared with the text; failures are re-generated with another seed.
NUMBER_WORDS = set("""zero one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty
hundred thousand million zéro un une deux trois quatre cinq six sept huit neuf dix onze douze vingt trente quarante
cinquante soixante cent cents mille null eins zwei drei vier fünf sechs sieben acht neun zehn elf zwölf zwanzig
dreißig vierzig hundert tausend percent prozent pour thirteen fourteen fifteen sixteen seventeen eighteen
nineteen sixty seventy eighty ninety treize quatorze quinze seize dix-sept septante octante nonante quatre-vingt
quatre-vingts dreizehn vierzehn fünfzehn sechzehn siebzehn achtzehn neunzehn fünfzig sechzig siebzig achtzig
neunzig first second third premier première""".split())
_ASR = {}
_NUM = re.compile("^(?:" + "|".join(sorted({w.replace("ß", "ss").replace("ü", "u").replace("é", "e").replace("è", "e")
                                              for w in NUMBER_WORDS} | {"und", "and", "et", "zig", "ssig"},
                                             key=len, reverse=True)) + ")+$")


def _words(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", t.lower().replace("’", "'").replace("ß", "ss"))
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"\b(dot|point|punkt)\b", " ", t)   # "MyGuichet dot L-U" is written "MyGuichet.lu"
    t = re.sub(r"\b([a-z])-(?=[a-z]\b)", r"\1", t)   # spelled letters "C-N-S" -> "cns"
    return [w for w in re.split(r"[^a-z0-9]+", t)
            if len(w) > 1 and not re.search(r"\d", w) and not _NUM.match(w) and w != "lu"]


def asr_problem(expected, heard):
    """Return a short reason when the recording does not match the text, else None."""
    import difflib
    e, h = _words(expected), _words(heard)
    if len(e) <= 2:   # very short lines ("Trente-cinq pour cent ?"): only flag clearly added words
        return ("extra words: " + " ".join(h)) if len(h) - len(e) >= 3 else None
    # same letters with different word breaks ("wiederzuentdecken" / "wieder zu entdecken",
    # "MyGuichet dot L-U" / "MyGuichet.lu") is fine
    ej, hj = "".join(e), "".join(h)
    if abs(len(ej) - len(hj)) <= 3 and difflib.SequenceMatcher(None, ej, hj, autojunk=False).ratio() >= 0.85:
        return None
    sm = difflib.SequenceMatcher(None, e, h, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "insert" and (j1 == 0 or j2 == len(h)) and any(len(w) >= 3 for w in h[j1:j2]):
            return "extra words: " + " ".join(h[j1:j2])
        if op == "insert" and j2 - j1 >= 2:
            return "extra words: " + " ".join(h[j1:j2])
        if op == "delete" and i2 - i1 >= 2:
            return "missing words: " + " ".join(e[i1:i2])
        if op == "replace" and (j2 - j1) - (i2 - i1) >= 2:
            return "extra words: " + " ".join(h[j1:j2])
    if sm.ratio() < 0.6:
        return "does not match the text"
    return None


def transcribe(path, lang, size):
    from faster_whisper import WhisperModel
    if size not in _ASR:
        _ASR[size] = WhisperModel(size, device="cpu", compute_type="int8", cpu_threads=os.cpu_count() or 4)
    segs, _ = _ASR[size].transcribe(path, language=lang, beam_size=1 if size == "base" else 3)
    return " ".join(x.text.strip() for x in segs)


# ---------- API ----------
def request(method, path, api_key, body=None, query=""):
    url = f"{API}{path}{query}"
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(6):
        req = urllib.request.Request(url, data=data, method=method, headers={
            "xi-api-key": api_key, "Content-Type": "application/json", "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:400]
            if "quota_exceeded" in detail:
                die("ElevenLabs credit limit reached for this API key (raise the key's credit limit in "
                    "ElevenLabs > Developers > API keys, or wait for the monthly reset).\n" + detail)
            if e.code == 401:
                die("API key rejected (401). Check ELEVENLABS_API_KEY in .env and the key's permissions.\n" + detail)
            if e.code in (429, 500, 502, 503, 504) and attempt < 5:
                wait = 2 ** attempt * 2
                print(f"  HTTP {e.code}, retrying in {wait}s…")
                time.sleep(wait)
                continue
            die(f"HTTP {e.code}: {detail}")
        except urllib.error.URLError as e:
            if attempt < 5:
                time.sleep(2 ** attempt * 2)
                continue
            die(f"network error: {e}")


def resolve_voice(role, lang, voices):
    R, L = role.upper(), lang.upper()
    vid = os.environ.get(f"{R}_VOICE_ID_{L}")
    if vid:
        return vid, vid
    default = DEFAULT_VOICES.get(lang, DEFAULT_VOICES["en"])[role]
    want = os.environ.get(f"{R}_VOICE_{L}", default).lower()
    hits = [v for v in voices if v["name"].lower() == want
            or v["name"].lower().split(" - ")[0].strip() == want]
    if not hits:
        hits = [v for v in voices if v["name"].lower().startswith(want)]
    if len(hits) == 1:
        return hits[0]["voice_id"], hits[0]["name"]
    listing = "\n".join(f"   {v['voice_id']}  {v['name']}" for v in (hits or voices))
    if not hits:
        die(f"No voice named '{want}' for {role} ({lang}) in My Voices. Add it from the Voice Library "
            f"(Add to My Voices) or set {R}_VOICE_ID_{L} in .env. Available:\n{listing}")
    die(f"Several voices match '{want}' for {role} ({lang}); set {R}_VOICE_ID_{L} in .env to one of:\n{listing}")


# ---------- main ----------
def main():
    args = sys.argv[1:]
    if len(args) < 2 or args[1] not in LANG_CODE:
        print(__doc__)
        sys.exit(1)
    key, lang = args[0], args[1]
    first = int(args[args.index("--first") + 1]) if "--first" in args else None
    confirmed = "--yes" in args
    estimate = "--estimate" in args

    load_env()
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        die("ELEVENLABS_API_KEY missing — put it in .env in the project root.")

    model = "eleven_v3" if lang == "lb" else os.environ.get("EL_MODEL", "eleven_multilingual_v2")
    stitching = model != "eleven_v3"  # previous_text/next_text context (not used with v3)

    voices = json.loads(request("GET", "/voices", api_key))["voices"]
    vids = {}
    for role in ("Anna", "Tom"):
        vids[role], vname = resolve_voice(role, lang, voices)
        print(f"{role}: {vname}  ({vids[role]})")
    print(f"model: {model}   language: {lang}")

    # sentences, with neighbouring sentences of the same turn as context
    segs = []
    for spk, txt in read_turns(key, lang):
        sents = split_sentences(txt)
        if os.environ.get("EL_MERGE_SHORT", "1") == "1":
            sents = merge_short(sents)
        for j, s in enumerate(sents):
            segs.append({"speaker": spk, "text": s,
                         "prev": " ".join(sents[max(0, j - 2):j]),
                         "next": sents[j + 1] if j + 1 < len(sents) else ""})
    if first:
        segs = segs[:first]

    os.makedirs(CACHE, exist_ok=True)
    for s in segs:
        body = {"text": spoken(s["text"], lang), "model_id": model,
                "voice_settings": VOICE_SETTINGS, "seed": 1234}
        if stitching:
            if s["prev"]:
                body["previous_text"] = spoken(s["prev"], lang)
            if s["next"]:
                body["next_text"] = spoken(s["next"], lang)
        if model in ("eleven_v3", "eleven_flash_v2_5", "eleven_turbo_v2_5"):
            body["language_code"] = LANG_CODE[lang]
        s["body"] = body
        h = hashlib.sha1(json.dumps([vids[s["speaker"]], body], sort_keys=True).encode()).hexdigest()[:20]
        s["cache"] = os.path.join(CACHE, h + ".mp3")

    todo = [s for s in segs if not (os.path.exists(s["cache"]) and os.path.getsize(s["cache"]) > 500)]
    cost = sum(len(s["body"]["text"]) for s in todo)
    print(f"sentences: {len(segs)}   to generate: {len(todo)}   ≈ {cost:,} credits")
    try:  # best effort: needs the key's "user read" permission
        req = urllib.request.Request(f"{API}/user/subscription", headers={"xi-api-key": api_key})
        sub = json.loads(urllib.request.urlopen(req, timeout=30).read())
        left = sub.get("character_limit", 0) - sub.get("character_count", 0)
        print(f"credits left this period: {left:,}")
    except Exception:
        pass
    if estimate:
        sys.exit(0)
    if cost > CONFIRM_ABOVE and not confirmed:
        print(f"This run would use more than {CONFIRM_ABOVE:,} credits. Re-run with --yes to proceed.")
        sys.exit(0)

    def gen(s):
        audio = request("POST", f"/text-to-speech/{vids[s['speaker']]}", api_key, s["body"],
                        query="?output_format=mp3_44100_128")
        if len(audio) < 500:
            raise RuntimeError(f"empty audio for: {s['text'][:60]}")
        tmp = s["cache"] + ".part"
        open(tmp, "wb").write(audio)
        os.replace(tmp, s["cache"])

    jobs = max(1, int(os.environ.get("EL_CONCURRENCY", "1")))
    from concurrent.futures import ThreadPoolExecutor, as_completed
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futs = [pool.submit(gen, s) for s in todo]
        for n, f in enumerate(as_completed(futs), 1):
            try:
                f.result()
            except SystemExit:
                pool.shutdown(wait=False, cancel_futures=True)
                raise
            except Exception as e:
                pool.shutdown(wait=False, cancel_futures=True)
                die(str(e))
            if n % 10 == 0 or n == len(todo):
                print(f"  generated {n}/{len(todo)}", flush=True)

    # re-generate sentences whose ending was cut off, with another seed (up to 3 tries)
    if os.environ.get("EL_FIX_CUTS", "1") == "1":
        rpath = os.path.join(CACHE, "reseed.json")
        reseed = json.load(open(rpath)) if os.path.exists(rpath) else {}
        fixed = still = 0
        for s in segs:
            base = os.path.basename(s["cache"])
            if base in reseed and os.path.exists(os.path.join(CACHE, reseed[base])):
                s["cache"] = os.path.join(CACHE, reseed[base]); continue
            if not is_cut(s["cache"]):
                continue
            for seed in (1235, 1236, 1237):
                body = dict(s["body"], seed=seed)
                h = hashlib.sha1(json.dumps([vids[s["speaker"]], body], sort_keys=True).encode()).hexdigest()[:20]
                alt = os.path.join(CACHE, h + ".mp3")
                if not (os.path.exists(alt) and os.path.getsize(alt) > 500):
                    gen(dict(s, body=body, cache=alt))
                if not is_cut(alt):
                    reseed[base] = h + ".mp3"; s["cache"] = alt; fixed += 1
                    break
            else:
                still += 1
                print(f"  still cut after 3 tries: {s['text'][:70]}")
            json.dump(reseed, open(rpath, "w"))
        save_cut_cache()
        print(f"cut-off endings re-generated: {fixed}" + (f", still cut: {still}" if still else ""))

    # listening check: re-generate sentences where the voice added, dropped or garbled words
    asr_on = os.environ.get("EL_ASR", "1") == "1" and lang in ("en", "fr", "de")
    if asr_on:
        try:
            import faster_whisper  # noqa: F401
        except ImportError:
            print("listening check skipped (pip install faster-whisper to enable it)")
            asr_on = False
    if asr_on:
        apath = os.path.join(CACHE, "asr.json")
        rpath = os.path.join(CACHE, "reseed.json")
        asr = json.load(open(apath)) if os.path.exists(apath) else {}
        reseed = json.load(open(rpath)) if os.path.exists(rpath) else {}
        def heard(path, size):
            k = os.path.basename(path) + ":" + size
            if k not in asr:
                asr[k] = transcribe(path, lang, size)
            return asr[k]
        def verdict(path, s):
            exp = s["body"]["text"]
            if not asr_problem(exp, heard(path, "base")):
                return None
            return asr_problem(exp, heard(path, "small"))   # confirm with the better model
        fixed = kept = 0; n = 0
        for s in segs:
            n += 1
            if n % 20 == 0:
                json.dump(asr, open(apath, "w"), ensure_ascii=False)
            why = verdict(s["cache"], s)
            if not why:
                continue
            base = os.path.basename(s["cache"])
            ok = False
            for seed in (1238, 1239, 1240):
                body = dict(s["body"], seed=seed)
                h = hashlib.sha1(json.dumps([vids[s["speaker"]], body], sort_keys=True).encode()).hexdigest()[:20]
                alt = os.path.join(CACHE, h + ".mp3")
                if not (os.path.exists(alt) and os.path.getsize(alt) > 500):
                    gen(dict(s, body=body, cache=alt))
                if not is_cut(alt) and not verdict(alt, s):
                    reseed[base] = h + ".mp3"; s["cache"] = alt; ok = True; fixed += 1
                    json.dump(reseed, open(rpath, "w"))
                    break
            if not ok:
                kept += 1
                print(f"  check manually ({why}): {s['text'][:80]}")
        json.dump(asr, open(apath, "w"), ensure_ascii=False)
        print(f"listening check: {len(segs)} sentences, re-generated {fixed}" + (f", {kept} to check by ear" if kept else ""))

    # assemble the rebuild.py work folder
    suffix = "" if lang == "en" else f"_{lang}"
    work = f"/tmp/{key}{suffix}_el_seg" + ("_test" if first else "")
    if os.path.isdir(work):
        shutil.rmtree(work)
    os.makedirs(work)
    for i, s in enumerate(segs):
        shutil.copyfile(s["cache"], f"{work}/seg_{i:04d}.mp3")
    json.dump({"meta": [{"speaker": s["speaker"], "text": s["text"]} for s in segs], "n": len(segs)},
              open(f"{work}/meta.json", "w"), ensure_ascii=False)
    print("ALL SEGMENTS DONE", len(segs))

    if first:
        os.makedirs(TEST_DIR, exist_ok=True)
        out = os.path.join(TEST_DIR, f"{key}_{lang}_first{first}.mp3")
        env = dict(os.environ, TEMPO="1.0", LOUDNORM=os.environ.get("LOUDNORM", "-20"))
        subprocess.run([sys.executable, os.path.join(ROOT, "build", "rebuild.py"), work, out], env=env, check=True)
        print(f"\nTest file ready to listen to:\n  {out}")
    else:
        out = f"podcast_{key}{suffix}.mp3"
        print(f"\nNext: assemble the episode (no speed-up for ElevenLabs):\n"
              f"  TEMPO=1.0 LOUDNORM=-20 python3 build/rebuild.py {work} {work}/{out}")


if __name__ == "__main__":
    main()
