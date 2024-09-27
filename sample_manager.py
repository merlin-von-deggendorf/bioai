import tkinter as tk
import bioai as ba
import settings
import os
import gui
import protein_container_gui as pcg
class SampleManager:
    def __init__(self,master:tk.Tk):
        # generate window 
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Sample Manager")
        # generate button to generate samples
        self.sample_name = gui.helpers.LabeledEntry(self.window,"Sample Name",0,0)
        self.skip = gui.helpers.LabeledEntry(self.window,"Skip",1,0)
        self.sample_size = gui.helpers.LabeledEntry(self.window,"Count",1,1)
        self.generate_button = tk.Button(self.window,text="Generate Samples",command=self.generate)
        self.generate_button.grid(row=2,column=0)
        # list all files in samples folder
        self.file_list=tk.Listbox(self.window)
        self.file_list.grid(row=4,column=0)
        self.load_files()
        self.load_button = tk.Button(self.window,text="Load",command=self.load_selected)
        self.load_button.grid(row=4,column=1)
        self.protein_container:ba.ProteinContainer = None
        self.generate_shuffled_button = tk.Button(self.window,text="Generate Shuffled",command=self.generate_shuffled)
        self.generate_shuffled_button.grid(row=5,column=0)
    def generate_shuffled(self):
        proco:ba.ProteinContainer=self.protein_container.generate_shuffled(self.sample_size.get_int())
        proco.save(settings.SAMPLES_PATH+self.sample_name.get())
        self.load_files()

        
    def load_selected(self):
        selected = self.file_list.get(self.file_list.curselection())
        self.protein_container = ba.ProteinContainer.load(settings.SAMPLES_PATH+selected)
        window = tk.Toplevel(self.master)
        pcg.ProteinContainerGUI(window,self.protein_container)
    def generate(self):
        sample_name=self.sample_name.get()
        sample_count=self.sample_size.get_int()
        skip=self.skip.get_int()
        skip = 0 if skip is None else skip
        if sample_name == '':
            return
        
        self.protein_container=ba.ProteinContainer()
        if sample_count is None:
            self.protein_container.generate()
        else:
            self.protein_container.generate(skip=skip,limit=sample_count)
        
        self.protein_container.save(settings.SAMPLES_PATH+sample_name)
        self.load_files()
    
    def load_files(self):
        self.file_list.delete(0,tk.END)
        for file in os.listdir(settings.SAMPLES_PATH):
            self.file_list.insert(tk.END,file)