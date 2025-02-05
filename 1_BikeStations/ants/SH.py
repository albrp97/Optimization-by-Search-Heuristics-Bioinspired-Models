import random
import time

import numpy as np
from matplotlib import pyplot as plt

from funcionesAuxiliares import Hormigas


def SistemaHormigas(semillas, archivo):
    xs = []
    ys = []

    soluciones = []
    costes = []
    evaluaciones = []
    iteraciones = []

    ciudades = Hormigas.leerCiudades(archivo)
    nCiudades = len(ciudades)

    print("SISTEMA DE HORMIGAS")
    print(archivo)
    print(f"Numero de ciudades: {nCiudades}")

    # Parametros fijos
    m = 10
    alfa = 1
    beta = 2
    p = .1

    for semilla in semillas:
        x = []
        y = []

        iteracion = 0
        evaluacion = 0
        random.seed(semilla)
        greedy = Hormigas.greedy(archivo, random)
        print(f"\n-----------\nSemilla: {semilla}\n-----------\n")
        costesHormigas = np.ones(shape=m)
        costesHormigas *= 999
        # Nodos visitados por hormiga
        L = np.ones(shape=(m, nCiudades + 1))
        L *= -1
        Lnv = np.ones(shape=(m, nCiudades))
        Lnv[0:m] = np.arange(0, nCiudades)

        distancias = Hormigas.matrizDistancias(ciudades)
        matrizHeuristica = Hormigas.matrizHeuristica(distancias)
        matrizFeromonas = np.ones(shape=(nCiudades, nCiudades))

        matrizFeromonas *= 1 / (nCiudades * greedy)
        costeFinal = 9999
        solFinal = []

        x.append(evaluacion)
        y.append(costeFinal)

        # Iniciamos cada hormiga con el nodo inicial
        for i in range(m):
            r = random.randint(0, nCiudades - 1)
            L[i, 0] = r
            Lnv[i, r] = -1

        t0 = time.time()
        tf = time.time() - t0

        while tf < 300 and iteracion < (nCiudades * 1000):
            costeActual = costeFinal
            # soluciones por hormiga
            for i in range(m):
                for j in range(1, nCiudades):
                    ciudad = Hormigas.reglaTransicion(int(L[i, j - 1]), matrizFeromonas, matrizHeuristica, alfa, beta,
                                                      Lnv[i, :])
                    L[i, j] = ciudad
                    Lnv[i, ciudad] = -1
                L[i, j + 1] = L[i, 0]

                costesHormigas[i] = Hormigas.evalua(L[i, :], distancias)
                iteracion += 1
                if costesHormigas[i] < costeActual:
                    costeActual = costesHormigas[i]
                    solActual = np.array(L[i]).copy()

            # Actualizo feromonas
            matrizFeromonas *= (1 - p)
            for i in range(m):
                for j in range(1, len(L[i, :])):
                    matrizFeromonas[int(L[i, j - 1]), int(L[i, j])] += (1 / costesHormigas[i])
                    matrizFeromonas[int(L[i, j]), int(L[i, j - 1])] = np.array(
                        matrizFeromonas[int(L[i, j - 1]), int(L[i, j])]).copy()

            tf = time.time() - t0

            if costeActual < costeFinal:
                costeFinal = costeActual
                solFinal = np.array(solActual).copy()
                evaluacion = iteracion
                print(f"Mejora: {costeFinal} \t\t Tiempo: {round(tf)} segundos")
                x.append(evaluacion)
                y.append(costeFinal)

            # Reinicializo
            Lnv[0:m] = np.arange(0, nCiudades)
            for i in range(m):
                L[i, 1:] = -1
                Lnv[i, int(L[i, 0])] = -1

        print(f"\nCoste Final: {costeFinal} km")
        print(f"Evaluaciones hasta mejor solucion: {evaluacion}")
        print(f"Numero total de iteraciones: {iteracion}")
        soluciones.append(solFinal)
        costes.append(costeFinal)
        evaluaciones.append(evaluacion)
        iteraciones.append(iteracion)

        xs.append(x)
        ys.append(y)

    soluciones = np.array(soluciones)
    costes = np.array(costes)
    evaluaciones = np.array(evaluaciones)
    iteraciones = np.array(iteraciones)

    print(f"\nGreedy: {Hormigas.greedy(archivo, random)}")
    print(f"Costes: {costes} \t\t Media: {round(costes.mean(), 2)} \t\t Desv: {round(costes.std(), 2)}")
    print(
        f"Evaluaciones: {evaluaciones} \t\t Media: {round(evaluaciones.mean(), 2)} \t\t Desv: {round(evaluaciones.std(), 2)}")
    print(f"Iteraciones: {iteraciones}")

    for i in range(len(xs)):
        plt.subplot(2, len(xs), i + 1)
        plt.plot(xs[i], ys[i])
        plt.xlabel('Evaluacion')
        plt.ylabel('Coste')
        plt.title(f'Evolucion {i}')

    for j in range(len(soluciones)):
        plt.subplot(2, len(soluciones), j + 4)
        sol = soluciones[j]
        x = np.zeros(shape=len(ciudades))
        y = np.zeros(shape=len(ciudades))

        for ciudad in range(len(ciudades)):
            x[ciudad] = ciudades[ciudad][0]
            y[ciudad] = ciudades[ciudad][1]

        plt.scatter(x, y)
        for i in range(len(sol) - 1):
            Punto1 = (x[int(sol[i])], x[int(sol[i + 1])])
            Punto2 = (y[int(sol[i])], y[int(sol[i + 1])])
            plt.plot(Punto1, Punto2, color='black')
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(f'Dibujo {j}')
    plt.show()

    return np.array(soluciones), np.array(costes), np.array(evaluaciones), np.array(iteraciones)
