# lib
import tkinter
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) # type: ignore
import matplotlib.style as mplstyle
from time import time
import numpy
import pathlib

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
        self.show_legend: bool = True
        if self.gui.optimize:
            mplstyle.use('fast')
        
        # containers
        self.container: dict[str,load.single_line] = dict()
        
        # default style
        self.legend_style = dict(
            loc='upper center',
            bbox_to_anchor=(0.5, 1.1),
            facecolor="black",
            ncol=3,
            edgecolor="black",
            labelcolor="white"
        )
        
        # init figure
        self._figure_initialization()
    
    def _figure_initialization(self) -> None:
        self.matplot_figure: Figure = Figure(figsize = (8, 5), dpi = 100)
        self.matplot_subplot: Axes = self.matplot_figure.add_subplot(1,1,1) # type: ignore
        self.change_color_theme(theme="dark")
        self.matplot_subplot.grid(color="grey", visible=True)
        self.tk_canvas = FigureCanvasTkAgg(self.matplot_figure, master=self.frame)
        self.tk_toolbar = NavigationToolbar2Tk(self.tk_canvas, self.frame)
        self.tk_canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1) # type: ignore
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
        for i in list(self.container.keys()):
            if pathlib.Path(path).name in i:
                raise ValueError("line already loaded")
        
        # if not, load line
        layers: dict[str,list[list[float]]] = load.read_file(path)
        for k, v in layers.items():
            l = load.single_line(name=k, cords=v)
            x_cords: list[float] = l.abs_cords_x
            y_cords: list[float] = l.abs_cords_y
            main_l, = self.matplot_subplot.plot(*[x_cords, y_cords], **l.parameters)
            l.line2d_object.append(main_l)
            
            # add line_object to container, key is full path
            self.container[l.nick] = l
        
        # refresh canvas and stop timer
        self._refresh_canvas()
        self.gui.pref.refresh()
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
        self.tk_canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1) # type: ignore
        self.tk_toolbar.update()
        self.frame.pack(fill=tkinter.BOTH, expand=1)
        
        if len(list(self.container.keys())) > 0:
            if self.show_legend:
                self.matplot_subplot.legend(**self.legend_style)
            else:
                self.matplot_subplot.legend().remove()
    
    def change_color_theme(self, theme: str) -> None:
        if theme == "light":
            FACE_COLOR = "white"
            EDGE_COLOR = "white"
            TICK_COLOR = "black"
            LABEL_COLOR = "black"
            SPINE_COLOR = "black"
        else:
            FACE_COLOR = "black"
            EDGE_COLOR = "black"
            TICK_COLOR = "white"
            LABEL_COLOR = "white"
            SPINE_COLOR = "white"
        self.matplot_figure.set_facecolor(EDGE_COLOR)
        self.matplot_subplot.set_facecolor(FACE_COLOR)
        self.matplot_subplot.tick_params(axis="x", colors=TICK_COLOR)
        self.matplot_subplot.tick_params(axis="y", colors=TICK_COLOR)
        self.matplot_subplot.set_xlabel("Time", color=LABEL_COLOR)
        self.matplot_subplot.set_ylabel("Position", color=LABEL_COLOR)
        self.matplot_subplot.spines["bottom"].set_color(SPINE_COLOR)
        self.matplot_subplot.spines["top"].set_color(SPINE_COLOR)
        self.matplot_subplot.spines["left"].set_color(SPINE_COLOR)
        self.matplot_subplot.spines["right"].set_color(SPINE_COLOR)
    
    def change_grid(self, show: bool) -> None:
        if show:
            self.matplot_subplot.grid(color="grey", visible=True)
        else:
            self.matplot_subplot.grid(False)
    
    def change_label(self, show: bool, x: str="Time", y: str="Position") -> None:
        if show:
            self.matplot_subplot.set_xlabel(x)
            self.matplot_subplot.set_ylabel(y)
        else:
            self.matplot_subplot.set_xlabel("")
            self.matplot_subplot.set_ylabel("")
    
    def change_axis(self, show: bool) -> None:
        if show:
            self.matplot_subplot.axis("on")
        else:
            self.matplot_subplot.axis("off")
    
    def change_legend(self, show: bool) -> None:
        self.show_legend = True if show else False
    
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
