import numpy as np
import pytest

from numlib.ode.rk4 import rk4


# ---------- helpers ----------

def decay(t, y):
    return -y


def oscillator(t, y):
    # y = [x, v];  x'' = -x
    return np.array([y[1], -y[0]])


def max_error_decay(n):
    ts, ws = rk4(decay, 0.0, [1.0], 1.0, n)
    return abs(ws[-1, 0] - np.exp(-1.0))


# ---------- output structure ----------

@pytest.mark.parametrize("n", [1, 5, 100])
def test_output_shapes(n):
    ts, ws = rk4(decay, 0.0, [1.0, 2.0], 1.0, n)
    assert ts.shape == (n + 1,)
    assert ws.shape == (n + 1, 2)


def test_time_grid_endpoints_and_spacing():
    ts, _ = rk4(decay, 2.0, [1.0], 5.0, 6)
    assert ts[0] == pytest.approx(2.0)
    assert ts[-1] == pytest.approx(5.0)
    assert np.allclose(np.diff(ts), 0.5)


def test_first_row_is_initial_condition():
    y0 = [1.5, -2.0, 3.0]
    _, ws = rk4(lambda t, y: np.zeros_like(y), 0.0, y0, 1.0, 4)
    assert np.array_equal(ws[0], y0)


def test_scalar_y0_gives_column_vector():
    _, ws = rk4(decay, 0.0, 1.0, 1.0, 10)
    assert ws.shape == (11, 1)


def test_accepts_list_and_int_initial_conditions():
    _, ws = rk4(decay, 0.0, [1], 1.0, 10)
    assert ws.dtype == float
    assert ws[-1, 0] == pytest.approx(np.exp(-1.0), abs=1e-6)


def test_does_not_mutate_y0():
    y0 = np.array([1.0, 0.0])
    original = y0.copy()
    rk4(oscillator, 0.0, y0, 1.0, 10)
    assert np.array_equal(y0, original)


def test_rows_are_independent_snapshots():
    # guards against ws[i] aliasing the in-place-updated w
    _, ws = rk4(decay, 0.0, [1.0], 1.0, 5)
    assert len(np.unique(ws[:, 0])) == 6
    assert np.all(np.diff(ws[:, 0]) < 0)


# ---------- correctness ----------

def test_zero_rhs_keeps_solution_constant():
    _, ws = rk4(lambda t, y: np.zeros_like(y), 0.0, [3.0, -1.0], 10.0, 7)
    assert np.allclose(ws, [3.0, -1.0])


def test_constant_rhs_is_exact_linear_growth():
    ts, ws = rk4(lambda t, y: np.array([2.0]), 0.0, [1.0], 3.0, 4)
    assert np.allclose(ws[:, 0], 1.0 + 2.0 * ts)


def test_exact_for_cubic_time_dependent_rhs():
    # y' = t^3  ->  y = t^4/4 ; RK4 reduces to Simpson's rule, exact up to cubics
    ts, ws = rk4(lambda t, y: np.array([t**3]), 0.0, [0.0], 2.0, 3)
    assert np.allclose(ws[:, 0], ts**4 / 4, atol=1e-12)


def test_exponential_decay_accuracy():
    ts, ws = rk4(decay, 0.0, [1.0], 1.0, 50)
    assert np.allclose(ws[:, 0], np.exp(-ts), atol=1e-8)


def test_nonautonomous_ode():
    # y' = t*y, y(0)=1  ->  y = exp(t^2/2)
    ts, ws = rk4(lambda t, y: t * y, 0.0, [1.0], 1.0, 100)
    assert np.allclose(ws[:, 0], np.exp(ts**2 / 2), rtol=1e-8)


def test_harmonic_oscillator_system():
    ts, ws = rk4(oscillator, 0.0, [1.0, 0.0], 2 * np.pi, 200)
    assert np.allclose(ws[:, 0], np.cos(ts), atol=1e-6)
    assert np.allclose(ws[:, 1], -np.sin(ts), atol=1e-6)


def test_harmonic_oscillator_energy_nearly_conserved():
    _, ws = rk4(oscillator, 0.0, [1.0, 0.0], 10.0, 1000)
    energy = 0.5 * (ws[:, 0] ** 2 + ws[:, 1] ** 2)
    assert np.allclose(energy, 0.5, atol=1e-8)


def test_backward_integration():
    ts, ws = rk4(decay, 1.0, [np.exp(-1.0)], 0.0, 50)
    assert ts[-1] == pytest.approx(0.0)
    assert ws[-1, 0] == pytest.approx(1.0, abs=1e-8)


# ---------- convergence order ----------

def test_fourth_order_convergence():
    e1, e2, e3 = max_error_decay(10), max_error_decay(20), max_error_decay(40)
    assert e1 > e2 > e3
    # halving h should cut error by ~2^4 = 16
    assert np.log2(e1 / e2) == pytest.approx(4, abs=0.3)
    assert np.log2(e2 / e3) == pytest.approx(4, abs=0.3)


# ---------- edge cases ----------

def test_single_step():
    ts, ws = rk4(decay, 0.0, [1.0], 0.1, 1)
    assert ts.shape == (2,)
    # one RK4 step on y'=-y equals the degree-4 Taylor polynomial of exp(-h)
    h = 0.1
    taylor = 1 - h + h**2 / 2 - h**3 / 6 + h**4 / 24
    assert ws[1, 0] == pytest.approx(taylor, rel=1e-14)


def test_zero_steps_raises():
    with pytest.raises(ZeroDivisionError):
        rk4(decay, 0.0, [1.0], 1.0, 0)


def test_rhs_called_four_times_per_step():
    calls = []

    def f(t, y):
        calls.append(t)
        return -y

    rk4(f, 0.0, [1.0], 1.0, 5)
    assert len(calls) == 20


def test_rhs_returning_list_fails():
    # h * list would repeat/raise; f must return an ndarray
    with pytest.raises(TypeError):
        rk4(lambda t, y: [-y[0]], 0.0, [1.0], 1.0, 3)