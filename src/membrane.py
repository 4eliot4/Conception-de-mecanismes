class Membrane(object):
    def __init__(self, R_int, t):
        self.R = R_int
        self.h = t
        self.b = 10 * t
        self.L = 100 * t
        self.E_m = 114 * 10 ** 9
        self.G_m = 80e9  # module de cisaillement (Pa), typique acier

        # rigidité en z
        self.kz_m = 3*(self.E_m*self.b*self.h**3)/(self.L**3)

        # calcul intermédiaire pour rigidité en rotation
        self.k_torsion = (self.G_m * self.b*self.h**3) / (3*self.L)  # N·m/rad
        self.k_flex_pure = (self.E_m*self.b*self.h**3)/(12*self.L)
        self.k_flex_s = (self.E_m*self.b*self.h**3)/(self.L**3)

        # rigidité en rotation
        self.rx = (3/2)*(self.k_torsion + self.k_flex_pure + (self.k_flex_s * self.R ** 2))
        self.ry = self.rx

        # rigidité en translation en x et y
        self.kx_m = ((3*self.b*self.h*self.E_m)/(2*self.L))*(1+(self.b**2)/self.L**2)
        self.ky_m = self.kx_m
