# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 01:56:48 2025

@author: mdrmi
"""
import random as rnd

def community_control(community, nrow, ncol): 
    '''
    controls the number of individuals in all of the world (not just mainland) so it doesnt get full too quickly.
    allows 60% of world to be occupied. 
    
    community : the list of plants in community.
    nrow : dimentions of mainland. one number
    ncol : dimentions of column. one number
    Returns : list of individuals to eliminate
    '''
    
    # max number of individuals that will be allowed in the mainland
    max_num_in_world = int(0.6 * (nrow * ncol))
    
    # we pic the number of individuals in mainland
    individuals_world = []
    
    for plant in community: 
        # if the plant is in the mainland will have the y coordinate
        # of its position in the mainland not active here, active in community_control.py
        #if plant.pos[0] < main: #so in mainland, x coordinate of sps. 
        individuals_world.append(plant)
    #more individuals than allowed
    if len(individuals_world) > max_num_in_world: 
        # avoid bias
        ##rnd.shuffle(individuals_mainland) this is not necesary because rnd.sample is already aleatory 
        # sample instead to avoid duplicates — sample instead of choices
        excess = len(individuals_world) - max_num_in_world
        #simple and efficient; stuning
        selected_to_die = rnd.sample(individuals_world, k=excess)

        return selected_to_die
    else: 
        return []
