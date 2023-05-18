import numpy
from helper import load
from tkinter import ttk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main

class operations:
    FILE = "untitled"
    TYPE = "Operations"
    CURVE = 0
    def __init__(self):
        pass
    def subtract(self, target_A: load.single_line, target_B: load.single_line):
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
        operations.CURVE += 1
        return target_C
    def addition(self, target_A: load.single_line, target_B: load.single_line):
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
        operations.CURVE += 1
        return target_C
    def perform(self, gui: "main.GUI", action: str):
        container = gui.container.container
        widget = gui.pref.tree
        A = widget.selection()[0].split("@")
        B = widget.selection()[1].split("@")
        target_A = container[A[1]][A[0]][A[2]]
        target_B = container[B[1]][B[0]][B[2]]
        if len(widget.selection()) == 2:
            if action == "+":
                obj = self.addition(target_A, target_B)
            elif action == "-":
                obj = self.subtract(target_A, target_B)
            elif action == "*":
                pass
            elif action == "/":
                pass
        gui.container.load_and_plot_obj(target=obj)