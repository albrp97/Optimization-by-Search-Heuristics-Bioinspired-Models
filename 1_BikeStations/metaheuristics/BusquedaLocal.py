import random
import time
import numpy as np
import matplotlib.pyplot as plt

from funcionesAuxiliares import Estaciones as e, GreedyAleatoria

e = e.estaciones()

def busquedaLocal(semillas=np.random.randint(-999,999,size=5),nLote=20,nCambio=2,mostrar=True,grafica=True):
    """
    Ejecuta la busqueda local segun las semillas
    :param semillas: Array de semillas a ejecutar.e Default: 5 semillas aleatorias
    :param nLote: Tamaño de lote para buscar el primer mejor vecino. Default: 20
    :param nCambio: Tamaño del cambio al generar un vecino. Default: 2
    :param mostrar: Para mostrar por consola la informacion de la ejecucion
    :param grafica: Para mostrar la grafica de evolucion del algoritmo
    :return: Devuelve las soluciones, costes y evaluaciones ejecutadas
    """
    maxIteraciones=3000
    soluciones=[]
    costes=[]
    evaluaciones=[]

    xs=[]
    ys=[]

    if mostrar:
        print("\nBUSQUEDA LOCAL")
        print(f"\nParametros:\n\nTamaño de lote: {nLote}\nTamaño de cambio: {nCambio}\nIteraciones maximas: {maxIteraciones}")

    for semilla in semillas:
        x=[]
        y=[]

        #Permutaciones para la generacion de los vecinos, unica para cada semilla
        permutaciones=[]
        for i in range(16):
            for j in range(16):
                if i!=j:
                    permutaciones.append([i,j])
        random.seed(semilla)
        random.shuffle(permutaciones)
        nPermutaciones=len(permutaciones)


        #Solucion inicial
        random.seed(semilla)
        solAct= GreedyAleatoria.generarSolucionAleatoria(random)
        costeAct=e.evalua(solAct)

        solFinal=solAct
        costeFinal=costeAct

        iteracion = 0
        permutacion=0

        x.append(iteracion)
        y.append(costeFinal)

        if mostrar:
            print("\n\n-----------------")
            print(f"Semilla: {semilla}")
            print("-----------------")
            print("\nInicial")
            print(f"Solucion: {solFinal}\t\tCoste: {costeFinal}")



        #Mientras no se recorran todas las permutaciones (hay mejora) o no se llegue al maximo de iteraciones
        while iteracion<3000 and permutacion<nPermutaciones:

            contadorLote=0

            #Comprobamos los vecinos del lote
            while contadorLote<nLote and iteracion<3000 and permutacion<nPermutaciones:
                solLote= GreedyAleatoria.generadorMovimiento(solFinal, permutaciones[permutacion][0], permutaciones[permutacion][1], nCambio)
                costeLote=e.evalua(solLote)
                if costeLote<costeAct:
                    solAct=solLote
                    costeAct=costeLote
                contadorLote+=1
                iteracion+=1
                permutacion+=1

            #Si hay solucion en el lote
            if costeAct<costeFinal:
                solFinal=solAct
                costeFinal=costeAct
                permutacion=0
                x.append(iteracion)
                y.append(costeFinal)

        soluciones.append(solFinal)
        costes.append(costeFinal)
        evaluaciones.append(iteracion)

        if mostrar:
            print("\n\nFinal")
            print(f"Solucion: {solFinal}\t\tCoste: {costeFinal}")
            print(f"\nIteraciones: {iteracion}")

        x.append(iteracion)
        y.append(costeFinal)

        xs.append(x)
        ys.append(y)

    if grafica:
        for i in range(len(xs)):
            plt.subplot(1, len(xs), i + 1)
            plt.plot(xs[i], ys[i])
            plt.xlabel('Iteracion')
            plt.ylabel('Coste')
            plt.title(f'Evolucion {i}')
        plt.show()

    return soluciones,costes,evaluaciones

def estudioParametros(semillas,nLote=20,nCambio=2):
    """
    Metodo para comparar parametros en la Busqueda local
    :param semillas: Semillas a ejecutar
    :param nLote: Tamaño de lotes para primer mejor vecino
    :param nCambio: Tamaño de cambio al generar vecinos
    """
    costes=[]
    tiempos=[]
    if type(nLote)==list:
        for i in nLote:
            t=time.time()
            costes.append(np.array(busquedaLocal(semillas,nLote=i,grafica=False)[1]).mean())
            tiempos.append((time.time()-t)/len(semillas))
        x=nLote
        label="Tamaño de lotes"
    elif type(nCambio)==list:
        for i in nCambio:
            t = time.time()
            costes.append(np.array(busquedaLocal(semillas, nCambio=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nCambio
        label = "Tamaño de cambio"
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

def busquedaLocalSolucion(sol,semilla,nLote=20,nCambio=2):
    """
    Pasada una solucion ejecuta la busquedaLocal y devuelve la nueva solucion
    :param sol: Solucion inicial de la que parte
    :param semilla: Semilla que genera la solucion inicial
    :param nLote: Tamaño de lote para buscar el primer mejor vecino. Default: 20
    :param nCambio: Tamaño del cambio al generar un vecino. Default: 2
    :return: Devuelve nueva solucion, coste y evaluaciones ejecutadas
    """
    permutaciones = []
    for i in range(16):
        for j in range(16):
            if i != j:
                permutaciones.append([i, j])
    random.seed(semilla)
    random.shuffle(permutaciones)
    nPermutaciones = len(permutaciones)

    solAct=np.array(sol)
    costeAct = e.evalua(solAct)

    solFinal = solAct
    costeFinal = costeAct

    iteracion = 0
    permutacion = 0

    # Mientras no se recorran todas las permutaciones (hay mejora) o no se llegue al maximo de iteraciones
    while iteracion < 3000 and permutacion < nPermutaciones:

        contadorLote = 0

        # Comprobamos los vecinos del lote
        while contadorLote < nLote and iteracion < 3000 and permutacion < nPermutaciones:
            solLote = GreedyAleatoria.generadorMovimiento(solFinal, permutaciones[permutacion][0],
                                                          permutaciones[permutacion][1], nCambio)
            costeLote = e.evalua(solLote)
            if costeLote < costeAct:
                solAct = solLote
                costeAct = costeLote
            contadorLote += 1
            iteracion += 1
            permutacion += 1

        # Si hay solucion en el lote
        if costeAct < costeFinal:
            solFinal = solAct
            costeFinal = costeAct
            permutacion = 0

    return solFinal,costeFinal,iteracion