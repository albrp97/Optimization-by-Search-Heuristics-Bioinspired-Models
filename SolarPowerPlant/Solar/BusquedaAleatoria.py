import random

import numpy as np
from SolarPowerPlant.Solar import Solar as s, FuncionesAuxiliares as fa


def busquedaAleatoria(semillas=np.random.randint(-999, 999, size=5), mostrar=False):
    soluciones = []
    costes = []
    evaluaciones = []

    if mostrar:
        print("\nBUSQUEDA ALEATORIA")

    for semilla in semillas:
        ev = 0

        random.seed(semilla)
        np.random.seed(abs(semilla))

        solMin = fa.generarSolucionAleatoria()
        costeMin = s.evalua(solMin)
        ev += 1
        if mostrar:
            print("\n------------------")
            print(f"Semilla: {semilla}")
            print("------------------")
            print("\nInicial")
            print(f"Ganancia: {-costeMin}\t\tSolucion: {solMin}")
        for i in range(99):
            solActual = np.random.randint(-10, 10 + 1, size=s.tam)
            costeActual = s.evalua(solActual)
            ev += 1
            if costeActual < costeMin:
                costeMin = costeActual
                solMin = solActual
        if mostrar:
            print("\nFinal")
            print(f"Ganancia: {-costeMin}\t\tSolucion: {solMin}")
        soluciones.append(solMin)
        costes.append(-costeMin)
        evaluaciones.append(ev)

    return np.array(soluciones), np.array(costes), np.array(evaluaciones)
