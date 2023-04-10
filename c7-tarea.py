# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

empleado_01 = [[20222333, 45,2,20000],[33456234,40,0,25000],[45432345,41,1,10000]]
empleado_02 = [[20222333, 45,2,20000],[33456234,40,0,25000],[45432345,41,1,10000], [43957304,37,0,12000],[42236276,36,0,18000]]
empleado_03 = [[20222333, 20000, 45,2],[33456234,25000,40,0],[45432345,10000,41,1], [43957304,12000,37,0],[42236276,18000,36,0]]


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
            mayores.insert(i,empl)
            i += 1
    return mayores

print(superarSalarioBloque03(empleado_03))