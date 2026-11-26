# Biergerpakt Podcast — Build Guide & Project State

This file is the single source of truth for continuing work on this project in a new session.

## What this project is

A static website for the **Biergerpakt Podcast**: short, friendly audio episodes (hosts **Anna** + **Tom**) explaining Luxembourg public services / initiatives in simple English, with a **synced read-along transcript**, a **language switcher (EN / FR / DE / LB)**, and a **5-question quiz** per episode that yields a printable certificate.

Open `index.html` in a browser — it's a static site, no server needed.

## Hosting

The site is served by **Railway** (project "proactive-fulfillment", service `bp-podcast`), auto-deployed from the GitHub repo `jinesch75/bp-podcast` (branch `main`) on every push. Live URL: https://bp-podcast-production.up.railway.app/ — GitHub Pages is NOT used. If a push doesn't show up, check the Railway dashboard: when deploys are paused ("Limited Access"), the site stays online with the last successful deployment.

## Quiz quality (added 2026-09-30)

- **Answer positions:** `node build/balance_quiz_answers.js --write` spreads the correct answers evenly over A–D (max 2× the same letter per episode; ~25% each overall) and applies the same reordering to `questions`, `questions_fr`, `questions_de`, `questions_lb`. Deterministic and idempotent. Run it after adding a new episode's quiz.
- **No "longest answer" giveaway:** wrong answers are written to be as long and specific as the right one. Source of truth: `build/quiz_distractors/*.json` (per episode, per question, the 3 wrong answers in A→D order, per language); `node build/apply_quiz_distractors.js --write` puts them into `episodes_data.js` and reports how often the correct answer is still the longest (target ≈ 25%; 2026-09-30: EN 29%, FR 22%, DE 24%, LB 20%). For a new episode, add its wrong answers to a JSON file there.
- After either script: `node build/bump_version.js` and `node build/make_review.js <keys>`.

## Browser caching (added 2026-09-29)

File names never change, so browsers may keep playing/using an old cached copy after a deploy. Two safeguards:
- **Audio:** `audioForLang()` in `app.js` requests `podcast_<key>[_<lang>].mp3?v=<duration>`. A re-recorded mp3 always gets a new duration, so no manual step is needed.
- **Data + code:** `index.html` loads `episodes_data.js?v=…` and `app.js?v=…`. After changing either file, run `node build/bump_version.js` (update_audio_elevenlabs.js does it automatically), then `node build/make_review.js <key>` for review pages you share.

## Files

- `index.html` — page structure + CSS (registration, episode list, player+transcript, quiz, results, certificate).
- `app.js` — all logic (episode rendering, audio↔transcript sync, language toggle, quiz, certificate).
- `episodes_data.js` — `const EPISODES = [ ... ];` the data for every episode (see schema below). Episodes render dynamically from this array, so adding an entry is all that's needed to publish an episode.
- `podcast_<key>.mp3` — audio for each episode (English voices only).
- `podcast_script_<key>.md` — English script. `_fr.md` / `_de.md` / `_lb.md` — translations.
- `favicon.svg`, `gov-light.svg` — branding.
- `build/` — reusable build scripts (see "Tooling").
- `episodes_data.*.js` (backup.js / prevsync.js / prelb.js) — old backups; harmless. iCloud blocks `rm` from bash; delete via Finder if wanted.

## July 2026 rework (episodes 1–5) + review pages

- Episodes 1–5 rebuilt from the user's reworked EN scripts (`Biergerpakt_Podcast_Scripts_All_Episodes_EN_2026-07-07.docx`): new intro (long Biergerpakt paragraph naming the Ministry of Family Affairs...) and new outro (Biergerpakt activities promo). Order swapped to match the doc: **2 = benevolat, 4 = dsp_cns** (ids + numbers + array order swapped). FR/DE/LB retranslated, EN/FR/DE audio re-recorded, quizzes fixed (see `build/en_content_ep1_5_2026-07.json`, `build/tr_new_{fr,de,lb}.json`, `build/inject_ep1_5_2026-07.js`).
- EN `.md` scripts of ALL other episodes got the new intro/outro applied (scripts + Word doc only — their audio/segments/translations are NOT yet updated; do this per-episode later like eps 1–5).
- **Review pages**: `node build/make_review.js key1,key2` generates fully isolated per-episode pages under `review/<key>-<token>/` (one-episode `episodes_data.js` slice; app.js/svg/audio referenced from root via `../../`; tokens persist in `build/review_tokens.json`). Live at `https://bp-podcast-production.up.railway.app/review/<slug>/` after push.

## Episodes (55 so far)

(Clarvia (ex-42) was removed from the site on 30 Sept 2026 at Jacques's request; its scripts and build files are kept in `archive/clarvia/` — the audio there is git-ignored.)

(+ 40:lll — lifelong-learning.lu, a longer ~10-min episode, tagged `work`. + 41:cnap — Pensiounskeess/CNAP pension system, ~16-min, tagged `seniors,social,crossborder`, native EN/FR/DE audio + LB read-along.)

id:key (order changed Sept 2026, `build/reorder_episodes.js`) — 1:myguichet, 2:luxtrust, 3:benevolat, 4:eltereforum, 5:digitalinclusion, 6:workinluxembourg, 7:dsp_cns, 8:lualert, 9:maison_orientation, 10:infosenior, 11:accessibilite, 12:granderegion, 13:adem, 14:zukunftskeess, 15:fns, 16:onis, 17:habitat, 18:klima, 19:snj, 20:enfance, 21:cepas, 22:fondseuropeens, 23:zesumme, 24:cgdis, 25:statec, 26:environnement, 27:syvicol, 28:research, 29:agriculture, 30:amenagement, 31:aaa, 32:geoportail, 33:govcert, 34:culture, 35:demenz, 36:ess, 37:luxinnovation, 38:logement, 39:space, 40:lll, 41:cnap, 42:ebl, 43:letzprepare, 44:dondusang.

Batch tip: episodes 19-23 were built five at a time. `build/tts_batch.py` now also generates English (pass langs as 4th arg, e.g. `python3 build/tts_batch.py 40 snj,enfance,cepas en,fr,de`). Content for a batch: one `new_content_en.json` (with a `categories` field per episode) + two subagents → `tr_new_fr.json`/`tr_new_de.json`, then `build/inject_5.js`.

Episodes 1–8 predate this workflow (timestamps were forced-aligned). Episodes 9–16 were built with the workflow below. ADEM (16) was the first episode built end-to-end with native EN/FR/DE audio + full content translation + topic tag from the start; see `build/inject_adem.js` and `build/adem_content.json` for the per-episode pattern (it also builds `segments_lb` via `lib_segments` for read-along data).

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

## Topic tags + filter (added 2026-06-16)

Each episode has a `categories` array of tag ids. The episode-list screen shows a topic dropdown (SINGLE-select; "All topics" clears) above a compact list with one row per episode (number + title; the description is only a hover tooltip, and tags are no longer shown on the rows — simplified 2026-11-17). Tags + filter labels + the "{n} of {total} episodes" count are localized.

- **Where things live:** the taxonomy is `CATEGORIES` in `app.js` (id + en/fr/de label, ordered). Per-episode tags are `ep.categories` in `episodes_data.js`. Filter UI markup is the `.filter-row` block (`#filter-select` / `#filter-count`) in `index.html` (CSS: `.filter-select`, `.ep-row`). Logic: `renderFilterBar()`, `episodeMatchesFilter()`, `selectedCat` (single id or null) in `app.js`; `renderEpisodeList()` filters + renders the rows + count.
- **Current categories:** digital, social, housing, energy ("Environment & energy"), research ("Research & innovation"), agriculture ("Agriculture & food"), culture ("Culture & arts"), work, family, health, seniors, inclusion, safety, civic, crossborder. (`culture` added with ep 34.) A category option only appears once ≥1 episode uses it. (`housing` added with ep 17; `energy` added with ep 18 Klima-Agence and relabelled to "Environment & energy" when the emwelt.lu episode 26 joined it; `research` added with ep 28 Research Luxembourg.)
- **To re-tag or add an episode's tags:** edit `build/inject_tags.js` (the `TAGS` map) and run `node build/inject_tags.js`, or set `categories: [...]` directly in the episode dict. To add a NEW category, add an entry to `CATEGORIES` in `app.js` (with fr/de labels) and tag episodes with its id. When adding a new episode, give it a `categories` array too.

## Multilingual audio + full-site i18n (added 2026-06-16)

**One toggle (header), EN / FR / DE** (`setSiteLang()`). It drives EVERYTHING together: UI chrome, audio track, episode title/description/topics, quiz, certificate, AND the transcript. The transcript always shows the chosen UI language only (`segmentsForScript` keys off `currentLang`). There is no separate script-language switcher.
- **Luxembourgish is not displayed** anywhere (no LB site language, no LB script toggle), but the LB data is intentionally KEPT in `episodes_data.js` (`segments_lb`, and `title_lb`/etc. on episodes 1-2) in case it's wanted later. To re-enable an LB read-along, restore a script switcher and point `segmentsForScript` at `segments_lb`.
- Since every episode has native FR/DE audio, the transcript is always karaoke-synced to the audio (`isScriptSynced` stays true), so lines are click-to-seek and highlight. `isScriptSynced`, `LANG_NAMES`, `langName`, and the `lang_note_tmpl` strings remain in `app.js` as dormant helpers (no read-along note is shown while every episode has native audio).
- History: this was briefly a two-toggle design (site language + separate EN/FR/DE/LB script switcher). Per user request (2026-06-16) the script switcher was removed so the transcript simply mirrors the UI language.

- **Native FR/DE audio for ALL 15 episodes** (completed 2026-06-16): voices fr=Denise/Henri, de=Katja/Conrad, rate -6%; assembled with `build/rebuild.py` exactly like EN → `podcast_<key>_<lang>.mp3` + sentence-level `segdata_fixed.json`. Generators: `build/tts_lang.py <key> <fr|de>` (single) or `build/tts_batch.py` (parallel, 8 workers, resumable, with a wall-clock budget arg — used for episodes 3-15). NOTE: `tts_batch.py`'s sentence splitter merges punctuation-only fragments (e.g. a lone `»`) into the previous sentence so edge-tts never gets an empty segment.
- **FR/DE content for all 15 episodes** (title/description/topics/quiz): `build/lang_translations.json` (eps 1-2) + `build/lang_translations_3_15.json` (eps 3-15). Injected via `build/inject_lang.js` (1-2) and `build/inject_3_15.js` (3-15). Episodes 3-15 were translated by subagents from `en_content_*.json` extracts.
- **No Luxembourgish TTS voice exists** in edge-tts. LB stays **read-along**: LB selected → plays the English audio with the turn-level LB transcript and shows the read-along note. Same fallback applies to any language/episode with no native track (e.g. episodes 3–15 in FR/DE/LB).
- **Per-episode data fields** added for localized episodes: `audio_fr/audio_de`, `duration_fr/duration_de`, sentence-level `segments_fr/segments_de` (synced to their own audio; `segments_lb` stays turn-level on EN audio), and `title_/description_/topics_/questions_` + `_fr/_de/_lb`. All have English fallback in `app.js`, so untranslated episodes just show English.
- **app.js**: `I18N` table holds all UI strings (56 keys × 4 langs); `t(key,vars)` resolves with EN fallback. `applyLang()` updates every `[data-i18n]` / `[data-i18n-ph]` element and re-renders the active screen. `audioForLang()` / `hasNativeAudio()` pick the track and decide whether to show the read-along note.
- **index.html**: static strings carry `data-i18n` / `data-i18n-ph`; header has `#lang-switch-global`.
- **Reproduce / extend translations**: `build/lang_translations.json` (content) + `build/inject_lang.js` (merges audio + segments + content into `episodes_data.js`). To localize more episodes: add their native audio (tts_lang.py), add their content block to `lang_translations.json`, extend the `TARGETS` array in `inject_lang.js`, and run `node build/inject_lang.js`.
- **Validate**: `node --check app.js episodes_data.js`; a jsdom smoke test (register → switch langs → audio src per lang → quiz → certificate) is the recommended check.

## ElevenLabs voices (added 2026-09-28)

Jacques has an ElevenLabs Pro licence. `build/tts_elevenlabs.py` replaces edge-tts for new recordings and keeps the same pipeline (per-sentence mp3 + `meta.json` → `build/rebuild.py` PCM assembly → sample-accurate `segdata_fixed.json`).

- **API key:** `ELEVENLABS_API_KEY=...` in `.env` at the project root. `.env` is git-ignored (the repo is PUBLIC) — never commit it, never paste the key in chat.
- **Hosts (native voice per language, chosen by Jacques 2026-09-29):** EN Anna = **Elizabeth**, Tom = **James** · FR Anna = **Lucie**, Tom = **Marcel** · DE Anna = **Lola**, Tom = **Benjamin** ("Efficient & Intelligent Agent"; replaced Felix 2026-09-30, used for all German episodes) · LB falls back to the English pair. Resolved by name from "My Voices" (library voices must be added to My Voices first). Per-language overrides in `.env`: `ANNA_VOICE_FR=…` / `TOM_VOICE_ID_DE=…` etc.
- **Model:** `eleven_multilingual_v2` for en/fr/de (with previous/next-sentence context for natural flow); `eleven_v3` for **lb** — Luxembourgish is supported, so LB can get native audio for the first time (have a native speaker check it).
- **Commands (run from project root):**
  - Test: `python3 build/tts_elevenlabs.py <key> <lang> --first 25` → `build/el_test/<key>_<lang>_first25.mp3` (≈1,400 credits).
  - Full: `python3 build/tts_elevenlabs.py <key> <lang> --yes`, then `TEMPO=1.0 LOUDNORM=-20 python3 build/rebuild.py /tmp/<key>[_<lang>]_el_seg /tmp/<key>[_<lang>]_el_seg/podcast_<key>[_<lang>].mp3`.
- **Pronunciation fixes:** all rules live in `build/pronunciation.py` (imported by `tts_elevenlabs.py`) and change only the text sent to ElevenLabs — transcripts keep the written form. They cover: `.lu` addresses always spoken as letters (EN "dot L-U", FR "point L-U", DE "Punkt L-U", also for spelled-out "cae dot lu"/"f-n-s point l-u"); letter acronyms written as "C-N-S" (CNS, FNS, SNJ, CNAP, CGDIS, ONE, AAA, DSP, EU/UE, ID, IT, AI/IA/KI …); word acronyms in normal case (ADEM→Adem, REVIS, ONIS, STATEC, SYVICOL, LISER …); emphasis capitals (NOT/PAS/NICHT…) lowered; phone numbers and 1-1-2 read digit by digit (FR says "cent-douze"); LU-Alert → "L-U Alert", GOVCERT.LU → "Gov-Cert dot L-U"; stage directions like *(laughs)* removed; "+" → "plus", "/" → "or/ou/oder"; FR "Äddi" → "Addi". Biergerpakt, MyGuichet, Guichet, LuxTrust, matricule and eSpace were approved by ear in MyGuichet and are left as written. `python3 build/pronunciation_report.py` writes `build/pronunciation_report.md` listing every affected sentence (all episodes, EN/FR/DE). Hard Luxembourgish names: A/B listening test with `python3 build/pron_names_test.py <en|fr>` → `build/el_test/pron_names_<lang>.mp3`; chosen spellings go in `NAMES`. Chosen 2026-09-30 — EN: Zukunftskeess → "Tsoo-koonfts-kayss", Pensiounskeess → "Pen-see-ouns-kayss" (Eltereforum, Info-Zenter Demenz, Zesumme Vereinfachen, Lëtzebuerg, CePAS, Kannergeld as written); FR: Zukunftskeess → "Tsoukounftskéss", Pensiounskeess → "Pènnsiounskéss", Eltereforum → "Eltèreu-forum", Zesumme Vereinfachen → "Tsézoumeu Fèraïnnfarènn" (Info-Zenter Demenz, Lëtzebuerg, Kannergeld as written); DE: all as written.
- **LOUDNORM=-20** for ElevenLabs: raw ElevenLabs voices differ a lot in level (James came out ~10 dB louder than Elizabeth). `rebuild.py` measures each sentence (EBU R128) and applies a gain so every sentence sits at -20 LUFS (true peak capped at -1.5 dBTP via `PEAK_MAX`). Gain only — no time change, so timestamps stay sample-accurate. -20 LUFS matches the existing edge-tts episodes. Off by default (edge-tts builds unchanged); the `--first` test turns it on automatically.
- **TEMPO=1.0** for ElevenLabs (no atempo speed-up; edge-tts episodes used 1.08). `rebuild.py` now reads `TEMPO` and `GAP` from the environment; defaults unchanged.
- **Cost:** ~1 credit per character; Pro = 600,000 credits/month. One episode ≈ 7–9k chars per language (MyGuichet EN+FR+DE ≈ 25k, +LB ≈ 33k). Full catalogue EN/FR/DE ≈ 1.2M. Runs above 3,000 credits need `--yes`.
- **Cache:** every sentence is stored in `build/el_cache/<hash>.mp3` (hash of voice+model+settings+text), so re-runs only pay for changed sentences. `build/el_cache/` and `build/el_test/` are git-ignored.
- **Re-recording an EXISTING episode (text unchanged):** after tts_elevenlabs.py + `TEMPO=1.0` rebuild.py for each language, run `node build/update_audio_elevenlabs.js <key> en,fr,de`. It verifies speakers/texts are identical to the live data (aborts otherwise), copies the mp3s into the root, updates durations + timestamps only (titles, quizzes, LB untouched), and backs up to `episodes_data.pre_el_<key>.js`. Then `node build/make_review.js <key>` to refresh the review page. `segments_lb` keeps its old timestamps (turn-level, timed to the old English audio); harmless while Luxembourgish is not shown on the site, but re-time it if LB is re-enabled. First used for MyGuichet (ep 1) on 2026-09-29: EN 7:39, FR 7:48, DE 8:25.

## Fact-check (30 Sept 2026, episodes 1–13)

Episodes 1–13 were checked against the official websites; Jacques approved all suggestions (list: project doc `claude/factcheck_episodes_1-13_2026-09-30.md`). Applied with `build/apply_factcheck_2026_09.py` (EN/FR/DE/LB `.md` scripts, turn counts unchanged) and `build/apply_factcheck_quiz_2026_09.js` (quiz text only). Both are idempotent. Transcripts in `episodes_data.js` were NOT changed, because they must match the recorded audio: re-record the affected episodes (all of 1–13 except Eltereforum and Maison de l'orientation) to bring audio + transcripts in line with the scripts. `pronunciation.py` now also reads e-mail addresses (`@` → at / arobase), 247-86000 digit by digit, and SIMPA/COMPA as words.

## Re-recording after script changes + "in progress" status (30 Sept 2026)

- `python3 build/el_run_batch.py <key,key,...> en,fr,de [--budget 165]` generates + assembles many episodes in one go (parallel requests, `EL_CONCURRENCY`, default 6); it stops before the time budget and resumes where it left off (state in `/tmp/el_batch_state.json`). `tts_elevenlabs.py --estimate` prints the credits a run needs without generating.
- `node build/replace_audio_elevenlabs.js <key,key> en,fr,de` puts a re-recording on the site when the SCRIPT CHANGED: it checks the recording matches the current `.md` scripts, copies the mp3s, replaces `segments`/`segments_fr`/`segments_de` (text + timings) and durations, and rebuilds `segments_lb` from the LB script on the new English audio. (`update_audio_elevenlabs.js` is only for unchanged text.)
- ElevenLabs API key "Biergerpakt podcast" has its own credit limit (100,000). When it is used up, the API answers `quota_exceeded`; raise the key's limit in ElevenLabs (Developers → API keys) and re-run the batch.
- `status: "in_progress"` on an episode shows an "In progress" badge on its card and a notice on its page (EN/FR/DE/LB strings `status_in_progress`, `in_progress_note` in `app.js`). Set/clear with `node build/set_status.js in_progress|final <from>-<to> | key,key`. Re-recorded with ElevenLabs (EN/FR/DE, final): episodes 1–13 (30 Sept 2026). Episodes 14–41 re-recorded with ElevenLabs on 9 Nov 2026 (final). All 41 episodes now have ElevenLabs EN/FR/DE audio. (voices to be done later).

## Audio quality pass (30 Sept 2026) — applies to every ElevenLabs recording

Jacques heard a "fade-in" at the start, slightly cut sentence transitions (mostly French) and odd "Ah/Exactly" moments. Causes and fixes, now built into the pipeline (`el_run_batch.py` uses them automatically):
- `rebuild.py CLEAN=1 OUT_SR=44100`: 0.6 s of silence before the first word (players/Bluetooth swallowed the start); stray bits of the neighbouring word that ElevenLabs sometimes adds at a sentence edge are removed; silences trimmed with short fades; even pauses (`GAP_SAME` 0.28 s within a turn, `GAP_TURN` 0.42 s at a speaker change); full 44.1 kHz output.
- `tts_elevenlabs.py`: very short sentences ("Exactly.", "Ah.", "Oui.", "Genau.") are recorded together with the next sentence of the same turn (`EL_MERGE_SHORT`); German dates ("am 28. Mai 2019") are no longer split after the day; sentences whose ending is cut off are re-recorded with another seed (`EL_FIX_CUTS`, cached in `el_cache/cut.json`, choices in `el_cache/reseed.json`).
- Listening check (`EL_ASR`, needs `pip install faster-whisper`): every sentence is transcribed (whisper "base", confirmed with "small") and compared with the text; added/dropped/garbled words are re-recorded (up to 3 seeds). It caught e.g. an invented "Jamais !" in French LuxTrust. Transcripts are cached in `el_cache/asr.json`. Sentences it still doubts are listed in `/tmp/el_check_by_ear.txt` — so far all were recognition mistakes (e.g. "Parents forts" heard as "Par en fort", place names), not audio errors.
- Episodes 1–13 were re-recorded with all of this (EN/FR/DE). Episodes 14–41 remain "in progress".

## Ministry name (30 Sept 2026, set by Jacques)

FR: "Ministère de la Famille, des Solidarités, du Vivre ensemble et de l'Accueil" · DE: "Ministerium für Familie, Solidarität, Zusammenleben und Unterbringung von Flüchtlingen" · EN: "Ministry of Family Affairs, Solidarity, Living Together and Reception of Refugees". Applied to all FR/DE scripts (EN already matched); French and German audio of episodes 1–13 re-recorded. LB scripts keep their Luxembourgish wording.

## Fact-check MyGuichet (2 Nov 2026)

Checked against official sites; Jacques approved all three changes: (1) business part — VAT returns are filed on eCDF, so now "declaring their staff to social security, checking their VAT account, or applying for a business permit"; (2) new AI assistant on Guichet.lu (gouvernement.lu, 6 July 2026), added to Anna's help line; (3) eID card usable with a smartphone via the GouvID app (ctie.gouvernement.lu). Applied with `build/apply_factcheck_myguichet_2026_11.py` (EN/FR/DE/LB, turn counts unchanged, idempotent). `pronunciation.py`: GouvID → "Gouv I-D". Re-recorded with `el_run_batch.py myguichet en,fr,de` (only 19 changed sentences regenerated, ≈2,600 credits) and put live with `replace_audio_elevenlabs.js`. New durations: EN 7:49, FR 8:11, DE 9:12. Quiz unchanged. iCloud may evict files (`Resource deadlock avoided`): stage them once to download, then retry.

## Fact-check LuxTrust (2 Nov 2026)

Checked against luxtrust.com (and Spuerkeess for 3D Secure); Jacques approved all seven changes: data stored in EU data centres (not "in Luxembourg"); summary safety line now matches line 121 (no "access your devices"); "qualified" EU provider since 2005 (not "certified by the EU… about twenty years"), summary + quiz Q1 to match; exact prices (app €47, Scan from €105, SmartCard from €129, 3 years); in-person identification at LuxTrust, a partner such as your bank, or a notary (quiz Q4 explanation; correct option shortened to "in person, or remotely by video identification" so it isn't the longest); app activation about 5 minutes; "most popular" → "simplest" (not stated officially) — also in MyGuichet line 55. Scripts: `build/apply_factcheck_luxtrust_2026_11.py`; quiz: `build/apply_factcheck_quiz_2026_11.js --write` (LuxTrust has no LB quiz). Re-recorded EN/FR/DE of both episodes (changed sentences only, ≈7,400 credits). LuxTrust now EN 11:13, FR 10:33, DE 12:35.

## Fact-check Volunteering (2 Nov 2026)

No errors found (benevolat.lu, STATEC Regards 10/24, luxembourg.public.lu, gouvernement.lu). Jacques approved three optional additions: smart matching also sends mission suggestions by email (benevolat.lu, 01.06.2026); the 12th field "Association board" added to the list; EN "International Volunteer Day" (UN name). Script: `build/apply_factcheck_benevolat_2026_11.py`. Quiz unchanged. Re-recorded EN/FR/DE (changed sentences only, ≈1,700 credits): EN 7:37, FR 7:01, DE 8:40.

## Fact-check Digital Inclusion (2 Nov 2026)

The menu page "How to apply for a free second-hand computer" (digital-inclusion.lu/get-a-free-second-hand-computer/) is now authoritative; the older /get-a-free-computer/ page (one laptop per household) is still online but no longer in the menu. Applied (Jacques approved): eligibility incl. collective debt settlement and 'vie privée' permit; since 22.09.2025 every household member 12+ can get their own computer (if donations allow), adults apply themselves, a parent applies for teenagers (one minor at a time); waiting time worded without a figure ("the website always shows the current waiting time") — Jacques prefers no figures that go stale; donations: laptops erased/disk returned, smartphones/tablets factory-reset first; Open Classroom also helps with LuxTrust/MyGuichet and free scanning/printing; removed unverified "over two thousand machines in a single recent year". Kept "more than ten thousand" and the refugee volunteers line (confirmed by Jacques). Script: `build/apply_factcheck_digitalinclusion_2026_11.py`; quiz Q3 explanation via `build/apply_factcheck_quiz_2026_11.js`. Re-recorded EN/FR/DE (changed sentences only, ≈4,900 credits).

## Fact-check Work in Luxembourg (2 Nov 2026)

Applied (Jacques: "apply all"): "Live here" contents (housing is under "Get started"); "~11,000 candidates" (no longer published) → profiles pre-screened by ADEM; Job Board focuses on shortage occupations, other jobs via EURES; shortage jobs: no local search first, ADEM green light within a few days; durable figures instead of dated ones ("around three quarters", "more than two hundred thousand", "among the safest", "among the very best"). Script: `build/apply_factcheck_workinluxembourg_2026_11.py`; quiz Q3 via `build/apply_factcheck_quiz_2026_11.js`. Re-recorded EN/FR/DE (changed sentences only, ≈5,300 credits).

**Standing rule (Jacques, 2 Nov 2026): avoid precise figures that go stale within months** (counts, percentages, rankings, waiting times) — use rounded, durable wording or point to the website.

## Fact-check Your health / DSP & CNS (9 Nov 2026)

Applied (Jacques: "apply all suggestions"): "about half of doctors" → "more and more doctors and dentists" (PID); eSanté activation on MyGuichet.lu web/app with LuxTrust or Luxembourg eID (no postal code), otherwise eSanté portal / MyDSP; DSP opens in the MyGuichet eSpace; block access to certain documents + close DSP any time; organ donation wishes in the DSP; no stamp needed from inside Luxembourg + CNS letterboxes; children under 18 usually pay nothing for doctor visits. Script: `build/apply_factcheck_dsp_cns_2026_11.py`; quiz Q3/Q5 explanations via `build/apply_factcheck_quiz_2026_11.js`. Re-recorded EN/FR/DE (changed sentences only, ≈5,200 credits).

## Fact-check LU-Alert (9 Nov 2026)

Applied (Jacques: "apply all suggestions"): sirens now "warn of a serious danger, locally or nationwide" with the steady / rising-and-falling signals (lu-alert.lu Sirens page; the channel overview page still says "only nuclear" — flagged for the administration's review); app: less serious warnings in principle only via app + website, choose alerts and places of interest; Cell Broadcast shows even on silent with a loud sound; keep phone software up to date; CB languages (always French + EN/DE by phone language); some tests need "LU-Alert Test" / app "Test" switched on; dropped "can't really opt out". Script: `build/apply_factcheck_lualert_2026_11.py`; quiz Q2/Q4 via `build/apply_factcheck_quiz_2026_11.js`. Re-recorded EN/FR/DE (changed sentences only, ≈6,600 credits).

Note (Jacques, 9 Nov 2026): after these fact-checks, every episode's script is also sent to the respective administration by email so its experts can double-check it.

## Fact-check Maison de l'Orientation (9 Nov 2026)

Applied (Jacques: "apply all suggestions"): Espace orientation hours 10:00–17:00 (page of 31.08.2026; the general page of 22.01.2026 still says 8:00–17:00 — flag for the expert review); e-mail info@maison-orientation.public.lu (spoken "info, at, maison dash orientation dot public dot l-u"); website has a dash ("maison, dash, orientation, dot public dot l-u"); coaching up to 22, LU/FR/DE/EN, in person or online via MyGuichet.lu, confidential; event examples from the current agenda. Script: `build/apply_factcheck_maison_orientation_2026_11.py`; quiz Q2 explanation via `build/apply_factcheck_quiz_2026_11.js`. Re-recorded EN/FR/DE (changed sentences only, ≈4,600 credits).

## Fact-check Info-Seniors (9 Nov 2026)

No errors. Applied (Jacques: "apply all"): register "still growing" instead of "complete" (infosenior.public.lu says it is completed as data arrives); COMPA paid by the National Solidarity Fund, for approved care homes / supervised housing; ala help line 26 432 432 (24/7) — added "26 432 432" to PHONE_NUMBERS in `pronunciation.py` (read digit by digit); Red Cross service named Iris. Script: `build/apply_factcheck_infosenior_2026_11.py`. Quiz unchanged. Re-recorded EN/FR/DE (changed sentences only, ≈3,300 credits). FR "C'était notre épisode sur Info-Seniors." flagged "still cut" by the checker but is complete (unchanged audio).

## Fact-check Accessibility (9 Nov 2026)

Applied (Jacques: "apply all"): digital complaint procedure — organisation first (contact in its accessibility declaration), then the SIP (answers within a month) or the Ombudsman; OSAPS reporting also by phone, e-mail or WhatsApp photo (no numbers); financial aid — plan compliance check first, works finished by July 2031; new collective housing — one home in ten accessible. Script: `build/apply_factcheck_accessibilite_2026_11.py`. Quiz unchanged. Re-recorded EN/FR/DE (changed sentences only, ≈3,400 credits).

## Fact-check ADEM (9 Nov 2026)

No errors. Applied (Jacques: "apply all"): scams now include fake e-mails / social-media accounts and phishing for personal details (ADEM alerts 02.10.2026 and 09.09.2026), "don't pay, don't click, check ADEM's official channels"; login with LuxTrust or Luxembourg eID; unemployment benefit — ADEM's letter, then the application on MyGuichet.lu; Youth Guarantee — monthly counsellor meetings in the first six months; Club Emploi — CV and cover letter, CV photo, group workshops. Script: `build/apply_factcheck_adem_2026_11.py`. Quiz unchanged. Re-recorded EN/FR/DE (changed sentences only, ≈3,500 credits).

## Fact-check Zukunftskeess (9 Nov 2026) + first ElevenLabs recording

New law no. 8746 (voted 15 Oct 2026, in force 1 Jan 2027): family allowance +45 €/child/month and +15 € more from 12; back-to-school allowance 175 € (6–11) / 325 € (12+); indexation extended to birth, back-to-school and special supplementary allowances; children of a cross-border worker's spouse/partner (presumption if they mainly live with the worker). Jacques: "go ahead with all suggestions". Applied with `build/apply_factcheck_zukunftskeess_2026_11.py` (EN/FR/DE/LB, turn counts unchanged, idempotent; durable wording "more than…", no cents) and quiz Q2/Q4 + EN/FR/DE descriptions via `build/apply_factcheck_quiz_2026_11.js` (now also handles descriptions, list `D`). Also: payment certificate = online form on the CAE site; maintenance request for adult pupils now online on MyGuichet.lu; bank abroad may credit 1–2 days later. Whole episode recorded with ElevenLabs (`EL_STATE=/tmp/el_state_zuk.json python3 build/el_run_batch.py zukunftskeess en,fr,de`, ≈ 42,500 credits), put live with `replace_audio_elevenlabs.js`, status set to final. `el_run_batch.py` now accepts `EL_STATE` (the shared /tmp state file can be read-only from an older session). faster-whisper installed → listening check passed in EN/FR/DE (only the name line "The Zukunftskeess. cae.lu." flagged, expected). New durations: EN 14:54, FR 13:35, DE 16:06.

## Fact-check FNS (9 Nov 2026) + first ElevenLabs recording

Jacques: "apply all". Applied with `build/apply_factcheck_fns_2026_11.py` (EN/FR/DE/LB, idempotent, footers too) and EN/FR/DE descriptions via `apply_factcheck_quiz_2026_11.js` (quiz unchanged). Main points: no FNS procedure on MyGuichet.lu (forms by post or at the counter, 8-10 rue de la Fonderie, mornings; office social helps) → MyGuichet removed from line 135, summary and descriptions; 2026 AVC deadline sentence replaced (pre-filled form sent to last year's beneficiaries); amounts → "more than €1,800 a year for a single person"; planned complément vie chère (bill 8716, still in committee, planned 1 Jan 2027) mentioned as planned + "check fns.lu" — re-check when the law is voted; COMPA named; maintenance-advance conditions (court decision + failed bailiff attempt). Recorded with `EL_STATE=/tmp/el_state_fns.json python3 build/el_run_batch.py fns en,fr,de` (≈ 41,300 credits), listening check clean, put live with `replace_audio_elevenlabs.js`, status final. New durations: EN 13:49, FR 14:04, DE 15:58.

## Fact-check ONIS (9 Nov 2026) + first ElevenLabs recording

No new law. Main correction: ADEM first profiles REVIS applicants under 65 who can work; only people with specific activation needs are referred to ONIS (onis.gouvernement.lu, 04.08.2025) — added in lines 33, 69, 121, 165, quiz Q2/Q4 explanations and EN/FR/DE descriptions. Also: activation allowance for TUC work (based on minimum wage), sanctions (reduction/suspension), plan up to one year, temporary exemptions. Jacques: "apply all". `build/apply_factcheck_onis_2026_11.py` (EN/FR/DE/LB, idempotent) + `apply_factcheck_quiz_2026_11.js`. Recorded with `EL_STATE=/tmp/el_state_onis.json python3 build/el_run_batch.py onis en,fr,de` (≈ 39,400 credits), put live, status final. Listening check flagged only FR "Le REVIS a deux facettes." (ASR hears "revient"; check by ear at FR 1:12). New durations: EN 13:26, FR 12:28, DE 15:08.

## Fact-check episodes 17–21 (9 Nov 2026) + first ElevenLabs recordings

Jacques: "do the next 5 episodes" (applied directly, as all earlier suggestions had been approved). New shared helper `build/lib_factcheck.py` (`apply(key, CHANGES, NOTES)` replaces whole turns by index in EN/FR/DE/LB and appends a dated note to the sources footer; idempotent) used by `build/apply_factcheck_{habitat,klima,snj,enfance,cepas}_2026_11.py`. Quiz: habitat Q4, klima Q4 via `apply_factcheck_quiz_2026_11.js`. Recorded in one batch: `EL_STATE=/tmp/el_state_b5.json python3 build/el_run_batch.py habitat,klima,snj,enfance,cepas en,fr,de` (≈ 118,000 credits, listening check clean), put live with `replace_audio_elevenlabs.js habitat,klima,snj,enfance,cepas en,fr,de`, status final.
- 17 Observatoire de l'Habitat: Q3-2025 prices replaced by durable wording; STATEC partner; STATEC house price index; rents via a property portal; Géoportail; rent simulator. EN 9:47, FR 9:29, DE 11:02.
- 18 Klima-Agence: Klimabonus renewed 2026–2030 (Mobilitéit until 30.06.2030), PV subsidy deducted from invoice; full ministry names. EN 9:00, FR 9:06, DE 10:25.
- 19 SNJ: "more than sixty years"; national youth report + Youth Pact 2026–2030; sixth centre in Esch-sur-Alzette. EN 7:46, FR 7:30, DE 8:38.
- 20 ONE: hedged mention of youth-protection reform bill 7994 (still in Parliament). EN 7:10, FR 7:05, DE 8:09.
- 21 CePAS: "more than sixty years"; low-income school subsidy (SMFR) via SePAS + planned complément vie chère (bill 8716). EN 7:03, FR 6:39, DE 7:59.
⚠ Re-check FNS, CePAS (bill 8716) and ONE (bill 7994) when those laws are voted.

## Fact-check episodes 22–26 (9 Nov 2026) + first ElevenLabs recordings

Jacques: "do the next 5". All changes in `build/apply_factcheck_eps22-26_2026_11.py` (uses `lib_factcheck.py`; `build/show_turns.py <key> "phrase"…` prints the matching turns in EN/FR/DE/LB — /tmp is wiped when the VM restarts, keep helpers in build/). Quiz: CGDIS Q3 explanation. Batch: `EL_STATE=/tmp/el_state_b6.json python3 build/el_run_batch.py fondseuropeens,zesumme,cgdis,statec,environnement en,fr,de` (≈ 92,000 credits), put live, status final.
- 22 European funds: Interreg (Greater Region) added; next EU period from 2028 being prepared. EN 6:56, FR 6:47, DE 8:06.
- 23 Zesumme Vereinfachen: ministries/administrations can also post projects for feedback. EN 6:19, FR 6:19, DE 7:04.
- 24 CGDIS: wrong "more than 3,900 volunteers" → "thousands… about nine in ten firefighters are volunteers" (annual report 2025: 6,890 volunteers, 694 professionals); quiz explanation too. EN 8:24, FR 8:14, DE 9:29.
- 25 STATEC: no change (footer note only). EN 6:20, FR 6:06, DE 6:56.
- 26 Environment portal: emwelt.lu → environnement.public.lu; apps Meng Loft / Mäin Offall; adaptation strategy adopted 2026; "calls for projects for nature in towns" (not found) → national nature restoration plan. EN 6:29, FR 6:22, DE 7:08. FR listening check flags the "Null Offall Lëtzebuerg" sentence (2:16) — Luxembourgish name, check by ear.

## Fact-check episodes 27–31 (9 Nov 2026) + first ElevenLabs recordings

Jacques: "do the next 5 episodes". `build/apply_factcheck_eps27-31_2026_11.py`; quiz unchanged. Batch `EL_STATE=/tmp/el_state_b7.json python3 build/el_run_batch.py syvicol,research,agriculture,amenagement,aaa en,fr,de` (≈ 82,000 credits, listening check clean), put live, status final.
- 27 SYVICOL: founded 1986 added; 100 communes confirmed. EN 5:48, FR 5:45, DE 6:29.
- 28 Research Luxembourg: no change (six members confirmed). EN 6:13, FR 6:15, DE 7:04.
- 29 Agriculture: ALVA named (created 2022); PAN-Bio 2030 (2026–2030). EN 6:33, FR 6:39, DE 7:28.
- 30 Spatial planning: PDAT adopted 2023, horizon 2035. EN 5:48, FR 5:51, DE 6:33.
- 31 AAA: created 1902; MyGuichet declarations for work and school accidents; online appointments. EN 5:51, FR 5:45, DE 6:25.

## Fact-check episodes 32–36 (9 Nov 2026) + first ElevenLabs recordings

Jacques: "next 5". `build/apply_factcheck_eps32-36_2026_11.py`; quiz: GOVCERT Q2 and ESS Q3 explanations (in `build/apply_factcheck_quiz_2026_11.js`). Batch `EL_STATE=/tmp/el_state_b8.json python3 build/el_run_batch.py geoportail,govcert,culture,demenz,ess en,fr,de` (≈ 85,000 credits), put live, status final.
- Fix: the quiz script re-applied a substring edit when the new text contained the old one (habitat Q4 explanation had the STATEC sentence 3×). Now skips when the new text is already present; habitat repaired.
- 32 Geoportal: new 3D viewer since Dec 2025. EN 5:09, FR 5:15, DE 5:47.
- 33 GOVCERT.LU: NIS2 law of 5 May 2026 – GOVCERT.LU (HCPN) for the State and critical entities, CIRCL for other companies and communes. EN 5:46, FR 5:56, DE 6:31.
- 34 Culture portal: KEP 2018–2028; national action plan "Access to culture" (April 2026, to 2030); Kulturpass. EN 5:27, FR 5:24, DE 6:09.
- 35 Info-Zenter Demenz: more than 100 services; awareness campaigns + national prevention programme; in person in Luxembourg City and sometimes elsewhere. EN 5:29, FR 5:22, DE 6:15.
- 36 Social and solidarity economy: SIS since 2016, approved by the Ministry of Labour; portal + free Social Business Incubator. EN 5:21, FR 5:20, DE 6:02.

## Fact-check episodes 37–41 (9 Nov 2026) + ElevenLabs recordings (partly)

Jacques: "do the rest". `build/apply_factcheck_eps37-41_2026_11.py`; quiz: LLL Q4 explanation (language leave = Luxembourgish). Batch `EL_STATE=/tmp/el_state_b9.json python3 build/el_run_batch.py luxinnovation,logement,space,lll,cnap en,fr,de`.
- 37 Luxinnovation: Fit 4 Start since 2015; digital, health tech, space, and defence (new in edition 17). EN 5:22, FR 5:17, DE 6:05. Final.
- 38 Housing portal: most eligible households don't claim the rent subsidy; online appointments at the Guichet unique via MyGuichet; national register of affordable housing (RENLA) since 2026. EN 5:05, FR 5:09, DE 5:57. Final.
- 39 Space Agency: LuxImpulse national programme; ESA member since 2005. EN 5:28, FR 5:30, DE 6:14. Final.
- 40 Lifelong learning: catalogue "more than ten thousand courses, more than 300 approved providers"; individual training leave up to 80 days per career; language leave is for Luxembourgish only (was "to learn a language"). EN 9:39, FR 10:04, DE 11:14. Final.
- 41 CNAP: minimum pension "a little over €2,400 in 2026" (was May 2025 figure); 2026 increases +1.5% (Jan) and +2.5% index (June). EN 15:21, FR 15:11, DE 17:27. Final.
- The API key "Biergerpakt podcast" hit its 300,000-credit limit during LLL FR. Remaining ≈ 50,000 credits (LLL FR/DE, CNAP EN/FR/DE). After raising the limit: re-run the same batch command (state b9 keeps the done parts; if /tmp was wiped, cached sentences in build/el_cache are reused at no cost), then `replace_audio_elevenlabs.js lll,cnap en,fr,de`, `set_status.js final lll,cnap`, `make_review.js`.
- Fix: `die()` in `build/tts_elevenlabs.py` now uses `os._exit(1)`. Before, a quota error inside a worker thread only ended that thread, the run printed ALL SEGMENTS DONE with sentences missing and the batch marked LLL FR as done (the broken file stayed in /tmp, never went live).
- Jacques raised the key's limit the same evening; LLL FR/DE and CNAP EN/FR/DE recorded with the same batch command, put live, status final (batch total ≈ 75,000 credits).

## Episode 42 — EBL / Ëmweltberodung Lëtzebuerg (10 Nov 2026)

New episode on ebl.lu (Jacques: "add a new episode about https://www.ebl.lu/"). ebl.lu blocks automated fetchers (robots), so it was researched in the built-in browser: EBL pages (founded 1992, neutral non-profit, member communes ≈ 95% of the population — scripted as "most communes… the vast majority of residents", no count per the no-stale-figures rule; funded by fees + agreement with the environment ministry since 1994), Projeten (Klimapakt, Naturpakt, Ouni Pestiziden, Green Events with SDK, Gutt Geschier, Grénge Web, Mol nach emol, school workshops Precious Ocean / Wuerzelwierk, children's books), Material/Ausléinen, Green Job, newsletter, contact (info@ebl.lu).
- Scripts `podcast_script_ebl{,_fr,_de,_lb}.md` — 71 turns each, standard intro/outro, ~8 min. Content (titles, descriptions, topics, quiz) in `build/ebl_content.json`; wrong answers written to match the right ones in length, so no quiz_distractors file.
- `pronunciation.py`: "EBL" added to LETTERS (E-B-L); "Ëmweltberodung" → EN "Um-velt-beh-roh-doong", FR "Eumvèlt-bérodoung" (DE as written) — not A/B tested, check by ear.
- Recorded: `EL_STATE=/tmp/el_state_ebl.json python3 build/el_run_batch.py ebl en,fr,de` (≈ 22,200 credits); faster-whisper had to be reinstalled on the VM (`pip install faster-whisper --break-system-packages`), listening check then clean in EN/FR/DE.
- Injected with `node build/inject_ebl.js` (adds the episode with content, categories energy + civic) followed by `node build/replace_audio_elevenlabs.js ebl en,fr,de` (audio, segments, durations, segments_lb), then `balance_quiz_answers.js --write`, `bump_version.js`, `make_review.js ebl`. Durations: EN 7:49, FR 7:44, DE 8:39. Backup: `episodes_data.pre_ebl.js`.
- This inject + replace pair is the simplest pattern for any NEW ElevenLabs episode.

## Fact-check House of the Greater Region (10 Nov 2026)

Episode 12 had been skipped in the November round (no review page). Checked against granderegion.net (chiffres clés, dates clés, Sommet, présidence, Secrétariat, Maison, CESGR, se soigner, se déplacer), iba-oie.eu and STATEC. Jacques: "apply all". Changes: "almost twelve million" (11.8 M on 1 Jan 2023); "more than half live in France, more than four out of five work in Luxembourg" (276,360 cross-border workers in 2024, ≈230,000 in Luxembourg — was "three-quarters"); the House is in Esch since 2015, shared office in Luxembourg City since 1999 (Tom: "So the idea is older than the building", Anna "Exactly." instead of "Young, yes."); Summit = "a member of the Luxembourg government… representatives from the French side" (currently Vice-PM Bettel + the Préfet); cross-border emergency teams "in some places" (was "the closest ambulance comes"); granderegion.net has a Biergerpakt page under Discover/Découvrir/Entdecken. Script: `build/apply_factcheck_granderegion_2026_11.py` (substring edits per turn, built on `lib_factcheck.py`); quiz Q1–Q3 + EN/FR/DE descriptions via `node build/apply_factcheck_quiz_2026_11.js --only=granderegion --write` — new `--only=` flag, because some older WIL entries no longer match after `balance_quiz_answers.js` reshuffled options (run without `--only` it stops on those). Re-recorded changed sentences: `EL_STATE=/tmp/el_state_gr.json python3 build/el_run_batch.py granderegion en,fr,de` (≈ 6,800 credits, listening check clean), `replace_audio_elevenlabs.js granderegion en,fr,de`, `make_review.js granderegion` → review/granderegion-0c4d09710e/. New durations: EN 13:44, FR 12:40, DE 15:21.

## Hesitations removed — MyGuichet (10 Nov 2026)

Jacques: spoken hesitations ("Nice. And, hmm... what can I…", "Mmm,", "..." pauses) sound awkward with the ElevenLabs voices — **avoid them in scripts**: no "hmm"/"mmm"/"uh", no "..." pauses; use a comma, colon or full stop instead. Applied to MyGuichet with `build/apply_nofillers_myguichet_2026_11.py` (24 edits per language, EN/FR/DE/LB, turn counts unchanged, idempotent). Re-recorded (changed sentences + neighbours, ≈11,200 credits, listening check clean), put live with `replace_audio_elevenlabs.js`. New durations: EN 7:47, FR 8:09, DE 9:03. Other episodes still contain such hesitations.

## Partner review documents (10 Nov 2026)

`node build/make_review_doc.js <key>[,<key>…]` writes `Relecture partenaires/Biergerpakt_Capsule_<key>_relecture.docx` (folder git-ignored): French instructions + review link (from `build/review_tokens.json`), then per language (FR, DE, EN) the script from `podcast_script_<key>{_fr,_de,}.md` and the quiz from `episodes_data.js` (correct answer highlighted in green, explanations). Check first that the scripts match the recorded audio. Partners are now told about "capsules audio" (Jacques, 10 Nov 2026). Partner contact list: `Biergerpakt_Podcast_Contacts_relecture.xlsx` (git-ignored, personal data).

## Voice fixes — Maison de l'orientation (12 Nov 2026)

Jacques heard two bad lines by Anna ("And the fourth?" too loud, "And how to start?" squeaky) and wanted French names said the French way.
- Lines lengthened so the voice has context: "And what's the fourth theme?" / "And what's the best way to get started?" (+ FR/DE/LB equivalents) — `build/apply_voicefix_maison_orientation_2026_11.py`.
- **New QC tools** (keep using them after each recording):
  - `build/voice_qc.py <key> <lang>` measures every sentence (pace, pitch, pitch spread, loudness, voicing, whisper confidence) and lists sentences that sound unlike the rest of that host's voice (it flagged both lines Jacques heard). Results in `/tmp/voice_qc_<key>_<lang>.json`; resumable (`BUDGET=` seconds).
  - `build/best_take.py <key> <lang> <i,i>` records 3 extra takes (seeds 1241–1243) and keeps the one closest to the host's normal profile (writes `el_cache/reseed.json`); then re-run `el_run_batch.py` (0 credits) and `replace_audio_elevenlabs.js`.
  - `build/match_pron.py <key> <lang> [start]` for sentences containing a French name: keeps the take whose pronunciation (whisper word timing + MFCC/DTW, same voice) is closest to the approved A/B reference.
- Pronunciation A/B (`build/pron_fr_words_test.py`, files `build/el_test/pron_maison_en_AB.mp3`, `pron_lycee_en_AB.mp3`): Jacques chose "Maison de l'Orientation" **as written** and **"leessay"** for lycée/lycées → EN rule in `pronunciation.py`. (CePAS EN also says "lycée": the rule applies at its next re-recording.)
- Retakes kept: EN 7 (plus 6 name sentences), FR 11, DE 5. ≈ 5,000 credits in total (incl. A/B tests). New durations: EN 11:54, FR 11:59, DE 14:03.

## Official ministry name — Info-Seniors, FNS, ONIS (13 Nov 2026)

Jacques: use the ministry's official name, not "the Ministry of Family". Fixed in Info-Seniors line 21 (`build/apply_ministry_name_infosenior_2026_11.py`) and, by the same standing rule, FNS line 23 and ONIS line 41 (`build/apply_ministry_name_fns_onis_2026_11.py`), EN/FR/DE/LB. These were the only short forms left in any script's spoken lines. Re-recorded the changed sentences (≈2,500 credits), put live with `replace_audio_elevenlabs.js infosenior,fns,onis en,fr,de`.

## Accessibility voice fixes (13 Nov 2026)

- Anna's "And the message for today?" sounded wrong → "And what's the one message to remember from today?" (+ FR/DE/LB); "So..." pause in her next line removed. `build/apply_voicefix_accessibilite_2026_11.py`.
- Website said the French way in English: Jacques's A/B choice A → EN rule `accessibilite` → "accessibilité" in `pronunciation.py` (A/B file `build/el_test/pron_accessibilite_en_AB.mp3`, made with the new generic `build/pron_ab.py`). `match_pron.py` now also handles it.
- "agrément" (Info-Seniors EN): A/B tested, Jacques: leave as is.
- Voice QC (EN): 6 odd-sounding sentences retaken with `best_take.py`. ≈ 3,500 credits in total. New durations: EN 13:12, FR 13:20, DE 15:21.

## Episode 43 — Lëtz prepare / 72-hour guide (14 Nov 2026)

New episode on letzprepare.public.lu (Jacques: "create an episode about letzprepare", guide page). Sources: home page + FAQ (National Resilience Strategy, launched 2025, HCPN, eight pillars, slogan), news of 09.10.2026 (guide + campaign "Bass du prett?"), and the three October 2026 PDFs (guide, 72-hour checklist, personal emergency plan; EN and DE read, FR titles from fr/guide.html — the FR guide PDF could not be fetched).
- Scripts `podcast_script_letzprepare{,_fr,_de,_lb}.md` — 77 turns each, standard intro/outro, no hesitations/"..." pauses. Only durable figures: 72 hours, at least 3 litres of water per person per day, kit check twice a year, 112/113. LB titles and motto are free translations (the official LB guide was not read) — check against the LB version before LB goes live.
- Content in `build/letzprepare_content.json` (wrong answers matched in length; no quiz_distractors file). Categories: safety + civic.
- `pronunciation.py` (all NOT A/B tested — check by ear): "Lëtz prepare"/"letzprepare" → EN "Let's prepare", FR "Lets pri-pair", DE "Lets pripär"; "Bass du prett" → EN "Bass doo prett", FR "Bass dou prèt"; "infocrise" → EN "info-creeze", DE "Info-Kriis"; EN "113" → "one one three" (scripts write 1-1-3 in EN/DE/LB, 113 in FR).
- Recorded: `EL_STATE=/tmp/el_state_letz.json python3 build/el_run_batch.py letzprepare en,fr,de` (≈ 24,000 credits; listening check re-generated 3 FR and 1 DE sentence, nothing left to check by ear). `voice_qc.py` was NOT run (librosa missing on the VM).
- `node build/inject_letzprepare.js` → `replace_audio_elevenlabs.js letzprepare en,fr,de` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js letzprepare` → review/letzprepare-7e85b794e5/. Durations: EN 8:30, FR 8:24, DE 9:25. Backup: `episodes_data.pre_letzprepare.js`.

- 15 Nov 2026: Jacques heard Anna's "Or a wind-up radio." (EN, sentence 61) sounding off; `voice_qc.py` (librosa reinstalled) flagged it too (pitch). Retaken with `best_take.py letzprepare en 61` (≈ 60 credits), rebuilt, put live. EN now 8:30 (509.96 s). QC also flagged EN #2 "Hello everyone!" (loud), #6 "Anna, a question to start." and #27 "Who is behind the strategy?" (pitch) — not retaken.

## Video page — Lëtz prepare (15 Nov 2026)

Jacques asked for the English episode as a motion graphics video and a separate page to share it. `video/letzprepare/` holds `index.html` (standalone page, noindex, not linked from the site), `letzprepare_en.mp4` (1080p, 8:30, 27 MB, captions burnt in, built in the cloud session with a Python/Skia renderer from the episode segments — render scripts saved in `build/video/`: engine.py, scenes_letzprepare_en.py (imported as `scenes`), render.py; they need skia-python, the Font Awesome free solid font, and segs.json + audio.pcm extracted from the episode) and `poster.jpg`. Live at https://bp-podcast-production.up.railway.app/video/letzprepare/ after push. If the English audio is re-recorded, the video must be re-rendered.

## Greater Region voice fixes (16 Nov 2026)

- `split_sentences` (tts_elevenlabs.py) no longer splits after "J.F." → "On the boulevard J.F. Kennedy." is one sentence (EN/FR/DE; the voice used to pause/skip a beat). Applies to all future recordings.
- EN "In German, the Haus der Großregion." took a French accent from the French name before it → "And in German, it's the Haus der Großregion."; take chosen with the new `build/pick_word_take.py` (whisper word confidence for "German": 0.37 before, 0.94 now; seed 1262 kept because 1263 said "Großrégion").
- Tom's short "And where is it?" (wrong pitch) → "And where can you find it?" (DE "Und wo findet man es?", LB "A wou fënnt een et?"; FR already a full question). `build/apply_voicefix_granderegion_2026_11.py`.
- Voice QC EN: 6 more short lines retaken (incl. Tom's "And third?"). ≈ 1,300 credits. EN 13:45, FR 12:39, DE 15:21.

## Zukunftskeess voice fixes (16 Nov 2026)

- `cae.lu` always spelled out: new rule `cae` → "C-A-E" in `pronunciation.py` (all languages) → "C-A-E dot L-U / point L-U / Punkt L-U".
- EN Zukunftskeess → "Tsoo-koonfts-kehs" (Jacques's A/B choice C, closest to the German voice; was "Tsoo-koonfts-kayss"). EN "allocation de rentrée scolaire" → "allo-cah-syon de ron-tray sko-lair" (choice B). A/B files `build/el_test/pron_zukunftskeess_en_AB.mp3`, `pron_rentree_en_AB.mp3` (`pron_ab.py` now takes `REF_LANG=de|fr`).
- Tom's "Anna, tell us its name." dropped the name → "Tell us its name, Anna." (EN), take picked with `pick_word_take.py` (p(Anna) 0.48 → 0.90). `build/apply_voicefix_zukunftskeess_2026_11.py`.
- "Luxembourg" said the French way: new `build/lux_en_vs_fr.py` compares each "Luxembourg" with an English and a French-style reference by the same voice (whisper confidence can't tell, same spelling). None came out closer to French after the re-recording; the 3 least English ones were retaken (`THRESH=-1.0 … --fix`). `pick_word_take.py` now has `"*"` + `MIN_P` to scan all sentences with a word; `match_pron.py` has `ONLY`, `SCORE_ONLY`, `MAX_D`.
- Pitch of "No. You apply once…" (Anna, f0 225 vs her median 196) + 8 other odd short lines retaken with `best_take.py`. ≈ 6,500 credits in total. EN 14:55, FR 13:37, DE 16:09.
- Follow-up (same day): EN Zukunftskeess still not good → Jacques: say it only once by Anna and once by Tom at the start, then "the CAE" (spoken C-A-E; "CAE" added to LETTERS) — `build/apply_cae_name_zukunftskeess_2026_11.py` (14 lines, EN only; Anna's intro now ends "the CAE. That's what we'll call it today."). Tom's closing "So..." pause removed. ≈ 2,800 credits. EN 14:51.

## Klima-Agence in English (16 Nov 2026)

Anna said "Kly-ma", Tom "clee-ma" (Jacques: Tom is right). A/B (`REF_LANG=en REF_ROLE=Tom python3 build/pron_ab.py klima …`, file `build/el_test/pron_klima_en_AB.mp3`) → choice B: EN rule `klima-agence` → "Clima-Agence" (also the website). Re-recorded the EN sentences in klima, environnement, govcert, logement (≈ 2,200 credits), put live with `replace_audio_elevenlabs.js … en`. "Klimabonus" unchanged.

## LISER / STATEC / observation foncière in English (17 Nov 2026)

Jacques's A/B choices (files `build/el_test/pron_{liser,fonciere,statec}_en_AB.mp3`): EN "LISER" → "Lyser" (English way, D), "STATEC" → "Statek" (French way, D) via `WORDS_LANG["en"]`; "observation foncière" → "observassion fonsyère" (C) in `NAMES["en"]`. FR/DE unchanged. Habitat EN: two "..." pauses removed (LISER lines). Re-recorded the EN sentences of habitat, research and statec (≈ 2,900 credits), put live with `replace_audio_elevenlabs.js … en`.

## SNJ motto in English (17 Nov 2026)

Jacques: the English voice can't say "Jonker staark maachen" → left out of the EN spoken lines, only the English motto "empowering youth" (2 lines, Anna; "..." pauses there removed). `build/apply_motto_snj_2026_11.py`; sources footer keeps the original. FR/DE unchanged. ≈ 130 credits.
- Follow-up (same day): glitch at the start of Tom's "BEE SECURE promotes…" (turn started directly on "Bee"; all 4 takes weak) → "Yes, BEE SECURE promotes…". All 15 "..." pauses removed from the SNJ EN script (`build/apply_nofillers_snj_2026_11.py`; e.g. 1 s gap after "Fourth..."). `pick_word_take.py` now takes a regex word (e.g. "Bee?"). ≈ 1,500 credits. EN 7:37.

## ONE (enfance) quality pass (17 Nov 2026)

Jacques: recording quality not good → all 16 "..." pauses removed per language (new reusable `build/remove_ellipses.py <key> [langs] [--dry]`; then 5 hand-picked colons: initials "O, N, E", list of family types, "is this helping?", "has a name: the Office…", "a caring one: support…"). Tom's short "Where is it?" merged: "Now, how do you actually reach the ONE, and where can you find it?" (EN). Voice QC on EN/FR/DE + `best_take.py` on flagged lines (EN 6, FR 7, DE 1). NB: after a script edit that merges/splits sentences, re-check indices before `best_take.py` (they shift). ≈ 7,000 credits. EN 7:05, FR 7:03, DE 8:08. DE was already clean.
- CePAS EN (17 Nov 2026): the one "lycée" sentence re-recorded with the EN "leessay" rule (Maison de l'orientation choice) + take matched to the reference (`ONLY=lycée match_pron.py cepas en`), ≈ 280 credits.

## Zesumme Vereinfachen (17 Nov 2026)

"millions of procedures" → "hundreds" (EN/FR/DE/LB, `build/apply_hundreds_zesumme_2026_11.py`). EN name: A/B with the German voice as reference (`build/el_test/pron_zesumme_en_AB.mp3`) → Jacques chose "as written"; the 5 EN sentences got the take closest to that reference (`ONLY="zesumme vereinfachen" match_pron.py zesumme en`; the outro take had the name unrecognisable). ≈ 1,300 credits.
- Follow-up (same day): Anna's "I love that. Together." (lone one-word sentence, sounded disconnected) → "I love that idea — doing it together." (+ FR/DE/LB). EN: the name only once (Tom's introduction), then "this project" / "the platform" / outro "about this platform for simpler public services" (`build/apply_voicefix_zesumme_2026_11.py`). Voice QC EN + 8 retakes. ≈ 1,500 credits.

## CGDIS said less often (17 Nov 2026)

Jacques: "C-G-D-I-S" is cumbersome → said only in the introduction (line 15), the name explanation (21) and the summary (79), 3× instead of 14×; elsewhere "the rescue corps" / "it" / "they" / "volunteer firefighter" (FR "le corps de secours", DE "das Rettungskorps", LB "de Rettungsdéngscht"; outro "Luxembourg's fire and rescue corps"). `build/apply_fewer_cgdis_2026_11.py`, EN/FR/DE/LB. ≈ 4,400 credits. EN 8:19, FR 8:07, DE 9:22.

## Hosts addressing themselves (17 Nov 2026)

Tom said "So Tom, let's make it practical" in agriculture, amenagement, cepas, cgdis, fondseuropeens; Anna said "So Anna, what is…" in demenz. The other host answers each time → only the name changed ("So Anna…" / "So Tom…"), "..." after it removed. EN/FR/DE/LB, `build/apply_vocative_fix_2026_11.py`. No self-address left in any episode. ≈ 1,500 credits.

## ONIS pitch pass (17 Nov 2026)

Jacques: "Exactly. It's dignity…" sounded off. EN line reworded "Exactly — it gives dignity and preparation at the same time." (metrics rated the old take normal; trust the ear). `voice_qc.py` now also flags statements whose melody rises at the end (`tail`), and `best_take.py` penalises a rising end on statements. Retakes kept: EN 16, FR 18, DE 11. ≈ 5,400 credits. FR "Le REVIS a deux facettes." still a known ASR false positive.

## FNS voice fixes (17 Nov 2026)

- EN "Now — the FNS doesn't…" ("Now" was cut) → "Now, the FNS…" (p(Now) 0.96). EN French term "revenu pour personnes gravement handicapées" removed (DE/LB keep it).
- Closing "…The National Solidarity Fund. fns.lu." — the lone "fns.lu." was cut off → one sentence "…remember the name: the National Solidarity Fund, fns.lu." (EN/FR/DE/LB). New rule `fns` → "F-N-S" (all languages, like `cae`).
- Short questions made fuller (EN/FR/DE/LB): "Let's start simply: what exactly is it?", "And is it only money, or is there more to it?", "And what's the third step?", "And what's the one message to remember from today?".
- Voice QC EN/FR/DE + retakes (EN 13, FR 7, DE 7). `best_take.py` now saves after each sentence (long FR sentences can hit the 180 s limit). ≈ 6,500 credits. EN 13:52, FR 14:08, DE 16:07.

## Environment portal (17 Nov 2026)

EN: "Null Offall Lëtzebuerg" and "Mäin Offall" left out of the spoken lines ("the country's zero-waste strategy", "an app to help you know what goes in which bin"); sources footer keeps them. `build/apply_waste_names_environnement_2026_11.py`. Voice QC EN/FR/DE, retakes EN 4, FR 3, DE 1. ≈ 1,200 credits.

## SYVICOL pitch pass (19 Nov 2026)

All 15 "..." pauses removed per language (`remove_ellipses.py syvicol`; EN: 7 colons/dashes by hand), then voice QC EN/FR/DE + retakes (EN 6, FR 4, DE 4). Standard intro/outro sentences deliberately NOT retaken: they are identical (same text + context = same cache hash) in every episode, so a reseed would change all episodes. ≈ 6,000 credits. EN 5:46, FR 5:43, DE 6:24.

## Agriculture pitch pass (19 Nov 2026)

All 15 "..." pauses removed per language (`remove_ellipses.py agriculture`; EN: 10 colons by hand), voice QC EN/FR/DE + retakes (EN 6, FR 5, DE 2); standard intro/outro not retaken. ≈ 6,500 credits. EN 6:32, FR 6:35, DE 7:21.

## Spatial planning pitch pass (19 Nov 2026)

All 16 "..." pauses removed per language (`remove_ellipses.py amenagement`; EN: 11 colons by hand), voice QC EN/FR/DE + retakes (EN 4, FR 1, DE 4); standard intro/outro not retaken. ≈ 6,300 credits. EN 5:48, FR 5:49, DE 6:28.

## CNAP / Pensiounskeess (19 Nov 2026)

- EN Pensiounskeess → "Pen-si-yons-kees" (Jacques's spelling; was "Pen-see-ouns-kayss"). EN "Caisse nationale d'assurance pension" → "Kess nassyonal dassuranss pansyon" (A/B choice B, `build/el_test/pron_caissepension_en_AB.mp3`). Anna's "Good. And what exactly does the CNAP do?" ("Good" swallowed) → "Good — and what…", take picked (p(Good) 0.61 → 0.81). "..." removed (1 per language). Live.
- Pitch pass (after the key's limit was raised): voice QC EN/FR/DE + retakes EN 12, FR 6, DE 10 (≈ 2,600 credits). Live. EN 15:21, FR 15:10, DE 17:27.
- `best_take.py` now writes takes atomically (a run cut off by the 180 s limit had left a broken mp3 in el_cache; moved to `build/_to_delete/`).

## Culture portal (19 Nov 2026)

Scripts ready: all "..." pauses removed (`remove_ellipses.py culture`; EN: 8 colons/dashes by hand). Recorded after the key's limit was raised; voice QC EN/FR/DE + retakes (EN 3, FR 2, DE 2). ≈ 4,300 credits. Live. EN 5:27, FR 5:21, DE 6:07.

## Info-Zenter Demenz + assembly fix (19 Nov 2026)

- Tom's "And not every memory slip is dementia." sounded incomplete ("and not" rushed into ~0.25 s) → "Of course, not every memory slip is dementia." (p(not) 1.00). "..." pauses removed (12 per language; EN 7 colons by hand), voice QC + retakes (EN 3, FR 2 incl. the same line, DE 2). ≈ 5,000 credits.
- **`rebuild.py` CLEAN fix**: the "stray fragment" rule dropped any short sound (<250 ms) at a sentence edge followed by a ≥120 ms pause — which also removed real short words before a comma pause (found: FR demenz "Oui. Vivre sainement…" lost "Oui."). Now a fragment is only dropped if it is also ≥ 8 dB quieter than the speech (or < 80 ms). `CLEAN_OLD=1` restores the old rule. Other episodes are assembled with the old rule until they are rebuilt (0 credits: `el_run_batch.py <keys> en,fr,de` + `replace_audio_elevenlabs.js`).

## GOVCERT (19 Nov 2026)

EN "analyses them" was read as the noun ("an-AL-uh-seez") → rule `analyses them/it/what/the` → "analyzes …" (spoken only; script keeps British spelling). "..." pauses removed (14/language; EN 9 colons/dashes by hand), voice QC + retakes (EN 3, FR 1, DE 4). Rebuilt with the new CLEAN rule. ≈ 5,600 credits.

## Geoportail (19 Nov 2026)

Tom's "…and have a lot of fun with... maps." had a strange pause → "…fun with: maps." (0.3 s beat; FR " : les cartes", DE/LB ": Karten/Kaarten"). All "..." pauses removed (EN 3 dashes/colons by hand), voice QC + retakes (EN 12, FR 3, DE 3). ≈ 6,300 credits.

## Research Luxembourg (19 Nov 2026)

- "..." pauses removed (17/language; EN 14 colons/dashes by hand). "Belval." no longer a lone sentence (EN ": Belval." by hand; FR/DE/LB too).
- "Luxembourg" sounded odd: `lux_en_vs_fr.py` scores all occurrences English-like (incl. Tom's "a side of Luxembourg", -2.04 — re-recorded anyway with the pause change); retook Anna's 4 least English ones (`INCLUDE=6 THRESH=-1.0 … --fix`; new `INCLUDE` option). If Jacques still hears it, the issue is stress, not French accent → consider an EN respelling A/B test.
- Tom's closing "…to build with knowledge." faded (last word -8…-12 dB in all takes) → "And more and more, Luxembourg is choosing knowledge to build its future." (-2 dB). New `build/last_word_take.py` (keeps the take with the loudest last word).
- Voice QC + retakes (EN 6, FR 0 extra, DE 2). ≈ 8,000 credits. EN 6:15, FR 6:13, DE 6:58.

## Social & solidarity economy (19 Nov 2026)

EN "status" (societal impact company) sounded strange → 3 sentences re-taken against a plain "status" reference (`ONLY=status match_pron.py ess en`, new term), Tom's line now heard p(status)=0.99. "..." pauses removed (11/language; EN 7 colons/dashes by hand), voice QC + retakes (EN 1, FR 1, DE 1). ≈ 4,600 credits.

## Luxinnovation (19 Nov 2026)

Tom's "Research Luxembourg" sounded odd: spelling A/B (`build/el_test/pron_researchlux_en_AB.mp3`) → Jacques: as written; sentence re-taken, most English take kept (`INCLUDE=18 THRESH=5 lux_en_vs_fr.py luxinnovation --fix`, -1.32 → -1.88). "..." pauses removed (13/language; EN 7 colons/dashes by hand), voice QC + retakes (EN 3, DE 1; FR clean). ≈ 5,500 credits.

## Lëtz prepare (19 Nov 2026)

No "..." pauses in this episode. Rebuilt with the new CLEAN rule; voice QC + retakes (EN 2, FR 13, DE 8). DE Tom's "Was ist das?" bad in every take → "Was ist das genau?". ≈ 2,800 credits.

## EBL (19 Nov 2026)

Jacques: avoid Luxembourgish terms (badly pronounced) → EN/FR/DE spoken lines say "Ëmweltberodung Lëtzebuerg" only once (Anna's explanation at the start, as Jacques asked), the "Ëmwelt/Berodung" explanation (→ "the name says exactly what it does"), "Grénge Web", "SuperDrecksKëscht" (→ national waste-prevention programme), "Ouni Pestiziden" (→ campaign for gardens "without pesticides"), "Gutt Geschier" (→ sharing tools / the tool library). Kept: the websites ounipestiziden.lu and guttgeschier.lu (said once each). `build/apply_no_lux_terms_ebl_2026_11.py`; LB script and footers unchanged. "..." pauses removed, voice QC + retakes (EN 5, FR 4, DE 2). ≈ 9,000 credits.
- Follow-up: EN "Ëmweltberodung Lëtzebuerg" → "Emvelt-berodung Letze-burg" (A/B choice E with an eleven_v3 Luxembourgish reference: `REF_LANG=lb pron_ab.py`, file `build/el_test/pron_emwelt_en_AB.mp3`). FR/DE unchanged (assumed fine).

## Space agency (19 Nov 2026)

"..." pauses removed (10/language; EN 6 colons/dashes by hand), voice QC + retakes (EN 5, FR 2, DE 3). ≈ 4,000 credits.

## European funds (19 Nov 2026)

Jacques: "integration" → "living together" (Tom's AMIF line, summary line; official fund name "Asylum, Migration and Integration Fund" kept); FEDER amount ("around twenty-one million euros") removed — no amounts for the other funds, avoids stale figures. `build/apply_fondseuropeens_2026_11.py` (EN/FR/DE/LB). "..." pauses removed (18/language; EN 9 colons/dashes by hand), voice QC + retakes (EN 0, FR 10, DE 5). ≈ 10,000 credits.

## Episode list: "Show episodes by topic" view (19 Nov 2026)

Jacques: a second way to browse. A tick box next to the topic dropdown (`<label class="view-check"><input type="checkbox" id="view-toggle">`, label i18n `view_by_topic`, count `topics_count`, EN/FR/DE/LB; Jacques preferred a tick box to a button) switches the landing page between the full list (default; the site always opens on it) and a grouped view: one section per topic in `CATEGORIES` order, each with its episodes — an episode with several topics appears in each of its sections (43 episodes → 69 rows in 15 groups). The dropdown still works in both views (grouped view + a topic = that one group). Code: `episodeRow()`, `renderViewToggle()`, `renderEpisodeList()` in app.js; CSS `.view-check`, `.topic-group*` in index.html. Tested with jsdom.

## 2026-11-20 — Broad themes + topic map (bubbles)

Jacques: a visual grouping of the episodes by theme, as an extra option, with fewer categories.
- **Themes.** `THEMES` in `app.js` regroups the 15 detailed `CATEGORIES` into 7 families (id, colour, `cats: [...]`, en/fr/de label): digital · social (+inclusion) · family (+health, seniors) · work (+research) · living (housing, energy, agriculture) · civic (+culture, crossborder) · safety. The dropdown, the "by topic" view and the map all use `THEMES`; `ep.categories` in `episodes_data.js` is unchanged. **A new category id must be added to one theme's `cats`**, otherwise its episodes are not grouped. `selectedCat` now holds a theme id.
- **Topic map.** Second tick box `#map-toggle` ("Show the topic map", i18n `view_map`, off by default) shows `#topic-map-wrap` above the list: one bubble per theme sized by its number of episodes, one numbered dot per episode (an episode appears in each of its themes). Clicking a bubble or its label = same as choosing the theme in the dropdown (click again to clear); a dot opens the episode (title on hover/focus; on touch screens first tap shows the title, second tap opens). Code: `renderTopicMap()`, `tmDotLayout()`, `tmPack()` (layout recomputed from the container width, also on resize); CSS `.tm-*` in index.html. Checked in Chrome at 1280 px and 390 px.

## Episode 44 — Blood donation / dondusang.lu (20 Nov 2026)

New episode (Jacques: "a new episode about blood donation in Luxembourg and the platform dondusang"). Sources: dondusang.lu EN/FR/DE (home, How to donate, Who can donate, Contraindications, The blood, Plasma, Where and when, Ambassadors, Help us, FAQ) and the Red Cross press release of 6 July 2026 (since 1 July 2026 the Centre de Transfusion Sanguine is the "Fondation de la Croix-Rouge luxembourgeoise pour la transfusion sanguine"; nothing changes for donors).
- Scripts `podcast_script_dondusang{,_fr,_de,_lb}.md` — 95 turns each, standard intro/outro, no "..." pauses. Figures kept are the site's own rules (18 years, 50 kg, 60/65, 4 months tattoo, 6 months tropics, 3/4 months between donations, 1 month plasma, "about 100 bags every weekday"); no donor counts, no opening hours (days only), no phone number. Not on the site and therefore not said: residence/nationality conditions. LB terms are free translations (the site has no Luxembourgish version).
- Content in `build/dondusang_content.json`; categories health + civic. `build/inject_dondusang.js` → `replace_audio_elevenlabs.js dondusang en,fr,de` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js dondusang` → review/dondusang-74fd7fcb50/ → `make_review_doc.js dondusang`. Backup: `episodes_data.pre_dondusang.js`.
- `pronunciation.py`: "dondusang" / "Don du sang" → EN "dawn dew sahn" (Jacques's A/B choice B, 20 Nov; `build/el_test/pron_dondusang_en_AB.mp3`; the 4 EN sentences retaken with `best_take.py`), FR "don du sang", DE "Don dü Sang" (not A/B tested).
- DE: "vor dem 60. Lebensjahr" was split after "60." by the sentence splitter (cut-off audio) → reworded "vor dem Alter von 60 Jahren". Avoid ordinal numbers with a full stop in German scripts.
- Recorded with `EL_STATE=/tmp/el_state_dds.json python3 build/el_run_batch.py dondusang en,fr,de` (≈ 27,000 credits, listening check clean); voice QC EN/FR/DE + `best_take.py` retakes (EN 9, FR 9, DE 11; ≈ 3,500 credits; standard intro/outro not retaken). DE Tom "Was ist der erste Schritt?" is flagged by QC in every take (pitch not measurable) — check by ear. Durations: EN 9:28, FR 8:52, DE 10:06.

## Episode 45 — I can vote / jepeuxvoter.lu (20 Nov 2026)

New episode (Jacques: "another episode about the platform 'I can vote' and the right for foreigners to vote in Luxembourg; it should encourage political participation"). Key `jepeuxvoter`, category `civic`. Sources: communales-jepeuxvoter.public.lu (Who can vote?, How to register?, How does voting work?, Becoming a candidate, Good to know), europeennes-jepeuxvoter.public.lu, guichet.public.lu (registration for municipal elections), law of 23 Aug 2023 on intercultural living together (communal commission, also open to people who work in the commune).
- Scripts `podcast_script_jepeuxvoter{,_fr,_de,_lb}.md` — 85 turns each, standard intro/outro, no "..." pauses, no party or candidate named. Each language says its own address: EN icanvote.lu, FR jepeuxvoter.lu, DE ichkannwaehlen.lu, LB echkawielen.lu (names shown on the site's language versions). Durable facts only: no residence period for non-Luxembourgers, registration at the latest 55 days before election day, compulsory voting once registered (removal on request, excused over 75), postal vote, no proxy, polling 8:00–14:00, candidates 6 months in the commune, next municipal and European elections 2029. No registration figures ("only a minority have registered").
- ⚠ Re-check when the 2029 dates are fixed; the site also has a "Journée Nationale de l'Inscription" page (FR menu) that is not in the episode.
- Content `build/jepeuxvoter_content.json`; `pronunciation.py`: icanvote → "I can vote", jepeuxvoter → "je peux voter", ichkannwaehlen → "ich kann wählen".
- Recorded `EL_STATE=/tmp/el_state_jpv.json python3 build/el_run_batch.py jepeuxvoter en,fr,de` (≈ 28,000 credits); faster-whisper + librosa had to be reinstalled on the VM, listening check then clean. Voice QC EN/FR/DE: very short lines joined to the next sentence in all four languages (`build/apply_voicefix_jepeuxvoter_2026_11.py`), retakes EN 9, FR 5, DE 3 (≈ 3,500 credits more); standard intro/outro not retaken.
- `node build/inject_jepeuxvoter.js` → `replace_audio_elevenlabs.js jepeuxvoter en,fr,de` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js jepeuxvoter` → review/jepeuxvoter-5783e3b5c4/. Durations: EN 9:30, FR 8:58, DE 10:18. Backup: `episodes_data.pre_jepeuxvoter.js`.

## Lifelong learning (20 Nov 2026)

"..." pauses removed (17/language; EN 11 colons/dashes by hand), voice QC + retakes (EN 7, FR 9, DE 2). Tom's short "That's powerful." bad in every take → "I find that really powerful." (FR "Je trouve ça vraiment puissant.", DE "Das finde ich wirklich stark.", LB too). ≈ 8,000 credits.

## Working folder for audio builds: `EL_TMP` (20 Nov 2026)

Several sessions share the VM's /tmp; folders another session created there (`/tmp/<key>_el_seg`, `/tmp/voice_qc_<key>_<lang>.json`) are read-only for the next one (`Permission denied` on rmtree). `tts_elevenlabs.py`, `el_run_batch.py`, `voice_qc.py`, `best_take.py` and `replace_audio_elevenlabs.js` now take `EL_TMP=<dir>` (default /tmp), e.g. `mkdir -p /tmp/s2 && export EL_TMP=/tmp/s2`, and use it for all of these files. (lux_en_vs_fr.py / match_pron.py / pick_word_take.py / last_word_take.py only read the cache, not /tmp.)
- Second pitch check (20 Nov, later): only a few outliers left; retakes EN 1 ("It takes only a few minutes."), FR 2; ≈ 300 credits.

## AAA (20 Nov 2026)

Anna's "People know it by its initials in French... AAA, the Association d'assurance accident." badly recorded → "People know it by its French initials: AAA, for Association d'assurance accident."; take chosen by ear-proxy = full transcript correct (seed 1261; the best `pick_word_take` score had "d'assurance" garbled — check the "heard" text, not only the score). "..." pauses removed (19/language; EN 11 colons/dashes by hand), voice QC + retakes (EN 8, FR 3, DE 2). VM was under heavy load from another session (best_take ~40 s/sentence). ≈ 8,500 credits.

## Episode 46 — Social security / CCSS, ccss.public.lu (20 Nov 2026)

New episode (Jacques: "another episode on social security and affiliation to the social security; if there is a platform, explain what it is about; there is ccss.public.lu"). Key `ccss`, categories `social` + `work`. Sources: ccss.public.lu (home/missions, employees in the private sector, hiring staff, social security card, trainees and students, private households, voluntary health and pension insurance + simulator news of 05.11.2026, affiliation certificate, change of address, phishing warning), cns.public.lu "Affiliation" (cover for the current month + 3 months after 6 months of continuous affiliation, co-insurance, cross-border workers), guichet.public.lu.
- Scripts `podcast_script_ccss{,_fr,_de,_lb}.md` — 99 turns each (longer episode), standard intro/outro, no "..." pauses. Names: EN "the Social Security Centre" (the CCSS site's own English name; "CCSS" said only in the introduction and the summary, otherwise "the Centre"), FR "Centre commun (de la sécurité sociale)", DE "Zentralstelle der Sozialversicherungen" (name used on the German site), LB "Centre commun". Website said as ccss.lu (official short address). No contribution rates or amounts (they change); legal periods kept: 13 digits, 8 days, about 3 weeks for the card, 2 months before expiry, 6 months / 3 months for continued cover, 3 months for voluntary insurance.
- From general knowledge, not from the site: "a system of solidarity", the countries named for the European card (Switzerland, Norway).
- `pronunciation.py`: "CCSS" added to LETTERS; `ccss` → "C-C-S-S" (website, like cae/fns).
- Recorded with `EL_TMP=/tmp/s_ccss EL_STATE=… python3 build/el_run_batch.py ccss en,fr,de` (≈ 36,000 credits), listening check clean in EN/FR/DE. Several sessions were recording at once: `tts_elevenlabs.py` now takes `EL_ASR_FILE=<file>` (private listening-check cache; the shared `el_cache/asr.json` was being overwritten by the other session, so the check never finished) and saves it every 4 sentences.
- Voice QC: **EN done** (Anna's short "Quite a lot." joined to the next sentence in all languages, `build/apply_voicefix_ccss_2026_11.py`; 1 retake). FR/DE pitch check done later the same day (VM idle again): retakes FR 9, DE 2 (≈ 1,800 credits); listening check clean.
- `node build/inject_ccss.js` → `replace_audio_elevenlabs.js ccss en,fr,de` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js ccss` → review/ccss-f953fc8734/. Durations: EN 11:48, FR 11:21, DE 13:22. Backup: `episodes_data.pre_ccss.js`.

## Episode 48 — Who does what for seniors? / "Activités seniors" on infosenior.public.lu (20 Nov 2026)

New episode (Jacques: "an episode about actors that work in the field of seniors … briefly explain who they are and what they do; remind people that they are regrouped on infosenior.public.lu and that we have an episode about this platform"). Key `activitesseniors`, categories seniors + social. Source: infosenior.public.lu/fr/activites-seniors.html and the register page of each of the ten approved services listed on 20 Nov 2026 (the list is loaded by JavaScript: open it in a browser, WebFetch sees an empty page): GERO, Amiperas Generatiounstreff, GoldenMe, Super Senior (MEC), IRIS (Red Cross), Info-Zenter Demenz, Accompagnement et Conseil (ALA), Berodungsdëngscht (Stëftung Hëllef Doheem), Omega 90, Mäi Wëllen Mäi Wee.
- Scripts `podcast_script_activitesseniors{,_fr,_de,_lb}.md` — 105 turns each, standard intro/outro, no "..." pauses, five groups (active & learning / loneliness / memory & dementia / family carers / end of life). Refers to the Info-Seniors episode (10) and the Info-Zenter Demenz episode (35). Durable wording: no staff numbers, no phone numbers, "ten services at the time of this recording", GERO without its age; the only years are 1990 (Omega 90) and 2009 (law on euthanasia and assisted suicide). EN/FR say "GERO, the competence centre for old age" (Luxembourgish full name only in DE/LB).
- `pronunciation.py`: geroAKTIV/geroPRO/geroRESEARCH → "gero Aktiv/Pro/Research", MEC → "M-E-C". Not A/B tested yet (as written): Berodungsdëngscht, Stëftung Hëllef Doheem, Generatiounstreff, Amiperas, Mäi Wëllen Mäi Wee in EN and FR.
- Recorded `EL_TMP=/tmp/s_as EL_STATE=/tmp/s_as/state.json python3 build/el_run_batch.py activitesseniors en,fr,de` (≈ 35,500 credits). The VM was very busy (several sessions, load > 10): listening check complete and clean for DE, only about 60 % done for EN and FR (one remark: "It is called Mäi Wëllen, Mäi Wee." — a name the recogniser cannot know), then assembled with `EL_ASR=0`. ⚠ Still to do when the VM is free: finish the listening check EN/FR (`EL_ASR_FILE=/tmp/<own>.json` so sessions do not overwrite each other's transcripts) and run `voice_qc.py` + `best_take.py` for EN/FR/DE.
- `tts_elevenlabs.py`: the listening check now saves each transcript at once (a run stopped mid-sentence lost its work). Two runs started at the same second can collide on `el_cache/cut.json` (JSON error) — start them 20–30 s apart.
- `node build/inject_activitesseniors.js` → `EL_TMP=/tmp/s_as node build/replace_audio_elevenlabs.js activitesseniors en,fr,de` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js activitesseniors` → review/activitesseniors-7f6bba3acf/ → `make_review_doc.js activitesseniors`. Durations: EN 12:29, FR 11:28, DE 13:10. Backup: `episodes_data.pre_activitesseniors.js`.

## ADEM (20 Nov 2026)

- EN/DE: French motto "Facilitons l'emploi" left out, only "Let's make employment easier." / „Machen wir die Beschäftigung einfacher." (FR keeps its original motto).
- EN ADEM pronunciation unified: A/B (`build/el_test/pron_adem_en_AB.mp3`) → choice E "Addem" in `WORDS_LANG["en"]` (all EN episodes; others at their next re-recording). All 85 affected EN sentences re-recorded (≈ 6,300 credits). FR/DE assumed consistent.
- "..." pauses removed (27–28/language; EN 18 colons by hand). FR/DE recorded (≈ 6,800 credits). DE assembled without the listening check (VM overloaded); EN/FR listening check clean.
- Finished in the afternoon (VM idle): ADEM consistency scored for all 40 EN occurrences (`ONLY=adem SCORE_ONLY=1 match_pron.py adem en`), the 5 outliers (> 4.0) retaken (`MAX_D=4.0`); pitch QC + retakes EN 9, FR 7 (+ colon before the French motto), DE 6 ("Das ist es." joined to the next sentence); full listening check clean in EN/FR/DE (incl. DE). ≈ 2,600 credits.
- Incidents fixed: `build/el_cache/asr.json` was truncated by a cut-off write (recovered 1,324 entries; the rest is re-transcribed on demand, no credits) → all shared cache JSON writes are now atomic (`el.save_json`). VM disk was full (/tmp) → removed own finished `*_el_seg` folders.

## Episode 47 — Club Aktiv Plus / clubaktivplus.lu (20 Nov 2026)

New episode (Jacques: "another episode about the clubs aktiv plus and their platform: clubaktivplus.lu"). Key `clubaktivplus`, categories `seniors` + `civic`. Sources: clubaktivplus.lu FR/DE (Qui sommes-nous / Über uns, Tous les clubs + one club page, Activités, Foire aux questions, News & Publications), press release "Club Senior becomes Club Aktiv Plus" (gouvernement.lu, 25.03.2024), mfsva.gouvernement.lu.
- Scripts `podcast_script_clubaktivplus{,_fr,_de,_lb}.md` — 93 turns each, standard intro/outro, no "..." pauses, no very short lines. The pages disagree on the network size (23 or 24 clubs; 83, 86 or 89 communes; 11 or 14 managing organisations), so the episode says "more than twenty clubs" and "more than eighty partner communes" and gives no number of managers. Dated facts kept: first clubs 1999, new name 2024. Not said: GERO (only in the sources footer; the spoken line is "the national coordination of the clubs"), club names and place names, phone numbers. "The website exists in French and in German" — re-check if an English version appears. LB is a free translation (the site has no Luxembourgish version).
- Content `build/clubaktivplus_content.json`; `pronunciation.py`: clubaktivplus → "Club Aktiv Plus" (EN/FR/DE; not A/B tested — check "Aktiv" and "ClubPages" by ear, above all in French).
- Recorded with `EL_ASR_FILE=$HOME/s3/asr.json EL_TMP=$HOME/s3 EL_STATE=$HOME/s3/el_state_cap.json python3 build/el_run_batch.py clubaktivplus en,fr,de` (≈ 27,000 credits, listening check clean in EN/FR/DE). Voice QC EN/FR/DE + `best_take.py` retakes (EN 8, FR 7, DE 7; ≈ 2,900 credits; standard intro/outro not retaken). DE Tom "Was ist der zweite Bereich?" is flagged in every take (pitch not measurable, as in dondusang) — check by ear.
- `node build/inject_clubaktivplus.js` → `replace_audio_elevenlabs.js clubaktivplus en,fr,de` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js clubaktivplus` → review/clubaktivplus-6b657355c2/ → `make_review_doc.js clubaktivplus`. Durations: EN 9:36, FR 9:04, DE 10:28. Backup: `episodes_data.pre_clubaktivplus.js`.
- **Several sessions on the same VM (lessons from this build):** (1) the VM's `/` (with /tmp) was full — `rebuild.py` failed with "No space left on device"; use a working folder under `$HOME` (`EL_TMP=$HOME/<dir>`) and `pip cache purge`. (2) `el_cache/asr.json` is rewritten whole by every session, so two sessions recording at once erase each other's progress and the listening check never finishes: always set `EL_ASR_FILE` to a private file. (3) `el_cache/reseed.json` has the same last-writer-wins problem: `best_take.py` choices were lost when two runs (or two sessions) wrote at the same time. Run `best_take.py` one language at a time, then run it again (0 credits): every line must say "kept current" before the rebuild. (4) A process started in the background does not survive the end of a shell call.

## Eltereforum pitch pass (20 Nov 2026)

Jacques: "check for the pitch of voice", then yes to retakes and to rewording very short lines (script validated by the Eltereforum → meaning unchanged). The recording dated from 30 Sept (before `voice_qc.py`). "..." pauses removed (2/language, `remove_ellipses.py eltereforum`). Voice QC EN/FR/DE + `best_take.py`: new takes EN 5 (#14, 17, 72, 88, 96), FR 10, DE 6. Lines that stayed low/creaky in every take were joined with a colon (`build/apply_voicefix_eltereforum_2026_11.py`, EN/FR/DE/LB): "Let's start there: what does it mean?", "…and this is important: it's for everyone.", "Exactly: it's a friendly first step."; DE also "Die Schule, und dann die Teenagerjahre.". Standard intro/outro not retaken. ≈ 2,500 credits. EN 6:34, FR 6:34, DE 7:24. Known listening-check false positives: FR "Parents forts, enfants forts" and the list of towns; EN "Strong parents, strong children." is reported as "still cut" — check by ear.
- **VM disk full** (/ and /sessions at 99 %, /tmp files of older sessions cannot be removed): tools were installed into the project folder instead — `PYTHONUSERBASE=<folder>/build/el_test/vm.nosync/py pip install --user --no-compile …` (a `.nosync` folder is not uploaded to iCloud), with `EL_TMP`, `HF_HOME` pointing there too; needs delete permission for the folder (the tools remove their work files). `el_run_batch.py` now writes `el_check_by_ear.txt` to `EL_TMP`. Removed again after the pass. With a loaded VM use `OMP_NUM_THREADS=1..2` (whisper is slower with 4 threads) and never run two `best_take.py` at once (both rewrite `el_cache/reseed.json`).
- Club Aktiv Plus, follow-up (20 Nov 2026, afternoon): Jacques had Anna's EN sentence "Club Aktiv Plus: active, and a little bit more." removed (EN only; FR/DE/LB keep their line, turn counts unchanged). Re-recorded (1 sentence, ≈ 60 credits), put live with `replace_audio_elevenlabs.js clubaktivplus en`. Voice QC EN run again on the whole episode: only the standard "Hello everyone!" and "Thank you so much for listening." are flagged (shared with every episode, not retaken). EN now 9:32 (571.69 s).
- Later on 20 Nov (Jacques): EN line "run by the Ministry of Family Affairs" → full ministry name (script, quiz explanation); **GERO is said "Jero"** — `pronunciation.py`, English only so far (GERO → "Jero", geroAKTIV → "Jero Aktiv" …; FR/DE unchanged, the Info-Seniors episode's one EN line with GERO not re-recorded yet). Listening check finished for EN/FR: FR "Faut-il être soi-même senior…" had stray sounds at the end in the first takes → new take. Voice QC EN/FR/DE + `best_take.py` (new takes: EN 2, FR 7, DE 4); short lines reworded: EN "So what happens in this meeting place?", "No, that is not necessary at all."; DE "Was passiert denn an diesem Treffpunkt?", "Ja, GERO hat drei Abteilungen.", "Ja, dort gibt es noch viel mehr." (FR/LB unchanged). ≈ 4,000 credits. The pending ⚠ above is done. Durations: EN 12:34, FR 11:25, DE 13:11.

## Episode 49 — CET / Centre for Equal Treatment, cet.lu (23 Nov 2026)

New episode (Jacques: "make a new episode about CET … only use official data. official site: cet.lu"). Key `cet`, categories `inclusion` + `civic`. Only source: cet.lu, consulted 23 Nov 2026 (FR/EN/DE/LB versions): Présentation + presentation brochure, Missions, Champ d'application, Collège, La discrimination, Défense des droits et voies de recours, FAQ, Lanceur·se d'alerte, Contact, Langage simple.
- Scripts `podcast_script_cet{,_fr,_de,_lb}.md` — 97 turns each, standard intro/outro, no "..." pauses, no very short lines ("Yes, it does." / "Yes, it has." / "Yes, that is true." / "Not always." were joined to the next sentence in all four languages after the first voice check). Names: EN "the CET, the Centre for Equal Treatment" (French name said once), FR "le CET, le Centre pour l'égalité de traitement", DE "das CET, das Zentrum für Gleichbehandlung", LB "de CET, de Centre pour l'égalité de traitement" (names used on each language version of the site).
- Durable facts only: law of 28 November 2006; college of five members appointed by the Grand Duke on a proposal from the Chamber, five-year mandate renewable once; six grounds; fields of application; the four forms of discrimination; burden of proof; whistleblower law of 2023. No member names, no phone number, no postal address, no deadlines of the whistleblower procedure.
- Not on the site and therefore NOT said: that the service is free of charge; opening hours. The site's pages disagree on the grounds: "La discrimination" lists seven (with nationality, "the CET does not handle complaints based on nationality"), FAQ/brochure list six → the episode says "six grounds the CET can act on" and explains the nationality point. The two examples (landlord; neutral rule that disadvantages older or disabled people) are illustrations by the hosts (said so in the sources footer).
- ⚠ Re-check: the CET published (28.10.2026) an opinion on draft law No. 8764 about the Ombudsman, the Ombudsman fir Kanner a Jugendlecher and a "Centre national anti-discrimination" — a pending text, not mentioned in the episode; if it is adopted, the episode must be revised. Also re-check the list of website languages (FR/DE/LB/EN/PT + plain language + German Sign Language videos).
- `pronunciation.py`: "CET" added to LETTERS ("C-E-T" in EN/FR/DE); `cet` before dot/point/Punkt → "C-E-T" (website and e-mail; only there, because "cet" is also a French word). Not A/B tested — check by ear "C-E-T dot L-U" (the recogniser wrote "cut.lu" for EN sentence 12 and FR sentence 133) and the French name in the English episode.
- Recorded with `EL_TMP=$HOME/s_cet EL_STATE=$HOME/s_cet/state.json EL_ASR_FILE=$HOME/s_cet/asr.json python3 build/el_run_batch.py cet en,fr,de` (≈ 31,000 credits incl. the reworded lines), listening check clean in EN/FR/DE (1 FR sentence re-generated). Voice QC EN/FR/DE + `best_take.py` (new takes EN 3, FR 1, DE 4; ≈ 1,200 credits; standard intro/outro not retaken). best_take.py with 8 sentences ran past the 180 s shell limit — give it 3–4 sentences per call.
- `node build/inject_cet.js` → `EL_TMP=$HOME/s_cet node build/replace_audio_elevenlabs.js cet en,fr,de` → `balance_quiz_answers.js --write` → quiz answers evened out in length (correct answer no longer the longest) → `bump_version.js` → `make_review.js cet` → review/cet-cffb9579a9/ → `make_review_doc.js cet`. Durations: EN 10:24, FR 9:53, DE 11:25. Backup: `episodes_data.pre_cet.js`.
- Another session was building an `ombudsman` episode in the same folder at the same time (untracked `*ombudsman*` files, not yet in `episodes_data.js`): commit the CET files by name, not with `git add -A`.

## Episode 50 — The Ombudsman and the OKaJu / ombudsman.lu, okaju.lu (23 Nov 2026)

New episode (Jacques: "a new episode about the Ombudsman (Médiateur) and the OKaJu, the children's and young people's ombudsman; apply all the rules; only use official data"). Key `ombudsman`, categories `civic` + `family`. One episode, two parts: Anna explains the Ombudsman (Tom asks), then Tom explains the OKaJu (Anna asks).
- Sources (official only): ombudsman.lu FR/EN (home, Mission, Réclamation, Règlementation, plain-language page, Lanceur d'alerte, contact), guichet.public.lu "Faire appel au médiateur (Ombudsman)", law of 22 Aug 2003 + Rules of the Chamber (legilux: attached to the Chamber, eight years, not renewable), law of 11 April 2010 (CELPL); okaju.lu FR/EN/DE (home, Saisir l'OKAJU, FAQ, Les missions, Droits de l'enfant, Young Advisors, contact), law of 1 April 2020 (legilux).
- Scripts `podcast_script_ombudsman{,_fr,_de,_lb}.md` — 103 turns each, standard intro/outro, no "..." pauses, no very short lines, no host name at the start of a line. Durable wording: no office-holder names (the Ombudsman changed in 2025), no phone numbers, no e-mail addresses, no yearly figures or percentages ("most individual complaints come from parents", "a large part is about family matters"); kept: laws of 2003 and 2020, eight-year term, one month without an answer, under eighteen, Convention ratified in 1993, Young Advisors 13–18. Websites: ombudsman.lu (FR + EN, with a plain-language page), okaju.lu (FR, EN, DE, PT) — re-check if languages are added.
- Not on the sites and therefore not said: where the word "ombudsman" comes from, how long a case takes. "House of Human Rights" / „Haus der Menschenrechte" is a translation of "Maison des Droits de l'homme" (OKaJu address; the Ombudsman gives the same street address). German terms for the Ombudsman part are free translations (no German version of ombudsman.lu); "Abschiebehaftzentrum" = Centre de rétention. LB is a free translation.
- `pronunciation.py`: OKaJu → EN "Oh-kah-yoo", FR "Okayou", DE "Okaju" (mixed capitals must not be spelled). **Not chosen by ear yet**: A/B file `build/el_test/pron_okaju_en_AB.mp3` (LB reference, then A "OKaJu", B "Okaju", C "Oh-kah-yoo" = used, D "Okayou", E "Oka-you"). "Ombudsman fir Kanner a Jugendlecher" and "médiateur" are left as written — check by ear (EN/FR).
- Content `build/ombudsman_content.json` (quiz answers evened out in length). Recorded with `EL_ASR_FILE=/tmp/s_omb/asr.json EL_TMP=/tmp/s_omb EL_STATE=/tmp/s_omb/state.json python3 build/el_run_batch.py ombudsman en,fr,de` (≈ 32,000 credits; listening check clean in EN/FR/DE; whisper + librosa installed with `PYTHONUSERBASE=/tmp/s_omb/py`). Voice QC EN/FR/DE + `best_take.py` (new takes EN 6, FR 8, DE 7; ≈ 3,400 credits; standard intro/outro not retaken), then rebuilt and listening check clean again. FR Tom "L'adresse est okaju point l-u." stays "unclear" for the recogniser in every take — check by ear.
- `node build/inject_ombudsman.js` → `EL_TMP=/tmp/s_omb node build/replace_audio_elevenlabs.js ombudsman en,fr,de` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js ombudsman` → review/ombudsman-3d112debc2/ → `make_review_doc.js ombudsman`. Durations: EN 11:08, FR 10:17, DE 11:39. Backup: `episodes_data.pre_ombudsman.js`.
- Built at the same time as episode 49 (CET) by another session: it became episode 50 because CET was injected first.

## Openings varied + hosts balanced — CET and Ombudsman/OKaJu (23 Nov 2026)

Jacques: the latest episodes all opened with "I have a question to start with" → **the opening must differ from episode to episode**; **both hosts must explain and both must ask** (no episode where one only asks), and this must happen **fluently, never announced** (no "this time I will explain, and you can ask the questions"). Standing rules for every new episode.
- `build/apply_openings_balance_2026_11.py` (EN/FR/DE/LB, idempotent). A role change is made by merging the question with the answer: the other host simply starts the next section with the explanation.
- **cet** 97 → 91 turns. Opening = a principle ("every person has the right to be treated equally"). Anna explains the basics, the forms of discrimination, courts/proof, the website; Tom explains the six grounds + fields, what the CET does, how to contact it. EN only: Tom now says "Its website is cet dot l-u" BEFORE Anna gives the French name (her "cet dot l-u" right after "Centre pour l'égalité de traitement" came out with a French accent); the French name is the last thing in her line.
- **ombudsman** 103 → 97 turns. Opening = a scene ("Imagine that a letter from an administration arrives…"). Hand-over line removed; Tom now also explains the first step with the administration and the second mission (places of detention), Anna explains who can contact the OKaJu. EN only: "Ombudsman fir Kanner a Jugendlecher" is no longer spoken (Jacques: the Luxembourgish pronunciation is not good) → "It is short for a Luxembourgish name. In English, it means…"; FR/DE keep the name.
- **OKaJu pronunciation (Jacques, 23 Nov): "OKA-JUU", J as in "juice"** → `pronunciation.py`: EN "Oka-joo", FR "Okadjou", DE "Okadschuh" (was Oh-kah-yoo / Okayou / Okaju). Check by ear.
- Still opening with "I have a question to start with": activitesseniors, ccss, clubaktivplus, dondusang, jepeuxvoter (+ letzprepare "Anna, a question to start") — not changed yet.
- Recorded with `EL_TMP=$HOME/s_bal` (≈ 25,000 credits incl. a first version that was replaced), listening check clean EN/FR/DE; voice QC + `best_take.py` (new takes: cet EN 9, FR 4, DE 1; ombudsman EN 3, FR 1, DE 1). `replace_audio_elevenlabs.js cet,ombudsman en,fr,de` → `bump_version.js` → `make_review.js` (same review links) → `make_review_doc.js`. Durations: cet EN 10:17, FR 9:52, DE 11:14; ombudsman EN 10:52, FR 10:06, DE 11:31. Backup: `episodes_data.pre_balance.js`.
- Tooling notes: voice_qc.py segfaults if several copies start at once with a cold numba cache — warm it with one run first, set `NUMBA_CACHE_DIR`, and use `OMP_NUM_THREADS=1` when running the six in parallel (much faster). The session disk is small: keep `HF_HOME` (whisper models) in /tmp.

## Episode 52 — CNPD / your data protection rights, cnpd.public.lu (24 Nov 2026)

New episode (Jacques: "make a new episode about CNPD: your data protection rights. apply all the rules … only use official data. official site: cnpd.public.lu/en.html"). Key `cnpd`, categories `digital` + `civic`. **State: scripts + content ready, NOT yet recorded and NOT yet in `episodes_data.js`** — the ElevenLabs key "Biergerpakt podcast" answered `quota_exceeded` (10 credits left of 600,000) after about 50 English sentences (those are in `build/el_cache/`).
- Only source: cnpd.public.lu, consulted 24 Nov 2026 (EN, with FR/DE pages for the official terms): CNPD, Duties, Powers, Individuals, Your rights + the nine right pages, Asserting your rights, Complaint form, Contact, About this site.
- Scripts `podcast_script_cnpd{,_fr,_de,_lb}.md` — 95 turns each, standard intro/outro, no "..." pauses, no very short lines, no host name at the start of a line. Opening = an ordinary day (loyalty card, online order, app, form at the doctor's) — different from the other episodes. Both hosts explain and ask, section by section. Names: EN "the CNPD … National Commission for Data Protection" (site header; French name said once, at the END of Anna's line, next line is Tom's), FR "la CNPD, la Commission nationale pour la protection des données", DE "die CNPD, die Nationale Kommission für den Datenschutz", LB free translation ("Nationalkommissioun fir den Dateschutz"). Official terms per language from the site: FR responsable du traitement / réclamation / droit à l'effacement, au déréférencement, d'opposition, à la limitation, à la portabilité; DE Verantwortlicher / Beschwerde / Auskunftsrecht, Recht auf Berichtigung, Löschung, Dereferenzierung, Datenübertragbarkeit, Widerspruchsrecht, Einschränkung der Verarbeitung.
- Durable facts only: GDPR directly applicable since 25 May 2018; law of 1 August 2018; one month to answer, up to two more months for complex requests; free in principle; proof of identity only in case of reasonable doubts; controller first, then complaint (online form or by post); CNPD checks, corrective + investigative powers, administrative fines; indirect exercise of rights (police, customs); court + lawyer for damages; website in FR/EN/DE. NOT said: names of the commissioners, postal address, phone number, telephone hours (the contact page gives Mon–Fri 9:00–11:30 → "the telephone hours shown on the contact page"), fine amounts, the year the CNPD was created (home page says 2002 act, CNPD page cites the 2018 act).
- Website is said as "cnpd dot l-u" (www.cnpd.lu is the address the site itself gives; the pages live on cnpd.public.lu). Illustrations by the hosts (said so in the sources footer): the opening scene, cross-border workers protected by the same regulation, changing provider (portability).
- `pronunciation.py`: CNPD, GDPR, RGPD, DSGVO added to LETTERS; `cnpd` → "C-N-P-D" (website). No other script contains these words. Check by ear: "C-N-P-D dot L-U", "G-D-P-R", the French name in the English episode.
- Content `build/cnpd_content.json` (title, description, 8 topics, 5 quiz questions EN/FR/DE, answers of similar length), injector `build/inject_cnpd.js`.
- **To finish once the ElevenLabs key has credits again (≈ 38,000 needed: EN ≈ 8,000 left, FR ≈ 13,600, DE ≈ 13,400, plus retakes):** `mkdir -p /tmp/s_cnpd && export EL_TMP=/tmp/s_cnpd EL_STATE=/tmp/s_cnpd/state.json EL_ASR_FILE=/tmp/s_cnpd/asr.json` (+ whisper/librosa via `PYTHONUSERBASE`, `HF_HOME` in /tmp) → `python3 build/el_run_batch.py cnpd en,fr,de` until DONE ALL → voice QC + `best_take.py` → `node build/inject_cnpd.js` → `node build/replace_audio_elevenlabs.js cnpd en,fr,de` → `node build/balance_quiz_answers.js --write` → `node build/bump_version.js` → `node build/make_review.js cnpd` → `node build/make_review_doc.js cnpd` → update the "Length" line of the four scripts and the episode count above.
- Another session was building a `consommateurs` episode at the same time (24 Nov, `/tmp/s_con`): the episode number of `cnpd` is whatever is free at injection time; commit the CNPD files by name.

## Episode 51 — Consumer protection: ULC + European Consumer Centre / ulc.lu, cecluxembourg.lu (24 Nov 2026)

New episode (Jacques: "a new episode about Consumer protection: ULC and the European Consumer Centre; apply all the rules; only use official data"). Key `consommateurs`, categories `civic` + `crossborder`. A `cnpd` episode was being built by another session at the same time — commit files by name, not with `git add -A`. This episode was injected first and is **id 51**; the CNPD episode (announced above as 51, audio pending) will therefore become 52 when it is injected.
- Sources (official only, consulted 24 Nov 2026): ulc.lu (home, Votre ASBL, Consultation gratuite, Services proposés, Affiliez-vous, À qui m'adresser ?, Service contentieux, CLLV, Médiateur en assurances; DE home), cecluxembourg.lu FR/EN/DE (home, About us, What does ECC do?, easy-to-read page, Defend your rights, Right of withdrawal, FAQ, Contact), eccnet.eu (Our services), guichet.public.lu (ULC, CEC, unfair commercial practices), mpc.gouvernement.lu + press conference "Droits des consommateurs" of 14 Jan 2026 (gouvernement.lu).
- Scripts `podcast_script_consommateurs{,_fr,_de,_lb}.md` — 97 turns each, generated by `python3 build/make_scripts_consommateurs.py` from `build/consommateurs_src/<lang>.txt` (body) + the standard intro/outro copied from the ombudsman scripts. **Edit the `.txt` files and re-run the generator**, not the `.md`. Opening = "something all of us did this week: we bought something" (no "I have a question to start with"). Roles: Tom explains what the ULC is, Anna its services and membership, Tom its limits + travel/insurance bodies; Anna explains the European Consumer Centre, Tom the steps of a complaint, Anna the limits; both share the two rights (14 days, 2-year legal guarantee). No "..." pauses, no very short lines, no host name at the start of a line.
- Names: EN "the ULC, the Luxembourg Consumer Protection Association" (guichet.public.lu's English name; French name said once, last in Tom's line) and "the European Consumer Centre (Luxembourg)", "CEC" said once; FR "l'ULC", "le Centre européen des consommateurs (le CEC)"; DE "die ULC, der Luxemburgische Verbraucherverband" (guichet DE) and "das Europäische Verbraucherzentrum Luxemburg". LB is a free translation (no Luxembourgish version of either site).
- Durable wording: no membership fee amount (80 € on 24 Nov 2026), no opening hours, no phone numbers, no office-holder names; "tens of thousands of households" (site: ± 43,000 families); "most of its money comes from members' fees" (site: over 75 %); "a part of the costs of a lawyer or expert, with conditions, limits and a waiting period" (site: 50 %, max. 10,000 €, 6 months); network "one centre in every EU country + Iceland and Norway" (site: 29 centres); small claims "for smaller amounts" (site: up to 5,000 €). Kept: founded 1961; 14-day withdrawal for distance purchases; 2-year legal guarantee for new products.
- Not said because the sources disagree or are silent: Ettelbruck days ("at certain times"), number of magazine issues (8 or 9), the magazine's name, the UK (handled through a separate cooperation), Portuguese as a consultation language (contact page yes, FAQ no → "several languages, among them French, German, English and Luxembourgish"). guichet.public.lu still says the ULC's tasks come from the "Ministry of the Economy"; ulc.lu says "Minister of Consumer Protection" → the episode only says "the State, on the basis of an agreement". The cross-border-worker line ("contact the centre of the country where you live") comes from eccnet.eu. Sofa-from-Germany / rental-car-in-Spain are illustrations by the hosts.
- ⚠ Re-check later: languages of ulc.lu (FR + DE today) and cecluxembourg.lu (FR/EN/DE + easy-to-read page).
- Content `build/consommateurs_content.json` (EN/FR/DE title, description, 8 topics, 5 questions with wrong answers as long as the right one); `build/inject_consommateurs.js` ready (not run).
- `pronunciation.py`: "ULC" and "CEC" added to LETTERS; `ulc` before dot/point/Punkt → "U-L-C"; `cecluxembourg` → "C-E-C Luxembourg". No other episode contains these words. Not A/B tested — check by ear "C-E-C Luxembourg dot L-U" and the French name of the ULC in the English and German episodes.
- Recording: `EL_TMP=/tmp/s_con` (+ `EL_STATE`, `EL_ASR_FILE`, `PYTHONUSERBASE=/tmp/s_con/py`, `HF_HOME`), `el_run_batch.py consommateurs en,fr,de` (≈ 34,000 credits). The API key "Biergerpakt podcast" hit its 600,000 limit after EN and during FR (`quota_exceeded`); Jacques raised it and the run was resumed from the cache. Listening check clean in EN/FR/DE (1 FR sentence re-generated).
- Voice QC EN/FR/DE + `best_take.py` (new takes EN 11, FR 5, DE 6; ≈ 3,800 credits; standard intro/outro not retaken). FR Tom "Que faut-il retenir ?" stayed off in every take → joined: "Résumons tout cela : que faut-il retenir de cet épisode ?" (FR only, so FR has 164 sentences, EN/DE 165). Check by ear: EN Tom "Who pays for the centre, then?" (best take still 4.6), FR Anna "…sur ulc point l-u et sur cecluxembourg point l-u." (recogniser unsure), "C-E-C Luxembourg dot L-U".
- `node build/inject_consommateurs.js` → `EL_TMP=/tmp/s_con node build/replace_audio_elevenlabs.js consommateurs en,fr,de` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js consommateurs` → review/consommateurs-a4ada45bc1/ → `make_review_doc.js consommateurs`. Durations: EN 11:29, FR 10:56, DE 12:33. Backup: `episodes_data.pre_consommateurs.js`.
- **Finished 24 Nov 2026 (later the same day, after the key's credits were restored):** recorded with `EL_TMP=/tmp/s_cnpd` (whisper/librosa from `PYTHONUSERBASE=/tmp/s_con/py`), listening check clean in EN/FR/DE (0 re-generated). Voice QC + `best_take.py`: new takes EN 6, FR 8, DE 7 (≈ 3,400 credits; standard intro/outro not retaken; slow lines with spelled letters — CNPD, DSGVO, "cnpd point l-u" — left as they are). `inject_cnpd.js` → **episode 52** (`consommateurs` took 51) → `replace_audio_elevenlabs.js` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js cnpd` → review/cnpd-81e066a1c8/ → `make_review_doc.js cnpd`. Durations: EN 12:50, FR 12:20, DE 13:58 (longer than CET/Ombudsman: 165 sentences). Backup: `episodes_data.pre_cnpd.js`.
- **CNPD, English only (24 Nov 2026, Jacques: the French part is not pronounced well):** the sentence "The four letters come from its French name: Commission nationale pour la protection des données." was removed from Anna's line → "In English, it is called the National Commission for Data Protection." No French is spoken in the English episode any more. FR/DE/LB scripts unchanged (DE and LB still say the French name once). 1 sentence re-recorded (≈ 70 credits), listening check clean, `replace_audio_elevenlabs.js cnpd en` → `bump_version.js` → `make_review.js cnpd` (same link) → `make_review_doc.js cnpd`. EN 12:44 (164 sentences).

## Episode 53 — The health mediator / Médiateur santé, mediateursante.public.lu (24 Nov 2026)

New episode (Jacques: "make a new episode about médiateur santé in Luxembourg. apply all the rules … only use official data. official site: mediateursante.public.lu/fr.html"). Key `mediateursante`, categories `health` + `civic` + `crossborder`. A `kjt` episode was being built by another session at the same time (untracked `*kjt*` files) — commit the mediateursante files by name, not with `git add -A`.
- Sources (official only, consulted 24 Nov 2026): mediateursante.public.lu FR (+ DE pages for the German terms): home, Qui sommes-nous, Droits / Obligations du patient, FAQs, Réclamation, Médiation en santé (Médiateur(s), Demander une médiation, Pour quel conflit ou situation ?, Avantages et limites, Exemples concrets, Déroulement: entretien préalable, accord en vue de la médiation, réunion en médiation, médiation indirecte / à distance, accompagnateurs-avocats-experts, accord de médiation, garanties légales), Recours juridictionnels, Soins transfrontaliers + Points de contact, Associations de patients, Contact; guichet.public.lu "Appealing to the National Health Mediation and Information Service" (English name, who can refer a matter).
- Scripts `podcast_script_mediateursante{,_fr,_de,_lb}.md` — 107 turns each (178 sentences), standard intro/outro, no "..." pauses, no very short lines, no host name at the start of a line. Opening = a statement about trust ("Good health care is built on trust") — different from the other episodes. Both hosts explain and ask: Anna explains what the service is, Tom the information mission and the patient rights, Anna the first steps (direct dialogue, complaints service), Tom the principles of mediation, Anna the steps of a mediation, Tom the example case + limits + the three situations outside its remit, Anna cross-border care, Tom contact and website.
- Names: EN "the health mediator" / "the National Health Information and Mediation Service" (guichet.public.lu's English contact name; "health mediation service" as short form), French short name "Médiateur santé" said once, LAST in Anna's line (next line is Tom's); FR "le médiateur de la santé" / "Service national d'information et de médiation dans le domaine de la santé" / "Médiateur santé"; DE "der Mediator für das Gesundheitswesen" / "Nationale Informations- und Mediationsstelle im Gesundheitswesen" (terms of the German site); LB free translation (keeps the French name). German words for the steps (Vorgespräch, Vereinbarung über die Teilnahme an der Mediation, indirekte Mediation) are free translations — the step pages were read in French.
- Durable facts only: law of 24 July 2014; "working since 2015" (the site says May 2015, the 2025 annual report April 2015); three missions; neutral/independent/impartial; mediators approved by the Minister of Justice, often two mediators; voluntary, confidential, each side may stop; contact by phone, email or form; request from one side or all; the service may refuse; preliminary interview (also by video); agreement to mediate not always needed; meeting "generally two hours at the most"; companions + lawyer, announced in advance; indirect / remote mediation; written, dated, signed agreement that binds; not for decisions of social security bodies (→ Ombudsman, with a pointer to our Ombudsman episode), long-term care only, or professionals only; two national contact points for cross-border care (the service + CNS). NOT said: names of the mediator and team, phone number, e-mail address, street address ("in Luxembourg City"), secretariat hours (Mon–Fri 9:00–13:00 on 24 Nov 2026 → "shown on the website"), the 30-year limitation period, the personal-convenience supplements (CP1/CP2/CP4), the two-year deadlines of the FAQ, figures from the annual reports.
- **Not on the site and therefore NOT said: that the service is free of charge** (neither mediateursante.public.lu nor the guichet page states it; the "Costs" heading on guichet is empty) — ask the service in the partner review. Languages: "several languages, among them Luxembourgish, French, German and English" (team page; one member also Portuguese; guichet names FR/DE/LB for referring a matter). The example is the site's anonymised case "Aux urgences", shortened. Opening lines and the examples of providers (doctor, dentist, hospital) are illustrations by the hosts (said so in the sources footer).
- ⚠ Re-check later: website languages (FR + DE today); the e-mail shown on the site is @mediateursante.lu while its link points to @mediateursante.public.lu (not used in the episode).
- `pronunciation.py`: `mediateursante` → "médiateur santé" (so the address is read "médiateur santé dot public dot L-U" / "point public point L-U" / "Punkt public Punkt L-U"). Not A/B tested — **check by ear**: "Médiateur santé" in the English and German episodes (whisper heard "Midiata Sante" / "Mediathe, Sonté"), the address in EN/DE, and that Tom's English line after "Médiateur santé" has no French accent.
- Content `build/mediateursante_content.json` (EN/FR/DE title, description, 8 topics, 5 questions, wrong answers as long as the right one), injector `build/inject_mediateursante.js`.
- Recorded with `. /tmp/s_ms/env.sh` (`EL_TMP=/tmp/s_ms`, `EL_STATE`, `EL_ASR_FILE`, whisper/librosa from `PYTHONUSERBASE=/tmp/s_con/py`, `HF_HOME=/tmp/s_con/hf`): `el_run_batch.py mediateursante en,fr,de` (≈ 41,000 credits), listening check clean in EN/FR/DE (0 re-generated). Voice QC EN/FR/DE + `best_take.py` (new takes EN 12, FR 3, DE 2; ≈ 2,750 credits; standard intro/outro not retaken), rebuilt, listening check clean again.
- Tooling notes: background jobs (`nohup … &`) are killed when the shell call ends — run voice_qc.py for the three languages in parallel INSIDE one call (`… & … & wait`, `BUDGET=140`, `OMP_NUM_THREADS=1`) and repeat until 178/178. Do NOT run two `best_take.py` at the same time: both rewrite `build/el_cache/reseed.json` and the last one wins (re-running them one after the other costs 0 credits, the takes are cached).
- `node build/inject_mediateursante.js` → **episode 53** → `replace_audio_elevenlabs.js mediateursante en,fr,de` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js mediateursante` → review/mediateursante-47187b4da0/ → `make_review_doc.js mediateursante`. Durations: EN 13:32, FR 12:50, DE 14:48 (178 sentences — the longest of the recent episodes). Backup: `episodes_data.pre_mediateursante.js`.

## Episode 54 — Kanner-Jugendtelefon (KJT) / kjt.lu (24 Nov 2026)

New episode (Jacques: "make a new episode about Kanner-Jugendtelefon in Luxembourg. apply all the rules … only use official data. official site: kjt.lu"). Key `kjt`, categories `family` + `safety`. Built at the same time as episode 53 (`mediateursante`, another session): commit the kjt files by name.
- Sources (official only, consulted 24 Nov 2026): kjt.lu in DE/EN/FR — home, 116 111, Online Help, Chatberodung / Chat counselling, Elterentelefon (Ecoute Parents), BEE SECURE Helpline, BEE SECURE Stopline, Wer wir sind / Who we are, Träger, Ehrenamtliche Mitarbeit, Kontakt, Beratungsstellen, news item "116111 now also in English on Thursdays" (4 June 2026); stopline.bee-secure.lu (what can be reported, what happens with a report, anonymity). ⚠ On 24 Nov 2026 the bare address `kjt.lu` / `www.kjt.lu` redirected to a staging host of the web agency (`kjt-stage2.fachhandel-ehses.de`); the pages under `www.kjt.lu/de|en|fr/…` answered normally. Worth mentioning to the KJT in the partner review.
- Scripts `podcast_script_kjt{,_fr,_de,_lb}.md` — 83 turns, 144 sentences each, generated by `python3 build/make_scripts_kjt.py` from `build/kjt_src/<lang>.txt` (`A:` Anna, `T:` Tom, `C:` Anna's closing line + standard outro) with the standard intro/outro copied from the cnpd scripts. **Edit the `.txt` files and re-run the generator**, not the `.md`. Opening = a telephone number ("It has six digits: 116 111") — different from the other episodes. Roles: Tom explains the KJT, its history and principles; Anna the line 116 111 and the Online Help; Tom the chat; Anna the Elterentelefon; Tom the BEE SECURE Helpline and Stopline; Anna the volunteers and the networks; Tom the website. No "..." pauses, no very short lines, no host name at the start of a line.
- Names: EN "the KJT … Kanner-Jugendtelefon … Children and Youth Helpline" (English site), "chat counselling", "Elterentelefon" (the English site gives no English name); FR "service d'assistance pour enfants et jeunes", "conseil par chat", "Elterentelefon, ou Écoute parents"; DE "Chatberatung", "Elterentelefon", "Schweigepflicht"; mottos as on each language version ("No one should be abandoned." / « Personne ne doit rester seul. » / „Niemand muss alleine bleiben."). LB is a free translation.
- Kept (durable): 116 111, 8002 4444, 8002 1234 (the numbers are the point of the episode); founded 1992 in connection with the UN Convention on the Rights of the Child; 2007 Elterentelefon + BEE SECURE Helpline + Stopline; 2021 chat; five principles; Online Help in LB/DE/FR/EN; BEE SECURE Helpline only reachable from the Luxembourg network, contact form confidential but not anonymous; three Stopline categories; website in DE/FR/EN.
- Durable wording instead of figures: opening hours ("in the afternoon and in the evening, from Monday to Saturday"; parents' line "on weekdays, mostly in the morning"; chat "at fixed times in the evening" — site: Tuesdays 18–21 h), English service ("on one day of the week" — site: Thursdays for 116 111, Monday evening slot for the Elterentelefon), Online Help reply times ("within a few days" — site: first reply within 3 days, later ones within 10), volunteer training ("a basic training … an internship in two phases" — site: 70 h + about 50 h; two shifts a month; new training about every two years, next one autumn 2027). Not said: founders' names (Croix-Rouge, Fondation Kannerschlass, Ligue Médico-Sociale, Caritas Jeunes et Familles → "four organisations from the social sector"), Insafe/INHOPE/INACH/Child Helpline International by name, team names, annual-report figures.
- **The language versions of kjt.lu disagree** (24 Nov 2026) → not said: Friday hours of 116 111 (DE/EN 14–22 h, FR 17–22 h); age limit of the chat counsellors (DE "bis 27", EN "up to 30"); Elterentelefon counsellors (DE/FR professionals and volunteers, EN "professionals" → "trained counsellors"). The site does not list the languages of the 116 111 line. Worth asking the KJT in the partner review.
- Additions by the hosts (said so in the sources footer): adults can pass on the number; parents/teachers can read the topic pages; reminder that 112 is the emergency number (with a pointer to the CGDIS/112 episode). The SNJ episode is mentioned too.
- `pronunciation.py`: "KJT", "CJF" added to LETTERS; `kjt` → "K-J-T" (website); the three numbers are read digit by digit with a pause between the two groups (EN/DE; "eight zero zero two, four four four four"), **FR says "cent seize, cent onze" for 116 111** (like "cent-douze": three "un" in a row were not clearly audible) and the 8002 numbers digit by digit; EN "Kanner-Jugendtelefon" → "Kanner-Yoogunt-telefon", FR → "Kanneur-Youguènnt-téléfone", FR "Elterentelefon" → "Elteurènn-téléfone" (DE as written). **Not A/B tested — check by ear**: these names, "C-J-F Lëtzebuerg" in EN/FR, and the telephone numbers (the recogniser's digit strings were re-checked with whisper "small" on the end of each sentence; all eight digits are there).
- Recorded with `EL_TMP=$HOME/s_kjt` (env in `$HOME/s_kjt/env.sh`; whisper/librosa from `PYTHONUSERBASE=/tmp/s_con/py`, `HF_HOME=/tmp/s_con/hf` read-only → `HF_HUB_OFFLINE=1`), ≈ 36,000 credits + ≈ 650 for the French number change; listening check clean in EN/FR/DE (0 re-generated). Voice QC + `best_take.py`: new takes EN 7, FR 4, DE 4 (≈ 3,400 credits; standard intro/outro not retaken).
- ⚠ **`build/el_cache/reseed.json` is shared**: the other session's run overwrote some of this session's best-take choices (EN all 7, DE 2). Check after a parallel build that the new takes are really used (the episode's duration must change after `best_take.py`), and simply run `best_take.py` again with the same sentence numbers — the takes are cached, so it costs 0 credits.
- `node build/inject_kjt.js` → **episode 54** → `EL_TMP=$HOME/s_kjt node build/replace_audio_elevenlabs.js kjt en,fr,de` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js kjt` → review/kjt-1097f21c71/ → `make_review_doc.js kjt`. Durations: EN 12:17, FR 11:32, DE 12:59. Content `build/kjt_content.json`. Backup: `episodes_data.pre_kjt.js`.

## Episode 55 — SIMPA / information and mediation for older people, simpa.public.lu (26 Nov 2026)

New episode (Jacques: "make a new episode about SIMPA in Luxembourg. apply all the rules … only use official data. official site: simpa.public.lu/fr.html", plus SIMPA's own PowerPoint "Lunchtalk: Vun Informatioun a Begleedung bis zur Mediatioun" of Nov 2026 as reference). Key `simpa`, categories `seniors` + `social`.
- Sources (official only, consulted 26 Nov 2026): simpa.public.lu FR/DE (home, Information, Seniorentelefon, Registre public, Aides, Médiation, Déroulement, Demander une médiation, Autres instances, Alternatives, Qui sommes-nous / missions / valeurs, FAQ, Législation), mfsva.gouvernement.lu SIMPA page, press release of 25 March 2025 (presentation of SIMPA), guichet.public.lu (Senioren-Telefon number). From the PPT: the three verbs (listen / understand and explain / strengthen dialogue), the four ideas of the 2023 quality law (more information, transparency, quality, say), the themes of mediations (care and help, living situation, meals, hygiene, family–service relationship), the "3 things to remember" used as the summary. Its statistics (calls, dossiers 2025) are NOT used (durable-wording rule).
- Scripts `podcast_script_simpa{,_fr,_de,_lb}.md` — 85 turns each, generated by `python3 build/make_scripts_simpa.py` from `build/simpa_src/<lang>.txt` (same A:/T:/C: format as kjt; intro/outro copied from the kjt scripts). **Edit the `.txt` files and re-run the generator.** Opening = a family scene at the table ("Mum is finding the stairs difficult") — different from the other episodes. Roles: Tom explains what SIMPA is, the law, the missions, the mediation rules, the example and the limits; Anna explains the services covered, who can contact it, the Seniorentelefon, what mediation is, the steps, money and contact. No "..." pauses, no host name at the start of a line, short lines joined with a colon after voice QC ("That is the first step, yes: every organisation…" in all four languages; FR "Cela fait une longue liste : qui…", FR "Premièrement, celui qu'il faut appeler : le Seniorentelefon…", DE "Erstens, wen man anrufen kann: das Seniorentelefon…").
- Names: EN "SIMPA … the national information and mediation service for older people" (no French spoken in the English episode: "The letters come from its French name"), FR "le Service national d'information et de médiation pour les personnes âgées", DE "der Nationale Dienst für Information und Mediation im Bereich der Dienstleistungen für ältere Menschen" (German site), LB free translation. Health mediator / Ombudsman / Info-Seniors / Club Aktiv Plus episodes are pointed to.
- Kept (durable): law of 23 August 2023; presented in March 2025; Seniorentelefon since 1999 (International Year of Older Persons), number 247-86000 (same as the Info-Seniors episode), languages LU/FR/DE/PT/EN, "in the morning, Monday to Friday"; all services free of charge (FAQ); no representation of the parties; confidentiality; mediation steps; Mr Muller example (site); three situations outside the remit; website "simpa dot l-u" (www.simpa.lu, the address the ministry gives), in French and German. NOT said: team names, street address, general number 247 76 500, exact hours, statistics.
- ⚠ Sources disagree (26 Nov 2026): the ministry's English SIMPA page gives the Seniorentelefon as (+352) 247 76 500, Mon–Fri 8:30–11:30; simpa.public.lu FR/DE and guichet.public.lu give 247 86 000, Mon–Fri 8:30–12:30 (and 247 76 500 as SIMPA's general number). The episode follows simpa.public.lu — worth asking SIMPA in the partner review.
- `pronunciation.py`: EN "Seniorentelefon" → "Senioren-Telefon", FR → "Séniorènn-téléfone" (not A/B tested — check by ear); SIMPA/COMPA already said as words.
- Recorded with `. /tmp/s_simpa/env.sh` (`EL_TMP=/tmp/s_simpa`, own `EL_STATE`/`EL_ASR_FILE`, whisper/librosa installed with `PYTHONUSERBASE=/tmp/s_simpa/py`): ≈ 44,000 credits, listening check clean in EN/FR/DE. Voice QC + `best_take.py` (new takes EN 6, FR 12, DE 1; ≈ 4,000 credits; standard intro/outro not retaken), then second QC pass clean apart from the standard intro/outro.
- `node build/inject_simpa.js` → **episode 55** → `replace_audio_elevenlabs.js simpa en,fr,de` → `balance_quiz_answers.js --write` → `bump_version.js` → `make_review.js simpa` → review/simpa-e4154868ab/ → `make_review_doc.js simpa`. Durations: EN 14:55, FR 13:37, DE 15:50 (the longest of the recent episodes). Backup: `episodes_data.pre_simpa.js`.

- **Shortened the same day (Jacques: "keep the episode at around ten minutes"):** 80 → 48 body turns (85 → 53 turns in all). Cut: the four missions one by one (now folded into SIMPA's three ideas listen / explain / dialogue), limitation period on hold, homologation by a judge, outside experts, SIMPA refusing a mediation, family quarrels / family mediation, going to court, most of the list of financial aid (kept: long-term care insurance, COMPA, housing). Short lines joined after voice QC: "…with help close by, and then the day centres." and "The third idea is dialogue: SIMPA wants…" (all four languages), DE "Sie endet mit einer Einigung, ganz oder teilweise, und die Mediatorin…". Topic 5 renamed "Listening, explaining, dialogue" / « Écouter, expliquer, dialoguer » / „Zuhören, erklären, Dialog". The key hit its 700,000 limit during DE; Jacques raised it. ≈ 15,000 credits incl. retakes (EN 8, FR 3, DE 1). `replace_audio_elevenlabs.js simpa en,fr,de` → same review link → Word file rebuilt. **Durations: EN 9:53, FR 8:59, DE 10:38.** Backup of the long version: `episodes_data.pre_simpa_short.js`. Check by ear: DE Tom "Er wurde durch das Gesetz vom 23. August 2023…" (slow in every take), FR Tom "Beaucoup de familles connaissent ce moment." (a little fast).

- **Date line (26 Nov 2026, Jacques: "the date is pronounced in a strange way"):** EN "the law of 23 August 2023" came out garbled (recogniser: "20th-throw them August"), DE "vom 23. August 2023" was slow in every take, FR was correct. `pronunciation.py` now sends the date written out: EN "the twenty-third of August, twenty twenty-three", FR "vingt-trois août deux mille vingt-trois", DE "vom dreiundzwanzigsten August zweitausenddreiundzwanzig" (transcripts unchanged; no other episode speaks this date). Re-recorded (≈ 900 credits), voice QC clean, `replace_audio_elevenlabs.js simpa en,fr,de`. EN 9:55, FR 8:59, DE 10:37. If another English date sounds odd, use the same written-out form.

## Playlist + player bar (26 Nov 2026)

Jacques: "a playlist on the webapp so that people can select episodes … so that they can listen in the car".

- **What listeners get:** a "+" next to every episode in the list (and a button on the episode page), a "My playlist" button with a counter in the header, a "My playlist" screen (play all, reorder with the arrows, remove, empty with two taps), and a player bar fixed at the bottom of every screen. When an episode ends the next one starts; at the end of the list the bar goes back to the first episode, paused.
- **Two players, one at a time:** the bar has its own `<audio id="pl-audio">`; the episode page keeps `#ep-audio` with the read-along script. Starting one pauses the other. Starting the quiz pauses the playlist.
- **Car / lock screen:** Media Session API (title, "Biergerpakt Podcast", previous / next / seek) with the cover `podcast-cover-192.png` / `podcast-cover-512.png` (generated, orange with headphones). It is only claimed while the playlist is the active player.
- **Storage:** `localStorage` key `bp_playlist_v1` = `{ids, cur, t}` (list, episode loaded in the bar, position in seconds). On the device only, nothing is sent. The bar comes back paused where the listener stopped.
- **Language:** the playlist plays in the site language. Switching language while a track is loaded reloads the same episode in the new language at about the same relative position.
- **Where the code is:** `app.js`, section "Playlist" (all functions start with `pl`, strings `pl_*` added to `I18N.en/fr/de` with `Object.assign`); `index.html`: CSS block "PLAYLIST", `#btn-playlist` in the header, `#btn-pl-toggle` on the episode page, `#screen-playlist`, `#pl-bar` before `</body>`.
- **Review pages are not affected:** the playlist switches itself off when the page has only one episode or when the HTML has no `#pl-audio` (review pages generated before this date). No need to regenerate them.
- **Luxembourgish:** the `pl_*` strings exist in EN/FR/DE only (LB falls back to English) — add them to `I18N.lb` before LB goes live.
- **Tested** in Chrome (desktop and phone-size window): add/remove, reorder, play all, auto-advance, previous/next, language switch, reload/resume, one player at a time, single-episode page, old index.html with the new app.js. **Not yet tested on a real iPhone or in a car** (Safari can refuse to start the next episode with the screen locked — check this before announcing the feature).
- Also fixed on the way: on very narrow phones (320 px) the topic dropdown was wider than the screen.
- **Column titles (26 Nov 2026, Jacques: the "+" was not clear to users):** the full list starts with a header row "Episode … + Add to my playlist" (`.ep-list-head`, built in `renderEpisodeList()`); in the "by topic" view the same label sits at the right of each topic heading (`.topic-group-pl`). Both come from `plColLabel()` and use the `pl_add` string, so they follow the site language and disappear where the playlist is off.

## Temporary access password (26 Nov 2026)

Jacques: "For the moment, I want to limit access" — main site only, partner review pages stay open.

- **What it does:** the main site shows a password screen (`#screen-login`, EN/FR/DE) before anything else. After a correct entry the device remembers it (`localStorage` key `bp_access_v1`); changing the password asks everyone again.
- **Set / change / remove:** `node build/set_password.js "<password>"` (at least 8 characters) or `node build/set_password.js --off`, then commit and push. The script writes only a SHA-256 fingerprint to `ACCESS_HASH` in `app.js` and bumps the asset version. **Never write the password into a file — the repository is public.**
- **Review pages are not locked:** pages generated before this date have no `#screen-login`; `build/make_review.js` now marks new ones with `<body data-access="open">`. `video/letzprepare/` is a standalone page and is not locked either.
- **Limits:** this is a curtain, not a vault. The check runs in the browser; the mp3 files and `episodes_data.js` can still be opened by their direct address, and everything is in the public GitHub repository. A real lock needs a password at server level on Railway (and a private repository).
- **Code:** `app.js` section "Access password" (`accessInit`, `accessLocked`, `sha256`), guard at the top of `showScreen()`; CSS `body.locked` in `index.html`.
- Tested in Chrome: locked state, wrong / right password, reload, password change, existing review page, regenerated review page.

### Médiateur santé shortened to ~10 min (26 Nov 2026)

Jacques: "The episode is a bit long. It should be around 10 minutes … without losing any important information." 107 → 77 turns (178 → 134 sentences) in EN/FR/DE/LB; EN 13:32 → 10:17, FR 12:50 → 9:41, DE 14:48 → 11:20. Only whole question/answer pairs were removed (A/T alternation and the balance between the hosts are unchanged), so almost nothing was re-recorded (4 sentences per language, ≈ 1,000 credits in all); listening check clean.
- Removed: who counts as a healthcare provider (examples); the "obligations" exchange; the FAQ examples; professionals may ask for information; who the mediators are (training, approval by the Minister of Justice, two mediators); "am I obliged to continue" (voluntary stays in the definition and the summary); the service may refuse a request; preliminary interview by video; the agreement to mediate; length of a meeting (two hours); indirect / remote mediation; "not only about money" + insurers; the second and third situation outside the remit (long-term care, professionals only); appointments outside the secretariat hours; patient associations + glossary; the roadmap sentence in Tom's opening line.
- Reworded: "the website names three. The first is…" → "the website names several. One of them is…" (only the social-security / Ombudsman case is told). Quiz explanation 3: the clause "each of them is free to stop the mediation at any moment" removed (no longer in the audio), in `episodes_data.js` and `build/mediateursante_content.json`.
- Rebuilt with `. /tmp/s_ms2/env.sh` (whisper/librosa from `/tmp/s_simpa/py`), `replace_audio_elevenlabs.js`, `bump_version.js`, `make_review.js` (same link) and `make_review_doc.js`. The full 107-turn version is in git (commit "Add episode 53").
- A session shortening `kjt` was running at the same time: commit the mediateursante files by name.


## KJT shortened to about 10 minutes (26 Nov 2026)

Jacques: "The episode is a bit long. It should be around 10 minutes … without losing any important information." → `build/apply_shorten_kjt_2026_11.py` (runs once; 78 → 50 body lines in `build/kjt_src/<lang>.txt`, EN/FR/DE/LB, then `make_scripts_kjt.py`). 83 → 55 turns, 144 → 108 sentences. **Durations: EN 9:58, FR 9:14, DE 10:26** (were 12:17 / 11:32 / 12:59).
- Kept: everything a listener needs to use the services — the three numbers, who each service is for, free / anonymous / confidential, Online Help with username + password and its four languages, peer-to-peer chat, the three Stopline categories, the 112 reminder, the four-point summary, the motto.
- Merged into neighbouring lines (said more briefly): operator + financing (CJF Lëtzebuerg, agreement with the Service National de la Jeunesse), the five principles, English availability ("the times when you can call in English are on the website"), the opening hours of the chat and of the Elterentelefon, what happens with a Stopline report, internship + supervision of the volunteers, topic pages + toolbox.
- Dropped: "four organisations founded it together"; the pointer to the SNJ episode and the letters "SNJ"; referral to other services in the principles part; "someone close to their own age"; training + supervision of the parents' line counsellors; the BEE SECURE contact form (confidential but not anonymous); "the authorities decide what happens next" and "the form is online day and night"; the two phases of the internship, the monthly shifts, "a new training does not start every year"; the international networks; ordering information material; the hosts' remark about parents and teachers.
- 26 new sentences per language (≈ 8,900 credits), listening check clean in EN/FR/DE; voice QC flagged none of the new sentences, so no retakes. `replace_audio_elevenlabs.js kjt en,fr,de` → `bump_version.js` → `make_review.js kjt` (same link) → `make_review_doc.js kjt`. Backup of the long version: `episodes_data.pre_kjt_short.js` (and git commit b4bfe40).
- Whisper/librosa for this run came from `/tmp/s_simpa/py` (`/tmp/s_con` no longer exists).

### Médiateur santé EN: "No" line redone + pitch check (26 Nov 2026)

Jacques: Anna's "No, and that is important to understand." had to be redone because the "No" is very short; plus a pitch check of the English voice. Fixed the usual way (fuller sentence): EN only, "No, it does not, and that is important to understand." (FR/DE/LB unchanged). Voice QC on the whole English episode: outliers outside the standard intro/outro were "There are three main tasks." (pitch high, retakes no better → merged into a fuller sentence: "It has three main tasks, and the first one is to be an information centre about rights in health care."), "I have also heard about a person of trust." (current take kept, best of 4) and "Then health mediation can be the next step." (new take). Second QC pass: only the standard intro/outro lines are flagged. ≈ 670 credits. EN now 133 sentences, 10:19; FR/DE untouched. Rebuilt with `. /tmp/s_ms2/env.sh`, `replace_audio_elevenlabs.js mediateursante en`, `bump_version.js`, `make_review.js`, `make_review_doc.js`.


### KJT pitch check (26 Nov 2026)

Jacques: "Check for the pitch of the voice." Voice QC on the shortened episode in EN/FR/DE with a wider net than the default report (pitch and pitch spread from z 2.6, rising end on a statement from z 2.2), then `best_take.py`: new takes EN 3 ("What does a child have to say…", "The website describes it as peer-to-peer…", "Those cases are not for the Stopline."), FR 2 (the long "Même si vous êtes adulte…" and "Voici quelque chose que je ne savais pas…"), DE 9 (among them "Sie hat sechs Ziffern: 116 111." — all six digits re-checked — and Anna's questions that came out high). Current take kept (best of four): EN "So tell us, how did this whole story begin?", FR "Passons maintenant aux adultes…", DE "Der Chat ist zu festen Zeiten am Abend geöffnet…". ≈ 3,700 credits. Second QC pass: outside the standard intro/outro only FR/DE "Premièrement / Erstens: … Kanner-Jugendtelefon …" (slow because of the name) and two mild German rising ends (Tom, "Der Chat ist zu festen Zeiten…", "Sie ist keine Telefonnummer…") remain. Listening check clean. `replace_audio_elevenlabs.js kjt en,fr,de` (`update_audio_elevenlabs.js` does not read `EL_TMP`) → `bump_version.js` → `make_review.js kjt`. Durations: EN 9:59, FR 9:14, DE 10:27.

### KJT German: the year 1992 (26 Nov 2026)

Jacques: in the German episode, Tom's "Das KJT wurde 1992 gegründet" has the date wrong — the voice said "1990" (the recogniser heard it too; the listening check had let it pass). `pronunciation.py` (DE) now sends "wurde neunzehnhundertzweiundneunzig gegründet" (transcript unchanged; only this sentence in all German scripts matches). 3 sentences re-recorded (≈ 460 credits), re-heard as "1992"; Anna's "seit 1992" and the years in EN/FR were already right. `replace_audio_elevenlabs.js kjt de` → `bump_version.js` → `make_review.js kjt`. DE 10:27. If another German year comes out wrong, write it out the same way.

## Zesumme Vereinfachen — partner feedback, less digital (26 Nov 2026)

Steve (Zesumme Vereinfachen team, Ministry for Digitalisation) asked for less focus on the digital component and more on administrative steps in general, suggesting the "Guichet de proximité" project (consultation online, on paper, in workshops and at stands → Guichet.lu on tour bus) or the water plan (AGE, `waasser-PDG4`). Jacques: "go for it" (both examples, MyGuichet-app example dropped).
- `build/apply_partner_zesumme_2026_11.py` (runs once; aborts unless the old 61 turns are found): 61 → 85 turns in EN/FR/DE/LB. New: "not only apps and websites" exchange, "taking part offline" exchange, Guichet.lu on tour story (Tom explains: one reception desk in Luxembourg City, coalition promise of regional desks, multi-channel consultation, nearly eight thousand participants, need for closer services, fully electric bus fitted out like a reception desk, what you can do on board), 4th water management plan (Anna explains: every six years, EU directive, state of waters / main issues / measures, Water Management Administration = FR "Administration de la gestion de l'eau" / DE "Wasserwirtschaftsamt", 2027–2033, with citizens, communes, businesses, experts; consultations, round tables, seminars, workshops). Recap point 4 → the bus; tip 2 adds workshops/round tables; "..." removed in the body (standard intro/outro untouched). EN still says the name only once. Header length → about 9 minutes; sources rewritten.
- Sources (consulted 26 Nov 2026): zesumme-vereinfachen.lu projects `guichet-de-proximite` (≈ 8,000 participants, phase 2: CTIE call for a mobile reception desk serving each region) and `waasser-PDG4`; press slides 1 Oct 2024 (gouvernement.lu: online + paper form); guichet.public.lu "Guichet.lu on tour" (100 % electric, services on board). Workshops/stands for the consultation come from Steve's e-mail. Not said: the bus schedule (one week a month per region in the press), street address of the desk, event dates.
- After voice QC two short lines were joined in all four languages ("…ask people: only online, or in other ways too?", "Yes, they can, because in some projects…"). Retakes with `best_take.py`: EN 2, FR 3, DE 2. ≈ 18,000 credits in all; listening check clean.
- `replace_audio_elevenlabs.js zesumme en,fr,de` (`EL_TMP=/tmp/s_zes`) → `node build/update_content_zesumme_2026_11.js` (description, 8 topics, Q1 explanation "participation platform", new Q5 on the bus + its wrong answers in `build/quiz_distractors/batch3.json`) → `bump_version.js` → `make_review.js zesumme` (same link) → `make_review_doc.js zesumme`. Durations: EN 9:09, FR 9:05, DE 10:16 (were 6:18 / 6:20 / 7:06). Backup: `episodes_data.pre_partner_zesumme.js`.
- NB: `node build/apply_quiz_distractors.js` currently stops on "unknown episode clarvia" (batch file still lists the removed episode) — not run this time.
