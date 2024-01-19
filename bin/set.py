import tkinter
from tkinter import scrolledtext

# typecheck
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import main


class setting(object):
    # Data settings
    SPERATOR = "----------"

    # Program settings
    DEBUG_MODE = True
    DEBUG_PRINT = True
    OPTIMIZE = False
    BUFFER_SIZE_KB = -1

    # Style settings
    THEME_USE = "clam"
    TREEVIEW_ROW_HEIGHT = 40
    PROGRESS_BAR_COLOR_FG = "green"
    PROGRESS_BAR_COLOR_BG = "green"

    # Graph settings
    TYPES = {
        "system": dict(linewidth=0.5, color="yellow"),
        "background": dict(linewidth=0.5, color="green"),
        "data": dict(linewidth=0.0, color="red", marker=".", markersize=2.8),
        "default": dict(linewidth=0.5, color="white"),
    }
    ANNOTATION_KWARG = dict(
        bbox=dict(
            boxstyle="round,pad=.5",
            fc="white",
            alpha=1,
            ec="k",
        ),
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="arc3",
            shrinkB=0,
            ec="k",
        ),
    )
    HIGHLIGHT_KWARG = dict(
        color="white",
        markeredgecolor="white",
        linewidth=3,
        markeredgewidth=3,
        facecolor="white",
        edgecolor="white",
    )
    LEGEND_STYLE = dict(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.1),
        facecolor="black",
        ncol=3,
        edgecolor="black",
        labelcolor="white",
    )
    GRAPH_THEME = dict(
        DARK=dict(
            FACE_COLOR="black",
            EDGE_COLOR="black",
            TICK_COLOR="white",
            LABEL_COLOR="white",
            SPINE_COLOR="white",
        ),
        LIGHT=dict(
            FACE_COLOR="white",
            EDGE_COLOR="white",
            TICK_COLOR="black",
            LABEL_COLOR="black",
            SPINE_COLOR="black",
        ),
    )
    WIN_FIGURE_WIDTH = 4
    WIN_FIGURE_HEIGHT = 4
    WIN_FIGURE_DPI = 100
    UNX_FIGURE_WIDTH = 8
    UNX_FIGURE_HEIGHT = 5
    UNX_FIGURE_DPI = 100
    ZOOM_FACTOR = 0.5
    BASE_SCALE = 2

    # GUI settings
    NAME = "GRTK: Data Visualization Software"
    FAVICON = "favicon.ico"
    APP_ID = "DingLab.GRTK"
    WIN_GUI_WIDTH = 1200
    WIN_GUI_HEIGHT = 800
    WIN_SCALE_DIVIDER = 90
    UNX_GUI_WIDTH = 1125
    UNX_GUI_HEIGHT = 800

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
        self.save_button = tkinter.Button(
            self.setting_window, text="Save", command=self.save_setting
        )
        self.save_button.pack(fill="both", expand=1)

    def save_setting(self):
        setting.SPERATOR = self.seperator_setting.get()
        setting.TYPES = eval(self.types_define.get("1.0", tkinter.END))
        self.setting_window.destroy()
