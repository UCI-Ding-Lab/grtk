import tkinter
from tkinter import filedialog as fd
import tkinter.messagebox
import timeit
from bin.data_plot_new import line_container
import os
# from queue import Queue

def do_nothing():
    pass

class RecentFilesManager():
    def __init__(self, FileMenu):
        self.q = []
        self.max_size = 5
        self.FileMenu = FileMenu
        self.menu = None
        self.file_path = r"data/recent_paths.txt"
        self.file = None
        # self.read()
        # self.write()
        # self.read()

    def add(self, item):
        self.read()
        if item in self.q:
            self.q.remove(item)
        if len(self.q) >= self.max_size:
            self.q.pop()
        self.q.insert(0, item)
        temp = ""
        for i in self.q:
            temp = temp + i + "\n"
        self.file = open(self.file_path, "w")
        self.file.write(temp)
        self.file.close()
        self.menu.delete(0, "end")
        for i in self.q:
            self.menu.add_command(label=i, command=lambda: self.FileMenu._load_gr_file(i))

    def read(self):
        self.q = []
        if os.path.exists(self.file_path) == False:
            self.file = open(self.file_path, "w")
            self.file.close()
        self.file = open(self.file_path, "r")
        lines = self.file.readlines()
        for i in lines:
            self.q.append(i.strip())
        self.file.close()

    def add_recent_menu(self):
        if self.menu == None:
            self.menu = tkinter.Menu(self.FileMenu.fm, tearoff=0)
        self.read()
        for i in self.q:
            self.menu.add_command(label=i, command=lambda: self.FileMenu._load_gr_file(i))
        self.FileMenu.fm.add_cascade(label="Recent Gr File", menu=self.menu)

        # print(self.q)

    # def write(self):
    #     self.file = open(self.file_path, "w")
    #     self.file.write("hello world:\n")
    #     self.file.close()

class FileMenu():
    def __init__(self, GUI, container: line_container):
        self.GUI = GUI
        self.line_container = container

        self.fm = None
        self.RFM = RecentFilesManager(self)
        self._init_file_menu()
        

    def _init_file_menu(self):
        self.fm = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        self.fm.add_command(label="Test OpenGL", command=do_nothing)
        self.fm.add_command(label="Load Gr File", command=self._load_gr_file)
        
        self.RFM.add_recent_menu()

        self.fm.add_separator()
        self.fm.add_command(label="Load Plug'in", command=do_nothing)
        self.fm.add_command(label="Unload Plug'in", command=do_nothing)
        self.fm.add_separator()
        self.fm.add_command(label="Quit All Windows", command=self.GUI.root.quit)
        self.GUI.menu_bar.add_cascade(label="File", menu=self.fm)

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


            self.RFM.add(file_path)

            start = timeit.default_timer()
            self.line_container.load_and_plot(path=file_path)
            stop = timeit.default_timer()
            if self.GUI.debug_mode:
                self.GUI.log._log(f'graph loaded, runtime = {stop-start} s')
        except Exception as e:
            if self.GUI.debug_mode:
                self.GUI.log._log("ERROR: "+repr(e))
            raise e
