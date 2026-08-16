    # Challenge 3

"""
analyseurs.py

Analyseurs des promotions EduStat.
"""

from .modeles import Promotion


# ==========================================================
# CLASSE MÈRE
# ==========================================================

class AnalyseurPromotion:

    SEUIL_ADMISSION = 10.0

    def __init__(self, promotion: Promotion):
        self.promotion = promotion
        self._stats = {}

    def analyser(self):

        self._stats = {
            "nb_eleves": len(self.promotion),
            "moyenne": self.promotion.moyenne_generale(),
            "taux_admission": self.promotion.taux_admission(
                self.SEUIL_ADMISSION
            ),
        }

        return self

    def rapport(self):

        print("\n" + "=" * 60)
        print(type(self).__name__)
        print("=" * 60)

        print(f"Nombre d'élèves : {self._stats['nb_eleves']}")
        print(f"Moyenne générale : {self._stats['moyenne']}")
        print(f"Taux admission : {self._stats['taux_admission']} %")

    def top_n(self, n=3):
        return self.promotion.classement()[:n]


# ==========================================================
# FILIÈRE GÉNÉRALE
# ==========================================================

class AnalyseurGenerale(AnalyseurPromotion):

    def analyser(self):

        super().analyser()

        maths = []
        sciences = []
        lettres = []

        for e in self.promotion:

            if e.maths is not None:
                maths.append(e.maths)

            notes_sciences = []

            if e.svt is not None:
                notes_sciences.append(e.svt)

            if e.physique is not None:
                notes_sciences.append(e.physique)

            if notes_sciences:
                sciences.append(sum(notes_sciences) / len(notes_sciences))

            notes_lettres = []

            if e.francais is not None:
                notes_lettres.append(e.francais)

            if e.histoire is not None:
                notes_lettres.append(e.histoire)

            if notes_lettres:
                lettres.append(sum(notes_lettres) / len(notes_lettres))

        self._stats["moy_maths"] = round(sum(maths) / len(maths), 2) if maths else None
        self._stats["moy_sciences"] = round(sum(sciences) / len(sciences), 2) if sciences else None
        self._stats["moy_lettres"] = round(sum(lettres) / len(lettres), 2) if lettres else None

        return self

    def rapport(self):

        super().rapport()

        print(f"Moyenne Maths : {self._stats['moy_maths']}")
        print(f"Moyenne Sciences : {self._stats['moy_sciences']}")
        print(f"Moyenne Lettres : {self._stats['moy_lettres']}")


# ==========================================================
# FILIÈRE TECHNOLOGIQUE
# ==========================================================

class AnalyseurTechno(AnalyseurPromotion):

    def __init__(self, promotion, matiere_dominante="maths"):
        super().__init__(promotion)
        self.matiere_dominante = matiere_dominante

    def analyser(self):

        super().analyser()

        notes = []

        for e in self.promotion:

            note = getattr(e, self.matiere_dominante)

            if note is not None:
                notes.append(note)

        self._stats["moy_matiere"] = (
            round(sum(notes) / len(notes), 2)
            if notes else None
        )

        return self

    def rapport(self):

        super().rapport()

        print(
            f"Moyenne {self.matiere_dominante} : "
            f"{self._stats['moy_matiere']}"
        )


# ==========================================================
# FILIÈRE PROFESSIONNELLE
# ==========================================================

class AnalyseurPro(AnalyseurPromotion):

    SEUIL_ADMISSION = 8.0

    def analyser(self):

        super().analyser()

        self._stats["taux_admission"] = (
            self.promotion.taux_admission(self.SEUIL_ADMISSION)
        )

        return self

    def rapport(self):

        super().rapport()

        print(f"Seuil d'admission : {self.SEUIL_ADMISSION}/20")