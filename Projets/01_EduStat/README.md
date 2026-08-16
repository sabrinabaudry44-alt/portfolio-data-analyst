# Challenge 5

# EduStat

## Description

EduStat est un projet Python orienté objet permettant d'analyser les résultats scolaires de plusieurs établissements.

Le projet permet :

- de charger un fichier CSV contenant les notes des élèves ;
- de créer des objets `Eleve` et `Promotion` ;
- d'analyser les résultats par filière ;
- de profiler la qualité des données.

---

## Arborescence

```text
EduStat/
│
├── main.py
├── notes.py
├── notes_brutes.csv
│
└── edustat/
    ├── __init__.py
    ├── modeles.py
    ├── analyseurs.py
    ├── utils.py
    └── profiler.py
```

---

## Installation

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## Exécution

Générer les données :

```bash
python notes.py
```

Lancer le projet :

```bash
python main.py
```

---

## Résultats

Le projet affiche :

- les statistiques par filière ;
- les moyennes générales ;
- le taux d'admission ;
- le profil du jeu de données ;
- les doublons ;
- les valeurs manquantes ;
- les moyennes par matière ;
- les moyennes par établissement.

Un fichier `profil_edustat.csv` est également généré.