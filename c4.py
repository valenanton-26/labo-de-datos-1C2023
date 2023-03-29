#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:14:40 2023

@author: labo2023
"""
import pandas as pd
import os

nombre = "Actividad-01-datos.csv"

# abrir el archivo como un data frame con panda
fname = os.path.join(nombre)
df = pd.read_csv(fname)

conj_muni = df["municipio"].unique() #crea un conjunto

def cant_muni():
    dic = {}
    for m in conj_muni:
        cant = (df["municipio"] == m).sum() #suma la cantidad de elementos
        dic[m] = cant
    return dic

#%% MOVILIDAD
    
nombre2 = "EncuestaMovilidadRespuestas.csv"

fname2 = os.path.join(nombre2)
df2 = pd.read_csv(fname2)

# opc 1
conj_tra = set(df2.iloc[:,5])

def cant_tra():
    dic = {}
    for m in conj_tra:
        cant = (df2.iloc[:,5] == m).sum() #suma la cantidad de elementos
        dic[m] = cant
    return dic

#print(cant_tra())

# opc 2
maximo = df2.iloc[:,5].value_counts().idxmin()
print(maximo)