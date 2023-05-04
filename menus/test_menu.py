import tkinter
import tkinter.messagebox
from bin.db_manager import DBManager
import numpy as np
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
        self.GUI.menu_bar.add_cascade(label="Test", menu=test_menu)

    def _temp(self):
        # print(self.GUI.container.container)
        # for k, v in self.GUI.container.container.items():
        #     print(k)
        # print("++++++++++++++++")
        # for k, v in self.GUI.container.container.items():
        #     print(v)
        # print(self.GUI.container.container['303.gr']['system']['graph 6'])
        
        
        # for i, j in self.GUI.container.container.items():
        #     for r in self.GUI.container.container[i][self.GUI.container.container[i]].items():
        #         print(r)
        
        # temp = []
        # for i in self.GUI.container.container.keys():
        #     for j in self.GUI.container.container[i].keys():
        #         for r in self.GUI.container.container[i][j].keys():
        #             print(self.GUI.container.container[i][j][r].line2d_object[0].get_marker())
        # print(self.GUI.container.get_curves_list())
        
        """
        for i in self.GUI.container.get_curves_list():
            print(len(list(zip(i[-1][0], i[-1][1]))))
        """
        temp = DBManager(self.GUI)
        # temp.load(self.GUI.container, r"Data/Untitled.db")
        
        arr = np.array(temp.fetch_coords(r"Data/Untitled.db", \
            r'C:/Work/Ding Lab/GitRepo/grtk/(Multi-layer)FRD/303.gr', \
            'system', 'graph 1'))
        print(arr[:,0].shape)
        
        #             temp.append([i, j, r, \
        #                 self.GUI.container.container[i][j][r].plt_cords])
        # print(temp)
                    # print(i, j, r)
                    # print(self.GUI.container.container[i][j][r].plt_cords)
                    # return None
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