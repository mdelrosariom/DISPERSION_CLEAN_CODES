# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 22:43:03 2024

@author: mdrmi
"""
import math
import random as rnd 
import numpy as np
def landscape_fixed_insolation_area(nrow, ncol, size, shape, insolation): #size can it be 0.1, 0.2, 0. 3, 0.4, at least in 20x20, 50x50. in bigger can be larger
    '''
this creates a matrix 3 values 
1 represents mainland, generally the half of it in the lef side from top to bottom, given by mean or ncol//2
0 represents the sea 
2 represents the island, which position in the sea is ramdom, but always is at least 2 squares away from the island. The 
size of the island can be modified by the size argument. The shape can be a square (shape ==0) or a rectangle (shape ==1)
fixed area (always)

now fixed insolation 3 possibilities, close, medium, far

''' 
    landscape = np.zeros((nrow, ncol))
    landscape[:, 0:ncol//2] = 1
    if shape == 0: #island is a square
        dim = math.floor(ncol * size)
        posx = rnd.randint(0, nrow - dim)
        
        if insolation == "close": 
            posy = ncol//2 +  (ncol//2-dim)//3
            if posy == ncol//2: 
                posy = ncol//2 + 2
            
        if insolation == "medium": 
            posy = ncol//2 + 2*(ncol//2-dim)//3         
        if insolation== "far":                    
            posy = ncol//2 +  3*(ncol//2-dim)//3 
        landscape[posx:posx+dim, posy:posy+dim] = 2
        
    elif shape == 1:  # island is a rectangle (more high than wide)
        dimx = math.floor(ncol * size)
        dimy = dimx // 2
        posx = abs(rnd.randint(0, nrow - dimx))  
        
        if insolation == "close": 
            posy = ncol//2 +  (ncol//2-dimy)//3
            if posy == ncol//2: 
                posy = ncol//2 +2
        if insolation == "medium": 
            posy = ncol//2 + 2*(ncol//2-dimy)//3         
        if insolation== "far":                    
            posy = ncol//2 +  3*(ncol//2-dimy)//3 
        
        landscape[posx:posx+dimx, posy:posy+dimy] = 2
    return landscape