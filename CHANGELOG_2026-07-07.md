# Update 7 July 2026 — Episodes 1–5 rework

## What changed

- Episodes 1–5 rebuilt from the reworked English scripts (new Biergerpakt intro & outro, updated content). FR / DE / LB scripts retranslated one-to-one; EN / FR / DE audio re-recorded; read-along transcripts re-synced.
- Episode order now matches the document: **Episode 2 = Volunteering**, **Episode 4 = Your Health, Online (DSP & CNS)** (previously swapped).
- New titles on the site: Ep 1 "…Administrations" (plural), Ep 4 "Your Health, Online – The Dossier de Soins Partagé and How the CNS Pays You Back".
- All other episodes (6–41): new intro/outro applied to their English `.md` scripts and to the Word document only. Their audio, translations and website transcripts are unchanged until each episode is reworked.
- New Word document: `Biergerpakt_Podcast_Scripts_All_Episodes_EN_2026-07-07.docx` (all 41 episodes, new intro/outro everywhere, new numbering).

## Quiz changes (questions about removed content)

| Episode | Question | Change | Reason |
|---|---|---|---|
| 1 MyGuichet.lu | Q2 "What does the French word 'guichet' mean?" | Replaced with: "Why is MyGuichet.lu described as an 'online counter'?" | The explanation of the word "guichet" was removed from the script (only the online-counter comparison remains). |
| 2 Volunteering | Q5 on "voluntary service" for under-30s | Replaced with: question on the 3-step method to start (think about what you enjoy → register on benevolat.lu → offer your help) | The voluntary-service / National Youth Service passage was removed. |
| 3 Eltereforum | Q4 "Does using the Eltereforum cost money?" | Replaced with: question on what happens with a serious, specific problem (team listens and guides you to the right specialised service) | The "free of charge" statement was removed from the script. |
| 3 Eltereforum | Q5 on the "Elteremobil" | Replaced with: question on what you find on eltereforum.lu (information platform + agenda of all activities) | The Elteremobil was removed from the script. |
| 4 DSP & CNS | Q5 on activating the eSanté account | Reworded: removed "immediately, with your LuxTrust login"; now mentions the MyDSP app | Script no longer says "immediately with LuxTrust"; MyDSP app is new content. |
| 5 LU-Alert | — | No changes needed | All 5 questions still match the new script. |

All replacements were translated to FR / DE / LB as well. Episode descriptions and topic chips for episodes 1–4 were updated to match the new scripts (e.g. removed "Mostly free" and "The Elteremobil" chips on Ep 3).

## Review links for institutions (one episode per link)

Each link shows ONLY that institution's episode — the other episodes are not present in the page at all. Links go live after the next push to GitHub Pages.

| Episode | Institution link |
|---|---|
| 1 — MyGuichet.lu | https://jinesch75.github.io/bp-podcast/review/myguichet-053c48e6e0/ |
| 2 — Volunteering | https://jinesch75.github.io/bp-podcast/review/benevolat-2f0edbec5e/ |
| 3 — Eltereforum | https://jinesch75.github.io/bp-podcast/review/eltereforum-12a64449a2/ |
| 4 — DSP & CNS | https://jinesch75.github.io/bp-podcast/review/dsp-cns-4d7196ead9/ |
| 5 — LU-Alert | https://jinesch75.github.io/bp-podcast/review/lualert-7beafb2771/ |

To generate a review page for any other episode later: `node build/make_review.js <key>`.
