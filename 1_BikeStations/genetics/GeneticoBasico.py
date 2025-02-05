import random
import time

import matplotlib.pyplot as plt
import numpy as np

from funcionesAuxiliares import Estaciones as e, GreedyAleatoria

e = e.estaciones()


def geneticoBasico(semillas=np.random.randint(-999, 999, size=5), nIndividuos=30,
                   maxIteraciones=1000, nSeleccion=30, nMutacion=20, nReemplazo=30, mostrar=True, grafica=True):
    """
    Algoritmo genetico que devuelve soluciones, costes y evaluaciones a partir de semillas
    :param semillas: Semillas a ejecutar. Default: 5 semillas aleatorias
    :param nIndividuos: Numero de individuos en la poblacion. Default: 30
    :param maxIteraciones: Maximas iteraciones a ejecutar. Default: 1000
    :param nSeleccion: Porcentaje para seleccion por torneo. Default: 30
    :param nMutacion: Porcentaje de mutacion por gen. Default: 20
    :param nReemplazo: Porcentaje de reemplazo por torneo. Default: 30
    :param mostrar: Muestra por consola la ejecucion. Default: True
    :param grafica: Muestra grafica de evolucion. Default: True
    :return: Devuelve soluciones, costes y evaluaciones
    """
    soluciones = []
    costes = []
    evaluaciones = []

    xs = []
    ys = []

    if mostrar:
        print("\nGENETICO BASICO")
        print(
            f"\nParametros:\n\nNumero de individuos: {nIndividuos}\nIteraciones maximas: {maxIteraciones}\nPorcentaje de seleccion: {nSeleccion}")
        print(f"Porcentaje de mutacion: {nMutacion}\nPorcentaje de reemplazo: {nReemplazo}")
    for semilla in semillas:
        x = []
        y = []
        iteracion = 0
        evaluacion = 0

        #Inicio, evaluo la poblacion y obtengo el mejor individuo
        np.random.seed(abs(semilla))
        random.seed(semilla)
        P = iniciarPoblacion(nIndividuos)
        E = evaluarPoblacion(P)
        evaluacion += nIndividuos

        mejorIndividuo = min(E)

        sinMejora = 0
        minimoSinMejora=int(maxIteraciones/4)

        if grafica:
            x.append(iteracion)
            y.append(min(E))

        if mostrar:
            print("\n\n-----------------")
            print(f"Semilla: {semilla}")
            print("-----------------")
            indice = np.argmin(E)
            print(f"\n\n\nIteracion inicial. Mejor individuo {E[indice]} - {P[indice]}")
            print("\nVeces que mejora: ", end="")

        #Mientras no llegue al maximo de iteraciones o hay una mejora reciente
        while iteracion < maxIteraciones and sinMejora<minimoSinMejora:

            # Comprobamos si el mejor individuo ha cambiado para saber cuantas generaciones llevamos sin mejora
            nuevoMejorIndividuo = min(E)
            if mejorIndividuo == nuevoMejorIndividuo:
                sinMejora += 1
            else:
                sinMejora = 0
                mejorIndividuo = nuevoMejorIndividuo
                if mostrar:
                    print("o", end="")
                if grafica:
                    x.append(iteracion)
                    y.append(mejorIndividuo)
                #Si hay una mejora en las ultimas 250 iteraciones aumento el limite
                if iteracion>maxIteraciones-minimoSinMejora:
                    maxIteraciones+=minimoSinMejora

            # Cruzo, muto e introduzco individuos en la poblacion
            hijos = repodruccion(P, E, nSeleccion, nMutacion)
            P = reemplazoTorneo(P, E, hijos, nReemplazo)
            evaluacion += 2
            E = evaluarPoblacion(P)
            evaluacion += nIndividuos

            iteracion += 1

        indice = np.argmin(E)
        soluciones.append(P[indice])
        costes.append(E[indice])
        evaluaciones.append(evaluacion)

        if grafica:
            x.append(iteracion)
            y.append(min(E))
            xs.append(x)
            ys.append(y)

        if mostrar:
            print(f"\n\nIteracion final. Mejor individuo {E[indice]} - {P[indice]}")

    if grafica:
        for i in range(len(xs)):
            plt.subplot(1, len(xs), i + 1)
            plt.plot(xs[i], ys[i])
            plt.xlabel('Iteracion')
            plt.ylabel('Coste')
            plt.title(f'Evolucion {i}')
        plt.show()

    return soluciones, costes, evaluaciones


def iniciarPoblacion(nIndividuos):
    """
    Iniciamos la poblacion a partir del numero de individuos indicado
    :param nIndividuos:
    :return:
    """
    P = []
    P.append(GreedyAleatoria.generarSolucionGreedy(e.movimientosIniciales))
    for i in range(nIndividuos - 1):
        P.append(GreedyAleatoria.generarSolucionAleatoria(random))
    return np.array(P)


def evaluarPoblacion(P):
    """
    Evaluamos la poblacion con el nuevo metodo
    :param P:
    :return:
    """
    E = []
    for individuo in P:
        E.append(e.evaluaCapacidad(individuo))
    return np.array(E)


def repodruccion(P, E, nSeleccion, nMutacion):
    """
    Seleccionamos los padres y ejecutamos un método para el cruce y para la mutacion
    :param P:
    :param E:
    :param nSeleccion:
    :param nMutacion:
    :return:
    """
    # Numero de individuos para el torneo
    nTorneo = round(nSeleccion / 100 * len(P))
    # Minimo 3 individuos
    if nTorneo < 3:
        nTorneo = 3

    indicesElegidos = []
    individuosTorneo = []
    costesTorneo = []
    # Elijo a los individuos del torneo, asegurandome de que no son iguales
    for i in range(nTorneo):
        indice = random.randint(0, len(P) - 1)
        while indice in indicesElegidos:
            indice += 1
            if indice >= len(P):
                indice = 0
        individuosTorneo.append(P[indice])
        costesTorneo.append(E[indice])
        indicesElegidos.append(indice)
    individuosTorneo = np.array(individuosTorneo)
    costesTorneo = np.array(costesTorneo)

    # Escojo a los mejores 2 de los individuos en el torneo
    indicesPadres = np.argpartition(costesTorneo, 1)[0:2]
    padres = individuosTorneo[indicesPadres]

    # TIPOS DE CRUCES: INDIVIDUAL Y CORTE
    hijos = cruceIndividual(padres)
    while sum(hijos[0]) < 205:
        hijos = cruceIndividual(padres)
    # TIPOS DE MUTACION: INTERCAMBIO, NGENES FIJOS, PROPORCION INDIVIDUAL
    mutacionIndividual(hijos, nMutacion)

    return hijos


def cruceCorte(padres):
    """
    Cruza por corte, con genes continuos
    :param padres:
    """
    [a, b] = np.sort(np.random.randint(0, len(padres[0] - 1), size=2))
    hijos = [[], []]

    for i in range(len(padres[0])):
        if i > a and i < b:
            hijos[0].append(padres[0][i])
            hijos[1].append(padres[1][i])
        else:
            hijos[0].append(padres[1][i])
            hijos[1].append(padres[0][i])

    return np.array(hijos)


def cruceIndividual(padres):
    """
    Cruza de forma individual los genes
    :param padres:
    :return:
    """
    hijos = [[], []]
    for i in range(len(padres[0])):
        r = random.random()
        if r < .5:
            hijos[0].append(padres[0][i])
            hijos[1].append(padres[1][i])
        else:
            hijos[0].append(padres[1][i])
            hijos[1].append(padres[0][i])
    return np.array(hijos)


def mutacionIndividual(hijos, nMutacion):
    """
    Muta por cada gen con una std=3 segun porcentaje de nMutacion
    :param hijos:
    :param nMutacion:
    :return:
    """
    for hijo in hijos:
        for i in range(len(hijo)):
            r = random.randint(0, 100)
            if r <= nMutacion:
                hijo[i] = round(random.gauss(hijo[i], 3))
                if hijo[i] < 0:
                    hijo[i] = 0


def mutacionIndividualFijo(hijos, nMutacion):
    """
    Muta los genes con una distribucion gaussiana con un numero de genes a mutar fijo
    :param hijos:
    :param nMutacion:
    :return:
    """
    # Numero de genes a mutar
    nGenesMutados = round(nMutacion / 100 * len(hijos[0]))
    for hijo in hijos:
        for i in range(nGenesMutados):
            genMutar = random.randint(0, len(hijo) - 1)
            hijo[genMutar] = round(random.gauss(hijo[genMutar], 3))
            if hijo[genMutar] < 0:
                hijo[genMutar] = 0


def mutacionIntercambio(hijos, nMutacion):
    """
    Mutar los genes por intercambios de x plazas
    :param hijos:
    :param nMutacion:
    :return:
    """
    # Numero de genes a mutar
    nGenesMutados = round(nMutacion / 100 * len(hijos[0]))
    # Como el intercambio es de 2 genes hay que dividirlo por la mitad
    nGenesMutados /= 2
    for j in range(len(hijos)):
        for i in range(int(nGenesMutados)):
            hijos[j] = GreedyAleatoria.generadorMovimientoAleatorio(hijos[j], 3)


def reemplazoTorneo(P, E, hijos, nReemplazo):
    """
    Reemplaza individuos de la poblacion por nuevos por torneo
    :param P:
    :param E:
    :param hijos:
    :param nReemplazo:
    :return:
    """
    # Numero de individuos en el torneo
    nTorneo = round(nReemplazo / 100 * len(P))
    # Minimo 3 individuos
    if nTorneo < 3:
        nTorneo = 3
    individuosTorneo = []
    costesTorneo = []
    # Elijo a los individuos del torneo, asegurandome de que no son iguales
    for i in range(nTorneo):
        indice = random.randint(0, len(P) - 1)

        individuosTorneo.append(P[indice])
        costesTorneo.append(E[indice])

        P = np.delete(P, indice, 0)
        E = np.delete(E, indice)

    for hijo in hijos:
        individuosTorneo.append(hijo)
        costesTorneo.append(e.evaluaCapacidad(hijo))
    individuosTorneo = np.array(individuosTorneo)
    costesTorneo = np.array(costesTorneo)

    # Devuelvo la nueva poblacion que consiste en la poblacion anterior y los elegidos en el torneo+hijos
    nuevaPoblacion = []
    for i in P:
        nuevaPoblacion.append(i)
    indicesElegidos = np.argpartition(costesTorneo, 1)[:-2]
    for i in indicesElegidos:
        nuevaPoblacion.append(individuosTorneo[i])

    return np.array(nuevaPoblacion)


def estudioParametros(semillas, nIndividuos=30, nMejoresIndividuos=3, maxIteraciones=1000, nSeleccion=30, nMutacion=20,
                      nReemplazo=30):
    """
    Estudio de parametros para la optimizacion del genetico
    :param semillas:
    :param nIndividuos:
    :param nMejoresIndividuos:
    :param maxIteraciones:
    :param nSeleccion:
    :param nMutacion:
    :param nReemplazo:
    :return:
    """
    costes = []
    tiempos = []
    if type(nIndividuos) == list:
        for i in nIndividuos:
            t = time.time()
            costes.append(np.array(geneticoBasico(semillas, nIndividuos=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nIndividuos
        label = "Numero de individuos en poblacion"
    elif type(nMejoresIndividuos) == list:
        for i in nMejoresIndividuos:
            t = time.time()
            costes.append(np.array(geneticoBasico(semillas, nMejoresIndividuos=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nMejoresIndividuos
        label = "Numero de individuos que esperan mejora"
    elif type(maxIteraciones) == list:
        for i in maxIteraciones:
            t = time.time()
            costes.append(np.array(geneticoBasico(semillas, maxIteraciones=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = maxIteraciones
        label = "Iteraciones maximas"
    elif type(nSeleccion) == list:
        for i in nSeleccion:
            t = time.time()
            costes.append(np.array(geneticoBasico(semillas, nSeleccion=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nSeleccion
        label = "Porcentaje de seleccion para torneo"
    elif type(nMutacion) == list:
        for i in nMutacion:
            t = time.time()
            costes.append(np.array(geneticoBasico(semillas, nMutacion=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nMutacion
        label = "Porcentaje de mutacion"
    elif type(nReemplazo) == list:
        for i in nReemplazo:
            t = time.time()
            costes.append(np.array(geneticoBasico(semillas, nReemplazo=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nReemplazo
        label = "Porcentaje de reemplazo para torneo"
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
