from dataclasses import dataclass, asdict

# ------------------------------------------------------------------
C2_TABLE = {
    1.0: 0.1406,
    1.2: 0.1661,
    1.5: 0.1958,
    2.0: 0.2290,
    2.5: 0.2490,
    3.0: 0.2630,
}

def c2_from_ratio(r):
    if r >= 3.0:
        return 1.0 / 3.0
    keys = sorted(C2_TABLE)
    if r <= keys[0]:
        return C2_TABLE[keys[0]]
    for k1, k2 in zip(keys[:-1], keys[1:]):
        if k1 <= r <= k2:
            c1, c2 = C2_TABLE[k1], C2_TABLE[k2]
            return c1 + (c2 - c1) * (r - k1) / (k2 - k1)

# ------------------------------------------------------------------
@dataclass
class Soufflet:
    E : float
    nu: float
    L : float
    b : float
    t : float
    h : float

    @property
    def G(self):
        return self.E / (2 * (1 + self.nu))

    @property
    def Iy(self):
        return self.t * self.b**3 / 12

    @property
    def Iz(self):
        return self.b * self.t**3 / 12

    @property
    def A(self):
        return self.b * self.t

    @property
    def C2(self):
        ratio = max(self.b, self.t) / min(self.b, self.t)
        return c2_from_ratio(ratio)

    @property
    def k_torsion_lamella(self):
        a = max(self.b, self.t)
        b_small = min(self.b, self.t)
        return self.C2 * a * b_small**3 * self.G / self.L

    def stiffness(self):
        """Raideur complète du soufflet (dict, unités SI)."""
        k_ax  = self.E * self.Iz      / (2*self.L)          
        k_y   = 12 * self.E * self.Iz / self.L**3       
        k_z   = self.b * self.t**3 * self.G / (6 * self.L**3)       
        k_tx  = self.b * self.t**3 * self.G / (6 * self.L**3)     
        k_ty  = self.E * self.Iy / (2 * self.L)                    
        k_tz  = self.E * self.Iz / (2*self.L)    

        return dict(
            k_axial_x = k_ax,
            k_y = k_y,
            k_z = k_z,
            k_theta_x = k_tx,
            k_theta_y = k_ty,
            k_theta_z = k_tz
        )

    def summary(self):
        """Retourne toutes les données + raideurs (dict)."""
        return {**asdict(self), **self.stiffness()}

# ------------------------------------------------------------------
# Exemple d’utilisation
if __name__ == "__main__":
    s = Soufflet(E=210e9, nu=0.3, L=0.02, b=0.008, t=0.0008, h=0.03)
    ratio = max(s.b, s.t) / min(s.b, s.t)
    print(f"ratio a/b = {ratio:.2f}  →  C2 = {s.C2:.4f}")
    for k, v in s.stiffness().items():
        u = "N/m" if "k_" in k and "theta" not in k else "N·m/rad"
        print(f"{k:>11s} : {v:9.3e}  {u}")

    s = Soufflet(E=210e9, nu=0.3, L=0.3, b=0.030, t=0.001, h=0.03)
    print("SSS")
    raideurs = s.stiffness()
    for nom, valeur in raideurs.items():
        unite = "N/m" if "k_" in nom and "theta" not in nom else "N·m/rad"
        print(f"{nom} : {valeur:.3e} {unite}")