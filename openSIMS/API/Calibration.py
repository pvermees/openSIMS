import numpy as np
import matplotlib.pyplot as plt
from . import Standards, Ellipse

def plot(simplex,show=True,num=None):
    standards = Standards.getStandards(simplex)
    p = simplex.pars
    fig, ax = plt.subplots()
    lines = dict()
    np.random.seed(0)
    for sname, standard in standards.standards.items():
        group = standard.group
        if group in lines.keys():
            colour = lines[group]['colour']
        else:
            lines[group] = dict()
            lines[group]['colour'] = np.random.rand(3,)
            lines[group]['offset'] = standards.offset(standard)
        x, y = standards.calibration_data(standard,p['b'])
        Ellipse.confidence_ellipse(x,y,ax,
                                   alpha=0.25,
                                   facecolor=lines[group]['colour'],
                                   edgecolor='black',
                                   zorder=0)
        ax.scatter(np.mean(x),np.mean(y),s=3,c='black')
    xmin = ax.get_xlim()[0]
    for group, val in lines.items():
        ymin = p['A'] + val['offset'] + p['B'] * xmin
        ax.axline((xmin,ymin),slope=p['B'],color=val['colour'])
    if show:
        plt.show()
    return fig, ax
