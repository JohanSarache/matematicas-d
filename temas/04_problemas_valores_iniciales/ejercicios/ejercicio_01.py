import numpy as np
import pandas as pd

from metodos import euler1

# ============================================================
# Ejercicio 1 - Problemas a valores iniciales
#     y' = -y
#     y(0) = 1
#     0 <= t <= 1
# ============================================================

def f(t, y):
    return -y

y0 = 1.0

# ============================================================
# PARTE (a)-- Obtener y(1) con precisión de 4 dígitos decimales.
# Se comienza con L = 10 y se duplica L.
# ============================================================

print("\n" + "=" * 60)
print("PARTE (a)")
print("=" * 60)

L = 10

# Para 4 cifras decimales usamos como criterio
# una diferencia menor que 0.5 * 10^(-4)
tolerancia = 0.5e-4

datos_a = []

# Primera aproximación
t, y = euler1(f, [0, 1], y0, L)

y_anterior = y[-1]

datos_a.append(
    {
        "L": L,
        "h": 1 / L,
        "y(1)": y_anterior,
        "Diferencia": np.nan
    }
)

duplicaciones = 0

while True:
    # Duplicamos el número de pasos
    L = 2 * L

    duplicaciones += 1

    # Aplicamos nuevamente Euler
    t, y = euler1(f, [0, 1], y0, L)

    y_actual = y[-1]

    # Diferencia entre dos aproximaciones consecutivas
    diferencia = abs(y_actual - y_anterior)

    datos_a.append(
        {
            "L": L,
            "h": 1 / L,
            "y(1)": y_actual,
            "Diferencia": diferencia
        }
    )

    # Verificamos si se alcanzó la precisión requerida
    if diferencia < tolerancia:
        break

    y_anterior = y_actual


tabla_a = pd.DataFrame(datos_a)

print(tabla_a)

print("\nResultado:")
print(f"L = {L}")
print(f"Número de duplicaciones = {duplicaciones}")
print(f"y(1) ≈ {y_actual:.8f}")
print(f"Diferencia entre las últimas aproximaciones = {diferencia:.8e}")


# ============================================================
# PARTE (b)
# Calcular y(t) para t = 0.687 con 3 decimales exactos.
# ============================================================

print("\n" + "=" * 60)
print("PARTE (b)")
print("=" * 60)

TF = 0.687

L = 10

# Para tres decimales
tolerancia = 0.5e-3

t, y = euler1(f, [0, TF], y0, L)

y_anterior = y[-1]

while True:
    L = 2 * L

    t, y = euler1(f, [0, TF], y0, L)

    y_actual = y[-1]

    diferencia = abs(y_actual - y_anterior)

    if diferencia < tolerancia:
        break

    y_anterior = y_actual


print(f"L = {L}")
print(f"y(0.687) ≈ {y_actual:.8f}")
print(f"y(0.687) con 3 decimales ≈ {y_actual:.3f}")


# ============================================================
# PARTE (c)
# Tabla del error global
# Solución exacta: y(t) = exp(-t)
# E_L = max |y(t_i) - Y_i|
# ============================================================

print("\n" + "=" * 60)
print("PARTE (c)")
print("=" * 60)

def solucion_exacta(t):
    return np.exp(-t)

valores_L = [10,20,40,80,160,320,640,1280]

datos_c = []

error_anterior = None

for L in valores_L:
    # Aplicamos Euler
    t, y_num = euler1(f, [0, 1], y0, L)

    # Paso
    h = 1 / L

    # Solución exacta evaluada en los mismos nodos
    y_exacta = solucion_exacta(t)

    # Error en cada nodo
    errores = np.abs(y_exacta - y_num)

    # Error global
    E_L = np.max(errores)

    # Cociente E_{L/2} / E_L
    if error_anterior is None:
        cociente = np.nan
    else:
        cociente = error_anterior / E_L

    datos_c.append(
        {
            "L": L,
            "h": h,
            "E_L": E_L,
            "E_(L/2)/E_L": cociente
        }
    )

    error_anterior = E_L


tabla_c = pd.DataFrame(datos_c)

print(tabla_c)