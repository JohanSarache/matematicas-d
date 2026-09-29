import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from metodos import euler1

# ============================================================
# Ejercicio 3 - Problemas a valores iniciales
#     y' = y(1-y)(1+y)
#     y(0) = y0
#     0 <= t <= 2
#
# Método de Euler con L = 10000 pasos
# ============================================================

def f(t, y):
    return y * (1 - y) * (1 + y)


# Intervalo temporal
inter = [0, 2]

# Número de pasos indicado por el ejercicio
L = 10000

# ------------------------------------------------------------
# Condiciones iniciales: y0 = -1.4, -1.3, ..., 1.3, 1.4
# ------------------------------------------------------------

valores_y0 = np.round(
    np.arange(-1.4, 1.41, 0.1),
    1
)

# ------------------------------------------------------------
# Carpeta para guardar las figuras
# ------------------------------------------------------------

carpeta_capitulo = Path(__file__).resolve().parents[1]

carpeta_figuras = carpeta_capitulo / "figuras"

carpeta_figuras.mkdir(exist_ok=True)

# ============================================================
# PARTE (a)
# Resolver todos los PVI usando Euler y superponer
# las soluciones en un mismo gráfico.
# ============================================================

print("\n" + "=" * 70)
print("PARTE (a)")
print("=" * 70)


# Diccionario para guardar todas las soluciones
soluciones = {}

# Lista para construir una tabla con pandas
datos = []

for y0 in valores_y0:
    # Resolver el PVI mediante Euler
    t, y = euler1(f,inter,y0,L)

    # Guardamos la solución asociada a cada condición inicial
    soluciones[y0] = (t, y)

    # Guardamos algunos datos para mostrar posteriormente
    datos.append(
        {
            "y(0)": y0,
            "y(2)": y[-1]
        }
    )

# ------------------------------------------------------------
# Tabla con los valores iniciales y finales
# ------------------------------------------------------------

tabla = pd.DataFrame(datos)


print("\nValores aproximados de las soluciones en t = 2:\n")

print(tabla)

# ------------------------------------------------------------
# Gráfico de todas las soluciones
# ------------------------------------------------------------
plt.figure(figsize=(10, 7))

for y0 in valores_y0:

    t, y = soluciones[y0]

    plt.plot(t,y,linewidth=1.2)

# ------------------------------------------------------------
# Soluciones de equilibrio
#
# f(y) = 0
#
# y(1-y)(1+y) = 0
#
# Por lo tanto:
#
# y = -1, 0, 1
# ------------------------------------------------------------

plt.axhline(y=-1,linestyle="--",linewidth=1.2,label="Equilibrios y = -1, 0, 1")

plt.axhline(y=0,linestyle="--",linewidth=1.2)

plt.axhline(y=1,linestyle="--",linewidth=1.2)

plt.xlabel("t")
plt.ylabel("y(t)")

plt.title(
    "Método de Euler para diferentes condiciones iniciales"
)

plt.grid()
plt.legend()
plt.tight_layout()

# Guardar figura
plt.savefig(
    carpeta_figuras / "ejercicio_03_a_soluciones.png",
    dpi=300
)

plt.close()

print(
    "\nFigura guardada en:\n",
    carpeta_figuras / "ejercicio_03_a_soluciones.png"
)

# ============================================================
# PARTE (b)--Estudiar el signo de:
#
#           df
#           --
#           dy
# ============================================================

print("\n" + "=" * 70)
print("PARTE (b)")
print("=" * 70)

# Tenemos:
# f(y) = y(1-y^2)
#
#      = y - y^3
#
# Por lo tanto:
#
# df/dy = 1 - 3y^2


def df_dy(y):
    return 1 - 3 * y**2

# Puntos donde df/dy = 0
# 1 - 3y^2 = 0
# y = +-1/sqrt(3)

y_critico = 1 / np.sqrt(3)

print(f"\n1/sqrt(3) = {y_critico:.8f}")
print("\nSigno de df/dy:")

print(
    f"""
df/dy < 0   si   y < {-y_critico:.6f}

df/dy > 0   si   {-y_critico:.6f} < y < {y_critico:.6f}

df/dy < 0   si   y > {y_critico:.6f}
"""
)


# ============================================================
# Gráfico adicional con las regiones determinadas por df/dy
# ============================================================
plt.figure(figsize=(10, 7))

for y0 in valores_y0:

    t, y = soluciones[y0]

    plt.plot(t,y,linewidth=1.0)


# Equilibrios
plt.axhline(-1,linestyle="--",linewidth=1)
plt.axhline(0,linestyle="--",linewidth=1)
plt.axhline(1,linestyle="--",linewidth=1)

# Límites donde df/dy cambia de signo
plt.axhline(
    -y_critico,
    linestyle=":",
    linewidth=1.5,
    label=r"$y=\pm 1/\sqrt{3}$"
)

plt.axhline(
    y_critico,
    linestyle=":",
    linewidth=1.5
)

plt.xlabel("t")
plt.ylabel("y(t)")

plt.title(
    r"Soluciones y regiones determinadas por $\partial f/\partial y$"
)

plt.grid()
plt.legend()
plt.tight_layout()

plt.savefig(
    carpeta_figuras / "ejercicio_03_b_dfdy.png",
    dpi=300
)

plt.close()


print(
    "\nFigura guardada en:\n",
    carpeta_figuras / "ejercicio_03_b_dfdy.png"
)