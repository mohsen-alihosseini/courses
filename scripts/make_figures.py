"""Regenerate the figures made for this site (quantum and math courses).

Run from the project root:  python scripts/make_figures.py
Needs numpy and matplotlib. The site build itself does not run this.
"""
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path("quantum/fundamentals-of-quantum-algorithms/figures")
INK, MUTED, BLUE, ORANGE = "#1d2433", "#5c6370", "#3b5bdb", "#d9480f"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 13,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "svg.fonttype": "none",
})


def grover_success():
    """Success probability sin^2((2t+1) theta) against the iteration count t."""
    n_items = 2**8
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    for s, color, dx in [(1, BLUE, 1.2), (4, ORANGE, -6.5)]:
        theta = np.arcsin(np.sqrt(s / n_items))
        t = np.arange(0, 41)
        p = np.sin((2 * t + 1) * theta) ** 2
        t_star = int(np.floor(np.pi / (4 * theta)))
        ax.plot(t, p, "o-", ms=3.5, lw=1.4, color=color, label=f"s = {s} solution{'s' if s > 1 else ''}")
        ax.plot([t_star], [np.sin((2 * t_star + 1) * theta) ** 2], "o", ms=10,
                mfc="none", mec=color, mew=2)
        ax.annotate(f"t = ⌊π/4θ⌋ = {t_star}", (t_star, 1.0), xytext=(t_star + dx, 1.06),
                    color=color, fontsize=12)
    ax.set_xlabel("number of Grover iterations t")
    ax.set_ylabel("probability of finding a solution")
    ax.set_ylim(0, 1.15)
    ax.set_yticks([0, 0.5, 1])
    ax.set_title(f"N = 2⁸ = {n_items} strings", color=INK, loc="left", fontsize=13)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "grover-success.svg")


def query_counts():
    """Queries needed: classical vs quantum, for Simon's problem and for search."""
    n = np.arange(4, 41)
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    ax.semilogy(n, 2.0 ** (n / 2 - 1) - 1, color=ORANGE, lw=2, label="Simon, classical (lower bound): 2^(n/2−1) − 1")
    ax.semilogy(n, n + 10, color=ORANGE, lw=2, ls="--", label="Simon, quantum: n + 10")
    ax.semilogy(n, 2.0**n, color=BLUE, lw=2, label="Search, classical: N = 2ⁿ")
    ax.semilogy(n, np.pi / 4 * 2.0 ** (n / 2), color=BLUE, lw=2, ls="--", label="Search, Grover: (π/4)√N")
    ax.set_xlabel("input length n (bits)")
    ax.set_ylabel("queries")
    ax.legend(frameon=False, fontsize=11, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "query-counts.svg")


def strip_doctype(path):
    """Matplotlib writes a DOCTYPE line; some hosts reject SVGs that carry one."""
    text = re.sub(r"<!DOCTYPE[^>]*>\s*", "", path.read_text())
    path.write_text(text)


def classical_measurement():
    """A probabilistic state before and after it is observed (basics course, lecture 1)."""
    out = Path("quantum/basics-of-quantum-information/figures")
    fig, axes = plt.subplots(1, 2, figsize=(8, 2.8), sharey=True)
    for ax, probs, title in [(axes[0], [0.75, 0.25], "before: (3/4, 1/4)"),
                             (axes[1], [1.0, 0.0], "after seeing 0: |0⟩")]:
        ax.bar(["0", "1"], probs, color=[BLUE, ORANGE], width=0.55)
        ax.set_ylim(0, 1.05)
        ax.set_yticks([0, 0.5, 1])
        ax.set_title(title, color=INK, fontsize=13, loc="left")
    axes[0].set_ylabel("probability")
    fig.tight_layout()
    fig.savefig(out / "basics-measure-classical.svg")
    strip_doctype(out / "basics-measure-classical.svg")


def label_for(a, b, c):
    """Readable equation label such as 'x₁ − x₂ = 1'."""
    def term(coef, name, first):
        sign = "" if first else (" − " if coef < 0 else " + ")
        if first and coef < 0:
            sign = "−"
        mag = abs(coef)
        return f"{sign}{'' if mag == 1 else mag}{name}"
    return f"{term(a, 'x₁', True)}{term(b, 'x₂', False)} = {c}"


def three_systems():
    """Row picture of 2x2 linear systems: one, none, infinitely many solutions (MML course, ch. 2)."""
    out = Path("math/mathematics-for-machine-learning/figures")
    out.mkdir(parents=True, exist_ok=True)
    x = np.linspace(-1, 4, 50)
    cases = [
        ("one solution", [(1, 1, 3), (1, -1, 1)], (2, 1)),
        ("no solution", [(1, 1, 3), (1, 1, 1)], None),
        ("infinitely many", [(1, 1, 3), (2, 2, 6)], None),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
    for ax, (title, eqs, sol) in zip(axes, cases):
        for (a, b, c), color, ls, lw in zip(eqs, [BLUE, ORANGE], ["-", "--"], [2.5, 2]):
            ax.plot(x, (c - a * x) / b, color=color, ls=ls, lw=lw,
                    label=label_for(a, b, c))
        if sol:
            ax.plot(*sol, "o", color=INK, ms=7)
            ax.annotate(f"({sol[0]}, {sol[1]})", sol, xytext=(8, -14), textcoords="offset points", color=INK)
        ax.set_title(title, color=INK, loc="left", fontsize=13)
        ax.set_xlim(-1, 4); ax.set_ylim(-1, 4)
        ax.set_xlabel("x₁")
        ax.legend(frameon=False, fontsize=10, loc="upper right")
    axes[0].set_ylabel("x₂")
    fig.tight_layout()
    fig.savefig(out / "three-systems.svg")
    strip_doctype(out / "three-systems.svg")

MML = Path("math/mathematics-for-machine-learning/figures")


def unit_balls():
    """Unit balls of the 1-, 2- and max-norm (MML ch. 3)."""
    t = np.linspace(0, 2 * np.pi, 400)
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.1))
    shapes = [
        ("‖x‖₁ = |x₁| + |x₂| = 1", np.array([[1, 0], [0, 1], [-1, 0], [0, -1], [1, 0]]).T),
        ("‖x‖₂ = √(x₁² + x₂²) = 1", np.vstack([np.cos(t), np.sin(t)])),
        ("‖x‖∞ = max(|x₁|, |x₂|) = 1", np.array([[1, 1], [-1, 1], [-1, -1], [1, -1], [1, 1]]).T),
    ]
    for ax, (title, pts) in zip(axes, shapes):
        ax.fill(pts[0], pts[1], color=BLUE, alpha=0.12)
        ax.plot(pts[0], pts[1], color=BLUE, lw=2.2)
        ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
        ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4); ax.set_aspect("equal")
        ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
        ax.set_title(title, color=INK, fontsize=11.5)
    fig.tight_layout()
    fig.savefig(MML / "unit-balls.svg"); strip_doctype(MML / "unit-balls.svg")


def low_rank():
    """Rank-k approximations of a synthetic 'image' via the SVD (MML ch. 4)."""
    n = 120
    yy, xx = np.mgrid[0:n, 0:n] / n
    img = (np.sin(6 * xx) * np.cos(4 * yy) + 0.8 * np.exp(-((xx - 0.6) ** 2 + (yy - 0.35) ** 2) / 0.01)
           + 0.6 * ((xx - 0.3) ** 2 + (yy - 0.7) ** 2 < 0.02) + 0.3 * (xx > yy))
    U, s, Vt = np.linalg.svd(img)
    ks = [1, 3, 10, n]
    fig, axes = plt.subplots(1, 4, figsize=(10, 2.9))
    for ax, k in zip(axes, ks):
        approx = (U[:, :k] * s[:k]) @ Vt[:k]
        ax.imshow(approx, cmap="Blues", vmin=img.min(), vmax=img.max())
        err = np.linalg.norm(img - approx) / np.linalg.norm(img)
        ax.set_title(f"rank {k}" + ("" if k == n else f" · error {err:.0%}") if k != n else f"original (rank {np.linalg.matrix_rank(img)})",
                     color=INK, fontsize=11)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
    fig.tight_layout()
    fig.savefig(MML / "low-rank.svg"); strip_doctype(MML / "low-rank.svg")


def gradient_field():
    """Contours of f(x, y) = x² + 3y² with gradient arrows (MML ch. 5)."""
    xs = np.linspace(-2, 2, 200)
    X, Y = np.meshgrid(xs, xs)
    F = X ** 2 + 3 * Y ** 2
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    ax.contour(X, Y, F, levels=[0.25, 1, 2, 4, 7, 10], colors=MUTED, linewidths=1)
    g = np.linspace(-1.5, 1.5, 7)
    GX, GY = np.meshgrid(g, g)
    ax.quiver(GX, GY, 2 * GX, 6 * GY, color=BLUE, angles="xy", scale_units="xy", scale=14, width=0.006)
    ax.plot(0, 0, "o", color=ORANGE, ms=7)
    ax.set_aspect("equal"); ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title("f(x, y) = x² + 3y²", color=INK, fontsize=12, loc="left")
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
    fig.tight_layout()
    fig.savefig(MML / "gradient-field.svg"); strip_doctype(MML / "gradient-field.svg")


def gaussian_conditional():
    """Bivariate Gaussian, its marginal of x₁ and the conditional p(x₁ | x₂ = 3) (MML ch. 6)."""
    mu = np.array([1.0, 2.0]); S = np.array([[2.0, 1.0], [1.0, 2.0]])
    xs = np.linspace(-3, 5, 300); ys = np.linspace(-2, 6, 300)
    X, Y = np.meshgrid(xs, ys)
    P = np.dstack([X - mu[0], Y - mu[1]])
    Si = np.linalg.inv(S)
    Z = np.exp(-0.5 * np.einsum("...i,ij,...j", P, Si, P))
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.8), gridspec_kw={"width_ratios": [1, 1.25]})
    ax = axes[0]
    ax.contour(X, Y, Z, levels=[0.05, 0.2, 0.45, 0.75], colors=BLUE, linewidths=1.4)
    ax.axhline(3, color=ORANGE, ls="--", lw=1.5)
    ax.text(-2.8, 3.15, "x₂ = 3", color=ORANGE)
    ax.plot(*mu, "o", color=INK, ms=5)
    ax.set_xlabel("x₁"); ax.set_ylabel("x₂"); ax.set_aspect("equal")
    ax.set_title("joint p(x₁, x₂)", color=INK, loc="left", fontsize=12)
    ax = axes[1]
    pdf = lambda x, m, v: np.exp(-(x - m) ** 2 / (2 * v)) / np.sqrt(2 * np.pi * v)
    ax.plot(xs, pdf(xs, 1.0, 2.0), color=BLUE, lw=2, label="marginal p(x₁) = N(1, 2)")
    ax.plot(xs, pdf(xs, 1.5, 1.5), color=ORANGE, lw=2, ls="--", label="conditional p(x₁ | x₂ = 3) = N(1.5, 1.5)")
    ax.set_xlabel("x₁"); ax.set_yticks([]); ax.legend(frameon=False, fontsize=10, loc="upper left")
    ax.set_ylim(0, 0.55)
    fig.tight_layout()
    fig.savefig(MML / "gaussian-conditional.svg"); strip_doctype(MML / "gaussian-conditional.svg")


def convexity():
    """A convex and a non-convex function with a chord (MML ch. 7)."""
    x = np.linspace(-2, 2, 300)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
    f1 = lambda t: 0.5 * t ** 2 + 0.3 * t
    f2 = lambda t: 0.25 * t ** 4 - t ** 2 + 0.3 * t
    for ax, f, title in [(axes[0], f1, "convex: the graph stays below every chord"), (axes[1], f2, "not convex: the graph rises above this chord")]:
        ax.plot(x, f(x), color=BLUE, lw=2.2)
        a, b = (-1.6, 1.5) if f is f1 else (-1.45, 1.35)
        ax.plot([a, b], [f(a), f(b)], color=ORANGE, lw=2, ls="--")
        ax.plot([a, b], [f(a), f(b)], "o", color=ORANGE, ms=6)
        ax.set_title(title, color=INK, loc="left", fontsize=12)
        ax.set_yticks([]); ax.set_xlabel("x")
    fig.tight_layout()
    fig.savefig(MML / "convexity.svg"); strip_doctype(MML / "convexity.svg")



def overfitting():
    """Polynomial fits of increasing degree, and training vs test error (MML ch. 8)."""
    rng = np.random.default_rng(3)
    x = np.linspace(0, 1, 10); y = np.sin(2 * np.pi * x) + 0.25 * rng.standard_normal(10)
    xt = rng.uniform(0, 1, 200); yt = np.sin(2 * np.pi * xt) + 0.25 * rng.standard_normal(200)
    P = np.polynomial.Polynomial
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    ax = axes[0]; xs = np.linspace(0, 1, 300)
    for deg, c, ls in [(1, MUTED, ":"), (3, BLUE, "-"), (9, ORANGE, "--")]:
        ax.plot(xs, P.fit(x, y, deg)(xs), color=c, ls=ls, lw=2, label=f"degree {deg}")
    ax.plot(x, y, "o", color=INK, ms=6)
    ax.set_ylim(-1.8, 1.8); ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.legend(frameon=False, fontsize=10, loc="lower left")
    ax.set_title("10 training points", color=INK, loc="left", fontsize=12)
    ax = axes[1]; degs = range(10)
    rmse = lambda d, a, b: np.sqrt(np.mean((P.fit(x, y, d)(a) - b) ** 2))
    ax.plot(degs, [rmse(d, x, y) for d in degs], "o-", color=BLUE, label="training error")
    ax.plot(degs, [rmse(d, xt, yt) for d in degs], "s--", color=ORANGE, label="test error")
    ax.set_ylim(0, 1.0); ax.set_xlabel("polynomial degree"); ax.set_ylabel("RMSE")
    ax.legend(frameon=False, fontsize=10)
    ax.set_title("more flexible is not always better", color=INK, loc="left", fontsize=12)
    fig.tight_layout()
    fig.savefig(MML / "overfitting.svg"); strip_doctype(MML / "overfitting.svg")


def bayes_regression():
    """Posterior predictive of Bayesian linear regression on four points (MML ch. 9)."""
    X = np.array([[1, 0], [1, 1], [1, 2], [1, 3]], float); y = np.array([1, 3, 2, 5], float)
    S = np.linalg.inv(X.T @ X + np.eye(2)); m = S @ X.T @ y          # prior N(0, I), noise variance 1
    xs = np.linspace(-1, 5, 200); F = np.column_stack([np.ones_like(xs), xs])
    mean = F @ m; sd = np.sqrt(np.einsum("ij,jk,ik->i", F, S, F) + 1)
    rng = np.random.default_rng(1)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.fill_between(xs, mean - 2 * sd, mean + 2 * sd, color=BLUE, alpha=0.12, lw=0, label="±2 std (predictive)")
    for i, th in enumerate(rng.multivariate_normal(m, S, 6)):
        ax.plot(xs, F @ th, color=MUTED, lw=0.9, alpha=0.8, label="posterior samples" if i == 0 else None)
    ax.plot(xs, mean, color=BLUE, lw=2.2, label="posterior mean")
    ax.plot(X[:, 1], y, "o", color=ORANGE, ms=7, zorder=5, label="data")
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_ylim(-4, 11)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    fig.tight_layout()
    fig.savefig(MML / "bayes-regression.svg"); strip_doctype(MML / "bayes-regression.svg")


def pca_figure():
    """Principal axes of 2D data and the projection onto the first one (MML ch. 10)."""
    rng = np.random.default_rng(7)
    X = rng.multivariate_normal([0, 0], [[2.5, 2], [2, 2.5]], 150)
    X = X - X.mean(0)
    lam, U = np.linalg.eigh(np.cov(X.T, bias=True)); lam, U = lam[::-1], U[:, ::-1]
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.2))
    for ax in axes:
        ax.set_aspect("equal"); ax.set_xlim(-5, 5); ax.set_ylim(-4.2, 4.2)
        ax.set_xlabel("x₁"); ax.set_ylabel("x₂")
    ax = axes[0]
    ax.plot(*X.T, "o", color=BLUE, ms=3.5, alpha=0.55)
    for l, u, c, name in [(lam[0], U[:, 0], ORANGE, "PC 1"), (lam[1], U[:, 1], INK, "PC 2")]:
        v = 2 * np.sqrt(l) * u * np.sign(u[0])
        ax.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=c, lw=2.2))
        ax.text(*(v * (1.12 if name == "PC 1" else 1.45)), name, color=c, fontsize=11, ha="center", va="center")
    ax.set_title(f"variance along PC 1: {lam[0] / lam.sum():.0%}", color=INK, loc="left", fontsize=12)
    ax = axes[1]
    u = U[:, 0]; Z = (X @ u)[:, None] * u
    ax.plot([-6 * u[0], 6 * u[0]], [-6 * u[1], 6 * u[1]], color=ORANGE, lw=1.5)
    for a, b in zip(X[:40], Z[:40]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=MUTED, lw=0.8)
    ax.plot(*X[:40].T, "o", color=BLUE, ms=4)
    ax.plot(*Z[:40].T, "o", color=ORANGE, ms=4)
    ax.set_title("project onto PC 1 (40 points shown)", color=INK, loc="left", fontsize=12)
    fig.tight_layout()
    fig.savefig(MML / "pca.svg"); strip_doctype(MML / "pca.svg")


def em_1d(x, mu, var, pi, iters):
    """Plain EM for a 1D Gaussian mixture; returns parameters and log-likelihood history."""
    mu, var, pi = (np.array(a, float) for a in (mu, var, pi)); ll = []
    for _ in range(iters):
        dens = pi * np.exp(-(x[:, None] - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)
        ll.append(np.log(dens.sum(1)).sum())
        r = dens / dens.sum(1, keepdims=True); Nk = r.sum(0)
        mu = (r * x[:, None]).sum(0) / Nk
        var = (r * (x[:, None] - mu) ** 2).sum(0) / Nk
        pi = Nk / len(x)
    return mu, var, pi, ll


def gmm_figure():
    """EM fit of a two-component mixture to 1D data (MML ch. 11)."""
    rng = np.random.default_rng(11)
    x = np.concatenate([rng.normal(-2, 0.6, 120), rng.normal(2, 1.0, 180)])
    mu, var, pi, ll = em_1d(x, [-0.5, 0.5], [4, 4], [0.5, 0.5], 40)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), gridspec_kw={"width_ratios": [1.4, 1]})
    ax = axes[0]; xs = np.linspace(-5, 6, 400)
    ax.hist(x, bins=35, density=True, histtype="step", color=MUTED, lw=1)
    comp = pi * np.exp(-(xs[:, None] - mu) ** 2 / (2 * var)) / np.sqrt(2 * np.pi * var)
    ax.fill_between(xs, comp[:, 0], color=BLUE, alpha=0.35, lw=0, label="component 1 × π₁")
    ax.fill_between(xs, comp[:, 1], color=ORANGE, alpha=0.35, lw=0, label="component 2 × π₂")
    ax.plot(xs, comp.sum(1), color=INK, lw=2.2, label="mixture")
    ax.set_yticks([]); ax.set_xlabel("x"); ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    ax.set_ylim(0, 0.42)
    ax.set_title("300 points, two-component fit", color=INK, loc="left", fontsize=12)
    ax = axes[1]
    ax.plot(range(1, len(ll) + 1), ll, "o-", color=BLUE, ms=3.5)
    ax.set_xlabel("EM iteration"); ax.set_ylabel("log-likelihood")
    ax.set_title("never decreases", color=INK, loc="left", fontsize=12)
    fig.tight_layout()
    fig.savefig(MML / "gmm.svg"); strip_doctype(MML / "gmm.svg")


def svm_figure():
    """Maximum-margin line for a small data set, and a circular boundary from a feature map (MML ch. 12)."""
    pos = np.array([[1, 1], [2, 3], [3, 1]]); neg = np.array([[-1, -1], [-2, -1], [-1, -3]])
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.2))
    ax = axes[0]; t = np.linspace(-4, 4, 2)
    ax.fill_between(t, -t - 2, -t + 2, color=BLUE, alpha=0.08, lw=0)
    ax.plot(t, -t, color=INK, lw=2, label="w·x + b = 0")
    for c in (-2, 2):
        ax.plot(t, -t + c, color=MUTED, lw=1.2, ls="--")
    ax.plot(*pos.T, "o", color=ORANGE, ms=8, label="y = +1")
    ax.plot(*neg.T, "s", color=BLUE, ms=8, label="y = −1")
    for p in ([1, 1], [-1, -1]):
        ax.plot(*p, "o", ms=17, mfc="none", mec=INK, mew=1.4)
    ax.annotate("", xy=(1, 1), xytext=(0, 0), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
    ax.text(0.15, 0.75, "√2", color=INK, fontsize=12)
    ax.set_aspect("equal"); ax.set_xlim(-3.5, 3.8); ax.set_ylim(-3.6, 3.6)
    ax.legend(frameon=False, fontsize=9.5, loc="lower left")
    ax.set_title("maximum margin; circled: support vectors", color=INK, loc="left", fontsize=12)
    ax = axes[1]; rng = np.random.default_rng(5)
    r = np.concatenate([rng.uniform(0, 1, 40), rng.uniform(1.6, 2.4, 60)])
    a = rng.uniform(0, 2 * np.pi, 100); P = np.column_stack([r * np.cos(a), r * np.sin(a)])
    ax.plot(*P[:40].T, "s", color=BLUE, ms=5); ax.plot(*P[40:].T, "o", color=ORANGE, ms=5)
    s = np.linspace(0, 2 * np.pi, 200); ax.plot(1.3 * np.cos(s), 1.3 * np.sin(s), color=INK, lw=2)
    ax.set_aspect("equal"); ax.set_xlim(-2.8, 2.8); ax.set_ylim(-2.8, 2.8)
    ax.set_title("linear in (x₁², x₂²) = a circle here", color=INK, loc="left", fontsize=12)
    fig.tight_layout()
    fig.savefig(MML / "svm.svg"); strip_doctype(MML / "svm.svg")


if __name__ == "__main__":
    grover_success()
    query_counts()
    for name in ("grover-success.svg", "query-counts.svg"):
        strip_doctype(OUT / name)
    classical_measurement()
    three_systems()
    for make in (unit_balls, low_rank, gradient_field, gaussian_conditional, convexity,
                 overfitting, bayes_regression, pca_figure, gmm_figure, svm_figure):
        make()
