import random
from Bio import SwissProt
from Bio.SwissProt import Record
import sys
from tkinter import ttk
import tkinter as tk
import data_manager
import os
import shutil
import settings

class GoAnalyzer:
    def __init__(self,frame : ttk.Frame):
        self.frame = frame
        self.sample_size = ttk.Entry(frame, width=20)
        self.sample_size.insert(0, "5000")
        self.sample_size_label = ttk.Label(frame, text="Sample Size:")
        self.sample_size_label.grid(row=0, column=0)
        self.sample_size.grid(row=0, column=1)

        self.sample_name_label = ttk.Label(frame, text="Sample Name:")
        self.sample_name_label.grid(row=1, column=0)
        #combobox with all available samples
        #read sample names from the samples folder
        samples_path = settings.samples_folder
        # List all files in the samples path
        sample_files = os.listdir(samples_path)
        filenames = []
        for file in sample_files:
            file_path = os.path.join(samples_path, file)
            if os.path.isfile(file_path):
                filenames.append(file)
        
        self.sample_name : ttk.Combobox = ttk.Combobox(frame)
        self.sample_name['values'] = filenames
        self.sample_name.grid(row=1, column=1)
        self.sample_name.current(0)
        self.generate_sample_button = ttk.Button(frame, text="Generate Sample", command=self.generate_sample)
        self.generate_sample_button.grid(row=1, column=2)
        self.load_sample_button = ttk.Button(frame, text="Load Sample", command=self.load_sample)
        self.load_sample_button.grid(row=1, column=3)
        self.count_alpha_button=tk.Button(frame,text="Count AlphaFold",command=self.count_alpha)
        self.count_alpha_button.grid(row=1,column=4)
        self.count_pdb_button=tk.Button(frame,text="Count PDB",command=self.count_pdb)
        self.copy_to_test_button=tk.Button(frame,text="Copy to Test",command=self.copy_to_test)
        self.copy_to_test_button.grid(row=2,column=2)
        self.count_pdb_button.grid(row=2,column=3)
        #list of samples
        self.samples = ttk.Combobox(frame)
        self.samples.grid(row=3, column=0)
        #add select listener
        self.samples.bind("<<ComboboxSelected>>", self.sample_selected)
        self.sample_data_text_area = tk.Text(frame, width=100, height=20)
        self.sample_data_text_area.grid(row=5, column=0, columnspan=8)
        self.sample_data_text_area.config(state="disabled")
        self.load_sample()
    def copy_to_test(self):
        sample_name = self.sample_name.get()
        #copy the selected sample to the test folder
        if not os.path.exists(settings.test_samples_folder):
            os.makedirs(settings.test_samples_folder)
        shutil.copy(settings.samples_folder+sample_name, settings.test_samples_folder+sample_name)
        newfiles = os.listdir(settings.test_samples_folder)
        print(newfiles)
        
    def sample_selected(self,event):
        #get the selected sample
        self.selected_sample_id=self.samples.get()
        self.selected_sample=self.sample_list.get_sample_by_id(self.selected_sample_id)
        self.sequence=self.selected_sample.sequence
        #display the sample data
        self.sample_data_text_area.config(state="normal")
        self.sample_data_text_area.delete(1.0,tk.END)
        self.sample_data_text_area.insert(tk.END,f'ID:\n{self.selected_sample.id}\n\nSequence:\n{self.sequence}\n\nPDB IDs:\n{self.selected_sample.pdb_ids}\n\nAlphaFold IDs:\n{self.selected_sample.alpha_fold_ids}')
        
        
    def load_sample(self):
        samples:list[data_manager.Sample] = data_manager.load_samples(self.sample_name.get())
        self.samples['values'] = [sample.id for sample in samples]
        self.sample_list=data_manager.SampleList(samples)
        #select the first sample
        self.samples.current(0)
        self.sample_selected(None)

    def generate_sample(self):
        data_manager.create_sample_file(int(self.sample_size.get()), self.sample_name.get())

    def count_alpha(self):
        count=0
        for sample in self.sample_list.samples:
            if len(sample.alpha_fold_ids)>0:
                count+=1
        self.sample_data_text_area.config(state="normal")
        self.sample_data_text_area.delete(1.0,tk.END)
        self.sample_data_text_area.insert(tk.END,f'Total samples with AlphaFold IDs: {count}')

    def count_pdb(self):
        count=0
        for sample in self.sample_list.samples:
            if len(sample.pdb_ids)>0:
                count+=1
        self.sample_data_text_area.config(state="normal")
        self.sample_data_text_area.delete(1.0,tk.END)
        self.sample_data_text_area.insert(tk.END,f'Total samples with PDB IDs: {count}')