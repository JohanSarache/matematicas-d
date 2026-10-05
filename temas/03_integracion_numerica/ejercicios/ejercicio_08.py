# ============================================================
# EJERCICIO 8 - Área de una superficie de revolución
#
# Dar el resultado con 12 dígitos exactos.
#
# La integral se aproxima mediante Newton-Cotes compuesta con
# 3 puntos, equivalente a la regla de Simpson.
#
# Para estimar el error se comparan dos aproximaciones
# consecutivas, con L y 2L subintervalos:
#
#      error ≈ |A_2L - A_L| / 15
#
# El factor 15 aparece porque Simpson es de orden 4:
#
#      2⁴ - 1 = 15
# ============================================================

import numpy as np
import pandas as pd

from metodos import *


# ============================================================
# 1. Datos del problema
# ============================================================

a = 0
b = 4

# Newton-Cotes de 3 puntos corresponde a Simpson
n = 3

# Para obtener 12 cifras decimales correctas se exige
# un error menor que 0.5 x 10⁻¹²
tolerancia = 0.5e-12

# ============================================================
# 2. Definición de la función
# ============================================================

def f(x):
    return 1 + x + np.cos(x)

# ============================================================
# 3. Derivada de la función
# ============================================================
# f(x) = 1 + x + cos(x)
#
# f'(x) = 1 - sin(x)

def df(x):
    return 1 - np.sin(x)


# ============================================================
# 4. Integrando del área de revolución
# ============================================================

# El área está dada por:
#
# A = integral de:
#
#     2*pi*f(x)*sqrt(1 + (f'(x))²)

def g(x):
    return (2* np.pi* f(x)* np.sqrt(1 + df(x)**2))


# ============================================================
# 5. Primera aproximación
# ============================================================
# Se comienza con un subintervalo.

L = 1

A_anterior = intNCcompuesta(g, a, b, L, n)

# Lista donde se guardarán las aproximaciones
resultados = []

# ============================================================
# 6. Refinamiento sucesivo de la integración
# ============================================================

while True:
    # Se duplica el número de subintervalos.
    # Esto equivale a dividir el paso h por 2.

    L = 2 * L

    # Nueva aproximación del área

    A_actual = intNCcompuesta(g, a, b, L, n)

    # Estimación del error mediante Richardson:
    #
    # error ≈ |A_2L - A_L| / (2⁴ - 1)

    error = np.abs(A_actual - A_anterior) / 15

    # Se guardan los resultados

    resultados.append(
        [
            L,
            A_actual,
            error
        ]
    )


    # Si el error es menor que la tolerancia,
    # se detiene el proceso.

    if error < tolerancia:
        break


    # La aproximación actual pasa a ser la anterior
    # para la siguiente iteración.

    A_anterior = A_actual


# ============================================================
# 7. Tabla de resultados
# ============================================================

tabla = pd.DataFrame(
    resultados,
    columns=[
        "L",
        "Área aproximada",
        "Error estimado"
    ]
)


print("\n" + "=" * 65)
print("APROXIMACIONES SUCESIVAS")
print("=" * 65)

print(tabla)


# ============================================================
# 8. Resultado final
# ============================================================

print("\n" + "=" * 65)
print("RESULTADO FINAL")
print("=" * 65)

print(
    f"Área de la superficie = {A_actual:.12f}"
)

print(
    f"Error estimado = {error:.3e}"
)

print(
    f"Número de subintervalos L = {L}"
)