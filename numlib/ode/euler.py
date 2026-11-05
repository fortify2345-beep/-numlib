from collections.abc import Callable
from math import exp, log, sqrt, cos, sin, tan, pi, floor
def euler(g: Callable[[float, float], float],
        N: int,
        a: int | float,
        b: int | float,
        y0: int | float):
    """Solve y' = g(t, y) on [a, b] with Euler's method.

    Returns lists (ts, ws)
    """
    w = y0
    h = (b - a) / N
    t = a
    ts, ws = [t], [w] 
    for i in range(1, N+1):
        w  += h * g(t,w)
        t += h
        ts.append(t); ws.append(w)
    return ts, ws