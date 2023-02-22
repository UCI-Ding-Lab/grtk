import tkinter
import tkinter.messagebox

def do_nothing():
    pass

class ToolsMenu():
    def __init__(self, GUI):
        self.GUI = GUI
        self._init_tools_menu()

    def _init_tools_menu(self):
        tm = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        tm.add_command(label="Whatever", command=do_nothing)
        self.GUI.menu_bar.add_cascade(label="Tools", menu=tm)