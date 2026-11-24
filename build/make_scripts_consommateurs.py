#!/usr/bin/env python3
"""Builds podcast_script_consommateurs{,_fr,_de,_lb}.md from build/consommateurs_src/<lang>.txt
(body turns, 'A| text' / 'T| text') + the standard Biergerpakt intro/outro taken from the ombudsman scripts."""
import re
KEY = "consommateurs"
HEAD = {
 "en": ('# Podcast Script — "Consumer Protection – The ULC and the European Consumer Centre"', "**Part of the Biergerpakt programme**", "**Hosts:** Anna (woman) and Tom (man)", "**Length:** about 11 minutes — spoken slowly, in simple English"),
 "fr": ("# Script du podcast — « La protection des consommateurs – l'ULC et le Centre européen des consommateurs »", "**Dans le cadre du programme Biergerpakt**", "**Animateurs :** Anna (femme) et Tom (homme)", "**Durée :** environ 10 minutes — parlé lentement, dans un français simple"),
 "de": ("# Podcast-Skript — „Verbraucherschutz – die ULC und das Europäische Verbraucherzentrum“", "**Teil des Biergerpakt-Programms**", "**Moderation:** Anna (Frau) und Tom (Mann)", "**Länge:** etwa 12 Minuten — langsam gesprochen, in einfachem Deutsch"),
 "lb": ("# Podcast-Skript — „Konsumenteschutz – d'ULC an den Europäesche Konsumentenzentrum“", "**Deel vum Biergerpakt-Programm**", "**Moderatioun:** Anna (Fra) an Tom (Mann)", "**Längt:** ongeféier 11 Minutten — lues geschwat, an engem einfache Lëtzebuergesch"),
}
OUTRO_START = {"en": "This podcast is part of the Biergerpakt, a programme", "fr": "Ce podcast fait partie du Biergerpakt, un programme",
               "de": "Dieser Podcast ist Teil des Biergerpakt, ein Programm", "lb": "Dëse Podcast ass Deel vum Biergerpakt, engem Programm"}
SOURCES = {
 "en": "*Sources: ulc.lu (Union luxembourgeoise des consommateurs nouvelle a.s.b.l.) — home page, \"Votre ASBL\" (first constitution in 1961, missions, financing, member households), \"Consultation gratuite\", \"Services proposés\", \"Affiliez-vous\", \"À qui m'adresser ?\", \"Service contentieux ULC\", \"Commission luxembourgeoise des litiges de voyages\", \"Médiateur en assurances\"; cecluxembourg.lu (Centre Européen des Consommateurs GIE Luxembourg) — home page in French, English and German, \"About us\", \"What does ECC do?\", easy-to-read page, \"Defend your rights\", \"The right of withdrawal\", FAQ, \"Contact\"; eccnet.eu (European Consumer Centres Network, \"Our services\"); guichet.public.lu (pages on the ULC and on the European Consumer Centre, \"Reporting unfair commercial practices\"); Directorate for Consumer Protection (mpc.gouvernement.lu, \"Legal protection\"; press conference \"Droits des consommateurs\" of 14 January 2026, gouvernement.lu). The membership fee, opening hours, phone numbers and the amounts of the legal-costs contribution are deliberately not given, because they change. The two opening examples (the sofa, the rental car) are illustrations by the hosts. General information only. Accurate as of November 2026.*",
 "fr": "*Sources : ulc.lu (Union luxembourgeoise des consommateurs nouvelle a.s.b.l.) — page d'accueil, « Votre ASBL » (première constitution en 1961, missions, financement, ménages membres), « Consultation gratuite », « Services proposés », « Affiliez-vous », « À qui m'adresser ? », « Service contentieux ULC », « Commission luxembourgeoise des litiges de voyages », « Médiateur en assurances » ; cecluxembourg.lu (Centre Européen des Consommateurs GIE Luxembourg) — page d'accueil en français, anglais et allemand, « About us », « What does ECC do? », page en langage facile à lire, « Defend your rights », « The right of withdrawal », FAQ, « Contact » ; eccnet.eu (réseau des Centres européens des consommateurs, « Our services ») ; guichet.public.lu (pages sur l'ULC et sur le Centre européen des consommateurs, « Dénoncer une pratique commerciale déloyale ») ; Direction de la protection des consommateurs (mpc.gouvernement.lu, « Protection juridique » ; conférence de presse « Droits des consommateurs » du 14 janvier 2026, gouvernement.lu). Le montant de la cotisation, les horaires, les numéros de téléphone et les montants de la participation aux frais de justice ne sont volontairement pas donnés, car ils changent. Les deux exemples du début (le canapé, la voiture de location) sont des illustrations des animateurs. Informations générales uniquement. Exact en novembre 2026.*",
 "de": "*Quellen: ulc.lu (Union luxembourgeoise des consommateurs nouvelle a.s.b.l.) — Startseite, „Votre ASBL“ (erste Gründung 1961, Aufgaben, Finanzierung, Mitgliedshaushalte), „Consultation gratuite“, „Services proposés“, „Affiliez-vous“, „À qui m'adresser ?“, „Service contentieux ULC“, „Commission luxembourgeoise des litiges de voyages“, „Médiateur en assurances“; cecluxembourg.lu (Europäisches Verbraucherzentrum Luxemburg GIE) — Startseite auf Französisch, Englisch und Deutsch, „About us“, „What does ECC do?“, Seite in leicht lesbarer Sprache, „Defend your rights“, „The right of withdrawal“, FAQ, „Contact“; eccnet.eu (Netzwerk der Europäischen Verbraucherzentren, „Our services“); guichet.public.lu (Seiten über die ULC und über das Europäische Verbraucherzentrum); Direktion für Verbraucherschutz (mpc.gouvernement.lu; Pressekonferenz „Droits des consommateurs“ vom 14. Januar 2026, gouvernement.lu). Die Höhe des Mitgliedsbeitrags, Öffnungszeiten, Telefonnummern und die Beträge der Beteiligung an den Rechtskosten werden bewusst nicht genannt, weil sie sich ändern. Die beiden Beispiele am Anfang (das Sofa, der Mietwagen) sind Veranschaulichungen der Moderatoren. Nur allgemeine Informationen. Stand: November 2026.*",
 "lb": "*Quellen: ulc.lu (Union luxembourgeoise des consommateurs nouvelle a.s.b.l.); cecluxembourg.lu (Centre Européen des Consommateurs GIE Luxembourg); eccnet.eu; guichet.public.lu; Direction de la protection des consommateurs (mpc.gouvernement.lu, gouvernement.lu). Fräi Iwwersetzung: d'Internetsitte hu keng lëtzebuergesch Versioun. D'Cotisatioun, d'Ëffnungszäiten, d'Telefonsnummeren an d'Betrag gi bewosst net genannt, well se änneren. Nëmmen allgemeng Informatiounen. Stand: November 2026.*",
}
def turns(path):
    return [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.startswith("**ANNA") or l.startswith("**TOM")]
for lang in ("en", "fr", "de", "lb"):
    sfx = "" if lang == "en" else "_" + lang
    ref = turns(f"podcast_script_ombudsman{sfx}.md")
    intro, closing, last2 = ref[:3], ref[-3], ref[-2:]
    outro = closing[closing.index(OUTRO_START[lang]):]
    body = []
    for l in open(f"build/consommateurs_src/{lang}.txt", encoding="utf-8"):
        l = l.strip()
        if not l: continue
        who, txt = l.split("| ", 1)
        body.append(f"**{'ANNA' if who == 'A' else 'TOM'}:** {txt.replace('{OUTRO}', outro)}")
    assert "{OUTRO}" not in "".join(body) and len(body) == 92, (lang, len(body))
    out = "\n".join([HEAD[lang][0], "", *HEAD[lang][1:], "", "---", "", *intro, *body, *last2, "", "---", "", SOURCES[lang], ""])
    open(f"podcast_script_{KEY}{sfx}.md", "w", encoding="utf-8").write(out)
    t = turns(f"podcast_script_{KEY}{sfx}.md")
    print(lang, len(t), "turns;", "..." in out, "ellipsis;", sum(len(x.split(":** ",1)[1]) for x in t), "chars")
