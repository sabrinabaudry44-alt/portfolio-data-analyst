# Challenge 2 

"""
modeles.py

Classes Eleve et Promotion.
"""

class Eleve:

    def __init__(
        self,
        identifiant,
        prenom,
        nom,
        etablissement,
        filiere,
        maths=None,
        francais=None,
        anglais=None,
        histoire=None,
        svt=None,
        physique=None
    ):

        self.identifiant = identifiant
        self.prenom = prenom
        self.nom = nom
        self.etablissement = etablissement
        self.filiere = filiere

        self.maths = maths
        self.francais = francais
        self.anglais = anglais
        self.histoire = histoire
        self.svt = svt
        self.physique = physique

    # =====================================================
    # CONSTRUCTEUR ALTERNATIF
    # =====================================================

    @classmethod
    def depuis_dict(cls, d):

        def parse(val):
            try:
                return float(str(val).replace(",", ".")) if str(val).strip() else None
            except (ValueError, TypeError):
                return None

        return cls(
            identifiant=str(d.get("id_eleve", "")).strip(),
            prenom=str(d.get("prenom", "")).strip(),
            nom=str(d.get("nom", "")).strip(),
            etablissement=str(d.get("etablissement", "")).strip(),
            filiere=cls.normaliser_filiere(d.get("filiere", "")),
            maths=parse(d.get("maths")),
            francais=parse(d.get("francais")),
            anglais=parse(d.get("anglais")),
            histoire=parse(d.get("histoire")),
            svt=parse(d.get("svt")),
            physique=parse(d.get("physique")),
        )

    # =====================================================
    # MÉTHODES STATIQUES
    # =====================================================

    @staticmethod
    def normaliser_filiere(filiere_brute):

        if not filiere_brute:
            return "Inconnue"

        correspondances = {
            "générale": "Générale",
            "technologique": "Technologique",
            "professionnelle": "Professionnelle",
        }

        return correspondances.get(
            filiere_brute.strip().lower(),
            filiere_brute.strip().capitalize()
        )

    @staticmethod
    def est_note_valide(note):

        try:
            return 0 <= float(note) <= 20
        except (TypeError, ValueError):
            return False

    # =====================================================
    # MÉTHODES
    # =====================================================

    def notes(self):

        toutes = [
            self.maths,
            self.francais,
            self.anglais,
            self.histoire,
            self.svt,
            self.physique
        ]

        return [n for n in toutes if n is not None]

    def moyenne(self):

        notes = self.notes()

        if not notes:
            return None

        return round(sum(notes) / len(notes), 2)

    def est_admis(self, seuil=10.0):

        moyenne = self.moyenne()

        return moyenne is not None and moyenne >= seuil

    def bulletin(self):

        print("=" * 50)
        print(f"{self.prenom} {self.nom}")
        print(self.filiere)
        print(f"Moyenne : {self.moyenne()}")
        print(f"Admis : {self.est_admis()}")

    # =====================================================
    # MÉTHODES SPÉCIALES
    # =====================================================

    def __repr__(self):

        return (
            f"Eleve(id='{self.identifiant}', "
            f"nom='{self.nom}', "
            f"filiere='{self.filiere}')"
        )

    def __str__(self):

        moyenne = self.moyenne()

        if moyenne is None:
            moyenne = "N/A"
        else:
            moyenne = f"{moyenne}/20"

        return (
            f"{self.prenom} {self.nom} | "
            f"{self.filiere} | "
            f"moy. {moyenne}"
        )

    def __eq__(self, other):

        if not isinstance(other, Eleve):
            return NotImplemented

        return self.identifiant == other.identifiant

    def __lt__(self, other):

        return (self.moyenne() or 0) < (other.moyenne() or 0)


# ==========================================================
# PROMOTION
# ==========================================================

class Promotion:

    def __init__(self, nom, etablissement, filiere):

        self.nom = nom
        self.etablissement = etablissement
        self.filiere = filiere

        self._eleves = []

    def ajouter(self, eleve):

        self._eleves.append(eleve)

    def __len__(self):

        return len(self._eleves)

    def __iter__(self):

        return iter(self._eleves)

    def __contains__(self, eleve):

        return eleve in self._eleves

    def __repr__(self):

        return (
            f"Promotion('{self.nom}', "
            f"{len(self)} élève(s))"
        )

    def __str__(self):

        return (
            f"{self.nom} - "
            f"{self.etablissement}"
        )

    def moyenne_generale(self):

        moyennes = [
            e.moyenne()
            for e in self
            if e.moyenne() is not None
        ]

        if not moyennes:
            return None

        return round(sum(moyennes) / len(moyennes), 2)

    def taux_admission(self, seuil=10):

        eleves = [
            e for e in self
            if e.moyenne() is not None
        ]

        if not eleves:
            return 0

        admis = sum(
            1 for e in eleves
            if e.est_admis(seuil)
        )

        return round(admis / len(eleves) * 100, 1)

    def classement(self):

        return sorted(
            self._eleves,
            reverse=True
        )

    def rapport(self):

        print("=" * 50)
        print(self)
        print(f"Moyenne : {self.moyenne_generale()}")
        print(f"Taux admission : {self.taux_admission()} %")

        print("\nTop 3")

        for i, eleve in enumerate(self.classement()[:3], start=1):
            print(i, eleve)


# ==========================================================
# TEST RAPIDE
# ==========================================================

if __name__ == "__main__":

    d = {
        "id_eleve": "E001",
        "prenom": "Lucas",
        "nom": "Martin",
        "etablissement": "Lycée Victor Hugo",
        "filiere": "GÉNÉRALE",
        "maths": "15.5",
        "francais": "14",
        "anglais": "13",
        "histoire": "12",
        "svt": "16",
        "physique": "17",
    }

    eleve = Eleve.depuis_dict(d)

    print(eleve)
    print(Eleve.normaliser_filiere("GÉNÉRALE"))
    print(Eleve.est_note_valide(18))