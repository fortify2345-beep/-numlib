'''
import decimal
from decimal import Decimal, localcontext
import math
from math import factorial as fac
with localcontext() as ctx:
    ctx.prec = 4
    ctx.rounding = decimal.ROUND_DOWN
    sm = Decimal('1')
    curr_fac = Decimal('1')
    e = +Decimal('2.71828182845904523536')
    for i in range(1,6):
        a = Decimal(str(i))
        curr_fac *= a
        ai = Decimal('1')/curr_fac
        sm += ai
    err = Decimal(e - sm)
    rel_err = err/e
print(sm)
print(err)
print(rel_err)
'''
'''
#Bisection method implementation
import math
from math import sin, cos, exp, log, pi, log10
from collections.abc import Callable
def sign(x):
    return (x > 0) - (x < 0)
def f(x : float):
    return x  + 2 * log10(1.08108 * 10 ** (-4) + 2.52 * 10 ** (-5) * x)
def BRS(a : float, b : float, g : Callable[[float], float], act : float | int, prev = 10**5, tol = 10**(-6), max_cnt = 500, itr = 0):
    itr_cnt = itr + 1
    if itr_cnt >= max_cnt:
        print("Too much work")
        return
    fa = g(a)
    fb = g(b)
    p = a + (b-a)/2
    fp = g(p)
    if p and prev and abs((p - prev)/p) <= tol:
        print(f"The required root: {p},The number of iterations for termination: {itr_cnt}")
        return
    print(f"{p},{abs((p - prev)/p)}, {abs((p-act)/act)}")
    prev = p 

    if sign(fp) * sign(fa) > 0:
        BRS(p, b, g, act, prev, tol, max_cnt, itr_cnt)
    else:
        BRS(a, p, g, act, prev, tol, max_cnt, itr_cnt)
    return
'''
'''
from math import sin, cos, tan, pi 
from collections.abc import Callable 
def sgn(x):
    return int(math.copysign(1, x))
def h(x):
    return x - cos(x)

def g(x, y):
    return x - h(x) * (x - y) / (h(x) - h(y))
def SM(a: int | float, b: int | float,
       f: Callable[[int | float, int | float], int | float],
       reltol=1e-10, maxitr=500):
    p0, p1 = a, b
    if sgn(p0) * sgn(p1) >= 0:
        print("NOT FALSE POSITION COMPATIBLE! OR ALREADY DONE!")
        return
    for itr_cnt in range(1, maxitr + 1):
        if h(p1) == h(p0):                      # avoid division by zero
            print(f"Root ≈ {p1}. Iterations: {itr_cnt - 1}")
            return p1
        p2 = f(p1, p0)                          # newest point first

        if abs(p2 - p1) <= reltol * abs(p2):
            print(f"Root ≈ {p2}. Iterations: {itr_cnt}")
            return p2
        if sgn(p2) * sgn(p0) < 0:
            p0, p1 = p1, p0
        p0, p1 = p1, p2 
    raise ValueError("ITERATION LIMIT EXCEEDED!")
SM(-0.00001, 0.000001, g)
'''
'''
#Fixed Point ineration implementation
import math
from math import sin, cos, exp, log, pi
from collections.abc import Callable 
def g(x):
    u = 1.08108e-4 + 2.51e-5 * x
    return 2 * (2.51e-5 * x - u * log(u)) / (u * log(10) + 2 * 2.51e-5)
def FPI(a : int | float, f : Callable[[int | float], int | float], act, reltol = 10 ** (-6), maxitr = 500):
    p = a
    itr_cnt = 0
    while itr_cnt < maxitr:
        if p and abs((f(p) - p) / f(p)) <= reltol:
            print(f"The required fixed point is approx : {f(p)}. Number of iterations : {itr_cnt}")
            return
        if not p and abs(f(p)) <= reltol :
            print(f"The required fixed point is approx : {f(p)}. Number of iterations : {itr_cnt}")
        print(f"{p}, {abs((f(p) - p) / f(p))}, {abs((p - act)/act)}")
        itr_cnt += 1
        p = f(p)
    raise ValueError("ITERATION LIMIT EXCEEDED!")
FPI(7, g, 7.08727207)


import numpy as np
from numpy.polynomial import Polynomial

def NVM(ls: list, io: int | float, tol: int | float):
    deg = len(ls)
    x = Polynomial([0, 1])                      
    x_vals = [i[0] for i in ls]
    tab = np.zeros((len(ls), len(ls)), dtype=object)   
    for j in range(len(ls)):
        tab[j , 0] = ls[j][1]
    for i in range(len(ls)):
        for j in range(1, i + 1):
            tab[i, j] = ((tab[i - 1, j - 1] * (x - x_vals[i])) / (x_vals[i - j] - x_vals[i])) + (tab[i, j - 1] * (x - x_vals[i - j]) / (x_vals[i] - x_vals[i - j]))
        if i == 1 and abs(tab[i, i](io) - tab[i - 1, i - 1]) <= tol:
            print(f"Nevilles method returned : {tab[i, i](io)} and ended on the iteration : {i} ")
            return            
        if i > 1 and abs(tab[i, i](io) - tab[i - 1, i - 1](io)) <= tol:
            print(f"Nevilles method returned : {tab[i, i](io)} and ended on the iteration : {i} ")
            return
    print(f"Neville's method failed but last pass was {tab[-1, -1](io)}")
    return
'''
'''
#Assignment_1_sols
#Q1
def f(x):
    if x == 0 or x == 1:
        return 2.96875
    return 3 * f(x - 1) - 2 * f(x-2)

for i in range(2,6):
    print(f"Iteration number {i}: {f(i)}")

let size = 20;
let x = 0;
let y = 0;

function setup() {
  createCanvas(500, 500)
    frameRate(60);
    background(168, 230, 193);
}

function draw() {
  if(random(1) > 0.5){
    arc(x, y, size, size, 0, PI/2)
    arc(x + size, y+size, size, size, PI,PI + PI/2)
    fill(228, 230, 168)
    stroke(113, 185, 191)
    stroke(3)

  }
  else{
  arc(x, y+size, size, size, PI + PI/2, 2*PI)
  fill(168, 199, 230)
  stroke(147, 113, 191)
  strokeWeight(1)
  arc(x+size, y, size, size, PI/2, PI)

  }
  x = x + size
  if(x > width){
    x = 0; 
    y = y + size;
  
  }
}
let scl = 20;
let noiceval = 0;
let xScale = 0.015;
let yScale = 0.02;
let gapSlider;
let gap;
let offsetSlider;
let noiseLevel = 255;
  let noiseScale = 0.02;
let offset;
function setup() {
  createCanvas(400, 400);
  angleMode(DEGREES);
  // Set up the sliders
  
  //frameRate(2)
}

function draw() {
  background(220);

  for (let i = 0; i <= width; i += scl) {
    for (let j = 0; j <= width; j += scl) {
      push();
      let nx = noiseScale * i;
      let ny = noiseScale * j;
      translate(i, j);
      //let noiseValue = noise((x + offset) * xScale, (y + offset) * yScale);
      noiseDetail(6, 0.25);
      let c = noiseLevel * noise(nx, ny);
      //print(c)
      
      rotate(c);
      //rect(0,0,scl,scl)
      line(0, 0, scl, scl);
      //line(i,j,i+scl,j+scl)
      pop();
    }
  }
}


#Composite_Numerical_integration
from math import exp, log, sqrt, cos
from collections.abc import Callable
def g(x):
    return sqrt(1 + (cos(x))**2)
def CNI(a : int | float, b : int | float, f : Callable[[int | float], int | float], n : int | float):
    h = (b - a) / n
    x0 = f(a) + f(b)
    x1 = 0
    x2 = 0
    for i in range(1, n):
        x = a + i * h
        if i%2 == 0:
            x1 += 2 * f(x)
        else: 
            x2 += 4 * f(x)
    return h * (x0 + x1 + x2) / 3
print(CNI(0,48,g, 1000))

#Euler's method
from collections.abc import Callable
from math import exp, log, sqrt, cos, sin, tan, pi

import matplotlib.pyplot as plt


r = 0.1
d = 0.015
b = 0.02


def f(t, p):
    return r * b * (1 - p)
def exact(t: float) -> float:
    """Exact solution of y' = y - t^2 + 1, y(0) = 0.5 (used only for comparison)."""
    return 1 - 0.99 * exp(-r * b * t)


def EM(
    a: float,
    b: float,
    f: Callable[[float, float], float],
    alpha: float,
    n: int,
    M: float,
    L: float,
    y_exact: Callable[[float], float] | None = None,
):
    """
    Euler's method on [a, b] with n steps and y(a) = alpha.
    M bounds |y''| on [a, b]; L is the Lipschitz constant of f in y.
    Plots everything at once after computing.
    Returns (ts, ws, err_bounds).
    """
    step = (b - a) / n
    t, w = a, alpha

    ts, ws, bounds = [t], [w], [0.0]

    for i in range(1, n + 1):
        w += step * f(t, w)
        t = a + i * step
        bounds.append(step * M / (2 * L) * (exp(L * (t - a)) - 1))
        ts.append(t)
        ws.append(w)

    # --- plot ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    if y_exact is not None:
        N = 200
        xs = [a + (b - a) * k / N for k in range(N + 1)]
        ax1.plot(xs, [y_exact(x) for x in xs], "g-", alpha=0.6, label="exact")
    ax1.plot(ts, ws, "bo-", label="Euler")
    ax1.set_title("Euler's method")
    ax1.set_xlabel("t")
    ax1.set_ylabel("y")
    ax1.legend()

    ax2.plot(ts, bounds, "r.-", label="error bound")
    if y_exact is not None:
        ax2.plot(ts, [abs(y_exact(ti) - wi) for ti, wi in zip(ts, ws)], "b.-", label="actual error")
    ax2.set_title("Error bound  hM/(2L)(e^{L(t-a)} - 1)")
    ax2.set_xlabel("t")
    ax2.legend()

    plt.tight_layout()
    plt.show()
    return ts, ws, bounds


if __name__ == "__main__":
    # y' = y - t^2 + 1, 0 <= t <= 2, y(0) = 0.5
    # L = 1, M = 0.5*e^2 - 2 (max of |y''| on [0, 2])
    ts, ws, bounds = EM(
        a=0,
        b= 50,
        f=f,
        alpha=0.01,
        n=50,
        M=0.99 * (r * b)**2,
        L= r * b,
        y_exact=exact,
    )
    for t, w, e in zip(ts, ws, bounds):
        print(f"t={t:.2f}  w={w:.6f}  error bound={e:.6f}")
'''
from collections.abc import Callable
from math import exp, log, sqrt, cos, sin, tan, pi, floor

import matplotlib.pyplot as plt


def exact(t):
    return (t+1)**2 - 1/2 * exp(t)
def RK2(g: Callable[[float, float], float],
        N: int,
        a: int | float,
        b: int | float,
        y0: int | float):
    w = y0
    h = (b - a) / N
    t = a
    print("RK2 \n")
    print(f"{'Iteration_count':<12} {'t':>9} {'w':>12}{exact(t):>12} {'Error':>12}")
    print(f"{'0':<12} {t:>12} {w:>12}{exact(t):>12.6f}{'0':>12}")

    for i in range(1, N+1):
        w  += h * (g(t + h/2, w + h/2 * g(t, w)))
        t += h
        print(f"{i:<12} {t:>12.2f} {w:>12.6f}{exact(t):>12.6f}{abs(w - exact(t)):>12.7f}")
    print("\n")
    return
def RKme(g: Callable[[float, float], float],
        N: int,
        a: int | float,
        b: int | float,
        y0: int | float):
    w = y0
    h = (b - a) / N
    t = a
    print("Modified Euler \n")
    print(f"{'Iteration_count':<12} {'t':>9} {'w':>12}{'exact':>12} {'Error':>12}")
    print(f"{'0':<12} {t:>12} {w:>12}{exact(t):>12.6f}{'0':>12}")

    for i in range(1, N+1):
        w  += h/2 * (g(t,w) + g(t + h, w + h * g(t, w)))
        t += h
        print(f"{i:<12} {t:>12.2f} {w:>12.6f}{exact(t):>12.6f}{abs(w - exact(t)):>12.7f}")
    print("\n")
    return
def Euler(g: Callable[[float, float], float],
        N: int,
        a: int | float,
        b: int | float,
        y0: int | float):
    w = y0
    h = (b - a) / N
    t = a
    print("Euler \n")
    print(f"{'Iteration_count':<12} {'t':>9} {'w':>12}{'exact':>12} {'Error':>12}")
    print(f"{'0':<12} {t:>12} {w:>12}{exact(t):>12.6f}{'0':>12}")

    for i in range(1, N+1):
        w  += h * g(t,w)
        t += h
        print(f"{i:<12} {t:>12.2f} {w:>12.6f}{exact(t):>12.6f}{abs(w - exact(t)):>12.7f}")
    print("\n")
    return
def RK4(g: Callable[[float, float], float],
        N: int,
        a: int | float,
        b: int | float,
        y0: int | float):
    w = y0
    h = (b - a) / N
    t = a
    k1, k2, k3, k4 = None,None,None,None
    print("RK4 \n")
    print(f"{'Iteration_count':<12} {'t':>9} {'w':>12}{'exact':>12} {'Error':>12}")
    print(f"{'0':<12} {t:>12} {w:>12}{exact(t):>12.6f}{'0':>12}")

    for i in range(1, N+1):
        k1 = h * g(t,w)
        k2 = h * g(t + h/2, w + k1/2)
        k3 = h * g(t + h/2, w + k2/2)
        t += h
        k4 = h * g(t, w + k3)
        w  += 1/6 * (k1 + 2 * k2 + 2 * k3 + k4)
        print(f"{i:<12} {t:>12.2f} {w:>12.6f}{exact(t):>12.6f}{abs(w - exact(t)):>12.7f}")
    print("\n")
    return
from math import pi, sqrt

def rhs(t, y):
    y = max(y, 0.0)   # guard against negative values in intermediate stages
    return -0.6*pi*(0.1)**2 * sqrt(y) / (pi*(y + 0.1)**2) * sqrt(2*32.1)
'''
def RK42(g, N, a, b, y0):
    w = y0
    h = (b - a) / N
    t = a
    print("RK4\n")
    while t < b - 1e-12:
        k1 = h*g(t, w)
        k2 = h*g(t + h/2, w + k1/2)
        k3 = h*g(t + h/2, w + k2/2)
        k4 = h*g(t + h, w + k3)
        w_new = w + (k1 + 2*k2 + 2*k3 + k4)/6
        if w_new <= 0:                          # crossed empty in this step
            t_empty = t + h * w / (w - w_new)   # linear interpolation
            print(f"Empty at t = {t_empty:.2f} s ({t_empty/60:.2f} min)")
            return t_empty
        t, w = t + h, w_new
    print(f"t = {t:.2f} s, level = {w:.6f} ft")
    return w

RK42(rhs, 30, 0, 600, 8)       # (a) h = 20 s, level after 10 min
RK42(rhs, 300, 0, 6000, 8)     # (b) h = 20 s, time to empty
'''
import matplotlib.pyplot as plt

def RK45(g, a, b, y0, q_min, q_max, h_max, h_min, tol):
    t, w = a, y0
    h = h_max

    # live plot setup
    ts, ws = [t], [w]
    w0, dif = [exact(t)], [0]
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    print("RK45\n")
    print(f"{'t':>12} {'w':>14}{'error':>12} {'h':>10}")
    print(f"{t:>12.4f} {w:>14.8f}{0.0:>12.2e} {h:>10.4f}")

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
            ex = exact(t)
            w += 25*k1/216 + 1408*k3/2565 + 2197*k4/4104 - k5/5
            diff = abs(ex - w)
            print(f"{t:>12.4f} {w:>14.8f}{R:>12.2e} {h:>10.4f}")

            # update the plots with the new accepted point
            ts.append(t); ws.append(w); w0.append(ex); dif.append(diff)

            ax1.clear()
            ax1.plot(ts, ws, 'o-', label='w')
            ax1.plot(ts, w0, '--', color='red', label='w0 (exact)')
            ax1.set_ylabel("w")
            ax1.set_xlim(a, b)
            ax1.legend()

            ax2.clear()
            ax2.plot(ts, dif, color='green', label='error')
            ax2.set_xlabel("t")
            ax2.set_ylabel("|exact - w|")
            ax2.set_xlim(a, b)
            ax2.legend()

            plt.pause(0.05)

        delta = 0.84 * (tol / R) ** 0.25 if R > 0 else q_max
        h *= min(max(delta, q_min), q_max)
        h = min(h, h_max)

        if h < h_min and t < b:
            print("Can't reach b: minimum h exceeded")
            plt.ioff()
            return None

    print()
    plt.ioff()
    plt.show()
    return w
def f(t,y):
    return (t+2*t**3)*y**3 - t*y
def exact(t):
    return (3+2*t**2 + 6*exp(t**2))**(-0.5)
RK45(f, 0, 2, 1/3, 0.1, 4, 0.25, 0.01, 10**(-5))