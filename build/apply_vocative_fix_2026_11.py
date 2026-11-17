"""Hosts addressing themselves by name (Jacques, 17 Nov 2026): Tom said "So Tom, let's make it practical" in
agriculture, amenagement, cepas, cgdis, fondseuropeens; Anna said "So Anna, what is…" in demenz. The other host
answers each time, so the name is changed (Tom -> "So Anna…", Anna -> "So Tom…"); "..." after it removed.
EN/FR/DE/LB, idempotent; speakers and turn counts unchanged."""
import re, sys
TURN = re.compile(r"^\*\*(?:ANNA|TOM)\s?:\*\*", re.M)
JOBS = {"agriculture": ("TOM", "Tom", "Anna"), "amenagement": ("TOM", "Tom", "Anna"), "cepas": ("TOM", "Tom", "Anna"),
        "cgdis": ("TOM", "Tom", "Anna"), "fondseuropeens": ("TOM", "Tom", "Anna"), "demenz": ("ANNA", "Anna", "Tom")}
for key, (spk, wrong, right) in JOBS.items():
    for sfx in ("", "_fr", "_de", "_lb"):
        p = f"podcast_script_{key}{sfx}.md"; lines = open(p, encoding="utf-8").read().split("\n"); n0 = sum(1 for l in lines if TURN.match(l)); n = 0
        for k, ln in enumerate(lines):
            m = re.match(r"^(\*\*" + spk + r"\s?:\*\*\s?)(So|Alors|Also) " + wrong + r"(\.\.\.|,)\s*(.*)$", ln)
            if m:
                lines[k] = f"{m.group(1)}{m.group(2)} {right}, {m.group(4)}"; n += 1
        assert sum(1 for l in lines if TURN.match(l)) == n0
        assert not any(re.match(r"^\*\*" + spk + r"\s?:\*\*\s?(So|Alors|Also) " + wrong + r"\b", l) for l in lines)
        print(f"{p}: {n}")
        if "--dry" not in sys.argv: open(p, "w", encoding="utf-8").write("\n".join(lines))
