import numpy as np 
import matplotlib.pyplot as plt
from metodos import *
import pandas as pd

def pesosNC(n):
    # Calcula los pesos de la fórmula de Newton-Cotes de n puntos
    x = np.linspace(0, 1, n)
    A = np.ones((n, n))
    for i in range(1, n):
        A[i, :] = A[i-1, :] * x
    b = 1 / np.arange(1, n+1)
    w = np.linalg.solve(A, b)
    return w

def integralNC(f,a,b,n):
    w = pesosNC(n)
    x = np.linspace(a,b,n)
    y = f(x)
    Q = (b - a)*np.sum(y * w)
    return Q

def intNCcompuesta(f, a, b, L, n):
    z = np.linspace(a, b, L + 1)
    h = (b - a) / L
    w = pesosNC(n)
    Q = 0
    for i in range(L):
        x = np.linspace(z[i], z[i+1], n)
        y = f(x)
        Q += h * np.sum(y * w)
    return Q

Sigma = 0.8

def S(I):
    f = lambda nu: np.log(1+I*nu**2)
    Int = intNCcompuesta(f, 0, 1, 100, 3)
    return Int

def F(s,I):
    return Sigma*S(I)*I

inter = [0,1]; s0 = np.array([1])

s1,I1 = rk4(F, inter, s0, 200)
Is1 = I1[::20]

s2,I2 = rk4(F, inter, s0, 400)
Is2 = I2[::40]

data = {"I1":Is1[:,0], "I2":Is2[:,0]}
pf = pd.DataFrame(data)
print(pf)

