import numpy
from helper import load
from tkinter import ttk
import custom
import inspect

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main

class operations:
    FILE = "untitled"
    TYPE = "Operations"
    CURVE = 0
    def __init__(self):
        pass
    def opt_subtract(self, target_A: load.single_line, target_B: load.single_line):
        if target_A.abs_cords_x.size != target_B.abs_cords_x.size:
            bigger = target_A if target_A.abs_cords_x.size > target_B.abs_cords_x.size else target_B
        else:
            bigger = target_A
        if target_A.abs_cords_y.size >= target_B.abs_cords_y.size:
            cords_y = numpy.array(target_A.abs_cords_y[:target_B.abs_cords_y.size] - target_B.abs_cords_y)
            cords_x = bigger.abs_cords_x[:target_B.abs_cords_y.size]
        else:
            cords_y = numpy.array(target_A.abs_cords_y - target_B.abs_cords_y[:target_A.abs_cords_y.size])
            cords_x = bigger.abs_cords_x[:target_A.abs_cords_y.size]
        target_C: load.single_line = load.single_line(
            file=operations.FILE,
            curve=str(operations.CURVE),
            type=operations.TYPE,
            cords=numpy.array([cords_x, cords_y]),
            file_path=operations.FILE
        )
        return target_C
    def opt_addition(self, target_A: load.single_line, target_B: load.single_line):
        if target_A.abs_cords_x.size != target_B.abs_cords_x.size:
            bigger = target_A if target_A.abs_cords_x.size > target_B.abs_cords_x.size else target_B
        else:
            bigger = target_A
        if target_A.abs_cords_y.size >= target_B.abs_cords_y.size:
            cords_y = numpy.array(target_A.abs_cords_y[:target_B.abs_cords_y.size] + target_B.abs_cords_y)
            cords_x = bigger.abs_cords_x[:target_B.abs_cords_y.size]
        else:
            cords_y = numpy.array(target_A.abs_cords_y + target_B.abs_cords_y[:target_A.abs_cords_y.size])
            cords_x = bigger.abs_cords_x[:target_A.abs_cords_y.size]
        target_C: load.single_line = load.single_line(
            file=operations.FILE,
            curve=str(operations.CURVE),
            type=operations.TYPE,
            cords=numpy.array([cords_x, cords_y]),
            file_path=operations.FILE
        )
        return target_C
    
    def selection(self, gui: "main.GUI"):
        container = gui.container.container
        widget = gui.pref.tree
        if len(widget.selection()) == 2:
            A = widget.selection()[0].split("@")
            B = widget.selection()[1].split("@")
            target_A = container[A[1]][A[0]][A[2]]
            target_B = container[B[1]][B[0]][B[2]]
            return target_A, target_B
        else:
            return None, None
        
    def menu_perform(self, gui: "main.GUI", action: str):
        target_A, target_B = self.selection(gui)
        if target_A is not None and target_B is not None:
            if action == "+":
                obj = self.opt_addition(target_A, target_B)
            elif action == "-":
                obj = self.opt_subtract(target_A, target_B)
        gui.container.load_and_plot_obj(target=obj)
        operations.CURVE += 1
    
    def cus_perform(self, gui: "main.GUI", cus):
        A, B = self.selection(gui)
        func = getattr(custom.labCustom, cus)
        X, Y = func(gui.usr_cus, A, B)
        target_C: load.single_line = load.single_line(
            file=operations.FILE,
            curve=str(operations.CURVE),
            type=operations.TYPE,
            cords=numpy.array([X, Y]),
            file_path=operations.FILE
        )
        gui.container.load_and_plot_obj(target=target_C)
        operations.CURVE += 1