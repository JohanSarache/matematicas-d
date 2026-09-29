import numpy as np
import matplotlib.pyplot as plt

# ── Funciones ────────────────────────────────────────────────────────────────────
def intNCcompuesta(f, a, b, L, n):
    z = np.linspace(a, b, L + 1)
    h = (b - a) / L
    w = pesosNC(n)
    Q = 0
    for i in range(L):
        x = np.linspace(z[i], z[i+1], n)
        y = f(x)  
        Q += h * np.sum(y * w)
    return Q

def pesosNC(n):
    # Calcula los pesos de la fórmula de Newton-Cotes de n puntos
    x = np.linspace(0, 1, n)
    A = np.ones((n, n))
    for i in range(1, n):
        A[i, :] = A[i-1, :] * x
    b = 1 / np.arange(1, n+1)
    w = np.linalg.solve(A, b)
    return w

def simpsoncomp(x,y):
    L=len(x)-1
    if L%2:
        raise ValueError("Atencion: Tiene que dar una cantidad impar de datos.")
        Q=np.nan
        return Q
    h = (x[-1]-x[0])/(L/2)
    Q = h/6 * (y[0] + 4*sum(y[1:-1:2]) + 2*sum(y[2:-2:2]) + y[-1])
    return Q

def trapcomp(x,y):
    L=len(x)-1
    deltax=np.diff(x)
    Q=0
    for i in range(0,L):
        Q+=0.5*deltax[i]*(y[i]+y[i+1])
    return Q


# ── Datos ────────────────────────────────────────────────────────────────────
alpha = 6e5
beta  = -3.3e3

def modelo(T_val):
    return alpha * np.exp(beta / T_val)

T = np.array([280, 300, 320, 340, 360, 380, 400], dtype=float)
P = np.array([4.6, 10, 19.9, 36.6, 62.7, 101.5, 156.8], dtype=float)
# P = modelo(T)

# ── Inciso (a): interpolación a trozos  ──────────────────────────

L = len(T)-1

# -- Lineal a trozos: 6 trozos, índices consecutivos --
L = len(T) - 1
err_lineal = np.array([])
for i in range(L):
    coefs = np.polyfit(T[i:i+2], P[i:i+2], deg=1)
    T_eval = np.linspace(T[i], T[i+1], 100)
    err = abs(np.polyval(coefs, T_eval) - modelo(T_eval)) / modelo(T_eval) * 100
    err_lineal = np.append(err_lineal, err)

# -- Cúbica a trozos: 2 trozos con nodo compartido en T = 340 --
trozos_cub = [(0, 4), (3, 7)]   # índices de inicio y fin en T
err_cub = np.array([])
for i0, i1 in trozos_cub:
    coefs = np.polyfit(T[i0:i1], P[i0:i1], deg=3)
    T_eval = np.linspace(T[i0], T[i1-1], 100)
    err = abs(np.polyval(coefs, T_eval) - modelo(T_eval)) / modelo(T_eval) * 100
    err_cub = np.append(err_cub, err)

max_err_lineal = np.max(err_lineal)
max_err_cub    = np.max(err_cub)
print("=" * 55)
print("Inciso (a): interpolación a trozos")
print(f"  Max error rel. lineal a trozos = {max_err_lineal:.4f}%")
print(f"  Max error rel. cúbica a trozos = {max_err_cub:.4f}%")
print()
print("  Comentario: la interpolación cúbica es notablemente más preciso (~0.75%)")
print("  que la interpolación lineal (~6.68%) usando exactamente los mismos nodos,")
print("  esto se condice con el hecho que las derivadas del modelo son pequeñas")
print("  en el [4.6,157]")
print("=" * 55)


# Verificación visual
T_plot = np.linspace(280, 400, 500)

# Modelo exacto
P_modelo = modelo(T_plot)

# Lineal a trozos
P_lin_plot = np.zeros_like(T_plot)
for i in range(L):
    coefs = np.polyfit(T[i:i+2], P[i:i+2], deg=1)
    mask = (T_plot >= T[i]) & (T_plot <= T[i+1])
    P_lin_plot[mask] = np.polyval(coefs, T_plot[mask])

# Cúbica a trozos
P_cub_plot = np.zeros_like(T_plot)
for i0, i1 in trozos_cub:
    coefs = np.polyfit(T[i0:i1], P[i0:i1], deg=3)
    mask = (T_plot >= T[i0]) & (T_plot <= T[i1-1])
    P_cub_plot[mask] = np.polyval(coefs, T_plot[mask])

plt.figure(figsize=(8, 4.5))
plt.plot(T_plot, P_modelo,   label="Modelo exacto",     color="steelblue", linewidth=1.5)
plt.plot(T_plot, P_lin_plot, label="Lineal a trozos",   color="tomato",    linestyle="--")
plt.plot(T_plot, P_cub_plot, label="Cúbica a trozos",   color="seagreen",  linestyle="-.")
plt.scatter(T, P, color="black", zorder=5, label="Datos experimentales")
plt.xlabel("Temperatura T (K)")
plt.ylabel("Presión de vapor P (kPa)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()

# ── Inciso (b): cuadratura compuesta ─────────────────────────────────────────

# Trapecio compuesto con los 7 nodos de la tabla
I_trap = trapcomp(T, P)

# Simpson 1/3 compuesto con los 7 nodos de la tabla
# 7 datos -> 6 subintervalos (par) -> OK para Simpson 1/3
I_simp = simpsoncomp(T, P)

print("\n" + "=" * 55)
print("Inciso (b): cuadratura compuesta")
print(f"  Trapecio compuesto (6 subint.):     I = {I_trap:.4f} kPa·K")
print(f"  Simpson compuesto (3 subint.):  I = {I_simp:.4f} kPa·K")


# ── Inciso (c): valor de referencia y errores ─────────────────────────────────
#
# Se usa intNCcompuesta con orden 4 y L = 100 subintervalos.
# Con tantos subintervalos el error de la referencia es despreciable
# frente al error de las reglas con solo 6 o 3 subintervalos.

I_ref = intNCcompuesta(modelo, 280, 400, 100, 4)

err_trap = abs(I_trap - I_ref) / I_ref * 100
err_simp = abs(I_simp - I_ref) / I_ref * 100

print("\n" + "=" * 55)
print("Inciso (c): valor de referencia y errores relativos")
print(f"  I referencia (L=100, orden 4)   = {I_ref:.6f} kPa·K")
print(f"  Error rel. trapecio compuesto   = {err_trap:.7f}%")
print(f"  Error rel. Simpson compuesto    = {err_simp:.7f}%")
print()
print("  Comentario: Simpson compuesto es notablemente más preciso (~0.003%)")
print("  que el trapecio (~1.66%) usando exactamente los mismos nodos,")
print("  lo que ilustra la ganancia de emplear una fórmula de mayor orden.")
print("=" * 55)
