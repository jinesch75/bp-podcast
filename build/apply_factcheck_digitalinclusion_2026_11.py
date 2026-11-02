"""Fact-check Digital Inclusion (ep 5), 2 Nov 2026 — approved by Jacques.
Source: digital-inclusion.lu main application page (menu "How to apply for a free second-hand computer"):
eligibility incl. debt settlement + 'vie privée' permit; since 22.09.2025 each household member 12+ can get
their own computer (if donations allow); adults apply themselves, an adult applies for 12-18 (one minor at a time).
Waiting time: no figure (Jacques: avoid numbers that go stale) -> 'the website always shows the current waiting time'.
Donations: laptops erased/disk returned; smartphones/tablets need a factory reset first.
Open Classroom also helps with LuxTrust/MyGuichet + free scanning/printing. Removed unverified '2,000 in one year'.
Kept: 'more than ten thousand', 'refugee volunteers' (confirmed by Jacques). Turn counts unchanged. Idempotent."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R={
"en":[
 ("In a single recent year, volunteers refurbished over two thousand machines. ",""),
 ("the allocation de vie chère. Or you're a refugee — an asylum seeker, a person under temporary protection, or an unaccompanied minor. There are a few other cases too, so check the website to see if you qualify.",
  "the allocation de vie chère. Or you're in a collective debt settlement procedure. Or you have a residence permit in the 'private life' category. Or you're a refugee — an asylum seeker, a person under temporary protection, or an unaccompanied minor. Check the website to see if you qualify."),
 ("would be a real struggle. Usually, it's one laptop per household. But other members of the family can often ask for an extra computer too.",
  "would be a real struggle. And since September 2025, every member of the household aged twelve or older can get their own computer — as long as there are enough donations."),
 ("may each get a machine?","can each get a machine?"),
 ("Often, yes. The rules change from time to time, so the website explains the latest ones — and how long you might have to wait.",
  "Yes. Each adult applies for themselves, and a parent applies for the teenagers. And the website always shows the current waiting time."),
 ("It's open from half past nine to half past one.","It's open from half past nine to half past one. They'll even help you with LuxTrust and MyGuichet — and you can scan and print a few pages for free."),
 ("And she can ask whether her two teenagers can get a computer for their schoolwork too.","And she can apply for her two teenagers too, one after the other, so each of them gets a computer for school."),
 ("Just wipe your worries — they handle the data cleaning securely.","Don't worry about your data — for a laptop, they erase it securely, or they can even give you back your hard disk. For a smartphone or tablet, just do a factory reset before you bring it."),
],
"fr":[
 ("En une seule année récente, les bénévoles ont reconditionné plus de deux mille machines. ",""),
 ("l'AVC. Ou vous êtes réfugié — demandeur d'asile, personne sous protection temporaire, ou mineur non accompagné. Il existe aussi quelques autres cas, alors vérifiez sur le site si vous y avez droit.",
  "l'AVC. Ou vous bénéficiez d'une procédure de règlement collectif des dettes. Ou vous avez un titre de séjour « vie privée ». Ou vous êtes réfugié — demandeur d'asile, personne sous protection temporaire, ou mineur non accompagné. Vérifiez sur le site si vous y avez droit."),
 ("serait une vraie difficulté. En général, c'est un ordinateur portable par ménage. Mais les autres membres de la famille peuvent souvent demander un ordinateur en plus.",
  "serait une vraie difficulté. Et depuis septembre 2025, chaque membre du ménage âgé de douze ans ou plus peut recevoir son propre ordinateur — tant qu'il y a assez de dons."),
 ("peuvent peut-être avoir chacun une machine ?","peuvent avoir chacun une machine ?"),
 ("Souvent, oui. Les règles changent de temps en temps, donc le site explique les plus récentes — et combien de temps vous devrez peut-être attendre.",
  "Oui. Chaque adulte fait sa propre demande, et un parent fait la demande pour les adolescents. Et le site indique toujours le délai d'attente actuel."),
 ("C'est ouvert de neuf heures et demie à une heure et demie.","C'est ouvert de neuf heures et demie à une heure et demie. Ils vous aident même avec LuxTrust et MyGuichet — et vous pouvez scanner et imprimer quelques pages gratuitement."),
 ("Et elle peut demander si ses deux adolescents peuvent aussi obtenir un ordinateur pour leurs devoirs.","Et elle peut aussi faire une demande pour ses deux adolescents, l'un après l'autre, pour que chacun ait un ordinateur pour l'école."),
 ("Oubliez vos inquiétudes — ils s'occupent de l'effacement des données en toute sécurité.","Ne vous inquiétez pas pour vos données — pour un ordinateur portable, ils les effacent en toute sécurité, ou ils peuvent même vous rendre votre disque dur. Pour un smartphone ou une tablette, faites simplement une réinitialisation d'usine avant de l'apporter."),
],
"de":[
 ("In einem einzigen jüngeren Jahr haben Freiwillige über zweitausend Geräte wiederaufbereitet. ",""),
 ("(allocation de vie chère). Oder Sie sind ein Flüchtling — ein Asylsuchender, eine Person unter vorübergehendem Schutz oder ein unbegleiteter Minderjähriger. Es gibt auch noch einige andere Fälle, schauen Sie also auf der Website nach, ob Sie berechtigt sind.",
  "(allocation de vie chère). Oder Sie sind in einem kollektiven Schuldenregulierungsverfahren. Oder Sie haben eine Aufenthaltserlaubnis in der Kategorie „Privatleben\". Oder Sie sind ein Flüchtling — ein Asylsuchender, eine Person unter vorübergehendem Schutz oder ein unbegleiteter Minderjähriger. Schauen Sie auf der Website nach, ob Sie berechtigt sind."),
 ("eine echte Herausforderung wäre. Meistens gibt es einen Laptop pro Haushalt. Aber die anderen Familienmitglieder können oft auch einen zusätzlichen Computer beantragen.",
  "eine echte Herausforderung wäre. Und seit September 2025 kann jedes Haushaltsmitglied ab zwölf Jahren einen eigenen Computer bekommen — solange es genug Spenden gibt."),
 ("vielleicht jeweils ein Gerät bekommen?","jeweils ein Gerät bekommen?"),
 ("Oft, ja. Die Regeln ändern sich von Zeit zu Zeit, deshalb erklärt die Website die aktuellen — und wie lange Sie vielleicht warten müssen.",
  "Ja. Jeder Erwachsene stellt seinen eigenen Antrag, und ein Elternteil stellt den Antrag für die Teenager. Und die Website zeigt immer die aktuelle Wartezeit."),
 ("Geöffnet ist von halb zehn bis halb zwei.","Geöffnet ist von halb zehn bis halb zwei. Sie helfen Ihnen sogar mit LuxTrust und MyGuichet — und Sie können ein paar Seiten kostenlos scannen und drucken."),
 ("Und sie kann fragen, ob auch ihre beiden Teenager einen Computer für ihre Schularbeiten bekommen können.","Und sie kann auch für ihre beiden Teenager einen Antrag stellen, einen nach dem anderen, damit jeder einen Computer für die Schule bekommt."),
 ("Machen Sie sich keine Sorgen — sie kümmern sich sicher um die Datenlöschung.","Machen Sie sich keine Sorgen um Ihre Daten — bei einem Laptop löschen sie sie sicher, oder sie geben Ihnen sogar Ihre Festplatte zurück. Bei einem Smartphone oder Tablet machen Sie einfach vorher einen Werksreset."),
],
"lb":[
 ("An engem eenzege rezenten Joer hunn d'Benevoll iwwer zweedausend Maschinne renovéiert. ",""),
 ("(AVC). Oder du bass e Flüchtling — en Asylsicher, eng Persoun ënner temporärem Schutz, oder e mannerjäregen Onbegleeten. Et ginn nach e puer aner Fäll, also kuck um Site, ob s du berechtegt bass.",
  "(AVC). Oder du bass an enger Prozedur vu kollektiver Scholdenreegelung. Oder du hues eng Openthaltserlaabnes an der Kategorie \"vie privée\". Oder du bass e Flüchtling — en Asylsicher, eng Persoun ënner temporärem Schutz, oder e mannerjäregen Onbegleeten. Kuck um Site, ob s du berechtegt bass."),
 ("e richtege Kampf wier. Meeschtens ass et e Laptop pro Haushalt. Mä déi aner Membere vun der Famill kënnen dacks och en zousätzleche Computer froen.",
  "e richtege Kampf wier. A zënter September 2025 kann all Member vum Haushalt vun zwielef Joer un säin eegene Computer kréien — soulaang et genuch Done gëtt."),
 ("Also kéinten den Teenager","Also kënnen den Teenager"),
 ("Dacks, jo. D'Reegelen änneren sech vun Zäit zu Zäit, dofir erkläert de Site déi aktuell — a wéi laang s du eventuell muss waarden.",
  "Jo. All Erwuessenen mécht seng eege Demande, an en Elterendeel mécht d'Demande fir d'Teenager. An de Site weist ëmmer déi aktuell Waardezäit."),
 ("Et ass op vun hallwer zéng bis hallwer zwee.","Et ass op vun hallwer zéng bis hallwer zwee. Si hëllefen der souguer mat LuxTrust a MyGuichet — an du kanns e puer Säite gratis scannen an drécken."),
 ("A si ka froen, ob hir zwee Teenager och e Computer fir hir Schoulaarbecht kréie kënnen.","A si kann och fir hir zwee Teenager eng Demande maachen, een nom aneren, fir datt jidderee vun hinnen e Computer fir d'Schoul kritt."),
 ("Maach der just keng Suergen — si këmmere sech sécher ëm d'Botzen vun den Donnéeën.","Maach der keng Suergen ëm deng Donnéeën — bei engem Laptop läsche si se sécher, oder si ginn der souguer deng Festplack zréck. Bei engem Smartphone oder Tablet maach einfach virdrun e Reset op d'Fabréckastellungen."),
],
}
SRC_OLD="When checked on 30.09.2026, the site's pages differed on further cases, the number of computers per household and waiting times — check with Digital Inclusion for the current conditions."
SRC_NEW="Rechecked 02.11.2026 on the main application page (menu): conditions also include a collective debt settlement procedure and a 'vie privée' residence permit; since 22.09.2025 each household member aged 12+ can get their own computer (as long as donations allow); adults apply for themselves, an adult applies for 12–18-year-olds. Smartphones/tablets must be factory-reset before donating. Open Classroom also helps with LuxTrust and MyGuichet.lu."
for lang,reps in R.items():
    p=os.path.join(ROOT,"podcast_script_digitalinclusion"+("" if lang=="en" else "_"+lang)+".md")
    s=open(p,encoding="utf-8").read(); n0=s.count("\n**")
    for old,new in reps:
        if new and new in s: continue
        if not new and old not in s: continue
        assert s.count(old)==1,(lang,old); s=s.replace(old,new)
    assert s.count("\n**")==n0
    if lang=="en" and SRC_NEW not in s:
        assert s.count(SRC_OLD)==1; s=s.replace(SRC_OLD,SRC_NEW)
    open(p,"w",encoding="utf-8").write(s); print("ok",lang)
