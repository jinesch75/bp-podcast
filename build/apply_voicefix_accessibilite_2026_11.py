"""Accessibility (Jacques, 13 Nov 2026): Anna's very short "And the message for today?" sounded wrong -> a fuller
question gives the voice context; "So..." pause in her next line removed (no hesitations). EN/FR/DE/LB, idempotent."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
R = {"": [("**ANNA:** And the message for today?", "**ANNA:** And what's the one message to remember from today?"),
          ("**ANNA:** So... whether you're", "**ANNA:** So, whether you're")],
     "_fr": [("**ANNA :** Et le message d'aujourd'hui ?", "**ANNA :** Et quel est le message à retenir aujourd'hui ?"),
             ("**ANNA :** Alors... que vous soyez", "**ANNA :** Alors, que vous soyez")],
     "_de": [("**ANNA:** Und die Botschaft für heute?", "**ANNA:** Und was ist die wichtigste Botschaft für heute?"),
             ("**ANNA:** Also... ob Sie", "**ANNA:** Also, ob Sie")],
     "_lb": [("**ANNA:** An d'Message fir haut?", "**ANNA:** A wat ass de wichtegste Message fir haut?"),
             ("**ANNA:** Also... egal ob", "**ANNA:** Also, egal ob")]}
for sfx, pairs in R.items():
    p = f"podcast_script_accessibilite{sfx}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
    for old, new in pairs:
        if new in s: continue
        assert s.count(old) == 1, (p, old); s = s.replace(old, new)
    assert len(TURN.findall(s)) == n0; print(p, "ok")
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
