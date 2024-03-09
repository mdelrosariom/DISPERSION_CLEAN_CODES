# -*- coding: utf-8 -*-
import random as rnd
def adapt(island_niche, plant_niche, evolution_type, stop_after_adapt):
    '''
    this function takes the environmental niche and the niche of each plant
    and shift the niche of the plant to be more similar to the niche of the
    environment i.e. adapts plant to the environmental niche. Now with options 
    1. adaptation (directional, selection) or neutral evolution
    2. stop after adaptation (reached by directional or neutral evo)
    3. continue after adaptation 
    '''
    adapted_niche = []
    if evolution_type == "natural_selection" and stop_after_adapt =="yes":
        #habitat that plant can utilize
        niche_overlap = list(set(island_niche) & set(plant_niche))
        if niche_overlap[-1] in island_niche[0:len(plant_niche)]:
            #if all the niche of the plant is not inside the environment, i.e. not
            #totally adapted continue adaptation
            if len(niche_overlap) != len(plant_niche): 
                plant_niche = [i+1 for i in plant_niche]
            else:# if niche of plan is in environment, i.e. totally adapted then stop
                pass 
        else:  # *else will be at the right of the island_niche
            if len(niche_overlap) != len(plant_niche): 
                plant_niche = [i-1 for i in plant_niche]
            else: 
                pass 
    if evolution_type == "natural_selection" and stop_after_adapt =="no":
        #habitat that plant can utilize
        niche_overlap = list(set(island_niche) & set(plant_niche))
        if niche_overlap[-1] in island_niche[0:len(plant_niche)]:
            #if all the niche of the plant is not inside the environment, i.e. not
            #totally adapted continue adaptation
            if len(niche_overlap) != len(plant_niche): 
                plant_niche = [i+1 for i in plant_niche]
            else:# if niche of plan is in environment, i.e. totally adapted then stop
                adapted_niche = plant_niche     
        else:  # *else will be at the right of the island_niche
            if len(niche_overlap) != len(plant_niche): 
                plant_niche = [i-1 for i in plant_niche]
            else: 
                adapted_niche = plant_niche   
        random_walk = rnd.randint(1, 2)
        if random_walk == 1: 
            adapted_niche = [i+1 for i in adapted_niche]
        if random_walk == 2: 
            adapted_niche = [i-1 for i in adapted_niche]
   
    
    if evolution_type == "neutral" and stop_after_adapt =="yes":
        niche_overlap = list(set(island_niche) & set(plant_niche))        
        if len(niche_overlap) != len(plant_niche): 
            random_walk = rnd.randint(1, 2)
            if random_walk == 1: 
                plant_niche = [i+1 for i in plant_niche]
            if random_walk == 2: 
                plant_niche = [i-1 for i in plant_niche]
    if evolution_type == "neutral" and stop_after_adapt =="no":
        random_walk = rnd.randint(1, 2)
        if random_walk == 1: 
            plant_niche = [i+1 for i in plant_niche]
        if random_walk == 2: 
            plant_niche = [i-1 for i in plant_niche]
    if len(adapted_niche) != 0: 
        return(adapted_niche)
          
    return plant_niche

x = [8,9,10]
for i in range(20): 
    x = adapt([3,4,5,6,7,8], x, "natural_selection", "no")  # Set to "no" to continue adaptation
    print(x)

