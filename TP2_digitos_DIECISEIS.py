import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import seaborn as sns

encabezado = np.arange(0, 785, 1)
datos = pd.read_csv("~/Descargas/mnist_desarrollo.csv", names=encabezado)

# Analisis exploratorio

#Funcion que, dado un dígito y una base de datos devuelve un nuevo df con las filas correspondientes a ese digito
def df_digito (n, datos):
    nombre_columna = datos.columns[0]
    df = datos[datos[nombre_columna] == n]
    return df

#Dada una base de datos y un dígito, la función devuelve la cantidad de filas que corresponden a ese dígito
def cantidad(n, datos):
    df = df_digito(n, datos)
    cantidad = df.shape[0]
    return cantidad


def cantidad_por_digitos(datos):
    cantPorDigito = []
    for i in range(0,10,1):
        c = cantidad(i,datos)
        cantPorDigito = np.append(cantPorDigito, c)
    return cantPorDigito


def promedio_pixeles(datos):
    x = []
    for i in range(0,785,1):
        prom = datos[i].mean()
        x = np.append(x, prom)
        
    return x


def graficar(v):
    figura = v[1:].reshape(28, 28)
    
    plt.imshow(figura, cmap='inferno')
    plt.title("Grafico de calor del promedio de todos los digitos")
    plt.show()
    plt.close()
    
    
def pixeles_mas_relevantes(dat0, dat1, dat0y1):
    pixeles_relevantes = []
    
    for i in range(1,785,1):
        if((np.linalg.norm(dat0[i] - dat0y1[i]) > 80) or (np.linalg.norm(dat1[i] - dat0y1[i]) > 80)):
            pixeles_relevantes = np.append(pixeles_relevantes, i)
    
    return pixeles_relevantes    


def matriz_pixeles_relevantes(array):
    m = np.zeros(784)
    
    for i in range(0,785,1):
        if(i in array):
            m[i] = 1
    m = m.reshape(28,28)
    return m


def convertir_matriz_df(m):
    x = []
    y = []
    for i in range(0,28,1):
        for j in range(0,28,1):
            if m[i][j] == 1:
                x = np.append(x,j)
                y = np.append(y,i)
    df = pd.DataFrame({'x':x, 'y':y})
    return df
                
# variables

cantidadDatos = datos.shape[0]

digitos = datos[0]
digitos = digitos.drop_duplicates().to_numpy()
digitos.sort()

# data frames creados    
df_0 = df_digito(0,datos)
df_1 = df_digito(1,datos)

df_0y1 = pd.concat([df_0, df_1])

can_0 = cantidad(0,datos)
can_1 = cantidad(1,datos)


cantPorDigito =cantidad_por_digitos(datos)

# los distintos promedios en arrays
promedios = promedio_pixeles(datos)
promedios_0 = promedio_pixeles(df_0)
promedios_1 = promedio_pixeles(df_1)
promedios_0y1 = promedio_pixeles(df_0y1)

# df con los promedios varios por las dudas
pixel = np.arange(0,785,1)
df_promedios = pd.DataFrame({'pixel': pixel, 'valor_promedio':promedios,'valor_promedio_0': promedios_0, 
                             'valor_promedio_1': promedios_1})
pixeles_relevantes = pixeles_mas_relevantes(promedios_0, promedios_1, promedios_0y1)
m_pixeles_relevantes = matriz_pixeles_relevantes(pixeles_relevantes)

#graficos para explorar los datos
plt.title("Cantidad de digitos por digito")
plt.bar(digitos,cantPorDigito,label="cantidad por digitos" )
plt.xticks(digitos)
plt.xlabel("digitos")
plt.ylabel("cantidad")
plt.legend(loc='best')
plt.show()


sns.scatterplot(data = df_promedios , x = 'pixel' , y = 'valor_promedio_0')
sns.scatterplot(data = df_promedios , x = 'pixel' , y = 'valor_promedio_1')
sns.scatterplot(data = df_promedios , x = 'pixel' , y = 'valor_promedio')
plt.show()
plt.close()

# grafico de calor
graficar(promedios_0y1)

# grafico para buscar mis atributos relevantes
df_pixeles_relevantes = convertir_matriz_df(m_pixeles_relevantes)

sns.scatterplot(data = df_pixeles_relevantes , x = 'x' , y = 'y')
plt.xlim(0,28)
plt.ylim(0,28)
plt.show()
plt.close()
