# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 11:12:18 2024

@author: mdrmi-modifeid 17/04/2025
"""
import random as rnd

def color_species(species_list):
    '''
    Gives different colors to different species. For visual output.
    '''
    unique_species = set(species_list)
    colors = set()

    while len(colors) < len(unique_species):
        c = '#%06X' % rnd.randint(0, 0xFFFFFF)
        colors.add(c)

    return list(colors)
