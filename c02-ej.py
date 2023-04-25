#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 09:52:11 2023

@author: clinux01
"""
import random
import csv

#%% GENERALA
def generala_tirar():
    lista = []
    for i in range(5):
        lista.append(random.randrange(1,7))
    return lista

print(generala_tirar())

#%% DATAME

def filtro_palabras(palabra):
    with open("datame.txt", 'rt', encoding='utf-8') as file:
        for line in file:
            if palabra in line:
                print(line)
            
filtro_palabras("estudiante")

#%% CRONOGRAMA
nombre_archivo = 'cronograma_sugerido.csv'

def lista_materias(nombre):
    with open(nombre, 'rt', encoding='utf-8') as file:
        for line in file:
            datos_linea = line.split(',')
            print(datos_linea[1])


lista_materias(nombre_archivo)
#%% CUANTAS MATERIAS
def cantidad_materias(cuatri):
    cantidad = 0
    with open(nombre_archivo, 'rt', encoding='utf-8') as file:
        for line in file:
            datos = line.split(',')
            if datos[0] == cuatri:
                cantidad += 1
                
    return cantidad

print(cantidad_materias("5"))
print(cantidad_materias("7"))
#%% MATERIAS POR CUATRI
def materias_cuatrimestre(nombre, cuatri):
    lista = []
    with open(nombre, 'rt', encoding='utf-8') as file:
        filas = csv.reader(file)
        encabezado = next(filas)

        for fila in filas:
            
            if fila[0] == cuatri:
                reg = dict(zip(encabezado, fila))
                lista.append(reg)

    return lista

print(materias_cuatrimestre(nombre_archivo, "3"))
