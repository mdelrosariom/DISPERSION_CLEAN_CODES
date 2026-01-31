# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 16:22:00 2025

@author: mdrmi
"""
import random as rnd
import numpy as np

def species_niche(sps_list, environmental_niche, len_res_gen=10, len_res_esp=5): 
    '''
    Creates niches of the species in a community. 
    50% of species are generalists, 50% especialists.
    resources of generalists 10. now option to be added as argument of function
    resources of especialists 5. now option to be added as argument of function

    now also produces another data that contains the q* and v (width) of species
    the v is the same for all species 
    q* change for each resource 
    '''
    niche_sps = {}
    #this only divides species in two to construct generalists and especialists
    generalists = sps_list[:len(sps_list)//2]
    especialists = sps_list[len(sps_list)//2:]
    
    for species in generalists: 
        resources = rnd.sample(environmental_niche, len_res_gen)
        q = [rnd.uniform(0, 0.9) for _ in range(len_res_gen)]
        q = np.round(q,1)
        #for generalists, we will fix the v for ALL resources
        width = [0.05 for _ in range(len_res_gen)]
        niche_sps[species] = {"niche": resources, "q_ast": q, "v": width}

    for species in especialists: 
        resources = rnd.sample(environmental_niche, len_res_esp)
        q = [rnd.uniform(0, 0.9)  for _ in range(len_res_esp)]
        q = np.round(q,1)
        width = [0.05 for _ in range(len_res_esp)]
        niche_sps[species] = {"niche": resources, "q_ast": q, "v": width}
          
    return niche_sps
