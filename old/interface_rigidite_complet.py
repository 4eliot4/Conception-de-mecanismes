
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from old.soufflet_code import Soufflet
from old.pivot import Pivot
from old.membrane import Membrane

root = tk.Tk()
root.title("Rigidité totale du système - Export complet")
root.geometry("750x800")

parametres = {}
options = {}

def ajouter_champs(frame, label_default_pairs, offset=0):
    for i, (label, default) in enumerate(label_default_pairs):
        tk.Label(frame, text=label).grid(row=i+offset, column=0, sticky="e")
        entry = tk.Entry(frame)
        entry.insert(0, default)
        entry.grid(row=i+offset, column=1)
        parametres[label] = entry

frame_soufflet = ttk.LabelFrame(root, text="Soufflet (x3)")
frame_soufflet.pack(fill="x", padx=10, pady=5)
options['soufflet'] = tk.BooleanVar(value=True)
tk.Checkbutton(frame_soufflet, text="Inclure Soufflets", variable=options['soufflet']).grid(row=0, column=0, sticky="w")
soufflet_fields = [("E (Pa)", "210e9"), ("ν", "0.3"), ("L (m)", "0.02"), ("b (m)", "0.008"), ("t (m)", "0.0008"), ("h (m)", "0.03")]
ajouter_champs(frame_soufflet, soufflet_fields, offset=1)

frame_pivot = ttk.LabelFrame(root, text="Pivot Composite (x6)")
frame_pivot.pack(fill="x", padx=10, pady=5)
options['pivot'] = tk.BooleanVar(value=True)
tk.Checkbutton(frame_pivot, text="Inclure Pivots", variable=options['pivot']).grid(row=0, column=0, sticky="w")
pivot_fields = [("E_pivot (Pa)", "210e9"), ("G (Pa)", "80e9"), ("b_pivot (m)", "0.02"), ("e (m)", "50e-6"), ("r (m)", "0.003"), ("l_pivot (m)", "0.1")]
ajouter_champs(frame_pivot, pivot_fields, offset=1)

frame_membrane = ttk.LabelFrame(root, text="Membrane (x6)")
frame_membrane.pack(fill="x", padx=10, pady=5)
options['membrane'] = tk.BooleanVar(value=True)
tk.Checkbutton(frame_membrane, text="Inclure Membranes", variable=options['membrane']).grid(row=0, column=0, sticky="w")
membrane_fields = [("F (N/mm)", "0.25"), ("D (mm)", "50"), ("h_membrane (m)", "0.0002"), ("l_membrane (m)", "0.1")]
ajouter_champs(frame_membrane, membrane_fields, offset=1)

frame_force_moment = ttk.LabelFrame(root, text="Force et Moment appliqués")
frame_force_moment.pack(fill="x", padx=10, pady=5)
force_moment_fields = [("Force F (N)", "10"), ("Moment M (Nm)", "1"), ("Nom fichier Excel", "resultats_complet.xlsx")]
ajouter_champs(frame_force_moment, force_moment_fields)

def calculer_et_exporter():
    try:
        k_translation = 0
        k_rotation = 0

        if options['soufflet'].get():
            s = Soufflet(float(parametres["E (Pa)"].get()), float(parametres["ν"].get()),
                         float(parametres["L (m)"].get()), float(parametres["b (m)"].get()),
                         float(parametres["t (m)"].get()), float(parametres["h (m)"].get()))
            k_s = s.stiffness()
            k_translation += k_s["k_axial_x"] + k_s["k_y"] + k_s["k_z"]
            k_rotation += k_s["k_theta_x"] + k_s["k_theta_y"] + k_s["k_theta_z"]

        if options['pivot'].get():
            p1 = Pivot(float(parametres["E_pivot (Pa)"].get()), float(parametres["G (Pa)"].get()),
                       float(parametres["b_pivot (m)"].get()), float(parametres["e (m)"].get()),
                       float(parametres["r (m)"].get()))
            p2 = Pivot(float(parametres["E_pivot (Pa)"].get()), float(parametres["G (Pa)"].get()),
                       float(parametres["b_pivot (m)"].get()), float(parametres["e (m)"].get()),
                       float(parametres["r (m)"].get()))
            rx_p = 1 / (1 / p1.rigidite_equivalente_flexion() + 1 / p2.rigidite_equivalente_flexion())
            ry_p = rx_p
            rz_p = 1 / (1 / p1.rigidite_equivalente_torsion() + 1 / p2.rigidite_equivalente_torsion())
            l_p = float(parametres["l_pivot (m)"].get())
            kx_pivot = 6 * rx_p / l_p**2
            ky_pivot = 6 * ry_p / l_p**2
            k_translation += kx_pivot + ky_pivot
            k_rotation += 2 * rz_p + 4 * rx_p + 4 * ry_p

        if options['membrane'].get():
            m = Membrane(F=float(parametres["F (N/mm)"].get()), D_int=float(parametres["D (mm)"].get()),
                         h=float(parametres["h_membrane (m)"].get()))
            kz_m = m.kz_m
            rx_m = m.rx
            ry_m = m.ry
            rz_m = m.k_torsion
            l_m = float(parametres["l_membrane (m)"].get())
            k_translation += 2 * kz_m + 4 * (rx_m / l_m**2 + ry_m / l_m**2)
            k_rotation += 2 * 1 / (1 / rz_p + 1 / rz_m) + 4 * 1 / (1 / rx_p + 1 / rx_m) + 4 * 1 / (1 / ry_p + 1 / ry_m)

        F_appliquee = float(parametres["Force F (N)"].get())
        M_applique = float(parametres["Moment M (Nm)"].get())
        fichier = parametres["Nom fichier Excel"].get()

        deplacement = F_appliquee / k_translation
        rotation = M_applique / k_rotation

        resultats = {cle: [float(parametres[cle].get())] for cle in parametres if not cle.startswith("Nom")}
        resultats.update({
            "k_translation (N/m)": [k_translation],
            "k_rotation (Nm/rad)": [k_rotation],
            "Déplacement (m)": [deplacement],
            "Rotation (rad)": [rotation]
        })

        df_nouveau = pd.DataFrame(resultats)

        if os.path.exists(fichier):
            df_existant = pd.read_excel(fichier)
            df_total = pd.concat([df_existant, df_nouveau], ignore_index=True)
        else:
            df_total = df_nouveau

        df_total.to_excel(fichier, index=False)

        messagebox.showinfo("Succès",
            f"✅ Données ajoutées à '{fichier}' !\nDéplacement : {deplacement:.2e} m\nRotation : {rotation:.2e} rad")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

btn_calc = tk.Button(root, text="Calculer et Ajouter au fichier", command=calculer_et_exporter)
btn_calc.pack(pady=20)

root.mainloop()
