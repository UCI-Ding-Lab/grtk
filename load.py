class read_gr_file(object):
    def __init__(self):
        self.container = []
    
    def read_file(self, dir):
        self.container = []
        with open(dir, "r") as target:
            temp = target.read().splitlines()
            for i in temp:
                self.container.append(float(i.split(" ")[1]))
    
    def get_result(self):
        return self.container