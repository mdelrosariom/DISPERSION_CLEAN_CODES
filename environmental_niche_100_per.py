# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 15:03:00 2025
@author: mdrmi
"""

import numpy as np
import random as rnd

def niche_construction(mainland_island): 
    ''' 
    construct a dataframe with the same dimentions as mainland island and different resources. 
    island has a subset of resources of the mainland
    now island_resources 50% of the mainland

    adjusted to Ramiadantsoa et al. 2018: 
    each cell will be represented by the resource and a value of q [0,1)
    its discrete from 0 to 1
    '''    
    mainland_resources = list(range(1,100)) #resources present in mainland
    island_resources = rnd.sample(mainland_resources, 50) #resources present island. now random number
    environmental_niche = mainland_island.copy().astype(float) #copy mainland island
    ques = mainland_island.copy().astype(float)
    environmental_niche[environmental_niche == 0] = np.nan #replace 0 values for NA values (sea)
    ques[ques == 0] = np.nan 
    for i in range(environmental_niche.shape[0]): 
        for j in range(environmental_niche.shape[1]): 
            if environmental_niche[i, j] == 1: #mainland              
                environmental_niche[i, j] = rnd.choice(mainland_resources)          
                q = rnd.uniform(0, 0.9)
                q = round(q,1)
                ques[i,j] = q
            if environmental_niche[i, j] == 2: #island   
                environmental_niche[i, j] = rnd.choice(island_resources)
                q = rnd.uniform(0, 0.9)
                q = round(q,1)
                ques[i,j] = q

    return environmental_niche, island_resources, mainland_resources, ques
    