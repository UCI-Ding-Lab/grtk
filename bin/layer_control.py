# library
import tkinter
import tkinter.ttk
from tkinter import colorchooser
import os

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import data_plot_new

class layers(object):
    def __init__(self, frame: tkinter.Frame, lines: "data_plot_new.line_container"):
        self.frame = frame
        self.lines = lines
    
    def add_layer(self, path: str):
        """create a new checkbox line in the container
        set the initial check box value to 1(checked)
        bind checkbox command to hide and show graph
        set up color change button and bind command to preference change

        Args:
            path (str): full file path in string
        """
        # beautification
        tkinter.ttk.Separator(self.frame, orient=tkinter.HORIZONTAL).pack(fill="x")
        single_layer_frame = tkinter.Frame(self.frame)
        single_layer_frame.pack()
        # full path is too long for the checkbox text to parse into just file name
        head, tail = os.path.split(path)
        # initial the checkbox value
        attri = tkinter.IntVar()
        attri.set(1)
        # create checkbox and color button
        new_layer = tkinter.Checkbutton(
            single_layer_frame,
            text=tail,
            variable=attri,
            # if value is 0 hide else show
            command=lambda: self.hide_on_graph(path) if not attri.get() else self.show_on_graph(path)
        )
        color_button = tkinter.Button(
            single_layer_frame,
            text="Color",
            command=lambda: self.change_color(path)
        )
        new_layer.pack(side="left")
        color_button.pack(side="right")
    
    def hide_on_graph(self, path: str):
        self.lines.remove_line(path)
    
    def show_on_graph(self, path: str):
        self.lines.load_and_plot(path)
    
    def change_color(self, path: str):
        """change the color of a line by ask the color hex code
        build a update kwargs manually then pass out to change preference

        Args:
            path (str): full file path
        """
        hexcode = colorchooser.askcolor()[1]
        # build update parameter(s)
        update_dict = dict(
            color=hexcode
        )
        self.lines.change_line_preference(path, **update_dict)
        
        
        