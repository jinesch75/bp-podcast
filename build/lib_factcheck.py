"""Shared helper for fact-check scripts (Nov 2026).
apply(key, CHANGES, NOTES): CHANGES = {turn_index: {"en": text, "fr": text, "de": text, "lb": text}}
replaces the WHOLE text of that turn (speaker kept) in podcast_script_<key>[_lang].md; NOTES = {lang: sentence}
is appended once to the sources footer (marker "Fact-checked/Vérifié/Geprüft/Iwwerpréift 9 November").
Idempotent, turn counts unchanged. Run from the project root; pass --dry to preview."""
import re, sys
SFX = {"en": "", "fr": "_fr", "de": "_de", "lb": "_lb"}
TURN = re.compile(r"^(\*\*(?:ANNA|TOM)\s?:\*\*\s?)(.*)$", re.M)
def apply(key, CHANGES, NOTES, marker="9 November 2026|9 novembre 2026|9. November 2026|9. November 2026|den 9. November 2026"):
    write = "--dry" not in sys.argv
    for lang, sfx in SFX.items():
        p = f"podcast_script_{key}{sfx}.md"
        s = open(p, encoding="utf-8").read()
        ms = list(TURN.finditer(s)); n0 = len(ms); done = 0
        for idx in sorted(CHANGES, reverse=True):
            new = CHANGES[idx].get(lang)
            if new is None: continue
            m = ms[idx]
            if m.group(2) == new: continue
            s = s[:m.start(2)] + new + s[m.end(2):]; done += 1
        if lang in NOTES and NOTES[lang] not in s:
            e = [m for m in re.finditer(r"\*\s*$", s)][-1].start()
            s = s[:e].rstrip() + " " + NOTES[lang] + s[e:]; done += 1
        assert len(TURN.findall(s)) == n0
        print(p, "changes:", done, "turns:", n0)
        if write: open(p, "w", encoding="utf-8").write(s)
