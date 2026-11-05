from collections.abc import Callable
def rkme(g: Callable[[float, float], float],
        N: int,
        a: int | float,
        b: int | float,
        y0: int | float):
    """Solve y' = f(t, y) with n RK - Modified Euler steps. Returns lists ts, ws."""
    w = y0
    h = (b - a) / N
    t = a
    ts, ws = [t], [w]
    for i in range(1, N+1):
        w  += h/2 * (g(t,w) + g(t + h, w + h * g(t, w)))
        t += h
        ts.append(t); ws.append(w)   
    return ts, ws