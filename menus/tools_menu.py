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
        self._init_tools_menu()

    def _init_tools_menu(self):
        tm = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        tm.add_command(label="Expand Tree", command=self.expand_tree)
        tm.add_command(label="Fold Tree", command=self.fold_tree)
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