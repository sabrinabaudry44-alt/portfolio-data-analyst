# Challenge 5 - EduStat

"""
profiler.py

Contient :
- DataProfiler (générique)
- ProfileurNotes (spécialisé)
"""

import pandas as pd


# ==========================================================
# CLASSE GÉNÉRIQUE
# ==========================================================

class DataProfiler:
    """
    Profileur générique pour un DataFrame pandas.
    """

    def __init__(self, df, nom="DataFrame"):

        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                "df doit être un pandas.DataFrame"
            )

        self._df = df.copy()
        self.nom = nom
        self._profil = {}

    def __len__(self):
        return len(self._df)

    def __repr__(self):

        return (
            f"DataProfiler("
            f"nom={self.nom!r}, "
            f"lignes={len(self)}, "
            f"colonnes={len(self._df.columns)})"
        )

    def __str__(self):

        return (
            f"{self.nom} : "
            f"{len(self)} ligne(s), "
            f"{len(self._df.columns)} colonne(s)"
        )

    @classmethod
    def depuis_csv(
        cls,
        chemin,
        separateur=";",
        nom="CSV"
    ):

        df = pd.read_csv(
            chemin,
            sep=separateur,
            dtype=str
        )

        return cls(df, nom)

    def types_colonnes(self):

        return self._df.dtypes

    def valeurs_manquantes(self):

        return self._df.isna().sum()

    def doublons(self):

        return self._df.duplicated().sum()

    def stats_numeriques(self):

        return self._df.describe(include="all")

    def profiler(self):

        self._profil = {

            "lignes": len(self._df),

            "colonnes": len(self._df.columns),

            "doublons": self.doublons(),

            "manquantes": self.valeurs_manquantes(),

        }

        return self

    def rapport(self):

        print("\n" + "=" * 60)
        print(f"PROFIL : {self.nom}")
        print("=" * 60)

        print(f"Nombre de lignes : {self._profil['lignes']}")
        print(f"Nombre de colonnes : {self._profil['colonnes']}")
        print(f"Nombre de doublons : {self._profil['doublons']}")

        print("\nValeurs manquantes :")
        print(self._profil["manquantes"])

    def exporter(self, chemin):

        resume = pd.DataFrame({

            "Indicateur": [

                "Lignes",

                "Colonnes",

                "Doublons",

            ],

            "Valeur": [

                self._profil["lignes"],

                self._profil["colonnes"],

                self._profil["doublons"],

            ],

        })

        resume.to_csv(
            chemin,
            sep=";",
            index=False
        )

        print(f"\nProfil exporté dans : {chemin}")

    def comparer(self, autre):
        """
        Compare deux profils.
        """

        if not isinstance(autre, DataProfiler):
            raise TypeError(
                "autre doit être un DataProfiler"
            )

        print("\n" + "=" * 60)
        print("COMPARAISON DES PROFILS")
        print("=" * 60)

        print(
            f"{'Indicateur':<25}"
            f"{self.nom:<20}"
            f"{autre.nom}"
        )

        print("-" * 65)

        print(
            f"{'Nombre de lignes':<25}"
            f"{self._profil['lignes']:<20}"
            f"{autre._profil['lignes']}"
        )

        print(
            f"{'Nombre de colonnes':<25}"
            f"{self._profil['colonnes']:<20}"
            f"{autre._profil['colonnes']}"
        )

        print(
            f"{'Doublons':<25}"
            f"{self._profil['doublons']:<20}"
            f"{autre._profil['doublons']}"
        )

# ==========================================================
# CLASSE SPÉCIALISÉE
# ==========================================================

class ProfileurNotes(DataProfiler):
    """
    Profileur spécialisé pour les données EduStat.
    """

    def profiler(self):

        super().profiler()

        notes = [
            "maths",
            "francais",
            "anglais",
            "histoire",
            "svt",
            "physique",
        ]

        # -------------------------------
        # Moyennes par matière
        # -------------------------------

        moyennes = {}

        for matiere in notes:

            valeurs = pd.to_numeric(
                self._df[matiere],
                errors="coerce"
            )

            moyennes[matiere] = round(
                valeurs.mean(),
                2
            )

        self._profil["moyennes"] = moyennes

        # -------------------------------
        # Moyennes par filière
        # -------------------------------

        df = self._df.copy()

        from .modeles import Eleve

        df["filiere"] = df["filiere"].apply(
            Eleve.normaliser_filiere
        )

        # Conversion des notes
        for col in notes:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        # Moyenne par élève
        df["moyenne"] = df[notes].mean(axis=1)

        # Moyenne par filière
        self._profil["filiere"] = (
            df.groupby("filiere")["moyenne"]
              .mean()
              .round(2)
        )

        # Moyenne par établissement
        self._profil["etablissement"] = (
            df.groupby("etablissement")["moyenne"]
              .mean()
              .round(2)
        )

        return self

    def rapport(self):

        super().rapport()

        print("\n" + "=" * 60)
        print("MOYENNES PAR MATIÈRE")
        print("=" * 60)

        for matiere, moyenne in self._profil["moyennes"].items():

            print(f"{matiere:<12} : {moyenne}")

        print("\n" + "=" * 60)
        print("MOYENNES PAR FILIÈRE")
        print("=" * 60)

        print(self._profil["filiere"])

        print("\n" + "=" * 60)
        print("MOYENNES PAR ÉTABLISSEMENT")
        print("=" * 60)

        print(self._profil["etablissement"])

    def histogramme_notes(self):
        """
        Affiche un histogramme ASCII
        des moyennes des élèves.
        """

        notes = [
            "maths",
            "francais",
            "anglais",
            "histoire",
            "svt",
            "physique",
        ]

        df = self._df.copy()

        for col in notes:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        df["moyenne"] = df[notes].mean(axis=1)

        print("\n" + "=" * 60)
        print("RÉPARTITION DES MOYENNES DES ÉLÈVES")
        print("=" * 60)

        for debut in range(0, 20, 2):

            fin = debut + 2

            if fin == 20:

                masque = (
                    (df["moyenne"] >= debut)
                    &
                    (df["moyenne"] <= fin)
                )

            else:

                masque = (
                    (df["moyenne"] >= debut)
                    &
                    (df["moyenne"] < fin)
                )

            nb = masque.sum()

            print(
                f"{debut:>2}-{fin:<2} | "
                f"{'*' * int(nb)} ({int(nb)})"
            )

    def exporter_html(self, chemin="rapport_edustat.html"):
        """
        Exporte un rapport HTML.
        """

        # Tableau des valeurs manquantes
        manquantes = (
            self._profil["manquantes"]
            .to_frame(name="Valeurs manquantes")
            .to_html()
        )

        # Tableau des moyennes par matière
        moyennes = (
            pd.DataFrame.from_dict(
                self._profil["moyennes"],
                orient="index",
                columns=["Moyenne"]
            ).to_html()
        )

        # Tableau des moyennes par filière
        filiere = (
            self._profil["filiere"]
            .to_frame(name="Moyenne")
            .to_html()
        )

        # Tableau des moyennes par établissement
        etab = (
            self._profil["etablissement"]
            .to_frame(name="Moyenne")
            .to_html()
        )

        html = f"""
<!DOCTYPE html>
<html lang="fr">

<head>

    <meta charset="UTF-8">

    <title>{self.nom}</title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
            color: #333;
        }}

        h1 {{
            color: #0A4A8A;
        }}

        h2 {{
            color: #006699;
            margin-top: 30px;
        }}

        table {{
            border-collapse: collapse;
            width: 80%;
            margin-bottom: 30px;
        }}

        th {{
            background-color: #0A4A8A;
            color: white;
            padding: 8px;
        }}

        td {{
            border: 1px solid #cccccc;
            padding: 8px;
            text-align: center;
        }}

        tr:nth-child(even) {{
            background-color: #eeeeee;
        }}

    </style>

</head>

<body>

    <h1>{self.nom}</h1>

    <h2>Informations générales</h2>

    <ul>
        <li><strong>Nombre de lignes :</strong> {self._profil["lignes"]}</li>
        <li><strong>Nombre de colonnes :</strong> {self._profil["colonnes"]}</li>
        <li><strong>Nombre de doublons :</strong> {self._profil["doublons"]}</li>
    </ul>

    <h2>Valeurs manquantes</h2>

    {manquantes}

    <h2>Moyennes par matière</h2>

    {moyennes}

    <h2>Moyennes par filière</h2>

    {filiere}

    <h2>Moyennes par établissement</h2>

    {etab}

</body>

</html>
"""

        with open(
            chemin,
            "w",
            encoding="utf-8"
        ) as fichier:
            fichier.write(html)

        print(f"\nRapport HTML créé : {chemin}")

        # EXCEL

    def exporter_excel(self, chemin="rapport_edustat.xlsx"):
        """
        Exporte les données dans un fichier Excel
        avec un onglet par établissement.
        """

        with pd.ExcelWriter(chemin) as writer:

            etablissements = (
                self._df["etablissement"]
                .dropna()
                .unique()
            )

            for etablissement in etablissements:

                df_etab = self._df[
                    self._df["etablissement"] == etablissement
                ]

                # Le nom d'une feuille Excel est limité à 31 caractères
                nom_feuille = str(etablissement)[:31]

                df_etab.to_excel(
                    writer,
                    sheet_name=nom_feuille,
                    index=False
                )

        print(f"\nRapport Excel créé : {chemin}")