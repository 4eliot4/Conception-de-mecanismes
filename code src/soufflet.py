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
        k_ax  = 2 * self.E * self.Iz / (self.L * self.h**2)
        k_y   = 6 * self.E * self.Iz / self.L**3
        k_z   = 2* self.b * self.t**3 * self.G / (3 * self.L * self.h**2)
        k_tx  = self.b * self.t**3 * self.G / (6 * self.L)
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
