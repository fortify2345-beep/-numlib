import numpy as np
import pytest

from numlib.ode.rk4 import rk4
from numlib.systems.double_pendulum import DoublePendulum


def test_eqm_shape_and_rest_equilibrium():
    p = DoublePendulum()
    assert p.eqm(0, p.default_state()).shape == (4,)
    assert np.allclose(p.eqm(0, [0, 0, 0, 0]), 0)


def test_con_and_cart_der_shapes():
    p = DoublePendulum()
    s = p.default_state()
    assert p.con(s).shape == (4,)
    assert p.cart_der(s).shape == (4,)


def test_cart_der_matches_finite_difference_of_con():
    p = DoublePendulum(1.2, 0.7, 1.0, 2.0)
    s = np.array([0.5, -0.3, 0.8, -1.1])
    eps = 1e-6
    ds = np.array([s[2], s[3], 0, 0]) * eps
    fd = (p.con(s + ds) - p.con(s - ds)) / (2 * eps)
    assert np.allclose(p.cart_der(s), fd, atol=1e-6)


def test_energy_conserved_by_rk4():
    p = DoublePendulum(1.0, 0.8, 1.0, 1.5)
    _, ws = rk4(p.eqm, 0.0, p.default_state(), 10.0, 5000)
    e = np.array([p.te(w) for w in ws])
    assert np.allclose(e, e[0], rtol=1e-6)
