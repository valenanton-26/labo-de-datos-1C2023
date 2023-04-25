# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 21:39:50 2023

@author: Valen
"""

#%% IMPORTS

import pandas as pd
from inline_sql import sql, sql_val

datos = pd.read_csv("C:/Users/Valen/Documents/FACULTAD/LABO DE DATOS/LDC codigo/DatosDengueYZikaCorregida.csv")   
#%% EJERCICIO A
# a : listar nombres de departamentos (dejando repetidos)

consultaSQL = """
               SELECT departamento_nombre
               FROM datos
              """
nombres_deptos = sql^ consultaSQL
print(nombres_deptos)  

# b : listar nombres de departamentos (sin repetidos)
consultaSQL = """
               SELECT DISTINCT departamento_nombre
               FROM datos
              """
nombres_deptos = sql^ consultaSQL
print(nombres_deptos)   

# c : Listar sólo los códigos de departamento y sus nombres de todos los departamentos 
consultaSQL = """
               SELECT DISTINCT departamento_nombre AS nombre, departamento_id AS codigo
               FROM datos
              """
nombres_deptos = sql^ consultaSQL
print(nombres_deptos)   

# d : listar todas las columnas de la tabla departamento  
consultaSQL = """
               SELECT DISTINCT  departamento_id AS id, departamento_nombre AS descripcion, 
                   provincia_id AS id_provincia
               FROM datos
              """
deptos = sql^ consultaSQL
print(deptos)   

# e : listar todas las columnas de la tabla departamento  
consultaSQL = """
               SELECT DISTINCT  departamento_id AS codigo_depto, departamento_nombre AS nombre_depto, 
                   provincia_id AS id_provincia
               FROM datos
              """
deptos = sql^ consultaSQL
print(deptos)   

# f = Listar los códigos de departamento y sus nombres, ordenados por sus nombres de manera 
# descendentes. En caso de empate, desempatar por código de departamento de manera ascendente.
consultaSQL = """
               SELECT DISTINCT  departamento_id AS codigo_depto, 
                   departamento_nombre AS nombre_depto
               FROM datos
               ORDER BY nombre_depto DESC, codigo_depto ASC
              """
deptos = sql^ consultaSQL
print(deptos)   

# g = Listar los registros de la tabla departamento cuyo código de provincia es igual a 54
consultaSQL = """
               SELECT DISTINCT  departamento_id AS codigo_depto, 
                   departamento_nombre AS nombre_depto
               FROM datos
               WHERE provincia_id = 54
              """
deptos = sql^ consultaSQL
print(deptos)  

# h = Listar los registros de la tabla departamento cuyo código de provincia es 22, 78 u 86.
consultaSQL = """
               SELECT DISTINCT  departamento_id AS codigo_depto, 
                   departamento_nombre AS nombre_depto
               FROM datos
               WHERE provincia_id = 54 OR provincia_id = 78 OR provincia_id = 86 
              """
deptos = sql^ consultaSQL
print(deptos)  

# i = Listar los registros de la tabla departamento cuyo código de provincia es esta entre 50 y 59 inclusive
consultaSQL = """
               SELECT DISTINCT  departamento_id AS codigo_depto, 
                   departamento_nombre AS nombre_depto , provincia_id
               FROM datos
               WHERE provincia_id >= 50 AND provincia_id<=59 
              """
deptos = sql^ consultaSQL
print(deptos)  

# j = Listar los registros de la tabla provincia cuyos nombres comiencen con la letra M.
consultaSQL = """
               SELECT DISTINCT provincia_id,  provincia_nombre
               FROM datos
               WHERE provincia_nombre LIKE 'M%' 
              """
deptos = sql^ consultaSQL
print(deptos) 

# k = Listar los registros de la tabla provincia cuyos nombres comiencen con la
# letra S y su quinta letra sea una letra A
consultaSQL = """
               SELECT DISTINCT provincia_id,  provincia_nombre
               FROM datos
               WHERE (provincia_nombre LIKE 'S%' ) AND (provincia_nombre LIKE '____a%' )
              """
deptos = sql^ consultaSQL
print(deptos) 

# l = Listar los registros de la tabla provincia cuyos nombres terminan con la letra A.
consultaSQL = """
               SELECT DISTINCT provincia_id,  provincia_nombre
               FROM datos
               WHERE (provincia_nombre LIKE '%A' )
              """
deptos = sql^ consultaSQL
print(deptos)

# m = Listar los registros de la tabla provincia cuyos nombres tengan exactamente 5 letras.
consultaSQL = """
               SELECT DISTINCT provincia_id,  provincia_nombre
               FROM datos
               WHERE (provincia_nombre LIKE '_____' )
              """
deptos = sql^ consultaSQL
print(deptos) 

# n = Listar los registros de la tabla provincia cuyos nombres tengan ”do” en alguna parte de su nombre
consultaSQL = """
               SELECT DISTINCT provincia_id,  provincia_nombre
               FROM datos
               WHERE (provincia_nombre LIKE '%do%' )
              """
deptos = sql^ consultaSQL
print(deptos)

# o = Listar los registros de la tabla provincia cuyos nombres tengan ”do” en alguna parte de su nombre 
# y su codigo sea menor a 30
consultaSQL = """
               SELECT DISTINCT provincia_id,  provincia_nombre
               FROM datos
               WHERE (provincia_nombre LIKE '%do%' ) AND ( provincia_id < 30 )
              """
deptos = sql^ consultaSQL
print(deptos)

# P = Listar los registros de la tabla departamento cuyos nombres tengan ”san” en alguna parte de su nombre. 
# Listar sólo id y descripcion. Utilizar los siguientes alias para las columnas: codigo_depto y nombre_depto,
# respectivamente. El resultado debe estar ordenado por sus nombres de manera descendentes (de la Z a la A).
consultaSQL = """
               SELECT DISTINCT  departamento_id AS codigo_depto, 
                   departamento_nombre AS nombre_depto
               FROM datos
               WHERE (nombre_depto LIKE '%San%' )
               ORDER BY nombre_depto DESC
              """
deptos = sql^ consultaSQL
print(deptos)   


#%% EJERCICIO B

# a. Devolver una lista con los código y nombres de departamentos, asociados al nombre de la provincia
#    al que pertenecen.






#%% EJERCICIO C

#%% EJERCICIO D

#%% EJERCICIO E

#%% EJERCICIO F

#%% EJERCICIO G

#%% EJERCICIO H






