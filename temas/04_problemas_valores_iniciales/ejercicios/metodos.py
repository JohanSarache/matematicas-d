import numpy as np

def euler1(f, inter, y0, L):
    """
    Método de Euler para resolver

        y' = f(t, y),   t0 <= t <= TF
        y(t0) = y0

    usando L pasos.

    Parámetros
    ----------
    f : función
        Función que define la ecuación diferencial.
    inter : lista o tupla
        Intervalo [t0, TF].
    y0 : float
        Condición inicial.
    L : int
        Número de pasos.

    Retorna
    -------
    t : ndarray
        Nodos temporales.
    y : ndarray
        Aproximación numérica en cada nodo.
    """

    t = np.linspace(inter[0], inter[1], L + 1)

    h = (inter[1] - inter[0]) / L

    # Reservamos lugar en memoria para y
    y = np.zeros(L + 1)

    y[0] = y0

    for n in range(L):
        y[n + 1] = y[n] + h * f(t[n], y[n])

    return t, y