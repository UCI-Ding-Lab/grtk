# typecheck
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import main


class KeyboardEvents:
    def __init__(self, GUI: "main.GUI"):
        self.GUI = GUI
        self.GUI.root.bind("<Up>", self._keypress_up)
        self.GUI.root.bind("<Down>", self._keypress_down)
        self.GUI.root.bind("<Left>", self._keypress_left)
        self.GUI.root.bind("<Right>", self._keypress_right)

    def _keypress_up(self, event):
        self.GUI.container.view_zoom_out()

    def _keypress_down(self, event):
        self.GUI.container.view_zoom_in()

    def _keypress_left(self, event):
        self.GUI.container.view_shift_left()

    def _keypress_right(self, event):
        self.GUI.container.view_shift_right()
