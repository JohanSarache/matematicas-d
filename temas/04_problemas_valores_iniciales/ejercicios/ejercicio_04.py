# ============================================================
# EJERCICIO 4 - Problema a valores iniciales
#
# Considere el PVI:
#
#       y' = -y + sin(t) + cos(t)
#
#       y(0) = 0
#
# Se desea determinar y(2).
#
# (a) Aproximar y(2) mediante:
#
#       - Euler
#       - Runge-Kutta de orden 2 (RK2)
#       - Runge-Kutta de orden 4 (RK4)
#
#     utilizando:
#
#       h = 1/10, 1/20, 1/40, 1/80, 1/160, 1/320
#
# (b) Determinar el número de pasos L y el número de
#     evaluaciones de f necesarios para obtener:
#
#       - 3 decimales correctos
#       - 6 decimales correctos
#       - 10 decimales correctos
#
#
# La solución exacta del problema es:
#
#       y(t) = sin(t)
#
# por lo tanto:
#
#       y(2) = sin(2)
#
# Este valor se utilizará para calcular los errores.
# ============================================================


import numpy as np
import pandas as pd

from metodos import *

# ============================================================
# 1. Definición del problema
# ============================================================

def f(t, y):
    return -y + np.sin(t) + np.cos(t)


inter = [0, 2]

# Euler trabaja con y0 escalar
y0_euler = 0.0

# RK2 y RK4, tal como están definidas en metodos.py,
# esperan que y0 sea un arreglo.
y0_rk = np.array([0.0])


# Solución exacta en t = 2
y_exacta = np.sin(2)


print("\n" + "=" * 70)
print("SOLUCIÓN EXACTA")
print("=" * 70)

print(f"y(2) = sin(2) = {y_exacta:.15f}")


# ============================================================
# 2. Pasos indicados en el ejercicio
# ============================================================
h_valores = np.array([1/10, 1/20, 1/40, 1/80, 1/160, 1/320])

# Listas donde se guardarán los resultados
resultados = []

errores_euler = []
errores_rk2 = []
errores_rk4 = []

L_valores = []

# ============================================================
# PARTE (a)
# Aproximaciones de y(2)
# ============================================================

for h in h_valores:
    # --------------------------------------------------------
    # Número de pasos
    # --------------------------------------------------------
    #     L = (TF - t0) / h

    L = int(round( (inter[1] - inter[0]) / h ) )

    L_valores.append(L)

    # --------------------------------------------------------
    # Método de Euler
    # --------------------------------------------------------

    t_euler, y_euler = euler1(f, inter, y0_euler, L )

    # Último valor del vector:
    # corresponde a t = 2
    y2_euler = y_euler[-1]

    # --------------------------------------------------------
    # Método RK2
    # --------------------------------------------------------
    t_rk2, y_rk2 = rk2(f, inter, y0_rk, L)

    # Como y_rk2 es una matriz, tomamos:
    #
    # última fila -> t = 2
    # columna 0   -> única variable y
    y2_rk2 = y_rk2[-1, 0]


    # --------------------------------------------------------
    # Método RK4
    # --------------------------------------------------------
    t_rk4, y_rk4 = rk4(f, inter, y0_rk, L)

    y2_rk4 = y_rk4[-1, 0]

    # --------------------------------------------------------
    # Errores absolutos
    # --------------------------------------------------------

    error_euler = np.abs(y2_euler - y_exacta)

    error_rk2 = np.abs(y2_rk2 - y_exacta)

    error_rk4 = np.abs(y2_rk4 - y_exacta)


    errores_euler.append(error_euler)
    errores_rk2.append(error_rk2)
    errores_rk4.append(error_rk4)


    # Guardamos los resultados
    resultados.append([h, L, y2_euler, y2_rk2, y2_rk4])


# ============================================================
# 3. Tabla de la parte (a)
# ============================================================

tabla = pd.DataFrame(
    resultados,
    columns=[
        "h",
        "L",
        "Euler",
        "RK2",
        "RK4"
    ]
)


print("\n" + "=" * 70)
print("PARTE (a)")
print("=" * 70)

print(tabla)

# ============================================================
# PARTE (b)
# Número de pasos y evaluaciones de f
# ============================================================
# Para considerar d decimales correctos se exige:
#
#     error < 0.5 * 10^(-d)
#
# Los métodos tienen órdenes:
#
#     Euler -> p = 1
#     RK2   -> p = 2
#     RK4   -> p = 4
#
# Cuando h se divide por 2:
#
#     error_nuevo ≈ error_anterior / 2^p
#
# Esto permite estimar refinamientos adicionales sin tener que
# ejecutar una cantidad enorme de pasos, especialmente para
# Euler cuando se requieren 10 decimales.


ordenes = {"Euler": 1, "RK2": 2, "RK4": 4 }


evaluaciones_por_paso = {"Euler": 1, "RK2": 2, "RK4": 4}


errores_metodos = {
    "Euler": np.array(errores_euler),
    "RK2": np.array(errores_rk2),
    "RK4": np.array(errores_rk4)
}


# ============================================================
# 4. Función para determinar L
# ============================================================

def determinar_L(
    errores,
    L_valores,
    orden,
    tolerancia
):

    # Primero revisamos si alguna de las aproximaciones
    # ya calculadas en la parte (a) satisface la tolerancia.

    for L, error in zip(L_valores, errores):

        if error < tolerancia:
            return L, error, False


    # Si ninguna cumple, usamos como punto de partida
    # el último cálculo disponible.

    L = L_valores[-1]
    error = errores[-1]

    # Como cada refinamiento divide h por 2:
    #
    #     L -> 2L
    #
    # y el error disminuye aproximadamente como:
    #
    #     error -> error / 2^p

    while error >= tolerancia:

        L = 2 * L

        error = error / (2**orden)


    return L, error, True


# ============================================================
# 5. Tolerancias requeridas
# ============================================================

decimales = [3, 6, 10]

resultados_b = []

for d in decimales:

    tolerancia = 0.5 * 10**(-d)

    for metodo in ["Euler", "RK2", "RK4"]:

        L, error, estimado = determinar_L(
            errores_metodos[metodo],
            L_valores,
            ordenes[metodo],
            tolerancia
        )


        # Número de evaluaciones de f
        #
        # Euler -> 1 evaluación por paso
        # RK2   -> 2 evaluaciones por paso
        # RK4   -> 4 evaluaciones por paso

        N_eval = evaluaciones_por_paso[metodo] * L


        resultados_b.append([
            d,
            metodo,
            L,
            N_eval,
            error,
            estimado
        ])


# ============================================================
# 6. Tabla final de la parte (b)
# ============================================================

tabla_b = pd.DataFrame(
    resultados_b,
    columns=[
        "Decimales",
        "Método",
        "L",
        "Evaluaciones de f",
        "Error aproximado",
        "L estimado"
    ]
)


print("\n" + "=" * 70)
print("PARTE (b)")
print("=" * 70)

print(tabla_b)