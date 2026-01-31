import random as rnd
import numpy as np
from collections import defaultdict
from scipy.special import i0

def competition(community, environmental_niche, mainland_island, ques):#competition(community, plants_to_remove, environmental_niche, mainland_island, ques): 
    '''
    Based on Ramiadantsoa et al 2018. At each occupied position we check which sps will have more competitive 
    adventage based on the equation (3). the one who has the biggest sum of this equations (taking into account all resources) win.
    We will always start with plants that have at least one resource shared with the island.
    modification, only apply this to the species on the island

    resources_island need to be the first element of the running of niche construction, environmental_niche
    the idea is as follows, each cell is represented by a q, value of the resource, we compute equation (3) for this
    resource and then we sum for all of the shared resources between the plant and its cell. if the plant has this higher value
    sum of all the resources (of eq. 3) higher then can keep the space, if not it gets eliminated. 

    '''
    #so first we need to extract the agents on the island 
    competitive_ab_sps = []
    community2 = []
    elimate_plants = []
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
          #  print("OK")
            # Initialize variables for the winner
            winner = None
            highest_energy_resource = 0  # Start with the lowest number
            #this is the easiest way to avoid priviledges in selecting the plant
            rnd.shuffle(plants)
            # Calculate the energy_resource for each plant and find the one with the highest value
            for plant in plants:
                plant_resources_fitness = []
                print("plants competing")
                print(plant.type_sps)
                # Calculate energy_resource

                for resource in environmental_niche[tuple(plant.pos)]:
                    print("this is thing",resource)
                    #so if plant has some resource present on the cell we compute the eq. 3 for that resource 
                    for niche_element in plant.niche['niche']:
                        #print(niche_element) 
                        if resource == niche_element: 
                            print("this is res", resource)
                            index_resource_plant = plant.niche["niche"].index(resource) #should be niche element for plant but because they are equals no problem
                            index_environmental_resource = environmental_niche[tuple(plant.pos)].index(resource)
                            f_res = np.exp((1/(plant.niche["v"][index_resource_plant]))*np.cos(2*np.pi*(ques[tuple(plant.pos)][index_environmental_resource]-plant.niche["q_ast"][index_resource_plant])))/i0(1/plant.niche["v"][index_resource_plant])
                            
                            plant_resources_fitness.append(f_res)
                            print(plant_resources_fitness)

                energy_resource= sum(plant_resources_fitness)
                # If this plant has the highest energy_resource, it becomes the new winner
                if energy_resource > highest_energy_resource:
                    highest_energy_resource = energy_resource
                    winner = plant
                    print(plant.species)
                    print(plant.type_sps)
                    competitive_ab_sps.append(highest_energy_resource)

            # Add all other plants (except the winner) to plants_to_remove
            losers = [p for p in plants if p != winner]
            elimate_plants.extend(losers)#plants_to_remove.extend(losers)

    return elimate_plants, set(competitive_ab_sps)#plants_to_remove, set(competitive_ab_sps)
