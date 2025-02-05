import math
import random
import time

import numpy as np
from matplotlib import pyplot as plt

from SolarPowePlant.Solar import Solar as s, FuncionesAuxiliares as fa, Greedy


def temperaturaInicial(mu=0.12, phi=0.15):
    """
    Devuelve la temperatura inicial dependiendo de mu, phi y el coste de la solucion Greedy
    :param mu: Parametro mu. Default: 0.12
    :param phi: Parametro phi. Default: 0.15
    :return: Temperatura inicial
    """

    kmGreedy = Greedy.greedy()[1]
    return (mu / -math.log(phi)) * kmGreedy


def estudioMuPhi(mu=0.12, phi=0.15):
    """
    Devuelve la cantidad de soluciones iniciales aceptadas dependiendo de el calculo de la temperatura inicial
    :param mu: Parametro del que depende la temperatura inicial. Default: 0.12
    :param phi: Parametro del que depende la temperatura inicial. Default: 0.15
    :return: Numero de soluciones iniciales aceptadas de 100
    """
    tInicial = temperaturaInicial(mu, phi)
    # print(tInicial)

    tIni=tInicial

    solActual = fa.generarSolucionAleatoria()
    costeActual = s.evalua(solActual)

    random.seed(10)

    k = 0
    h = 0
    f=0

    for i in range(100):
        solCandidata = fa.generarMovimientoAleatorio(solActual, 12)
        costeCandidata = s.evalua(solCandidata)

        d = costeCandidata - costeActual
        n = random.random()

        if (n < np.exp(-d / tInicial)):
            k += 1

        if d < 0:
            h += 1
            # print(f"{costeCandidata} - {costeActual}")
            # N de soluciones iniciales aceptadas

        if (n < np.exp(-d / tInicial)) or d < 0:
            f+=1

    return k, h,f


def enfriamientoSimulado(semillas=np.random.randint(-999, 999, size=5), nVecinos=24, nCambio=11, maxIteraciones=100, mostrar=True, grafica=True):
    """
    Devuelve las soluciones, costes y evaluaciones tras ejecutar el algoritmo enfriamiento simulado
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
        print(f"\nParametros:\n\nNumero de vecinos: {nVecinos}\nTamaño de cambio: {nCambio}\nIteraciones maximas: {maxIteraciones}")

    for semilla in semillas:
        x = []
        y = []
        ev = 0

        random.seed(semilla)
        np.random.seed(abs(semilla))

        solActual = fa.generarSolucionAleatoria()
        costeActual = s.evalua(solActual)
        ev += 1

        solFinal = solActual
        costeFinal = costeActual

        if mostrar:
            print("\n\n------------------")
            print(f"Semilla: {semilla}")
            print("------------------")
            print("\nInicial")
            print(f"Ganancia: {-costeActual}\t\tSolucion: {solActual}")

        iteracion = 0
        tAct = tIni

        x.append(-costeActual)
        y.append(iteracion)

        # Condicion de parada
        while iteracion < maxIteraciones:
            # Velocidad de enfriamiento
            for vecino in range(nVecinos):
                solCandidata = fa.generarMovimientoAleatorio(solFinal, nCambio)
                costeCandidata = s.evalua(solCandidata)
                ev += 1

                d = costeCandidata - costeActual
                r = random.random()

                if r < np.exp(-d / tAct) or d < 0:
                    solActual = solCandidata
                    costeActual = costeCandidata

                    x.append(-costeActual)
                    y.append(iteracion)

            if costeActual < costeFinal:
                solFinal = solActual
                costeFinal = costeActual

            iteracion += 1
            tAct = tIni / (1 + iteracion)

        if mostrar:
            print("\n\nFinal")
            print(f"Ganancia: {-costeActual}\t\tSolucion: {solActual}")

        soluciones.append(solFinal)
        costes.append(-costeFinal)

        x.append(-costeFinal)
        y.append(iteracion)

        xs.append(x)
        ys.append(y)

        evaluaciones.append(ev)

    if grafica:
        for i in range(len(xs)):
            plt.subplot(1, len(xs), i + 1)
            plt.plot(ys[i], xs[i])
            plt.xlabel('Iteracion')
            plt.ylabel('Ganancia')
            plt.title(f'Evolucion {i}')
        plt.show()

    return soluciones, costes, evaluaciones


def estudioParametros(semillas, nVecinos=24, nCambio=11, maxIteraciones=150):
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
    plt.ylabel('Ganancia')
    plt.xlabel(label)
    plt.title("Eficacia")

    plt.subplot(1, 2, 2)
    plt.plot(x, tiempos)
    plt.ylabel('Tiempo')
    plt.xlabel(label)
    plt.title("Eficiencia")

    print(f"\nGanancias: {costes}\nTiempos: {tiempos}")

    plt.show()
