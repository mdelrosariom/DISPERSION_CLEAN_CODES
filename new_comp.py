# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 11:57:04 2024

@author: mdrmi
"""
import random as rnd

def competence (population, environmental_niche, plants_to_remove): 
    '''
 will select the species that are better adapted in the case in which multiple species are in the same positon

    '''
    #in this chunk we add to the same list all the plants that are in the same space
    for plant_1 in population: 
        same_place = []
        comp = []        
        bests = []
        same_place.append(plant_1)        
        rest = [x for x in population if x != plant_1]       
        for plant_2 in rest: 
            if plant_1.pos == plant_2.pos:
                same_place.append(plant_2)
        #if there is more than 1 plant in the same space, we proceed to check its 
        #competitive ability                 
        if len(same_place) > 1:              
            winner = []                 
            for competitor in same_place:  
                #competitive ability is given by how well the plant is adapted to the 
                #environment she is in, so we check the superposition between its environmental niche and its own niche
                comp_ab = len(set(environmental_niche[competitor.x][competitor.y]) & set(competitor.niche))/len(competitor.niche)
                competitor.comp_ab = comp_ab                
            #to not totally determine that the most adapted will always win we pick a random number     
            winners = rnd.random()
            for options in same_place: 
                #if the plant in the same place has a number bigger than the random number
                #it gets added to the bests list
                if options.comp_ab > winners :
                    bests.append(options)
            #if there is only one member of bests, that plant stays
            if len(bests) == 1: 
                    winner = bests[0]
                   
                    losers = [x for x in same_place if x !=winner]                    
            #other ways the plant gets chosen randomply         
            else: 
                rnd.shuffle(same_place)
                winner = rnd.choice(same_place)                
                losers = [x for x in same_place if x !=winner]
               
            for los in losers: 
                
                plants_to_remove.append(los)    
        else: 
            continue
    return(plants_to_remove)