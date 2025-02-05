import random
import numpy as np

nSlots = 220


# Genera solucion greedy con round
def generarSolucionGreedy(ocupados):
    sum = 0
    nEstaciones = len(ocupados)
    ocupadosIniciales = np.zeros(nEstaciones, dtype=int)
    solGreedy = np.zeros(nEstaciones, dtype=int)
    for i in range(nEstaciones):
        ocupadosIniciales[i] = ocupados[i][1]
        sum += ocupadosIniciales[i]
    for i in range(nEstaciones):
        solGreedy[i] = round(nSlots * ocupadosIniciales[i] / sum)
    return solGreedy


# Mueve en una solucion n plazas de 2 estaciones aleatorias
def generadorMovimientoAleatorio(sol, n):
    solucion = sol.copy()
    e1 = random.randint(0, len(solucion) - 1)
    e2 = random.randint(0, len(solucion) - 1)
    if e1 == e2:
        if e1 == len(solucion) - 1:
            e1 -= 1
        else:
            e1 += 1
    if solucion[e1] - n < 0:
        n = solucion[e1]
    solucion[e1] -= n
    solucion[e2] += n
    return solucion.copy()

# Mueve en una solucion n plazas de 2 estaciones aleatorias y devuelve las estaciones modificadas con sus valores
def generadorMovimientoAleatorioTabu(sol, n):
    solucion = sol.copy()
    e1 = random.randint(0, len(solucion) - 1)
    e2 = random.randint(0, len(solucion) - 1)
    if e1 == e2:
        if e1 == len(solucion) - 1:
            e1 -= 1
        else:
            e1 += 1
    if solucion[e1] - n < 0:
        n = solucion[e1]
    solucion[e1] -= n
    solucion[e2] += n
    movimiento = [e1, e2]
    return solucion.copy(), movimiento

# Mueve n plazas en una solucion de e1 a e2
def generadorMovimiento(sol, e1, e2, n):
    solucion = sol.copy()
    if solucion[e1] - n < 0:
        n = solucion[e1]
    solucion[e1] -= n
    solucion[e2] += n
    return solucion

# Crea una solucion aleatoria a partir de un random con seed
def generarSolucionAleatoria(r):
    ran = np.zeros(16, dtype=int)
    solucion = np.zeros(16, dtype=int)
    sum = 0
    sum2 = 0
    for i in range(16):
        ran[i] = r.randint(2, 10)
        sum += ran[i]
    for i in range(16):
        solucion[i] = int(nSlots * (ran[i] / sum))
        sum2 += solucion[i]
    if sum2 < 205:
        solucion[r.randint(0, 15)] += 205 - sum2
        print(sum2)
        print(solucion)
    if sum2 > 220:
        solucion[r.randint(0, 15)] -= 220 - sum2
        print(sum2)
        print(solucion)
    return solucion.copy()

def mutar(sol,n=3):
    solucion=np.array(sol)
    r=random.randint(0,len(solucion)-1)
    solucion[r]=round(random.gauss(solucion[r],n))
    if solucion[r]<0:
        solucion[r]=0
    return solucion