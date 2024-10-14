import pandas as pd

def csv(simplex,path):
    averages = []
    for method, results in simplex.results.items():
        averages.append(results.average())
    df = pd.concat(averages,axis=1)
    df.to_csv(path)
