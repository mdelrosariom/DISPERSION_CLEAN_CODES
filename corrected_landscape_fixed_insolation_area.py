# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 17:18:08 2025

@author: mdrmi
"""

import math
import random as rnd 
import numpy as np

def landscape_fixed_insolation_area(nrow, ncol, size, insolation, main):
    '''
    This creates a matrix with 3 values:
    1 represents mainland, generally the half of it in the left side from top to bottom, given by main
    0 represents the sea 
    2 represents the island, which position in the sea is random, but always is at least 2 squares away (easy to change, look at it!) from the mainland. The 
    size of the island can be modified by the size argument. it needs to be a whole number. 
    nrow, ncol and size
    Now fixed insolation 3 possibilities, close, medium, far
    ''' 
    landscape = np.zeros((nrow, ncol))
    landscape[:, 0:main] = 1
    
    min_distance = 2  # Minimum distance from the mainland and edges
   
    dim = math.floor(ncol * size)
    posx = rnd.randint(0, max(0, nrow - dim))
    
    if insolation == "close":
        posy = main + min_distance
    elif insolation == "medium":
        posy = main + min_distance + (ncol - main - min_distance - dim) // 2
    elif insolation == "far":
        posy = ncol - dim - min_distance

    # ensure posy does not go out of bounds
    posy = max(posy, main + min_distance)
    posy = min(posy, ncol - dim - min_distance)

    landscape[posx:posx+dim, posy:posy+dim] = 2

   
    
    return landscape

