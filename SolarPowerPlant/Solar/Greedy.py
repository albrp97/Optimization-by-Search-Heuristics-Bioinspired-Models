import statistics
from SolarPowerPlant.Solar import Solar as s

def greedy(mostrar=False):
    p=s.p
    media=statistics.mean(p)
    sol=[]
    for i in p:
        if i<media:
            sol.append(10)
        else:
            sol.append(-10)
    ganancia=-s.evalua(sol)
    if mostrar:
        print("\nGREEDY\n")
        print("GANANCIA\t\tSOLUCION")
        print(f"{round(ganancia,2)}\t\t{sol}")

    return sol,ganancia,1


