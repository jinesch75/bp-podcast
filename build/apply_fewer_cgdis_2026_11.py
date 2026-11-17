"""CGDIS (Jacques, 17 Nov 2026): "C-G-D-I-S" is cumbersome to hear -> said only in the introduction (line 15), the
explanation of the name (line 21) and the summary (line 79); elsewhere "the rescue corps" / "it" / "they"
(FR "le corps de secours", DE "das Rettungskorps", LB "de Rettungsdéngscht"). EN/FR/DE/LB, idempotent."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
KEEP = {15, 21, 79}
SPECIAL = {
 "": [("So Anna, what exactly is the CGDIS?", "So Anna, what exactly is this organisation?"),
      ("The CGDIS has professional firefighters", "It has professional firefighters"),
      ("The CGDIS also gives fire-prevention advice", "They also give fire-prevention advice"),
      ("because the CGDIS does more", "because the firefighters do more"),
      ("becoming a volunteer with the CGDIS.", "becoming a volunteer firefighter."),
      ("our episode about the CGDIS and the emergency number 112.", "our episode about Luxembourg's fire and rescue corps and the emergency number 112.")],
 "_fr": [("qu'est-ce que le CGDIS exactement ?", "qu'est-ce que cette organisation exactement ?"),
         ("Le CGDIS compte des pompiers professionnels", "Il compte des pompiers professionnels"),
         ("pensez à devenir bénévole au CGDIS.", "pensez à devenir pompier volontaire."),
         ("notre épisode sur le CGDIS et le numéro d'urgence 112.", "notre épisode sur le corps grand-ducal d'incendie et de secours et le numéro d'urgence 112.")],
 "_de": [("was genau ist das CGDIS?", "was genau ist diese Organisation?"),
         ("Das CGDIS hat Berufsfeuerwehrleute", "Es hat Berufsfeuerwehrleute"),
         ("unsere Folge über das CGDIS und die Notrufnummer 112.", "unsere Folge über das großherzogliche Feuerwehr- und Rettungskorps und die Notrufnummer 112.")],
 "_lb": [("wat ass de CGDIS genau?", "wat ass dës Organisatioun genau?"),
         ("De CGDIS huet beruffleg Pompjeeën", "Hien huet beruffleg Pompjeeën")]}
GENERIC = {"": [("the CGDIS", "the rescue corps"), ("The CGDIS", "The rescue corps")],
           "_fr": [("le CGDIS", "le corps de secours"), ("Le CGDIS", "Le corps de secours"), ("au CGDIS", "au corps de secours")],
           "_de": [("das CGDIS", "das Rettungskorps"), ("Das CGDIS", "Das Rettungskorps"), ("dem CGDIS", "dem Rettungskorps"), ("beim CGDIS", "beim Rettungskorps")],
           "_lb": [("de CGDIS", "de Rettungsdéngscht"), ("De CGDIS", "De Rettungsdéngscht"), ("dem CGDIS", "dem Rettungsdéngscht"), ("beim CGDIS", "beim Rettungsdéngscht")]}
for sfx in ("", "_fr", "_de", "_lb"):
    p = f"podcast_script_cgdis{sfx}.md"; lines = open(p, encoding="utf-8").read().split("\n"); n0 = sum(1 for l in lines if TURN.match(l))
    for k, ln in enumerate(lines):
        if not TURN.match(ln) or (k + 1) in KEEP or "CGDIS" not in ln: continue
        for a, b in SPECIAL[sfx] + GENERIC[sfx]: ln = ln.replace(a, b)
        lines[k] = ln
    s = "\n".join(lines); left = [k + 1 for k, l in enumerate(lines) if TURN.match(l) and "CGDIS" in l]
    assert sum(1 for l in lines if TURN.match(l)) == n0 and set(left) <= KEEP, (p, left)
    print(p, "CGDIS left in lines", left, "count", sum(l.count("CGDIS") for l in lines if TURN.match(l)))
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
