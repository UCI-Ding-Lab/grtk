import tkinter
from tkinter import scrolledtext
# typecheck
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main

class setting(object):
    SPERATOR = "----------"
    TYPES = {
        "system": dict(linewidth=0.5,color="yellow"),
        "background": dict(linewidth=0.5,color="green"),
        "data": dict(linewidth=0.0,color="red",marker=".",markersize=2.8),
        "default": dict(linewidth=0.5,color="white"),
    }

    def __init__(self):
        pass
    
    def change_setting(self, base: "main.GUI"):
        self.setting_window = tkinter.Toplevel(base.root)
        self.setting_window.title("Setting")
        self.setting_window.geometry("300x420")
        self.lf_separator = tkinter.LabelFrame(self.setting_window, text="Separator")
        self.lf_separator.pack(fill="both", expand=1)
        self.seperator_setting = tkinter.Entry(self.lf_separator)
        self.seperator_setting.insert(0, self.SPERATOR)
        self.seperator_setting.pack(fill="both", expand=1)
        self.lf_types = tkinter.LabelFrame(self.setting_window, text="Type Presets")
        self.lf_types.pack(fill="both", expand=1)
        self.types_define = scrolledtext.ScrolledText(self.lf_types)
        self.types_define.insert(tkinter.INSERT, str(self.TYPES))
        self.types_define.pack(fill="both", expand=1)
        self.save_button = tkinter.Button(self.setting_window, text="Save", command=self.save_setting)
        self.save_button.pack(fill="both", expand=1)
    
    def save_setting(self):
        setting.SPERATOR = self.seperator_setting.get()
        setting.TYPES = eval(self.types_define.get("1.0", tkinter.END))
        self.setting_window.destroy()
        
        
        
        