# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
# geringoso
cadena = 'Geringoso'
capadepenapa = ''
vocales = ["a", "e", "i", "o", "u"]

# RANGE
for c in cadena:
    capadepenapa += c
    if c in vocales:
        capadepenapa += "p"+c 

print(capadepenapa)

#WHILE
capadepenapa = ''
i=0
while i< len(cadena):
    capadepenapa += cadena[i]
    if cadena[i] in vocales:
        capadepenapa += "p"+cadena[i]
    i += 1
print(capadepenapa)

# altura de una pelota cada vez que rebota
altura = 100
rebotes = 1

while rebotes <= 10:
    altura = altura * 3/5
    print(rebotes , altura)
    rebotes +=1
    

# traducir las palabras masculinas a e
frase = 'todos somos programadores'
palabras = frase.split()
frase_t = ""
for palabra in palabras: 
    palabra_t = ""
    if palabra[-1] == "o":
        palabra_t = palabra[:-1] + "e"
    elif palabra[-2] == "o":
        palabra_t = palabra[:-2] + "e" + palabra[-1]
    else:
        palabra_t = palabra
    
    frase_t += palabra_t + " "        

print(frase_t)
