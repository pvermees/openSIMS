from SIMplex import Sample
import csv

class Cameca_Sample(Sample):

    def __init__(self):
        super().__init__()
        self.x = []
        self.y = []
        self.ions = []
        self.background = []
        self.yld = []

    def read(self,fname):
        with open(fname,'r') as file:
            rows = csv.reader(file,delimiter='\t')
            for row in rows:
                if len(row)>0 and 'X POSITION' in row[0]:
                    self.x = float(row[1])
                    self.y = float(row[3])
                if len(row)>0 and "ACQUISITION PARAMETERS" in row[0]:
                    row = read_block(rows,2)
                    self.ions = row[1:]
                    row = read_block(rows,5)
                    self.dwelltime = map(float,row[1:])
                    self.detector = next(rows)[1:]
                    self.dtype = next(rows)[1:]

def read_block(rows,n=1):
    for _ in range(n-1):
        next(rows)
    return next(rows)

