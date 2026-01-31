# -*- coding: utf-8 -*-

import random as rnd

def niche_construction2(niche_width_mainland, niche_width_island, island_niche_overlap): 
    '''
    Creates the identity of resources of the mainland and the island. the island have some resorces in common with the mainland and other unique ones, the num of shared resources depend on island_niche_overlap
    1. Niche_width_mainland, number of resouces in mainland
    2. Niche_width_island, number of resources in island
    3. island_niche_overlap resources sharing between island and mainland
    This function creates:
    1. The niche of the mainland.
    2. The niche of the island.    
    '''
    niches = []
    niche_mainland = list(range(1,niche_width_mainland + 1))
    niches.append(niche_mainland)       
    #niche of island 
    portion = int((island_niche_overlap/100)*len(niche_mainland))   
    #we will select randomly which resources mainland and island share. how many is given by portion
    shared = list(rnd.sample(niche_mainland,portion))
    num_new_resources = niche_width_island - len(shared)
    new_resources = list(range(niche_width_mainland + 1, niche_width_mainland + 1 + num_new_resources+1))
    niche_island = shared + new_resources
    niches.append(niche_island)    
    
    return niches
