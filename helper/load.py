class single_line(object):
    def __init__(self, cords: list[tuple[float,float]], file_path: str):
        """single line object is the object for a single file path
        a single file path may contain up to one line
        this object has the lines cordinates in a list of anchor object
        it also has the full file path, drawing preference, seperate cords, etc.

        Args:
            cords (list[load.anchor]): list of anchor objects
            file_path (str): full file path
        """
        # single line cords in anchor object
        self.cord = cords
        self.file_path = file_path
        self.parameters = dict(
            linewidth=0.5,
            color="black",
        )
        # single line xy cords
        self.abs_cords_y = [i[1] for i in cords]
        self.abs_cords_x = [i[0] for i in cords]
        
    def set_parameters(self, new_parameters: dict) -> None:
        self.parameters = new_parameters

def read_file(dir: str) -> single_line:
    """read file from path and build a single_line object

    Args:
        dir (str): full file path

    Returns:
        single_line: single line object reference
    """
    container = []
    with open(dir, "r") as target:
            temp = target.read().splitlines()
            for i in temp:
                container.append((float(i.split(" ")[0]),float(i.split(" ")[1])))
    return single_line(container, dir)
    