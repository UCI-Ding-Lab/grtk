import tkinter
import tkinter.messagebox

def do_nothing():
    pass

class TestMenu():
    def __init__(self, GUI):
        self.GUI = GUI
        self._init_test_menu()

    def _init_test_menu(self):
        test_menu = tkinter.Menu(self.GUI.menu_bar, tearoff=0)
        # test_menu.add_command(label="Graph", command=self._test_graph)
        # test_menu.add_command(label="Show Cordinate Marker", command=self._enable_cord_marker)
        test_menu.add_command(label="Shift Left", command=do_nothing)
        self.GUI.menu_bar.add_cascade(label="Test", menu=test_menu)

    def _shift_left(self):
        self.GUI.plot.shift_left()
   

if __name__ == '__main__':
    pass
