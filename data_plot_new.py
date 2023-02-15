# lib
import tkinter
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import axes

# file
import load

class single_line(object):
    def __init__(self, cords: list[tuple], file_path: str):
        self.cord: list[tuple] = cords
        self.file_path = file_path
        self.parameters = {}
        self.ploted = False
        
    def set_parameters(self, new_parameters: dict):
        self.parameters = new_parameters

class line_container(object):
    def __init__(self, frame: tkinter.Frame, root: tkinter.Tk):
        self.root = root
        self.frame = frame
        self.container: list[single_line] = []
        self.garbage: list[single_line] = []
        self.loader = load.read_gr_file()
        self.matplot_figure = Figure(figsize = (8, 5), dpi = 100)
        self.matplot_subplot = self.matplot_figure.add_subplot(111)
        self.tk_canvas = FigureCanvasTkAgg(self.matplot_figure, master=self.root)
        self.tk_canvas.draw()
        self.tk_canvas.get_tk_widget().pack()
        self.tk_toolbar = NavigationToolbar2Tk(self.tk_canvas, self.root)
        self.tk_toolbar.update()
        self.tk_canvas.get_tk_widget().pack()
    
    def load_and_plot(self, path: str):
        self.loader.read_file(path)
        anchor_container = self.loader.get_result()
        path_object = single_line(anchor_container, path)
        self.matplot_subplot.plot(*path_object.cord, **path_object.parameters)
        path_object.ploted = True
        self.container.append(path_object)
    
    def remove_line(self, path: str):
        counter = 0
        target: int = None
        for i in self.container:
            if i.file_path == path:
                target = counter
                break
            counter += 1
        self.matplot_subplot.lines.pop(target)
        self.garbage.append(self.container[counter])
        self.container.pop(counter)
    
    def change_line_preference(self, path: str,**kwargs: dict):
        counter = 0
        target: int = None
        for i in self.container:
            if i.file_path == path:
                target = counter
                break
            counter += 1
        self.matplot_subplot.get_lines()[target].update(kwargs)




