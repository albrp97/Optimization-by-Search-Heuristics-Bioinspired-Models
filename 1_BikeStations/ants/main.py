import random
import numpy as np
from ants import SH,SHE,SCH
from funcionesAuxiliares import Hormigas

a="a280.tsp"
b="ch130.tsp"

semillas=[10,20,30]

# SH.SistemaHormigas(semillas,a)
# SHE.SistemaHormigasElitista(semillas,a)
SCH.SistemaColoniasHormigas(semillas,a)