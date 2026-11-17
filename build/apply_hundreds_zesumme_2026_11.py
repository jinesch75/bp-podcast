"""Zesumme Vereinfachen (Jacques, 17 Nov 2026): "millions of procedures" is exaggerated -> "hundreds". EN/FR/DE/LB, idempotent."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
R = {"": ("a tool that millions of procedures pass through.", "a tool that hundreds of procedures pass through."),
     "_fr": ("par lequel passent des millions de démarches.", "par lequel passent des centaines de démarches."),
     "_de": ("durch das Millionen von Verfahren laufen.", "durch das Hunderte von Verfahren laufen."),
     "_lb": ("duerch deen Millioune Prozeduren goen.", "duerch deen Honnerte Prozeduren goen.")}
for sfx, (old, new) in R.items():
    p = f"podcast_script_zesumme{sfx}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
    if new not in s:
        assert s.count(old) == 1, (p, old); s = s.replace(old, new)
    assert len(TURN.findall(s)) == n0; print(p, "ok")
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
