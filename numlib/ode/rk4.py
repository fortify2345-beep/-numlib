import numpy as np
def rk4(f, t0, y0, t_end, n):
    """Solve y' = f(t, y) with n RK4 steps. Returns lists ts, ws."""
    y0 = np.asarray(y0, dtype = float)
    h = (t_end - t0) / n
    t, w = t0, y0.copy()
    ws = np.empty((n+1, y0.size))
    ts = t0 + h * np.arange(n+1)
    ws[0] = y0 
    for i in range(n):
        t = ts[i]
        k1 = h * f(t, w)
        k2 = h * f(t + h/2, w + k1/2)
        k3 = h * f(t + h/2, w + k2/2)
        k4 = h * f(t + h, w + k3)
        w += (k1 + 2*k2 + 2*k3 + k4) / 6
        ws[i + 1] = w
    return ts, ws