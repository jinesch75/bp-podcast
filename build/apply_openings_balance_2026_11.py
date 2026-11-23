#!/usr/bin/env python3
"""23 Nov 2026 (Jacques): openings must differ from episode to episode (no more "I have a question to start with"),
and both hosts must explain (no episode where one only asks and the other only explains).
No explicit hand-over lines ("this time I explain, you ask"): a section simply starts with the other host explaining.
- cet: new opening; roles now alternate by section (Anna: basics, forms of discrimination, courts, website;
  Tom: grounds + fields, what the CET does, how to contact it). 97 -> 91 turns. EN only: the website is said by Tom
  BEFORE the French name (Anna's "cet dot l-u" took a French accent after "Centre pour l'égalité de traitement").
- ombudsman: new opening; the hand-over line is gone and the roles are mixed inside both parts (Tom: first step with the
  administration, second mission; Anna: who can contact the OKaJu). 103 -> 97 turns. EN only: the Luxembourgish name
  "Ombudsman fir Kanner a Jugendlecher" is no longer spoken (English meaning given straight away).
EN/FR/DE/LB. Idempotent (skips a file that no longer has the old opening). Run from the project root; --dry to preview."""
import re, sys
SFX = {"en": "", "fr": "_fr", "de": "_de", "lb": "_lb"}
TURN = re.compile(r"^\*\*(ANNA|TOM)(\s?):\*\*\s?(.*)$", re.M)
OLD = {"en": "I have a question to start with", "fr": "J'ai une question pour commencer", "de": "Ich habe eine Frage zum Anfang", "lb": "Ech hunn eng Fro fir unzefänken"}

CET_OPEN_T = {"en": "Today, we begin with a principle that sounds very simple: every person has the right to be treated equally.",
 "fr": "Aujourd'hui, nous partons d'un principe qui paraît très simple : chaque personne a le droit d'être traitée de la même manière.",
 "de": "Heute beginnen wir mit einem Grundsatz, der ganz einfach klingt: Jeder Mensch hat das Recht, gleich behandelt zu werden.",
 "lb": "Haut fänke mer mat engem Grondsaz un, dee ganz einfach kléngt: All Mënsch huet d'Recht, gläich behandelt ze ginn."}
CET_OPEN_A = {"en": "In daily life, it is not always that simple. And when people are treated unfairly, they often don't know if the law is on their side, or who they could ask.",
 "fr": "Dans la vie de tous les jours, ce n'est pas toujours aussi simple. Et quand on est traité de façon injuste, on ne sait souvent pas si la loi est de notre côté, ni à qui poser la question.",
 "de": "Im Alltag ist das nicht immer so einfach. Und wer ungerecht behandelt wird, weiß oft nicht, ob das Gesetz auf seiner Seite ist, oder wen man fragen könnte.",
 "lb": "Am Alldag ass dat net ëmmer esou einfach. A wien ongerecht behandelt gëtt, weess dacks net, ob d'Gesetz op senger Säit ass, oder wie ee kéint froen."}
CET_5 = {"en": "That is exactly why we are talking today about the CET, the Centre for Equal Treatment. Its website is cet dot l-u."}
CET_6 = {"en": "The three letters CET come from its French name: Centre pour l'égalité de traitement."}
F3T = {"en": "Let's come to the practical side. For people who feel that they are victims of discrimination, the CET has an advice and guidance service.",
 "fr": "Passons au côté pratique. Pour les personnes qui s'estiment victimes d'une discrimination, le CET a un service de conseil et d'orientation.",
 "de": "Kommen wir zur praktischen Seite. Für Menschen, die sich diskriminiert fühlen, hat das CET einen Beratungs- und Orientierungsdienst.",
 "lb": "Komme mer zur praktescher Säit. Fir Leit, déi sech diskriminéiert fillen, huet de CET e Berodungs- an Orientéierungsservice."}
P4 = {"en": "There is also something that the CET does not do.", "fr": "Il y a aussi quelque chose que le CET ne fait pas.",
      "de": "Es gibt auch etwas, das das CET nicht tut.", "lb": "Et gëtt och eppes, wat de CET net mécht."}
P5 = {"en": "Now imagine that you want to contact the CET.", "fr": "Imaginons maintenant que vous vouliez contacter le CET.",
      "de": "Stellen wir uns jetzt vor, Sie möchten das CET kontaktieren.", "lb": "Stelle mer eis elo vir, Dir wéilt de CET kontaktéieren."}
P6 = {"en": "Let's look at the website a little more.", "fr": "Regardons le site d'un peu plus près.",
      "de": "Schauen wir uns die Website noch etwas genauer an.", "lb": "Kucke mer eis de Site nach e bësse méi genee un."}

OMB_T = {"en": "Imagine that a letter from an administration arrives at your home. You read it twice, and you are sure that the decision cannot be right.",
 "fr": "Imaginez qu'une lettre d'une administration arrive chez vous. Vous la lisez deux fois, et vous vous dites que la décision ne peut pas être juste.",
 "de": "Stellen Sie sich vor, ein Brief von einer Verwaltung kommt bei Ihnen zu Hause an. Sie lesen ihn zweimal, und Sie sind sicher, dass die Entscheidung nicht richtig sein kann.",
 "lb": "Stellt Iech vir, e Bréif vun enger Verwaltung kënnt bei Iech doheem un. Dir liest en zweemol, an Dir sidd sécher, datt d'Decisioun net richteg ka sinn."}
OMB_A = {"en": "Many people know that feeling. And the hardest part is often that you do not know who could help you.",
 "fr": "Beaucoup de gens connaissent ce sentiment. Et le plus difficile, c'est souvent de ne pas savoir qui peut vous aider.",
 "de": "Dieses Gefühl kennen viele Menschen. Und das Schwierigste ist oft, dass man nicht weiß, wer einem helfen kann.",
 "lb": "Dëst Gefill kenne vill Leit. An dat Schwéierst ass dacks, datt een net weess, wien engem hëllefe kann."}

M29 = {"en": "Before you write to the Ombudsman, there is one step that people often forget.", "fr": "Avant d'écrire à l'Ombudsman, il y a une étape que l'on oublie souvent.",
       "de": "Bevor Sie dem Ombudsman schreiben, gibt es einen Schritt, den viele vergessen.", "lb": "Ier Dir dem Ombudsman schreift, gëtt et e Schrëtt, dee vill Leit vergiessen."}
M35 = {"en": "You then send your complaint to the Ombudsman by email or by post, with a copy of what you wrote to the administration.",
       "fr": "Vous envoyez alors votre réclamation à l'Ombudsman par e-mail ou par courrier, avec une copie de ce que vous avez écrit à l'administration.",
       "de": "Sie schicken Ihre Beschwerde dann per E-Mail oder per Post an den Ombudsman, mit einer Kopie von dem, was Sie der Verwaltung geschrieben haben.",
       "lb": "Dir schéckt Är Reklamatioun dann per E-Mail oder per Post un den Ombudsman, mat enger Kopie vun deem, wat Dir der Verwaltung geschriwwen hutt."}
M55 = {"en": "Now let's turn to the second institution, the OKaJu. What does this name mean?", "fr": "Passons maintenant à la deuxième institution, l'OKaJu. Que veut dire ce nom ?",
       "de": "Kommen wir jetzt zur zweiten Institution, dem OKaJu. Was bedeutet dieser Name?", "lb": "Komme mir elo bei déi zweet Institutioun, den OKaJu. Wat bedeit dësen Numm?"}
O57 = {"en": "It is short for a Luxembourgish name. In English, it means the Ombudsman for children and young people."}
M66 = {"en": "The OKaJu is there, first of all, for every child and every young person under eighteen.", "fr": "L'OKaJu est là, tout d'abord, pour chaque enfant et chaque jeune de moins de dix-huit ans.",
       "de": "Das OKaJu ist zuerst einmal für jedes Kind und jeden Jugendlichen unter achtzehn Jahren da.", "lb": "Den OKaJu ass als éischt fir all Kand an all Jugendlechen ënner uechtzéng Joer do."}
M76 = {"en": "To reach the OKaJu, you can call, write an email, or fill in the contact form on the website.",
       "fr": "Pour joindre l'OKaJu, vous pouvez appeler, écrire un e-mail, ou remplir le formulaire de contact sur le site.",
       "de": "Um das OKaJu zu erreichen, können Sie anrufen, eine E-Mail schreiben oder das Kontaktformular auf der Website ausfüllen.",
       "lb": "Fir den OKaJu z'erreechen, kënnt Dir uruffen, eng E-Mail schreiwen oder de Kontaktformulaire um Site ausfëllen."}
first = lambda t: t.split(". ", 1)[0] + "."      # first sentence of a turn
rest = lambda t: t.split(". ", 1)[1]             # everything after the first sentence

def cet(L, lang):
    o = lambda i: list(L[i])
    s = lambda i: ["TOM" if L[i][0] == "ANNA" else "ANNA", L[i][1]]
    N = [o(0), o(1), o(2), ["TOM", CET_OPEN_T[lang]], ["ANNA", CET_OPEN_A[lang]],
         ["TOM", CET_5.get(lang, L[5][1])], ["ANNA", CET_6.get(lang, L[6][1])]]
    N += [o(i) for i in range(7, 19)]                                            # Anna explains: the basics
    N += [["TOM", first(L[19][1]) + " " + L[20][1]]] + [s(i) for i in range(21, 37)]   # Tom: grounds + fields
    N += [["ANNA", first(L[37][1]) + " " + L[38][1]]] + [o(i) for i in range(39, 49)]  # Anna: forms
    N += [["TOM", F3T[lang]]] + [s(i) for i in range(51, 61)]                    # Tom: what the CET does
    N += [["ANNA", P4[lang] + " " + L[62][1]]] + [o(i) for i in range(63, 71)]   # Anna: courts
    N += [["TOM", P5[lang] + " " + L[72][1]]] + [s(i) for i in range(73, 81)]    # Tom: contact
    N += [["ANNA", P6[lang] + " " + L[82][1]]] + [o(i) for i in range(83, 97)]   # Anna: website; summary; outro
    assert len(L) == 97 and len(N) == 91
    return N

def omb(L, lang):
    o = lambda i: list(L[i])
    s = lambda i: ["TOM" if L[i][0] == "ANNA" else "ANNA", L[i][1]]
    N = [o(0), o(1), o(2), ["TOM", OMB_T[lang]], ["ANNA", OMB_A[lang]]] + [o(i) for i in range(5, 29)]   # Anna: the Ombudsman
    N += [["TOM", M29[lang] + " " + rest(L[30][1])]] + [s(i) for i in range(31, 35)]       # Tom: first write to the administration
    N += [["ANNA", M35[lang] + " " + rest(L[36][1])]] + [o(i) for i in range(37, 49)]      # Anna: sending the complaint, limits, deadlines
    N += [["TOM", L[50][1]]] + [s(i) for i in range(51, 55)]                               # Tom: second mission, website
    N += [["ANNA", M55[lang]], ["TOM", O57.get(lang, L[57][1])]] + [o(i) for i in range(58, 66)]   # Tom: the OKaJu
    N += [["ANNA", M66[lang] + " " + rest(L[67][1])]] + [s(i) for i in range(68, 76)]      # Anna: who can contact it
    N += [["TOM", M76[lang] + " " + rest(L[77][1])]] + [o(i) for i in range(78, 103)]      # Tom: steps, limits; summary; outro
    assert len(L) == 103 and len(N) == 97
    return N

for key, fn in (("cet", cet), ("ombudsman", omb)):
    for lang, sfx in SFX.items():
        p = f"podcast_script_{key}{sfx}.md"; text = open(p, encoding="utf-8").read()
        ms = list(TURN.finditer(text))
        if OLD[lang] not in ms[3].group(3): print(p, "already done"); continue
        sp = ms[3].group(2)
        L = [(m.group(1), m.group(3)) for m in ms]
        N = fn(L, lang)
        assert all(N[i][0] != N[i+1][0] for i in range(len(N)-1)), "speakers must alternate"
        body = "\n".join(f"**{a}{sp}:** {t}" for a, t in N)
        out = text[:ms[0].start()] + body + text[ms[-1].end():]
        print(p, len(L), "->", len(N), "turns;", sum(1 for a, t in N if (a, t) not in L), "new/changed lines")
        if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write(out)
