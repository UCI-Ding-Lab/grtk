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

class EditMenu():
    def __init__(self, GUI):
        self.GUI = GUI
        self._init_edit_menu()

    def _init_edit_menu(self):
        em = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        em.add_command(label="Copy Image", command=do_nothing)
        self.GUI.menu_bar.add_cascade(label="Edit", menu=em)