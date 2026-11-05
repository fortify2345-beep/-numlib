import matplotlib.pyplot as plt
def rk45(g, a, b, y0, q_min = 0.1, q_max = 4, h_max = 0.25, h_min = 0.01, tol = 10**(-6)):
    """Solve y' = g(t, y) on [a, b] with adaptive Runge-Kutta-Fehlberg (RK45).

    Returns lists (ts, ws), or None if the step size drops below h_min.
    """
    t, w = a, y0
    h = h_max
    ts, ws = [t],[w]
    while t < b:
        h = min(h, b - t)

        k1 = h * g(t, w)
        k2 = h * g(t + h/4,     w + k1/4)
        k3 = h * g(t + 3*h/8,   w + 3*k1/32 + 9*k2/32)
        k4 = h * g(t + 12*h/13, w + 1932*k1/2197 - 7200*k2/2197 + 7296*k3/2197)
        k5 = h * g(t + h,       w + 439*k1/216 - 8*k2 + 3680*k3/513 - 845*k4/4104)
        k6 = h * g(t + h/2,     w - 8*k1/27 + 2*k2 - 3544*k3/2565 + 1859*k4/4104 - 11*k5/40)

        R = abs(k1/360 - 128*k3/4275 - 2197*k4/75240 + k5/50 + 2*k6/55) / h

        if R <= tol:
            t += h
            w += 25*k1/216 + 1408*k3/2565 + 2197*k4/4104 - k5/5
            ts.append(t); ws.append(w)

        delta = 0.84 * (tol / R) ** 0.25 if R > 0 else q_max
        h *= min(max(delta, q_min), q_max)
        h = min(h, h_max)

        if h < h_min and t < b:
            print("Can't reach b: minimum h exceeded")
            return None
    return ts, ws