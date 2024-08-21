
import tkinter as tk
import settings

class SampleSplitter:
    def __init__(self, parent:tk.Frame):
        self.text_area = tk.Text(parent, width=300, height=200)
        self.text_area.grid(row=0, column=0)
        # Make the text area read-only
        self.text_area.config(state="disabled")
        