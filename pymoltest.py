import tkinter as tk
from pymol import cmd
from pymol import finish_launching

# Start PyMOL
finish_launching()

def load_pdb():
    cmd.reinitialize()
    cmd.load("/mnt/data/structures/ORFC3_PICV/ORFC3_PICV_relaxed_rank_001_alphafold2_ptm_model_2_seed_000.pdb")
    cmd.show("cartoon")
    cmd.zoom()

root = tk.Tk()
root.title("3D Protein Viewer")

load_button = tk.Button(root, text="Load PDB", command=load_pdb)
load_button.pack()

root.mainloop()
