def csv(simplex,path):
    if simplex.hasMethods(['U-Pb']):
        df = simplex.results['U-Pb'].average()
        df.to_csv(path)
    else:
        raise ValueError('Results lacks U-Pb data')

def json(simplex,path):
    pass

def help():
    return "Contains the following columns:\n" + \
        "X=238U/206Pb, s[X], Y=204Pb/206Pb, s[Y], rho[X,Y]."
