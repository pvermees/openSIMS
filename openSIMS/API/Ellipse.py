# modified from
# https://matplotlib.org/stable/gallery/statistics/confidence_ellipse.html

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transforms as transforms
from matplotlib.patches import Ellipse

# x, y and z are lists of raw data
def xzyz2ellipse(x,y,z,sx=None,sy=None,sz=None):
    mx = np.mean(x)
    my = np.mean(y)
    mz = np.mean(z)
    mxz = np.mean(mx/mz)
    myz = np.mean(my/mz)
    cov = np.cov(np.array([x,y,z]))/x.size
    if sx is not None:
        cov[0,0] = sx**2
    if sy is not None:
        cov[1,1] = sy**2
    if sz is not None:
        cov[2,2] = sz**2
    J = np.array([[1/mz,0.0,-mx/mz**2],
                  [0.0,1/mz,-my/mz**2]])
    E = J @ cov @ np.transpose(J)
    sxz = np.sqrt(E[0,0])
    syz = np.sqrt(E[1,1])
    pearson = E[0,1]/(sxz*syz)
    return mxz, sxz, myz, syz, pearson

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
