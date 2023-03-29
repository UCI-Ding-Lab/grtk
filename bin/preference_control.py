import tkinter
import pathlib
from tkinter import ttk
from tkinter import colorchooser


# typecheck
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main
    import data_plot_new

class perf_ctl(object):
    def __init__(self, GUI: "main.GUI"):
        self.GUI = GUI
        self.target_obj = None
        self.pack_stat = False
        
        self.changes = {
            "show": False,
            "color": False,
        }
        
        self.show_var = tkinter.IntVar()
        self.update_dict = dict()
        
        self.pop_up = tkinter.Toplevel(self.GUI.root)
        self.pop_up.geometry("750x250")
        self.pop_up.title("Edit Preference")
        
        possible_files = []
        for i in self.GUI.container.container:
            possible_files.append(pathlib.Path(i.file_path).name)
        for i in self.GUI.container.garbage:
            possible_files.append(pathlib.Path(i.file_path).name)
        
        self.select_box = ttk.Combobox(self.pop_up, values=possible_files, state="readonly")
        self.select_box.bind("<<ComboboxSelected>>", self.build_pref_options)
        self.select_box.pack()
        
        self.pref_frame = tkinter.LabelFrame(self.pop_up, text="Set preference for selected file")
        
        self.pref_show_line = tkinter.Checkbutton(self.pref_frame, text="Show on graph", variable=self.show_var, command=self.change_show)
        self.pref_color = tkinter.Button(self.pref_frame, text="Change Color", command=lambda: self.change_color())
        
        tkinter.Button(self.pop_up, text="Save & Quit", command=self.quit_pop_up).pack(side=tkinter.BOTTOM, anchor="e")
    
    def build_pref_options(self, event):
        if self.pack_stat:
            self.pref_color.pack_forget()
            self.pref_show_line.pack_forget()
            self.pref_frame.pack_forget()
            self.update_dict = dict()
        self.target_obj = None
        self.pref_frame.pack()
        target = self.select_box.get()
        for i in self.GUI.container.container:
            if pathlib.Path(i.file_path).name == target:
                self.target_obj = i
        if self.target_obj is None:
            for i in self.GUI.container.garbage:
                if pathlib.Path(i.file_path).name == target:
                    self.target_obj = i
        if self.target_obj is None:
            raise ValueError("No such file in container")
            
        self.show_var.set(self.target_obj.show.get())
        self.pref_show_line.update()
        self.pref_show_line.pack()
        self.pref_color.pack()
        self.pack_stat = True
    
    def change_show(self):
        self.changes["show"] = True
    
    def change_color(self):
        self.update_dict["color"] = colorchooser.askcolor()[1]
        self.changes["color"] = True
        
    
    def quit_pop_up(self):
        self.pop_up.destroy()
        self.pop_up.update()
        
        if self.changes["color"]:
            self.GUI.container.change_line_preference(self.target_obj.file_path, self.update_dict)
        
        if self.changes["show"]:
            if self.show_var.get() == 1:
                self.target_obj.show.set(1)
                self.GUI.container.load_and_plot(self.target_obj.file_path)
            else:
                self.target_obj.show.set(0)
                self.GUI.container.remove_line(self.target_obj.file_path)
        
    