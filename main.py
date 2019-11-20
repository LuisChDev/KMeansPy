# implementación K Means en Python
from copy import copy
from math import sqrt
from typing import List, Tuple
import seaborn as sns   # type: ignore
import pandas as pd  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
sns.set()

# Tipos
Coord = Tuple[float, float]
Coords = List[Coord]

# parámetros
ks: List[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10]
loops = 1000

# -- -- -- -- -- --
# funciones auxiliares


# normaliza los datos que se le den
# toma una lista de coordenadas, y retorna una lista de coordenadas
def normalize(datos: Coords) -> Coords:
    xs = [x[0] for x in datos]
    ys = [x[1] for x in datos]
    # promedio del valor X
    prom_x: float = sum(xs) / len(datos)
    # rango de X
    ran_x: float = max(xs) - min(xs)
    # promedio del valor Y
    prom_y = sum(ys) / len(datos)
    # rango de Y
    ran_y: float = max(ys) - min(ys)
    # se normalizan los valores de x.
    xs_norm: List[float] = [(x - prom_x) / ran_x for x in xs]
    ys_norm: List[float] = [(y - prom_y) / ran_y for y in ys]
    # se retorna la lista de coordenadas normalizadas
    return [(x, y) for (x, y) in zip(xs_norm, ys_norm)]


# función que calcula la distancia euclidiana entre dos puntos.
def euclid(dato: Coord, centr: Coord) -> float:
    return sqrt((dato[0] - centr[0])**2 + (dato[1] - centr[1])**2)


# diagrama de voronoi
# toma dos lista de coordenadas (una de datos y una de centroides),
# y retorna la clasificación de cada dato según la distancia más corta
# a uno de los centroides. (una lista de enteros, donde cada entero
# es la posición del centroide en la lista que es pasado.)
def voronoi(datos: Coords, centroids: Coords) -> List[int]:
    # la lista de clasificaciones
    clasf: List[int] = []
    # para cada elemento de la lista de datos:
    for x in datos:
        # se calcula la distancia del punto a todos los centroides.
        dists = [euclid(x, i) for i in centroids]
        # se escoje la más baja y se agrega a la lista.
        clasf.append(dists.index(min(dists)))
    return clasf


# centroide de los puntos
# dada una lista de coordenadas, retorna otra coordenada que representa
# el centro de los puntos.
def centroid(datos: Coords) -> Coord:
    return (sum([x[0] for x in datos]) / len(datos),
            sum([x[1] for x in datos]) / len(datos))


# -- -- -- -- -- --
# secuencia principal

# se parsea el archivo
vals_: List[Tuple[float, float]] = []
with open("cluster.txt", 'r') as f:
    coords = list(
        map(lambda x: (float(x[0]), float(x[1])),
            map(lambda x: x.split(";"), f.readlines())))
    for x in coords:
        vals_.append(x)

# se normalizan los valores.
vals = normalize(vals_)


# ## ciclo principal
# repetir *loop* iteraciones
def loop(k: int) -> List[Tuple[Coord, Coords]]:
    # se inicializan los centroides]
    # se escogen K puntos del dataset como semilla.
    centroides = []
    for i in range(k):
        centroides.append(copy(vals[i]))

    puntos: List[List[Coord]] = []

    for _ in range(loops):
        # se calcula la clasificación de los datos con los centroides actuales
        clasf = voronoi(vals, centroides)

        # se recalcula la posición de los centroides, de acuerdo a los puntos
        # que les pertenezcan
        # se crean listas para cada centroide
        puntos = []
        for ctr in centroides:
            puntos.append([])

        # se toman de la lista de valores, los correspondientes al centroide
        # dado
        for ind, i in enumerate(clasf):
            puntos[i].append(vals[ind])

        # se calcula la nueva posición del centroide
        for ind, ctr in enumerate(centroides):
            centroides[ind] = centroid(puntos[ind])

    result = []
    for ind, ctr in enumerate(centroides):
        result.append((ctr, puntos[ind]))

    return result


# -- -- -- -- --
# se calculan los clusters para un rango de valores de k.
# se calculan los valores del error cuadrático para cada cluster,
# y se suman al total de error cuadrático para la solución con k
# medias.
if __name__ == "__main__":
    errores: List[float] = [0 for k in ks]
    for ind, k in enumerate(ks):
        errores[ind] = 0
        clusters = loop(k)
        for (cluster, points) in clusters:
            errores[ind] += sum(
                [((point[0] - cluster[0])**2 + (point[1] - cluster[1])**2)
                 for point in points])

    # creando el dataframe para generar el gráfico.
    valores = {}
    valores["cluster"] = ks
    valores["error cuadrático"] = errores  # type: ignore - cuz we dont care
    valores = pd.DataFrame(valores)
    print(valores)

    # Se produce una gráfica con los resultados.
    plot = sns.barplot(data=valores)
    plt.show()

# x="num. clusters", y="error cuadratico",
