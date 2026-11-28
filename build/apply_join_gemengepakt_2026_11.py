#!/usr/bin/env python3
"""Joins the short lines that stayed off in every take (finish reports 28 Nov 2026, passes 1 and 2) to the next sentence, in all four languages.
Edits build/gemengepakt_src/<lang>.txt, then run: python3 build/make_scripts_gemengepakt.py"""
J = {
 "en": [
        ("Yes, you can. The commune must make sure", "Yes, you can: the commune must make sure"),
        ("And that is a real change of view. In the past,", "And that is a real change of view: in the past,"),
        ("Yes, and that is the whole point. The actions are not invented in an office: they come", "Yes, and that is the whole point: the actions are not invented in an office, they come"),
        ("a moment ago. What is that exactly?", "a moment ago: what is that exactly?"),
        ("Through a forum on living together in our communes. It meets", "Through a forum on living together in our communes: it meets")],
 "fr": [
        ("Oui, tout à fait. La commune doit veiller", "Oui, tout à fait : la commune doit veiller"),
        ("Et c'est un vrai changement de regard. Avant,", "Et c'est un vrai changement de regard : avant,"),
        ("Oui, et c'est tout le principe. Les actions ne sont pas inventées dans un bureau : elles viennent", "Oui, et c'est tout le principe : les actions ne sont pas inventées dans un bureau, elles viennent"),
        ("il y a un instant de la commission communale du vivre-ensemble. De quoi s'agit-il exactement ?", "il y a un instant de la commission communale du vivre-ensemble : de quoi s'agit-il exactement ?"),
        ("Grâce à un forum sur le vivre-ensemble dans nos communes. Il se réunit", "Grâce à un forum sur le vivre-ensemble dans nos communes : il se réunit")],
 "de": [
        ("Ja, das können Sie. Die Gemeinde muss dafür sorgen", "Ja, das können Sie: Die Gemeinde muss dafür sorgen"),
        ("Und das ist ein echter Perspektivwechsel. Früher", "Und das ist ein echter Perspektivwechsel: Früher"),
        ("Ja, und genau darum geht es. Die Aktionen werden nicht in einem Büro erfunden: Sie kommen", "Ja, und genau darum geht es: Die Aktionen werden nicht in einem Büro erfunden, sie kommen"),
        ("für das Zusammenleben erwähnt. Was ist das genau?", "für das Zusammenleben erwähnt: Was ist das genau?"),
        ("Über ein Forum zum Zusammenleben in unseren Gemeinden. Es trifft sich", "Über ein Forum zum Zusammenleben in unseren Gemeinden: Es trifft sich")],
 "lb": [
        ("Jo, dat kënnt Dir. D'Gemeng muss dofir suergen", "Jo, dat kënnt Dir: d'Gemeng muss dofir suergen"),
        ("An dat ass e richtege Perspektivwiessel. Fréier", "An dat ass e richtege Perspektivwiessel: Fréier"),
        ("Jo, an dorëm geet et. D'Aktioune ginn net an engem Büro erfonnt: se kommen", "Jo, an dorëm geet et: d'Aktioune ginn net an engem Büro erfonnt, se kommen"),
        ("fir d'Zesummeliewen ernimmt. Wat ass dat genee?", "fir d'Zesummeliewen ernimmt: wat ass dat genee?"),
        ("Iwwer de Forum fir d'Zesummeliewen an eise Gemengen. En trëfft sech", "Iwwer de Forum fir d'Zesummeliewen an eise Gemengen: en trëfft sech")],
}
for lang, pairs in J.items():
    p = f"build/gemengepakt_src/{lang}.txt"; s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        if b in s: continue
        assert a in s, (lang, a); s = s.replace(a, b, 1)
    open(p, "w", encoding="utf-8").write(s); print(lang, "ok")
