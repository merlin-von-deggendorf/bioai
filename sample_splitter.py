
import os
import tkinter as tk
import tkinter.ttk as ttk
import settings
import gui

class SampleSplitter:
    def __init__(self, parent:tk.Frame):
        self.settings = settings.load_settings()
        self.text_area = tk.Text(parent, width=150, height=45)
        self.text_area.grid(row=0, column=0)
        # Make the text area read-only
        self.text_area.config(state="disabled")
        #container to the right of the text area
        self.container = tk.Frame(parent)
        self.container.config()
        self.container.grid(row=0, column=1)
        #entry for start line
        self.start_line = gui.LabeledEntry(self.container, "Start Line", 0, 0)
        self.start_line.entry.config(width=6)
        self.load_button = tk.Button(self.container, text="Generate", command=self.load)
        self.load_button.grid(row=2, column=0)
        self.count_lines = tk.Button(self.container, text="Count Lines", command=self.count_lines)
        self.count_lines.grid(row=1, column=1)
        self.line_count=gui.LabeledEntry(self.container, "Line Count", 1, 0)
        self.line_count.entry.config(width=6)
        #set linecount to the value in the settings file
        self.line_count.entry.insert(0, str(self.settings.swiss_line_count))

    def count_lines(self):
        print("Count lines clicked")
        file=settings.abs_uni_prot_db
        #read file line by line
        count = 0
        with open(file, "r") as f:
            for line in f:
                count+=1
        self.line_count.entry.delete(0, tk.END)
        self.line_count.entry.insert(0, str(count))
        #save the line count to settings file


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
                    
