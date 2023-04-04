# lib
import tkinter
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from time import time

# file
from helper import load

# typecheck
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main

class line_container(object):
    def __init__(self, gui: "main.GUI"):
        self.gui: "main.GUI" = gui
        self.frame: tkinter.Frame = self.gui.line_frame
        
        # containers
        self.container: dict[str,load.single_line] = dict()
        self._figure_initialization()
    
    def _figure_initialization(self) -> None:
        self.matplot_figure: Figure = Figure(figsize = (8, 5), dpi = 100)
        self.matplot_subplot: Axes = self.matplot_figure.add_subplot(111)
        self.matplot_subplot.grid()
        self.tk_canvas = FigureCanvasTkAgg(self.matplot_figure, master=self.frame)
        self.tk_toolbar = NavigationToolbar2Tk(self.tk_canvas, self.frame)
        self.tk_canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1)
        self.tk_toolbar.update()
        self.frame.pack(fill=tkinter.BOTH, expand=1)
    
    def load_and_plot(self, path: str) -> None:
        """load and plot a line
        if line is already loaded, raise error
        if not, load line and plot it on canvas
        build then append line_object to container

        Args:
            path (str): full path of line

        Raises:
            ValueError: line already loaded
        """
        # start timer
        start_time = time()
        
        # check if line already loaded
        # if yes, raise error
        if path in self.container.keys():
            raise ValueError("line already loaded")
        
        # if not, load line
        l: load.single_line = load.read_file(path)
        x_cords: list[float] = l.abs_cords_x
        y_cords: list[float] = l.abs_cords_y
        
        # plot line on canvas, finishing building line_object by appending line2d_object
        # if this is unclear, refer to load.py for more information
        temp, = self.matplot_subplot.plot(*[x_cords, y_cords], **l.parameters)
        l.line2d_object.append(temp)
        
        # add line_object to container, key is full path
        self.container[l.nick] = l
        
        # refresh canvas and stop timer
        self._refresh_canvas()
        end_time = time()
        print("[GRTK] graph loaded: ", round((end_time-start_time)*1000, 2), "ms")
    
    
    def change_line_preference(self, path: str, kwargs: dict) -> None:
        """update line preference from kwargs
        get line_object from container, update line2d_object[0] with kwargs

        Args:
            path (str): full path of line
            kwargs (dict): parameters to update
        """
        # start timer
        start_time = time()
        
        # update line preference
        self.container[path].line2d_object[0].update(kwargs)
        
        # refresh canvas and stop timer
        self._refresh_canvas()
        end_time = time()
        print("[GRTK] pref changed: ", round((end_time-start_time)*1000, 2), "ms")
    
    def _refresh_canvas(self) -> None:
        """refresh canvas after make any changes
        helper function
        """
        self.frame.pack_forget()
        self.tk_toolbar.destroy()
        self.tk_canvas.get_tk_widget().destroy()
        
        self.tk_canvas = FigureCanvasTkAgg(self.matplot_figure, master=self.frame)
        self.tk_toolbar = NavigationToolbar2Tk(self.tk_canvas, self.frame)
        self.tk_canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1)
        self.tk_toolbar.update()
        self.frame.pack(fill=tkinter.BOTH, expand=1)
        self.matplot_subplot.legend()
    
    def view_shift_left(self) -> None:
        xrange = self.matplot_subplot.get_xlim()[1] - self.matplot_subplot.get_xlim()[0]
        self.matplot_subplot.set_xlim(\
            xmin=self.matplot_subplot.get_xlim()[0]-xrange/4, \
            xmax=self.matplot_subplot.get_xlim()[1]-xrange/4)
        self.tk_canvas.draw()

    def view_shift_right(self) -> None:
        xrange = self.matplot_subplot.get_xlim()[1] - self.matplot_subplot.get_xlim()[0]
        self.matplot_subplot.set_xlim(\
            xmin=self.matplot_subplot.get_xlim()[0]+xrange/4, \
            xmax=self.matplot_subplot.get_xlim()[1]+xrange/4)
        self.tk_canvas.draw()

    def view_zoom_out(self) -> None:
        xrange = self.matplot_subplot.get_xlim()[1] - self.matplot_subplot.get_xlim()[0]
        self.matplot_subplot.set_xlim(\
            xmin=self.matplot_subplot.get_xlim()[0]-xrange/4, \
            xmax=self.matplot_subplot.get_xlim()[1]+xrange/4)
        self.tk_canvas.draw()

    def view_zoom_in(self) -> None:
        xrange = self.matplot_subplot.get_xlim()[1] - self.matplot_subplot.get_xlim()[0]
        self.matplot_subplot.set_xlim(\
            xmin=self.matplot_subplot.get_xlim()[0]+xrange/4, \
            xmax=self.matplot_subplot.get_xlim()[1]-xrange/4)
        self.tk_canvas.draw()
