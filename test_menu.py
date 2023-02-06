import tkinter
from tkinter import filedialog as fd
import tkinter.messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import load
import data_plot
import timeit
from logger import logger

def do_nothing():
    pass

class TestMenu():
    def __init__(self, GUI):
        self.GUI = GUI
        self._init_test_menu()

    def _init_test_menu(self):
        test_menu = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        # test_menu.add_command(label="Graph", command=self._test_graph)
        # test_menu.add_command(label="Show Cordinate Marker", command=self._enable_cord_marker)
        self.GUI.menu_bar.add_cascade(label="Test", menu=test_menu)

    def _linear_regression(self):
        pass
    # def _test_graph(self):
    #     fig = Figure(figsize = (8, 5),
    #                 dpi = 100)
    
    #     # list of squares
    #     y = [i**2 for i in range(101)]
    
    #     # adding the subplot
    #     plot1 = fig.add_subplot(111)
    
    #     # plotting the graph
    #     plot1.plot(y)
    
    #     # creating the Tkinter canvas
    #     # containing the Matplotlib figure
    #     canvas = FigureCanvasTkAgg(fig,
    #                             master = self.GUI.root)  
    #     canvas.draw()
    
    #     # placing the canvas on the Tkinter window
    #     canvas.get_tk_widget().pack()
    
    #     # creating the Matplotlib toolbar
    #     toolbar = NavigationToolbar2Tk(canvas,
    #                                 self.GUI.root)
    #     toolbar.update()
    
    #     # placing the toolbar on the Tkinter window
    #     canvas.get_tk_widget().pack()

    # def _enable_cord_marker(self):
    #     if not self.GUI.plot and self.GUI.debug_mode:
    #         self.GUI.log._log("ERROR: Failed to enable cord marker, plot does not exist")
    #     else:
    #         self.GUI.plot.enable_dot = True
    #         self.GUI.plot._replace_plot()

if __name__ == '__main__':
    pass
    # from scipy import stats

    # x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
    # y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

    # slope, intercept, r, p, std_err = stats.linregress(x, y)

    # def myfunc(x):
    #     return slope * x + intercept

    # speed = myfunc(10)

    # print(speed)