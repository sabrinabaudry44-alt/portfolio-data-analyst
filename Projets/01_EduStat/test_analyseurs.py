# Challenge 3

"""
test_analyseurs.py

Tests des analyseurs EduStat
Challenge 3
"""

from edustat import (
    Eleve,
    Promotion,
    AnalyseurPromotion,
    AnalyseurGenerale,
    AnalyseurTechno,
    AnalyseurPro,
)

# ==========================================================
# Création des promotions
# ==========================================================

promo_gen = Promotion(
    "Générale T1",
    "Lycée Victor Hugo",
    "Générale"
)

promo_tech = Promotion(
    "Technologique T1",
    "Lycée Victor Hugo",
    "Technologique"
)

promo_pro = Promotion(
    "Professionnelle T1",
    "Lycée Victor Hugo",
    "Professionnelle"
)

# ==========================================================
# Élèves Générale
# ==========================================================

promo_gen.ajouter(
    Eleve(
        "E001",
        "Lucas",
        "Martin",
        "Lycée Victor Hugo",
        "Générale",
        14.5,
        13,
        16,
        12.5,
        15,
        14,
    )
)

promo_gen.ajouter(
    Eleve(
        "E002",
        "Camille",
        "Dubois",
        "Lycée Victor Hugo",
        "Générale",
        17,
        16.5,
        15,
        14,
        18,
        17.5,
    )
)

promo_gen.ajouter(
    Eleve(
        "E003",
        "Nathan",
        "Leroy",
        "Lycée Victor Hugo",
        "Générale",
        9,
        11,
        10.5,
        8,
        9.5,
        8.5,
    )
)

# ==========================================================
# Élèves Technologique
# ==========================================================

promo_tech.ajouter(
    Eleve(
        "E004",
        "Emma",
        "Michel",
        "Lycée Victor Hugo",
        "Technologique",
        15,
        13.5,
        14,
        12,
        15.5,
        14.5,
    )
)

promo_tech.ajouter(
    Eleve(
        "E005",
        "Zoé",
        "Lefebvre",
        "Lycée Victor Hugo",
        "Technologique",
        12.5,
        11.5,
        13,
        11,
        12,
        12.5,
    )
)

promo_tech.ajouter(
    Eleve(
        "E006",
        "Axel",
        "Robert",
        "Lycée Victor Hugo",
        "Technologique",
        11,
        10,
        12,
        9.5,
        11.5,
        12.5,
    )
)

# ==========================================================
# Élèves Professionnelle
# ==========================================================

promo_pro.ajouter(
    Eleve(
        "E007",
        "Théo",
        "Dupont",
        "Lycée Victor Hugo",
        "Professionnelle",
        10,
        11.5,
        9,
        10.5,
        None,
        10,
    )
)

promo_pro.ajouter(
    Eleve(
        "E008",
        "Louis",
        "Mercier",
        "Lycée Victor Hugo",
        "Professionnelle",
        13,
        12,
        11.5,
        12.5,
        13,
        12,
    )
)

promo_pro.ajouter(
    Eleve(
        "E009",
        "Sarah",
        "Girard",
        "Lycée Victor Hugo",
        "Professionnelle",
        9.5,
        11,
        10,
        10.5,
        9,
        10,
    )
)

# ==========================================================
# Création des analyseurs
# ==========================================================

analyseurs = [
    AnalyseurGenerale(promo_gen),
    AnalyseurTechno(
        promo_tech,
        matiere_dominante="physique",
    ),
    AnalyseurPro(promo_pro),
]

# ==========================================================
# Tests
# ==========================================================

print("=" * 70)
print("TEST DES ANALYSEURS")
print("=" * 70)

for analyseur in analyseurs:

    analyseur.analyser()

    analyseur.rapport()

    print("-" * 70)

# ==========================================================
# Héritage
# ==========================================================

print("\n")
print("=" * 70)
print("TEST DE L'HÉRITAGE")
print("=" * 70)

for analyseur in analyseurs:

    print(type(analyseur).__name__)

    print(
        isinstance(
            analyseur,
            AnalyseurPromotion,
        )
    )

# ==========================================================
# Top 3
# ==========================================================

print("\n")
print("=" * 70)
print("TOP 3 GÉNÉRALE")
print("=" * 70)

top = analyseurs[0].top_n(3)

for i, eleve in enumerate(top, start=1):

    print(f"{i}. {eleve}")

print("\n")
print("=" * 70)
print("TEST TERMINÉ")
print("=" * 70)