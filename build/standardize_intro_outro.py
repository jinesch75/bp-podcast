#!/usr/bin/env python3
"""Give every episode script (EN/FR/DE/LB) the same beginning and ending:
greeting (2 lines, MyGuichet wording) + revised Biergerpakt intro ... revised outro + farewell (2 lines).
Run from the project root. --write to save; without it, dry run."""
import glob, os, re, sys

LANGS = {"en": "", "fr": "_fr", "de": "_de", "lb": "_lb"}
T = lambda path: open(path, encoding="utf-8").read()
TURN = re.compile(r"^\*\*(ANNA|TOM)( ?):\*\*\s*(.*)$", re.M)

def turns(text):
    return [(m.start(), m.end(), m.group(1), m.group(2), m.group(3)) for m in TURN.finditer(text)]

# ---- standard blocks, taken from MyGuichet (greeting/farewell) and the revised Eltereforum (intro/outro) ----
STD = {}
for lang, suf in LANGS.items():
    myg = turns(T(f"podcast_script_myguichet{suf}.md"))
    elt = turns(T(f"podcast_script_eltereforum{suf}.md"))
    outro = elt[-3][4]
    lead = {"en": "That was our episode about the Eltereforum. ", "fr": "C'était notre épisode sur l'Eltereforum. ",
            "de": "Das war unsere Folge über das Eltereforum. ", "lb": "Dat war eis Episod iwwer den Eltereforum. "}[lang]
    assert outro.startswith(lead), (lang, outro[:60])
    STD[lang] = {"greet": [myg[0][4], myg[1][4]], "intro": elt[2][4],
                 "outro_tail": outro[len(lead):], "bye": [myg[-2][4], myg[-1][4]],
                 "lead": {"en": "That was our episode about {}. ", "fr": "C'était notre épisode sur {}. ",
                          "de": "Das war unsere Folge über {}. ", "lb": "Dat war eis Episod iwwer {}. "}[lang]}

# ---- episode subjects for "That was our episode about ..." ----
SUBJ = {  # key: (en, fr, de, lb) ; None = take it from the existing outro of that language
 "aaa": ("the accident insurance, the AAA", "l'assurance accident, l'AAA", "die Unfallversicherung, die AAA", "d'Accidentsversécherung, d'AAA"),
 "adem": ("ADEM", "l'ADEM", "die ADEM", "d'ADEM"),
 "agriculture": ("the agriculture portal", "le portail de l'agriculture", "das Landwirtschaftsportal", "de Landwirtschaftsportal"),
 "amenagement": ("spatial planning", "l'aménagement du territoire", "die Raumplanung", "d'Landesplanung"),
 "cepas": ("CePAS", "le CePAS", "das CePAS", "de CePAS"),
 "cgdis": ("the CGDIS and the emergency number 112", "le CGDIS et le numéro d'urgence 112", "das CGDIS und die Notrufnummer 112", "de CGDIS an d'Noutruffnummer 112"),
 "cnap": ("the Pensiounskeess", "la Pensiounskeess", "die Pensiounskeess", "d'Pensiounskeess"),
 "culture": ("the culture portal", "le portail de la culture", "das Kulturportal", "de Kulturportal"),
 "demenz": ("the Info-Zenter Demenz", "l'Info-Zenter Demenz", "das Info-Zenter Demenz", "den Info-Zenter Demenz"),
 "enfance": ("the Office National de l'Enfance", "l'Office national de l'enfance", "das Office National de l'Enfance", "den Office national de l'enfance"),
 "environnement": ("the environment portal", "le portail de l'environnement", "das Umweltportal", "den Ëmweltportal"),
 "ess": ("the social and solidarity economy", "l'économie sociale et solidaire", "die Sozial- und Solidarwirtschaft", "d'Sozial- a Solidarwirtschaft"),
 "fondseuropeens": ("European funds in Luxembourg", "les fonds européens au Luxembourg", "die europäischen Fonds in Luxemburg", "d'europäesch Fongen zu Lëtzebuerg"),
 "geoportail": ("the Geoportal", "le Géoportail", "das Geoportal", "de Geoportal"),
 "govcert": ("GOVCERT.LU", "GOVCERT.LU", "GOVCERT.LU", "GOVCERT.LU"),
 "habitat": ("the Observatoire de l'Habitat", "l'Observatoire de l'Habitat", "das Observatoire de l'Habitat", "den Observatoire de l'Habitat"),
 "klima": ("the Klima-Agence", "la Klima-Agence", "die Klima-Agence", "d'Klima-Agence"),
 "lll": ("lifelong learning", "la formation tout au long de la vie", "das lebenslange Lernen", "dat liewenslaangt Léieren"),
 "logement": ("the housing portal", "le portail du logement", "das Wohnungsportal", "de Wunnengsportal"),
 "luxinnovation": ("Luxinnovation", "Luxinnovation", "Luxinnovation", "Luxinnovation"),
 "research": ("Research Luxembourg", "Research Luxembourg", "Research Luxembourg", "Research Luxembourg"),
 "snj": ("the Service National de la Jeunesse", "le Service national de la jeunesse", "den Service National de la Jeunesse", "de Service national de la jeunesse"),
 "space": ("the Luxembourg Space Agency", "la Luxembourg Space Agency", "die Luxembourg Space Agency", "d'Luxembourg Space Agency"),
 "statec": ("STATEC and the statistics portal", "le STATEC et le portail des statistiques", "das STATEC und das Statistikportal", "de STATEC an de Statistikportal"),
 "syvicol": ("SYVICOL", "le SYVICOL", "den SYVICOL", "de SYVICOL"),
 "zesumme": ("Zesumme Vereinfachen", "Zesumme Vereinfachen", "Zesumme Vereinfachen", "Zesumme Vereinfachen"),
}
SUBJ_RE = {"en": r"That was our episode about (.+?)\. This podcast",
           "fr": r"C'était notre épisode sur (.+?)(?:\. Ce podcast|, dans le cadre|, qui fait partie)",
           "de": r"Das war unsere (?:Folge|Episode) über (.+?)(?:\. Dieser Podcast|, Teil des)",
           "lb": r"Dat war eis Episod iwwer?t? (.+?)(?:\. Dëse Podcast|, (?:en )?Deel vum)"}

def subject(key, lang, text_turns):
    if key in SUBJ:
        return SUBJ[key][list(LANGS).index(lang)]
    for t in reversed(text_turns[-4:]):
        m = re.search(SUBJ_RE[lang], t[4])
        if m:
            return m.group(1)
    raise SystemExit(f"no subject for {key} {lang}")

def line(spk, sp, text):
    return f"**{spk}{sp}:** {text}"

write = "--write" in sys.argv
keys = sorted(set(re.sub(r"_(fr|de|lb)$", "", os.path.basename(f)[15:-3]) for f in glob.glob("podcast_script_*.md")))
en_count = {}
for key in keys:
    for lang, suf in LANGS.items():
        path = f"podcast_script_{key}{suf}.md"
        text = T(path)
        tt = turns(text)
        sp = tt[2][3]                      # keep the file's label style ("ANNA :" in FR v "ANNA:")
        std = STD[lang]
        assert tt[0][2] == "ANNA" and tt[1][2] == "TOM" and tt[2][2] == "ANNA" and "Biergerpakt" in tt[2][4], (path, "start")
        subj = subject(key, lang, tt)
        # ending block: last 3 lines (outro + 2 farewell). ADEM translations have only the 2 farewell lines.
        n_end = 3
        if lang != "en" and key in en_count and len(tt) == en_count[key] - 1:
            n_end = 2   # ADEM translations: no outro line yet, only the 2 farewell lines
        if n_end == 3:
            assert re.search(r"Merci|Thank|Dank|merci|Merci|That was|C'était|Das war|Dat war|Wonnerbar|Merveilleux|Wunderbar", tt[-3][4]), (path, "end", tt[-3][4][:60])
        new_start = [line("ANNA", sp, std["greet"][0]), line("TOM", sp, std["greet"][1]), line("ANNA", sp, std["intro"])]
        new_end = [line("ANNA", sp, std["lead"].format(subj) + std["outro_tail"]),
                   line("TOM", sp, std["bye"][0]), line("ANNA", sp, std["bye"][1])]
        sep = text[tt[4][1]:tt[5][0]]      # keep the file's own spacing between lines
        a0, a1 = tt[0][0], tt[2][1]
        b0, b1 = tt[-n_end][0], tt[-1][1]
        middle = text[a1:b0]
        new = text[:a0] + sep.join(new_start) + middle + sep.join(new_end) + text[b1:]
        cnt = len(turns(new))
        if lang == "en":
            en_count[key] = cnt
        else:
            assert cnt == en_count[key], (path, cnt, en_count[key])
        changed = new != text
        print(f"{key:20} {lang} turns={cnt:3} {'changed' if changed else 'same   '} subject=[{subj}]")
        if write and changed:
            open(path, "w", encoding="utf-8").write(new)
