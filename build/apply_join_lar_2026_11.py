#!/usr/bin/env python3
"""LAR ep (2026-11-26): short lines that stayed off in every take are joined to the next sentence,
in all four languages (CLAUDE.md rule 5). Runs once; then python3 build/make_scripts_lar.py."""
R = {
 "en": [("It is something different. LAR describes", "It is something different: LAR describes"),
        ("No, it does not. LAR is part", "No, it does not: LAR is part"),
        ("No, not always. Depending", "No, not always: depending"),
        ("That is good to know. Let's move to the second big activity: bringing people home from abroad.", "That is good to know, and it brings us to the second big activity, bringing people home from abroad."),
        ("during a business trip. What can LAR do then?", "during a business trip: what can LAR do then?"),
        ("Then let's go through them together. Which ones", "Then let's go through them together: which ones"),
        ("Let's start with the helicopters. When there is", "Let's start with the helicopters: when there is"),
        ("What counts is your main residence. You can join", "What counts is your main residence: you can join")],
 "fr": [("C'est quelque chose de différent. La LAR se présente", "C'est quelque chose de différent : la LAR se présente"),
        ("Non, pas du tout. La LAR fait partie", "Non, pas du tout : la LAR fait partie"),
        ("Non, pas toujours. Selon le patient", "Non, pas toujours : selon le patient"),
        ("C'est bon à savoir. Passons à la deuxième grande activité : ramener les gens de l'étranger.", "C'est bon à savoir, et cela nous amène à la deuxième grande activité, ramener les gens de l'étranger."),
        ("voyage d'affaires. Que peut faire la LAR dans ce cas ?", "voyage d'affaires : que peut faire la LAR dans ce cas ?"),
        ("Alors, parcourons-les ensemble. Quelles sont", "Alors, parcourons-les ensemble : quelles sont"),
        ("Commençons par les hélicoptères. Quand il y a", "Commençons par les hélicoptères : quand il y a"),
        ("c'est votre résidence principale. Vous pouvez", "c'est votre résidence principale : vous pouvez")],
 "de": [("Sie ist etwas anderes. Die LAR beschreibt", "Sie ist etwas anderes: Die LAR beschreibt"),
        ("Nein, ganz und gar nicht. Die LAR ist Teil", "Nein, ganz und gar nicht: Die LAR ist Teil"),
        ("Nein, nicht immer. Je nach Patient", "Nein, nicht immer: Je nach Patient"),
        ("Das ist gut zu wissen. Kommen wir zur zweiten großen Aufgabe: Menschen aus dem Ausland nach Hause bringen.", "Das ist gut zu wissen, und damit kommen wir zur zweiten großen Aufgabe, Menschen aus dem Ausland nach Hause zu bringen."),
        ("schwer verletzt. Was kann die LAR dann tun?", "schwer verletzt: Was kann die LAR dann tun?"),
        ("Dann gehen wir sie gemeinsam durch. Welche sind", "Dann gehen wir sie gemeinsam durch: Welche sind"),
        ("Fangen wir mit den Hubschraubern an. Wenn es", "Fangen wir mit den Hubschraubern an: Wenn es"),
        ("Entscheidend ist Ihr Hauptwohnsitz. Sie können", "Entscheidend ist Ihr Hauptwohnsitz: Sie können")],
 "lb": [("Si ass eppes anescht. D'LAR beschreift", "Si ass eppes anescht: D'LAR beschreift"),
        ("Nee, guer net. D'LAR ass Deel", "Nee, guer net: D'LAR ass Deel"),
        ("Nee, net ëmmer. Jee no Patient", "Nee, net ëmmer: Jee no Patient"),
        ("Dat ass gutt ze wëssen. Komme mir zur zweeter grousser Aufgab: Leit aus dem Ausland heembréngen.", "Dat ass gutt ze wëssen, an domat komme mir zur zweeter grousser Aufgab, Leit aus dem Ausland heemzebréngen."),
        ("schwéier blesséiert. Wat kann d'LAR dann maachen?", "schwéier blesséiert: Wat kann d'LAR dann maachen?"),
        ("Da gi mir se zesummen duerch. Wéi eng", "Da gi mir se zesummen duerch: Wéi eng"),
        ("Fänke mir mat den Helikopteren un. Wann et", "Fänke mir mat den Helikopteren un: Wann et"),
        ("Wat zielt, ass Ären Haaptwunnsëtz. Dir kënnt", "Wat zielt, ass Ären Haaptwunnsëtz: Dir kënnt")],
}
for lang, pairs in R.items():
    p = f"build/lar_src/{lang}.txt"; s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (lang, a)
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s); print(lang, len(pairs), "joined")
