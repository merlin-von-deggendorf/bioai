
import tkinter as tk
from tkinter import ttk
import bioai
import autodocker
class ProteinContainerGUI:
    def __init__(self,frame:tk.Frame, protein_container: bioai.ProteinContainer):
        self.protein_container = protein_container

        self.frame=tk.Frame(frame)
        self.frame.grid(row=0,column=0)
        #generate combobox with the list of proteins
        self.combo = ttk.Combobox(self.frame)
        #load keys from the protein container
        self.combo['values'] = self.protein_container.get_ids()
        self.combo.grid(row=0,column=0)
        #select protein on value change
        self.combo.bind("<<ComboboxSelected>>", self.protein_selected)
        self.text_area = tk.Text(self.frame,width=150,height=40)
        self.text_area.grid(row=5, column=0,columnspan=20)
        self.ligands:dict[str:bioai.Feature]=None
        self.ligands=self.protein_container.extract_ligands()
        self.ligand_combo = ttk.Combobox(self.frame)
        self.ligand_combo['values'] = list(self.ligands.keys())
        self.ligand_combo.grid(row=0,column=1)
        self.ligand_combo.bind("<<ComboboxSelected>>", self.find_by_ligand)
        self.filtered_proteins=ttk.Combobox(self.frame)
        self.filtered_proteins.grid(row=0,column=2)
        self.filtered_proteins.bind("<<ComboboxSelected>>", self.protein_selected)
        self.protein_features=ttk.Combobox(self.frame,width=100)
        self.protein_features.grid(row=0,column=3)

        self.dock_button = tk.Button(self.frame, text="AutoDock",command=self.dock)
        self.dock_button.grid(row=0,column=4)
    def dock(self):
        protein_id = self.filtered_proteins.get()
        protein=self.protein_container.find_by_id(protein_id)
        current=self.protein_features.current()
        print(f"Docking {protein_id} with feature nr. {current}")
        
    def destroy(self):
        self.frame.destroy()

    def find_by_ligand(self,value):
        ligand_name = self.ligand_combo.get()
        feature :bioai.Feature = self.ligands.get(ligand_name)
        self.filtered_proteins['values']=self.protein_container.find_by_ligand(ligand_name)
    def protein_selected(self,event):

        id = event.widget.get()
        protein=self.protein_container.find_by_id(id)
        self.text_area.delete(1.0,tk.END)
        self.text_area.insert(tk.END,str(protein))
        self.protein_features['values'] = [str(feature) for feature in protein.features]
        #add code to display the protein in a new window