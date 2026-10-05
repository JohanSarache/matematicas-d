# ============================================================
# EJERCICIO 7 - Área de superficies de revolución
#
# Para controlar el error, se duplica sucesivamente el número
# de subintervalos y se utiliza la estimación:
#
#      error ≈ |A_2L - A_L| / 15
#
# hasta obtener un error menor que 10⁻³.
# ============================================================

import numpy as np
import pandas as pd

from metodos import *

# ============================================================
# Parámetros generales
# ============================================================
tolerancia = 1e-3

# Para n = 3, la fórmula de Newton-Cotes corresponde
# a la regla de Simpson.
n = 3

# ============================================================
# PARTE (a)
#
# f(x) = 2 + cos(pi*x),     x ∈ [0, 2]
# ============================================================
a = 0
b = 2

# Función
def f1(x):
    return 2 + np.cos(np.pi * x)

# Derivada:
# f'(x) = -pi*sin(pi*x)

def df1(x):
    return -np.pi * np.sin(np.pi * x)


# Integrando correspondiente al área:
#
# g(x) = 2*pi*|f(x)|*sqrt(1 + (f'(x))²)

def g1(x):
    return (2* np.pi* np.abs(f1(x))* np.sqrt(1 + df1(x)**2))


# ============================================================
# Aproximaciones sucesivas para la parte (a)
# ============================================================
# Comenzamos con un solo subintervalo
L = 1

A_anterior = intNCcompuesta(g1, a, b, L, n)

resultados_a = []

while True:
    # Duplicamos el número de subintervalos
    L = 2 * L

    # Nueva aproximación del área
    A_actual = intNCcompuesta(g1, a, b, L, n)

    # Estimación del error de Simpson
    error = np.abs(A_actual - A_anterior) / 15

    # Guardamos los resultados
    resultados_a.append(
        [L, A_actual, error]
    )

    # Verificamos la tolerancia
    if error < tolerancia:
        break

    # La aproximación actual pasa a ser la anterior
    A_anterior = A_actual


# Tabla de resultados

tabla_a = pd.DataFrame(
    resultados_a,
    columns=[
        "L",
        "Área aproximada",
        "Error estimado"
    ]
)


print("\n" + "=" * 60)
print("PARTE (a)")
print("=" * 60)

print(tabla_a)

print(
    f"\nÁrea de la superficie = {A_actual:.8f}"
)

print(
    f"Error estimado = {error:.3e}"
)

print(
    f"Número de subintervalos L = {L}"
)


# ============================================================
# PARTE (b)
#
# f(x) = x(x - 1)(x - 2) + 2,     x ∈ [0, 3]
# ============================================================
a = 0
b = 3

# Función

def f2(x):
    return x * (x - 1) * (x - 2) + 2


# Podemos desarrollar:
#
# f(x) = x³ - 3x² + 2x + 2
#
# Por lo tanto:
#
# f'(x) = 3x² - 6x + 2

def df2(x):
    return 3*x**2 - 6*x + 2


# Integrando correspondiente al área

def g2(x):
    return (2* np.pi* np.abs(f2(x))* np.sqrt(1 + df2(x)**2))


# ============================================================
# Aproximaciones sucesivas para la parte (b)
# ============================================================

L = 1

A_anterior = intNCcompuesta(g2, a, b, L, n)

resultados_b = []

while True:
    # Duplicamos el número de subintervalos
    L = 2 * L

    # Nueva aproximación
    A_actual = intNCcompuesta(g2, a, b, L, n)

    # Estimación del error
    error = np.abs(A_actual - A_anterior) / 15

    # Guardamos los resultados
    resultados_b.append(
        [L, A_actual, error]
    )

    # Condición de parada
    if error < tolerancia:
        break

    # Actualizamos la aproximación anterior
    A_anterior = A_actual


# Tabla de resultados

tabla_b = pd.DataFrame(
    resultados_b,
    columns=[
        "L",
        "Área aproximada",
        "Error estimado"
    ]
)


print("\n" + "=" * 60)
print("PARTE (b)")
print("=" * 60)

print(tabla_b)

print(
    f"\nÁrea de la superficie = {A_actual:.8f}"
)

print(
    f"Error estimado = {error:.3e}"
)

print(
    f"Número de subintervalos L = {L}"
)