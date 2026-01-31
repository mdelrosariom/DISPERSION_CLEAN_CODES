import numpy as np
import csv
import os

def data_fast_append(community, mainland_island, current_time_step, rep, comp_ab_winners,
    island_niche, type_simulation):
    '''
    For phase 1: outputs data including presence of species in the island (yes/no), abundance on the island, abundance of generalists 
    and especialists, competitive ability of the best competitors and niche of island. niche of the mainland always the same.
    type_simulation: now suppo will append the rows in a doc instrad of doing it for every time steps (so we dont have 1000* idk how much)
    documents
    '''

    # ----------------------------------------------------------
    # Extract info in one pass
    # ----------------------------------------------------------
    species_list = []
    niche_list = []

    abundance_count = 0
    species_name = None
    n_generalist = 0
    n_specialist = 0

    for ind in community:

        species_list.append(ind.species)
        niche_list.append(ind.niche)

        if mainland_island[ind.x][ind.y] == 2:

            abundance_count += 1
            species_name = ind.species

            if ind.type_sps == "Generalist":
                n_generalist += 1
            elif ind.type_sps == "Epecialist":
                n_specialist += 1

    presence = 1 if abundance_count > 0 else 0
    species_niche_map = {}
    for sp, niche in zip(species_list, niche_list):
        if sp not in species_niche_map:
            species_niche_map[sp] = niche

    # ----------------------------------------------------------
    # Vectorized species + niche extraction
    # ----------------------------------------------------------
   #### species_arr = np.array(species_list, dtype=object)
    ######niche_arr = np.array(niche_list, dtype=float)

   ###### unique_species, first_idx = np.unique(species_arr, return_index=True)
   ######### unique_niches = niche_arr[first_idx]

    # ----------------------------------------------------------
    # Prepare rows
    # ----------------------------------------------------------
    row_main = [
        current_time_step,
        species_name,
        presence,
        abundance_count,
        n_generalist,
        n_specialist,
        list(comp_ab_winners)
    ]

   # rows_niches = [
   #     [current_time_step, island_niche, sp, niche]
    #    for sp, niche in zip(unique_species, unique_niches)
   # ]
    rows_niches = [
        [current_time_step, island_niche, sp, species_niche_map[sp]]
        for sp in species_niche_map
    ]


    # ----------------------------------------------------------
    # Append to CSVs instead of creating new ones
    # ----------------------------------------------------------
    output_dir = "C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU/FAST_LAST_ORIGINAL"

    main_file = f"{output_dir}/{type_simulation}_{rep}.csv"
    niche_file = f"{output_dir}/{type_simulation}_niche_{rep}.csv"

    # ---- MAIN FILE ----
    write_header_main = not os.path.exists(main_file)

    with open(main_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header_main:
            writer.writerow([
                "time_step",
                "species_in_island",
                "island_populated",
                "abundance_island",
                "number_of_generalists",
                "number_of_especialist",
                "comp_ability_winners"
            ])
        writer.writerow(row_main)

    # ---- NICHE FILE ----
    write_header_niche = not os.path.exists(niche_file)

    with open(niche_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header_niche:
            writer.writerow([
                "time_step",
                "island_niche",
                "species",
                "niche"
            ])
        writer.writerows(rows_niches)
