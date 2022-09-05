import numpy as np

np.set_printoptions(linewidth=160)

# Tamaño de cromosoma
tam = 24

# precio por hora en kW
p = [0.26, 0.26, .25, .24, .23, .24, .25, .27, .30, .29, .34, .32, .31, .31, .25, .24, .25, .26, .34, .36, .39, .4, .31, .29]

def evalua(sol):
    # Sol va tener 24 elementos (por cada hora) de numeros entre 0 y 10
    # estos *10 representan el porcentaje de kw que se van a comprar (positivo) o vender (negativo)
    # La cantidad de compra es lo que cabe en la bateria * sol o lo que se ha generado en el dia si es menos
    # La cantidad de venta es lo almacenado en bateria * sol

    # radiacion por hora en W * m^2
    r = [0, 0, 0, 0, 0, 0, 0, 0, 100, 313, 500, 661, 786, 419, 865, 230, 239, 715, 634, 468, 285, 96, 0, 0]

    # m^2
    area = 1000
    rendimiento = .2
    # kW
    bateriaCapacidad = 500
    bateriaOcupada = 0

    # kW generados por la planta
    generado = []

    for i in r:
        generado.append(i * area * rendimiento / 1000)

    # por cada elemento de sol
    # ver si es negativo (vender) porcentaje de bateria
    # o positivo (comprar) porcentaje de bateria

    dineroFinal = 0


    for i in range(tam):
        a = sol[i] / 10

        if a < 0:
            a = -a
            cantidadBateria = bateriaOcupada * a
            dinero = cantidadBateria * p[i]

            dineroFinal += dinero
            bateriaOcupada -= cantidadBateria
        else:
            cantidadBateria = (bateriaCapacidad - bateriaOcupada) * a
            if cantidadBateria > generado[i]: cantidadBateria = generado[i]
            dinero = cantidadBateria * p[i]

            dineroFinal -= dinero
            bateriaOcupada += cantidadBateria


    # Los metodos estan hechos para minimizar para el escenario de junio
    # Para que maximice negamos la ganancia para convertirlo en coste
    # Cuando devolvamos las soluciones la negamos de nuevo
    return -dineroFinal

def evaluaMostrar(sol):
    # Sol va tener 24 elementos (por cada hora) de numeros entre -10 y 10
    # estos *10 representan el porcentaje de kw que se van a comprar (positivo) o vender (negativo)
    # La cantidad de compra es lo que cabe en la bateria * sol o lo que se ha generado en el dia si es menos
    # La cantidad de venta es lo almacenado en bateria * sol

    # radiacion por hora en W * m^2
    r = [0, 0, 0, 0, 0, 0, 0, 0, 100, 313, 500, 661, 786, 419, 865, 230, 239, 715, 634, 468, 285, 96, 0, 0]

    # m^2
    area = 1000
    rendimiento = .2
    # kW
    bateriaCapacidad = 500
    bateriaOcupada = 0

    # kW generados por la planta
    generado = []

    for i in r:
        generado.append(i * area * rendimiento / 1000)

    # por cada elemento de sol
    # ver si es negativo (vender) porcentaje de bateria
    # o positivo (comprar) porcentaje de bateria

    dineroFinal = 0

    print(f"Solucion a evaluar {sol}")

    for i in range(tam):
        a = sol[i] / 10
        print(f"\n\nHora {i}\n")
        print(f"Bateria actual {round(bateriaOcupada, 2)} kW")
        if a < 0:
            a = -a
            cantidadBateria = bateriaOcupada * a
            dinero = cantidadBateria * p[i]
            print(f"He vendido {round(cantidadBateria, 2)} kW ({a*100}%) por {p[i]} €/kW\nHe ganado {round(dinero, 2)} €")
            dineroFinal += dinero
            bateriaOcupada -= cantidadBateria
        else:
            cantidadBateria = (bateriaCapacidad - bateriaOcupada) * a
            if cantidadBateria > generado[i]: cantidadBateria = generado[i]
            dinero = cantidadBateria * p[i]
            print(f"He comprado {round(cantidadBateria, 2)} kW ({a*100}%) por {p[i]} €/kW\nHe gastado {round(dinero, 2)} €")
            dineroFinal -= dinero
            bateriaOcupada += cantidadBateria
        print(f"Bateria final {round(bateriaOcupada, 2)} kW")
    print(f"\nDinero total: {round(dineroFinal, 2)} €")

    # Los metodos estan hechos para minimizar para el escenario de junio
    # Para que maximice negamos la ganancia para convertirlo en coste
    # Cuando devolvamos las soluciones la negamos de nuevo
    return -dineroFinal
