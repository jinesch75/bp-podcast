"""Maison de l'orientation (Jacques, 12 Nov 2026): two very short questions by Anna sounded bad
("And the fourth?" too loud, "And how to start?" squeaky). Slightly longer wording gives the voice
enough context for a natural tone. EN/FR/DE/LB, turn counts unchanged, idempotent. --dry to preview."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
R = {"": [("**ANNA:** And the fourth?", "**ANNA:** And what's the fourth theme?"),
          ("**ANNA:** And how to start?", "**ANNA:** And what's the best way to get started?")],
     "_fr": [("**ANNA :** Et le quatrième ?", "**ANNA :** Et quel est le quatrième thème ?"),
             ("**ANNA :** Et comment commencer ?", "**ANNA :** Et concrètement, comment est-ce qu'on commence ?")],
     "_de": [("**ANNA:** Und das vierte?", "**ANNA:** Und was ist das vierte Thema?"),
             ("**ANNA:** Und wie fängt man an?", "**ANNA:** Und wie fängt man am besten an?")],
     "_lb": [("**ANNA:** An dat véiert?", "**ANNA:** A wat ass dat véiert Thema?"),
             ("**ANNA:** A wéi ufänken?", "**ANNA:** A wéi fänkt een am beschten un?")]}
for sfx, pairs in R.items():
    p = f"podcast_script_maison_orientation{sfx}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s)); d = 0
    for old, new in pairs:
        if new in s: continue
        assert s.count(old) == 1, (p, old); s = s.replace(old, new); d += 1
    assert len(TURN.findall(s)) == n0; print(p, "changes:", d)
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
