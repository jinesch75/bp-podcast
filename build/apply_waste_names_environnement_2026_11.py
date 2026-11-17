"""Environment portal EN (Jacques, 17 Nov 2026): Luxembourgish names "Null Offall Lëtzebuerg" and "Mäin Offall"
left out of the spoken English lines (sources footer keeps them). EN only; idempotent; turn counts unchanged."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
p = "podcast_script_environnement.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
R = [('and the country\'s zero-waste strategy, "Null Offall Lëtzebuerg".', "and the country's zero-waste strategy."),
     ("There's even an app, Mäin Offall, to help you know what goes in which bin.", "There's even an app to help you know what goes in which bin.")]
for old, new in R:
    if new in s: continue
    assert s.count(old) == 1, old; s = s.replace(old, new)
assert "Offall" not in "\n".join(l for l in s.split("\n") if TURN.match(l)) and len(TURN.findall(s)) == n0
print(p, "ok")
if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
