from dataclasses import dataclass, asdict

# ------------------------------------------------------------------
# Tableau C2 (torsion rectangulaire)  :   ratio a/b  ->  C2
C2_TABLE = {
    1.0: 0.1406,
    1.2: 0.1661,
    1.5: 0.1958,
    2.0: 0.2290,
    2.5: 0.2490,
    3.0: 0.2630,
}

def c2_from_ratio(r):
    """Renvoie le coefficient C2 (torsion) pour un ratio a/b donné.
       - Interpolation linéaire entre les points connus.
       - Si a/b ≥ 3  →  C2 = 1/3 (plaque mince)."""
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
    """Modèle 2‑lames pour guidage flexible type 'soufflet'.

    E  : module de Young (Pa)
    nu : Poisson
    L  : longueur libre d'une lame (m)
    b  : largeur de la lame (dans z) (m)
    t  : épaisseur de la lame (dans y) (m)
    h  : distance verticale entre les deux lames (m)
    """
    E : float
    nu: float
    L : float
    b : float
    t : float
    h : float

    # ---------------- modules --------------------------------------
    @property
    def G(self):
        return self.E / (2 * (1 + self.nu))

    # ---------------- inerties de section --------------------------
    @property
    def Iy(self):                    # flexion dans x‑y  (flèche z)
        return self.t * self.b**3 / 12   # b^3 car flèche = z

    @property
    def Iz(self):                    # flexion dans x‑z  (flèche y)
        return self.b * self.t**3 / 12   # t^3 car flèche = y

    @property
    def A(self):
        return self.b * self.t

    # ---------------- torsion (C2) ---------------------------------
    @property
    def C2(self):
        ratio = max(self.b, self.t) / min(self.b, self.t)
        return c2_from_ratio(ratio)

    @property
    def k_torsion_lamella(self):
        a = max(self.b, self.t)
        b_small = min(self.b, self.t)
        return self.C2 * a * b_small**3 * self.G / self.L   # N·m/rad

    # ---------------- raideur d'une lame ---------------------------
    def _k_lamella(self):
        k_ax  = self.E * self.A      / self.L          # traction (x)
        k_y   = 3 * self.E * self.Iz / self.L**3       # flèche y (flex hors‑plan)
        k_z   = 3 * self.E * self.Iy / self.L**3       # flèche z (flex in‑plane)
        k_tx  = self.k_torsion_lamella                 # torsion autour x
        k_ty  = k_z * self.h**2                        # rotation autour y
        k_tz  = k_y * self.h**2                        # rotation autour z
        return dict(k_ax=k_ax, k_y=k_y, k_z=k_z,
                    k_theta_x=k_tx, k_theta_y=k_ty, k_theta_z=k_tz)

    # ---------------- assemblage 2 lames ---------------------------
    def stiffness(self):
        """Raideur du soufflet complet (dict, unités SI)."""
        k = self._k_lamella()
        return {
            # translations
            "k_axial_x" : k["k_ax"] / 2,   # lames en série (traction)
            "k_y"       : 2 * k["k_y"],    # lames en parallèle (flèche y)
            "k_z"       : k["k_z"] / 2,    # lames en série (flèche z)
            # rotations
            "k_theta_x" : 2 * k["k_theta_x"],
            "k_theta_y" : 2 * k["k_theta_y"],
            "k_theta_z" : 2 * k["k_theta_z"],
        }

    def summary(self):
        """Retourne toutes les données + raideurs (dict)."""
        return {**asdict(self), **self.stiffness()}

