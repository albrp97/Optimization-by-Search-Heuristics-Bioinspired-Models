import random
import time
import numpy as np
import matplotlib.pyplot as plt

from SolarPowePlant.Solar import Solar as s, FuncionesAuxiliares as fa


def busquedaLocal(semillas=np.random.randint(-999, 999, size=5), nLote=90, nCambio=12, mostrar=True, grafica=True):
    """
    Ejecuta la busqueda local segun las semillas
    :param semillas: Array de semillas a ejecutar.e Default: 5 semillas aleatorias
    :param nLote: Tamaño de lote para buscar el primer mejor vecino. Default: 20
    :param nCambio: Tamaño del cambio al generar un vecino. Default: 2
    :param mostrar: Para mostrar por consola la informacion de la ejecucion
    :param grafica: Para mostrar la grafica de evolucion del algoritmo
    :return: Devuelve las soluciones, costes y evaluaciones ejecutadas
    """
    maxIteraciones = 3000
    soluciones = []
    costes = []
    evaluaciones = []

    xs = []
    ys = []

    if mostrar:
        print("\nBUSQUEDA LOCAL")
        print(f"\nParametros:\n\nTamaño de lote: {nLote}\nTamaño de cambio: {nCambio}\nIteraciones maximas: {maxIteraciones}")

    for semilla in semillas:
        x = []
        y = []

        random.seed(semilla)
        np.random.seed(abs(semilla))

        # Permutaciones para la generacion de los vecinos, unica para cada semilla
        permutaciones = []
        for i in range(s.tam):
            for j in range(s.tam):
                if i != j:
                    permutaciones.append([i, j])
        random.shuffle(permutaciones)
        nPermutaciones = len(permutaciones)

        # Solucion inicial
        solAct = fa.generarSolucionAleatoria()
        costeAct = s.evalua(solAct)

        solFinal = solAct
        costeFinal = costeAct

        iteracion = 0
        permutacion = 0

        x.append(iteracion)
        y.append(-costeFinal)

        if mostrar:
            print("\n\n-----------------")
            print(f"Semilla: {semilla}")
            print("-----------------")
            print("\nInicial")
            print(f"Ganancia: {-costeFinal}\t\tSolucion: {solFinal}")

        # Mientras no se recorran todas las permutaciones (hay mejora) o no se llegue al maximo de iteraciones
        while iteracion < maxIteraciones and permutacion < nPermutaciones:

            contadorLote = 0

            # Comprobamos los vecinos del lote
            while contadorLote < nLote and iteracion < 3000 and permutacion < nPermutaciones:
                solLote = fa.generarMovimientoPareja(solFinal, permutaciones[permutacion], nCambio)
                # solLote = fa.generarMovimiento(solFinal, permutaciones[permutacion][0], nCambio)
                costeLote = s.evalua(solLote)
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
                x.append(iteracion)
                y.append(-costeFinal)

        soluciones.append(solFinal)
        costes.append(-costeFinal)
        evaluaciones.append(iteracion)

        if mostrar:
            print("\n\nFinal")
            print(f"Ganancia: {-costeFinal}\t\tSolucion: {solFinal}")
            print(f"\nIteraciones: {iteracion}")

        x.append(iteracion)
        y.append(-costeFinal)

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

    return soluciones, costes, evaluaciones


def estudioParametros(semillas=np.random.randint(-999, 999, size=5), nLote=90, nCambio=12):
    """
    Metodo para comparar parametros en la Busqueda local
    """
    costes = []
    tiempos = []
    if type(nLote) == list:
        for i in nLote:
            t = time.time()
            costes.append(np.array(busquedaLocal(semillas, nLote=i, grafica=False)[1]).mean())
            tiempos.append((time.time() - t) / len(semillas))
        x = nLote
        label = "Tamaño de lotes"
    elif type(nCambio) == list:
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
