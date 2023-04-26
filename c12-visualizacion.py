# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

df = pd.read_csv('~/Descargas/penguins_size.csv')


df.head(5) #para ver las primeras 5 lineas del dataset

df.columns
#ahora vemos que el dataset tiene las columnas
#especie isla longitud_culmen produndiad_culmen
#longitud_aleta masa_corporal sexo

#vamos a verificar algunas caracteristicas, para ello, necesitamos
#hablar de estadistica... vamos a hablar de las medidas de resumen

#media, mediana, quartiles, max, min

#como diria jack el destripador, vamos por partes...

#armemos un sub df con fines puramente didacticos

Adelie_macho = df[(df['species']=='Adelie') & (df['sex']=='MALE')]

media_masa = Adelie_macho['body_mass_g'].mean()

mediana_masa = Adelie_macho['body_mass_g'].median()

cuantil_50_masa = Adelie_macho['body_mass_g'].quantile(0.5)

cuantil_25_masa = Adelie_macho['body_mass_g'].quantile(0.25)

cuantil_75_masa = Adelie_macho['body_mass_g'].quantile(0.75)

desvio = Adelie_macho['body_mass_g'].std()

#sns.kdeplot(data = Adelie_macho , x = 'body_mass_g')


#el grafiquito...

Adelie_macho['body_mass_g'].plot.kde().set(title='Distribucion peso de machos Adelie', xlabel='Peso(g)')


plt.axvline(x = media_masa, color='red')

plt.axvline(x = mediana_masa, color = 'blue')

plt.axvline(x = cuantil_50_masa,color='yellow', linestyle='--')

plt.axvline(x = cuantil_25_masa, color='orange')

plt.axvline(x = cuantil_75_masa, color='violet')

plt.axvline(x = media_masa+desvio , color='black' , linestyle = '-.')

plt.axvline(x = media_masa-desvio , color='black' , linestyle = '-.')

plt.show()

plt.close()

#quiero agregarle a ese grafico constantes en x como la media, mediana

#como metodo super general existe describe

df.describe()

#por ejemplo...cuantos pinguinos hay por isla??

df['island'].value_counts()

#todo muy lindo, pero esto es una tabla, y gr;aficamente? como podria
#verlo?  una buena herramienta son los graficos de barras

df['island'].value_counts().plot.bar().set(title='Pinguinos por isla')
plt.show()
plt.close()

#podriamos preguntarnos, cual es la distribucion de los pesos de los
#pinguinos?

#jugar con los bins, que pasa si ponen menos, y si ponen mas?

#y si los bins tienden a infinito??

#df.plot.hist(bins = )

df['body_mass_g'].plot(kind = 'hist').set(xlabel = 'masa(g)')
plt.show()
plt.close()

df['body_mass_g'].plot(kind = 'kde').set(xlabel = 'masa(g)')#density kernel
plt.show()
plt.close()

#pareciera tener varios picos, valdra la pena preguntarse por especie?

#probemos graficando con una herramienta mas poderosa, y versatil
#que nos permite especificar con ciertos parametros, lo que queremos
#graficar, y nos va a ser muy util.

sns.kdeplot(data = df , x = 'body_mass_g' , hue = 'species').set(xlabel = 'masa(g)')
plt.show()
plt.close()

dfM = df[df['sex']=='MALE']
dfF = df[df['sex']=='FEMALE']

#male = sns.load_dataset('df')

sns.kdeplot(data = dfM , x = 'body_mass_g' , hue = 'species').set(xlabel = 'masa(g)')
plt.show()
plt.close()

#ahora podemos ver que en realidad la dsitribucion de pesos
#de cada especie es bien dsitinta, no?

#por que no nos disponems a ver si
# en alguna especie, y vemos que pasa con los sexos, seran distintos?

sns.violinplot(data = df ,
               x = 'species' , y = 'body_mass_g' , hue = 'sex').set(xlabel = 'especie' , ylabel='masa(g)')
plt.show()
plt.close()

df.isna().any()
df2 = df.dropna().isna().any()
print(df2)

#de aca logramos desprender que usando dos variables categoricas
#para separar la visualizacion de datos, y una numerica continua,
#que efectivamente el dataset tiene poblaciones distintas
#observando el peso, entre machos , y hembras, para cada especie
#ademas se observa que en el sexado hay elementos faltantes

#ya si quisieramos ver relaciones entre variables, puede resultar
#conveniente ir a otro tipo de graficos, como los de dispercion
#o scatter plot...

sns.scatterplot(data = df , x = 'flipper_length_mm', y = 'body_mass_g').set(title= 'Relacion entre aleta y peso', xlabel = 'Largo aleta(cm)' , ylabel = 'masa(g)')
plt.show()
plt.close()
#parece una buena relacion, pero fue una buena idea no diferenciar por
#sexo? o por especie?
#veamos...

sns.scatterplot(data = df , x = 'flipper_length_mm', y = 'body_mass_g' , hue = 'species' , style = 'sex').set(xlabel = 'Largo aleta(cm)' , ylabel = 'masa(g)')
plt.show()
plt.close()
#con esta visualizacion, podemos ver hasta 4 variables en juego
#en un grafico 2D

#bueno, por loque se ve, una recta ajustaria bastante bien a esos datos, no?

#probemos graficar con un ajuste lineal, a ver que pinta tienen...

dfM = df[df['sex']=='MALE']
dfF = df[df['sex']=='FEMALE']

sns.lmplot(data=df, x='flipper_length_mm', y='body_mass_g').set(title = 'regresion lineal Largo aleta(cm) vs masa(g)')
plt.show()
plt.close()

#ah, y si mejor separamos por sexos??

sns.lmplot(data=dfM, x='flipper_length_mm', y='body_mass_g', hue='sex').set(title = 'regresion lineal Largo aleta(cm) vs masa(g)')
plt.show()
plt.close()

sns.lmplot(data=dfF, x='flipper_length_mmoxplot, por', y='body_mass_g', hue='sex').set(title = 'regresion lineal Largo aleta(cm) vs masa(g)')
plt.show()
plt.close()

#y si quisiera ver las relaciones entre multiples variables?
#de una sola vez?
#Bueno!!!  existe una herrmaienta para ello...

sns.pairplot(data = df)

#aca vemos que hace scatter fuera de la diagonal, y en esta, hist
#ven que fuera del a diagonal, la informacion es redundante??

#habra manera de aprobechar esto??

#bueno, la hay!!

plot = sns.PairGrid(df)

plot.map_diag(sns.histplot)#histograma en la diagonal

plot.map_upper(sns.scatterplot)

plot.map_lower(sns.kdeplot)

#podriamos querer ver con numeros, si existen
#correlaciones entre las distintas variables

correlacion = df.corr()

#y como verlo? bueno, para este tipo de cosas estan los heatmap

sns.heatmap(correlacion)

#y si ademas quisiera ver relaciones jerarquicas entre variables?

sns.clustermap(correlacion)

#hay algun metodo para agrupar-ver si las especies son diferenciables
#facil-rico-barato? en solo dos dimensiones, teniendo en cuenta
#varias variables a la vez???

#bueno, si, es un metodo llamado PCA!!!

from sklearn.decomposition import PCA

#import numpy as np

#voy a aplicar el metodo solo a un subconjunto de los datos,
#por simplicidad, solo me quedo con machos de las tres especies

X = df[(df['sex']=='MALE')].loc[: , ['culmen_length_mm',
'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g']]

pca = PCA(n_components=2)

matriz_pca = pca.fit_transform(X.T)

pd.DataFrame(matriz_pca).plot(x = 0 , y=1 , kind = 'scatter').set(xlabel = 'Componente 1' , ylabel = 'Componente 2')