import os
import openSIMS as S
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
            line = f.readline()
            if not line:
                break
            else:
                sname = line.replace('\n','').replace('\r','')
                self[sname] = SHRIMP_Sample()
                self[sname].read_op(f)

    def read_pd(self,f):
        while True:
            line = f.readline()
            if not line:
                break
            elif '***' in line:
                header = [f.readline().strip() for _ in range(4)]
                namedate = header[0].split(', ')
                sname = namedate[0].replace('\n','').replace('\r','')
                self[sname] = SHRIMP_Sample()
                self[sname].date = ' '.join(namedate[1:3])
                self[sname].read_pd(f,header)

class SHRIMP_Sample(Sample.Sample):
        
    def __init__(self):
        super().__init__()

    def read_op(self,f):
        self.date = f.readline().strip()
        self.set = int(self.read_numbers(f)[0])
        nscans = int(self.read_numbers(f)[0]) # nscans, not used
        nions = int(self.read_numbers(f)[0])
        self.deadtime = 0
        dd = {'dwelltime': self.read_numbers(f)}
        dd['detector'] = ['COUNTER'] * nions
        dd['dtype'] = ['Em'] * nions
        ions = [f'm{i+1}' for i in range(nions)]
        self.channels = pd.DataFrame(dd,index=ions)
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

    def split_mixed(self,line,i,j):
        chunk = line.split(', ')[i]
        return chunk.split(' ')[j]

    def read_pd(self,f,header):
        self.set = int(self.split_mixed(header[1],0,1))
        nscans = int(self.split_mixed(header[1],1,0))
        nions = int(self.split_mixed(header[1],2,0))
        self.sbmbkg = float(self.split_mixed(header[1],4,2))
        self.deadtime = float(self.split_mixed(header[1],3,0))
        ion_block = [f.readline().strip() for _ in range(nions)]
        ion_table = pd.DataFrame([line.split() for line in ion_block])
        ions = ion_table[0].tolist()
        dd = {'dwelltime': ion_table[3].astype(float).values}
        dd['detector'] = ion_table[10].tolist()
        dd['dtype'] = ['Fc' if det == 'COUNTER' else 'Em' for det in dd['detector']]
        self.channels = pd.DataFrame(dd,index=ions)
        self.time = pd.DataFrame(0,index=np.arange(nscans),columns=ions)
        self.signal = pd.DataFrame(0,index=np.arange(nscans),columns=ions)
        self.sbm = pd.DataFrame(0,index=np.arange(nscans),columns=ions)
        block_data = [f.readline().strip() for _ in range(1 + nscans * nions * 2)][1:]
        for row in range(nscans):
            for col in range(nions):
                ion = ions[col]
                i = row * nions * 2 + col * 2
                time_data = block_data[i].split()
                sbm_data = block_data[i+1].split()
                self.time.loc[row,ion] = float(time_data[2])
                self.signal.loc[row,ion] = sum(map(float,time_data[4:]))
                self.sbm.loc[row,ion] = sum(map(float,sbm_data))

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
        channel = S.get('methods')[method][ion]
        bkg_channel = S.get('methods')[method]['bkg']
        dwelltime = self.channels.loc[channel,'dwelltime']
        raw_cps = self.signal[channel]
        counts = raw_cps*dwelltime
        adjusted_dwelltime = dwelltime - counts*self.deadtime/1e9
        adjusted_cps = counts/adjusted_dwelltime
        blank_cps = self.signal[bkg_channel]
        blank_corrected_cps = adjusted_cps - blank_cps
        return pd.DataFrame({'time': self.time[channel],
                             'cps': blank_corrected_cps})