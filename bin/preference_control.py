import tkinter
from tkinter import ttk
from tkinter import colorchooser


# typecheck
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main
    from helper import load
    from matplotlib import lines
    from matplotlib import axes

class perf_ctl(object):
    def __init__(self, GUI: "main.GUI"):
        """a popup window to edit preference for each line
        will be called by edit menu

        Args:
            GUI (main.GUI): GUI object
        """
        # from GUI object
        self.GUI: "main.GUI" = GUI
        self.container: dict[str,load.single_line] = GUI.container.container
        self.axes: axes = self.GUI.container.matplot_subplot
        
        # private variables
        self.pack_stat: bool = False
        
        # True if any changes made
        # use to determine if save is needed
        self.changes: dict[str,bool] = {
            "show": False,
            "color": False,
        }
        
        # changes variables
        self.show_var = tkinter.IntVar()
        self.color_var = tkinter.StringVar()
        
        # pop up window initialization
        self.pop_up = tkinter.Toplevel(self.GUI.root)
        self.pop_up.geometry("250x250")
        self.pop_up.title("Edit Preference")
        
        # get a list of all the file paths
        possible_files = list(self.container.keys())
        
        # build combobox line selector
        self.select_box = ttk.Combobox(self.pop_up, values=possible_files, state="readonly")
        self.select_box.bind("<<ComboboxSelected>>", self.build_pref_options)
        self.select_box.pack()
        
        # build preference options
        self.pref_frame = tkinter.LabelFrame(self.pop_up, text="Set preference for selected file")
        self.pref_show_line = tkinter.Checkbutton(self.pref_frame, text="Show on graph", variable=self.show_var, command=self.change_show)
        self.pref_color_preview = tkinter.Label(self.pref_frame, text="__")
        self.pref_color = tkinter.Button(self.pref_frame, text="Change Color", command=lambda: self.change_color())
        
        # build save and quit button
        tkinter.Button(self.pop_up, text="Save & Quit", command=self.quit_pop_up).pack(side=tkinter.BOTTOM, anchor="e")
    
    def build_pref_options(self, event):
        """this is a callback function for the combobox
        after a selection is made, this function will be called
        if there is any previous options widgets packed, it will be cleared
        pack new options widgets according to the selection file path

        Args:
            event (event): a must have argument for tkinter callback function
        """
        # clear previous options
        if self.pack_stat:
            self.pref_color.pack_forget()
            self.pref_show_line.pack_forget()
            self.pref_frame.pack_forget()
            self.update_dict = dict()
        
        # check current status
        self.target_path = self.select_box.get()
        self.target_line2d = self.container[self.target_path].line2d_object[0]
        self.show_var.set(1) if self.target_line2d.get_visible() else self.show_var.set(0)
        self.pref_color_preview.configure(bg=self.target_line2d.get_color(), fg=self.target_line2d.get_color())
        
        # build new options
        self.pref_frame.pack(expand=True, fill="y")
        self.pref_show_line.grid(row=0, column=0, columnspan=2)
        self.pref_color_preview.grid(row=1, column=0)
        self.pref_color.grid(row=1, column=1)
        self.pack_stat = True
    
    def change_show(self):
        """record change in show variable
        """
        self.changes["show"] = True
    
    def change_color(self):
        """record change in color variable
        ask for color and update preview
        """
        self.changes["color"] = True
        self.color_var = colorchooser.askcolor()[1]
        self.pref_color_preview.configure(bg=self.color_var, fg=self.color_var)
    
    def quit_pop_up(self):
        """destory pop up window
        then save changes by calling container.change_line_preference
        """
        # destroy pop up window
        self.pop_up.destroy()
        self.pop_up.update()
        
        # save changes to container
        if self.changes["color"]:
            self.GUI.container.change_line_preference(self.target_path, {"color": self.color_var})
        
        if self.changes["show"]:
            self.GUI.container.change_line_preference(self.target_path, {"visible": self.show_var.get()})