"""Info-Seniors (Jacques, 13 Nov 2026): use the ministry's official name in line 21 (was "the Ministry of Family").
EN/FR/DE/LB, turn counts unchanged, idempotent. --dry to preview."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
R = {"": ("It's run by the State — by the Ministry of Family.",
          "It's run by the State — by the Ministry of Family Affairs, Solidarity, Living Together and Reception of Refugees."),
     "_fr": ("C'est géré par l'État — par le ministère de la Famille.",
             "C'est géré par l'État — par le Ministère de la Famille, des Solidarités, du Vivre ensemble et de l'Accueil."),
     "_de": ("Er wird vom Staat betrieben — vom Familienministerium.",
             "Er wird vom Staat betrieben — vom Ministerium für Familie, Solidarität, Zusammenleben und Unterbringung von Flüchtlingen."),
     "_lb": ("De Staat féiert et — d'Familljeministère.",
             "De Staat féiert et — de Ministère fir Famill, Solidaritéit, Zesummeliewen an Accueil vu Flüchtlingen.")}
for sfx, (old, new) in R.items():
    p = f"podcast_script_infosenior{sfx}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
    if new not in s:
        assert s.count(old) == 1, (p, old); s = s.replace(old, new)
    assert len(TURN.findall(s)) == n0; print(p, "ok")
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
