import tkinter
import tkinter.messagebox
from bin import preference_control

# typecheck
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main

def do_nothing():
    pass

class EditMenu():
    def __init__(self, GUI: "main.GUI", container):
        self.container = container
        self.GUI = GUI
        self.init_edit_menu()

    def init_edit_menu(self):
        self.main = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        self.main.add_command(label="Copy Image", command=do_nothing)
        self.main.add_separator()
        self.main.add_cascade(label="Delete", command=do_nothing)
        self.GUI.menu_bar.add_cascade(label="Edit", menu=self.main)