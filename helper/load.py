from matplotlib import lines
import numpy as np
import pathlib
from bin.set import setting
# from bin.db_manager import DBManager
from bin.save_manager import SaveManager
import os
import copy
import random
import colorsys

class single_line(object):
    def __init__(self, curve: str, type: str, file: str, cords: np.ndarray, file_path: str=None):
        """single line object is the object for a single file path
        a single file path may contain up to one line
        this object has the lines cordinates in a list of anchor object
        it also has the full file path, drawing preference, seperate cords, etc.

        Args:
            cords (list[load.anchor]): list of anchor objects
            file_path (str): full file path
        """
        # nick stands for filename with extension
        self.nick = curve
        self.curve_type = type
        self.parent = file

        # matplotlib line2d object
        # the reason why it is a list is because line2d object need to be passed by reference
        # and it is not possible to pass by reference in python by assigning a variable
        # so we need to use a list to store the line2d object
        # usage: self.line2d_object[0] to get the line2d object
        self.line2d_object: list[lines.Line2D] = []

        # drawing preference
        if self.curve_type in list(setting.TYPES.keys()):
            self.parameters = setting.TYPES[self.curve_type].copy()
        else:
            self.parameters = dict(linewidth=0.5,color="white")
        self.parameters["label"] = f"{file}@{type}@{curve}"
        
        if self.curve_type == "data":
            h = random.randint(0, 360)/360
            s = 1
            l = 0.5
            color_str = colorsys.hls_to_rgb(h, l, s)
            self.parameters['color'] = color_str

        # seperate xy
        # shape: (n,)
        self.abs_cords_x = np.array(cords[0])
        self.abs_cords_y = np.array(cords[1])
        
        # together xy
        # shape: (2, n)
        self.plt_cords = np.array([cords[0], cords[1]])
        # shape: (n, 2)
        self.plt_cords_T = self.plt_cords.transpose()

        # Added by Guanchen @ 4/30/2023
        self.file_path = file_path
        
        # A string showing on the hovertip describing the computation of the curve \
        # if the curve is not native to the lab data.
        self.tip = "native"

def read_file(dir: str, container) -> None:
    """read file from path and build a single_line object

    Args:
        dir (str): full file path

    Returns:
        single_line: single line object reference
    """
    SEPERATOR = "\n" + setting.SPERATOR + "\n"
    short = pathlib.Path(dir).name
    with open(dir, "r") as target:
        all_data = target.read()
        while all_data[-1:] == "\n":
            all_data = all_data[:-1]
        if SEPERATOR in all_data:
            layers_raw = all_data.split(SEPERATOR)
            for i in layers_raw:
                temp = i.split("\n")
                curve_x = []
                curve_y = []
                container[short][temp[0]][temp[1]] = read_file_helper(short, temp, curve_x, curve_y, dir)
        else:
            temp = all_data.split("\n")
            curve_x = []
            curve_y = []
            container[short][temp[0]][temp[1]] = read_file_helper(short, temp, curve_x, curve_y, dir)


def read_file_helper(
    dir: str, aftersplit: list[str], curve_x: list[float], curve_y: list[float], file_path: str
) -> single_line:
    if " " in aftersplit[2]:
        for o in aftersplit[2:]:
            curve_x.append(float(o.split(" ")[0]))
            curve_y.append(float(o.split(" ")[1]))
    else:
        for index, val in enumerate(aftersplit[2:]):
            curve_x.append(float(index))
            curve_y.append(float(val))
    cords = np.array([np.array(curve_x), np.array(curve_y)])
    single_line_object = single_line(aftersplit[1], aftersplit[0], dir, cords, file_path)
    return single_line_object

def read_txt(dir: str, container) -> None:
    """load db from path dir and build container

    Args:
        dir (str): directory of db.
        container (line_container): container of single_line objects.
    """
    # SEPERATOR = "\n" + setting.SPERATOR + "\n"
    # short = pathlib.Path(dir).name
    # dm = DBManager()
    sm = SaveManager()
    # curves = dm.fetch_curves(dir)
    prefs, coords = sm.fetch_curves(dir)
    # for i in curves:
    #     print(i[1])
    # return
    key_list = []
    short = None
    for i, c in list(zip(prefs, coords)):
        processed_coords = np.array(c)
        # print(i[0])
        if i[0] == 'untitled':
            short = 'untitled' # For operations
        else:
            short = pathlib.Path(i[0]).name
        # short_list.append(short)
        # coords = dm.fetch_coords(dir, i[0], i[1], i[2])
        # print(short, dir, i[0], i[1], i[2])
        if short not in container:
            container[short] = {}
        if i[1] not in container[short]:
            container[short][i[1]] = {}
        if i[2] not in container[short][i[1]]:
            container[short][i[1]][i[2]] = None
        # coords = np.array(dm.fetch_coords(dir, i[0], i[1], i[2]))
        # temp_line = single_line(i[2], i[1], short, \
        #     np.array([coords[:, 0], coords[:, 1]]), i[0])
        # print(c[0])
        container[short][i[1]][i[2]] = single_line(i[2], i[1], short, \
            np.array([processed_coords[:, 0], processed_coords[:, 1]]), i[0])#copy.copy(temp_line)
        temp_line = None
        # print(container[short][i[1]][i[2]].parameters["label"])
        key_list.append([short, i[1], i[2]])
        pref_params = dict(\
            visible= i[3], \
            color= i[4], \
            linewidth= i[5], \
            marker= i[6], \
            markersize= i[7], \
            markerfacecolor= i[8], \
            markeredgecolor= i[9]
        )
        container[short][i[1]][i[2]].parameters.update(pref_params)
        # print(container[short][i[1]][i[2]].parameters["label"])
    # for st, ky, i2 in key_list:
    #     # # print(short, key, i2)
    #     # l = self.container[short][key][i2]
    #     # # print(l.parameters["label"])
    #     # main_l, = self.matplot_subplot.plot(*l.plt_cords, **l.parameters)
    #     # l.line2d_object.append(main_l)
    #     # # l = None
    #     print(container[st][ky][i2].parameters["label"])
    # print("done")
    return key_list
            

            
        
    # coords = dm.fetch_coords(dir)