#!/usr/bin/env python3
"""Fact-check FNS (9 Nov 2026): no MyGuichet for FNS procedures, durable amounts, planned complément vie chère
(bill 8716, hedged), COMPA name, maintenance-advance conditions, counter in the mornings.
EN/FR/DE/LB scripts. Idempotent. Turn counts unchanged. Run from the project root."""
import re, sys
R = {}
R[""] = [
 ("Right now it's roughly between one thousand eight hundred euros for a single person, up to around three thousand six hundred for a large household, each year.",
  "For a single person, it's more than one thousand eight hundred euros a year — and more for bigger households."),
 ("Right. For everyone else, you apply each year. For the year twenty twenty-six, for example, you can apply across the whole year, up to the end of December. And the FNS even has",
  "Right. And there's a change coming. The government plans to merge these three helps — plus a new help for families with school children — into one single help, the complément vie chère, from 2027. Then you'd apply only once, and it would continue as long as you qualify. The law is still being discussed in Parliament, so check f-n-s dot l-u for the latest. For now, everyone else applies with a form — and if you got it last year, the FNS sends you a pre-filled one at the end of the year. And the FNS even has"),
 ("to recover the money.", "to recover the money. To ask for it, you need a court decision that sets the support — and a bailiff must first have tried to collect it."),
 ("the FNS can help pay the difference.", "the FNS can help pay the difference. It's called COMPA."),
 ("For several things, yes — through MyGuichet.lu, the State's digital platform, with a secure login. And for the cost-of-living allowance, there's that online calculator first. But you can also do it on paper — download the form, or get it by post, fill it in, and send it back to the FNS.",
  "Partly. On the website you find the forms — and, for the cost-of-living allowance, that online calculator. But mostly, you fill in a paper form. You download it, or pick it up at the FNS counter, sign it, and send it by post or hand it in. And the social office of your commune can help you fill it in."),
 ("on the rue de la Fonderie, in Luxembourg City.", "on the rue de la Fonderie, in Luxembourg City — the counter is open in the mornings."),
 ("You apply on fns.lu or MyGuichet.lu — and REVIS recipients", "You find all the forms on fns.lu — and REVIS recipients"),
]
R["_fr"] = [
 ("En ce moment, c'est à peu près entre mille huit cents euros pour une personne seule, jusqu'à environ trois mille six cents pour un grand ménage, chaque année.",
  "Pour une personne seule, c'est plus de mille huit cents euros par an — et davantage pour les ménages plus grands."),
 ("Exact. Pour tout le monde, vous faites votre demande chaque année. Pour l'année deux mille vingt-six, par exemple, vous pouvez faire votre demande tout au long de l'année, jusqu'à la fin décembre. Et le FNS a même",
  "Exact. Et un changement se prépare. Le gouvernement prévoit de regrouper ces trois aides — plus une nouvelle aide pour les familles avec des enfants scolarisés — en une seule, le complément vie chère, à partir de 2027. Vous n'auriez alors qu'une seule demande à faire, et l'aide continuerait tant que vous y avez droit. La loi est encore en discussion à la Chambre des députés, alors consultez f-n-s point l-u pour les dernières nouvelles. Pour l'instant, les autres font leur demande avec un formulaire — et si vous l'avez reçue l'an dernier, le FNS vous envoie un formulaire pré-rempli en fin d'année. Et le FNS a même"),
 ("pour récupérer l'argent.", "pour récupérer l'argent. Pour la demander, il faut une décision de justice qui fixe la pension — et un huissier doit d'abord avoir essayé de la récupérer."),
 ("le FNS peut aider à payer la différence.", "le FNS peut aider à payer la différence. Il s'appelle le COMPA."),
 ("Pour plusieurs choses, oui — via MyGuichet.lu, la plateforme numérique de l'État, avec une connexion sécurisée. Et pour l'allocation de vie chère, il y a d'abord ce calculateur en ligne. Mais vous pouvez aussi le faire sur papier — téléchargez le formulaire, ou recevez-le par la poste, remplissez-le, et renvoyez-le au FNS.",
  "En partie. Sur le site, vous trouvez les formulaires — et, pour l'allocation de vie chère, ce calculateur en ligne. Mais la plupart du temps, vous remplissez un formulaire papier. Vous le téléchargez, ou vous le prenez au guichet du FNS, vous le signez, et vous l'envoyez par la poste ou vous le déposez. Et l'office social de votre commune peut vous aider à le remplir."),
 ("rue de la Fonderie, à Luxembourg-Ville.", "rue de la Fonderie, à Luxembourg-Ville — le guichet est ouvert le matin."),
 ("Vous faites votre demande sur fns.lu ou MyGuichet.lu — et", "Vous trouvez tous les formulaires sur fns.lu — et"),
]
R["_de"] = [
 ("Im Moment liegt er ungefähr zwischen tausendachthundert Euro für eine alleinstehende Person, bis zu rund dreitausendsechshundert für einen großen Haushalt, pro Jahr.",
  "Für eine alleinstehende Person sind es mehr als tausendachthundert Euro im Jahr — und mehr für größere Haushalte."),
 ("Richtig. Für alle anderen stellen Sie jedes Jahr einen Antrag. Für das Jahr zweitausendsechsundzwanzig zum Beispiel können Sie das ganze Jahr über einen Antrag stellen, bis Ende Dezember. Und der FNS hat sogar",
  "Richtig. Und es kommt eine Änderung. Die Regierung plant, diese drei Hilfen — plus eine neue Hilfe für Familien mit Schulkindern — ab 2027 zu einer einzigen zusammenzulegen, dem complément vie chère. Dann müssten Sie nur noch einmal einen Antrag stellen, und die Hilfe liefe weiter, solange Sie Anspruch haben. Das Gesetz wird noch im Parlament beraten — schauen Sie also auf f-n-s Punkt l-u nach dem neuesten Stand. Bis dahin stellen alle anderen ihren Antrag mit einem Formular — und wenn Sie die Zulage im letzten Jahr bekommen haben, schickt Ihnen der FNS Ende des Jahres ein vorausgefülltes Formular. Und der FNS hat sogar"),
 ("um das Geld zurückzuholen.", "um das Geld zurückzuholen. Dafür braucht es eine Gerichtsentscheidung, die den Unterhalt festlegt — und ein Gerichtsvollzieher muss zuerst versucht haben, ihn einzutreiben."),
 ("kann der FNS helfen, die Differenz zu zahlen.", "kann der FNS helfen, die Differenz zu zahlen. Er heißt COMPA."),
 ("Für mehrere Dinge, ja — über MyGuichet.lu, die digitale Plattform des Staates, mit einem sicheren Login. Und für die Teuerungszulage gibt es zuerst diesen Online-Rechner. Aber Sie können es auch auf Papier machen — laden Sie das Formular herunter, oder bekommen Sie es per Post, füllen Sie es aus, und schicken Sie es an den FNS zurück.",
  "Teilweise. Auf der Website finden Sie die Formulare — und für die Teuerungszulage diesen Online-Rechner. Aber meistens füllen Sie ein Papierformular aus. Sie laden es herunter oder holen es am Schalter des FNS ab, unterschreiben es, und schicken es per Post oder geben es dort ab. Und das Office social Ihrer Gemeinde kann Ihnen beim Ausfüllen helfen."),
 ("rue de la Fonderie, in Luxemburg-Stadt.", "rue de la Fonderie, in Luxemburg-Stadt — der Schalter ist vormittags geöffnet."),
 ("Sie stellen Ihren Antrag auf fns.lu oder MyGuichet.lu — und", "Alle Formulare finden Sie auf fns.lu — und"),
]
R["_lb"] = [
 ("Am Moment ass et ongeféier tëscht dausendaachthonnert Euro fir eng eenzel Persoun, bis ëm déi dräidausendsechshonnert fir e groussen Stot, all Joer.",
  "Fir eng eenzel Persoun sinn et méi wéi dausendaachthonnert Euro d'Joer — a méi fir méi grouss Stéit."),
 ("Richteg. Fir all déi aner mécht Dir all Joer eng Demande. Fir d'Joer zweedausendsechsanzwanzeg zum Beispill, kënnt Dir iwwert dat ganzt Joer hi eng Demande maachen, bis Enn Dezember. An de FNS huet souguer",
  "Richteg. An et kënnt eng Ännerung. D'Regierung plangt, dës dräi Hëllefen — plus eng nei Hëllef fir Famillje mat Schoulkanner — ab 2027 zu enger eenzeger zesummenzeleeën, dem complément vie chère. Da misst Dir nëmmen nach eng Kéier eng Demande maachen, an d'Hëllef géif weidergoen, soulaang wéi Dir en Usproch hutt. D'Gesetz gëtt nach an der Chamber diskutéiert — kuckt also op f-n-s Punkt l-u fir déi neist Informatiounen. Bis dohin maachen all déi aner eng Demande mat engem Formulaire — a wann Dir se d'lescht Joer kritt hutt, schéckt de FNS Iech um Enn vum Joer e virausgefëllte Formulaire. An de FNS huet souguer"),
 ("fir d'Geld erëmzekréien.", "fir d'Geld erëmzekréien. Dofir brauch een eng Geriichtsentscheedung, déi den Ënnerhalt festleet — an en Huissier muss fir d'éischt probéiert hunn, en anzedreiwen."),
 ("da kann de FNS hëllefen, den Ënnerscheed ze bezuelen.", "da kann de FNS hëllefen, den Ënnerscheed ze bezuelen. Et heescht COMPA."),
 ("Fir verschidde Saachen, jo — iwwer MyGuichet.lu, déi digital Plattform vum Staat, mat engem séchere Login. A fir d'Liewensdeierungszoulag gëtt et fir d'éischt deen Rechner um Internet. Awer Dir kënnt et och op Pabeier maachen — den Formulaire eroflueden, oder en iwwert d'Post kréien, en ausfëllen, an en zréck un de FNS schécken.",
  "Deelweis. Um Internetsite fannt Dir d'Formulairen — a fir d'Liewensdeierungszoulag dee Rechner um Internet. Mee meeschtens fëllt Dir e Pabeierformulaire aus. Dir luet en erof, oder huelt en um Guichet vum FNS, ënnerschreift en, a schéckt en per Post oder gitt en do of. An den Office social vun Ärer Gemeng kann Iech hëllefen, en auszefëllen."),
 ("rue de la Fonderie, an der Stad Lëtzebuerg.", "rue de la Fonderie, an der Stad Lëtzebuerg — de Guichet ass moies op."),
 ("Dir maacht eng Demande op fns.lu oder MyGuichet.lu — an", "All d'Formulairen fannt Dir op fns.lu — an"),
]
NOTE = {
 "": " Planned 'complément vie chère' (bill 8716, still in committee on 9 November 2026, planned start 1 January 2027) would merge the cost-of-living allowance, energy premium, senior aid and the low-income school subsidy into one aid managed by the FNS. FNS applications are made on paper (by post or at the counter at 8-10, rue de la Fonderie), not on MyGuichet.lu. Fact-checked 9 November 2026.",
 "_fr": " Le « complément vie chère » prévu (projet de loi 8716, encore en commission le 9 novembre 2026, début prévu le 1er janvier 2027) regrouperait l'allocation de vie chère, la prime énergie, l'aide aux personnes âgées et la subvention pour ménages à faible revenu en une aide gérée par le FNS. Les demandes au FNS se font sur papier (par la poste ou au guichet, 8-10, rue de la Fonderie). Vérifié le 9 novembre 2026.",
 "_de": " Der geplante „complément vie chère“ (Gesetzentwurf 8716, am 9. November 2026 noch im Ausschuss, geplanter Start 1. Januar 2027) würde Teuerungszulage, Energieprämie, Seniorenhilfe und den Zuschuss für Haushalte mit geringem Einkommen zu einer Hilfe des FNS zusammenlegen. Anträge beim FNS auf Papier (per Post oder am Schalter, 8-10, rue de la Fonderie). Geprüft am 9. November 2026.",
 "_lb": " De geplangte „complément vie chère“ (Gesetzesprojet 8716, den 9. November 2026 nach an der Kommissioun, geplangte Start 1. Januar 2027) géif Liewensdeierungszoulag, prime énergie, Senioren-Hëllef an d'Subventioun fir Stéit mat klengem Akommes zesummeleeën. Demanden beim FNS op Pabeier (per Post oder um Guichet). Iwwerpréift den 9. November 2026.",
}
write = "--dry" not in sys.argv
for L, pairs in R.items():
    p = f"podcast_script_fns{L}.md"
    s = open(p, encoding="utf-8").read()
    n0 = len(re.findall(r"^\*\*(ANNA|TOM)\s?:\*\*", s, re.M)); done = 0
    for old, new in pairs:
        if new in s: continue
        c = s.count(old)
        if c != 1: sys.exit(f"{p}: expected 1 match, got {c}: {old[:60]}")
        s = s.replace(old, new); done += 1
    if "8716" not in s:
        m = list(re.finditer(r"\*\s*$", s))
        if not m: sys.exit(f"{p}: footer end not found")
        e = m[-1].start(); s = s[:e].rstrip() + NOTE[L] + s[e:]; done += 1
    n1 = len(re.findall(r"^\*\*(ANNA|TOM)\s?:\*\*", s, re.M)); assert n0 == n1
    print(p, "changes:", done, "turns:", n1)
    if write: open(p, "w", encoding="utf-8").write(s)
