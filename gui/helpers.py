import tkinter as tk
from typing import Optional

class LabeledEntry:
    def __init__(self,parent:tk.Frame,label:str,grid_x,grid_y) -> None:
        self.frame = tk.Frame(parent)
        self.frame.grid(row=grid_x,column=grid_y)
        self.label = tk.Label(self.frame,text=label)
        self.label.grid(row=0,column=0)
        self.entry = tk.Entry(self.frame)
        self.entry.grid(row=0,column=1)

class FileListComboBox:
    def __init__(self,parent:tk.Frame,path:str,calback:callable,label:str=None) -> None:
        callback(path)
        pass

if __name__ == "__main__":
    def callback(value):
        print(value)
    root = tk.Tk()
    root.title("FileListComboBox Example")
    FileListComboBox(root,"/home/runner/",callback)
    root.mainloop()