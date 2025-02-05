import numpy as np
from csv import reader


class matrices():

    def __init__(self):
        self.nEstaciones = 0
        self.movimientosIniciales = []

    def movimientos(self):
        movimientos = []
        with open('../bicicletas/deltas_5m.csv') as lecturaMovimientos:
            r = reader(lecturaMovimientos)
            self.nEstaciones = len(next(r))
            movIni = next(r)
            movimientosIniciales = []
            estacion = 0
            for n in movIni:
                movimientosIniciales.append([estacion, n])
                self.movimientosIniciales = np.array(movimientosIniciales, dtype=int)
                estacion += 1
            for line in r:
                estacion = 0
                for mov in line:
                    if mov != '0':
                        movimiento = []
                        movimiento.append(estacion)
                        movimiento.append(int(mov) * 2)
                        movimientos.append(movimiento)
                    estacion += 1
        return np.array(movimientos)

    def cercanas(self):
        cercanas = []
        with open('../bicicletas/cercanas_indices.csv') as lecturaCercanas:
            r = reader(lecturaCercanas)
            next(r)
            for line in r:
                cercanas.append(line)
        return np.array(cercanas, dtype=int)

    def kmCercanos(self):
        kmCercanos = []
        with open('../bicicletas/cercanas_kms.csv') as lecturaKm:
            r = reader(lecturaKm)
            next(r)
            for line in r:
                kmCercanos.append(line)

        return (np.array(kmCercanos, dtype=float))
