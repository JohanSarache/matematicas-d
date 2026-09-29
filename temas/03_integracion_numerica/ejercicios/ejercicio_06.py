"""
x (cm)       0 200 400 600 800 1000 1200
ρ(x) (g/cm3) 4 3.95 3.89 3.80 3.60 3.41 3.30
Ac(x) (cm2) 100 103 106 110 120 133 149.6
Barra L = 12 m
"""
import numpy as np
import pandas as pd
from metodos import *

x = np.array([0, 200, 400, 600, 800, 1000, 1200])
rho = np.array([4, 3.95, 3.89, 3.80, 3.60, 3.41, 3.30])
Ac = np.array([100, 103, 106, 110, 120, 133, 149.6])

# (a) calculo de la masa de la barra
L = 12 * 100  # cm
mt = trapcomp(x, rho * Ac)  # g
print(f"\nMasa con trapecio: {mt:.5f} g")

ms = simpsoncomp(x, rho * Ac)  # g
print(f"Masa con Simpson: {ms:.5f} g")

