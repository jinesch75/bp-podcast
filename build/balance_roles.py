#!/usr/bin/env python3
"""Balance the hosts' roles and tidy the junctions around the standard intro/outro (EN/FR/DE/LB .md scripts).
1. SWAP episodes: Anna becomes the explainer and Tom asks (body lines only; names and French gender adjusted).
2. RESTORE: caring/closing lines lost in earlier rewrites, put back just before the outro.
3. Junctions: if Anna would speak twice (intro + next line, or last line + outro), the two lines are joined.
Run from the project root; --write to save (otherwise dry run)."""
import glob, os, re, sys

LANGS = {"en": "", "fr": "_fr", "de": "_de", "lb": "_lb"}
# Episodes where Tom was the explainer and Anna mostly asked; every second one (by episode number) is swapped.
SWAP = ["benevolat", "dsp_cns", "luxtrust", "infosenior", "zukunftskeess", "granderegion", "onis", "clarvia"]
FR_GENDER = {  # French lines whose speaker changes gender
    "benevolat": [("Je suis convaincue", "Je suis convaincu"), ("un chiffre qui m'a surpris", "un chiffre qui m'a surprise")],
    "dsp_cns": [("je suis remboursée", "je suis remboursé")],
}
RESTORE = {  # key: [(speaker, {lang: text})] inserted before the outro
 "cepas": [("TOM", {"en": "And remember... if you or a young person you know is struggling, reaching out is always okay.",
                    "fr": "Et souvenez-vous... si vous, ou un jeune que vous connaissez, traversez une période difficile, demander de l'aide est toujours une bonne chose.",
                    "de": "Und denken Sie daran... wenn Sie oder ein junger Mensch, den Sie kennen, Schwierigkeiten haben, ist es immer in Ordnung, sich Hilfe zu holen.",
                    "lb": "An denkt drun... wann Dir oder e jonke Mënsch, deen Dir kennt, Schwieregkeeten hutt, ass et ëmmer an der Rei, sech Hëllef ze sichen."})],
 "demenz": [("ANNA", {"en": "This was a sensitive topic, so please be gentle with yourself.",
                      "fr": "C'était un sujet sensible, alors soyez doux avec vous-même.",
                      "de": "Das war ein sensibles Thema, also seien Sie sanft mit sich selbst.",
                      "lb": "Dat war e sensibelt Thema, also sidd sanft mat Iech selwer."}),
            ("TOM", {"en": "And if you or someone you love is affected, reaching out for help is always okay.",
                     "fr": "Et si vous ou une personne que vous aimez êtes concernés, demander de l'aide est toujours une bonne chose.",
                     "de": "Und wenn Sie oder ein geliebter Mensch betroffen sind, ist es immer in Ordnung, um Hilfe zu bitten.",
                     "lb": "A wann Dir oder e Mënsch, deen Dir gär hutt, betraff sidd, ass et ëmmer an der Rei, no Hëllef ze froen."})],
 "cnap": [("ANNA", {"en": "Wonderful. That's the end of our journey through the pension system. And remember, it's never too early to think about your pension.",
                    "fr": "Merveilleux. C'est la fin de notre voyage à travers le système de pension. Et rappelez-vous, il n'est jamais trop tôt pour penser à votre pension.",
                    "de": "Wunderbar. Das ist das Ende unserer Reise durch das Pensionssystem. Und denken Sie daran: Es ist nie zu früh, an Ihre Pension zu denken.",
                    "lb": "Wonnerbar. Dat ass d'Enn vun eiser Rees duerch de Pensiounssystem. An denkt drun, et ass ni ze fréi, fir un Är Pensioun ze denken."}),
          ("TOM", {"en": "Check that career statement!", "fr": "Vérifiez ce relevé de carrière !",
                   "de": "Prüfen Sie diesen Laufbahnauszug!", "lb": "Kontrolléiert dee Carrièresrelevé!"})],
}
AFFIRM = {"en": r"^(?:Exactly|Right|Yes|Indeed)[.!,]\s+", "fr": r"^(?:Exactement|Tout à fait|Oui)[.!,]\s+",
          "de": r"^(?:Genau|Richtig|Ja)[.!,]\s+", "lb": r"^(?:Genee|Genau|Richteg|Jo)[.!,]\s+"}
TURN = re.compile(r"^\*\*(ANNA|TOM)( ?):\*\*\s*(.*)$", re.M)

def swap_names(t):
    return re.sub(r"\b(Tom|Anna)\b", lambda m: "Anna" if m.group(1) == "Tom" else "Tom", t)

def process(key, lang, text):
    ms = list(TURN.finditer(text))
    head, foot = text[:ms[0].start()], text[ms[-1].end():]
    sep = text[ms[4].end():ms[5].start()]
    lab = ms[2].group(2)
    L = [[m.group(1), m.group(3)] for m in ms]
    notes = []
    if key in SWAP:
        for t in L[3:-3]:
            t[0] = "TOM" if t[0] == "ANNA" else "ANNA"
            t[1] = swap_names(t[1])
            if lang == "fr":
                for a, b in FR_GENDER.get(key, []):
                    t[1] = t[1].replace(a, b)
        notes.append("roles swapped")
    if key in RESTORE:
        L[-3:-3] = [[spk, d[lang]] for spk, d in RESTORE[key]]
        notes.append(f"restored {len(RESTORE[key])} line(s)")
    if L[3][0] == L[2][0]:                       # Anna: intro + next line -> one line
        L[2][1] += " " + re.sub(AFFIRM[lang], "", L[3][1])
        del L[3]
        notes.append("joined line after intro")
    if L[-4][0] == L[-3][0]:                     # Anna: last line + outro -> one line
        L[-3][1] = L[-4][1] + " " + L[-3][1]
        del L[-4]
        notes.append("joined line before outro")
    body = sep.join(f"**{s}{lab}:** {t}" for s, t in L)
    return head + body + foot, [s for s, _ in L], notes

write = "--write" in sys.argv
keys = sorted(set(re.sub(r"_(fr|de|lb)$", "", os.path.basename(f)[15:-3]) for f in glob.glob("podcast_script_*.md")))
for key in keys:
    seqs = {}
    for lang, suf in LANGS.items():
        path = f"podcast_script_{key}{suf}.md"
        old = open(path, encoding="utf-8").read()
        new, seq, notes = process(key, lang, old)
        seqs[lang] = seq
        if write and new != old:
            open(path, "w", encoding="utf-8").write(new)
    assert all(s == seqs["en"] for s in seqs.values()), (key, "speaker order differs between languages")
    words = {"ANNA": 0, "TOM": 0}
    en = open(f"podcast_script_{key}.md", encoding="utf-8").read() if write else process(key, "en", open(f"podcast_script_{key}.md", encoding="utf-8").read())[0]
    for m in TURN.finditer(en):
        words[m.group(1)] += len(m.group(3).split())
    doubles = [i for i in range(1, len(seqs['en'])) if seqs['en'][i] == seqs['en'][i-1] and (i <= 3 or i >= len(seqs['en']) - 3)]
    print(f"{key:18} lines={len(seqs['en']):3} Anna/Tom words={words['ANNA']:4}/{words['TOM']:4} {'; '.join(notes) or '-'}{'  !! junction double' if doubles else ''}")
