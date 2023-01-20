import tkinter
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import load
from plot_preference import preference

class DataPlot():
    def __init__(self, frame: tkinter.Frame):
        self.frame = frame
        self.plot = None
        self.tool_bar = None
        self.cords = None
        self.file_path = None
        self.canvas = None
        self.fig = None
        self.options = {
            "style": "solid",
            "width": .5,
            "dot_color": "red",
            "dot_size": 2.5,
            "line_color": "red",
        }

    def plot_file(self, file_path):
        self.file_path = file_path
        if not self.file_path:
            print("Error")
        else:
            if self.plot == None:
                self._plot()
            else:
                self._replace_plot()

    def _plot(self):
        self.fig = Figure(figsize = (8, 5), dpi = 100)
        self.plot = self.fig.add_subplot(111)

        obj = load.read_gr_file()
        obj.read_file(self.file_path)
        self.cords = [float(i.y) for i in obj.container]
        
        self.plot.plot(self.cords, **preference(self.options))
        self.plot.grid()
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.tool_bar = NavigationToolbar2Tk(self.canvas, self.frame)
        self.tool_bar.update()
        self.canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1)
        self.frame.pack(fill=tkinter.BOTH, expand=1)

    def _replace_plot(self):
        self.tool_bar.destroy()
        self.canvas.get_tk_widget().destroy()
        self.plot.clear()
        self._plot()