import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Problema de interpolación polinomial a trozos
# Aproximar f(x) = sin(x) en [0, pi]
# ============================================================

# ------------------------------------------------------------
# 1. Definimos la función
# ------------------------------------------------------------
f = lambda x: np.sin(x)

# ------------------------------------------------------------
# 2. Elegimos la cantidad de elementos de la partición
# ------------------------------------------------------------
# Interpolación lineal:
#   cada polinomio utiliza 2 puntos -> cubre 1 elemento.
#   No hay restricción especial sobre N.
#
# Interpolación cuadrática:
#   cada polinomio utiliza 3 puntos -> cubre 2 elementos.
#   Por lo tanto, N debe ser múltiplo de 2.
#
# Interpolación cúbica:
#   cada polinomio utiliza 4 puntos -> cubre 3 elementos.
#   Por lo tanto, N debe ser múltiplo de 3.
#
# Para que se puedan realizar las tres interpolaciones,
# N debe ser múltiplo de mcm(2, 3) = 6.
#
# Elegimos:
N = 12

# Si tenemos N elementos, necesitamos N+1 puntos
inter = np.linspace(0, np.pi, N + 1)

# Evaluamos la función en los nodos de la partición
f_eval = f(inter)

# ------------------------------------------------------------
# 3. Función para realizar una interpolación polinomial
#    a trozos de grado dado
# ------------------------------------------------------------

def interpolacion_trozos(inter, f_eval, grado):
    # Listas donde guardaremos los puntos de cada tramo
    X_total = []
    Y_total = []

    # Para un polinomio de grado "grado" necesitamos
    # grado + 1 nodos.
    #
    # Además, cada polinomio cubre "grado" elementos.
    #
    # grado = 1 -> avanzamos de 1 en 1
    # grado = 2 -> avanzamos de 2 en 2
    # grado = 3 -> avanzamos de 3 en 3

    for i in range(0, len(inter) - 1, grado):
        # Seleccionamos los nodos correspondientes al tramo
        x_nodos = inter[i:i + grado + 1]
        y_nodos = f_eval[i:i + grado + 1]

        # Calculamos el polinomio interpolante
        coefs = np.polyfit(x_nodos, y_nodos, grado)

        # Evaluamos únicamente dentro del tramo correspondiente
        x_eval = np.linspace(x_nodos[0], x_nodos[-1], 100)
        y_eval = np.polyval(coefs, x_eval)

        # Guardamos los resultados
        X_total.extend(x_eval)
        Y_total.extend(y_eval)

    return np.array(X_total), np.array(Y_total)


# ------------------------------------------------------------
# 4. Interpolación lineal a trozos
# ------------------------------------------------------------
X_lineal, Y_lineal = interpolacion_trozos(inter,f_eval,grado=1)

# ------------------------------------------------------------
# 5. Interpolación cuadrática a trozos
# ------------------------------------------------------------
X_cuadratica, Y_cuadratica = interpolacion_trozos(inter,f_eval,grado=2)

# ------------------------------------------------------------
# 6. Interpolación cúbica a trozos
# ------------------------------------------------------------
X_cubica, Y_cubica = interpolacion_trozos(inter,f_eval,grado=3)

# ------------------------------------------------------------
# 7. Graficamos la función original y las interpolaciones
# ------------------------------------------------------------
xx = np.linspace(0, np.pi, 500)

plt.figure(figsize=(10, 6))

# Función original
plt.plot(xx,f(xx),"k--",label="f(x) = sin(x)")

# Interpolación lineal
plt.plot(X_lineal,Y_lineal,label="Interpolación lineal")

# Interpolación cuadrática
plt.plot(X_cuadratica,Y_cuadratica,label="Interpolación cuadrática")

# Interpolación cúbica
plt.plot(X_cubica,Y_cubica,label="Interpolación cúbica")

# Nodos de la partición
plt.plot(inter,f_eval,"ko",label="Nodos")

plt.xlabel("x")
plt.ylabel("y")
plt.title("Interpolación polinomial a trozos de sin(x)")
plt.grid()
plt.legend()
plt.tight_layout()

plt.show()

# ------------------------------------------------------------
# 8. Evaluación de los errores en x = pi/8
# ------------------------------------------------------------

x_error = np.pi / 8

# Valor exacto
valor_exacto = f(x_error)

# ------------------------------------------------------------
# Función para evaluar la interpolación a trozos
# en un punto particular
# ------------------------------------------------------------
def evaluar_interpolacion(x, inter, f_eval, grado):

    # Buscamos el elemento de la partición donde está x
    i = np.searchsorted(inter, x) - 1

    # Evitamos problemas si x coincide con el primer nodo
    if i < 0:
        i = 0

    # Determinamos a qué tramo pertenece
    inicio = (i // grado) * grado

    # Si x es el último punto del intervalo
    if np.isclose(x, inter[-1]):
        inicio = len(inter) - grado - 1

    # Tomamos grado + 1 nodos
    x_nodos = inter[inicio:inicio + grado + 1]
    y_nodos = f_eval[inicio:inicio + grado + 1]

    # Construimos el polinomio interpolante
    coefs = np.polyfit(x_nodos, y_nodos, grado)

    # Evaluamos el polinomio en x
    return np.polyval(coefs, x)


# Evaluamos las tres interpolaciones
valor_lineal = evaluar_interpolacion(x_error,inter,f_eval,grado=1)

valor_cuadratico = evaluar_interpolacion(x_error,inter,f_eval,grado=2)

valor_cubico = evaluar_interpolacion(x_error,inter,f_eval,grado=3)

# ------------------------------------------------------------
# 9. Calculamos los errores
# ------------------------------------------------------------
error_lineal = np.abs(valor_exacto - valor_lineal)

error_cuadratico = np.abs(valor_exacto - valor_cuadratico)

error_cubico = np.abs(valor_exacto - valor_cubico)

# ------------------------------------------------------------
# 10. Mostramos los resultados
# ------------------------------------------------------------

print()
print("Resultados en x = pi/8")
print("-------------------------------------------")

print(f"Valor exacto       = {valor_exacto:.10f}")

print()
print(f"Valor lineal       = {valor_lineal:.10f}")
print(f"Error lineal       = {error_lineal:.10e}")

print()
print(f"Valor cuadrático   = {valor_cuadratico:.10f}")
print(f"Error cuadrático   = {error_cuadratico:.10e}")

print()
print(f"Valor cúbico       = {valor_cubico:.10f}")
print(f"Error cúbico       = {error_cubico:.10e}")