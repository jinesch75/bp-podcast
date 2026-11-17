"""SNJ EN (Jacques, 17 Nov 2026): (also: Tom's "BEE SECURE promotes…" started with a glitch -> "Yes, BEE SECURE promotes…", done by hand) no "..." pauses (they sound awkward; e.g. a 1-second gap after "Fourth...").
Colon where a list or definition follows, otherwise comma (lowercase next word) or full stop. EN only; idempotent."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
p = "podcast_script_snj.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
COLON = ["its initials...", "experiencing languages...", "A life project...", "a fourth part..."]
out = []
for ln in s.split("\n"):
    if TURN.match(ln):
        for c in COLON:
            ln = ln.replace(c, c[:-3] + ":")
        ln = re.sub(r"\.\.\.\s+(?=[a-z])", ", ", ln)
        ln = re.sub(r"\.\.\.\s+(?=[A-Z])", ". ", ln)
        ln = ln.replace("...", ".")
    out.append(ln)
s = "\n".join(out)
assert "..." not in "\n".join(l for l in s.split("\n") if TURN.match(l)) and len(TURN.findall(s)) == n0
print(p, "ok")
if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
