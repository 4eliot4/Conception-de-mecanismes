class Membrane(object):
    def __init__(self,F ,D_int, h = 200*10**(-6)):
        '''
        F ~ N/mm
        mu defaut = 200µm peut descendre jusqu'à 60µm maif le mieux c'est 200
        D = diamètre mesuré a l'extrémité la plus proche de l'axe des lames
        '''
        self.F = F
        self.D = D_int
        self.h = h
        intervalle_b = [1, 100]
        intervalle_L = [60, 100]
        internalF = F/3  # force sur chaque lame
        self.E_m = 200 * 10 ** 9
        self.G_m = 80e9  # module de cisaillement (Pa), typique acier

        best_dim = (0, 0, 0, 1e6)  # coeff b, coeff L, K, erreur

        #Recherche du meilleur dimensionnement pour les lames en fonction
        #de la force choisie pour un déplacement d'1mm
        for cb in range(intervalle_b[0], intervalle_b[1]):
            for cL in range(intervalle_L[0], intervalle_L[1]):
                b = cb * self.h
                L = cL * self.h
                K = (12 * self.E_m * b * self.h) / (L ** 3)  # rigidité flexion

                # déplacement sous charge
                x = (internalF / K) * 1000  # en mm

                err = abs(1 - x)
                if best_dim[3] >= err:
                    best_dim = (cb, cL, K, err)

        self.coeff_b = best_dim[0]
        self.coeff_L = best_dim[1]
        self.kz_m = best_dim[2] * 3  # rigidité totale des 3 lames
        self.err = best_dim[3] / 1000
        self.I = (self.coeff_b * self.h ** 4) / 12  # moment d'inertie

        # Stockage de dimensions
        self.b = self.coeff_b * self.h
        self.L = self.coeff_L * self.h

        # Calcul du module de torsion J sans inverser b et h
        ratio = self.b / self.h
        kappa = (1 / 3) * (1 - 0.63 * (1 / ratio) + 0.052 * (1 / ratio) ** 5)
        self.J = kappa * self.h * self.b ** 3  # mm⁴ si dimensions en mm

        # Rigidité en torsion
        self.k_torsion = (self.G_m * self.J) / self.L  # N·m/rad
        self.k_flex_pure = (self.E_m*self.b*self.h**3)/(12*self.L)
        self.k_flex_simple = (self.E_m*self.b*self.h**3)/(4*self.L**3)

        self.rx = (3/2)*(self.k_torsion + self.k_flex_pure + (self.k_flex_simple*self.D**2)/4)
        self.ry = self.rx

        if internalF-self.kz_m*0.001 > internalF*0.10 :
            print(f"\033[93mbelek le dimensionnement de la lame fait qu'il y a une erreur d'au moins 10% : {self.F - self.kz_m * 0.001}")
