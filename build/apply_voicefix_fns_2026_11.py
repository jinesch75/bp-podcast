"""FNS EN (Jacques, 17 Nov 2026): "Now" cut at the start of "Now — the FNS doesn't…" -> "Now, the FNS…" (take picked
with pick_word_take.py); French term "revenu pour personnes gravement handicapées" removed (English term only);
Anna's closing "…The National Solidarity Fund. fns.lu." — the lone "fns.lu." was cut off -> one sentence, "So..."
pause removed. Also (by hand): 4 very short questions by Anna made fuller (wrong pitch). EN only; idempotent."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
p = "podcast_script_fns.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
R = [("Now — the FNS doesn't do just one thing.", "Now, the FNS doesn't do just one thing."),
     ("It's the income for severely disabled persons — in French, the revenu pour personnes gravement handicapées.", "It's the income for severely disabled persons."),
     ("**ANNA:** So... if you, or someone you know, is struggling — remember the name. The National Solidarity Fund. fns.lu.",
      "**ANNA:** So, if you, or someone you know, is struggling, remember the name: the National Solidarity Fund, fns.lu.")]
for old, new in R:
    if new in s: continue
    assert s.count(old) == 1, old; s = s.replace(old, new)
assert len(TURN.findall(s)) == n0; print(p, "ok")
if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)

# FR/DE/LB (same day): same structure fixes — short questions made fuller, closing "… fns.lu." as one sentence.
X = {"_fr": [("Commençons simplement. Qu'est-ce que c'est ?", "Commençons simplement : qu'est-ce que c'est exactement ?"),
             ("Et est-ce que c'est seulement de l'argent ? Ou est-ce qu'il y a plus que ça ?", "Et est-ce que c'est seulement de l'argent, ou est-ce qu'il y a plus que ça ?"),
             ("**ANNA :** Et troisièmement ?", "**ANNA :** Et quelle est la troisième étape ?"),
             ("**ANNA :** Et le message du jour ?", "**ANNA :** Et quel est le message à retenir aujourd'hui ?"),
             ("Alors... si vous, ou quelqu'un que vous connaissez, êtes en difficulté — souvenez-vous du nom. Le Fonds national de solidarité. fns.lu.",
              "Alors, si vous, ou quelqu'un que vous connaissez, êtes en difficulté, souvenez-vous du nom : le Fonds national de solidarité, fns.lu.")],
     "_de": [("Fangen wir einfach an. Was ist das?", "Fangen wir einfach an: Was ist das genau?"),
             ("Und ist es nur Geld? Oder steckt mehr dahinter?", "Und ist es nur Geld, oder steckt mehr dahinter?"),
             ("**ANNA:** Und drittens?", "**ANNA:** Und was ist der dritte Schritt?"),
             ("**ANNA:** Und die Botschaft für heute?", "**ANNA:** Und was ist die wichtigste Botschaft für heute?"),
             ("Also... wenn Sie, oder jemand, den Sie kennen, in Schwierigkeiten ist — merken Sie sich den Namen. Der Nationale Solidaritätsfonds. fns.lu.",
              "Also, wenn Sie, oder jemand, den Sie kennen, in Schwierigkeiten ist, merken Sie sich den Namen: der Nationale Solidaritätsfonds, fns.lu.")],
     "_lb": [("Loosse mer einfach ufänken. Wat ass dat?", "Loosse mer einfach ufänken: wat ass dat genau?"),
             ("An ass et just Geld? Oder steet", "An ass et just Geld, oder steet"),
             ("**ANNA:** A fir d'drëtt?", "**ANNA:** A wat ass den drëtte Schrëtt?"),
             ("**ANNA:** An d'Botschaft fir haut?", "**ANNA:** A wat ass déi wichtegst Botschaft fir haut?"),
             ("Also... wann Dir, oder een, deen Dir kennt, Schwieregkeeten huet — denkt un den Numm. Den Nationale Solidaritéitsfong. fns.lu.",
              "Also, wann Dir, oder een, deen Dir kennt, Schwieregkeeten huet, denkt un den Numm: den Nationale Solidaritéitsfong, fns.lu.")]}
for sfx, pairs in X.items():
    p = f"podcast_script_fns{sfx}.md"; s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s))
    for old, new in pairs:
        if new in s: continue
        assert s.count(old) == 1, (p, old); s = s.replace(old, new)
    assert len(TURN.findall(s)) == n0; print(p, "ok")
    if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(s)
