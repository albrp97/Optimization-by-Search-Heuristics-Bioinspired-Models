import numpy as np
from funcionesAuxiliares import Estaciones,GreedyAleatoria
import BusquedaAleatoria,BusquedaLocal,EnfriamientoSimulado,BusquedaTabu

# Inicia la lectura de plazas ocupadas inicialmente
e = Estaciones.estaciones()

semillas = [10, 20, 30, 40, 50]

# ------
# GREEDY
# ------

# print("\nGREEDY\n")
# solGreedy=GreedyAleatoria.generarSolucionGreedy(e.movimientosIniciales)
# print("SOLUCION\t\t\t\t\t\t\t\t\t\t\tPLAZAS\t\tCOSTE")
# print(f"{solGreedy}\t{solGreedy.sum()}\t\t\t{e.evalua(solGreedy)}")

# ------------------
# BUSQUEDA ALEATORIA
# ------------------

# BusquedaAleatoria.BAramdom()

# ------------------
# BUSQUEDA LOCAL
# ------------------

# BusquedaLocal.busquedaLocal(semillas,grafica=False)

# BusquedaLocal.estudioParametros(semillas,nLote=[10,20,30,40,50,60,70])

# ---------------------
# ENFRIAMIENTO SIMULADO
# ---------------------

# Para sacar phi y mu. 0.11 y 0.11 para media 90 y min 85

# a=[]
# for x in range(200):
#     print(x)
#     a.append(EnfriamientoSimulado.estudioMuPhi())
# print(np.array(a).mean())

# EnfriamientoSimulado.estudioParametros(semillas,nCambio=[2,3])

# EnfriamientoSimulado.enfriamientoSimulado(semillas,grafica=False)

# -------------
# BUSQUEDA TABU
# -------------

# [sols,costes,_]=BusquedaTabu.busquedaTabu(semillas,grafica=False)

# i=np.argmin(costes)
# print(sols[i])
# print(costes[i])

# BusquedaTabu.estudioParametros(semillas,nVecinos=[28,29,30,31,32])

# -----------
# COMPARACION
# -----------

# indices=["Algoritmo","Media Ev.","Mejor Ev.","Desv. Ev","Media Costes","Mejor Coste","Desv. Costes"]
# filas=[]
# sol=GreedyAleatoria.generarSolucionGreedy(e.movimientosIniciales)
# coste=round(e.evalua(sol),2)
# filas.append(["Greedy ",1,1,0,coste,coste,0])
#
# print("Aleatoria: ",end="")
# [sol,coste,ev]=BusquedaAleatoria.BArSemillas(semillas,mostrar=False)
# filas.append(["Aleatoria",round(np.array(ev).mean(),2),round(min(ev),2),round(np.array(ev).std(),2),round(np.array(coste).mean(),2),round(min(coste),2),round(np.array(coste).std(),2)])
# print(round(min(coste),2))
#
# print("BL: ",end="")
# [sol,coste,ev]=BusquedaLocal.busquedaLocal(semillas,mostrar=False,grafica=False)
# filas.append(["Busqueda Local",round(np.array(ev).mean(),2),round(min(ev),2),round(np.array(ev).std(),2),round(np.array(coste).mean(),2),round(min(coste),2),round(np.array(coste).std(),2)])
# print(round(min(coste),2))
#
# print("Enfriamiento: ",end="")
# [sol,coste,ev]=EnfriamientoSimulado.enfriamientoSimulado(semillas,mostrar=False,grafica=False)
# filas.append(["Enfriamiento Simulado",round(np.array(ev).mean(),2),round(min(ev),2),round(np.array(ev).std(),2),round(np.array(coste).mean(),2),round(min(coste),2),round(np.array(coste).std(),2)])
# print(round(min(coste),2))
#
# print("Tabu: ",end="")
# [sol,coste,ev]=BusquedaTabu.busquedaTabu(semillas,mostrar=True,grafica=False)
# filas.append(["Busqueda Tabu",round(np.array(ev).mean(),2),round(min(ev),2),round(np.array(ev).std(),2),round(np.array(coste).mean(),2),round(min(coste),2),round(np.array(coste).std(),2)])
# print(round(min(coste),2))
#
#
# for i in indices:
#     print(i,end="\t")
# print("")
# for i in filas:
#     for j in i:
#         print(f"{j}",end="\t\t")
#     print("")