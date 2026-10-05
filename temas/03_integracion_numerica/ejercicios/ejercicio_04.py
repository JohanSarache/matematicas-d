import numpy as np
from metodos import *

t = np.array([0, 10, 20, 30, 35, 40, 45, 50])  # min
c = np.array([10, 35, 55, 52, 40, 37, 432, 34])  # mg/m³

m = trapcomp(t,c)

print("La cantidad de masa es: ", m, "mg")

