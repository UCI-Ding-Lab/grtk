import tkinter
from tkinter import filedialog as fd
import tkinter.messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import load
from data_plot import DataPlot
import timeit
from logger import logger


def do_nothing():
    pass

class GUI:
    def __init__(self, root: tkinter.Tk):
        self.log = logger()
        self.debug_mode = False
        self.root = root
        self.menu_bar = tkinter.Menu(root)
        self.frame = tkinter.Frame()
        self.option_frame = tkinter.Frame()
        self.plot = None
        self._window()
        self._menu_bar_main()

        root.config(menu=self.menu_bar)
        root.mainloop()
        self.log._close()

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
        file_menu.add_command(label="Load Gr File", command=self._menu_bar_file_load_gr_file)
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
        options_menu.add_command(label="Line Color", command=lambda: self._color_options("l"))
        options_menu.add_command(label="Marker Color", command=lambda: self._color_options("m"))
        options_menu.add_command(label="Line Width", command=do_nothing)
        options_menu.add_command(label="Line Type", command=do_nothing)
        
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
        test_menu.add_command(label="Show Cordinate Marker", command=self._enable_cord_marker)
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

    def _menu_bar_file_load_gr_file(self):
        try:
            filetypes = (
                ('gr files', '*.gr'),
                ('text files', '*.txt'),
                ('All files', '*.*')
            )

            file_path = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)

            start = timeit.default_timer()
            if self.plot == None:
                self.plot = DataPlot(self.frame)
            
            self.plot.plot_file(file_path)
            
            stop = timeit.default_timer()
            if self.debug_mode:
                self.log._log(f'graph loaded, runtime = {stop-start} s')
        except Exception as e:
            if self.debug_mode:
                self.log._log("ERROR: "+repr(e))
            raise e
    
    def _enable_cord_marker(self):
        if not self.plot and self.debug_mode:
            self.log._log("ERROR: Failed to enable cord marker, plot does not exist")
        else:
            self.plot.enable_dot = True
            self.plot._replace_plot()
    
    def _color_options(self, type):
        def save_to_opt(self, choice: tkinter.StringVar):
            if type == "m":
                self.plot.options["dot_color"] = choice.get()
            else:
                self.plot.options["line_color"] = choice.get()
            self.plot._replace_plot()
            for i in self.option_frame.winfo_children():
                i.destroy()
            self.option_frame.pack_forget()
        choice = tkinter.StringVar()
        tkinter.Radiobutton(self.option_frame, value="red", variable=choice, bg='red').grid(row=0,column=0)
        tkinter.Radiobutton(self.option_frame, value="green", variable=choice, bg='green').grid(row=0,column=1)
        tkinter.Radiobutton(self.option_frame, value="blue", variable=choice, bg='blue').grid(row=0,column=2)
        tkinter.Radiobutton(self.option_frame, value="cyan", variable=choice, bg='cyan').grid(row=0,column=3)
        tkinter.Radiobutton(self.option_frame, value="magenta", variable=choice, bg='magenta').grid(row=0,column=4)
        tkinter.Radiobutton(self.option_frame, value="yellow", variable=choice, bg='yellow').grid(row=0,column=5)
        tkinter.Radiobutton(self.option_frame, value="black", variable=choice, bg='black').grid(row=0,column=6)
        tkinter.Radiobutton(self.option_frame, value="white", variable=choice, bg='white').grid(row=0,column=7)
        tkinter.Button(self.option_frame, text="Save", command=lambda: save_to_opt(self, choice)).grid(row=0,column=8)
        self.option_frame.pack()
        
        


class Window:
    pass

if __name__ == '__main__':
    root = tkinter.Tk()
    app = GUI(root)