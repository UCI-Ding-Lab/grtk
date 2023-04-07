from matplotlib import lines
import pathlib

class single_line(object):
    def __init__(self, cords: list[tuple[float,float]], file_path: str, x: list[float], y: list[float]):
        """single line object is the object for a single file path
        a single file path may contain up to one line
        this object has the lines cordinates in a list of anchor object
        it also has the full file path, drawing preference, seperate cords, etc.

        Args:
            cords (list[load.anchor]): list of anchor objects
            file_path (str): full file path
        """
        # nick stands for filename with extension
        self.nick = pathlib.Path(file_path).name
        
        # matplotlib line2d object
        # the reason why it is a list is because line2d object need to be passed by reference
        # and it is not possible to pass by reference in python by assigning a variable
        # so we need to use a list to store the line2d object
        # usage: self.line2d_object[0] to get the line2d object
        self.line2d_object: list[lines.Line2D] = []
        
        # drawing preference
        self.parameters = dict(
            linewidth=0.5,
            color="white",
            label=self.nick,
        )
        
        # cords
        self.cord = cords
        self.abs_cords_y = y
        self.abs_cords_x = x

def read_file(dir: str) -> single_line:
    """read file from path and build a single_line object

    Args:
        dir (str): full file path

    Returns:
        single_line: single line object reference
    """
    container = []
    x = []
    y = []
    with open(dir, "r") as target:
            temp = target.read().splitlines()
            for i in temp:
                container.append((float(i.split(" ")[0]),float(i.split(" ")[1])))
                x.append(float(i.split(" ")[0]))
                y.append(float(i.split(" ")[1]))
    return single_line(container, dir, x, y)
    