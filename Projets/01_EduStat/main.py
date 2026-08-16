# Challenge 4

from edustat import ProfileurNotes

"""
main.py

Point d'entrée du projet EduStat.

Charge les données,
crée les promotions,
analyse les résultats
et affiche les rapports.
"""

from edustat import (
    Promotion,
    AnalyseurGenerale,
    AnalyseurTechno,
    AnalyseurPro,
    charger_notes,
)


def main():

    print("=" * 70)
    print("                  PROJET EDUSTAT")
    print("=" * 70)

    # ======================================================
    # Chargement des données
    # ======================================================

    promotions = charger_notes("notes_brutes.csv")

    print(f"\n{len(promotions)} établissement(s) chargé(s)\n")

    for nom, promo in sorted(promotions.items()):
        print(f"{nom:<30} : {len(promo)} élève(s)")

    # ======================================================
    # Regroupement par filière
    # ======================================================

    pool = {
        "Générale": Promotion(
            "Générale - Réseau",
            "Réseau Avenir+",
            "Générale"
        ),

        "Technologique": Promotion(
            "Technologique - Réseau",
            "Réseau Avenir+",
            "Technologique"
        ),

        "Professionnelle": Promotion(
            "Professionnelle - Réseau",
            "Réseau Avenir+",
            "Professionnelle"
        )
    }

    for promo in promotions.values():

        for eleve in promo:

            if eleve.filiere in pool:

                pool[eleve.filiere].ajouter(eleve)

    # ======================================================
    # Analyseurs
    # ======================================================

    analyseurs = [

        AnalyseurGenerale(
            pool["Générale"]
        ),

        AnalyseurTechno(
            pool["Technologique"],
            matiere_dominante="physique"
        ),

        AnalyseurPro(
            pool["Professionnelle"]
        )
    ]

    # ======================================================
    # Rapports
    # ======================================================

    print("\n")
    print("=" * 70)
    print("              RAPPORTS DES FILIÈRES")
    print("=" * 70)

    for analyseur in analyseurs:

        analyseur.analyser()
        analyseur.rapport()

        print("-" * 70)


if __name__ == "__main__":
    main()

print("\n" + "=" * 70)
print("Analyse EduStat terminée avec succès.")
print("=" * 70)

# Challenge 5

# ======================================================
# PROFIL DES DONNÉES
# ======================================================

print("\n")
print("=" * 70)
print("             PROFIL DES DONNÉES")
print("=" * 70)

profiler = ProfileurNotes.depuis_csv(
    "notes_brutes.csv",
    separateur=";",
    nom="EduStat 2023-2024"
)

profiler.profiler().rapport()

profiler.exporter("profil_edustat.csv")