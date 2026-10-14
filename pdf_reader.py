"""Étapes 1 et 2 : lire un PDF et découper son texte en morceaux."""
from pypdf import PdfReader


def lire_pdf(chemin):
    """Retourne une liste de (numéro de page, texte de la page)."""
    lecteur = PdfReader(chemin)
    pages = []
    for numero, page in enumerate(lecteur.pages, start=1):
        texte = page.extract_text() or ""
        texte = " ".join(texte.split())  # enlève les sauts de ligne et espaces en trop
        if texte:
            pages.append((numero, texte))
    return pages


def decouper(texte, taille=800, chevauchement=150):
    """Coupe un long texte en morceaux d'environ `taille` caractères.

    Les morceaux se chevauchent un peu (150 caractères) pour ne pas couper
    une idée en plein milieu sans garder de contexte.
    """
    morceaux = []
    debut = 0
    while debut < len(texte):
        fin = min(debut + taille, len(texte))
        # Si possible, on coupe à la fin d'une phrase plutôt qu'au milieu d'un mot.
        if fin < len(texte):
            point = texte.rfind(". ", debut + taille // 2, fin)
            if point != -1:
                fin = point + 1
        morceau = texte[debut:fin].strip()
        if morceau:
            morceaux.append(morceau)
        if fin >= len(texte):
            break
        debut = fin - chevauchement
    return morceaux


def pdf_en_morceaux(chemin, nom_source):
    """Lit un PDF et retourne tous ses morceaux, avec le fichier et la page d'origine."""
    resultats = []
    for numero, texte in lire_pdf(chemin):
        for morceau in decouper(texte):
            resultats.append({"source": nom_source, "page": numero, "contenu": morceau})
    return resultats
