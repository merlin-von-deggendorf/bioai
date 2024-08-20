import tkinter as tk
from tkinter import ttk
import go_analyzer_gui
import colabfold
import autodock

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
notebook = ttk.Notebook(root,width=1600,height=600)
notebook.grid(row=0, column=0)

# Create the first tab
tab1 = tk.Frame(notebook)
notebook.add(tab1, text="go")
tk.Label(tab1, text="This is the content of Tab 1").grid(row=0, column=0)
text_area = tk.Text(tab1, width=40, height=10)
text_area.grid(row=1, column=0)
# Make the text area read-only
text_area.config(state="disabled")

testing_tab = tk.Frame(notebook)
notebook.add(testing_tab, text="Testing")
go_analyzer_gui.GoAnalyzer(testing_tab)

# Local colabfold tab
colabfold_tab = tk.Frame(notebook)
notebook.add(colabfold_tab, text="ColabFold")
colabfold.ColabFoldGui(colabfold_tab)

autodock_tab = tk.Frame(notebook)
notebook.add(autodock_tab, text="AutoDock")
autodock.AutoDockGui(autodock_tab)
# Focus the testing tab
notebook.select(colabfold_tab)
# Start the Tkinter event loop
root.mainloop()
