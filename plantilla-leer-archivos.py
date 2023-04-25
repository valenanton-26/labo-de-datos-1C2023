# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 21:29:08 2023

@author: Valen
"""

# Importamos bibliotecas
import pandas as pd
from inline_sql import sql, sql_val

# leer el archivo
nombreArchivo      = pd.read_csv("~/Descargas/vuelo.csv")   

# funcion para imprimir mas lindos los ejercicios
def imprimirEjercicio(consigna, listaDeDataframesDeEntrada, consultaSQL):
    
    print("# -----------------------------------------------------------------------------")
    print("# Consigna: ", consigna)
    print("# -----------------------------------------------------------------------------")
    print()
    for i in range(len(listaDeDataframesDeEntrada)):
        print("# Entrada 0",i,sep='')
        print("# -----------")
        print(listaDeDataframesDeEntrada[i])
        print()
    print("# SQL:")
    print("# ----")
    print(consultaSQL)
    print()
    print("# Salida:")
    print("# -------")
    print(sql^ consultaSQL)
    print()
    print("# -----------------------------------------------------------------------------")
    print("# -----------------------------------------------------------------------------")
    print()
    print()
    
    
# OPCIONES DE LECTURA DE LA CONSULTA
# 1
consigna    = "Còdigo y nombre de los aeropuertos de Londres "
consultaSQL = """
               SELECT DISTINCT Codigo, Nombre
               FROM aeropuerto
               WHERE Ciudad = 'Londres'
              """
imprimirEjercicio(consigna, [nombreArchivo], consultaSQL) 

# 2
datosEstudiantes = sql^ consultaSQL
print(datosEstudiantes)   