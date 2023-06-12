import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

encabezado = np.arange(0, 785, 1)
datos = pd.read_csv("~/Descargas/mnist_desarrollo.csv", names=encabezado)


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


df_0 = df_digito(0,datos)
df_1 = df_digito(1,datos)

can_0 = cantidad(0,datos)
can_1 = cantidad(1,datos)
