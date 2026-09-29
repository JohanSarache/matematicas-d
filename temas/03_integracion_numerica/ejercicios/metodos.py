import numpy as np

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

def trapcomp(x,y):
    L=len(x)-1
    deltax=np.diff(x) #calcula la diferencia entre cada par de datos sucesivos
    Q=0
    for i in range(0,L):
        Q+=0.5*deltax[i]*(y[i]+y[i+1])
    return Q

def simpsoncomp(x,y):
    L=len(x)-1
    if L%2:
        raise ValueError("Atencion: Tiene que dar una cantidad impar de datos.")
        Q=np.nan
        return Q
    h = (x[-1]-x[0])/(L/2)
    Q = h/6 * (y[0] + 4*sum(y[1:-1:2]) + 2*sum(y[2:-2:2]) + y[-1])
    return Q