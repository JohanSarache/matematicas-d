import numpy as np
import pandas as pd

from metodos import trapcomp, simpsoncomp

# ============================================================
# Ejercicio 3 - Integración numérica
#
# Se comparan:
#
#   - Regla del trapecio compuesta
#   - Regla de Simpson compuesta
#
# para distintos valores de:
#
#       h = (b-a)/L
#
# con:
#
#       h = 1/2, 1/4, ..., 1/4096
# ============================================================


# ------------------------------------------------------------
# Funciones del ejercicio
# ------------------------------------------------------------
f1 = lambda x: np.sin(np.pi * x)

f2 = lambda x: 1 / (1 + x**2)


# ------------------------------------------------------------
# Integrales exactas
# ------------------------------------------------------------
I1 = 2 / np.pi

I2 = 2 * np.arctan(5)

# ------------------------------------------------------------
# Valores de h
# 1/2, 1/4, 1/8, ..., 1/4096
# Como:
# 4096 = 2^12
# necesitamos exponentes desde 1 hasta 12.
# ------------------------------------------------------------

valores_h = 1 / 2**np.arange(1, 13)


# ============================================================
# Función para construir la tabla
# ============================================================

def tabla_errores(f, a, b, integral_exacta):
    """
    Construye la tabla de aproximaciones y errores para
    trapecio compuesto y Simpson compuesto.

    Parámetros
    ----------
    f : function
        Función a integrar.

    a, b : float
        Extremos del intervalo.

    integral_exacta : float
        Valor exacto de la integral.

    Retorna
    -------
    DataFrame
        Tabla con h, L, aproximaciones, errores y cocientes.
    """

    datos = []

    # Guardamos los errores de la fila anterior
    error_trap_anterior = None
    error_simp_anterior = None


    for h in valores_h:
        # ----------------------------------------------------
        # Número de subintervalos:
        #       h = (b-a)/L
        # entonces:
        #       L = (b-a)/h
        # ----------------------------------------------------

        L = int(round((b - a) / h))

        # ----------------------------------------------------
        # Nodos de integración
        # L subintervalos -> L+1 puntos
        # ----------------------------------------------------

        x = np.linspace(a,b,L + 1)

        y = f(x)

        # ----------------------------------------------------
        # Trapecio compuesto
        # ----------------------------------------------------

        Q_trap = trapcomp(x,y)


        error_trap = np.abs(
            integral_exacta - Q_trap
        )

        # ----------------------------------------------------
        # Simpson compuesto
        # ----------------------------------------------------
        Q_simp = simpsoncomp(x,y)

        error_simp = np.abs(
            integral_exacta - Q_simp
        )

        # ----------------------------------------------------
        # Cociente entre errores:
        #
        #           E_(L/2)
        #           -------
        #              E_L
        #
        # Como cada fila duplica L, el error anterior
        # corresponde justamente a E_(L/2).
        # ----------------------------------------------------

        if error_trap_anterior is None:
            cociente_trap = np.nan
            cociente_simp = np.nan

        else:
            cociente_trap = (
                error_trap_anterior / error_trap
            )

            cociente_simp = (
                error_simp_anterior / error_simp
            )


        # ----------------------------------------------------
        # Guardamos la fila
        # ----------------------------------------------------

        datos.append(
            {
                "h": h,
                "L": L,

                "Q_trap": Q_trap,
                "E_trap": error_trap,
                "E_(L/2)/E_L trap": cociente_trap,

                "Q_simp": Q_simp,
                "E_simp": error_simp,
                "E_(L/2)/E_L simp": cociente_simp
            }
        )


        # Los errores actuales serán los anteriores
        # en la siguiente iteración

        error_trap_anterior = error_trap
        error_simp_anterior = error_simp


    return pd.DataFrame(datos)


# ============================================================
# Primera función
#
# f1(x) = sin(pi*x), [0,5]
# ============================================================

tabla_f1 = tabla_errores(
    f1,
    0,
    5,
    I1
)


print("\n" + "=" * 100)
print("f(x) = sin(pi*x),   [a,b] = [0,5]")
print("=" * 100)


print(
    tabla_f1
)


# ============================================================
# Segunda función
# f2(x) = 1/(1+x²), [-5,5]
# ============================================================

tabla_f2 = tabla_errores(f2,-5,5,I2)


print("\n" + "=" * 100)
print("f(x) = 1/(1+x²),   [a,b] = [-5,5]")
print("=" * 100)

print(
    tabla_f2
)


# ============================================================
# Órdenes esperados
# ============================================================

print("\n" + "=" * 70)
print("ORDEN DE CONVERGENCIA")
print("=" * 70)


print(
    """
Para el trapecio compuesto se espera:

    E_L = O(h^2)

Por lo tanto, al dividir h por 2:

    E(h) / E(h/2) ≈ 2^2 = 4


Para Simpson compuesto se espera:

    E_L = O(h^4)

Por lo tanto:

    E(h) / E(h/2) ≈ 2^4 = 16
"""
)