# lib
import tkinter
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# file
from helper import load
from menus import edit_menu
from bin import layer_control

class single_line(object):
    def __init__(self, cords: list[load.anchor], file_path: str):
        
        # single line cords in anchor object
        self.cord: list[load.anchor] = cords
        
        self.file_path = file_path
        self.parameters = dict(
            linewidth=0.5,
            color="black",
        )
        
        # single line y cords
        self.abs_cords_y = [float(i.y) for i in cords]
        # single line x cords
        self.abs_cords_x = [float(i.x) for i in cords]
        
    def set_parameters(self, new_parameters: dict):
        self.parameters = new_parameters

class line_container(object):
    def __init__(self, frame: tkinter.Frame, menu_obj: dict[str, object]):
        self.frame = frame
        self.menu_obj = menu_obj
        # containers
        self.container: list[single_line] = []
        self.garbage: list[single_line] = []
        # file loader object
        self.loader = load.read_gr_file()
        # figure init
        self.matplot_figure: Figure = Figure(figsize = (8, 5), dpi = 100)
        self.matplot_subplot: Axes = self.matplot_figure.add_subplot(111)
        self.matplot_subplot.grid()
        self.tk_canvas = FigureCanvasTkAgg(self.matplot_figure, master=self.frame)
        self.tk_toolbar = NavigationToolbar2Tk(self.tk_canvas, self.frame)
        self.tk_canvas._tkcanvas.pack(fill=tkinter.BOTH, expand=1)
        self.tk_toolbar.update()
        self.frame.pack(fill=tkinter.BOTH, expand=1)
    
    def load_and_plot(self, path: str) -> None:
        """Load line by path.
        get path and build a single line object
        draw single line object on the canvas
        add single line object to container
        add single line to edit menu
        refresh canvas

        Args:
            path (str): full file path
        """
        in_garbage = False
        for i in self.garbage:
            if i.file_path == path:
                in_garbage = True
                path_object = i
                x_cords = i.abs_cords_x
                y_cords = i.abs_cords_y
                break
        if not in_garbage:
            self.loader.read_file(path)
            anchor_container = self.loader.get_result()
            path_object = single_line(anchor_container, path)
            x_cords = path_object.abs_cords_x
            y_cords = path_object.abs_cords_y
            self.menu_obj["layer"].add_layer(path)
            
        self.matplot_subplot.plot(*[x_cords, y_cords], **path_object.parameters)
        self.container.append(path_object)
        self.add_to_menu(path)
        self.refresh_canvas()
    
    def remove_line(self, path: str) -> None:
        """Remove line from the graph
        get path and find the index of single line obeject in the container
        use index to pop the line by index in Axes
        use path to remove from menu
        put the deleted single line object in garbage container for future use

        Args:
            path (str): full file path
        """
        counter = 0
        target: int = None
        for i in self.container:
            if i.file_path == path:
                target = counter
                break
            counter += 1
        self.matplot_subplot.lines.pop(target)
        
        found = False
        for i in self.garbage:
            if i.file_path == path:
                found = True
                break
        if not found:
            self.garbage.append(self.container[counter])

        self.container.pop(counter)
        self.remove_from_menu(path)
        self.refresh_canvas()
    
    def change_line_preference(self, path: str, **kwargs: dict) -> None:
        """change line preference according to content in dictionary
        find the single line object that need to change preference in the container
        get the line Axes from subplot and update configs
        
        Args:
            path (str): full file path
        """
        counter = 0
        target: int = None
        for i in self.container:
            if i.file_path == path:
                target = counter
                break
            counter += 1
        self.matplot_subplot.get_lines()[target].update(kwargs)
    
    def refresh_canvas(self) -> None:
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
    
    def add_to_menu(self, path: str) -> None:
        """add path to edit menu
        helper function

        Args:
            path (str): full file path
        """
        em: edit_menu.EditMenu = self.menu_obj["edit"]
        em.add_path(path=path)
    
    def remove_from_menu(self, path: str) -> None:
        """delete path from edit menu
        helper function

        Args:
            path (str): full file path
        """
        em: edit_menu.EditMenu = self.menu_obj["edit"]
        em.del_path(path=path)
    
    def view_shift_left(self):
        xrange = self.matplot_subplot.get_xlim()[1] - self.matplot_subplot.get_xlim()[0]
        self.matplot_subplot.set_xlim(\
            xmin=self.matplot_subplot.get_xlim()[0]-xrange/4, \
            xmax=self.matplot_subplot.get_xlim()[1]-xrange/4)
        self.tk_canvas.draw()

    def view_shift_right(self):
        xrange = self.matplot_subplot.get_xlim()[1] - self.matplot_subplot.get_xlim()[0]
        self.matplot_subplot.set_xlim(\
            xmin=self.matplot_subplot.get_xlim()[0]+xrange/4, \
            xmax=self.matplot_subplot.get_xlim()[1]+xrange/4)
        self.tk_canvas.draw()

    def view_zoom_out(self):
        xrange = self.matplot_subplot.get_xlim()[1] - self.matplot_subplot.get_xlim()[0]
        self.matplot_subplot.set_xlim(\
            xmin=self.matplot_subplot.get_xlim()[0]-xrange/4, \
            xmax=self.matplot_subplot.get_xlim()[1]+xrange/4)
        self.tk_canvas.draw()

    def view_zoom_in(self):
        xrange = self.matplot_subplot.get_xlim()[1] - self.matplot_subplot.get_xlim()[0]
        self.matplot_subplot.set_xlim(\
            xmin=self.matplot_subplot.get_xlim()[0]+xrange/4, \
            xmax=self.matplot_subplot.get_xlim()[1]-xrange/4)
        self.tk_canvas.draw()




