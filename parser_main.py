# import tkinter as tk

# def do_nothing():
#     return None

# class ParserGUI():
#     def __init__(self, root):
#         self.root = root
#         self.root.title('Parser')
#         self.root.geometry("500x500")
        
#         self.menu_bar = tk.Menu(root)
#         self.file_menu = None
#         # root.config(menu=self.menu_bar)
#         self._menu_bar_main()
#         self.root.config(menu=self.menu_bar)
#         self.root.mainloop()
        
#     def _menu_bar_main(self):
#         self._init_menu_bar_file()
    
#     def _init_menu_bar_file(self):
#         self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
#         self.file_menu.add_command(label="Load", command=do_nothing)
#         self.file_menu.add_command(label="Export", command=do_nothing)
#         self.menu_bar.add_cascade(label="File", menu=self.file_menu)
    
# def main():
#     root = tk.Tk()
#     app = ParserGUI(root)
#     return root, app

# if __name__ == '__main__':
#     root, app = main()




import tkinter as tk

def do_nothing():
    return None

class ParserGUI():
    def __init__(self, root):
        self.root = root
        self.root.title('Parser')
        self.root.geometry("800x500")
        
        self.menu_bar = tk.Menu(root)
        self.file_menu = None
        self._menu_bar_main()
        self.root.config(menu=self.menu_bar)
        
        self.top_frame = tk.Frame(root)
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        
        self.bottom_frame = tk.Frame(root, bg='gray80')
        self.bottom_frame.grid(row=1, column=0, sticky='nsew')
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        temp_placeholder = "Data Information:\n-Rows:\n-Columns:\n---------------\n" + \
            "Configuration Info:\n-Assigned Curves:\n"
        self.label = tk.Label(self.top_frame, text=temp_placeholder, bg="white", anchor='nw', justify='left')
        self.label.pack(fill=tk.BOTH, expand=True)

        self.config_label = tk.Label(self.bottom_frame, text="Configurations")
        self.config_label.grid(row=0, column=0, sticky='nw')

        self.button3 = tk.Button(self.bottom_frame, text="Apply", command=lambda: self._file_menu_export())
        self.button3.grid(row=1, column=0, sticky='se', padx=5, pady=5)

        self.button1 = tk.Button(self.bottom_frame, text="Load", command=lambda: self._file_menu_load())
        self.button1.grid(row=1, column=1, sticky='se', padx=5, pady=5)  # using grid instead of pack and modified sticky attribute



        self.button2 = tk.Button(self.bottom_frame, text="Export", command=lambda: self._file_menu_export())
        self.button2.grid(row=1, column=2, sticky='se', padx=5, pady=5)  # using grid instead of pack and modified sticky attribute

        self.bottom_frame.grid_columnconfigure(0, weight=1)  # setting the weight of the leftmost column
        self.bottom_frame.grid_rowconfigure(0, weight=1)  # setting the weight of the topmost row to push buttons to the bottom

        
        root.mainloop()
        
    def _menu_bar_main(self):
        self._init_menu_bar_file()
        self._init_menu_bar_help()
    
    def _init_menu_bar_file(self):
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Load", command=lambda: self._file_menu_load())
        self.file_menu.add_command(label="Export", command=lambda: self._file_menu_export())
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
    def _init_menu_bar_help(self):
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="User Manual", command=lambda: self._help_menu_user_manual())
        self.menu_bar.add_cascade(label="Help", menu=self.file_menu)
    
    
    def _file_menu_load(self):
        
        return None
    
    def _file_menu_export(self):
        return None
    
    def _help_menu_user_manual(self):
        return None
    
    
def main():
    root = tk.Tk()
    app = ParserGUI(root)
    return root, app

if __name__ == '__main__':
    root, app = main()

