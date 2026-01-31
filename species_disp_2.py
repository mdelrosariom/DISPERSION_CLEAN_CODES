# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 13:20:44 2024

@author: mdrmi
"""

import random as rnd

def dispersion_species(species_list, main):
    '''
    It assigns the mean of the gaussian function n(m, sd) of the dispersal per species
    main: the portion of the landscape that is mainland. 
    '''
    available_values = list(range(1, main + 1))
    dispersal_all = []
    
    for i in species_list:
        if not available_values:
            # If all values are used up, reset available values
            available_values = list(range(1, main + 1))
        
        dispersal_sp = rnd.choice(available_values)
        available_values.remove(dispersal_sp)
        dispersal_all.append(dispersal_sp)
    
    return dispersal_all