import numpy as np
import matplotlib.pyplot as plt
from metodos import *

A1 = 0.5; A2 = 0.3; E1 = 1000; E2 = 1500; R=1.9872
Cv= 18; DH1 = 2000; DH2 = 1200
# CA, CB, T =y
f = lambda t, y: np.array([
    -A1*np.exp(-E1/(R*y[2]))*y[0],
    A1*np.exp(-E1/(R*y[2]))*y[0]-A2*np.exp(-E2/(R*y[2]))*y[1],
    1/Cv*(A1*np.exp(-E1/(R*y[2]))*y[0]*DH1+A2*np.exp(-E2/(R*y[2]))*y[1]*DH2)
])

y0 = np.array([0.5,0,298])
intervalo = [0, 30]

t,R= rk4(f, intervalo, y0, 1000)
t2,R2= rk4(f, intervalo, y0, 2000)

ErroCA = abs(R[:,0][-1]-R2[:,0][-1])
ErroCB = abs(R[:,1][-1]-R2[:,1][-1])
print(f"El error de CA {ErroCA} y CB {ErroCB}")

