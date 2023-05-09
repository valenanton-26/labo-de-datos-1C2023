#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:11:54 2023

@author: labo2023
"""

import pandas as pd
import csv
from inline_sql import sql, sql_val

padron = pd.read_csv("~/Descargas/padron-de-operadores-organicos-certificados.csv", encoding='latin-1')
salarios = pd.read_csv("~/Descargas/w_median_depto_priv_clae2.csv")
localidades_censales = pd.read_csv("~/Descargas/localidades-censales.csv")
dic_clases = pd.read_csv("~/Descargas/diccionario_clae2.csv")
dic_dptos = pd.read_csv("~/Descargas/diccionario_cod_depto.csv")

#Normalización

#Padron a 1FN
padron['productos'] = padron['productos'].str.split(',')
padron = padron.explode('productos')
padron['productos'] = padron['productos'].str.split(' Y ')
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

info_localidades = localidades_censales[['id', 'nombre', 'categoria', 'centroide_lat', 'centroide_lon', 'departamento_id']].copy()

#Tabla de municipios

consulta_SQL = """
            SELECT id AS localidad_id, municipio_id, municipio_nombre
            FROM localidades_censales
            WHERE municipio_id IS NOT NULL;
            """
municipios = sql^consulta_SQL

#Salarios a 3FN

#consulta_SQL = """
#            SELECT fecha, codigo_departamento_indec, clae2, COUNT(*) as C
#            FROM salarios
#            GROUP BY fecha, codigo_departamento_indec, clae2;
#            """
#s = sql^consulta_SQL

info_salarios = salarios[['fecha', 'codigo_departamento_indec', 'clae2','w_median']].copy()
info_salarios = info_salarios[info_salarios['w_median']>=0]


#Padron a 3FN

info_padron = padron.copy()
info_padron = info_padron.rename(columns={'razón social' : 'razon_social', 'productos' : 'producto'})
info_padron = info_padron[['departamento', 'establecimiento','razon_social', 'producto', 'rubro','Certificadora_id', 'categoria_id', 'provincia_id']]
info_padron = info_padron.drop_duplicates()

#consulta_SQL = """
#            SELECT rubro, establecimiento, departamento, razon_social, producto, COUNT(*) AS C
#            FROM info_padron
#            GROUP BY rubro, establecimiento, departamento, razon_social, producto
#            ORDER BY C;
            
#            """
#s = sql^consulta_SQL

certificadora = padron[['Certificadora_id', 'certificadora_deno']].copy()

categoria = padron[['categoria_id', 'categoria_desc']].copy()


#Buscamos definir un df que exprese la relación entre rubro y clase

#Creamos una lista con todos los valores posibles que toma rubro, para poder crear un df
rubros = info_padron['rubro'].unique().tolist()
actividades = pd.DataFrame({'Rubro': rubros})

#formo una lista con todos los distintos rubros que se encuentran dentro de la categoría 1
df_productores = info_padron[info_padron['categoria_id']==1]
rubros_productores = df_productores['rubro'].unique().tolist()

#Vemos que todos los elementos de esta lista pertenecen a la clase 1, excepto acuicultura
rubros_clase1 = rubros_productores.remove('ACUICULTURA')
rubros_clase3 = ['ACUICULTURA']

#Ahora, hacemos lo mismo con los rubros de la categoría 2
df_elaboradores = info_padron[info_padron['categoria_id']==2]
rubros_elaboradores = df_elaboradores['rubro'].unique().tolist()

"""
SQL
"""

# ¿Existen provincias que no presentan Operadores Orgánicos Certificados?

consulta_sql = """
                SELECT DISTINCT prov.nombre_provincia_indec AS 'Provincias sin Operadores'
                FROM info_padron AS padron
                RIGHT OUTER JOIN provincias AS prov
                ON padron.provincia_id = prov.id_provincia_indec
                WHERE padron.provincia_id IS NULL;
                """

#¿Existen departamentos que no presentan Operadores Orgánicos Certificados?
                
consulta_sql= """
                SELECT DISTINCT dpto.nombre_departamento_indec AS 'Departamentos sin Operadores'
                FROM info_padron AS padron
                RIGHT OUTER JOIN departamentos AS dpto
                ON padron.departamento = UPPER(dpto.nombre_departamento_indec)
                WHERE padron.departamento IS NULL;
                """
Dptos_sin_operadores = sql^consulta_sql

consulta_sql = """
                SELECT COUNT(*) AS 'Cantidad de departamentos sin Operadores'
                FROM Dptos_sin_operadores;
                """
cant_dptos_sin_operadores = sql^consulta_sql

#¿Cuál es el promedio anual de los salarios en Argentina y cual es su desvío?

consulta_sql = """
                SELECT YEAR(CAST(fecha AS DATE)) AS año, MEAN(w_median) AS salario_promedio, STDDEV(w_median) AS desviacion_estandar_salarios
                FROM info_salarios
                GROUP BY YEAR(CAST(fecha AS DATE))
                ORDER BY año;
                """
prom_y_desv_país = sql^consulta_sql

#A nivel provincial

consulta_sql = """
                SELECT p.nombre_provincia_indec AS provincia, YEAR(CAST(s.fecha AS DATE)) AS año, MEAN(s.w_median) AS salario_promedio, STDDEV(s.w_median) AS desviacion_estandar_salarios
                FROM info_salarios AS s, departamentos AS d, provincias AS p
                WHERE s.codigo_departamento_indec = d.codigo_departamento_indec AND d.id_provincia_indec = p.id_provincia_indec
                GROUP BY p.nombre_provincia_indec, YEAR(CAST(s.fecha AS DATE))
                ORDER BY provincia, año;
                """
prom_y_desv_prov = sql^consulta_sql

print(prom_y_desv_prov)