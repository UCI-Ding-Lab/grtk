class load_error(Exception):
    print("Error loading file")

class anchor(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class read_gr_file(object):
    def __init__(self):
        self.container = []
    
    def read_file(self, dir):
        try:
            with open(dir, "r") as target:
                temp = target.read().splitlines()
                for i in temp:
                    self.container.append(anchor(x=i.split(" ")[0], y=i.split(" ")[1]))
        except:
            raise load_error