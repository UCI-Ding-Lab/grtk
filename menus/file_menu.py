import tkinter
from tkinter import filedialog as fd
import tkinter.messagebox
import timeit
from bin.data_plot_new import line_container

def do_nothing():
    pass

class FileMenu():
    def __init__(self, GUI, container: line_container):
        self.GUI = GUI
        self.line_container = container
        self.recent_menu = None
        self.recent_files = []
        self._init_file_menu()

    def _init_file_menu(self):
        fm = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        fm.add_command(label="Test OpenGL", command=do_nothing)
        fm.add_command(label="Load Gr File", command=self._load_gr_file)
        #fm.add_command(label="Recent Gr File", command=do_nothing)
        self.recent_menu = tkinter.Menu(fm, tearoff=0)
        self._recent_gr_file(self.recent_menu)
        fm.add_cascade(label="Recent Gr File", menu=self.recent_menu)

        fm.add_separator()
        fm.add_command(label="Load Plug'in", command=do_nothing)
        fm.add_command(label="Unload Plug'in", command=do_nothing)
        fm.add_separator()
        fm.add_command(label="Quit All Windows", command=self.GUI.root.quit)
        self.GUI.menu_bar.add_cascade(label="File", menu=fm)

    def _load_gr_file(self, file_path=None):
        try:
            filetypes = (
                ('gr files', '*.gr'),
                ('text files', '*.txt'),
                ('All files', '*.*')
            )
            if file_path == None:
                file_path = fd.askopenfilename(
                    title='Open a file',
                    initialdir='/',
                    filetypes=filetypes)
            
            try:
                data_file = open(r"data/recent_paths.txt", "r")
                self.recent_files = []
                while True:
                    line = data_file.readline()
                    if not line:
                        data_file.close()
                        break
                    self.recent_files.append(line)
            except:
                pass

            if file_path not in self.recent_files :
                append_line = file_path + "\n"
                data_file = open(r"data/recent_paths.txt", "a")
                data_file.write(append_line)
                data_file.close()
                self.recent_files.append(file_path)
                self._recent_gr_file(self.recent_files, file_path)



            start = timeit.default_timer()
            self.line_container.load_and_plot(path=file_path)
            stop = timeit.default_timer()
            if self.GUI.debug_mode:
                self.GUI.log._log(f'graph loaded, runtime = {stop-start} s')
        except Exception as e:
            if self.GUI.debug_mode:
                self.GUI.log._log("ERROR: "+repr(e))
            raise e


    def _recent_gr_file(self, menu, file_path=None):
        if file_path != None:
            self.recent_menu.add_command(label=file_path, command=lambda: self._load_gr_file(file_path))
        else:
            try:
                data_file = open(r"data/recent_paths.txt", "r")
                for i in data_file.readlines():
                    menu.add_command(label=i, command=lambda: self._load_gr_file(i.strip()))
                data_file.close()
            except:
                pass
        # menu.add_command(label="test 1", command=do_nothing)