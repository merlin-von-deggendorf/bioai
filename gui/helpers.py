import os
import tkinter as tk
from tkinter import ttk
from typing import Optional

class LabeledEntry:
    def __init__(self,parent:tk.Frame,label:str,grid_x:int,grid_y:int,value:str=None) -> None:
        self.frame = tk.Frame(parent)
        self.frame.grid(row=grid_x,column=grid_y)
        self.label = tk.Label(self.frame,text=label)
        self.label.grid(row=0,column=0)
        self.entry = tk.Entry(self.frame)
        self.entry.grid(row=0,column=1)
        if value is not None:
            self.entry.insert(0,value)
    def get(self) -> str:
        return self.entry.get()
    def get_int(self) -> int:
        try:
            return int(self.entry.get())
        except ValueError:
            return None



class FileListComboBox:
    def __init__(self,parent:tk.Frame,path:str,row,column,label:str='OK',calback:callable=None,delte_button=False) -> None:

        self.frame = tk.Frame(parent)
        self.path = path
        self.callback = calback
        self.combo = ttk.Combobox(self.frame)
        self.reload()
        self.combo.grid(row=0, column= 0)
        self.frame.grid(row=row,column=column)
        self.button = tk.Button(self.frame, text=label, command=self.file_selected)
        self.button.grid(row=0, column=1)
        if delte_button:
            self.delete_button = tk.Button(self.frame, text="Delete", command=self.delte_selected)
            self.delete_button.grid(row=0, column=2)
    def reload(self):
        self.files = os.listdir(self.path)
        self.combo['values'] = self.files
    def file_selected(self):
        #generate the full path
        full_path = os.path.join(self.path,self.combo.get())
        if self.callback is not None:
            self.callback(full_path)
    def delte_selected(self):
        #generate the full path
        full_path = os.path.join(self.path,self.combo.get())
        os.remove(full_path)
        self.reload()

        

if __name__ == "__main__":
    def callback(value):
        print(value)
    root = tk.Tk()
    root.title("FileListComboBox Example")
    FileListComboBox(root,"/mnt/data",0,0,label="Select File",calback=callback)
    root.mainloop()