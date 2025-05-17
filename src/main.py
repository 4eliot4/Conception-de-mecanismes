import tkinter as tk
from tkinter import ttk, messagebox

from membrane import Membrane
from pivot import Pivot
from soufflet import Soufflet

class RigiditeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calcul de rigidité - Membrane | Pivot | Soufflet")

        self.tabControl = ttk.Notebook(root)

        self.tabs = {
            "Membrane": self.create_membrane_tab,
            "Pivot": self.create_pivot_tab,
            "Soufflet": self.create_soufflet_tab
        }

        self.inputs = {}

        for name, create_tab_func in self.tabs.items():
            frame = ttk.Frame(self.tabControl)
            self.tabControl.add(frame, text=name)
            create_tab_func(frame)

        self.tabControl.pack(expand=1, fill="both")

        self.result_box = tk.Text(root, height=10, width=80)
        self.result_box.pack(pady=10)

        calc_button = ttk.Button(root, text="Calculer rigidités totales", command=self.calculate_total)
        calc_button.pack()

        self.results = {}

    def create_membrane_tab(self, frame):
        labels = ["F (N/mm)", "R_int (m)", "bt (m)", "Lt (m)", "h (m)","D_m (m)"]
        defaults = [0.5, 7.5e-3, 300e-6, 15e-3, 100e-6, 18e-3]
        self.create_inputs(frame, "Membrane", labels, defaults)

    def create_pivot_tab(self, frame):
        labels = ["L (m)", "b (m)", "h (m)"]
        defaults = [10.0e-3, 2.0e-3, 100e-6]
        self.create_inputs(frame, "Pivot", labels, defaults)

    def create_soufflet_tab(self, frame):
        labels = ["E (Pa)", "nu", "L (m)", "b (m)", "t (m)", "h (m)"]
        defaults = [114e9, 0.34, 0.011, 0.012, 0.0002, 0.05]
        self.create_inputs(frame, "Soufflet", labels, defaults)

    def create_inputs(self, frame, section, labels, defaults):
        self.inputs[section] = []
        for i, (label, default) in enumerate(zip(labels, defaults)):
            ttk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entry = ttk.Entry(frame)
            entry.insert(0, str(default))
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.inputs[section].append(entry)

    def calculate_total(self):
        self.result_box.delete("1.0", tk.END)

        try:
            # Membrane
            F = float(self.inputs["Membrane"][0].get())
            R_int = float(self.inputs["Membrane"][1].get())
            bt = float(self.inputs["Membrane"][2].get())
            Lt = float(self.inputs["Membrane"][3].get())
            h_m = float(self.inputs["Membrane"][4].get())
            D_m = float(self.inputs["Membrane"][5].get())
            membrane = Membrane(F, R_int, bt, Lt, h_m)

            # Pivot
            L_p = float(self.inputs["Pivot"][0].get())
            b_p = float(self.inputs["Pivot"][1].get())
            h_p = float(self.inputs["Pivot"][2].get())
            pivot = Pivot(L_p, b_p, h_p)

            # Soufflet
            E = float(self.inputs["Soufflet"][0].get())
            nu = float(self.inputs["Soufflet"][1].get())
            L_s = float(self.inputs["Soufflet"][2].get())
            b_s = float(self.inputs["Soufflet"][3].get())
            t_s = float(self.inputs["Soufflet"][4].get())
            h_s = float(self.inputs["Soufflet"][5].get())
            soufflet = Soufflet(E, nu, L_s, b_s, t_s, h_s)

            # pov le calcul est la
            rigidite = 4 * membrane.rx/(D_m**2) + 2 * pivot.kx_p + 2 * pivot.rz_p/(D_m**2) + soufflet.stiffness()["k_axial_x"]\
                      + soufflet.stiffness()["k_y"] + soufflet.stiffness()["k_z"] + 2*pivot.k_simple/(D_m**2)

            self.results = {
                "kx": rigidite,
                "ky": rigidite,
                "kz": rigidite
            }
            print(4 * membrane.rx/(D_m**2))
            print(2 * pivot.rz_p/(D_m**2))
            print(2 * pivot.kx_p)
            print(2* pivot.k_simple/(D_m**2))
            print(soufflet.stiffness()["k_axial_x"] + soufflet.stiffness()["k_y"] + soufflet.stiffness()["k_z"])

            self.display_results(membrane, pivot, soufflet)

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def display_results(self, membrane, pivot, soufflet):
        self.result_box.insert(tk.END, "=== Rigidités individuelles ===\n")
        self.result_box.insert(tk.END, f"Membrane: kz = {membrane.kz_m:.2f} N/m | kx, ky = {membrane.kx_m:.2f} N/m | Torsion = {membrane.k_torsion:.2f} N·m/rad\n")
        self.result_box.insert(tk.END, f"Pivot:    kz = {pivot.kz_p:.2f} N/m | kx = {pivot.kx_p:.2f} | ky = {pivot.ky_p:.2f} | Torsion = {pivot.rz_p:.2f} N·m/rad\n")
        self.result_box.insert(tk.END, "Soufflet:\n")
        for k, v in soufflet.stiffness().items():
            unit = "N·m/rad" if "theta" in k else "N/m"
            self.result_box.insert(tk.END, f"  {k} = {v:.2e} {unit}\n")

        self.result_box.insert(tk.END, "\n=== Rigidités totales ===\n")
        for name, value in self.results.items():
            unit = "N·m/rad" if "r" in name else "N/m"
            self.result_box.insert(tk.END, f"{name} = {value:.2f} {unit}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = RigiditeApp(root)
    root.mainloop()