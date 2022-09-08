import random
import time
import numpy as np
import matplotlib.pyplot as plt

from SolarPowePlant.Solar import Solar as s, FuncionesAuxiliares as fa, Greedy


def CHC(semillas=np.random.randint(-999, 999, size=2), maxReinicios=75, nElite=5, nIndividuos=22, mostrar=True, grafica=True):
    soluciones = []
    costes = []
    evaluaciones = []

    xs = []
    ys = []

    if mostrar:
        print("\nCHC")
        print(
            f"\nParametros:\n\nNumero de individuos: {nIndividuos}\nReinicios maximos: {maxReinicios}\nIndividuos elites: {nElite}")

    for semilla in semillas:
        evaluacion = 0
        x = []
        y = []

        random.seed(semilla)
        np.random.seed(abs(semilla))

        nReinicios = 0
        d = int(nIndividuos / 4)

        # Iniciamos la poblacion
        P = iniciarPoblacion(nIndividuos)
        E = evaluarPoblacion(P)
        evaluacion += len(P)

        if grafica:
            x.append(nReinicios)
            y.append(-min(E))

        if mostrar:
            print("\n\n-----------------")
            print(f"Semilla: {semilla}")
            print("-----------------")
            indice = np.argmin(E)
            print(f"\nIteracion inicial. Mejor individuo {-E[indice]} - {P[indice]}")
            print("\nReinicios: ", end="")

        while nReinicios < maxReinicios:
            poblacionC = selectR(P)
            costeC = evaluarPoblacion(poblacionC)
            evaluacion += len(poblacionC)

            poblacionCRecombinado = recombinar(poblacionC, d)
            costeCRecombiando = evaluarPoblacion(poblacionCRecombinado)
            evaluacion += len(poblacionCRecombinado)

            P2 = P.copy()
            E2 = E.copy()
            [P, E] = selectS(poblacionC, costeC, poblacionCRecombinado, costeCRecombiando)
            [P, E] = ordenarPoblacion(P, E)
            [P2, E2] = ordenarPoblacion(P2, E2)

            indicesP = np.argsort(E)
            indicesP2 = np.argsort(E2)

            if (indicesP == indicesP2).all():
                d -= 1
            if d < 0:
                nReinicios += 1
                if nReinicios <= maxReinicios:
                    [P, E] = divergir(P, E, nElite, nIndividuos)
                    if mostrar:
                        print("*", end="")
                d = int(nIndividuos / 4)
                if grafica:
                    x.append(nReinicios)
                    y.append(-min(E))

        indice = np.argmin(E)
        soluciones.append(P[indice])
        costes.append(-E[indice])
        evaluaciones.append(evaluacion)
        if grafica:
            x.append(nReinicios)
            y.append(-min(E))
            xs.append(x)
            ys.append(y)
        if mostrar:
            print(f"\n\nIteracion final. Mejor individuo {-E[indice]} - {P[indice]}")

    if grafica:
        for i in range(len(xs)):
            plt.subplot(1, len(xs), i + 1)
            plt.plot(xs[i], ys[i])
            plt.xlabel('Iteracion')
            plt.ylabel('Ganancia')
            plt.title(f'Evolucion {i}')
        plt.show()

    return soluciones, costes, evaluaciones


def iniciarPoblacion(nIndividuos):
    P = [Greedy.greedy()[0]]
    for i in range(nIndividuos - 1):
        P.append(fa.generarSolucionAleatoria())
    return np.array(P)


def evaluarPoblacion(P):
    E = []
    for individuo in P:
        E.append(s.evalua(individuo))
    return np.array(E)


def selectR(P):
    poblacionC = np.array(P).copy()
    np.random.shuffle(poblacionC)
    return poblacionC


def selectS(poblacionC, costeC, poblacionCRecombinado, costeCRecombiando):
    for i in range(len(costeCRecombiando)):
        indice = np.argmax(costeC)
        if costeCRecombiando[i] < costeC[indice]:
            costeC[indice] = costeCRecombiando[i]
            poblacionC[indice] = poblacionCRecombinado[i]
    return poblacionC, costeC


def recombinar(poblacionC, d):
    out = []
    i = 0
    while i < len(poblacionC):
        distancia = distanciaHamming(np.array(poblacionC[i]), np.array(poblacionC[i + 1]))
        if sum(distancia) / 2 > d:
            indices = np.argwhere(distancia == 1)
            np.random.shuffle(indices)

            cambios = round(len(indices) / 2)
            if cambios < 1:
                cambios = 1
            for j in range(cambios):
                v1 = np.array(poblacionC[j]).copy()
                v2 = np.array(poblacionC[j + 1]).copy()
                v1[indices[j]] = poblacionC[j + 1][indices[j]]
                v2[indices[j]] = poblacionC[j][indices[j]]
                # Mutacion
                r = int(random.gauss(v1[indices[j]], 2))
                if r < -10:
                    r = -10
                elif r > 10:
                    r = 10
                v1[indices[j]] = r
                r = int(random.gauss(v1[indices[j]], 2))
                if r < -10:
                    r = -10
                elif r > 10:
                    r = 10
                v2[indices[j]] = r
            out.append(v1)
            out.append(v2)
        i += 2
    return np.array(out)


def distanciaHamming(v1, v2):
    diferencia = abs(v1 - v2)
    diferencia[diferencia > 0] = 1
    return diferencia


def ordenarPoblacion(P, E):
    indices = np.argsort(E)
    outP = []
    outE = []
    for i in range(len(indices)):
        outP.append(P[indices[i]])
        outE.append(E[indices[i]])
    return np.array(outP), np.array(outE)


def divergir(P, E, nElite, nIndividuos):
    outP = iniciarPoblacion(nIndividuos)
    outE = evaluarPoblacion(outP)

    indices = np.argsort(E)[0:nElite]

    outP[0:nElite] = P[indices]
    outE[0:nElite] = E[indices]

    return outP, outE


def estudioParametros(semillas, maxReinicios=75, nElite=5, nIndividuos=22):
    costes = []
    tiempos = []
    if type(maxReinicios) == list:
        for i in maxReinicios:
            t = time.time()
            costes.append(np.array(CHC(semillas, maxReinicios=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = maxReinicios
        label = "Numero de reinicios"
    elif type(nElite) == list:
        for i in nElite:
            t = time.time()
            costes.append(np.array(CHC(semillas, nElite=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nElite
        label = "Numero individuos elite"
    elif type(nIndividuos) == list:
        for i in nIndividuos:
            t = time.time()
            costes.append(np.array(CHC(semillas, nIndividuos=i, grafica=False)[1]).mean())
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
