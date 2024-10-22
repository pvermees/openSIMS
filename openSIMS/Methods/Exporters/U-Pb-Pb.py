import pandas as pd

def csv(simplex,path):
    if not simplex.hasMethods(['U-Pb']):
        raise ValueError('Results lacks U-Pb data')
    elif not simplex.hasMethods(['Pb-Pb']):
        raise ValueError('Results lacks Pb-Pb data')
    else:
        UPb = simplex.results['U-Pb'].average()
        PbPb = simplex.results['Pb-Pb'].average()
        df = pd.DataFrame({'Y=U238/Pb206':UPb['U238/Pb206'],
                           's[Y]':UPb['s[U238/Pb206]'],
                           'X=Pb207/Pb206':PbPb['Pb207/Pb206'],
                           's[X]':PbPb['s[Pb207/Pb206]'],
                           'Z=Pb204/Pb206':PbPb['Pb204/Pb206'],
                           's[Z]':PbPb['s[Pb204/Pb206]'],
                           'rho[X,Y]':[0.0]*UPb.shape[0],
                           'rho[X,Z]':UPb['rho[U238/Pb206,Pb204/Pb206]'],
                           'rho[Y,Z]':PbPb['rho[Pb204/Pb206,Pb207/Pb206]']})
        df.to_csv(path)

def json(simplex,path):
    pass

def help():
    return "Contains the following columns:\n" + \
        "X=238U/206Pb, s[X], Y=207Pb/206Pb, s[Y], " + \
        "Z=204Pb/206Pb, s[Z], rho[X,Y], rho[X,Z], rho[Y,Z]."
