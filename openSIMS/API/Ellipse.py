# modified from
# https://matplotlib.org/stable/gallery/statistics/confidence_ellipse.html

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transforms as transforms
from matplotlib.patches import Ellipse

# a, b and c are lists of raw data
def acbc2ellipse(a,b,c,sa=None,sb=None,sc=None):
    ma = np.mean(a)
    mb = np.mean(b)
    mc = np.mean(c)
    mx = np.mean(ma/mc)
    my = np.mean(mb/mc)
    cov = np.cov(np.array([a,b,c]))/a.size
    if sa is not None:
        cov[0,0] = sa**2
    if sb is not None:
        cov[1,1] = sb**2
    if sc is not None:
        cov[2,2] = sc**2
    J = np.array([[1/mc,0.0,-ma/mc**2],
                  [0.0,1/mc,-mb/mc**2]])
    E = J @ cov @ np.transpose(J)
    sx = np.sqrt(E[0,0])
    sy = np.sqrt(E[1,1])
    pearson = E[0,1]/(sx*sy)
    return mx, sx, my, sy, pearson

# x and y are lists of logratios
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
    ax.scatter(mean_x,mean_y,s=3,c='black')
    return ax.add_patch(ellipse)
