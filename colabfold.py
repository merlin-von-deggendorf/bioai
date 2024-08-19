import tkinter as tk
import subprocess
import settings

class ColabFoldGui:
    def __init__(self, parent):
        self.cwd=settings.folds_folder
        self.parent = parent
        self.fold_button = tk.Button(parent, text="Fold", command=self.fold)
        self.fold_button.grid(row=0, column=0)
        self.clear_button = tk.Button(parent, text="Clear", command=self.clear)
    def fold(self):
        #execute a shell command
        subprocess.run(['ls'])
        result=subprocess.run(['mkdir','asdf'],cwd=self.cwd,capture_output=True,text=True)
        result=subprocess.run(['ls'],cwd=self.cwd,capture_output=True,text=True)
        print(result.stdout)
    def clear(self):
        pass
        