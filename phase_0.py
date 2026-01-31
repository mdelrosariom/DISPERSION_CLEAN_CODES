# -*- coding: utf-8 -*-

import random as rnd
import tkinter as tk
import numpy as np
import math as math
from PIL import Image, ImageDraw
import time
import os
'''
in phase 0 we are only interested in achieving a constant non zero abundance of the species on the island. 
only one species. 
no niche.
we change the dispersal, now only long, short dispersal given by gaussean, centered in the mean
and sd 1/4 mainland
"competition" occurs by randomly selecting an individual if is in the same place than other
'''
#my functions 
os.chdir("C:/Users/mdrmi/OneDrive/Escritorio/ABM_PHASES_SIMU")
from corrected_landscape_fixed_insolation_area import landscape_fixed_insolation_area
from species_colors import color_species #we are only working with one specie. 
#from species_disp_2 import dispersion_species  
from data_collection_2_phase_0 import data
from competition_phase_0 import competition
from community_control import community_control
#GLOBAL VARIABLES RELATED TO LANDSCAPE 

nrow = ncol = 100
size = 1/3
main = ncol // 3
shape = 0
current_time_step = 0
## species_list = list_of_species(1) THIS IS FROM A FUNCTION, WE DONT USE THIS HERE
species_list = [1]
species_colors = color_species([1]) #we need to put it like this because there is one sps.
# time steps of the simulation
max_time_steps = 100

#per =  50 we dont use this 
rep = 1
#species_dispersal = dispersion_species([1], main)

mainland_island = landscape_fixed_insolation_area(nrow, ncol, size, 'medium', main)
species_list_stable = species_list[:]

species_colors_dict = dict(zip(species_list_stable, species_colors)) #this is ok, will produce 1 sps.
#species_disp_dict = dict(zip(species_list_stable, species_dispersal))
#class visual is not modified in phase 0.
class Visual:
    def __init__(self, max_x, max_y):
        '''
        defines visual output mainland island species
        '''
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
    '''
    in phase 0 plant does not have a niche
    '''
    def __init__(self, x, y, drawing, species):
        self.x = x
        self.y = y
        self.drawing = drawing
        self.age = 0
        self.pos = [x, y]
        #self.disp_cap = species_disp_dict.get(species)          
        self.color = species_colors_dict.get(species)
        self.species = species            
                         
            
def create_plant(x, y,initial_color):
    '''
    the plant is created on the window in a different function
    '''    
    radius = 0.5
    return canvas.create_oval(
        (x - radius) * visual.zoom, (y - radius) * visual.zoom,
        (x + radius) * visual.zoom, (y + radius) * visual.zoom,
        outline='black', 
        fill = initial_color
        )

def dispersal(indiv):
    type =  rnd. uniform(0, 1)
    if type >= 0.9: 
        dispersal_type = 'long_distance' # Randomly choose type
    else: 
        dispersal_type = 'short_distance'
    
    if dispersal_type == 'short_distance':
        lam_x = nrow // 10
        lam_y = nrow // 10
    else:  # long_distance
        lam_x = nrow // 4
        lam_y = nrow // 4
    
    dispersal_x = np.random.poisson(lam_x)
    dispersal_y = np.random.poisson(lam_y)
    
    direction = rnd.choice([-1, 1])
    dx = dispersal_x * direction
    direction = rnd.choice([-1, 1])
    dy = dispersal_y * direction
    x_new = int(indiv.x + dx)
    y_new = int((indiv.y + dy) % nrow)  # Wrap around vertically

    if 0 <= x_new < mainland_island.shape[1] and 0 <= y_new < mainland_island.shape[0]:  # Check horizontal boundaries
        if mainland_island[y_new, x_new] != 0:
            canvas.coords(indiv.drawing, (x_new - 0.5) * visual.zoom, (y_new - 0.5) * visual.zoom,
                          (x_new + 0.5) * visual.zoom, (y_new + 0.5) * visual.zoom)
            indiv.x = x_new
            indiv.y = y_new
            return [indiv.x, indiv.y]
    else: 
        return None

visual = Visual(ncol, nrow)
canvas = visual.canvas
community = []


def stop_clock(num_steps, current_time_step, pause_time):
    if current_time_step in (num_steps):        
        time.sleep(pause_time)
         
def update():    
          
    global current_time_step
    global community  # Declare community as a global variable
    #for specie in species_list:    
    for i in species_list:
        #for phase 0 we need more individuals 
        for _ in range(20):        
            x = int(rnd.uniform(0, main)) # they get inizialized in the mainland             
           # if 0 <= x < ncol: i think this is trivial, we know x should be in 0 main
            y = int(rnd.uniform(0, nrow))  # discrete position
            drawing = create_plant(x, y, initial_color='red')
            plant = Plant(x, y, drawing, i)
            community.append(plant)

    
   # create_individuals_mainland()
    update_time_step_label(current_time_step)
    plants_to_remove = []         #offspring    
    
       
    for x in range(len(community)):         
        plant = community[x]
        #now the plant could produce more than 1 seed/ offspring, randomly. i changed it to three. trivial
        num_offspring = rnd.randint(1,3)
        if plant.age>1: 
            for seed in range(num_offspring):     
                position = dispersal(plant) #for now its that parent
                if position != None: #so not out of the x limits
                    x_off = position[0]
                    y_off =position[1] 
                    #i think we already covered this in the definition of dispersal
                    #if x_off <0 or x_off> ncol: #this is because we took of the round wold in the y 
                    #   continue
                    #for the visual output                    
                    drawing_off = create_plant(x_off, y_off, plant.color)
                    #for the community
                    offspring = Plant(x_off, y_off, drawing_off, plant.species)
                    community.append(offspring)  
                    
            if plant.age >= 1:
                #for visual output
                canvas.delete(plant.drawing)
                #for community
                plants_to_remove.append(plant)     
    #simple competition phase 0
    plants_down_for_competition  = competition(community,plants_to_remove)  
    #adding plants lost for competition to list to eliminate 
    plants_to_remove.extend(plants_down_for_competition)
    com_control = community_control(community,nrow,main)
    plants_to_remove.extend(com_control)
    for plant in plants_to_remove:
        canvas.delete(plant.drawing)
        if plant in community:
            community.remove(plant)
        

    for plant in community:
       
        plant.age += 1
     
    print(len(community))    
    
    # Data collection chunk

    #for now i want to know specifically what happens, thats the objective of phase 0
    # so we record data at each time step
    # if current_time_step % 10 == 0:

    #data(community, mainland_island, current_time_step,rep)

    current_time_step += 1
        
    if current_time_step < max_time_steps:
        # Schedule the next update with an interval
        visual.root.after(200, update)
    else:
        # Stop the simulation when we reach the maximum time steps
        print("Simulation finished.")


update()
visual.root.mainloop()
