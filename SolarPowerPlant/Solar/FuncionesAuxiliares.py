import random
import numpy as np
from SolarPowerPlant.Solar import Solar as s


def generarSolucionAleatoria():
    return np.random.randint(-10, 10 + 1, size=s.tam)


def generarMovimiento(sol, hora, nCambio):
    """
    Genera un movimiento en una hora, aumentando o disminuyendo la compra/venta
    :param sol:
    :param hora:
    :param nCambio:
    :return:
    """
    solOut = sol.copy()
    a = solOut[hora]
    if a + nCambio < -10:
        nCambio = -10 - a
    elif a + nCambio > 10:
        nCambio = 10 - a

    solOut[hora] += nCambio

    return solOut


def generarMovimientoPareja(sol, horas, nCambio):
    """
    Varia en 2 horas la compra venta
    Ej: 0: vende 30 1:vende 10, con cambio de 10 -> 0: vende 40 1: vende 0
    :param sol:
    :param horas:
    :param nCambio:
    :return:
    """
    solOut = sol.copy()
    a = solOut[horas[0]]
    b = solOut[horas[1]]
    if a + nCambio < -10:
        nCambio = -10 - a
    elif a + nCambio > 10:
        nCambio = 10 - a
    if b - nCambio < -10:
        nCambio = 10 + b
    elif b - nCambio > 10:
        nCambio = 10 - b

    solOut[horas[0]] += nCambio
    solOut[horas[1]] -= nCambio

    return solOut


def generarMovimientoAleatorio(sol, nCambio):
    a = random.randint(0, len(sol) - 1)
    b = random.randint(0, len(sol) - 1)
    if a == b:
        if a == len(sol) - 1:
            a -= 1
        else:
            a += 1
    return generarMovimientoPareja(sol, [a, b], nCambio)

def generarMovimientoAleatorioTabu(sol,nCambio):
    a = random.randint(0, len(sol) - 1)
    b = random.randint(0, len(sol) - 1)
    if a == b:
        if a == len(sol) - 1:
            a -= 1
        else:
            a += 1
    return generarMovimientoPareja(sol, [a, b], nCambio),[a,b]


# s=[]
# for i in range(24):
#     s.append(random.randint(-10,10))
#
# nCambio=3
# print(s)
# print(generarMovimientoAleatorio(s,nCambio,random.random()))


# total=0

# 48
# for i in range(len(s)):
#     generarMovimiento(s,i,nCambio)
#     generarMovimiento(s, i, -nCambio)
#     total+=2

# 552
# for i in range(len(s)):
#     for j in range(len(s)):
#         if i!=j:
#             generarMovimientoPareja(s,[i,j],3)
#             # generarMovimientoPareja(s, [i+1, i], 3)
#             total+=1

# print(total)
