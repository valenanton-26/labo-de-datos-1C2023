#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:11:54 2023

@author: 
    Lara Herling, LU: 314/22
    Camila Dramis, LU: 535/23
    Valentina Anton, LU:322/20
"""
import pandas as pd
import csv
from inline_sql import sql, sql_val
from unidecode import unidecode
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

padron = pd.read_csv("~/Descargas/padron-de-operadores-organicos-certificados.csv", encoding='latin-1')
salarios = pd.read_csv("~/Descargas/w_median_depto_priv_clae2.csv")
localidades_censales = pd.read_csv("~/Descargas/localidades-censales.csv")
dic_clases = pd.read_csv("~/Descargas/diccionario_clae2.csv")
dic_dptos = pd.read_csv("~/Descargas/diccionario_cod_depto.csv")

"""
CALIDAD DE DATOS
"""
#Utilizando el sistema de GQM, definimos distintas metricas para analizar en 
#cantidad la calidad de datos afectada, y utilizamos las siguientes consultas
#SQL para contestarnos las preguntas planteadas. 
consulta_sql = """
            	SELECT COUNT(*)
            	FROM localidades_censales
            	WHERE municipio_id IS NULL;
"""
#municipio_nulo = sql^consulta_sql

consulta_sql = """
SELECT COUNT(localidad)
FROM padron
WHERE localidad LIKE 'INDEFINID%' ;
"""
#localidad_nulos = sql^consulta_sql

consulta_sql = """
SELECT COUNT(establecimiento)
FROM padron
WHERE establecimiento LIKE 'NC' ;
"""
#establecimiento_nulos = sql^consulta_sql

consulta_sql = """
SELECT COUNT(w_median)
FROM salarios
WHERE w_median < 0;
"""
#salario_invalido = sql^consulta_sql

"""
CODIGOS NORMALIZACION
"""
#Normalización
#Defino una función para elimiar las tildes de un string
def eliminar_tildes(s):
    return unidecode(s)

#Padron a 1FN
padron['productos'] = padron['productos'].str.split(',')
padron = padron.explode('productos')
padron['productos'] = padron['productos'].str.split(' Y ')
padron = padron.explode('productos')
padron['productos'] = padron['productos'].str.split('?')
padron = padron.explode('productos')
padron['productos'] = padron['productos'].str.split(';')
padron = padron.explode('productos')
padron['productos'] = padron['productos'].str.split(':')
padron = padron.explode('productos')
padron['productos'] = padron['productos'].str.split('-')
padron = padron.explode('productos')

# limpieza de datos de Padron en 1FN
padron['productos'] = padron['productos'].str.replace('FRUTAS AL NATURAL \(FRAMBUESAS','FRUTAS AL NATURAL = FRAMBUESA')
padron['productos'] = padron['productos'].str.replace('GANADERIA OVINA \(CARNE','GANADERIA OVINA = CARNE')
padron['productos'] = padron['productos'].str.split('=')
padron = padron.explode('productos')

padron['productos'] = padron['productos'].str.strip()

padron['productos'] = padron['productos'].str.replace('ARANDANOS','ARANDANO')
padron['productos'] = padron['productos'].str.replace('ARVEJAS','ARVEJA')
padron['productos'] = padron['productos'].str.replace('CEBOLLA VERDEO','CEBOLLA DE VERDEO')
padron['productos'] = padron['productos'].str.replace('CERELAES','CEREALES')
padron['productos'] = padron['productos'].str.replace('CITRICOS\)','CITRICOS')
padron['productos'] = padron['productos'].str.replace('CEREZAS','CEREZA')
padron['productos'] = padron['productos'].str.replace('DAMASCOS','DAMASCO')
padron['productos'] = padron['productos'].str.replace('DURAZNOS','DURAZNO')
padron['productos'] = padron['productos'].str.replace('ESPARRAGOS','ESPARRAGO')
padron['productos'] = padron['productos'].str.replace('FRUTILLAS','FRUTILLA')
padron['productos'] = padron['productos'].str.replace('FRUTOS DEL BOSQUE\)','FRUTOS DEL BOSQUE')
padron['productos'] = padron['productos'].str.replace('FRUTOS\)','FRUTOS')
padron['productos'] = padron['productos'].str.replace('\(CAROZO','CAROZO')
padron['productos'] = padron['productos'].str.replace('HARINAS','HARINA')
padron['productos'] = padron['productos'].str.replace('HIGOS','HIGO')
padron['productos'] = padron['productos'].str.replace('HOJAS','HOJA')
padron['productos'] = padron['productos'].str.replace('\(RAIZ','RAIZ')
padron['productos'] = padron['productos'].str.replace('JUGOS','JUGO')
padron['productos'] = padron['productos'].str.replace('KIWIS','KIWI')
padron['productos'] = padron['productos'].str.replace('LANA\)','LANA')
padron['productos'] = padron['productos'].str.replace('MANZANAS','MANZANA')
padron['productos'] = padron['productos'].str.replace('OELAGINOSAS','OLEAGINOSAS')
padron['productos'] = padron['productos'].str.replace('OLIVAS','OLIVA')
padron['productos'] = padron['productos'].str.replace('OLIVOS','OLIVO')
padron['productos'] = padron['productos'].str.replace('PERAS','PERA')
padron['productos'] = padron['productos'].str.replace('PIMIENTOS','PIMIENTO')
padron['productos'] = padron['productos'].str.replace('PONELO','POMELO')
padron['productos'] = padron['productos'].str.replace('PUERROS','PUERRO')
padron['productos'] = padron['productos'].str.replace('PULPAS','PULPA')
padron['productos'] = padron['productos'].str.replace('UVAS','UVA')
padron['productos'] = padron['productos'].str.replace('VINOS','VINO')
padron['productos'] = padron['productos'].str.replace('ZUCCINI','ZUCCHINI')
padron['productos'] = padron['productos'].str.replace('NUECES','NUEZ')
padron['productos'] = padron['productos'].str.replace('PALTAS','PALTA')
padron['productos'] = padron['productos'].str.replace('CIRUELAS DESECADAS','CIRUELA DESECADA')
padron['productos'] = padron['productos'].str.replace('CIRUELAS','CIRUELA')
padron['productos'] = padron['productos'].str.replace('MANZANZA','MANZANA')
padron['productos'] = padron['productos'].str.replace('NOGALES','NOGAL')
padron['productos'] = padron['productos'].str.replace('\(CAROZO','CAROZO')
padron['productos'] = padron['productos'].str.replace('.','')

padron['rubro'] = padron['rubro'].str.strip()

#Departamentos a 3FN

provincias = dic_dptos[['id_provincia_indec', 'nombre_provincia_indec']].copy()
provincias = provincias.drop_duplicates()
provincias = provincias.rename(columns={'id_provincia_indec' : 'id_provincia', 'nombre_provincia_indec' :'nombre_provincia'})


departamentos = dic_dptos[['codigo_departamento_indec', 'nombre_departamento_indec', 'id_provincia_indec']].copy()
departamentos = departamentos.rename(columns={'codigo_departamento_indec' : 'id_depto', 'nombre_departamento_indec' : 'nombre_depto', 'id_provincia_indec' : 'id_provincia'})
departamentos['nombre_depto'] = departamentos['nombre_depto'].apply(eliminar_tildes)

#Clases a 3FN

info_letra = dic_clases[['letra', 'letra_desc']].copy()
info_letra =  info_letra.drop_duplicates()
info_letra['letra_desc'] = info_letra['letra_desc'].apply(eliminar_tildes)
info_letra['letra_desc'] = info_letra['letra_desc'].str.strip()

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

#Empiezo la limpieza de padron
info_padron = padron.copy()
info_padron = info_padron.rename(columns={'razón social' : 'razon_social', 'productos' : 'producto'})
info_padron = info_padron.drop_duplicates()
info_padron['departamento'] = info_padron['departamento'].apply(eliminar_tildes)
info_padron = info_padron.rename(columns={'Certificadora_id' : 'certificadora_id'})


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
                SELECT l.departamento_id, p.*
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
                SELECT m.id_depto AS departamento_id, p.*
                FROM info_padron AS p, son_municipios AS m
                WHERE p.departamento = m.municipio AND p.provincia_id = m.provincia_id
                ORDER BY departamento_id;
"""
info_padron_B = sql^consulta_sql

#Ahora vamos obtener un df de las filas en info_padron que tienen el dato de departamento correctamente cargado
#lo vamos a relacionar con su id de departamento y organizarlo de la misma manera que los dos padrones anteriores, para luego poder unirlos

consulta_sql = """
                SELECT d.id_depto AS departamento_id, p.*
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
padron_limpio = sql^consulta_sql

#Vemos que todos los Operadores de la categoría 3 tienen su rubro como 'SIN DEFINIR' 
#Decidimos completar la columna rubro con 'COMERCIALIZADORES'
#En esta consulta, eliminamos también la columna de localidades y departamentos, dejando el id del dpto como identificador
consulta_sql = """
                SELECT departamento_id, pais_id, pais, provincia_id, provincia,
                producto, categoria_id, categoria_desc, certificadora_id, certificadora_deno,
                razon_social, establecimiento, REPLACE(rubro, 'SIN DEFINIR', 'COMERCIALIZADORES') AS rubro
                FROM padron_limpio
                ;
"""
padron_limpio = sql^consulta_sql

#Hacemos el paso a 3FN
certificadora = padron_limpio[['certificadora_id', 'certificadora_deno']].copy()
certificadora = certificadora.drop_duplicates()

categoria = padron_limpio[['categoria_id', 'categoria_desc']].copy()
categoria =categoria.drop_duplicates()

df_padron = padron_limpio[['razon_social', 'establecimiento', 'producto', 'rubro', 'departamento_id', 'certificadora_id', 'categoria_id']].copy()

#Buscamos definir un df que exprese la relación entre rubro y clase
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
                FROM (
                        SELECT *
                        FROM df_padron AS padron, departamentos AS d
                        WHERE padron.departamento_id = d.id_depto
                        ) AS p
                RIGHT OUTER JOIN provincias AS prov
                ON p.id_provincia = prov.id_provincia
                WHERE prov.id_provincia IS NULL;
                """
prov_sin_operadores = sql^consulta_sql

#¿Existen departamentos que no presentan Operadores Orgánicos Certificados?
                
consulta_sql= """
                SELECT DISTINCT d.nombre_depto AS 'Departamentos sin Operadores', d.id_provincia
                FROM df_padron AS p
                RIGHT OUTER JOIN departamentos AS d
                ON p.departamento_id = d.id_depto 
                WHERE p.departamento_id IS NULL
                ORDER BY nombre_depto;
                """
dptos_sin_operadores = sql^consulta_sql

consulta_sql = """
                SELECT COUNT(*) AS 'Cantidad de departamentos sin Operadores'
                FROM dptos_sin_operadores;
                """
cant_dptos_sin_operadores = sql^consulta_sql

#¿Cuál es la actividad que más operadores tiene?
#Como separamos los productos, sabemos que la tabla cuenta con varias filas que corresponden 
#a un mismo operador trabajando en un mismo rubro y, por lo tanto, en una misma actividad. 

#Para poder responder esta pregunta, primero vamos a filtrar el df
#Dejando una sola fila por cada operador orgánico trabajando en un rubro
consulta_sql = """
                SELECT DISTINCT departamento_id, establecimiento, razon_social, 
                certificadora_id, categoria_id, rubro
                FROM df_padron;
"""
operadores_por_rubro = sql^consulta_sql

#Ahora si, contamos la cantidad de operadores sobre este nuevo df

consulta_sql = """
                SELECT a.clase, COUNT(*) AS cantidad_de_operadores
                FROM operadores_por_rubro AS p, actividades AS a, info_clase AS c
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

#¿Cuál fue el salario promedio de esa actividad en 2022? 
#(si hay variosregistros de salario, mostrar el más actual de ese año)
consulta_sql = """
                SELECT fecha, clase, salario_promedio
                FROM (
                    SELECT CAST(s.fecha AS DATE) AS fecha, m.clase, MEAN(s.salario) AS salario_promedio
                    FROM max_cant_operadores AS m, info_salarios AS s
                    WHERE m.clase = s.id_clase AND YEAR(CAST(fecha AS DATE))=2022
                    GROUP BY CAST(s.fecha AS DATE), m.clase
                    )
                WHERE fecha = (
                                    SELECT MAX(CAST(fecha AS DATE))
                                    FROM info_salarios
                                    WHERE YEAR(CAST(fecha AS DATE))=2022
                                )
                
                ;
"""
salario_prom_c1_2022 = sql^consulta_sql

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

"""
GRAFICOS
"""
# I
#Cantidad de Operadores por provincia
sns.set_palette('pastel')
op = padron['provincia'].value_counts()
op.plot.bar().set(title='Operadores por provincia') 


# II
#Boxplot, por cada provincia, donde se pueda observar la cantidad de productos por operador

def grafico_provincia_prodXoperador(prov):
    # del padron ya separado por producto pero antes de expresarlo en 3FN, busca los de la prov pasada
    df_prov = padron_limpio[padron_limpio['provincia']== prov]

    # cuenta la cantidad de cada producto, dejando la separacion por certificadora
    consulta_sql = """
                    SELECT certificadora_deno AS certificadora, producto , COUNT(producto) AS cantidad
                    FROM df_prov
                    GROUP BY producto, certificadora_deno;
                    """
    producto_y_cert = sql^consulta_sql

    # grafica el df obtenido con la cantidad en funcion de la certificadora
    sns.boxplot(data=producto_y_cert, x='certificadora', y='cantidad').set(title='Operadores por provincia: ' + prov) 
    plt.show()
    plt.close()
    
provincias_grafico = padron_limpio['provincia'].unique().tolist()

# un for para que vaya graficando todas las provincias que aparecen en el df. 
# Lo dejo comentado porque sino muy gede que se impriman todas
"""
for p in provincias_grafico:
    grafico_provincia_prodXoperador(p)
"""  

grafico_provincia_prodXoperador("BUENOS AIRES")
grafico_provincia_prodXoperador("ENTRE RIOS")

    
# III
# Relación entre cantidad de emprendimientos certificados de cada provincia y el salario promedio 
# en dicha provincia (para la actividad) en el año 2022. En caso de existir más de un
# salario promedio para ese año, mostrar el último del año 2022. 
consulta_sql = """
                SELECT p.provincia_id, a.clase, COUNT(*) AS cant_estab_rubro
                FROM padron_limpio AS p
                INNER JOIN actividades AS a ON p.rubro = a.rubro
                GROUP BY p.provincia_id, a.clase;
                """
establecimientos_por_prov = sql^consulta_sql


consulta_sql = """
                 SELECT p.nombre_provincia AS provincia, s.id_clase AS actividad ,MEAN(s.salario) AS salario, CAST(s.fecha AS DATE) AS fecha, e.cant_estab_rubro AS cantidad_establecimientos
                 FROM info_salarios AS s
                 INNER JOIN departamentos AS d ON s.id_depto = d.id_depto
                 INNER JOIN provincias AS p ON d.id_provincia = p.id_provincia
                 INNER JOIN establecimientos_por_prov AS e ON e.provincia_id = d.id_provincia AND e.clase = s.id_clase
                 WHERE NOT EXISTS (
                         SELECT *
                         FROM info_salarios AS s1, departamentos AS d1, provincias AS p1, establecimientos_por_prov AS e1
                         WHERE s1.id_depto = d1.id_depto AND d1.id_provincia = p1.id_provincia 
                         AND e1.provincia_id = d1.id_provincia AND e1.clase = s1.id_clase
                         AND p.nombre_provincia = p1.nombre_provincia 
                         AND s.id_clase = s1.id_clase
                         AND CAST(s1.fecha AS DATE) > CAST(s.fecha AS DATE) 
                 )
                 GROUP BY  p.nombre_provincia, s.id_clase ,s.fecha, e.cant_estab_rubro
                 ORDER BY p.nombre_provincia ASC, s.fecha DESC, s.id_clase
                 
"""
salario_por_prov_estab = sql^consulta_sql


def grafico_prov_act_cant(prov):
    salario_prov = salario_por_prov_estab[salario_por_prov_estab['provincia'] == prov]

    sal = salario_prov['salario']/1000
    cant = salario_prov['cantidad_establecimientos']
    clase = salario_prov['actividad']
    
    n=len(clase)
    x=np.arange(n)
    
    plt.title("Salario promedio y cantidad de establecimientos en cada clase en " + prov)
    plt.bar(x-0.10, sal, width=0.20 ,label="salario promedio" )
    plt.bar(x+0.10, cant,width=0.20,label="cantidad" )
    plt.xticks(x,clase)
    plt.xlabel("id de la clase")
    plt.ylabel("cantidad")
    plt.legend(loc='best')
    plt.show()


prov_graficoIII = salario_por_prov_estab['provincia'].unique().tolist()
prov_graficoIII = np.sort(prov_graficoIII)

for p in prov_graficoIII:
    grafico_prov_act_cant(p)


# IV
# ¿Cuál es la distribución de los salarios promedio en Argentina? Realicen un 
# violinplot de los salarios promedio por provincia. 
# Grafiquen el último ingreso medio por provincia.

consulta_sql = """
                 SELECT p.nombre_provincia AS provincia, MEAN(s.salario) AS salario, CAST(s.fecha AS DATE) AS fecha
                 FROM info_salarios AS s
                 INNER JOIN departamentos AS d ON s.id_depto = d.id_depto
                 INNER JOIN provincias AS p ON d.id_provincia = p.id_provincia
                 GROUP BY  p.nombre_provincia, s.fecha
                 ORDER BY p.nombre_provincia ASC
                 
"""
salario_por_prov = sql^consulta_sql


# grafico de todos los promedios de salarios
sns.set_palette('pastel')
sns.violinplot(data = salario_por_prov, x = 'provincia' , y = 'salario', scale ='width').set(title='Operadores por provincia') 
plt.tick_params(axis='x', labelrotation = 85)
plt.show()
plt.close()


