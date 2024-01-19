# lib
import colorsys
import tkinter
from tkinter import ttk
import matplotlib.backend_bases
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) # type: ignore
import matplotlib.style as mplstyle
from time import time
import pathlib
import random
import sys

from collections import defaultdict

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
        self.show_legend: bool = False
        self.color_rand = lambda: random.randint(128,255)
        if self.gui.setting.OPTIMIZE:
            mplstyle.use('fast')
            
        # plugins
        self.on_draw_job=[]
        
        # containers
        self.container = defaultdict(lambda: defaultdict(dict[str, load.single_line]))
             
        # default style
        self.legend_style = self.gui.setting.LEGEND_STYLE
        
        # init figure
        self._figure_initialization()
    
    def _figure_initialization(self) -> None:
        if sys.platform == "win32":
            self.matplot_figure: Figure = Figure(
                figsize=(self.gui.setting.WIN_FIGURE_WIDTH,self.gui.setting.WIN_FIGURE_HEIGHT),
                dpi=self.gui.setting.WIN_FIGURE_DPI
            )
        else:
            self.matplot_figure: Figure = Figure(
                figsize=(self.gui.setting.UNX_FIGURE_WIDTH,self.gui.setting.UNX_FIGURE_HEIGHT),
                dpi=self.gui.setting.UNX_FIGURE_DPI
            )
        self.matplot_subplot: Axes = self.matplot_figure.add_subplot(1,1,1) # type: ignore
        self.change_color_theme(theme="DARK")
        self.matplot_subplot.grid(color="grey", visible=True)
        self.tk_canvas = FigureCanvasTkAgg(self.matplot_figure, master=self.frame)
        self.tk_toolbar = NavigationToolbar2Tk(self.tk_canvas, self.frame)
        self.tk_canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1) # type: ignore
        self.tk_toolbar.update()
        self.scroll = self.zoom_factory()
        self.tk_canvas.mpl_connect('scroll_event', self.scroll)
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
        self.gui.log.timerStart("line_container.load_and_plot")
        short = pathlib.Path(path).name
        
        # if not, load line
        if path.endswith('.gr') or path.endswith('.gz'):
            # readfile
            self.gui.log.timerStart("line_container.load_and_plot/load.read_file")
            if path.endswith('.gr'):
                load.read_file(path, self.container, self.gui.log)
            elif path.endswith('.gz'):
                load.read_gzip(path, self.container, self.gui.log)
            self.gui.log.timerEnd("line_container.load_and_plot/load.read_file")
            
            # progressbar init
            self.gui.log.timerStart("line_container.load_and_plot/progressbar_init")
            ttlLines = 0
            for key in list(self.container[short].keys()):
                ttlLines += len(list(self.container[short][key].values()))
            progressbar = ttk.Progressbar(
                self.gui.tip_frame,
                maximum=ttlLines,
                length=300,
                style="red.Horizontal.TProgressbar"
            )
            progressbar.pack()
            self.gui.log.timerEnd("line_container.load_and_plot/progressbar_init")
            
            # plot dict
            self.gui.log.timerStart("line_container.load_and_plot/plot_dict")
            for key in list(self.container[short].keys()):
                for l in list(self.container[short][key].values()):
                    # plot line
                    self.gui.log.timerStart(f"line_container.load_and_plot/plot_{l.nick}")
                    main_l, = self.matplot_subplot.plot(l.abs_cords_x, l.abs_cords_y, **l.parameters)
                    self.gui.log.timerEnd(f"line_container.load_and_plot/plot_{l.nick}")
                    # plugin router
                    self.gui.log.timerStart(f"line_container.load_and_plot/plot_{l.nick}_plugin")
                    for job in self.on_draw_job:
                        job()
                    self.gui.log.timerEnd(f"line_container.load_and_plot/plot_{l.nick}_plugin")
                    # store reference
                    l.line2d_object.append(main_l)
                    # enhance progressbar
                    self.gui.log.timerStart(f"line_container.load_and_plot/plot_{l.nick}_pgbarstep")
                    progressbar.step()
                    self.gui.log.timerEnd(f"line_container.load_and_plot/plot_{l.nick}_pgbarstep")
                    self.gui.log.timerStart(f"line_container.load_and_plot/plot_{l.nick}_update")
                    self.gui.tip_frame.update_idletasks()
                    self.gui.log.timerEnd(f"line_container.load_and_plot/plot_{l.nick}_update")
            self.gui.log.timerEnd("line_container.load_and_plot/plot_dict")
            
            progressbar.destroy()
        elif path.endswith('.txt'):
            key_list = list(load.read_txt(path, self.container))
            for short, key, i2 in key_list:
                l = self.container[short][key][i2]
                main_l, = self.matplot_subplot.plot(*l.plt_cords, **l.parameters)
                l.line2d_object.append(main_l)
                

        
        # refresh canvas and stop timer
        self._refresh_canvas()
        self.gui.pref.refresh()
        self.gui.log.timerEnd("line_container.load_and_plot")
    
    def load_and_plot_obj(self, target: load.single_line):
        main_l, = self.matplot_subplot.plot(*target.plt_cords, **target.parameters)
        target.line2d_object.append(main_l)
        self.container[target.parent][target.curve_type][target.nick] = target
        self._refresh_canvas()
        self.gui.pref.refresh()
    
    def change_line_preference(self, path: str, type: str, curve: str, kwargs: dict) -> None:
        """update line preference from kwargs
        get line_object from container, update line2d_object[0] with kwargs

        Args:
            path (str): full path of line
            kwargs (dict): parameters to update
        """
        # update line preference
        self.container[path][type][curve].line2d_object[0].update(kwargs)
        
        # refresh canvas
        self._refresh_canvas()
        self._set_GUI_saved_false()
    
    def _refresh_canvas(self) -> None:
        """refresh canvas after make any changes
        helper function
        """
        self.tk_canvas.draw_idle()
        
        if len(list(self.container.keys())) > 0:
            if self.show_legend:
                self.matplot_subplot.legend(**self.legend_style)
            else:
                self.matplot_subplot.legend().remove()
    
    def change_color_theme(self, theme: str) -> None:
        self.matplot_figure.set_facecolor(self.gui.setting.GRAPH_THEME[theme]["EDGE_COLOR"])
        self.matplot_subplot.set_facecolor(self.gui.setting.GRAPH_THEME[theme]["FACE_COLOR"])
        self.matplot_subplot.tick_params(axis="x", colors=self.gui.setting.GRAPH_THEME[theme]["TICK_COLOR"])
        self.matplot_subplot.tick_params(axis="y", colors=self.gui.setting.GRAPH_THEME[theme]["TICK_COLOR"])
        self.matplot_subplot.set_xlabel("Time", color=self.gui.setting.GRAPH_THEME[theme]["LABEL_COLOR"])
        self.matplot_subplot.set_ylabel("Position", color=self.gui.setting.GRAPH_THEME[theme]["LABEL_COLOR"])
        self.matplot_subplot.spines["bottom"].set_color(self.gui.setting.GRAPH_THEME[theme]["SPINE_COLOR"])
        self.matplot_subplot.spines["top"].set_color(self.gui.setting.GRAPH_THEME[theme]["SPINE_COLOR"])
        self.matplot_subplot.spines["left"].set_color(self.gui.setting.GRAPH_THEME[theme]["SPINE_COLOR"])
        self.matplot_subplot.spines["right"].set_color(self.gui.setting.GRAPH_THEME[theme]["SPINE_COLOR"])
    
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
    
    def zoom_factory(self):
        ax = self.matplot_subplot
        base_scale = self.gui.setting.BASE_SCALE
        def zoom_fun(event: matplotlib.backend_bases.MouseEvent):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            cur_xrange = (cur_xlim[1] - cur_xlim[0]) * self.gui.setting.ZOOM_FACTOR
            cur_yrange = (cur_ylim[1] - cur_ylim[0]) * self.gui.setting.ZOOM_FACTOR
            xdata = event.xdata
            ydata = event.ydata
            if event.button == 'up':
                scale_factor = 1 / base_scale
            else:
                scale_factor = base_scale
            ax.set_xlim([xdata - cur_xrange * scale_factor, xdata + cur_xrange * scale_factor])
            ax.set_ylim([ydata - cur_yrange * scale_factor, ydata + cur_yrange * scale_factor])
            self.tk_canvas.draw()
        return zoom_fun

    def get_curves_list(self) -> list:
        """ In each row of the returned list:
            0 : file path
            1 : curve type
            2 : curve id
            3 : visibility (visible)
            4 : color
            5 : linewidth
            6 : marker
            7 : markersize
            8 : markerfacecolor
            9 : markeredgecolor
            10 : hovertip
            11 : coordinates

        Returns:
            list: a list of curves in the container with all properties specified.
        """
        temp = []
        for i in self.container.keys():
            for j in self.container[i].keys():
                for r in self.container[i][j].keys():
                    temp.append((self.container[i][j][r].file_path, j, r, \
                        self.container[i][j][r].line2d_object[0].get_visible(), \
                        self.container[i][j][r].line2d_object[0].get_color(), \
                        self.container[i][j][r].line2d_object[0].get_linewidth(), \
                        self.container[i][j][r].line2d_object[0].get_marker(), \
                        self.container[i][j][r].line2d_object[0].get_markersize(), \
                        self.container[i][j][r].line2d_object[0].get_markerfacecolor(), \
                        self.container[i][j][r].line2d_object[0].get_markeredgecolor(), \
                        self.container[i][j][r].tip, \
                        self.container[i][j][r].plt_cords))
        return temp
        
    def _set_GUI_saved_false(self):
        self.gui.root.title('Data Visualization Software (unsaved)')
        self.gui.saved = False
        return None