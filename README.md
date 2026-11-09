# numlib

A small pure-Python library of numerical methods. It currently contains solvers for first-order ordinary differential equations (ODEs) of the form

```
y' = g(t, y),   y(a) = y0,   t in [a, b]
```

## Layout

```
numlib/
└── numlib/
    └── ode/
        ├── __init__.py   # package exports
        ├── euler.py      # Euler's method
        ├── rk2.py        # Runge-Kutta 2 (midpoint)
        ├── rkme.py       # Runge-Kutta 2 (modified Euler / Heun)
        ├── rk4.py        # classical Runge-Kutta 4
        └── rk45.py       # adaptive Runge-Kutta-Fehlberg (RKF45)
```

## Methods

| Method | Function | Order | Step size | Notes |
|---|---|---|---|---|
| Euler | `Euler` | 1 | fixed | `w += h*g(t, w)` |
| RK2 (midpoint) | `RK2` | 2 | fixed | evaluates `g` at `t + h/2` |
| RK2 (modified Euler) | `RKme` | 2 | fixed | averages slopes at both ends of the step |
| RK4 | `rk4` | 4 | fixed | classical four-stage method |
| RKF45 | `RK45` | 4(5) | adaptive | step size is controlled by an error tolerance |

All solvers return two lists `(ts, ws)`: the time points and the approximate solution values at those points. They work on scalar `y` only.

## Usage

Solve `y' = y` with `y(0) = 1` on `[0, 1]`. The exact solution is `e`.

```python
from math import e
from numlib.ode.euler import Euler
from numlib.ode.rk4 import rk4
from numlib.ode.rk45 import RK45

g = lambda t, y: y

ts, ws = Euler(g, N=100, a=0, b=1, y0=1)
print(ws[-1], abs(ws[-1] - e))

ts, ws = rk4(g, t0=0, y0=1, t_end=1, n=10)
print(ws[-1], abs(ws[-1] - e))

ts, ws = RK45(g, a=0, b=1, y0=1, tol=1e-8)
print(ws[-1], abs(ws[-1] - e))
```

Import each function from its own module, as above. See "Known issues" for why the package-level import currently fails.

## Function signatures

Argument order differs between solvers:

```python
Euler(g, N, a, b, y0)
RK2(g, N, a, b, y0)
RKme(g, N, a, b, y0)
rk4(f, t0, y0, t_end, n)
RK45(g, a, b, y0, q_min=0.1, q_max=4, h_max=0.25, h_min=0.01, tol=1e-6)
```

- `g` / `f`: right-hand side `g(t, y)`.
- `N` / `n`: number of fixed steps.
- `a, b` (or `t0, t_end`): interval endpoints.
- `y0`: initial value.

`RK45` takes these extra parameters:

- `tol`: error tolerance per step.
- `h_max`, `h_min`: bounds on the step size.
- `q_min`, `q_max`: bounds on how much the step size can change in one step.

If the step size falls below `h_min` before reaching `b`, `RK45` prints a message and returns `None`.

## Known issues

- **`ode/__init__.py` fails on import.** It imports lowercase names (`euler`, `rk2`, `rk45`, `rkme`) from modules that define `Euler`, `RK2`, `RK45` and `RKme`. Only `rk4` matches. As a result, `import numlib.ode` raises `ImportError`. Fix this by renaming the functions or changing the imports.
- **Inconsistent signatures.** `rk4` uses a different argument order from the other solvers (see above).
- **Unneeded imports.** `rk45.py` imports `matplotlib` without using it, which makes matplotlib a hard dependency. `euler.py` imports several unused `math` names.
- **No packaging or tests.** There is no `pyproject.toml`, so the library can't be installed with `pip`. Run Python from this folder (the one containing this README) for `numlib` to be importable.

## Requirements

- Python 3.10 or newer (the code uses `int | float` type syntax).
- `matplotlib`, only because of the unused import in `rk45.py`.
