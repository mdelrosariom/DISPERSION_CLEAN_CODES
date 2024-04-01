# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:39:32 2024

@author: mdrmi
"""

import statistics as stats
import pandas as pd

def data(population, mainland_island, environmental_niche,filename):
    abundance_of_community = len(population)
    richness_of_community = set()
    richness_of_island = set()
    abundance_in_island = []
    identity_island = set()
    adaptation_island = []
    adaptation_continent_island_sp = []
    adaptation_continet_population_not_island = []

    for individual in population:
        richness_of_community.add(individual.species)

    richness_of_community = len(richness_of_community)

    for individual in population:
        if mainland_island[individual.x][individual.y] == 2:  # on island
            abundance_in_island.append(individual)
            richness_of_island.add(individual.species)
            identity_island.add(individual.species)
            adaptation_sp = len(set(environmental_niche[individual.x][individual.y]) & set(individual.niche))
            adaptation_island.append(adaptation_sp)

    abundance_in_island = len(abundance_in_island)
    richness_of_island = len(richness_of_island)
    identity_island = set(identity_island)
    if len(adaptation_island) != 0:
        adaptation_island = stats.mean(adaptation_island)

    for species_ada in population:
        if mainland_island[species_ada.x][species_ada.y] == 1:  # in continent
            adaptation_sp_ada = len(set(environmental_niche[species_ada.x][species_ada.y]) & set(species_ada.niche))

            if species_ada.species in identity_island:  # if the sp also in island
                adaptation_continent_island_sp.append(adaptation_sp_ada)
            else:
                adaptation_continet_population_not_island.append(adaptation_sp_ada)
    if len(adaptation_continent_island_sp) != 0:
        adaptation_continent_island_sp = stats.mean(adaptation_continent_island_sp)
    if len(adaptation_continet_population_not_island) != 0:
        adaptation_continet_population_not_island = stats.mean(adaptation_continet_population_not_island)
    data_dict = {
        "a_comm": (abundance_of_community) ,
        "rich_comm": (richness_of_community), 
        "rich_island": (richness_of_island),         
        "abu_island":(abundance_in_island), 
        "identity_island": tuple(identity_island), 
        "adaptation_island": (adaptation_island), 
        "ad_sps_cont_present_island": (adaptation_continent_island_sp ),     
        "ad_sps_cont_not_in_island": (adaptation_continet_population_not_island)
        
        } 
   
    
    data_df = pd.DataFrame(data_dict)
    
    data_df.to_excel(filename, index=False)
    
    
    
    
def data_2(population, mainland_island, niche_island, current_time_step, timesteps): 
    
    no_sp_is_be = []
    no_sp_is_end = []
    no_sp_ml_be = []
    no_sp_ml_end = []
   
    numbers_list = list(range(1,timesteps+1))
    
    beggining = numbers_list[:int(timesteps*0.1)]
    print("START",beggining)
    end = numbers_list[int(0.9 *timesteps):]       
     
    if current_time_step in beggining:     
       
        for i in population:      
        
            if mainland_island[i.x][i.y] == 1:
                adaptation_sp_mainland = len(set(niche_island) & set(i.niche))
                no_sp_ml_be.append(adaptation_sp_mainland)        
            #no_sp_ml_be = stats.mean(no_sp_ml_be)
            if mainland_island[i.x][i.y] == 2:
                adaptation_sp_is = len(set(niche_island) & set(i.niche))
                no_sp_is_be.append(adaptation_sp_is)
        if len(no_sp_ml_be) != 0: 
            no_sp_ml_be = stats.mean(no_sp_ml_be) 
        if len(no_sp_is_be) != 0: 
            no_sp_is_be = stats.mean(no_sp_is_be)
        
                       
    if current_time_step in end:  
        for i in population:    
            if mainland_island[i.x][i.y] == 1:
                adaptation_sp_mainland = len(set(niche_island) & set(i.niche))
                no_sp_ml_end.append(adaptation_sp_mainland)        
            #no_sp_ml_end = stats.mean(no_sp_ml_end) 
            if mainland_island[i.x][i.y] == 2:
                adaptation_sp_is = len(set(niche_island) & set(i.niche))
                no_sp_is_end.append(adaptation_sp_is)   
        if len(no_sp_ml_end) != 0: 
            no_sp_ml_end = stats.mean(no_sp_ml_end) 
        if len(no_sp_is_end) != 0: 
            no_sp_is_end = stats.mean(no_sp_is_end)
    data_dict_2 = {"niche_sp_mainland_start": [no_sp_ml_be], 
                    "niche_sp_island_start": [no_sp_is_be], 
                    "niche_sp_mainland_end": [no_sp_ml_end], 
                    "niche_sp_island_end": [no_sp_is_end]}
    print(data_dict_2)
    data_df_2 = pd.DataFrame(data_dict_2)

    print("estooo", data_df_2)
    
    if current_time_step in beggining:
        data_df_2.to_excel("C:/Users/mdrmi/OneDrive/Escritorio/data_simus_disp/Data_2_BEGGINING"+ str(current_time_step)+ ".xlsx", index=False)
    if current_time_step in end:
        data_df_2.to_excel("C:/Users/mdrmi/OneDrive/Escritorio/data_simus_disp/Data_2_END"+ str(current_time_step)+ ".xlsx", index=False)
