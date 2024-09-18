import pkgutil
import io
import pandas as pd

def get_table(setting):
    if setting in ['O','S','U-Pb']:
        fname = 'aux/' + setting + '.csv'
    else:
        raise ValueError('Invalid setting.')
    return load_settings(fname)

def get(setting,refmat):
    df = get_table(setting)
    out = df.loc[df['standard'] == refmat]
    return out.iloc[0][1:]

def load_settings(fname):
    data = pkgutil.get_data(__name__,fname)
    csv_data = io.StringIO(data.decode('utf-8'))
    return pd.read_csv(csv_data)
