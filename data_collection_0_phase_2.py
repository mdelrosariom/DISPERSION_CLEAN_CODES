# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:20:21 2024

@author: mdrmi
"""

import pandas as pd

def data(community, mainland_island, current_time_step, rep):
    '''
    For phase 0: outputs a single-row DataFrame with the species name, its presence (0/1),
    and the number of individuals on the island.
    '''
    
    species_name = None
    abundance_count = 0
    number_generalists = []
    number_especialists = []
    for individual in community:
        #if individual in the island
        if mainland_island[individual.x][individual.y] == 2:
            abundance_count += 1
            species_name = individual.species  # All individuals share the same species
            if individual.type_sps ==  "Generalist": 
                number_generalists.append(individual)
            if individual.type_sps == "Epecialist": 
                number_especialists.append(individual)

    presence = 1 if abundance_count > 0 else 0

    df = pd.DataFrame({
        'time_step': [current_time_step],
        'species_in_island': [species_name],
        'island_populated': [presence],
        'abundance_island': [abundance_count],
        'number_of_generalists': len(number_generalists), 
        'number_of_especialist': len(number_especialists)
        
    })

    df.to_excel(f"C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/output_data_phase_1_1000_run/phase_1{rep}{current_time_step}.xlsx", index=False)
