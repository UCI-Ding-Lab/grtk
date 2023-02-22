import tkinter
import tkinter.messagebox

def do_nothing():
    pass

class OptionsMenu():
    def __init__(self, GUI):
        self.GUI = GUI
        self._init_options_menu()

    def _init_options_menu(self):
        om = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        om.add_command(label="Whatever", command=do_nothing)
        om.add_command(label="Line Color", command=do_nothing)
        om.add_command(label="Marker Color", command=do_nothing)
        om.add_command(label="Line Width", command=do_nothing)
        om.add_command(label="Line Type", command=do_nothing)
        
        self.GUI.menu_bar.add_cascade(label="Options", menu=om)