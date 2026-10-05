import numpy as np
from pathlib import Path

from metodos import trapcomp

# ============================================================
# 1. Lectura de los datos
# ============================================================

# Carpeta donde se encuentra este script
carpeta_actual = Path(__file__).resolve().parent

# Archivo de datos
archivo = carpeta_actual.parent / "datos" / "datos_temperatura.txt"

datos = np.loadtxt(archivo)


# ============================================================
# 2. Datos físicos del problema
# ============================================================
L = 1; A = 0.01; c = 1; rho = 1

# ============================================================
# 3. Separación de los datos
# ============================================================
# Primera columna: tiempo
tiempo = datos[:, 0]

# Columnas restantes:
# temperatura en los 41 puntos espaciales
Matriz_T = datos[:, 1:]


# Posiciones espaciales de las mediciones
x = np.linspace(0, L, Matriz_T.shape[1])


# ============================================================
# PARTE (a)
# Energía total en t = 1 s
# ============================================================
t1 = 1

# Buscar la posición correspondiente a t = 1 s
kt1 = np.argmin(np.abs(tiempo - t1))

# Distribución de temperatura en t = 1 s
T_t1 = Matriz_T[kt1, :]

# Integral espacial de la temperatura
integral_T = trapcomp(x, T_t1)

# Energía total
E_total_t1 = rho * c * A * integral_T


print("\n(a) " + "=" * 65)

print(f"Energía total del dispositivo en t = 1 s: {E_total_t1:.8f} J")


# ============================================================
# PARTE (b)
# Energía total para todos los instantes
# ============================================================

# Vector donde se almacenará la energía correspondiente
# a cada instante de tiempo
E_total = np.zeros(len(tiempo))


for k in range(len(tiempo)):
    # Temperatura en todos los puntos espaciales
    # para el instante k
    T_k = Matriz_T[k, :]

    # Energía total en ese instante
    E_total[k] = rho* c* A* trapcomp(x, T_k)


# ============================================================
# 4. Máximo y mínimo de la energía
# ============================================================

# Posición donde ocurre la energía máxima
k_max = np.argmax(E_total)

# Posición donde ocurre la energía mínima
k_min = np.argmin(E_total)


# Valores de energía
E_max = E_total[k_max]
E_min = E_total[k_min]


# Instantes correspondientes
t_max = tiempo[k_max]
t_min = tiempo[k_min]


# ============================================================
# 5. Resultados
# ============================================================
print("\n(b) " + "=" * 65)

print(f"Energía máxima alcanzada: {E_max:.8f} J en t = {t_max:.3f} s")

print(f"Energía mínima alcanzada: {E_min:.8f} J en t = {t_min:.3f} s")