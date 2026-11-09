import numpy as np

G = 9.81


class DoublePendulum:
    """Compound double pendulum: two uniform rods, lengths l1, l2, masses m1, m2.

    State is [a1, a2, w1, w2]: angles from the downward vertical and their
    angular velocities. Rod 1 pivots at the origin, rod 2 pivots at the end
    of rod 1. con() and cart_der() give the rods' centres of mass,
    as [x1, y1, x2, y2].
    """

    def __init__(self, l1=1, l2=1, m1=1, m2=1):
        self.l1 = l1
        self.l2 = l2
        self.m1 = m1
        self.m2 = m2

    def default_state(self):
        return np.array([np.pi / 4, np.pi / 6, 0, 0])

    def eqm(self, t, s):
        """Returns d/dt of the state [a1, a2, w1, w2].

        From the Lagrangian with T = 1/2 M11 w1^2 + M12 w1 w2 + 1/2 M22 w2^2:
            M11 = (m1/3 + m2) l1^2,  M22 = m2 l2^2 / 3,
            M12 = (m2 l1 l2 / 2) cos(a1 - a2)
        giving a 2x2 linear system for (a1'', a2'').
        """
        a1, a2, w1, w2 = np.asarray(s, dtype=float)
        l1, l2, m1, m2 = self.l1, self.l2, self.m1, self.m2
        d = a1 - a2
        c = m2 * l1 * l2 / 2

        M11 = (m1 / 3 + m2) * l1**2
        M22 = m2 * l2**2 / 3
        M12 = c * np.cos(d)

        b1 = -c * np.sin(d) * w2**2 - G * l1 * (m1 /2 + m2) * np.sin(a1)
        b2 = c * np.sin(d) * w1**2 - G * m2 * l2 / 2 * np.sin(a2)

        det = M11 * M22 - M12**2
        der = np.empty(4)
        der[0] = w1
        der[1] = w2
        der[2] = (b1 * M22 - M12 * b2) / det
        der[3] = (M11 * b2 - M12 * b1) / det
        return der

    def con(self, st):
        """Centre-of-mass positions [x1, y1, x2, y2] of the two rods."""
        a1, a2, _, _ = np.asarray(st, dtype=float)
        return np.array([self.l1 * np.sin(a1) / 2,
                         -self.l1 * np.cos(a1) / 2,
                         self.l1 * np.sin(a1) + self.l2 * np.sin(a2) / 2,
                         -self.l1 * np.cos(a1) - self.l2 * np.cos(a2) / 2])
    def jt(self, st):
        """joint and tip positions [x1, y1, x2, y2] of the two rods."""
        a1, a2, _, _ = np.asarray(st, dtype=float)
        return np.array([self.l1 * np.sin(a1),
                         -self.l1 * np.cos(a1),
                         self.l1 * np.sin(a1) + self.l2 * np.sin(a2),
                         -self.l1 * np.cos(a1) - self.l2 * np.cos(a2)])

    def cart_der(self, st):
        """Centre-of-mass velocities [x1', y1', x2', y2']."""
        a1, a2, w1, w2 = np.asarray(st, dtype=float)
        return np.array([self.l1 * np.cos(a1) * w1 / 2,
                         self.l1 * np.sin(a1) * w1 / 2,
                         self.l1 * np.cos(a1) * w1 + self.l2 * np.cos(a2) * w2 / 2,
                         self.l1 * np.sin(a1) * w1 + self.l2 * np.sin(a2) * w2 / 2])

    def te(self, st):
        return self.ke(st) + self.pe(st)

    def ke(self, st):
        """Translational KE of the centres of mass + rotational KE (I = m l^2 / 12)."""
        w1, w2 = np.asarray(st, dtype=float)[2:]
        vx1, vy1, vx2, vy2 = self.cart_der(st)
        return (self.m1 * (vx1**2 + vy1**2) / 2
                + self.m2 * (vx2**2 + vy2**2) / 2
                + self.m1 * self.l1**2 * w1**2 / 24
                + self.m2 * self.l2**2 * w2**2 / 24)

    def pe(self, st):
        _, y1, _, y2 = self.con(st)
        return G * (self.m1 * y1 + self.m2 * y2)
