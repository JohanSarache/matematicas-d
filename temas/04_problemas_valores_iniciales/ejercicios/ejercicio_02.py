import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from metodos import euler1

# ============================================================
# Ejercicio 2 - Problemas a valores iniciales
#     y' = -cos(2*pi*t^2) - t*y
#     y(0) = 2
#     0 <= t <= 4
# ============================================================

def f(t, y):
    return -np.cos(2 * np.pi * t**2) - t * y

inter = [0, 4]
y0 = 2.0

# ------------------------------------------------------------
# Carpeta donde se guardarán las figuras
# ------------------------------------------------------------

carpeta_capitulo = Path(__file__).resolve().parents[1]
carpeta_figuras = carpeta_capitulo / "figuras"

carpeta_figuras.mkdir(exist_ok=True)

# ============================================================
# PARTE (a)--Resolver mediante Euler para diferentes valores de L.
# Graficar las aproximaciones.
# ============================================================

print("\n" + "=" * 70)
print("PARTE (a)")
print("=" * 70)

valores_L = [10,20,40,80,160,320,640,1280]

# Aquí guardaremos las soluciones
soluciones = {}

# Aquí guardaremos información para una tabla
datos_convergencia = []

y_anterior = None

for L in valores_L:
    # Aplicamos Euler
    t, y = euler1(f, inter, y0, L)

    soluciones[L] = (t, y)

    # Tamaño de paso
    h = (inter[1] - inter[0]) / L

    # --------------------------------------------------------
    # Comparamos con la aproximación anterior.
    #
    # Como L se duplica:
    #
    #     L, 2L
    #
    # los puntos de la malla gruesa están también contenidos
    # en la malla más fina.
    #
    # Por eso y[::2] selecciona los puntos que coinciden con
    # la solución anterior.
    # --------------------------------------------------------

    if y_anterior is None:
        diferencia_maxima = np.nan

    else:

        diferencia_maxima = np.max(
            np.abs(y[::2] - y_anterior)
        )


    datos_convergencia.append(
        {
            "L": L,
            "h": h,
            "max |Y_L - Y_(L/2)|": diferencia_maxima
        }
    )


    y_anterior = y


# ------------------------------------------------------------
# Tabla de convergencia
# ------------------------------------------------------------

tabla_convergencia = pd.DataFrame(datos_convergencia)

print("\nComparación entre aproximaciones sucesivas:\n")

print(
    tabla_convergencia
)


# ------------------------------------------------------------
# Gráfico de todas las aproximaciones
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

for L in valores_L:

    t, y = soluciones[L]

    plt.plot(t,y,label=f"L = {L}")


plt.xlabel("t")
plt.ylabel("y(t)")
plt.title("Método de Euler para diferentes valores de L")
plt.grid()
plt.legend()

plt.tight_layout()

plt.savefig(
    carpeta_figuras / "ejercicio_02_a_aproximaciones.png",
    dpi=300
)

plt.close()


print(
    "\nFigura guardada en:\n",
    carpeta_figuras / "ejercicio_02_a_aproximaciones.png"
)


# ------------------------------------------------------------
# Un valor razonable puede elegirse observando cuándo las
# curvas dejan de distinguirse visualmente.
#
# Este valor puede modificarse después de mirar el gráfico.
# ------------------------------------------------------------

L_visual = 320

print(
    f"\nUn valor que puede tomarse como visualmente convergido "
    f"es aproximadamente L = {L_visual}."
)

# ============================================================
# Para las partes (b) y (c) usaremos una malla bastante fina.
# ============================================================

L_fino = 5120

t, y = euler1(f,inter,y0,L_fino)

# ============================================================
# PARTE (b)
# Calcular máximo y mínimo global de la solución.
# ============================================================

print("\n" + "=" * 70)
print("PARTE (b)")
print("=" * 70)

# Índices donde se encuentran máximo y mínimo
indice_max = np.argmax(y)
indice_min = np.argmin(y)


t_max = t[indice_max]
y_max = y[indice_max]

t_min = t[indice_min]
y_min = y[indice_min]


tabla_extremos = pd.DataFrame(
    {
        "Extremo": ["Máximo", "Mínimo"],
        "t": [t_max, t_min],
        "y(t)": [y_max, y_min]
    }
)


print("\nMáximo y mínimo aproximados:\n")

print(
    tabla_extremos
)

# ============================================================
# PARTE (c)
# Encontrar aproximadamente t tal que: y(t) = 1
# Primero localizamos entre qué dos nodos ocurre el cruce.
# Luego usamos interpolación lineal.
# ============================================================

print("\n" + "=" * 70)
print("PARTE (c)")
print("=" * 70)

nivel = 1.0

g = y - nivel

# Buscamos cambios de signo
indices_cruce = np.where(
    g[:-1] * g[1:] <= 0
)[0]

valores_t_cruce = []

for i in indices_cruce:

    t0 = t[i]
    t1 = t[i + 1]

    y0_local = y[i]
    y1_local = y[i + 1]

    # Interpolación lineal
    t_cruce = (
        t0
        + (nivel - y0_local)
        * (t1 - t0)
        / (y1_local - y0_local)
    )


    valores_t_cruce.append(t_cruce)


tabla_cruces = pd.DataFrame(
    {
        "y(t)": [nivel] * len(valores_t_cruce),
        "t aproximado": valores_t_cruce
    }
)


print(
    tabla_cruces
)


# ============================================================
# PARTE (d)
#
# Resolver la misma ecuación diferencial con:
#
#     y(0) = 1
#     y(0) = 0
#     y(0) = -1
#
# y graficar las tres soluciones.
# ============================================================

print("\n" + "=" * 70)
print("PARTE (d)")
print("=" * 70)


condiciones_iniciales = [1.0,0.0,-1.0]

plt.figure(figsize=(10, 6))

datos_finales = []

for condicion_inicial in condiciones_iniciales:

    t_sol, y_sol = euler1(f,inter,condicion_inicial,L_fino)


    plt.plot(t_sol,y_sol,label=f"y(0) = {condicion_inicial:g}")


    datos_finales.append(
        {
            "y(0)": condicion_inicial,
            "y(4)": y_sol[-1]
        }
    )


plt.xlabel("t")
plt.ylabel("y(t)")
plt.title("Soluciones para diferentes condiciones iniciales")
plt.grid()
plt.legend()

plt.tight_layout()

plt.savefig(
    carpeta_figuras / "ejercicio_02_d_condiciones_iniciales.png",
    dpi=300
)

plt.close()


tabla_final = pd.DataFrame(datos_finales)


print("\nValores de las soluciones en t = 4:\n")

print(
    tabla_final
)

print(
    "\nFigura guardada en:\n",
    carpeta_figuras / "ejercicio_02_d_condiciones_iniciales.png"
)

# ============================================================
# Interpretación de la parte (d)
# ============================================================

print("\nInterpretación:")

print(
    """
Las trayectorias correspondientes a diferentes condiciones
iniciales se acercan entre sí a medida que aumenta t.

Para

    f(t,y) = -cos(2*pi*t^2) - t*y

se tiene

    df/dy = -t.

En el intervalo [0,4]:

    df/dy <= 0,

y para t > 0:

    df/dy < 0.

Por lo tanto, diferencias entre soluciones tienden a disminuir
a medida que avanza el tiempo.
"""
)