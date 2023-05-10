import tkinter
import tkinter.messagebox
from tkinter import ttk
from bin.set import setting


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main
    from bin import operation

def do_nothing():
    pass

class OptionsMenu():
    def __init__(self, GUI):
        self.GUI: "main.GUI" = GUI
        self.operation: operation.operations = self.GUI.operation
        self.setting: setting = self.GUI.setting
        self._init_options_menu()

    def _init_options_menu(self):
        om = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        om.add_command(label="Setting", command=lambda: self.setting.change_setting(self.GUI))
        om.add_separator()
        om.add_command(label="+", command=lambda: self.operation.perform(self.GUI, "+"))
        om.add_command(label="-", command=lambda: self.operation.perform(self.GUI, "-"))
        self.GUI.menu_bar.add_cascade(label="Options", menu=om)