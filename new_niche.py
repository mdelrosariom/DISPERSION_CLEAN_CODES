# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 22:54:12 2024

@author: mdrmi
"""
import numpy as np 
import random as rnd

def new_niche(mainland_island, range_niche_island, range_niche_mainland):
    '''
    this functions assignates random resourses to the cells of the landscape. 
    range_niche_mainland number of resources in mainland (will not determine any stablishment). NEEDS TO BE A LIST WITH THE RESOURCES
    range_niche_island number of resources in island (will determine which resourses are in the island)

    '''
    niche_info= np.zeros(mainland_island.shape)   
    nrow, ncol = mainland_island.shape  # Get the shape values directly
    for i in range(nrow):    #rows
        for j in range(ncol): #columns
            if mainland_island[i][j] == 1:
                niche_info[i][j] = rnd.choice(range_niche_mainland)
            if mainland_island[i][j] == 2:            
                niche_info[i][j] = rnd.choice(range_niche_island)
    return niche_info
            