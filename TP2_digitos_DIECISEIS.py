#%% IMPORTS
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import seaborn as sns

#%% DATOS
encabezado = np.arange(0, 785, 1)
datos = pd.read_csv("~/Descargas/mnist_desarrollo.csv", names=encabezado)

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
def knn(X, Y, rep, n):
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
    plt.title('Exactitud del modelo de knn')
    plt.xlabel('Cantidad de vecinos')
    plt.ylabel('Exactitud (accuracy)')
    plt.show()
    plt.close()
    
    return promedios_train, promedios_test

#Defino una lista con los atributos que más marcan la difererencia entre 0 y 1, a partir de la función 
#de pixeles_mas_relevantes

pixeles_relevantesA = pixeles_mas_relevantes(promedios_0, promedios_1, promedios_0y1, 100)
atributosA = []
for p in pixeles_relevantesA:
    atributosA.append(int(p))

#Probamos la precisión de un modelo knn para distintos conjuntos de 3 atributos

#Primero evaluamos con atributos seleccionados del listado reducido de atributos relevantes
cA = random.sample(atributosA, 3)

X = df_0y1[[cA[0], cA[1], cA[2]]]
Y = df_0y1[0]

#Pruebo los resultados hasta 7 vecinos, usando 5 repeticiones
knn_A = knn(X, Y, 5, 7)

#Evaluamos la precisión del modelo extendiendo el listado de los atributos, usando la función
#pixeles_mas_relevantes
pixeles_relevantesB = pixeles_mas_relevantes(promedios_0, promedios_1, promedios_0y1, 80)
atributosB = []
for p in pixeles_relevantesB:
    atributosB.append(int(p))

#Probamos la precisión de un modelo knn para distintos conjuntos de 3 atributos

#Primero evaluamos con atributos seleccionados del listado reducido de atributos relevantes
cB = random.sample(atributosB, 3) 

X = df_0y1[[cB[0], cB[1], cB[2]]]
Y = df_0y1[0]

knn_B = knn(X, Y, 5, 7)

#Ahora evaluamos el comportamiento de la precisión del modelo tomando 3 atributos
#aleatorios del conjunto total de atributos

cC = []
for i in range(1, 4):
    atributo = random.randint(1, 785)
    cC.append(atributo)

X = df_0y1[[cC[0], cC[1], cC[2]]]
Y = df_0y1[0]

knn_C = knn(X, Y, 5, 7)

#Hacemos lo mismo para 7 atributos
#Primero evaluamos con atributos seleccionados del listado reducido de atributos relevantes
cA = random.sample(atributosA, 7)

X = df_0y1[[cA[0], cA[1], cA[2], cA[3], cA[4], cA[5], cA[6]]]
Y = df_0y1[0]

knn_A = knn(X, Y, 5, 7)

#Ahora evaluamos con atributos seleccionados del listado reducido de atributos relevantes
cB = random.sample(atributosB, 7) 

X = df_0y1[[cB[0], cB[1], cB[2], cB[3], cB[4], cB[5], cB[6]]]
Y = df_0y1[0]

knn_B = knn(X, Y, 5, 7)

#Ahora con 7 atributos aleatorios del conjunto total de atributos

cC = []
for i in range(1, 8):
    atributo = random.randint(1, 785)
    cC.append(atributo)

X = df_0y1[[cC[0], cC[1], cC[2], cC[3], cC[4], cC[5], cC[6]]]
Y = df_0y1[0]

knn_C = knn(X, Y, 5, 7)

#Hacemos lo mismo para 10 atributos
#Primero evaluamos con atributos seleccionados del listado reducido de atributos relevantes
cA = random.sample(atributosA, 10)

X = df_0y1[[cA[0], cA[1], cA[2], cA[3], cA[4], cA[5], cA[6], cA[7], cA[8], cA[9]]]
Y = df_0y1[0]

knn_A = knn(X, Y, 5, 7)

#Ahora evaluamos con atributos seleccionados del listado reducido de atributos relevantes
cB = random.sample(atributosB, 10) 

X = df_0y1[[cB[0], cB[1], cB[2], cB[3], cB[4], cB[5], cB[6], cB[7], cB[8], cB[9]]]
Y = df_0y1[0]

knn_B = knn(X, Y, 5, 7)

#%% 
# Árboles de decisión

X=datos
Y=datos[0].to_frame()

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3) # 70% para train y 30% para test

clf = DecisionTreeClassifier()
clf = clf.fit(X_train, Y_train)


arbol = tree.DecisionTreeClassifier(criterion = "entropy", max_depth= 6)
arbol = arbol.fit(X_train,Y_train)
#print(X_train)
#print(X_test)
Y_pred = arbol.predict(X_test)
print("Exactitud del modelo:", metrics.accuracy_score(Y_test, Y_pred))

#Usando un conjunto de atributos relevantes
X=datos[[324,351,352,379,380,406,407,434,435,462,463,484,490,491]]
Y=datos[0]
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

clf_info = tree.DecisionTreeClassifier(criterion = "gini", max_depth = 6)
clf_info = clf_info.fit(X_train, y_train)

plt.figure(figsize= [40,20])
tree.plot_tree(clf_info, feature_names = [324,351,352,379,380,406,407,434,435,462,463,484,490,491], filled = True, rounded = True, fontsize = 8)
