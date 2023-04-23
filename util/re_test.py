import os
import glob
import tkinter
from tkinter import ttk

def insert_file():
    pass

if __name__ == "__main__":
    root = tkinter.Tk()
    columns = ('file', 'type', 'curve')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.heading('file', text='File')
    tree.heading('type', text='Type')
    tree.heading('curve', text='Curve')
    tree.pack()
    root.mainloop()