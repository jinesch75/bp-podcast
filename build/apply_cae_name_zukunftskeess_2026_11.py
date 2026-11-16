"""Zukunftskeess EN (Jacques, 16 Nov 2026): the English voices can't say "Zukunftskeess" well -> say it once by Anna
and once by Tom at the start, then call it "the CAE" (spoken C-A-E) everywhere else. Spoken lines only (sources
footer unchanged). EN only; FR/DE/LB unchanged. Idempotent; turn counts unchanged."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
p = "podcast_script_zukunftskeess.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
intro_old = "People also use the short name — C-A-E."
intro_new = "People also use the short name — the CAE. That's what we'll call it today."
if intro_new not in s:
    assert s.count(intro_old) == 1; s = s.replace(intro_old, intro_new)
keep = ("**ANNA:** It's called the Zukunftskeess.", "**TOM:** Zukunftskeess. That's a lovely name")
lines = s.split("\n"); n = 0
for k, ln in enumerate(lines):
    if not TURN.match(ln) or "Zukunftskeess" not in ln: continue
    if ln.startswith(keep[0]):   # Anna's introduction: keep only its first "Zukunftskeess"
        head, tail = ln.split("Zukunftskeess", 1); new = head + "Zukunftskeess" + tail.replace("Zukunftskeess", "CAE")
    elif ln.startswith(keep[1]):
        head, tail = ln.split("Zukunftskeess", 1); new = head + "Zukunftskeess" + tail.replace("Zukunftskeess", "CAE")
    else:
        new = ln.replace("Zukunftskeess", "CAE")
    if new != ln: lines[k] = new; n += 1
s = "\n".join(lines)
spoken = "\n".join(l for l in s.split("\n") if TURN.match(l))
assert spoken.count("Zukunftskeess") == 2, spoken.count("Zukunftskeess")
assert len(TURN.findall(s)) == n0; print(p, "lines changed:", n)
if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
