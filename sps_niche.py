# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 16:22:00 2025

@author: mdrmi
"""
import random as rnd

def species_niche(sps_list, environmental_niche): 
    '''
    creates niches of the species in community. For now each one has 5 resources
    can be modified to differenciate between generalists/specialists very easily
    '''
    niche_sps = {}
    
    for i in sps_list: 
        niche_sps[i] = rnd.sample(environmental_niche, 5)
    
    return niche_sps