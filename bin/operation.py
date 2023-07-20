import numpy
from helper import load
from tkinter import ttk
import custom
import inspect
from tkinter import messagebox
import tkinter as tk
import pathlib

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main
    
def do_nothing():
    pass

class operations:
    FILE = "untitled"
    TYPE = "Operations"
    CURVE = 0
    def __init__(self):
        pass
    # def opt_subtract(self, target_A: load.single_line, target_B: load.single_line):
    #     if target_A.abs_cords_x.size != target_B.abs_cords_x.size:
    #         bigger = target_A if target_A.abs_cords_x.size > target_B.abs_cords_x.size else target_B
    #     else:
    #         bigger = target_A
    #     if target_A.abs_cords_y.size >= target_B.abs_cords_y.size:
    #         cords_y = numpy.array(target_A.abs_cords_y[:target_B.abs_cords_y.size] - target_B.abs_cords_y)
    #         cords_x = bigger.abs_cords_x[:target_B.abs_cords_y.size]
    #     else:
    #         cords_y = numpy.array(target_A.abs_cords_y - target_B.abs_cords_y[:target_A.abs_cords_y.size])
    #         cords_x = bigger.abs_cords_x[:target_A.abs_cords_y.size]
    #     target_C: load.single_line = load.single_line(
    #         file=operations.FILE,
    #         curve=str(operations.CURVE),
    #         type=operations.TYPE,
    #         cords=numpy.array([cords_x, cords_y]),
    #         file_path=operations.FILE
    #     )
    #     return target_C
    # def opt_addition(self, target_A: load.single_line, target_B: load.single_line):
    #     if target_A.abs_cords_x.size != target_B.abs_cords_x.size:
    #         bigger = target_A if target_A.abs_cords_x.size > target_B.abs_cords_x.size else target_B
    #     else:
    #         bigger = target_A
    #     if target_A.abs_cords_y.size >= target_B.abs_cords_y.size:
    #         cords_y = numpy.array(target_A.abs_cords_y[:target_B.abs_cords_y.size] + target_B.abs_cords_y)
    #         cords_x = bigger.abs_cords_x[:target_B.abs_cords_y.size]
    #     else:
    #         cords_y = numpy.array(target_A.abs_cords_y + target_B.abs_cords_y[:target_A.abs_cords_y.size])
    #         cords_x = bigger.abs_cords_x[:target_A.abs_cords_y.size]
    #     target_C: load.single_line = load.single_line(
    #         file=operations.FILE,
    #         curve=str(operations.CURVE),
    #         type=operations.TYPE,
    #         cords=numpy.array([cords_x, cords_y]),
    #         file_path=operations.FILE
    #     )
    #     return target_C
    
    # def opt_averaging(self, target_A: load.single_line, target_B: load.single_line):
    #     # print('targ A x:::', target_A.abs_cords_x.size)
    #     # print('targ A y:::', target_A.abs_cords_y.size)
    #     # print('targ B x:::', target_B.abs_cords_x.size)
    #     # print('targ B y:::', target_B.abs_cords_y.size)
    #     if target_A.abs_cords_x.size != target_B.abs_cords_x.size:
    #         messagebox.showerror("Operation Unsuccessful", "The selected curves have different sizes:\n" + \
    #             f"{target_A.nick}(x, y): ({target_A.abs_cords_x.size}, {target_A.abs_cords_y.size})\n" + \
    #             f"{target_B.nick}(x, y): ({target_B.abs_cords_x.size}, {target_B.abs_cords_y.size})")
    #         return None
    #     coords_y = (target_A.abs_cords_y + target_B.abs_cords_y) / 2
    #     target_C: load.single_line = load.single_line(
    #         file=operations.FILE,
    #         curve=str(operations.CURVE),
    #         type=operations.TYPE,
    #         cords=numpy.array([target_A.abs_cords_x, coords_y]),
    #         file_path=operations.FILE
    #     )
    #     return target_C
    
    
    def _get_subtraction_result(self, window, result_curve, gui, listbox1, listbox2):
        # listbox1 is minuend.
        # listbox2 is subtrahend.
        
        # selected_items = []
        # for i in listboxes:
        #     selected_items.append([i.get(idx) for idx in i.curselection()])
        # return selected_items

        minuend_curves = [listbox1.get(idx) for idx in listbox1.curselection()]
        subtrahend_curves = [listbox2.get(idx) for idx in listbox2.curselection()]
        
        if minuend_curves == [] or subtrahend_curves == []:
            return None
        
        file_name, type_name, nick_name = minuend_curves[0].split('/')
        print(file_name, type_name, nick_name)
        cords_y = numpy.array(gui.container.container[file_name][type_name][nick_name].abs_cords_y)
        cords_x = numpy.array(gui.container.container[file_name][type_name][nick_name].abs_cords_x)
        for i in subtrahend_curves:
            file_name, type_name, nick_name = i.split('/')
            cords_y = cords_y - gui.container.container[file_name][type_name][nick_name].abs_cords_y
        result_curve: load.single_line = load.single_line(
            file=operations.FILE,
            curve=str(operations.CURVE),
            type=operations.TYPE,
            cords=numpy.array([cords_x, cords_y]),
            file_path=operations.FILE
        )
        gui.container.load_and_plot_obj(target=result_curve)
        window.destroy()
        return result_curve
        #.abs_cords_y
        
    
    def opt_subtraction(self, gui):
        # top = tk.Toplevel(gui.root)
        # top.geometry("750x250")
        # top.title("Subtraction")
        
        # frame = tk.Frame(top)
        # frame.pack(pady=10)

        # # Create a scroll bar
        # scrollbar = tk.Scrollbar(frame)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
        # listbox.pack(side=tk.LEFT)

        # # Configure the scroll bar
        # scrollbar.config(command=listbox.yview)
        
        
        
        # button1=tk.Button(top,text='Cancel',width=15,height=1, command=do_nothing)
        # button1.pack(side='right', anchor='sw', padx=10, pady=10)
        # button2=tk.Button(top,text='Confirm',width=15,height=1, command=do_nothing)
        # button2.pack(side='right', anchor='se', expand=True, padx=10, pady=10)
        # # print("DONE")
        result_curve = None
        
        top = tk.Toplevel(gui.root)
        top.geometry("500x250")
        top.title("Subtraction")

        frame_lists = tk.Frame(top)
        frame_lists.pack(side='top', expand=True, fill=tk.X)

        frame_list1 = tk.Frame(frame_lists)
        frame_list1.pack(side='left', expand=True, fill=tk.BOTH)

        # subtract from
        label1 = tk.Label(frame_list1, text="Subtract From:")
        label1.pack()

        scrollbar1 = tk.Scrollbar(frame_list1)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

        listbox1 = tk.Listbox(frame_list1, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar1.set, exportselection=False)
        listbox1.pack(expand=True, fill=tk.BOTH)

        # Configure the scroll bar
        scrollbar1.config(command=listbox1.yview)

        frame_list2 = tk.Frame(frame_lists)
        frame_list2.pack(side='left', expand=True, fill=tk.BOTH)
        # subtract with
        label2 = tk.Label(frame_list2, text="Subtract With:")
        label2.pack()

        scrollbar2 = tk.Scrollbar(frame_list2)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

        listbox2 = tk.Listbox(frame_list2, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar2.set, exportselection=False)
        listbox2.pack(expand=True, fill=tk.BOTH)

        # Configure the scroll bar
        scrollbar2.config(command=listbox2.yview)

        frame_buttons = tk.Frame(top)
        frame_buttons.pack(side='bottom', expand=True, fill=tk.X)
        button1 = tk.Button(frame_buttons, text='Cancel', width=15, height=1, command=top.destroy)
        button1.pack(side='right', anchor='sw', padx=10, pady=10)
        button2 = tk.Button(frame_buttons, text='Confirm', width=15, height=1, \
            command=lambda: self._get_subtraction_result(top, result_curve, gui, listbox1, listbox2))
        button2.pack(side='right', anchor='se', expand=True, padx=10, pady=10)
       
        for i in gui.container.get_curves_list():
            temp_str = f"{pathlib.Path(i[0]).name}/{i[1]}/{i[2]}"
            listbox1.insert(tk.END, temp_str)
            listbox2.insert(tk.END, temp_str)
       
       
        gui.root.wait_window(top)
        

        return result_curve
    
    def opt_addition(self, selected_curves: list):
        cords_y = numpy.sum([i.abs_cords_y for i in selected_curves], axis=0)
        cords_x = selected_curves[0].abs_cords_x
        result_curve: load.single_line = load.single_line(
            file=operations.FILE,
            curve=str(operations.CURVE),
            type=operations.TYPE,
            cords=numpy.array([cords_x, cords_y]),
            file_path=operations.FILE
        )
        return result_curve
    
    def opt_averaging(self, selected_curves: list):
        selected_curves_sz = len(selected_curves)
        cords_y = numpy.mean([i.abs_cords_y for i in selected_curves], axis=0)# / selected_curves_sz
        cords_x = selected_curves[0].abs_cords_x
        result_curve: load.single_line = load.single_line(
            file=operations.FILE,
            curve=str(operations.CURVE),
            type=operations.TYPE,
            cords=numpy.array([cords_x, cords_y]),
            file_path=operations.FILE
        )
        return result_curve
    
    
    
    def selection(self, gui: "main.GUI"):
        container = gui.container.container
        widget = gui.pref.tree
        # if len(widget.selection()) == 2:
        #     A = widget.selection()[0].split("@")
        #     B = widget.selection()[1].split("@")
        #     # print(len(widget.selection()))
        #     target_A = container[A[1]][A[0]][A[2]]
        #     target_B = container[B[1]][B[0]][B[2]]
        #     return target_A, target_B
        if len(widget.selection()) >= 2:
            selected_curves = []
            for i in widget.selection():
                temp = i.split("@")
                # print('testing::')
                # print(temp)
                selected_curves.append(container[temp[1]][temp[0]][temp[2]])
            return selected_curves

        return None#, None
        
    def menu_perform(self, gui: "main.GUI", action: str):
        selected_curves = self.selection(gui)
        
        # if target_A is not None and target_B is not None:
        #     if action == "+":
        #         obj = self.opt_addition(target_A, target_B)
        #     elif action == "-":
        #         obj = self.opt_subtract(target_A, target_B)
        #     elif action == "AVG":
        #         obj = self.opt_averaging(target_A, target_B)
        #     gui.container.load_and_plot_obj(target=obj)
        #     operations.CURVE += 1
        if selected_curves is not None or action == "-":
            if action == "+":
                obj = self.opt_addition(selected_curves)
            elif action == "-":
                obj = self.opt_subtraction(gui) #, selected_curves
            elif action == "AVG":
                obj = self.opt_averaging(selected_curves)
            gui.container.load_and_plot_obj(target=obj)
            operations.CURVE += 1
        return None
    
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