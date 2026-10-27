"""Regenerate the two new figures of the quantum-algorithms course.

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


if __name__ == "__main__":
    grover_success()
    query_counts()
    for name in ("grover-success.svg", "query-counts.svg"):
        strip_doctype(OUT / name)
    classical_measurement()
