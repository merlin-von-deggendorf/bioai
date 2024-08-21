
import os
import tkinter as tk
import tkinter.ttk as ttk
import settings

class SampleSplitter:
    def __init__(self, parent:tk.Frame):
        self.text_area = tk.Text(parent, width=150, height=45)
        self.text_area.grid(row=0, column=0)
        # Make the text area read-only
        self.text_area.config(state="disabled")
        #container to the right of the text area
        self.container = tk.Frame(parent)
        self.container.config()
        self.container.grid(row=0, column=1)
        #entry for start line
        self.start_line = tk.Entry(self.container)
        self.start_line.grid(row=0, column=0)
        self.load_button = tk.Button(self.container, text="Generate", command=self.load)
        self.load_button.grid(row=0, column=0)
        #combobox for selecting samplename
        self.sample_name = ttk.Combobox(self.container)
        self.sample_name.grid(row=0, column=1)
        self.load_sample_names()


    def load_sample_names(self):
        path=settings.text_sample_folder
        #get all files in the samples folder
        files = os.listdir(path)
        #set filnames to the combobox
        self.sample_name['values'] = files

    def load(self):
        print("Load button clicked")
        file=settings.abs_uni_prot_db
        #read file line by line
        count = 0
        with open(file, "r") as f:
            for line in f:
                count+=1
                print(line)
                if count > 100:
                    break
    def generate_samples(self):
        print("Generate samples clicked")
        pass
                    
