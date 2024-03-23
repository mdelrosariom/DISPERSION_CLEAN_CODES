# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 11:12:18 2024

@author: mdrmi
"""
import random as rnd

def color_species(species_list):
    colors = []
    
    for i in range(len(species_list)):
        colors.append('#%06X' % rnd.randint(0, 0xFFFFFF))
        
    return(colors)