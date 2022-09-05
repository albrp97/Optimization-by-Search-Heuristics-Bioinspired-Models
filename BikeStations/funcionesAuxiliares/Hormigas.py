import math
import random

import numpy as np


def evalua(L, distancias):
    out = 0
    for i in range(len(L) - 1):
        out += distancias[int(L[i]), int(L[i + 1])]
    return out


def greedy(nombre, random):
    ciudades = leerCiudades(nombre)
    distancias = matrizDistancias(ciudades)
    r = random.randint(0, len(ciudades))
    L = np.ones(shape=(len(ciudades) + 1))
    L *= -1
    L[0] = r

    for i in range(1, len(L)):
        L[i] = nodoCercano(distancias[int(L[i - 1])], L)
    L[-1] = L[0]
    return evalua(L, distancias)


def leerCiudades(nombre):
    file = open(nombre, 'r')

    name = file.readline().strip().split()[1]
    fileType = file.readline().strip().split()[1]
    comment = file.readline().strip().split()[1]
    dimension = file.readline().strip().split()[1]
    edgeWeightType = file.readline().strip().split()[1]
    file.readline()

    out = []
    n = int(dimension)

    for i in range(n):
        [x, y] = file.readline().strip().split()[1:]
        out.append([float(x), float(y)])

    return np.array(out)


def matrizDistancias(ciudades):
    out = np.zeros(shape=(len(ciudades), len(ciudades)))
    for i in range(len(ciudades)):
        for j in range(len(ciudades)):
            out[i, j] = int(distancia(ciudades[i], ciudades[j]))
    return out


def distancia(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return float(math.sqrt(x * x + y * y))


def nodoCercano(distancias, L):
    out = np.array(distancias).copy()
    ciudadesVisitadas = L[L != -1]
    for c in ciudadesVisitadas:
        out[int(c)] += 999
    out[out < 1] += 999
    return np.argmin(out)


def matrizHeuristica(distancia):
    out = np.array(distancia).copy()
    out[np.where(out == 0)] = -1
    out = np.divide(1, out)
    return out


def reglaTransicion(ciudad, matrizFeromonas, matrizHeuristica, alfa, beta, Lnv):
    ciudadesNoVisitadas = np.array(Lnv[Lnv != -1])
    n = np.zeros(shape=len(ciudadesNoVisitadas))
    d = 0
    for j in range(len(ciudadesNoVisitadas)):
        d += (matrizFeromonas[ciudad, int(ciudadesNoVisitadas[j])]) ** alfa * (
        matrizHeuristica[ciudad, int(ciudadesNoVisitadas[j])]) ** beta
        n[j] = (matrizFeromonas[ciudad, int(ciudadesNoVisitadas[j])]) ** alfa * (
        matrizHeuristica[ciudad, int(ciudadesNoVisitadas[j])]) ** beta
    p = n[:] / d
    indice = elegirProbabilidad(p)
    return int(ciudadesNoVisitadas[indice])

def reglaTransicionColonia(L,ciudad,ciudades,matrizFeromonas,matrizHeuristica,alfa,beta,q0,Lnv):
    ciudadesNoVisitadas=np.array(Lnv[Lnv!=-1])
    v=np.zeros(shape=len(ciudadesNoVisitadas))
    for i in range(len(ciudadesNoVisitadas)):
        f1=(matrizFeromonas[ciudad, int(ciudadesNoVisitadas[i])]) ** alfa
        f2 = (matrizHeuristica[ciudad, int(ciudadesNoVisitadas[i])]) ** beta
        v[i]=f1*f2
    return int(ciudadesNoVisitadas[np.argmax(v)])

def elegirProbabilidad(p):
    r = random.random()
    stop = False
    indice = 0
    i = 0
    while not stop:
        if p[i] < r:
            p[i + 1] += p[i]
            i += 1
        else:
            stop = True
            indice = i
    return indice
