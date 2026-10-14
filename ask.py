"""Poser des questions depuis le terminal :  python ask.py"""
from assistant import repondre
from database import connexion

conn = connexion()
print("Pose ta question (ou tape 'quitter').")
while True:
    question = input("\n> ").strip()
    if question.lower() in {"quitter", "q", "exit"}:
        break
    if question:
        texte, _ = repondre(conn, question)
        print("\n" + texte)
