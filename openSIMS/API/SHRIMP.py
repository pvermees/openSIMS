import os
import pandas as pd
import numpy as np
from . import Sample

class SHRIMP_run(pd.Series):

    def __init__(self):
        super().__init__()

    def read(self,fname):
        ext = os.path.splitext(fname)
        with open(fname,'r') as f:
            if ext[1] == '.op':
                self.read_op(f)
            elif ext[1] == '.pd':
                self.read_pd(f)
            else:
                raise ValueError('Invalid file type.')

    def read_op(self,f):
        while True:
            line = f.readline().strip()
            if not line:
                break
            else:
                sname = line
                self[sname] = SHRIMP_sample()
                self[sname].read_op(f)
    
class SHRIMP_sample(Sample.Sample):
        
    def __init__(self):
        super().__init__()

    def read_op(self,f):
        self.date = f.readline().strip()
        self.set = int(self.read_numbers(f)[0])
        nscans = int(self.read_numbers(f)[0]) # nscans, not used
        nions = int(self.read_numbers(f)[0])
        self.deadtime = 0
        self.dwelltime = self.read_numbers(f)
        ions = [f'm{i+1}' for i in range(nions)]
        self.detector = ['COUNTER'] * nions
        self.dtype = ['Em'] * nions
        self.time = pd.DataFrame(0,index=np.arange(nscans),columns=ions)
        for ion in ions:
            self.time[ion] = self.read_numbers(f)
        self.signal = pd.DataFrame(0,index=np.arange(nscans),columns=ions)
        for ion in ions:
            self.signal[ion] = self.read_numbers(f)
        self.sbmbkg = self.read_numbers(f)[0]
        self.sbm = pd.DataFrame(0,index=np.arange(nscans),columns=ions)
        for ion in ions:
            self.sbm[ion] = self.read_numbers(f)
        _ = f.readline().strip() # empty line

    def parse_line(self,line,remove=None):
        parsed = [elem.strip() for elem in line.split('\t')]
        if remove is None:
            out = parsed
        else:
            out = [parsed[i] for i in range(len(parsed)) if i not in remove]
        return out
    
    def read_text(self,f,remove=None):
        line = f.readline().strip()
        return self.parse_line(line, remove=remove)

    def read_numbers(self,f,remove=None):
        parsed = self.read_text(f,remove=remove)
        return [float(x) for x in parsed]
    
    def cps(self,method,ion):
        pass