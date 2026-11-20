"""Extra figures for Chapter 3 (Measuring the Radio)."""
import math, os, sys
import numpy as np
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BASE = sys.argv[1] if len(sys.argv) > 1 else "telecom"
OUT = os.path.join(BASE, "ch3-measuring-the-radio", "figures")
os.makedirs(OUT, exist_ok=True)
INK, MUTED, LINE, ACC, ACC2, TEAL, SOFT, WARM, GOLD = "#1d2433", "#5c6370", "#e3e1da", "#3b5bdb", "#c2410c", "#0f766e", "#eef1fb", "#fdf1e8", "#fde68a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "svg.fonttype": "none", "figure.facecolor": "none", "axes.facecolor": "none", "legend.frameon": False,
    "axes.grid": True, "grid.color": LINE, "grid.linewidth": 0.7})
def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", transparent=True); plt.close(fig)
def title(ax, t): ax.set_title(t, color=INK, fontsize=12, loc="left")
def box(ax, x, y, w, h, text, fc=SOFT, ec=ACC, fs=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", facecolor=fc, edgecolor=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK)
def arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.3))
def lin(db): return 10 ** (np.asarray(db) / 10)
def db(x): return 10 * np.log10(x)

# 1. RSRP offset vs carrier bandwidth
def rsrp_offset():
    fig, ax = plt.subplots(figsize=(8.5, 4))
    for scs, nrb, col in [(15, {5: 25, 10: 52, 20: 106, 40: 216, 50: 270}, TEAL), (30, {10: 24, 20: 51, 40: 106, 50: 133, 60: 162, 80: 217, 100: 273}, ACC)]:
        bw = sorted(nrb); off = [db(12 * nrb[b]) for b in bw]
        ax.plot(bw, off, "o-", color=col, label=f"{scs} kHz SCS")
        for b, o in zip(bw, off):
            if b in (20, 100) or (scs == 15 and b == 50): ax.annotate(f"{o:.1f} dB", (b, o), textcoords="offset points", xytext=(4, -14), fontsize=9, color=col)
    ax.set_xlabel("carrier bandwidth (MHz)"); ax.set_ylabel("total power − RSRP (dB)")
    ax.legend(loc="lower right"); title(ax, "RSRP ≈ total power − 10·lg(12 × N_RB), if power is spread evenly")
    save(fig, "rsrp-offset.svg")

# 2. SINR between two cells, load dependency
def sinr_two_cells():
    x = np.linspace(0.05, 0.95, 300); isd = 500
    pl = lambda d: 13.54 + 39.08 * np.log10(np.maximum(d, 10)) + 20 * np.log10(3.5)
    rs1 = -5 - pl(x * isd) + 30 - 10; rs2 = -5 - pl((1 - x) * isd) + 30 - 10
    rs1 = 18 - pl(x * isd); rs2 = 18 - pl((1 - x) * isd)
    n = -174 + db(30e3) + 7
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.9))
    a1.plot(x * isd, rs1, color=ACC, label="RSRP cell A"); a1.plot(x * isd, rs2, color=ACC2, label="RSRP cell B")
    a1.axhline(n, color=MUTED, ls=":"); a1.text(10, n + 1.5, "noise per RE (NF 7 dB)", fontsize=9, color=MUTED)
    a1.set_xlabel("distance from site A (m)"); a1.set_ylabel("dBm per RE"); a1.legend(loc="upper center"); title(a1, "Two cells, 500 m apart")
    for load, col in [(1.0, ACC2), (0.5, GOLD), (0.2, TEAL)]:
        s = lin(rs1) / (load * lin(rs2) + lin(n)); a2.plot(x * isd, db(s), color=col if col != GOLD else "#b45309", label=f"neighbour load {int(load*100)} %")
    a2.set_xlabel("distance from site A (m)"); a2.set_ylabel("SINR (dB)"); a2.legend(); title(a2, "SINR of cell A: the neighbour's load decides")
    a2.set_ylim(-8, 45)
    fig.tight_layout(); save(fig, "sinr-two-cells.svg")

# 3. RSRQ vs SINR for several loads (simplified)
def rsrq_load():
    s = np.linspace(-10, 30, 300)
    fig, ax = plt.subplots(figsize=(8.5, 4))
    for rho, col in [(1.0, ACC2), (0.5, "#b45309"), (0.25, TEAL), (1 / 12, ACC)]:
        r = -db(12 * (rho + 1 / lin(s)))
        lab = "empty cell (reference REs only)" if rho < 0.1 else f"own cell {int(rho*100)} % loaded"
        ax.plot(s, r, color=col, label=lab)
    ax.set_xlabel("SINR (dB)"); ax.set_ylabel("RSRQ (dB)"); ax.legend(loc="lower right")
    title(ax, "Same SINR, different RSRQ: own-cell load lowers RSRQ (simplified model)")
    save(fig, "rsrq-load.svg")

# 4. DL vs UL SINR versus path loss
def ul_dl():
    pl = np.linspace(100, 160, 300); n_re = -174 + db(30e3)
    dl = 49 - db(273 * 12) + 18 + 0 - pl - (n_re + 7)       # 80 W, 273 PRB, gNB ant gain incl. in EIRP? simple
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.plot(pl, dl, color=ACC, lw=2, label="DL: 80 W over 273 PRB, UE NF 7 dB")
    for nprb, col in [(273, "#9ca3af"), (10, ACC2), (2, TEAL)]:
        ul = 23 - db(nprb * 12) + 18 - pl - (n_re + 3)
        ax.plot(pl, ul, color=col, lw=2, ls="--" if nprb == 273 else "-", label=f"UL: 23 dBm over {nprb} PRB, gNB NF 3 dB")
    ax.axhline(-5, color=MUTED, ls=":"); ax.text(101, -4, "≈ minimum usable SINR", fontsize=9, color=MUTED)
    ax.set_xlabel("path loss (dB)"); ax.set_ylabel("SINR per RE, no interference (dB)"); ax.set_ylim(-20, 60); ax.legend(loc="upper right", fontsize=9.5)
    title(ax, "The uplink runs out first, unless the UE concentrates its power in few PRBs")
    save(fig, "ul-dl-sinr.svg")

# 5. PUSCH power control with alpha
def alpha_pc():
    pl = np.linspace(70, 140, 300)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.9))
    for a, p0, col in [(1.0, -100, ACC), (0.8, -80, TEAL), (0.6, -60, ACC2)]:
        ptx = np.minimum(23, p0 + db(10) + a * pl)
        a1.plot(pl, ptx, color=col, label=f"α = {a}, P0 = {p0} dBm")
        a2.plot(pl, ptx - pl, color=col, label=f"α = {a}")
    a1.set_xlabel("path loss (dB)"); a1.set_ylabel("UE PUSCH power, 10 PRB (dBm)"); a1.legend(fontsize=9.5); title(a1, "Transmit power")
    a2.set_xlabel("path loss (dB)"); a2.set_ylabel("received power at gNB (dBm)"); a2.legend(fontsize=9.5); title(a2, "Received power: α < 1 lets near UEs arrive louder")
    fig.tight_layout(); save(fig, "alpha-pc.svg")

# 6. Link budget waterfall
def waterfall():
    items = [("UE power", 23), ("body loss", -3), ("gNB antenna", 18), ("sensitivity\n(10 PRB)", 108.4),
             ("shadow\nmargin", -7.7), ("O2I +\nindoor", -16.8), ("interf.\nmargin", -2)]
    fig, ax = plt.subplots(figsize=(10.5, 4.2)); cum = 0
    for i, (lab, v) in enumerate(items):
        col = TEAL if v > 0 else ACC2
        ax.bar(i, v, bottom=cum, color=col, width=0.6)
        ax.text(i, cum + v + (2 if v > 0 else -2), f"{v:+.1f}", ha="center", va="bottom" if v > 0 else "top", fontsize=9.5, color=INK)
        cum += v
    ax.bar(len(items), cum, color=ACC, width=0.6); ax.text(len(items), cum + 2, f"MAPL\n{cum:.1f} dB", ha="center", fontsize=10, color=INK)
    ax.set_xticks(range(len(items) + 1)); ax.set_xticklabels([l for l, _ in items] + ["result"], fontsize=9.5)
    ax.set_ylabel("dB"); ax.set_ylim(0, 165); ax.grid(axis="x", visible=False)
    title(ax, "Uplink link budget at 3.5 GHz, indoor UE: income in green, costs in orange")
    save(fig, "lb-waterfall.svg")

# 7. UMa NLOS path loss vs distance for 3 bands
def uma_bands():
    d = np.logspace(np.log10(30), np.log10(5000), 300)
    fig, ax = plt.subplots(figsize=(9, 4.2))
    for f, col, lab in [(0.7, TEAL, "700 MHz"), (3.5, ACC, "3.5 GHz"), (28, ACC2, "28 GHz")]:
        pl = 13.54 + 39.08 * np.log10(d) + 20 * np.log10(f) - 0.6 * (1.5 - 1.5)
        ax.plot(d, pl, color=col, label=lab)
        r = 10 ** ((130 - 13.54 - 20 * np.log10(f)) / 39.08)
        ax.plot([r], [130], "o", color=col); ax.annotate(f"{r:,.0f} m", (r, 130), textcoords="offset points", xytext=(5, 8), fontsize=9.5, color=col)
    ax.axhline(130, color=MUTED, ls=":"); ax.text(32, 131.5, "MAPL 130 dB", fontsize=9, color=MUTED)
    ax.set_xscale("log"); ax.set_xlabel("distance (m)"); ax.set_ylabel("path loss (dB)"); ax.legend(loc="lower right")
    title(ax, "TR 38.901 UMa NLOS: same budget, very different radius")
    save(fig, "uma-bands.svg")

# 8. O2I penetration vs frequency
def o2i():
    f = np.linspace(0.5, 40, 300)
    glass, irr, conc = 2 + 0.2 * f, 23 + 0.3 * f, 5 + 4 * f
    low = 5 - db(0.3 * lin(-glass) + 0.7 * lin(-conc))
    high = 5 - db(0.7 * lin(-irr) + 0.3 * lin(-conc))
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(f, low, color=TEAL, lw=2, label="low-loss building (standard glass)")
    ax.plot(f, high, color=ACC2, lw=2, label="high-loss building (IRR glass, concrete)")
    for x in (0.7, 3.5, 28):
        ax.axvline(x, color=LINE, lw=1)
        for y, c in [(np.interp(x, f, low), TEAL), (np.interp(x, f, high), ACC2)]:
            ax.plot(x, y, "o", color=c); ax.annotate(f"{y:.0f}", (x, y), textcoords="offset points", xytext=(5, -12), fontsize=9, color=c)
    ax.set_xlabel("frequency (GHz)"); ax.set_ylabel("through-wall loss (dB)"); ax.legend(loc="lower right")
    title(ax, "TR 38.901 outdoor-to-indoor loss (without the indoor part)")
    save(fig, "o2i-loss.svg")

# 9. L3 filtering
def l3():
    rng = np.random.default_rng(3); t = np.arange(0, 6, 0.04)
    true = -90 - 4 * t; raw = true + rng.normal(0, 4, t.size) + 3 * np.sin(2 * np.pi * 1.7 * t)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(t, raw, color="#9ca3af", lw=1, label="L1 samples")
    for k, col in [(4, ACC), (12, ACC2)]:
        a = 1 / 2 ** (k / 4); fl = np.empty_like(raw); fl[0] = raw[0]
        for i in range(1, raw.size): fl[i] = (1 - a) * fl[i - 1] + a * raw[i]
        ax.plot(t, fl, color=col, lw=2, label=f"L3 filtered, k = {k} (a = {a:.2f})")
    ax.set_xlabel("time (s), one sample per 40 ms"); ax.set_ylabel("RSRP (dBm)"); ax.legend(loc="upper right")
    title(ax, "Layer-3 filter: smoother, but later. Fₙ = (1−a)·Fₙ₋₁ + a·Mₙ, a = 1/2^(k/4)")
    save(fig, "l3-filter.svg")

# 10. Drive-test scatter RSRP vs SINR (illustrative)
def scatter():
    rng = np.random.default_rng(7); n = 900
    r = rng.uniform(-125, -65, n); s = 0.45 * (r + 125) - 6 + rng.normal(0, 4, n)
    k = rng.random(n) < 0.18; s[k] = rng.uniform(-8, 5, k.sum()); r[k] = rng.uniform(-95, -70, k.sum())
    fig, ax = plt.subplots(figsize=(9, 4.4))
    ax.scatter(r, s, s=7, color=ACC, alpha=0.45, edgecolors="none")
    ax.axvline(-105, color=MUTED, ls="--"); ax.axhline(3, color=MUTED, ls="--")
    for x, y, t, c in [(-123, 24, "weak but clean:\ncoverage-limited", TEAL), (-123, -7, "weak and noisy:\ncoverage hole", ACC2),
                       (-88, -7, "strong but dirty:\ninterference / overlap", ACC2), (-80, 24, "strong and clean", TEAL)]:
        ax.text(x, y, t, fontsize=9.5, color=c, bbox=dict(facecolor="white", edgecolor=LINE, boxstyle="round,pad=0.3"))
    ax.set_xlabel("SS-RSRP (dBm)"); ax.set_ylabel("SS-SINR (dB)"); ax.set_ylim(-10, 30)
    title(ax, "Drive-test scatter (illustrative): the quadrant names the problem")
    save(fig, "rsrp-sinr-scatter.svg")

# 11. Drive-test analysis flow
def dt_flow():
    fig, ax = plt.subplots(figsize=(11, 2.8)); ax.grid(False)
    steps = [("1 Check\nthe log\nGPS, UE,\nconfig", SOFT, ACC), ("2 Coverage\nRSRP map", SOFT, ACC), ("3 Quality\nSINR vs\nRSRP", SOFT, ACC),
             ("4 Dominance\nbest server,\noverlap", SOFT, ACC), ("5 Mobility\nevents,\nHO, RLF", WARM, ACC2), ("6 Throughput\nMCS, BLER,\nrank,\ngrants/s", WARM, ACC2), ("7 Root\ncause\n+ action", GOLD, "#b45309")]
    w, gap = 1.55, 0.3
    for i, (t, fc, ec) in enumerate(steps):
        x = i * (w + gap); box(ax, x, 0, w, 1.1, t, fc, ec, fs=9)
        if i: arrow(ax, x - gap, 0.55, x, 0.55)
    ax.set_xlim(-0.1, len(steps) * (w + gap)); ax.set_ylim(-0.2, 1.4); ax.axis("off")
    title(ax, "Reading a drive test: from the radio upward, one layer at a time")
    save(fig, "dt-flow.svg")

for fn in [rsrp_offset, sinr_two_cells, rsrq_load, ul_dl, alpha_pc, waterfall, uma_bands, o2i, l3, scatter, dt_flow]:
    fn()
print("ok")
