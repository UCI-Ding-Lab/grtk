# library
import tkinter
import tkinter.ttk
from tkinter import colorchooser
import os

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bin import data_plot_new

class layers(object):
    def __init__(self, frame: tkinter.Frame, lines: "data_plot_new.line_container"):
        self.select_status: dict[str,tkinter.IntVar] = dict()
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
        # create checkbox and color button
        new_layer = tkinter.Checkbutton(
            single_layer_frame,
            text=tail,
            variable=attri
        )
        new_layer.pack(side="left")
        self.select_status[path] = attri
    
    def hide_on_graph(self, path: str):
        self.lines.remove_line(path)
    
    def show_on_graph(self, path: str):
        self.lines.load_and_plot(path)
    
    
        
        
        