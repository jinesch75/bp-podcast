# Biergerpakt Podcast — standing rules (read before any work)

Jacques Brosius (Biergerpakt coordinator, Ministry of Family Affairs) runs this project. Follow these rules
**without being asked**. If Jacques has to ask for one of these steps, the rule was missed.
When he gives a new standing rule, add it here (short, in the right section).

Technical detail: `BUILD_GUIDE.md` (read its top sections and the most recent episode section before building).
Site: static `index.html` + `app.js` + `episodes_data.js`, served by `server.js` on Railway
(auto-deploys from github.com/jinesch75/bp-podcast, **public repo**). Live: https://bp-podcast-production.up.railway.app

## Definition of done: every new or changed episode

1. Script rules below applied. Only official sources, listed in the `*Sources:*` footer.
2. All four scripts updated: `podcast_script_<key>.md`, `_fr.md`, `_de.md`, `_lb.md`, with the same turns in each.
3. New episode: `build/inject_<key>.js` written (title, description, 8 topics, 5-question quiz in EN/FR/DE; pattern `build/inject_simpa.js`).
4. Run **`python3 build/finish_episode.py <key> en,fr,de`** (add `--new` for a new episode). Re-run the same
   command until it prints FINISHED. It does: recording + listening check → pitch check → retakes of the lines
   that sound off → rebuild + second pitch check → live → version bump → review page → partner Word file → report.
   (Only the languages that changed? Pass just those, e.g. `en`.)
5. A short line that stays off in every take: join it to the next sentence (colon/comma) in all four languages,
   then run the command again with `--reset`.
6. Add a short dated section to `BUILD_GUIDE.md`. If the length changed a lot, update the `**Length:**` line of the scripts.
7. End the reply to Jacques with: durations, the "still worth a listen" lines from the report, the review link,
   and the git push commands (see below).

"Check the pitch" of an existing episode = the same command (text unchanged → 0 credits except retakes).
`--check-only` measures and reports without changing anything.

## Script rules

- Hosts **Anna** and **Tom**. Keep them balanced: both explain and both ask. Never say so out loud
  (no "This time I will explain, and you can ask the questions").
- The opening must differ from episode to episode (not always "I have a question to start with").
- Standard Biergerpakt intro (read by the first speaker after the hello lines) and standard outro
  ("That was our episode about X…"): copy the exact wording from a recent script.
- Length **about 10 minutes** unless Jacques says otherwise. When shortening, keep all important information.
- Simple language, spoken slowly.
- No hesitations: no "hmm", "mmm", "uh", no "..." pauses. Use a comma, colon or full stop.
- No very short lines ("And the fourth?", "Quite a lot."). Write fuller sentences ("And what's the fourth theme?").
  Don't start a line with the other host's name ("Tell us its name, Anna.", not "Anna, tell us its name").
- No precise figures that go stale (counts, percentages, rankings, waiting times). Use durable wording
  ("more than ten thousand"). Drop figures you can't verify. Word laws that are still pending as pending.
- Ministry name in full. EN: "Ministry of Family Affairs, Solidarity, Living Together and Reception of Refugees".
  FR: "Ministère de la Famille, des Solidarités, du Vivre ensemble et de l'Accueil".
  DE: "Ministerium für Familie, Solidarität, Zusammenleben und Unterbringung von Flüchtlingen".
- English episodes:
  - Avoid French or Luxembourgish names that the voice pronounces badly; give the English name directly.
  - French words that stay are said the French way.
  - "Luxembourg" is said the English way.
  - Don't put an English line straight after a French name (the accent carries over).
- The Eltereforum episode was validated by the Eltereforum: keep its content unchanged in fact-checks.

## Pronunciation (rules live in `build/pronunciation.py`; transcripts keep the written form)

- `.lu` addresses always as letters: EN "dot L U", FR "point L U", DE "Punkt L U". cae.lu = "C-A-E dot L-U".
- Dates or years said wrongly: write them out in `pronunciation.py` (see the SIMPA/KJT examples).
- Settled by Jacques's ear: OKaJu "OKA-JUU", GERO "Jero", Howald "HO-WALD", Zukunftskeess as in the German version,
  lycée "leessay", Maison de l'Orientation as written, Findel "Finndel" (EN). A new hard name → A/B test, Jacques chooses.

## Partner review

- One email per organisation, in French:
  - greeting "Madame, Monsieur,"
  - reply asked by mid-December ("d'ici la mi-décembre")
  - the episodes are "capsules audio"
- The email says:
  - the information comes from official websites
  - the scripts were checked by the Biergerpakt team at MIFA, and MIFA takes responsibility for any errors
  - AI was used for fact-checking and for the voices
  - partners may correct in any language, and the change is carried into the others
- Attachment: `Relecture partenaires/Biergerpakt_Capsule_<key>_relecture.docx`. It must match the current
  recording; `finish_episode.py` rebuilds it.
- Partner corrections: apply them in all four languages, then run `finish_episode.py`.
- In the compiled all-episodes Word document, keep Jacques's status notes in the headings ("final → à envoyer à…").

## Site and safety rules

- Luxembourgish is hidden on the site, but **keep all LB data** (`segments_lb`, `*_lb` fields, `_lb.md` scripts).
- The temporary password screen is for the main site only, never for review pages.
- Admin space `/admin/`: no individual or personal data about listeners.
- The ElevenLabs key lives only in `.env`. Never commit `.env` or paste the key anywhere.

## Git

Jacques pushes himself. After every change, give him:

```
git add -A
git commit -m "<what changed>"
git push
```

Prepend `rm -f .git/index.lock` if a stale lock exists (the iCloud folder sometimes leaves one).
