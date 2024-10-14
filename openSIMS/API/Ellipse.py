# modified from
# https://matplotlib.org/stable/gallery/statistics/confidence_ellipse.html

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transforms as transforms
from matplotlib.patches import Ellipse

def xy2ellipse(x, y,
               ax, n_std=1.0, facecolor='none', **kwargs):
    cov = np.cov(x,y) / x.size
    sx = np.sqrt(cov[0,0])
    sy = np.sqrt(cov[1,1])
    pearson = cov[0,1]/(sx*sy)
    return result2ellipse(np.mean(x),sx,np.mean(y),sy,pearson,ax,
                          n_std=n_std,facecolor=facecolor,**kwargs)

def result2ellipse(mean_x, sx, mean_y, sy, pearson,
                   ax, n_std=1.0, facecolor='none', **kwargs):
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)
    scale_x = sx * n_std
    scale_y = sy * n_std
    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)
    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)
