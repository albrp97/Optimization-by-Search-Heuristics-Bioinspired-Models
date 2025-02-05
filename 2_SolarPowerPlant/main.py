import math
import random

import numpy as np

from SolarPowePlant.Solar import Solar as s, Greedy, FuncionesAuxiliares as fa, BusquedaAleatoria, BusquedaLocal, EnfriamientoSimulado, BusquedaTabu, GeneticoBasico, CHC, GeneticoMultimodal

semillas = [10, 20, 30, 40, 50]

#################
# ENTRADA
#################

# Para modificar R y P

# np.random.seed(10)
#
# pp=[]
# for i in range(s.tam):
#     r=np.random.randint(20,40)/100
#     pp.append(r)
# s.p=pp
#
# rr=[]
# for i in range(s.tam):
#     r=np.random.randint(0,900)
#     rr.append(r)
# s.r=rr
#
# print(f"p: {s.p}")
# print(f"r: {s.r}")


#################
# GREEDY
#################

# Greedy.greedy(mostrar=True)


#################
# BUSQUEDA ALEATORIA
#################

# BusquedaAleatoria.busquedaAleatoria(semillas,mostrar=True)


#################
# BUSQUEDA LOCAL
#################

# BusquedaLocal.busquedaLocal(semillas=semillas,grafica=False)

# BusquedaLocal.estudioParametros(semillas=semillas,nLote=[50,100,150,200,250,300,350])
# BusquedaLocal.estudioParametros(semillas=semillas,nLote=[50,60,70,80,90,100,110,120,130,140,150])
# BusquedaLocal.estudioParametros(semillas=semillas,nLote=[80,82,84,86,88,90,92,94,96,98,100])

# BusquedaLocal.estudioParametros(semillas=semillas,nCambio=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])

# BusquedaLocal.busquedaLocal(semillas)


#################
# ENFRIAMIENTO SIMULADO
#################

# print(EnfriamientoSimulado.temperaturaInicial())

# EnfriamientoSimulado.enfriamientoSimulado(semillas=[10])

# EnfriamientoSimulado.estudioParametros(semillas,maxIteraciones=[50,75,100,125,150,175,200,225,250])
# EnfriamientoSimulado.estudioParametros(semillas,nVecinos=[16,18,20,22,24,26])
# EnfriamientoSimulado.estudioParametros(semillas,nCambio=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])

# EnfriamientoSimulado.enfriamientoSimulado(semillas)


#################
# BUSQUEDA TABU
#################

# BusquedaTabu.busquedaTabu(semillas)

# BusquedaTabu.estudioParametros(semillas,nCambio=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
# BusquedaTabu.estudioParametros(semillas,nVecinos=[10,15,20,25,30,35,40,45,50,75,100])
# BusquedaTabu.estudioParametros(semillas,divisionFrecuencia=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21])
# BusquedaTabu.estudioParametros(semillas,maxIteraciones=[100,125,150,175,200,225,250,275,300])
# BusquedaTabu.estudioParametros(semillas,nReiniciaciones=[1,2,3,4,5,6,7,8,9,10])

# BusquedaTabu.busquedaTabu(semillas)


#################
# GENETICO BASICO
#################

# GeneticoBasico.estudioParametros(semillas,nIndividuos=[15,20,25,30])
# GeneticoBasico.estudioParametros(semillas,maxIteraciones=[500,600,700,800,900,1000,1100,1200,1300,1400,1500])
# GeneticoBasico.estudioParametros(semillas,nSeleccion=[15,20,25,30,35,40,45,50,55])
# GeneticoBasico.estudioParametros(semillas,nMutacion=[5,10,15,20,25])
# GeneticoBasico.estudioParametros(semillas,nReemplazo=[15,20,25,30,35,40,45,50,55])

# GeneticoBasico.geneticoBasico(semillas)


#################
# CHC
#################

# CHC.CHC(semillas)

# CHC.estudioParametros(semillas,maxReinicios=[50,60,70,80,90,100,110,120,130,140,150])
# CHC.estudioParametros(semillas,nElite=list(range(10)))
# CHC.estudioParametros(semillas,nIndividuos=[16,18,20,22,24,26])

# CHC.CHC(semillas)


#################
# GENETICO MULTIMODAL
#################

# GeneticoMultimodal.geneticoMultimodal(semillas)

# GeneticoMultimodal.estudioParametros(semillas,nClearing=[10,20,30,40,50,60,70,80,90,100,110,120,130,140,150])
# GeneticoMultimodal.estudioParametros(semillas,distanciaMinima=list(range(10)))
# GeneticoMultimodal.estudioParametros(semillas,nIndividuos=[15,20,25,30])

# GeneticoMultimodal.geneticoMultimodal(semillas)


#################
# COMPARACION
#################

print("\nGreedy")
f = Greedy.greedy(mostrar=False)
a = round(f[1],3)
print(f"{1} - {1} - {0} - {a} - {a} - {0}")

print("\nAleatoria")
f = BusquedaAleatoria.busquedaAleatoria(semillas, mostrar=False)
a = np.array(f[1])
b = np.array(f[2])
print(f"{round(b.mean(),3)} - {round(min(b),3)} - {round(b.std(),3)} - {round(a.mean(),3)} - {round(max(a),3)} - {round(a.std(),3)}")

print("\nBusqueda local")
f = BusquedaLocal.busquedaLocal(semillas, mostrar=False, grafica=False)
a = np.array(f[1])
b = np.array(f[2])
print(f"{round(b.mean(),3)} - {round(min(b),3)} - {round(b.std(),3)} - {round(a.mean(),3)} - {round(max(a),3)} - {round(a.std(),3)}")

print("\nEnfriamiento")
f = EnfriamientoSimulado.enfriamientoSimulado(semillas, mostrar=False, grafica=False)
a = np.array(f[1])
b = np.array(f[2])
print(f"{round(b.mean(),3)} - {round(min(b),3)} - {round(b.std(),3)} - {round(a.mean(),3)} - {round(max(a),3)} - {round(a.std(),3)}")

print("\nBusqueda tabu")
f = BusquedaTabu.busquedaTabu(semillas, mostrar=False, grafica=False)
a = np.array(f[1])
b = np.array(f[2])
print(f"{round(b.mean(),3)} - {round(min(b),3)} - {round(b.std(),3)} - {round(a.mean(),3)} - {round(max(a),3)} - {round(a.std(),3)}")

print("\nGenetico")
f = GeneticoBasico.geneticoBasico(semillas, mostrar=False, grafica=False)
a = np.array(f[1])
b = np.array(f[2])
print(f"{round(b.mean(),3)} - {round(min(b),3)} - {round(b.std(),3)} - {round(a.mean(),3)} - {round(max(a),3)} - {round(a.std(),3)}")

print("\nCHC")
f = CHC.CHC(semillas, mostrar=False, grafica=False)
a = np.array(f[1])
b = np.array(f[2])
print(f"{round(b.mean(),3)} - {round(min(b),3)} - {round(b.std(),3)} - {round(a.mean(),3)} - {round(max(a),3)} - {round(a.std(),3)}")

print("\nMultimodal")
f = GeneticoMultimodal.geneticoMultimodal(semillas, mostrar=False, grafica=False)
a = np.array(f[1])
b = np.array(f[2])
print(f"{round(b.mean(),3)} - {round(min(b),3)} - {round(b.std(),3)} - {round(a.mean(),3)} - {round(max(a),3)} - {round(a.std(),3)}")

