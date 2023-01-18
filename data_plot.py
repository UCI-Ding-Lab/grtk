import tkinter
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import load

class DataPlot():
    def __init__(self, frame: tkinter.Frame):
        self.frame = frame
        self.plot = None
        self.tool_bar = None
        self.enable_dot = False
        self.cords = None
        self.cur_path = None
        self.canvas = None
        self.fig = None

    def plot_file(self):
        if not self.cur_path:
            print("Error")
        else:
            if self.plot == None:
                # make initial plot
                # setup mapping
                # setup canvas
                self.fig = Figure(figsize = (8, 5), dpi = 100)
                self.plot = self.fig.add_subplot(111)
                self._plot()
                self.plot.grid()
                self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
                self.tool_bar = NavigationToolbar2Tk(self.canvas, self.frame)
                self.tool_bar.update()
                self.canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1)
                self.frame.pack(fill=tkinter.BOTH, expand=1)
            else:
                self.frame.pack_forget()
                self._replace_plot()
                self.plot.grid()
                
                self.frame.pack(fill=tkinter.BOTH, expand=1)
                # self.canvas.get_tk_widget().destroy()
                # self.canvas = FigureCanvasTkAgg(fig, self.frame)
                
                #self.plot.draw()
                # self.canvas.draw()
                # self.canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1)
                #self.plot.show()
                #self.plot.draw()

    def _plot(self):
        obj = load.read_gr_file()
        obj.read_file(self.cur_path)
        self.cords = [float(i.y) for i in obj.container]
        
        self.plot.plot(self.cords, linewidth=.5)
        # preference
        if self.enable_dot:
            self.plot.plot(self.cords,'o',markersize=2,color=(1,0,0))

        

    def _replace_plot(self):
        self.clear_plot()
        self._plot()
        self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.draw()
        self.canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1)
        
        #canvas = FigureCanvasTkAgg(self.fig, self.frame)
        #self.canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1)
        #self.tool_bar.update()
        #self.frame.pack(fill=tkinter.BOTH, expand=1)
        #self.root.mainloop()

    def clear_plot(self):
        self.plot.clear()
    
    def _set_path(self, path):
        # set target path
        self.cur_path = path
    
    def _set_all_default(self):
        self.cur_path = None
        self.enable_dot = False