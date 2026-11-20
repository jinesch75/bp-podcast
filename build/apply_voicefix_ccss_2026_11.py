#!/usr/bin/env python3
"""Voice fix, social security episode (20 Nov 2026): Anna's short "Quite a lot." (pitch outlier in voice_qc.py)
joined to the next sentence, EN/FR/DE/LB. Turn counts unchanged. Idempotent. Run from the project root."""
R = {"": [("Quite a lot. On the website ccss dot l-u, you find", "Quite a lot: on the website ccss dot l-u, you find")],
     "_fr": [("Beaucoup de choses. Sur le site ccss point l-u, vous trouvez", "Beaucoup de choses : sur le site ccss point l-u, vous trouvez")],
     "_de": [("Eine ganze Menge. Auf der Website ccss Punkt l-u finden Sie", "Eine ganze Menge: Auf der Website ccss Punkt l-u finden Sie")],
     "_lb": [("Eng ganz Rei Saachen. Um Site ccss Punkt l-u fannt Dir", "Eng ganz Rei Saachen: um Site ccss Punkt l-u fannt Dir")]}
for sfx, pairs in R.items():
    p = f"podcast_script_ccss{sfx}.md"; s = open(p, encoding="utf-8").read(); n = 0
    for a, b in pairs:
        if a in s: s = s.replace(a, b); n += 1
        elif b not in s: raise SystemExit(f"{p}: not found: {a[:50]}")
    open(p, "w", encoding="utf-8").write(s); print(p, n, "changed")
