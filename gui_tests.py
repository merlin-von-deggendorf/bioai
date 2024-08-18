import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Tabbed Interface Example")

# Create a Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create the first tab
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="go")
ttk.Label(tab1, text="This is the content of Tab 1").grid(row=0, column=0)

# Create a text area
text_area = tk.Text(tab1, height=10, width=50)
text_area.grid(row=1, column=0)

# Create the second tab
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Tab 2")
ttk.Label(tab2, text="This is the content of Tab 2").pack(padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()


