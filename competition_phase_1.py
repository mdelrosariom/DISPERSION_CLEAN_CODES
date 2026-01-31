import random as rnd
from collections import defaultdict

def competition(community, plants_to_remove, resources_island, mainland_island): 
    '''
    For phase 1. At each occupied position we check which sps will have more competitive 
    adventage based on the number of resources that the species can utilize and its overposition
    with the island resources
    We will always start with plants that have at least one resource shared with the island.
    modification, only apply this to the species on the island
    '''
    #so first we need to extract the species on the island 
    competitive_ab_sps = []
    community2 = []
    for plant_in_island in community: 
        if mainland_island[plant_in_island.pos[0], plant_in_island.pos[1]]==2:
            community2.append(plant_in_island)
    
    # Create a directory to group plants by position
    position_dict = defaultdict(list)

    #for each plant in the island
    for plant in community2:
        # Use a tuple of the position to group the plants
        position_dict[tuple(plant.pos)].append(plant)

    for pos,  plants in position_dict.items():
        if len(plants) > 1:  # If there are more than 1 plant/individual in a position
           
            # Initialize variables for the winner
            winner = None
            highest_energy_resource = 0  # Start with the lowest number
            #this is the easiest way to avoid priviledges in selecting the plant
            rnd.shuffle(plants)
            # Calculate the energy_resource for each plant and find the one with the highest value
            for plant in plants:
                print("plants competing")
                print(plant.type_sps)
                # Calculate energy_resource
                energy_resource = (1 / len(plant.niche) )* (len(list(set(resources_island) & set(plant.niche))))**2
                
                # If this plant has the highest energy_resource, it becomes the new winner
                if energy_resource > highest_energy_resource:
                    highest_energy_resource = energy_resource
                    winner = plant
                    print(plant.species)
                    print(plant.type_sps )
                    competitive_ab_sps.append(highest_energy_resource)

            # Add all other plants (except the winner) to plants_to_remove
            losers = [p for p in plants if p != winner]
            plants_to_remove.extend(losers)

    return plants_to_remove, set(competitive_ab_sps)

