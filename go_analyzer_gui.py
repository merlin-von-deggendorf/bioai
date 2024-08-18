import random
from Bio import SwissProt
from Bio.SwissProt import Record
import sys
from tkinter import ttk
import data_manager


class GoAnalyzer:
    def __init__(self,frame : ttk.Frame):
        self.frame = frame
        self.sample_size = ttk.Entry(frame, width=5)
        self.sample_size.insert(0, "5000")
        self.sample_size.grid(row=1, column=0)
        self.generate_sample_button = ttk.Button(frame, text="Generate Sample", command=self.generate_sample)
        self.generate_sample_button.grid(row=1, column=1)

    def generate_sample(self):
        data_manager.create_sample_file(int(self.sample_size.get()), 'sample.json')