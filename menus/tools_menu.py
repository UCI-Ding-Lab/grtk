import tkinter
import tkinter.messagebox

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main

def do_nothing():
    pass

class ToolsMenu():
    def __init__(self, GUI):
        self.GUI: "main.GUI" = GUI
        self.mode_var = tkinter.StringVar()
        self.mode_var.set("normal")
        self._init_tools_menu()

    def _init_tools_menu(self):
        tm = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        mode = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        tm.add_command(label="Expand Tree", command=self.expand_tree)
        tm.add_command(label="Fold Tree", command=self.fold_tree)
        tm.add_separator()
        mode.add_radiobutton(label="Normal Mode", command=self.change_mode, variable=self.mode_var, value="normal")
        mode.add_radiobutton(label="Select Mode", command=self.change_mode, variable=self.mode_var, value="select")
        tm.add_cascade(label="Mode", menu=mode)
        self.GUI.menu_bar.add_cascade(label="Tools", menu=tm)
    
    def expand_tree(self):
        for type in self.GUI.pref.tree.get_children():
            self.GUI.pref.tree.item(type, open=True)
            for file in self.GUI.pref.tree.get_children(type):
                self.GUI.pref.tree.item(file, open=True)
    
    def fold_tree(self):
        for type in self.GUI.pref.tree.get_children():
            self.GUI.pref.tree.item(type, open=False)
            for file in self.GUI.pref.tree.get_children(type):
                self.GUI.pref.tree.item(file, open=False)
    
    def change_mode(self):
        if self.mode_var.get() == "select":
            self.GUI.pref.tree.selection_remove(self.GUI.pref.tree.selection())
            self.GUI.pref.tree.tag_configure("selected", background="yellow")
            self.GUI.pref.tree.configure(selectmode="extended")
            self.GUI.pref.global_hide()
            self.GUI.pref.selection_mode = True
        elif self.mode_var.get() == "normal":
            self.GUI.pref.tree.selection_remove(self.GUI.pref.tree.selection())
            self.GUI.pref.tree.tag_configure("selected", background="lightgrey")
            self.GUI.pref.tree.configure(selectmode="browse")
            self.GUI.pref.global_show()
            self.GUI.pref.selection_mode = False
            