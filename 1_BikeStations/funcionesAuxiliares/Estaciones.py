import numpy as np
from . import Matrices as m

mtr = m.matrices()


class estaciones():

    def __init__(self):
        self.movimientos = mtr.movimientos()
        self.nEstaciones = mtr.nEstaciones

        self.slots = np.array(np.zeros(self.nEstaciones, dtype=int))
        self.ocupados = np.array(np.zeros(self.nEstaciones, dtype=int))

        self.movimientosIniciales = mtr.movimientosIniciales


        self.cercanas = mtr.cercanas()
        self.kmCercanos = mtr.kmCercanos()

        self.nSlots = 220

    def getSlots(self):
        return self.slots.copy()

    def getOcupados(self):
        return self.ocupados.copy()

    def introducirIniciales(self):
        self.ocupados = np.array(np.zeros(self.nEstaciones, dtype=int))
        for movimiento in self.movimientosIniciales:
            self.mover(movimiento)

    def mover(self, movimiento):  # todo mirar si es negativo para sacar bicis y devolver kms
        km = 0
        if movimiento[1] > 0:
            km += self.meterBicis(movimiento[0], movimiento[1])
        else:
            km += self.sacarBicis(movimiento[0], abs(movimiento[1]))
        return km

    # meterBicis: mete en la estacion el nBicis indicado en el movimiento en forma de bloques
    # 1k iteraciones: 0.06 sec quitando introducciones de 0 bicis bajamos a 0.05
    # mas optimizado que hacer los movimientos uno a uno, y que no hacer la primera comprobacion (0.23 - 0.3)
    def meterBicis(self, estacion, nBicis):
        km = 0
        if self.ocupados[estacion] + nBicis <= self.slots[estacion]:
            self.ocupados[estacion] += nBicis
        else:
            bicisRestantes = nBicis
            bicisRestantes -= (self.slots[estacion] - self.ocupados[estacion])
            self.ocupados[estacion] += (self.slots[estacion] - self.ocupados[estacion])
            i = 1
            while (i < self.nEstaciones and bicisRestantes > 0):
                estacion2 = self.cercanas[estacion][i]
                if self.ocupados[estacion2] + bicisRestantes <= self.slots[estacion2]:
                    self.ocupados[estacion2] += bicisRestantes
                    km += (self.kmCercanos[estacion][i] * bicisRestantes)
                    bicisRestantes = 0
                elif (self.slots[estacion2] - self.ocupados[estacion2]) > 0:
                    bicisRestantes -= (self.slots[estacion2] - self.ocupados[estacion2])
                    km += (self.kmCercanos[estacion][i] * (self.slots[estacion2] - self.ocupados[estacion2]))
                    self.ocupados[estacion2] += (self.slots[estacion2] - self.ocupados[estacion2])
                i += 1
        return km

    # 1k iteraciones 0.04 porque no hace tantos accesos ni comprobaciones como meter bici, ya que compara con 0
    def sacarBicis(self, estacion, nBicis):
        km = 0
        if self.ocupados[estacion] - nBicis >= 0:
            self.ocupados[estacion] -= nBicis
        else:
            bicisRestantes = nBicis
            bicisRestantes -= self.ocupados[estacion]
            self.ocupados[estacion] = 0
            i = 1
            while (i < self.nEstaciones and bicisRestantes > 0):
                estacion2 = self.cercanas[estacion][i]
                if self.ocupados[estacion2] - bicisRestantes >= 0:
                    self.ocupados[estacion2] -= bicisRestantes
                    km += self.kmCercanos[estacion][i] * bicisRestantes
                    bicisRestantes = 0
                elif self.ocupados[estacion2] > 0:
                    bicisRestantes -= self.ocupados[estacion2]
                    km += self.kmCercanos[estacion][i] * self.ocupados[estacion2]
                    self.ocupados[estacion2] = 0
                i += 1
        return km * 3

    def evalua(self, inSlots):
        self.slots = inSlots.copy()
        km = 0
        self.introducirIniciales()
        for movimiento in self.movimientos:
            km += self.mover(movimiento)
        return km

    def evaluaCapacidad(self,sol,pesoExtra=5):
        if sum(sol)<205:
            return 1000
        else:
            return self.evalua(sol)+(sum(sol)-205)*pesoExtra
