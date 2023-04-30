from matplotlib import lines
import numpy
import pathlib
from bin.set import setting


class single_line(object):
    def __init__(self, curve: str, type: str, file: str, cords: numpy.ndarray, file_path: str):
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
            self.parameters = setting.TYPES[self.curve_type]
        else:
            self.parameters = setting.TYPES["default"]
        self.parameters["label"] = f"{file}@{type}@{curve}"

        # cords
        self.abs_cords_x = numpy.array(cords[0])
        self.abs_cords_y = numpy.array(cords[1])
        self.plt_cords = numpy.array([cords[0], cords[1]])

        # Added by Guanchen @ 4/30/2023
        self.file_path = file_path

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
                # if temp[0] in list(container[short].keys()):
                #     container[short][temp[0]][temp[1]] = read_file_helper(
                #         short, temp, curve_x, curve_y
                #     )
                # else:
                #     container[short][temp[0]] = {
                #         temp[1]: read_file_helper(short, temp, curve_x, curve_y)
                #     }
                container[short][temp[0]][temp[1]] = read_file_helper(short, temp, curve_x, curve_y, dir)
        else:
            temp = all_data.split("\n")
            curve_x = []
            curve_y = []
            # if temp[0] in list(container[short].keys()):
            #     container[short][temp[0]][temp[1]] = read_file_helper(
            #         short, temp, curve_x, curve_y
            #     )
            # else:
            #     container[short][temp[0]] = {
            #         temp[1]: read_file_helper(short, temp, curve_x, curve_y)
            #     }
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
    cords = numpy.array([numpy.array(curve_x), numpy.array(curve_y)])
    single_line_object = single_line(aftersplit[1], aftersplit[0], dir, cords, file_path)
    return single_line_object
