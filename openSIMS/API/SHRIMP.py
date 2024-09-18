from . import Sample

class SHRIMP_Sample(Sample.Sample):

    def __init__(self):
        super().__init__()
        self.date = None
        self.set = []
        self.sbmbkg = []
        
