from matplotlib import lines
import numpy
import pathlib

class single_line(object):
    def __init__(self, name: str, cords: list[list[float]]):
        """single line object is the object for a single file path
        a single file path may contain up to one line
        this object has the lines cordinates in a list of anchor object
        it also has the full file path, drawing preference, seperate cords, etc.

        Args:
            cords (list[load.anchor]): list of anchor objects
            file_path (str): full file path
        """
        # nick stands for filename with extension
        self.nick = name
        
        # matplotlib line2d object
        # the reason why it is a list is because line2d object need to be passed by reference
        # and it is not possible to pass by reference in python by assigning a variable
        # so we need to use a list to store the line2d object
        # usage: self.line2d_object[0] to get the line2d object
        self.line2d_object: list[lines.Line2D] = []
        
        # drawing preference
        self.curve_type = name.split(" ")[1]
        if self.curve_type == "system":
            self.parameters = dict(
                linewidth=0.5,
                color="yellow",
                label=self.nick,
            )
        elif self.curve_type == "background":
            self.parameters = dict(
                linewidth=0.5,
                color="green",
                label=self.nick,
            )
        elif self.curve_type == "data":
            self.parameters = dict(
                linewidth=0.0,
                color="red",
                label=self.nick,
                marker=".",
                markersize=2.8,
            )
        else:
            self.parameters = dict(
                linewidth=0.5,
                color="white",
                label=self.nick,
            )
        
        # cords
        self.abs_cords_x = cords[0]
        self.abs_cords_y = cords[1]
        

def read_file(dir: str) -> dict[str,list[list[float]]]:
    """read file from path and build a single_line object

    Args:
        dir (str): full file path

    Returns:
        single_line: single line object reference
    """
    SEPERATOR = "\n----------\n"
    with open(dir, "r") as target:
        all_data = target.read()
        while all_data[-1:] == "\n":
            all_data = all_data[:-1]
        layers_data = dict()
        if SEPERATOR in all_data:
            layers_raw = all_data.split("\n----------\n")
            for i in layers_raw:
                temp = i.split("\n")
                curve_x = []
                curve_y = []
                layers_data[f"{pathlib.Path(dir).name} {temp[0]}"] = read_file_helper(temp, curve_x, curve_y)
        else:
            temp = all_data.split("\n")
            curve_x = []
            curve_y = []
            layers_data[f"{pathlib.Path(dir).name} {temp[0]}"] = read_file_helper(temp, curve_x, curve_y)
        return layers_data

def read_file_helper(aftersplit: list[str], curve_x: list[float], curve_y: list[float]) -> list[list[float]]:
    if " " in aftersplit[1]:
        for o in aftersplit[1:]:
            curve_x.append(float(o.split(" ")[0]))
            curve_y.append(float(o.split(" ")[1]))
    else:
        for index, val in enumerate(aftersplit[1:]):
            curve_x.append(float(index))
            curve_y.append(float(val))
    cords = [curve_x, curve_y]
    return cords
    
    