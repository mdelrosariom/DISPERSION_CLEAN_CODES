# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 15:20:03 2024

@author: mdrmi
"""
import math
import random as rnd 
import numpy as np
def simple_landscape(nrow, ncol, size, shape): #size can it be 0.1, 0.2, 0. 3, 0.4, at least in 20x20, 50x50. in bigger can be larger
    landscape = np.zeros((nrow, ncol))
    landscape[:, 0:ncol//2] = 1
    if shape == 0: #island is a square
        dim = math.floor(ncol * size)
        posx = rnd.randint(0, nrow - dim)
        posy = rnd.randint(ncol // 2 + 2, ncol - dim)
        landscape[posx:posx+dim, posy:posy+dim] = 2
        
    elif shape == 1:  # island is a rectangle (more high than wide)
        dimx = math.floor(ncol * size)
        dimy = dimx // 2
        posx = abs(rnd.randint(0, nrow - dimx))
        posy = abs(rnd.randint(ncol // 2 + 2, nrow - dimy))
        landscape[posx:posx+dimx, posy:posy+dimy] = 2
    return landscape
