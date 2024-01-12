import tkinter
import tkinter.messagebox
from bin.db_manager import DBManager
import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main
    import custom
    
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
        test_menu.add_command(label="clear recent file", command=self._clear_recent_file)
        test_menu.add_command(label="show temp", command=self._temp)
        test_menu.add_command(label="list opt child", command=self._radom)
        self.GUI.menu_bar.add_cascade(label="Test", menu=test_menu)
    
    def _radom(self):
        i:  custom.labCustom = self.GUI.custom
        print(i.CURVE)

    def _temp(self):

        
        """
        for i in self.GUI.container.get_curves_list():
            print(len(list(zip(i[-1][0], i[-1][1]))))
        """

        for i in self.GUI.container.get_curves_list():
            print(i)
        # print(self.GUI.container.get_curves_list()[0][11])
        # print(len(self.GUI.container.get_curves_list()[0][11]))

        return None

    def _clear_recent_file(self):
        file_path = r"data/recent_paths.txt"
        file = open(file_path, "w")
        file.write('')
        file.close()

    def _shift_left(self):
        self.GUI.plot.shift_left()
   

if __name__ == '__main__':
    pass
# defaultdict(<function line_container.__init__.<locals>.<lambda> at 0x000001BB3DCA74C0>, {'303.gr': 
#     defaultdict(<class 'dict'>, {'system': {'graph 1': <helper.load.single_line object at 0x000001BB3FAD0DC0>}, 'background': {'graph 1': <helper.load.single_line object at 0x000001BB3FAD9DF0>}, 'data': {'graph 6': <helper.load.single_line object at 0x000001BB3FAD99D0>}})})