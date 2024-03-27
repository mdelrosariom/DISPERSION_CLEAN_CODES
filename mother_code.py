# -*- coding: utf-8 -*-

import random as rnd
import tkinter as tk
import numpy as np
import math as math
from PIL import ImageGrab #to take snaps of the tk 


#my functions 
from simple_landscape import simple_landscape
from landscape_fixed_insolation_area import landscape_fixed_insolation_area
from adaptation import adapt 
from niche_construction import niche_construction
from niche_positioning import niche
from comp import competence
from list_of_species import list_of_species
from species_colors import color_species
from species_disp import dispersion_species
#GLOBAL VARIABLES RELATED TO LANDSCAPE 


nrow = ncol = 50
size = 1/4
main = ncol // 2
shape = 0
current_time_step = 0


species_list = list_of_species(10)
species_colors = color_species(species_list)
# time steps of the simulation
max_time_steps = 1000 


niches = niche_construction(species_list, 10,5,3)
niche_mainland = niches[0]
niche_island = niches[1]
#to create niches for all of the plants
for i in range(2, len(niches)):
    sp_num = i - 1    
    name_of_species = "niche_sp" + str(sp_num)
    globals()[name_of_species] = niches[i]

species_dispersal = dispersion_species(species_list, main)
#mainland_island = simple_landscape(nrow, ncol, size, shape)
mainland_island = landscape_fixed_insolation_area(nrow, ncol, size, shape, 'medium')
species_list_stable = species_list[:]
species_colors_dict = dict(zip(species_list_stable, species_colors))
species_niches_dict = dict(zip(species_list_stable, niches))
species_disp_dict = dict(zip(species_list_stable, species_dispersal))

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

def save_as_image(filename):
    # Capture the screen of the Tkinter application
    x = visual.winfo_rootx()
    y = visual.winfo_rooty()
    w = visual.winfo_width()
    h = visual.winfo_height()
    img = ImageGrab.grab(bbox=(x, y, x + w, y + h))

    # Save the captured screen as an image
    img.save(filename)


def update():
      
    global current_time_step
    global population  # Declare population as a global variable
    #for specie in species_list:
    for i in species_list:        
        for _ in range(2):        
            x = int(rnd.uniform(0, ncol//2))  # they get inizialized in the mainland 
            y = int(rnd.uniform(0, nrow))  # discrete mov
            drawing = create_plant(x, y, initial_color='red')        
           
            plant = Plant(x, y, drawing, i)             
            population.append(plant)

    
   # create_individuals_mainland()
   
    plants_to_remove = []         #offspring    

    for x in range(len(population)): 
        
        plant = population[x]
        num_offspring = rnd.randint(1,4) #now the plant could produce more than 1 seed/ offspring, randomly 
        if plant.age>1: 
            for seed in range(num_offspring):        
               
                position = dispersal(plant) #for now its that parent
                if position != None: 
                    x_off = position[0]
                    y_off =position[1] 
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


