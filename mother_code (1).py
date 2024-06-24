# -*- coding: utf-8 -*-

import random as rnd
import tkinter as tk
import numpy as np
import math as math
from PIL import Image, ImageDraw
import time


#my functions 
from simple_landscape import simple_landscape
from ok_landscape_fixed_insolation_area import landscape_fixed_insolation_area
from adaptation import adapt 
from niche_construction_2 import niche_construction2
from niche_positioning import niche
from comp import competence
from list_of_species import list_of_species
from species_colors import color_species
from species_disp_2 import dispersion_species
from data_collection_2 import data, data_2

#GLOBAL VARIABLES RELATED TO LANDSCAPE 

nrow = ncol = 100
#nrow = 100
#ncol = 200
size = 1/3
main = ncol // 3

shape = 0
current_time_step = 0
species_list = list_of_species(20)
species_colors = color_species(species_list)
# time steps of the simulation
max_time_steps = 0

per =  50 
rep = 5
niches = niche_construction2(species_list, 1000,250,25,per) #PER!!!!!!!!!!!!!!!
niche_mainland = niches[0]
niche_island = niches[1]
#to create niches for all of the plants
for i in range(2, len(niches)):
    sp_num = i - 1    
    name_of_species = "niche_sp" + str(sp_num)
    globals()[name_of_species] = niches[i]

species_dispersal = dispersion_species(species_list, main)

mainland_island = landscape_fixed_insolation_area(nrow, ncol, size, shape, 'medium', main)
species_list_stable = species_list[:]
species_colors_dict = dict(zip(species_list_stable, species_colors))
species_niches_dict = dict(zip(species_list_stable, niches))
species_disp_dict = dict(zip(species_list_stable, species_dispersal))

class Visual:
    def __init__(self, max_x, max_y):
        self.zoom = 4
        self.max_x = max_x
        self.max_y = max_y
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=max_x * self.zoom, height=max_y * self.zoom)
        self.canvas.pack()
        self.canvas.config(background='royalblue')
        self.squares = np.empty((self.max_x, self.max_y), dtype=object)
        self.initialize_squares()
        self.time_step_label = tk.Label(self.root, text="Time Step: 0", fg="white", bg="royalblue")
        self.time_step_label.pack()
    def update_time_step(self, time_step):
        self.time_step_label.config(text=f"Time Step: {time_step}")
    def initialize_squares(self):
        '''
        create the land (island and mainland as brown) and the squares that represent each coordinate

        '''
        for x in range(self.max_x):
            for y in range(self.max_y):
                fill_color = 'saddlebrown' if mainland_island[y, x] != 0 else ''
                self.squares[x, y] = self.canvas.create_rectangle(
                    x * self.zoom, y * self.zoom, (x + 1) * self.zoom, (y + 1) * self.zoom,
                    outline='black', fill=fill_color )
def update_time_step_label(time_step):
    
    visual.update_time_step(time_step)

class Plant:
    def __init__(self, x, y, drawing, species):
        self.x = x
        self.y = y
        self.drawing = drawing
        self.age = 0
        self.pos = [x, y]
        self.disp_cap = species_disp_dict.get(species)          
        self.color = species_colors_dict.get(species)
        self.niche = species_niches_dict.get(species)
        self.species = species            
                         
            
def create_plant(x, y,initial_color):
    '''
    the plant is created on the windowa in a different function
    '''
    
    radius = 0.5
    return canvas.create_oval(
        (x - radius) * visual.zoom, (y - radius) * visual.zoom,
        (x + radius) * visual.zoom, (y + radius) * visual.zoom,
        outline='black', 
        fill = initial_color
        )

environmental_niche = niche(mainland_island, niche_island, niche_mainland)   


def dispersal(indiv,where):
    # Gaussian for dispersal with standard deviation
    dispersal_x = np.random.normal(indiv.disp_cap, indiv.disp_cap // 3)
    dispersal_y = np.random.normal(indiv.disp_cap, indiv.disp_cap // 3)
    
    # Random direction for x and y
    direction = rnd.choice([-1, 1])
    if where ==1:     
        dx = dispersal_x * direction
    if where ==2: 
        dx = (dispersal_x * direction)//3
    direction = rnd.choice([-1, 1])
    if where == 1:
        dy = dispersal_y * direction
    if where == 2: 
        dy = (dispersal_y * direction)//3
        
    
    # Ensure the new position wraps around vertically but not horizontally
    x_new = int(indiv.x + dx)
    y_new = int((indiv.y + dy) % nrow)  # Wrap around vertically

    if 0 <= x_new < ncol:  # Check horizontal boundaries
        if mainland_island[y_new, x_new] != 0:
            canvas.coords(indiv.drawing, (x_new - 0.5) * visual.zoom, (y_new - 0.5) * visual.zoom,
                          (x_new + 0.5) * visual.zoom, (y_new + 0.5) * visual.zoom)
            indiv.x = x_new
            indiv.y = y_new
            return [indiv.x, indiv.y]
    return None


visual = Visual(ncol, nrow)
canvas = visual.canvas
population = []


def stop_clock(num_steps, current_time_step, pause_time):
    if current_time_step in (num_steps):        
        time.sleep(pause_time)
         
def update():
    
          
    global current_time_step
    global population  # Declare population as a global variable
    #for specie in species_list:
    #stop_clock([50, 100, 150, 200,800,850,900,950], current_time_step, 5)
    for i in species_list:        
        for _ in range(2):        
            x = int(rnd.uniform(0, main))  # they get inizialized in the mainland 
             
            if 0 <= x < ncol:
                y = int(rnd.uniform(0, nrow))  # discrete move
                drawing = create_plant(x, y, initial_color='red')
                plant = Plant(x, y, drawing, i)
                population.append(plant)

    
   # create_individuals_mainland()
    update_time_step_label(current_time_step)
    plants_to_remove = []         #offspring    
    
   ##########33     
    for x in range(len(population)): 
        
        plant = population[x]
        num_offspring = rnd.randint(1,2) #now the plant could produce more than 1 seed/ offspring, randomly 
        if plant.age>1: 
            for seed in range(num_offspring):     
                where = rnd.randint(1, 2)
               
                position = dispersal(plant, where) #for now its that parent
                if position != None: 
                    x_off = position[0]
                    y_off =position[1] 
                    if x_off <0 or x_off> ncol: #this is because we took of the round wold in the y 
                        continue
                    else:
                        drawing_off = create_plant(x_off, y_off, plant.color)
                        offspring = Plant(x_off, y_off, drawing_off, plant.species)
                        possibility_of_adaptation = rnd.choice([1,2])
                        if possibility_of_adaptation ==2:               
                            if mainland_island[offspring.x][offspring.y] >1: #23 11 23 correction so occurs in future islands #== 2: #adaptation occur in islands
                                offspring.niche = adapt(environmental_niche[offspring.x][offspring.y],plant.niche, "natural_selection", "yes")
                        population.append(offspring)     
    
            if plant.age >= 1:
                canvas.delete(plant.drawing)
                plants_to_remove.append(plant)     

    for plant in population: 
        if mainland_island[plant.x][plant.y] > 1: # Only consider islands #this is in the case we build multiple islands in the future
           
            if not set(environmental_niche[plant.x][plant.y]) & set(plant.niche):
                canvas.delete(plant.drawing)
                plants_to_remove.append(plant)
            
    competence(population, environmental_niche, plants_to_remove)   
   #----------------------------------------------------------------------------
# =============================================================================
#    #KILL RANDOM MAINLAND SECTION    

    to_kill = []
          
    for i in range(nrow): 
        for j in range(ncol // 2):
            ctk = [j, i]
            to_kill.append(ctk)   
        
    tc = int(len(to_kill) * 0.2)
    target_cor = rnd.sample(to_kill, tc)                    
          
    to_remplace = []
          
    for plant in population: 
        if plant.pos in target_cor:
            plants_to_remove.append(plant)   
            to_remplace.append(plant.pos)           
    
    for to_re in to_remplace: 
        species = rnd.choice(species_list)    
        x = to_re[0]
        y = to_re[1]
          
       
       # re_plant = Plant(x, y)       
        #population.append(re_plant)
    


#      
#   # =============================================================================
   
    for plant in plants_to_remove:
        canvas.delete(plant.drawing)
        if plant in population:
            population.remove(plant)
        

    for plant in population:
       
        plant.age += 1
     
    print(len(population))
    
    
    # Data collection chunk

    if current_time_step % 10 == 0:

       data(population, mainland_island, environmental_niche, current_time_step,per, rep, niche_island)

    data_2(population, mainland_island, niche_island, current_time_step, max_time_steps,per,rep)

    current_time_step += 1
    
    
    if current_time_step < max_time_steps:
        # Schedule the next update with an interval
        visual.root.after(200, update)
    else:
        # Stop the simulation when we reach the maximum time steps
        print("Simulation finished.")


update()
visual.root.mainloop()
