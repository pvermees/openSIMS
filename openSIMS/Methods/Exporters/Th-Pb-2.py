def csv(simplex,path):
    if simplex.hasMethods(['Th-Pb']):
        df = simplex.results['Th-Pb'].average()
        df.to_csv(path)
    else:
        raise ValueError('Results lacks Th-Pb data')

def json(simplex,path):
    pass
