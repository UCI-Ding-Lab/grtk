import tkinter
import tkinter.messagebox
from bin.set import setting

def do_nothing():
    pass

class OptionsMenu():
    def __init__(self, GUI):
        self.GUI = GUI
        self.setting: setting = self.GUI.setting
        self._init_options_menu()

    def _init_options_menu(self):
        om = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        om.add_command(label="Setting", command=lambda: self.setting.change_setting(self.GUI))
        self.GUI.menu_bar.add_cascade(label="Options", menu=om)