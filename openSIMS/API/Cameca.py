import openSIMS as S
import pandas as pd
import csv
import os
import datetime
from . import Sample, Toolbox

class Cameca_Sample(Sample.Sample):

    def __init__(self):
        super().__init__()
        self.x = []
        self.y = []

    def read(self,fname):
        with open(fname,'r') as file:
            rows = csv.reader(file,delimiter='\t')
            for row in rows:
                if len(row)<1:
                    pass
                elif 'CAMECA' in row[0]:
                    datestring = row[1]
                    timestring = clean_list(next(rows))[0]
                    dt = Toolbox.get_date(datestring)
                    tm = Toolbox.get_time(timestring)
                    self.date = datetime.datetime.combine(dt,tm)
                elif 'X POSITION' in row[0]:
                    self.x = float(row[1])
                    self.y = float(row[3])
                elif 'ACQUISITION PARAMETERS' in row[0]:
                    row = skip_block(rows,2)
                    ions = clean_list(row[1:])
                    self.signal = pd.DataFrame(columns=ions)
                    self.sbm = pd.DataFrame(columns=ions)
                    self.time = pd.DataFrame(columns=ions)
                    row = skip_block(rows,5)
                    dd = {'dwelltime': string2float(row[1:])}
                    row = skip_block(rows,5)
                    dd['detector'] = clean_list(row[1:])
                    dd['dtype'] = clean_list(next(rows)[1:])
                    self.channels = pd.DataFrame(dd,index=ions)
                elif 'DETECTOR PARAMETERS' in row[0]:
                    row = clean_list(skip_block(rows,4))
                    detector = []
                    dd = {'yield': [], 'bkg': [], 'deadtime': []}
                    while len(row)>1:
                        detector.append(row[0])
                        values = string2float(row[1:])
                        dd['yield'].append(values[0])
                        dd['bkg'].append(values[1])
                        dd['deadtime'].append(values[2])
                        row = clean_list(next(rows))
                    self.detector = pd.DataFrame(dd,index=detector)
                elif 'RAW DATA' in row[0]:
                    skip_block(rows,5)
                    read_asc_block(self.signal,rows)
                elif 'PRIMARY INTENSITY' in row[0]:
                    skip_block(rows,5)
                    read_asc_block(self.sbm,rows)
                elif 'TIMING' in row[0]:
                    skip_block(rows,5)
                    read_asc_block(self.time,rows)
                else:
                    pass

    def cps(self,ion):
        channel = S.get('channels')[ion]
        detector = self.channels.loc[channel,'detector']
        dwelltime = self.channels.loc[channel,'dwelltime']
        deadtime = self.detector.loc[detector,'deadtime']
        raw_cps = self.signal[channel]
        counts = raw_cps*dwelltime
        adjusted_dwelltime = dwelltime - counts*deadtime/1e9
        adjusted_cps = counts/adjusted_dwelltime
        blank_cps = self.detector.loc[detector,'bkg']
        blank_corrected_cps = adjusted_cps - blank_cps
        return pd.DataFrame({'time': self.time[channel],
                             'cps': blank_corrected_cps})

def skip_block(rows,n=1):
    for _ in range(n-1):
        next(rows)
    return next(rows)

def read_asc_block(df,rows):
    while True:
        row = next(rows)
        if len(row)>0:
            df.loc[len(df)] = string2float(row[2:])
        else:
            break

# removes leading and trailing spaces from list of strings
def clean_list(row):
    return [item.strip() for item in row if item.strip()]

# cleans list of strings and converts it to a list of floats
def string2float(lst):
    values = [float(i) for i in clean_list(lst)]
    return values
