import random
import time

import matplotlib.pyplot as plt
import numpy as np

from metaheuristics import BusquedaLocal
from funcionesAuxiliares import Estaciones as e, GreedyAleatoria

e = e.estaciones()


def VNS(semillas=np.random.randint(-999, 999, size=5), maxIteraciones=50, nIntercambios=3, nCambio=3, mostrar=True,
        grafica=True):
    """
    Algoritmo VNS que devuelve soluciones costes y evaluaciones a partir de semillas
    :param semillas: Semillas a ejecutar. Default: 5 semillas aleatorias
    :param maxIteraciones: Maximas busquedas locales a ejecutar. Default: 50
    :param nIntercambios: Numero de cambios al hacer en una soluciones. Default: 3
    :param nCambio: Desviacion a la hora de cambiar una solucion. Default: 3
    :param mostrar: Muestra por consola la ejecucion. Default: True
    :param grafica: Muestra grafica de evolucion. Default: True
    :return: Devuelve soluciones, costes y evaluaciones
    """
    soluciones = []
    costes = []
    evaluaciones = []

    xs = []
    ys = []

    # numero maximo de k
    kmax = 4

    if mostrar:
        print("\nVNS")
        print(
            f"\nParametros:\n\nNumero de intercambios: {nIntercambios}\nTamaño de cambio: {nCambio}\nIteraciones maximas: {maxIteraciones}")

    for semilla in semillas:
        x = []
        y = []

        evaluacion = 0
        # Iniciamos con una solucion aleatoria
        random.seed(semilla)
        solActual = GreedyAleatoria.generarSolucionAleatoria(random)
        costeActual = e.evaluaCapacidad(solActual)
        evaluacion += 1

        # Varia la cantidad de mutacion
        k = 1
        # Numero de busquedas locales realizadas
        iteraciones = 0

        if mostrar:
            print("\n\n-----------------")
            print(f"Semilla: {semilla}")
            print("-----------------")
            print("\nInicial")
            print(f"Solucion: {solActual}\t\tCoste: {costeActual}\t\tPlazas: {sum(solActual)}")
            print("\nEjecutando busquedas locales: ", end="")

        x.append(iteraciones)
        y.append(costeActual)

        # Mientras no se llegue al maximo de busquedas locales
        while iteraciones < maxIteraciones:

            if k > kmax:
                k = 1

            # Mutamos la solucion actual y la evaluamos con la nueva funcion
            solCandidata = mutar(solActual, k, nIntercambios, nCambio)
            [solCandidata, _, ev] = BusquedaLocal.busquedaLocalSolucion(solCandidata, semilla)
            costeCandidata = e.evaluaCapacidad(solCandidata)

            evaluacion += ev

            # Si mejora
            if costeCandidata < costeActual:
                costeActual = costeCandidata
                solActual = solCandidata
                k = 1
                x.append(iteraciones)
                y.append(costeActual)
                if mostrar:
                    print("\033[34mx", end="")
            # Aumentamos el grado de mutacion
            else:
                k += 1
                if mostrar:
                    print("\033[0mo", end="")

            iteraciones += 1

        if mostrar:
            print("\033[0m\n\nFinal")
            print(f"Solucion: {solActual}\t\tCoste: {costeActual}\t\tPlazas: {sum(solActual)}")
        x.append(iteraciones)
        y.append(costeActual)

        xs.append(x)
        ys.append(y)

        soluciones.append(solActual)
        costes.append(costeActual)
        evaluaciones.append(evaluacion)

    if grafica:
        for i in range(len(xs)):
            plt.subplot(1, len(xs), i + 1)
            plt.plot(xs[i], ys[i])
            plt.xlabel('Iteracion')
            plt.ylabel('Coste')
            plt.title(f'Evolucion {i}')
        plt.show()

    return soluciones, costes, evaluaciones


def mutar(sol, k, nIntercambios, nCambio):
    """
    Muta la solucion dependiendo del valor de k, el numero de veces a cambiar la solucion y cuanto cambia la solucion
    :param sol:
    :param k:
    :param nIntercambios:
    :param nCambio:
    :return:
    """
    solAux = np.array(sol)
    s = k * 4

    indice = random.randint(0, len(sol) - 1)
    indice2 = indice

    subLista = []
    for i in range(s):
        subLista.append(solAux[indice2])
        indice2 += 1
        if indice2 >= len(sol):
            indice2 = 0

    for i in range(nIntercambios * k):
        subLista = GreedyAleatoria.mutar(subLista, nCambio)

    for e in subLista:
        solAux[indice] = e
        indice += 1
        if indice >= len(sol):
            indice = 0

    return solAux


def estudioParametros(semillas, maxIteraciones=50, nIntercambios=3, nCambio=3):
    """
    Estudio de parametros para la optimizacion del VNS
    :param semillas:
    :param maxIteraciones:
    :param nIntercambios:
    :param nCambio:
    :return:
    """
    costes = []
    tiempos = []
    if type(maxIteraciones) == list:
        for i in maxIteraciones:
            t = time.time()
            costes.append(np.array(VNS(semillas, maxIteraciones=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = maxIteraciones
        label = "Numero de busquedas locales"
    elif type(nIntercambios) == list:
        for i in nIntercambios:
            t = time.time()
            costes.append(np.array(VNS(semillas, nIntercambios=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nIntercambios
        label = "Numero de mutaciones"
    elif type(nCambio) == list:
        for i in nCambio:
            t = time.time()
            costes.append(np.array(VNS(semillas, nCambio=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nCambio
        label = "Desviacion gaussiana por mutacion"
    else:
        return

    plt.subplot(1, 2, 1)
    plt.plot(x, costes)
    plt.ylabel('Coste')
    plt.xlabel(label)
    plt.title("Eficacia")

    plt.subplot(1, 2, 2)
    plt.plot(x, tiempos)
    plt.ylabel('Tiempo')
    plt.xlabel(label)
    plt.title("Eficiencia")

    print(f"\nCostes: {costes}\nTiempos: {tiempos}")

    plt.show()
