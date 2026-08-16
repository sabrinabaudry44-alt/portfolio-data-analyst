# COMMENTAIRE DU NOTEBOOK du Nettoyage.py DU DATASET WORLD DATA 2023

from pathlib import Path
import pandas as pd

# ==========================================================
# NETTOYAGE DU DATASET WORLD DATA 2023
# ==========================================================

# Détermine le répertoire racine du projet.
# __file__ correspond au chemin du fichier Python actuel.
# .resolve() obtient le chemin absolu, puis .parent.parent
# remonte de deux niveaux dans l'arborescence des dossiers.
BASE_DIR = Path(__file__).resolve().parent.parent

# Construit le chemin vers le fichier CSV contenant les données brutes.
# L'opérateur "/" de pathlib permet d'assembler les dossiers et le nom du fichier.
input_path = BASE_DIR / "data" / "world-data-2023.csv"

# Affiche dans la console le chemin du fichier qui va être lu.
# Cela permet de vérifier que le bon fichier est utilisé.
print("Lecture du fichier :", input_path)

# Charge le fichier CSV dans un DataFrame pandas.
# Chaque ligne du fichier devient une ligne du DataFrame,
# et chaque colonne du CSV devient une colonne du DataFrame.
df = pd.read_csv(input_path)

# Crée une copie indépendante du DataFrame d'origine.
# Les opérations de nettoyage seront effectuées sur cette copie,
# ce qui permet de conserver les données brutes intactes.
df_clean = df.copy()

# ==========================================================
# 1. Nettoyage des noms de colonnes
# ==========================================================

# Standardise les noms des colonnes afin d'obtenir un format
# homogène et plus facile à manipuler dans le code :
# - remplace les retours à la ligne par des espaces ;
# - convertit tous les caractères en minuscules ;
# - supprime les espaces en début et fin de texte ;
# - remplace les caractères spéciaux et les espaces par des underscores (_);
# - supprime les underscores en début et en fin de nom.

df_clean.columns = (
    df_clean.columns.str.replace("\n", " ", regex=False)  # Remplace les sauts de ligne par un espace.
    .str.lower()  # Convertit les noms en minuscules.
    .str.strip()  # Supprime les espaces inutiles.
    .str.replace(r"[^a-z0-9]+", "_", regex=True)  # Remplace les caractères non alphanumériques par "_".
    .str.strip("_")  # Supprime les "_" en début et fin de chaîne.
)

# ==========================================================
# 2. Suppression de la colonne "abbreviation"
# ==========================================================

# Supprime la colonne "abbreviation" du DataFrame, car elle
# n'est pas utile pour les analyses réalisées.
# L'option errors="ignore" permet d'éviter une erreur si la
# colonne est absente du jeu de données.

df_clean = df_clean.drop(columns=["abbreviation"], errors="ignore")

# ==========================================================
# 3. Suppression des espaces
# ==========================================================

# Parcourt toutes les colonnes de type texte (object) et
# supprime les espaces inutiles en début et en fin de chaque
# valeur. Cette étape permet d'éviter des erreurs lors des
# traitements, des comparaisons ou des regroupements de données.

for col in df_clean.select_dtypes(include="object").columns:
    df_clean[col] = df_clean[col].str.strip()  # Retire les espaces au début et à la fin des chaînes de caractères.

# ==========================================================
# 4. Détection des caractères mal encodés
# ==========================================================

# Recherche dans toutes les colonnes de type texte la présence
# du caractère "", qui apparaît généralement lorsqu'un problème
# d'encodage s'est produit lors de la lecture ou de l'importation
# des données. Si des valeurs concernées sont trouvées, elles sont
# affichées afin de faciliter leur identification et leur correction.

print("\n===== CARACTÈRES MAL ENCODÉS =====")

# Parcourt chaque colonne contenant des chaînes de caractères.
for col in df_clean.select_dtypes(include="object"):
    # Sélectionne les lignes contenant le caractère "".
    erreurs = df_clean[df_clean[col].str.contains("", na=False)]

    # Si des erreurs d'encodage sont détectées, les affiche.
    if not erreurs.empty:
        print(f"\nColonne : {col}")
        print(erreurs[[col]])

# ==========================================================
# 5. Correction des caractères mal encodés
# ==========================================================

# Corrige les caractères mal encodés présents dans certaines
# valeurs du jeu de données. Les corrections sont appliquées
# manuellement pour les pays, les capitales et les principales
# villes concernés.

# Recherche les lignes où le nom du pays contient le caractère
# de remplacement "", puis remplace cette valeur par le nom
# correctement encodé.
mask = df_clean["country"].astype(str).str.contains("", na=False)
df_clean.loc[mask, "country"] = "São Tomé and Príncipe"

# Dictionnaire regroupant les corrections à appliquer.
# Pour chaque pays, les colonnes concernées sont associées
# à leur valeur correctement encodée.
corrections = {
    "Brazil": {
        "capital_major_city": "Brasília",
        "largest_city": "São Paulo",
    },
    "Cameroon": {
        "capital_major_city": "Yaoundé",
    },
    "Colombia": {
        "capital_major_city": "Bogotá",
        "largest_city": "Bogotá",
    },
    "Costa Rica": {
        "capital_major_city": "San José",
        "largest_city": "San José",
    },
    "Cyprus": {
        "largest_city": "Strovolos",
    },
    "Iceland": {
        "capital_major_city": "Reykjavík",
        "largest_city": "Reykjavík",
    },
    "Maldives": {
        "capital_major_city": "Malé",
        "largest_city": "Malé",
    },
    "Moldova": {
        "capital_major_city": "Chișinău",
        "largest_city": "Chișinău",
    },
    "Paraguay": {
        "capital_major_city": "Asunción",
    },
    "São Tomé and Príncipe": {
        "capital_major_city": "São Tomé",
        "largest_city": "São Tomé",
    },
    "Sweden": {
        "largest_city": "Stockholm",
    },
    "Switzerland": {
        "largest_city": "Zürich",
    },
    "Togo": {
        "capital_major_city": "Lomé",
        "largest_city": "Lomé",
    },
    "Tonga": {
        "capital_major_city": "Nukuʻalofa",
        "largest_city": "Nukuʻalofa",
    },
}

# Parcourt le dictionnaire des corrections et met à jour les
# valeurs correspondantes dans le DataFrame.
for pays, valeurs in corrections.items():
    for colonne, valeur in valeurs.items():
        # Vérifie que la colonne existe avant d'effectuer la modification.
        if colonne in df_clean.columns:
            df_clean.loc[df_clean["country"] == pays, colonne] = valeur

# ==========================================================
# 6. Vérification des caractères mal encodés
# ==========================================================

# Effectue un contrôle final sur toutes les colonnes contenant
# des données textuelles afin de vérifier qu'aucun caractère
# mal encodé ("") n'est encore présent dans le DataFrame.

print("\n===== VÉRIFICATION =====")

reste = 0
for col in df_clean.select_dtypes(include="object"):
    # Compte le nombre de valeurs contenant le caractère "".
    nb = df_clean[col].astype(str).str.contains("", na=False).sum()
    if nb > 0:
        print(f"{col} : {nb} erreur(s)")
        reste += nb

if reste == 0:
    print("\n✅ Tous les caractères mal encodés ont été corrigés avec succès.")
else:
    print(f"\n⚠️ Il reste {reste} valeur(s) à corriger.")

# ==========================================================
# 7. Conversion des colonnes numériques
# ==========================================================

# Recherche les colonnes de type texte qui contiennent en réalité
# des valeurs numériques. Les caractères de mise en forme
# (virgules, symbole "$" et "%") sont supprimés avant la conversion.

for col in df_clean.select_dtypes(include="object"):
    # Supprime les caractères pouvant empêcher la conversion en nombre.
    temp = (
        df_clean[col]
        .astype(str)
        .str.replace(",", "", regex=False)  # Retire les séparateurs de milliers.
        .str.replace("$", "", regex=False)  # Retire le symbole monétaire.
        .str.replace("%", "", regex=False)  # Retire le symbole de pourcentage.
    )

    # Tente de convertir les valeurs en type numérique.
    # Les valeurs non convertibles sont remplacées par NaN.
    numeric = pd.to_numeric(temp, errors="coerce")

    # Si au moins 50 % des valeurs de la colonne sont convertibles,
    # la colonne est considérée comme numérique et remplace la colonne d'origine.
    if numeric.notna().sum() >= len(df_clean) * 0.5:
        df_clean[col] = numeric

# ==========================================================
# 8. Gestion des valeurs manquantes
# ==========================================================

# Identifie les valeurs manquantes présentes dans le jeu de
# données, puis applique une méthode de remplacement adaptée
# selon le type de variable.

print("\nValeurs manquantes :")
print(df_clean.isna().sum())

print("\nLignes contenant des valeurs manquantes :")
print(df_clean[df_clean.isna().any(axis=1)])

# Liste des colonnes textuelles pour lesquelles les valeurs
# manquantes seront remplacées par "Unknown".
colonnes_texte_manquantes = [
    "currency_code",
    "official_language",
    "capital_major_city",
    "largest_city",
]

# Ne conserve que les colonnes réellement présentées dans le DataFrame
colonnes_texte_manquantes = [col for col in colonnes_texte_manquantes if col in df_clean.columns]
df_clean[colonnes_texte_manquantes] = df_clean[colonnes_texte_manquantes].fillna("Unknown")

# Sélectionne toutes les colonnes numériques du DataFrame.
numeric_cols = df_clean.select_dtypes(include="number").columns

# Remplace les valeurs manquantes des colonnes numériques
# par la médiane de chaque colonne afin de limiter l'impact
# des valeurs extrêmes.
df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())

# ==========================================================
# 9. Vérification des doublons
# ==========================================================

# Vérifie si le jeu de données contient des lignes dupliquées.
print("\nNombre de doublons :", df_clean.duplicated().sum())

# ==========================================================
# 10. Recherche des valeurs aberrantes (méthode IQR)
# ==========================================================

# Détecte les valeurs aberrantes dans les colonnes numériques
# à l'aide de la méthode de l'intervalle interquartile (IQR).

print("\n===== VALEURS ABERRANTES =====")

colonnes_num = df_clean.select_dtypes(include="number").columns

for col in colonnes_num:
    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1

    borne_inf = Q1 - 1.5 * IQR
    borne_sup = Q3 + 1.5 * IQR

    nb = ((df_clean[col] < borne_inf) | (df_clean[col] > borne_sup)).sum()
    print(f"{col} : {nb} valeur(s) aberrante(s)")

# ==========================================================
# 11. Sauvegarde du jeu de données nettoyé
# ==========================================================

# Définit le chemin du fichier dans lequel sera enregistré
# le jeu de données après les différentes étapes de nettoyage.
output_path = BASE_DIR / "data" / "world-data-2023-clean.csv"

# Enregistre le DataFrame nettoyé au format CSV.
df_clean.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\nFichier nettoyé enregistré :", output_path)