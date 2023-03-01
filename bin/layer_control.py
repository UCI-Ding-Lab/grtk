# library
import tkinter
import tkinter.ttk
import os

# module
from bin import data_plot_new

class layers(object):
    def __init__(self, frame: tkinter.Frame, lines):
        self.frame = frame
        self.checkbutton_container: list[tkinter.Checkbutton] = [None]
        self.attri_container: list[tkinter.IntVar] = [None]
        self.lines = lines
    
    def add_layer(self, path: str):
        head, tail = os.path.split(path)
        attri = tkinter.IntVar()
        attri.set(1)
        new_layer = tkinter.Checkbutton(
            self.frame,
            text=tail,
            variable=attri,
            command=lambda: self.hide_on_graph(path) if not attri.get() else self.show_on_graph(path)
        )
        self.checkbutton_container.append(new_layer)
        self.attri_container.append(attri)
        tkinter.ttk.Separator(self.frame, orient=tkinter.HORIZONTAL).pack(fill="x")
        new_layer.pack()
    
    def hide_on_graph(self, path):
        self.lines.remove_line(path)
    
    def show_on_graph(self, path):
        self.lines.load_and_plot(path)