"""Ajouter des PDF depuis le terminal :  python ingest.py notes/MAT145.pdf notes/LOG320.pdf"""
import sys

from assistant import ajouter_document
from database import connexion

if len(sys.argv) < 2:
    print("Utilisation : python ingest.py fichier1.pdf [fichier2.pdf ...]")
    sys.exit(1)

conn = connexion()
for chemin in sys.argv[1:]:
    n = ajouter_document(conn, chemin)
    print(f"{chemin} : {n} morceaux ajoutés" if n else f"{chemin} : aucun texte trouvé (PDF scanné ?)")
