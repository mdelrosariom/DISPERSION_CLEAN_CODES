# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 18:10:31 2024

@author: mdrmi
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 22:18:22 2024

@author: mdrmi
"""
import random as rnd

def niche_construction2(species_list, environment_niche_width, island_niche_width, species_niche_width, island_niche_overlap): 
    '''
    This function creates:
    1. The niche of the environment, a sequence of ascending numbers from 1 to a number defined by the environment_niche_width.
    2. The niche of the island,
    3. The niche of each species of the simulation, a subset of the environmental niche with a width specified by species_niche_width.
    4. possibilities of niche overlap, integral number that is the percentage of niche that the island will have
    '''
    niches = []
    niche_mainland = list(range(1, environment_niche_width + 1))
    niches.append(niche_mainland)   
    
    #niche of island 
    portion = int((island_niche_overlap/100)*len(niche_mainland))
    position_ni = rnd.randint(1,2)
    if position_ni ==1: #grab niche_mainland from right 
        niche_island = niche_mainland[len(niche_mainland)-portion:len(niche_mainland)]        
        
    if position_ni ==2:#grab niche_mainland from right 
        niche_island = niche_mainland[:portion]    
    niches.append(niche_island)
    
    for species in species_list:         
        niche_sp_start = rnd.randint(1, environment_niche_width - species_niche_width + 1)
        niche_sp = list(range(niche_sp_start, niche_sp_start + species_niche_width))           
        niches.append(niche_sp)
    return niches
