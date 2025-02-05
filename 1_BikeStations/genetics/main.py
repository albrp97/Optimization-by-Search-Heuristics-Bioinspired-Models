import random
import time
import numpy as np
from funcionesAuxiliares import Estaciones, GreedyAleatoria

import VNS, GeneticoBasico, CHC,GeneticoMultimodal

# Inicia la lectura de plazas ocupadas inicialmente
e = Estaciones.estaciones()

semillas = [10, 20, 30, 40, 50]

# Limite de 30 min

# ---
# VNS
# ---

# VNS.estudioParametros(semillas, maxIteraciones=[25,50,75,100])

# [soluciones,costes,iteraciones]=VNS.VNS(semillas,grafica=False)
# b=np.array(iteraciones)
# a=[]
# for sol in soluciones:
#     a.append(e.evalua(sol))
# a=np.array([a])
# print(round(b.mean(),2))
# print(round(b.min(),2))
# print(round(b.std(),2))
# print(round(a.mean(),2))
# print(round(a.min(),2))
# print(round(a.std(),2))
#     print(e.evalua(sol))
# print(iteraciones)

# a=np.array([269.9904727423709, 275.70070460479866, 276.51339377912103, 276.3913268570024, 239.7776664318583])
# b=np.array([35641, 33641, 39961, 29161, 37241])

# ---------------
# GENETICO BASICO
# ---------------

# GeneticoBasico.estudioParametros(semillas,nMutacion=[5,10,15,20,25,30])

# [soluciones,costes,iteraciones]=GeneticoBasico.geneticoBasico(semillas,grafica=False)
#
# a=[]
# for sol in soluciones:
#     a.append(e.evalua(sol))
# print(a)
# print(iteraciones)
#
# a=np.array([272.7947000380668, 284.2663910407856, 273.1751235657079, 275.84464752660676, 265.79519703323626])
# b=np.array([34270, 62942, 48734, 48190, 116158])





# ---
# CHC
# ---

# print(CHC.CHC([10,20],grafica=False))

# 409.26809738468864, 411.5186093617613

# CHC.estudioParametros(semillas,nElite=[4,6,8,10,12,14])

# [soluciones,costes,iteraciones]=CHC.CHC(semillas,grafica=False)
#
# a=[]
# for sol in soluciones:
#     a.append(e.evalua(sol))
# print(a)
# print(iteraciones)

# a=np.array([269.26809738468864, 271.5186093617613, 267.53745219174357, 293.8387833187429, 272.7657548715179])
# b=np.array([46160, 43926, 52674, 40568, 45172])



# -------------------
# GENETICO MULTIMODAL
# -------------------

# GeneticoMultimodal.estudioParametros(semillas,distanciaMinima=[1,2,3,4,5,6,7,8,9,10])

# [soluciones,costes,iteraciones]=GeneticoMultimodal.geneticoMultimodal(semillas,grafica=False)
#
# a=[]
# for sol in soluciones:
#     a.append(e.evalua(sol))
# print(a)
# print(iteraciones)

# a=np.array([274.77471580862897, 267.8291517460243, 258.757125493376, 263.8318579539716, 262.37421041605904])
# b=np.array([23353, 38932, 37420, 23623, 40228])
#

