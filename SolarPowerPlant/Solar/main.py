import math
import random

import numpy as np

from SolarPowerPlant.Solar import Solar as s, Greedy, FuncionesAuxiliares as fa, BusquedaAleatoria, BusquedaLocal, EnfriamientoSimulado,BusquedaTabu

semillas = [10, 20, 30, 40, 50]

#################
# GREEDY
#################

# Greedy.greedy(mostrar=True)


#################
# BUSQUEDA ALEATORIA
#################

# print(BusquedaAleatoria.busquedaAleatoria(mostrar=True))

#################
# BUSQUEDA LOCAL
#################

# BusquedaLocal.busquedaLocal(semillas=semillas,grafica=False)

# BusquedaLocal.estudioParametros(semillas=semillas,nLote=[50,100,150,200,250,300,350])
# BusquedaLocal.estudioParametros(semillas=semillas,nLote=[50,60,70,80,90,100,110,120,130,140,150])
# BusquedaLocal.estudioParametros(semillas=semillas,nLote=[80,82,84,86,88,90,92,94,96,98,100])
#
# BusquedaLocal.estudioParametros(semillas=semillas,nCambio=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])

# BusquedaLocal.estudioParametros(semillas=semillas,nCambio=[1,2,3,4,5,12,19,20])

# BusquedaLocal.busquedaLocal(semillas,grafica=False)


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

BusquedaTabu.busquedaTabu(semillas)