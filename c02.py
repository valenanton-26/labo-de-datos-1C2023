# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
#%% Definir una función maximo(a,b) que tome dos parámetros numéricos y devuelva el máximo.
def maximo(a,b):
    max = 0
    if a > b:
        max = a
    else:
        max = b
    
    return max

#%% Definir una función dos_pertenece(lista) que tome una lista y devuelva True si la lista 
# tiene al 2 y False en caso contrario.

def dos_pertenece(lista):
    resul = False
    if 2 in lista:
        resul = True
    
    return resul

#%% Definir una función pertenece(lista, elem) que tome una lista y un elemento y devuelva True si la lista 
# tiene al elemento dado y False en caso contrario
    
def pertenece(lista, elem):
    resul = False
    if elem in lista:
        resul = True
    
    return resul

#%% Definir una función es_par(n) que devuelva True si el número es par y False en caso contrario.
    
def es_par(n):
    resul = False
    if n%2 == 0:
        resul = True
    return resul

#%% Definir una función mas_larga(lista1, lista2) que tome dos listas y devuelva la más larga.
    
def mas_larga(lista1, lista2):
    if len(lista1) > len(lista2):
        return lista1
    elif len(lista2) > len(lista1):
        return lista2
    else : 
        return "son iguales"
    
#%% Definir una función tachar_pares(lista) que tome una lista de números y devuelva una similar pero 
# donde los números pares estén reemplazados por ‘x’.
        
def tachar_pares(lista):
    i = 0
    
    while i < len(lista):
        if lista[i]%2 == 0:
            lista[i] = "x"  
        i += 1
    return lista

    
#%% Definir una función cant_e que tome una lista y devuelva la cantidad de letras ‘e’ que tiene.  

def cant_e(lista):
    cont = 0
    for elem in lista:
        for e in elem:
            if e == "e":
                cont +=1
    return cont
    
#%% Definir una función sumar_unos que tome una lista, les sume 1 a todos sus elementos, y devuelva la 
# lista modificada.

def sumar_unos(lista):
    i = 0
    
    while i < len(lista):   
        lista[i] = lista[i]+1  
        i += 1
    return lista
    
#%% Definir la función mezclar(cadena1, cadena2) que tome dos strings y devuelva el resultado de 
# intercalar elemento a elemento. Por ejemplo: si intercalamos Pepe con Jose darı́a PJeopsee
def minimo(cadena1,cadena2):
    if len(cadena1)>len(cadena2):
        return len(cadena2)
    else:
        return len(cadena1)

def mezclar(cadena1, cadena2):
    min = minimo(cadena1, cadena2)
    nueva = ""
    i = 0
    while i<min:
        nueva += cadena1[i] + cadena2[i]
        i += 1
    if min < len(cadena1):
        nueva += cadena1[i:]
    else:
        nueva += cadena2[i:]
    
    return nueva 
    

#%% Construí una función traductor_geringoso(lista) que, a partir de una lista de palabras, devuelva un
# diccionario geringoso.
    
def geringoso(cadena):

    capadepenapa = ''
    vocales = ["a", "e", "i", "o", "u"]

    for c in cadena:
        capadepenapa += c
        if c in vocales:
            capadepenapa += "p"+c 
    return capadepenapa

def traductor_geringoso(lista):
    dic = {}
    
    for p in lista:
        dic[p] = geringoso(p)
    
    return dic
    
