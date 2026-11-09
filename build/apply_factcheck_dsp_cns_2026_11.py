"""Fact-check Your health / DSP & CNS (ep 7), 9 Nov 2026 — Jacques: "apply all suggestions".
1 'about half of doctors' -> 'more and more doctors and dentists' (no stale figures; CNS PID page 26.10.2026)
2 eSanté activation on MyGuichet.lu web + app with LuxTrust or Luxembourg eID, no postal code; otherwise eSanté portal / MyDSP;
  DSP opens in the MyGuichet eSpace (guichet.lu DSP page 26.05.2026; gouvernement.lu 01.12.2025)
3 'hide documents' -> block access to certain documents; close DSP any time (guichet.lu)
4 organ donation wishes in the DSP (esante.lu, 16.10.2026)
5 no stamp needed from inside Luxembourg; CNS letterboxes (guichet.lu; cns.public.lu)
6 children under 18 usually pay nothing for doctor visits (CNS PID page)
Turn counts unchanged. Idempotent."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R={
"en":[
 ("because the result is already there.","because the result is already there. You can even write down your wishes about organ donation in it."),
 ("You can even hide certain documents if you want.","You can even block access to certain documents — and you can close your DSP at any time."),
 ("you activate your \"eSanté account\". And you can do that directly through MyGuichet.lu.",
  "you activate your \"eSanté account\". With LuxTrust or a Luxembourg ID card, you can do that in a few clicks on MyGuichet.lu — on the website or in the app — without waiting for a code by post. Otherwise, you can activate it on the eSanté portal or in the MyDSP app."),
 ("You log in to your DSP online, through the eSanté portal. And there's also a mobile app",
  "Then you can open your DSP right in your MyGuichet eSpace, or on the eSanté portal. And there's also a mobile app"),
 ("But today, about half of doctors use","But today, more and more doctors and dentists use"),
 ("So you carry a small part yourself, and the rest comes back to you.","So you carry a small part yourself, and the rest comes back to you. And for children under eighteen, there's usually nothing to pay at all."),
 ("You can send it by post, or drop it in one of their boxes.","You can send it by post — from inside Luxembourg, you don't even need a stamp — or drop it in one of their letterboxes."),
],
"fr":[
 ("parce que le résultat est déjà là.","parce que le résultat est déjà là. Vous pouvez même y noter vos souhaits concernant le don d'organes."),
 ("Vous pouvez même masquer certains documents si vous le souhaitez.","Vous pouvez même bloquer l'accès à certains documents — et vous pouvez fermer votre DSP à tout moment."),
 ("vous activez votre « compte eSanté ». Et vous pouvez le faire directement via MyGuichet.lu.",
  "vous activez votre « compte eSanté ». Avec LuxTrust ou une carte d'identité luxembourgeoise, vous pouvez le faire en quelques clics sur MyGuichet.lu — sur le site ou dans l'application — sans attendre un code par la poste. Sinon, vous pouvez l'activer sur le portail eSanté ou dans l'application MyDSP."),
 ("Vous vous connectez à votre DSP en ligne, via le portail eSanté. Et il y a aussi une application mobile",
  "Ensuite, vous pouvez ouvrir votre DSP directement dans votre eSpace MyGuichet, ou sur le portail eSanté. Et il y a aussi une application mobile"),
 ("Mais aujourd'hui, environ la moitié des médecins utilisent","Mais aujourd'hui, de plus en plus de médecins et de dentistes utilisent"),
 ("Donc vous supportez une petite partie vous-même, et le reste vous revient.","Donc vous supportez une petite partie vous-même, et le reste vous revient. Et pour les enfants de moins de dix-huit ans, il n'y a en général rien à payer."),
 ("Vous pouvez l'envoyer par la poste, ou la déposer dans une de leurs boîtes.","Vous pouvez l'envoyer par la poste — depuis le Luxembourg, vous n'avez même pas besoin de timbre — ou la déposer dans une de leurs boîtes aux lettres."),
],
"de":[
 ("weil das Ergebnis schon da ist.","weil das Ergebnis schon da ist. Sie können darin sogar Ihre Wünsche zur Organspende festhalten."),
 ("Sie können sogar bestimmte Dokumente verbergen, wenn Sie möchten.","Sie können sogar den Zugang zu bestimmten Dokumenten sperren — und Sie können Ihr DSP jederzeit schließen."),
 ("aktivieren Sie Ihr „eSanté-Konto“. Und das können Sie direkt über MyGuichet.lu machen.",
  "aktivieren Sie Ihr „eSanté-Konto“. Mit LuxTrust oder einem luxemburgischen Personalausweis geht das mit ein paar Klicks auf MyGuichet.lu — auf der Website oder in der App — ohne auf einen Code per Post zu warten. Sonst können Sie es auf dem eSanté-Portal oder in der App MyDSP aktivieren."),
 ("Sie melden sich online bei Ihrem DSP an, über das eSanté-Portal. Und es gibt auch eine mobile App",
  "Dann können Sie Ihr DSP direkt in Ihrem MyGuichet-eSpace öffnen, oder auf dem eSanté-Portal. Und es gibt auch eine mobile App"),
 ("Aber heute nutzt etwa die Hälfte der Ärzte","Aber heute nutzen immer mehr Ärzte und Zahnärzte"),
 ("Sie tragen also einen kleinen Teil selbst, und der Rest kommt zu Ihnen zurück.","Sie tragen also einen kleinen Teil selbst, und der Rest kommt zu Ihnen zurück. Und für Kinder unter achtzehn gibt es meistens gar nichts zu zahlen."),
 ("Sie können sie per Post schicken, oder in einen ihrer Briefkästen werfen.","Sie können sie per Post schicken — innerhalb Luxemburgs brauchen Sie nicht einmal eine Briefmarke — oder in einen ihrer Briefkästen werfen."),
],
"lb":[
 ("well d'Resultat schonn do ass.","well d'Resultat schonn do ass. Dir kënnt do souguer Är Wënsch zum Don vun Organer festhalen."),
 ("Dir kënnt souguer verschidde Dokumenter verstoppen, wann Dir wëllt.","Dir kënnt souguer den Zougang zu verschiddenen Dokumenter spären — an Dir kënnt Ären DSP zu all Moment zoumaachen."),
 ("aktivéiert Dir Ären \"eSanté-Kont\". An dat kënnt Dir direkt iwwer MyGuichet.lu maachen.",
  "aktivéiert Dir Ären \"eSanté-Kont\". Mat LuxTrust oder enger Lëtzebuerger Identitéitskaart geet dat mat e puer Klicken op MyGuichet.lu — op der Websäit oder an der App — ouni op e Code mat der Post ze waarden. Soss kënnt Dir en um eSanté-Portal oder an der App MyDSP aktivéieren."),
 ("Dir loggt Iech online an Ären DSP an, iwwer den eSanté-Portal. An et gëtt och eng mobil App",
  "Da kënnt Dir Ären DSP direkt an Ärem MyGuichet-eSpace opmaachen, oder um eSanté-Portal. An et gëtt och eng mobil App"),
 ("Mä haut benotzt ongeféier d'Hallschent vun den Dokteren den","Mä haut benotze ëmmer méi Dokteren an Zänndokteren den"),
 ("Also drot Dir e klengen Deel selwer, an de Rescht kënnt bei Iech zeréck.","Also drot Dir e klengen Deel selwer, an de Rescht kënnt bei Iech zeréck. A fir Kanner ënner uechtzéng ass meeschtens guer näischt ze bezuelen."),
 ("Dir kënnt se mat der Post schécken, oder an eng vun hire Boîten deposéieren.","Dir kënnt se mat der Post schécken — bannent Lëtzebuerg braucht Dir net emol eng Timber — oder an eng vun hire Bréifkëschten deposéieren."),
],
}
SRC_OLD="General information, not medical or financial advice"
SRC_ADD="Fact-checked 9 November 2026: guichet.public.lu DSP page (26.05.2026: activation on MyGuichet.lu web/app with LuxTrust or Luxembourg eID; DSP in the MyGuichet eSpace), cns.public.lu (PID 26.10.2026, digitised invoices 01.09.2026), esante.lu (organ donation wishes in the DSP). "
for lang,reps in R.items():
    p=os.path.join(ROOT,"podcast_script_dsp_cns"+("" if lang=="en" else "_"+lang)+".md")
    s=open(p,encoding="utf-8").read(); n0=s.count("\n**")
    for old,new in reps:
        if new in s: continue
        assert s.count(old)==1,(lang,old); s=s.replace(old,new)
    assert s.count("\n**")==n0
    if lang=="en" and SRC_ADD not in s:
        assert s.count(SRC_OLD)==1; s=s.replace(SRC_OLD,SRC_ADD+SRC_OLD)
    open(p,"w",encoding="utf-8").write(s); print("ok",lang)
