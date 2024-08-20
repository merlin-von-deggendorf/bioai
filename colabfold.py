import tkinter as tk
import subprocess
from tkinter import ttk
import settings
import alphafoldcall
import os
from pymol import cmd
from pymol import finish_launching

class ColabFoldGui:
    def __init__(self, parent):
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
        structure_result.generate_structure()
        structure_result.join()
        self.structure_result=structure_result
        self.update_structure_combobox()
    def open_structure(self):
        id=self.structure_combobox.get()
        
        finish_launching()
        cmd.reinitialize()
        cmd.load(path)
        cmd.show("cartoon")
        cmd.zoom()
      