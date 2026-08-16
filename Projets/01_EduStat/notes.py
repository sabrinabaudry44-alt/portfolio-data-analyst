# Challenge 1

"""
notes.py — Réseau Avenir+ / EduStat
Script de génération FOURNI (Brief S9 — situation "EduStat").

Simule l'export trimestriel des notes du réseau de lycées Avenir+.
Les données reproduisent les défauts réels d'un export de logiciel de vie scolaire :
casse incohérente sur les filières, notes manquantes, doublons, valeur sentinelle.

Usage (depuis le terminal, environnement activé) :
    python notes.py

Produit le fichier : notes_brutes.csv  (séparateur ';', encodage UTF-8)

Colonnes :
    id_eleve ; prenom ; nom ; etablissement ; filiere ;
    maths ; francais ; anglais ; histoire ; svt ; physique

  NE PAS MODIFIER : ce script fournit les données telles quelles.
    Le traitement se fait dans le projet (cf. brief).
"""

import csv

# Chaque tuple :
# (id_eleve, prenom, nom, etablissement, filiere,
#  maths, francais, anglais, histoire, svt, physique)
ELEVES = [

    # ── Lycée Victor Hugo ── Générale ──────────────────────────────────────
    ("E001","Lucas",   "Martin",   "Lycée Victor Hugo","Générale",  "14.5","13.0","16.0","12.5","15.0","14.0"),
    ("E002","Camille", "Dubois",   "Lycée Victor Hugo","Générale",  "17.0","16.5","15.0","14.0","18.0","17.5"),
    ("E003","Nathan",  "Leroy",    "Lycée Victor Hugo","Générale",  "9.0", "11.0","10.5","8.0", "9.5", "8.5"),
    ("E004","Inès",    "Moreau",   "Lycée Victor Hugo","Générale",  "12.0","14.0","13.5","11.0","12.5","13.0"),
    ("E005","Tom",     "Bernard",  "Lycée Victor Hugo","Générale",  "7.5", "9.0", "8.0", "6.5", "7.0", ""),      # svt manquante
    ("E006","Jade",    "Petit",    "Lycée Victor Hugo","Générale",  "15.5","15.0","17.0","16.0","15.5","16.0"),

    # ── Lycée Victor Hugo ── Technologique ─────────────────────────────────
    ("E007","Axel",    "Robert",   "Lycée Victor Hugo","Technologique","11.0","10.0","12.0","9.5","11.5","12.5"),
    ("E008","Léa",     "Simon",    "Lycée Victor Hugo","Technologique","13.5","12.0","11.0","13.0","14.0","13.0"),
    ("E009","Hugo",    "Laurent",  "Lycée Victor Hugo","Technologique","8.0", "9.5","10.0","8.5","7.5","9.0"),
    ("E010","Emma",    "Michel",   "Lycée Victor Hugo","Technologique","15.0","13.5","14.0","12.0","15.5","14.5"),
    ("E011","Rayan",   "Garcia",   "Lycée Victor Hugo","Technologique","6.5", "8.0","7.5", "7.0","6.0","7.0"),
    ("E012","Zoé",     "Lefebvre", "Lycée Victor Hugo","Technologique","12.5","11.5","13.0","11.0","12.0","12.5"),

    # ── Lycée Victor Hugo ── Professionnelle ───────────────────────────────
    ("E013","Théo",    "Dupont",   "Lycée Victor Hugo","Professionnelle","10.0","11.5","9.0","10.5","","10.0"),   # svt manquante
    ("E014","Manon",   "Bonnet",   "Lycée Victor Hugo","Professionnelle","8.5","10.0","9.5","9.0","8.0","9.0"),
    ("E015","Louis",   "Mercier",  "Lycée Victor Hugo","Professionnelle","13.0","12.0","11.5","12.5","13.0","12.0"),
    ("E016","Chloé",   "Morin",    "Lycée Victor Hugo","Professionnelle","7.0","8.5","8.0","7.5","7.0","8.0"),
    ("E017","Enzo",    "Fournier", "Lycée Victor Hugo","Professionnelle","11.0","10.5","12.0","10.0","11.5","11.0"),
    ("E018","Sarah",   "Girard",   "Lycée Victor Hugo","Professionnelle","9.5","11.0","10.0","10.5","9.0","10.0"),

    # ── Lycée Marie Curie ── Générale ──────────────────────────────────────
    ("E019","Yasmine", "Thomas",   "Lycée Marie Curie","Générale",  "18.0","17.0","16.5","15.5","18.5","17.0"),
    ("E020","Baptiste","Petit",    "Lycée Marie Curie","Générale",  "11.5","13.0","12.0","11.0","10.5","12.0"),
    ("E021","Lina",    "Durand",   "Lycée Marie Curie","Générale",  "16.0","15.5","17.0","14.5","16.5","15.5"),
    ("E022","Mathis",  "Leroy",    "Lycée Marie Curie","Générale",  "9.5","10.5","11.0","9.0","8.5","10.0"),
    ("E023","Ambre",   "Moreau",   "Lycée Marie Curie","Générale",  "14.0","14.5","15.0","13.5","13.0","14.0"),
    ("E024","Noa",     "Simon",    "Lycée Marie Curie","Générale",  "19.0","18.0","17.5","16.0","19.5","18.5"),

    # ── Lycée Marie Curie ── Technologique ─────────────────────────────────
    ("E025","Clara",   "Bernard",  "Lycée Marie Curie","technologique","12.0","11.0","13.0","10.5","12.5","11.5"),  # casse incohérente
    ("E026","Alexis",  "Martin",   "Lycée Marie Curie","technologique","14.5","13.0","12.5","13.0","15.0","14.0"),  # casse incohérente
    ("E027","Lucie",   "Dubois",   "Lycée Marie Curie","Technologique","9.0","10.0","9.5","8.5","8.0","9.5"),
    ("E028","Kilian",  "Robert",   "Lycée Marie Curie","Technologique","16.0","14.5","15.0","13.5","16.5","15.0"),
    ("E029","Maëlys",  "Laurent",  "Lycée Marie Curie","Technologique","7.5","9.0","8.5","7.0","7.5","8.0"),
    ("E030","Arthur",  "Michel",   "Lycée Marie Curie","Technologique","13.0","12.5","14.0","11.5","13.5","13.0"),

    # ── Lycée Marie Curie ── Professionnelle ───────────────────────────────
    ("E031","Océane",  "Garcia",   "Lycée Marie Curie","Professionnelle","10.5","12.0","11.0","11.5","10.0","11.0"),
    ("E032","Timéo",   "Lefebvre", "Lycée Marie Curie","Professionnelle","8.0","9.5","8.5","8.0","7.5","8.5"),
    ("E033","Eva",     "Dupont",   "Lycée Marie Curie","Professionnelle","13.5","13.0","12.0","12.5","14.0","13.0"),
    ("E034","Léo",     "Bonnet",   "Lycée Marie Curie","Professionnelle","6.5","8.0","7.0","7.5","6.0","7.5"),
    ("E035","Anaïs",   "Mercier",  "Lycée Marie Curie","Professionnelle","11.5","11.0","12.5","10.5","11.0","12.0"),
    ("E036","Dylan",   "Morin",    "Lycée Marie Curie","Professionnelle","9.0","10.5","9.5","9.5","8.5","10.0"),

    # ── Lycée Jean Moulin ── Générale ──────────────────────────────────────
    ("E037","Inaya",   "Fournier", "Lycée Jean Moulin","Générale",  "13.0","12.5","14.0","11.5","13.5","12.5"),
    ("E038","Romain",  "Girard",   "Lycée Jean Moulin","Générale",  "16.5","15.0","16.0","14.5","17.0","16.0"),
    ("E039","Mia",     "Thomas",   "Lycée Jean Moulin","Générale",  "10.5","12.0","11.5","10.0","9.5","11.0"),
    ("E040","Julien",  "Petit",    "Lycée Jean Moulin","Générale",  "8.0","9.5","9.0","8.5","7.5","8.5"),
    ("E041","Pauline", "Durand",   "Lycée Jean Moulin","Générale",  "15.0","14.5","15.5","13.0","14.5","15.0"),
    ("E042","Adrien",  "Leroy",    "Lycée Jean Moulin","Générale",  "12.5","13.0","12.0","12.0","13.0","12.5"),

    # ── Lycée Jean Moulin ── Technologique ─────────────────────────────────
    ("E043","Lola",    "Moreau",   "Lycée Jean Moulin","TECHNOLOGIQUE","11.5","10.5","12.5","10.0","11.0","12.0"),  # tout maj
    ("E044","Maxime",  "Simon",    "Lycée Jean Moulin","TECHNOLOGIQUE","14.0","13.0","13.5","12.5","14.5","13.5"),  # tout maj
    ("E045","Alicia",  "Bernard",  "Lycée Jean Moulin","Technologique","8.5","9.5","8.0","8.0","8.5","9.0"),
    ("E046","Florian", "Martin",   "Lycée Jean Moulin","Technologique","15.5","14.0","15.0","13.5","16.0","15.0"),
    ("E047","Noémie",  "Dubois",   "Lycée Jean Moulin","Technologique","7.0","8.5","7.5","7.5","6.5","8.0"),
    ("E048","Quentin", "Robert",   "Lycée Jean Moulin","Technologique","13.0","12.0","13.5","11.5","12.5","13.0"),

    # ── Lycée Jean Moulin ── Professionnelle ───────────────────────────────
    ("E049","Elisa",   "Laurent",  "Lycée Jean Moulin","Professionnelle","9.5","11.0","10.5","10.0","9.0","10.5"),
    ("E050","Valentin","Michel",   "Lycée Jean Moulin","Professionnelle","12.0","11.5","11.0","11.5","12.5","11.5"),
    ("E051","Fatoumata","Garcia",  "Lycée Jean Moulin","Professionnelle","8.5","10.0","9.0","9.5","8.0","9.0"),
    ("E052","Corentin","Lefebvre", "Lycée Jean Moulin","Professionnelle","14.0","13.5","13.0","13.0","14.5","13.5"),
    ("E053","Melissa", "Dupont",   "Lycée Jean Moulin","Professionnelle","7.0","8.5","8.0","7.5","7.0","8.0"),
    ("E054","Bastien", "Bonnet",   "Lycée Jean Moulin","Professionnelle","11.0","10.5","11.5","10.5","10.0","11.0"),

    # ── Lycée Simone Veil ── Générale ──────────────────────────────────────
    ("E055","Céleste", "Mercier",  "Lycée Simone Veil","Générale",  "17.5","16.0","18.0","15.5","17.0","17.5"),
    ("E056","Théodore","Morin",    "Lycée Simone Veil","Générale",  "11.0","12.5","11.5","11.0","10.5","11.5"),
    ("E057","Laure",   "Fournier", "Lycée Simone Veil","Générale",  "14.5","14.0","15.0","13.5","14.0","14.5"),
    ("E058","Sacha",   "Girard",   "Lycée Simone Veil","Générale",  "","11.0","10.0","9.5","8.5","9.0"),           # maths manquante
    ("E059","Margot",  "Thomas",   "Lycée Simone Veil","Générale",  "16.0","15.5","16.5","14.5","15.5","16.0"),
    ("E060","Liam",    "Petit",    "Lycée Simone Veil","Générale",  "9.0","10.5","10.0","9.0","8.5","9.5"),

    # ── Lycée Simone Veil ── Technologique ─────────────────────────────────
    ("E061","Iris",    "Durand",   "Lycée Simone Veil","Technologique","12.5","11.5","13.0","11.0","12.0","12.5"),
    ("E062","Ethan",   "Leroy",    "Lycée Simone Veil","Technologique","15.0","13.5","14.5","12.5","15.5","14.5"),
    ("E063","Chiara",  "Moreau",   "Lycée Simone Veil","Technologique","8.0","9.0","8.5","8.0","7.5","8.5"),
    ("E064","Mehdi",   "Simon",    "Lycée Simone Veil","Technologique","16.5","15.0","15.5","14.0","17.0","16.0"),
    ("E065","Apolline","Bernard",  "Lycée Simone Veil","Technologique","7.5","8.5","8.0","7.0","7.0","8.0"),
    ("E066","Sébastien","Martin",  "Lycée Simone Veil","Technologique","13.5","12.5","14.0","12.0","13.0","13.5"),

    # ── Lycée Simone Veil ── Professionnelle ───────────────────────────────
    ("E067","Louna",   "Dubois",   "Lycée Simone Veil","Professionnelle","10.0","11.5","10.5","11.0","9.5","10.5"),
    ("E068","Erwann",  "Robert",   "Lycée Simone Veil","Professionnelle","8.0","9.5","8.5","9.0","7.5","8.5"),
    ("E069","Tiana",   "Laurent",  "Lycée Simone Veil","Professionnelle","13.0","12.5","12.0","12.5","13.5","12.5"),
    ("E070","Nolan",   "Michel",   "Lycée Simone Veil","Professionnelle","6.5","8.0","7.5","7.0","6.0","7.5"),
    ("E071","Salomé",  "Garcia",   "Lycée Simone Veil","Professionnelle","11.5","11.0","12.0","10.5","11.0","11.5"),
    ("E072","Killian", "Lefebvre", "Lycée Simone Veil","Professionnelle","9.5","10.5","9.5","10.0","9.0","10.0"),

    # ── Doublons intentionnels (même contenu, à détecter) ──────────────────
    ("E008","Léa",     "Simon",    "Lycée Victor Hugo","Technologique","13.5","12.0","11.0","13.0","14.0","13.0"),  # doublon E008
    ("E024","Noa",     "Simon",    "Lycée Marie Curie","Générale",  "19.0","18.0","17.5","16.0","19.5","18.5"),    # doublon E024
]


def main():
    fichier = "notes_brutes.csv"
    colonnes = [
        "id_eleve", "prenom", "nom", "etablissement", "filiere",
        "maths", "francais", "anglais", "histoire", "svt", "physique",
    ]
    with open(fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(colonnes)
        writer.writerows(ELEVES)
    print(f"{len(ELEVES)} lignes écrites dans {fichier}")
    print("Pensez à inspecter le fichier : il contient des défauts intentionnels.")


if __name__ == "__main__":
    main()
