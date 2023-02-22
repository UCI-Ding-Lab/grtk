import tkinter
from tkinter import filedialog as fd
import tkinter.messagebox
import timeit
from logger import logger
from data_plot_new import line_container

def do_nothing():
    pass

class FileMenu():
    def __init__(self, GUI, container: line_container):
        self.GUI = GUI
        self.line_container = container

        self._init_file_menu()

    def _init_file_menu(self):
        fm = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        fm.add_command(label="Test OpenGL", command=do_nothing)
        fm.add_command(label="Load Gr File", command=self._load_gr_file)
        fm.add_command(label="Recent Gr File", command=do_nothing)
        fm.add_separator()
        fm.add_command(label="Load Plug'in", command=do_nothing)
        fm.add_command(label="Unload Plug'in", command=do_nothing)
        fm.add_separator()
        fm.add_command(label="Quit All Windows", command=self.GUI.root.quit)
        self.GUI.menu_bar.add_cascade(label="File", menu=fm)

    def _load_gr_file(self):
        try:
            filetypes = (
                ('gr files', '*.gr'),
                ('text files', '*.txt'),
                ('All files', '*.*')
            )

            file_path = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)

            start = timeit.default_timer()
            self.line_container.load_and_plot(path=file_path)
            stop = timeit.default_timer()
            if self.GUI.debug_mode:
                self.GUI.log._log(f'graph loaded, runtime = {stop-start} s')
        except Exception as e:
            if self.GUI.debug_mode:
                self.GUI.log._log("ERROR: "+repr(e))
            raise e
