# lib
import tkinter
import tkinter.ttk
import tkinter.messagebox
import ctypes
import sys

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
from bin import preference_control
from bin import set
from bin import operation
from bin import selector
from bin import states
from plugins import *
from pathlib import Path
import custom
def do_nothing():
    pass

class GUI:
    def __init__(self, root: tkinter.Tk):
        # ATTR
        self.root = root
        
        # Load setting
        self.setting = set.setting()
        
        # init menu
        self.menu_obj: dict[str, object] = {}
        self.file_menu = None
        self.edit_menu = None
        self.option_menu = None
        self.tools_menu = None
        self.treatment_menu = None
        self.test_menu = None
        self.keyboard_events = None
        self.saved = True # indicates whether the current graph is saved.
        # self.saved = True #
        
        # build
        self._init_frames()
        self._window()
        
        # load all modules
        # Warning: the order of the following lines matters
        self.log = logger(self)
        self.menu_bar = tkinter.Menu(root)
        self.operation = operation.operations()
        self.container = data_plot_new.line_container(gui=self)
        self.pref = preference_control.perf_ctl(self)
        self.lasso = selector.lasso(self)
        self.usr_cus = custom.labCustom()

        # style
        self._stylesheet()
        
        # plugin router
        self.on_draw = states.on_draw(self)
        self.on_change_color = states.on_change_color(self)
        self.all_plugins = []
        for i in sys.modules.keys():
            if i.startswith("plugins."):
                for name, obj in sys.modules[i].__dict__.items():
                    if name.startswith("p_"):
                        self.all_plugins.append(obj(self))
        
        # database
        self.txt_path = None # text datafile path if .txt file is loaded.
        #self.save_state = False # indicates whether the current graph is saved.
        
        # menu bar
        self._menu_bar_main()
        root.config(menu=self.menu_bar)
        
        # update timer
        self.root.after(10, self.container._refresh_canvas)
        
        # save quit process
        root.protocol("WM_DELETE_WINDOW", self._quit_process)
        root.mainloop()
        self.log.close()
    
    def _init_frames(self):
        """left and right frame initialization
        left frame contains the graph itself
        right frame contains the layer control and preference control
        """
        self.graph_frame = tkinter.Frame(self.root)
        self.graph_frame.pack(fill=tkinter.BOTH, expand=1, side=tkinter.LEFT)
        self.line_frame = tkinter.Frame(self.graph_frame)
        

        
        self.right_frame = tkinter.Frame(self.root, bg="white")
        self.right_frame.pack(fill=tkinter.BOTH, expand=1, side=tkinter.RIGHT)
        
        self.curve_pref_frame = tkinter.Frame(self.right_frame, bg="white")
        self.curve_pref_frame.pack(fill=tkinter.BOTH, expand=1, side=tkinter.TOP)
        self.curve_pref_down = tkinter.Frame(self.right_frame, bg="white")
        self.curve_pref_down.pack(fill=tkinter.BOTH, expand=1, side=tkinter.TOP)
        self.tip_frame = tkinter.Frame(self.right_frame, bg="white")
        self.tip_frame.pack(fill=tkinter.BOTH, expand=0, side=tkinter.TOP)
        self.global_pref_frame = tkinter.Frame(self.right_frame, bg="white")
        self.global_pref_frame.pack(fill=tkinter.X, side=tkinter.BOTTOM)
        
    def _window(self):
        """set title and window size
        """
        if sys.platform == 'win32':
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
            self.root.tk.call('tk', 'scaling', ScaleFactor/75)
            self.root.title(self.setting.NAME)
            width = self.setting.WIN_GUI_WIDTH * ScaleFactor/self.setting.WIN_SCALE_DIVIDER
            height = self.setting.WIN_GUI_HEIGHT * ScaleFactor/self.setting.WIN_SCALE_DIVIDER
            self.root.geometry(str(int(width)) + 'x' + str(int(height)))
        else:
            self.root.tk.call('tk', 'scaling', 1.2)
            self.root.title(self.setting.NAME)
            self.root.geometry(str(self.setting.UNX_GUI_WIDTH) + 'x' + str(self.setting.UNX_GUI_HEIGHT))
    
    def _stylesheet(self):
        """set style
        """
        style = tkinter.ttk.Style(self.root)
        style.theme_use(self.setting.THEME_USE)
        style.configure(
            "red.Horizontal.TProgressbar",
            foreground=self.setting.PROGRESS_BAR_COLOR_FG,
            background=self.setting.PROGRESS_BAR_COLOR_BG
        )
        if sys.platform == 'win32':
            style.configure('Treeview', rowheight=self.setting.TREEVIEW_ROW_HEIGHT)
    
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
        
    def _quit_process(self):
        choice = None
        question = None
        if self.saved == True:
            self.root.destroy()
            return None
        if self.txt_path == None:
            question = "Want to save your changes?"
            choice = tkinter.messagebox.askyesnocancel("Quit", question)
            if choice == True:
                self.file_menu.save_as()
                self.root.destroy()
            elif choice == False:
                self.root.destroy()
            else:
                pass
        else:
            file_name = Path(self.txt_path).name
            question = f"Want to save your changes to '{file_name}'?"
            choice = tkinter.messagebox.askyesnocancel("Quit", question)
            if choice == True:
                self.file_menu.save()
                self.root.destroy()
            elif choice == False:
                self.root.destroy()
            else:
                pass
        return None
        
def GUI_manager():
    root = tkinter.Tk()
    app = GUI(root)
    return root, app

if __name__ == '__main__':
    root, app = GUI_manager()

