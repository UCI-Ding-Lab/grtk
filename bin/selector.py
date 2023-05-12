from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import numpy as np
from helper import load

# typecheck
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main

class lasso(object):
    """lasso selector object

    Args:
        object (object): grtk modules
    """
    # ref: https://matplotlib.org/stable/gallery/widgets/lasso_selector_demo_sgskip.html
    
    # indicator preference
    PREF = dict(
        color="#F6CEFC",
        linewidth=1.5,
        linestyle="-",
        visible=True,
    )
    
    # generater preference
    TYPE = "Lasso Results"
    FILE = "untitled"
    CURVE = 0
    
    def __init__(self, GUI: "main.GUI"):
        self.GUI = GUI
        self.path = None
    
    def start(self):
        """start lasso
        """
        self.LS = LassoSelector(self.GUI.container.matplot_subplot, self.onselect, props=lasso.PREF, useblit=False)
        self.GUI.container._refresh_canvas()
    
    def stop(self):
        """disconnect lasso
        """
        self.path = None
        self.LS.disconnect_events()
        self.GUI.container._refresh_canvas()
    
    def onselect(self, verts):
        """covert selected region to matplotlib.path(space) and store it

        Args:
            verts (unknown): selection summary
        """
        # make space
        # matplotlib.path.Path
        # doc: https://matplotlib.org/stable/api/path_api.html
        self.path = Path(verts)
    
    def delete_selected(self):
        """delete selected region on selected layer
        """
        selected_layer = self.GUI.pref.tree.selection()[0].split("@")
        
        # err if not selected curce & region
        if len(selected_layer) != 3:
            print("Select a curve to delete")
            return
        if self.path is None:
            print("Select a region to delete")
            return
        
        # find in container
        t = selected_layer[0]
        f = selected_layer[1]
        c = selected_layer[2]
        curv: "load.single_line" = self.GUI.container.container[f][t][c]
        curv_raw_data = curv.plt_cords_T
        
        # generate index
        selected_pts_index = np.nonzero(self.path.contains_points(curv_raw_data))[0]
        new_raw_data = np.delete(curv_raw_data, selected_pts_index, axis=0)
        
        # save
        self.GUI.container.container[f][t][c].plt_cords = new_raw_data.transpose()
        self.GUI.container.container[f][t][c].plt_cords_T = new_raw_data
        self.GUI.container.container[f][t][c].abs_cords_x = new_raw_data[0]
        self.GUI.container.container[f][t][c].abs_cords_y = new_raw_data[1]
        self.GUI.container.container[f][t][c].line2d_object[0].set_data(new_raw_data.transpose())
        self.GUI.container._refresh_canvas()
    
    def copy_selected(self):
        """copy selected and put it in a new layer
        """
        selected_layer = self.GUI.pref.tree.selection()[0].split("@")
        
        # err if not selected curce & region
        if len(selected_layer) != 3:
            print("Select a curve to copy")
            return
        if self.path is None:
            print("Select a region to copy")
            return
        
        # find in container
        t = selected_layer[0]
        f = selected_layer[1]
        c = selected_layer[2]
        curv: "load.single_line" = self.GUI.container.container[f][t][c]
        curv_raw_data = curv.plt_cords_T
        
        # generate index
        selected_pts_index = np.nonzero(self.path.contains_points(curv_raw_data))[0]
        new_raw_data = curv_raw_data[selected_pts_index, :]
        
        # save
        self.save_obj(raw=new_raw_data.transpose())
        self.GUI.container._refresh_canvas()
        
    
    def save_obj(self, raw):
        target: load.single_line = load.single_line(
            file=lasso.FILE,
            curve=str(lasso.CURVE),
            type=lasso.TYPE,
            cords=np.array(raw)
        )
        lasso.CURVE += 1
        self.GUI.container.load_and_plot_obj(target=target)