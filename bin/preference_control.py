import math
import tkinter
from tkinter import ttk
from tkinter import colorchooser

from helper import markerlib


# typecheck
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main
    from helper import load
    from matplotlib import axes

class perf_ctl(object):
    def __init__(self, GUI: "main.GUI"):
        """a popup window to edit preference for each line
        will be called by edit menu

        Args:
            GUI (main.GUI): GUI object
        """
        # plugin
        self.on_change_color_job=[]
        
        # private initialization
        self.init_private()
        
        # from GUI object
        self.GUI: "main.GUI" = GUI
        self.container = GUI.container.container
        self.axes: axes.Axes = self.GUI.container.matplot_subplot
        
        # structure initialization
        self.structure = self.GUI.curve_pref_frame
        self.specific = self.GUI.curve_pref_down
        
        # scrpll style
        style = ttk.Style()
        style.theme_use('classic')

        # Tree
        self.tree = ttk.Treeview(self.structure, selectmode='browse')
        self.treebar = ttk.Scrollbar(self.structure, orient ="vertical", command = self.tree.yview)
        self.tree.heading("#0", text="GRTK Layout Tree")
        possible_type = []
        
        # Sort to tree
        for file in list(self.container.keys()):
            for type in list(self.container[file].keys()):
                possible_type.append(type)
        for type in set(possible_type):
            self.add_type_to_tree(type)
        for file in list(self.container.keys()):
            for type in list(self.container[file].keys()):
                self.add_file_to_type(file, type)
                for curve in list(self.container[file][type].keys()):
                    self.add_curve_to_file(file, type, curve)
        
        # Init action
        self.tree.bind("<<TreeviewSelect>>", self.build_pref_options)
        self.tree.pack(side="left", fill="both", expand=True)
        self.treebar.pack(side="right", fill="y")
        self.tree.configure(xscrollcommand = self.treebar.set)
        
        # build preference widgets
        self.build_pref_widgets()
        self.build_high_level_widgets()
        
        # build global preference widgets
        self.build_and_pack_global_widgets()
    
    def add_type_to_tree(self, type: str):
        """add a type to a file in the tree

        Args:
            file (str): file name
            type (str): type name
        """
        self.tree.insert("", "end", type, text=type)
    
    def add_file_to_type(self, file: str, type: str):
        """add a file to a type in the tree

        Args:
            file (str): file name
            type (str): type name
        """
        self.tree.insert(type, "end", type+"@"+file, text=file)
    
    def add_curve_to_file(self, file: str, type: str, curve: str):
        """add a curve to a file in the tree

        Args:
            file (str): file name
            type (str): type name
            curve (str): curve name
        """
        self.tree.insert(type+"@"+file, "end", type+"@"+file+"@"+curve, text=curve)
    
    def init_private(self):
        self.pack_stat: bool = False
        self.pack_stat_high_level: bool = False
        self.selection_mode: bool = False
        
        self.show_var = tkinter.IntVar()
        self.color_var = tkinter.StringVar()
        self.width_var = tkinter.DoubleVar()
        self.marker_size_var = tkinter.DoubleVar()
        self.show_grid_var = tkinter.IntVar()
        self.show_axis_var = tkinter.IntVar()
        self.show_label_var = tkinter.IntVar()
        self.show_legend_var = tkinter.IntVar()
        self.dark_mode_var = tkinter.IntVar()
        self.indicate_var = tkinter.StringVar()
        
        self.show_grid_var.set(1)
        self.show_axis_var.set(1)
        self.show_label_var.set(1)
        self.show_legend_var.set(0)
        self.dark_mode_var.set(1)

    ### GLOBAL PREFERENCE WIDGETS ###
    
    def build_and_pack_global_widgets(self):
        self.glb_pref = tkinter.LabelFrame(self.GUI.global_pref_frame, text="Global preference", padx=5)
        self.show_grid = tkinter.Checkbutton(self.glb_pref, text="Show grid", variable=self.show_grid_var, command=self.global_change_show_grid)
        self.show_axis = tkinter.Checkbutton(self.glb_pref, text="Show axis", variable=self.show_axis_var, command=self.global_change_show_axis)
        self.show_label = tkinter.Checkbutton(self.glb_pref, text="Show label", variable=self.show_label_var, command=self.global_change_show_label)
        self.show_legend = tkinter.Checkbutton(self.glb_pref, text="Show legend", variable=self.show_legend_var, command=self.global_change_show_legend)
        self.dark_mode = tkinter.Checkbutton(self.glb_pref, text="Dark mode", variable=self.dark_mode_var, command=self.global_change_dark_mode)
        
        self.glb_pref.pack(fill=tkinter.BOTH, expand=True, padx=10)
        self.show_grid.grid(row=0, column=0, sticky=tkinter.W)
        self.show_axis.grid(row=0, column=1, sticky=tkinter.W)
        self.show_label.grid(row=0, column=2, sticky=tkinter.W)
        self.show_legend.grid(row=1 ,column=0, sticky=tkinter.W)
        self.dark_mode.grid(row=1, column=1, sticky=tkinter.W)
    
    def global_change_show_grid(self):
        visibility = True if self.show_grid_var.get() == 1 else False
        self.GUI.container.change_grid(visibility)
        self.GUI.container._refresh_canvas()
    
    def global_change_show_axis(self):
        visibility = True if self.show_axis_var.get() == 1 else False
        self.GUI.container.change_axis(visibility)
        self.GUI.container._refresh_canvas()
    
    def global_change_show_label(self):
        visibility = True if self.show_label_var.get() == 1 else False
        self.GUI.container.change_label(visibility)
        self.GUI.container._refresh_canvas()
    
    def global_change_show_legend(self):
        visibility = True if self.show_legend_var.get() == 1 else False
        self.GUI.container.change_legend(visibility)
        self.GUI.container._refresh_canvas()
    
    def global_change_dark_mode(self):
        theme = "dark" if self.dark_mode_var.get() == 1 else "light"
        self.GUI.container.change_color_theme(theme)
        self.GUI.container._refresh_canvas()
    
    ### CURVE PREFERENCE WIDGETS ###
    
    def build_pref_widgets(self):
        self.pref_frame = tkinter.LabelFrame(self.specific, text="Set preference for selected file", padx=7)
        self.pref_show_line = tkinter.Checkbutton(self.pref_frame, text="Show on graph", variable=self.show_var, command=self.change_show)
        self.sep1 = ttk.Separator(self.pref_frame, orient=tkinter.HORIZONTAL)
        self.pref_color_preview = tkinter.Label(self.pref_frame, text="__")
        self.pref_color = tkinter.Button(self.pref_frame, text="Change Color", command=self.change_color)
        self.sep2 = ttk.Separator(self.pref_frame, orient=tkinter.HORIZONTAL)
        self.pref_width_preview = tkinter.Canvas(self.pref_frame, width=50, height=10)
        self.pref_width = tkinter.Spinbox(self.pref_frame, from_=0 ,to=100 ,increment=1 ,command=self.change_width ,textvariable=self.width_var)
        self.sep3 = ttk.Separator(self.pref_frame, orient=tkinter.HORIZONTAL)
        self.pref_marker_txt = tkinter.Label(self.pref_frame, text="Marker")
        self.pref_marker = ttk.Combobox(self.pref_frame, values=list(markerlib.MARKERS.keys()), state="readonly")
        self.pref_marker.bind("<<ComboboxSelected>>", self.change_marker)
        self.sep4 = ttk.Separator(self.pref_frame, orient=tkinter.HORIZONTAL)
        self.pref_marker_size_txt = tkinter.Label(self.pref_frame, text="Marker Size")
        self.pref_marker_size = tkinter.Spinbox(self.pref_frame, from_=0 ,to=100 ,increment=0.1 ,command=self.change_marker_size ,textvariable=self.marker_size_var)
        self.sep5 = ttk.Separator(self.pref_frame, orient=tkinter.HORIZONTAL)
        self.pref_marker_color_preview = tkinter.Label(self.pref_frame, text="__")
        self.pref_marker_color = tkinter.Button(self.pref_frame, text="Change Marker Color", command=self.change_marker_color)
    
    def build_high_level_widgets(self):
        self.high_level_frame = tkinter.LabelFrame(self.specific, text="High level preference", padx=7)
        self.indicate_entry = tkinter.Label(self.high_level_frame, textvariable=self.indicate_var)
        self.high_level_show_line = tkinter.Button(self.high_level_frame, text="Show", command=self.change_show_all)
        self.high_level_hide_line = tkinter.Button(self.high_level_frame, text="Hide", command=self.change_hide_all)
    
    def pack_all(self):
        """pack all widgets
        """
        self.pref_frame.pack(expand=True, fill=tkinter.BOTH, padx=10)
        self.pref_show_line.grid(row=0, column=0, columnspan=2)
        self.sep1.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        self.pref_color_preview.grid(row=2, column=0, sticky="ew")
        self.pref_color.grid(row=2, column=1, sticky="ew")
        self.sep2.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        self.pref_width_preview.grid(row=4, column=0)
        self.pref_width.grid(row=4, column=1)
        self.sep3.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)
        self.pref_marker_txt.grid(row=6, column=0)
        self.pref_marker.grid(row=6, column=1)
        self.sep4.grid(row=7, column=0, columnspan=2, sticky="ew", pady=5)
        self.pref_marker_size_txt.grid(row=8, column=0)
        self.pref_marker_size.grid(row=8, column=1)
        self.sep5.grid(row=9, column=0, columnspan=2, sticky="ew", pady=5)
        self.pref_marker_color_preview.grid(row=10, column=0, sticky="ew")
        self.pref_marker_color.grid(row=10, column=1, sticky="ew")
        # refresh frame
        self.pref_frame.update()
    
    def pack_all_high_level(self):
        """pack all high level widgets
        """
        self.high_level_frame.pack(expand=True, fill=tkinter.BOTH, padx=10)
        self.indicate_entry.grid(row=0, column=0, sticky="ew", columnspan=2, pady=5)
        self.high_level_show_line.grid(row=1, column=0, sticky="ew")
        self.high_level_hide_line.grid(row=1, column=1, sticky="ew")
        # refresh frame
        self.high_level_frame.update()
    
    def unpack_all(self):
        """unpack all widgets
        """
        self.pref_frame.pack_forget()
        self.pref_show_line.grid_forget()
        self.sep1.grid_forget()
        self.pref_color_preview.grid_forget()
        self.pref_color.grid_forget()
        self.sep2.grid_forget()
        self.pref_width_preview.grid_forget()
        self.pref_width.grid_forget()
        self.sep3.grid_forget()
        self.pref_marker_txt.grid_forget()
        self.pref_marker.grid_forget()
        self.sep4.grid_forget()
        self.pref_marker_size_txt.grid_forget()
        self.pref_marker_size.grid_forget()
        self.sep5.grid_forget()
        self.pref_marker_color_preview.grid_forget()
        self.pref_marker_color.grid_forget()
    
    def unpack_all_high_level(self):
        """unpack all high level widgets
        """
        self.high_level_frame.pack_forget()
        self.indicate_entry.grid_forget()
        self.high_level_show_line.grid_forget()
        self.high_level_hide_line.grid_forget()
    
    def build_pref_options(self, event: tkinter.Event):
        """this is a callback function for the combobox
        after a selection is made, this function will be called
        if there is any previous options widgets packed, it will be cleared
        pack new options widgets according to the selection file path

        Args:
            event (event): a must have argument for tkinter callback function
        """
        # check current status
        self.target_path: ttk.Treeview = event.widget
        if (len(self.target_path.selection()) != 1) or (len(self.target_path.focus().split("@")) != 3):
            if self.pack_stat:
                self.unpack_all()
                self.update_dict = dict()
                self.pack_stat = False
            elif self.pack_stat_high_level:
                self.unpack_all_high_level()
                self.update_dict = dict()
                self.pack_stat_high_level = False
            
            self.c = None
            
            if self.selection_mode:
                self.global_hide()
                for single_select in self.target_path.selection():
                    self.t = single_select.split("@")[0]
                    self.f = single_select.split("@")[1]
                    self.c = single_select.split("@")[2]
                    self.GUI.container.container[self.f][self.t][self.c].line2d_object[0].set_visible(True)
            
            else:
                
                if len(self.target_path.focus().split("@")) == 2:
                    self.t = self.target_path.focus().split("@")[0]
                    self.f = self.target_path.focus().split("@")[1]
                    self.indicate_var.set(f"File: {self.f}\nType: {self.t}")
                elif len(self.target_path.focus().split("@")) == 1:
                    self.t = self.target_path.focus().split("@")[0]
                    self.f = None
                    self.indicate_var.set(f"File: ALL\nType: {self.t}")
                else:
                    self.t = None
                    self.f = None
                    self.indicate_var.set(f"NULL")
                    
                self.pack_all_high_level()
                self.pack_stat_high_level = True
        
        else:
            # clear previous options
            if self.pack_stat:
                self.unpack_all()
                self.update_dict = dict()
                self.pack_stat = False
            elif self.pack_stat_high_level:
                self.unpack_all_high_level()
                self.update_dict = dict()
                self.pack_stat_high_level = False
            
            self.t = self.target_path.focus().split("@")[0]
            self.f = self.target_path.focus().split("@")[1]
            self.c = self.target_path.focus().split("@")[2]
            
            if self.selection_mode:
                self.global_hide()
                self.GUI.container.container[self.f][self.t][self.c].line2d_object[0].set_visible(True)
            
            self.target_line2d = self.container[self.f][self.t][self.c].line2d_object[0]
            self.show_var.set(1) if self.target_line2d.get_visible() else self.show_var.set(0)
            if type(self.target_line2d.get_color()) is tuple:
                r = math.ceil(self.target_line2d.get_color()[0]*255)
                g = math.ceil(self.target_line2d.get_color()[1]*255)
                b = math.ceil(self.target_line2d.get_color()[2]*255)
                color = '#%02x%02x%02x' % (r, g, b) 
                self.pref_color_preview.configure(bg=color, fg=color)
            else:
                self.pref_color_preview.configure(bg=self.target_line2d.get_color(), fg=self.target_line2d.get_color())
            self.width_var.set(self.target_line2d.get_linewidth())
            self.pref_width_preview.delete("all")
            self.pref_width_preview.create_line(0, 5, 50, 5, width=self.width_var.get())
            self.pref_marker.set(markerlib.MARKERS_R[self.target_line2d.get_marker()])
            self.marker_size_var.set(self.target_line2d.get_markersize())
            if type(self.target_line2d.get_markerfacecolor()) is tuple:
                r = math.ceil(self.target_line2d.get_markerfacecolor()[0]*255)
                g = math.ceil(self.target_line2d.get_markerfacecolor()[1]*255)
                b = math.ceil(self.target_line2d.get_markerfacecolor()[2]*255)
                color = '#%02x%02x%02x' % (r, g, b) 
                self.pref_marker_color_preview.configure(bg=color, fg=color) # type: ignore
            else:
                self.pref_marker_color_preview.configure(bg=self.target_line2d.get_markerfacecolor(), fg=self.target_line2d.get_markerfacecolor()) # type: ignore
            
            # build new options
            self.pack_all()
            self.pack_stat = True
    
    def change_show(self):
        """record change in show variable
        """
        kwargs = {"visible": self.show_var.get()}
        self.GUI.container.change_line_preference(
            path=self.f,
            type=self.t,
            curve=self.c,
            kwargs=kwargs,
        )
    
    def change_color(self):
        """record change in color variable
        ask for color and update preview
        """
        self.color_var = colorchooser.askcolor()[1]
        self.pref_color_preview.configure(bg=self.color_var, fg=self.color_var) # type: ignore
        kwargs = {"color": self.color_var}
        self.GUI.container.change_line_preference(
            path=self.f,
            type=self.t,
            curve=self.c,
            kwargs=kwargs,
        )
        for job in self.on_change_color_job:
            job()
    
    def change_width(self):
        """record change in width variable
        """
        self.pref_width_preview.delete("all")
        self.pref_width_preview.create_line(0, 5, 50, 5, width=self.width_var.get())
        kwargs = {"linewidth": self.width_var.get()}
        self.GUI.container.change_line_preference(
            path=self.f,
            type=self.t,
            curve=self.c, 
            kwargs=kwargs,
        )
    
    def change_marker_size(self):
        """record change in marker size variable
        """
        kwargs = {"markersize": self.marker_size_var.get()}
        self.GUI.container.change_line_preference(
            path=self.f,
            type=self.t,
            curve=self.c, 
            kwargs=kwargs,
        )
    
    def change_marker(self, event):
        """record change in marker variable
        """
        kwargs = {"marker": markerlib.MARKERS[self.pref_marker.get()]}
        self.GUI.container.change_line_preference(
            path=self.f,
            type=self.t,
            curve=self.c, 
            kwargs=kwargs,
        )
    
    def change_marker_color(self):
        """record change in marker color variable
        """
        self.marker_color_var = colorchooser.askcolor()[1]
        self.pref_marker_color_preview.configure(bg=self.marker_color_var, fg=self.marker_color_var) # type: ignore
        kwargs = {
            "markerfacecolor": self.marker_color_var,
            "markeredgecolor": self.marker_color_var
        }
        self.GUI.container.change_line_preference(
            path=self.f,
            type=self.t,
            curve=self.c, 
            kwargs=kwargs,
        )
    
    def change_show_all(self):
        """record change in show variable
        """
        kwargs = {"visible": 1}
        if self.f is not None and self.t is not None:
            for curve in list(self.GUI.container.container[self.f][self.t].keys()):
                self.GUI.container.change_line_preference(
                    path=self.f,
                    type=self.t,
                    curve=curve,
                    kwargs=kwargs,
                )
        elif self.t is not None and self.f is None:
            for files in list(self.GUI.container.container.keys()):
                for curve in list(self.GUI.container.container[files][self.t].keys()):
                    self.GUI.container.change_line_preference(
                        path=files,
                        type=self.t,
                        curve=curve,
                        kwargs=kwargs,
                    )
        else:
            return
    
    def change_hide_all(self):
        """record change in show variable
        """
        kwargs = {"visible": 0}
        if self.f is not None and self.t is not None:
            for curve in list(self.GUI.container.container[self.f][self.t].keys()):
                self.GUI.container.change_line_preference(
                    path=self.f,
                    type=self.t,
                    curve=curve,
                    kwargs=kwargs,
                )
        elif self.t is not None and self.f is None:
            for files in list(self.GUI.container.container.keys()):
                for curve in list(self.GUI.container.container[files][self.t].keys()):
                    self.GUI.container.change_line_preference(
                        path=files,
                        type=self.t,
                        curve=curve,
                        kwargs=kwargs,
                    )
        else:
            return
    
    def global_show(self):
        kwargs = {"visible": 1}
        for file in list(self.GUI.container.container.keys()):
            for type in list(self.GUI.container.container[file].keys()):
                for curve in list(self.GUI.container.container[file][type].keys()):
                    self.GUI.container.change_line_preference(
                        path=file,
                        type=type,
                        curve=curve,
                        kwargs=kwargs,
                    )
    
    def global_hide(self):
        kwargs = {"visible": 0}
        for file in list(self.GUI.container.container.keys()):
            for type in list(self.GUI.container.container[file].keys()):
                for curve in list(self.GUI.container.container[file][type].keys()):
                    self.GUI.container.change_line_preference(
                        path=file,
                        type=type,
                        curve=curve,
                        kwargs=kwargs,
                    )
    
    def refresh(self):
        """refresh the treeview
        """
        self.tree.delete(*self.tree.get_children())
        
        # Re-sort to tree 
        possible_type = []
        for file in list(self.container.keys()):
            for type in list(self.container[file].keys()):
                possible_type.append(type)
        for type in set(possible_type):
            self.add_type_to_tree(type)
        for file in list(self.container.keys()):
            for type in list(self.container[file].keys()):
                self.add_file_to_type(file, type)
                for curve in list(self.container[file][type].keys()):
                    self.add_curve_to_file(file, type, curve)
        