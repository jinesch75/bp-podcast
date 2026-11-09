"""Fact-check LU-Alert (ep 8), 9 Nov 2026 — Jacques: "apply all suggestions" (scripts will also be checked by the administrations).
1 sirens: warn of serious danger locally or nationwide + signals (lu-alert.lu Sirens page; overview page still says 'only nuclear')
2 app: less serious warnings in principle only via app/website; choose alerts, places of interest
3 Cell Broadcast appears even on silent, loud sound; keep phone software up to date
4 CB languages: always French + English/German if phone language
5 some tests need 'LU-Alert Test' (phone) / 'Test' (app) switched on
6 dropped 'I can't really opt out either' (not stated officially)
Turn counts unchanged. Idempotent."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R={
"en":[
 ("your phone is targeted automatically.","your phone is targeted automatically. A Cell Broadcast alert even appears when your phone is on silent — with a loud sound."),
 ("So I don't have to do anything, and I can't really opt out either.","So I don't have to do anything."),
 ("Yes, but today the sirens are used only in one specific case — a nuclear alert. For everything else, it's the phone and the other channels.",
  "Yes, the same kind. Sirens can warn the population of a serious danger — in one area, or across the whole country. A long, steady tone means: get to safety and follow the news. A rising and falling tone means: go into a solid building and close the doors and windows. But for most alerts, it's the phone and the other channels."),
 ("It's a good idea to install it.","It's a good idea to install it. Because many less serious warnings are sent only through the app and the website, not by SMS. In the app, you can also choose which alerts you want, and add places that matter to you — like your home or your children's school."),
 ("In the app, you receive the language you chose in the settings.","In the app, you receive the language you chose in the settings. With Cell Broadcast, you always get French — and also English or German, if that's your phone's language."),
 ("It's normal, don't worry.","It's normal, don't worry. And some tests on the phone only reach you if you switch on 'LU-Alert Test' in your phone's settings — or 'Test' in the app."),
 ("Two — check that your phone can receive these alerts; you can look in your phone settings, under emergency or government alerts.",
  "Two — keep your phone's software up to date, and check in your phone settings, under emergency or government alerts, that it can receive these alerts."),
 ("and, for nuclear alerts, sirens.","and, for serious danger, sirens."),
],
"fr":[
 ("votre téléphone est ciblé automatiquement.","votre téléphone est ciblé automatiquement. Une alerte Cell Broadcast s'affiche même si votre téléphone est en mode silencieux — avec un son fort."),
 ("Donc je n'ai rien à faire, et je ne peux pas vraiment m'y soustraire non plus.","Donc je n'ai rien à faire."),
 ("Oui, mais aujourd'hui les sirènes ne sont utilisées que dans un seul cas précis — une alerte nucléaire. Pour tout le reste, c'est le téléphone et les autres canaux.",
  "Oui, le même genre. Les sirènes peuvent avertir la population d'un danger grave — dans une zone, ou dans tout le pays. Un son long et continu veut dire : mettez-vous en sécurité et suivez les informations. Un son montant et descendant veut dire : entrez dans un bâtiment solide et fermez les portes et les fenêtres. Mais pour la plupart des alertes, c'est le téléphone et les autres canaux."),
 ("C'est une bonne idée de l'installer.","C'est une bonne idée de l'installer. Parce que beaucoup d'alertes moins graves sont envoyées uniquement par l'application et le site internet, pas par SMS. Dans l'application, vous pouvez aussi choisir les alertes que vous voulez, et ajouter les lieux qui comptent pour vous — comme votre domicile ou l'école de vos enfants."),
 ("Dans l'application, vous recevez la langue que vous avez choisie dans les paramètres.","Dans l'application, vous recevez la langue que vous avez choisie dans les paramètres. Par Cell Broadcast, vous recevez toujours le français — et aussi l'anglais ou l'allemand, si c'est la langue de votre téléphone."),
 ("C'est normal, pas d'inquiétude.","C'est normal, pas d'inquiétude. Et certains tests sur le téléphone ne vous arrivent que si vous activez « LU-Alert Test » dans les paramètres de votre téléphone — ou « Test » dans l'application."),
 ("Deux — vérifiez que votre téléphone peut recevoir ces alertes ; vous pouvez regarder dans les paramètres de votre téléphone, sous alertes d'urgence ou alertes gouvernementales.",
  "Deux — gardez le logiciel de votre téléphone à jour, et vérifiez dans les paramètres, sous alertes d'urgence ou alertes gouvernementales, qu'il peut recevoir ces alertes."),
 ("et, pour les alertes nucléaires, les sirènes.","et, en cas de danger grave, les sirènes."),
],
"de":[
 ("wird Ihr Telefon automatisch erreicht.","wird Ihr Telefon automatisch erreicht. Eine Cell-Broadcast-Warnung erscheint sogar, wenn Ihr Telefon stummgeschaltet ist — mit einem lauten Ton."),
 ("Ich muss also nichts tun, und ich kann mich auch nicht wirklich abmelden.","Ich muss also nichts tun."),
 ("Ja, aber heute werden die Sirenen nur noch in einem bestimmten Fall benutzt — bei einem Nuklearalarm. Für alles andere sind es das Telefon und die anderen Kanäle.",
  "Ja, die gleiche Art. Sirenen können die Bevölkerung vor einer ernsten Gefahr warnen — in einem Gebiet oder im ganzen Land. Ein langer, gleichbleibender Ton heißt: Bringen Sie sich in Sicherheit und verfolgen Sie die Nachrichten. Ein auf- und abschwellender Ton heißt: Gehen Sie in ein festes Gebäude und schließen Sie Türen und Fenster. Aber bei den meisten Warnungen sind es das Telefon und die anderen Kanäle."),
 ("Es ist eine gute Idee, sie zu installieren.","Es ist eine gute Idee, sie zu installieren. Denn viele weniger ernste Warnungen werden nur über die App und die Website verschickt, nicht per SMS. In der App können Sie auch auswählen, welche Warnungen Sie möchten, und Orte hinzufügen, die Ihnen wichtig sind — wie Ihr Zuhause oder die Schule Ihrer Kinder."),
 ("In der App erhalten Sie die Sprache, die Sie in den Einstellungen gewählt haben.","In der App erhalten Sie die Sprache, die Sie in den Einstellungen gewählt haben. Per Cell Broadcast bekommen Sie immer Französisch — und dazu Englisch oder Deutsch, wenn das die Sprache Ihres Telefons ist."),
 ("Das ist normal, keine Sorge.","Das ist normal, keine Sorge. Und manche Tests auf dem Telefon erreichen Sie nur, wenn Sie „LU-Alert Test“ in den Telefoneinstellungen einschalten — oder „Test“ in der App."),
 ("Zwei — prüfen Sie, ob Ihr Telefon diese Warnungen empfangen kann; schauen Sie in Ihren Telefoneinstellungen nach, unter Notfall- oder Behördenwarnungen.",
  "Zwei — halten Sie die Software Ihres Telefons aktuell, und prüfen Sie in den Einstellungen, unter Notfall- oder Behördenwarnungen, ob es diese Warnungen empfangen kann."),
 ("und, bei Nuklearalarm, Sirenen.","und, bei ernster Gefahr, Sirenen."),
],
"lb":[
 ("gëtt Ären Handy automatesch erreecht.","gëtt Ären Handy automatesch erreecht. Eng Cell-Broadcast-Warnung erschéngt souguer, wann Ären Handy op lautlos ass — mat engem haarden Toun."),
 ("Also muss ech näischt maachen, an ech kann mech och net wierklech ofmellen.","Also muss ech näischt maachen."),
 ("Jo, mä haut ginn d'Sirenen nëmmen an engem spezifesche Fall benotzt — bei engem Nuklearalarm. Fir alles anescht sinn et den Handy an déi aner Kanäl.",
  "Jo, déi selwecht Aart. D'Sirene kënnen d'Bevëlkerung virun enger eeschter Gefor warnen — an enger Regioun oder am ganze Land. E laangen, gläichméissegen Toun heescht: bréngt Iech a Sécherheet a verfollegt d'Noriichten. En op- an ofschwellenden Toun heescht: gitt an e feste Gebai a maacht Dieren a Fënsteren zou. Mä fir déi meescht Alarmer sinn et den Handy an déi aner Kanäl."),
 ("Et ass eng gutt Iddi, se z'installéieren.","Et ass eng gutt Iddi, se z'installéieren. Well vill manner eescht Warnungen nëmmen iwwer d'App an d'Websäit verschéckt ginn, net per SMS. An der App kënnt Dir och auswielen, wéi eng Alarmer Dir wëllt, a Plazen derbäisetzen, déi Iech wichteg sinn — wéi Äert Doheem oder d'Schoul vun Äre Kanner."),
 ("An der App kritt Dir déi Sprooch, déi Dir an den Astellunge gewielt hutt.","An der App kritt Dir déi Sprooch, déi Dir an den Astellunge gewielt hutt. Per Cell Broadcast kritt Dir ëmmer Franséisch — an och Englesch oder Däitsch, wann dat d'Sprooch vun Ärem Handy ass."),
 ("Dat ass normal, keng Suerg.","Dat ass normal, keng Suerg. A verschidden Tester um Handy kritt Dir nëmmen, wann Dir \"LU-Alert Test\" an den Handy-Astellungen aschalt — oder \"Test\" an der App."),
 ("Zwee — kuckt no, ob Ären Handy dës Alarmer empfänke kann; Dir kënnt an den Handy-Astellunge kucken, ënner Noutfall- oder Regierungsalarmer.",
  "Zwee — haalt d'Software vun Ärem Handy um neiste Stand, a kuckt an den Astellungen, ënner Noutfall- oder Regierungsalarmer, ob en dës Alarmer empfänke kann."),
 ("an, bei Nuklearalarmer, d'Sirenen.","an, bei eeschter Gefor, d'Sirenen."),
],
}
SRC_OLD="General information only — always check lu-alert.lu"
SRC_ADD="Fact-checked 9 November 2026 (lu-alert.lu Sirens, Mobile app, Cell Broadcast, Mobile device setup and Testing strategy pages; the Sirens page now describes local or nationwide warnings, while the channel overview still says sirens are currently only used for a nuclear alert). "
for lang,reps in R.items():
    p=os.path.join(ROOT,"podcast_script_lualert"+("" if lang=="en" else "_"+lang)+".md")
    s=open(p,encoding="utf-8").read(); n0=s.count("\n**")
    for old,new in reps:
        if new in s: continue
        assert s.count(old)==1,(lang,old); s=s.replace(old,new)
    assert s.count("\n**")==n0
    if lang=="en" and SRC_ADD not in s:
        assert s.count(SRC_OLD)==1; s=s.replace(SRC_OLD,SRC_ADD+SRC_OLD)
    open(p,"w",encoding="utf-8").write(s); print("ok",lang)
