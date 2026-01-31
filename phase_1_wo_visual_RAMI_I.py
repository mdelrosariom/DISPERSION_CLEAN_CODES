# -*- coding: utf-8 -*-
"""
Created on Mon May 12 20:46:54 2025

@author: mdrmi
"""
import random as rnd
import numpy as np
import math as math
import os

'''
in phase 1 we add the environmental resources + plant niche.

has the modifications to implement the competition of Ramiadantsoa et al 2018
'''
#my functions 
os.chdir("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU")
from corrected_landscape_fixed_insolation_area import landscape_fixed_insolation_area
from data_collection_2_phase_0 import data
from competition_phase_RAMI_VERSION import competition
from community_control import community_control
from list_of_species import list_of_species
from sps_niche_phase_RAMI_VERSION import species_niche
from environmental_niche_10_per_RAMI_VERSION import  niche_construction
   

def dispersal(indiv, nrow, mainland_island):
    '''
    dispersal function, the offspring of the plants (seeds) are the one that get dispersed. 
    two types of dispersal: short and more frequent, long and less frequent. returns the new position of 
    the seeds (in update controls to make sure seed disperse in landscape boundaries and in land)
    indiv: agent 
    nrow: length (number of rows) of mainland matrix 
    mainland_island: landscape 
    '''
    type_d =  rnd. uniform(0, 1)
    if type_d >= 0.9: 
        #dispersal_type = 'long_distance' #less probable 10%
        lam_x = nrow // 5
        lam_y = nrow // 5
    else: 
       # dispersal_type = 'short_distance' #more probable, almost always 90%
       lam_x = nrow // 10
       lam_y = nrow // 10        
    
    dispersal_x = np.random.poisson(lam_x)
    dispersal_y = np.random.poisson(lam_y)
    
    direction = rnd.choice([-1, 1])
    dx = dispersal_x * direction

    direction = rnd.choice([-1, 1])
    dy = dispersal_y * direction

    x_new = int(indiv.x + dx)
    y_new = int((indiv.y + dy) % nrow)  # Wrap around vertically

    if 0 <= x_new < mainland_island.shape[0] and 0 <= y_new < mainland_island.shape[1]:  # Check horizontal boundaries
        if mainland_island[y_new, x_new] != 0:
            indiv.x = x_new
            indiv.y = y_new
            return [indiv.x, indiv.y]
        else: 
            return None 
    else: 
        return None
community = []

    
def simulations(num_simus):     
    
    '''
    this gives all of the parameters to run the simulations
    '''
    for i in range(num_simus): 
        print("THIS IS THE SIM",i )
        #to track info of simus
        rnd.seed(i)
        np.random.seed(i)  
          
        # time steps of the simulation + replicas 
        max_time_steps = 1000        
        rep = i    

        #parameters of landscape + creation
        nrow = ncol = 100
        size = 1/3
        main = ncol // 3             
        mainland_island = landscape_fixed_insolation_area(nrow, ncol, size, 'medium', main)  

        #define number of species
        #directory that contains the name of the sps "sp1, sp2,... spx"
        species_list = list_of_species(2)         
              
        #resources available in the environment, niche of environment + niche sps
        resources = niche_construction(mainland_island) #function call
        resources_environment = resources[0] #matrix with resources (overlaps with landscape)
        resources_island = resources[1] 
        resources_mainland = resources[2]
        ques = resources[3]
        species_niches_dict = species_niche(species_list, resources_mainland)             
        
        #added, i need to define class here 
        
        
        class Plant:  
            '''
            this function defines the agents of this project: plants. 
            they are defined by a 2D position (x and y), they have an age (annual plants), 
            they have a niche which defined if they are generalists; use + resources but in a -efficient 
            way, and especialists - resources in a + efficient way.
            '''   
            def __init__(self, x, y,  species):
                self.x = x
                self.y = y      
                self.age = 0
                self.pos = [x, y]      
                self.species = species       
                self.niche = species_niches_dict.get(species)["niche"]#species_niches_dict.get(species)   
                self.v = species_niches_dict.get(species)["v"]
                self.q_ast = species_niches_dict.get(species)["q_ast"]
                if len(self.niche) == max(len(d["niche"]) for d in species_niches_dict.values()): 
                    self.type_sps = "Generalist"
                    
                else: 
                    self.type_sps = "Epecialist"           
                    
        community = []     
        #runs update    
        update(nrow, main, species_list, max_time_steps, rep, mainland_island, resources_island, community, "sim_RAMI_10", Plant,resources_environment, ques )
                
        print("Starting", i)
        
        
def update(nrow,  main, species_list, max_time_steps, rep, mainland_island, resources_island, community, type_sim, Plant,resources_environment, ques ):    
    ''' 
    this is the core of all of the simulations, basically creates offspring and disperse it, carry out competition (inter and intra)
    in the island, carries out community control in the mainland, eliminates from community the plants that are lost due to this
    and export data. 
    ''' 
    current_time_step = 0   
         
    while current_time_step < max_time_steps:
        
        #-------- formation of the community chunk 
        for i in species_list:
            #20 indiv. per species
            for _ in range(20):        
                x = rnd.randint(0, main) # they get inizialized in the mainland             
               # if 0 <= x < ncol: i think this is trivial, we know x should be in 0 main
                y = rnd.randint(0, nrow-1)  # discrete position              
                plant = Plant(x, y,i) 
                community.append(plant)
        #----------------------------------------------------------------------------------------
        plants_to_remove = []     #plants that will be excluded to the community   

        #-------- offspring creation chunk             
        for x in range(len(community)):         
            plant = community[x]
            #plants can have between 1 to 3 seeds            
            num_offspring = rnd.randint(1,3)
            if plant.age>1: 
                for seed in range(num_offspring):    #seed not used as variable, named for ilustrative porpuses 
                    position = dispersal(plant, nrow, mainland_island) #for now its that parent
                    if position != None: #so not out of the x limits, not in sea. meaning if falls on the sea or outside world limits it will not be taken into account
                        x_off = position[0]
                        y_off = position[1] 

                        #in phase 1, estableshisment only occurs if offspring can use resources present in the island. 
                        #clarification, sps always can be in the mainland because always has overlapping resources with mainland
                    
                        if mainland_island[x_off, y_off] == 2: #in island                            
                            if len(list(set(resources_island) & set(plant.niche))) != 0: # niche of the parent for now                                
                                offspring = Plant(x_off, y_off, plant.species) #again, establishment only if seed overlaps with island
                                community.append(offspring)  
                            else: 
                                continue  # seed cant stablish in the island, move 
                                
                        else: #in mainland establishment always possible because overlapping always occur
                            offspring = Plant(x_off, y_off, plant.species) 
                            community.append(offspring)  
                    else: #new part, if it falls outside the limits of the world or in the ocean seed not considered and next case
                        continue                        
                if plant.age >= 1:
                    plants_to_remove.append(plant)  
        #----------------------------------------------------------------------------------------
        
        #-----------competition chunk
        plants_down_for_competition = competition(community,plants_to_remove,resources_environment, mainland_island, ques)  
        #adding plants lost for competition to list to eliminate 
        plants_to_remove.extend(plants_down_for_competition[0])
        #----------------------------------------------------------------------------------------  

        #----------community control on mainland line 
        #avoid monopolization in island
        com_control = community_control(community,nrow,main)
        plants_to_remove.extend(com_control)
        #-----------------------------------------------------------------------------------------

        #---------- elimination of all plants that didnt make it chunk 
        for plant in plants_to_remove:          
            if plant in community:
                community.remove(plant)    
        for plant in community:            
            plant.age += 1     
        #-----------------------------------------------------------------------------------------
        print(len(community))    
        print('CURRENT TIME STEP', current_time_step)        
        # Data collection chunk
        # so we record data at each time step    
        #---------- export data chunk 
        data(community, mainland_island, current_time_step,rep, plants_down_for_competition[1],resources_island, type_sim )
        current_time_step += 1         
    
    print("simulation finished")       
        
      
simulations(100)
