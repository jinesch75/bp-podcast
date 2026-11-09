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

## Episodes (41 so far)

(Clarvia (ex-42) was removed from the site on 30 Sept 2026 at Jacques's request; its scripts and build files are kept in `archive/clarvia/` — the audio there is git-ignored.)

(+ 40:lll — lifelong-learning.lu, a longer ~10-min episode, tagged `work`. + 41:cnap — Pensiounskeess/CNAP pension system, ~16-min, tagged `seniors,social,crossborder`, native EN/FR/DE audio + LB read-along.)

id:key (order changed Sept 2026, `build/reorder_episodes.js`) — 1:myguichet, 2:luxtrust, 3:benevolat, 4:eltereforum, 5:digitalinclusion, 6:workinluxembourg, 7:dsp_cns, 8:lualert, 9:maison_orientation, 10:infosenior, 11:accessibilite, 12:granderegion, 13:adem, 14:zukunftskeess, 15:fns, 16:onis, 17:habitat, 18:klima, 19:snj, 20:enfance, 21:cepas, 22:fondseuropeens, 23:zesumme, 24:cgdis, 25:statec, 26:environnement, 27:syvicol, 28:research, 29:agriculture, 30:amenagement, 31:aaa, 32:geoportail, 33:govcert, 34:culture, 35:demenz, 36:ess, 37:luxinnovation, 38:logement, 39:space, 40:lll, 41:cnap.

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

Each episode has a `categories` array of tag ids. The episode-list screen shows a filter bar (SINGLE-select: one topic at a time; clicking the active chip or "All topics" clears) and every card shows its tags. Tags + filter labels + the "{n} of {total} episodes" count are localized.

- **Where things live:** the taxonomy is `CATEGORIES` in `app.js` (id + en/fr/de label, ordered). Per-episode tags are `ep.categories` in `episodes_data.js`. Filter UI markup is the `#filter-bar` / `#filter-count` block in `index.html` (CSS: `.filter-chip`, `.cat-tag`). Logic: `renderFilterBar()`, `episodeMatchesFilter()`, `selectedCat` (single id or null) in `app.js`; `renderEpisodeList()` filters + renders tags + count.
- **Current categories:** digital, social, housing, energy ("Environment & energy"), research ("Research & innovation"), agriculture ("Agriculture & food"), culture ("Culture & arts"), work, family, health, seniors, inclusion, safety, civic, crossborder. (`culture` added with ep 34.) A category chip only appears once ≥1 episode uses it. (`housing` added with ep 17; `energy` added with ep 18 Klima-Agence and relabelled to "Environment & energy" when the emwelt.lu episode 26 joined it; `research` added with ep 28 Research Luxembourg.)
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
- `status: "in_progress"` on an episode shows an "In progress" badge on its card and a notice on its page (EN/FR/DE/LB strings `status_in_progress`, `in_progress_note` in `app.js`). Set/clear with `node build/set_status.js in_progress|final <from>-<to> | key,key`. Re-recorded with ElevenLabs (EN/FR/DE, final): episodes 1–13 (30 Sept 2026). Episodes 14–36 re-recorded with ElevenLabs on 9 Nov 2026 (final). In progress: 37–41 (voices to be done later).

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
