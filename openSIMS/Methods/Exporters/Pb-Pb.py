def csv(simplex,path):
    if simplex.hasMethods(['Pb-Pb']):
        df = simplex.results['Pb-Pb'].average()
        df.to_csv(path)
    else:
        raise ValueError('Results lacks Pb-Pb data')

def json(simplex,path):
    pass

def help():
    return "Contains the following columns:\n" + \
        "X=204Pb/206Pb, s[X], Y=207Pb/206Pb, s[Y], rho[X,Y]."
