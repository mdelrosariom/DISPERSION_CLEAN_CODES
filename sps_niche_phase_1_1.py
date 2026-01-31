# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 16:22:00 2025

@author: mdrmi
"""
import random as rnd

def species_niche(sps_list, environmental_niche, len_res_gen=10, len_res_esp=5): 
    '''
    Creates niches of the species in a community. 
    50% of species are generalists, 50% especialists.
    resources of generalists 10. now option to be added as argument of function
    resources of especialists 5. now option to be added as argument of function
    '''
    niche_sps = {}
    
    generalists = sps_list[:len(sps_list)//2]
    especialists = sps_list[len(sps_list)//2:]
    
    for species in generalists: 
        niche_sps[species] = rnd.sample(environmental_niche, len_res_gen)
    for species in especialists: 
        niche_sps[species] = rnd.sample(environmental_niche, len_res_esp)
          
    return niche_sps
