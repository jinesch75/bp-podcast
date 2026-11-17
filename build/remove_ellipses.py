#!/usr/bin/env python3
"""Remove "..." pauses from an episode's spoken lines (Jacques: they sound awkward with the ElevenLabs voices).
python3 build/remove_ellipses.py <key> [en,fr,de,lb] [--dry]
"x... y" -> "x, y" (lowercase next word), "x... Y" -> "x. Y"; a leading/trailing "..." is dropped.
Turn counts unchanged; idempotent. Prints every change for review."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
key = sys.argv[1]; langs = (sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "en,fr,de,lb").split(",")
SFX = {"en": "", "fr": "_fr", "de": "_de", "lb": "_lb"}
for lang in langs:
    p = f"podcast_script_{key}{SFX[lang]}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s)); out = []; n = 0
    for ln in s.split("\n"):
        if TURN.match(ln) and "..." in ln:
            new = re.sub(r"(\*\*\s?)\.\.\.\s*", r"\1", ln)                       # "**ANNA:** ...text"
            new = re.sub(r"\s*\.\.\.\s+(?=[a-zà-ÿäöüß«„\"'])", ", ", new)
            new = re.sub(r"\s*\.\.\.\s+(?=\S)", ". ", new)
            new = re.sub(r"\s*\.\.\.(?=\s*$)", ".", new)
            new = re.sub(r"\.\.\.", ".", new)
            new = re.sub(r",\s*([?!.])", r"\1", new)
            if new != ln:
                n += 1
                for a, b in zip(re.findall(r".{0,18}\.\.\..{0,14}", ln), [None] * 99): print(f"  {lang}: …{a}…")
            ln = new
        out.append(ln)
    s = "\n".join(out); assert len(TURN.findall(s)) == n0
    assert "..." not in "\n".join(l for l in s.split("\n") if TURN.match(l))
    print(p, "lines changed:", n)
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
