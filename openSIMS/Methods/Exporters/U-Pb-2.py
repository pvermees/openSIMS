def csv(simplex,path):
    if simplex.hasMethods(['U-Pb']):
        df = simplex.results['U-Pb'].average()
        df.to_csv(path)
    else:
        raise ValueError('Results lacks U-Pb data')

def json(simplex,path):
    pass
