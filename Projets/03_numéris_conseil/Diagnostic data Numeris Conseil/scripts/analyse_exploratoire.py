"""=============================================================================
ANALYSE EXPLORATOIRE DES DONNÉES (EDA) - WORLD DATA 2023
=============================================================================
Problématique métier :
Identifier les principaux indicateurs socio-économiques pouvant caractériser
les pays les plus attractifs pour un investissement international.
============================================================================="""

from pathlib import Path
from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# =============================================================================
# CONFIGURATION DES CHEMINS (CONSTANTES)
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
FIGURES_DIR = PROJECT_ROOT / "figures"

# Sous-dossiers pour l'organisation des figures
HIST_DIR = FIGURES_DIR / "histogrammes"
BOXPLOTS_DIR = FIGURES_DIR / "boxplots"
CORR_DIR = FIGURES_DIR / "correlations"
TOP10_DIR = FIGURES_DIR / "top10"
REGPLOT_DIR = FIGURES_DIR / "relations"

DATA_INPUT_PATH = DATA_DIR / "world-data-2023-clean.csv"
DATA_OUTPUT_PATH = DATA_DIR / "world-data-2023-eda-enrichi.csv"


# =============================================================================
# CONFIGURATION DU STYLE GRAPHIQUE GLOBAL
# =============================================================================

def setup_graphics_style() -> None:
    """Configure le thème visuel global pour Matplotlib et Seaborn."""
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        "figure.figsize": (12, 7),  # Taille équilibrée par défaut
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
    })


# =============================================================================
# FONCTIONS UTILITAIRES & INSPECTION
# =============================================================================

def init_environment() -> None:
    """Crée l'arborescence des dossiers si elle n'existe pas."""
    folders = [DATA_DIR, FIGURES_DIR, HIST_DIR, BOXPLOTS_DIR, CORR_DIR, TOP10_DIR, REGPLOT_DIR]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)


def load_dataset(file_path: Path) -> pd.DataFrame:
    """Charge le fichier CSV en vérifiant son existence."""
    if not file_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")
    print(f"Chargement des données depuis : {file_path}")
    return pd.read_csv(file_path)


def print_section_header(title: str) -> None:
    """Affiche un titre de section formaté en console."""
    print("\n" + "=" * 80)
    print(f" {title.upper()} ")
    print("=" * 80)


def inspect_dataset(df: pd.DataFrame) -> None:
    """Affiche un rapport complet d'inspection du jeu de données."""
    print_section_header("Aperçu des 5 premières lignes")
    print(df.head())

    print_section_header("Dimensions du Dataset")
    print(f"Lignes   : {df.shape[0]}")
    print(f"Colonnes : {df.shape[1]}")

    print_section_header("Informations Générales & Types")
    df.info()

    print_section_header("Statistiques Descriptives")
    print(df.describe().T)

    print_section_header("Valeurs Manquantes")
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    if not missing_cols.empty:
        print(missing_cols)
    else:
        print("Aucune valeur manquante détectée.")
    print(f"\nTotal des valeurs manquantes : {missing.sum()}")

    print_section_header("Doublons")
    print(f"Nombre de doublons : {df.duplicated().sum()}")


# =============================================================================
# FONCTIONS DE VISUALISATION (EDA)
# =============================================================================

def plot_histograms(df: pd.DataFrame, variables: List[str], save_dir: Path) -> None:
    """Génère et sauvegarde un histogramme avec KDE, moyenne et médiane pour chaque variable."""
    print_section_header("Génération des Histogrammes")
    for var in variables:
        if var not in df.columns:
            continue
        
        valid_data = df[var].dropna()
        if valid_data.empty:
            continue

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(
            data=df,
            x=var,
            bins=25,
            kde=True,
            color="#2E86C1",
            edgecolor="black",
            alpha=0.75,
            ax=ax
        )

        mean_val = valid_data.mean()
        median_val = valid_data.median()

        ax.axvline(mean_val, color="red", linestyle="--", linewidth=2, label=f"Moyenne : {mean_val:.2f}")
        ax.axvline(median_val, color="green", linestyle="-", linewidth=2, label=f"Médiane : {median_val:.2f}")

        ax.set_title(f"Distribution de : {var}")
        ax.set_xlabel(var)
        ax.set_ylabel("Nombre de pays")
        ax.legend()
        ax.grid(alpha=0.3)

        fig.tight_layout()
        fig.savefig(save_dir / f"hist_{var}.png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f" Saved: hist_{var}.png")


def plot_standardized_boxplots(df: pd.DataFrame, variables: List[str], save_dir: Path) -> None:
    """Génère un boxplot comparatif normalisé sans texte ni étiquette coupés."""
    print_section_header("Génération du Boxplot Standardisé")
    available_vars = [v for v in variables if v in df.columns]
    
    if not available_vars:
        return

    df_clean = df[available_vars].dropna()
    if df_clean.empty:
        return

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_clean)
    df_scaled = pd.DataFrame(scaled_data, columns=available_vars)

    fig, ax = plt.subplots(figsize=(14, 7))
    sns.boxplot(
        data=df_scaled,
        palette="Set2",
        linewidth=1.5,
        showmeans=True,
        meanprops={"marker": "*", "markerfacecolor": "gold", "markeredgecolor": "black", "markersize": 10},
        flierprops={"marker": "o", "markerfacecolor": "red", "markeredgecolor": "black", "markersize": 5, "alpha": 0.6},
        ax=ax
    )

    ax.set_title("Comparaison des distributions (Variables Standardisées Z-Score)")
    ax.set_ylabel("Valeur Z-score")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    # Réajustement des marges pour éviter la coupure sous le graphique
    fig.tight_layout()
    fig.savefig(save_dir / "boxplots_standardises.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(" Saved: boxplots_standardises.png")


def plot_correlation_matrix(df: pd.DataFrame, save_dir: Path) -> pd.DataFrame:
    """Affiche la heatmap de corrélation pour les variables numériques."""
    print_section_header("Génération de la Matrice de Corrélation")
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="RdYlBu_r",
        fmt=".2f",
        linewidths=0.5,
        square=True,
        cbar_kws={"shrink": 0.8},
        annot_kws={"size": 9},
        ax=ax
    )

    ax.set_title("Matrice de Corrélation des Indicateurs Socio-Économiques", pad=15)
    
    fig.tight_layout()
    fig.savefig(save_dir / "heatmap_correlation.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(" Saved: heatmap_correlation.png")
    return corr_matrix


def plot_top10_bar(
    df: pd.DataFrame, 
    x_col: str, 
    y_col: str, 
    title: str, 
    x_label: str,
    save_dir: Path, 
    filename: str
) -> None:
    """Génère un graphique en barres du Top 10 des pays selon une variable spécifiée."""
    print_section_header(f"Génération du Top 10 : {title}")
    if x_col not in df.columns or y_col not in df.columns:
        print(f"Colonnes {x_col} ou {y_col} absentes du DataFrame.")
        return

    top10_df = df.dropna(subset=[x_col]).sort_values(by=x_col, ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(11, 6))
    graph = sns.barplot(
        data=top10_df,
        x=x_col,
        y=y_col,
        hue=y_col,
        palette="viridis",
        legend=False,
        ax=ax
    )

    for container in graph.containers:
        graph.bar_label(container, fmt="%.0f", padding=5, fontsize=9)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Pays")
    ax.grid(axis="x", alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_dir / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f" Saved: {filename}")


def plot_regression(
    df: pd.DataFrame, 
    x_col: str, 
    y_col: str, 
    title: str, 
    save_dir: Path, 
    filename: str, 
    color: str = "#3498DB",
    log_scale_x: bool = False
) -> None:
    """Génère un graphique de régression bivariée avec calcul automatique de la corrélation."""
    if x_col not in df.columns or y_col not in df.columns:
        return

    df_clean = df[[x_col, y_col]].dropna()
    if df_clean.empty:
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(
        data=df_clean,
        x=x_col,
        y=y_col,
        scatter_kws={"s": 60, "color": color, "alpha": 0.7},
        line_kws={"color": "#E74C3C", "linewidth": 2},
        ax=ax
    )

    if log_scale_x:
        ax.set_xscale("log")
        ax.set_xlabel(f"{x_col} (Échelle Log)")

    correlation = df_clean[x_col].corr(df_clean[y_col])
    ax.set_title(title)
    ax.text(
        0.95, 0.05,
        f"Corrélation Pearson = {correlation:.2f}",
        transform=ax.transAxes,
        fontsize=11,
        ha="right",
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.5", alpha=0.8)
    )
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_dir / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f" Saved: {filename}")


def plot_bubble_chart(df: pd.DataFrame, save_dir: Path) -> None:
    """Génère un graphique à bulles (Population vs CO2 vs PIB per capita vs Espérance de vie)."""
    print_section_header("Génération du Bubble Chart")
    cols_needed = ["population", "co2_emissions", "GDP_per_capita", "life_expectancy"]
    if not all(col in df.columns for col in cols_needed):
        print("Variables requises absentes pour le graphique à bulles.")
        return

    df_clean = df.dropna(subset=cols_needed)

    fig, ax = plt.subplots(figsize=(12, 7))
    sns.scatterplot(
        data=df_clean,
        x="population",
        y="co2_emissions",
        size="GDP_per_capita",
        hue="life_expectancy",
        palette="viridis",
        sizes=(30, 400),
        alpha=0.75,
        ax=ax
    )

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_title("Population, Émissions de CO₂ et Espérance de vie (Échelle Log)")
    ax.set_xlabel("Population (Log)")
    ax.set_ylabel("Émissions de CO₂ (Log)")
    ax.grid(True, which="both", linestyle="--", alpha=0.3)
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")

    fig.tight_layout()
    fig.savefig(save_dir / "population_co2_bubble.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(" Saved: population_co2_bubble.png")


def plot_target_correlations(corr_matrix: pd.DataFrame, target_col: str, save_dir: Path) -> None:
    """Affiche le Top 10 des variables les plus corrélées avec la variable cible."""
    print_section_header(f"Correlations avec la cible : {target_col}")
    if target_col not in corr_matrix.columns:
        return

    top_corr = corr_matrix[target_col].drop(target_col).abs().sort_values(ascending=False).head(10)
    signed_top_corr = corr_matrix.loc[top_corr.index, target_col]

    fig, ax = plt.subplots(figsize=(10, 6))
    graph = sns.barplot(
        x=signed_top_corr.values,
        y=signed_top_corr.index,
        hue=signed_top_corr.index,
        palette="viridis",
        legend=False,
        ax=ax
    )

    for container in graph.containers:
        graph.bar_label(container, fmt="%.2f", padding=4)

    ax.set_title(f"Top 10 des variables les plus corrélées avec '{target_col}'")
    ax.set_xlabel("Coefficient de corrélation de Pearson")
    ax.set_ylabel("Variables")
    ax.grid(axis="x", alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_dir / "top_correlations_target.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(" Saved: top_correlations_target.png")


# =============================================================================
# PIPELINE PRINCIPAL D'EXÉCUTION
# =============================================================================

def main() -> None:
    """Orchestre la totalité du workflow EDA."""
    # 1. Initialisation de l'environnement et du style
    init_environment()
    setup_graphics_style()

    # 2. Chargement du Dataset
    df = load_dataset(DATA_INPUT_PATH)

    # 3. Feature Engineering
    if "gdp" in df.columns and "population" in df.columns:
        df["GDP_per_capita"] = np.where(df["population"] > 0, df["gdp"] / df["population"], np.nan)
        print("\n[Feature Engineering] 'GDP_per_capita' calculé avec succès.")

    # 4. Inspection générale du Dataset
    inspect_dataset(df)

    # 5. Définition des variables d'intérêt
    numerical_vars = [
        "GDP_per_capita", "life_expectancy", "population",
        "unemployment_rate", "birth_rate", "fertility_rate",
        "infant_mortality", "maternal_mortality_ratio", "co2_emissions"
    ]

    # 6. Génération des visualisations
    plot_histograms(df, [v for v in numerical_vars if v in df.columns], HIST_DIR)
    plot_standardized_boxplots(df, numerical_vars, BOXPLOTS_DIR)
    
    corr_matrix = plot_correlation_matrix(df, CORR_DIR)

    plot_top10_bar(
        df=df, 
        x_col="GDP_per_capita", 
        y_col="country", 
        title="Top 10 des pays selon le PIB par habitant", 
        x_label="PIB par habitant ($)",
        save_dir=TOP10_DIR, 
        filename="top10_gdp.png"
    )

    plot_regression(
        df=df, 
        x_col="GDP_per_capita", 
        y_col="life_expectancy",
        title="PIB par habitant vs Espérance de vie", 
        save_dir=REGPLOT_DIR, 
        filename="scatter_gdp_life.png", 
        color="#3498DB",
        log_scale_x=True
    )

    plot_regression(
        df=df, 
        x_col="GDP_per_capita", 
        y_col="infant_mortality",
        title="PIB par habitant vs Mortalité infantile", 
        save_dir=REGPLOT_DIR, 
        filename="gdp_vs_infant.png", 
        color="#8E44AD",
        log_scale_x=True
    )

    plot_bubble_chart(df, REGPLOT_DIR)

    if "life_expectancy" in df.columns:
        plot_target_correlations(corr_matrix, "life_expectancy", CORR_DIR)

    # 7. Préparation de la matrice d'entraînement / Machine Learning
    print_section_header("Préparation de la Matrice de Features (X) et Cible (y)")
    if "life_expectancy" in df.columns:
        y = df["life_expectancy"]
        cols_to_drop = [
            "country", "capital_major_city", "largest_city",
            "official_language", "currency_code", "calling_code", "life_expectancy"
        ]
        X = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
        print(f"Dimensions de la matrice X : {X.shape}")
        print(f"Dimensions de la cible y    : {y.shape}")

    # 8. Sauvegarde du Dataset enrichi
    df.to_csv(DATA_OUTPUT_PATH, index=False, encoding="utf-8")

    print("\n" + "=" * 70)
    print("ANALYSE EXPLORATOIRE TERMINÉE AVEC SUCCÈS")
    print(f"✅ Dataset enrichi enregistré dans : {DATA_OUTPUT_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    main()