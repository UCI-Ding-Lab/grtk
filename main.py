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
        self._init_frames()
        self.container = data_plot_new.line_container(gui=self)
        self.layer_ctl = layer_control.layers(self.rightframe, self.container)
        self._window()
        self._menu_bar_main()
        root.config(menu=self.menu_bar)
        root.mainloop()
        self.log._close()
    
    def _init_frames(self):
        """left and right frame initialization
        left frame contains the graph itself
        right frame contains the layer control and preference control
        """
        self.leftframe = tkinter.Frame(self.root)
        self.leftframe.pack(fill=tkinter.BOTH, expand=1, side="left")
        tkinter.ttk.Separator(self.root, orient=tkinter.VERTICAL).pack(fill="y", side="left")
        self.rightframe = tkinter.Frame(self.root)
        self.rightframe.pack(fill="y", expand=1, side="left")
        tkinter.Label(self.rightframe, text="Layers", bg='yellow').pack(side="top")

        self.line_frame = tkinter.Frame(self.leftframe)

    def _window(self):
        """set title and window size
        """
        self.root.title('Data Visualization Software')
        self.root.geometry("1150x700")
    
    def _menu_bar_main(self):
        """initializations of each tool bar selection
        """
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
        self.file_menu = file_menu.FileMenu(self, container=self.container)
        
    def _init_menu_bar_edit(self):
        self.edit_menu = edit_menu.EditMenu(self, container=self.container)

    def _init_menu_bar_options(self):
        self.option_menu = options_menu.OptionsMenu(self)

    def _init_menu_bar_tools(self):
        self.tools_menu = tools_menu.ToolsMenu(self)

    def _init_menu_bar_treatment(self):
        self.treatment_menu = treatment_menu.TreatmentMenu(self)

    def _init_menu_bar_test(self):
       self.test_menu = test_menu.TestMenu(self)

    def _init_keyboard_events(self):
        self.keyboard_events =  keyboard_events.KeyboardEvents(self)
        
def GUI_manager():
    root = tkinter.Tk()
    app = GUI(root)

if __name__ == '__main__':
    GUI_manager()
