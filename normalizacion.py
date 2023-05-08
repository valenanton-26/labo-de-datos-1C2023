#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:14:05 2023

@author: labo2023
"""

import pandas as pd
import csv

padron = pd.read_csv("~/Descargas/padron-de-operadores-organicos-certificados.csv", encoding = 'latin-1')

#Normalizacion

padron['productos'] = padron['productos'].str.split(',')
padron['productos'] = padron['productos'].str.split('-')
padron['productos'] = ¨padron['productos'].str.split('Y')


