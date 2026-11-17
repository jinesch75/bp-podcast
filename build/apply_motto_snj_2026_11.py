"""SNJ EN (Jacques, 17 Nov 2026): the English voice can't say the Luxembourgish motto "Jonker staark maachen" ->
leave it out of the spoken lines and use only the English motto. Sources footer keeps the original motto.
EN only; idempotent; turn counts unchanged."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
p = "podcast_script_snj.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
R = [('The SNJ has a lovely motto in Luxembourgish... "Jonker staark maachen". It means "empowering youth".',
      'The SNJ has a lovely motto: "empowering youth".'),
     ('First... it is Luxembourg\'s National Youth Service, here to empower young people, with the motto "Jonker staark maachen".',
      'First, it is Luxembourg\'s National Youth Service, with the motto "empowering youth".')]
for old, new in R:
    if new in s: continue
    assert s.count(old) == 1, old; s = s.replace(old, new)
spoken = "\n".join(l for l in s.split("\n") if TURN.match(l))
assert "Jonker" not in spoken and len(TURN.findall(s)) == n0; print(p, "ok")
if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
