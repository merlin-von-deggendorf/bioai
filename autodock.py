import tkinter as tk
import bioai
import os
import subprocess
import settings
import gui
import protein_container_gui as pcg
import shutil
import autodocker

class AutoDockGui:
    def __init__(self,frame:tk.Frame) -> None:
        self.button = tk.Button(frame, text="AutoDock")
        self.button.grid(row=5, column=0)
        self.button.config(command=self.autodock)
        self.button = tk.Button(frame, text="Analyze Features")
        self.button.grid(row=5, column=1)
        self.button.config(command=self.analyze_features)
        self.skip=gui.LabeledEntry(frame,'Skip',0,0,'0')
        self.limit=gui.LabeledEntry(frame,'Limit',0,1,'1000')
        self.sample_name=gui.LabeledEntry(frame,'Sample Name',0,2,'sample')
        self.generate_sample_button=tk.Button(frame,text='Generate Sample')
        self.generate_sample_button.grid(row=0,column=3)
        self.generate_full_sample_button=tk.Button(frame,text='Generate Full Sample')
        self.generate_full_sample_button.grid(row=0,column=4)
        self.generate_full_sample_button.config(command=self.generate_full_sample)
        self.generate_sample_button.config(command=self.generate_sample)
        self.file_list_combo=gui.FileListComboBox(frame,settings.samples_folder,1,0,label='Load Sample',calback=self.load_sample,delte_button=True)
        self.gui_sub_frame=tk.Frame(frame)
        self.gui_sub_frame.grid(row=10,column=0,columnspan=100)
        self.pcg:pcg.ProteinContainerGUI=None
        self.load_sample(settings.samples_folder+'reduced')
    def generate_sample(self):
        skip=self.skip.get_int()
        limit=self.limit.get_int()
        sample_name=self.sample_name.get()
        protein_container = bioai.ProteinContainer()
        protein_container.generate(skip,limit)
        path=settings.samples_folder+sample_name
        pc=bioai.ProteinContainer()
        pc.generate(skip,limit)
        pc.save(path)
        self.file_list_combo.reload()
    def generate_full_sample(self):
        path=settings.samples_folder+'full'
        pc=bioai.ProteinContainer()
        pc.generate()
        pc.save(path)
        self.file_list_combo.reload()
    def load_sample(self,path:str):
        self.protein_container=bioai.ProteinContainer.load(path)
        if self.pcg is not None:
            self.pcg.destroy()
        self.pcg=pcg.ProteinContainerGUI(self.gui_sub_frame,self.protein_container)
        
    

    def autodock(self):
        print("AutoDock button clicked")
        # Add code to run AutoDock here
        #call command line command
        #./bin/autodock_gpu_64wi --help
        #the working directory is set up in the settings
        command = "./bin/autodock_gpu_64wi --help"
        # Specify the current working directory
        cwd = settings.autodock_directory
        # Execute the command and capture the output
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
        stdout, stderr = process.communicate()

        # Print the output
        print(stdout.decode())
        if stderr:
            print("Error:", stderr.decode())
    def analyze_features(self):
        proteins=bioai.ProteinContainer.load()

                    
if __name__ == '__main__':
    def store_proteins():
        protein_container = bioai.ProteinContainer()
        protein_container.generate(100000,10000)
        protein_container.save()
    def load_proteins() -> bioai.ProteinContainer:
        prots=bioai.ProteinContainer.load()
        for prot in prots.proteins:
            print(prot.id)
            print(prot.sequence)
            print(prot.go_terms)
            print('Features:')
            for feature in prot.features:
                print(feature)
            print('PDB structures:')
            for pdb in prot.pdb_structures:
                print(pdb)
            print('AlphaFold structures:')
            for af in prot.alpha_folds:
                print(af)
    
    load_proteins()