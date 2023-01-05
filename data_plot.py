import tkinter
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import load

class DataPlot():
    def __init__(self, frame):
        self.frame = frame
        self.plot = None
        self.tool_bar = None
        #self.canvas = None

    def plot_file(self, file_path):
        
        if self.plot == None:
            self._plot(file_path)
        else:
            self._replace_plot(file_path)

    def _plot(self, file_path):
        obj = load.read_gr_file()
        obj.read_file(file_path)
        fig = Figure(figsize = (8, 5),
                    dpi = 100)

        y = [float(i.y) for i in obj.container]

        self.plot = fig.add_subplot(111)

        self.plot.plot(y)
        self.plot.grid()
        
        canvas = FigureCanvasTkAgg(fig, self.frame)
        #self.fig = fig
        #self.canvas = canvas
        self.tool_bar = NavigationToolbar2Tk(canvas, self.frame)
        self.tool_bar.update()
        canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1)
        
        
        self.frame.pack(fill=tkinter.BOTH, expand=1)


    def _replace_plot(self, file_path):
        obj = load.read_gr_file()
        obj.read_file(file_path)
        y = [float(i.y) for i in obj.container]
        self.plot.clear()
        self.plot.plot(y)
        self.plot.grid()
        
        #canvas = FigureCanvasTkAgg(self.fig, self.frame)
        #self.canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1)
        #self.tool_bar.update()
        #self.frame.pack(fill=tkinter.BOTH, expand=1)
        #self.root.mainloop()

    def clear_plot(self):
        self.plot.clear()