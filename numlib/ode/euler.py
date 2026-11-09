from collections.abc import Callable
import numpy as np
def euler(g: Callable[[float, float], float],
        N: int,
        a: int | float,
        b: int | float,
        y0: int | float):
    """Solve y' = g(t, y) on [a, b] with Euler's method.

    Returns lists (ts, ws)
    """
    y0 = np.asarray(y0, dtype = float)
    w = y0.copy()
    h = (b - a) / N
    t = a
    ts = a + h * np.arange(N + 1)
    ws = np.empty((N+1, y0.size))
    ws[0] = w
    for i in range(N):
        t = ts[i]
        w  += h * g(t,w)
        ws[i+1] = w
    return ts, ws