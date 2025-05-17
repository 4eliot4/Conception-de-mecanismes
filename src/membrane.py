class Membrane(object):
    def __init__(self, F, R_int, bt, Lt, h =200 * 10 ** (-6)):
        '''
        F ~ N/mm
        mu defaut = 200µm peut descendre jusqu'à 60µm maif le mieux c'est 200
        D = diamètre mesuré a l'extrémité la plus proche de l'axe des lames
        D_int = 5.5mm
        dimensions choisies : h = 0.1mm | b = 1.0mm | L = 24.3mm | k = 0.5017803795090455 N/mm| err = 3.5481249999997912e-06
        h = 100e-6, cb = 10, cL = 243
        '''
        self.F = F
        self.R = R_int
        self.h = h
        self.bt = bt
        self.Lt = Lt
        intervalle_b = [10,10]
        intervalle_L = [100, 100]
        internalF = F/3  # force sur chaque lame
        self.E_m = 114 * 10 ** 9
        self.G_m = 80e9  # module de cisaillement (Pa), typique acier

        best_dim = (0, 0, 0, 1e6)  # coeff b, coeff L, K, erreur

        #Recherche du meilleur dimensionnement pour les lames en fonction
        #de la force choisie pour un déplacement d'1mm
        for cb in range(intervalle_b[0], intervalle_b[1]+1):
            b = cb * self.h
            for cL in range(intervalle_L[0],intervalle_L[1]+1):

                L = cL * self.h
                #K = (12 * self.E_m * b * self.h**3) / (L ** 3)  # rigidité flexion
                K = (self.E_m*b*self.h**3)/(L**3)
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


        # Rigidité en torsion
        self.k_torsion = (self.G_m * self.b*self.h**3) / (3*self.L)  # N·m/rad
        self.k_flex_pure = (self.E_m*self.b*self.h**3)/(12*self.L)
        self.k_flex_s = (self.E_m*self.b*self.h**3)/(self.L**3)
        self.k_tige_rot = ((self.bt**4)*self.G_m)/(3*self.Lt)


        self.rx = (3/2)*(self.k_torsion + self.k_flex_pure + (self.k_flex_s * self.R ** 2)) #+self.k_tige_rot
        self.ry = self.rx

        self.kx_m = ((3*self.b*self.h*self.E_m)/(2*self.L))*(1+(self.b**2)/self.L**2)
        self.ky_m = self.kx_m

        if self.err*1000 >= 0.1:
            print(f"\033[93mbelek le dimensionnement de la lame fait qu'il y a une erreur d'au moins 10% : {self.err*1000}mm\033[00m")

    def print_dim(self):
        print(f"h = {self.h*1000}mm | b = {self.b*1000}mm | L = {self.L*1000}mm | k = {self.kz_m / 1000} N/mm| err = {self.err*1000} mm")

F = 0.5
s = Membrane(0.5, 7.5e-3, 300e-6, 15e-3, 100e-6)
s.print_dim()
print(s.coeff_b,s.coeff_L)
print(s.kz_m, s.ky_m,s.ry)