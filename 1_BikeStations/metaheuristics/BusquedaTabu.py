import math
import random
import time
import numpy as np
import matplotlib.pyplot as plt

from funcionesAuxiliares import Estaciones as e, GreedyAleatoria

e = e.estaciones()

def busquedaTabu(semillas=np.random.randint(-999, 999, size=5), nVecinos=30, nCambio=3, divisionFrecuencia=10,
                 nReiniciaciones=4, maxIteraciones=150, mostrar=True, grafica=True):
    soluciones = []
    costes = []
    evaluaciones = []

    xs = []
    ys = []

    # Iteraciones en las que hay que hacer una reinicialización
    qIteraciones = int(maxIteraciones / nReiniciaciones)

    if mostrar:
        print("\nBUSQUEDA TABU")
        print(
            f"\nParametros:\n\nNumero de vecinos: {nVecinos}\nTamaño de cambio: {nCambio}\nIteraciones maximas: {maxIteraciones}\nDivision para matriz de frecuencias: {divisionFrecuencia}\nNumero de reiniciaciones: {nReiniciaciones}")

    for semilla in semillas:
        x = []
        y = []
        evaluacion = 0

        # Matriz de frecuencias a largo plazo, guarda las veces que cada estacion tiene ese rango de valores
        matrizFrecuencia = np.zeros(shape=(int(220 / divisionFrecuencia), 16))

        listaTabuTam = 4
        # Lista que guarda los movimientos restringidos
        listaTabu = np.zeros(shape=(listaTabuTam, 2))
        # Tiempos que los movimientos de la lista tabu estan restringidos
        listaTabuTiempo = np.zeros(shape=(listaTabuTam, 2))
        indiceTabu = 0

        # Generamos la solucion inicial aleatoria
        random.seed(semilla)
        solActual = GreedyAleatoria.generarSolucionAleatoria(random)
        costeActual = e.evalua(solActual)

        solFinal = solActual
        costeFinal = costeActual

        iteracion = 0

        x.append(iteracion)
        y.append(costeActual)

        if mostrar:
            print("\n\n------------------")
            print(f"Semilla: {semilla}")
            print("------------------")
            print("\nInicial")
            print(f"Solucion: {solActual}\t\tCoste: {costeActual}\n")

        while iteracion < maxIteraciones:

            # Para ver si hay una mejora en el lote
            movimientoActual = 0

            # Recorremos los vecinos buscando una solucion mejor
            for i in range(nVecinos):
                actualizarMatrizFrecuencia(matrizFrecuencia, solActual, divisionFrecuencia)
                [solCandidata, movimiento] = GreedyAleatoria.generadorMovimientoAleatorioTabu(solActual, nCambio)
                costeCandidata = e.evalua(solCandidata)
                evaluacion += 1

                if costeCandidata < costeActual and not movimientoTabu(listaTabu,
                                                                       movimiento) or costeCandidata < costeFinal:
                    costeLote = costeCandidata
                    solLote = solCandidata
                    movimientoActual = movimiento

            solActual = solLote
            costeActual = costeLote

            # Si hay una mejora actualizamos la tabla tabu con sus tiempos
            if movimientoActual != 0 and not movimientoTabu(listaTabu, movimientoActual):
                listaTabu[indiceTabu] = np.array(movimientoActual)
                listaTabuTiempo[indiceTabu] = 3
                indiceTabu += 1
            if indiceTabu >= listaTabuTam:
                indiceTabu = 0

            actualizarListaTabu(listaTabu, listaTabuTiempo)

            # Si hay mejora actualizamos la solucion final
            if costeActual < costeFinal:
                costeFinal = costeActual
                solFinal = solActual

            # Reinicialización
            if iteracion % qIteraciones == 0 and iteracion > 0:
                if mostrar:
                    print(f"Iteracion: {iteracion}, ", end="")
                # print(listaTabu)
                r = random.random()
                [filas, _] = np.shape(listaTabu)
                if r < .5:
                    # Forzamos para que no sea una longitud<1
                    if filas > 1:
                        listaTabu = np.zeros(shape=(int(filas / 2), 2), dtype=int)
                        listaTabuTiempo = np.zeros(shape=(int(filas / 2), 2), dtype=int)
                        listaTabuTam /= 2
                        if indiceTabu >= listaTabuTam:
                            indiceTabu = 0
                        if mostrar:
                            print(f"Decrementamos lista tabu ({int(listaTabuTam)}), ", end="")
                else:
                    listaTabu = np.zeros(shape=(int(filas * 2), 2), dtype=int)
                    listaTabuTiempo = np.zeros(shape=(int(filas * 2), 2), dtype=int)
                    listaTabuTam *= 2
                    if mostrar:
                        print(f"Incrementamos lista tabu ({int(listaTabuTam)}), ", end="")

                r = random.random()
                if r < .25:
                    # Reinicializamos con solucion aleatoria
                    solActual = GreedyAleatoria.generarSolucionAleatoria(random)
                    costeActual = e.evalua(solActual)
                    if mostrar:
                        print("Reinicializamos con solucion aleatoria")
                elif r < .75:
                    # Reinicializamos con memoria a largo plazo (solGreedy)
                    solActual = greedyTabu(matrizFrecuencia)
                    costeActual = e.evalua(solActual)
                    if mostrar:
                        print("Reinicializamos con memoria a largo plazo")
                else:
                    # Reinicializamos desde la mejor solucion
                    solActual = solFinal
                    costeActual = costeFinal
                    if mostrar:
                        print("Reinicializamos desde la mejor solucion")
            iteracion += 1
            x.append(iteracion)
            y.append(costeActual)

        soluciones.append(solFinal)
        costes.append(costeFinal)
        evaluaciones.append(evaluacion)

        x.append(iteracion)
        y.append(costeFinal)

        xs.append(x)
        ys.append(y)

        if mostrar:
            print("\nFinal")
            print(f"Solucion: {np.array(solFinal)}\t\tCoste: {costeFinal}")

    if grafica:
        for i in range(len(xs)):
            plt.subplot(1, len(xs), i + 1)
            plt.plot(xs[i], ys[i])
            plt.xlabel('Iteracion')
            plt.ylabel('Coste')
            plt.title(f'Evolucion {i}')
        plt.show()

    return soluciones, costes, evaluaciones

def actualizarMatrizFrecuencia(matrizFrecuencia, sol, divisionFrecuencia):
    """
    Acualiza la matrizFrecuencia de frecuencia con la solucion dada
    :param matrizFrecuencia: Matriz a modificar
    :param sol: Solucion con valores a actualizar
    """
    for i in range(len(sol)):
        rango = int(sol[i] / divisionFrecuencia)
        matrizFrecuencia[rango][i] += 1

def movimientoTabu(listaTabu, movimiento):
    """
    Comprueba si el movimiento (1 para cada estacion) es tabu
    """
    if np.any(np.all(movimiento == listaTabu, axis=1)):
        return True
    else:
        return False

def actualizarListaTabu(listaTabu, listaTabuTiempo):
    listaTabuTiempo -= 1
    listaTabu[listaTabuTiempo == 0] = 0
    listaTabuTiempo[listaTabuTiempo < 0] = 0

def greedyTabu(matrizFrecuencia):
    """
    Devuelve la solucion Greedy con la inversa de la matriz de frecuencia
    :param matrizFrecuencia:
    """
    np.seterr(divide='ignore')
    solGreedy = [0] * 16

    inversa = np.ones(shape=matrizFrecuencia.shape) / matrizFrecuencia
    inversa[inversa == math.inf] = 0

    [filas, columnas] = matrizFrecuencia.shape
    listaAux = np.array(matrizFrecuencia)

    for c in range(columnas):
        listaAux[:, c] = np.divide(inversa[:, c], sum(inversa[:, c]))
    for i in range(16):
        r = random.random()
        suma = 0
        for f in range(filas):
            suma += listaAux[f, i]
            if r < suma:
                v = f * 10
                solGreedy[i] = random.randint(v, v + 9)
                break  # Break, algoritmo sacado de los apuntes de la practica
    out = [0] * 16
    suma = sum(solGreedy)
    for i in range(len(solGreedy)):
        out[i] = (int((220 * solGreedy[i]) / suma))
    return out

def estudioParametros(semillas, nVecinos=30, nCambio=3, divisionFrecuencia=10, nReiniciaciones=4, maxIteraciones=150):
    costes = []
    tiempos = []
    if type(nVecinos) == list:
        for i in nVecinos:
            t = time.time()
            costes.append(np.array(busquedaTabu(semillas, nVecinos=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nVecinos
        label = "Numero de Vecinos"
    elif type(nCambio) == list:
        for i in nCambio:
            t = time.time()
            costes.append(
                np.array(busquedaTabu(semillas, nCambio=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nCambio
        label = "Tamaño de cambio"
    elif type(maxIteraciones) == list:
        for i in maxIteraciones:
            t = time.time()
            costes.append(
                np.array(busquedaTabu(semillas, maxIteraciones=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = maxIteraciones
        label = "Numero de Iteraciones Maximo"
    elif type(divisionFrecuencia) == list:
        for i in divisionFrecuencia:
            t = time.time()
            costes.append(
                np.array(busquedaTabu(semillas, divisionFrecuencia=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = divisionFrecuencia
        label = "Divisiones para matriz de frecuencias"
    elif type(nReiniciaciones) == list:
        for i in nReiniciaciones:
            t = time.time()
            costes.append(
                np.array(busquedaTabu(semillas, nReiniciaciones=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nReiniciaciones
        label = "Numero de reinicializaciones"
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
