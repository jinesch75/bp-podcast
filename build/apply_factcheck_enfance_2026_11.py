#!/usr/bin/env python3
"""Fact-check Office national de l'enfance (9 Nov 2026): bill 7994 (aid, support and protection for minors, young
adults and families) still in Parliament -> hedged mention; rest confirmed (14 regional offices, voluntary approach)."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from lib_factcheck import apply
C = {
57: {"en": "And the ONE's whole approach is built on respect and collaboration. A big reform of child and youth protection is being discussed in Parliament, and it keeps this voluntary approach first, with the ONE at its centre.",
     "fr": "Et toute l'approche de l'ONE repose sur le respect et la collaboration. Une grande réforme de la protection de l'enfance et de la jeunesse est en discussion à la Chambre des députés, et elle garde cette approche volontaire en premier, avec l'ONE au centre.",
     "de": "Und der ganze Ansatz des ONE beruht auf Respekt und Zusammenarbeit. Eine große Reform des Kinder- und Jugendschutzes wird im Parlament beraten, und sie stellt diesen freiwilligen Ansatz an die erste Stelle, mit dem ONE im Mittelpunkt.",
     "lb": "An déi ganz Approche vum ONE baséiert op Respekt a Zesummenaarbecht. Eng grouss Reform vum Kanner- a Jugendschutz gëtt an der Chamber diskutéiert, a si stellt dës fräiwëlleg Approche op déi éischt Plaz, mam ONE an der Mëtt."},
}
N = {"en": "Update: bill 7994 'portant aide, soutien et protection aux mineurs, aux jeunes adultes et aux familles' (reform of youth protection, voluntary procedure first, measures set up by the ONE) still in Parliament (Council of State complementary opinion 17.07.2026). ONE created by the law of 16 December 2008; fourteen regional offices confirmed (officenationalenfance.lu). Fact-checked 9 November 2026.",
     "fr": "Mise à jour : projet de loi 7994 portant aide, soutien et protection aux mineurs, aux jeunes adultes et aux familles encore en discussion (avis complémentaire du Conseil d'État du 17.07.2026) ; quatorze offices régionaux confirmés. Vérifié le 9 novembre 2026.",
     "de": "Aktualisierung: Gesetzentwurf 7994 (Hilfe, Unterstützung und Schutz für Minderjährige, junge Erwachsene und Familien) noch im Parlament (ergänzendes Gutachten des Staatsrats vom 17.07.2026); vierzehn Regionalbüros bestätigt. Geprüft am 9. November 2026.",
     "lb": "Aktualiséierung: Gesetzesprojet 7994 nach an der Chamber; véierzéng regional Büroen confirméiert. Iwwerpréift den 9. November 2026."}
apply("enfance", C, N)
