"""European funds (Jacques, 19 Nov 2026): "integration" -> "living together" (the official fund name "Asylum, Migration
and Integration Fund" is kept); FEDER amount removed (no amounts for the other funds either; avoids stale figures).
EN/FR/DE/LB, idempotent; turn counts unchanged."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
R = {"": [("That one supports welcoming and integrating people who come to Luxembourg, including those seeking asylum.",
           "That one supports welcoming people who come to Luxembourg, including those seeking asylum, and living together."),
          ("people and jobs, and integration.", "people and jobs, and living together."),
          ("For Luxembourg, in the current period from 2021 to 2027, this fund is around twenty-one million euros.", "For Luxembourg, the current period runs from 2021 to 2027.")],
     "_fr": [("Celui-là soutient l'accueil et l'intégration des personnes qui viennent au Luxembourg, y compris celles qui demandent l'asile.",
              "Celui-là soutient l'accueil des personnes qui viennent au Luxembourg, y compris celles qui demandent l'asile, et le vivre-ensemble."),
             ("les personnes et les emplois, et l'intégration.", "les personnes et les emplois, et le vivre-ensemble."),
             ("Pour le Luxembourg, dans la période actuelle de 2021 à 2027, ce fonds représente environ vingt et un millions d'euros.", "Pour le Luxembourg, la période actuelle va de 2021 à 2027.")],
     "_de": [("Dieser unterstützt die Aufnahme und Integration von Menschen, die nach Luxemburg kommen, einschließlich derjenigen, die Asyl suchen.",
              "Dieser unterstützt die Aufnahme von Menschen, die nach Luxemburg kommen, einschließlich derjenigen, die Asyl suchen, und das Zusammenleben."),
             ("die Menschen und Arbeitsplätze, und die Integration.", "die Menschen und Arbeitsplätze, und das Zusammenleben."),
             ("Für Luxemburg beläuft sich dieser Fonds im aktuellen Zeitraum von 2021 bis 2027 auf etwa einundzwanzig Millionen Euro.", "Für Luxemburg läuft der aktuelle Zeitraum von 2021 bis 2027.")],
     "_lb": [("Deen do ënnerstëtzt d'Opname an d'Integratioun vu Leit, déi op Lëtzebuerg kommen, dorënner déi, déi Asyl sichen.",
              "Deen do ënnerstëtzt d'Opname vu Leit, déi op Lëtzebuerg kommen, dorënner déi, déi Asyl sichen, an d'Zesummeliewen."),
             ("d'Leit an d'Aarbechtsplazen, an d'Integratioun.", "d'Leit an d'Aarbechtsplazen, an d'Zesummeliewen."),
             ("Fir Lëtzebuerg beleeft sech dëse Fong an der aktueller Period vu 2021 bis 2027 op ongeféier eenanzwanzeg Milliounen Euro.", "Fir Lëtzebuerg leeft déi aktuell Period vu 2021 bis 2027.")]}
for sfx, pairs in R.items():
    p = f"podcast_script_fondseuropeens{sfx}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
    for old, new in pairs:
        if new in s: continue
        assert s.count(old) == 1, (p, old); s = s.replace(old, new)
    spoken = "\n".join(l for l in s.split("\n") if TURN.match(l))
    print(p, "ok; integration words left:", re.findall(r"(?i)\w*integ?rat\w*", spoken), "| million left:", bool(re.search(r"(?i)million|milliou", spoken)))
    assert len(TURN.findall(s)) == n0
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
