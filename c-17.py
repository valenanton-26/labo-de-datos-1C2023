#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 09:22:57 2023

@author: labo2023
"""

import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt

ru = [0,50,100,200,300,400,500,750,1000,1250,1750]
di = [104,106,112.3,117,115.3,117.5,130.22,139.8,140.6,154.12,170.5]

di2 = [105.62,109,109.37,110.71,116.17,120.25,120.57,133.46,146.62,155.03,171.61]

datos = pd.DataFrame({'RU': ru, 'DI': di})


x = pd.DataFrame(datos['RU'])
y = pd.DataFrame(datos['DI'])

model = linear_model.LinearRegression()

model.fit(x,y)

print(model.coef_)
print(model.intercept_)


plt.scatter(x,y,color='lightpink', marker='X')
plt.plot(x, model.predict(x), color='crimson', linewidth=2)
plt.xlabel('Dosis de RU (ug/huevo)')
plt.ylabel('Indice de daño')
plt.show()


data = pd.DataFrame({'RU': ru, 'DI': di2})
x = pd.DataFrame(data['RU'])
y = pd.DataFrame(data['DI'])
model = linear_model.LinearRegression()

model.fit(x,y)
pendiente = model.coef_
ordenada = model.intercept_
R2 = model.score(x,y)
print(ordenada)
print(pendiente)
print(R2)


