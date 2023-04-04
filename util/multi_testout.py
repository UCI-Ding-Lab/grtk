from numpy import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import math
import tkinter
from matplotlib import axes, lines

def func(plot: axes.Axes):
    plot1.plot(t, b, **parameterB, label = "cos(t)")
    # hide sin(t)
    for i in plot.get_lines():
        if i.get_label() == "sin(t)":
            i.set_visible(False)
    plot.legend()

def func2(plot: axes.Axes):
    for i in plot.get_lines():
        print(i.get_label())

if __name__ == "__main__":
    t = linspace(0, 2*math.pi, 400)
    a = sin(t)
    b = cos(t)
    c = a + b
    
    root = tkinter.Tk()
    
    fig = Figure(figsize = (8, 5), dpi = 100)
    plot1 = fig.add_subplot(111)
    
    parameterA  = dict(
        color="blue",
        linewidth=1,
    )
    parameterB  = dict(
        color="red",
        linewidth=1,
    )
    plot1.plot(t, a, **parameterA, label = "sin(t)")
    plot1.grid()
    plot1.legend()
    canvas = FigureCanvasTkAgg(fig, master = root)  
    canvas.draw()
    canvas.get_tk_widget().pack()
    but = tkinter.Button(root, text = "test", command = lambda: func(plot1))
    but.pack()
    but2 = tkinter.Button(root, text = "print line", command = lambda: func2(plot1))
    but2.pack()
    root.mainloop()