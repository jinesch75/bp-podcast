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
LETTERS = ["KJT", "CJF", "CNPD", "GDPR", "RGPD", "DSGVO", "CAE", "CCSS", "CET", "ULC", "CEC", "CNS", "FNS", "SNJ", "CNAP", "AAA", "DSP", "CGDIS", "CSU", "CIS", "CNIS", "INFS", "INFPC",
           "ASBL", "EBL", "ONE", "FNR", "LIH", "SES", "IMD", "FSE", "ESF", "GAP", "SIA", "ATVA", "OTP", "QR",
           "ID", "CV", "SMS", "GDP", "PIB", "BIP", "VAT", "TVA", "ATM", "AVC", "EU", "UE"]
LETTERS_LANG = {"en": ["IT", "AI"], "fr": ["IA"], "de": ["IT", "KI"]}
# Acronyms said as a word -> written in normal case so no voice spells them out.
WORDS = {"ADEM": "Adem", "REVIS": "Revis", "ONIS": "Onis", "SYVICOL": "Syvicol", "STATEC": "Statec",
         "LISER": "Liser", "LIST": "List", "ASTA": "Asta", "OSAPS": "Osaps", "ARIS": "Aris", "AMIF": "Amif",
         "BOOST": "Boost", "BEE SECURE": "Bee Secure", "UNESCO": "Unesco", "IBAN": "Iban",
         "PIN": "Pin", "CSIRT": "C-Sirt", "PAN-Bio": "Pan-Bio",
         "SIMPA": "Simpa", "COMPA": "Compa"}
# EN LISER/STATEC: Jacques's A/B choices D/D (2026-11-17)
# EN ADEM: A/B choice E "Addem", one pronunciation everywhere (2026-11-20)
WORDS_LANG = {"en": {"FEDER": "Feder", "LISER": "Lyser", "STATEC": "Statek", "ADEM": "Addem"}, "fr": {"FEDER": "Féder"}, "de": {"FEDER": "Feder"}}
# Capitals used only for emphasis ("you do NOT need") -> normal words.
EMPHASIS = {"en": ["NOT", "AND"], "fr": ["PAS", "ET"], "de": ["NICHT", "UND"]}
# Names. Biergerpakt, MyGuichet, Guichet, LuxTrust, matricule, eSpace were approved by ear in the
# MyGuichet recordings (EN/FR/DE), so they are deliberately left as written.
# Luxembourgish names: phonetic spellings chosen by Jacques from the A/B test (2026-09-30).
# Everything not listed here was judged fine as written.
NAMES = {
    "en": [(r"\b23 August 2023\b", "the twenty-third of August, twenty twenty-three"),   # SIMPA ep: Jacques 2026-11-26, the date was garbled
           (r"(?i)\bZukunftskeess\b", "Tsoo-koonfts-kehs"),                   # A/B choice C, closer to German (2026-11-16; was "Tsoo-koonfts-kayss")
           (r"(?i)\ballocation de rentrée scolaire\b", "allo-cah-syon de ron-tray sko-lair"),  # A/B choice B (2026-11-16)
           (r"(?i)\bPensiounskeess\b", "Pen-si-yons-kees"),
           (r"\banalyses (them|it|what|the)\b", r"analyzes \1"),            # verb, not the noun "an-AL-uh-seez" (govcert, 2026-11-19)
           (r"(?i)\bCaisse nationale d'assurance pension\b", "Kess nassyonal dassuranss pansyon"),  # A/B choice B (2026-11-19)                  # Jacques, 2026-11-19 (was "Pen-see-ouns-kayss")
           (r"\bËmweltberodung Lëtzebuerg\b", "Emvelt-berodung Letze-burg"),  # A/B choice E (2026-11-19)
           (r"\bËmweltberodung\b", "Um-velt-beh-roh-doong"),                 # EBL ep (2026-11-10), check by ear
           (r"(?i)\blycées?\b", "leessay"),                                  # Jacques's A/B choice C (2026-11-12)
           (r"\baccessibilite\b", "accessibilité"),
           (r"(?i)\bklima-agence\b", "Clima-Agence"),
           (r"(?i)\bobservation foncière\b", "observassion fonsyère"),       # A/B choice C (2026-11-17)                       # A/B choice B: Anna said "Kly-ma" (2026-11-16)
           (r"(?i)\bl[ëe]tz ?prepare\b", "Let's prepare"),                  # Lëtz prepare ep (2026-11-14), check by ear
           (r"\bLëtz\b", "Lets"),
           (r"\bBass du prett\b", "Bass doo prett"),
           (r"\binfocrise\b", "info-creeze"),
           (r"\b113\b", "one one three"),
           (r"(?i)\bdon ?du ?sang\b", "dawn dew sahn"),                     # dondusang ep: Jacques's A/B choice B (2026-11-20)
           (r"(?i)\bicanvote\b", "I can vote"),
           (r"(?i)\bclubaktivplus\b", "Club Aktiv Plus"),
           (r"\bSeniorentelefon\b", "Senioren-Telefon"),   # SIMPA ep (2026-11-26), as written "Senioren-Telefon" in the Info-Seniors episode; check by ear
           (r"\bKanner-Jugendtelefon\b", "Kanner-Yoogunt-telefon"),   # KJT ep (2026-11-24), not A/B tested: check by ear
           (r"\bHowald\b", "Hoh-wald"),   # consommateurs ep: Jacques 2026-11-24 "HO-WALD", Wald as in Waldorf (A/B build/el_test/pron_howald_en_AB.mp3, B used)
           (r"(?i)\bokaju\b", "Oka-joo")],   # ombudsman ep: Jacques 2026-11-23 "OKA-JUU", J as in "juice" (was "Oh-kah-yoo")
    #jepeuxvoter ep (2026-11-20)                         # website said the French way, A/B choice A (2026-11-13)
    "fr": [(r"\b23 août 2023\b", "vingt-trois août deux mille vingt-trois"),   # SIMPA ep (2026-11-26)
           (r"\bÄddi\b", "Addi"),                                             # no "Ä" in French
           (r"(?i)\bZukunftskeess\b", "Tsoukounftskéss"),                     # FR 1B
           (r"(?i)\bPensiounskeess\b", "Pènnsiounskéss"),                     # FR 2B
           (r"(?i)\bEltereforum\b", "Eltèreu-forum"),                         # FR 3B
           (r"\bZesumme\b", "Tsézoumeu"), (r"\bVereinfachen\b", "Fèraïnnfarènn"),  # FR 5B
           (r"\bËmweltberodung\b", "Eumvèlt-bérodoung"),                     # EBL ep (2026-11-10), check by ear
           (r"(?i)\bl[ëe]tz ?prepare\b", "Lets pri-pair"),                   # Lëtz prepare ep (2026-11-14), check by ear
           (r"\bLëtz\b", "Lets"),
           (r"\bBass du prett\b", "Bass dou prèt"),
           (r"\bKanner-Jugendtelefon\b", "Kanneur-Youguènnt-téléfone"),   # KJT ep (2026-11-24), not A/B tested: check by ear
           (r"\bElterentelefon\b", "Elteurènn-téléfone"),
           (r"\bSeniorentelefon\b", "Séniorènn-téléfone"),   # SIMPA ep (2026-11-26), not A/B tested: check by ear
           (r"(?i)\bdondusang\b", "don du sang"),                           # dondusang ep (2026-11-20)
           (r"(?i)\bjepeuxvoter\b", "je peux voter"),
           (r"(?i)\bclubaktivplus\b", "Club Aktiv Plus"),
           (r"(?i)\bokaju\b", "Okadjou")],   # ombudsman ep: Jacques 2026-11-23 "OKA-JUU", J as in "juice" (was "Okayou")
    #jepeuxvoter ep (2026-11-20)
    "de": [(r"\bwurde 1992 gegründet\b", "wurde neunzehnhundertzweiundneunzig gegründet"),
           (r"\bwurde 2022 gestartet\b", "wurde zweitausendzweiundzwanzig gestartet"),   # Zesumme Vereinfachen: Jacques 2026-11-26, year not pronounced correctly   # KJT ep: Jacques 2026-11-26, Tom said "1990"
           (r"\bvom 23\. August 2023\b", "vom dreiundzwanzigsten August zweitausenddreiundzwanzig"),   # SIMPA ep (2026-11-26), was slow
           (r"(?i)\bl[ëe]tz ?prepare\b", "Lets pripär"),                    # Lëtz prepare ep (2026-11-14), check by ear
           (r"\bLëtz\b", "Lets"),
           (r"\binfocrise\b", "Info-Kriis"),
           (r"(?i)\bdon ?du ?sang\b", "Don dü Sang"),                       # dondusang ep (2026-11-20), check by ear
           (r"(?i)\bichkannwaehlen\b", "ich kann wählen"),
           (r"(?i)\bclubaktivplus\b", "Club Aktiv Plus"),
           (r"(?i)\bokaju\b", "Okadschuh")],   # ombudsman ep: Jacques 2026-11-23 "OKA-JUU", J as in "juice" (was "Okaju")
    #                # jepeuxvoter ep (2026-11-20)
}
# Phone numbers written as plain numbers in the scripts -> read digit by digit.
PHONE_NUMBERS = ["8002", "8181", "261210", "247-86000", "26 432 432"]  # 26 432 432: ala Alzheimer help line (fact-check 2026-11-09)
# e-mail addresses (fact-check update 2026-09-30: contact@talentdesk.lu)
AT = {"en": "at", "fr": "arobase", "de": "at", "lb": "at"}


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
        # e-mail: "name@site.lu" -> "name at site dot L-U"
        (r"(\w)@(\w)", r"\1 " + AT[lang] + r" \2"),
        # general .lu rule (Jacques, 2026-09-30): always "dot L-U", never "lu"
        (r"(\w)\.lu\b", r"\1 " + dot + " L-U"),
        (r"\b(" + dot + r") lu\b", r"\1 L-U"),
        # cae.lu (Zukunftskeess) always spelled out: "C-A-E dot L-U" (Jacques, 2026-11-16)
        (r"\bcae\b", "C-A-E"),
        # fns.lu likewise spelled out: "F-N-S dot L-U" (Jacques, 2026-11-17; "fns.lu" was cut off)
        (r"\bfns\b", "F-N-S"),
        # ccss.lu spelled out: "C-C-S-S dot L-U" (ccss ep, 2026-11-20)
        (r"\bccss\b", "C-C-S-S"),
        # cnpd.lu (CNPD ep, 2026-11-24): "C-N-P-D dot L-U"
        (r"\bcnpd\b", "C-N-P-D"),
        # kjt.lu (KJT ep, 2026-11-24): "K-J-T dot L-U"
        (r"\bkjt\b", "K-J-T"),
        # cet.lu (CET ep, 2026-11-23): "C-E-T dot L-U"; only before dot/point/Punkt, because "cet" is a French word
        (r"\bcet(?= (?:dot|point|Punkt) )", "C-E-T"),
        # consommateurs ep (2026-11-24): ulc.lu -> "U-L-C dot L-U", cecluxembourg.lu -> "C-E-C Luxembourg dot L-U"
        (r"\bulc(?= (?:dot|point|Punkt) )", "U-L-C"),
        (r"\bcecluxembourg\b", "C-E-C Luxembourg"),
        # mediateursante ep (2026-11-24): mediateursante.public.lu -> "médiateur santé dot public dot L-U" (French words said the French way)
        (r"\bmediateursante\b", "médiateur santé"),
        # GouvID app (fact-check 2026-11-02): "Gouv I-D"
        (r"\bGouvID\b", "Gouv I-D"),
        # activitesseniors ep (2026-11-20): GERO departments read as two words; MEC asbl spelled out
        (r"\bgeroAKTIV\b", "gero Aktiv"), (r"\bgeroPRO\b", "gero Pro"), (r"\bgeroRESEARCH\b", "gero Research"),
        (r"\bMEC\b", "M-E-C"),
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
    if lang == "en":   # GERO is said "Jero" (Jacques, 2026-11-20); English only so far
        r += [(r"\bGERO\b", "Jero"), (r"\bgero (Aktiv|Pro|Research)\b", r"Jero \1")]
    if lang in DIGITS:
        # KJT ep (2026-11-24): helpline numbers digit by digit, with a small pause between the two groups
        if lang == "fr":   # like "cent-douze" for 112: three "un" in a row were not clearly audible
            r.append((r"\b116 111\b", "cent seize, cent onze"))
        for num in ("116 111", "8002 4444", "8002 1234"):
            g1, g2 = num.split()
            r.append((r"\b" + num + r"\b", " ".join(DIGITS[lang][int(c)] for c in g1) + ", " + " ".join(DIGITS[lang][int(c)] for c in g2)))
        r.append((r"\b\d(?:-\d)+\b", _digits(lang)))                      # 2-4-7, 8-0-0-2
        r.append((r"\b(?:" + "|".join(PHONE_NUMBERS) + r")\b", _digits(lang)))
    return r


PRONUNCIATION = {lang: rules(lang) for lang in ("en", "fr", "de", "lb")}


def spoken(text, lang):
    text = text.replace("**", "")
    for pat, rep in PRONUNCIATION.get(lang, []):
        text = re.sub(pat, rep, text)
    return re.sub(r"\s{2,}", " ", text).strip()
