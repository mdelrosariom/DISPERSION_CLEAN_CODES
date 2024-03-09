# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 22:54:12 2024

@author: mdrmi
"""
import numpy as np 
import random as rnd

def niche(mainland_island, niche_island, niche_mainland):
    en_niche = np.zeros(mainland_island.shape)
    en_niche = [[[item] for item in row] for row in en_niche] 
    niche_of_island =  rnd.randint(1,9)  
    for i in range(len(en_niche)):    
        for j in range(len(en_niche)): 
            if mainland_island[i][j] == 1:
                en_niche[i][j] = niche_mainland #complete niches only 4 availables
            if mainland_island[i][j] == 2:            
                en_niche[i][j] = niche_island 
    return en_niche
            