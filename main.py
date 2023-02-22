import tkinter
import tkinter.messagebox
from logger import logger
import sys

import file_menu
import edit_menu
import options_menu
import tools_menu
import treatment_menu
import test_menu
import data_plot_new
import keyboard_events

def do_nothing():
    pass

class GUI:
    def __init__(self, root: tkinter.Tk):
        self.menu_obj: dict[str, object] = {}
        self.log = logger()
        self.debug_mode = False
        self.root = root
        self.menu_bar = tkinter.Menu(root)
        self.frame = tkinter.Frame(self.root)
        self.option_frame = tkinter.Frame()
        self.container = data_plot_new.line_container(frame=self.frame, root=self.root, menu_obj=self.menu_obj)
        self._window()
        self._menu_bar_main()

        root.config(menu=self.menu_bar)
        root.mainloop()
        self.log._close()

    def _window(self):
        self.root.title('Data Visualization Software')
        self.root.geometry("800x600")
    
    def _menu_bar_main(self):
        self._init_menu_bar_file()
        self._init_menu_bar_edit()
        self._init_menu_bar_options()
        self._init_menu_bar_tools()
        self._init_menu_bar_treatment()
        
        # for testing purpose
        self._init_menu_bar_test()

        #keyboard events
        self._init_keyboard_events()
        
    def _init_menu_bar_file(self):
        fm = file_menu.FileMenu(self, container=self.container)
        self.menu_obj["file"] = fm
        
    def _init_menu_bar_edit(self):
        em = edit_menu.EditMenu(self, container=self.container)
        self.menu_obj["edit"] = em

    def _init_menu_bar_options(self):
        om = options_menu.OptionsMenu(self)
        self.menu_obj["open"] = om

    def _init_menu_bar_tools(self):
        tm = tools_menu.ToolsMenu(self)
        self.menu_obj["tools"] = tm

    def _init_menu_bar_treatment(self):
        tm = treatment_menu.TreatmentMenu(self)
        self.menu_obj["treatment"] = tm

    def _init_menu_bar_test(self):
       tm = test_menu.TestMenu(self)
       self.menu_obj["test"] = tm

    def _init_keyboard_events(self):
        ke =  keyboard_events.KeyboardEvents(self)
        
def GUI_manager():
    root = tkinter.Tk()
    app = GUI(root)

if __name__ == '__main__':
    GUI_manager()
