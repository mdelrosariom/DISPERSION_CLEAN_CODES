from collections import defaultdict
import numpy as np
from scipy.special import i0
import random as rnd

def competition(community, environmental_niche, mainland_island, ques):#(community, plants_to_remove, environmental_niche, mainland_island, ques):
    
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
    eliminated_plants = []
    comp_ability_sps = []
    # Vector way to select only plants in island
    community2 = [p for p in community if mainland_island[p.pos[0], p.pos[1]] == 2]
    
    # Create a directory to group plants by position
    position_dict = defaultdict(list)

    # Use a tuple of the position to group the plants
    for p in community2:
        position_dict[tuple(p.pos)].append(p) #dictionary with keys being the position and values being the agents

    for pos, plants in position_dict.items():
        if len(plants) <= 1: #
            continue
        rnd.shuffle(plants)

        env_niche = environmental_niche[pos] #resources in the environment in the position we are analyzing 
        ques_cell = np.array(ques[pos]) #values of qs of the resources in that environment

        best = -np.inf
        winner = None

        for p in plants: #plants in the position we are analyzing
            niche_map = {r: i for i, r in enumerate(p.niche)} #this puts a value from 1 to length of the niche to each resource so e.g res_1:1, res_2:2, res_3:3...
            shared = [r for r in env_niche if r in niche_map] #resources of plant that are in the environment

            if not shared:
                continue #it the plant do not share any resources with the environment, continue

            idx_p = np.array([niche_map[r] for r in shared]) #number of the resource in plant
            idx_e = np.array([env_niche.index(r) for r in shared]) #value of that resourse in the environment
            diff = 2*np.pi*(ques_cell[idx_e] - np.array(p.q_ast)[idx_p]) #computes the equation of rami
            f_res = np.exp((1/np.array(p.v)[idx_p]) * np.cos(diff)) / i0(1/np.array(p.v)[idx_p])
            energy = f_res.sum() #sum for all resources

            if energy > best:
                best = energy
                winner = p
                comp_ability_sps.append(best)
        eliminated_plants.extend([pl for pl in plants if pl != winner])
    return eliminated_plants, set(comp_ability_sps)
