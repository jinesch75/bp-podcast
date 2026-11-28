#!/usr/bin/env python3
"""INLL ep (second pass 28 Nov: "Good to know" joined as well; this file records the joins, the .txt files already contain them)
 (27-28 Nov 2026): short lines that stayed off in every take, joined to the next sentence in all four languages.
Edits build/inll_src/<lang>.txt; then run build/make_scripts_inll.py and finish_episode.py inll en,fr,de --reset."""
J = {
 "en": [("Yes, two more. The first", "Yes, there are two more: the first"),
        ("That sounds fair. Where does", "That sounds fair, so where does"),
        ("What happens in the test itself? Is there", "What happens in the test itself: is there"),
        ("Eight weeks sounds short. What can", "Eight weeks sounds short: what can"),
        ("And who are the courses for? Can a teenager", "And who are the courses for: can a teenager"),
        ("And how do you pass? Do the two", "And how do you pass: do the two"),
        ("making progress? Is there a test", "making progress: is there a test"),
        ("many ways to learn it. Classic courses", "many ways to learn it: classic courses"),
        ("price of a course? Does everybody", "price of a course: does everybody")],
 "fr": [("Oui, deux autres. Le premier", "Oui, il y en a deux autres : le premier"),
        ("Cela paraît juste. Où le test", "Cela paraît juste : où le test"),
        ("le test lui-même ? Y a-t-il", "le test lui-même : y a-t-il"),
        ("cela paraît court. Qu'est-ce", "cela paraît court : qu'est-ce"),
        ("s'adressent les cours ? Un adolescent", "s'adressent les cours : un adolescent"),
        ("Et comment réussit-on ? Les deux", "Et comment réussit-on : les deux"),
        ("si je progresse ? Y a-t-il", "si je progresse : y a-t-il"),
        ("façons de l'apprendre. Les cours classiques", "façons de l'apprendre : les cours classiques"),
        ("Et le prix d'un cours ? Est-ce que", "Et le prix d'un cours : est-ce que")],
 "de": [("Ja, noch zwei. Die erste", "Ja, es gibt noch zwei: Die erste"),
        ("Das klingt fair. Wo findet", "Das klingt fair: Wo findet"),
        ("Test selbst ab? Muss man", "Test selbst ab, und muss man"),
        ("Acht Wochen klingt kurz. Was kann", "Acht Wochen klingt kurz: Was kann"),
        ("Kurse gedacht? Kann ein Jugendlicher", "Kurse gedacht: Kann ein Jugendlicher"),
        ("Und wie besteht man? Zählen", "Und wie besteht man: Zählen"),
        ("Fortschritte mache? Gibt es", "Fortschritte mache: Gibt es"),
        ("Arten, es zu lernen. Klassische", "Arten, es zu lernen: Klassische"),
        ("kostet ein Kurs? Zahlt jeder", "kostet ein Kurs, zahlt jeder")],
 "lb": [("Jo, nach zwee. Dat éischt", "Jo, et ginn der nach zwee: Dat éischt"),
        ("Dat kléngt fair. Wou", "Dat kléngt fair: Wou"),
        ("Test selwer of? Muss een", "Test selwer of, a muss een"),
        ("kléngt kuerz. Wat kann", "kléngt kuerz: Wat kann"),
        ("Coursen geduecht? Kann e Jugendlechen", "Coursen geduecht: Kann e Jugendlechen"),
        ("besteet een en? Zielen", "besteet een en: Zielen"),
        ("Fortschrëtter maachen? Gëtt et", "Fortschrëtter maachen: Gëtt et"),
        ("Weeër, et ze léieren. Klassesch", "Weeër, et ze léieren: Klassesch"),
        ("kascht e Cours? Bezilt", "kascht e Cours, bezilt")],
}
J2 = {'en': [('Good to know. One thing', 'Good to know, and one thing')], 'fr': [('Bon à savoir. Ce que', 'Bon à savoir, et ce que')], 'de': [('Gut zu wissen. Was das INLL', 'Gut zu wissen, und was das INLL')], 'lb': [('Gutt ze wëssen. Wat den INLL', 'Gutt ze wëssen, a wat den INLL')]}
if __name__ == "__main__":
  raise SystemExit("Already applied to build/inll_src/*.txt (first pass: J, second pass: J2).")
for lang, pairs in J.items():
    p = f"build/inll_src/{lang}.txt"; s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (lang, a); s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s); print(lang, len(pairs), "joined")
