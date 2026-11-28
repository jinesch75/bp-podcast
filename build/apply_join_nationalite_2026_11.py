#!/usr/bin/env python3
"""nationalite (27 Nov 2026): short lines that stayed off in every take are joined to the next/previous sentence,
in all four languages (CLAUDE.md rule 5). Runs once; aborts if a source text is not found. Then make_scripts_nationalite.py."""
R = {
 "en": [("There are several. Some people", "There are several: some people"),
        ("There are three. You need to pass", "There are three: you need to pass"),
        ("worried about it. What does it look like?", "worried about it, so what does it look like?"),
        ("So the law already does a lot. For adults", "So the law already does a lot, and for adults"),
        ("That sounds fair. And what about people", "That sounds fair, and what about people"),
        ("That already covers many families. Who are the remaining cases for?", "That already covers many families, so who are the remaining cases for?"),
        ("So the Biergerpakt counts here too! And how does", "So the Biergerpakt counts here too, and how does")],
 "fr": [("Il y en a plusieurs. Certaines personnes", "Il y en a plusieurs : certaines personnes"),
        ("Il y en a trois. Il faut réussir", "Il y en a trois : il faut réussir"),
        ("s'en inquiètent. À quoi ressemble-t-il ?", "s'en inquiètent : à quoi ressemble-t-il ?"),
        ("La loi fait donc déjà beaucoup. Pour les adultes", "La loi fait donc déjà beaucoup, et pour les adultes"),
        ("Cela paraît juste. Et qu'en est-il", "Cela paraît juste, et qu'en est-il"),
        ("Cela couvre déjà beaucoup de familles. À qui sont destinés", "Cela couvre déjà beaucoup de familles, alors à qui sont destinés"),
        ("Le Biergerpakt compte donc ici aussi ! Et comment", "Le Biergerpakt compte donc ici aussi, et comment")],
 "de": [("Es gibt mehrere. Manche Menschen", "Es gibt mehrere: Manche Menschen"),
        ("Es gibt drei. Man muss", "Es gibt drei: Man muss"),
        ("Sorgen deswegen. Wie sieht er aus?", "Sorgen deswegen: Wie sieht er aus?"),
        ("Das Gesetz regelt also schon viel. Für Erwachsene", "Das Gesetz regelt also schon viel, und für Erwachsene"),
        ("Das klingt fair. Und was ist mit", "Das klingt fair, und was ist mit"),
        ("Das betrifft schon viele Familien. Für wen", "Das betrifft schon viele Familien, aber für wen"),
        ("Der Biergerpakt zählt also auch hier! Und wie", "Der Biergerpakt zählt also auch hier, und wie")],
 "lb": [("Et gëtt der e puer. Verschidde Leit", "Et gëtt der e puer: Verschidde Leit"),
        ("Et gëtt der dräi. Ee muss", "Et gëtt der dräi: Ee muss"),
        ("Suerge maachen. Wéi gesäit en aus?", "Suerge maachen: Wéi gesäit en aus?"),
        ("D'Gesetz mécht also schonn eng ganz Partie. Fir Erwuessener", "D'Gesetz mécht also schonn eng ganz Partie, a fir Erwuessener"),
        ("Dat kléngt fair. A wéi ass et", "Dat kléngt fair, a wéi ass et"),
        ("Dat betrëfft schonn eng ganz Rëtsch Famillen. Fir wien", "Dat betrëfft schonn eng ganz Rëtsch Famillen, mee fir wien"),
        ("De Biergerpakt zielt also och hei! A wéi", "De Biergerpakt zielt also och hei, a wéi")],
}
for lang, pairs in R.items():
    p = f"build/nationalite_src/{lang}.txt"; s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (lang, a); s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s); print(lang, len(pairs), "joins")
