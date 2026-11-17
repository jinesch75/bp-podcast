"""Zesumme Vereinfachen (Jacques, 17 Nov 2026):
1. Anna's "I love that. Together." — the lone "Together." was recorded on its own and sounded disconnected -> one
   sentence (EN/FR/DE/LB).
2. EN: the name is hard for the English voices -> said once (Tom's introduction), then "this project" / "the
   platform". "Second..." pause removed in that line. Idempotent; turn counts unchanged."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
R = {"": [('I love that. Together.', 'I love that idea — doing it together.'),
          ('So Anna, what exactly is Zesumme Vereinfachen?', 'So Anna, what exactly is this project?'),
          ('Second... visit the Zesumme Vereinfachen platform and share', 'Second, visit the platform and share'),
          ('What should people remember about Zesumme Vereinfachen?', 'What should people remember about the platform?'),
          ('That was our episode about Zesumme Vereinfachen.', 'That was our episode about this platform for simpler public services.')],
     "_fr": [("J'adore ça. Ensemble.", "J'adore cette idée — le faire ensemble.")],
     "_de": [("Das gefällt mir sehr. Gemeinsam.", "Die Idee gefällt mir sehr — es gemeinsam zu machen.")],
     "_lb": [("Dat gefält mer immens. Zesummen.", "D'Iddi gefält mer immens — et zesummen ze maachen.")]}
for sfx, pairs in R.items():
    p = f"podcast_script_zesumme{sfx}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
    for old, new in pairs:
        if new in s: continue
        assert s.count(old) == 1, (p, old); s = s.replace(old, new)
    assert len(TURN.findall(s)) == n0
    if sfx == "": assert "\n".join(l for l in s.split("\n") if TURN.match(l)).count("Zesumme Vereinfachen") == 1
    print(p, "ok")
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
