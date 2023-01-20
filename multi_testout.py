from numpy import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import math
import tkinter
from matplotlib import axes

# root object
root = tkinter.Tk()

# create lines' cords
t = linspace(0, 2*math.pi, 400)
a = sin(t)
b = cos(t)
c = a + b

# object of A single line
class single_line(object):
    def __init__(self, cords, file_path):
        self.cords = cords
        self.file_path = file_path
        self.parameters = dict()
        
    def set_parameters(self, new_parameters: dict):
        self.parameters = new_parameters
        
# canvas
fig = Figure(figsize = (8, 5), dpi = 100)
plot1 = fig.add_subplot(111)

# create multiple lines and store in container
container = []
container.append(single_line([t,a], "/user/home/fileA.gr"))
container.append(single_line([t,b], "/user/home/fileB.gr"))
container.append(single_line([t,c], "/user/home/fileC.gr"))

# draw lines and put references in a container
def plot_all_graph(sub_plot: axes.Axes, container: list[single_line]):
    ploted_container = [sub_plot.plot(*i.cords, **i.parameters) for i in container]
    return ploted_container

# edit a single line w/o changing others
# use file_path to find index, use index to find plot in figure
def remove_line(sub_plot: axes.Axes, file_path,  container: list[single_line]):
    counter = 0
    target: int = None
    for i in container:
        if i.file_path == file_path:
            target = counter
            break
        counter += 1
    sub_plot.lines.pop(target)

def change_line_preference(sub_plot: axes.Axes, file_path,  container: list[single_line], **kwargs):
    counter = 0
    target: int = None
    for i in container:
        if i.file_path == file_path:
            target = counter
            break
        counter += 1
    sub_plot.get_lines()[target].update(kwargs)

# (main) 
# plot all fileA fileB fileC then remove fileC then change fileA to black and thick line
ploted_container = plot_all_graph(plot1, container)
remove_line(plot1, "/user/home/fileC.gr", container)

parameter_to_update = dict(
    color="black",
    linewidth=5,
)
change_line_preference(plot1, "/user/home/fileA.gr", container, **parameter_to_update)

# mapping to tkinter
canvas = FigureCanvasTkAgg(fig, master = root)  
canvas.draw()
canvas.get_tk_widget().pack()
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack()

# end loop
root.mainloop()