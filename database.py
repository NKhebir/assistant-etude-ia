"""Étapes 4 et 5 : ranger les morceaux dans PostgreSQL et chercher les plus proches."""
import psycopg
from pgvector.psycopg import register_vector

from config import DATABASE_URL, DIMENSION


def connexion():
    """Ouvre la connexion et crée la table si elle n'existe pas encore."""
    conn = psycopg.connect(DATABASE_URL, autocommit=True)
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")  # active pgvector
    register_vector(conn)  # permet d'envoyer des listes de nombres à PostgreSQL
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS morceaux (
            id        SERIAL PRIMARY KEY,
            source    TEXT    NOT NULL,   -- nom du fichier PDF
            page      INTEGER NOT NULL,   -- page d'où vient le morceau
            contenu   TEXT    NOT NULL,   -- le texte du morceau
            embedding vector({DIMENSION}) NOT NULL
        )
        """
    )
    return conn


def remplacer_source(conn, source, morceaux, vecteurs):
    """Enlève l'ancienne version d'un fichier puis ajoute ses nouveaux morceaux."""
    with conn.transaction():  # tout réussit ensemble, ou rien n'est changé
        conn.execute("DELETE FROM morceaux WHERE source = %s", (source,))
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO morceaux (source, page, contenu, embedding) VALUES (%s, %s, %s, %s)",
                [(m["source"], m["page"], m["contenu"], v) for m, v in zip(morceaux, vecteurs)],
            )


def chercher(conn, vecteur_question, limite):
    """Retourne les morceaux dont le sens est le plus proche de la question.

    `<=>` est l'opérateur de pgvector qui mesure la "distance" entre deux sens :
    plus c'est petit, plus les textes parlent de la même chose.
    """
    lignes = conn.execute(
        """
        SELECT source, page, contenu, embedding <=> %s AS distance
        FROM morceaux
        ORDER BY distance
        LIMIT %s
        """,
        (vecteur_question, limite),
    ).fetchall()
    return [
        {"source": s, "page": p, "contenu": c, "distance": float(d)}
        for s, p, c, d in lignes
    ]


def lister_sources(conn):
    lignes = conn.execute("SELECT DISTINCT source FROM morceaux ORDER BY source").fetchall()
    return [l[0] for l in lignes]
