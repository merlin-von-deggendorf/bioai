import tkinter as tk

class AutoDockGui:
    def __init__(self,frame:tk.Frame) -> None:
        label = tk.Label(frame, text="This is the content of Tab 3")
        label.grid(row=0, column=0)