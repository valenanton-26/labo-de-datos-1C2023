# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
#%% IMPORTS
import csv

#%% VARIABLES Y FUNCIONES GENERALES
nombre_archivo = "arbolado-en-espacios-verdes.csv"

with open(nombre_archivo, 'rt') as file:
    for line in file:
        datos_linea = line.split(',')
        

#%% PUNTO 1
# 
        
def leer_parque(archivo, parque):
    file = open(archivo)
    filas = csv.reader(file)
    encabezado = next(filas)
    dic = []
    for fila in filas :
        if parque in fila:
            reg = dict(zip(encabezado, fila))
            dic.append(reg)
    
    return dic

p = leer_parque(nombre_archivo, "GENERAL PAZ")
print(len(p))

#%% PUNTO 2 