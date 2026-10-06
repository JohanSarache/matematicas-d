# ============================================================
# EJERCICIO 7 - Modelo predador-presa de Lotka-Volterra
#
# Se considera el sistema:
#
#     x1' = x1 * (3 - 0.002*x2)
#
#     x2' = -x2 * (0.5 - 0.0006*x1)
#
#
# (a) Identificar cuál variable representa a las presas y cuál
#     a los predadores.
#
#     Si x2 = 0:
#
#         x1' = 3*x1
#
#     por lo tanto x1 puede crecer aunque x2 no exista.
#
#     Si x1 = 0:
#
#         x2' = -0.5*x2
#
#     por lo tanto x2 disminuye y se extingue si x1 no existe.
#
#     Entonces:
#
#         x1 = población de presas
#         x2 = población de predadores
#
#
# (b) Graficar la evolución de las poblaciones para:
#
#         x1(0) = 1600
#         x2(0) = 800
#
#     utilizando RK4.
#
# (c) Determinar aproximadamente el período del ciclo.
#
# (d) Determinar el primer instante en el que ambas poblaciones
#     coinciden y calcular sus tasas de crecimiento instantáneas.
# ============================================================


import numpy as np
import matplotlib.pyplot as plt

from metodos import rk4


# ============================================================
# 1. Definición del sistema
# ============================================================

def f(t, x):

    x1 = x[0]     # Presas
    x2 = x[1]     # Predadores

    dx1 = x1 * (3 - 0.002*x2)

    dx2 = -x2 * (0.5 - 0.0006*x1)

    return np.array([dx1, dx2])


# ============================================================
# 2. Condiciones iniciales
# ============================================================

x0 = np.array([
    1600.0,   # Presas
    800.0     # Predadores
])


# ============================================================
# 3. Intervalo de tiempo
# ============================================================
#
# El tiempo se mide en meses.
#
# Se utiliza un intervalo suficientemente largo como para
# observar varios ciclos.

inter = [0, 20]


# Número de pasos
#
# Con L = 20000:
#
#     h = 20 / 20000 = 0.001 meses

L = 20000


# ============================================================
# 4. Resolución mediante RK4
# ============================================================

t, x = rk4(f, inter, x0, L)

# La función rk4 retorna:
#
#     x[:, 0] -> primera variable  -> presas
#     x[:, 1] -> segunda variable -> predadores

presas = x[:, 0]
predadores = x[:, 1]


# ============================================================
# PARTE (b)
# Evolución de las poblaciones
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(t, presas, label="Presas")

plt.plot(t, predadores, label="Predadores" )

plt.xlabel("Tiempo [meses]")
plt.ylabel("Población")
plt.title("Modelo predador-presa de Lotka-Volterra")
plt.grid()
plt.legend()
plt.tight_layout()

plt.show()

# ============================================================
# PARTE (c)
# Determinación del período
# ============================================================
#
# Una forma de obtener el período es localizar los máximos
# consecutivos de una de las poblaciones.
#
# Un punto i es un máximo local si:
#
#     presas[i] > presas[i-1]
#
# y
#
#     presas[i] > presas[i+1]
#
# Se excluyen los extremos del vector.


indices_max = np.where(
    (presas[1:-1] > presas[:-2])
    &
    (presas[1:-1] > presas[2:])
)[0] + 1


# Instantes en los que ocurren los máximos

tiempos_max = t[indices_max]


# El período se obtiene como la diferencia entre máximos
# consecutivos.

periodos = np.diff(tiempos_max)


# Se toma el promedio para reducir el efecto de la
# discretización temporal.

periodo = np.mean(periodos)


print("\n(c) " + "=" * 65)

print("Instantes de máximos consecutivos de las presas:")

print(tiempos_max)

print(f"\nPeríodo aproximado = {periodo:.4f} meses")


# ============================================================
# PARTE (d)
# Primer instante en que ambas poblaciones coinciden
# ============================================================
#
# Buscamos los ceros de:
#
#     presas - predadores
#
# Si esta diferencia cambia de signo entre dos tiempos
# consecutivos, significa que ocurrió un cruce.


diferencia = presas - predadores


# Buscamos dónde cambia de signo

indices_cruce = np.where(
    diferencia[:-1] * diferencia[1:] < 0
)[0]


# Primer cruce

k = indices_cruce[0]


# ============================================================
# 5. Interpolación lineal del instante del cruce
# ============================================================
#
# El cruce ocurre entre:
#
#     t[k]
#
# y
#
#     t[k+1]
#
# Como generalmente no ocurre exactamente en un nodo,
# interpolamos linealmente la función:
#
#     d(t) = presas(t) - predadores(t)
#
# buscando d(t_cruce) = 0.


t_cruce = (
    t[k]
    -
    diferencia[k]
    * (t[k+1] - t[k])
    / (diferencia[k+1] - diferencia[k])
)


# ============================================================
# 6. Interpolación de las poblaciones en el cruce
# ============================================================

alpha = (
    (t_cruce - t[k])
    /
    (t[k+1] - t[k])
)


x_cruce = (
    x[k, :]
    +
    alpha * (x[k+1, :] - x[k, :])
)


presa_cruce = x_cruce[0]
predador_cruce = x_cruce[1]


# ============================================================
# 7. Tasas de crecimiento instantáneas
# ============================================================
#
# Evaluamos directamente el lado derecho del sistema:
#
#     x'(t) = f(t,x)
#
# en el instante del cruce.

tasas = f(
    t_cruce,
    x_cruce
)


tasa_presas = tasas[0]
tasa_predadores = tasas[1]


print("\n(d) " + "=" * 65)

print(
    f"Primer instante en que coinciden: "
    f"t = {t_cruce:.6f} meses"
)

print(
    f"Población de presas = "
    f"{presa_cruce:.6f}"
)

print(
    f"Población de predadores = "
    f"{predador_cruce:.6f}"
)

print()

print(
    f"Tasa instantánea de las presas: "
    f"{tasa_presas:.6f}"
)

print(
    f"Tasa instantánea de los predadores: "
    f"{tasa_predadores:.6f}"
)


# ============================================================
# 8. Interpretación del signo de las tasas
# ============================================================

if tasa_presas > 0:
    print("Las presas están creciendo.")
else:
    print("Las presas están decreciendo.")


if tasa_predadores > 0:
    print("Los predadores están creciendo.")
else:
    print("Los predadores están decreciendo.")