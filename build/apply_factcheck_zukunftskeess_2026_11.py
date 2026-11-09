#!/usr/bin/env python3
"""Fact-check Zukunftskeess (9 Nov 2026): law 8746 (in force 1 Jan 2027) + small corrections.
EN/FR/DE/LB scripts. Idempotent (skips a change whose new text is already present). Turn counts unchanged.
Run from the project root."""
import re, sys
R = {}
R[""] = [
 ("The total is about one thousand seven hundred and forty euros.",
  "The total is more than one thousand seven hundred euros — and from 2027, it rises with the cost of living."),
 ("three equal parts, of about five hundred and eighty euros each.", "three equal parts, of nearly six hundred euros each."),
 ("Right now it's a bit over three hundred euros per child each month.",
  "And there's good news: a new law raises it from January 2027. From then on, it's more than three hundred and fifty euros per child each month."),
 ("with what's called the index. So for the exact figure today",
  "with what's called the index. And from 2027, the same goes for the birth allowance, the back-to-school allowance, and the extra allowance for children with a disability. So for the exact figure today"),
 ("It lands in your bank account that day or the next.", "It lands in your bank account that day or the next — or a day or two later with a bank abroad."),
 ("For children from six to eleven, it's around one hundred and fifteen euros. For children twelve and over, it's around two hundred and thirty-five euros.",
  "With the new law, from 2027 it's more than one hundred and seventy-five euros for children from six to eleven. And more than three hundred and twenty-five euros for children twelve and over."),
 ("keeps the right to the family allowance.",
  "keeps the right to the family allowance. And from 2027, a new law makes one more thing clear: the children of your husband, wife or partner can count too — if they mainly live with you, or if you can show that you really support them."),
 ("send documents to the Zukunftskeess, change your bank details, or get a payment certificate. There's even an online assistant that guides you through the family allowance application, step by step.",
  "send documents to the Zukunftskeess, or change your bank details. There's even an online assistant that guides you through the family allowance application, step by step. And if you need a payment certificate, there's a simple online form on the Zukunftskeess website."),
 ("the prenatal part. About five hundred and eighty euros.", "the prenatal part. Nearly six hundred euros."),
 ("by the twenty-fifth — a bit over three hundred euros, automatically.", "by the twenty-fifth — more than three hundred and fifty euros, automatically."),
 ("to keep the allowance going up to twenty-five.", "to keep the allowance going up to twenty-five — you can now do it online too, on MyGuichet.lu."),
 ("A birth allowance of about one thousand seven hundred euros", "A birth allowance of more than one thousand seven hundred euros"),
 ("for each child — a bit over three hundred euros — that grows", "for each child — more than three hundred and fifty euros from 2027 — that grows"),
]
R["_fr"] = [
 ("Le total est d'environ mille sept cent quarante euros.",
  "Le total est de plus de mille sept cents euros — et à partir de 2027, il suit le coût de la vie."),
 ("en trois parts égales, d'environ cinq cent quatre-vingts euros chacune.", "en trois parts égales, de près de six cents euros chacune."),
 ("En ce moment, c'est un peu plus de trois cents euros par enfant chaque mois. Et voici un point clé — elle augmente à mesure",
  "Et il y a une bonne nouvelle : une nouvelle loi l'augmente à partir de janvier 2027. Dès lors, c'est plus de trois cent cinquante euros par enfant chaque mois. Et voici un point clé — elle augmente encore à mesure"),
 ("avec ce qu'on appelle l'index. Donc pour le chiffre exact",
  "avec ce qu'on appelle l'index. Et à partir de 2027, c'est aussi le cas pour l'allocation de naissance, l'allocation de rentrée scolaire, et l'allocation spéciale pour les enfants en situation de handicap. Donc pour le chiffre exact"),
 ("ce jour-là ou le lendemain.", "ce jour-là ou le lendemain — ou un ou deux jours plus tard avec une banque à l'étranger."),
 ("Pour les enfants de six à onze ans, c'est environ cent quinze euros. Pour les enfants de douze ans et plus, c'est environ deux cent trente-cinq euros.",
  "Avec la nouvelle loi, à partir de 2027, c'est plus de cent soixante-quinze euros pour les enfants de six à onze ans. Et plus de trois cent vingt-cinq euros pour les enfants de douze ans et plus."),
 ("garde le droit à l'allocation familiale.",
  "garde le droit à l'allocation familiale. Et à partir de 2027, une nouvelle loi précise encore une chose : les enfants de ton mari, de ta femme ou de ton partenaire peuvent aussi compter — s'ils vivent principalement avec toi, ou si tu peux montrer que tu subviens vraiment à leurs besoins."),
 ("envoyer des documents à la Zukunftskeess, changer tes coordonnées bancaires, ou obtenir un certificat de paiement. Il y a même un assistant en ligne qui te guide pas à pas dans la demande d'allocation familiale.",
  "envoyer des documents à la Zukunftskeess, ou changer tes coordonnées bancaires. Il y a même un assistant en ligne qui te guide pas à pas dans la demande d'allocation familiale. Et si tu as besoin d'un certificat de paiement, il y a un simple formulaire en ligne sur le site de la Zukunftskeess."),
 ("la part prénatale. Environ cinq cent quatre-vingts euros.", "la part prénatale. Près de six cents euros."),
 ("pour le vingt-cinq — un peu plus de trois cents euros, automatiquement.", "pour le vingt-cinq — plus de trois cent cinquante euros, automatiquement."),
 ("pour que l'allocation continue jusqu'à vingt-cinq ans.", "pour que l'allocation continue jusqu'à vingt-cinq ans — tu peux maintenant le faire en ligne aussi, sur MyGuichet.lu."),
 ("Une allocation de naissance d'environ mille sept cents euros", "Une allocation de naissance de plus de mille sept cents euros"),
 ("pour chaque enfant — un peu plus de trois cents euros — qui augmente", "pour chaque enfant — plus de trois cent cinquante euros à partir de 2027 — qui augmente"),
]
R["_de"] = [
 ("Insgesamt sind das etwa eintausendsiebenhundertvierzig Euro.",
  "Insgesamt sind das mehr als eintausendsiebenhundert Euro — und ab 2027 steigt sie mit den Lebenshaltungskosten."),
 ("von je etwa fünfhundertachtzig Euro.", "von je fast sechshundert Euro."),
 ("Im Moment sind es etwas mehr als dreihundert Euro pro Kind jeden Monat.",
  "Und es gibt gute Nachrichten: Ein neues Gesetz erhöht es ab Januar 2027. Ab dann sind es mehr als dreihundertfünfzig Euro pro Kind jeden Monat."),
 ("mit dem sogenannten Index. Für die genaue Zahl",
  "mit dem sogenannten Index. Und ab 2027 gilt das auch für die Geburtszulage, die Schulanfangszulage und die Sonderzulage für Kinder mit einer Behinderung. Für die genaue Zahl"),
 ("an diesem Tag oder am nächsten auf deinem Bankkonto.", "an diesem Tag oder am nächsten auf deinem Bankkonto — oder ein, zwei Tage später bei einer Bank im Ausland."),
 ("Für Kinder von sechs bis elf Jahren sind es etwa einhundertfünfzehn Euro. Für Kinder ab zwölf Jahren sind es etwa zweihundertfünfunddreißig Euro.",
  "Mit dem neuen Gesetz sind es ab 2027 mehr als einhundertfünfundsiebzig Euro für Kinder von sechs bis elf Jahren. Und mehr als dreihundertfünfundzwanzig Euro für Kinder ab zwölf Jahren."),
 ("behält den Anspruch auf das Kindergeld.",
  "behält den Anspruch auf das Kindergeld. Und ab 2027 stellt ein neues Gesetz noch etwas klar: Auch die Kinder deines Mannes, deiner Frau oder deines Partners können zählen — wenn sie hauptsächlich bei dir leben, oder wenn du zeigen kannst, dass du wirklich für sie sorgst."),
 ("Dokumente an die Zukunftskeess schicken, deine Bankdaten ändern, oder eine Zahlungsbescheinigung bekommen. Es gibt sogar einen Online-Assistenten, der dich Schritt für Schritt durch den Kindergeldantrag führt.",
  "Dokumente an die Zukunftskeess schicken, oder deine Bankdaten ändern. Es gibt sogar einen Online-Assistenten, der dich Schritt für Schritt durch den Kindergeldantrag führt. Und wenn du eine Zahlungsbescheinigung brauchst, gibt es ein einfaches Online-Formular auf der Website der Zukunftskeess."),
 ("den vorgeburtlichen Teil. Etwa fünfhundertachtzig Euro.", "den vorgeburtlichen Teil. Fast sechshundert Euro."),
 ("bis zum fünfundzwanzigsten — etwas mehr als dreihundert Euro, automatisch.", "bis zum fünfundzwanzigsten — mehr als dreihundertfünfzig Euro, automatisch."),
 ("damit das Kindergeld bis fünfundzwanzig weiterläuft.", "damit das Kindergeld bis fünfundzwanzig weiterläuft — das geht jetzt auch online, auf MyGuichet.lu."),
 ("Eine Geburtszulage von etwa eintausendsiebenhundert Euro", "Eine Geburtszulage von mehr als eintausendsiebenhundert Euro"),
 ("für jedes Kind — etwas mehr als dreihundert Euro — das mit sechs", "für jedes Kind — mehr als dreihundertfünfzig Euro ab 2027 — das mit sechs"),
]
R["_lb"] = [
 ("Den Total ass ongeféier dausendsiwenhonnertvéierzeg Euro.",
  "Den Total ass méi wéi dausendsiwenhonnert Euro — an ab 2027 geet en mat de Liewenskäschten erop."),
 ("vu ronderëm fënnefhonnertachtzeg Euro pro Stéck.", "vu bal sechshonnert Euro pro Stéck."),
 ("Am Moment ass et e bësse méi wéi dräihonnert Euro pro Kand all Mount.",
  "An et gëtt eng gutt Noriicht: En neit Gesetz hieft et ab Januar 2027 un. Vun do un ass et méi wéi dräihonnertfofzeg Euro pro Kand all Mount."),
 ("wat een den Index nennt. Also fir déi genee Zuel",
  "wat een den Index nennt. An ab 2027 gëllt dat och fir d'Geboortsprime, d'Schoulufanksallocatioun an d'Spezialallocatioun fir Kanner mat enger Behënnerung. Also fir déi genee Zuel"),
 ("deen Dag oder deen drop.", "deen Dag oder deen drop — oder een, zwee Deeg méi spéit bei enger Bank am Ausland."),
 ("Fir Kanner vu sechs bis eelef ass et ronderëm honnertfofzéng Euro. Fir Kanner zwielef an eeler ass et ronderëm zweehonnertfënnefandrësseg Euro.",
  "Mam neie Gesetz ass et ab 2027 méi wéi honnertfënnefasiwwenzeg Euro fir Kanner vu sechs bis eelef. A méi wéi dräihonnertfënnefanzwanzeg Euro fir Kanner zwielef an eeler."),
 ("behält d'Recht op d'Kannergeld.",
  "behält d'Recht op d'Kannergeld. An ab 2027 mécht en neit Gesetz nach eng Saach kloer: D'Kanner vun dengem Mann, denger Fra oder dengem Partner kënnen och zielen — wa si haaptsächlech bei dir wunnen, oder wann s du weise kanns, datt s du wierklech fir si suergs."),
 ("Dokumenter un d'Zukunftskeess schécken, deng Bankdaten änneren, oder e Bezuelungszertifikat kréien. Et gëtt esouguer en Online-Assistent, deen dech Schrëtt fir Schrëtt duerch d'Kannergeld-Demande féiert.",
  "Dokumenter un d'Zukunftskeess schécken, oder deng Bankdaten änneren. Et gëtt esouguer en Online-Assistent, deen dech Schrëtt fir Schrëtt duerch d'Kannergeld-Demande féiert. A wann s du e Bezuelungszertifikat brauchs, gëtt et en einfache Online-Formulaire op der Websäit vun der Zukunftskeess."),
 ("de pränatalen Deel. Ongeféier fënnefhonnertachtzeg Euro.", "de pränatalen Deel. Bal sechshonnert Euro."),
 ("bis de fënnefanzwanzegsten — e bësse méi wéi dräihonnert Euro, automatesch.", "bis de fënnefanzwanzegsten — méi wéi dräihonnertfofzeg Euro, automatesch."),
 ("bis op fënnefanzwanzeg weidergoen ze loossen.", "bis op fënnefanzwanzeg weidergoen ze loossen — dat geet elo och online, op MyGuichet.lu."),
 ("Eng Geboortsprime vun ongeféier dausendsiwenhonnert Euro", "Eng Geboortsprime vu méi wéi dausendsiwenhonnert Euro"),
 ("fir all Kand — e bësse méi wéi dräihonnert Euro — dat", "fir all Kand — méi wéi dräihonnertfofzeg Euro ab 2027 — dat"),
]
SRC_OLD = re.compile(r"\*Sources?:.*?\*\s*$", re.S)
SRC_EN = ("*Sources: cae.public.lu (Caisse pour l'avenir des enfants / Zukunftskeess — the Children's Future Fund), guichet.public.lu official pages "
 "\"Family allowance\", \"Birth allowance\" and \"Social parameters\" (IGSS social parameters at 1 June 2026, index 992.24: family allowance €315.04 per child/month, "
 "+€23.81 from age 6, +€59.44 from age 12; back-to-school allowance €115 / €235; birth allowance €1,740.09 in three instalments of €580.03; special supplementary allowance €200), "
 "and law no. 8746 (voted 15 October 2026, in force 1 January 2027): family allowance +€45 per child/month and +€15 more from age 12; back-to-school allowance €175 (6–11) and €325 (12+); "
 "indexation extended to the birth, back-to-school and special supplementary allowances; children of a cross-border worker's spouse or partner (chd.lu dossier 8746). "
 "Amounts are indexed and change over time — check the official \"social parameters\" page on guichet.lu for the current figures. General information only. Fact-checked 9 November 2026.*")
write = "--dry" not in sys.argv
for L, pairs in R.items():
    p = f"podcast_script_zukunftskeess{L}.md"
    s = open(p, encoding="utf-8").read()
    n0 = len(re.findall(r"^\*\*(ANNA|TOM)\s?:\*\*", s, re.M))
    done = 0
    for old, new in pairs:
        if new in s: continue
        c = s.count(old)
        if c != 1: sys.exit(f"{p}: expected 1 match, got {c}: {old[:60]}")
        s = s.replace(old, new); done += 1
    if L == "" and "law no. 8746" not in s:
        s2, k = SRC_OLD.subn(SRC_EN, s)
        if k != 1: sys.exit("EN sources footer not found")
        s = s2; done += 1
    n1 = len(re.findall(r"^\*\*(ANNA|TOM)\s?:\*\*", s, re.M))
    assert n0 == n1, (p, n0, n1)
    print(p, "changes:", done, "turns:", n1)
    if write: open(p, "w", encoding="utf-8").write(s)

# Source footers FR/DE/LB (not spoken)
FOOT = {
 "_fr": "*Sources : cae.public.lu (Caisse pour l'avenir des enfants / Zukunftskeess), pages officielles de guichet.public.lu « Allocation familiale », « Allocation de naissance » et « Paramètres sociaux » (paramètres sociaux IGSS au 1er juin 2026, indice 992,24 : allocation familiale 315,04 € par enfant/mois, +23,81 € dès 6 ans, +59,44 € dès 12 ans ; allocation de rentrée scolaire 115 € / 235 € ; allocation de naissance 1 740,09 € en trois tranches de 580,03 € ; allocation spéciale supplémentaire 200 €), et loi n° 8746 (votée le 15 octobre 2026, en vigueur le 1er janvier 2027) : allocation familiale +45 € par enfant/mois et +15 € de plus dès 12 ans ; allocation de rentrée scolaire 175 € (6-11 ans) et 325 € (12 ans et plus) ; indexation étendue aux allocations de naissance, de rentrée scolaire et spéciale supplémentaire ; enfants du conjoint ou partenaire d'un frontalier (dossier chd.lu 8746). Les montants sont indexés — consultez la page « Paramètres sociaux » sur guichet.lu pour les chiffres actuels. Information générale. Vérifié le 9 novembre 2026.*",
 "_de": "*Quellen: cae.public.lu (Caisse pour l'avenir des enfants / Zukunftskeess), offizielle Seiten von guichet.public.lu „Kindergeld\", „Geburtszulage\" und „Soziale Parameter\" (IGSS-Sozialparameter am 1. Juni 2026, Index 992,24: Kindergeld 315,04 € pro Kind/Monat, +23,81 € ab 6 Jahren, +59,44 € ab 12 Jahren; Schulanfangszulage 115 € / 235 €; Geburtszulage 1.740,09 € in drei Raten von 580,03 €; Sonderzulage 200 €) sowie Gesetz Nr. 8746 (verabschiedet am 15. Oktober 2026, in Kraft am 1. Januar 2027): Kindergeld +45 € pro Kind/Monat und +15 € zusätzlich ab 12 Jahren; Schulanfangszulage 175 € (6–11) und 325 € (ab 12); Indexierung auch für Geburtszulage, Schulanfangszulage und Sonderzulage; Kinder des Ehe- oder Lebenspartners eines Grenzgängers (chd.lu, Dossier 8746). Die Beträge sind indexiert — aktuelle Zahlen auf der Seite „Soziale Parameter\" auf guichet.lu. Allgemeine Informationen. Geprüft am 9. November 2026.*",
 "_lb": "*Quellen: cae.public.lu (Caisse pour l'avenir des enfants / Zukunftskeess), offiziell Säite vu guichet.public.lu (Kannergeld, Geboortsprime, Sozialparameter vum 1. Juni 2026, Index 992,24: 315,04 € pro Kand/Mount, +23,81 € ab 6 Joer, +59,44 € ab 12 Joer; Schoulufanksallocatioun 115 € / 235 €; Geboortsprime 1.740,09 € an dräi Tranchë vu 580,03 €; Spezialallocatioun 200 €) an d'Gesetz Nr. 8746 (gestëmmt den 15. Oktober 2026, a Kraaft den 1. Januar 2027): +45 € pro Kand/Mount an +15 € méi ab 12 Joer; Schoulufanksallocatioun 175 € (6–11) an 325 € (ab 12); Indexéierung och fir Geboortsprime, Schoulufanksallocatioun a Spezialallocatioun; Kanner vum Partner vun engem Grenzgänger (chd.lu, Dossier 8746). D'Beträg sinn indexéiert — kuckt d'Säit „Sozialparameter\" op guichet.lu. Allgemeng Informatioun. Iwwerpréift den 9. November 2026.*",
}
for L, f in FOOT.items():
    p = f"podcast_script_zukunftskeess{L}.md"
    s = open(p, encoding="utf-8").read()
    if "8746" in s: continue
    s2, k = re.subn(r"\*(Sources?|Quellen)\s?:.*?\*\s*$", lambda m: f + "\n", s, flags=re.S)
    if k != 1: print("footer not found", p); continue
    if write: open(p, "w", encoding="utf-8").write(s2); print(p, "footer updated")
