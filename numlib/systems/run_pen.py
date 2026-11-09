import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
from numlib.ode import rk4
from numlib.ode import euler
from numlib.systems.double_pendulum import DoublePendulum
from math import pi
rng = np.random.default_rng(seed = 42)

def main(t_end=20, n=4000, fps=60):
    p = DoublePendulum()
    st0 = [0, 0,4, 0]
    st1 = [0, 0, 4 + 0.1 * (rng.random()-0.5), 0]
    st2 = [0,0,4 +0.1 * (rng.random()-0.5), 0]
    ts, st = rk4(p.eqm, 0, st0, t_end, n)
    ts1, st_1 = rk4(p.eqm, 0, st1, t_end, n)
    ts2, st_2 = rk4(p.eqm, 0, st2, t_end, n)
    h = ts[1] - ts[0]

    KE = np.array([p.ke(s) for s in st])
    KE1= np.array([p.ke(s) for s in st_1])
    KE2 = np.array([p.ke(s) for s in st_2])
    PE = np.array([p.pe(s) for s in st])
    PE1 = np.array([p.pe(s) for s in st_1])
    PE2 = np.array([p.pe(s) for s in st_2])
    TE = KE + PE
    TE1 = KE1 + PE1
    TE2 = KE2 + PE2
    pos =np.array([p.jt(s) for s in st])      
    pos1 = np.array([p.jt(s) for s in st_1])      
    pos2 = np.array([p.jt(s) for s in st_2])      
    xj, yj, xt, yt = pos.T
    xj_1, yj_1, xt_1, yt_1 = pos1.T
    xj_2, yj_2, xt_2, yt_2 = pos2.T

    
    fig = plt.figure(figsize=(11, 6))
    gs = GridSpec(3, 2, width_ratios=[2, 1], figure=fig)
    ax_p = fig.add_subplot(gs[:, 0])
    ax_k = fig.add_subplot(gs[0, 1])
    ax_u = fig.add_subplot(gs[1, 1], sharex=ax_k)
    ax_e = fig.add_subplot(gs[2, 1], sharex=ax_k)

    R = (p.l1 + p.l2) * 1.1
    ax_p.set_xlim(-R, R)
    ax_p.set_ylim(-R, R)
    ax_p.set_aspect("equal")
    ax_p.grid(alpha=0.3)
    rods, = ax_p.plot([], [], "o-", lw=3, color="C1")
    trail, = ax_p.plot([], [], "-", lw=1, color="C1", alpha=0.6)
    rods1, = ax_p.plot([], [], "o-", lw=3, color="C2")
    trail1, = ax_p.plot([], [], "-", lw=1, color="C2", alpha=0.6)
    rods2, = ax_p.plot([], [], "o-", lw=3, color="C3")
    trail2, = ax_p.plot([], [], "-", lw=1, color="C3", alpha=0.6)
    clock = ax_p.text(0.02, 0.95, "", transform=ax_p.transAxes)

    ax_k.set_xlim(ts[0], ts[-1])
    energy = []
    for ax, y, label, c in [(ax_k, [KE, KE1, KE2], "K", ["C1", "C2", "C3"]), (ax_u, [PE,PE1,PE2], "U", ["C1", "C2", "C3"]),
                            (ax_e, [TE,TE1,TE2], "E = K + U", ["C1", "C2", "C3"])]:
        ax.plot(ts, y[0], color=c[0], alpha=0.25)      
        ax.plot(ts, y[1], color=c[1], alpha=0.25)      
        ax.plot(ts, y[2], color=c[2], alpha=0.25)      
        line, = ax.plot([], [], color=c[0])         
        line1, = ax.plot([], [], color=c[1])
        line2, = ax.plot([], [], color=c[2])
        dot, = ax.plot([], [], "o", color=c[0])
        dot1, = ax.plot([], [], "o", color=c[1])
        dot2, = ax.plot([], [], "o", color=c[2])
        ax.set_ylabel(label)
        lo = min(y[0].min(), y[1].min(), y[2].min())
        hi = max(y[0].max(), y[1].max(), y[2].max())
        pad = 0.05 * (hi - lo) + 1e-9
        ax.set_ylim(lo - pad, hi + pad)
        ax.grid(alpha=0.3)
        energy.append((line, dot, y[0]))
        energy.append((line1, dot1, y[1]))
        energy.append((line2, dot2, y[2]))
    ax_e.set_xlabel("t (s)")
    plt.setp(ax_k.get_xticklabels(), visible=False)
    plt.setp(ax_u.get_xticklabels(), visible=False)
    fig.tight_layout()

    def update(i):
        rods.set_data([0, xj[i], xt[i]], [0, yj[i], yt[i]])
        trail.set_data(xt[:i + 1], yt[:i + 1])
        rods1.set_data([0, xj_1[i], xt_1[i]], [0, yj_1[i], yt_1[i]])
        trail1.set_data(xt_1[:i + 1], yt_1[:i + 1])
        rods2.set_data([0, xj_2[i], xt_2[i]], [0, yj_2[i], yt_2[i]])
        trail2.set_data(xt_2[:i + 1], yt_2[:i + 1])
        clock.set_text(f"t = {ts[i]:.2f} s")
        for line, dot, y in energy:
            line.set_data(ts[:i + 1], y[:i + 1])
            dot.set_data([ts[i]], [y[i]])
        return (rods, trail, rods1, trail1, rods2, trail2, clock, *[a for m in energy for a in m[:2]])

    step = max(1, round(1 / (fps * h)))        
    ani = FuncAnimation(fig, update, frames=range(0, len(ts), step),
                        interval=1000 / fps, blit=True)
    ani.save("pendulum_rk4.gif", writer="pillow", fps=60)
    plt.show()
    return ani
def main_euler(t_end=20, n=4000, fps=60):
    p = DoublePendulum()
    st0 = [0, 0,4, 0]
    st1 = [0, 0, 4 + 0.1 * (rng.random()-0.5), 0]
    st2 = [0,0,4 +0.1 * (rng.random()-0.5), 0]
    ts, st = euler(p.eqm, n, 0, t_end, st0)
    ts1, st_1 = euler(p.eqm, n, 0, t_end, st1)
    ts2, st_2 = euler(p.eqm, n, 0, t_end, st2)
    h = ts[1] - ts[0]

    KE = np.array([p.ke(s) for s in st])
    KE1= np.array([p.ke(s) for s in st_1])
    KE2 = np.array([p.ke(s) for s in st_2])
    PE = np.array([p.pe(s) for s in st])
    PE1 = np.array([p.pe(s) for s in st_1])
    PE2 = np.array([p.pe(s) for s in st_2])
    TE = KE + PE
    TE1 = KE1 + PE1
    TE2 = KE2 + PE2
    pos =np.array([p.jt(s) for s in st])      
    pos1 = np.array([p.jt(s) for s in st_1])      
    pos2 = np.array([p.jt(s) for s in st_2])      
    xj, yj, xt, yt = pos.T
    xj_1, yj_1, xt_1, yt_1 = pos1.T
    xj_2, yj_2, xt_2, yt_2 = pos2.T

    
    fig = plt.figure(figsize=(11, 6))
    gs = GridSpec(3, 2, width_ratios=[2, 1], figure=fig)
    ax_p = fig.add_subplot(gs[:, 0])
    ax_k = fig.add_subplot(gs[0, 1])
    ax_u = fig.add_subplot(gs[1, 1], sharex=ax_k)
    ax_e = fig.add_subplot(gs[2, 1], sharex=ax_k)

    R = (p.l1 + p.l2) * 1.1
    ax_p.set_xlim(-R, R)
    ax_p.set_ylim(-R, R)
    ax_p.set_aspect("equal")
    ax_p.grid(alpha=0.3)
    rods, = ax_p.plot([], [], "o-", lw=3, color="C1")
    trail, = ax_p.plot([], [], "-", lw=1, color="C1", alpha=0.6)
    rods1, = ax_p.plot([], [], "o-", lw=3, color="C2")
    trail1, = ax_p.plot([], [], "-", lw=1, color="C2", alpha=0.6)
    rods2, = ax_p.plot([], [], "o-", lw=3, color="C3")
    trail2, = ax_p.plot([], [], "-", lw=1, color="C3", alpha=0.6)
    clock = ax_p.text(0.02, 0.95, "", transform=ax_p.transAxes)

    ax_k.set_xlim(ts[0], ts[-1])
    energy = []
    for ax, y, label, c in [(ax_k, [KE, KE1, KE2], "K", ["C1", "C2", "C3"]), (ax_u, [PE,PE1,PE2], "U", ["C1", "C2", "C3"]),
                            (ax_e, [TE,TE1,TE2], "E = K + U", ["C1", "C2", "C3"])]:
        ax.plot(ts, y[0], color=c[0], alpha=0.25)      
        ax.plot(ts, y[1], color=c[1], alpha=0.25)      
        ax.plot(ts, y[2], color=c[2], alpha=0.25)      
        line, = ax.plot([], [], color=c[0])         
        line1, = ax.plot([], [], color=c[1])
        line2, = ax.plot([], [], color=c[2])
        dot, = ax.plot([], [], "o", color=c[0])
        dot1, = ax.plot([], [], "o", color=c[1])
        dot2, = ax.plot([], [], "o", color=c[2])
        ax.set_ylabel(label)
        lo = min(y[0].min(), y[1].min(), y[2].min())
        hi = max(y[0].max(), y[1].max(), y[2].max())
        pad = 0.05 * (hi - lo) + 1e-9
        ax.set_ylim(lo - pad, hi + pad)
        ax.grid(alpha=0.3)
        energy.append((line, dot, y[0]))
        energy.append((line1, dot1, y[1]))
        energy.append((line2, dot2, y[2]))
    ax_e.set_xlabel("t (s)")
    plt.setp(ax_k.get_xticklabels(), visible=False)
    plt.setp(ax_u.get_xticklabels(), visible=False)
    fig.tight_layout()

    def update(i):
        rods.set_data([0, xj[i], xt[i]], [0, yj[i], yt[i]])
        trail.set_data(xt[:i + 1], yt[:i + 1])
        rods1.set_data([0, xj_1[i], xt_1[i]], [0, yj_1[i], yt_1[i]])
        trail1.set_data(xt_1[:i + 1], yt_1[:i + 1])
        rods2.set_data([0, xj_2[i], xt_2[i]], [0, yj_2[i], yt_2[i]])
        trail2.set_data(xt_2[:i + 1], yt_2[:i + 1])
        clock.set_text(f"t = {ts[i]:.2f} s")
        for line, dot, y in energy:
            line.set_data(ts[:i + 1], y[:i + 1])
            dot.set_data([ts[i]], [y[i]])
        return (rods, trail, rods1, trail1, rods2, trail2, clock, *[a for m in energy for a in m[:2]])

    step = max(1, round(1 / (fps * h)))        
    ani = FuncAnimation(fig, update, frames=range(0, len(ts), step),
                        interval=1000 / fps, blit=True)
    ani.save("pendulum_euler.gif", writer="pillow", fps=60)
    plt.show()
    return ani
def main_euler_vs_rk4(t_end=20, n=4000, fps=60):
    p = DoublePendulum()
    st0 = [0, 0,4, 0]
    ts, st = euler(p.eqm, n, 0, t_end, st0)
    ts1, st_1 = rk4(p.eqm, 0, st0, t_end, n)
    h = ts[1] - ts[0]

    KE = np.array([p.ke(s) for s in st])
    KE1= np.array([p.ke(s) for s in st_1])
    PE = np.array([p.pe(s) for s in st])
    PE1 = np.array([p.pe(s) for s in st_1])
    TE = KE + PE
    TE1 = KE1 + PE1
    pos =np.array([p.jt(s) for s in st])      
    pos1 = np.array([p.jt(s) for s in st_1])            
    xj, yj, xt, yt = pos.T
    xj_1, yj_1, xt_1, yt_1 = pos1.T

    
    fig = plt.figure(figsize=(11, 6))
    gs = GridSpec(3, 2, width_ratios=[2, 1], figure=fig)
    ax_p = fig.add_subplot(gs[:, 0])
    ax_k = fig.add_subplot(gs[0, 1])
    ax_u = fig.add_subplot(gs[1, 1], sharex=ax_k)
    ax_e = fig.add_subplot(gs[2, 1], sharex=ax_k)

    R = (p.l1 + p.l2) * 1.1
    ax_p.set_xlim(-R, R)
    ax_p.set_ylim(-R, R)
    ax_p.set_aspect("equal")
    ax_p.grid(alpha=0.3)
    rods, = ax_p.plot([], [], "o-", lw=3, color="C1")
    trail, = ax_p.plot([], [], "-", lw=1, color="C1", alpha=0.6)
    rods1, = ax_p.plot([], [], "o-", lw=3, color="C2")
    trail1, = ax_p.plot([], [], "-", lw=1, color="C2", alpha=0.6)
    clock = ax_p.text(0.02, 0.95, "", transform=ax_p.transAxes)

    ax_k.set_xlim(ts[0], ts[-1])
    energy = []
    for ax, y, label, c in [(ax_k, [KE, KE1], "K", ["C1", "C2"]), (ax_u, [PE,PE1], "U", ["C1", "C2"]),
                            (ax_e, [TE,TE1], "E = K + U", ["C1", "C2"])]:
        ax.plot(ts, y[0], color=c[0], alpha=0.25)      
        ax.plot(ts, y[1], color=c[1], alpha=0.25)          
        line, = ax.plot([], [], color=c[0])         
        line1, = ax.plot([], [], color=c[1])
        dot, = ax.plot([], [], "o", color=c[0])
        dot1, = ax.plot([], [], "o", color=c[1])
        ax.set_ylabel(label)
        lo = min(y[0].min(), y[1].min())
        hi = max(y[0].max(), y[1].max())
        pad = 0.05 * (hi - lo) + 1e-9
        ax.set_ylim(lo - pad, hi + pad)
        ax.grid(alpha=0.3)
        energy.append((line, dot, y[0]))
        energy.append((line1, dot1, y[1]))
    ax_e.set_xlabel("t (s)")
    plt.setp(ax_k.get_xticklabels(), visible=False)
    plt.setp(ax_u.get_xticklabels(), visible=False)
    fig.tight_layout()

    def update(i):
        rods.set_data([0, xj[i], xt[i]], [0, yj[i], yt[i]])
        trail.set_data(xt[:i + 1], yt[:i + 1])
        rods1.set_data([0, xj_1[i], xt_1[i]], [0, yj_1[i], yt_1[i]])
        trail1.set_data(xt_1[:i + 1], yt_1[:i + 1])
        clock.set_text(f"t = {ts[i]:.2f} s")
        for line, dot, y in energy:
            line.set_data(ts[:i + 1], y[:i + 1])
            dot.set_data([ts[i]], [y[i]])
        return (rods, trail, rods1, trail1, clock, *[a for m in energy for a in m[:1]])

    step = max(1, round(1 / (fps * h)))        
    ani = FuncAnimation(fig, update, frames=range(0, len(ts), step),
                        interval=1000 / fps, blit=True)
    ani.save("pendulum_euler_vs_rk4.gif", writer="pillow", fps=60)
    plt.show()
    return ani


if __name__ == "__main__":
    main_euler_vs_rk4()
