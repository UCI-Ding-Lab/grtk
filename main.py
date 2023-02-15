import tkinter
from tkinter import filedialog as fd
import tkinter.messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import load
#from data_plot import DataPlot
import timeit
from logger import logger

import file_menu
import edit_menu
import options_menu
import tools_menu
import treatment_menu
import test_menu
import data_plot_new

def do_nothing():
    pass

class GUI:
    def __init__(self, root: tkinter.Tk):
        self.log = logger()
        self.debug_mode = False
        self.root = root
        self.menu_bar = tkinter.Menu(root)
        self.frame = tkinter.Frame(self.root).pack()
        self.option_frame = tkinter.Frame()
        self.plot = None
        self.container = data_plot_new.line_container(frame=self.frame, root=self.root)
        self._window()
        self._menu_bar_main()

        root.config(menu=self.menu_bar)
        root.mainloop()
        self.log._close()

    def _window(self):
        self.root.title('Data Visualization Software')
        self.root.geometry("800x600")
        
    def _menu_bar_main(self):
        self._menu_bar_file()
        self._menu_bar_edit()
        self._menu_bar_options()
        self._menu_bar_tools()
        self._menu_bar_treatment()

        # for testing purpose
        self._menu_bar_test()
    
    def _menu_bar_file(self):
        fm = file_menu.FileMenu(self, container=self.container)

    def _menu_bar_edit(self):
        em = edit_menu.EditMenu(self)

    def _menu_bar_options(self):
        om = options_menu.OptionsMenu(self)

    def _menu_bar_tools(self):
        tm = tools_menu.ToolsMenu(self)

    def _menu_bar_treatment(self):
        tm = treatment_menu.TreatmentMenu(self)

    def _menu_bar_test(self):
       tm = test_menu.TestMenu(self)

        
        
def GUI_manager():
    root = tkinter.Tk()
    app = GUI(root)

if __name__ == '__main__':

    GUI_manager()
