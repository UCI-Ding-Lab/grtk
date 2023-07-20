import tkinter
import tkinter.messagebox
from tkinter import ttk
from bin.set import setting
import custom


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
        om.add_command(label="Setting", command=lambda: [self.setting.change_setting(self.GUI), self._set_GUI_saved_false()])
        om.add_separator()
        om.add_command(label="Add", command=lambda: [self.operation.menu_perform(self.GUI, "+"), self._set_GUI_saved_false()])
        om.add_command(label="Subtract", command=lambda: [self.operation.menu_perform(self.GUI, "-"), self._set_GUI_saved_false()])
        om.add_command(label="AVG", command=lambda: [self.operation.menu_perform(self.GUI, "AVG"), self._set_GUI_saved_false()])
        om.add_separator()
        for key in custom.labCustom.__dict__:
            if key.startswith("opt_"):
                om.add_command(label=key[4:], command=lambda key=key: [self.operation.cus_perform(self.GUI, key), self._set_GUI_saved_false()])
        self.GUI.menu_bar.add_cascade(label="Options", menu=om)
        
    def _set_GUI_saved_false(self):
        self.GUI.root.title('Data Visualization Software (unsaved)')
        self.GUI.saved = False
        return None