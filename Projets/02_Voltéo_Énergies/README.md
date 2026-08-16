# Projet de nettoyage de données de production énergétique

## Objectif

Ce projet a pour objectif de collecter des données de production énergétique,
puis de les nettoyer afin d'obtenir un fichier homogène, exploitable et sans doublons.

Le résultat final est le fichier :

`production_propre.csv`

---

## Exécution des scripts

### 1. Générer les données brutes

```bash
python collecte.py
```

Ce script crée :

```text
production_brute.csv
```

### 2. Nettoyer les données

```bash
python nettoyage.py
```

Ce script crée :

```text
production_propre.csv
```

---

## Contrôles appliqués

Le script `nettoyage.py` applique les règles suivantes :

1. Normalisation des noms des sites
2. Conversion des séparateurs décimaux (, → .)
3. Gestion des valeurs manquantes
4. Suppression des productions négatives
5. Conversion des MW vers kW
6. Suppression des doublons stricts
7. Suppression des doublons de même site et même horodatage

---

## Répartition du travail

**Membre 1**
- collecte des données
- création de `collecte.py`

**Membre 2**
- nettoyage des données
- création de `nettoyage.py`

Travail commun :
- vérification qualité
- rédaction du README
- suivi du projet (`suivi.md`)