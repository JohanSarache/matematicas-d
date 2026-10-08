import numpy as np
import matplotlib.pyplot as plt

from metodos import *


# ============================================================
# FUNCIONES VISTAS EN CLASE
# ============================================================

def simpsoncomp(x, y):
    L = len(x)-1

    if L % 2:
        raise ValueError("Atencion: Tiene que dar una cantidad impar de datos.")

    h = (x[-1]-x[0])/(L/2)

    Q = h/6 * (y[0] + 4*sum(y[1:-1:2])
               + 2*sum(y[2:-2:2]) + y[-1])

    return Q


# ============================================================
# SISTEMA DE ECUACIONES DIFERENCIALES
# ============================================================

def f(t, y):
    x1, x2 = y
    return np.array([-t*x2, t*x1-t*x2])


# Condición inicial
y0 = [-1, 1]


# ============================================================
# (a) TRAYECTORIA DURANTE LOS PRIMEROS 20 SEGUNDOS
# ============================================================

# Utilizamos h = 0.1, por lo tanto L = 200
t, y = rk4(f, [0, 20], y0, 200)

plt.figure()
plt.plot(y[:, 0], y[:, 1], label="Trayectoria")

plt.plot(y[0, 0], y[0, 1], 'go', label="Inicio")
plt.plot(y[-1, 0], y[-1, 1], 'ro', label="Final")

plt.xlabel("$x_1$")
plt.ylabel("$x_2$")
plt.title("Trayectoria de la partícula")
plt.axis("equal")
plt.grid()
plt.legend()
plt.show()


# ============================================================
# (b) POSICIÓN Y RAPIDEZ A LOS 3 SEGUNDOS
# ============================================================

# RK4 con h = 0.1, entonces L = 30
t3, y3 = rk4(f, [0, 3], y0, 30)

# Posición a los 3 segundos
posicion = y3[-1]

# Vector velocidad a los 3 segundos
velocidad = f(3, posicion)

# Rapidez: norma del vector velocidad
rapidez = np.linalg.norm(velocidad)

print("\nINCISO (b)")
print("Posición a los 3 segundos:", posicion)
print("Rapidez a los 3 segundos:", rapidez)


# ============================================================
# (c) ESTIMACIÓN DE DÍGITOS CORRECTOS
# ============================================================

# Calculamos una solución de referencia con h = 0.001
t_ref, y_ref = rk4(f, [0, 3], y0, 3000)

pos_ref = y_ref[-1]
rapidez_ref = np.linalg.norm(f(3, pos_ref))

# Resultados obtenidos con h = 0.1
aprox = np.array([posicion[0], posicion[1], rapidez])

# Resultados de referencia
ref = np.array([pos_ref[0], pos_ref[1], rapidez_ref])

nombres = ["x1(3)", "x2(3)", "Rapidez"]

print("\nINCISO (c)")

for i in range(3):
    error_rel = abs(aprox[i] - ref[i]) / abs(ref[i])

    # Estimación orientativa de cifras significativas
    cifras = max(0, int(np.floor(-np.log10(error_rel))))

    print(nombres[i])
    print("  Error relativo:", error_rel)
    print("  Cifras estimadas:", cifras)


# ============================================================
# (d) DISTANCIA RECORRIDA
# ============================================================

# Calculamos la rapidez en cada instante
rapideces = np.zeros(len(t))
for i in range(len(t)):
    rapideces[i] = np.linalg.norm(f(t[i], y[i]))


# Distancia desde t = 0 hasta t = 3
# Con h = 0.1, t = 3 corresponde al índice 30
D1 = simpsoncomp(t[:31], rapideces[:31])

# Distancia desde t = 3 hasta t = 20
D2 = simpsoncomp(t[30:], rapideces[30:])

print("\nINCISO (d)")
print("Distancia de 0 a 3 segundos:", D1)
print("Distancia de 3 a 20 segundos:", D2)
print("Distancia total:", D1 + D2)


# Refinamos el cálculo con h = 0.001
t_fino, y_fino = rk4(f, [0, 20], y0, 20000)

rapideces_fino = np.zeros(len(t_fino))
for i in range(len(t_fino)):
    rapideces_fino[i] = np.linalg.norm(f(t_fino[i], y_fino[i]))

# Con h = 0.001, t = 3 corresponde al índice 3000
D1_fino = simpsoncomp(t_fino[:3001], rapideces_fino[:3001])
D2_fino = simpsoncomp(t_fino[3000:], rapideces_fino[3000:])

print("\nDistancias con h = 0.001")
print("Distancia de 0 a 3 segundos:", D1_fino)
print("Distancia de 3 a 20 segundos:", D2_fino)


# ============================================================
# (e) DISTANCIA AL ORIGEN MENOR QUE 0.01
# ============================================================

# Distancia de la partícula al origen
distancias = np.zeros(len(t_fino))

for i in range(len(t_fino)):
    distancias[i] = np.sqrt(y_fino[i, 0]**2 + y_fino[i, 1]**2)

# Buscamos los índices donde la distancia es menor que 0.01
indices = np.where(distancias < 0.01)[0]

print("\nINCISO (e)")

if len(indices) > 0:
    i = indices[0]

    print("Primer instante en la malla:", t_fino[i])
    print("Distancia al origen:", distancias[i])

    # Verificamos también en los puntos posteriores de la malla
    print("¿Permanece dentro en la malla?",
          np.all(distancias[i:] < 0.01))

else:
    print("No se alcanzó una distancia menor que 0.01")
