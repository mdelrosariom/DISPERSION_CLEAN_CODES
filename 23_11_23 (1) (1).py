# -*- coding: utf-8 -*-

import random as rnd
import tkinter as tk
import numpy as np
import math as math
#my functions 

from simple_landscape import simple_landscape
from adaptation import adapt 
from niche_construction import niche_construction
from niche_positioning import niche
from comp import competence
nrow = ncol = 20
size = 1/4
main = ncol // 2
shape = 0
time_of_adaptation =5 #the adaptation will occur if the time step is multiple of this number
current_time_step = 0


species_list= ["sp_1", "sp_2"]

# time steps of the simulation
max_time_steps = 10  


niches = niche_construction([1,2], 10,5,3)
niche_mainland = niches[0]
niche_island =niches[1]
niche_sp1 = niches[2]
niche_sp2 = niches[3]

mainland_island = simple_landscape(nrow, ncol, size, shape)

class Visual:
    def __init__(self, max_x, max_y):
        self.zoom = 15
        self.max_x = max_x
        self.max_y = max_y
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=max_x * self.zoom, height=max_y * self.zoom)
        self.canvas.pack()
        self.canvas.config(background='royalblue')
        self.squares = np.empty((self.max_x, self.max_y), dtype=object)
        self.initialize_squares()

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

class Plant:
    def __init__(self, x, y, drawing, specie):
        self.x = x
        self.y = y
        self.drawing = drawing
        self.age = 0
        self.pos = [x,y]
        self.disp_cap = rnd.randint(2,main) #for now random, after we can define diferent species based on this
        self.specie = specie
        if specie == "sp_1": 
            self.color = 'forestgreen'
            self.niche = niche_sp1
        if specie == "sp_2": 
            self.color = 'blue'
            self.niche = niche_sp2
        self.comp_ab = rnd.random()
        

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


def dispersal(indiv):
       
 #I will use the gaussian for dispersal because its simple and commonly used in dispersal 
 #studies 
    dispersal_x = np.random.normal(indiv.disp_cap, 1) #standar derivation common 1 
    dispersal_y = np.random.normal(indiv.disp_cap, 1)    
    #a chunck so the seed can be dispersed also to left and down
    direction = rnd.choice([-1, 1])
    dx = dispersal_x*direction
    direction = rnd.choice([-1, 1])
    dy = dispersal_y*direction    
    x_new = int((indiv.x + dx) % nrow) #%nrow module to wrap up the world 
    y_new = int((indiv.y + dy) % ncol) #%nrow module to wrap up the world 

    if mainland_island[int(y_new), int(x_new)] != 0:
        canvas.coords(indiv.drawing, (x_new - 0.5) * visual.zoom, (y_new - 0.5) * visual.zoom,
                      (x_new + 0.5) * visual.zoom, (y_new + 0.5) * visual.zoom)
        indiv.x = x_new
        indiv.y = y_new       

        return ([indiv.x, indiv.y])
    else: 
        pass

visual = Visual(ncol, nrow)
canvas = visual.canvas
population = []

# Create individuals only on the mainland
for specie in species_list:
    for _ in range(50):
    
        x = int(rnd.uniform(0, main))  # discrete mov
        y = int(rnd.uniform(0, nrow))  # discrete mov
        drawing = create_plant(x, y, initial_color='red')
        plant = Plant(x, y, drawing, specie)
        population.append(plant)

def update():
    global current_time_step
    global population  # Declare population as a global variable
   
    plants_to_remove = []         #offspring    

    for x in range(len(population)): 
        plant = population[x]
        num_offspring = rnd.randint(1,4) #now the plant could produce more than 1 seed/ offspring, randomly 
        for seed in range(num_offspring):        
           
            position = dispersal(plant) #for now its that parent
            if position != None: 
                x_off = position[0]
                y_off =position[1]                   
                drawing_off = create_plant(x_off, y_off, plant.color)
                offspring = Plant(x_off, y_off, drawing_off, plant.specie)
                possibility_of_adaptation = rnd.choice([1,2])
                if possibility_of_adaptation ==2:               
                    if mainland_island[offspring.x][offspring.y] >1: #23 11 23 correction so occurs in future islands #== 2: #adaptation occur in islands
                        offspring.niche = adapt(environmental_niche[offspring.x][offspring.y],plant.niche, "natural_selection", "yes")
                population.append(offspring)     
                          
   
    for plant in population:
        if plant.age >= 1:
            canvas.delete(plant.drawing)
            plants_to_remove.append(plant)     

    for plant in population: 
        if mainland_island[plant.x][plant.y] > 1:  # Only consider islands #this is in the case we build multiple islands in the future
            if not set(environmental_niche[plant.x][plant.y]) & set(plant.niche):
                canvas.delete(plant.drawing)
                plants_to_remove.append(plant)
            
    plants_to_remove = competence(population, environmental_niche, plants_to_remove)
  
                    
    population = [plant for plant in population if plant not in plants_to_remove]

    for plant in plants_to_remove:
        canvas.delete(plant.drawing)

    for plant in population:
       
        plant.age += 1
     
    print(len(population))
    current_time_step += 1
    if current_time_step < max_time_steps:
        # Schedule the next update with an interval
        visual.root.after(200, update)
    else:
        # Stop the simulation when we reach the maximum time steps
        print("Simulation finished.")

update()
visual.root.mainloop()


