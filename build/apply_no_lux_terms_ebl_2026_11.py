"""EBL (Jacques, 19 Nov 2026): Luxembourgish terms are badly pronounced by the voices -> avoided as much as possible in
EN/FR/DE spoken lines ("Ëmweltberodung Lëtzebuerg", the "Ëmwelt/Berodung" explanation, "Grénge Web",
"SuperDrecksKëscht"). The name EBL stays. LB script and sources footers unchanged. Idempotent; turn counts unchanged."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
R = {"": [('EBL stands for Ëmweltberodung Lëtzebuerg. In English, that means "Environmental Advice Luxembourg".',
           'EBL is short for a Luxembourgish name that means "Environmental Advice Luxembourg".'),
          ('"Ëmwelt" is the Luxembourgish word for environment, and "Berodung" means advice.',
           'So the name says exactly what it does: it gives advice on the environment.'),
          ("coordinated by the EBL together with the SuperDrecksKëscht.", "coordinated by the EBL together with the national waste-prevention programme."),
          ("a project for greener websites, called Grénge Web, and one", "a project for greener websites, and one"),
          ("That was our episode about the EBL, the Ëmweltberodung Lëtzebuerg.", "That was our episode about the EBL.")],
     "_fr": [("EBL veut dire Ëmweltberodung Lëtzebuerg. En français, cela signifie « Conseil en environnement Luxembourg ».",
              "EBL est l'abréviation d'un nom luxembourgeois qui signifie « Conseil en environnement Luxembourg »."),
             ("« Ëmwelt » est le mot luxembourgeois pour environnement, et « Berodung » veut dire conseil.",
              "Le nom dit donc exactement ce qu'elle fait : elle conseille sur l'environnement."),
             ("coordonné par l'EBL avec la SuperDrecksKëscht.", "coordonné par l'EBL avec le programme national de prévention des déchets."),
             ("des sites web plus verts, appelé Grénge Web, et un autre", "des sites web plus verts, et un autre"),
             ("C'était notre épisode sur l'EBL, l'Ëmweltberodung Lëtzebuerg.", "C'était notre épisode sur l'EBL.")],
     "_de": [("EBL steht für Ëmweltberodung Lëtzebuerg. Auf Deutsch heißt das „Umweltberatung Luxemburg\".",
              "EBL ist die Abkürzung eines luxemburgischen Namens, der „Umweltberatung Luxemburg\" bedeutet."),
             ("„Ëmwelt\" ist das luxemburgische Wort für Umwelt, und „Berodung\" bedeutet Beratung.",
              "Der Name sagt also genau, was sie tut: Sie berät zur Umwelt."),
             ("von der EBL zusammen mit der SuperDrecksKëscht koordiniert.", "von der EBL zusammen mit dem nationalen Programm zur Abfallvermeidung koordiniert."),
             ("grünere Webseiten, Grénge Web, und eines", "grünere Webseiten und eines"),
             ("Das war unsere Folge über die EBL, die Ëmweltberodung Lëtzebuerg.", "Das war unsere Folge über die EBL.")]}
for sfx, pairs in R.items():
    p = f"podcast_script_ebl{sfx}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
    for old, new in pairs:
        if new in s: continue
        assert s.count(old) == 1, (p, old); s = s.replace(old, new)
    spoken = "\n".join(l for l in s.split("\n") if TURN.match(l))
    left = re.findall(r"\b\w*[ëé]\w*\b", spoken)
    assert len(TURN.findall(s)) == n0; print(p, "ok; remaining words with ë/é:", sorted(set(left))[:15])
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
# Also (same day, by hand): "Ouni Pestiziden" -> "the campaign for gardens 'without pesticides'", "Gutt Geschier" -> "sharing
# tools" / "the tool library" in EN/FR/DE; the two website addresses (ounipestiziden.lu, guttgeschier.lu) are kept.
