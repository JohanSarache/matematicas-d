import numpy as np
import matplotlib.pyplot as plt
from metodos import *

def f(t, y):
    z1,z2,z3=y
    return np.array([
        z2,z3,-4*np.sin(t)-2*np.cos(t)-2*z1-5*z2-4*z3
    ])

z0=np.array([1,0,-1])
intervalo=[0,2.5]

t,z= rk4(f, intervalo, z0, 200)
t,z4 = rk4(f, intervalo, z0, 400)

z1=z4[:,0]
z2=z4[:,1]
z3=z4[:,2]

print("y(2.5) con 200 pasos: ", z[:,0][-1])
print("y(2.5) con 400 pasos: ", z1[-1])
error = abs(z[:,0][-1]-z1[-1])  

print(
    "Dígitos son:",-int(np.log10(error)) 
    )

"""plt.plot(t,z1,label="z1")
plt.grid()
plt.show()"""

t15,z15= rk4(f, [0,15], z0, 1000)
plt.plot(t15,z15[:,1],label="y'(t)")
plt.xlabel("t")
plt.ylabel("y'(t)")
plt.grid()
plt.legend()
plt.show()

zr = z15[:,0]
k_max = np.where(
    (zr[1:-1] > zr[0:-2]) & (zr[1:-1] > zr[2:])
)[0]+1

tmax = t15[k_max]
T = np.diff(tmax)
print("Períodos: ",T)

tmin= np.where(
    np.isclose(zr,0,atol=1e-2)
)

tceros= t15[tmin]
Tceros = np.diff(tceros)
print("T: ",2*Tceros)