import tkinter
from tkinter import filedialog as fd
# import tkinter.messagebox
from tkinter import messagebox
import timeit
from bin.data_plot_new import line_container
import os
import sqlite3
# from bin.db_manager import DBManager
# from queue import Queue

from bin.save_manager import SaveManager

# typecheck
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main


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


    def add(self, item):
        """
        Add item to recent list.
        """

        
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
            self.menu.add_command(label=i, command=lambda: self.FileMenu._load_file(i))
        return

    def delete(self, item):
        """
        Remove item from recent list.
        """
        self.read()
        if item in self.q:
            self.q.remove(item)
        temp = ""
        for i in self.q:
            temp = temp + i + "\n"
        self.file = open(self.file_path, "w")
        self.file.write(temp)
        self.file.close()
        self.menu.delete(0, "end")
        for i in self.q:
            self.menu.add_command(label=i, command=lambda: self.FileMenu._load_file(i))
        return
    
    def read(self):
        """
        Update self.q from file.
        """
        self.q = []
        if os.path.exists(self.file_path) == False:
            self.file = open(self.file_path, "w")
            self.file.close()
        self.file = open(self.file_path, "r")
        lines = self.file.readlines()
        for i in lines:
            self.q.append(i.strip())
        self.file.close()
        return

    def add_recent_menu(self):
        if self.menu == None:
            self.menu = tkinter.Menu(self.FileMenu.fm, tearoff=0)
        self.read()
        for i in self.q:
            self.menu.add_command(label=i, command=lambda: self.FileMenu._load_file(i))
        self.FileMenu.fm.add_cascade(label="Recent Gr File", menu=self.menu)
        return



class FileMenu():
    def __init__(self, GUI: "main.GUI", container: line_container):
        self.GUI = GUI
        self.line_container = container

        self.fm = None
        self.RFM = RecentFilesManager(self)
        self._init_file_menu()
        self._bind_shortcuts()

    def _init_file_menu(self):
        self.fm = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        self.fm.add_command(label="Test OpenGL", command=do_nothing)
        self.fm.add_command(label="Load Gr File", command=self._load_file)
        self.fm.add_command(label="Load TXT File", command=self._load_txt_file)
        self.RFM.add_recent_menu()

        self.fm.add_command(label="Save", command=self._save, accelerator="Ctrl+S")
        self.fm.add_command(label="Save As...", command=self._save_as, accelerator="Ctrl+Shift+S")

        self.fm.add_separator()
        self.fm.add_command(label="Load Plug'in", command=do_nothing)
        self.fm.add_command(label="Unload Plug'in", command=do_nothing)
        self.fm.add_separator()
        self.fm.add_command(label="Quit All Windows", command=self.GUI.root.quit)
        self.GUI.menu_bar.add_cascade(label="File", menu=self.fm)

    def _bind_shortcuts(self):
        self.GUI.root.bind('<Control-s>', self._save)
        self.GUI.root.bind('<Control-S>', self._save_as)

    def _load_txt_file(self):
        self._load_file(type='.txt')
        return None
    
    def _load_file(self, file_path=None, type='gr'):
        filetypes = None
        if type == 'gr':
            filetypes = (
                ('All files', '*.*'),
                ('gr files', '*.gr'),
                ('text files', '*.txt')
            )
        else:
            filetypes = (
                ('databases', '*.txt'),
                ('All files', '*.*')
            )
        if file_path == None:
            file_path = fd.askopenfilenames(
                title='Open a file',
                filetypes=filetypes)
            

        # self.RFM.add(file_path)
        for i in file_path:
            if os.path.exists(i) == True:
                self.RFM.add(i)
            else:
                if i == '':
                    return
                file_missing_error = "The following file is missing:\n" + i
                messagebox.showerror("File Missing", file_missing_error)
                self.RFM.delete(i)
                return
            
            
            if i.endswith(".gr"):
                self.line_container.load_and_plot(path=i)
                self._set_GUI_saved_false()
            elif i.endswith(".txt"):
                self.GUI.txt_path = i
                self.line_container.load_and_plot(path=i)
                # print("test")
        return
    
    
    def _save(self, event=None):
        if self.GUI.txt_path == None:
            self._save_as(event)
        else:
            sm = SaveManager(self.GUI)
            sm.save(self.line_container, self.GUI.txt_path)
            self._set_GUI_saved_true()
            messagebox.showinfo("Notification", "Saved Successfully!")
        return None
    
    def _save_as(self, event=None):
        filetypes = (
            ('databases', '*.txt'),
        )
        file_path = fd.asksaveasfilename(
            initialfile = "Untitled.txt", \
            defaultextension=".txt", \
            filetypes=filetypes)
        if file_path == '':
            return None
        # print(directory_path)
        sm = SaveManager(self.GUI)
        sm.save(self.line_container, file_path)
        self._set_GUI_saved_true()
        messagebox.showinfo("Notification", "Saved Successfully!")
        return None 
    
    # def _load_db_file(self):
    #     self._load_file(type='db')
    #     return None

    # def _load_file(self, file_path=None, type='gr'):
    #     filetypes = None
    #     if type == 'gr':
    #         filetypes = (
    #             ('All files', '*.*'),
    #             ('gr files', '*.gr'),
    #             ('text files', '*.txt'),
    #             ('databases', '*.db')
    #         )
    #     else:
    #         filetypes = (
    #             ('databases', '*.db'),
    #             ('All files', '*.*')
    #         )
    #     if file_path == None:
    #         file_path = fd.askopenfilenames(
    #             title='Open a file',
    #             filetypes=filetypes)
            

    #     # self.RFM.add(file_path)
    #     for i in file_path:
    #         if os.path.exists(i) == True:
    #             self.RFM.add(i)
    #         else:
    #             if i == '':
    #                 return
    #             file_missing_error = "The following file is missing:\n" + i
    #             messagebox.showerror("File Missing", file_missing_error)
    #             self.RFM.delete(i)
    #             return
            
            
    #         if i.endswith(".gr"):
    #             self.line_container.load_and_plot(path=i)
    #             self._set_GUI_saved_false()
    #         elif i.endswith(".db"):
    #             self.GUI.db_path = i
    #             self.line_container.load_and_plot(path=i)
    #     return

    # def _save(self, event=None):
    #     if self.GUI.db_path == None:
    #         self._save_as(event)
    #     else:
    #         sm = DBManager(self.GUI)
    #         sm.save(self.line_container, self.GUI.db_path)
    #         self._set_GUI_saved_true()
    #         messagebox.showinfo("Notification", "Saved Successfully!")
    #     return None
    #     # messagebox.showerror("Notice", "The function 'Save' executed.")

    # def _save_as(self, event=None):
    #     filetypes = (
    #         ('databases', '*.db'),
    #     )
    #     file_path = fd.asksaveasfilename(
    #         initialfile = "Untitled.db", \
    #         defaultextension=".db", \
    #         filetypes=filetypes)
    #     if file_path == '':
    #         return None
    #     # print(directory_path)
    #     sm = DBManager(self.GUI)
    #     sm.save(self.line_container, file_path)
    #     self._set_GUI_saved_true()
    #     messagebox.showinfo("Notification", "Saved Successfully!")
    #     return None
        
    #     messagebox.showerror("Notice", "The function 'Save As' executed.")
        
    def save_as(self):
        self._save_as()
        return None
    
    def save(self):
        self._save()
        return None
    
    def _set_GUI_saved_false(self):
        self.GUI.root.title('Data Visualization Software (unsaved)')
        self.GUI.saved = False
        return None
    
    def _set_GUI_saved_true(self):
        self.GUI.root.title('Data Visualization Software')
        self.GUI.saved = True
        return None