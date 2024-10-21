def csv(simplex,path):
    if simplex.hasMethods(['Th-Pb']):
        df = simplex.results['Th-Pb'].average()
        df.to_csv(path)
    else:
        raise ValueError('Results lacks Th-Pb data')

def json(simplex,path):
    pass

def help():
    return "Contains the following columns:\n" + \
        "X=232Th/208Pb, s[X], Y=204Pb/208Pb, s[Y], rho[X,Y]."
