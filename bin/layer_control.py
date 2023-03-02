# library
import tkinter
import tkinter.ttk
from tkinter import colorchooser
import os

class layers(object):
    def __init__(self, frame: tkinter.Frame, lines):
        self.frame = frame
        self.lines = lines
    
    def add_layer(self, path: str):
        tkinter.ttk.Separator(self.frame, orient=tkinter.HORIZONTAL).pack(fill="x")
        single_layer_frame = tkinter.Frame(self.frame)
        single_layer_frame.pack()
        head, tail = os.path.split(path)
        attri = tkinter.IntVar()
        attri.set(1)
        new_layer = tkinter.Checkbutton(
            single_layer_frame,
            text=tail,
            variable=attri,
            command=lambda: self.hide_on_graph(path) if not attri.get() else self.show_on_graph(path)
        )
        color_button = tkinter.Button(
            single_layer_frame,
            text="Color",
            command=lambda: self.change_color(path)
        )
        new_layer.pack(side="left")
        color_button.pack(side="right")
    
    def hide_on_graph(self, path):
        self.lines.remove_line(path)
    
    def show_on_graph(self, path):
        self.lines.load_and_plot(path)
    
    def change_color(self, path):
        hexcode = colorchooser.askcolor()[1]
        update_dict = dict(
            color=hexcode
        )
        self.lines.change_line_preference(path, **update_dict)
        
        
        