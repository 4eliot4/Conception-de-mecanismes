E_p = 114 * 10 ** 9
nu_p = 0.34
G_p = E_p / (2*(1+nu_p))

class Pivot(object):
    '''
     __
    |  |        ↑ z
    |  |        → x
    |  |        o y
    |  |
    |  |  L     longueur: L
    |  |        epaisseur: h
    |  |        largeur: b
    |  |
    |__|
     h


    '''

    def __init__(self, L, b, h):

        self.L = L
        self.b = b
        self.h = h

        self.rz_p = self.b*self.h**3*G_p/(3*self.L)

        self.kx_p = (E_p*self.b*self.h**3)/(self.L**3)
        self.ky_p = (E_p*self.h*self.b**3)/(self.L**3)
        self.kz_p = (self.b*self.h*E_p)/(self.L**2)

        self.k_simple = E_p*self.b*self.h**3/(12*self.L)

p = Pivot(10.0e-3, 2e-3, 100e-6)
print(p.k_simple/((18e-3)**2))

