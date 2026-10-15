import numpy as np
import matplotlib.pyplot as plt
from metodos import *

c,m,M,G = 12000, 80, 5e10, 6e-11

def f(t, y):
    z1,z2,z3,z4 = y
    return np.array([
        z2,
        z1*z4**2 + (c/m)/z1**3-M*G/z1**2,
        z4,   
        -2*(z2/z1)*z4
    ])
z0= np.array([60, -0.12, 0, 0.0016])
inter = [0,200]

t,z = rk4(f,inter, z0,  1000)
t2,z2 = rk4(f, inter,z0,  2000)

r1 = z[:,0][-1]
r2 = z2[:,0][-1]

theta1 = z[:,2][-1]
theta2 = z2[:,2][-1]
#(b) De su resultado con 5 cifras significativas
#  correctas, justificando cómo verificó que alcanzó
#  dicha precisión 
print(f"r1 = {r1:.8f}, r2 = {r2:.8f}")
print(f"theta1 = {theta1:.8f}, theta2 = {theta2:.8f}")

x = r1*np.cos(theta1)
y = r1*np.sin(theta1)
x2 = r2*np.cos(theta2)
y2 = r2*np.sin(theta2)

err_x = abs(x-x2)
err_y = abs(y-y2)
print(f"err_x = {err_x:.8e}, err_y = {err_y:.8e}")
print(f"Las coordenadas finales son: x = {x2:.8f}, y = {y2:.8f}")

err_r = abs(r1-r2)
err_theta = abs(theta1-theta2)
print(f"err_r = {err_r:.8e}, err_theta = {err_theta:.8e}")

plt.polar(z[:,0], z[:,2], label="1000 pasos")
plt.scatter(z[:,0][0], z[:,2][0], label="Inicio", s=4,color="red")
plt.grid()
plt.show()