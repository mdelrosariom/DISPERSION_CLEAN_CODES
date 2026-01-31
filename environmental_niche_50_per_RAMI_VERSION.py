import numpy as np
import random as rnd

def niche_construction(mainland_island): 
    ''' 
    construct a dataframe with the same dimentions as mainland island and different resources. island has a subset of 
    resources of the mainland
    now island_resources 50% of the mainland

    adjusted to Ramiadantsoa et al. 2018: 
    each cell will be represented by the resource and a value of q [0,1)
    its discrete from 0 to 1
    
    environmental_niche its an array in which element contains i,j contains a list of is land (1 or 2, mainland or island
    respectivelly), the length of the list is the number of resources, the identity of resources is each element of the list
    so a longer list indicates more richness of resources.
    the identity of the total resources in mainland or island are in island_resources and mainland_resources respectivelly, 
    there is just a list, not formated as an array but a list. 
    Finally ques includes the q value for each resource on environmental_niche as described by RAMI.. et al 2018
    '''    

    mainland_resources = list(range(1,100)) #resources present in mainland
    island_resources = rnd.sample(mainland_resources, 50) #resources present island. now random number   
    
    environmental_niche = mainland_island.copy().astype(object) #copy mainland island
    ques = mainland_island.copy().astype(object)
    environmental_niche[environmental_niche == 0] = np.nan #replace 0 values for NA values (sea)
    for i in range(environmental_niche.shape[0]): 
        for j in range(environmental_niche.shape[1]): 
            if environmental_niche[i, j] == 1: #mainland              
                environmental_niche[i, j] = mainland_resources         
                q = [rnd.uniform(0, 0.9)  for _ in range(len(environmental_niche[i, j]))]
                q = np.round(q,1)
                ques[i,j] = q
            if environmental_niche[i, j] == 2: #island   
                environmental_niche[i, j] = island_resources
                q = [rnd.uniform(0, 0.9)  for _ in range(len(environmental_niche[i, j]))]
                q = np.round(q,1)
                ques[i,j] = q

    return environmental_niche, island_resources, mainland_resources, ques