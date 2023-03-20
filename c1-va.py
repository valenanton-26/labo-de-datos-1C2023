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