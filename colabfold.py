import tkinter as tk
import subprocess
from tkinter import ttk
import settings
import alphafoldcall
import os

class ColabFoldGui:
    def __init__(self, parent):
        self.pymol_process=None
        self.cwd=settings.folds_folder
        self.parent = parent
        self.fold_button = tk.Button(parent, text="Fold", command=self.fold)
        self.fold_button.grid(row=0, column=0)
        #add TextArea for the sequence
        self.sequence_text = tk.Text(parent, height=10, width=50)
        self.sequence_text.grid(row=1, column=0,columnspan=100)
        #add open structure button
        self.open_structure_button = tk.Button(parent, text="Open Structure", command=self.open_structure)
        self.open_structure_button.grid(row=0, column=2)
        self.close_structure_button = tk.Button(parent, text="Close Structure", command=self.close_structure)
        self.close_structure_button.grid(row=0, column=3)
        #get list of all files in the structure folder
        self.structure_result=None
        self.structure_folder=settings.structure_folder
        #list filenames in a combobox
        self.structure_combobox = ttk.Combobox(parent)
        self.structure_combobox.grid(row=0, column=1)
        #add open structure button
        self.update_structure_combobox()
    def update_structure_combobox(self):
        files=os.listdir(self.structure_folder)
        self.structure_combobox['values']=files
    def fold(self):
        sequence=self.sequence_text.get("1.0", tk.END)
        print(sequence)
        structure_result=alphafoldcall.StructureResult(sequence)
        structure_result.generate_structure(amber=True)
        structure_result.join()
        self.structure_result=structure_result
        self.update_structure_combobox()
        #select the item with the id
        self.structure_combobox.set(structure_result.id)
        print(structure_result.stdout)
        print(structure_result.stderr)
    def open_structure(self):
        self.close_structure()
        id=self.structure_combobox.get()
        path=alphafoldcall.get_pdb(id,1,True)
        print(path)
        self.pymol_process = subprocess.Popen(["pymol", path])

    def close_structure(self):
        if self.pymol_process!=None:
            self.pymol_process.terminate()
      