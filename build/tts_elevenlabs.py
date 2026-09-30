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
# General rule (Jacques, 2026-09-30): a web address ending in .lu is always spoken
# "... dot L-U" (letters), never "lu" like the French word. Covers written addresses
# (biergerpakt.lu, MyGuichet.lu, guichet.public.lu/...) and spelled-out ones already in the
# scripts ("cae dot lu", "fns point lu", "Punkt lu").
def _dot_lu(word):
    return [(r"(\w)\.lu\b", r"\1 " + word + " L-U"),
            (r"\b(" + word + r") lu\b", r"\1 L-U")]

PRONUNCIATION = {
    "en": _dot_lu("dot"),
    "fr": _dot_lu("point"),
    "de": _dot_lu("Punkt"),
    "lb": _dot_lu("Punkt"),
}


def spoken(text, lang):
    text = text.replace("**", "")
    for pat, rep in PRONUNCIATION.get(lang, []):
        text = re.sub(pat, rep, text)
    return text


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
    for p in parts:  # glue punctuation-only fragments (a lone ») onto the previous sentence
        if re.search(r'[0-9A-Za-zÀ-ÿ]', p) or not merged:
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
    if cost > CONFIRM_ABOVE and not confirmed:
        print(f"This run would use more than {CONFIRM_ABOVE:,} credits. Re-run with --yes to proceed.")
        sys.exit(0)

    for n, s in enumerate(todo, 1):
        audio = request("POST", f"/text-to-speech/{vids[s['speaker']]}", api_key, s["body"],
                        query="?output_format=mp3_44100_128")
        if len(audio) < 500:
            die(f"empty audio for: {s['text'][:60]}")
        tmp = s["cache"] + ".part"
        open(tmp, "wb").write(audio)
        os.replace(tmp, s["cache"])
        if n % 10 == 0 or n == len(todo):
            print(f"  generated {n}/{len(todo)}")

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
