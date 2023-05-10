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
provincias = provincias.rename(columns={'id_provincia_indec' : 'id_provincia', 'nombre_provincia_indec' :'nombre_provincia'})

departamentos = dic_dptos[['codigo_departamento_indec', 'nombre_departamento_indec', 'id_provincia_indec']].copy()
departamentos = departamentos.rename(columns={'codigo_departamento_indec' : 'id_depto', 'nombre_departamento_indec' : 'nombre_depto', 'id_provincia_indec' : 'id_provincia'})
#Clases a 3FN

info_letra = dic_clases[['letra', 'letra_desc']].copy()
info_letra =  info_letra.drop_duplicates()

info_clase = dic_clases[['clae2', 'clae2_desc', 'letra']].copy()
info_clase = info_clase.rename(columns={'clae2' : 'id_clase', 'clae2_desc' : 'clase_desc'})

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
info_salarios = info_salarios.rename(columns={'codigo_departamento_indec' : 'id_depto', 'clae2' : 'id_clase', 'w_median' : 'salario'})
info_salarios = info_salarios[info_salarios['salario']>=0]


#Padron a 3FN

info_padron = padron.copy()
info_padron = info_padron.rename(columns={'razón social' : 'razon_social', 'productos' : 'producto'})
info_padron = info_padron[['departamento', 'establecimiento','razon_social', 'producto', 'rubro','Certificadora_id', 'categoria_id', 'provincia_id']]
info_padron = info_padron.drop_duplicates()


#Buscamos los departamentos que figuran en padron que no están registrados como departamentos en el diccionario
consulta_sql = """
                SELECT DISTINCT p.departamento
                FROM departamentos AS d
                RIGHT OUTER JOIN info_padron AS p
                ON p.departamento = UPPER(d.nombre_depto)
                WHERE d.id_depto IS NULL;
                """
no_departamentos = sql^consulta_sql
print(no_departamentos)

#Verificamos si alguno de estos departamentos es localidad
consulta_sql = """
                SELECT DISTINCT nd.departamento AS localidad
                FROM no_departamentos AS nd, info_localidades AS l
                WHERE nd.departamento = UPPER(l.nombre);
                """
son_localidades = sql^consulta_sql

#Asignamos a estas localidades el id del dpto correspondiente
consulta_sql = """
                SELECT DISTINCT sl.localidad, l.departamento_id, d.nombre_depto
                FROM son_localidades AS sl, info_localidades AS l, departamentos AS d
                WHERE sl.localidad = UPPER(l.nombre) AND l.departamento_id = d.id_depto;
                """
loc_y_deptos = sql^consulta_sql

#Remplazamos esta información en el df info_padron


certificadora = padron[['Certificadora_id', 'certificadora_deno']].copy()

categoria = padron[['categoria_id', 'categoria_desc']].copy()


#Buscamos definir un df que exprese la relación entre rubro y clase

#Creamos una lista con todos los valores posibles que toma rubro, para poder crear un df
rubros = info_padron['rubro'].unique().tolist()
actividades = pd.DataFrame({'rubro': rubros})

#formo una lista con todos los distintos rubros que se encuentran dentro de la categoría 1
df_productores = info_padron[info_padron['categoria_id']==1]
rubros_productores = df_productores['rubro'].unique().tolist()

#Vemos que todos los elementos de esta lista pertenecen a la clase 1, excepto acuicultura
rubros_productores.remove('ACUICULTURA')
rubros_clase1 = rubros_productores
rubros_clase3 = ['ACUICULTURA']

#Ahora, hacemos lo mismo con los rubros de la categoría 2
df_elaboradores = info_padron[info_padron['categoria_id']==2]
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
            
#Ahora defino los rubros de la clase 10 eliminando de la lista original
#los rubros que ya se encuentran definidos dentro de otras clases
rubros_clase10 = []
for l in rubros_elaboradores:
    if l not in rubros_clase13 and l not in rubros_clase21 and l not in rubros_clase11:
        rubros_clase10.append(l)

#Ahora, agregamos el valor de la columna 'Clase' al df creado
actividades['clase'] = ''
i = 0
while i < len(actividades):
    if actividades.loc[i, 'rubro'] in rubros_clase1:
        actividades.loc[i, 'clase'] = 1
    else if actividades.loc[i, 'rubro'] in rubros_clase3:
        actividades.loc[i, 'clase'] = 3
    i += 1

print(actividades)

"""
SQL
"""

# ¿Existen provincias que no presentan Operadores Orgánicos Certificados?

consulta_sql = """
                SELECT DISTINCT prov.nombre_provincia AS 'Provincias sin Operadores'
                FROM info_padron AS padron
                RIGHT OUTER JOIN provincias AS prov
                ON padron.provincia_id = prov.id_provincia
                WHERE padron.provincia_id IS NULL;
                """

#¿Existen departamentos que no presentan Operadores Orgánicos Certificados?
                
consulta_sql= """
                SELECT DISTINCT dpto.nombre_depto AS 'Departamentos sin Operadores'
                FROM info_padron AS padron
                RIGHT OUTER JOIN departamentos AS dpto
                ON padron.departamento = UPPER(dpto.nombre_depto)
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

print(prom_y_desv_prov)
