import tkinter as tk
from tkinter import ttk
import go_analyzer_gui
import colabfold
import autodock
import sample_splitter

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
notebook.add(testing_tab, text="Testing2")
go_analyzer_gui.GoAnalyzer(testing_tab)

# Local colabfold tab
colabfold_tab = tk.Frame(notebook)
notebook.add(colabfold_tab, text="ColabFold")
colabfold.ColabFoldGui(colabfold_tab)

autodock_tab = tk.Frame(notebook)
notebook.add(autodock_tab, text="AutoDock")
autodock.AutoDockGui(autodock_tab)
# Focus the testing tab
notebook.select(tab1)
# Start the Tkinter event loop
root.mainloop()
