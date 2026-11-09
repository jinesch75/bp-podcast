"""Fact-check Maison de l'Orientation (ep 9), 9 Nov 2026 — Jacques: "apply all suggestions".
1 hours 10:00-17:00 (Espace conseil et information page, 31.08.2026; general page 22.01.2026 still says 8-17 — flag for review)
2 email info@maison-orientation.public.lu (only address listed now)
3 website has a dash: maison-orientation.public.lu
4 coaching: up to 22, LU/FR/DE/EN, in person or online via MyGuichet.lu, confidential
5 event examples from the current agenda (CV, job interview, studying abroad, trades)
Turn counts unchanged. Idempotent."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R={
"en":[
 ("from 8 in the morning to 5 in the afternoon.","from 10 in the morning to 5 in the afternoon."),
 ("and an email, info at m-o dot l-u.","and an email: info, at, maison dash orientation dot public dot l-u."),
 ("This one is for students, it's voluntary, and for this you do need an appointment.",
  "It's voluntary, and for this you do need an appointment, on MyGuichet.lu — in person or online. It's for young people up to 22, it's confidential, and it's offered in Luxembourgish, French, German or English."),
 ("The website is maison-orientation, all one word, dot public dot l-u.","The website is maison, dash, orientation, dot public dot l-u."),
 ("For example, workshops on how to write a CV — they even have one on making a video CV. Information evenings about studying and working abroad. And sessions for the parents of future apprentices.",
  "For example, workshops on writing a CV or preparing for a job interview. Information sessions about studying abroad. And events to discover different trades."),
 ("Monday to Friday, between 8 and 5,","Monday to Friday, between 10 and 5,"),
],
"fr":[
 ("de 8 heures du matin à 5 heures de l'après-midi.","de 10 heures du matin à 5 heures de l'après-midi."),
 ("et une adresse e-mail, info arobase m-o point l-u.","et une adresse e-mail : info, arobase, maison tiret orientation point public point l-u."),
 ("Celui-ci est pour les élèves, c'est volontaire, et là, il faut un rendez-vous.",
  "C'est volontaire, et là, il faut un rendez-vous, sur MyGuichet.lu — sur place ou en ligne. C'est pour les jeunes jusqu'à 22 ans, c'est confidentiel, et ça se fait en luxembourgeois, en français, en allemand ou en anglais."),
 ("Le site, c'est maison-orientation, tout en un seul mot, point public point l-u.","Le site, c'est maison, tiret, orientation, point public point l-u."),
 ("Par exemple, des ateliers sur comment rédiger un CV — ils en ont même un sur la réalisation d'un CV vidéo. Des soirées d'information sur les études et le travail à l'étranger. Et des séances pour les parents des futurs apprentis.",
  "Par exemple, des ateliers pour rédiger un CV ou préparer un entretien d'embauche. Des séances d'information sur les études à l'étranger. Et des événements pour découvrir différents métiers."),
 ("du lundi au vendredi, entre 8 et 5 heures,","du lundi au vendredi, entre 10 et 5 heures,"),
],
"de":[
 ("von 8 Uhr morgens bis 5 Uhr nachmittags.","von 10 Uhr morgens bis 5 Uhr nachmittags."),
 ("und eine E-Mail-Adresse, info at m-o Punkt l-u.","und eine E-Mail-Adresse: info, at, maison Bindestrich orientation Punkt public Punkt l-u."),
 ("Diese ist für Schüler, sie ist freiwillig, und dafür brauchen Sie tatsächlich einen Termin.",
  "Sie ist freiwillig, und dafür brauchen Sie einen Termin, über MyGuichet.lu — vor Ort oder online. Sie ist für junge Menschen bis 22, vertraulich, und wird auf Luxemburgisch, Französisch, Deutsch oder Englisch angeboten."),
 ("Die Website ist maison-orientation, alles in einem Wort, Punkt public Punkt l-u.","Die Website ist maison, Bindestrich, orientation, Punkt public Punkt l-u."),
 ("Zum Beispiel Workshops dazu, wie man einen Lebenslauf schreibt — sie haben sogar einen über das Erstellen eines Video-Lebenslaufs. Informationsabende über das Studieren und Arbeiten im Ausland. Und Sitzungen für die Eltern künftiger Auszubildender.",
  "Zum Beispiel Workshops zum Schreiben eines Lebenslaufs oder zur Vorbereitung auf ein Vorstellungsgespräch. Informationsveranstaltungen über das Studium im Ausland. Und Veranstaltungen, um verschiedene Berufe zu entdecken."),
 ("von Montag bis Freitag, zwischen 8 und 5 Uhr,","von Montag bis Freitag, zwischen 10 und 5 Uhr,"),
],
"lb":[
 ("vun 8 Auer moies bis 5 Auer nomëttes.","vun 10 Auer moies bis 5 Auer nomëttes."),
 ("an eng E-Mail, info at m-o Punkt l-u.","an eng E-Mail: info, at, maison Bindestrich orientation Punkt public Punkt l-u."),
 ("Deen hei ass fir Schüler, en ass fräiwëlleg, an heifir braucht Dir e Rendez-vous.",
  "En ass fräiwëlleg, an heifir braucht Dir e Rendez-vous, iwwer MyGuichet.lu — virun Uert oder online. En ass fir jonk Leit bis 22, vertraulech, a gëtt op Lëtzebuergesch, Franséisch, Däitsch oder Englesch ugebueden."),
 ("D'Websäit ass maison-orientation, alles ee Wuert, Punkt public Punkt l-u.","D'Websäit ass maison, Bindestrich, orientation, Punkt public Punkt l-u."),
 ("Zum Beispill, Workshoppen iwwer wéi een e CV schreift — si hunn esouguer een iwwer e Video-CV ze maachen. Informatiounsowender iwwer studéieren a schaffen am Ausland. A Sëtzunge fir d'Eltere vun zukünftege Léierjongen.",
  "Zum Beispill Workshoppen, fir e CV ze schreiwen oder sech op en Entretien d'embauche virzebereeden. Informatiounsversammlungen iwwer d'Studien am Ausland. An Evenementer, fir verschidde Beruffer z'entdecken."),
 ("vu méindes bis freides, tëschent 8 an 5,","vu méindes bis freides, tëschent 10 an 5,"),
],
}
SRC_OLD="General information only — check the official website"
SRC_ADD="Fact-checked 9 November 2026: Espace conseil et information page (31.08.2026: Monday–Friday 10:00–17:00; the general page of 22.01.2026 still says 8:00–17:00), e-mail info@maison-orientation.public.lu, coaching page (up to 22, LU/FR/DE/EN, in person or online, confidential), agenda. "
for lang,reps in R.items():
    p=os.path.join(ROOT,"podcast_script_maison_orientation"+("" if lang=="en" else "_"+lang)+".md")
    s=open(p,encoding="utf-8").read(); n0=s.count("\n**")
    for old,new in reps:
        if new in s: continue
        assert s.count(old)==1,(lang,old); s=s.replace(old,new)
    assert s.count("\n**")==n0
    if lang=="en" and SRC_ADD not in s:
        assert s.count(SRC_OLD)==1; s=s.replace(SRC_OLD,SRC_ADD+SRC_OLD)
    open(p,"w",encoding="utf-8").write(s); print("ok",lang)
