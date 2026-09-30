#!/usr/bin/env python3
"""Apply the fact-check changes of 30 Sept 2026 (episodes 1-13) to the .md scripts.

Validated by Jacques ("apply all suggestions"), see project doc
claude/factcheck_episodes_1-13_2026-09-30.md. Each edit replaces exactly one
occurrence; re-running is safe (already-applied edits are skipped).
Usage: python3 build/apply_factcheck_2026_09.py [--write]
"""
import re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = "re:"  # prefix: regex (MULTILINE), replaces up to end of line when pattern ends with .*$

E = []
def ed(key, lang, old, new):
    E.append((key, lang, old, new))

# ---------------- 1 MyGuichet ----------------
# 1D Guichet.lu = information portal, MyGuichet.lu = secure space
ed("myguichet", "en", "MyGuichet.lu is the information portal that simplifies your interactions with the State. It gives you",
   "Guichet.lu is the State's information website, and MyGuichet.lu is its secure online space. Together they give you")
ed("myguichet", "en", "It's secure, and it's your...", "MyGuichet.lu is secure, and it's your...")
ed("myguichet", "fr", "MyGuichet.lu est le portail d'information qui simplifie vos échanges avec l'État. Il vous donne",
   "Guichet.lu est le site d'information de l'État, et MyGuichet.lu est son espace sécurisé en ligne. Ensemble, ils vous donnent")
ed("myguichet", "fr", "C'est sécurisé, et c'est votre...", "MyGuichet.lu est sécurisé, et c'est votre...")
ed("myguichet", "de", "MyGuichet.lu ist das Informationsportal, das Ihre Interaktionen mit dem Staat vereinfacht. Es bietet Ihnen",
   "Guichet.lu ist die Informationsseite des Staates, und MyGuichet.lu ist der dazugehörige sichere Online-Bereich. Zusammen bieten sie Ihnen")
ed("myguichet", "de", "Es ist sicher, und es ist Ihre...", "MyGuichet.lu ist sicher, und es ist Ihre...")
ed("myguichet", "lb", "MyGuichet.lu ass den Informatiounsportal, deen Är Kontakter mam Staat méi einfach mécht. E gëtt Iech",
   "Guichet.lu ass d'Informatiounssäit vum Staat, a MyGuichet.lu ass säi séchere Beräich online. Zesumme ginn se Iech")
ed("myguichet", "lb", "En ass sécher, an en ass Är...", "MyGuichet.lu ass sécher, an en ass Är...")
# 1A first registration needs a computer
ed("myguichet", "en", "Then you need an email address, a computer or a smartphone... and one more thing. A way to prove your identity online.",
   "Then you need an email address, and a computer — for the first registration, a laptop or desktop, not your phone. And one more thing: a way to prove your identity online.")
ed("myguichet", "fr", "Ensuite, il vous faut une adresse e-mail, un ordinateur ou un smartphone... et encore une chose. Un moyen de prouver votre identité en ligne.",
   "Ensuite, il vous faut une adresse e-mail et un ordinateur — pour la première inscription, un ordinateur portable ou fixe, pas votre téléphone. Et encore une chose : un moyen de prouver votre identité en ligne.")
ed("myguichet", "de", "Dann brauchen Sie eine E-Mail-Adresse, einen Computer oder ein Smartphone... und noch eine Sache. Eine Möglichkeit, Ihre Identität online nachzuweisen.",
   "Dann brauchen Sie eine E-Mail-Adresse und einen Computer — für die erste Registrierung einen Laptop oder Desktop-PC, nicht Ihr Handy. Und noch eine Sache: eine Möglichkeit, Ihre Identität online nachzuweisen.")
ed("myguichet", "lb", "Da braucht Dir eng E-Mail-Adress, e Computer oder e Smartphone... an nach eppes. E Wee, fir Är Identitéit online ze beweisen.",
   "Da braucht Dir eng E-Mail-Adress an e Computer — fir déi éischt Aschreiwung e Laptop oder en Desktop, net Ären Handy. An nach eppes: e Wee, fir Är Identitéit online ze beweisen.")
# 1C foreign (eIDAS) login
ed("myguichet", "en", "you can often use it to log in to MyGuichet. And one more thing",
   "you can often use it to log in to MyGuichet — you still need your matricule. But with a foreign login, you can't sign some forms, like your tax return. And one more thing")
ed("myguichet", "fr", "vous pouvez souvent l'utiliser pour vous connecter à MyGuichet. Et encore une chose",
   "vous pouvez souvent l'utiliser pour vous connecter à MyGuichet — il vous faut quand même votre matricule. Mais avec un accès étranger, vous ne pouvez pas signer certains formulaires, comme votre déclaration d'impôts. Et encore une chose")
ed("myguichet", "de", "können Sie es oft nutzen, um sich bei MyGuichet anzumelden. Und noch eine Sache",
   "können Sie es oft nutzen, um sich bei MyGuichet anzumelden — Ihre Matricule-Nummer brauchen Sie trotzdem. Aber mit einem ausländischen Zugang können Sie manche Formulare nicht unterschreiben, zum Beispiel Ihre Steuererklärung. Und noch eine Sache")
ed("myguichet", "lb", "kënnt Dir en dacks benotzen, fir Iech op MyGuichet anzeloggen. An nach eppes",
   "kënnt Dir en dacks benotzen, fir Iech op MyGuichet anzeloggen — Äre Matricule braucht Dir awer ëmmer. Mä mat engem auslännesche Login kënnt Dir verschidde Formulairen net ënnerschreiwen, wéi Är Steiererklärung. An nach eppes")
# 1B European elections: EU citizens only
ed("myguichet", "en", "so you can vote in the communal elections, and in the European elections.",
   "so you can vote in the communal elections. And if you're a citizen of another EU country, in the European elections too.")
ed("myguichet", "fr", "pour pouvoir voter aux élections communales, et aux élections européennes.",
   "pour pouvoir voter aux élections communales. Et si vous êtes citoyen d'un autre pays de l'UE, aussi aux élections européennes.")
ed("myguichet", "de", "damit Sie bei den Gemeindewahlen und bei den Europawahlen wählen können.",
   "damit Sie bei den Gemeindewahlen wählen können. Und wenn Sie Bürger eines anderen EU-Landes sind, auch bei den Europawahlen.")
ed("myguichet", "lb", "sou datt Dir bei de Gemengewalen, an och bei den Europawale wiele kënnt.",
   "sou datt Dir bei de Gemengewale wiele kënnt. A wann Dir Bierger vun engem anere Land vun der EU sidd, och bei den Europawalen.")

# ---------------- 2 LuxTrust ----------------
# 2A 4-hour delay only for the SmartCard
ed("luxtrust", "en", "after activation, the certificate becomes usable after about four hours.",
   "if you have the SmartCard, the certificate becomes usable only about four hours after activation.")
ed("luxtrust", "fr", "après l'activation, le certificat devient utilisable au bout d'environ quatre heures.",
   "si vous avez la SmartCard, le certificat ne devient utilisable qu'environ quatre heures après l'activation.")
ed("luxtrust", "de", "nach der Aktivierung ist das Zertifikat nach etwa vier Stunden nutzbar.",
   "wenn Sie die SmartCard haben, ist das Zertifikat erst etwa vier Stunden nach der Aktivierung nutzbar.")
ed("luxtrust", "lb", "no der Aktivéierung gëtt de Certificat no ongeféier véier Stonnen benotzbar.",
   "wann Dir d'SmartCard hutt, gëtt de Certificat eréischt ongeféier véier Stonnen no der Aktivéierung benotzbar.")
# 2B official LuxTrust wording (codes are already covered in the previous turn)
ed("luxtrust", "en", "They will never ask for access to your computer or your phone.",
   "They will never ask you to confirm a payment or a banking operation.")
ed("luxtrust", "fr", "Ils ne demanderont jamais l'accès à votre ordinateur ou à votre téléphone.",
   "Ils ne vous demanderont jamais de confirmer un paiement ou une opération bancaire.")
ed("luxtrust", "de", "Sie werden niemals nach Zugang zu Ihrem Computer oder Ihrem Telefon fragen.",
   "Sie werden Sie niemals bitten, eine Zahlung oder eine Bankoperation zu bestätigen.")
ed("luxtrust", "lb", "Si wäerten ni no Zougang zu Ärem Computer oder Ärem Handy froen.",
   "Si wäerten Iech ni froen, e Paiement oder eng Bankoperatioun ze confirméieren.")

# ---------------- 3 Volunteering ----------------
ed("benevolat", "en", "Real examples on the site right now: helping at a gymnastics gala for one weekend. Being a marshal for one day at a cycling race. Manning the barbecue at a summer party. Making Christmas decorations.",
   "For example: helping at a sports gala for one weekend. Being a marshal for one day at a cycling race. Helping at a summer party. Or making Christmas decorations.")
ed("benevolat", "fr", "Des exemples réels sur le site en ce moment : aider à un gala de gymnastique pendant un week-end. Être signaleur pour une journée lors d'une course cycliste. Tenir le barbecue à une fête d'été. Fabriquer des décorations de Noël.",
   "Par exemple : aider à un gala sportif pendant un week-end. Être signaleur pour une journée lors d'une course cycliste. Donner un coup de main à une fête d'été. Ou fabriquer des décorations de Noël.")
ed("benevolat", "de", "Echte Beispiele, die gerade auf der Seite stehen: bei einer Turngala ein Wochenende lang helfen. Einen Tag lang Streckenposten bei einem Radrennen sein. Beim Sommerfest den Grill übernehmen. Weihnachtsdekoration basteln.",
   "Zum Beispiel: bei einer Sportgala ein Wochenende lang helfen. Einen Tag lang Streckenposten bei einem Radrennen sein. Bei einem Sommerfest mithelfen. Oder Weihnachtsdekoration basteln.")
ed("benevolat", "lb", "Richteg Beispiller, déi elo grad um Site stinn: e Weekend bei engem Turngala hëllefen. Een Dag Commissaire bei engem Vëlosrennen sinn. De Grill op engem Summerfest bedéngen. Chrëschtdekoratioune bastelen.",
   "Zum Beispill: e Weekend bei engem Sportsgala hëllefen. Een Dag Commissaire bei engem Vëlosrennen sinn. Bei engem Summerfest mat upaken. Oder Chrëschtdekoratioune bastelen.")

# ---------------- 5 Digital Inclusion (hedged wording, 5A option b) ----------------
ed("digitalinclusion", "en", R + r"Or you hold a residence permit of the .*$",
   "There are a few other cases too, so check the website to see if you qualify.")
ed("digitalinclusion", "fr", R + r"Ou vous détenez un titre de séjour .*$",
   "Il existe aussi quelques autres cas, alors vérifiez sur le site si vous y avez droit.")
ed("digitalinclusion", "de", R + r"Oder Sie haben einen Aufenthaltstitel vom Typ .*$",
   "Es gibt auch noch einige andere Fälle, schauen Sie also auf der Website nach, ob Sie berechtigt sind.")
ed("digitalinclusion", "lb", R + r"Oder du hues eng Openthaltserlaabnis vum Typ .*$",
   "Et ginn nach e puer aner Fäll, also kuck um Site, ob s du berechtegt bass.")
ed("digitalinclusion", "en", R + r"And here's some good recent news\. In the past, it was one computer per household\..*$",
   "Usually, it's one laptop per household. But other members of the family can often ask for an extra computer too.")
ed("digitalinclusion", "fr", R + r"Et voici une bonne nouvelle récente\..*$",
   "En général, c'est un ordinateur portable par ménage. Mais les autres membres de la famille peuvent souvent demander un ordinateur en plus.")
ed("digitalinclusion", "de", R + r"Und hier eine gute Neuigkeit aus jüngster Zeit\..*$",
   "Meistens gibt es einen Laptop pro Haushalt. Aber die anderen Familienmitglieder können oft auch einen zusätzlichen Computer beantragen.")
ed("digitalinclusion", "lb", R + r"An hei ass e puer gutt rezent Neiegkeet\..*$",
   "Meeschtens ass et e Laptop pro Haushalt. Mä déi aner Membere vun der Famill kënnen dacks och en zousätzleche Computer froen.")
ed("digitalinclusion", "en", R + r"So now the teenager doing homework, .*$",
   "So the teenager doing homework, and the parent looking for work, may each get a machine?")
ed("digitalinclusion", "fr", R + r"Donc maintenant, l'adolescent qui fait ses devoirs, .*$",
   "Donc l'adolescent qui fait ses devoirs, et le parent qui cherche du travail, peuvent peut-être avoir chacun une machine ?")
ed("digitalinclusion", "de", R + r"Jetzt können also der Jugendliche, .*$",
   "Dann können also der Jugendliche, der seine Hausaufgaben macht, und der Elternteil, der Arbeit sucht, vielleicht jeweils ein Gerät bekommen?")
ed("digitalinclusion", "lb", R + r"Also kënnen elo den Teenager, .*$",
   "Also kéinten den Teenager, deen Hausaufgaben mécht, an den Elterendeel, deen Aarbecht sicht, all een e Computer kréien?")
ed("digitalinclusion", "en", R + r"Each their own\. Adults apply .*$",
   "Often, yes. The rules change from time to time, so the website explains the latest ones — and how long you might have to wait.")
ed("digitalinclusion", "fr", R + r"Chacun la sienne\. .*$",
   "Souvent, oui. Les règles changent de temps en temps, donc le site explique les plus récentes — et combien de temps vous devrez peut-être attendre.")
ed("digitalinclusion", "de", R + r"Jeder sein eigenes\. .*$",
   "Oft, ja. Die Regeln ändern sich von Zeit zu Zeit, deshalb erklärt die Website die aktuellen — und wie lange Sie vielleicht warten müssen.")
ed("digitalinclusion", "lb", R + r"All säin eegenen\. .*$",
   "Dacks, jo. D'Reegelen änneren sech vun Zäit zu Zäit, dofir erkläert de Site déi aktuell — a wéi laang s du eventuell muss waarden.")
ed("digitalinclusion", "en", "Under a month — that's fast. ", "Good to know. ")
ed("digitalinclusion", "fr", "Moins d'un mois — c'est rapide. ", "Bon à savoir. ")
ed("digitalinclusion", "de", "Unter einem Monat — das ist schnell. ", "Gut zu wissen. ")
ed("digitalinclusion", "lb", "Ënner engem Mount — dat ass séier. ", "Gutt ze wëssen. ")
# 5B operating systems
ed("digitalinclusion", "en", "Windows, or a Mac, or sometimes Linux.", "usually Windows, or a Mac.")
ed("digitalinclusion", "fr", "Windows, ou un Mac, ou parfois Linux.", "généralement Windows, ou un Mac.")
ed("digitalinclusion", "de", "Windows, oder ein Mac, oder manchmal Linux.", "meistens Windows, oder ein Mac.")
ed("digitalinclusion", "lb", "Windows, oder e Mac, oder heiansdo Linux.", "meeschtens Windows, oder e Mac.")
# Amina's story and the summary
ed("digitalinclusion", "en", "She applies — and within about a month, she receives a working laptop. And because of the new rule, her two teenagers can get computers for their schoolwork too.",
   "She applies — and some time later, she receives a working laptop. And she can ask whether her two teenagers can get a computer for their schoolwork too.")
ed("digitalinclusion", "fr", "Elle fait une demande — et en un mois environ, elle reçoit un ordinateur portable qui fonctionne. Et grâce à la nouvelle règle, ses deux adolescents peuvent aussi obtenir des ordinateurs pour leurs devoirs.",
   "Elle fait une demande — et quelque temps plus tard, elle reçoit un ordinateur portable qui fonctionne. Et elle peut demander si ses deux adolescents peuvent aussi obtenir un ordinateur pour leurs devoirs.")
ed("digitalinclusion", "de", "Sie stellt einen Antrag — und innerhalb von etwa einem Monat erhält sie einen funktionierenden Laptop. Und wegen der neuen Regel können auch ihre beiden Teenager Computer für ihre Schularbeiten bekommen.",
   "Sie stellt einen Antrag — und einige Zeit später erhält sie einen funktionierenden Laptop. Und sie kann fragen, ob auch ihre beiden Teenager einen Computer für ihre Schularbeiten bekommen können.")
ed("digitalinclusion", "lb", "Si bewerbt sech — an no ongeféier engem Mount kritt si e funktionéierende Laptop. A wéinst der neier Reegel kënnen hir zwee Teenager och Computere fir hir Schoulaarbecht kréien.",
   "Si bewerbt sech — an e bësse méi spéit kritt si e funktionéierende Laptop. A si ka froen, ob hir zwee Teenager och e Computer fir hir Schoulaarbecht kréie kënnen.")
ed("digitalinclusion", "en", "A free, working computer, usually within a month.", "A free, working computer.")
ed("digitalinclusion", "fr", "Un ordinateur gratuit, qui fonctionne, généralement en moins d'un mois.", "Un ordinateur gratuit, qui fonctionne.")
ed("digitalinclusion", "de", "Ein kostenloser, funktionierender Computer, meist innerhalb eines Monats.", "Ein kostenloser, funktionierender Computer.")
ed("digitalinclusion", "lb", "E gratis, funktionéierende Computer, meeschtens bannent engem Mount.", "E gratis, funktionéierende Computer.")
# source notes
ed("digitalinclusion", "en", R + r"Free second-hand computers go to .*?own computer\.",
   "Free second-hand computers go to people living in Luxembourg who meet one of the conditions — for example households receiving the cost-of-living allowance (allocation de vie chère), asylum seekers and beneficiaries of temporary protection; unaccompanied minors apply through their social worker. When checked on 30.09.2026, the site's pages differed on further cases, the number of computers per household and waiting times — check with Digital Inclusion for the current conditions.")
ed("digitalinclusion", "fr", R + r"Les ordinateurs d'occasion gratuits sont destinés .*?propre ordinateur\.",
   "Les ordinateurs d'occasion gratuits sont destinés aux personnes vivant au Luxembourg qui remplissent une des conditions — par exemple les ménages qui perçoivent l'allocation de vie chère (AVC), les demandeurs d'asile et les bénéficiaires de la protection temporaire ; les mineurs non accompagnés font la demande via leur assistant social. Lors de la vérification du 30.09.2026, les pages du site divergeaient sur les autres cas, le nombre d'ordinateurs par ménage et les délais d'attente — renseignez-vous auprès de Digital Inclusion pour les conditions actuelles.")
ed("digitalinclusion", "de", R + r"Kostenlose gebrauchte Computer gehen an .*?eigenen Computer erhalten\.",
   "Kostenlose gebrauchte Computer gehen an Menschen mit Wohnsitz in Luxemburg, die eine der Bedingungen erfüllen — zum Beispiel Haushalte, die die Teuerungszulage (allocation de vie chère) beziehen, Asylsuchende und Begünstigte vorübergehenden Schutzes; unbegleitete Minderjährige stellen den Antrag über ihren Sozialarbeiter. Bei der Prüfung am 30.09.2026 widersprachen sich die Seiten der Website zu weiteren Fällen, zur Zahl der Computer pro Haushalt und zu den Wartezeiten — die aktuellen Bedingungen bitte bei Digital Inclusion erfragen.")
ed("digitalinclusion", "lb", R + r"Gratis Occasiouns-Computere ginn .*?Computer kréien\.",
   "Gratis Occasiouns-Computere ginn un d'Leit, déi zu Lëtzebuerg wunnen an eng vun de Konditiounen erfëllen — zum Beispill Haushalter, déi d'allocation de vie chère (AVC) kréien, Asylsicher a Beneficiairë vun temporärem Schutz; mannerjäreg Onbegleete stellen hiren Demande iwwer hire Sozialaarbechter. Bei der Kontroll den 30.09.2026 waren d'Säite vum Site sech net eens iwwer aner Fäll, d'Zuel vu Computeren pro Haushalt an d'Waardezäiten — frot bei Digital Inclusion no den aktuelle Konditiounen.")

# ---------------- 6 Work in Luxembourg ----------------
ed("workinluxembourg", "en", "it puts you in touch with the right one.",
   "it puts you in touch with the right one. You can reach the Talent Desk by email, at contact@talentdesk.lu, or visit them in Kirchberg, by appointment.")
ed("workinluxembourg", "fr", "il vous met en contact avec la bonne.",
   "il vous met en contact avec la bonne. Vous pouvez joindre le Talent Desk par e-mail, à contact@talentdesk.lu, ou lui rendre visite au Kirchberg, sur rendez-vous.")
ed("workinluxembourg", "de", "stellt er den Kontakt zur richtigen her.",
   "stellt er den Kontakt zur richtigen her. Du erreichst den Talent Desk per E-Mail unter contact@talentdesk.lu, oder du besuchst ihn nach Terminvereinbarung auf Kirchberg.")
ed("workinluxembourg", "lb", "bréngt hien dech mat der richteger a Kontakt.",
   "bréngt hien dech mat der richteger a Kontakt. Du erreechs den Talent Desk per E-Mail op contact@talentdesk.lu, oder du besichs en um Kierchbierg, op Rendez-vous.")

# ---------------- 7 Your health (DSP / CNS) ----------------
# 7D DSP is created automatically
ed("dsp_cns", "en", R + r"Every person affiliated to the Luxembourg health insurance can have one\..*$",
   "Good news — you don't need to open it. If you're affiliated to the Luxembourg health insurance, your DSP is created automatically. To use it yourself online, you activate your \"eSanté account\". And you can do that directly through MyGuichet.lu.")
ed("dsp_cns", "fr", R + r"Toute personne affiliée à l'assurance maladie luxembourgeoise peut en avoir un\..*$",
   "Bonne nouvelle — vous n'avez pas besoin de l'ouvrir. Si vous êtes affilié à l'assurance maladie luxembourgeoise, votre DSP est créé automatiquement. Pour l'utiliser vous-même en ligne, vous activez votre « compte eSanté ». Et vous pouvez le faire directement via MyGuichet.lu.")
ed("dsp_cns", "de", R + r"Jede Person, die bei der luxemburgischen Krankenversicherung angemeldet ist, kann eines haben\..*$",
   "Gute Nachricht — Sie müssen es nicht eröffnen. Wenn Sie bei der luxemburgischen Krankenversicherung angemeldet sind, wird Ihr DSP automatisch angelegt. Um es selbst online zu nutzen, aktivieren Sie Ihr „eSanté-Konto“. Und das können Sie direkt über MyGuichet.lu machen.")
ed("dsp_cns", "lb", R + r"All Persoun, déi bei der Lëtzebuerger Gesondheetskeess affiliéiert ass, kann een hunn\..*$",
   "Gutt Nouvelle — Dir musst en net opmaachen. Wann Dir bei der Lëtzebuerger Gesondheetskeess affiliéiert sidd, gëtt Ären DSP automatesch ugeluecht. Fir en selwer online ze benotzen, aktivéiert Dir Ären \"eSanté-Kont\". An dat kënnt Dir direkt iwwer MyGuichet.lu maachen.")
# 7A immediate direct payment
ed("dsp_cns", "en", R + r"The Luxembourg system traditionally works by reimbursement\..*$",
   "Traditionally, you pay the doctor first, and then the CNS pays you back most of it. But today, about half of doctors use \"immediate direct payment\". Then you only pay your own small share, and the CNS pays the doctor the rest straight away.")
ed("dsp_cns", "fr", R + r"Le système luxembourgeois fonctionne traditionnellement par remboursement\..*$",
   "Traditionnellement, vous payez d'abord le médecin, et ensuite la CNS vous rembourse la plus grande partie. Mais aujourd'hui, environ la moitié des médecins utilisent le « paiement immédiat direct ». Dans ce cas, vous ne payez que votre petite part, et la CNS paie le reste au médecin tout de suite.")
ed("dsp_cns", "de", R + r"Das luxemburgische System funktioniert traditionell über die Rückerstattung\..*$",
   "Traditionell zahlen Sie zuerst beim Arzt, und dann zahlt die CNS Ihnen das meiste davon zurück. Aber heute nutzt etwa die Hälfte der Ärzte die „sofortige Direktzahlung“. Dann zahlen Sie nur Ihren eigenen kleinen Anteil, und die CNS zahlt dem Arzt den Rest sofort.")
ed("dsp_cns", "lb", R + r"De Lëtzebuerger System funktionéiert traditionell mam Remboursement\..*$",
   "Traditionell bezuelt Dir fir d'éischt den Dokter, an duerno bezilt d'CNS Iech dat meescht zeréck. Mä haut benotzt ongeféier d'Hallschent vun den Dokteren den \"direkte Sofortpaiement\", de Paiement immédiat direct. Da bezuelt Dir just Ären eegene klengen Undeel, an d'CNS bezilt dem Dokter de Rescht direkt.")
ed("dsp_cns", "en", "So I pay the full price at the doctor, and then get money back later.",
   "So either I pay the full price and get money back later — or, with direct payment, I only pay my share.")
ed("dsp_cns", "fr", "Donc je paie le prix complet chez le médecin, et je récupère l'argent plus tard.",
   "Donc soit je paie le prix complet et je récupère l'argent plus tard — soit, avec le paiement direct, je ne paie que ma part.")
ed("dsp_cns", "de", "Ich zahle also beim Arzt den vollen Preis, und bekomme später Geld zurück.",
   "Ich zahle also entweder den vollen Preis und bekomme später Geld zurück — oder, mit der Direktzahlung, nur meinen Anteil.")
ed("dsp_cns", "lb", "Also bezuelen ech de vollen Präis beim Dokter, a kréien duerno Suen zeréck.",
   "Also entweder bezuelen ech de vollen Präis a kréie méi spéit Suen zeréck — oder, mam direkte Paiement, bezuelen ech just mäin Undeel.")
# 7C digital invoices
ed("dsp_cns", "en", "You can send it by post, or drop it in one of their boxes.",
   "You can send it by post, or drop it in one of their boxes. And if your doctor gives you a digital invoice, you can send it with a few clicks — in the CNS app, the GesondheetsApp, or on MyGuichet.lu.")
ed("dsp_cns", "fr", "Vous pouvez l'envoyer par la poste, ou la déposer dans une de leurs boîtes.",
   "Vous pouvez l'envoyer par la poste, ou la déposer dans une de leurs boîtes. Et si votre médecin vous donne une facture digitale, vous pouvez l'envoyer en quelques clics — dans l'application de la CNS, la GesondheetsApp, ou sur MyGuichet.lu.")
ed("dsp_cns", "de", "Sie können sie per Post schicken, oder in einen ihrer Briefkästen werfen.",
   "Sie können sie per Post schicken, oder in einen ihrer Briefkästen werfen. Und wenn Ihr Arzt Ihnen eine digitale Rechnung gibt, können Sie sie mit ein paar Klicks einreichen — in der App der CNS, der GesondheetsApp, oder auf MyGuichet.lu.")
ed("dsp_cns", "lb", "Dir kënnt se mat der Post schécken, oder an eng vun hire Boîten deposéieren.",
   "Dir kënnt se mat der Post schécken, oder an eng vun hire Boîten deposéieren. A wann Ären Dokter Iech eng digital Rechnung gëtt, kënnt Dir se mat e puer Klicken eraschécken — an der App vun der CNS, der GesondheetsApp, oder op MyGuichet.lu.")
# 7B payment times
ed("dsp_cns", "en", "Usually less than three weeks.", "For a paper bill, usually two to four weeks. With a digital bill, it can be just a few days.")
ed("dsp_cns", "fr", "En général, moins de trois semaines.", "Pour une facture papier, en général deux à quatre semaines. Avec une facture digitale, ça peut être quelques jours seulement.")
ed("dsp_cns", "de", "Normalerweise weniger als drei Wochen.", "Bei einer Papierrechnung meist zwei bis vier Wochen. Bei einer digitalen Rechnung können es nur ein paar Tage sein.")
ed("dsp_cns", "lb", "Normalerweis manner wéi dräi Wochen.", "Fir eng Rechnung op Pabeier normalerweis zwou bis véier Wochen. Mat enger digitaler Rechnung kënnen et just e puer Deeg sinn.")
ed("dsp_cns", "en", "The normal doctor visit — I pay first and get reimbursed.",
   "The normal doctor visit — I pay first and get reimbursed, unless my doctor uses direct payment.")
ed("dsp_cns", "fr", "La visite normale chez le médecin — je paie d'abord et je suis remboursé.",
   "La visite normale chez le médecin — je paie d'abord et je suis remboursé, sauf si mon médecin utilise le paiement direct.")
ed("dsp_cns", "de", "Der normale Arztbesuch — ich zahle zuerst und werde erstattet.",
   "Der normale Arztbesuch — ich zahle zuerst und werde erstattet, außer mein Arzt nutzt die Direktzahlung.")
ed("dsp_cns", "lb", "Déi normal Visite beim Dokter — ech bezuele fir d'éischt a gi rembourséiert.",
   "Déi normal Visite beim Dokter — ech bezuele fir d'éischt a gi rembourséiert, ausser mäin Dokter benotzt den direkte Paiement.")
# 7E social third-party payment: municipal social office
ed("dsp_cns", "en", "you can ask about the social third-party payment — often through your doctor or the social office.",
   "you can ask for the social third-party payment at the social office — the office social — of your municipality.")
ed("dsp_cns", "fr", "vous pouvez vous renseigner sur le tiers payant social — souvent via votre médecin ou l'office social.",
   "vous pouvez demander le tiers payant social à l'office social de votre commune.")
ed("dsp_cns", "de", "können Sie nach dem sozialen Drittzahlersystem fragen — oft über Ihren Arzt oder das Sozialamt.",
   "können Sie das soziale Drittzahlersystem beim Sozialamt — dem Office social — Ihrer Gemeinde beantragen.")
ed("dsp_cns", "lb", "kënnt Dir nom Tiers payant social froen — dacks iwwer Ären Dokter oder den Office social.",
   "kënnt Dir den Tiers payant social beim Office social vun Ärer Gemeng ufroen.")
# summary
ed("dsp_cns", "en", "For a normal doctor visit, you pay first and the CNS reimburses most of it into your bank account, in about three weeks.",
   "For a normal doctor visit, either your doctor uses immediate direct payment and you only pay your share — or you pay first, and the CNS reimburses most of it into your bank account, within a few weeks, or a few days for a digital bill.")
ed("dsp_cns", "fr", "Pour une visite normale chez le médecin, vous payez d'abord et la CNS vous rembourse la plus grande partie sur votre compte bancaire, en environ trois semaines.",
   "Pour une visite normale chez le médecin, soit votre médecin utilise le paiement immédiat direct et vous ne payez que votre part — soit vous payez d'abord, et la CNS vous rembourse la plus grande partie sur votre compte bancaire, en quelques semaines, ou en quelques jours pour une facture digitale.")
ed("dsp_cns", "de", "Beim normalen Arztbesuch zahlen Sie zuerst, und die CNS erstattet das meiste davon auf Ihr Bankkonto, in etwa drei Wochen.",
   "Beim normalen Arztbesuch nutzt Ihr Arzt entweder die sofortige Direktzahlung, und Sie zahlen nur Ihren Anteil — oder Sie zahlen zuerst, und die CNS erstattet das meiste davon auf Ihr Bankkonto, innerhalb weniger Wochen, oder weniger Tage bei einer digitalen Rechnung.")
ed("dsp_cns", "lb", "Bei enger normaler Visite beim Dokter bezuelt Dir fir d'éischt, an d'CNS rembourséiert dat meescht dovun op Äre Bankkont, an ongeféier dräi Wochen.",
   "Bei enger normaler Visite beim Dokter benotzt Ären Dokter entweder den direkte Paiement, an Dir bezuelt just Ären Undeel — oder Dir bezuelt fir d'éischt, an d'CNS rembourséiert dat meescht dovun op Äre Bankkont, bannent e puer Wochen, oder e puer Deeg bei enger digitaler Rechnung.")

# ---------------- 8 LU-Alert ----------------
ed("lualert", "en", "Luxembourg runs national tests.", "Luxembourg tests the system every month — and the sirens are tested on the first Monday of the month, around noon.")
ed("lualert", "fr", "Le Luxembourg organise des tests nationaux.", "Le Luxembourg teste le système chaque mois — et les sirènes sont testées le premier lundi du mois, vers midi.")
ed("lualert", "de", "Luxemburg führt nationale Tests durch.", "Luxemburg testet das System jeden Monat — und die Sirenen werden am ersten Montag im Monat gegen Mittag getestet.")
ed("lualert", "lb", "Lëtzebuerg mécht national Tester.", "Lëtzebuerg test de System all Mount — an d'Sirene gi den éischte Méindeg vum Mount géint Mëtteg getest.")

# ---------------- 10 Info-Senior ----------------
ed("infosenior", "en", "It's built on a law that's in force since the first of March, 2024.",
   "It's based on a law from 2023, and the register has been online since the first of March, 2024.")
ed("infosenior", "fr", "Il repose sur une loi en vigueur depuis le premier mars 2024.",
   "Il repose sur une loi de 2023, et le registre est en ligne depuis le premier mars 2024.")
ed("infosenior", "de", "Es beruht auf einem Gesetz, das seit dem ersten März 2024 in Kraft ist.",
   "Es beruht auf einem Gesetz von 2023, und das Register ist seit dem ersten März 2024 online.")
ed("infosenior", "lb", "Hien baséiert op engem Gesetz, dat zënter dem éischte Mäerz 2024 a Kraaft ass.",
   "Hie baséiert op engem Gesetz vun 2023, an de Register ass zënter dem éischte Mäerz 2024 online.")
ed("infosenior", "en", "There's a competence centre for ageing that has existed for about thirty years.",
   "There's a competence centre for ageing, called GERO, that has existed for more than thirty-five years.")
ed("infosenior", "fr", "Il y a un centre de compétences sur le vieillissement qui existe depuis une trentaine d'années.",
   "Il y a un centre de compétences sur le vieillissement, appelé GERO, qui existe depuis plus de trente-cinq ans.")
ed("infosenior", "de", "Es gibt ein Kompetenzzentrum für das Altern, das seit etwa dreißig Jahren besteht.",
   "Es gibt ein Kompetenzzentrum für das Altern, GERO, das seit mehr als fünfunddreißig Jahren besteht.")
ed("infosenior", "lb", "Et gëtt e Kompetenzzenter fir d'Eelerwerden, dee säit ongeféier drësseg Joer existéiert.",
   "Et gëtt e Kompetenzzenter fir d'Eelerwerden, de GERO, dee säit méi wéi fënnefandrësseg Joer existéiert.")
ed("infosenior", "en", R + r"There is a national service for information and mediation in this field\..*$",
   "You can simply call the Senioren-Telefon, 247-86000, for information and advice. And if there's a disagreement with a service, there's SIMPA, the national information and mediation service — a neutral place that helps you find a solution.")
ed("infosenior", "fr", R + r"Il existe un service national d'information et de médiation dans ce domaine\..*$",
   "Vous pouvez tout simplement appeler le Senioren-Telefon, au 247-86000, pour vous informer et vous faire conseiller. Et s'il y a un désaccord avec un service, il y a le SIMPA, le service national d'information et de médiation — un endroit neutre qui vous aide à trouver une solution.")
ed("infosenior", "de", R + r"Es gibt einen nationalen Dienst für Information und Vermittlung in diesem Bereich\..*$",
   "Sie können einfach das Senioren-Telefon anrufen, 247-86000, für Information und Beratung. Und wenn es eine Meinungsverschiedenheit mit einem Dienst gibt, gibt es SIMPA, den nationalen Informations- und Vermittlungsdienst — einen neutralen Ort, der Ihnen hilft, eine Lösung zu finden.")
ed("infosenior", "lb", R + r"Et gëtt en nationale Service fir Informatioun a Mediatioun an dësem Beräich\..*$",
   "Dir kënnt einfach d'Senioren-Telefon uruffen, op 247-86000, fir Informatioun a Berodung. A wann et eng Meenungsverschiddenheet mat engem Service gëtt, da gëtt et de SIMPA, den nationale Service fir Informatioun a Mediatioun — eng neutral Plaz, déi Iech hëlleft, eng Léisung ze fannen.")
ed("infosenior", "en", "And there's also financial support — for people who don't have enough money to cover the cost of care, the State helps.",
   "And there's also financial support. Since 2026, a scheme called COMPA helps people who don't have enough money to pay for a care home or supervised housing.")
ed("infosenior", "fr", "Et il y a aussi un soutien financier — pour les personnes qui n'ont pas assez d'argent pour couvrir le coût des soins, l'État aide.",
   "Et il y a aussi un soutien financier. Depuis 2026, un dispositif appelé COMPA aide les personnes qui n'ont pas assez d'argent pour payer une maison de soins ou un logement encadré.")
ed("infosenior", "de", "Und es gibt auch finanzielle Unterstützung — für Menschen, die nicht genug Geld haben, um die Pflegekosten zu decken, hilft der Staat.",
   "Und es gibt auch finanzielle Unterstützung. Seit 2026 hilft ein Programm namens COMPA Menschen, die nicht genug Geld haben, um ein Pflegeheim oder betreutes Wohnen zu bezahlen.")
ed("infosenior", "lb", "An et gëtt och finanziell Ënnerstëtzung — fir Leit, déi net genuch Geld hunn, fir d'Käschte vun der Fleeg ze decken, hëlleft de Staat.",
   "An et gëtt och finanziell Ënnerstëtzung. Zënter 2026 hëlleft e System mam Numm COMPA de Leit, déi net genuch Geld hunn, fir e Fleegeheem oder e betreit Wunnen ze bezuelen.")
ed("infosenior", "en", "The Public Register is based on the law in force since 1 March 2024.",
   "The Public Register is based on the amended law of 23 August 2023 on the quality of services for older people and has been online since 1 March 2024. Since 1 January 2026, the COMPA scheme (Complément pour personnes âgées, Fonds national de solidarité) helps people with limited resources pay for a care home or supervised housing. Information and advice: Senioren-Telefon 247-86000; mediation: SIMPA (simpa.public.lu).")
ed("infosenior", "fr", "Le Registre public repose sur la loi en vigueur depuis le 1er mars 2024.",
   "Le Registre public repose sur la loi modifiée du 23 août 2023 sur la qualité des services pour personnes âgées et est en ligne depuis le 1er mars 2024. Depuis le 1er janvier 2026, le dispositif COMPA (Complément pour personnes âgées, Fonds national de solidarité) aide les personnes aux ressources limitées à payer une maison de soins ou un logement encadré. Information et conseil : Senioren-Telefon 247-86000 ; médiation : SIMPA (simpa.public.lu).")
ed("infosenior", "de", "Das Öffentliche Register beruht auf dem seit dem 1. März 2024 geltenden Gesetz.",
   "Das Öffentliche Register beruht auf dem geänderten Gesetz vom 23. August 2023 über die Qualität der Dienstleistungen für ältere Menschen und ist seit dem 1. März 2024 online. Seit dem 1. Januar 2026 hilft der COMPA (Complément pour personnes âgées, Nationaler Solidaritätsfonds) Menschen mit geringen Mitteln, ein Pflegeheim oder betreutes Wohnen zu bezahlen. Information und Beratung: Senioren-Telefon 247-86000; Vermittlung: SIMPA (simpa.public.lu).")
ed("infosenior", "lb", "D'Ëffentlecht Register baséiert op dem Gesetz, dat zënter dem 1. Mäerz 2024 a Kraaft ass.",
   "D'Ëffentlecht Register baséiert op dem geännerte Gesetz vum 23. August 2023 iwwer d'Qualitéit vun de Servicer fir eeler Leit an ass zënter dem 1. Mäerz 2024 online. Zënter dem 1. Januar 2026 hëlleft de COMPA (Complément pour personnes âgées, Fonds national de solidarité) Leit mat wéineg Mëttelen, e Fleegeheem oder e betreit Wunnen ze bezuelen. Informatioun a Berodung: Senioren-Telefon 247-86000; Mediatioun: SIMPA (simpa.public.lu).")

# ---------------- 11 Accessibility ----------------
ed("accessibilite", "en", "Roughly speaking, the rules focus on companies with more than ten employees and a certain size of turnover.",
   "If a company has fewer than ten employees and a turnover under two million euros, the rules for services don't apply to it.")
ed("accessibilite", "fr", "En gros, les règles visent les entreprises de plus de dix salariés et d'une certaine taille de chiffre d'affaires.",
   "Si une entreprise a moins de dix salariés et un chiffre d'affaires de moins de deux millions d'euros, les règles sur les services ne s'appliquent pas à elle.")
ed("accessibilite", "de", "Grob gesagt, konzentrieren sich die Regeln auf Unternehmen mit mehr als zehn Mitarbeitern und einer bestimmten Umsatzgröße.",
   "Wenn ein Unternehmen weniger als zehn Mitarbeiter und weniger als zwei Millionen Euro Umsatz hat, gelten die Regeln für Dienstleistungen dort nicht.")
ed("accessibilite", "lb", "Gréif gesot, d'Reegele konzentréiere sech op Entreprise mat méi wéi zéng Mataarbechter an enger gewësser Gréisst u Chiffre d'affaires.",
   "Wann eng Entreprise manner wéi zéng Mataarbechter an e Chiffre d'affaires ënner zwou Milliounen Euro huet, da gëllen d'Reegele fir Déngschtleeschtungen do net.")
ed("accessibilite", "en", "So an architect, a commune, or an owner can find what they need to do it right.",
   "So an architect, a commune, or an owner can find what they need to do it right. And there's money to help: the State can pay half the cost of the works, up to twenty-four thousand euros per place — if you apply before July 2028.")
ed("accessibilite", "fr", "Comme ça, un architecte, une commune ou un propriétaire peut trouver ce qu'il faut faire pour bien s'y prendre.",
   "Comme ça, un architecte, une commune ou un propriétaire peut trouver ce qu'il faut faire pour bien s'y prendre. Et il y a une aide financière : l'État peut payer la moitié du coût des travaux, jusqu'à vingt-quatre mille euros par lieu — si vous faites la demande avant juillet 2028.")
ed("accessibilite", "de", "So kann ein Architekt, eine Gemeinde oder ein Eigentümer finden, was zu tun ist, um es richtig zu machen.",
   "So kann ein Architekt, eine Gemeinde oder ein Eigentümer finden, was zu tun ist, um es richtig zu machen. Und es gibt finanzielle Hilfe: Der Staat kann die Hälfte der Kosten für die Arbeiten übernehmen, bis zu vierundzwanzigtausend Euro pro Ort — wenn Sie den Antrag vor Juli 2028 stellen.")
ed("accessibilite", "lb", "Sou kann en Architekt, eng Gemeng, oder e Besëtzer fannen, wat se brauchen, fir et richteg ze maachen.",
   "Sou kann en Architekt, eng Gemeng, oder e Besëtzer fannen, wat se brauchen, fir et richteg ze maachen. An et gëtt finanziell Hëllef: de Staat ka d'Hallschent vun de Käschte vun den Aarbechten iwwerhuelen, bis zu véieranzwanzegdausend Euro pro Plaz — wann s du den Demande virum Juli 2028 mëss.")

# ---------------- 12 Greater Region ----------------
ed("granderegion", "en", "And there's the cultural association, the Espace Culturel.", "And there are networks of towns and communes, like QuattroPole and EuRegio.")
ed("granderegion", "fr", "Et il y a l'association culturelle, l'Espace Culturel.", "Et il y a des réseaux de villes et de communes, comme QuattroPole et EuRegio.")
ed("granderegion", "de", "Und es gibt den Kulturverein, den Espace Culturel.", "Und es gibt Netzwerke von Städten und Gemeinden, wie QuattroPole und EuRegio.")
ed("granderegion", "lb", "An et gëtt déi kulturell Associatioun, den Espace Culturel.", "An et ginn Netzwierker vu Stied a Gemengen, wéi QuattroPole an EuRegio.")
ed("granderegion", "en", "It links six universities", "It links seven universities")
ed("granderegion", "fr", "Elle relie six universités", "Elle relie sept universités")
ed("granderegion", "de", "Sie verbindet sechs Universitäten", "Sie verbindet sieben Universitäten")
ed("granderegion", "lb", "Si verbënnt sechs Universitéiten", "Si verbënnt siwen Universitéiten")
ed("granderegion", "en", "Six universities working as one network.", "Seven universities working as one network.")
ed("granderegion", "fr", "Six universités qui fonctionnent comme un seul réseau.", "Sept universités qui fonctionnent comme un seul réseau.")
ed("granderegion", "de", "Sechs Universitäten, die als ein Netzwerk arbeiten.", "Sieben Universitäten, die als ein Netzwerk arbeiten.")
ed("granderegion", "lb", "Sechs Universitéiten, déi als ee Reseau schaffen.", "Siwen Universitéiten, déi als ee Reseau schaffen.")
ed("granderegion", "en", "More than a hundred and thirty thousand students", "More than a hundred and forty thousand students")
ed("granderegion", "fr", "Plus de cent trente mille étudiants", "Plus de cent quarante mille étudiants")
ed("granderegion", "de", "Mehr als hundertdreißigtausend Studierende", "Mehr als hundertvierzigtausend Studierende")
ed("granderegion", "lb", "Méi wéi honnertdräissegdausend Studenten", "Méi wéi honnertvéierzegdausend Studenten")
ed("granderegion", "en", "That left behind a cultural association — the Espace Culturel — which is actually one of the neighbours in the House.",
   "That year left a real cross-border cultural spirit behind — and you can still feel it all over the Region.")
ed("granderegion", "fr", "Ça a laissé derrière une association culturelle — l'Espace Culturel — qui est justement l'un des voisins dans la Maison.",
   "Cette année a laissé un vrai esprit culturel transfrontalier — et on le sent encore partout dans la Région.")
ed("granderegion", "de", "Daraus ist ein Kulturverein hervorgegangen — der Espace Culturel — der tatsächlich einer der Nachbarn im Haus ist.",
   "Dieses Jahr hat einen echten grenzüberschreitenden Kulturgeist hinterlassen — und man spürt ihn noch überall in der Region.")
ed("granderegion", "lb", "Dat huet eng kulturell Associatioun hannerlooss — den Espace Culturel — deen tatsächlech ee vun den Noperen am Haus ass.",
   "Dat Joer huet e richtege grenziwwerschreidende kulturelle Geescht hannerlooss — an dee spiert een nach ëmmer an der ganzer Regioun.")
ed("granderegion", "en", "So the House isn't only about politics and paperwork — there's culture living inside it too.",
   "So the Greater Region isn't only about politics and paperwork — there's real culture living in it too.")
ed("granderegion", "fr", "Donc la Maison, ce n'est pas seulement de la politique et de la paperasse — il y a aussi de la culture qui vit à l'intérieur.",
   "Donc la Grande Région, ce n'est pas seulement de la politique et de la paperasse — il y a aussi une vraie culture qui y vit.")
ed("granderegion", "de", "Im Haus geht es also nicht nur um Politik und Papierkram — es lebt auch Kultur darin.",
   "In der Großregion geht es also nicht nur um Politik und Papierkram — es lebt auch echte Kultur darin.")
ed("granderegion", "lb", "Also geet et am Haus net nëmmen ëm Politik a Pabeierkrom — et lieft och Kultur dobannen.",
   "Also geet et an der Groussregioun net nëmmen ëm Politik a Pabeierkrom — et lieft och richteg Kultur dran.")
ed("granderegion", "en", "the representation of Rhineland-Palatinate and the Espace Culturel.",
   "the representation of Rhineland-Palatinate, EuRegio SaarLorLux+, QuattroPole and the Institut de la Grande Région. The University of the Greater Region (UniGR) links 7 universities (including one associated partner) with more than 141,000 students.")
ed("granderegion", "fr", "la représentation de la Rhénanie-Palatinat et l'Espace Culturel.",
   "la représentation de la Rhénanie-Palatinat, EuRegio SaarLorLux+, QuattroPole et l'Institut de la Grande Région. L'Université de la Grande Région (UniGR) relie 7 universités (dont un partenaire associé) et plus de 141 000 étudiants.")
ed("granderegion", "de", "die Vertretung von Rheinland-Pfalz und den Espace Culturel.",
   "die Vertretung von Rheinland-Pfalz, EuRegio SaarLorLux+, QuattroPole und das Institut der Großregion. Die Universität der Großregion (UniGR) verbindet 7 Universitäten (davon ein assoziierter Partner) mit mehr als 141.000 Studierenden.")
ed("granderegion", "lb", "d'Vertriedung vun der Rheinland-Pfalz an den Espace Culturel.",
   "d'Vertriedung vun der Rheinland-Pfalz, EuRegio SaarLorLux+, QuattroPole an den Institut vun der Groussregioun. D'Universitéit vun der Groussregioun (UniGR) verbënnt 7 Universitéiten (dovun ee associéierte Partner) mat méi wéi 141.000 Studenten.")

# ---------------- 13 ADEM ----------------
ed("adem", "en", "And ADEM has three locations... in Luxembourg City, in Esch-Belval, and in Diekirch. You'll be offered the office closest to your home.",
   "And you can register in person at three ADEM agencies... in Luxembourg City, in Esch-Belval, and in Diekirch. You'll be offered the one closest to your home.")
ed("adem", "fr", "Et l'ADEM a trois sites... à Luxembourg-Ville, à Esch-Belval, et à Diekirch. On vous proposera le bureau le plus proche de chez vous.",
   "Et vous pouvez vous inscrire sur place dans trois agences de l'ADEM... à Luxembourg-Ville, à Esch-Belval, et à Diekirch. On vous proposera celle qui est la plus proche de chez vous.")
ed("adem", "de", "Und die ADEM hat drei Standorte... in Luxemburg-Stadt, in Esch-Belval und in Diekirch. Man wird Ihnen das Büro anbieten, das Ihrem Wohnort am nächsten liegt.",
   "Und persönlich anmelden können Sie sich in drei Agenturen der ADEM... in Luxemburg-Stadt, in Esch-Belval und in Diekirch. Man wird Ihnen die Agentur anbieten, die Ihrem Wohnort am nächsten liegt.")
ed("adem", "lb", "An d'ADEM huet dräi Standuerter... an der Stad Lëtzebuerg, zu Esch-Belval, an zu Diekirch. Dir kritt de Büro proposéiert, dee bei Iech doheem am nootste läit.",
   "An Dir kënnt Iech perséinlech an dräi Agencë vun der ADEM aschreiwen... an der Stad Lëtzebuerg, zu Esch-Belval, an zu Diekirch. Dir kritt déi proposéiert, déi bei Iech doheem am nootste läit.")
ed("adem", "en", "aged fifteen to thirty", "aged sixteen to thirty")
ed("adem", "fr", "âgé de quinze à trente ans", "âgé de seize à trente ans")
ed("adem", "de", "im Alter von fünfzehn bis dreißig Jahren", "im Alter von sechzehn bis dreißig Jahren")
ed("adem", "lb", "am Alter vu fofzéng bis drësseg", "am Alter vu siechzéng bis drësseg")
ed("adem", "en", "That helps companies here find talent, and helps people abroad discover opportunities in the country.",
   "And since 2026 there's even a national website, workinluxembourg.com. It helps companies here find talent, and helps people abroad discover opportunities in the country.")
ed("adem", "fr", "Cela aide les entreprises d'ici à trouver des talents, et aide les personnes à l'étranger à découvrir des opportunités dans le pays.",
   "Et depuis 2026, il y a même un site national, workinluxembourg.com. Il aide les entreprises d'ici à trouver des talents, et aide les personnes à l'étranger à découvrir des opportunités dans le pays.")
ed("adem", "de", "Das hilft Unternehmen hier, Talente zu finden, und hilft Menschen im Ausland, Chancen im Land zu entdecken.",
   "Und seit 2026 gibt es sogar eine nationale Website, workinluxembourg.com. Sie hilft Unternehmen hier, Talente zu finden, und hilft Menschen im Ausland, Chancen im Land zu entdecken.")
ed("adem", "lb", "Dee hëlleft de Firmen hei, Talenter ze fannen, an hëlleft de Leit am Ausland, Méiglechkeeten am Land z'entdecken.",
   "An zënter 2026 gëtt et souguer eng national Websäit, workinluxembourg.com. Si hëlleft de Firmen hei, Talenter ze fannen, an hëlleft de Leit am Ausland, Méiglechkeeten am Land z'entdecken.")


def path(key, lang):
    return os.path.join(ROOT, "podcast_script_%s%s.md" % (key, "" if lang == "en" else "_" + lang))


def main(write):
    texts, problems, applied, skipped = {}, [], 0, 0
    for key, lang, old, new in E:
        p = path(key, lang)
        t = texts.setdefault(p, open(p, encoding="utf-8").read())
        if old.startswith(R):
            pat = re.compile(old[len(R):], re.M)
            n = len(pat.findall(t))
            if n == 0 and new in t:
                skipped += 1; continue
            if n != 1:
                problems.append("%s %s: regex matched %d times: %s" % (key, lang, n, old[:60])); continue
            t = pat.sub(lambda m: new, t, count=1)
        else:
            n = t.count(old)
            if n == 0 and new in t:
                skipped += 1; continue
            if n != 1:
                problems.append("%s %s: found %d times: %s" % (key, lang, n, old[:60])); continue
            t = t.replace(old, new, 1)
        texts[p] = t; applied += 1
    for p in problems: print("PROBLEM", p)
    print("edits: %d applied, %d already done, %d problems" % (applied, skipped, len(problems)))
    if problems:
        sys.exit(1)
    # turn counts must stay equal across languages
    for key in sorted({k for k, *_ in E}):
        counts = {}
        for lang in ("en", "fr", "de", "lb"):
            p = path(key, lang)
            t = texts.get(p) or open(p, encoding="utf-8").read()
            counts[lang] = len(re.findall(r"^\*\*(ANNA|TOM)", t, re.M))
        ok = len(set(counts.values())) == 1
        print("%-18s turns %s %s" % (key, counts, "ok" if ok else "MISMATCH"))
        if not ok:
            sys.exit(1)
    if write:
        for p, t in texts.items():
            open(p, "w", encoding="utf-8").write(t)
        print("written: %d files" % len(texts))


if __name__ == "__main__":
    main("--write" in sys.argv)
