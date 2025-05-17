class Pivot:
    def __init__(self, E, G, b, e, r):
        self.E = E  # Module de Young
        self.G = G  # Module de cisaillement
        self.b = b  # Largeur
        self.e = e  # Epaisseur
        self.r = r  # Rayon de raccordement

        # Vérification des contraintes
        erreurs = []
        if (r/e) <= 5:
            erreurs.append("Le rapport r/e doit être supérieur à 5.")
        if not (1e-6 <= e <= 1e-3):
            erreurs.append("L'épaisseur e doit être comprise entre 10^-6 et 10^-3 m.")
        if not (1e-4 <= r <= 1):
            erreurs.append("Le rayon r doit être compris entre 10^-4 et 1 m.")

        if erreurs:
            for erreur in erreurs:
                print(f"Erreur : {erreur}")

    def rigidite_angulaire(self):
        from math import pi, sqrt
        K_alphaM = (2 * self.E * self.b * self.e**2.5) / (9 * pi * sqrt(self.r))
        return K_alphaM

    def rigidite_angulaire_transverse(self):
        from math import sqrt
        Kt_alphaM = 0.0295 * (self.E * self.b**3 * sqrt(self.e)) / sqrt(self.r)
        return Kt_alphaM

    def rigidite_equivalente_flexion(self):
        K_alphaM = self.rigidite_angulaire()
        Kt_alphaM = self.rigidite_angulaire_transverse()

        # Maintenant les deux en série :
        K_equivalente_flexion = 1 / (1/K_alphaM + 1/Kt_alphaM)

        return K_equivalente_flexion

    def rigidite_torsion(self):
        from math import sqrt
        K_tors = 0.284 * (self.G * self.b * self.e**2.5) / sqrt(self.r)
        return K_tors

    def rigidite_equivalente_torsion(self):
        K_tors = self.rigidite_torsion()

        # Deux cols identiques en série :
        K_equivalente_torsion = 1 / (1/K_tors + 1/K_tors)

        return K_equivalente_torsion

    def deplacement_angulaire_en_flexion(self, moment_applique):
        # Calcul du déplacement angulaire en radians sous un moment donné en flexion
        K_eq = self.rigidite_equivalente_flexion()
        alpha = moment_applique / K_eq
        return alpha

    def moment_applique_en_flexion(self, deplacement_angulaire):
        # Calcul du moment appliqué en flexion en Nm pour un déplacement angulaire donné (en radians)
        K_eq = self.rigidite_equivalente_flexion()
        moment = deplacement_angulaire * K_eq
        return moment

    def contrainte(self, deplacement_angulaire): # la formule est fausse 
        from math import pi, sqrt
        sigma_adm = (4 * self.E * sqrt(self.e) * deplacement_angulaire) / (3 * pi * sqrt(self.r))
        return sigma_adm

# Exemple d'utilisation :
if __name__ == "__main__":
    pivot = Pivot(E=210e9, G=80e9, b=0.02, e=50*10**(-6), r=3*10**(-3))
    rigidite_eq_flexion = pivot.rigidite_equivalente_flexion()
    print(f"Rigidité équivalente en flexion du pivot : {rigidite_eq_flexion:.2e} Nm/rad")

    rigidite_eq_torsion = pivot.rigidite_equivalente_torsion()
    print(f"Rigidité équivalente en torsion du pivot : {rigidite_eq_torsion:.2e} Nm/rad")

    moment = 10  # Nm par exemple
    deplacement = pivot.deplacement_angulaire_en_flexion(moment)
    print(f"Déplacement angulaire sous {moment} Nm en flexion : {deplacement:.4e} rad")

    deplacement_donne = 0.01  # radian par exemple
    moment_calcule = pivot.moment_applique_en_flexion(deplacement_donne)
    print(f"Moment nécessaire pour un déplacement de {deplacement_donne:.4e} rad en flexion : {moment_calcule:.2e} Nm")

    contrainte = pivot.contrainte(deplacement_donne) 
    print(f"Contrainte pour un déplacement de {deplacement_donne:.4e} rad : {contrainte:.2e} Pa")
