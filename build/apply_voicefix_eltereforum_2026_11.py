"""Eltereforum pitch pass (Jacques, 20 Nov 2026): very short lines that stayed low/creaky in every take are joined
to their neighbour or made into a full sentence. Meaning unchanged (script validated by the Eltereforum).
EN/FR/DE/LB, turn counts unchanged, idempotent."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
R = {"": [("Let's start there. What does it mean?", "Let's start there: what does it mean?"),
          ("and this is important. It's for everyone.", "and this is important: it's for everyone."),
          ("**TOM:** Exactly. A friendly first step.", "**TOM:** Exactly: it's a friendly first step.")],
     "_fr": [("Commençons par là. Qu'est-ce que ça veut dire ?", "Commençons par là : qu'est-ce que ça veut dire ?"),
             ("et c'est important. C'est pour tout le monde.", "et c'est important : c'est pour tout le monde."),
             ("**TOM :** Exactement. Un premier pas convivial.", "**TOM :** Exactement : c'est un premier pas convivial.")],
     "_de": [("Fangen wir dort an. Was bedeutet es?", "Fangen wir dort an: Was bedeutet es?"),
             ("und das ist wichtig. Es ist für alle.", "und das ist wichtig: Es ist für alle."),
             ("Die Schule. Teenager.", "Die Schule, und dann die Teenagerjahre."),
             ("**TOM:** Genau. Ein freundlicher erster Schritt.", "**TOM:** Genau: Es ist ein freundlicher erster Schritt.")],
     "_lb": [("Loosse mer do ufänken. Wat heescht et?", "Loosse mer do ufänken: wat heescht et?"),
             ("an dat ass wichteg. Et ass fir jiddereen.", "an dat ass wichteg: et ass fir jiddereen."),
             ("**TOM:** Genee. E frëndlechen éischte Schrëtt.", "**TOM:** Genee: et ass e frëndlechen éischte Schrëtt.")]}
for sfx, pairs in R.items():
    p = f"podcast_script_eltereforum{sfx}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
    for old, new in pairs:
        if new in s: continue
        assert s.count(old) == 1, (p, old); s = s.replace(old, new)
    assert len(TURN.findall(s)) == n0; print(p, "ok")
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
