# Biergerpakt Podcast — Build Guide & Project State

This file is the single source of truth for continuing work on this project in a new session.

## What this project is

A static website for the **Biergerpakt Podcast**: short, friendly audio episodes (hosts **Anna** + **Tom**) explaining Luxembourg public services / initiatives in simple English, with a **synced read-along transcript**, a **language switcher (EN / FR / DE / LB)**, and a **5-question quiz** per episode that yields a printable certificate.

Open `index.html` in a browser — it's a static site, no server needed.

## Hosting

The site is served by **Railway** (project "proactive-fulfillment", service `bp-podcast`), auto-deployed from the GitHub repo `jinesch75/bp-podcast` (branch `main`) on every push. Live URL: https://bp-podcast-production.up.railway.app/ — GitHub Pages is NOT used. If a push doesn't show up, check the Railway dashboard: when deploys are paused ("Limited Access"), the site stays online with the last successful deployment.

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

## Episodes (42 so far)

(+ 42:clarvia — Clarvia ASBL bereavement guidance service, ~9.5 min, tagged `social,family,crossborder`, native EN/FR/DE audio + LB read-along; built July 2026 with the new intro/outro from the start; see `build/clarvia_content.json`, `build/clarvia_tr_{fr,de,lb}.json`, `build/inject_clarvia.js`.)

(+ 40:lll — lifelong-learning.lu, a longer ~10-min episode, tagged `work`. + 41:cnap — Pensiounskeess/CNAP pension system, ~16-min, tagged `seniors,social,crossborder`, native EN/FR/DE audio + LB read-along.)

id:key — 1:myguichet, 2:dsp_cns, 3:eltereforum, 4:benevolat, 5:lualert, 6:luxtrust, 7:maison_orientation, 8:infosenior, 9:accessibilite, 10:zukunftskeess, 11:fns, 12:granderegion, 13:digitalinclusion, 14:onis, 15:workinluxembourg, 16:adem, 17:habitat (Observatoire de l'Habitat), 18:klima (Klima-Agence), 19:snj (Service National de la Jeunesse), 20:enfance (Office National de l'Enfance), 21:cepas (CePAS), 22:fondseuropeens (Fonds européens), 23:zesumme (Zesumme Vereinfachen), 24:cgdis (CGDIS / 112), 25:statec (STATEC / statistics portal), 26:environnement (emwelt.lu), 27:syvicol (SYVICOL), 28:research (Research Luxembourg), 29:agriculture (agriculture portal), 30:amenagement (spatial planning), 31:aaa (accident insurance), 32:geoportail (national maps), 33:govcert (GOVCERT.LU cybersecurity), 34:culture (culture.lu), 35:demenz (Info-Zenter Demenz), 36:ess (social & solidarity economy), 37:luxinnovation (Luxinnovation), 38:logement (housing portal), 39:space (Luxembourg Space Agency).

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
