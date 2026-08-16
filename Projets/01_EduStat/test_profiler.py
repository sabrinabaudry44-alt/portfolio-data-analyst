# Challenge 5

"""
test_profiler.py

Tests du Challenge 5 - DataProfiler et ProfileurNotes
"""

import pandas as pd

from edustat import DataProfiler, ProfileurNotes

# ==========================================================
# TEST 1 : DataProfiler générique
# ==========================================================

print("=" * 60)
print("PROFIL : Exemple")
print("=" * 60)

df = pd.DataFrame({
    "Nom": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 28],
    "Ville": ["Paris", "Lyon", "Marseille"]
})

profiler = DataProfiler(df, nom="Exemple")

profiler.profiler()
profiler.rapport()

print("\n" + "=" * 60)
print("TESTS")
print("=" * 60)

print(f"Nombre de lignes : {len(profiler)}")
print(f"Doublons : {profiler.doublons()}")

print("\nTypes des colonnes :")
print(profiler.types_colonnes())

print("\nStatistiques :")
print(profiler.stats_numeriques())

# ==========================================================
# TEST 2 : Vérification TypeError
# ==========================================================

print("\n" + "=" * 60)
print("TEST TYPEERROR")
print("=" * 60)

try:
    DataProfiler(42)
except TypeError:
    print("✅ TypeError correctement levée")

# ==========================================================
# TEST 3 : ProfileurNotes
# ==========================================================

print("\n" + "=" * 60)
print("PROFILEUR NOTES")
print("=" * 60)

pn = ProfileurNotes.depuis_csv(
    "notes_brutes.csv",
    separateur=";",
    nom="EduStat 2023-2024"
)

pn.profiler()
pn.rapport()

# ==========================================================
# TEST 4 : Héritage
# ==========================================================

print("\n" + "=" * 60)
print("HÉRITAGE")
print("=" * 60)

print(isinstance(pn, DataProfiler))

# ==========================================================
# TEST 5 : Bonus Histogramme ASCII
# ==========================================================

print("\n" + "=" * 60)
print("BONUS : HISTOGRAMME")
print("=" * 60)

pn.histogramme_notes()

print("\n" + "=" * 60)
print("BONUS : EXPORT HTML")
print("=" * 60)

pn.exporter_html()

# Tableaux

print("\n" + "=" * 60)
print("TABLEAU : VALEURS MANQUANTES")
print("=" * 60)

print(pn._profil["manquantes"])

print("\n" + "=" * 60)
print("TABLEAU : MOYENNES PAR MATIÈRE")
print("=" * 60)

print(pd.DataFrame.from_dict(
    pn._profil["moyennes"],
    orient="index",
    columns=["Moyenne"]
))

print("\n" + "=" * 60)
print("TABLEAU : MOYENNES PAR FILIÈRE")
print("=" * 60)

print(pn._profil["filiere"])

print("\n" + "=" * 60)
print("TABLEAU : MOYENNES PAR ÉTABLISSEMENT")
print("=" * 60)

print(pn._profil["etablissement"])

# Comparaison

df_notes = pd.read_csv("notes_brutes.csv")

print("\n" + "=" * 60)
print("BONUS : COMPARAISON")
print("=" * 60)

df1 = pd.DataFrame({
    "Nom": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 28],
    "Ville": ["Paris", "Lyon", "Marseille"]
})

df2 = pd.DataFrame({
    "Nom": ["Alice", "Bob"],
    "Age": [25, 30],
    "Ville": ["Paris", "Lyon"]
})

profil1 = DataProfiler(df1, nom="Jeu 1")
profil2 = DataProfiler(df2, nom="Jeu 2")

profil1.profiler()
profil2.profiler()

profil1.comparer(profil2)

# EXCEL

print("\n" + "=" * 60)
print("BONUS : EXPORT EXCEL")
print("=" * 60)

pn.exporter_excel()