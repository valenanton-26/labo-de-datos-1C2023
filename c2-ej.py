#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 09:52:11 2023

@author: clinux01
"""
import random
#%% GENERALA
def generala_tirar():
    lista = []
    for i in range(5):
        lista.append(random.randrange(1,7))
    return lista

print(generala_tirar())

#%% DATAME

def filtro_palabras(palabra):
    with open("datame.txt", 'rt') as file:
    for line in file:
        if palabra in line:
            print(line)
            
filtro_palabras("estudiante)

#%% CRONOGRAMA

#%% CUANTAS MATERIAS

#%% MATERIAS POR CUATRI