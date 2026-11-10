"""Remove spoken hesitations ("hmm...", "Mmm,", "..." pauses) from the MyGuichet scripts (EN/FR/DE/LB).
Jacques, 10 Nov 2026: these pauses sound awkward in the recorded voices. Idempotent; turn counts unchanged.
Run from the project root; --dry to preview."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
R = {
"en": [
("Right. So, Tom... let's start", "Right. So, Tom, let's start"),
("Okay, so... Guichet.lu is", "Okay. Guichet.lu is"),
("it's your... let's say, your single point", "it's your single point"),
("So it's like... an online counter?", "So it's like an online counter?"),
("Nice. And, hmm... what can I", "Nice. And what can I"),
("The main thing is... you can", "The main thing is: you can"),
("status of your requests... so you can see, okay, my file arrived", "status of your requests. You can see, for example: my file arrived"),
("And... one more thing... you can book", "And one more thing: you can book"),
("So I can... do procedures", "So I can do procedures"),
("Now... the big question.", "Now, the big question."),
("doesn't speak French yet... it really helps.", "doesn't speak French yet, it really helps."),
("Mmm, that's important.", "That's important."),
("Right, so... to register", "Right. To register"),
("many listeners will have... do I need", "many listeners will have: do I need"),
("The answer is... not necessarily.", "The answer is: not necessarily."),
("other European countries... an eIDAS", "other European countries, an eIDAS"),
("eIDAS... that's the European", "eIDAS, that's the European"),
("So... having a real account", "So having a real account"),
("once, and... that's it.", "once, and that's it."),
("Now... what kind of procedures", "Now, what kind of procedures"),
("Let's see... citizenship", "Let's see: citizenship"),
("family and education... taxation", "family and education. Taxation"),
("Work and pension... and even leisure", "Work and pension. And even leisure"),
("Take care... and see you", "Take care, and see you"),
],
"fr": [
("Alors, Tom... commençons", "Alors, Tom, commençons"),
("D'accord, alors... Guichet.lu est", "D'accord. Guichet.lu est"),
("c'est votre... disons, votre point de contact", "c'est votre point de contact"),
("c'est comme... un guichet", "c'est comme un guichet"),
("Super. Et, hmm... qu'est-ce que", "Super. Et qu'est-ce que"),
("c'est que... vous pouvez", "c'est que vous pouvez"),
("l'état de vos demandes... vous pouvez donc voir, d'accord, mon dossier est arrivé", "l'état de vos demandes. Vous voyez par exemple : mon dossier est arrivé"),
("Et... encore une chose... vous pouvez", "Et encore une chose : vous pouvez"),
("Donc je peux... faire", "Donc je peux faire"),
("Maintenant... la grande question.", "Maintenant, la grande question."),
("pas encore français... ça aide", "pas encore français, ça aide"),
("Mmm, c'est important.", "C'est important."),
("Alors... pour vous inscrire", "Alors, pour vous inscrire"),
("vont se poser... est-ce que", "vont se poser : est-ce que"),
("La réponse est... pas nécessairement.", "La réponse est : pas nécessairement."),
("pays européens... un identifiant", "pays européens, un identifiant"),
("eIDAS... c'est le système", "eIDAS, c'est le système"),
("Donc... avoir un vrai compte", "Donc avoir un vrai compte"),
("une fois, et... c'est tout.", "une fois, et c'est tout."),
("Maintenant... de quels types", "Maintenant, de quels types"),
("Voyons... la citoyenneté", "Voyons : la citoyenneté"),
("la famille et l'éducation... la fiscalité", "la famille et l'éducation. La fiscalité"),
("la pension... et même les loisirs", "la pension. Et même les loisirs"),
("Prenez soin de vous... et à la prochaine", "Prenez soin de vous, et à la prochaine"),
],
"de": [
("Also, Tom... fangen wir", "Also, Tom, fangen wir"),
("Okay, also... Guichet.lu ist", "Okay. Guichet.lu ist"),
("es ist Ihre... sagen wir, Ihre zentrale", "es ist Ihre zentrale"),
("ist es wie... ein Online-Schalter?", "ist es wie ein Online-Schalter?"),
("Schön. Und, hmm... was kann", "Schön. Und was kann"),
("Das Wichtigste ist... Sie können", "Das Wichtigste ist: Sie können"),
("verfolgen können... Sie können also sehen, okay, mein Dossier ist angekommen", "verfolgen können. Sie sehen zum Beispiel: Mein Dossier ist angekommen"),
("Und... noch eine Sache... Sie können", "Und noch eine Sache: Sie können"),
("Also ich kann... Verfahren", "Also ich kann Verfahren"),
("Nun... die große Frage.", "Nun, die große Frage."),
("Also für jemanden, der gerade angekommen ist und noch kein Französisch spricht... das hilft wirklich.", "Für jemanden, der gerade angekommen ist und noch kein Französisch spricht, ist das wirklich eine große Hilfe."),
("Mmm, das ist wichtig.", "Das ist wichtig."),
("Also... um sich", "Also, um sich"),
("haben werden... brauche ich", "haben werden: Brauche ich"),
("Die Antwort ist... nicht unbedingt.", "Die Antwort ist: nicht unbedingt."),
("europäischen Ländern... eine eIDAS", "europäischen Ländern, eine eIDAS"),
("eIDAS... das ist", "eIDAS, das ist"),
("Also... ein richtiges Konto zu haben, ist viel besser.", "Ein richtiges Konto zu haben, ist also viel besser."),
("einmal, und... das war's.", "einmal, und das war's."),
("Nun... über welche", "Nun, über welche"),
("Mal sehen... Staatsbürgerschaft", "Mal sehen: Staatsbürgerschaft"),
("Familie und Bildung... Steuern", "Familie und Bildung. Steuern"),
("Rente... und sogar Freizeit", "Rente. Und sogar Freizeit"),
("auf sich auf... und bis", "auf sich auf, und bis"),
],
"lb": [
("Also, Tom... loosse mer", "Also, Tom, loosse mer"),
("Okay, also... Guichet.lu ass", "Okay. Guichet.lu ass"),
("en ass Är... soe mer, Är eenzeg", "en ass Är eenzeg"),
("ass wéi... en Online-Guichet?", "ass wéi en Online-Guichet?"),
("Schéin. An, hmm... wat kann", "Schéin. A wat kann"),
("D'Haaptsaach ass... Dir kënnt", "D'Haaptsaach ass: Dir kënnt"),
("verfollege kënnt... sou datt Dir gesitt, okay, mäin Dossier", "verfollege kënnt. Dir gesitt zum Beispill: mäin Dossier"),
("An... nach eppes... Dir kënnt", "An nach eppes: Dir kënnt"),
("Also ech kann... Prozeduren", "Also ech kann Prozeduren"),
("Elo... déi grouss Fro.", "Elo, déi grouss Fro."),
("Franséisch schwätzt... et hëlleft wierklech.", "Franséisch schwätzt, ass dat wierklech eng grouss Hëllef."),
("Mmm, dat ass wichteg.", "Dat ass wichteg."),
("Also... fir Iech", "Also, fir Iech"),
("Nolauschterer hunn... brauch ech", "Nolauschterer hunn: brauch ech"),
("D'Äntwert ass... net onbedéngt.", "D'Äntwert ass: net onbedéngt."),
("europäesche Länner... en eIDAS", "europäesche Länner, en eIDAS"),
("eIDAS... dat ass", "eIDAS, dat ass"),
("Also... e richtege Kont ze hunn ass vill besser.", "E richtege Kont ze hunn ass also vill besser."),
("eemol, an... dat war et.", "eemol, an dat war et."),
("Elo... vu wéi enge", "Elo, vu wéi enge"),
("Loosse mer kucken... Citoyennetéit", "Loosse mer kucken: Citoyennetéit"),
("Educatioun... Steieren", "Educatioun. Steieren"),
("Pensioun... a souguer", "Pensioun. A souguer"),
("op Iech op... a bis", "op Iech op, a bis"),
],
}
SFX = {"en": "", "fr": "_fr", "de": "_de", "lb": "_lb"}
write = "--dry" not in sys.argv
for lang, pairs in R.items():
    p = f"podcast_script_myguichet{SFX[lang]}.md"
    s = open(p, encoding="utf-8").read(); n0 = len(TURN.findall(s)); done = 0
    for old, new in pairs:
        if new in s and old not in s: continue
        assert s.count(old) == 1, (lang, old, s.count(old))
        s = s.replace(old, new); done += 1
    body = s.split("*Sources")[0]
    left = re.findall(r".{0,30}(?:\.\.\.|…|\b[Hh]mm+\b|\bMmm\b).{0,20}", body)
    assert not left, (lang, left)
    assert len(TURN.findall(s)) == n0
    print(p, "changes:", done, "turns:", n0)
    if write: open(p, "w", encoding="utf-8").write(s)
