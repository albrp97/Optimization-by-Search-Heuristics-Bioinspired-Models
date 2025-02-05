import math
import random
import time

import numpy as np
from matplotlib import pyplot as plt

from funcionesAuxiliares import Estaciones as e, GreedyAleatoria

e = e.estaciones()


def temperaturaInicial(mu=0.11, phi=0.11):
    """
    Devuelve la temperatura inicial dependiendo de mu, phi y el coste de la solucion Greedy
    :param mu: Parametro mu. Default: 0.11
    :param phi: Parametro phi. Default: 0.11
    :return: Temperatura inicial
    """
    kmGreedy = e.evalua(GreedyAleatoria.generarSolucionGreedy(e.movimientosIniciales))
    return (mu / -math.log(phi)) * kmGreedy


def estudioMuPhi(mu=0.11, phi=0.11):
    """
    Devuelve la cantidad de soluciones iniciales aceptadas dependiendo de el calculo de la temperatura inicial
    :param mu: Parametro del que depende la temperatura inicial. Default: 0.11
    :param phi: Parametro del que depende la temperatura inicial. Default: 0.11
    :return: Numero de soluciones iniciales aceptadas de 100
    """
    tInicial = temperaturaInicial(mu, phi)
    costeCandidato = e.evalua(GreedyAleatoria.generarSolucionGreedy(e.movimientosIniciales))
    random.seed(random.random())

    k = 0
    for i in range(100):
        costeActual = e.evalua(GreedyAleatoria.generarSolucionAleatoria(random))
        d = costeCandidato - costeActual
        n = random.random()

        if ((n < np.exp(-d / tInicial)) or d < 0):
            k = k + 1
            # N de soluciones iniciales aceptadas
    return k


def enfriamientoSimulado(semillas=np.random.randint(-999, 999, size=5), nVecinos=20, nCambio=2, maxIteraciones=90,
                         mostrar=True, grafica=True):
    """
    Devuelve las soluciones, costes y evaluaciones tras ejecutar el algoritmo enfriamiento simulado
    :param semillas: Semillas que se van a evaluar. Default: 5 semillas aleatorias
    :param nVecinos: Numero de vecinos a ejecutar en cada ejecucion. Default: 20
    :param nCambio: Tamaño del cambio al generar un vecino. Default: 2
    :param maxIteraciones: Iteraciones que se van a ejecutar como maximo. Default: 90
    :param mostrar: Para mostrar por consola la informacion de la ejecucion
    :param grafica: Para mostrar la grafica de evolucion del algoritmo
    :return: Devuelve las soluciones los costes y las evaluaciones ejecutadas
    """

    soluciones = []
    costes = []
    evaluaciones = []

    # Valor inicial del parametro de control
    tIni = temperaturaInicial()

    xs = []
    ys = []

    if mostrar:
        print("\nENFRIAMIENTO SIMULADO")
        print(
            f"\nParametros:\n\nNumero de vecinos: {nVecinos}\nTamaño de cambio: {nCambio}\nIteraciones maximas: {maxIteraciones}")

    for semilla in semillas:
        x = []
        y = []
        ev = 0

        random.seed(semilla)
        solActual = GreedyAleatoria.generarSolucionAleatoria(random)
        costeActual = e.evalua(solActual)
        ev += 1

        solFinal = solActual
        costeFinal = costeActual

        if mostrar:
            print("\n\n------------------")
            print(f"Semilla: {semilla}")
            print("------------------")
            print("\nInicial")
            print(f"Solucion: {solActual}\t\tCoste: {costeActual}")

        iteracion = 0
        tAct = tIni

        x.append(costeActual)
        y.append(iteracion)

        # Condicion de parada
        while iteracion < maxIteraciones:
            # Velocidad de enfriamiento
            for vecino in range(nVecinos):
                solCandidata = GreedyAleatoria.generadorMovimientoAleatorio(solFinal, nCambio)
                costeCandidata = e.evalua(solCandidata)
                ev += 1

                d = costeCandidata - costeActual
                r = random.random()

                if r < np.exp(-d / tAct) or d < 0:
                    solActual = solCandidata
                    costeActual = costeCandidata

                    x.append(costeActual)
                    y.append(iteracion)

            if costeActual < costeFinal:
                solFinal = solActual
                costeFinal = costeActual

            iteracion += 1
            tAct = tIni / (1 + iteracion)

        if mostrar:
            print("\n\nFinal")
            print(f"Solucion: {solFinal}\t\tCoste: {costeFinal}")

        soluciones.append(solFinal)
        costes.append(costeFinal)

        x.append(costeFinal)
        y.append(iteracion)

        xs.append(x)
        ys.append(y)

        evaluaciones.append(ev)

    if grafica:
        for i in range(len(xs)):
            plt.subplot(1, len(xs), i + 1)
            plt.plot(ys[i], xs[i])
            plt.xlabel('Iteracion')
            plt.ylabel('Coste')
            plt.title(f'Evolucion {i}')
        plt.show()

    return soluciones, costes, evaluaciones

def estudioParametros(semillas, nVecinos=20, nCambio=2, maxIteraciones=90):
    """
    Metodo para comparar parametros
    :param semillas: Semillas a ejecutar
    :param nVecinos: Numero de vecinos a ejecutar
    :param nCambio: Tamaño de cambio al generar vecinos
    :param maxIteraciones: Iteraciones maximas a ejecutar
    """
    costes = []
    tiempos = []
    if type(nVecinos) == list:
        for i in nVecinos:
            t = time.time()
            costes.append(np.array(enfriamientoSimulado(semillas, nVecinos=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nVecinos
        label = "Numero de Vecinos"
    elif type(nCambio) == list:
        for i in nCambio:
            t = time.time()
            costes.append(
                np.array(enfriamientoSimulado(semillas, nCambio=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nCambio
        label = "Tamaño de cambio"
    elif type(maxIteraciones) == list:
        for i in maxIteraciones:
            t = time.time()
            costes.append(
                np.array(enfriamientoSimulado(semillas, maxIteraciones=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = maxIteraciones
        label = "Numero de Iteraciones Maximo"
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
