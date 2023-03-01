# lib
import tkinter
import tkinter.ttk
import tkinter.messagebox

# files
from helper.logger import logger
from menus import file_menu
from menus import edit_menu
from menus import options_menu
from menus import tools_menu
from menus import treatment_menu
from menus import test_menu
from bin import data_plot_new
from bin import keyboard_events
from bin import layer_control

def do_nothing():
    pass

class GUI:
    def __init__(self, root: tkinter.Tk):
        self.menu_obj: dict[str, object] = {}
        self.log = logger()
        self.debug_mode = False
        self.root = root
        self.menu_bar = tkinter.Menu(root)
        
        self.init_frames()
        self.container = data_plot_new.line_container(
            frame=self.line_frame,
            menu_obj=self.menu_obj
        )
        self.init_layer_ctl(self.rightframe, self.container)
        
        self._window()
        self._menu_bar_main()

        root.config(menu=self.menu_bar)
        root.mainloop()
        self.log._close()
    
    def init_frames(self):
        self.leftframe = tkinter.Frame(self.root)
        self.leftframe.pack(fill=tkinter.BOTH, expand=1, side="left")
        tkinter.ttk.Separator(self.root, orient=tkinter.VERTICAL).pack(fill="y", side="left")
        self.rightframe = tkinter.Frame(self.root)
        self.rightframe.pack(fill="y", expand=1, side="left")
        tkinter.Label(self.rightframe, text="Layers", bg='yellow').pack(side="top")

        self.line_frame = tkinter.Frame(self.leftframe)
    
    def init_layer_ctl(self, frame: tkinter.Frame, container: data_plot_new.line_container):
        layer_ctl = layer_control.layers(frame, container)
        self.menu_obj["layer"] = layer_ctl
        
    def _window(self):
        self.root.title('Data Visualization Software')
        self.root.geometry("1050x700")
    
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
