from numpy import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import math
import tkinter
from matplotlib import axes, lines
from load import read_gr_file, anchor

class single_line(object):
    def __init__(self, cords: anchor, file_path):
        self.cords = cords
        self.file_path = file_path
        self.parameters = dict(
            color="black",
            linewidth=1,
        )
        self.abs_cords_y = [float(i.y) for i in cords]
        self.abs_cords_x = [float(i.x) for i in cords]
        
    def set_parameters(self, new_parameters: dict):
        self.parameters = new_parameters

def line_loader(container: dict[str, single_line], loader: read_gr_file, path: str):
    loader.read_file(path)
    container[path] = single_line(loader.get_result(), path)

def plot_line(sub_plot: axes.Axes, object_2d_container: dict, line: single_line):
    this_line, = sub_plot.plot(*[line.abs_cords_x, line.abs_cords_y], **line.parameters)
    object_2d_container[line.file_path] = this_line

def delete_line(object_2d_container: dict[str, lines.Line2D], container: dict[str, single_line], file_path: str, pop_container: bool=False):
    object_2d_container[file_path].remove()
    if pop_container:
        container.pop(file_path)

def change_line_pref(sub_plot: axes.Axes, object_2d_container: dict[str, lines.Line2D], container: dict[str, single_line], file_path: str, **kwargs):
    delete_line(object_2d_container, container, file_path)
    container[file_path].parameters = kwargs
    plot_line(sub_plot, object_2d_container, container[file_path])

if __name__ == "__main__":
    
    t = linspace(0, 2*math.pi, 400)
    a = sin(t)
    b = cos(t)
    c = a + b
    
    root = tkinter.Tk()
    
    fig = Figure(figsize = (8, 5), dpi = 100)
    plot1 = fig.add_subplot(111)
    
    container = dict()
    loader = read_gr_file()
    object_2d_container = dict()
    
    
    test_file_A = "/Users/tiger/Documents/Github/grtk/raw/formatted.gr"
    test_file_B = "/Users/tiger/Documents/Github/grtk/raw/formatted303.gr"
    line_loader(container, loader, test_file_A)
    line_loader(container, loader, test_file_B)
    parameter_to_update = dict(
    color="blue",
    linewidth=1,
    )
    container[test_file_B].abs_cords_x=t
    container[test_file_B].abs_cords_y=a
    for key, item in container.items():
        plot_line(plot1, object_2d_container, item)
    
    change_line_pref(plot1, object_2d_container, container, test_file_B, **parameter_to_update)
    
    plot1.grid()
    canvas = FigureCanvasTkAgg(fig, master = root)  
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack()
    root.mainloop()