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

class CheckButtonManager():
    def __init__(self, frame, textbox):
        self.check_buttons = []
        self.frame = frame
        self.counter = 1
        self.textbox = textbox
        return None
    
    def add(self, name, checked=0):
        var = tk.IntVar()
        self.check_buttons.append(\
            (tk.Checkbutton(self.frame, text=str(name), variable=var, command=self._refresh_textbox), var))
        self.check_buttons[self.counter-1][0].grid(row=self.counter, column=0, sticky="nw")
        if checked == 1:
            self.check_buttons[self.counter-1][0].select()
        self.counter += 1
        # self.radio_buttons.append(temp)
        # temp = None
        return None
    def _refresh_textbox(self):
        textbox_str = ""
        temp_str_list = []
        temp_str = ""
        for button, var in self.check_buttons:
            # if button.cget("text") == "time":
            #     temp_str = "time/"
            # self.textbox.append(button.cget("text"))
            temp_str = str(button.cget("text"))
            if var.get() == 0:
                temp_str = temp_str + "_del"
            temp_str_list.append(temp_str)
            temp_str = ""
        textbox_str = "/".join(temp_str_list)
        self.textbox.delete(1.0,"end")
        self.textbox.insert(1.0, textbox_str)

class ParserGUI():
    def __init__(self, root):
        self.root = root
        self.root.title('Parser')
        self.root.geometry("800x600")
        
        self.menu_bar = tk.Menu(root)
        self.file_menu = None
        self._init_menu_bar()
        
        
        self._init_top_frame()
        self._init_middle_frame()
        self._init_bottom_frame()

        # frames layout configs
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=5)
        self.root.grid_rowconfigure(2, weight=5)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.parser = gparse()

        root.mainloop()
        
    def _init_top_frame(self):
        self.top_frame = tk.LabelFrame(self.root, text="Data Information", labelanchor="nw")
        self.top_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 2))
        self.top_frame.grid_propagate(False)
        #Data Information:\n highlightbackground="black", highlightthickness=1
        
        # # Set up the canvas
        # self.top_canvas = tk.Canvas(self.top_label_frame)
        # self.top_canvas.grid(row=0, column=0, sticky="nsew")
        
        # # Set the frame inside the canvas
        # self.top_frame = tk.Frame(self.top_canvas)
        # self.top_frame.grid(row=0, column=0, sticky="nsew")
        
        
        top_placeholder = "Rows:\nColumns:\n" 
        #bg="white", 
        self.top_label = tk.Label(self.top_frame, text=top_placeholder, anchor='nw', \
            justify='left')
        self.top_label.pack(fill=tk.BOTH, expand=True)
    
    # def _init_middle_frame(self):
    #     self.middle_label_frame = tk.LabelFrame(self.root, text="Configuration Information", labelanchor="nw")
    #     self.middle_label_frame.grid(row=1, column=0, sticky='nsew')
    #     self.middle_scrollbar = tk.Scrollbar(self.root, orient="vertical")
    #     self.middle_scrollbar.grid(row=1, column=1, sticky="ns")
        
    #     self.middle_canvas = tk.Canvas(self.middle_label_frame, \
    #         yscrollcommand=self.middle_scrollbar.set)
    #     self.middle_canvas.pack(fill=tk.BOTH, expand=True)
        
    #     middle_placeholder = "Assigned Curves:\n"
    #     self.middle_label = tk.Label(self.middle_canvas, text=middle_placeholder, anchor='nw', justify='left')
    #     self.middle_label.grid(row=0, column=0, sticky="nw")
        

        
    #     self.middle_scrollbar.config(command=self.middle_canvas.yview)
    
    def _init_middle_frame(self):
        self.middle_label_frame = tk.LabelFrame(self.root, text="Configuration Information", \
            labelanchor="nw")
        self.middle_label_frame.grid(row=1, column=0, sticky='nsew', pady=2)
        # self.middle_label_frame.grid_columnconfigure(0, weight=1)  # make the frame expandable
        self.middle_label_frame.grid_propagate(False)
        
        # Set up the scrollbar
        self.middle_scrollbar = tk.Scrollbar(self.root, orient="vertical")
        self.middle_scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Set up the canvas
        self.middle_canvas = tk.Canvas(self.middle_label_frame, \
            yscrollcommand=self.middle_scrollbar.set, \
            width=800, \
            height=200)
        self.middle_canvas.grid(row=0, column=0, sticky="nsew")
        # self.middle_canvas.grid_propagate(False)
        
        # Set the frame inside the canvas
        self.middle_frame = tk.Frame(self.middle_canvas)
        self.middle_frame.grid(row=0, column=0, sticky="nsew")
        
        # Add the frame to the canvas
        self.middle_canvas.create_window((0, 0), window=self.middle_frame, anchor="nw")
        
        # Configure the scroll region of the canvas whenever it changes
        self.middle_frame.bind("<Configure>", lambda e: self.middle_canvas.configure(scrollregion=self.middle_canvas.bbox("all")))
        
        # Connect the scrollbar to the canvas
        self.middle_scrollbar.config(command=self.middle_canvas.yview)
        
        # Sample label inside the frame
        middle_placeholder = "Assigned Amount:\nAssigned Names:\n"
        self.middle_label = tk.Label(self.middle_frame, text=middle_placeholder, anchor='nw', justify='left')
        self.middle_label.grid(row=0, column=0, sticky="nw")

        
    
    def _init_bottom_frame(self):
        #bg='gray80', 
        self.bottom_label_frame = tk.LabelFrame(self.root, text="Configurations", labelanchor="nw")
        self.bottom_label_frame.grid(row=2, column=0, sticky='nsew', pady=(2, 0))
        self.bottom_label_frame.grid_propagate(False)
        # highlightbackground="black", highlightthickness=1, 
        # self.config_label = tk.Label(self.bottom_frame, text="Configurations")
        # self.config_label.grid(row=0, column=0, sticky='nw')


        # Set up the scrollbar
        self.bottom_scrollbar = tk.Scrollbar(self.root, orient="vertical")
        self.bottom_scrollbar.grid(row=2, column=1, sticky="ns")
        
        # Set up the canvas
        self.bottom_canvas = tk.Canvas(self.bottom_label_frame, \
            yscrollcommand=self.bottom_scrollbar.set, \
            width=750, \
            height=200)
        self.bottom_canvas.grid(row=0, column=0, sticky="nsew")
        # self.middle_canvas.grid_propagate(False)
        
        # Set the frame inside the canvas
        self.bottom_frame = tk.Frame(self.bottom_canvas)
        self.bottom_frame.grid(row=0, column=0, sticky="nsew")
        
        # Add the frame to the canvas
        self.bottom_canvas.create_window((0, 0), window=self.bottom_frame, anchor="nw")
        
        # Configure the scroll region of the canvas whenever it changes
        self.bottom_frame.bind("<Configure>", \
            lambda e: self.bottom_canvas.configure(scrollregion=self.bottom_canvas.bbox("all")))
        
        # Connect the scrollbar to the canvas
        self.bottom_scrollbar.config(command=self.bottom_canvas.yview)


        self.curve_names_label = tk.Label(self.bottom_frame, text="Assign Names: ",  anchor='nw', justify='left')
        self.curve_names_label.grid(row=0, column=0, sticky="nw")
  
        self.curve_names_textbox = tk.Text(self.bottom_frame, height=1, width=70)
        self.curve_names_textbox.grid(row=0, column=1, sticky="nw")


        self.button1 = tk.Button(self.bottom_frame, text="Load", command=lambda: self._file_menu_load())
        self.button1.grid(row=0, column=2, sticky='ne', padx=5, pady=0)  # using grid instead of pack and modified sticky attribute
        #column=0, 
        self.button3 = tk.Button(self.bottom_frame, text="Apply", command=lambda: self._file_menu_apply())
        self.button3.grid(row=0, column=3, sticky='ne', padx=5, pady=0)
        # 
        self.button2 = tk.Button(self.bottom_frame, text="Export", command=lambda: self._file_menu_export())
        self.button2.grid(row=0, column=4, sticky='ne', padx=5, pady=0)  # using grid instead of pack and modified sticky attribute
        # 
        #bg="white",  bg='gray80',
        

        
        # # self.curve_amount_label = tk.Label(self.bottom_frame, text="Assigned Amount: ",  anchor='nw', justify='left')
        # # self.curve_amount_label.grid(row=0, column=0, sticky="nw")
        

        # # self.curve_names_textbox_sb = tk.Scrollbar(self.bottom_frame, orient='horizontal')
        # # self.curve_names_textbox_sb.grid(row=1, column=1, sticky="nwe")
        
        
        
        # # self.bottom_frame.grid_rowconfigure(0, weight=1)
        # self.bottom_frame.grid_columnconfigure(0, weight=1)  # setting the weight of the leftmost column
        # self.bottom_frame.grid_columnconfigure(1, weight=1)
        # self.bottom_frame.grid_rowconfigure(0, weight=1)  # setting the weight of the topmost row to push buttons to the bottom
        # self.bottom_frame.grid_rowconfigure(1, weight=1)
        # self.bottom_frame.grid_rowconfigure(2, weight=1)
        
        
        
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
        for i in self.file_paths:
            if i == "":
                return
        self.row_count = 0
        self.col_count = 0
        self.cbm = CheckButtonManager(self.bottom_frame, self.curve_names_textbox)
        
        
        for f in self.file_paths:
            temp = self.parser.get_shape(f)
            self.row_count += temp[0]
            self.col_count += temp[1]
        self.top_label.config(text=f"Rows: {self.row_count}\nColumns: {self.col_count}\n")
        
        default_assigned_names = "time"
        self.cbm.add("time", 1)
        for i in range(self.col_count-1):
            default_assigned_names += f"/{i}_del"
            self.cbm.add(i)
        self.curve_names_textbox.insert(1.0, default_assigned_names) #tk.INSERT
        
        return None
    
    
    def _file_menu_apply(self):
        user_input = self.curve_names_textbox.get("1.0", tk.END)
        user_input = re.sub(r"[\n\t\s]*", "", user_input)
        self.assigned_names = user_input.split("/")
        assigned_names_text = "Assigned Names: \n"
        count = 0
        for i in self.assigned_names:
            if len(i) > 4 and i[-4:] == "_del":
                continue
            assigned_names_text += f" -{i} \n"
            count += 1
        assigned_amount_text = f"Assigned Amount: {count}\n"
        temp_str = assigned_amount_text + assigned_names_text
        self.middle_label.config(text=temp_str)
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

