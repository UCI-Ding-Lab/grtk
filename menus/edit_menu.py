import tkinter
import tkinter.messagebox

def do_nothing():
    pass

class EditMenu():
    def __init__(self, GUI, container):
        self.container = container
        self.GUI = GUI
        self.init_edit_menu()

    def init_edit_menu(self):
        self.main = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        self.preference_sub = tkinter.Menu(self.main)
        self.delete_sub = tkinter.Menu(self.main)
        self.main.add_command(label="Copy Image", command=do_nothing)
        self.main.add_separator()
        self.main.add_cascade(label="Preference", menu=self.preference_sub)
        self.main.add_separator()
        self.main.add_cascade(label="Delete", menu=self.delete_sub)
        self.GUI.menu_bar.add_cascade(label="Edit", menu=self.main)
    
    def add_path(self, path: str, sub: str=None):
        """add a line in sub menu

        Args:
            path (str): the name of the line (full file path)
            sub (str, optional): can choose to add to "preference" submenu or "del" submenu. Defaults to None to add to both.
        """
        if sub == "pref":
            self.preference_sub.add_command(label=path, command=do_nothing)
        elif sub == "del":
            self.delete_sub.add_command(label=path, command=lambda: self.trigger_del(path))
        else:
            self.preference_sub.add_command(label=path, command=do_nothing)
            self.delete_sub.add_command(label=path, command=lambda: self.trigger_del(path))

    def del_path(self, path: str, sub: str=None):
        """delete a line in sub menu

        Args:
            path (str): the name of the line (full file path)
            sub (str, optional): can choose to delete lines in "preference" submenu or "del" submenu. Defaults to None to add to both.
        """
        if sub == "pref":
            self.preference_sub.delete(path)
        elif sub == "del":
            self.delete_sub.delete(path)
        else:
            self.preference_sub.delete(path)
            self.delete_sub.delete(path)
    
    def trigger_del(self, path: str) -> None:
        """excecute after click on delete line
        helper function

        Args:
            path (str): full path to delete
        """
        self.container.remove_line(path)