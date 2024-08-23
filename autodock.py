import tkinter as tk
import bioai
class AutoDockGui:
    def __init__(self,frame:tk.Frame) -> None:
        self.button = tk.Button(frame, text="AutoDock")
        self.button.grid(row=0, column=0)
        self.button.config(command=self.autodock)
    def autodock(self):
        print("AutoDock button clicked")
        # Add code to run AutoDock here
        pass