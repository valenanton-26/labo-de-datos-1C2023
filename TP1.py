#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:11:54 2023

@author: labo2023
"""
import pandas as pd
import csv
from inline_sql import sql, sql_val
from unidecode import unidecode

padron = pd.read_csv("~/Descargas/padron-de-operadores-organicos-certificados.csv", encoding='latin-1')
salarios = pd.read_csv("~/Descargas/w_median_depto_priv_clae2.csv")
localidades_censales = pd.read_csv("~/Descargas/localidades-censales.csv")
dic_clases = pd.read_csv("~/Descargas/diccionario_clae2.csv")
dic_dptos = pd.read_csv("~/Descargas/diccionario_cod_depto.csv")

#Normalización
#Defino una función para elimiar las tildes de un string
def eliminar_tildes(s):
    return unidecode(s)

#Padron a 1FN
padron['productos'] = padron['productos'].str.split(',')
padron = padron.explode('productos')
padron['productos'] = padron['productos'].str.split(' Y ')
padron = padron.explode('productos')

#Departamentos a 3FN

provincias = dic_dptos[['id_provincia_indec', 'nombre_provincia_indec']].copy()
provincias =  provincias.drop_duplicates()
provincias = provincias.rename(columns={'id_provincia_indec' : 'id_provincia', 'nombre_provincia_indec' :'nombre_provincia'})


departamentos = dic_dptos[['codigo_departamento_indec', 'nombre_departamento_indec', 'id_provincia_indec']].copy()
departamentos = departamentos.rename(columns={'codigo_departamento_indec' : 'id_depto', 'nombre_departamento_indec' : 'nombre_depto', 'id_provincia_indec' : 'id_provincia'})
departamentos['nombre_depto'] = departamentos['nombre_depto'].apply(eliminar_tildes)

#Clases a 3FN

info_letra = dic_clases[['letra', 'letra_desc']].copy()
info_letra =  info_letra.drop_duplicates()
info_letra['letra_desc'] = info_letra['letra_desc'].apply(eliminar_tildes)

info_clase = dic_clases[['clae2', 'clae2_desc', 'letra']].copy()
info_clase = info_clase.rename(columns={'clae2' : 'id_clase', 'clae2_desc' : 'clase_desc'})
info_clase['clase_desc'] = info_clase['clase_desc'].apply(eliminar_tildes)

#Localidades a 3FN

info_localidades = localidades_censales[['id', 'nombre', 'categoria', 'centroide_lat', 'centroide_lon', 'departamento_id']].copy()
info_localidades['nombre'] = info_localidades['nombre'].apply(eliminar_tildes)

#Tabla de municipios

consulta_SQL = """
            SELECT id AS localidad_id, municipio_id, municipio_nombre
            FROM localidades_censales
            WHERE municipio_id IS NOT NULL;
            """
municipios = sql^consulta_SQL
municipios['municipio_nombre'] = municipios['municipio_nombre'].apply(eliminar_tildes)

#Salarios a 3FN

#consulta_SQL = """
#            SELECT fecha, codigo_departamento_indec, clae2, COUNT(*) as C
#            FROM salarios
#            GROUP BY fecha, codigo_departamento_indec, clae2;
#            """
#s = sql^consulta_SQL

info_salarios = salarios[['fecha', 'codigo_departamento_indec', 'clae2','w_median']].copy()
info_salarios = info_salarios.rename(columns={'codigo_departamento_indec' : 'id_depto', 'clae2' : 'id_clase', 'w_median' : 'salario'})
info_salarios = info_salarios[info_salarios['salario']>=0]

#Padron a 3FN

info_padron = padron.copy()
info_padron = info_padron.rename(columns={'razón social' : 'razon_social', 'productos' : 'producto'})
info_padron = info_padron[['departamento', 'establecimiento','razon_social', 'producto', 'rubro','Certificadora_id', 'categoria_id', 'provincia_id']]
info_padron = info_padron.drop_duplicates()
info_padron['departamento'] = info_padron['departamento'].apply(eliminar_tildes)


certificadora = padron[['Certificadora_id', 'certificadora_deno']].copy()

categoria = padron[['categoria_id', 'categoria_desc']].copy()


#Buscamos los departamentos que figuran en padron que no están registrados como departamentos en el diccionario
consulta_sql = """
                SELECT DISTINCT p.departamento, p.provincia_id
                FROM departamentos AS d
                RIGHT OUTER JOIN info_padron AS p
                ON p.departamento = UPPER(d.nombre_depto)
                WHERE d.id_depto IS NULL;
                """
no_departamentos = sql^consulta_sql

#Verificamos si alguno de estos departamentos es localidad
consulta_sql = """
                SELECT DISTINCT nd.departamento AS localidad
                FROM no_departamentos AS nd, info_localidades AS l
                WHERE nd.departamento = UPPER(l.nombre);
                """
son_localidades = sql^consulta_sql

#Asignamos a estas localidades los id de dpto y provincia correspondientes
consulta_sql = """
                SELECT DISTINCT sl.localidad, l.departamento_id, d.id_provincia
                FROM son_localidades AS sl, info_localidades AS l, departamentos AS d
                WHERE sl.localidad = UPPER(l.nombre) AND l.departamento_id = d.id_depto
                ORDER BY localidad;
                """
loc_y_deptos = sql^consulta_sql

#Saque las localidades con mismo nombre y provincia, pero departamento distinto.
consulta_sql = """
                SELECT DISTINCT *
                FROM loc_y_deptos AS l1
                WHERE NOT EXISTS (
                        SELECT *
                        FROM loc_y_deptos AS l2
                        WHERE l1.localidad = l2.localidad AND l1.id_provincia = l2.id_provincia AND NOT l1.departamento_id = l2.departamento_id)
                ORDER BY localidad;
                """

loc_deptos = sql^consulta_sql

#Ahora, busco obtener el df dentro de info_padron con la información 
#de los establecimientos que tienen cargada una localidad como nombre de departamento
consulta_sql = """
                SELECT l.departamento_id, p.establecimiento, p.razon_social, p.producto, p.rubro, p.Certificadora_id, p.categoria_id, p.provincia_id
                FROM info_padron AS p, loc_deptos AS l
                WHERE p.departamento = l.localidad AND p.provincia_id = l.id_provincia
                ORDER BY departamento_id;
"""
info_padron_A = sql^consulta_sql

#Ahora verificamos si los departamentos que no fueron identificados como localidad, son municipios
#Primero busco obtener una serie de los que no fueron identificados como localidad

consulta_sql = """
                SELECT DISTINCT nd.departamento AS no_departamento, nd.provincia_id
                FROM no_departamentos AS nd
                LEFT OUTER JOIN info_localidades AS l
                ON nd.departamento = UPPER(l.nombre)
                WHERE l.nombre IS NULL;
"""
no_localidades = sql^consulta_sql
#Verifico si alguno de ellos es un municipio y, mediante su provincia y localidad, lo asocio a su departamento
consulta_sql = """
                SELECT DISTINCT nl.no_departamento AS municipio, nl.provincia_id, d.id_depto
                FROM no_localidades AS nl, municipios AS m, info_localidades AS l, departamentos AS d
                WHERE nl.no_departamento = UPPER(m.municipio_nombre)
                AND m.localidad_id = l.id AND l.departamento_id = d.id_depto
                AND nl.provincia_id = d.id_provincia
                ORDER BY municipio;
                """
son_municipios = sql^consulta_sql

#Ahora, busco obtener el df dentro de info_padron con la información 
#de los establecimientos que tienen cargado un municipio como nombre de departamento
consulta_sql = """
                SELECT m.id_depto AS departamento_id, p.establecimiento, p.razon_social, p.producto, p.rubro, p.Certificadora_id, p.categoria_id, p.provincia_id
                FROM info_padron AS p, son_municipios AS m
                WHERE p.departamento = m.municipio AND p.provincia_id = m.provincia_id
                ORDER BY departamento_id;
"""
info_padron_B = sql^consulta_sql

#Ahora vamos obtener un df de las filas en info_padron que tienen el dato de departamento correctamente cargado
#lo vamos a relacionar con su id de departamento y organizarlo de la misma manera que los dos padrones anteriores, para luego poder unirlos

consulta_sql = """
                SELECT d.id_depto AS departamento_id, p.establecimiento, p.razon_social, p.producto, p.rubro, p.Certificadora_id, p.categoria_id, p.provincia_id
                FROM info_padron AS p, departamentos AS d
                WHERE p.departamento = UPPER(d.nombre_depto) AND p.provincia_id = d.id_provincia
                ORDER BY departamento, id_depto;
"""
info_padron_C = sql^consulta_sql

#Finalmente, unimos las 3 tablas para definir el df final con el que vamos a trabajar
consulta_sql = """
                SELECT DISTINCT *
                FROM info_padron_A
                UNION
                SELECT DISTINCT *
                FROM info_padron_B
                UNION
                SELECT DISTINCT *
                FROM info_padron_C;
"""
df_padron0 = sql^consulta_sql


#Buscamos definir un df que exprese la relación entre rubro y clase
#Vemos primero que todos los Operadores de la categoría 3 tienen su rubro como 'SIN DEFINIR' 
#Decidimos completar la columna rubro con 'COMERCIALIZADORES'

consulta_sql = """
                SELECT departamento_id, establecimiento, razon_social, producto, Certificadora_id, categoria_id, provincia_id, REPLACE(rubro, 'SIN DEFINIR', 'COMERCIALIZADORES') AS rubro
                FROM df_padron0;
"""
df_padron = sql^consulta_sql

#formo una lista con todos los distintos rubros que se encuentran dentro de la categoría 1
df_productores = df_padron[df_padron['categoria_id']==1]
rubros_productores = df_productores['rubro'].unique().tolist()

#Vemos que todos los elementos de esta lista pertenecen a la clase 1. 
#Creamos un df correspondiente a los rubros de la clase 1
rubros_clase1 = rubros_productores
df_clase1 = pd.DataFrame({'rubro': rubros_clase1, 'clase': '1'})

#Ahora, hacemos lo mismo con los rubros de la categoría 2
df_elaboradores = df_padron[df_padron['categoria_id']==2]
rubros_elaboradores = df_elaboradores['rubro'].unique().tolist()

#Defino los rubros de clase 13 y clase 21 
rubros_clase13 = ['PROCESAMIENTO TEXTIL']
rubros_clase21 = ['PRODUCTOS PARA EL CUIDADO PERSONAL', 'ELABORACION , FRACCIONAMIENTO Y DEPOSITO DE HIERBAS AROMATICAS Y MEDICINALES', 'ELABORACION DE ACEITE DE ROSA MOSQUETA']

#Armo una lista con los rubros pertenecientes a la clase 11
rubros_clase11 = []
palabras_clave = ['JUGO', 'VITIVINICOLA', 'MOSTO', 'VINO', 'VID'] 
for l in rubros_elaboradores:
    for p in palabras_clave:
        if p in l:
            rubros_clase11.append(l)
            
#Defino los rubros de la clase 10 eliminando de la lista original
#los rubros que ya se encuentran definidos dentro de otras clases
rubros_clase10 = []
for l in rubros_elaboradores:
    if l not in rubros_clase13 and l not in rubros_clase21 and l not in rubros_clase11:
        rubros_clase10.append(l)

#Ahora, creamos un df para cada una de las clases
df_clase10 = pd.DataFrame({'rubro': rubros_clase10, 'clase': '10'})
df_clase11 = pd.DataFrame({'rubro': rubros_clase11, 'clase': '11'})
df_clase13 = pd.DataFrame({'rubro': rubros_clase13, 'clase': '13'})
df_clase21 = pd.DataFrame({'rubro': rubros_clase21, 'clase': '21'})

#En el caso de la categoría 3, por el reemplazo que realizamos, sabemos que el rubro será 'COMERCIALIZADORES'
#Decidimos ubicar este rubro dentro de la clase 46
df_clase46 = df_clase46 = pd.DataFrame({'rubro': ['COMERCIALIZADORES'], 'clase': '46'})

#La relación final será el resultado de la unión de todas estas tablas
consulta_sql = """
                SELECT DISTINCT *
                FROM df_clase1
                WHERE rubro IS NOT NULL
                UNION
                SELECT DISTINCT *
                FROM df_clase10
                UNION
                SELECT DISTINCT *
                FROM df_clase11
                UNION
                SELECT DISTINCT *
                FROM df_clase13
                UNION
                SELECT DISTINCT *
                FROM df_clase21
                UNION
                SELECT DISTINCT *
                FROM df_clase46
                ORDER BY clase;
""" 
actividades = sql^consulta_sql

"""
SQL
"""

# ¿Existen provincias que no presentan Operadores Orgánicos Certificados?

consulta_sql = """
                SELECT DISTINCT prov.nombre_provincia AS 'Provincias sin Operadores'
                FROM df_padron AS padron
                RIGHT OUTER JOIN provincias AS prov
                ON padron.provincia_id = prov.id_provincia
                WHERE padron.provincia_id IS NULL;
                """

#¿Existen departamentos que no presentan Operadores Orgánicos Certificados?
                
consulta_sql= """
                SELECT DISTINCT dpto.nombre_depto AS 'Departamentos sin Operadores'
                FROM df_padron AS padron
                RIGHT OUTER JOIN departamentos AS dpto
                ON padron.departamento_id = dpto.id_depto
                WHERE padron.departamento_id IS NULL;
                """
Dptos_sin_operadores = sql^consulta_sql

consulta_sql = """
                SELECT COUNT(*) AS 'Cantidad de departamentos sin Operadores'
                FROM Dptos_sin_operadores;
                """
cant_dptos_sin_operadores = sql^consulta_sql

#¿Cuál es la actividad que más operadores tiene?
consulta_sql = """
                SELECT a.clase, COUNT(*) AS cantidad_de_operadores
                FROM df_padron AS p, actividades AS a, info_clase AS c
                WHERE p.rubro = a.rubro AND a.clase = c.id_clase
                GROUP BY a.clase
                ;
                
"""
cant_operadores = sql^consulta_sql

consulta_sql = """
                SELECT clase, cantidad_de_operadores
                FROM cant_operadores
                WHERE cantidad_de_operadores = (
                                                SELECT MAX(cantidad_de_operadores)
                                                FROM cant_operadores
                                                )
                ;
"""
max_cant_operadores = sql^consulta_sql

#¿Cuál es el promedio anual de los salarios en Argentina y cual es su desvío?

consulta_sql = """
                SELECT YEAR(CAST(fecha AS DATE)) AS año, MEAN(salario) AS salario_promedio, STDDEV(salario) AS desviacion_estandar_salarios
                FROM info_salarios
                GROUP BY YEAR(CAST(fecha AS DATE))
                ORDER BY año;
                """
prom_y_desv_país = sql^consulta_sql

#A nivel provincial

consulta_sql = """
                SELECT p.nombre_provincia AS provincia, YEAR(CAST(s.fecha AS DATE)) AS año, MEAN(s.salario) AS salario_promedio, STDDEV(s.salario) AS desviacion_estandar_salarios
                FROM info_salarios AS s, departamentos AS d, provincias AS p
                WHERE s.id_depto = d.id_depto AND d.id_provincia = p.id_provincia
                GROUP BY p.nombre_provincia, YEAR(CAST(s.fecha AS DATE))
                ORDER BY provincia, año;
                """
prom_y_desv_prov = sql^consulta_sql
