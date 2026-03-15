# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:20:21 2024

@author: mdrmi
"""
import pandas as pd 
from statistics import mean

def data(community, mainland_island, current_time_step, rep, comp_ab_winners, island_niche, type_simulation):
    '''
    For phase 1: outputs data including presence of species in the island (yes/no), abundance on the island, abundance of generalists 
    and especialists, competitive ability of the best competitors and niche of island. niche of the mainland always the same.
    type_simulation: tag to put in the output doc data. e.g. phase_1_10_per
    ADDING NOW WE SAVE MEAN AGE OF ESPECIALISTS AND GENERALISTS ON THE ISLAND. '''
    species_name = None
    abundance_count = 0
    number_generalists = []
    number_especialists = []  
    type_of_species = []
    age_generalists = []
    age_especialists = []

    for individual in community:
        if mainland_island[individual.x][individual.y] == 2:
            abundance_count += 1
            species_name = individual.species
            if individual.type_sps == "Generalist":
                number_generalists.append(individual)
                age_generalists.append(individual.age)
            elif individual.type_sps == "Epecialist":
                number_especialists.append(individual)
                age_especialists.append(individual.age)
        type_of_species.append(individual.species)
 
    presence = 1 if abundance_count > 0 else 0 
    # Eliminar duplicados
    type_of_species = set(type_of_species)       
    
    # Obtener nichos por especie (primer valor encontrado en comunidad)
    niches = []
    species_labels = []
    for sp in type_of_species:         
        niche_val = next(agent.niche for agent in community if agent.species == sp) #next gets the first value with those characteristics
        niches.append(niche_val)
        species_labels.append(sp)        

    niches_sps = pd.DataFrame({
        'species': species_labels,
        'niche': niches
    })
    
    df = pd.DataFrame({
        'time_step': [current_time_step],
        'species_in_island': [species_name],
        'island_populated': [presence],
        'abundance_island': [abundance_count],
        'number_of_generalists': [len(number_generalists)],
        'number_of_especialist': [len(number_especialists)],
        'comp_ability_winners': [list(comp_ab_winners)],
        'mean_age_generalists': [mean(age_generalists) if age_generalists else 0],
        'mean_age_especialists': [mean(age_especialists) if age_especialists else 0]
    })

    df_2 = pd.DataFrame({
        'island_niche': [island_niche]
    })

    # Combinar info de nichos
    df_niche = pd.concat([df_2]*len(niches_sps), ignore_index=True)
    df_full_niches = pd.concat([df_niche, niches_sps], axis=1)

    # Exportar
    output_dir = "C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/LAST_ORIGINAL"
    df.to_csv(f"{output_dir}/{type_simulation}_{rep}_{current_time_step}.csv", index=False)
    df_full_niches.to_csv(f"{output_dir}/{type_simulation}_niche_{rep}_{current_time_step}.csv", index=False)
