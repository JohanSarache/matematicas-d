# ============================================================
# EJERCICIO 14 - Masa de producto perdida en una corriente
# de desecho
#
# La masa de producto perdida está dada por:
#
#              t2
#     m = integral Q(t) * c(t) dt
#              t1
#
# El caudal volumétrico se considera constante:
#
#     Q = 30 m³/h
#
# La concentración está expresada en ppm y:
#
#     1 ppm = 1 g/m³
#
# Por lo tanto:
#
#     Q * c  -> (m³/h) * (g/m³) = g/h
#
# y al integrar respecto del tiempo:
#
#     m -> g
#
# Finalmente se divide entre 1000 para expresar la masa en kg.
#
# El archivo datos_muestreo.txt contiene:
#
#     columna 0: tiempo [h]
#     columna 1: concentración en operación normal [ppm]
#     columna 2: concentración durante una falla [ppm]
#
# Se utilizará como referencia el cálculo realizado con todas
# las mediciones disponibles, es decir, una medición cada hora.
#
# La integral se aproxima mediante la regla compuesta del
# trapecio definida en metodos.py.
# ============================================================


import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from metodos import trapcomp


# ============================================================
# 1. Lectura de los datos
# ============================================================

# Carpeta donde se encuentra este script
carpeta_actual = Path(__file__).resolve().parent

# Archivo de datos
archivo = carpeta_actual.parent / "datos" / "datos_muestreo.txt"

# La primera línea del archivo comienza con %, por lo que
# indicamos que % representa una línea de comentario.
datos = np.loadtxt(archivo, comments="%")


# ============================================================
# 2. Separación de las columnas
# ============================================================

tiempo = datos[:, 0]

# Concentración en condiciones normales
c_normal = datos[:, 1]

# Concentración durante una falla
c_falla = datos[:, 2]


# ============================================================
# 3. Datos del problema
# ============================================================

Q = 30            # [m³/h]
precision = 0.1   # [kg]


# ============================================================
# 4. Función para calcular la masa
# ============================================================

def calcular_masa(t, c):

    # Integral de la concentración respecto del tiempo:
    #
    #     integral c(t) dt
    #
    # unidades:
    #
    #     (g/m³) * h

    integral_c = trapcomp(t, c)

    # Multiplicando por Q:
    #
    #     (m³/h) * (g/m³) * h = g

    masa_g = Q * integral_c

    # Conversión de gramos a kilogramos

    masa_kg = masa_g / 1000

    return masa_kg


# ============================================================
# PARTE (a)
# Condiciones normales de operación
# ============================================================

# ------------------------------------------------------------
# 5. Masa de referencia: mediciones cada 1 hora
# ------------------------------------------------------------

m_ref_normal = calcular_masa(tiempo,c_normal)


# ------------------------------------------------------------
# 6. Mediciones cada 2 horas
# ------------------------------------------------------------
#
# [::2] toma un dato cada dos posiciones:
#
#     0, 2, 4, 6, ..., 24

tiempo_2h = tiempo[::2]
c_normal_2h = c_normal[::2]

m_normal_2h = calcular_masa(tiempo_2h, c_normal_2h)

error_2h = np.abs(m_normal_2h - m_ref_normal)


# ------------------------------------------------------------
# 7. Mediciones cada 4 horas
# ------------------------------------------------------------
#
# [::4] toma:
#
#     0, 4, 8, 12, ..., 24

tiempo_4h = tiempo[::4]
c_normal_4h = c_normal[::4]

m_normal_4h = calcular_masa(tiempo_4h, c_normal_4h)

error_4h = np.abs(m_normal_4h - m_ref_normal)


# ------------------------------------------------------------
# 8. Resultados de la parte (a)
# ------------------------------------------------------------

print("\n(a) " + "=" * 65)

print(f"Masa de referencia (cada 1 h): {m_ref_normal:.6f} kg")

print()

print(f"Masa usando datos cada 2 h: {m_normal_2h:.6f} kg")

print(f"Error respecto de la referencia: {error_2h:.6f} kg")

if error_2h < precision:
    print("Es posible tomar muestras cada 2 horas.")
else:
    print("NO es posible tomar muestras cada 2 horas.")


print()

print(f"Masa usando datos cada 4 h: {m_normal_4h:.6f} kg")

print(f"Error respecto de la referencia: {error_4h:.6f} kg")

if error_4h < precision:
    print("Es posible tomar muestras cada 4 horas.")
else:
    print("NO es posible tomar muestras cada 4 horas.")


# ============================================================
# PARTE (b)
# Falla en el sistema de separación
# ============================================================

# ------------------------------------------------------------
# 9. Masa de referencia durante la falla
# ------------------------------------------------------------

m_ref_falla = calcular_masa(tiempo, c_falla)


# ------------------------------------------------------------
# 10. Muestreo regular cada 2 horas
# ------------------------------------------------------------

tiempo_falla_2h = tiempo[::2]
c_falla_2h = c_falla[::2]

m_falla_2h = calcular_masa(tiempo_falla_2h, c_falla_2h)

error_falla_2h = np.abs(m_falla_2h - m_ref_falla)


# ------------------------------------------------------------
# 11. Resultados de la parte (b)
# ------------------------------------------------------------

print("\n(b) " + "=" * 65)

print(f"Masa de referencia durante la falla: {m_ref_falla:.6f} kg")

print(f"Masa usando muestras cada 2 h: {m_falla_2h:.6f} kg")

print(f"Error respecto de la referencia: {error_falla_2h:.6f} kg")

if error_falla_2h < precision:
    print("Es posible tomar muestras cada 2 horas.")
else:
    print("NO es posible tomar muestras cada 2 horas.")


# ============================================================
# PARTE (c)
# Selección de 12 puntos de muestreo
# ============================================================
#
# El problema del muestreo uniforme cada 2 horas es que durante
# la falla la concentración cambia rápidamente entre
# aproximadamente t = 2 h y t = 8 h.
#
# Por lo tanto, conviene concentrar más puntos de muestreo
# en esa región y utilizar intervalos más grandes cuando la
# concentración varía lentamente.
#
# Una posible selección de 12 puntos es:
#
#     t = 0, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24 h
#
# Esta selección no es única.


# ------------------------------------------------------------
# 12. Índices de los puntos seleccionados
# ------------------------------------------------------------

indices_12 = np.array([0,2,3,4,5,6,7,8,12,16,20,24])


# Datos correspondientes a esos puntos

tiempo_12 = tiempo[indices_12]
c_falla_12 = c_falla[indices_12]


# ------------------------------------------------------------
# 13. Masa utilizando los 12 puntos
# ------------------------------------------------------------

m_falla_12 = calcular_masa(tiempo_12, c_falla_12)

error_falla_12 = np.abs(m_falla_12 - m_ref_falla)


# ------------------------------------------------------------
# 14. Resultados de la parte (c)
# ------------------------------------------------------------

print("\n(c) " + "=" * 65)

print("Puntos de muestreo seleccionados [h]:")

print(tiempo_12)

print(f"\nMasa utilizando los 12 puntos: {m_falla_12:.6f} kg")

print(f"Error respecto de la referencia: {error_falla_12:.6f} kg")

if error_falla_12 < precision:
    print("La selección de 12 puntos conserva la precisión requerida.")
else:
    print("La selección de 12 puntos NO conserva la precisión requerida.")


# ============================================================
# 15. Gráfico de la situación de falla
# ============================================================

plt.figure(figsize=(10, 6))

# Todos los datos disponibles
plt.plot(tiempo,c_falla,"-o",label="Datos cada 1 h")

# Los 12 puntos seleccionados
plt.plot(tiempo_12, c_falla_12, "s", markersize=8, label="12 puntos seleccionados")

plt.xlabel("Tiempo [h]")
plt.ylabel("Concentración [ppm]")
plt.title("Concentración durante una falla")
plt.grid()
plt.legend()
plt.tight_layout()

plt.show()