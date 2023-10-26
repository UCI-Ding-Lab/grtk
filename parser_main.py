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
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import re
from Gparse.gparse import gparse

def do_nothing():
    return None

class ParserGUI():
    def __init__(self, root):
        self.root = root
        self.root.title('Parser')
        self.root.geometry("800x500")
        
        self.menu_bar = tk.Menu(root)
        self.file_menu = None
        self._init_menu_bar()
        
        
        self._init_top_frame()
        self._init_middle_frame()
        self._init_bottom_frame()

        # frames layout configs
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.parser = gparse()

        root.mainloop()
        
    def _init_top_frame(self):
        self.top_frame = tk.LabelFrame(self.root, text="Data Information", labelanchor="nw")
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        #Data Information:\n highlightbackground="black", highlightthickness=1
        top_placeholder = "Rows:\nColumns:\n" 
        #bg="white", 
        self.top_label = tk.Label(self.top_frame, text=top_placeholder, anchor='nw', justify='left')
        self.top_label.pack(fill=tk.BOTH, expand=True)
    
    def _init_middle_frame(self):
        self.middle_frame = tk.LabelFrame(self.root, text="Configuration Information", labelanchor="nw")
        self.middle_frame.grid(row=1, column=0, sticky='nsew')
        
        middle_placeholder = "Assigned Curves:\n"
        self.middle_label = tk.Label(self.middle_frame, text=middle_placeholder, anchor='nw', justify='left')
        self.middle_label.pack(fill=tk.BOTH, expand=True)
    
    def _init_bottom_frame(self):
        #bg='gray80', 
        self.bottom_frame = tk.LabelFrame(self.root, text="Configurations", labelanchor="nw")
        self.bottom_frame.grid(row=2, column=0, sticky='nsew')
        # highlightbackground="black", highlightthickness=1, 
        # self.config_label = tk.Label(self.bottom_frame, text="Configurations")
        # self.config_label.grid(row=0, column=0, sticky='nw')

        self.button1 = tk.Button(self.bottom_frame, text="Load", command=lambda: self._file_menu_load())
        self.button1.grid(row=2, column=2, sticky='se', padx=5, pady=5)  # using grid instead of pack and modified sticky attribute
        #column=0, 
        self.button3 = tk.Button(self.bottom_frame, text="Apply", command=lambda: self._file_menu_apply())
        self.button3.grid(row=2, column=3, sticky='se', padx=5, pady=5)
        # 
        self.button2 = tk.Button(self.bottom_frame, text="Export", command=lambda: self._file_menu_export())
        self.button2.grid(row=2, column=4, sticky='se', padx=5, pady=5)  # using grid instead of pack and modified sticky attribute
        # 
        #bg="white",  bg='gray80',
        

        
        self.curve_names_label = tk.Label(self.bottom_frame, text="Assigned Amount:\nAssign Names: ",  anchor='nw', justify='left')
        self.curve_names_label.grid(row=1, column=0, sticky="nw")
        

        
        self.curve_names_textbox = tk.Text(self.bottom_frame, height=10, width=70)
        self.curve_names_textbox.grid(row=1, column=1, sticky="nw")
 
        
        
        
        # self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)  # setting the weight of the leftmost column
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)  # setting the weight of the topmost row to push buttons to the bottom
        self.bottom_frame.grid_rowconfigure(1, weight=1)
        self.bottom_frame.grid_rowconfigure(2, weight=1)
        
        
        
    def _init_menu_bar(self):
        #self._init_menu_bar_file()
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
        self.root.config(menu=self.menu_bar)
        
    
    
    def _file_menu_load(self):
        # file_path = None
        # filetypes = None
        # if type == 'gr':
        #     filetypes = (
        #         ('All files', '*.*'),
        #         ('gr files', '*.gr'),
        #         ('text files', '*.txt')
        #     )
        # else:
        #     filetypes = (
        #         ('text files', '*.txt'),
        #         ('All files', '*.*')
        #     )
        # if file_path == None:
        #     file_path = fd.askopenfilenames(
        #         title='Open a file',
        #         filetypes=filetypes)
        filetypes = (('All files', '*.*'), ('text files', '*.txt'))
        self.file_paths = fd.askopenfilenames(
            title='Open a file',
            )#filetypes=filetypes
        # self.parser.proc_group(file_paths)
        self.row_count = 0
        self.col_count = 0
        for f in self.file_paths:
            temp = self.parser.get_shape(f)
            self.row_count += temp[0]
            self.col_count += temp[1]
        self.top_label.config(text=f"Rows: {self.row_count}\nColumns: {self.col_count}\n")
        
        default_assigned_names = "time"
        for i in range(self.col_count-1):
            default_assigned_names += f"/{i}"
        self.curve_names_textbox.insert(tk.INSERT, default_assigned_names)
        
        return None
    
    
    def _file_menu_apply(self):
        user_input = self.curve_names_textbox.get("1.0", tk.END)
        user_input = re.sub(r"[\n\t\s]*", "", user_input)
        self.assigned_names = user_input.split("/")
        temp_text = f"Assigned Amount: {len(self.assigned_names)}\nAssigned Names: "
        for i in self.assigned_names:
            temp_text += f" -{i} "
        self.middle_label.config(text=temp_text)
        return None
    
    
    def _file_menu_export(self):
        self.parser.proc_group(self.file_paths, self.assigned_names)
        return None
    
    def _help_menu_user_manual(self):
        return None
    
    
def main():
    root = tk.Tk()
    app = ParserGUI(root)
    return root, app

if __name__ == '__main__':
    root, app = main()

