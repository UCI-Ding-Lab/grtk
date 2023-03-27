import tkinter


# typecheck
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main
    import data_plot_new

def check_current_status(GUI: "main.GUI", dir: str, status: dict[str,tkinter.IntVar]) -> None:
    all_lines: "data_plot_new.line_container" = GUI.container
    for i in all_lines.container:
        if i.file_path == dir:
            status["show"].set(1)
            return None
    status["show"].set(0)

def confirm_button_action(pop_up: tkinter.Toplevel, status: dict[str,tkinter.IntVar], status_be4_edit: dict[str,tkinter.IntVar], GUI: "main.GUI", dir: str) -> None:
    for key, val in status.items():
        if status_be4_edit[key] != val.get():
            if key == "show":
                GUI.layer_ctl.hide_on_graph(dir) if val.get() == 0 else GUI.layer_ctl.show_on_graph(dir)
    pop_up.destroy()
    pop_up.update()

def pop_up(GUI: "main.GUI", dir: str):
    pop_up = tkinter.Toplevel(GUI.root)
    pop_up.geometry("750x250")
    pop_up.title("Edit Preference")
    tkinter.Label(pop_up, text=f"Currently editing: {dir}").pack()
    status: dict[str,tkinter.IntVar] = dict()
    status["show"] = tkinter.IntVar()
    check_current_status(GUI, dir, status)
    status_be4_edit = dict()
    for key, val in status.items():
        status_be4_edit[key] = val.get()
    tkinter.Checkbutton(pop_up, text="Show", variable=status["show"]).pack()
    tkinter.Button(pop_up, text="Color", command=lambda: GUI.layer_ctl.change_color(dir)).pack()
    tkinter.Button(pop_up, text="Save", command=lambda: confirm_button_action(pop_up, status, status_be4_edit, GUI, dir)).pack()