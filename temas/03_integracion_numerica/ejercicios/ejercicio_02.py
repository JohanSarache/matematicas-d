import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from metodos import integralNC


# ============================================================
# Ejercicio 2 - Integración numérica
#
# Se estudian las fórmulas de Newton-Cotes de n puntos
# para:
#
#   f1(x) = sin(pi*x)       en [0, 5]
#
#   f2(x) = 1/(1+x^2)       en [-5, 5]
#
# para n = 2, 3, ..., 13.
# ============================================================

f1 = lambda x: np.sin(np.pi * x)

f2 = lambda x: 1 / (1 + x**2)


# ------------------------------------------------------------
# Intervalos
# ------------------------------------------------------------
a1 = 0
b1 = 5

a2 = -5
b2 = 5

# ------------------------------------------------------------
# Integrales exactas
# ------------------------------------------------------------
I1 = 2 / np.pi

I2 = 2 * np.arctan(5)


print("\nIntegrales exactas:")

print(f"I1 = {I1:.10f}")
print(f"I2 = {I2:.10f}")

# ------------------------------------------------------------
# Valores de n indicados en la tabla
# ------------------------------------------------------------
valores_n = range(2, 14)

# ============================================================
# PARTE (a)
# Calcular: E_n = | I - Q_n |
# para n = 2, ..., 13.
# ============================================================

errores_1 = []
errores_2 = []

aproximaciones_1 = []
aproximaciones_2 = []


for n in valores_n:
    # Fórmula de Newton-Cotes para f1
    Q1 = integralNC(f1,a1,b1,n)

    # Fórmula de Newton-Cotes para f2
    Q2 = integralNC(f2,a2,b2,n)

    # --------------------------------------------------------
    # Error absoluto
    # --------------------------------------------------------
    E1 = np.abs(I1 - Q1)
    E2 = np.abs(I2 - Q2)

    # Guardamos los resultados
    aproximaciones_1.append(Q1)
    aproximaciones_2.append(Q2)

    errores_1.append(E1)
    errores_2.append(E2)


# ============================================================
# Tabla con Pandas
# ============================================================

tabla = pd.DataFrame(
    {
        "n": list(valores_n),
        "Q_n f1": aproximaciones_1,
        "Error f1": errores_1,
        "Q_n f2": aproximaciones_2,
        "Error f2": errores_2
    }
)


print("\n" + "=" * 75)
print("PARTE (a)")
print("=" * 75)

print("\nErrores de las fórmulas de Newton-Cotes:\n")

print(tabla)

# ============================================================
# Carpeta para guardar las figuras
# ============================================================

carpeta_capitulo = Path(__file__).resolve().parents[1]

carpeta_figuras = carpeta_capitulo / "figuras"

carpeta_figuras.mkdir(exist_ok=True)


# ============================================================
# PARTE (b)
#
# Graficar f y su polinomio interpolante en n puntos
# equidistantes para n = 2, ..., 13.
# ============================================================


def graficar_interpolantes(
    f,
    a,
    b,
    valores_n,
    titulo,
    nombre_archivo
):
    """
    Grafica la función f y los polinomios interpolantes
    construidos con n puntos equidistantes del intervalo [a,b].
    """

    # Puntos finos para representar la función
    x_grafico = np.linspace(a,b,1000)

    y_grafico = f(x_grafico)


    # --------------------------------------------------------
    # Creamos una figura de 3 filas x 4 columnas.
    # Tenemos 12 valores:
    # n = 2, 3, ..., 13
    # --------------------------------------------------------

    fig, axes = plt.subplots(3,4,figsize=(16, 11))

    # Convertimos la matriz de ejes en un vector
    axes = axes.flatten()


    for ax, n in zip(axes, valores_n):
        # ----------------------------------------------------
        # n nodos equidistantes
        # ----------------------------------------------------
        x_nodos = np.linspace(a,b,n)

        y_nodos = f(x_nodos)

        # ----------------------------------------------------
        # Polinomio interpolante de grado n-1
        #
        # Con n nodos se construye un polinomio de
        # grado máximo n-1.
        # ----------------------------------------------------

        coeficientes = np.polyfit(x_nodos,y_nodos,n - 1)

        # Evaluamos el polinomio
        y_interpolada = np.polyval(coeficientes,x_grafico)

        # ----------------------------------------------------
        # Gráfico
        # ----------------------------------------------------
        ax.plot(x_grafico,y_grafico,label="f(x)")

        ax.plot(x_grafico,y_interpolada,"--",label="Interpolante")

        ax.plot(x_nodos,y_nodos,"o",markersize=3)

        ax.set_title(
            f"n = {n}"
        )

        ax.grid()

        ax.legend(
            fontsize=7
        )


    # Título general
    fig.suptitle(
        titulo,
        fontsize=14
    )


    plt.tight_layout(
        rect=[0, 0, 1, 0.96]
    )


    # Guardamos la figura
    ruta_figura = carpeta_figuras / nombre_archivo

    plt.savefig(
        ruta_figura,
        dpi=300
    )

    plt.close()


    print(
        "\nFigura guardada en:\n",
        ruta_figura
    )


# ============================================================
# Gráfico para f1
# ============================================================

print("\n" + "=" * 75)
print("PARTE (b)")
print("=" * 75)


graficar_interpolantes(
    f1,
    a1,
    b1,
    range(2, 14),
    r"$f(x)=\sin(\pi x)$ y sus polinomios interpolantes",
    "ejercicio_02_b_interpolantes_f1.png"
)


# ============================================================
# Gráfico para f2
# ============================================================

graficar_interpolantes(
    f2,
    a2,
    b2,
    range(2, 14),
    r"$f(x)=1/(1+x^2)$ y sus polinomios interpolantes",
    "ejercicio_02_b_interpolantes_f2.png"
)


# ============================================================
# PARTE (c)
# ============================================================

print("\n" + "=" * 75)
print("PARTE (c)")
print("=" * 75)


print(
    """
Los resultados muestran que aumentar el número de puntos
de una fórmula de Newton-Cotes cerrada no garantiza que
la aproximación converja hacia la integral exacta.

El problema está relacionado con la interpolación mediante
polinomios de grado cada vez mayor en nodos equidistantes.

Para algunas funciones pueden aparecer oscilaciones importantes,
especialmente cerca de los extremos del intervalo.

Por lo tanto, en general no es cierto que:

    lim Q_n(f,a,b) = integral_a^b f(x) dx

para cualquier función f.
"""
)