# Challenge 4

"""
utils.py

Fonctions utilitaires du projet EduStat.
"""

import pandas as pd

from .modeles import Eleve, Promotion


def charger_notes(chemin_csv):
    """
    Charge le fichier notes_brutes.csv,
    supprime les doublons,
    crée les objets Eleve,
    regroupe les élèves par établissement.
    """

    df = pd.read_csv(
    chemin_csv,
    sep=";",
    dtype=str
    ).fillna("")

    # Suppression des doublons
    df = df.drop_duplicates()

    promotions = {}

    # Parcours des lignes du DataFrame
    for _, ligne in df.iterrows():

        # Création d'un objet Eleve
        eleve = Eleve.depuis_dict(ligne)

        nom_etab = eleve.etablissement

        # Si l'établissement n'existe pas encore
        if nom_etab not in promotions:

            promotions[nom_etab] = Promotion(
                nom=f"Promotion {nom_etab}",
                etablissement=nom_etab,
                filiere=eleve.filiere
            )

        # Ajout de l'élève
        promotions[nom_etab].ajouter(eleve)

    return promotions

