import tkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import load

def do_nothing():
    pass

class GUI:
    def __init__(self, root):
        self.root = root
        self.menu_bar = tkinter.Menu(root)

        self._window()
        self._menu_bar_main()

        root.config(menu=self.menu_bar)
        root.mainloop()

    def _window(self):
        self.root.title('Data Visualization Software')
        self.root.geometry("800x600")
        
    def _menu_bar_main(self):
        self._menu_bar_file()
        self._menu_bar_edit()
        self._menu_bar_options()
        self._menu_bar_tools()
        self._menu_bar_treatment()

        # for testing purpose
        self._menu_bar_test()
    
    def _menu_bar_file(self):
        file_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Test OpenGL", command=do_nothing)
        file_menu.add_command(label="Load Gr File", command=do_nothing)
        file_menu.add_command(label="Load Gr File in a New Window", command=do_nothing)
        file_menu.add_separator()
        file_menu.add_command(label="Load Plug'in", command=do_nothing)
        file_menu.add_command(label="Unload Plug'in", command=do_nothing)
        file_menu.add_separator()
        file_menu.add_command(label="Quit All Windows", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def _menu_bar_edit(self):
        edit_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Copy Image", command=do_nothing)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

    def _menu_bar_options(self):
        options_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        options_menu.add_command(label="Whatever", command=do_nothing)
        self.menu_bar.add_cascade(label="Options", menu=options_menu)

    def _menu_bar_tools(self):
        tools_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="Whatever", command=do_nothing)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)

    def _menu_bar_treatment(self):
        treatment_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        treatment_menu.add_command(label="Whatever", command=do_nothing)
        self.menu_bar.add_cascade(label="Treatment", menu=treatment_menu)

    def _menu_bar_test(self):
        test_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        test_menu.add_command(label="Graph", command=self._menu_bar_test_graph)
        test_menu.add_command(label="Float", command=self._menu_bar_test_float)
        self.menu_bar.add_cascade(label="Test", menu=test_menu)

    def _menu_bar_test_graph(self):
        fig = Figure(figsize = (8, 5),
                    dpi = 100)
    
        # list of squares
        y = [i**2 for i in range(101)]
    
        # adding the subplot
        plot1 = fig.add_subplot(111)
    
        # plotting the graph
        plot1.plot(y)
    
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                master = self.root)  
        canvas.draw()
    
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                    self.root)
        toolbar.update()
    
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
    
    def _menu_bar_test_float(self):
        dir = "test_data.gr"
        obj = load.read_gr_file()
        obj.read_file(dir)
        fig = Figure(figsize = (8, 5),
                    dpi = 100)
        y = [float(i.y) for i in obj.container]
        plot1 = fig.add_subplot(111)
        plot1.plot(y)
        canvas = FigureCanvasTkAgg(fig,
                                master = self.root)  
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,
                                    self.root)
        toolbar.update()
        canvas.get_tk_widget().pack()
        

if __name__ == '__main__':
    root = tkinter.Tk()
    app = GUI(root)

