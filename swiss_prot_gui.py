import tkinter as tk
from tkinter import ttk
import go_analyzer_gui
import colabfold
import autodock
import sample_splitter
import settings

# Create the main window
root = tk.Tk()
root.title("Tabbed Interface Example")
# Create the menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
# Create the File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menu", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)
# Create a Notebook widget
notebook = ttk.Notebook(root,width=1920,height=1000)
notebook.grid(row=0, column=0)
tab1 = tk.Frame(notebook)
notebook.add(tab1, text="Testing1")
sample_splitter.SampleSplitter(tab1)
testing_tab = tk.Frame(notebook)
notebook.add(testing_tab, text="Data Reformatter")
go_analyzer_gui.GoAnalyzer(testing_tab)

# Local colabfold tab
colabfold_tab = tk.Frame(notebook)
notebook.add(colabfold_tab, text="ColabFold")
colabfold.ColabFoldGui(colabfold_tab)
def on_closing():
    settings.save_settings()
    root.quit()
# Start the Tkinter event loop
root.protocol("WM_DELETE_WINDOW",on_closing )
notebook.select(colabfold_tab)
root.mainloop()
