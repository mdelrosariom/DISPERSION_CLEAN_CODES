# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 22:18:22 2024

@author: mdrmi
"""
import random as rnd
def niche_construction(species_list, environment_niche_width, island_niche_width, species_niche_width): 
    niches = []
    niche_mainland = list(range(1,environment_niche_width+1)) #(n, b-1)
    niches.append(niche_mainland)
    niche_island = rnd.randint(1, environment_niche_width - island_niche_width + 1)

    niche_island = list(range(niche_island, (niche_island + island_niche_width)))
    niches.append(niche_island)
    for species in range(len(species_list)): 
        niche_sp =  rnd.randint(1,environment_niche_width)
        niche_sp =  list(range(niche_sp, niche_sp+species_niche_width))
        niches.append(niche_sp)
    return(niches)