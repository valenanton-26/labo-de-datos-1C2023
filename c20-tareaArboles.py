#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 18:07:30 2023

@author: mcerdeiro
"""


from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import tree
import pandas as pd

#%%######################

        ####            Análisis exploratorio

#########################
#%%        
data = pd.read_csv('~/Descargas/arboles.csv')
#%%
nbins = 70

f, s = plt.subplots(1,2)
plt.suptitle('Histogramas de altura y diámetro', size = 'large')

sns.histplot(data = data, x = 'altura_tot', hue = 'nombre_com', bins = nbins, stat = 'probability', palette = 'viridis', ax=s[0])

sns.histplot(data = data, x = 'diametro', hue = 'nombre_com', bins = nbins, stat = 'probability', palette = 'viridis', ax=s[1])

#%%

plt.suptitle('Histogramas de la altura', size = 'large')
sns.histplot(data = data, x = 'altura_tot', hue = 'nombre_com', bins = nbins, stat = 'probability',  palette = 'viridis')
plt.show()

plt.suptitle('Histogramas del diametro', size = 'large')
sns.histplot(data = data, x = 'diametro', hue = 'nombre_com', bins = nbins, stat = 'probability',  palette = 'viridis')
plt.show()

plt.suptitle('Histogramas de la inclinacion', size = 'large')
sns.histplot(data = data, x = 'inclinacio', hue = 'nombre_com', bins = nbins, stat = 'probability', palette = 'viridis')
plt.show()

#%%
dataJ = data[data['nombre_com'] == 'Jacarandá']
dataC = data[data['nombre_com'] == 'Ceibo']
dataE = data[data['nombre_com'] == 'Eucalipto']
dataP = data[data['nombre_com'] == 'Pindó']

sns.scatterplot(data = dataJ , x = 'diametro', y = 'altura_tot').set(title= 'Relacion entre diametro y altura', xlabel = 'Diametro' , ylabel = 'Altura')
sns.scatterplot(data = dataC , x = 'diametro', y = 'altura_tot').set(title= 'Relacion entre diametro y altura', xlabel = 'Diametro' , ylabel = 'Altura')
sns.scatterplot(data = dataE , x = 'diametro', y = 'altura_tot').set(title= 'Relacion entre diametro y altura', xlabel = 'Diametro' , ylabel = 'Altura')
sns.scatterplot(data = dataP , x = 'diametro', y = 'altura_tot').set(title= 'Relacion entre diametro y altura', xlabel = 'Diametro' , ylabel = 'Altura')
plt.legend(('Jacarandá', 'Ceibo', 'Eucalipto', 'Pindó'))
plt.show()
plt.close()

#%%######################

        ####            Árboles de decisión

#########################
#%%

X = data[['altura_tot', 'diametro', 'inclinacio']]
Y = data['nombre_com']
#%%        
        
clf_info = tree.DecisionTreeClassifier(criterion = "entropy", max_depth= 4)
clf_info = clf_info.fit(X, Y)


plt.figure(figsize= [20,10])
tree.plot_tree(clf_info, feature_names = ['altura_tot', 'diametro', 'inclinacio'], class_names = ['Ceibo', 'Eucalipto', 'Jacarandá', 'Pindó'],filled = True, rounded = True, fontsize = 8)

# Si se saca la inclinacion, no se puede diferenciar entre Pindo y Jacaranda

#%%

datonuevo= pd.DataFrame([dict(zip(['altura_tot', 'diametro', 'inclinacio'], [22,56,8]))])
clf_info.predict(datonuevo)
# Seria Jacaranda si dejamos todos los valores para el arbol
# Seria Eucalipto si sacamos la inclinacion del arbol

#%%
# otra forma de ver el arbol
r = tree.export_text(clf_info, feature_names=['altura_tot', 'diametro', 'inclinacio'])
print(r)
#%%



