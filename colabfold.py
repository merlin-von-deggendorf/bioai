import tkinter as tk
import subprocess

class ColabFoldGui:
    def __init__(self, parent):
        self.parent = parent
        self.fold_button = tk.Button(parent, text="Fold", command=self.fold)
        self.fold_button.grid(row=0, column=0)
    def fold(self):
        #execute a shell command
        subprocess.run(['ls'])

        result=subprocess.run(['ls'],cwd='/',capture_output=True,text=True)
        print(result.stdout)
        