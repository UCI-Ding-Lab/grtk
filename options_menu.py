import tkinter
from tkinter import filedialog as fd
import tkinter.messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import load
import data_plot
import timeit
from logger import logger

def do_nothing():
    pass

class OptionsMenu():
    def __init__(self, GUI):
        self.GUI = GUI
        self._init_options_menu()

    def _init_options_menu(self):
        om = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        om.add_command(label="Whatever", command=do_nothing)
        om.add_command(label="Line Color", command=lambda: self._color_options("l"))
        om.add_command(label="Marker Color", command=lambda: self._color_options("m"))
        om.add_command(label="Line Width", command=do_nothing)
        om.add_command(label="Line Type", command=do_nothing)
        
        self.GUI.menu_bar.add_cascade(label="Options", menu=om)

    def _color_options(self, type):
        def save_to_opt(self, choice: tkinter.StringVar):
            if type == "m":
                self.plot.options["dot_color"] = choice.get()
            else:
                self.plot.options["line_color"] = choice.get()
            self.plot._replace_plot()
            for i in self.option_frame.winfo_children():
                i.destroy()
            self.option_frame.pack_forget()
        choice = tkinter.StringVar()
        tkinter.Radiobutton(self.GUI.option_frame, value="red", variable=choice, bg='red').grid(row=0,column=0)
        tkinter.Radiobutton(self.GUI.option_frame, value="green", variable=choice, bg='green').grid(row=0,column=1)
        tkinter.Radiobutton(self.GUI.option_frame, value="blue", variable=choice, bg='blue').grid(row=0,column=2)
        tkinter.Radiobutton(self.GUI.option_frame, value="cyan", variable=choice, bg='cyan').grid(row=0,column=3)
        tkinter.Radiobutton(self.GUI.option_frame, value="magenta", variable=choice, bg='magenta').grid(row=0,column=4)
        tkinter.Radiobutton(self.GUI.option_frame, value="yellow", variable=choice, bg='yellow').grid(row=0,column=5)
        tkinter.Radiobutton(self.GUI.option_frame, value="black", variable=choice, bg='black').grid(row=0,column=6)
        tkinter.Radiobutton(self.GUI.option_frame, value="white", variable=choice, bg='white').grid(row=0,column=7)
        tkinter.Button(self.GUI.option_frame, text="Save", command=lambda: save_to_opt(self.GUI, choice)).grid(row=0,column=8)
        self.GUI.option_frame.pack()