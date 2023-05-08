#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:14:05 2023

@author: labo2023
"""

import pandas as pd
import csv

padron = pd.read_csv("~/Descargas/padron-de-operadores-organicos-certificados.csv", encoding='latin-1')
salarios = pd.read_csv("~/Descargas/w_median_depto_priv_clae2.csv")
localidades = pd.read_csv("~/Descargas/localidades-censales.csv")
dic_clases = pd.read_csv("~/Descargas/diccionario_clae2.csv")
dic_dptos = pd.read_csv("~/Descargas/diccionario_cod_depto.csv")

#Normalización

#Padron a 1FN
padron['productos'] = padron['productos'].str.split(',')
padron['productos'] = padron['productos'].str.split('Y')
padron = padron.explode('productos')

#Departamentos a 3FN

provincias = dic_dptos[['id_provincia_indec', 'nombre_provincia_indec']].copy()
provincias =  provincias.drop_duplicates()

departamentos = dic_dptos[['codigo_departamento_indec', 'nombre_departamento_indec', 'id_provincia_indec']].copy()

#Clases a 3FN

info_letra = dic_clases[['letra', 'letra_desc']].copy()
info_letra =  info_letra.drop_duplicates()

info_clase = dic_clases[['clae2', 'clae2_desc', 'letra']].copy()

#Localidades a 3FN



print(info_clase)
