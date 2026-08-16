"""
profiler.py
============

Classes de diagnostic qualité des données
Projet FAO DataLab
"""

from typing import Optional
import pandas as pd


# ======================================================================
# CLASSE MÈRE
# ======================================================================

class DataProfiler:
    """
    Classe générique permettant d'analyser un DataFrame.
    """

    def __init__(self, df: pd.DataFrame, nom_source: str):
        self.df = df
        self.nom_source = nom_source

    # ==========================================================
    # INFORMATIONS GÉNÉRALES
    # ==========================================================

    def dimensions(self) -> tuple:
        """Retourne les dimensions du DataFrame."""
        return self.df.shape

    def informations(self):
        """Affiche les informations générales."""
        self.df.info()

    def types_colonnes(self) -> pd.Series:
        """Retourne le type de chaque colonne."""
        return self.df.dtypes

    # ==========================================================
    # VALEURS MANQUANTES
    # ==========================================================

    def rapport_nan(self) -> pd.DataFrame:
        """
        Nombre et pourcentage de NaN par colonne.
        """

        nb_nan = self.df.isna().sum()

        taux = (nb_nan / len(self.df) * 100).round(2)

        return pd.DataFrame({
            "Nb NaN": nb_nan,
            "% NaN": taux
        })

    # ==========================================================
    # DOUBLONS
    # ==========================================================

    def rapport_doublons(self, subset=None) -> int:
        """
        Nombre de doublons.
        """
        return self.df.duplicated(subset=subset).sum()

    # ==========================================================
    # UNITÉS
    # ==========================================================

    def rapport_unites(self):

        if "Unité" not in self.df.columns:
            return None

        return self.df["Unité"].value_counts()

    # ==========================================================
    # STATISTIQUES
    # ==========================================================

    def statistiques(self):

        return self.df.describe(include="all")

    # ==========================================================
    # VALEURS NÉGATIVES
    # ==========================================================

    def valeurs_negatives(self):
        """
        Retourne les lignes dont la valeur est négative.
        """

        if "Valeur" not in self.df.columns:
            return None

        valeurs = pd.to_numeric(
            self.df["Valeur"],
            errors="coerce"
        )

        return self.df[valeurs < 0]
    
    # ==========================================================
    # RÉSUMÉ
    # ==========================================================

    def resume(self):

        print("\n" + "=" * 90)
        print(f"DIAGNOSTIC : {self.nom_source.upper()}")
        print("=" * 90)

        print(f"Lignes   : {self.df.shape[0]:,}")
        print(f"Colonnes : {self.df.shape[1]}")

        print("\nTypes des colonnes")
        print(self.types_colonnes())

        print("\nValeurs manquantes")
        print(self.rapport_nan())

        print("\nDoublons")
        print(self.rapport_doublons())

        if self.rapport_unites() is not None:

            print("\nUnités")
            print(self.rapport_unites())


# ======================================================================
# CLASSE FILLE
# ======================================================================

class ProfileurFAO(DataProfiler):
    """
    Classe spécialisée pour les fichiers FAO.
    """

    CLE = "Zone"

    # ==========================================================
    # CLÉ MÉTIER
    # ==========================================================

    def verifier_cle_metier(self) -> int:
        """
        Vérifie les doublons sur la clé métier.
        """

        colonnes = [
            "Zone",
            "Produit",
            "Élément"
        ]

        colonnes = [
            c for c in colonnes
            if c in self.df.columns
        ]

        if len(colonnes) == 0:
            return 0

        return self.df.duplicated(subset=colonnes).sum()

    # ==========================================================
    # COMPARAISON DES ZONES
    # ==========================================================

    def verifier_zones(self, autre_df: pd.DataFrame):

        if "Zone" not in autre_df.columns:
            return set()

        return (
            set(self.df["Zone"])
            -
            set(autre_df["Zone"])
        )

    # ==========================================================
    # SYMBOLES FAO
    # ==========================================================

    def verifier_symboles(self):

        if "Symbole" not in self.df.columns:
            return None

        return self.df["Symbole"].value_counts()

    # ==========================================================
    # VALEURS EXTRÊMES
    # ==========================================================

    def verifier_valeurs_extremes(self):

        if "Valeur" not in self.df.columns:
            return None

        q1 = self.df["Valeur"].quantile(0.25)
        q3 = self.df["Valeur"].quantile(0.75)

        iqr = q3 - q1

        borne_inf = q1 - 1.5 * iqr
        borne_sup = q3 + 1.5 * iqr

        return self.df[
            (self.df["Valeur"] < borne_inf)
            |
            (self.df["Valeur"] > borne_sup)
        ]

    # ==========================================================
    # RAPPORT COMPLET
    # ==========================================================

    def rapport(self):

        self.resume()

        print("\nDoublons sur la clé métier")
        print(self.verifier_cle_metier())

        symboles = self.verifier_symboles()

        if symboles is not None:

            print("\nRépartition des symboles")
            print(symboles)

        neg = self.valeurs_negatives()

        if neg is not None:

            print(f"\nValeurs négatives : {len(neg)}")

        ext = self.verifier_valeurs_extremes()

        if ext is not None:

            print(f"Valeurs extrêmes : {len(ext)}")