from SIMplex import Sample

class Cameca_Sample(Sample):

    def __init__(self):
        super().__init__()
        self.background = []
        self.x = []
        self.y = []
        self.yld = []
