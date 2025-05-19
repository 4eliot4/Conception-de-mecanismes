
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



    def __init__(self, L, b, t):

        E_p = 114 * 10 ** 9
        nu_p = 0.34
        G_p = E_p / (2*(1+nu_p))

        self.L = L
        self.b = b
        self.h = t

        self.rz_p = self.b*self.h**3*G_p/(3*self.L)

        self.kx_p = (E_p*self.b*self.h**3)/(self.L**3)
        self.ky_p = (E_p*self.h*self.b**3)/(self.L**3)
        self.kz_p = (self.b*self.h*E_p)/(self.L**2)

        self.k_simple = E_p*self.b*self.h**3/(12*self.L)

        self.rx_p = E_p*self.h*self.b**3/(12*self.L)
