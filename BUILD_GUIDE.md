# Biergerpakt Podcast — Build Guide & Project State

This file is the single source of truth for continuing work on this project in a new session.

## What this project is

A static website for the **Biergerpakt Podcast**: short, friendly audio episodes (hosts **Anna** + **Tom**) explaining Luxembourg public services / initiatives in simple English, with a **synced read-along transcript**, a **language switcher (EN / FR / DE / LB)**, and a **5-question quiz** per episode that yields a printable certificate.

Open `index.html` in a browser — it's a static site, no server needed.

## Files

- `index.html` — page structure + CSS (registration, episode list, player+transcript, quiz, results, certificate).
- `app.js` — all logic (episode rendering, audio↔transcript sync, language toggle, quiz, certificate).
- `episodes_data.js` — `const EPISODES = [ ... ];` the data for every episode (see schema below). Episodes render dynamically from this array, so adding an entry is all that's needed to publish an episode.
- `podcast_<key>.mp3` — audio for each episode (English voices only).
- `podcast_script_<key>.md` — English script. `_fr.md` / `_de.md` / `_lb.md` — translations.
- `favicon.svg`, `gov-light.svg` — branding.
- `build/` — reusable build scripts (see "Tooling").
- `episodes_data.*.js` (backup.js / prevsync.js / prelb.js) — old backups; harmless. iCloud blocks `rm` from bash; delete via Finder if wanted.

## Episodes (15 so far)

id:key — 1:myguichet, 2:dsp_cns, 3:eltereforum, 4:benevolat, 5:lualert, 6:luxtrust, 7:maison_orientation, 8:infosenior, 9:accessibilite, 10:zukunftskeess, 11:fns, 12:granderegion, 13:digitalinclusion, 14:onis, 15:workinluxembourg.

Episodes 1–8 predate this workflow (timestamps were forced-aligned). Episodes 9–15 were built with the workflow below.

## episodes_data.js — per-episode schema

```
{
  id, key, number ("Episode N"), title, description,
  audio ("podcast_<key>.mp3"), duration (seconds, float),
  topics: [8 short strings],
  segments:    [ {speaker:"Anna"|"Tom", text, t} ],   // EN, SENTENCE-level, t = start sec
  segments_fr: [ {speaker, text, t} ],                 // FR, TURN-level
  segments_de: [ ... ],                                // DE, TURN-level
  segments_lb: [ ... ],                                // LB, TURN-level
  questions: [ {text, options:[4], correct:0-3, explanation} x5 ]
}
```

- EN `segments` are sentence-level (fine-grained karaoke highlight).
- FR/DE/LB segments are TURN-level (one entry per Anna/Tom turn), timestamped to the start of that turn. Audio is always English; translated transcripts are "read along" (app shows a note). `app.js > segmentsForLang()` picks the array by language.

## Script format (`.md`)

```
# Podcast Script — "Title"

**Part of the Biergerpakt programme**
**Hosts:** Anna (woman) and Tom (man)
**Length:** about NN minutes — spoken slowly, in simple English

---

**ANNA:** ...one turn, one line...
**TOM:** ...

---

*Sources: ... (attribute official sources; figures dated; "General information only")*
```

Rules: alternating-ish Anna/Tom turns, each turn ONE line, warm spoken simple English. Translations keep the SAME number of turns one-to-one (FR uses French typography `**ANNA :**` with a space; DE/LB use `**ANNA:**`). Spelled-out URLs: "dot"→ FR "point" / DE+LB "Punkt". "in simple English" → "en français simple" / "in einfachem Deutsch" / "an einfachem Lëtzebuergesch".

## How to add a NEW episode (full workflow)

1. **Research first** the official website the user names (WebSearch + web_fetch; gov sites are often JS-rendered — fetch guichet.public.lu equivalents or use search results). Get accurate facts/figures; attribute and date them.
2. **Write the EN script** `podcast_script_<key>.md` in the format above (~14–15 min ≈ 85–95 turns).
3. **Generate audio (PCM method — sample-accurate, NO drift):**
   - `python3 build/tts_generate.py <key>` → renders each sentence with edge-tts (Anna=en-US-JennyNeural, Tom=en-US-GuyNeural, rate -6%), resumable, into `/tmp/<key>_seg/`, writes `meta.json`. Run repeatedly until "ALL SEGMENTS DONE" (each call ~45s; files persist in /tmp within a session).
   - `python3 build/rebuild.py /tmp/<key>_seg /tmp/<key>_seg/podcast_<key>.mp3` → concatenates in raw PCM (GAP=0.14s, TEMPO=1.08, ENC_DELAY=0.05) and writes `segdata_fixed.json` (EN segments + exact duration). ⚠️ NEVER concatenate the per-sentence mp3s with ffmpeg stream-copy (`-c copy`) — it adds ~50ms per join → seconds of drift → highlight runs ahead. PCM concat fixes this.
4. **Translate** to FR, DE, LB (subagents or inline): write `_fr.md` `_de.md` `_lb.md`, same turn count.
5. **Inject** with `build/inject_episode.py` pattern (or inline python): build EN segments from `segdata_fixed.json`; build FR/DE/LB TURN-level segments via the run-starts mapper in `build/lib_segments.py`; append episode dict with 8 topics + 5 quiz Qs; write `episodes_data.js`; copy mp3 into project folder.
6. **Validate:** `node --check app.js`; load EPISODES in node and confirm `duration` ≈ actual mp3 (`ffprobe`), and `segments/_fr/_de/_lb` all present; last EN segment `t` should be ~1–2s before duration.

## Tooling (in `build/`)

- `rebuild.py` — sample-accurate audio assembler + EN timestamps (CORE; do not lose).
- `tts_generate.py` — resumable per-sentence edge-tts generator (writes meta.json).
- `lib_segments.py` — `turns_of(md)`, `run_starts(segs)`, `build_turns(segs, turns)` helpers for FR/DE/LB segment alignment.

edge-tts install (sandbox): `pip install edge-tts --break-system-packages`; binary at `/sessions/.../.local/bin` (add to PATH). ffmpeg/ffprobe preinstalled.

## Path mapping (sandbox bash ↔ file tools)

- Project (file tools): `/Users/jb/Library/Mobile Documents/com~apple~CloudDocs/Claude projects/Podcast myguichet/Podcast myguichet/`
- Project (bash): `/sessions/<id>/mnt/Podcast myguichet/`
- `/tmp` is sandbox-only and is NOT guaranteed to persist to a new session — regenerate segment audio if `/tmp/<key>_seg/` is gone.

## Conventions / gotchas

- Audio is English only. Translations are read-along transcripts.
- TURN-level mapper handles the rare case where the same speaker talks twice in a row (e.g. myguichet) by reusing the previous run's start time.
- Promotional sources (e.g. workinluxembourg rankings): attribute claims to their publisher; don't state as fact.
- Git auto-commits in this environment (commits named "update"); working tree is usually clean.
- iCloud sync: bash `rm` may be blocked on this folder; use Read to pull cloud-only files.

## Multilingual audio + full-site i18n (added 2026-06-16)

The site is now navigable in **EN / FR / DE / LB** via one global toggle in the header (plus the transcript toggle — both call `setLang()`). Switching language swaps **everything together**: UI chrome, episode title/description/topics, audio track, transcript, quiz, and certificate.

- **Native FR/DE audio** (test episodes `myguichet`, `dsp_cns`): generated with `build/tts_lang.py <key> <fr|de>` (voices fr=Denise/Henri, de=Katja/Conrad, rate -6%), assembled with `build/rebuild.py` exactly like EN. Produces `podcast_<key>_<lang>.mp3` + sentence-level `segdata_fixed.json`.
- **No Luxembourgish TTS voice exists** in edge-tts. LB stays **read-along**: LB selected → plays the English audio with the turn-level LB transcript and shows the read-along note. Same fallback applies to any language/episode with no native track (e.g. episodes 3–15 in FR/DE/LB).
- **Per-episode data fields** added for localized episodes: `audio_fr/audio_de`, `duration_fr/duration_de`, sentence-level `segments_fr/segments_de` (synced to their own audio; `segments_lb` stays turn-level on EN audio), and `title_/description_/topics_/questions_` + `_fr/_de/_lb`. All have English fallback in `app.js`, so untranslated episodes just show English.
- **app.js**: `I18N` table holds all UI strings (56 keys × 4 langs); `t(key,vars)` resolves with EN fallback. `applyLang()` updates every `[data-i18n]` / `[data-i18n-ph]` element and re-renders the active screen. `audioForLang()` / `hasNativeAudio()` pick the track and decide whether to show the read-along note.
- **index.html**: static strings carry `data-i18n` / `data-i18n-ph`; header has `#lang-switch-global`.
- **Reproduce / extend translations**: `build/lang_translations.json` (content) + `build/inject_lang.js` (merges audio + segments + content into `episodes_data.js`). To localize more episodes: add their native audio (tts_lang.py), add their content block to `lang_translations.json`, extend the `TARGETS` array in `inject_lang.js`, and run `node build/inject_lang.js`.
- **Validate**: `node --check app.js episodes_data.js`; a jsdom smoke test (register → switch langs → audio src per lang → quiz → certificate) is the recommended check.
