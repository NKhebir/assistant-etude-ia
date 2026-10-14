"""Étape 3 : transformer du texte en embeddings (listes de nombres qui représentent le sens)."""
import numpy as np
from google.genai import types

from config import DIMENSION, MODELE_EMBEDDING, client_gemini


def _vectoriser(textes, type_tache):
    vecteurs = []
    # On envoie les textes par paquets de 50 pour ne pas faire une requête trop grosse.
    for i in range(0, len(textes), 50):
        paquet = textes[i : i + 50]
        reponse = client_gemini().models.embed_content(
            model=MODELE_EMBEDDING,
            contents=paquet,
            config=types.EmbedContentConfig(
                task_type=type_tache, output_dimensionality=DIMENSION
            ),
        )
        for e in reponse.embeddings:
            v = np.array(e.values, dtype=np.float32)
            vecteurs.append(v / np.linalg.norm(v))  # on "normalise" : longueur 1, pour bien comparer
    return vecteurs


def vectoriser_documents(textes):
    """Pour les morceaux de notes qu'on range dans la base."""
    return _vectoriser(textes, "RETRIEVAL_DOCUMENT")


def vectoriser_question(question):
    """Pour la question de l'utilisatrice."""
    return _vectoriser([question], "RETRIEVAL_QUERY")[0]
