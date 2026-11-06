"""Black-ink line figures for every space. Outputs figs/<id>.svg and figs/<id>.pdf."""
import os, re, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc, Polygon, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D  # noqa

plt.rcParams.update({"mathtext.fontset": "cm", "font.family": "serif", "font.serif": ["DejaVu Serif"],
                     "font.size": 11, "lines.linewidth": 1.0, "svg.fonttype": "path",
                     "lines.solid_capstyle": "round"})
K = "black"; LW = 1.0; OUT = "figs"; os.makedirs(OUT, exist_ok=True)
FIG = {}
def fig(fn): FIG[fn.__name__.removeprefix("f_")] = fn; return fn

# ---------- helpers
def new(w=3.4, h=2.4, n=1):
    f, axs = plt.subplots(1, n, figsize=(w, h))
    axs = np.atleast_1d(axs)
    for a in axs: a.set_aspect("equal"); a.axis("off")
    return f, (axs if n > 1 else axs[0])
def new3d(w=3.4, h=2.6, elev=25, azim=-60, extra2d=False):
    f = plt.figure(figsize=(w, h))
    if extra2d:
        a = f.add_subplot(1, 2, 1, projection="3d"); b = f.add_subplot(1, 2, 2); b.set_aspect("equal"); b.axis("off")
    else:
        a = f.add_subplot(111, projection="3d"); b = None
    a.view_init(elev, azim); a.set_axis_off(); a.set_box_aspect((1, 1, 1))
    try: a.set_proj_type("ortho")
    except Exception: pass
    return f, a, b
def surf(a, X, Y, Z, lw=0.35, lim=None, zoom=1.45):
    a.plot_surface(X, Y, Z, color="white", edgecolor=K, linewidth=lw, shade=False, antialiased=True)
    rng = []
    for s, c in (("x", X), ("y", Y), ("z", Z)):
        lo, hi = c.min(), c.max(); getattr(a, f"set_{s}lim")(lo, hi); rng.append(hi - lo)
    a.set_box_aspect(tuple(rng), zoom=zoom)
def line(a, P, **kw):
    P = np.asarray(P); a.plot(P[:, 0], P[:, 1], color=K, lw=kw.pop("lw", LW), **kw)
def dot(a, p, open_=False, s=3.2, label=None, off=(0.08, 0.08), **kw):
    a.plot([p[0]], [p[1]], "o", ms=s, mfc="white" if open_ else K, mec=K, mew=0.9, zorder=5)
    if label: a.text(p[0] + off[0], p[1] + off[1], label, **kw)
def arrowhead(a, p, d, size=0.09, n=1):
    d = np.asarray(d, float); d /= np.linalg.norm(d); nrm = np.array([-d[1], d[0]])
    for k in range(n):
        tip = np.asarray(p) + d * size * 0.75 * (k - (n - 1) / 2)
        a.plot(*np.array([tip - size * d + 0.6 * size * nrm, tip, tip - size * d - 0.6 * size * nrm]).T, color=K, lw=LW)
def edge(a, p, q, n=1, rev=False, label=None, lo=0.16, size=0.09, lw=LW, ls="-"):
    p, q = np.asarray(p, float), np.asarray(q, float)
    a.plot([p[0], q[0]], [p[1], q[1]], color=K, lw=lw, ls=ls)
    if n: arrowhead(a, (p + q) / 2, (p - q) if rev else (q - p), size, n)
    if label:
        d = q - p; nrm = np.array([d[1], -d[0]]) / np.linalg.norm(d); m = (p + q) / 2 + lo * nrm
        a.text(*m, label, ha="center", va="center")
def word_polygon(a, word, r=1.0, rot=None, lo=0.2, size=0.09):
    """word: list of (label, exponent, nheads)."""
    n = len(word); rot = np.pi / 2 + np.pi / n if rot is None else rot
    V = [r * np.array([np.cos(rot - 2 * np.pi * i / n), np.sin(rot - 2 * np.pi * i / n)]) for i in range(n + 1)]
    for i, (lab, e, h) in enumerate(word):
        edge(a, V[i], V[i + 1], n=h, rev=(e < 0), size=size)
        m = (V[i] + V[i + 1]) / 2; m = m * (1 + lo / np.linalg.norm(m))
        a.text(*m, lab, ha="center", va="center")
    a.set_xlim(-r - .45, r + .45); a.set_ylim(-r - .45, r + .45)
def circ(a, c, r, **kw):
    a.add_patch(Circle(c, r, fill=False, ec=K, lw=kw.pop("lw", LW), **kw))
def arc(a, c, r, t1, t2, **kw):
    a.add_patch(Arc(c, 2 * r, 2 * r, theta1=t1, theta2=t2, ec=K, lw=kw.pop("lw", LW), **kw))
def lim(a, x0, x1, y0, y1): a.set_xlim(x0, x1); a.set_ylim(y0, y1)
def proj(P, elev=20, azim=-60):
    """Orthographic projection: returns (x2d, y2d, depth)."""
    P = np.asarray(P, float); e, z = np.radians(elev), np.radians(azim)
    Rz = np.array([[np.cos(z), -np.sin(z), 0], [np.sin(z), np.cos(z), 0], [0, 0, 1]])
    Q = P @ Rz.T
    x, y, d = Q[:, 1], Q[:, 2] * np.cos(e) - Q[:, 0] * np.sin(e), Q[:, 0] * np.cos(e) + Q[:, 2] * np.sin(e)
    return x, y, d
def knot_draw(a, curves, gap=0.11, lw=1.3, closed=True):
    """curves: list of (N,3) arrays in the drawing plane (x,y) with height z; breaks under-strands at crossings."""
    segs = []
    for ci, C in enumerate(curves):
        C = np.asarray(C); m = len(C) - (0 if closed else 1)
        for i in range(m):
            segs.append((ci, i, C[i], C[(i + 1) % len(C)]))
    hide = [np.zeros(len(C), bool) for C in curves]
    P = [np.asarray(C) for C in curves]
    for s in range(len(segs)):
        ci, i, p1, p2 = segs[s]
        for t in range(s + 2, len(segs)):
            cj, j, q1, q2 = segs[t]
            if ci == cj and (abs(i - j) <= 1 or abs(i - j) >= len(P[ci]) - 1): continue
            A = np.array([[p2[0] - p1[0], q1[0] - q2[0]], [p2[1] - p1[1], q1[1] - q2[1]]])
            if abs(np.linalg.det(A)) < 1e-12: continue
            u, v = np.linalg.solve(A, [q1[0] - p1[0], q1[1] - p1[1]])
            if 0 <= u <= 1 and 0 <= v <= 1:
                X = p1[:2] + u * (p2[:2] - p1[:2])
                z1 = p1[2] + u * (p2[2] - p1[2]); z2 = q1[2] + v * (q2[2] - q1[2])
                cu = ci if z1 < z2 else cj
                d = np.linalg.norm(P[cu][:, :2] - X, axis=1); hide[cu] |= d < gap
    for C, h in zip(P, hide):
        C2 = np.vstack([C, C[:1]]) if closed else C; h2 = np.append(h, h[:1]) if closed else h
        run = []
        for k in range(len(C2)):
            if not h2[k]: run.append(C2[k])
            else:
                if len(run) > 1: line(a, np.array(run)[:, :2], lw=lw)
                run = []
        if len(run) > 1: line(a, np.array(run)[:, :2], lw=lw)
def torus_xyz(R=2, r=0.8, n=(48, 24)):
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, n[0]), np.linspace(0, 2 * np.pi, n[1]))
    return (R + r * np.cos(v)) * np.cos(u), (R + r * np.cos(v)) * np.sin(u), r * np.sin(v)
def sphere_xyz(n=(36, 18), r=1):
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, n[0]), np.linspace(0, np.pi, n[1]))
    return r * np.cos(u) * np.sin(v), r * np.sin(u) * np.sin(v), r * np.cos(v)
def ellipse_back(a, c, rx, ry, front=True):
    t = np.linspace(np.pi, 2 * np.pi, 60); line(a, np.c_[c[0] + rx * np.cos(t), c[1] + ry * np.sin(t)])
    t = np.linspace(0, np.pi, 60); line(a, np.c_[c[0] + rx * np.cos(t), c[1] + ry * np.sin(t)], ls=(0, (3, 2)), lw=0.8)
def sphere2d(a, c=(0, 0), r=1, label=None):
    circ(a, c, r); ellipse_back(a, c, r, r * 0.3)
    if label: a.text(c[0] + r * 0.75, c[1] + r * 0.85, label)

# ---------- Basic
@fig
def f_point():
    f, a = new(2.4, 1.4); dot(a, (0, 0), s=5, label=r"$*$", off=(0.12, 0.05)); lim(a, -1, 1, -.5, .5); return f
@fig
def f_rn():
    f, a = new(3.0, 2.4)
    edge(a, (-1.4, 0), (1.5, 0), n=0); edge(a, (0, -1.1), (0, 1.2), n=0)
    arrowhead(a, (1.5, 0), (1, 0), .08); arrowhead(a, (0, 1.2), (0, 1), .08)
    for p in [(1, .7), (-1.1, .5), (.6, -.8), (-.7, -.75), (1.2, -.3), (-.4, .95)]:
        p = np.array(p); dot(a, p, s=2.6); q = p * 0.35
        FA = FancyArrowPatch(p * 0.92, q, arrowstyle="-|>", mutation_scale=7, color=K, lw=0.8, ls=(0, (3, 2))); a.add_patch(FA)
    a.text(1.35, 1.0, r"$\mathbb{R}^n$"); a.text(.6, .25, r"$H(x,t)=(1-t)x$", fontsize=9)
    lim(a, -1.6, 1.8, -1.2, 1.3); return f
@fig
def f_disk():
    f, a = new(2.8, 2.4); circ(a, (0, 0), 1, lw=1.3)
    for t in np.linspace(0, 2 * np.pi, 9)[:-1]:
        d = np.array([np.cos(t), np.sin(t)]); a.add_patch(FancyArrowPatch(d * .92, d * .25, arrowstyle="-|>", mutation_scale=7, color=K, lw=.7))
    dot(a, (0, 0), s=2.5); a.text(.75, .85, r"$S^{n-1}$"); a.text(-.25, -.3, r"$D^n$")
    lim(a, -1.3, 1.5, -1.2, 1.2); return f
@fig
def f_circle():
    f = plt.figure(figsize=(3.0, 3.0)); a = f.add_subplot(111); a.set_aspect("equal"); a.axis("off")
    t = np.linspace(0, 3 * 2 * np.pi, 600); el, az = 18, -55
    x, y, d = proj(np.c_[np.cos(t), np.sin(t), 0.35 * t / (2 * np.pi)], el, az)
    knot_draw(a, [np.c_[x, y, d]], gap=0.06, lw=1.1, closed=False)
    tb = np.linspace(0, 2 * np.pi, 200); bx, by, _ = proj(np.c_[np.cos(tb), np.sin(tb), -0.9 + 0 * tb], el, az)
    line(a, np.c_[bx, by], lw=1.2)
    for k in range(4):
        px, py, _ = proj([[1, 0, 0.35 * k], [1, 0, -0.9]], el, az)
        dot(a, (px[0], py[0]), s=2.4)
    px, py, _ = proj([[1, 0, 1.2], [1, 0, -0.9]], el, az); line(a, np.c_[px, py], ls=(0, (2, 2)), lw=.7)
    dot(a, (px[1], py[1]), s=3)
    a.text(px[1] + .08, py[1] - .22, r"$1$")
    a.text(-1.55, .75, r"$\mathbb{R}$"); a.text(-1.55, -1.05, r"$S^1$")
    a.add_patch(FancyArrowPatch((-1.45, .55), (-1.45, -.75), arrowstyle="-|>", mutation_scale=8, color=K, lw=.8))
    a.text(-1.35, -.15, r"$p$", fontsize=10)
    a.autoscale(); return f
@fig
def f_sphere():
    f, a, _ = new3d(2.8, 2.8, 22, -60); X, Y, Z = sphere_xyz((20, 11)); surf(a, X, Y, Z, lw=.35, zoom=1.05)
    a.text(0, 0, 1.25, r"$N$", ha="center"); a.text(0, 0, -1.4, r"$S$", ha="center")
    t = np.linspace(0, 2 * np.pi, 100); a.plot(np.cos(t), np.sin(t), 0 * t, color=K, lw=1.3, zorder=10)
    return f
@fig
def f_annulus():
    f, a = new(3.0, 2.6); circ(a, (0, 0), 1.2, lw=1.2); circ(a, (0, 0), .55, lw=1.2); circ(a, (0, 0), .87, ls=(0, (3, 2)), lw=.8)
    for t in np.linspace(0, 2 * np.pi, 9)[:-1]:
        d = np.array([np.cos(t), np.sin(t)])
        a.add_patch(FancyArrowPatch(d * 1.15, d * .93, arrowstyle="-|>", mutation_scale=6, color=K, lw=.7))
        a.add_patch(FancyArrowPatch(d * .6, d * .81, arrowstyle="-|>", mutation_scale=6, color=K, lw=.7))
    a.text(.95, 1.0, r"$S^1\times I$"); lim(a, -1.4, 1.8, -1.35, 1.35); return f
@fig
def f_mobius():
    f, a, _ = new3d(3.2, 2.4, 35, -55)
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 60), np.linspace(-.45, .45, 7))
    X = (1 + v * np.cos(u / 2)) * np.cos(u); Y = (1 + v * np.cos(u / 2)) * np.sin(u); Zz = v * np.sin(u / 2)
    surf(a, X, Y, Zz, lw=.35); t = np.linspace(0, 4 * np.pi, 300)
    a.plot((1 + .45 * np.cos(t / 2)) * np.cos(t), (1 + .45 * np.cos(t / 2)) * np.sin(t), .45 * np.sin(t / 2), color=K, lw=1.4)
    return f
@fig
def f_torus():
    f, a, b = new3d(5.2, 2.5, 30, -60, extra2d=True); X, Y, Z = torus_xyz(n=(36, 14)); surf(a, X, Y, Z, lw=.35)
    word_polygon(b, [(r"$a$", 1, 1), (r"$b$", 1, 2), (r"$a$", -1, 1), (r"$b$", -1, 2)], rot=3 * np.pi / 4)
    return f
@fig
def f_ntorus():
    f, a = new(3.0, 2.8); o = np.array([.45, .32])
    S = [np.array(p) for p in [(0, 0), (1.4, 0), (1.4, 1.4), (0, 1.4)]]; B = [s + o for s in S]
    for i in range(4):
        edge(a, S[i], S[(i + 1) % 4], n=(1 if i % 2 == 0 else 2), rev=(i >= 2))
        edge(a, B[i], B[(i + 1) % 4], n=(1 if i % 2 == 0 else 2), rev=(i >= 2), ls=((0, (3, 2)) if i in (0, 3) else "-"), lw=(.8 if i in (0, 3) else LW))
        edge(a, S[i], B[i], n=3, ls=((0, (3, 2)) if i == 0 else "-"), lw=(.8 if i == 0 else LW))
    a.text(.2, -.3, r"opposite faces identified by translation", fontsize=8)
    lim(a, -.3, 2.2, -.45, 2.0); return f
@fig
def f_genusg():
    f, (a, b) = new(5.6, 2.6, 2)
    w = [(r"$a_1$", 1, 1), (r"$b_1$", 1, 2), (r"$a_1$", -1, 1), (r"$b_1$", -1, 2),
         (r"$a_2$", 1, 3), (r"$b_2$", 1, 4), (r"$a_2$", -1, 3), (r"$b_2$", -1, 4)]
    word_polygon(a, w, size=.075)
    t = np.linspace(0, 2 * np.pi, 400); r = 1 + .18 * np.cos(2 * t) - .0 * t
    x = 1.9 * np.cos(t) * (1 - .25 * np.cos(2 * t) ** 2 * 0); y = 1.0 * np.sin(t) * (1 - .35 * np.cos(t) ** 2 * 0)
    x = 2.0 * np.cos(t); y = np.sin(t) * (0.95 - 0.35 * np.cos(t) ** 2 * 0) * (0.8 + 0.25 * np.cos(t) ** 2)
    line(b, np.c_[x, y], lw=1.2)
    for cx in (-.95, .95):
        s = np.linspace(.15 * np.pi, .85 * np.pi, 60); line(b, np.c_[cx + .45 * np.cos(s), -.12 + .22 * np.sin(s)])
        s = np.linspace(1.12 * np.pi, 1.88 * np.pi, 60); line(b, np.c_[cx + .52 * np.cos(s), .2 + .3 * np.sin(s)])
    b.text(1.5, .85, r"$\Sigma_2$"); lim(b, -2.2, 2.2, -1.2, 1.2); return f
@fig
def f_rp2():
    f, (a, b) = new(5.0, 2.4, 2)
    arc(a, (0, 0), 1, 0, 180, lw=1.2); arc(a, (0, 0), 1, 180, 360, lw=1.2)
    arrowhead(a, (0, 1), (-1, 0), .1); arrowhead(a, (0, -1), (1, 0), .1)
    a.text(0, 1.18, r"$a$", ha="center"); a.text(0, -1.38, r"$a$", ha="center")
    dot(a, (1, 0)); dot(a, (-1, 0)); a.text(1.08, .05, r"$x$"); a.text(-1.38, .05, r"$-x$")
    lim(a, -1.5, 1.5, -1.5, 1.4)
    sphere2d(b); p = np.array([.55, .55]); dot(b, p, label=r"$x$"); dot(b, -p, label=r"$-x$", off=(-.1, -.25))
    line(b, np.array([p, -p]), ls=(0, (2, 2)), lw=.7); dot(b, (0, 0), s=2)
    lim(b, -1.4, 1.4, -1.3, 1.3); return f
@fig
def f_klein():
    f, a, b = new3d(5.2, 2.6, 25, -50, extra2d=True)
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 44), np.linspace(0, 2 * np.pi, 18)); r = 2.2
    X = (r + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.cos(u)
    Y = (r + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.sin(u)
    Zz = np.sin(u / 2) * np.sin(v) + np.cos(u / 2) * np.sin(2 * v)
    surf(a, X, Y, Zz, lw=.3)
    word_polygon(b, [(r"$a$", 1, 1), (r"$b$", 1, 2), (r"$a$", 1, 1), (r"$b$", -1, 2)], rot=3 * np.pi / 4)
    return f
@fig
def f_nk():
    f, a = new(2.8, 2.6)
    word_polygon(a, [(r"$a_1$", 1, 1), (r"$a_1$", 1, 1), (r"$a_2$", 1, 2), (r"$a_2$", 1, 2), (r"$a_3$", 1, 3), (r"$a_3$", 1, 3)])
    return f
# ---------- graphs
@fig
def f_fig8():
    f, a = new(3.2, 2.0); circ(a, (-.8, 0), .8, lw=1.2); circ(a, (.8, 0), .8, lw=1.2); dot(a, (0, 0), s=3.5)
    arrowhead(a, (-.8, .8), (-1, 0)); arrowhead(a, (.8, .8), (1, 0), n=2)
    a.text(-.85, .95, r"$a$"); a.text(.75, .95, r"$b$"); lim(a, -1.8, 1.8, -1, 1.2); return f
@fig
def f_rose():
    f, (a, b) = new(5.4, 2.4, 2)
    for k in range(5):
        th = 2 * np.pi * k / 5 + np.pi / 2; t = np.linspace(-np.pi / 2, np.pi / 2, 80)
        loop = np.c_[np.cos(t) * np.cos(t) * np.cos(th + 0.42 * np.sin(t) * 1.0), np.cos(t) * np.cos(t) * np.sin(th + 0.42 * np.sin(t))]
        rr = np.cos(t * 1.0); phi = th + .55 * np.sin(t)
        line(a, np.c_[rr * np.cos(phi) * 1.1, rr * np.sin(phi) * 1.1], lw=1.1)
    dot(a, (0, 0), s=3.5); lim(a, -1.3, 1.3, -1.3, 1.3)
    b.add_patch(Polygon([(-1.6, -1), (1.6, -1), (1.6, 1), (-1.6, 1)], fill=False, ec=K, lw=.6, ls=(0, (3, 2))))
    for i, x in enumerate((-.9, 0, .9)):
        dot(b, (x, 0), open_=True, s=4); circ(b, (x, 0), .45, lw=1.1)
    b.text(1.05, .7, r"$\mathbb{R}^2\setminus 3$ pts", fontsize=9); lim(b, -1.7, 1.7, -1.1, 1.1); return f
@fig
def f_graph():
    f, (a, b) = new(5.2, 2.2, 2)
    P, Q = np.array([-1, 0]), np.array([1, 0]); dot(a, P); dot(a, Q)
    line(a, np.array([P, Q]), lw=2.4)
    for s in (1, -1):
        t = np.linspace(np.pi, 0, 60); line(a, np.c_[np.cos(t), s * .7 * np.sin(t)])
    a.text(-.3, -1.05, r"$V=2,\ E=3$", fontsize=9); lim(a, -1.3, 1.3, -1.2, 1)
    V = [np.array(v) for v in [(0, 1), (-1, -.6), (1, -.6), (0, -.05)]]
    E = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3)]; T = {(0, 3), (1, 3), (2, 3)}
    for e in E: line(b, np.array([V[e[0]], V[e[1]]]), lw=(2.4 if e in T else LW))
    for v in V: dot(b, v)
    b.text(-.75, -1.05, r"$K_4$: tree in bold", fontsize=9); lim(b, -1.3, 1.3, -1.2, 1.2); return f
@fig
def f_infwedge():
    f, a = new(3.0, 2.6)
    for k in range(14):
        th = 2 * np.pi * k / 14; t = np.linspace(-np.pi / 2, np.pi / 2, 60); rr = np.cos(t); phi = th + .2 * np.sin(t)
        line(a, np.c_[rr * np.cos(phi), rr * np.sin(phi)], lw=.9)
    dot(a, (0, 0), s=3.5); a.text(1.0, .9, r"$\cdots$"); lim(a, -1.2, 1.4, -1.15, 1.15); return f
@fig
def f_s1vs2():
    f, (a, b) = new(5.4, 2.2, 2)
    sphere2d(a, (.7, 0), .7); circ(a, (-.6, 0), .6); dot(a, (0, 0), s=3.2)
    a.text(.9, .62, r"$S^2$"); a.text(-.85, .7, r"$S^1$"); lim(a, -1.3, 1.5, -1, 1)
    line(b, np.array([[-2.2, 0], [2.2, 0]])); b.text(-2.3, -.45, r"$\cdots$"); b.text(1.95, -.45, r"$\cdots$")
    for x in (-1.5, -.5, .5, 1.5): sphere2d(b, (x, .32), .3); dot(b, (x, 0), s=2.5)
    b.text(-.5, -.6, r"universal cover", fontsize=9); lim(b, -2.4, 2.4, -1, 1); return f
@fig
def f_moore():
    f, (a, b) = new(4.8, 2.2, 2)
    for k in range(3):
        t1 = 90 + 120 * k; arc(a, (0, 0), 1, t1, t1 + 120, lw=1.2); m = np.radians(t1 + 60)
        arrowhead(a, (np.cos(m), np.sin(m)), (-np.sin(m), np.cos(m))); a.text(1.25 * np.cos(m) - .08, 1.25 * np.sin(m) - .08, r"$a$")
        dot(a, (np.cos(np.radians(t1)), np.sin(np.radians(t1))), s=2.8)
    a.text(-.15, -.1, r"$e^2$"); lim(a, -1.5, 1.5, -1.4, 1.4)
    circ(b, (0, 0), .8, lw=1.2); arrowhead(b, (0, .8), (-1, 0)); b.text(-.05, .95, r"$a$"); dot(b, (0, -.8), s=2.8)
    b.text(-.7, -1.35, r"boundary wraps $3$ times", fontsize=8.5); lim(b, -1.4, 1.4, -1.4, 1.2); return f
# ---------- projective / Lie
@fig
def f_rpn():
    f, (a, b) = new(5.2, 2.2, 2)
    sphere2d(a)
    for p in [(.6, .5), (-.3, .75), (.85, -.2)]:
        p = np.array(p); dot(a, p, s=2.6); dot(a, -p, s=2.6); line(a, np.array([p, -p]), ls=(0, (2, 2)), lw=.6)
    lim(a, -1.3, 1.3, -1.2, 1.2)
    b.text(0, .25, r"$\mathbb{Z}\overset{0}{\longleftarrow}\mathbb{Z}\overset{2}{\longleftarrow}\mathbb{Z}\overset{0}{\longleftarrow}\mathbb{Z}\overset{2}{\longleftarrow}\cdots$", ha="center", fontsize=11)
    b.text(0, -.45, r"$C_0\quad\ \ C_1\quad\ \ C_2\quad\ \ C_3$", ha="center", fontsize=9)
    lim(b, -1.6, 1.6, -1, 1); return f
@fig
def f_so3():
    f, a = new(3.0, 2.6); circ(a, (0, 0), 1, lw=1.2); ellipse_back(a, (0, 0), 1, .3)
    v = np.array([.62, .62]); dot(a, v, label=r"$v$"); dot(a, -v, label=r"$-v$", off=(-.15, -.28))
    a.add_patch(FancyArrowPatch(-v, v, arrowstyle="-|>", mutation_scale=9, color=K, lw=1.1))
    a.text(-1.2, 1.0, r"$|v|=\pi$", fontsize=9); a.text(.3, -1.25, r"$v\sim -v$ on $\partial$", fontsize=9)
    lim(a, -1.4, 1.5, -1.35, 1.2); return f
@fig
def f_un():
    f, a = new(3.4, 2.4); t = np.linspace(0, 2 * np.pi, 200)
    line(a, np.c_[1.4 * np.cos(t), -1 + .35 * np.sin(t)], lw=1.2)
    for k in range(7):
        th = 2 * np.pi * k / 7; x = 1.4 * np.cos(th); y = -1 + .35 * np.sin(th)
        line(a, np.c_[x + .12 * np.cos(t), y + .5 + .5 * np.sin(t)], lw=.8); dot(a, (x, y), s=2.2)
    a.text(1.55, -1.1, r"$S^1$"); a.text(1.45, .35, r"$SU(n)$", fontsize=9)
    a.add_patch(FancyArrowPatch((-1.9, .3), (-1.9, -.8), arrowstyle="-|>", mutation_scale=8, color=K, lw=.8)); a.text(-2.25, -.3, r"$\det$", fontsize=9)
    lim(a, -2.4, 2.2, -1.5, 1.1); return f
@fig
def f_gln():
    f, a = new(3.2, 2.2); t = np.linspace(0, 2 * np.pi, 200)
    line(a, np.c_[-1 + .75 * np.cos(t) + .08 * np.cos(3 * t), .7 * np.sin(t)], lw=1.2)
    line(a, np.c_[1 + .75 * np.cos(t) - .08 * np.cos(2 * t), .7 * np.sin(t)], lw=1.2)
    line(a, np.array([[0, -1], [0, 1]]), ls=(0, (3, 2)), lw=.8)
    a.text(-1.38, -.05, r"$\det>0$", fontsize=9); a.text(.62, -.05, r"$\det<0$", fontsize=9); a.text(.08, .85, r"$\det=0$", fontsize=8)
    lim(a, -1.9, 1.9, -1.1, 1.1); return f
@fig
def f_cpn():
    f, a = new(3.0, 3.0); el, az = 22, -55; curves = []; t = np.linspace(0, 2 * np.pi, 400, endpoint=False)
    for eta, m in ((np.pi / 4, 6),):
        for k in range(m):
            ph = 2 * np.pi * k / m
            z = np.cos(eta) * np.exp(1j * t); w = np.sin(eta) * np.exp(1j * (t + ph))
            x1, x2, x3, x4 = z.real, z.imag, w.real, w.imag
            P = np.c_[x1, x2, x3] / (1 - x4)[:, None]; P = P[np.linalg.norm(P, axis=1) < 6]
            x, y, d = proj(P, el, az); curves.append(np.c_[x, y, d])
    knot_draw(a, curves, gap=.07, lw=1.0)
    a.text(-1.3, -1.9, r"fibres of $S^3\to S^2$, projected", fontsize=8.5); a.autoscale(); return f
@fig
def f_hpn():
    f, a = new(4.4, 1.9); rows = [(r"$\mathbb{RP}^8$", range(9)), (r"$\mathbb{CP}^4$", range(0, 9, 2)), (r"$\mathbb{HP}^2$", range(0, 9, 4))]
    for i, (lab, cells) in enumerate(rows):
        y = -i * .55; a.text(-1.2, y - .08, lab, fontsize=10)
        line(a, np.array([[0, y], [8, y]]), lw=.5)
        for c in cells: dot(a, (c, y), s=4.2)
    for c in range(9): a.text(c - .08, .38, f"${c}$", fontsize=9)
    a.text(3.0, -1.55, r"cells by dimension", fontsize=8.5); lim(a, -1.4, 8.4, -1.7, .7); return f
# ---------- 3-manifolds
@fig
def f_lens():
    f = plt.figure(figsize=(3.2, 2.6)); a = f.add_subplot(111, projection="3d"); a.view_init(42, -60); a.set_axis_off()
    try: a.set_proj_type("ortho")
    except Exception: pass
    X, Y, Z = torus_xyz(2, .8, (40, 16)); a.plot_surface(X, Y, Z, color="white", edgecolor=K, linewidth=.2, shade=False)
    t = np.linspace(0, 2 * np.pi, 600); p, q = 5, 2
    a.plot((2 + .82 * np.cos(p * t)) * np.cos(q * t), (2 + .82 * np.cos(p * t)) * np.sin(q * t), .82 * np.sin(p * t), color=K, lw=1.4, zorder=10)
    for s in "xy": getattr(a, f"set_{s}lim")(-2.3, 2.3)
    a.set_zlim(-2.3, 2.3); a.set_box_aspect((1, 1, 1)); return f
@fig
def f_poincare():
    from scipy.spatial import ConvexHull
    f, a = new(2.8, 2.8); g = (1 + 5 ** .5) / 2; V = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            for s3 in (1, -1): V.append((s1, s2, s3))
            V += [(0, s1 / g, s2 * g), (s1 / g, s2 * g, 0), (s1 * g, 0, s2 / g)]
    V = np.array(V); h = ConvexHull(V); el, az = 20, -35
    x, y, d = proj(V, el, az); view = np.array(proj(np.eye(3), el, az)[2])
    edges = {}
    for simp, eq in zip(h.simplices, h.equations):
        vis = (eq[:3] @ view) > 0
        for i in range(3):
            e = tuple(sorted((simp[i], simp[(i + 1) % 3])))
            edges.setdefault(e, []).append((vis, tuple(np.round(eq[:3], 5))))
    for e, info in edges.items():
        if len(set(n for _, n in info)) < 2: continue  # interior triangulation edge
        vis = any(v for v, _ in info)
        line(a, np.c_[x[list(e)], y[list(e)]], lw=(1.1 if vis else .6), ls=("-" if vis else (0, (2, 2))))
    a.autoscale(); return f
@fig
def f_s1s2():
    f, a = new(3.0, 2.6); sphere2d(a, (0, 0), 1.15); sphere2d(a, (0, 0), .5)
    for t in (30, 150, 270):
        d = np.array([np.cos(np.radians(t)), np.sin(np.radians(t))])
        a.add_patch(FancyArrowPatch(d * .55, d * 1.1, arrowstyle="<|-|>", mutation_scale=7, color=K, lw=.7, ls=(0, (2, 2))))
    a.text(-1.6, -1.4, r"$S^2\times[0,1]$, inner $\sim$ outer", fontsize=8.5); lim(a, -1.7, 1.5, -1.5, 1.35); return f
def circle3(c, r, n, normal_axis="z", N=300):
    t = np.linspace(0, 2 * np.pi, N, endpoint=False)
    if normal_axis == "z": P = np.c_[c[0] + r * np.cos(t), c[1] + r * np.sin(t), c[2] + 0 * t]
    else: P = np.c_[c[0] + r * np.cos(t), c[1] + 0 * t, c[2] + r * np.sin(t)]
    return P
@fig
def f_hopflink():
    f, a = new(3.0, 2.2); t = np.linspace(0, 2 * np.pi, 300, endpoint=False)
    A = np.c_[-.5 + np.cos(t), .8 * np.sin(t), .3 * np.sin(t)]; B = np.c_[.5 + np.cos(t), .8 * np.sin(t), -.3 * np.sin(t)]
    knot_draw(a, [A, B], gap=.12, lw=1.4); lim(a, -1.7, 1.7, -1, 1); return f
@fig
def f_trefoil():
    f, a = new(2.8, 2.8); t = np.linspace(0, 2 * np.pi, 600, endpoint=False)
    C = np.c_[np.sin(t) + 2 * np.sin(2 * t), np.cos(t) - 2 * np.cos(2 * t), -np.sin(3 * t)]
    knot_draw(a, [C], gap=.28, lw=1.5); a.autoscale(); return f
@fig
def f_conf():
    f, a = new(3.4, 2.4); word = [(0, 1), (1, -1), (0, 1), (1, 1)]
    pos = [0., 1., 2.]; strands = [[] for _ in range(3)]; who = [0, 1, 2]; T = 0
    for (i, s) in word:
        tt = np.linspace(0, 1, 40)
        for k in range(3):
            j = who.index(k)
            if j == i: x = i + (1 - np.cos(np.pi * tt)) / 2; z = s * np.sin(np.pi * tt)
            elif j == i + 1: x = i + 1 - (1 - np.cos(np.pi * tt)) / 2; z = -s * np.sin(np.pi * tt)
            else: x = j + 0 * tt; z = 0 * tt
            strands[k].append(np.c_[x, -(T + tt) * .9, z])
        who[i], who[i + 1] = who[i + 1], who[i]; T += 1
    curves = [np.vstack(s) for s in strands]; knot_draw(a, curves, gap=.13, lw=1.4, closed=False)
    for x in range(3): dot(a, (x, 0), s=3); dot(a, (curves[0][-1][0] * 0 + x, -T * .9), s=3)
    a.text(2.35, -.1, r"$t=0$", fontsize=8); a.text(2.35, -T * .9 - .05, r"$t=1$", fontsize=8)
    lim(a, -.4, 3.0, -T * .9 - .3, .3); return f
@fig
def f_horned():
    f, a = new(3.0, 3.2); t = np.linspace(0, 2 * np.pi, 160, endpoint=False)
    def pair(c, s, depth):
        A = np.c_[c[0] + s * (-.22 + .42 * np.cos(t)), c[1] + s * .3 * np.sin(t), np.sin(t)]
        B = np.c_[c[0] + s * (.22 + .42 * np.cos(t)), c[1] + s * .3 * np.sin(t), -np.sin(t)]
        knot_draw(a, [A, B], gap=.1 * s, lw=max(.45, 1.3 * s))
        if depth:
            for sg in (-1, 1):
                cc = np.array([c[0] + sg * .36 * s, c[1] + .62 * s])
                a.plot([c[0] + sg * .36 * s, cc[0]], [c[1] + .3 * s, cc[1] - .14 * s], color=K, lw=max(.4, s))
                pair(cc, s * .5, depth - 1)
    a.plot([-.75, -.75, .75, .75], [-1.5, -.75, -.75, -1.5], color=K, lw=1.2)
    a.plot([-.75, -.35], [-.75, -.35], color=K, lw=1.1); a.plot([.75, .35], [-.75, -.35], color=K, lw=1.1)
    pair(np.array([0., 0.]), 1.6, 3)
    a.text(-1.1, -1.8, r"schematic: clasps nested forever", fontsize=8.5); a.autoscale(); return f
# ---------- classifying spaces
@fig
def f_sinf():
    f, a, _ = new3d(2.8, 2.8, 20, -60); X, Y, Z = sphere_xyz((20, 11)); surf(a, X, Y, Z, lw=.3, zoom=1.05)
    t = np.linspace(0, 2 * np.pi, 100); a.plot(np.cos(t), np.sin(t), 0 * t, color=K, lw=1.6, zorder=10)
    a.scatter([1, -1], [0, 0], [0, 0], color=K, s=22, zorder=11, depthshade=False)
    a.text(1.2, 0, .1, r"$S^0$"); a.text(-.4, -1.5, -.1, r"$S^1$"); a.text(0, 0, 1.2, r"$S^2\subset S^3\subset\cdots$", ha="center", fontsize=9)
    return f
def text_fig(lines, w=4.2, h=1.6, fs=11):
    f, a = new(w, h); n = len(lines)
    for i, s in enumerate(lines): a.text(0, (n - 1) / 2 * .5 - i * .5, s, ha="center", va="center", fontsize=fs)
    lim(a, -2, 2, -n * .35, n * .35); return f
@fig
def f_rpinf():
    return text_fig([r"$\mathbb{Z}/2\ \to\ S^\infty\ \to\ \mathbb{RP}^\infty$",
                     r"$\mathbb{Z}\overset{0}{\longleftarrow}\mathbb{Z}\overset{2}{\longleftarrow}\mathbb{Z}\overset{0}{\longleftarrow}\mathbb{Z}\overset{2}{\longleftarrow}\mathbb{Z}\leftarrow\cdots$"])
@fig
def f_cpinf():
    return text_fig([r"$S^1\ \to\ S^\infty\ \to\ \mathbb{CP}^\infty$",
                     r"$\mathbb{Z}\overset{0}{\longleftarrow}0\leftarrow\mathbb{Z}\overset{0}{\longleftarrow}0\leftarrow\mathbb{Z}\leftarrow\cdots$"])
@fig
def f_dunce():
    f, a = new(2.8, 2.6)
    word_polygon(a, [(r"$a$", 1, 1), (r"$a$", 1, 1), (r"$a$", -1, 1)], rot=np.pi / 2); return f
@fig
def f_hilbert():
    f, a = new(3.4, 2.2); xs = np.arange(1, 11); ys = []
    rng = np.random.default_rng(3)
    for n in xs:
        h = 1.6 / n; line(a, np.array([[n * .3, 0], [n * .3, h]]), lw=1.1); y = h * rng.uniform(.2, .9); ys.append(y)
        a.plot([n * .3 - .04, n * .3 + .04], [h, h], color=K, lw=.8); dot(a, (n * .3, y), s=2.6)
    line(a, np.c_[xs * .3, ys], ls=(0, (2, 2)), lw=.6)
    a.text(3.2, .05, r"$\cdots$"); a.text(.1, -.35, r"$x=(x_1,x_2,\dots),\ x_n\in[0,1/n]$", fontsize=8.5)
    lim(a, 0, 3.6, -.5, 1.8); return f
# ---------- pathological
@fig
def f_hawaii():
    f, a = new(3.0, 2.2)
    for n in range(1, 40): circ(a, (1 / n, 0), 1 / n, lw=(1.1 if n < 8 else .6))
    dot(a, (0, 0), s=3); lim(a, -.2, 2.1, -1.05, 1.05); return f
def sine_pts(x0=.004, n=4000):
    x = np.geomspace(x0, 1, n); return np.c_[x, np.sin(1 / x)]
@fig
def f_warsaw():
    f, a = new(3.2, 2.4); P = sine_pts(); line(a, P, lw=.7); line(a, np.array([[0, -1], [0, 1]]), lw=1.1)
    t = np.linspace(0, 1, 100); x1, y1 = 1, np.sin(1)
    arcx = x1 + (0 - x1) * t; arcy = y1 + (-1 - y1) * t
    path = np.c_[np.r_[1, 1.15, 1.15, 0.0, 0.0][::1], np.r_[y1, y1, -1.6, -1.6, -1]]
    line(a, path, lw=1.1); lim(a, -.2, 1.35, -1.75, 1.15); return f
@fig
def f_sine():
    f, a = new(3.2, 2.0); line(a, sine_pts(), lw=.7); line(a, np.array([[0, -1], [0, 1]]), lw=1.1)
    lim(a, -.2, 1.15, -1.2, 1.2); return f
@fig
def f_comb():
    f, a = new(3.0, 2.2); line(a, np.array([[0, 0], [1, 0]]), lw=1.1); line(a, np.array([[0, 0], [0, 1]]), lw=1.1)
    for n in range(1, 40): line(a, np.array([[1 / n, 0], [1 / n, 1]]), lw=(1.0 if n < 10 else .5))
    dot(a, (0, 1), label=r"$(0,1)$", off=(-.32, .06), fontsize=9); lim(a, -.4, 1.15, -.15, 1.25); return f
@fig
def f_solenoid():
    f, a = new(3.2, 2.8); el, az = 40, -60; R = 1.6
    def core(level, N=4000):
        phi = np.linspace(0, 2 * np.pi * 2 ** level, N); off = np.zeros((N, 2)); r = .55
        for k in range(1, level + 1):
            off += r * np.c_[np.cos(phi / 2 ** k), np.sin(phi / 2 ** k)]; r *= .42
        rr = R + off[:, 0]
        return np.c_[rr * np.cos(phi), rr * np.sin(phi), off[:, 1]]
    curves = []
    for lev, lw in ((0, .6), (2, 1.0)):
        x, y, d = proj(core(lev), el, az); curves.append(np.c_[x, y, d])
    knot_draw(a, curves[1:], gap=.05, lw=1.0)
    t = np.linspace(0, 2 * np.pi, 200)
    for rr in (R - .85, R + .85):
        x, y, _ = proj(np.c_[rr * np.cos(t), rr * np.sin(t), 0 * t], el, az); line(a, np.c_[x, y], lw=.5, ls=(0, (2, 2)))
    a.text(-1.9, -1.7, r"stage 2: winds $4$ times", fontsize=8.5); a.autoscale(); return f
@fig
def f_cantor():
    f, a = new(3.6, 1.8); I = [(0., 1.)]
    for lev in range(6):
        y = -lev * .22
        for (s, e) in I: line(a, np.array([[s, y], [e, y]]), lw=2.2 if lev < 4 else 1.6)
        I = [p for (s, e) in I for p in ((s, s + (e - s) / 3), (e - (e - s) / 3, e))]
    a.text(-.1, .1, r"$0$", fontsize=9); a.text(1.02, .1, r"$1$", fontsize=9); lim(a, -.15, 1.15, -1.3, .3); return f
@fig
def f_longline():
    f, a = new(4.4, 1.3)
    xs = [0, .6, 1.2, 1.8]; labs = [r"$0$", r"$1$", r"$2$", r"$3$"]
    line(a, np.array([[0, 0], [2.3, 0]])); a.text(2.38, -.06, r"$\cdots$")
    line(a, np.array([[2.75, 0], [3.9, 0]])); a.text(3.98, -.06, r"$\cdots$"); line(a, np.array([[4.4, 0], [5.0, 0]])); a.text(5.08, -.06, r"$\cdots$")
    for x, l in zip(xs + [2.85, 3.45, 4.5], labs + [r"$\omega$", r"$\omega{+}1$", r"$\omega\cdot2$"]):
        a.plot([x, x], [-.07, .07], color=K, lw=1); a.text(x - .08, -.35, l, fontsize=9)
    a.text(5.55, -.06, r"$\omega_1$", fontsize=10); lim(a, -.2, 6.0, -.5, .3); return f
@fig
def f_rationals():
    f, a = new(3.6, 2.0); line(a, np.array([[0, 0], [1, 0]]), lw=.8)
    from math import gcd
    for q in range(1, 22):
        for p in range(0, q + 1):
            if gcd(p, q) == 1: a.plot([p / q, p / q], [0, .9 / q], color=K, lw=.6); a.plot([p / q], [.9 / q], "o", ms=1.6 if q > 4 else 2.6, color=K)
    a.text(.02, -.15, r"$p/q$ drawn at height $1/q$", fontsize=8.5); lim(a, -.05, 1.05, -.22, 1.0); return f
@fig
def f_sorgenfrey():
    f, a = new(3.4, 1.8); line(a, np.array([[-.2, 0], [3.2, 0]]), lw=.7)
    for i, (s, e) in enumerate([(0, 1.1), (.6, 1.9), (1.4, 2.2), (2.0, 3.0)]):
        y = .25 + .2 * (i % 2) + .2 * (i // 2 % 2)
        line(a, np.array([[s, y], [e, y]]), lw=1.4); dot(a, (s, y), s=3.6); dot(a, (e, y), open_=True, s=3.6)
    a.text(0, -.3, r"basic open sets $[a,b)$", fontsize=8.5); lim(a, -.3, 3.3, -.45, .9); return f
@fig
def f_twoorigins():
    f, a = new(3.4, 1.4); line(a, np.array([[-1.6, 0], [-.07, 0]]), lw=1.3); line(a, np.array([[.07, 0], [1.6, 0]]), lw=1.3)
    dot(a, (0, .28), s=3.6, label=r"$0_1$", off=(.08, .02)); dot(a, (0, -.28), s=3.6, label=r"$0_2$", off=(.08, -.12))
    dot(a, (0, 0), open_=True, s=3.6); lim(a, -1.7, 1.7, -.55, .55); return f
@fig
def f_pseudocircle():
    f, (a, b) = new(4.6, 2.0, 2)
    P = {"c": (-.7, .7), "d": (.7, .7), "a": (-.7, -.7), "b": (.7, -.7)}
    for u in "ab":
        for v in "cd": line(a, np.array([P[u], P[v]]))
    for k, p in P.items(): dot(a, p, s=4, label=f"${k}$", off=(-.25 if p[0] < 0 else .1, .05))
    a.text(-.9, -1.25, r"Hasse diagram", fontsize=8.5); lim(a, -1.2, 1.2, -1.35, 1.1)
    circ(b, (0, 0), .8, lw=1.1)
    for ang, k in ((135, "c"), (45, "d"), (225, "a"), (315, "b")):
        p = .8 * np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang))]); dot(b, p, s=3, label=f"${k}$", off=tuple(.25 * p / .8 - np.array([.06, .06])))
    b.text(-.7, -1.25, r"order complex $\cong S^1$", fontsize=8.5); lim(b, -1.2, 1.2, -1.35, 1.1); return f
@fig
def f_sierpinski():
    f, a = new(2.8, 1.5); dot(a, (-.6, 0), s=4.5, label=r"$0$", off=(-.05, .1)); dot(a, (.6, 0), s=4.5, label=r"$1$", off=(-.05, .1))
    from matplotlib.patches import Ellipse
    a.add_patch(Ellipse((.6, 0), .7, .55, fill=False, ec=K, lw=.9, ls=(0, (3, 2))))
    a.add_patch(Ellipse((0, 0), 1.95, .95, fill=False, ec=K, lw=.9)); a.text(.75, .3, r"$\{1\}$", fontsize=9)
    lim(a, -1.1, 1.1, -.6, .6); return f
@fig
def f_cofinite():
    f, a = new(3.6, 1.2)
    for n in range(14):
        if n in (2, 5, 6, 10): a.text(n * .25 - .06, -.06, r"$\times$", fontsize=9)
        else: dot(a, (n * .25, 0), s=3)
    a.text(3.55, -.06, r"$\cdots$"); a.text(0, -.38, r"an open set: all but finitely many points", fontsize=8.5)
    lim(a, -.15, 3.9, -.5, .25); return f

def to_svg(path):
    s = open(path).read()
    s = re.sub(r"<\?xml.*?\?>\s*", "", s, flags=re.S); s = re.sub(r"<!DOCTYPE.*?>\s*", "", s, flags=re.S)
    s = re.sub(r"<metadata>.*?</metadata>\s*", "", s, flags=re.S)
    s = re.sub(r'(<svg[^>]*?) width="[^"]*" height="[^"]*"', r"\1", s, count=1)
    s = re.sub(r"\n\s*", "\n", s)
    open(path, "w").write(s)

# ---------- application figures
@fig
def f_app_ab():
    f, a = new(3.6, 2.2)
    dot(a, (0, 0), s=7); a.text(-.13, -.42, r"$\Phi$")
    for s_ in (1, -1):
        t = np.linspace(0, 1, 100); x = -2 + 4 * t; y = s_ * .75 * np.sin(np.pi * t)
        line(a, np.c_[x, y], lw=1.1); arrowhead(a, (0, s_ * .75), (1, 0), .1)
    dot(a, (-2, 0), s=3.5, label=r"source", off=(-.35, -.35), fontsize=8.5); line(a, np.array([[2.15, -1], [2.15, 1]]), lw=1.4)
    a.text(2.25, .75, r"screen", fontsize=8.5); a.text(-.6, 1.0, r"paths differ by one winding", fontsize=8.5)
    lim(a, -2.5, 3.0, -1.1, 1.3); return f
@fig
def f_app_nematic():
    f, a = new(2.8, 2.8)
    for x in np.linspace(-1, 1, 11):
        for y in np.linspace(-1, 1, 11):
            if x * x + y * y < .02: continue
            th = np.arctan2(y, x) / 2; d = .075 * np.array([np.cos(th), np.sin(th)])
            line(a, np.array([[x, y] - d, [x, y] + d]), lw=1.2)
    dot(a, (0, 0), s=3); a.text(-.9, -1.35, r"director angle $=\theta/2$", fontsize=8.5); lim(a, -1.15, 1.15, -1.45, 1.15); return f
@fig
def f_app_toric():
    f, a = new(2.8, 2.8); n = 6
    for i in range(n + 1):
        line(a, np.array([[0, i], [n, i]]), lw=.5); line(a, np.array([[i, 0], [i, n]]), lw=.5)
    edge(a, (0, 0), (n, 0), n=1, lw=.5); edge(a, (0, n), (n, n), n=1, lw=.5); edge(a, (0, 0), (0, n), n=2, lw=.5); edge(a, (n, 0), (n, n), n=2, lw=.5)
    line(a, np.array([[0, 2], [n, 2]]), lw=2.4); line(a, np.array([[4, 0], [4, n]]), lw=2.4)
    t = np.linspace(0, 2 * np.pi, 60); line(a, np.c_[1.5 + .6 * np.cos(t), 4.5 + .6 * np.sin(t)], ls=(0, (2, 2)), lw=.9)
    a.text(.2, -.8, r"bold: wrap the torus; dashed: contractible", fontsize=8); lim(a, -.4, n + .4, -1.1, n + .4); return f
NOTES = ["C", "C$\\sharp$", "D", "E$\\flat$", "E", "F", "F$\\sharp$", "G", "A$\\flat$", "A", "B$\\flat$", "B"]
@fig
def f_app_dyads():
    f, a = new(3.8, 4.2)
    line(a, np.array([[0, 0], [6, 0]]), lw=1.4); line(a, np.array([[0, 12], [6, 12]]), lw=1.4)
    line(a, np.array([[0, 0], [0, 12]]), lw=.9); line(a, np.array([[6, 0], [6, 12]]), lw=.9)
    a.add_patch(FancyArrowPatch((0, 5), (0, 7.2), arrowstyle="-|>", mutation_scale=11, color=K, lw=.9))
    a.add_patch(FancyArrowPatch((6, 7), (6, 4.8), arrowstyle="-|>", mutation_scale=11, color=K, lw=.9))
    line(a, np.array([[0, 6], [6, 6]]), ls=(0, (3, 2)), lw=.6)
    for i in range(13):
        for k in range(6):
            c = k + (0.5 if i % 2 else 0) + 0.25
            p = int(round(c - .25 - i / 2)) % 12; q = (p + i) % 12
            a.text(c, i, NOTES[p] + NOTES[q], ha="center", va="center", fontsize=5.6,
                   bbox=dict(fc="white", ec="none", pad=.4))
    a.text(3, -1.3, r"unisons: the boundary", ha="center", fontsize=8.5); a.text(3, 12.8, r"unisons: the boundary", ha="center", fontsize=8.5)
    a.text(6.25, 6, r"tritones", fontsize=8.5, va="center"); a.text(-1.0, 6, r"interval", fontsize=8, rotation=90, va="center")
    a.text(-.1, -2.5, r"left and right edges glued with a flip", fontsize=8)
    a.set_aspect(0.42); lim(a, -1.2, 7.6, -2.9, 13.4); return f
@fig
def f_app_tonnetz():
    f, a = new(4.0, 2.6)
    rows, cols = 4, 7; P = {}
    for r in range(rows):
        for c in range(cols):
            x = c + .5 * r; y = r * .866; P[(r, c)] = (x, y); pc = (7 * c + 4 * r) % 12
            a.text(x, y, NOTES[pc], ha="center", va="center", fontsize=8,
                   bbox=dict(boxstyle="circle,pad=0.18", fc="white", ec=K, lw=.6))
    for (r, c), (x, y) in P.items():
        for (dr, dc) in ((0, 1), (1, 0), (1, -1)):
            q = (r + dr, c + dc)
            if q in P:
                x2, y2 = P[q]; v = np.array([x2 - x, y2 - y]); u = v / np.linalg.norm(v)
                a.plot([x + .22 * u[0], x2 - .22 * u[0]], [y + .22 * u[1], y2 - .22 * u[1]], color=K, lw=.6, zorder=0)
    a.text(0, -.6, r"right: fifth up;  up-right: major third up;  up-left: minor third down", fontsize=7.5)
    lim(a, -.5, cols + 1.3, -.85, rows * .866); return f
@fig
def f_app_poly():
    f, a = new(2.8, 2.8)
    a.add_patch(Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], fill=False, ec=K, lw=1.0))
    edge(a, (0, 0), (1, 0), n=1, lw=1.0, size=.04); edge(a, (0, 1), (1, 1), n=1, lw=1.0, size=.04)
    edge(a, (0, 0), (0, 1), n=2, lw=1.0, size=.04); edge(a, (1, 0), (1, 1), n=2, lw=1.0, size=.04)
    t = np.linspace(0, 1, 400); x = (2 * t) % 1; y = (3 * t) % 1
    br = np.where(np.abs(np.diff(x)) > .5)[0].tolist() + np.where(np.abs(np.diff(y)) > .5)[0].tolist(); br = sorted(set(br))
    s0 = 0
    for b in br + [len(t) - 1]:
        line(a, np.c_[x[s0:b + 1], y[s0:b + 1]], lw=1.3); s0 = b + 1
    for k in range(2): dot(a, (k / 2, 0), s=3)
    for k in range(3): dot(a, (0, k / 3), s=3)
    a.text(.2, -.16, r"cycle of 2", fontsize=8.5); a.text(-.17, .25, r"cycle of 3", fontsize=8.5, rotation=90)
    lim(a, -.25, 1.1, -.22, 1.08); return f

if __name__ == "__main__":
    import sys
    names = sys.argv[1:] or list(FIG)
    for k in names:
        f = FIG[k]()
        for ext in ("svg", "pdf"):
            f.savefig(f"{OUT}/{k}.{ext}", bbox_inches="tight", pad_inches=0.04, transparent=True)
        plt.close(f); to_svg(f"{OUT}/{k}.svg")
    print(len(names), "figures")

