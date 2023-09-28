import numpy as np
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

    def _refresh_listbox(self, gui, listbox):
        listbox.delete(0, tk.END)
        for i in gui.container.get_curves_list():
            temp_str = f"{pathlib.Path(i[0]).name}/{i[1]}/{i[2]}"
            listbox.insert(tk.END, temp_str)
        return None
    
    def _pop_operation_result_window(self, window, message):
        messagebox.showinfo(title="Operation Successful!", message=message, parent=window)
        return None
    
    def _get_result_curve(self, file, curve, type, cords_x, cords_y, file_path):
        result_curve: load.single_line = load.single_line(
            file=file,
            curve=curve,
            type=type,
            cords=np.array([cords_x, cords_y]),
            file_path=file_path
        )
        return result_curve
    
    def _perform_subtraction(self, window, gui, listbox1, listbox2):
        # listbox1 is minuend.
        # listbox2 is subtrahend.
        

        minuend_curves = [listbox1.get(idx) for idx in listbox1.curselection()]
        subtrahend_curves = [listbox2.get(idx) for idx in listbox2.curselection()]
        
        subtrahend_message = ""
        message = "Below operations are performed:\n\n"
        
        if minuend_curves == [] or subtrahend_curves == []:
            return None
        
        subtrahend_sum = None
        for i in subtrahend_curves:
            file_name, type_name, nick_name = i.split('/')
            if subtrahend_sum is None:
                subtrahend_sum = np.array(gui.container.\
                    container[file_name][type_name][nick_name].abs_cords_y)
            else:
                subtrahend_sum = subtrahend_sum + np.array(gui.container.\
                    container[file_name][type_name][nick_name].abs_cords_y)
            subtrahend_message = subtrahend_message + f" - {file_name}/{type_name}/{nick_name}"
            
        for i in minuend_curves:
            file_name, type_name, nick_name = i.split('/')
            cords_y = np.array(gui.container.\
                container[file_name][type_name][nick_name].abs_cords_y)
            cords_x = np.array(gui.container.\
                container[file_name][type_name][nick_name].abs_cords_x)
            cords_y = cords_y - subtrahend_sum
            # result_curve: load.single_line = load.single_line(
            #     file=operations.FILE,
            #     curve=str(operations.CURVE),
            #     type=operations.TYPE,
            #     cords=np.array([cords_x, cords_y]),
            #     file_path=operations.FILE
            # )
            result_curve = self._get_result_curve(operations.FILE, \
                str(operations.CURVE), operations.TYPE, cords_x, cords_y, operations.FILE)
            gui.container.load_and_plot_obj(target=result_curve)
            operations.CURVE += 1
            message = message + f"{file_name}/{type_name}/{nick_name}" + subtrahend_message + \
                f" = {operations.FILE}/{operations.TYPE}/{str(operations.CURVE)}\n\n"

        self._refresh_listbox(gui, listbox1)
        self._refresh_listbox(gui, listbox2)
        self._pop_operation_result_window(window, message)
        # window.destroy()
        return None

        
    
    def opt_subtraction(self, gui):

        
        top = tk.Toplevel(gui.root)
        top.geometry("500x300")
        top.title("Subtraction")

        frame_lists = tk.Frame(top)
        frame_lists.pack(side='top', expand=True, fill=tk.X)


        # subtract from
        frame_list1 = tk.Frame(frame_lists)
        frame_list1.pack(side='left', expand=True, fill=tk.BOTH)

        
        label1 = tk.Label(frame_list1, text="Subtract From:\n(Select from this list to average)")
        label1.pack()

        scrollbar1 = tk.Scrollbar(frame_list1)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

        listbox1 = tk.Listbox(frame_list1, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar1.set, exportselection=False)
        listbox1.pack(expand=True, fill=tk.BOTH)

        # Configure the scroll bar
        scrollbar1.config(command=listbox1.yview)

        # subtract with
        frame_list2 = tk.Frame(frame_lists)
        frame_list2.pack(side='left', expand=True, fill=tk.BOTH)
        
        label2 = tk.Label(frame_list2, text="Subtract With:\n")
        label2.pack()

        scrollbar2 = tk.Scrollbar(frame_list2)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

        listbox2 = tk.Listbox(frame_list2, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar2.set, exportselection=False)
        listbox2.pack(expand=True, fill=tk.BOTH)

        # Configure the scroll bar
        scrollbar2.config(command=listbox2.yview)

        frame_buttons = tk.Frame(top)
        frame_buttons.pack(side='bottom', expand=True, fill=tk.X)
        button1 = tk.Button(frame_buttons, text='Close', width=15, height=1, command=top.destroy)
        button1.pack(side='right', anchor='sw', padx=10, pady=10)
        button2 = tk.Button(frame_buttons, text='Subtract', width=15, height=1, \
            command=lambda: self._perform_subtraction(top, gui, listbox1, listbox2))
        button2.pack(side='right', anchor='se', expand=True, padx=10, pady=10)
       
        button3 = tk.Button(frame_buttons, text='Average', width=15, height=1, \
            command=lambda: self._perform_averaging(top, gui, listbox1, listbox2))
        button3.pack(side='left', anchor='e', padx=10, pady=10)
       
        for i in gui.container.get_curves_list():
            temp_str = f"{pathlib.Path(i[0]).name}/{i[1]}/{i[2]}"
            listbox1.insert(tk.END, temp_str)
            listbox2.insert(tk.END, temp_str)
       
       
        gui.root.wait_window(top)
        

        return None
    
    def _perform_addition(self, window, gui, listbox1):
        selected_curves = [listbox1.get(idx) for idx in listbox1.curselection()]
        cords_y = None
        cords_x = None
        
        message = "Below operations are performed:\n\n"
        
        if selected_curves == []:
            return None
        
        for i in selected_curves:
            file_name, type_name, nick_name = i.split('/')
            if cords_y is None:
                cords_y = np.array(gui.container.\
                    container[file_name][type_name][nick_name].abs_cords_y)
                cords_x = np.array(gui.container.\
                    container[file_name][type_name][nick_name].abs_cords_x)
            else:
                cords_y = cords_y + np.array(gui.container.\
                    container[file_name][type_name][nick_name].abs_cords_y)
                
            if message == "Below operations are performed:\n\n":
                message = message + f"{file_name}/{type_name}/{nick_name}"
            else:
                message = message + f" + {file_name}/{type_name}/{nick_name}"
            
        result_curve = self._get_result_curve(operations.FILE, \
            str(operations.CURVE), operations.TYPE, cords_x, cords_y, operations.FILE)
        gui.container.load_and_plot_obj(target=result_curve)
        operations.CURVE += 1
        
        message = message + f" = {operations.FILE}/{operations.TYPE}/{str(operations.CURVE)}"
        
        # window.destroy()
        self._refresh_listbox(gui, listbox1)
        self._pop_operation_result_window(window, message)
        
        return None
    
    def opt_addition(self, gui):
        top = tk.Toplevel(gui.root)
        top.geometry("500x250")
        top.title("Addition")

        frame_lists = tk.Frame(top)
        frame_lists.pack(side='top', expand=True, fill=tk.X)

        frame_list1 = tk.Frame(frame_lists)
        frame_list1.pack(side='left', expand=True, fill=tk.BOTH)

        # subtract from
        label1 = tk.Label(frame_list1, text="Select curves to add:")
        label1.pack()

        scrollbar1 = tk.Scrollbar(frame_list1)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

        listbox1 = tk.Listbox(frame_list1, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar1.set, exportselection=False)
        listbox1.pack(expand=True, fill=tk.BOTH) #

        # Configure the scroll bar
        scrollbar1.config(command=listbox1.yview)



        frame_buttons = tk.Frame(top)
        frame_buttons.pack(side='bottom', expand=True, fill=tk.X)
        button1 = tk.Button(frame_buttons, text='Close', width=15, height=1, command=top.destroy)
        button1.pack(side='right', anchor='sw', padx=10, pady=10)
        button2 = tk.Button(frame_buttons, text='Confirm', width=15, height=1, \
            command=lambda: self._perform_addition(top, gui, listbox1))
        button2.pack(side='right', anchor='se', expand=True, padx=10, pady=10)
       
        for i in gui.container.get_curves_list():
            temp_str = f"{pathlib.Path(i[0]).name}/{i[1]}/{i[2]}"
            listbox1.insert(tk.END, temp_str)
            # listbox2.insert(tk.END, temp_str)
       
       
        gui.root.wait_window(top)
        return None
    
    
    def _perform_averaging(self, window, gui, listbox1, listbox2=None):
        selected_curves = [listbox1.get(idx) for idx in listbox1.curselection()]
        cords_y = None
        cords_x = None
        
        message = "Below operations are performed:\n\n"
        
        if selected_curves == []:
            return None
        
        for i in selected_curves:
            file_name, type_name, nick_name = i.split('/')
            if cords_y is None:
                cords_y = np.array(gui.container.\
                    container[file_name][type_name][nick_name].abs_cords_y)
                cords_x = np.array(gui.container.\
                    container[file_name][type_name][nick_name].abs_cords_x)
            else:
                cords_y = cords_y + np.array(gui.container.\
                    container[file_name][type_name][nick_name].abs_cords_y)
            if message == "Below operations are performed:\n\n":
                message = message + f"({file_name}/{type_name}/{nick_name}"
            else:
                message = message + f" + {file_name}/{type_name}/{nick_name}"
                
        cords_y = cords_y / len(selected_curves)
        result_curve = self._get_result_curve(operations.FILE, \
            str(operations.CURVE), operations.TYPE, cords_x, cords_y, operations.FILE)
        gui.container.load_and_plot_obj(target=result_curve)
        operations.CURVE += 1
        
        message = message + f")/{len(selected_curves)} = {operations.FILE}/{operations.TYPE}/{str(operations.CURVE)}"
        
        self._refresh_listbox(gui, listbox1)
        if listbox2 is not None:
            self._refresh_listbox(gui, listbox2)
        # window.destroy()
        
        self._pop_operation_result_window(window, message)
        
        return None    

    def opt_averaging(self, gui):
        top = tk.Toplevel(gui.root)
        top.geometry("500x250")
        top.title("Averaging")

        frame_lists = tk.Frame(top)
        frame_lists.pack(side='top', expand=True, fill=tk.X)

        frame_list1 = tk.Frame(frame_lists)
        frame_list1.pack(side='left', expand=True, fill=tk.BOTH)

        # subtract from
        label1 = tk.Label(frame_list1, text="Select curves to get the average:")
        label1.pack()

        scrollbar1 = tk.Scrollbar(frame_list1)
        scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

        listbox1 = tk.Listbox(frame_list1, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar1.set, exportselection=False)
        listbox1.pack(expand=True, fill=tk.BOTH) #

        # Configure the scroll bar
        scrollbar1.config(command=listbox1.yview)



        frame_buttons = tk.Frame(top)
        frame_buttons.pack(side='bottom', expand=True, fill=tk.X)
        button1 = tk.Button(frame_buttons, text='Close', width=15, height=1, command=top.destroy)
        button1.pack(side='right', anchor='sw', padx=10, pady=10)
        button2 = tk.Button(frame_buttons, text='Confirm', width=15, height=1, \
            command=lambda: self._perform_averaging(top, gui, listbox1))
        button2.pack(side='right', anchor='se', expand=True, padx=10, pady=10)
       
        for i in gui.container.get_curves_list():
            temp_str = f"{pathlib.Path(i[0]).name}/{i[1]}/{i[2]}"
            listbox1.insert(tk.END, temp_str)
            # listbox2.insert(tk.END, temp_str)
       
       
        gui.root.wait_window(top)
        

        return None
    
    
    
    
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

        obj = None
        if action == "+":
            self.opt_addition(gui)
        elif action == "-":
            self.opt_subtraction(gui) #, selected_curves
        elif action == "AVG":
            self.opt_averaging(gui)

        return None
    
    def cus_perform(self, gui: "main.GUI", cus):
        A, B = self.selection(gui)
        func = getattr(custom.labCustom, cus)
        X, Y = func(gui.usr_cus, A, B)
        target_C: load.single_line = load.single_line(
            file=operations.FILE,
            curve=str(operations.CURVE),
            type=operations.TYPE,
            cords=np.array([X, Y]),
            file_path=operations.FILE
        )
        gui.container.load_and_plot_obj(target=target_C)
        operations.CURVE += 1