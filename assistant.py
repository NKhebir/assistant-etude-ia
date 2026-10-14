"""Le cœur du projet : ajouter des notes et répondre aux questions (étapes 1 à 6)."""
import os

from config import MODELE_GENERATION, NB_EXTRAITS, client_gemini
from database import chercher, remplacer_source
from embeddings import vectoriser_documents, vectoriser_question
from pdf_reader import pdf_en_morceaux

CONSIGNE = """Tu es un assistant d'étude. Réponds à la question en français,
en utilisant SEULEMENT les extraits de notes ci-dessous.
Après chaque information, indique sa source entre crochets, par exemple [notes.pdf, p. 3].
Si la réponse n'est pas dans les extraits, dis-le clairement au lieu d'inventer.

Extraits :
{extraits}

Question : {question}
"""


def ajouter_document(conn, chemin, nom_source=None):
    """Lit un PDF, le découpe, le transforme en embeddings et le range dans la base."""
    nom_source = nom_source or os.path.basename(chemin)
    morceaux = pdf_en_morceaux(chemin, nom_source)
    if not morceaux:
        return 0  # PDF vide ou scanné (image) : pas de texte à lire
    vecteurs = vectoriser_documents([m["contenu"] for m in morceaux])
    remplacer_source(conn, nom_source, morceaux, vecteurs)
    return len(morceaux)


def repondre(conn, question):
    """Cherche les passages utiles dans les notes, puis demande à Gemini d'y répondre."""
    extraits = chercher(conn, vectoriser_question(question), NB_EXTRAITS)
    if not extraits:
        return "Aucune note dans la base. Ajoute d'abord un PDF.", []

    texte_extraits = "\n\n".join(
        f"[{e['source']}, p. {e['page']}]\n{e['contenu']}" for e in extraits
    )
    reponse = client_gemini().models.generate_content(
        model=MODELE_GENERATION,
        contents=CONSIGNE.format(extraits=texte_extraits, question=question),
    )
    return reponse.text, extraits
