import numpy as np
import matplotlib.pyplot as plt

f = lambda x: np.sin(x)

inter = np.linspace(0, np.pi, 12)
f_eval = f(inter)

grado = 3

for i in range(len(inter) - 1):

    # Elegimos 4 puntos cercanos al subintervalo [x_i, x_{i+1}]
    
    if i == 0:
        indices = np.arange(0, 4)

    elif i >= len(inter) - 3:
        indices = np.arange(len(inter)-4, len(inter))

    else:
        indices = np.arange(i-1, i+3)

    x_nodos = inter[indices]
    y_nodos = f_eval[indices]

    # Polinomio cúbico que interpola los 4 puntos
    coefs = np.polyfit(x_nodos, y_nodos, grado)

    # Se evalúa SOLO en el subintervalo correspondiente
    x_eval = np.linspace(inter[i], inter[i+1], 100)
    y_eval = np.polyval(coefs, x_eval)

    plt.plot(x_eval, y_eval)


# Función original
xx = np.linspace(0, np.pi, 500)

plt.plot(xx, f(xx), "--", label="f(x)")
plt.plot(inter, f_eval, "o", label="Nodos")

plt.legend()
plt.show()