#%% IMPORTS
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn import metrics
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import seaborn as sns

#%% DATOS
encabezado = np.arange(0, 785, 1)
datos = pd.read_csv("~/Descargas/mnist_desarrollo.csv", names=encabezado)
datosT = pd.read_csv("~/Descargas/mnist_test.csv", names=encabezado)
datosTB = pd.read_csv("~/Descargas/mnist_test_binario.csv", names=encabezado)

#%% Analisis exploratorio

# FUNCIONES
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
    plt.colorbar()
    plt.show()
    plt.close()
    
    
def pixeles_mas_relevantes(dat0, dat1, dat0y1, m):
    pixeles_relevantes = []
    l = dat0y1.shape[0]
    
    for i in range(1,l,1):
        if((np.linalg.norm(dat0[i] - dat0y1[i]) > m) or (np.linalg.norm(dat1[i] - dat0y1[i]) > m)):
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

promedio_total = cantidadDatos/ len(digitos)

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
pixeles_relevantes = pixeles_mas_relevantes(promedios_0, promedios_1, promedios_0y1, 80)
m_pixeles_relevantes = matriz_pixeles_relevantes(pixeles_relevantes)

#graficos para explorar los datos
x = np.arange(-0.4,10,1)

plt.title("Cantidad de datos por digito")
plt.bar(digitos,cantPorDigito,label="cantidad por digitos" )
plt.plot(x, x*0 + promedio_total, label="prom cant general", color="r")
plt.xticks(digitos)
plt.xlabel("digitos")
plt.ylabel("cantidad")
plt.legend(loc='best')
plt.show()

# grafico para ver la distribucion de los pixeles
plt.title("Promedio de intensidad por píxeĺ")
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

#%% KNN
#Defino una función que, dadas las variables X e Y, el número de repeticiones y un valor n de vecinos
#evalúa el modelo knn correspondiente, devoliendo el gráfico correspondiente a los promedios obtenidos
#en función de la cantidad de vecinos considerada, y las matrices de resultados
def knn(X, Y, rep, n, titulo):
    repeticiones = rep
    neigh = range(1, n+1)

    resultados_test = np.zeros((repeticiones, len(neigh)))
    resultados_train = np.zeros((repeticiones, len(neigh)))

    for i in range(repeticiones):
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2)
        for k in neigh:
            model = KNeighborsClassifier(n_neighbors = k)
            model.fit(X_train, Y_train) 
            Y_pred = model.predict(X_test)
            Y_pred_train = model.predict(X_train)
            acc_test = metrics.accuracy_score(Y_test, Y_pred)
            acc_train = metrics.accuracy_score(Y_train, Y_pred_train)
            resultados_test[i, k-1] = acc_test
            resultados_train[i, k-1] = acc_train

    promedios_train = np.mean(resultados_train, axis = 0) 
    promedios_test = np.mean(resultados_test, axis = 0) 

    plt.plot(neigh, promedios_train, label = 'Train')
    plt.plot(neigh, promedios_test, label = 'Test')
    plt.legend()
    plt.title(titulo)
    plt.xlabel('Cantidad de vecinos')
    plt.ylabel('Exactitud (accuracy)')
    plt.show()
    plt.close()
    
    return promedios_train, promedios_test

#Defino una lista con los atributos que más marcan la difererencia entre 0 y 1, a partir de la función 
#de pixeles_mas_relevantes

pixeles_relevantesA = pixeles_mas_relevantes(promedios_0, promedios_1, promedios_0y1, 87)
atributosA = []
for p in pixeles_relevantesA:
    atributosA.append(int(p))

#Probamos la precisión de un modelo knn para distintos conjuntos de 3 atributos

#Primero evaluamos con atributos seleccionados del listado reducido de atributos relevantes
cA = random.sample(atributosA, 3)

X = df_0y1[cA]
Y = df_0y1[0]

#Pruebo los resultados hasta 7 vecinos, usando 5 repeticiones
knn_A = knn(X, Y, 5, 10, 'Modelo knn - Grupo A - 3 atributos')
promedios_trainA = knn_A[0]
promedios_testA = knn_A[1]

#Evaluamos la precisión del modelo extendiendo el listado de los atributos, usando la función
#pixeles_mas_relevantes
pixeles_relevantesB = pixeles_mas_relevantes(promedios_0, promedios_1, promedios_0y1, 40)
atributosB = []
for p in pixeles_relevantesB:
    atributosB.append(int(p))

#Probamos la precisión de un modelo knn para distintos conjuntos de 3 atributos

#Primero evaluamos con atributos seleccionados del listado reducido de atributos relevantes
cB = random.sample(atributosB, 3) 

X = df_0y1[cB]
Y = df_0y1[0]

knn_B = knn(X, Y, 5, 10, 'Modelo knn - Grupo B - 3 atributos')
promedios_trainB = knn_B[0]
promedios_testB = knn_B[1]

#Ahora evaluamos el comportamiento de la precisión del modelo tomando 3 atributos
#aleatorios del conjunto total de atributos

cC = []
for i in range(1, 4):
    atributo = random.randint(1, 785)
    cC.append(atributo)

X = df_0y1[cC]
Y = df_0y1[0]

knn_C = knn(X, Y, 5, 10, 'Modelo knn - Grupo C - 3 atributos')
promedios_trainC = knn_C[0]
promedios_testC = knn_C[1]

#Hacemos lo mismo para 7 atributos
#Primero evaluamos con atributos seleccionados del listado reducido de atributos relevantes
cA = random.sample(atributosA, 7)

X = df_0y1[cA]
Y = df_0y1[0]

knn_A = knn(X, Y, 5, 10, 'Modelo knn - Grupo A - 7 atributos')
promedios_trainA = knn_A[0]
promedios_testA = knn_A[1]

#Ahora evaluamos con atributos seleccionados del listado reducido de atributos relevantes
cB = random.sample(atributosB, 7) 

X = df_0y1[cB]
Y = df_0y1[0]

knn_B = knn(X, Y, 5, 10, 'Modelo knn - Grupo B - 7 atributos')
promedios_trainB = knn_B[0]
promedios_testB = knn_B[1]

#Ahora con 7 atributos aleatorios del conjunto total de atributos
cC = []
for i in range(1, 8):
    atributo = random.randint(1, 785)
    cC.append(atributo)

X = df_0y1[cC]
Y = df_0y1[0]

knn_C = knn(X, Y, 5, 10, 'Modelo knn - Grupo C - 7 atributos')
promedios_trainC = knn_C[0]
promedios_testC = knn_C[1]

#Repetimos para 20 atributos

#Grupo A
cA = random.sample(atributosA, 20)

X = df_0y1[cA]
Y = df_0y1[0]

knn_A = knn(X, Y, 5, 10, 'Modelo knn - Grupo A - 20 atributos')
promedios_trainA = knn_A[0]
promedios_testA = knn_A[1]

#Ahora evaluamos con atributos seleccionados del listado B
cB = random.sample(atributosB, 20) 

X = df_0y1[cB]
Y = df_0y1[0]

knn_B = knn(X, Y, 5, 10, 'Modelo knn - Grupo B - 20 atributos')
promedios_trainB = knn_B[0]
promedios_testB = knn_B[1]

#Ahora con 20 atributos aleatorios del conjunto total de atributos
cC = []
for i in range(1, 21):
    atributo = random.randint(1, 785)
    cC.append(atributo)

X = df_0y1[cC]
Y = df_0y1[0]

knn_C = knn(X, Y, 5, 10, 'Modelo knn - Grupo C - 20 atributos')
promedios_trainC = knn_C[0]
promedios_testC = knn_C[1]

#%% TESTEO

#TEST BINARIO

df0_test = df_digito(0, datosTB)
df1_test = df_digito(1, datosTB)
df0y1_test = pd.concat([df0_test, df1_test])

#Defino el conjunto de los atributos relevantes para entrenamiento del modelo
pixeles_relevantes_train = pixeles_mas_relevantes(promedios_0, promedios_1, promedios_0y1, 87)
atributos_train = []
for p in pixeles_relevantes_train:
    atributos_train.append(int(p))

X_train = df_0y1[atributos_train]
Y_train = df_0y1[0]
X_test = df0y1_test[atributos_train]
Y_test = df0y1_test[0]

model = KNeighborsClassifier(n_neighbors = 7)
model.fit(X_train, Y_train) 
Y_pred = model.predict(X_test) 

#Calculo las métricas
metrics.accuracy_score(Y_test, Y_pred)
metrics.confusion_matrix(Y_test, Y_pred)

#%% ARBOLES DE DECISION

def max_altura_mejor_precision(datos):
    X=datos.iloc[:60000, 1:] # de los datos no consideramos el valor del digito
    Y=datos[0].to_frame()

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3,random_state=0)
        
    # metodo de cross_validation con k-folding para encontrar la altura que mejor precision nos ofrece para un set de datos
    profundidades = []
    for i in range(3,10):
        clf_info = tree.DecisionTreeClassifier(criterion = "entropy", max_depth = i)
        clf_info = clf_info.fit(X_train, y_train)
        kfold = KFold(n_splits=5,shuffle=True,random_state=42)
        scores = cross_val_score(clf_info, X, Y, cv=kfold)
        
        profundidades.append((i, scores.mean()))

    max_altura = max(profundidades)
    max_altura = max_altura[0]
    
    return max_altura


def arbol_decision(data , altura):
    X=data.iloc[:60000, 1:] # de los datos no consideramos el valor del digito
    Y=data[0].to_frame()

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
    
    # creamos el arbol con las siguientes decisiones:
    # criterio = ENTROPY
    # profundidad = 8
    clf_info = tree.DecisionTreeClassifier(criterion = "entropy", max_depth = altura)
    clf_info = clf_info.fit(X_train, y_train)
    
    Y_pred = clf_info.predict(X_test)
    exactitud = metrics.accuracy_score(y_test, Y_pred)
    
    # Creamos la matriz de confusion
    matriz = metrics.confusion_matrix(y_test, Y_pred)
    
    return clf_info, exactitud, matriz


# Datos desarrollo
alt = max_altura_mejor_precision(datos)

arbol = arbol_decision(datos, 9)
texto = tree.export_text(arbol[0])
#print(texto)
print("Exactitud del modelo:", arbol[1])
matriz_confusion = arbol[2]
print(matriz_confusion)

# Datos TEST
arbol_T = arbol_decision(datosT, 9) #usamos la altura hallada con los datos de desarrollo ya que es parte de las configuraciones del modelo
texto_T = tree.export_text(arbol_T[0])
#print(texto_T)
print("Exactitud del modelo:", arbol_T[1])
matriz_confusion_T = arbol_T[2]
print(matriz_confusion_T)
