"""Pronunciation rules for ElevenLabs (text sent to the voice only; transcripts keep the written form).

Used by build/tts_elevenlabs.py via spoken(text, lang). Rules run in order, per language.
Editing a rule re-generates only the sentences whose spoken text changes (cache key = spoken text).
Report of every affected line: python3 build/pronunciation_report.py
"""
import re

DIGITS = {
    "en": "zero one two three four five six seven eight nine".split(),
    "fr": "zéro un deux trois quatre cinq six sept huit neuf".split(),
    "de": "null eins zwei drei vier fünf sechs sieben acht neun".split(),
}
DOT = {"en": "dot", "fr": "point", "de": "Punkt", "lb": "Punkt"}
DASH = {"en": "dash", "fr": "tiret", "de": "Bindestrich", "lb": "Bindestrich"}
OR = {"en": "or", "fr": "ou", "de": "oder", "lb": "oder"}
EMERGENCY_112 = {"en": "one-one-two", "fr": "cent-douze", "de": "eins-eins-zwei"}

# Acronyms said letter by letter -> written "C-N-S" so every voice spells them.
LETTERS = ["CNS", "FNS", "SNJ", "CNAP", "AAA", "DSP", "CGDIS", "CSU", "CIS", "CNIS", "INFS", "INFPC",
           "ASBL", "ONE", "FNR", "LIH", "SES", "IMD", "FSE", "ESF", "GAP", "SIA", "ATVA", "OTP", "QR",
           "ID", "CV", "SMS", "GDP", "PIB", "BIP", "VAT", "TVA", "ATM", "AVC", "EU", "UE"]
LETTERS_LANG = {"en": ["IT", "AI"], "fr": ["IA"], "de": ["IT", "KI"]}
# Acronyms said as a word -> written in normal case so no voice spells them out.
WORDS = {"ADEM": "Adem", "REVIS": "Revis", "ONIS": "Onis", "SYVICOL": "Syvicol", "STATEC": "Statec",
         "LISER": "Liser", "LIST": "List", "ASTA": "Asta", "OSAPS": "Osaps", "ARIS": "Aris", "AMIF": "Amif",
         "BOOST": "Boost", "BEE SECURE": "Bee Secure", "UNESCO": "Unesco", "IBAN": "Iban",
         "PIN": "Pin", "CSIRT": "C-Sirt", "PAN-Bio": "Pan-Bio"}
WORDS_LANG = {"en": {"FEDER": "Feder"}, "fr": {"FEDER": "Féder"}, "de": {"FEDER": "Feder"}}
# Capitals used only for emphasis ("you do NOT need") -> normal words.
EMPHASIS = {"en": ["NOT", "AND"], "fr": ["PAS", "ET"], "de": ["NICHT", "UND"]}
# Names. Biergerpakt, MyGuichet, Guichet, LuxTrust, matricule, eSpace were approved by ear in the
# MyGuichet recordings (EN/FR/DE), so they are deliberately left as written.
# Luxembourgish names: phonetic spellings chosen by Jacques from the A/B test (2026-09-30).
# Everything not listed here was judged fine as written.
NAMES = {
    "en": [(r"(?i)\bZukunftskeess\b", "Tsoo-koonfts-kayss"),                  # EN 1B
           (r"(?i)\bPensiounskeess\b", "Pen-see-ouns-kayss")],                # EN 2B
    "fr": [(r"\bÄddi\b", "Addi"),                                             # no "Ä" in French
           (r"(?i)\bZukunftskeess\b", "Tsoukounftskéss"),                     # FR 1B
           (r"(?i)\bPensiounskeess\b", "Pènnsiounskéss"),                     # FR 2B
           (r"(?i)\bEltereforum\b", "Eltèreu-forum"),                         # FR 3B
           (r"\bZesumme\b", "Tsézoumeu"), (r"\bVereinfachen\b", "Fèraïnnfarènn")],  # FR 5B
}
# Phone numbers written as plain numbers in the scripts -> read digit by digit.
PHONE_NUMBERS = ["8002", "8181", "261210"]


def _digits(lang):
    words = DIGITS.get(lang)
    return lambda m: " ".join(words[int(c)] for c in re.sub(r"\D", "", m.group(0)))


def rules(lang):
    dot, dash = DOT[lang], DASH[lang]
    r = [
        # stage directions such as *(laughs)* are not read aloud
        (r"\s*\*\([^)]*\)\*\s*", " "),
        # "FSE+" -> "FSE plus"; "EFRE/FEDER" or "a / b" -> "EFRE or FEDER"
        (r"(\w)\+", r"\1 plus"),
        (r"\s\+\s", " plus "),
        (r"\s*/\s*(?=[A-ZÄÖÜa-zäöü])", " " + OR[lang] + " "),
        # names built on .LU / LU
        (r"\bGOVCERT\.LU\b", "Gov-Cert " + dot + " L-U"),
        (r"\blu-alert\b", "L-U " + dash + " Alert"),
        (r"\bLU-Alert\b", "L-U Alert"),
        (r"\bJ\.\s?F\.?(?=\s)", "J-F"),
        # spelled-out addresses in the scripts: "c-n-a-p", "m-o", "l-u" -> capital letters
        (r"(?<![\w-])[a-z](?:-[a-z])+(?![\w-])", lambda m: m.group(0).upper()),
        # general .lu rule (Jacques, 2026-09-30): always "dot L-U", never "lu"
        (r"(\w)\.lu\b", r"\1 " + dot + " L-U"),
        (r"\b(" + dot + r") lu\b", r"\1 L-U"),
        (r"(\w)\.(com|net|org|eu)\b", r"\1 " + dot + r" \2"),
    ]
    # Luxembourgish/foreign names: only where a voice clearly mis-reads them (see NAMES)
    for pat, rep in NAMES.get(lang, []):
        r.append((pat, rep))
    if lang in EMERGENCY_112:
        r += [(r"\bCSU-112\b", "C-S-U " + EMERGENCY_112[lang]),
              (r"\b1-1-2\b|\b112\b", EMERGENCY_112[lang])]
    for w, rep in {**WORDS, **WORDS_LANG.get(lang, {})}.items():
        r.append((r"\b" + re.escape(w) + r"\b", rep))
    for w in LETTERS + LETTERS_LANG.get(lang, []):
        r.append((r"\b" + w + r"\b", "-".join(w)))
    for w in EMPHASIS.get(lang, []):
        r.append((r"\b" + w + r"\b", w.lower()))
    if lang in DIGITS:
        r.append((r"\b\d(?:-\d)+\b", _digits(lang)))                      # 2-4-7, 8-0-0-2
        r.append((r"\b(?:" + "|".join(PHONE_NUMBERS) + r")\b", _digits(lang)))
    return r


PRONUNCIATION = {lang: rules(lang) for lang in ("en", "fr", "de", "lb")}


def spoken(text, lang):
    text = text.replace("**", "")
    for pat, rep in PRONUNCIATION.get(lang, []):
        text = re.sub(pat, rep, text)
    return re.sub(r"\s{2,}", " ", text).strip()
