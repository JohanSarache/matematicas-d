# Sabiendo que R = c = rho = 1
# u(r,theta) = 10 + r³ * np.cos(3*theta) + 2*r² * np.sin(2*theta)
# Determinar la energía total theta entre -pi y pi y r entre 0 y R=1 
#
#                     pi     R
#     E = c*rho * integral integral u(r,theta) * r dr dtheta
#                    -pi     0
#
# ============================================================
# 1. Sustitución de u(r,theta) en la integral
# ============================================================
#
# Como en coordenadas polares aparece el factor r del elemento
# de área, primero se multiplica la temperatura por r:
#
#     u(r,theta)*r
#
# Por lo tanto:
#
#                 pi   1
# E = c*rho * integral integral [
#               -pi    0
#
#             10*r
#           + r⁴*cos(3*theta)
#           + 2*r³*sin(2*theta)
#
#                              ] dr dtheta
#
# ============================================================
# 2. Separación de las variables r y theta
# ============================================================
#
# Cada término puede escribirse como un producto de una función
# que depende solamente de r y otra que depende solamente de
# theta.
#
# Primer término:
#
#     10*r = (10*r) * 1
#
# por lo tanto:
#
#                         1                  pi
#     E1 = 10 * [ integral r dr ] * [ integral 1 dtheta ]
#                         0                 -pi
#
#
# Segundo término:
#
#     r⁴*cos(3*theta)
#
# por lo tanto:
#
#                    1                      pi
#     E2 = [ integral r⁴ dr ] * [ integral cos(3*theta) dtheta ]
#                    0                     -pi
#
#
# Tercer término:
#
#     2*r³*sin(2*theta)
#
# por lo tanto:
#
#                         1                      pi
#     E3 = 2 * [ integral r³ dr ] * [ integral sin(2*theta) dtheta ]
#                         0                     -pi
#
#
# ============================================================
# 3. Expresión final para calcular numéricamente
# ============================================================
#
# La energía total queda:
#
#     E = c*rho * (E1 + E2 + E3)
#
# es decir:
#
# E = c*rho * [
#
#       10 * integral(r, 0, 1)
#          * integral(1, -pi, pi)
#
#     + integral(r⁴, 0, 1)
#          * integral(cos(3*theta), -pi, pi)
#
#     + 2 * integral(r³, 0, 1)
#          * integral(sin(2*theta), -pi, pi)
#
# ]
#
# De esta manera, la integral doble se transforma en seis
# integrales unidimensionales que pueden calcularse utilizando
# intNCcompuesta() definida en metodos.py.
#
#
# ============================================================
# 4. Observación sobre el resultado
# ============================================================
#
# Debido a la simetría del intervalo [-pi, pi]:
#
#     integral cos(3*theta) dtheta = 0
#
# y
#
#     integral sin(2*theta) dtheta = 0
#
# Por lo tanto, los términos E2 y E3 deberían resultar
# numéricamente iguales o muy próximos a cero.
#
# Solamente contribuye el primer término:
#
#     E = c*rho * 10
#         * integral(r, 0, 1)
#         * integral(1, -pi, pi)
#
# cuyo valor exacto es:
#
#     E = 10*pi*c*rho
#
# El cálculo numérico permitirá comprobar este resultado.
# ============================================================

import numpy as np
from metodos import *

c, rho, R = 1, 1, 1

fr1 = lambda r: 10*r
ftheta1 = lambda theta: 1

Er1 = intNCcompuesta(fr1, 0, R, 100, 3)

Etheta1 = intNCcompuesta(ftheta1, -np.pi, np.pi, 100, 3)

Etotal = c * rho * Er1 * Etheta1

Eexacta = 10 * np.pi * c * rho

print("\nEnergía total calculada numéricamente: ", Etotal)
print("Energía total exacta: ", Eexacta)