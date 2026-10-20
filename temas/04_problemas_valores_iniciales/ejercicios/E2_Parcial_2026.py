import numpy as np
import matplotlib.pyplot as plt
from metodos import *

beta1 = 0.15 ; gamma = 0.02; N = 10000 ; beta2 = 0.02

def f(t,y):
    s,I,R = y
    return(np.array([
        -beta1*s*I/N,
        beta1*s*I/N - gamma*I,
        gamma*I
    ]))

y0 = np.array([9990,10,0])
inter1 = [0,180]
t,Y = rk4(f, inter1, y0, 200)
s1 = Y[:,0][-1]
I1 = Y[:,1][-1]
R1 = Y[:,2][-1]

print(f"s: {s1}, I: {I1} , R: {R1}")
print()
print("La suma: ",s1+I1+R1)

# (b) Cambiando el valor de beta1 a 0.02 y repitiendo
#  el cálculo hasta 60 y despues a 180 

def f2(t,y):
    s,I,R = y
    return(np.array([
        -beta2*s*I/N,
        beta2*s*I/N - gamma*I,
        gamma*I
    ]))

t60,Y60 = rk4(f2, [0,60], y0, 200)
s60 = Y60[:,0]
I60 = Y60[:,1]
R60 = Y60[:,2]

y60 = np.array([s60[-1],I60[-1],R60[-1]])

t180,Y180 = rk4(f, [0,120], y60, 200)

print("A los 180 para b")
print()
print(f"s: {Y180[:,0][-1]}, I: {Y180[:,1][-1]} , R: {Y180[:,2][-1]}")

t2 = np.concatenate((t60,t180+60))
I2 = np.concatenate((Y60[:,1],Y180[:,1]))

plt.plot(t,Y[:,1] ,color="blue",label="caso a")
plt.plot(t2,I2,color="red",label="Caso b")
plt.grid()
plt.legend()
plt.show()



