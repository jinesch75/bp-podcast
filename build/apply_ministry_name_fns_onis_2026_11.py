"""FNS + ONIS (13 Nov 2026): the ministry's official name instead of "the Ministry of Family" (Jacques's standing rule).
EN/FR/DE/LB, turn counts unchanged, idempotent. --dry to preview."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
EN = "Ministry of Family Affairs, Solidarity, Living Together and Reception of Refugees"
FR = "Ministère de la Famille, des Solidarités, du Vivre ensemble et de l'Accueil"
DE = "Ministerium für Familie, Solidarität, Zusammenleben und Unterbringung von Flüchtlingen"
LB = "Ministère fir Famill, Solidaritéit, Zesummeliewen an Accueil vu Flüchtlingen"
R = {"fns": {"": ("It's run under the Ministry of Family.", f"It's run under the {EN}."),
             "_fr": ("Il dépend du ministère de la Famille.", f"Il dépend du {FR}."),
             "_de": ("Er gehört zum Familienministerium.", f"Er gehört zum {DE}."),
             "_lb": ("En ass ënner dem Familljeministère.", f"En ass ënner dem {LB}.")},
     "onis": {"": ("under the Ministry of Family.", f"under the {EN}."),
              "_fr": ("qui relève du ministère de la Famille.", f"qui relève du {FR}."),
              "_de": ("unter dem Familienministerium.", f"unter dem {DE}."),
              "_lb": ("ënnert dem Familljeministère.", f"ënnert dem {LB}.")}}
for key, d in R.items():
    for sfx, (old, new) in d.items():
        p = f"podcast_script_{key}{sfx}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
        if new not in s:
            assert s.count(old) == 1, (p, old, s.count(old)); s = s.replace(old, new)
        assert len(TURN.findall(s)) == n0; print(p, "ok")
        if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
