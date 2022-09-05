import random
import numpy as np
from BikeStations.funcionesAuxiliares import Estaciones as e, GreedyAleatoria

e = e.estaciones()

#Metodo por defecto. 5 semillas aleatorias
def BAramdom():
    return BArandomN(5)

#Recibe el numero de semillas aleatorias para generar
def BArandomN(n):
    semillas = np.zeros(n, dtype=int)
    for i in range(n):
        semillas[i] = random.randint(0, 999)
    return BArSemillas(semillas)

#Genera 100 soluciones por cada semilla en array semillas
def BArSemillas(semillas,mostrar=True):
    if mostrar:
        print("\nBUSQUEDA ALEATORIA\n")
    soluciones=[]
    kms=[]
    it=[]
    for i in range(len(semillas)):
        random.seed(semillas[i])
        solMinima = GreedyAleatoria.generarSolucionAleatoria(random)
        kmMinimo = e.evalua(solMinima)
        if mostrar:
            print(f"\n\nSemilla {i+1}: {semillas[i]}")
            print("\nSOLUCION INICIAL\t\t\t\t\t\t\t\t\tPLAZAS\t\tCOSTE")
            print(solMinima.__str__() + f"\t{solMinima.sum()}\t\t\t" + kmMinimo.__str__())
        iteraciones = 1
        for j in range(99):
            solActual = GreedyAleatoria.generarSolucionAleatoria(random)
            kmActual = e.evalua(solActual)
            iteraciones+=1
            if kmActual < kmMinimo:
                kmMinimo = kmActual
                solMinima = solActual
        if mostrar:
            print("SOLUCION FINAL\t\t\t\t\t\t\t\t\t\tPLAZAS\t\tCOSTE")
            print(solMinima.__str__() + f"\t{solMinima.sum()}\t\t\t" + kmMinimo.__str__())
        soluciones.append(solMinima)
        kms.append(kmMinimo)
        it.append(iteraciones)
    return np.array(soluciones),np.array(kms),np.array(it)