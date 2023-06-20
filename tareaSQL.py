# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

import pandas as pd
from inline_sql import sql, sql_val

casos = pd.read_csv("~/Downloads/casos.csv")
departamento = pd.read_csv("~/Downloads/departamento.csv")   
provincia = pd.read_csv("~/Downloads/provincia.csv")
grupoetario = pd.read_csv("~/Downloads/grupoetario.csv")
tipoevento = pd.read_csv("~/Downloads/tipoevento.csv") 


print()
print("# =============================================================================")
print("# A. CONSULTAS SOBRE TABLAS")
print("# =============================================================================")

consigna    = """a.- Listar sólo los nombres de todos los departamentos que hay en la tabla departamento (dejando los registros repetidos)."""
consultaSQL = """
                SELECT descripcion
                FROM departamento;
                """
    
imprimirEjercicio(consigna, [departamento], consultaSQL)

consigna    = """b.- Listar sólo los nombres de todos los departamentos que hay en la tabla departamento (eliminando los registros repetidos)."""
consultaSQL = """
                SELECT DISTINCT descripcion
                FROM departamento;
                """
    
imprimirEjercicio(consigna, [departamento], consultaSQL)

consigna    = """c.- Listar sólo los códigos de departamento y sus nombres de todos los departamentos que hay en la tabla departamento."""
consultaSQL = """
                SELECT id, descripcion
                FROM departamento;
                """
    
imprimirEjercicio(consigna, [departamento], consultaSQL)

consigna    = """d.- Listar todas las columnas de la tabla departamento"""
consultaSQL = """
                SELECT *
                FROM departamento;
                """
    
imprimirEjercicio(consigna, [departamento], consultaSQL)

consigna    = """e.- Listar los códigos de departamento y nombres de todos los departamentos que hay en la tabla departamento. Utilizar los siguientes alias para las columnas: codigo_depto, nombre_depto"""
consultaSQL = """
                SELECT id AS codigo_depto, descripcion AS nombre_depto
                FROM departamento;
                """
    
imprimirEjercicio(consigna, [departamento], consultaSQL)

consigna    = """f.- Listar los códigos de departamento y sus nombres, ordenados por sus nombres de manera descendentes (de la Z a la A). En caso de empate, desempatar por código de departamento de manera ascendente"""
consultaSQL = """
                SELECT id, descripcion
                FROM departamento
                ORDER BY descripcion DESC, id ASC;
                """
    
imprimirEjercicio(consigna, [departamento], consultaSQL)

consigna    = """g.- Listar los registros de la tabla departamento cuyo código de provincia es igual a 54"""
consultaSQL = """
                SELECT *
                FROM departamento
                WHERE id_provincia = 54;
                """
    
imprimirEjercicio(consigna, [departamento], consultaSQL)

consigna    = """h.- Listar los registros de la tabla departamento cuyo código de provincia es igual a 22, 78 u 86."""
consultaSQL = """
                SELECT *
                FROM departamento
                WHERE id_provincia = 22 OR id_provincia=78 OR id_provincia=86;
                """
    
imprimirEjercicio(consigna, [departamento], consultaSQL)

consigna    = """i.- Listar los registros de la tabla departamento cuyos códigos de provincia se encuentren entre el 50 y el 59 (ambos valores inclusive)."""
consultaSQL = """
                SELECT *
                FROM departamento
                WHERE id_provincia>=50 AND id_provincia<=59;
                """
    
imprimirEjercicio(consigna, [departamento], consultaSQL)

consigna    = """j.- Listar los registros de la tabla provincia cuyos nombres comiencen con la letra M."""
consultaSQL = """
                SELECT *
                FROM provincia
                WHERE descripcion LIKE 'M%';
                """
    
imprimirEjercicio(consigna, [provincia], consultaSQL)

consigna    = """k.- Listar los registros de la tabla provincia cuyos nombres comiencen con la letra S y su quinta letra sea una letra A."""
consultaSQL = """
                SELECT *
                FROM provincia
                WHERE descripcion LIKE 'S___a';
                """
    
imprimirEjercicio(consigna, [provincia], consultaSQL)

consigna    = """l.- Listar los registros de la tabla provincia cuyos nombres terminan con la letra A."""
consultaSQL = """
                SELECT *
                FROM provincia
                WHERE descripcion LIKE '%a';
                """
    
imprimirEjercicio(consigna, [provincia], consultaSQL)

consigna    = """m.- Listar los registros de la tabla provincia cuyos nombres tengan exactamente 5 letras."""
consultaSQL = """
                SELECT *
                FROM provincia
                WHERE descripcion LIKE '_____';
                """
    
imprimirEjercicio(consigna, [provincia], consultaSQL)

consigna    = """n.- Listar los registros de la tabla provincia cuyos nombres tengan ”do” en alguna parte de su nombre."""
consultaSQL = """
                SELECT *
                FROM provincia
                WHERE descripcion LIKE '%do%';
                """
    
imprimirEjercicio(consigna, [provincia], consultaSQL)

consigna    = """o.- Listar los registros de la tabla provincia cuyos nombres tengan ”do” en alguna parte de su nombre y su código sea menor a 30."""
consultaSQL = """
                SELECT *
                FROM provincia
                WHERE descripcion LIKE '%do%' AND id>30;
                """
    
imprimirEjercicio(consigna, [provincia], consultaSQL)

consigna    = """p.- Listar los registros de la tabla departamento cuyos nombres tengan ”san” en alguna parte de su nombre. Listar sólo id y descripcion. Utilizar los
siguientes alias para las columnas: codigo_depto y nombre_depto, respectivamente. El resultado debe estar ordenado por sus nombres de
manera descendentes (de la Z a la A).
"""
consultaSQL = """
                SELECT id AS codigo_depto, descripcion AS nombre_depto
                FROM departamento
                WHERE nombre_depto LIKE '%san%'
                ORDER BY nombre_depto DESC;
                """
    
imprimirEjercicio(consigna, [departamento], consultaSQL)

print()
print("# =============================================================================")
print("# B. CONSULTAS MULTITABLA (INNER JOIN)")
print("# =============================================================================")

consigna    = """a.- Devolver una lista con los código y nombres de departamentos, asociados al nombre de la provincia al que pertenecen"""
consultaSQL = """
                SELECT d.id AS codigo_depto, d.descripcion AS nombre_depto, p.descripcion AS nombre_provincia
                FROM departamento AS d
                INNER JOIN provincia as p
                ON d.id_provincia = p.id;
                """
    
imprimirEjercicio(consigna, [departamento, provincia], consultaSQL)

consigna    = """b.- Devolver una lista con los código y nombres de departamentos, asociados al
nombre de la provincia al que pertenecen. Ordenar el resultado por nombre
de provincia de manera ascendente, y dentro de cada una de ellas por
nombre de departamento, también de manera ascendente.
"""
consultaSQL = """
                SELECT d.id AS codigo_depto, d.descripcion AS nombre_depto, p.descripcion AS nombre_provincia
                FROM departamento AS d
                INNER JOIN provincia as p
                ON d.id_provincia = p.id
                ORDER BY nombre_provincia ASC, nombre_depto ASC;
                """
    
imprimirEjercicio(consigna, [departamento, provincia], consultaSQL)

consigna    = """c.- Devolver los casos registrados en la provincia de “Chaco”."""
consultaSQL = """
                SELECT c.*
                FROM casos AS c, departamento AS d, provincia AS p
                WHERE c.id_depto = d.id AND d.id_provincia = p.id AND p.descripcion = 'Chaco';
                """
    
imprimirEjercicio(consigna, [casos, departamento, provincia], consultaSQL)

consigna    = """d.- Devolver aquellos casos de la provincia de “Buenos Aires” cuyo campo cantidad supere los 10 casos."""
consultaSQL = """
                SELECT c.*
                FROM casos AS c, departamento AS d, provincia AS p
                WHERE c.id_depto = d.id AND d.id_provincia = p.id AND p.descripcion = 'Buenos Aires' AND c.cantidad > 10;
                """
    
imprimirEjercicio(consigna, [casos, departamento, provincia], consultaSQL)

consigna    = """d.- Devolver aquellos casos de las provincias cuyo nombre terminen con la letra
a y el campo cantidad supere 10. Mostrar: nombre de provincia, nombre de
departamento, año, semana epidemiológica, descripción de grupo etario y
cantidad. Ordenar el resultado por la cantidad (descendente), luego por el
nombre de la provincia (ascendente), nombre del departamento
(ascendente), año (ascendente) y la descripción del grupo etario
(ascendente).
"""
consultaSQL = """
                SELECT p.descripcion AS nombre_provincia, d.descripcion AS nombre_departamento, c.anio AS año, c.semana_epidemiologica, g.descripcion AS descripcion_grupoetario, c.cantidad
                FROM casos AS c, departamento AS d, provincia AS p, grupoetario AS g
                WHERE c.id_depto = d.id AND d.id_provincia = p.id AND p.descripcion like '%a' AND c.cantidad > 10 AND c.id_grupoetario = g.id
                ORDER BY c.cantidad DESC, nombre_provincia ASC, nombre_departamento ASC, año ASC, g.descripcion ASC;
                """
    
imprimirEjercicio(consigna, [casos, departamento, provincia, grupoetario], consultaSQL)

consigna    = """f.- Ídem anterior, pero devolver sólo aquellas tuplas que tienen el máximo en el campo cantidad"""
consultaSQL = """
                SELECT p.descripcion AS nombre_provincia, d.descripcion AS nombre_departamento, c.anio AS año, c.semana_epidemiologica, g.descripcion AS descripcion_grupoetario, c.cantidad
                FROM casos AS c, departamento AS d, provincia AS p, grupoetario AS g
                WHERE c.id_depto = d.id AND d.id_provincia = p.id AND p.descripcion like '%a' AND c.cantidad > 10 AND c.id_grupoetario = g.id AND c.cantidad >= ALL (
                    SELECT c2.cantidad
                    FROM casos AS c2, departamento AS d2, provincia AS p2, grupoetario AS g2
                    WHERE c2.id_depto = d2.id AND d2.id_provincia = p2.id AND p2.descripcion like '%a' AND c2.cantidad > 10 AND c2.id_grupoetario = g2.id)
                ORDER BY c.cantidad DESC, nombre_provincia ASC, nombre_departamento ASC, año ASC, g.descripcion ASC;
                """
    
imprimirEjercicio(consigna, [casos, departamento, provincia, grupoetario], consultaSQL)

print()
print("# =============================================================================")
print("# C. CONSULTAS MULTITABLA (OUTER JOIN)")
print("# =============================================================================")

consigna    = """a.- Devolver un listado con los nombres de los departamentos que no tienen ningún caso asociado."""
consultaSQL = """
                SELECT d.descripcion
                FROM departamento AS d
                LEFT OUTER JOIN casos AS c
                ON d.id = c.id_depto
                WHERE c.cantidad = NULL;
"""
    
imprimirEjercicio(consigna, [departamento, casos], consultaSQL)
      
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

