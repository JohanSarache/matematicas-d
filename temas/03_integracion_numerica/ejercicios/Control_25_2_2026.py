import numpy as np
import pandas as pd

from metodos import *


# ============================================================
# Control viejo - Integración numérica
#
# Energía térmica total de una placa circular
#
#     E = ∫∫ u(x,y) dA
#
# donde
#
#     u(x,y) = ln(1 + x² + y² + 0.6xy)
#
# y el dominio es:
#
#     x² + y² <= 1
#
# Como c = rho = 1, no aparecen factores adicionales.
# ============================================================


# ------------------------------------------------------------
# Cambio a coordenadas polares
#
# x = r cos(theta)
# y = r sin(theta)
#
# x² + y² = r²
# xy = r² cos(theta) sin(theta)
#
# dA = r dr dtheta        
# ------------------------------------------------------------


def f(r, theta):

    return (
        np.log(
            1
            + r**2
            + 0.6 * r**2 * np.cos(theta) * np.sin(theta)
        )* r
    )

# ============================================================
# Primera aproximación
# ============================================================

# Número de subintervalos en r
L_r = 100

# Número de subintervalos en theta
L_theta = 100


# IMPORTANTE:
# L_r subintervalos necesitan L_r + 1 nodos.
#
# Por eso usamos 101 puntos si L_r = 100.
ri = np.linspace(0, 1, L_r + 1)

# Aquí guardaremos:
# Q(r_k) = integral de f(r_k, theta) respecto de theta
Q = []


# ============================================================
# Integración respecto de theta
# ============================================================

for rk in ri:
    # Para cada valor fijo de r definimos una función
    # que depende solamente de theta.
    def ftheta(theta):
        return f(rk, theta)

    # Integramos respecto de theta:
    # Q(r_k) = integral_0^(2*pi) f(r_k, theta) dtheta

    Qk = intNCcompuesta(ftheta,0,2 * np.pi,L_theta,1)

    # Guardamos el resultado correspondiente a r_k
    Q.append(Qk)

# Convertimos la lista en un array de NumPy
Q = np.array(Q)

# ============================================================
# Integración respecto de r
# ============================================================

# Tamaño de paso radial
h_r = 1 / L_r

# ------------------------------------------------------------
# Método 1:
# suma rectangular por izquierda
#
# Se excluye Q[-1] porque tenemos L_r + 1 nodos
# pero solamente L_r rectángulos.
# ------------------------------------------------------------

E_rectangulos = h_r * np.sum(Q[:-1])

# ------------------------------------------------------------
# Método 2:
# trapecio compuesto
# ------------------------------------------------------------

E_trapecio = trapcomp(ri, Q)

# ============================================================
# Resultados
# ============================================================

resultados = pd.DataFrame(
    {
        "Método exterior": [
            "Rectángulos por izquierda",
            "Trapecio compuesto"
        ],
        "E": [
            E_rectangulos,
            E_trapecio
        ]
    }
)


print("\nAproximación de la energía térmica:\n")

print(resultados)

# ============================================================
# Estudio de convergencia
#
# Aumentamos la cantidad de subintervalos radiales para
# determinar las cifras estables de la integral.
# ============================================================

print("\n" + "=" * 60)
print("ESTUDIO DE CONVERGENCIA")
print("=" * 60)

valores_L = [100,200,400,800,1600,3200,6400]

datos_convergencia = []

for L_r in valores_L:
    # Nodos radiales
    ri = np.linspace(0,1,L_r + 1)

    Q = []

    # --------------------------------------------------------
    # Para cada r integramos primero respecto de theta
    # --------------------------------------------------------

    for rk in ri:
        def ftheta(theta):
            return f(rk, theta)

        Qk = intNCcompuesta(ftheta,0,2*np.pi,L_theta,1)

        Q.append(Qk)

    Q = np.array(Q)

    # --------------------------------------------------------
    # Integral exterior usando trapecio
    # --------------------------------------------------------

    E = trapcomp(ri,Q)

    datos_convergencia.append(
        {
            "L_r": L_r,
            "E": E
        }
    )

# ============================================================
# Tabla
# ============================================================

tabla_convergencia = pd.DataFrame(
    datos_convergencia
)

print(
    tabla_convergencia
)