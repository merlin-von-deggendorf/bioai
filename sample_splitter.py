
import os
import tkinter as tk
import tkinter.ttk as ttk
import settings
import gui
from Bio import SwissProt

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
        self.count_entries = tk.Button(self.container, text="Count Entries", command=self.count_entries)
        self.count_entries.grid(row=1, column=2)
        self.line_count=gui.LabeledEntry(self.container, "Line Count", 1, 0)
        self.line_count.entry.config(width=6)
        #set linecount to the value in the settings file
        self.line_count.entry.insert(0, str(self.settings.swiss_line_count))

    def count_lines(self):
        file=settings.abs_uni_prot_db
        #read file line by line
        count = 0
        with open(file, "r") as f:
            for line in f:
                count+=1
        self.line_count.entry.delete(0, tk.END)
        self.line_count.entry.insert(0, str(count))
        self.settings.swiss_line_count = count
        settings.save_settings()
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
                    
def count_entries():
    #read the file line by line
    with open(settings.abs_uni_prot_db, "r") as f:
        count = 0
        for line in f:
            if line.startswith("//"):
                count+=1
        print(count)
    #count using id line
    with open(settings.abs_uni_prot_db, "r") as f:
        count = 0
        for line in f:
            if line.startswith("ID"):
                count+=1
        print(count)
def analyse_database():
    with open(settings.abs_uni_prot_db, "r") as f:
        dic : dict[str:int] = {}
        third_char_dic : dict[str:int] = {}
        line_count = 0
        for line in f:
            line_count+=1
            #check if line starts with whitespace
            #get first two characters of the line
            substr = line[:2]
            if substr in dic:
                dic[substr]+=1
            else:
                dic[substr] = 1
            #get the third character of the line
            #test if the third character is aviailable
            if len(line) > 2:
                third_char = line[2]
                if third_char in third_char_dic:
                    third_char_dic[third_char]+=1
                else:
                    third_char_dic[third_char] = 1
        #list all keys in the dictionary
        print("Keys in the dictionary")
        for key in dic:
            print(key, dic[key])
        print("Third character dictionary")
        for key in third_char_dic:
            print(f'key: {key} value: {third_char_dic[key]}')
        print("Total lines", line_count)

def feature_analysis():
    with open(settings.abs_uni_prot_db, "r") as f:
        counter=0
        for record in SwissProt.parse(f):
            for feature in record.features:
                print(feature)
            counter+=1
            if counter > 1000:
                break
if __name__ == '__main__':
    #read first line of the file
    feature_analysis()