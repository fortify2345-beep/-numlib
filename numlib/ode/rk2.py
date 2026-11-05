from collections.abc import Callable
def rk2(g: Callable[[float, float], float],
        N: int,
        a: int | float,
        b: int | float,
        y0: int | float):
    """Solve y' = f(t, y) with n RK2. Returns lists ts, ws."""
    w = y0
    h = (b - a) / N
    t = a
    ts, ws = [t], [w]
    for i in range(1, N+1):
        w  += h * (g(t + h/2, w + h/2 * g(t, w)))
        t += h
        ts.append(t); ws.append(w)
    return ts, ws