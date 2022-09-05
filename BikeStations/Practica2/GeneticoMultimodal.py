import random
import time

import matplotlib.pyplot as plt
import numpy as np

from funcionesAuxiliares import Estaciones as e, GreedyAleatoria

e = e.estaciones()


def geneticoMultimodal(semillas=np.random.randint(-999, 999, size=5), nClearing=50, distanciaMinima=2, nIndividuos=25,
                       mostrar=True, grafica=True):
    soluciones = []
    costes = []
    evaluaciones = []

    xs = []
    ys = []

    maxIteraciones = 1000
    nSeleccion = 30
    nMutacion = 20
    nReemplazo = 30

    if mostrar:
        print("\nGENETICO MULTIMODAL")
        print(
            f"\nParametros:\n\nNumero de individuos: {nIndividuos}\nGeneraciones entre operaciones de aclarado: {nClearing}\nDistancia minima: {distanciaMinima}")

    iteracionClearing = int((nClearing * nIndividuos) / 2)

    for semilla in semillas:
        x = []
        y = []
        iteracion = 0
        evaluacion = 0

        # Inicio, evaluo la poblacion y obtengo el mejor individuo
        np.random.seed(abs(semilla))
        random.seed(semilla)
        P = iniciarPoblacion(nIndividuos)
        E = evaluarPoblacion(P)
        evaluacion += nIndividuos

        mediaE = sum(E) / len(P)

        sinMejora = 0
        minimoSinMejora = int(maxIteraciones / 4)

        if grafica:
            x.append(evaluacion)
            y.append(min(E))

        if mostrar:
            print("\n\n-----------------")
            print(f"Semilla: {semilla}")
            print("-----------------")
            indice = np.argmin(E)
            print(f"\n\n\nIteracion inicial. Mejor individuo {E[indice]} - {P[indice]}")

        # Mientras no llegue al maximo de iteraciones o hay una mejora reciente
        while sinMejora < minimoSinMejora:

            # Clearing
            if iteracion == iteracionClearing:
                [P, E] = seleccionClearing(P, E, distanciaMinima)
                iteracion = 1
            nuevaMediaE = sum(E) / len(P)
            if nuevaMediaE < mediaE - 0.1:
                sinMejora = 0
                mediaE = nuevaMediaE
                if grafica:
                    x.append(evaluacion)
                    y.append(min(E))
            else:
                sinMejora += 1
            # Cruzo, muto e introduzco individuos en la poblacion
            hijos = repodruccion(P, E, nSeleccion, nMutacion)
            # Reemplazo si la poblacion esta llena
            if len(P) < (nIndividuos):
                P = list(P)
                E = list(E)
                Ehijos = evaluarPoblacion(hijos)
                if len(P) == (nIndividuos - 1):
                    P.append(hijos[np.argmin(Ehijos)])
                    E.append(Ehijos[np.argmin(Ehijos)])
                else:
                    P.append(hijos[0])
                    P.append(hijos[1])
                    E.append(Ehijos[0])
                    E.append(Ehijos[1])
                P = np.array(P)
                E = np.array(E)
            else:
                P = reemplazoTorneo(P, E, hijos, nReemplazo)
            evaluacion += 2

            E = evaluarPoblacion(P)
            evaluacion += nIndividuos

            iteracion += 1

        [P, E] = seleccionClearing(P, E, distanciaMinima)

        indice = np.argmin(E)
        soluciones.append(P[indice])
        costes.append(E[indice])
        evaluaciones.append(evaluacion)

        if grafica:
            x.append(evaluacion)
            y.append(min(E))
            xs.append(x)
            ys.append(y)

        if mostrar:
            print(f"\nIteracion final. Mejor individuo {E[indice]} - {P[indice]}")

    if grafica:
        for i in range(len(xs)):
            plt.subplot(1, len(xs), i + 1)
            plt.plot(xs[i], ys[i])
            plt.xlabel('Evaluacion')
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
    if nTorneo>len(P):
        nTorneo=len(P)
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
    if nTorneo>len(P):
        nTorneo=len(P)
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


def seleccionClearing(Po, Ev, distanciaMinima):
    P = np.array(Po).copy()
    E = np.array(Ev).copy()
    outP = []
    outE = []
    [P, E] = ordenarPoblacion(P, E)

    indice = 1
    individuoAux = P[indice]
    costeAux = E[indice]
    stop = False

    while not stop:
        # Para comparar
        outP.append(P[0])
        outE.append(E[0])

        Paux = []
        Eaux = []

        for i in range(len(P)):
            d = distanciaHamming(outP[-1], P[i])
            if sum(d) > distanciaMinima:
                Paux.append(P[i])
                Eaux.append(E[i])
        if len(Paux) > 0:
            P = Paux
            E = Eaux
        else:
            stop = True

    if len(outP) == 1:
        outP.append(individuoAux)
        outE.append(costeAux)

    return np.array(outP), np.array(outE)


def ordenarPoblacion(P, E):
    indices = np.argsort(E)
    outP = []
    outE = []
    for i in range(len(indices)):
        outP.append(P[indices[i]])
        outE.append(E[indices[i]])
    return np.array(outP), np.array(outE)


def distanciaHamming(v1, v2):
    diferencia = abs(v1 - v2)
    diferencia[diferencia > 0] = 1
    return diferencia


def estudioParametros(semillas, nClearing=10, distanciaMinima=2, nIndividuos=15):
    costes = []
    tiempos = []
    if type(nClearing) == list:
        for i in nClearing:
            t = time.time()
            costes.append(np.array(geneticoMultimodal(semillas, nClearing=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nClearing
        label = "Generaciones entre operaciones de aclarado"
    elif type(distanciaMinima) == list:
        for i in distanciaMinima:
            t = time.time()
            costes.append(np.array(geneticoMultimodal(semillas, distanciaMinima=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = distanciaMinima
        label = "Distancia minima"
    elif type(nIndividuos) == list:
        for i in nIndividuos:
            t = time.time()
            costes.append(np.array(geneticoMultimodal(semillas, nIndividuos=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nIndividuos
        label = "Numero de individuos"
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
