#!/usr/bin/env python3
"""Fact-check ONIS (9 Nov 2026): ADEM profiles REVIS applicants first and refers only people far from work
to ONIS; activation allowance; sanctions; plan up to a year; temporary exemptions. EN/FR/DE/LB, idempotent."""
import re, sys
R = {}
R[""] = [
 ("Exactly. The FNS handles the money. ONIS handles the people, and their path forward.",
  "Partly — and this is important. The FNS handles the money. For people who are ready to look for a job, the inclusion side is ADEM, the employment agency. But for people who are still far from work, it's ONIS — it handles the people, and their path forward."),
 ("Sure. It usually begins with an invitation — you're invited to a meeting, a reception, with ONIS. And there, you sign",
  "Sure. It actually starts at ADEM. If you're under sixty-five and able to work, ADEM first looks at your situation. If you're ready for a job, ADEM accompanies you. But if there are other difficulties to deal with first, ADEM sends you to ONIS. Then ONIS invites you to an information meeting — and there, you sign"),
 ("and the concrete steps to move forward.",
  "and the concrete steps to move forward. The plan is set for up to a year at a time, and it can be changed whenever your situation changes."),
 ("a useful, community role — often in a non-profit organisation.", "a useful, community role — with a host organisation, for example an association."),
 ("a stepping stone toward a real job.", "a stepping stone toward a real job. And for that work, you receive an activation allowance — based on the minimum wage, for the hours you work."),
 ("that's the collaboration declaration. But the aim", "that's the collaboration declaration — and if someone repeatedly refuses to take part, the payment can be reduced or suspended. But the aim"),
 ("And then ONIS enters his life.", "ADEM looks at his situation, sees that he isn't ready for a job yet, and sends him to ONIS. And that's when ONIS enters his life."),
 ("Nobody is pushed faster than they can go.",
  "Nobody is pushed faster than they can go. And in some situations — for example if you look after a young child and have no childcare, if you care for a family member, or for health reasons — you can be exempted for a while."),
 ("ONIS helps the people furthest from work move forward", "ONIS helps the people furthest from work — the ones ADEM sends to it — move forward"),
]
R["_fr"] = [
 ("Exactement. Le FNS s'occupe de l'argent. L'ONIS s'occupe des personnes, et de leur chemin vers l'avenir.",
  "En partie — et c'est important. Le FNS s'occupe de l'argent. Pour les personnes prêtes à chercher un emploi, le volet inclusion, c'est l'ADEM, l'agence pour l'emploi. Mais pour les personnes encore éloignées du travail, c'est l'ONIS — il s'occupe des personnes, et de leur chemin vers l'avenir."),
 ("Bien sûr. Ça commence généralement par une invitation — on t'invite à un rendez-vous, à un accueil, avec l'ONIS. Et là, tu signes",
  "Bien sûr. En fait, ça commence à l'ADEM. Si tu as moins de soixante-cinq ans et que tu peux travailler, l'ADEM examine d'abord ta situation. Si tu es prêt pour un emploi, c'est l'ADEM qui t'accompagne. Mais s'il y a d'abord d'autres difficultés à régler, l'ADEM t'oriente vers l'ONIS. Ensuite, l'ONIS t'invite à une réunion d'information — et là, tu signes"),
 ("et les étapes concrètes pour avancer.", "et les étapes concrètes pour avancer. Le plan est fixé pour un an au maximum, et il peut être modifié dès que ta situation change."),
 ("— souvent dans une association sans but lucratif.", "— dans un organisme d'accueil, par exemple une association."),
 ("un tremplin vers un vrai emploi.", "un tremplin vers un vrai emploi. Et pour ce travail, tu reçois une allocation d'activation — calculée sur le salaire minimum, selon les heures que tu travailles."),
 ("c'est la déclaration de collaboration. Mais le but", "c'est la déclaration de collaboration — et si quelqu'un refuse plusieurs fois de participer, le paiement peut être réduit ou suspendu. Mais le but"),
 ("Et ensuite, l'ONIS entre dans sa vie.", "L'ADEM examine sa situation, voit qu'il n'est pas encore prêt pour un emploi, et l'oriente vers l'ONIS. Et c'est là que l'ONIS entre dans sa vie."),
 ("Personne n'est poussé plus vite qu'il ne peut aller.",
  "Personne n'est poussé plus vite qu'il ne peut aller. Et dans certaines situations — par exemple si tu t'occupes d'un jeune enfant sans solution de garde, si tu t'occupes d'un proche, ou pour des raisons de santé — tu peux être dispensé pendant un temps."),
 ("l'ONIS aide les personnes les plus éloignées du travail à avancer", "l'ONIS aide les personnes les plus éloignées du travail — celles que l'ADEM oriente vers lui — à avancer"),
]
R["_de"] = [
 ("Genau. Der FNS kümmert sich um das Geld. ONIS kümmert sich um die Menschen und ihren Weg nach vorn.",
  "Teilweise — und das ist wichtig. Der FNS kümmert sich um das Geld. Für Menschen, die bereit sind, eine Arbeit zu suchen, ist die Inklusionsseite die ADEM, die Arbeitsagentur. Aber für Menschen, die noch weit von der Arbeit entfernt sind, ist es ONIS — es kümmert sich um die Menschen und ihren Weg nach vorn."),
 ("Gern. Normalerweise beginnt es mit einer Einladung — du wirst zu einem Treffen eingeladen, einem Empfang, bei ONIS. Und dort unterschreibst du",
  "Gern. Eigentlich beginnt es bei der ADEM. Wenn du unter fünfundsechzig bist und arbeiten kannst, schaut sich die ADEM zuerst deine Situation an. Wenn du bereit für eine Arbeit bist, begleitet dich die ADEM. Aber wenn es zuerst andere Schwierigkeiten zu lösen gibt, schickt dich die ADEM zu ONIS. Dann lädt dich ONIS zu einer Informationsversammlung ein — und dort unterschreibst du"),
 ("und die konkreten Schritte, um voranzukommen.", "und die konkreten Schritte, um voranzukommen. Der Plan gilt jeweils höchstens ein Jahr, und er kann jederzeit geändert werden, wenn sich deine Situation ändert."),
 ("— oft in einer gemeinnützigen Organisation.", "— bei einer Gastorganisation, zum Beispiel einem Verein."),
 ("zu einem Sprungbrett in eine echte Arbeit werden.", "zu einem Sprungbrett in eine echte Arbeit werden. Und für diese Arbeit bekommst du eine Aktivierungszulage — berechnet auf Basis des Mindestlohns, für die Stunden, die du arbeitest."),
 ("das ist die Kooperationserklärung. Aber das Ziel", "das ist die Kooperationserklärung — und wenn jemand wiederholt nicht mitmacht, kann die Zahlung gekürzt oder ausgesetzt werden. Aber das Ziel"),
 ("Und dann tritt ONIS in sein Leben.", "Die ADEM schaut sich seine Situation an, sieht, dass er noch nicht bereit für eine Arbeit ist, und schickt ihn zu ONIS. Und dann tritt ONIS in sein Leben."),
 ("Niemand wird schneller gedrängt, als er gehen kann.",
  "Niemand wird schneller gedrängt, als er gehen kann. Und in manchen Situationen — zum Beispiel wenn du ein kleines Kind ohne Betreuungsplatz versorgst, einen Angehörigen pflegst, oder aus gesundheitlichen Gründen — kannst du für eine Weile davon befreit werden."),
 ("hilft ONIS den Menschen, die am weitesten von der Arbeit entfernt sind, voranzukommen", "hilft ONIS den Menschen, die am weitesten von der Arbeit entfernt sind — denen, die die ADEM zu ihm schickt — voranzukommen"),
]
R["_lb"] = [
 ("Genau. De FNS këmmert sech ëm d'Suen. Den ONIS këmmert sech ëm d'Leit, an ëm hire Wee no vir.",
  "Deelweis — an dat ass wichteg. De FNS këmmert sech ëm d'Suen. Fir Leit, déi prett sinn, eng Aarbecht ze sichen, ass d'Inklusiounssäit d'ADEM, d'Aarbechtsagence. Mä fir Leit, déi nach wäit vun der Aarbecht ewech sinn, ass et den ONIS — hie këmmert sech ëm d'Leit, an ëm hire Wee no vir."),
 ("Gär. Et fänkt normalerweis mat enger Invitatioun un — du gëss op eng Versammlung agelueden, op en Empfang, beim ONIS. An do ënnerschreifs du",
  "Gär. Eigentlech fänkt et bei der ADEM un. Wann s du ënner fënnefasechzeg bass a schaffe kanns, kuckt d'ADEM fir d'éischt deng Situatioun un. Wann s du prett bass fir eng Aarbecht, begleet dech d'ADEM. Mä wann et fir d'éischt aner Schwieregkeeten ze léisen gëtt, schéckt d'ADEM dech bei den ONIS. Dann invitéiert den ONIS dech op eng Informatiounsversammlung — an do ënnerschreifs du"),
 ("an déi konkret Schrëtt fir no vir ze kommen.", "an déi konkret Schrëtt fir no vir ze kommen. De Plang gëllt all Kéier héchstens ee Joer, an e kann ëmmer geännert ginn, wann deng Situatioun sech ännert."),
 ("— dacks an enger Asbl.", "— bei enger Gaaschtorganisatioun, zum Beispill enger Asbl."),
 ("e Schrëtt Richtung enger richteger Aarbecht ginn.", "e Schrëtt Richtung enger richteger Aarbecht ginn. A fir déi Aarbecht kriss du eng Aktivéierungsallocatioun — op Basis vum Mindestloun, fir d'Stonnen, déi s du schaffs."),
 ("dat ass d'Kollaboratiounserklärung. Mä d'Zil", "dat ass d'Kollaboratiounserklärung — a wann een ëmmer erëm refuséiert matzemaachen, kann d'Bezuelung reduzéiert oder ausgesat ginn. Mä d'Zil"),
 ("An dann trëtt den ONIS a säi Liewen.", "D'ADEM kuckt seng Situatioun un, gesäit, datt hien nach net prett ass fir eng Aarbecht, a schéckt hien bei den ONIS. An dann trëtt den ONIS a säi Liewen."),
 ("Keen gëtt méi séier gedréckt, wéi hie ka goen.",
  "Keen gëtt méi séier gedréckt, wéi hie ka goen. An a verschiddene Situatiounen — zum Beispill wann s du dech ëm e klengt Kand ouni Betreiungsplaz këmmers, ëm e Familljemember, oder aus gesondheetleche Grënn — kanns du eng Zäit laang dispenséiert ginn."),
 ("hëlleft den ONIS deene Leit, déi am wäitsten ewech vun der Aarbecht sinn, no vir ze kommen", "hëlleft den ONIS deene Leit, déi am wäitsten ewech vun der Aarbecht sinn — deenen, déi d'ADEM bei hie schéckt — no vir ze kommen"),
]
NOTE = {
 "": " ADEM first profiles REVIS applicants under 65 who are able to work; only people with specific social/professional activation needs are referred to ONIS (onis.gouvernement.lu, updated 04.08.2025). Activation allowance for work of public utility (TUC), based on the unskilled social minimum wage; activation plan valid up to one year; temporary dispensations; sanctions. Fact-checked 9 November 2026.",
 "_fr": " L'ADEM procède d'abord au profilage des demandeurs du REVIS de moins de 65 ans aptes au travail ; seules les personnes ayant des besoins spécifiques d'activation sont orientées vers l'ONIS (onis.gouvernement.lu, mis à jour le 04.08.2025). Allocation d'activation pour les travaux d'utilité collective (TUC), sur base du salaire social minimum non qualifié ; plan d'activation d'un an au maximum ; dispenses temporaires ; sanctions. Vérifié le 9 novembre 2026.",
 "_de": " Die ADEM nimmt zuerst ein Profiling der REVIS-Antragsteller unter 65 vor, die arbeiten können; nur Menschen mit besonderem Aktivierungsbedarf werden an ONIS verwiesen (onis.gouvernement.lu, aktualisiert am 04.08.2025). Aktivierungszulage für gemeinnützige Arbeiten (TUC) auf Basis des unqualifizierten Mindestlohns; Aktivierungsplan höchstens ein Jahr; vorübergehende Befreiungen; Sanktionen. Geprüft am 9. November 2026.",
 "_lb": " D'ADEM mécht fir d'éischt e Profiling vun de REVIS-Demandeuren ënner 65, déi schaffe kënnen; nëmmen d'Leit mat spezifeschen Aktivéierungsbesoinen ginn op den ONIS orientéiert (onis.gouvernement.lu, 04.08.2025). Aktivéierungsallocatioun fir TUC; Aktivéierungsplang héchstens ee Joer; temporär Dispensen; Sanktiounen. Iwwerpréift den 9. November 2026.",
}
write = "--dry" not in sys.argv
for L, pairs in R.items():
    p = f"podcast_script_onis{L}.md"
    s = open(p, encoding="utf-8").read()
    n0 = len(re.findall(r"^\*\*(ANNA|TOM)\s?:\*\*", s, re.M)); done = 0
    for old, new in pairs:
        if new in s: continue
        c = s.count(old)
        if c != 1: sys.exit(f"{p}: expected 1 match, got {c}: {old[:60]}")
        s = s.replace(old, new); done += 1
    if "04.08.2025" not in s:
        m = list(re.finditer(r"\*\s*$", s))
        e = m[-1].start(); s = s[:e].rstrip() + NOTE[L] + s[e:]; done += 1
    n1 = len(re.findall(r"^\*\*(ANNA|TOM)\s?:\*\*", s, re.M)); assert n0 == n1
    print(p, "changes:", done, "turns:", n1)
    if write: open(p, "w", encoding="utf-8").write(s)
