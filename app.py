"""Étape 7 : l'interface web.  Lancer avec :  streamlit run app.py"""
import os
import tempfile

import streamlit as st

from assistant import ajouter_document, repondre
from database import connexion, lister_sources

st.set_page_config(page_title="Assistant d'étude", page_icon="📚")
st.title("📚 Assistant d'étude")
st.caption("Pose une question : la réponse vient de tes propres notes, avec la page citée.")


@st.cache_resource  # une seule connexion pour toute l'application
def get_conn():
    return connexion()


conn = get_conn()

# --- Barre de côté : ajouter des notes ---
with st.sidebar:
    st.header("Mes notes")
    fichiers = st.file_uploader("Ajoute des PDF", type="pdf", accept_multiple_files=True)
    if fichiers and st.button("Ajouter à mes notes"):
        for f in fichiers:
            with st.spinner(f"Lecture de {f.name}…"):
                # Streamlit garde le fichier en mémoire ; on l'écrit sur le disque pour pypdf.
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(f.getbuffer())
                n = ajouter_document(conn, tmp.name, nom_source=f.name)
                os.remove(tmp.name)
            if n:
                st.success(f"{f.name} : {n} morceaux")
            else:
                st.warning(f"{f.name} : aucun texte trouvé (PDF scanné ?)")

    sources = lister_sources(conn)
    st.write("**Dans la base :**")
    st.write("\n".join(f"- {s}" for s in sources) if sources else "_rien pour l'instant_")

# --- Zone principale : poser une question ---
question = st.text_input("Ta question", placeholder="Ex. : c'est quoi le test de la droite verticale ?")
if question:
    with st.spinner("Je cherche dans tes notes…"):
        texte, extraits = repondre(conn, question)
    st.markdown(texte)
    if extraits:
        with st.expander("Voir les passages utilisés"):
            for e in extraits:
                st.markdown(f"**{e['source']}, p. {e['page']}**")
                st.write(e["contenu"])
