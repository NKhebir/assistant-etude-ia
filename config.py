"""Réglages du projet : lus depuis le fichier .env."""
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()  # lit le fichier .env et met ses valeurs dans les variables d'environnement

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://rag:rag@localhost:5432/rag")
MODELE_GENERATION = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")      # le modèle qui écrit la réponse
MODELE_EMBEDDING = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")  # le modèle qui transforme le texte en nombres
DIMENSION = 768      # longueur de chaque liste de nombres (embedding)
NB_EXTRAITS = 5      # combien de morceaux de notes on donne à Gemini pour répondre


@lru_cache  # on crée le client une seule fois, puis on le réutilise
def client_gemini():
    from google import genai

    cle = os.getenv("GEMINI_API_KEY")
    if not cle:
        raise RuntimeError(
            "GEMINI_API_KEY manquante : copie .env.example en .env et ajoute ta clé Gemini."
        )
    return genai.Client(api_key=cle)
