"""
main.py
========

Projet FAO DataLab
Diagnostic qualité des données
"""

from pathlib import Path
import pandas as pd

from profiler import ProfileurFAO

# ==========================================================
# CHEMINS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"

# ==========================================================
# FICHIERS
# ==========================================================

fichiers = {
    "Animaux": "animaux.csv",
    "Végétaux": "vegetaux.csv",
    "Céréales": "cereales.csv",
    "Population": "population.csv",
    "Sous-alimentation": "sousalimentation.csv"
}

# ==========================================================
# CHARGEMENT DES DONNÉES
# ==========================================================

dataframes = {}

print("=" * 100)
print("FAO DATALAB")
print("Diagnostic qualité des données")
print("=" * 100)

for nom, fichier in fichiers.items():

    chemin = DATA_DIR / fichier

    if not chemin.exists():
        print(f"\n❌ {fichier} introuvable")
        continue

    print(f"\nLecture de {fichier}...")

    df = pd.read_csv(chemin)

    dataframes[nom] = df

print("\nTous les fichiers ont été chargés.")

# ==========================================================
# DIAGNOSTIC
# ==========================================================

profilers = {}

for nom, df in dataframes.items():

    profiler = ProfileurFAO(df, nom)

    profilers[nom] = profiler

    profiler.rapport()

# ==========================================================
# COMPARAISON DES ZONES
# ==========================================================

print("\n")
print("=" * 100)
print("COMPARAISON DES ZONES")
print("=" * 100)

comparaisons = [
    ("Végétaux", "Animaux"),
    ("Végétaux", "Population"),
    ("Végétaux", "Sous-alimentation"),
]

for source1, source2 in comparaisons:

    if source1 in profilers and source2 in profilers:

        zones_absentes = profilers[source1].verifier_zones(
            profilers[source2].df
        )

        print(f"\n{source1} → {source2}")

        print(f"Nombre de zones absentes : {len(zones_absentes)}")

        if len(zones_absentes) > 0:

            print(sorted(zones_absentes))

# ==========================================================
# RÉSUMÉ
# ==========================================================

print("\n")
print("=" * 100)
print("RÉSUMÉ")
print("=" * 100)

for nom, df in dataframes.items():

    print(f"\n{nom}")

    print(f"Lignes : {df.shape[0]:,}")

    print(f"Colonnes : {df.shape[1]}")

print("\nDiagnostic terminé.")