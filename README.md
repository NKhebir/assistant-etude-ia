# 📚 Assistant d'étude IA (RAG)

Un assistant qui répond à mes questions de cours **à partir de mes propres notes**
(MAT145, LOG320…), en citant le fichier et la page d'où vient chaque information.

## Comment ça marche

C'est le principe du **RAG** (*Retrieval-Augmented Generation*) : comme un examen à livre ouvert,
l'IA cherche d'abord les bons passages, puis répond à partir d'eux au lieu d'inventer.

```
PDF ──► texte ──► morceaux ──► embeddings ──► PostgreSQL (pgvector)
                                                     │
Question ──► embedding ──► recherche des 5 morceaux les plus proches
                                                     │
                       Gemini : « réponds seulement avec ces extraits » ──► réponse + sources
```

| Fichier | Rôle |
|---|---|
| `pdf_reader.py` | Lit les PDF et découpe le texte en morceaux |
| `embeddings.py` | Transforme le texte en embeddings avec Gemini |
| `database.py` | Range et cherche les morceaux dans PostgreSQL + pgvector |
| `assistant.py` | Assemble tout : ajouter un document, répondre à une question |
| `app.py` | Interface web Streamlit |
| `ingest.py` / `ask.py` | Versions en ligne de commande |

## Installation

Prérequis : Python 3.10+, Docker Desktop, une clé API Gemini (Google AI Studio).

```bash
docker compose up -d                 # démarre la base de données
python -m venv .venv
source .venv/bin/activate            # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                 # puis mets ta clé dans .env
```

## Utilisation

```bash
streamlit run app.py                 # interface web
# ou, dans le terminal :
python ingest.py notes/MAT145.pdf
python ask.py
```

## Technologies
Python · API Gemini · PostgreSQL · pgvector · Streamlit · Docker

## Prochaines étapes
- API back-end avec FastAPI
- Mise en ligne
- Support des PDF scannés (OCR)
