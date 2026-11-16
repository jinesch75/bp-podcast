"""Greater Region (Jacques, 16 Nov 2026): EN "In German, ..." came out with a French accent (it follows the French
name) -> fuller English lead-in; Tom's very short "And where is it?" had the wrong pitch -> fuller question
(DE/LB too; FR already full). J.F. Kennedy split: fixed in tts_elevenlabs.split_sentences. Idempotent."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
R = {"": [("In German, the Haus der Großregion.", "And in German, it's the Haus der Großregion."),
          ("**TOM:** And where is it?", "**TOM:** And where can you find it?")],
     "_de": [("**TOM:** Und wo ist es?", "**TOM:** Und wo findet man es?")],
     "_lb": [("**TOM:** A wou ass et?", "**TOM:** A wou fënnt een et?")]}
for sfx, pairs in R.items():
    p = f"podcast_script_granderegion{sfx}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
    for old, new in pairs:
        if new in s: continue
        assert s.count(old) == 1, (p, old); s = s.replace(old, new)
    assert len(TURN.findall(s)) == n0; print(p, "ok")
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
