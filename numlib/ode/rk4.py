def rk4(f, t0, y0, t_end, n):
    """Solve y' = f(t, y) with n RK4 steps. Returns lists ts, ws."""
    h = (t_end - t0) / n
    t, w = t0, y0
    ts, ws = [t], [w]
    for _ in range(n):
        k1 = h * f(t, w)
        k2 = h * f(t + h/2, w + k1/2)
        k3 = h * f(t + h/2, w + k2/2)
        k4 = h * f(t + h, w + k3)
        w += (k1 + 2*k2 + 2*k3 + k4) / 6
        t += h
        ts.append(t)
        ws.append(w)
    return ts, ws