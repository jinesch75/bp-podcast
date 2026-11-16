"""Zukunftskeess (Jacques, 16 Nov 2026): Tom's "Anna, tell us its name." swallowed the name "Anna" (first word of
the turn) -> name moved to the end. EN only. Idempotent; turn counts unchanged."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
p = "podcast_script_zukunftskeess.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
old, new = "Anna, tell us its name.", "Tell us its name, Anna."
if new not in s:
    assert s.count(old) == 1; s = s.replace(old, new)
assert len(TURN.findall(s)) == n0; print(p, "ok")
if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
