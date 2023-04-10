# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

empleado_01 = [[20222333, 45,2,20000],[33456234,40,0,25000],[45432345,41,1,10000]]
empleado_02 = [[20222333, 45,2,20000],[33456234,40,0,25000],[45432345,41,1,10000], [43957304,37,0,12000],[42236276,36,0,18000]]
empleado_03 = [[20222333, 20000, 45,2],[33456234,25000,40,0],[45432345,10000,41,1], [43957304,12000,37,0],[42236276,18000,36,0]]
empleado_04 = [[20222333,33456234,45432345,43957304,42236276],[20000,25000,10000,12000,18000],[45,40,41,37,36],[2,0,1,0,0]]


def superarSalarioBloque01(matriz):
    mayores = []
    i = 0
    for empl in matriz:
        if(empl[3] > 15000):
            mayores.insert(i,empl)
            i += 1
    return mayores


print(superarSalarioBloque01(empleado_01))
print(superarSalarioBloque01(empleado_02))

def superarSalarioBloque03(matriz):
    mayores = []
    i = 0
    for empl in matriz:
        if(empl[1] > 15000):
            mayores.insert(i,[empl[0],empl[3],empl[2],empl[1]])
            i += 1
    return mayores

print(superarSalarioBloque03(empleado_03))

def superarSalarioBloque04(matriz):
    mayores = []
    i = 0
    j = 0
    while (i < len(matriz[1])):
        if(matriz[1][i] > 15000):
            mayores.insert(j, [matriz[0][i],matriz[3][i],matriz[2][i],matriz[1][i]])
            j += 1
        i += 1
    return mayores

print(superarSalarioBloque04(empleado_04))
