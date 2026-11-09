"""Fact-check Info-Seniors (ep 10), 9 Nov 2026 — Jacques: "apply all".
1 register not yet 'complete': infosenior.public.lu says the site is completed as data arrives
2 COMPA paid by the National Solidarity Fund (FNS), for approved care homes / supervised housing (law 18.07.2025)
3 ala help line 26 432 432, 24/24 7/7 (infosenior.public.lu service sheet)
4 Red Cross service named Iris (croix-rouge.lu)
Turn counts unchanged. Idempotent."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R={
"en":[
 ("It's a complete, reliable list of the services and structures for older people in Luxembourg.","It's a reliable list of the approved services and structures for older people in Luxembourg — and it's still growing, as more services send in their information."),
 ("which even runs a help line, available around the clock,","which even runs a help line, 26 432 432, available around the clock,"),
 ("there's a service of the Red Cross, where","there's a service of the Red Cross, called Iris, where"),
 ("a scheme called COMPA helps people who don't have enough money to pay for a care home or supervised housing.","a scheme called COMPA, paid by the National Solidarity Fund, helps people who don't have enough money to pay for an approved care home or supervised housing."),
],
"fr":[
 ("C'est une liste complète et fiable des services et des structures pour les personnes âgées au Luxembourg.","C'est une liste fiable des services et des structures agréés pour les personnes âgées au Luxembourg — et elle s'agrandit encore, au fur et à mesure que les services envoient leurs informations."),
 ("qui gère même une ligne d'aide, disponible jour et nuit,","qui gère même une ligne d'aide, 26 432 432, disponible jour et nuit,"),
 ("il y a un service de la Croix-Rouge, où","il y a un service de la Croix-Rouge, appelé Iris, où"),
 ("un dispositif appelé COMPA aide les personnes qui n'ont pas assez d'argent pour payer une maison de soins ou un logement encadré.","un dispositif appelé COMPA, versé par le Fonds national de solidarité, aide les personnes qui n'ont pas assez d'argent pour payer une structure d'hébergement ou un logement encadré agréés."),
],
"de":[
 ("Es ist eine vollständige, verlässliche Liste der Dienste und Einrichtungen für ältere Menschen in Luxemburg.","Es ist eine verlässliche Liste der zugelassenen Dienste und Einrichtungen für ältere Menschen in Luxemburg — und sie wächst noch, je mehr Dienste ihre Informationen einschicken."),
 ("der sogar eine Hilfeleitung betreibt, rund um die Uhr verfügbar,","der sogar eine Hilfeleitung betreibt, 26 432 432, rund um die Uhr verfügbar,"),
 ("gibt es einen Dienst des Roten Kreuzes, bei dem","gibt es einen Dienst des Roten Kreuzes, namens Iris, bei dem"),
 ("hilft ein Programm namens COMPA Menschen, die nicht genug Geld haben, um ein Pflegeheim oder betreutes Wohnen zu bezahlen.","hilft ein Programm namens COMPA, gezahlt vom Nationalen Solidaritätsfonds, Menschen, die nicht genug Geld haben, um ein zugelassenes Pflegeheim oder betreutes Wohnen zu bezahlen."),
],
"lb":[
 ("Et ass eng komplett, zouverlässeg Lëscht vun de Servicer a Strukturen fir eeler Leit zu Lëtzebuerg.","Et ass eng zouverlässeg Lëscht vun den agreéierte Servicer a Strukturen fir eeler Leit zu Lëtzebuerg — an si gëtt nach ëmmer méi grouss, esou wéi d'Servicer hir Informatiounen aschécken."),
 ("déi souguer eng Hëllefslinn huet, rëm d'Auer disponibel,","déi souguer eng Hëllefslinn huet, 26 432 432, rëm d'Auer disponibel,"),
 ("gëtt et e Service vum Rouden Kräiz, wou","gëtt et e Service vum Rouden Kräiz, mam Numm Iris, wou"),
 ("hëlleft e System mam Numm COMPA de Leit, déi net genuch Geld hunn, fir e Fleegeheem oder e betreit Wunnen ze bezuelen.","hëlleft e System mam Numm COMPA, bezuelt vum Nationale Solidaritéitsfong, de Leit, déi net genuch Geld hunn, fir en agreéiert Fleegeheem oder e betreit Wunnen ze bezuelen."),
],
}
SRC_OLD="General information only — check infosenior.lu"
SRC_ADD="Fact-checked 9 November 2026 (infosenior.public.lu: register still being completed; COMPA under the law of 18 July 2025, paid by the FNS; ala help line 26 432 432, 24/7; Croix-Rouge Iris service). "
for lang,reps in R.items():
    p=os.path.join(ROOT,"podcast_script_infosenior"+("" if lang=="en" else "_"+lang)+".md")
    s=open(p,encoding="utf-8").read(); n0=s.count("\n**")
    for old,new in reps:
        if new in s: continue
        assert s.count(old)==1,(lang,old); s=s.replace(old,new)
    assert s.count("\n**")==n0
    if lang=="en" and SRC_ADD not in s:
        assert s.count(SRC_OLD)==1; s=s.replace(SRC_OLD,SRC_ADD+SRC_OLD)
    open(p,"w",encoding="utf-8").write(s); print("ok",lang)
