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
        # private initialization
        self.init_private()
        
        # from GUI object
        self.GUI: "main.GUI" = GUI
        self.container = GUI.container.container
        self.axes: axes.Axes = self.GUI.container.matplot_subplot
        
        # structure initialization
        self.structure = self.GUI.curve_pref_frame
        
        # TEST
        self.tree = ttk.Treeview(self.structure)
        self.tree.heading("#0", text="GRTK Layout Tree")
        for i in self.container:
            self.add_file_to_tree(i)
            for j in self.container[i]:
                self.add_type_to_file(i, j)
                for k in self.container[i][j]:
                    self.add_curve_to_type(i, j, k)
        self.tree.bind("<<TreeviewSelect>>", self.build_pref_options)
        self.tree.pack(fill=tkinter.BOTH, expand=1)
        
        # build preference widgets
        self.build_pref_widgets()
        
        # build global preference widgets
        self.build_and_pack_global_widgets()
    
    def add_file_to_tree(self, file: str):
        """add a file to the tree

        Args:
            file (str): file name
        """
        self.tree.insert("", "end", file, text=file)
    
    def add_type_to_file(self, file: str, type: str):
        """add a type to a file in the tree

        Args:
            file (str): file name
            type (str): type name
        """
        self.tree.insert(file, "end", file+"@"+type, text=type)
    
    def add_curve_to_type(self, file: str, type: str, curve: str):
        """add a curve to a type in the tree

        Args:
            file (str): file name
            type (str): type name
            curve (str): curve name
        """
        self.tree.insert(file+"@"+type, "end", file+"@"+type+"@"+curve, text=curve)
    
    def init_private(self):
        self.pack_stat: bool = False
        
        self.show_var = tkinter.IntVar()
        self.color_var = tkinter.StringVar()
        self.width_var = tkinter.DoubleVar()
        self.marker_size_var = tkinter.DoubleVar()
        self.show_grid_var = tkinter.IntVar()
        self.show_axis_var = tkinter.IntVar()
        self.show_label_var = tkinter.IntVar()
        self.show_legend_var = tkinter.IntVar()
        self.dark_mode_var = tkinter.IntVar()
        
        self.show_grid_var.set(1)
        self.show_axis_var.set(1)
        self.show_label_var.set(1)
        self.show_legend_var.set(1)
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
        self.pref_frame = tkinter.LabelFrame(self.structure, text="Set preference for selected file", padx=7)
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
            return
        else:
            # clear previous options
            if self.pack_stat:
                self.unpack_all()
                self.update_dict = dict()
            
            self.f = self.target_path.focus().split("@")[0]
            self.t = self.target_path.focus().split("@")[1]
            self.c = self.target_path.focus().split("@")[2]
            
            self.target_line2d = self.container[self.f][self.t][self.c].line2d_object[0]
            self.show_var.set(1) if self.target_line2d.get_visible() else self.show_var.set(0)
            self.pref_color_preview.configure(bg=self.target_line2d.get_color(), fg=self.target_line2d.get_color())
            self.width_var.set(self.target_line2d.get_linewidth())
            self.pref_width_preview.delete("all")
            self.pref_width_preview.create_line(0, 5, 50, 5, width=self.width_var.get())
            self.pref_marker.set(markerlib.MARKERS_R[self.target_line2d.get_marker()])
            self.marker_size_var.set(self.target_line2d.get_markersize())
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
    
    def refresh(self):
        """refresh the treeview
        """
        self.tree.delete(*self.tree.get_children())
        for i in self.container:
            self.add_file_to_tree(i)
            for j in self.container[i]:
                self.add_type_to_file(i, j)
                for k in self.container[i][j]:
                    self.add_curve_to_type(i, j, k)
        