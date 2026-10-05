import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from metodos import *

# ============================================================
# 1. Lectura de los datos
# ============================================================

# Carpeta donde se encuentra este script
carpeta_actual = Path(__file__).resolve().parent

# Archivo de datos
archivo = carpeta_actual.parent / "datos" / "Energias_renovables.txt"

datos = np.loadtxt(archivo)


# ============================================================
# 2. Separación de las columnas
# ============================================================

tiempo = datos[:, 0]

eolica = datos[:, 1]
fotovoltaica = datos[:, 2]
bioenergias = datos[:, 3]
hidraulica = datos[:, 4]

porcentaje_demanda = datos[:, 5]


# ============================================================
# 3. Potencia renovable total
# ============================================================

P_renovable = (eolica + fotovoltaica + bioenergias + hidraulica)


# ============================================================
# 4. Potencia total demandada
# ============================================================

# El archivo proporciona el porcentaje de la demanda cubierta
# por las fuentes renovables:
#
# porcentaje_demanda = 100 * P_renovable / P_demanda
#
# Por lo tanto:
#
# P_demanda = 100 * P_renovable / porcentaje_demanda

P_demanda = 100 * P_renovable / porcentaje_demanda


# ============================================================
# PARTE (a)
# Evolución de la generación renovable y de la demanda
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(tiempo, P_renovable, label="Potencia renovable")

plt.plot(tiempo, P_demanda, label="Demanda")

plt.xlabel("Tiempo [h]")
plt.ylabel("Potencia [MW]")
plt.title("Potencia renovable y demanda eléctrica")
plt.grid()
plt.legend()
plt.tight_layout()

plt.show()


# ============================================================
# 5. Horarios característicos
# ============================================================

# Índice correspondiente a la demanda máxima
i_dem_max = np.argmax(P_demanda)

# Índice correspondiente a la demanda mínima
i_dem_min = np.argmin(P_demanda)

# Índice correspondiente a la máxima generación renovable
i_ren_max = np.argmax(P_renovable)


print("\n" + "=" * 60)
print("PARTE (a)")
print("=" * 60)

print(
    f"Demanda máxima: {P_demanda[i_dem_max]:.2f} MW "
    f"a las {tiempo[i_dem_max]:.2f} h"
)

print(
    f"Demanda mínima: {P_demanda[i_dem_min]:.2f} MW "
    f"a las {tiempo[i_dem_min]:.2f} h"
)

print(
    f"Máxima potencia renovable: {P_renovable[i_ren_max]:.2f} MW "
    f"a las {tiempo[i_ren_max]:.2f} h"
)


# ============================================================
# PARTE (b)
# Energía generada durante todo el día
# ============================================================

# Como la potencia está expresada en MW y el tiempo en horas,
# la integral de P(t) respecto del tiempo queda expresada en MWh.

E_renovable = trapcomp(tiempo, P_renovable)

E_demanda = trapcomp(tiempo, P_demanda)


# Porcentaje de la energía demandada que fue cubierta
# mediante fuentes renovables

porcentaje_energia_renovable = (E_renovable / E_demanda) * 100


print("\n" + "=" * 60)
print("PARTE (b)")
print("=" * 60)

print(
    f"Energía renovable total = {E_renovable:.2f} MWh"
)

print(
    f"Energía demandada total = {E_demanda:.2f} MWh"
)

print(
    "Porcentaje de la demanda cubierto mediante "
    f"energías renovables = {porcentaje_energia_renovable:.2f} %"
)


# ============================================================
# PARTE (c)
# Evolución de cada fuente de energía renovable
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(tiempo, eolica, label="Eólica")
plt.plot(tiempo, fotovoltaica, label="Fotovoltaica")
plt.plot(tiempo, bioenergias, label="Bioenergías")
plt.plot(tiempo, hidraulica, label="Hidráulica")

plt.xlabel("Tiempo [h]")
plt.ylabel("Potencia [MW]")
plt.title("Generación eléctrica por fuente renovable")
plt.grid()
plt.legend()
plt.tight_layout()

plt.show()


# Máxima potencia fotovoltaica

i_fot_max = np.argmax(fotovoltaica)


print("\n" + "=" * 60)
print("PARTE (c)")
print("=" * 60)

print(
    f"Máxima potencia fotovoltaica: "
    f"{fotovoltaica[i_fot_max]:.2f} MW "
    f"a las {tiempo[i_fot_max]:.2f} h"
)


# ============================================================
# PARTE (d)
# Porcentaje de energía renovable proveniente de la eólica
# ============================================================

E_eolica = trapcomp(tiempo, eolica)

porcentaje_eolica = (E_eolica / E_renovable) * 100


print("\n" + "=" * 60)
print("PARTE (d)")
print("=" * 60)

print(
    f"Energía eólica total = {E_eolica:.2f} MWh"
)

print(
    "Porcentaje de la energía renovable generado "
    f"por energía eólica = {porcentaje_eolica:.2f} %"
)